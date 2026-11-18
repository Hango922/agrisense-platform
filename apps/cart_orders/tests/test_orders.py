# File: apps/cart_orders/tests/test_orders.py
"""
Kiểm thử chức năng đặt hàng, kiểm tra tồn kho và hủy đơn hàng.
"""
from decimal import Decimal

from django.test import TestCase

from apps.accounts.models import User
from apps.cart_orders.models import Cart, CartItem
from apps.cart_orders.services import (
    calculate_shipping_fee,
    cancel_order,
    create_order_from_cart,
)
from apps.products.models import Category, Product, Supplier
from tests.image_fixtures import png_upload


class OrderTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='u', password='p')
        self.cat = Category.objects.create(name='Test', slug='test')
        self.sup = Supplier.objects.create(name='S', address='A')
        self.product = Product.objects.create(
            name='P1', slug='p1', category=self.cat, supplier=self.sup,
            price=Decimal(50000), stock=10, unit='kg',
        )
        self.cart = Cart.objects.create(user=self.user)
        CartItem.objects.create(cart=self.cart, product=self.product, quantity=2)

    def test_create_order_success(self):
        order = create_order_from_cart(self.user, self.cart, {
            'full_name': 'Test', 'phone': '0900', 'address': 'HN',
        })
        self.assertEqual(order.items.count(), 1)
        self.product.refresh_from_db()
        self.assertEqual(self.product.stock, 8)

    def test_create_order_exceed_stock(self):
        CartItem.objects.filter(cart=self.cart).update(quantity=100)
        with self.assertRaises(ValueError):
            create_order_from_cart(self.user, self.cart, {
                'full_name': 'Test', 'phone': '0900', 'address': 'HN',
            })

    def test_cancel_order_returns_stock(self):
        order = create_order_from_cart(self.user, self.cart, {
            'full_name': 'Test', 'phone': '0900', 'address': 'HN',
        })
        cancel_order(order)
        self.product.refresh_from_db()
        self.assertEqual(self.product.stock, 10)

    def test_shipping_fee_calculation(self):
        # Đơn dưới 500k -> phí 30k
        self.assertEqual(calculate_shipping_fee(Decimal(200000)), 30000)
        # Đơn từ 500k trở lên -> miễn phí ship
        self.assertEqual(calculate_shipping_fee(Decimal(500000)), 0)
        self.assertEqual(calculate_shipping_fee(Decimal(600000)), 0)

    def test_cancel_non_pending_order_fails(self):
        order = create_order_from_cart(self.user, self.cart, {
            'full_name': 'Test', 'phone': '0900', 'address': 'HN',
        })
        order.status = 'shipping'
        order.save()
        with self.assertRaises(ValueError):
            cancel_order(order)

    def test_vietqr_generation(self):
        from apps.cart_orders.vietqr import get_vietqr_info, get_vietqr_url
        order = create_order_from_cart(self.user, self.cart, {
            'full_name': 'Test', 'phone': '0900', 'address': 'HN',
        })
        url = get_vietqr_url(order)
        self.assertIn('https://img.vietqr.io/image/', url)
        self.assertIn(str(int(order.final_amount)), url)
        self.assertIn(order.order_code, url)

        info = get_vietqr_info(order)
        self.assertEqual(info['transfer_content'], order.order_code)
        self.assertEqual(info['memo'], order.order_code)
        self.assertEqual(info['amount'], int(order.final_amount))
        self.assertIn(info['bank_id'], ['TCB', 'MB'])

    def test_order_detail_view_includes_vietqr(self):
        order = create_order_from_cart(self.user, self.cart, {
            'full_name': 'Test', 'phone': '0900', 'address': 'HN',
        })
        self.client.force_login(self.user)
        response = self.client.get(f'/orders/{order.order_code}/')
        self.assertEqual(response.status_code, 200)
        self.assertIn('vietqr', response.context)
        self.assertIn('qr_image_url', response.context['vietqr'])
        self.assertContains(response, 'Thanh Toán Nhanh VietQR')

    def test_vietqr_order_requires_payment_proof_to_confirm(self):
        from django.core.exceptions import ValidationError
        order = create_order_from_cart(self.user, self.cart, {
            'full_name': 'Khách VietQR', 'phone': '0900111222', 'address': 'HN',
        }, payment_method='vietqr')
        self.assertEqual(order.payment_method, 'vietqr')
        self.assertFalse(order.can_be_confirmed())

        # Thử đổi trạng thái sang confirmed mà không có bill -> phải văng ValidationError
        order.status = 'confirmed'
        with self.assertRaises(ValidationError):
            order.clean()
        with self.assertRaises(ValidationError):
            order.save()

    def test_upload_payment_proof_and_confirm_success(self):
        order = create_order_from_cart(self.user, self.cart, {
            'full_name': 'Khách VietQR', 'phone': '0900111222', 'address': 'HN',
        }, payment_method='vietqr')

        # Upload bill chuyển khoản
        self.client.force_login(self.user)
        fake_bill = png_upload("bill.png")
        response = self.client.post(
            f'/orders/{order.order_code}/upload-proof/',
            {'payment_proof': fake_bill},
            follow=True
        )
        self.assertEqual(response.status_code, 200)

        order.refresh_from_db()
        self.assertTrue(bool(order.payment_proof))
        self.assertIsNotNone(order.payment_proof_uploaded_at)
        self.assertTrue(order.can_be_confirmed())

        # Admin có thể xác nhận đơn hàng sau khi có bill
        order.status = 'confirmed'
        order.clean()
        order.save()
        self.assertEqual(order.status, 'confirmed')

        # Dọn dẹp file test
        if order.payment_proof:
            order.payment_proof.delete(save=False)

    def test_cod_order_can_be_confirmed_without_proof(self):
        order = create_order_from_cart(self.user, self.cart, {
            'full_name': 'Khách COD', 'phone': '0900333444', 'address': 'HN',
        }, payment_method='cod')
        self.assertEqual(order.payment_method, 'cod')
        self.assertTrue(order.can_be_confirmed())
        order.status = 'confirmed'
        order.clean()
        order.save()
        self.assertEqual(order.status, 'confirmed')

    def test_django_admin_order_changelist_and_display(self):
        # Tạo đơn COD và đơn VietQR chưa có bill
        order_cod = create_order_from_cart(self.user, self.cart, {
            'full_name': 'Khách COD Admin', 'phone': '0900333444', 'address': 'HN',
        }, payment_method='cod')

        CartItem.objects.create(cart=self.cart, product=self.product, quantity=1)
        order_vietqr = create_order_from_cart(self.user, self.cart, {
            'full_name': 'Khách VietQR Admin', 'phone': '0900555666', 'address': 'HCM',
        }, payment_method='vietqr')

        admin_user = User.objects.create_superuser(username='admin_test', password='p', email='admin@test.com')
        self.client.force_login(admin_user)

        response = self.client.get('/admin/cart_orders/order/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, order_cod.order_code)
        self.assertContains(response, order_vietqr.order_code)
        self.assertContains(response, 'COD (Tiền mặt)')
        self.assertContains(response, 'Chưa có bill')


