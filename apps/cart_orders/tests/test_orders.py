# File: apps/cart_orders/tests/test_orders.py
"""
Kiểm thử chức năng đặt hàng, kiểm tra tồn kho và hủy đơn hàng.
"""
from django.test import TestCase
from decimal import Decimal
from apps.accounts.models import User
from apps.products.models import Category, Supplier, Product
from apps.cart_orders.models import Cart, CartItem
from apps.cart_orders.services import create_order_from_cart, cancel_order, calculate_shipping_fee


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
        from apps.cart_orders.vietqr import get_vietqr_url, get_vietqr_info
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
        self.assertIn('MB', info['bank_id'])

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
