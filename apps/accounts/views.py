# File: apps/accounts/views.py
"""
Views xử lý đăng ký, đăng nhập, đăng xuất và xem hồ sơ người dùng.
"""
from django.shortcuts import redirect
from django.contrib.auth import login, logout
from django.contrib.auth.views import LoginView as DjangoLoginView
from django.views.generic import CreateView, TemplateView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import RegisterForm


class RegisterView(CreateView):
    """
    Trang đăng ký tài khoản khách hàng mới và tự động đăng nhập khi đăng ký thành công.
    """
    form_class = RegisterForm
    template_name = 'accounts/register.html'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return super().form_valid(form)


class LoginView(DjangoLoginView):
    """
    Trang đăng nhập hệ thống với giao diện Bootstrap 5.
    Tự động chuyển hướng Admin vào Dashboard và Khách hàng về Trang chủ.
    """
    template_name = 'accounts/login.html'

    def get_success_url(self):
        redirect_to = self.get_redirect_url()
        if redirect_to:
            return redirect_to
        if self.request.user.is_staff or self.request.user.is_superuser:
            return reverse_lazy('dashboard:home')
        return reverse_lazy('home')


class LogoutView(TemplateView):
    """
    Xử lý đăng xuất tài khoản và chuyển hướng về trang chủ.
    """
    def get(self, request):
        logout(request)
        return redirect('home')

    def post(self, request):
        logout(request)
        return redirect('home')


class ProfileView(LoginRequiredMixin, TemplateView):
    """
    Trang thông tin tài khoản, phân nhóm khách hàng và sổ địa chỉ.
    """
    template_name = 'accounts/profile.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['addresses'] = self.request.user.addresses.all()
        return ctx
