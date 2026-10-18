# File: apps/dashboard/tests/test_dashboard_orders.py
"""
Bộ kiểm thử tự động toàn diện cho quy trình Quản lý và Duyệt Đơn Hàng trong Dashboard:
- Duyệt đơn COD.
- Duyệt đơn VietQR có bill chuyển khoản.
- Duyệt đơn VietQR chưa có bill thông qua cơ chế Admin Đối Soát Nội Bộ (tự động tạo chứng từ).
- Duyệt đơn VietQR kèm tải trực tiếp ảnh bill từ Admin.
- Chu trình chuyển đổi trạng thái: pending -> confirmed -> shipping -> delivered.
- Hủy đơn hàng và tự động hoàn trả số lượng tồn kho sản phẩm.
- Kiểm tra phân quyền nhân viên / Admin (staff_member_required).
"""
from decimal import Decimal
from django.test import TestCase, Client
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse
from apps.accounts.models import User
from apps.products.models import Category, Supplier, Product
from apps.cart_orders.models import Cart, CartItem, Order
from apps.cart_orders.services import create_order_from_cart


class DashboardOrderWorkflowTests(TestCase):
    def setUp(self):
        # 1. Tạo tài khoản Admin/Staff và User thông thường
        self.admin_user = User.objects.create_user(
            username='staff_admin',
            email='admin@agrisense.vn',
            password='Password123!',
            is_staff=True,
            is_superuser=True
        )
        self.customer = User.objects.create_user(
            username='khach_hang',
            email='khach@gmail.com',
            password='Password123!',
            is_staff=False
        )

        # 2. Tạo danh mục, nhà cung cấp và sản phẩm nông sản
        self.category = Category.objects.create(name='Rau Củ Hữu Cơ', slug='rau-cu-huu-co')
        self.supplier = Supplier.objects.create(name='HTX Nông Nghiệp Sạch', address='Đà Lạt, Lâm Đồng')
        self.product = Product.objects.create(
            name='Cà Chua Beef Đà Lạt VietGAP',
            slug='ca-chua-beef-da-lat',
            category=self.category,
            supplier=self.supplier,
            price=Decimal(45000),
            stock=50,
            unit='kg',
            is_active=True
        )

        # 3. Client
        self.client = Client()

    def _create_test_order(self, payment_method='cod', quantity=2):
        cart = Cart.objects.create(user=self.customer)
        CartItem.objects.create(cart=cart, product=self.product, quantity=quantity)
        return create_order_from_cart(
            self.customer,
            cart,
            {
                'full_name': 'Nguyễn Văn Test',
                'phone': '0987654321',
                'address': '123 Đường Nông Nghiệp, Hà Nội'
            },
            payment_method=payment_method
        )

    def test_admin_approves_cod_order_success(self):
        """Admin duyệt đơn COD đang chờ xác nhận -> chuyển sang 'confirmed' thành công."""
        order = self._create_test_order(payment_method='cod')
        self.assertEqual(order.status, 'pending')

        self.client.force_login(self.admin_user)
        response = self.client.post(
            reverse('dashboard:update_order_status', kwargs={'order_id': order.id}),
            {'status': 'confirmed'},
            follow=True
        )
        self.assertEqual(response.status_code, 200)

        order.refresh_from_db()
        self.assertEqual(order.status, 'confirmed')

    def test_admin_approves_vietqr_order_with_existing_proof(self):
        """Admin duyệt đơn VietQR đã có bill chuyển khoản -> chuyển sang 'confirmed'."""
        order = self._create_test_order(payment_method='vietqr')
        fake_bill = SimpleUploadedFile("bill_vietqr.png", b"\x89PNG\r\n\x1a\nfakeimagecontent", content_type="image/png")
        order.payment_proof = fake_bill
        order.save()

        self.client.force_login(self.admin_user)
        response = self.client.post(
            reverse('dashboard:update_order_status', kwargs={'order_id': order.id}),
            {'status': 'confirmed'},
            follow=True
        )
        self.assertEqual(response.status_code, 200)

        order.refresh_from_db()
        self.assertEqual(order.status, 'confirmed')

        if order.payment_proof:
            order.payment_proof.delete(save=False)

    def test_admin_approves_vietqr_order_without_bill_via_internal_verification(self):
        """
        Quy trình xử lý vấn đề người dùng phản hồi:
        Đơn VietQR chưa có bill nhưng Admin đã đối soát tài khoản ngân hàng thực tế,
        Admin bấm 'Duyệt Đơn' -> Hệ thống tự động tạo chứng từ đối soát nội bộ và cập nhật 'confirmed'.
        """
        order = self._create_test_order(payment_method='vietqr')
        self.assertEqual(order.status, 'pending')
        self.assertFalse(bool(order.payment_proof))

        self.client.force_login(self.admin_user)
        response = self.client.post(
            reverse('dashboard:update_order_status', kwargs={'order_id': order.id}),
            {'status': 'confirmed', 'admin_verified': '1'},
            follow=True
        )
        self.assertEqual(response.status_code, 200)

        order.refresh_from_db()
        self.assertEqual(order.status, 'confirmed')
        self.assertTrue(bool(order.payment_proof), "Phải tự động tạo chứng từ nội bộ cho payment_proof")
        self.assertIsNotNone(order.payment_proof_uploaded_at)
        self.assertIn("đối soát ngân hàng", order.note)

        if order.payment_proof:
            order.payment_proof.delete(save=False)

    def test_admin_approves_vietqr_order_with_uploaded_proof(self):
        """Admin tải trực tiếp file bill thay khách hàng khi duyệt đơn."""
        order = self._create_test_order(payment_method='vietqr')
        self.client.force_login(self.admin_user)

        admin_bill = SimpleUploadedFile("admin_bill.png", b"\x89PNG\r\n\x1a\nadminbillcontent", content_type="image/png")
        response = self.client.post(
            reverse('dashboard:update_order_status', kwargs={'order_id': order.id}),
            {'status': 'confirmed', 'payment_proof': admin_bill},
            follow=True
        )
        self.assertEqual(response.status_code, 200)

        order.refresh_from_db()
        self.assertEqual(order.status, 'confirmed')
        self.assertTrue(bool(order.payment_proof))
        self.assertIn("đã tải lên bill đối soát", order.note)

        if order.payment_proof:
            order.payment_proof.delete(save=False)

    def test_full_order_status_pipeline(self):
        """Kiểm thử chu trình trạng thái toàn vẹn: pending -> confirmed -> shipping -> delivered."""
        order = self._create_test_order(payment_method='cod')
        self.client.force_login(self.admin_user)

        # 1. Pending -> Confirmed
        res1 = self.client.post(reverse('dashboard:update_order_status', kwargs={'order_id': order.id}), {'status': 'confirmed'})
        self.assertEqual(res1.status_code, 302)
        order.refresh_from_db()
        self.assertEqual(order.status, 'confirmed')

        # 2. Confirmed -> Shipping
        res2 = self.client.post(reverse('dashboard:update_order_status', kwargs={'order_id': order.id}), {'status': 'shipping'})
        self.assertEqual(res2.status_code, 302)
        order.refresh_from_db()
        self.assertEqual(order.status, 'shipping')

        # 3. Shipping -> Delivered
        res3 = self.client.post(reverse('dashboard:update_order_status', kwargs={'order_id': order.id}), {'status': 'delivered'})
        self.assertEqual(res3.status_code, 302)
        order.refresh_from_db()
        self.assertEqual(order.status, 'delivered')

    def test_admin_cancels_pending_order_and_returns_stock(self):
        """Khi Admin hủy đơn pending, hệ thống phải hoàn trả lại số lượng tồn kho sản phẩm."""
        initial_stock = self.product.stock  # 50
        order = self._create_test_order(payment_method='cod', quantity=5)
        self.product.refresh_from_db()
        self.assertEqual(self.product.stock, initial_stock - 5)  # 45

        self.client.force_login(self.admin_user)
        response = self.client.post(
            reverse('dashboard:update_order_status', kwargs={'order_id': order.id}),
            {'status': 'cancelled'},
            follow=True
        )
        self.assertEqual(response.status_code, 200)

        order.refresh_from_db()
        self.assertEqual(order.status, 'cancelled')

        # Kiểm tra hoàn tồn kho
        self.product.refresh_from_db()
        self.assertEqual(self.product.stock, initial_stock)

    def test_customer_forbidden_from_updating_order_status(self):
        """Người dùng thông thường không có quyền staff không được phép cập nhật đơn hàng."""
        order = self._create_test_order(payment_method='cod')
        self.client.force_login(self.customer)

        response = self.client.post(
            reverse('dashboard:update_order_status', kwargs={'order_id': order.id}),
            {'status': 'confirmed'}
        )
        # Chuyển hướng tới trang login của Django admin (/admin/login/) do decorator staff_member_required
        self.assertEqual(response.status_code, 302)
        self.assertIn('/admin/login/', response.url)

        order.refresh_from_db()
        self.assertEqual(order.status, 'pending')
