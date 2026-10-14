# File: apps/products/management/commands/seed_data.py
"""
Lệnh seed_data tạo dữ liệu mẫu hoàn chỉnh cho hệ sinh thái AgriSense:
1. Danh mục sản phẩm (5 danh mục)
2. Nhà cung cấp (5 nhà cung cấp nông nghiệp)
3. Sản phẩm nông sản (30 sản phẩm đa dạng)
4. Người dùng mẫu (20 user theo 4 nhóm hành vi AI)
5. Nhật ký sự kiện tương tác hành vi (UserEvent)
6. Đơn hàng mẫu (50 đơn hàng với các trạng thái và mặt hàng)
7. Lô hàng & mã QR truy xuất nguồn gốc (10 lô hàng kèm QR)
8. Tài khoản quản trị và khách hàng demo
"""
import random
from datetime import timedelta, date
from decimal import Decimal
from django.core.management.base import BaseCommand
from django.utils import timezone
from django.utils.text import slugify
from apps.accounts.models import User
from apps.products.models import Category, Supplier, Product
from apps.behavior.models import UserEvent
from apps.cart_orders.models import Order, OrderItem
from apps.traceability.models import ProductBatch
from apps.traceability.qr_generator import generate_qr_code


class Command(BaseCommand):
    help = 'Tạo dữ liệu mẫu cho hệ thống AgriSense'

    def handle(self, *args, **kwargs):
        self.stdout.write('🌱 Bắt đầu seed data...')

        # 1. Categories
        cat_names = ['Rau củ', 'Trái cây', 'Gạo', 'Đặc sản vùng miền', 'Hữu cơ']
        categories = []
        for name in cat_names:
            cat, _ = Category.objects.get_or_create(name=name, defaults={'slug': slugify(name)})
            categories.append(cat)

        # 2. Suppliers
        suppliers_data = [
            ('Trang trại Đà Lạt Xanh', 'Đà Lạt, Lâm Đồng', 'VietGAP'),
            ('HTX Nông nghiệp Miền Tây', 'Cần Thơ', 'GlobalGAP'),
            ('Trang trại Hữu cơ Sóc Sơn', 'Hà Nội', 'Organic'),
            ('HTX Lúa gạo An Giang', 'An Giang', 'VietGAP'),
            ('Trang trại Trái cây Bến Tre', 'Bến Tre', 'VietGAP'),
        ]
        suppliers = []
        for name, addr, cert in suppliers_data:
            s, _ = Supplier.objects.get_or_create(name=name, defaults={'address': addr, 'certification': cert})
            suppliers.append(s)

        # 3. Products
        products_data = [
            ('Cà rốt Đà Lạt', 25000, 'kg', 100), ('Cà chua bi', 35000, 'kg', 80),
            ('Xà lách Romaine', 40000, 'kg', 50), ('Bắp cải trắng', 20000, 'kg', 120),
            ('Súp lơ xanh', 45000, 'kg', 60), ('Táo Envy', 120000, 'kg', 40),
            ('Cam sành Hà Giang', 45000, 'kg', 100), ('Xoài cát Hòa Lộc', 85000, 'kg', 50),
            ('Thanh long ruột đỏ', 30000, 'kg', 80), ('Bơ sáp Đắk Lắk', 75000, 'kg', 60),
            ('Gạo ST25', 30000, 'kg', 200), ('Gạo lứt huyết rồng', 45000, 'kg', 150),
            ('Gạo nếp cái hoa vàng', 35000, 'kg', 100), ('Nếp than', 40000, 'kg', 80),
            ('Gạo Japonica', 50000, 'kg', 90), ('Mật ong rừng Tây Nguyên', 250000, 'hộp', 30),
            ('Tiêu đen Phú Quốc', 180000, 'kg', 40), ('Cà phê Robusta', 120000, 'kg', 50),
            ('Trà Thái Nguyên', 200000, 'kg', 35), ('Hạt điều rang muối', 220000, 'kg', 25),
            ('Rau muống hữu cơ', 30000, 'bó', 100), ('Cải ngọt hữu cơ', 35000, 'bó', 80),
            ('Rau dền hữu cơ', 30000, 'bó', 90), ('Mồng tơi hữu cơ', 25000, 'bó', 70),
            ('Cải thìa hữu cơ', 35000, 'bó', 60), ('Khoai lang Nhật', 45000, 'kg', 70),
            ('Khoai tây Đà Lạt', 35000, 'kg', 80), ('Hành tây Đà Lạt', 30000, 'kg', 90),
            ('Tỏi Lý Sơn', 180000, 'kg', 40), ('Gừng tươi', 60000, 'kg', 50),
        ]
        products = []
        for i, (name, price, unit, stock) in enumerate(products_data):
            cat = categories[i % 5]
            sup = suppliers[i % 5]
            p, _ = Product.objects.get_or_create(
                name=name,
                defaults={
                    'slug': slugify(name) + f'-{i}',
                    'category': cat, 'supplier': sup,
                    'price': Decimal(price), 'unit': unit, 'stock': stock,
                    'description': f'{name} tươi ngon, đạt tiêu chuẩn an toàn.',
                    'usage': 'Chế biến nhiều món ăn bổ dưỡng gia đình.',
                    'storage': 'Bảo quản nơi khô ráo, thoáng mát hoặc ngăn mát tủ lạnh.',
                    'season': random.choice(['Xuân', 'Hạ', 'Thu', 'Đông', 'Quanh năm']),
                    'origin': sup.address,
                }
            )
            products.append(p)

        # 4. Users (5 new, 5 interested, 5 loyal, 5 at_risk)
        segments = ['new'] * 5 + ['interested'] * 5 + ['loyal'] * 5 + ['at_risk'] * 5
        users = []
        for i, seg in enumerate(segments):
            username = f'demo_user_{i+1}'
            user, created = User.objects.get_or_create(
                username=username,
                defaults={
                    'email': f'{username}@demo.com',
                    'phone': f'09{random.randint(10000000, 99999999)}',
                    'segment': seg,
                }
            )
            if created:
                user.set_password('Demo@123')
                if seg == 'new':
                    user.date_joined = timezone.now() - timedelta(days=3)
                elif seg == 'at_risk':
                    user.date_joined = timezone.now() - timedelta(days=90)
                else:
                    user.date_joined = timezone.now() - timedelta(days=45)
                user.save()
            users.append(user)

        # 5. Events
        for user in users:
            num_events = random.randint(6, 15) if user.segment == 'interested' else random.randint(3, 8)
            for _ in range(num_events):
                p = random.choice(products)
                event_time = timezone.now() - timedelta(days=random.randint(0, 30))
                ev = UserEvent.objects.create(
                    user=user,
                    event_type=random.choice(['view', 'view', 'view', 'search', 'add_to_cart']),
                    product=p, category=p.category,
                )
                UserEvent.objects.filter(id=ev.id).update(created_at=event_time)

        # 6. Orders (50 orders)
        statuses = ['pending', 'confirmed', 'shipping', 'delivered', 'cancelled']
        for i in range(50):
            # Phân bổ đơn hàng hợp lý để bảo toàn đặc tính phân nhóm:
            # - users[0:5] (new): 0 đơn hàng
            # - users[5:10] (interested): 0 đơn hàng
            # - users[10:15] (loyal): đơn hàng gần đây (trong 30 ngày)
            # - users[15:20] (at_risk): đơn hàng cũ (> 30 ngày)
            if i < 28:
                user = random.choice(users[10:15])  # loyal users
                order_time = timezone.now() - timedelta(days=random.randint(1, 25))
                status = random.choice(['confirmed', 'shipping', 'delivered', 'pending'])
            elif i < 44:
                user = random.choice(users[15:20])  # at_risk users
                order_time = timezone.now() - timedelta(days=random.randint(35, 75))
                status = random.choice(['delivered', 'delivered', 'cancelled'])
            else:
                user = random.choice(users[10:15])
                order_time = timezone.now() - timedelta(days=random.randint(1, 50))
                status = random.choice(statuses)

            order_code = f'ORD{i+1:05d}'
            order, o_created = Order.objects.get_or_create(
                order_code=order_code,
                defaults={
                    'user': user,
                    'full_name': user.username,
                    'phone': user.phone or '0900000000',
                    'address': 'Địa chỉ demo, Việt Nam',
                    'total_amount': 0,
                    'final_amount': 0,
                    'status': status,
                    'payment_method': 'cod',
                }
            )
            if o_created:
                total = Decimal(0)
                for _ in range(random.randint(1, 3)):
                    p = random.choice(products)
                    qty = random.randint(1, 3)
                    subtotal = p.price * qty
                    total += subtotal
                    OrderItem.objects.create(
                        order=order, product=p, product_name=p.name,
                        price=p.price, quantity=qty, subtotal=subtotal,
                    )
                order.total_amount = total
                shipping = Decimal(0) if total >= Decimal(500000) else Decimal(30000)
                order.shipping_fee = shipping
                order.final_amount = total + shipping
                order.save()
                Order.objects.filter(id=order.id).update(created_at=order_time)

        # 7. Batches + QR (10 lô hàng)
        for i in range(10):
            p = random.choice(products)
            batch, _ = ProductBatch.objects.get_or_create(
                batch_code=f'BATCH2026{i+1:03d}',
                defaults={
                    'product': p,
                    'planting_location': p.supplier.address,
                    'harvest_date': date.today() - timedelta(days=random.randint(1, 30)),
                    'packaging_date': date.today() - timedelta(days=random.randint(0, 5)),
                    'certification': p.supplier.certification,
                    'quantity': f'{random.randint(50, 200)}kg',
                }
            )
            if not batch.qr_code:
                qr_file = generate_qr_code(batch)
                batch.qr_code.save(qr_file.name, qr_file, save=True)

        # 8. Demo accounts
        if not User.objects.filter(username='demo_admin').exists():
            User.objects.create_superuser('demo_admin', 'admin@demo.com', 'Admin@123')
        if not User.objects.filter(username='demo_customer').exists():
            User.objects.create_user('demo_customer', 'customer@demo.com', 'Demo@123', segment='loyal')

        self.stdout.write(self.style.SUCCESS('🎉 Seed data hoàn tất!'))
        self.stdout.write('👤 Admin: demo_admin / Admin@123')
        self.stdout.write('👤 Customer: demo_customer / Demo@123')
