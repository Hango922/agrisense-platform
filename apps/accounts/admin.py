# File: apps/accounts/admin.py
"""
Đăng ký giao diện quản trị Django Admin cho phân hệ Tài khoản người dùng.
"""
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, UserAddress


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ('username', 'email', 'phone', 'segment', 'is_staff', 'is_active', 'created_at')
    list_filter = ('segment', 'is_staff', 'is_superuser', 'is_active')
    search_fields = ('username', 'email', 'phone')
    ordering = ('-created_at',)
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Thông tin bổ sung AgriSense', {
            'fields': ('phone', 'segment', 'segment_updated_at')
        }),
    )
    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        ('Thông tin bổ sung AgriSense', {
            'fields': ('phone', 'segment')
        }),
    )


@admin.register(UserAddress)
class UserAddressAdmin(admin.ModelAdmin):
    list_display = ('user', 'full_name', 'phone', 'is_default', 'created_at')
    list_filter = ('is_default', 'created_at')
    search_fields = ('user__username', 'full_name', 'phone', 'address')
