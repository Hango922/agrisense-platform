# File: tests/test_phase5.py
"""
Kiểm thử toàn diện Dashboard Admin Phase 5:
1. Phân quyền: User thường bị chặn, Staff/Admin truy cập được
2. Số liệu thống kê Dashboard (doanh thu, đơn hàng, khách hàng, sản phẩm, phân nhóm)
3. Các trang phân hệ con của Dashboard
"""
from django.test import TestCase, Client
from apps.accounts.models import User
from apps.products.models import Product, Category, Supplier
from apps.cart_orders.models import Order


class Phase5ComprehensiveTests(TestCase):
    def setUp(self):
        self.cat = Category.objects.create(name='Rau củ', slug='rau-cu')
        self.sup = Supplier.objects.create(name='Đà Lạt Xanh', address='Đà Lạt')
        self.prod = Product.objects.create(
            name='Cà rốt', slug='ca-rot', category=self.cat, supplier=self.sup,
            price=25000, stock=50, unit='kg'
        )
        self.normal_user = User.objects.create_user(username='normal_user', password='Password@123')
        self.admin_user = User.objects.create_superuser(
            username='admin_user',
            email='admin@test.com',
            password='AdminPassword@123'
        )
        self.order = Order.objects.create(
            order_code='ORD-TEST-DASHBOARD',
            user=self.normal_user,
            full_name='Khách Mẫu Dashboard',
            phone='0901234567',
            address='TP. Hồ Chí Minh',
            total_amount=220000,
            shipping_fee=30000,
            final_amount=250000,
            status='confirmed',
            payment_method='cod'
        )
        self.client = Client()

    def test_permission_denied_for_normal_user(self):
        self.client.force_login(self.normal_user)
        response = self.client.get('/dashboard/')
        self.assertIn(response.status_code, [302, 403])

    def test_admin_dashboard_metrics(self):
        self.client.force_login(self.admin_user)
        response = self.client.get('/dashboard/')
        self.assertEqual(response.status_code, 200)
        ctx = response.context
        self.assertGreaterEqual(ctx['total_revenue'], 250000)
        self.assertGreaterEqual(ctx['total_orders'], 1)
        self.assertGreaterEqual(ctx['total_customers'], 1)
        self.assertGreaterEqual(ctx['total_products'], 1)

    def test_dashboard_subpages(self):
        self.client.force_login(self.admin_user)
        subpages = [
            '/dashboard/products/',
            '/dashboard/orders/',
            '/dashboard/customers/',
            '/dashboard/behavior/',
            '/dashboard/traceability/',
        ]
        for url in subpages:
            res = self.client.get(url)
            self.assertEqual(res.status_code, 200, f"Page {url} returned {res.status_code}")
