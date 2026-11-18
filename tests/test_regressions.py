import json
from datetime import date

from django.test import Client, TestCase

from apps.accounts.models import User
from apps.cart_orders.models import CartItem, Order
from apps.cart_orders.services import cancel_order, create_direct_order
from apps.products.models import Category, Product, Supplier
from apps.traceability.models import ProductBatch


class WorkflowRegressionTests(TestCase):
    def test_existing_multiple_chat_sessions_do_not_break_send(self):
        from apps.chatbot.models import ChatSession
        ChatSession.objects.create(user=self.user, session_key='old-one')
        ChatSession.objects.create(user=self.user, session_key='old-two')
        response = self.client.post('/chatbot/send/', json.dumps({'message': 'hello'}), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.json()['reply'])

    def test_recommendations_fill_shortage_and_include_cancelled_purchase(self):
        from apps.behavior.models import UserEvent
        from apps.recommendation.engine import recommend_for_user
        order = self.order()
        cancel_order(order)
        UserEvent.objects.create(user=self.user, event_type='view', category=self.product.category)
        other_category = Category.objects.create(name='Other', slug='other')
        other_product = Product.objects.create(name='Other', slug='other', category=other_category,
            supplier=self.product.supplier, price=10000, stock=2)
        results = recommend_for_user(self.user, limit=2)
        self.assertCountEqual([item['product'].pk for item in results], [self.product.pk, other_product.pk])

    def setUp(self):
        self.user = User.objects.create_user(username='owner', password='Password123!')
        self.other = User.objects.create_user(username='other', password='Password123!')
        self.staff = User.objects.create_user(username='staff', is_staff=True)
        category = Category.objects.create(name='Test', slug='test')
        supplier = Supplier.objects.create(name='Test', address='Test')
        self.product = Product.objects.create(name='Test', slug='test', category=category,
                                              supplier=supplier, price=10000, stock=5)
        self.address = {'full_name': 'Private Name', 'phone': '0901234567', 'address': 'Private Address'}
        self.client.force_login(self.user)

    def order(self):
        return create_direct_order(self.user, [{'product': self.product, 'quantity': 2}], self.address)

    def test_stale_stock_cannot_oversell(self):
        stale = Product.objects.get(pk=self.product.pk)
        self.order()
        with self.assertRaises(ValueError):
            create_direct_order(self.user, [{'product': stale, 'quantity': 4}], self.address)
        self.product.refresh_from_db()
        self.assertEqual(self.product.stock, 3)

    def test_stale_cancel_does_not_restore_twice(self):
        order = self.order()
        stale = Order.objects.get(pk=order.pk)
        cancel_order(order)
        with self.assertRaises(ValueError):
            cancel_order(stale)
        self.product.refresh_from_db()
        self.assertEqual(self.product.stock, 5)

    def test_chat_order_is_private(self):
        order = self.order()
        for user in (None, self.other):
            client = Client()
            if user:
                client.force_login(user)
            response = client.post('/chatbot/send/', json.dumps({'message': 'don hang ' + order.order_code}), content_type='application/json')
            self.assertNotIn('Private Address', response.json()['reply'])

    def test_chat_requires_csrf(self):
        client = Client(enforce_csrf_checks=True)
        client.force_login(self.user)
        self.assertEqual(client.post('/chatbot/clear/').status_code, 403)

    def test_invalid_quantity_and_checkout_are_rejected(self):
        for quantity in ('abc', '0', '-1'):
            self.assertEqual(self.client.post(f'/cart/add/{self.product.pk}/', {'quantity': quantity}).status_code, 400)
        self.assertEqual(self.client.post('/cart/checkout/', {}).status_code, 400)
        self.assertFalse(Order.objects.exists())

    def test_invalid_product_input_is_rejected(self):
        self.assertEqual(self.client.get('/products/?min_price=abc').status_code, 400)
        self.assertEqual(self.client.post('/products/test/review/', {'rating': 99}).status_code, 400)

    def test_cancelled_order_cannot_reopen(self):
        order = self.order()
        cancel_order(order)
        self.client.force_login(self.staff)
        self.client.post(f'/dashboard/orders/{order.pk}/update-status/', {'status': 'confirmed'})
        order.refresh_from_db()
        self.assertEqual(order.status, 'cancelled')

    def test_unknown_status_is_rejected(self):
        order = self.order()
        self.client.force_login(self.staff)
        self.client.post(f'/dashboard/orders/{order.pk}/update-status/', {'status': 'garbage'})
        order.refresh_from_db()
        self.assertEqual(order.status, 'pending')

    def test_renamed_batch_regenerates_qr(self):
        batch = ProductBatch.objects.create(product=self.product, batch_code='OLD', planting_location='Test', harvest_date=date.today(), packaging_date=date.today())
        old_name = batch.qr_code.name
        batch.batch_code = 'NEW'
        batch.save()
        self.assertNotEqual(batch.qr_code.name, old_name)

    def test_excel_untrusted_text_is_not_a_formula(self):
        import io

        import openpyxl
        order = self.order()
        order.full_name = '=1+1'
        order.save()
        self.client.force_login(self.staff)
        response = self.client.get('/dashboard/orders/export-excel/')
        sheet = openpyxl.load_workbook(io.BytesIO(response.content)).active
        self.assertEqual(sheet['D2'].data_type, 's')

    def test_bill_rejects_non_image(self):
        from django.core.files.uploadedfile import SimpleUploadedFile
        order = self.order()
        order.payment_method = 'vietqr'
        order.save()
        self.client.post(f'/orders/{order.order_code}/upload-proof/', {
            'payment_proof': SimpleUploadedFile('bill.txt', b'not an image')})
        order.refresh_from_db()
        self.assertFalse(order.payment_proof)

    def test_bank_proof_is_private(self):
        from django.core.files.base import ContentFile
        order = self.order()
        order.payment_proof.save('private.png', ContentFile(b'private'), save=True)
        self.assertEqual(Client().get(order.payment_proof.url).status_code, 302)
        client = Client()
        client.force_login(self.other)
        self.assertEqual(client.get(order.payment_proof.url).status_code, 404)
        response = self.client.get(order.payment_proof.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(b''.join(response.streaming_content), b'private')

    def test_ai_timeout_does_not_try_six_models(self):
        from unittest.mock import patch

        from requests.exceptions import Timeout

        from apps.chatbot.services import call_ai
        with self.settings(AI_PROVIDER='gemini', GEMINI_API_KEY='test-key'):
            with patch('apps.chatbot.services.requests.post', side_effect=Timeout) as request:
                self.assertTrue(call_ai('hello', product_context='test')[1])
                self.assertEqual(request.call_count, 1)

    def test_duplicate_chat_request_creates_one_exchange(self):
        from apps.chatbot.models import ChatMessage
        data = json.dumps({'message': 'xin chao', 'request_id': 'request-123'})
        first = self.client.post('/chatbot/send/', data, content_type='application/json')
        second = self.client.post('/chatbot/send/', data, content_type='application/json')
        self.assertEqual(first.json(), second.json())
        self.assertEqual(ChatMessage.objects.count(), 2)

    def test_request_id_cannot_be_reused_for_other_message(self):
        payload = {'message': 'xin chao', 'request_id': 'unique'}
        self.client.post('/chatbot/send/', json.dumps(payload), content_type='application/json')
        payload['message'] = 'khac'
        self.assertEqual(self.client.post('/chatbot/send/', json.dumps(payload), content_type='application/json').status_code, 409)

    def test_invalid_chat_payload(self):
        for payload in ('bad', '[]', 'null', '{"message": 5}', '{"message": ""}', json.dumps({'message': 'a' * 4001}), '{"message":"hi","request_id":5}'):
            self.assertEqual(self.client.post('/chatbot/send/', payload, content_type='application/json').status_code, 400)

    def test_real_csrf_chat_and_clear(self):
        client = Client(enforce_csrf_checks=True)
        client.force_login(self.user)
        client.get('/')
        token = client.cookies['csrftoken'].value
        self.assertEqual(client.post('/chatbot/send/', json.dumps({'message': 'hello'}), content_type='application/json', HTTP_X_CSRFTOKEN=token).status_code, 200)
        self.assertEqual(client.get('/chatbot/messages/').status_code, 200)
        self.assertEqual(client.post('/chatbot/clear/', HTTP_X_CSRFTOKEN=token).status_code, 200)
        self.assertEqual(client.get('/chatbot/messages/').json()['messages'], [])

    def test_cart_checkout_and_repeat(self):
        self.client.post(f'/cart/add/{self.product.pk}/', {'quantity': 1})
        item = CartItem.objects.get()
        self.assertEqual(self.client.post(f'/cart/update/{item.pk}/', {'quantity': 'abc'}).status_code, 400)
        self.client.post(f'/cart/update/{item.pk}/', {'quantity': 2})
        data = {**self.address, 'payment_method': 'cod'}
        self.assertEqual(self.client.post('/cart/checkout/', data).status_code, 302)
        self.client.post('/cart/checkout/', data)
        self.assertEqual(Order.objects.count(), 1)
        self.assertFalse(CartItem.objects.exists())
        from apps.behavior.models import UserEvent
        self.assertEqual(UserEvent.objects.filter(event_type='purchase').count(), 1)

    def test_cart_boundaries_and_removal(self):
        url = f'/cart/add/{self.product.pk}/'
        self.client.post(url, {'quantity': 6})
        self.assertFalse(CartItem.objects.exists())
        self.client.post(url, {'quantity': 3})
        self.client.post(url, {'quantity': 3})
        item = CartItem.objects.get()
        self.assertEqual(item.quantity, 3)
        self.client.post(f'/cart/update/{item.pk}/', {'quantity': 9})
        item.refresh_from_db()
        self.assertEqual(item.quantity, 3)
        self.client.post(f'/cart/update/{item.pk}/', {'quantity': 0})
        self.assertFalse(CartItem.objects.exists())
        self.client.post(url, {'quantity': 1})
        self.client.post(f'/cart/remove/{CartItem.objects.get().pk}/')
        self.assertFalse(CartItem.objects.exists())

    def test_purchase_validation_rolls_back(self):
        for quantity in (0, -1, True, 1.5):
            with self.assertRaises(ValueError):
                create_direct_order(self.user, [{'product': self.product, 'quantity': quantity}], self.address)
        self.product.is_active = False
        self.product.save()
        with self.assertRaises(ValueError):
            self.order()
        self.assertFalse(Order.objects.exists())

    def test_duplicate_product_lines_check_combined_stock(self):
        with self.assertRaises(ValueError):
            create_direct_order(self.user, [{'product': self.product, 'quantity': 3}] * 2, self.address)
        self.assertFalse(Order.objects.exists())

    def test_customer_cannot_access_other_orders(self):
        order = self.order()
        self.client.force_login(self.other)
        self.assertEqual(self.client.get(f'/orders/{order.order_code}/').status_code, 404)
        self.assertEqual(self.client.post(f'/orders/{order.order_code}/cancel/').status_code, 404)
        self.assertEqual(self.client.post(f'/orders/{order.order_code}/upload-proof/').status_code, 404)

    def test_customer_cancel_and_no_second_refund(self):
        order = self.order()
        for _ in range(2):
            self.client.post(f'/orders/{order.order_code}/cancel/')
        self.product.refresh_from_db()
        self.assertEqual(self.product.stock, 5)

    def test_bill_validation_and_state(self):
        from tests.image_fixtures import png_upload
        order = self.order()
        self.client.post(f'/orders/{order.order_code}/upload-proof/', {'payment_proof': png_upload()})
        order.refresh_from_db()
        self.assertFalse(order.payment_proof)
        order.payment_method = 'vietqr'
        order.save()
        upload = png_upload()
        upload.size = 6 * 1024 * 1024
        from apps.cart_orders.forms import PaymentProofForm
        self.assertFalse(PaymentProofForm(files={'payment_proof': upload}).is_valid())
        self.client.post(f'/orders/{order.order_code}/upload-proof/', {})
        order.refresh_from_db()
        self.assertFalse(order.payment_proof)

    def test_dashboard_rejects_invalid_proof_and_skipped_status(self):
        from django.core.files.uploadedfile import SimpleUploadedFile
        order = self.order()
        self.client.force_login(self.staff)
        url = f'/dashboard/orders/{order.pk}/update-status/'
        for data in ({'status': 'delivered'}, {'status': 'confirmed', 'payment_proof': SimpleUploadedFile('bad.txt', b'bad')}, {}):
            self.client.post(url, data)
            order.refresh_from_db()
            self.assertEqual(order.status, 'pending')

    def test_admin_cannot_edit_state_or_delete_order(self):
        from django.contrib.admin.sites import site
        from django.test import RequestFactory
        request = RequestFactory().get('/')
        request.user = self.staff
        model_admin = site._registry[Order]
        self.assertIn('status', model_admin.get_readonly_fields(request))
        self.assertFalse(model_admin.has_delete_permission(request, self.order()))
        self.assertFalse(model_admin.has_add_permission(request))
