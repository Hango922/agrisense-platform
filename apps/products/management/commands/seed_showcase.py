"""Create an isolated, repeatable presentation catalog without resetting data."""
import shutil
from datetime import timedelta
from pathlib import Path

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone

from apps.accounts.models import User
from apps.cart_orders.models import Order
from apps.cart_orders.services import create_direct_order
from apps.products.models import Category, ComboItem, Product, SeasonalCombo, Supplier
from apps.traceability.inventory import receive_batch

CATALOG = [
    ('ca-chua-bi', 'Cà chua bi', 'Rau củ', 35000, 'ca_chua_bi.jpg', 'Đà Lạt, Lâm Đồng'),
    ('ca-rot-da-lat', 'Cà rốt Đà Lạt', 'Rau củ', 25000, 'ca_rot_da_lat.jpg', 'Đà Lạt, Lâm Đồng'),
    ('sup-lo-xanh', 'Súp lơ xanh', 'Rau củ', 45000, 'sup_lo_xanh.jpg', 'Đà Lạt, Lâm Đồng'),
    ('xa-lach-romaine', 'Xà lách Romaine', 'Rau củ', 40000, 'xa_lach_romaine.jpg', 'Đà Lạt, Lâm Đồng'),
    ('bo-sap', 'Bơ sáp Đắk Lắk', 'Trái cây', 75000, 'bo_sap_dak_lak.jpg', 'Đắk Lắk'),
    ('cam-sanh', 'Cam sành Hà Giang', 'Trái cây', 45000, 'cam_sanh_ha_giang.jpg', 'Hà Giang'),
    ('thanh-long', 'Thanh long ruột đỏ', 'Trái cây', 30000, 'thanh_long_ruot_do.jpg', 'Bình Thuận'),
    ('buoi-da-xanh', 'Bưởi da xanh Bến Tre', 'Trái cây', 55000, 'buoi_da_xanh_ben_tre.jpg', 'Bến Tre'),
    ('gao-st25', 'Gạo ST25', 'Gạo & hạt', 30000, 'gao_st25.jpg', 'Sóc Trăng'),
    ('khoai-lang', 'Khoai lang Nhật', 'Rau củ', 45000, 'khoai_lang_nhat.jpg', 'Đà Lạt, Lâm Đồng'),
    ('cai-ngot', 'Cải ngọt hữu cơ', 'Rau củ', 35000, 'cai_ngot_huu_co.jpg', 'Sóc Sơn, Hà Nội'),
    ('hat-dieu', 'Hạt điều rang muối', 'Gạo & hạt', 220000, 'hat_dieu_rang_muoi.jpg', 'Bình Phước'),
]


class Command(BaseCommand):
    help = 'Tạo bản demo nâng cấp; chỉ chạy với nongsan_project.demo_settings.'

    def handle(self, *args, **options):
        if not settings.DEMO_MODE:
            raise CommandError('Chỉ được chạy với --settings=nongsan_project.demo_settings')
        today = timezone.localdate()
        supplier, _ = Supplier.objects.get_or_create(name='Nông trại AgriSense (minh họa)', defaults={'address': 'Việt Nam', 'description': 'Dữ liệu minh họa cho đồ án.'})
        customer, created = User.objects.get_or_create(username='demo_customer')
        if created:
            customer.set_password('Demo@123')
            customer.save()
        admin, created = User.objects.get_or_create(username='demo_admin', defaults={'is_staff': True, 'is_superuser': True})
        if created:
            admin.set_password('Admin@123')
            admin.save()
        products = {}
        for index, (slug, name, category, price, image, origin) in enumerate(CATALOG):
            cat, _ = Category.objects.get_or_create(name=category, defaults={'slug': {'Rau củ': 'rau-cu', 'Trái cây': 'trai-cay', 'Gạo & hạt': 'gao-hat'}[category]})
            product, created = Product.objects.get_or_create(slug=slug, defaults={
                'name': name, 'category': cat, 'supplier': supplier, 'price': price, 'stock': 0,
                'origin': origin, 'season': 'Tuyển chọn tháng 11',
                'description': f'{name} cho bữa cơm gia đình. Thông tin sản phẩm và nguồn gốc trong bản demo là dữ liệu minh họa.',
                'storage': 'Bảo quản nơi khô mát; rau củ nên để ngăn mát và dùng sớm.',
                'usage': 'Rửa sạch, sơ chế và chế biến phù hợp với từng loại nông sản.',
            })
            source = settings.BASE_DIR / 'media' / 'products' / image
            if not source.exists():
                source = settings.BASE_DIR / 'static' / 'images' / 'showcase' / image
            destination = Path(settings.MEDIA_ROOT) / 'products' / image
            if source.exists() and not destination.exists():
                destination.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(source, destination)
            if destination.exists() and not product.image:
                product.image = 'products/' + image
                product.save(update_fields=['image'])
            if created:
                receive_batch(product, quantity=6 if index == 2 else 30, batch_code=f'DEMO-{index + 1:03}',
                              harvest_date=today - timedelta(days=1), packaging_date=today,
                              expiry_date=today + timedelta(days=2 if index < 3 else 10), planting_location=origin)
            products[slug] = product
        combos = [
            ('bua-com-nha', 'Bữa cơm nhà', 'Rau củ dễ kết hợp cho những bữa cơm giản dị.', ['ca-chua-bi', 'ca-rot-da-lat', 'sup-lo-xanh']),
            ('sac-mau-trai-cay', 'Sắc màu trái cây', 'Thêm một chút tươi mát cho cả gia đình.', ['cam-sanh', 'thanh-long', 'bo-sap']),
            ('bep-am', 'Gian bếp ấm', 'Gạo thơm và rau củ để bắt đầu một bữa ngon.', ['gao-st25', 'khoai-lang', 'cai-ngot']),
        ]
        for slug, name, description, members in combos:
            combo, created = SeasonalCombo.objects.get_or_create(slug=slug, defaults={'name': name, 'description': description, 'season_label': 'Tuyển chọn tháng 11'})
            if created:
                for key in members:
                    ComboItem.objects.create(combo=combo, product=products[key], quantity=1)
        if not Order.objects.filter(user=customer).exists():
            order = create_direct_order(customer, [{'product': products['ca-chua-bi'], 'quantity': 1}],
                                        {'full_name': 'Khách hàng Demo', 'phone': '0901234567', 'address': 'Địa chỉ minh họa, Hà Nội'},
                                        payment_method='vietqr', note='Đơn minh họa cho phần trình diễn thanh toán.')
            Order.objects.filter(pk=order.pk).update(created_at=timezone.now() - timedelta(hours=26))
        self.stdout.write(self.style.SUCCESS('Demo ready: 12 products, 3 seasonal baskets, lot inventory and a pending payment.'))
