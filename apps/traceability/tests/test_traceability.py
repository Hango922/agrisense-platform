# File: apps/traceability/tests/test_traceability.py
"""
Kiểm thử tạo lô hàng, sinh mã QR tự động và xem trang truy xuất công khai.
"""
from datetime import date
from decimal import Decimal
from django.test import TestCase, Client
from apps.products.models import Category, Supplier, Product
from apps.traceability.models import ProductBatch, TraceabilityRecord
from apps.traceability.qr_generator import generate_qr_code


class TraceabilityTests(TestCase):
    def setUp(self):
        self.cat = Category.objects.create(name='Trái cây', slug='trai-cay')
        self.sup = Supplier.objects.create(name='HTX Bến Tre', address='Bến Tre', certification='VietGAP')
        self.prod = Product.objects.create(
            name='Bưởi da xanh', slug='buoi-da-xanh', category=self.cat, supplier=self.sup,
            price=Decimal(65000), stock=100, unit='kg'
        )
        self.batch = ProductBatch.objects.create(
            product=self.prod,
            batch_code='BATCH-TEST-001',
            planting_location='Bến Tre',
            harvest_date=date.today(),
            packaging_date=date.today(),
            certification='VietGAP',
            quantity='100kg'
        )
        self.client = Client()

    def test_qr_code_generation(self):
        qr_file = generate_qr_code(self.batch)
        self.assertIsNotNone(qr_file)
        self.assertTrue(qr_file.name.endswith('.png'))
        self.batch.qr_code.save(qr_file.name, qr_file, save=True)
        self.assertTrue(self.batch.qr_code)

    def test_public_trace_view_success(self):
        response = self.client.get(f'/trace/{self.batch.batch_code}/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Bưởi da xanh')
        self.assertContains(response, 'BATCH-TEST-001')

    def test_public_trace_view_404(self):
        response = self.client.get('/trace/NON-EXISTENT-CODE/')
        self.assertEqual(response.status_code, 404)
