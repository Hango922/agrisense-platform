import hashlib
import hmac
import json
import time
from datetime import timedelta

from django.conf import settings
from django.core.management import call_command
from django.core.management.base import CommandError
from django.test import Client, TestCase, override_settings
from django.urls import reverse
from django.utils import timezone

from apps.accounts.models import User
from apps.cart_orders.models import CartItem, Order, PaymentEvent
from apps.cart_orders.payments import record_payment
from apps.cart_orders.services import cancel_order, create_direct_order
from apps.products.discovery import (
    PlannerForm,
    add_selection,
    budget_chat_reply,
    make_plan,
)
from apps.products.models import Category, ComboItem, Product, SeasonalCombo, Supplier
from apps.traceability.inventory import (
    available_products,
    available_stock,
    receive_batch,
)
from apps.traceability.models import ProductBatch


class UpgradeTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user('upgrade-user', password='test-password')
        cls.other = User.objects.create_user('other-user', password='test-password')
        cls.staff = User.objects.create_user('upgrade-staff', password='test-password', is_staff=True)
        cls.cat = Category.objects.create(name='Rau củ', slug='rau-cu')
        cls.supplier = Supplier.objects.create(name='Farm', address='Da Lat')
        cls.product = Product.objects.create(name='Cà chua', slug='tomato', price=35000, stock=10, category=cls.cat, supplier=cls.supplier)
        cls.second = Product.objects.create(name='Cà rốt', slug='carrot', price=25000, stock=10, category=cls.cat, supplier=cls.supplier)
        cls.address = {'full_name': 'Test User', 'phone': '0901234567', 'address': 'Ha Noi'}

    def batch(self, product=None, **overrides):
        product = product or self.product
        data = {'quantity': product.stock, 'batch_code': 'LOT-1', 'harvest_date': timezone.localdate(),
                'packaging_date': timezone.localdate(), 'expiry_date': timezone.localdate() + timedelta(days=5),
                'planting_location': 'Da Lat', 'existing_stock': True}
        data.update(overrides)
        return receive_batch(product, **data)

    def order(self, **kwargs):
        return create_direct_order(self.user, [{'product': self.product, 'quantity': 2}], self.address, **kwargs)

    def test_receive_initial_lot_preserves_stock(self):
        batch = self.batch()
        self.product.refresh_from_db()
        self.assertTrue(self.product.track_batches)
        self.assertEqual(self.product.stock, 10)
        self.assertEqual(batch.remaining_quantity, 10)
        self.assertTrue(batch.qr_code)

    def test_receive_additional_stock(self):
        self.batch()
        self.batch(existing_stock=False, quantity=4, batch_code='LOT-2')
        self.product.refresh_from_db()
        self.assertEqual(self.product.stock, 14)
        self.assertEqual(available_stock(self.product), 14)

    def test_batch_enrollment_waits_for_pending_legacy_orders(self):
        order = self.order()
        self.product.refresh_from_db()
        with self.assertRaises(ValueError):
            self.batch()
        cancel_order(order)
        self.product.refresh_from_db()
        self.assertEqual(self.batch().remaining_quantity, 10)

    def test_invalid_receipts_do_not_change_stock(self):
        for data in [{'quantity': 9}, {'existing_stock': False}, {'quantity': 0},
                     {'expiry_date': timezone.localdate() - timedelta(days=1)},
                     {'harvest_date': timezone.localdate() + timedelta(days=1)}]:
            with self.subTest(data=data), self.assertRaises(ValueError):
                self.batch(**data)
        self.assertEqual(ProductBatch.objects.count(), 0)

    def test_fefo_split_and_restore_exact_lots(self):
        later = self.batch()
        earlier = self.batch(existing_stock=False, quantity=1, batch_code='EARLY', expiry_date=timezone.localdate())
        order = self.order()
        allocations = list(order.items.get().allocations.order_by('pk'))
        self.assertEqual([(a.batch_id, a.quantity) for a in allocations], [(earlier.pk, 1), (later.pk, 1)])
        cancel_order(order)
        earlier.refresh_from_db()
        later.refresh_from_db()
        self.assertEqual((earlier.remaining_quantity, later.remaining_quantity), (1, 10))
        with self.assertRaises(ValueError):
            cancel_order(order)

    def test_expired_lots_block_all_order_channels(self):
        batch = self.batch()
        ProductBatch.objects.filter(pk=batch.pk).update(expiry_date=timezone.localdate() - timedelta(days=1))
        with self.assertRaises(ValueError):
            self.order()
        self.product.refresh_from_db()
        self.assertEqual(self.product.stock, 10)
        self.assertEqual(available_stock(self.product), 0)
        self.assertNotIn(self.product, available_products())
        self.assertFalse(Order.objects.exists())
        self.client.force_login(self.user)
        self.client.post(reverse('cart_orders:add', args=[self.product.pk]), {'quantity': 1})
        self.assertFalse(CartItem.objects.exists())

    def test_atomic_rollback_for_multiline_lot_shortage(self):
        self.batch()
        ProductBatch.objects.update(remaining_quantity=1)
        with self.assertRaises(ValueError):
            create_direct_order(self.user, [{'product': self.second, 'quantity': 1}, {'product': self.product, 'quantity': 2}], self.address)
        self.second.refresh_from_db()
        self.assertEqual(self.second.stock, 10)
        self.assertFalse(Order.objects.exists())

    def test_order_displays_allocated_lot_not_latest_catalog_lot(self):
        batch = self.batch()
        order = self.order()
        self.batch(existing_stock=False, quantity=1, batch_code='UNUSED-LOT')
        self.client.force_login(self.user)
        response = self.client.get(reverse('cart_orders:order_detail', args=[order.order_code]))
        self.assertContains(response, batch.batch_code)
        self.assertNotContains(response, 'UNUSED-LOT')

    def test_cancellation_after_expiry_does_not_reenable_sales(self):
        batch = self.batch()
        order = self.order()
        ProductBatch.objects.filter(pk=batch.pk).update(expiry_date=timezone.localdate() - timedelta(days=1))
        cancel_order(order)
        self.product.refresh_from_db()
        self.assertEqual(available_stock(self.product), 0)

    def test_planner_parses_vietnamese_budget_people_days(self):
        form = PlannerForm({'wish': '300k mua rau củ cho 2 người trong 3 ngày', 'budget': 100000, 'people': 1, 'days': 1})
        self.assertTrue(form.is_valid(), form.errors)
        self.assertEqual((form.cleaned_data['budget'], form.cleaned_data['people'], form.cleaned_data['days']), (300000, 2, 3))
        for text in ['300.000đ', '300,000 VND', '0,3 triệu']:
            form = PlannerForm({'wish': text, 'budget': 100000, 'people': 1, 'days': 1})
            self.assertTrue(form.is_valid(), form.errors)
            self.assertEqual(form.cleaned_data['budget'], 300000)

    def test_planner_rejects_invalid_limits(self):
        for text in ['9 triệu cho 2 người', '300k cho 0 người', '300k cho 15 ngày']:
            form = PlannerForm({'wish': text, 'budget': 300000, 'people': 2, 'days': 3})
            self.assertFalse(form.is_valid())

    def test_plan_respects_budget_stock_and_expiry(self):
        batch = self.batch()
        ProductBatch.objects.filter(pk=batch.pk).update(expiry_date=timezone.localdate() - timedelta(days=1))
        plan = make_plan(100000, 2, 3)
        self.assertLessEqual(plan['grand_total'], 100000)
        self.assertNotIn(self.product.pk, [r['product'].pk for r in plan['rows']])
        self.assertTrue(all(r['quantity'] <= available_stock(r['product']) for r in plan['rows']))
        self.assertFalse(make_plan(30000, 2, 3)['rows'])

    def test_fruit_preference_does_not_select_vegetables(self):
        self.assertFalse(make_plan(300000, 2, 3, 'fruit')['rows'])

    def test_budget_chat_returns_preview_without_order(self):
        reply = budget_chat_reply('300k mua rau củ cho 2 người trong 3 ngày')
        assert reply is not None
        self.assertIn('/products/planner/', reply)
        self.assertFalse(Order.objects.exists())
        self.assertIsNone(budget_chat_reply('mua 2kg cà chua'))

    def plan_token(self):
        self.client.force_login(self.user)
        response = self.client.post(reverse('products:planner'), {'budget': 300000, 'people': 2, 'days': 3})
        return response.context['basket_token']

    def test_plan_edit_and_replay_protection(self):
        token = self.plan_token()
        payload = {'basket_token': token, f'quantity_{self.product.pk}': 2}
        self.assertEqual(self.client.post(reverse('products:add_plan'), payload).status_code, 302)
        self.assertEqual(CartItem.objects.get(product=self.product).quantity, 2)
        self.assertEqual(self.client.post(reverse('products:add_plan'), payload).status_code, 400)
        self.assertEqual(CartItem.objects.get(product=self.product).quantity, 2)

    def test_plan_revalidates_price_budget_and_quantity(self):
        for qty in ['100', '-1', 'NaN']:
            token = self.plan_token()
            self.client.post(reverse('products:add_plan'), {'basket_token': token, f'quantity_{self.product.pk}': qty})
            self.assertFalse(CartItem.objects.exists())
        token = self.plan_token()
        Product.objects.filter(pk=self.product.pk).update(price=40000)
        self.client.post(reverse('products:add_plan'), {'basket_token': token, f'quantity_{self.product.pk}': 1})
        self.assertFalse(CartItem.objects.exists())

    def test_plan_tampered_and_cross_session_tokens(self):
        token = self.plan_token()
        self.assertEqual(self.client.post(reverse('products:add_plan'), {'basket_token': token + 'x'}).status_code, 400)
        other = Client()
        other.force_login(self.other)
        self.assertEqual(other.post(reverse('products:add_plan'), {'basket_token': token}).status_code, 400)

    def test_add_selection_is_atomic_and_preserves_existing_cart(self):
        add_selection(self.user, {self.product.pk: 2})
        with self.assertRaises(ValueError):
            add_selection(self.user, {self.product.pk: 1, self.second.pk: 100})
        self.assertEqual(CartItem.objects.get(product=self.product).quantity, 2)
        self.assertEqual(CartItem.objects.count(), 1)

    def test_combo_and_reorder_use_current_prices_and_owner(self):
        combo = SeasonalCombo.objects.create(name='Combo', slug='combo')
        ComboItem.objects.create(combo=combo, product=self.product, quantity=1)
        self.client.force_login(self.user)
        self.assertContains(self.client.get(reverse('products:combos')), 'Combo')
        self.client.post(reverse('products:add_combo', args=[combo.slug]))
        order = self.order()
        Product.objects.filter(pk=self.product.pk).update(price=40000)
        self.client.post(reverse('cart_orders:reorder', args=[order.order_code]))
        item = CartItem.objects.select_related('product').get(product=self.product)
        self.assertEqual(item.quantity, 3)
        self.assertEqual(item.subtotal(), 120000)
        self.client.force_login(self.other)
        self.assertEqual(self.client.post(reverse('cart_orders:reorder', args=[order.order_code])).status_code, 404)

    def test_public_and_staff_pages_render(self):
        for name in ['home', 'products:planner', 'products:combos', 'products:list']:
            self.assertEqual(self.client.get(reverse(name)).status_code, 200)
        self.client.force_login(self.user)
        self.assertEqual(self.client.get(reverse('dashboard:operations')).status_code, 302)
        self.client.force_login(self.staff)
        self.assertContains(self.client.get(reverse('dashboard:operations')), 'Ưu tiên đúng')
        self.assertContains(self.client.get(reverse('dashboard:receive')), 'Ghi nhận lô nông sản')

    def test_staff_can_receive_and_sees_validation_errors(self):
        self.client.force_login(self.staff)
        data = {'product': self.product.pk, 'batch_code': 'NEW-LOT', 'quantity': 10, 'existing_stock': 'on',
                'planting_location': 'Da Lat', 'harvest_date': str(timezone.localdate()),
                'packaging_date': str(timezone.localdate()), 'expiry_date': str(timezone.localdate() + timedelta(days=3))}
        self.assertEqual(self.client.post(reverse('dashboard:receive'), data).status_code, 302)
        self.assertEqual(self.client.post(reverse('dashboard:receive'), data).status_code, 400)
        self.assertContains(self.client.get(reverse('dashboard:operations')), 'NEW-LOT')

    def test_demo_seed_refuses_normal_database(self):
        with self.assertRaises(CommandError):
            call_command('seed_showcase')

    def notification(self, order, **overrides):
        data = {'order_code': order.order_code, 'transaction_id': 'tx-1', 'amount': str(order.final_amount), 'currency': 'VND'}
        data.update(overrides)
        body = json.dumps(data).encode()
        timestamp = str(int(time.time()))
        signature = hmac.new(settings.PAYMENT_WEBHOOK_SECRET.encode(), timestamp.encode() + b'.' + body, hashlib.sha256).hexdigest()
        return self.client.post(reverse('cart_orders:payment_webhook'), body, content_type='application/json',
                                HTTP_X_PAYMENT_TIMESTAMP=timestamp, HTTP_X_PAYMENT_SIGNATURE=signature)

    @override_settings(PAYMENT_WEBHOOK_SECRET='test-only-webhook-key-at-least-32-characters')
    def test_signed_payment_confirms_once(self):
        order = self.order(payment_method='vietqr')
        self.assertEqual(self.notification(order).status_code, 200)
        self.assertEqual(self.notification(order).status_code, 200)
        order.refresh_from_db()
        self.assertEqual((order.status, order.payment_status), ('confirmed', 'paid'))
        self.assertEqual(PaymentEvent.objects.count(), 1)
        self.assertIsNotNone(order.paid_at)

    @override_settings(PAYMENT_WEBHOOK_SECRET='test-only-webhook-key-at-least-32-characters')
    def test_payment_rejects_wrong_amount_currency_and_nonfinite(self):
        order = self.order(payment_method='vietqr')
        for overrides in [{'amount': '1'}, {'amount': 'NaN'}, {'amount': 'Infinity'}, {'amount': '-1'},
                          {'currency': 'USD'}, {'transaction_id': ''}, {'amount': '100000.5'}]:
            self.assertEqual(self.notification(order, **overrides).status_code, 400)
        self.assertFalse(PaymentEvent.objects.exists())
        order.refresh_from_db()
        self.assertEqual(order.status, 'pending')

    @override_settings(PAYMENT_WEBHOOK_SECRET='test-only-webhook-key-at-least-32-characters')
    def test_payment_rejects_invalid_auth_and_stale_timestamp(self):
        for timestamp in [str(int(time.time())), '1', 'bad']:
            self.assertEqual(self.client.post(reverse('cart_orders:payment_webhook'), '{}', content_type='application/json',
                             HTTP_X_PAYMENT_TIMESTAMP=timestamp, HTTP_X_PAYMENT_SIGNATURE='bad').status_code, 403)

    @override_settings(PAYMENT_WEBHOOK_SECRET='')
    def test_unconfigured_gateway_is_disabled(self):
        self.assertEqual(self.client.post(reverse('cart_orders:payment_webhook'), '{}', content_type='application/json').status_code, 503)

    @override_settings(PAYMENT_WEBHOOK_SECRET='test-only-webhook-key-at-least-32-characters')
    def test_payment_cannot_pay_cancelled_or_cod_order(self):
        order = self.order(payment_method='vietqr')
        cancel_order(order)
        self.assertEqual(self.notification(order).status_code, 400)
        self.assertEqual(self.notification(self.order()).status_code, 400)

    @override_settings(PAYMENT_WEBHOOK_SECRET='test-only-webhook-key-at-least-32-characters')
    def test_transaction_id_cannot_pay_two_orders(self):
        order = self.order(payment_method='vietqr')
        self.assertEqual(self.notification(order).status_code, 200)
        other = self.order(payment_method='vietqr')
        self.assertEqual(self.notification(other).status_code, 400)
        other.refresh_from_db()
        self.assertEqual(other.payment_status, 'unpaid')

    @override_settings(DEMO_MODE=True, DEBUG=True)
    def test_demo_payment_is_separate_and_has_no_bank_qr(self):
        order = self.order(payment_method='vietqr')
        self.assertTrue(order.is_demo)
        self.client.force_login(self.user)
        response = self.client.get(reverse('cart_orders:order_detail', args=[order.order_code]))
        self.assertContains(response, 'Mô phỏng thanh toán thành công')
        self.assertNotContains(response, 'img.vietqr.io')
        self.assertEqual(self.client.post(reverse('cart_orders:demo_payment', args=[order.order_code])).status_code, 302)
        order.refresh_from_db()
        self.assertEqual(order.payment_status, 'demo_paid')
        with self.assertRaises(ValueError):
            record_payment(order.order_code, 'real-id', order.final_amount)

    def test_demo_route_disabled_in_normal_environment(self):
        order = self.order(payment_method='vietqr')
        self.client.force_login(self.user)
        self.assertEqual(self.client.post(reverse('cart_orders:demo_payment', args=[order.order_code])).status_code, 403)

    def test_cod_order_does_not_show_transfer_qr(self):
        order = self.order()
        self.client.force_login(self.user)
        self.assertNotContains(self.client.get(reverse('cart_orders:order_detail', args=[order.order_code])), 'img.vietqr.io')

    def test_write_endpoints_require_post_and_csrf(self):
        self.client.force_login(self.user)
        self.assertEqual(self.client.get(reverse('products:add_plan')).status_code, 405)
        client = Client(enforce_csrf_checks=True)
        client.force_login(self.user)
        self.assertEqual(client.post(reverse('products:add_plan')).status_code, 403)

    def test_unmanaged_legacy_products_can_still_be_ordered(self):
        order = self.order()
        self.assertFalse(order.items.get().allocations.exists())
        cancel_order(order)
        self.product.refresh_from_db()
        self.assertEqual(self.product.stock, 10)
