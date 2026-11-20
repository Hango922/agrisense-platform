"""Apply the reviewed local image catalog and add sample products idempotently."""
import json
import shutil
import unicodedata
from pathlib import Path

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from django.utils.text import slugify

from apps.products.models import Category, Product, Supplier


def name_key(value):
    value = unicodedata.normalize('NFKD', value.casefold().replace('đ', 'd'))
    return ' '.join(''.join(c for c in value if not unicodedata.combining(c)).split())


class Command(BaseCommand):
    help = 'Fix reviewed product images and add 20 sample catalog items without resetting stock.'

    def handle(self, *args, **options):
        if getattr(settings, 'OPERATIONAL_MODE', False):
            raise CommandError('Sample catalog updates are disabled in operational settings.')
        root = Path(settings.BASE_DIR) / 'static' / 'images' / 'catalog'
        entries = json.loads((root / 'catalog.json').read_text(encoding='utf-8'))
        # Validate the complete bundle before changing files or database rows.
        for entry in entries:
            filename = entry['image']
            if Path(filename).name != filename or not (root / filename).is_file():
                raise CommandError(f'Missing or invalid catalog image: {filename}')
        destination = Path(settings.MEDIA_ROOT) / 'products' / 'catalog-v2'
        destination.mkdir(parents=True, exist_ok=True)
        for entry in entries:
            shutil.copyfile(root / entry['image'], destination / entry['image'])

        created_count = updated_count = 0
        with transaction.atomic():
            products = {}
            for product in Product.objects.all():
                products.setdefault(name_key(product.name), []).append(product)
            for entry in entries:
                matches = products.get(name_key(entry['name']), [])
                image = f"products/catalog-v2/{entry['image']}"
                if not matches and entry.get('new'):
                    category = Category.objects.filter(name__iexact=entry['category']).first()
                    if category is None:
                        category, _ = Category.objects.get_or_create(
                            slug=entry['category_slug'], defaults={'name': entry['category']},
                        )
                    supplier, _ = Supplier.objects.get_or_create(
                        name='AgriSense - Danh mục minh họa',
                        defaults={'address': 'Việt Nam', 'description': 'Nhà cung cấp mẫu cho đồ án.'},
                    )
                    product = Product.objects.create(
                        name=entry['name'], slug='catalog-' + slugify(name_key(entry['name'])),
                        category=category, supplier=supplier, image=image,
                        price=entry['price'], unit=entry['unit'], stock=entry['stock'],
                        origin='Việt Nam (minh họa)', season='Theo nguồn cung',
                        description=entry['description'] + ' Giá, tồn kho và xuất xứ là dữ liệu minh họa cho đồ án.',
                        usage=entry['usage'], storage=entry['storage'],
                    )
                    products[name_key(entry['name'])] = [product]
                    created_count += 1
                else:
                    for product in matches:
                        if product.image.name != image:
                            product.image = image
                            product.save(update_fields=['image'])
                            updated_count += 1
        self.stdout.write(self.style.SUCCESS(
            f'Catalog ready: {updated_count} images updated, {created_count} products added.',
        ))
