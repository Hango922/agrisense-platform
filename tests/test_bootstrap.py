"""A fresh database must support the documented demo setup."""

from io import StringIO

from django.core.management import call_command
from django.test import TestCase

from apps.accounts.models import User
from apps.products.models import Product
from apps.traceability.models import ProductBatch


class DemoBootstrapTests(TestCase):
    def test_seeded_demo_supports_customer_and_admin_pages(self):
        output = StringIO()
        call_command('seed_data', stdout=output)
        call_command('update_segments', stdout=output)

        self.assertTrue(Product.objects.filter(is_active=True, stock__gt=0).exists())
        batch = ProductBatch.objects.first()
        self.assertIsNotNone(batch)
        self.assertTrue(batch.qr_code.storage.exists(batch.qr_code.name))
        self.assertEqual(self.client.get('/').status_code, 200)
        self.assertEqual(self.client.get(f'/trace/{batch.batch_code}/').status_code, 200)

        self.assertTrue(self.client.login(username='demo_customer', password='Demo@123'))
        self.assertEqual(self.client.get('/cart/').status_code, 200)
        self.assertEqual(self.client.get('/dashboard/').status_code, 302)

        self.assertTrue(self.client.login(username='demo_admin', password='Admin@123'))
        self.assertTrue(User.objects.get(username='demo_admin').is_staff)
        self.assertEqual(self.client.get('/dashboard/').status_code, 200)
        self.assertEqual(self.client.get('/dashboard/orders/export-excel/').status_code, 200)
