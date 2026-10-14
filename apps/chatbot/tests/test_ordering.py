# File: apps/chatbot/tests/test_ordering.py
"""
Kiểm thử tính năng lên đơn hàng tự động qua Chatbot AI (Conversational Ordering).
"""
import json
from decimal import Decimal
from django.test import TestCase, Client
from apps.accounts.models import User, UserAddress
from apps.products.models import Category, Supplier, Product
from apps.cart_orders.models import Order


class ChatbotOrderingTests(TestCase):
    def setUp(self):
        self.cat = Category.objects.create(name='Rau củ Đà Lạt', slug='rau-cu-da-lat')
        self.sup = Supplier.objects.create(name='Trang trại Đà Lạt Xanh', address='Đà Lạt', certification='VietGAP')
        self.product = Product.objects.create(
            name='Cà rốt Đà Lạt',
            slug='ca-rot-da-lat',
            category=self.cat,
            supplier=self.sup,
            price=Decimal(25000),
            stock=50,
            unit='kg'
        )
        self.user = User.objects.create_user(
            username='buyer_user',
            email='buyer@test.com',
            password='Password@123',
            phone='0912345678'
        )
        self.client = Client()

    def test_anonymous_user_ordering_prompt_login(self):
        """Khách chưa đăng nhập yêu cầu mua hàng sẽ được nhắc đăng nhập."""
        resp = self.client.post(
            '/chatbot/send/',
            json.dumps({'message': 'Tôi muốn mua 2kg cà rốt'}),
            content_type='application/json'
        )
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertIn('Đăng nhập tại đây', data['reply'])

    def test_authenticated_user_one_shot_ordering(self):
        """Đặt hàng thành công ngay trong 1 tin nhắn khi cung cấp đủ SĐT và Địa chỉ."""
        self.client.force_login(self.user)
        initial_stock = self.product.stock

        resp = self.client.post(
            '/chatbot/send/',
            json.dumps({'message': 'Tôi muốn mua 2kg cà rốt, giao về số 15 Hai Bà Trưng Hà Nội, sđt 0987654321'}),
            content_type='application/json'
        )
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertIn('ĐẶT HÀNG THÀNH CÔNG', data['reply'])
        self.assertIn('ORD', data['reply'])

        # Kiểm tra tồn kho đã bị giảm 2kg
        self.product.refresh_from_db()
        self.assertEqual(self.product.stock, initial_stock - 2)

        # Kiểm tra đơn hàng trong DB
        order = Order.objects.filter(user=self.user).latest('created_at')
        self.assertEqual(order.phone, '0987654321')
        self.assertIn('Hai Bà Trưng', order.address)
        self.assertEqual(order.items.first().quantity, 2)

    def test_multi_turn_ordering_flow(self):
        """Đặt hàng qua 2 lượt hội thoại (Lượt 1: chọn sản phẩm, Lượt 2: cung cấp SĐT & địa chỉ)."""
        self.client.force_login(self.user)
        initial_stock = self.product.stock

        # Lượt 1: Chỉ nói muốn mua sản phẩm và số lượng
        r1 = self.client.post(
            '/chatbot/send/',
            json.dumps({'message': 'Lên đơn 3kg cà rốt đà lạt'}),
            content_type='application/json'
        )
        self.assertEqual(r1.status_code, 200)
        d1 = r1.json()
        self.assertIn('Cà rốt Đà Lạt', d1['reply'])
        self.assertIn('Số điện thoại', d1['reply'])

        # Lượt 2: Cung cấp thông tin nhận hàng
        r2 = self.client.post(
            '/chatbot/send/',
            json.dumps({'message': 'SĐT 0933445566, địa chỉ: Số 88 Cầu Giấy, Hà Nội'}),
            content_type='application/json'
        )
        self.assertEqual(r2.status_code, 200)
        d2 = r2.json()
        self.assertIn('ĐẶT HÀNG THÀNH CÔNG', d2['reply'])

        # Kiểm tra tồn kho
        self.product.refresh_from_db()
        self.assertEqual(self.product.stock, initial_stock - 3)

    def test_ordering_with_default_address_confirmation(self):
        """Khách có sẵn địa chỉ mặc định, chatbot hỏi xác nhận và khách đồng ý."""
        UserAddress.objects.create(
            user=self.user,
            full_name='Nguyen Van Mac Dinh',
            phone='0977889900',
            address='Số 100 Nguyễn Trãi, Thanh Xuân, Hà Nội',
            is_default=True
        )
        self.client.force_login(self.user)

        # Lượt 1: Chatbot phát hiện địa chỉ mặc định
        r1 = self.client.post(
            '/chatbot/send/',
            json.dumps({'message': 'Mua 1kg cà rốt'}),
            content_type='application/json'
        )
        self.assertEqual(r1.status_code, 200)
        d1 = r1.json()
        self.assertIn('địa chỉ giao hàng sẵn có', d1['reply'])
        self.assertIn('Số 100 Nguyễn Trãi', d1['reply'])

        # Lượt 2: Khách nhắn "Đồng ý"
        r2 = self.client.post(
            '/chatbot/send/',
            json.dumps({'message': 'Đồng ý'}),
            content_type='application/json'
        )
        self.assertEqual(r2.status_code, 200)
        d2 = r2.json()
        self.assertIn('ĐẶT HÀNG THÀNH CÔNG', d2['reply'])
        self.assertIn('Số 100 Nguyễn Trãi', d2['reply'])

    def test_cancel_order_draft(self):
        """Khách đang lên đơn dở dang nhưng nhắn 'Thôi hủy không mua nữa'."""
        self.client.force_login(self.user)

        # Bắt đầu lên đơn
        self.client.post(
            '/chatbot/send/',
            json.dumps({'message': 'Đặt 2kg cà rốt'}),
            content_type='application/json'
        )

        # Hủy đơn
        r_cancel = self.client.post(
            '/chatbot/send/',
            json.dumps({'message': 'Thôi hủy, không mua nữa'}),
            content_type='application/json'
        )
        self.assertEqual(r_cancel.status_code, 200)
        data = r_cancel.json()
        self.assertIn('hủy yêu cầu lên đơn', data['reply'])

    def test_order_exceed_stock_warning(self):
        """Khách yêu cầu số lượng vượt quá tồn kho sẽ được cảnh báo thân thiện."""
        self.client.force_login(self.user)
        self.product.stock = 5
        self.product.save()

        resp = self.client.post(
            '/chatbot/send/',
            json.dumps({'message': 'Tôi muốn mua 20kg cà rốt'}),
            content_type='application/json'
        )
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertIn('chỉ còn', data['reply'])
        self.assertIn('5 kg', data['reply'])
