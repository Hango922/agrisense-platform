# File: apps/accounts/forms.py
"""
Biểu mẫu đăng ký và quản lý thông tin tài khoản người dùng.
"""
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User


class RegisterForm(UserCreationForm):
    """
    Form đăng ký tài khoản khách hàng mới cho AgriSense.
    """
    email = forms.EmailField(required=True, label='Địa chỉ Email')
    phone = forms.CharField(max_length=15, required=False, label='Số điện thoại')

    class Meta:
        model = User
        fields = ('username', 'email', 'phone', 'password1', 'password2')
