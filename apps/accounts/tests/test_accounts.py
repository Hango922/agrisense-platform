# File: apps/accounts/tests/test_accounts.py
"""
Kiểm thử mô hình User tùy chỉnh và sổ địa chỉ giao hàng UserAddress.
"""
from django.test import TestCase
from apps.accounts.models import User, UserAddress


class AccountTests(TestCase):
    def test_create_user_default_segment(self):
        user = User.objects.create_user(
            username='test_user',
            email='test@example.com',
            password='Password@123',
            phone='0912345678'
        )
        self.assertEqual(user.segment, 'new')
        self.assertEqual(user.phone, '0912345678')
        self.assertEqual(str(user), 'test_user')

    def test_user_address_ordering(self):
        user = User.objects.create_user(username='addr_user', password='Password@123')
        addr1 = UserAddress.objects.create(
            user=user,
            full_name='Nguyen Van A',
            phone='0987654321',
            address='123 Nguyen Trai, Ha Noi',
            is_default=False
        )
        addr2 = UserAddress.objects.create(
            user=user,
            full_name='Nguyen Van A',
            phone='0987654321',
            address='456 Le Loi, Ha Noi',
            is_default=True
        )
        # Sổ địa chỉ phải ưu tiên địa chỉ mặc định lên đầu
        addresses = list(user.addresses.all())
        self.assertEqual(addresses[0], addr2)
        self.assertEqual(addresses[1], addr1)
