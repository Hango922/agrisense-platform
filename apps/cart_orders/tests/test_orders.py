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
