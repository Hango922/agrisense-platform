"""Exercise stock locks using independent MySQL connections."""

from concurrent.futures import ThreadPoolExecutor
from threading import Barrier

from django.db import close_old_connections, connections
from django.test import TransactionTestCase

from apps.accounts.models import User
from apps.cart_orders.models import Order
from apps.cart_orders.services import cancel_order, create_direct_order
from apps.products.models import Category, Product, Supplier


class ConcurrentOrderTests(TransactionTestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='concurrent')
        category = Category.objects.create(name='Test', slug='test')
        supplier = Supplier.objects.create(name='Test', address='Test')
        self.product = Product.objects.create(
            name='Test', slug='test', category=category, supplier=supplier,
            price=10000, stock=5,
        )
        self.address = {'full_name': 'Test', 'phone': '0901234567', 'address': 'Test'}

    def race(self, action):
        barrier = Barrier(2)

        def worker():
            close_old_connections()
            try:
                barrier.wait(timeout=10)
                action()
                return 'success'
            except ValueError:
                return 'rejected'
            finally:
                connections.close_all()

        with ThreadPoolExecutor(max_workers=2) as pool:
            results = list(pool.map(lambda _: worker(), range(2)))
        self.assertCountEqual(results, ['success', 'rejected'])

    def test_simultaneous_purchases_cannot_oversell(self):
        self.race(lambda: create_direct_order(
            self.user, [{'product': self.product, 'quantity': 4}], self.address,
        ))
        self.product.refresh_from_db()
        self.assertEqual(self.product.stock, 1)
        self.assertEqual(Order.objects.count(), 1)

    def test_simultaneous_cancellations_refund_once(self):
        order = create_direct_order(
            self.user, [{'product': self.product, 'quantity': 4}], self.address,
        )
        self.race(lambda: cancel_order(order))
        self.product.refresh_from_db()
        self.assertEqual(self.product.stock, 5)
        order.refresh_from_db()
        self.assertEqual(order.status, 'cancelled')
