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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs.update({
                'class': 'form-control',
            })
        if 'username' in self.fields:
            self.fields['username'].widget.attrs.update({'placeholder': 'Ví dụ: nguyenvana'})
        if 'email' in self.fields:
            self.fields['email'].widget.attrs.update({'placeholder': 'example@gmail.com'})
        if 'phone' in self.fields:
            self.fields['phone'].widget.attrs.update({'placeholder': 'Ví dụ: 0912345678'})
        if 'password1' in self.fields:
            self.fields['password1'].widget.attrs.update({'placeholder': 'Nhập mật khẩu an toàn'})
        if 'password2' in self.fields:
            self.fields['password2'].widget.attrs.update({'placeholder': 'Nhập lại mật khẩu để xác nhận'})
