# File: apps/behavior/tests/test_behavior.py
"""
Kiểm thử phân loại hành vi người dùng AI (RFM-like rules) và lệnh cập nhật phân nhóm.
"""
from datetime import timedelta
from decimal import Decimal
from django.test import TestCase
from django.utils import timezone
from apps.accounts.models import User
from apps.products.models import Category, Supplier, Product
from apps.behavior.models import UserEvent, UserSegment
from apps.behavior.segmentation import classify_user, update_all_segments
from apps.cart_orders.models import Order, OrderItem


class BehaviorSegmentationTests(TestCase):
    def setUp(self):
        self.cat = Category.objects.create(name='Rau củ', slug='rau-cu')
        self.sup = Supplier.objects.create(name='Đà Lạt Xanh', address='Đà Lạt')
        self.prod = Product.objects.create(
            name='Cà rốt', slug='ca-rot', category=self.cat, supplier=self.sup,
            price=Decimal(25000), stock=50, unit='kg'
        )

    def test_classify_new_user(self):
        user = User.objects.create_user(username='newbie', password='Password@123')
        user.date_joined = timezone.now() - timedelta(days=2)
        user.save()
        seg, reason = classify_user(user)
        self.assertEqual(seg, 'new')

    def test_classify_interested_user(self):
        user = User.objects.create_user(username='interested_user', password='Password@123')
        user.date_joined = timezone.now() - timedelta(days=15)
        user.save()
        # Tạo 5 tương tác (view, search)
        for _ in range(5):
            UserEvent.objects.create(user=user, event_type='view', product=self.prod)
        seg, reason = classify_user(user)
        self.assertEqual(seg, 'interested')

    def test_classify_loyal_user(self):
        user = User.objects.create_user(username='loyal_user', password='Password@123')
        # Tạo 3 đơn hàng thành công trong 30 ngày
        for i in range(3):
            order = Order.objects.create(
                user=user, order_code=f'ORD-LOYAL-{i}',
                full_name='Loyal Customer', phone='0901', address='HN',
                total_amount=100000, final_amount=130000, status='delivered'
            )
            Order.objects.filter(id=order.id).update(created_at=timezone.now() - timedelta(days=5))
        seg, reason = classify_user(user)
        self.assertEqual(seg, 'loyal')

    def test_classify_at_risk_user(self):
        user = User.objects.create_user(username='at_risk_user', password='Password@123')
        # Tạo đơn hàng từ 40 ngày trước
        order = Order.objects.create(
            user=user, order_code='ORD-OLD-1',
            full_name='Old Customer', phone='0902', address='HCM',
            total_amount=100000, final_amount=130000, status='delivered'
        )
        Order.objects.filter(id=order.id).update(created_at=timezone.now() - timedelta(days=40))
        seg, reason = classify_user(user)
        self.assertEqual(seg, 'at_risk')

    def test_update_all_segments(self):
        user = User.objects.create_user(username='batch_user', password='Password@123')
        user.date_joined = timezone.now() - timedelta(days=20)
        user.save()
        for _ in range(6):
            UserEvent.objects.create(user=user, event_type='view', product=self.prod)
        update_all_segments()
        user.refresh_from_db()
        self.assertEqual(user.segment, 'interested')
        self.assertTrue(UserSegment.objects.filter(user=user, segment='interested').exists())
