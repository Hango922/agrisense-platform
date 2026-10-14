# File: apps/accounts/models.py
"""
Quản lý tài khoản người dùng và sổ địa chỉ giao hàng trong hệ thống AgriSense.
"""
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """
    Bảng accounts_user: Tài khoản người dùng với phân nhóm hành vi tự động bằng AI.
    """
    SEGMENT_CHOICES = [
        ('new', 'Khách mới'),
        ('interested', 'Khách quan tâm'),
        ('loyal', 'Khách mua thường xuyên'),
        ('at_risk', 'Khách có nguy cơ rời bỏ'),
        ('normal', 'Khách bình thường'),
    ]
    phone = models.CharField(max_length=15, blank=True, verbose_name='Số điện thoại')
    segment = models.CharField(
        max_length=20,
        choices=SEGMENT_CHOICES,
        default='new',
        db_index=True,
        verbose_name='Phân nhóm khách hàng'
    )
    segment_updated_at = models.DateTimeField(null=True, blank=True, verbose_name='Thời gian cập nhật nhóm')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Ngày tạo')

    class Meta:
        db_table = 'accounts_user'
        verbose_name = 'Người dùng'
        verbose_name_plural = 'Danh sách người dùng'

    def __str__(self):
        return self.username


class UserAddress(models.Model):
    """
    Bảng accounts_useraddress: Địa chỉ nhận hàng của khách hàng.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='addresses', verbose_name='Người dùng')
    full_name = models.CharField(max_length=100, verbose_name='Họ và tên người nhận')
    phone = models.CharField(max_length=15, verbose_name='Số điện thoại người nhận')
    address = models.TextField(verbose_name='Địa chỉ chi tiết')
    is_default = models.BooleanField(default=False, verbose_name='Địa chỉ mặc định')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Ngày tạo')

    class Meta:
        db_table = 'accounts_useraddress'
        ordering = ['-is_default', '-created_at']
        verbose_name = 'Địa chỉ giao hàng'
        verbose_name_plural = 'Danh sách địa chỉ giao hàng'

    def __str__(self):
        return f"{self.full_name} - {self.phone}"
