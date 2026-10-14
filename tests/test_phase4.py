# File: tests/test_phase4.py
"""
Kiểm thử toàn diện các tính năng AI Phase 4:
1. Phân nhóm hành vi & update_all_segments
2. Chatbot fallback rules & endpoint
3. Sinh mã QR & trang truy xuất nguồn gốc
4. Gợi ý cá nhân hóa & trang chủ
"""
import json
from datetime import date, timedelta
from django.test import TestCase, Client
from django.utils import timezone
from apps.accounts.models import User
from apps.products.models import Category, Supplier, Product
from apps.behavior.models import UserEvent, UserSegment
from apps.behavior.segmentation import update_all_segments, classify_user
from apps.chatbot.fallback import get_fallback_response
from apps.traceability.models import ProductBatch
from apps.traceability.qr_generator import generate_qr_code
from apps.recommendation.engine import recommend_for_user


class Phase4ComprehensiveTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='ai_test_user', email='ai@test.com', password='Password@123')
        self.cat = Category.objects.create(name='Trái Cây', slug='trai-cay')
        self.sup = Supplier.objects.create(name='HTX Nông Nghiệp Sạch', address='Long An', certification='GlobalGAP')
        self.prod = Product.objects.create(
            name='Dưa Lưới Huỳnh Long',
            slug='dua-luoi-huynh-long',
            category=self.cat,
            supplier=self.sup,
            price=90000,
            stock=100,
            origin='Long An'
        )
        self.batch = ProductBatch.objects.create(
            product=self.prod,
            batch_code='BATCH-DUALUOI-2026',
            planting_location='Nhà màng Long An Công nghệ cao',
            harvest_date=date.today(),
            packaging_date=date.today(),
            certification='GlobalGAP'
        )
        self.client = Client()

    def test_behavior_segmentation(self):
        self.user.date_joined = timezone.now() - timedelta(days=10)
        self.user.save()
        for _ in range(6):
            UserEvent.objects.create(user=self.user, event_type='view', product=self.prod, category=self.cat)
        seg, reason = classify_user(self.user)
        self.assertEqual(seg, 'interested')

        update_all_segments()
        self.user.refresh_from_db()
        self.assertEqual(self.user.segment, 'interested')

    def test_chatbot_fallback_rules(self):
        test_queries = [
            ('Giá cà chua bao nhiêu?', 'price'),
            ('Gia ca chua bao nhieu?', 'price'),
            ('Nguồn gốc xuất xứ ở đâu?', 'origin'),
            ('Bảo quản rau trong tủ lạnh được không?', 'storage'),
            ('Đơn hàng của tôi đã giao chưa?', 'order'),
            ('Hôm nay thời tiết thế nào?', 'default'),
        ]
        for q, expected_key in test_queries:
            resp_text, key = get_fallback_response(q)
            self.assertEqual(key, expected_key, f"Query '{q}' expected key '{expected_key}', got '{key}'")

    def test_chatbot_endpoint(self):
        resp = self.client.post(
            '/chatbot/send/',
            json.dumps({'message': 'Giá cải bó xôi bao nhiêu tiền?'}),
            content_type='application/json'
        )
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertIn('reply', data)

    def test_qr_traceability(self):
        qr_content = generate_qr_code(self.batch)
        self.batch.qr_code.save(qr_content.name, qr_content, save=True)
        self.assertTrue(self.batch.qr_code)

        resp_trace = self.client.get(f'/trace/{self.batch.batch_code}/')
        self.assertEqual(resp_trace.status_code, 200)
        self.assertContains(resp_trace, self.prod.name)

    def test_recommendation_and_home_view(self):
        UserEvent.objects.create(user=self.user, event_type='view', product=self.prod, category=self.cat)
        recs = recommend_for_user(self.user, limit=5)
        self.assertIsInstance(recs, list)

        self.client.force_login(self.user)
        resp_home = self.client.get('/')
        self.assertEqual(resp_home.status_code, 200)
