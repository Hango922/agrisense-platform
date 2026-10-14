# File: apps/products/tests/test_products.py
"""
Kiểm thử danh mục, nhà cung cấp, sản phẩm và hiển thị giao diện sản phẩm.
"""
from decimal import Decimal
from django.test import TestCase, Client
from apps.products.models import Category, Supplier, Product


class ProductTests(TestCase):
    def setUp(self):
        self.cat = Category.objects.create(name='Rau hữu cơ', slug='rau-huu-co')
        self.sup = Supplier.objects.create(name='Nông trại Xanh', address='Đà Lạt', certification='Organic')
        self.prod = Product.objects.create(
            name='Xà lách thủy canh',
            slug='xa-lach-thuy-canh',
            category=self.cat,
            supplier=self.sup,
            price=Decimal(35000),
            stock=40,
            unit='kg',
            description='Xà lách tươi sạch trồng thủy canh.',
            origin='Đà Lạt'
        )
        self.client = Client()

    def test_product_str_and_properties(self):
        self.assertEqual(str(self.cat), 'Rau hữu cơ')
        self.assertEqual(str(self.sup), 'Nông trại Xanh')
        self.assertEqual(str(self.prod), 'Xà lách thủy canh')

    def test_product_list_view(self):
        response = self.client.get('/products/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Xà lách thủy canh')

    def test_product_detail_view(self):
        response = self.client.get(f'/products/{self.prod.slug}/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Xà lách thủy canh')
        self.assertContains(response, 'Nông trại Xanh')
