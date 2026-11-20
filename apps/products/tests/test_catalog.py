"""Regression checks for applying catalog assets to existing stores."""
import json
import tempfile
from pathlib import Path

from django.core.management import call_command
from django.core.management.base import CommandError
from django.test import TestCase, override_settings

from apps.products.models import Category, Product, Supplier


class RefreshCatalogTests(TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.assets = self.root / 'static/images/catalog'
        self.assets.mkdir(parents=True)
        (self.assets / 'cucumber.jpg').write_bytes(b'fixture-image')
        self.entry = {
            'name': 'Dưa leo', 'image': 'cucumber.jpg', 'new': True,
            'category': 'Rau củ', 'category_slug': 'rau-cu', 'price': 22000,
            'unit': 'kg', 'stock': 60, 'description': 'Dưa leo mẫu.',
            'usage': 'Rửa sạch.', 'storage': 'Giữ lạnh.',
        }
        (self.assets / 'catalog.json').write_text(
            json.dumps([self.entry]), encoding='utf-8',
        )
        self.settings_override = override_settings(
            BASE_DIR=self.root, MEDIA_ROOT=self.root / 'media', OPERATIONAL_MODE=False,
        )
        self.settings_override.enable()
        self.addCleanup(self.settings_override.disable)

    def test_repeated_run_preserves_existing_inventory_and_price(self):
        call_command('refresh_catalog', verbosity=0)
        product = Product.objects.get()
        Product.objects.filter(pk=product.pk).update(stock=7, price=19000, is_active=False)
        call_command('refresh_catalog', verbosity=0)
        product.refresh_from_db()
        self.assertEqual(Product.objects.count(), 1)
        self.assertEqual(product.stock, 7)
        self.assertEqual(product.price, 19000)
        self.assertFalse(product.is_active)
        self.assertTrue((self.root / 'media' / product.image.name).is_file())

    def test_matches_name_without_assuming_primary_key_or_accents(self):
        category = Category.objects.create(name='Rau củ', slug='rau-cu')
        supplier = Supplier.objects.create(name='Existing', address='Existing')
        product = Product.objects.create(
            pk=900, name='Dua Leo', slug='existing-cucumber', category=category,
            supplier=supplier, price=12000, stock=11, image='products/old.jpg',
        )
        call_command('refresh_catalog', verbosity=0)
        product.refresh_from_db()
        self.assertEqual(Product.objects.count(), 1)
        self.assertEqual(product.image.name, 'products/catalog-v2/cucumber.jpg')
        self.assertEqual(product.supplier, supplier)
        self.assertEqual(product.stock, 11)

    def test_missing_asset_stops_before_database_changes(self):
        (self.assets / 'cucumber.jpg').unlink()
        with self.assertRaises(CommandError):
            call_command('refresh_catalog', verbosity=0)
        self.assertEqual(Product.objects.count(), 0)
        self.assertEqual(Supplier.objects.count(), 0)

    @override_settings(OPERATIONAL_MODE=True)
    def test_operational_database_rejects_sample_data(self):
        with self.assertRaises(CommandError):
            call_command('refresh_catalog', verbosity=0)
