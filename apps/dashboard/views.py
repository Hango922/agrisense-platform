# File: apps/dashboard/views.py
"""
Views cho trang quản trị riêng (Dashboard) của Admin:
Thống kê doanh thu, đơn hàng, khách hàng, hành vi AI và truy xuất nguồn gốc.
Sử dụng staff_member_required để phân quyền quản trị viên / nhân viên.
"""
from django.views.generic import TemplateView
from django.contrib.admin.views.decorators import staff_member_required
from django.utils.decorators import method_decorator
from django.db.models import Sum, Count
from datetime import timedelta
from django.utils import timezone
from apps.accounts.models import User
from apps.products.models import Product
from apps.cart_orders.models import Order, OrderItem
from apps.behavior.models import UserEvent
from apps.traceability.models import ProductBatch


@method_decorator(staff_member_required, name='dispatch')
class DashboardHomeView(TemplateView):
    """
    Trang tổng quan Dashboard: Doanh thu 30 ngày, tổng đơn, khách hàng, sản phẩm bán chạy và phân nhóm AI.
    """
    template_name = 'dashboard/index.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        d30 = timezone.now() - timedelta(days=30)
        orders_30d = Order.objects.filter(created_at__gte=d30).exclude(status='cancelled')
        ctx['total_revenue'] = orders_30d.aggregate(s=Sum('final_amount'))['s'] or 0
        ctx['total_orders'] = orders_30d.count()
        ctx['total_customers'] = User.objects.filter(is_staff=False).count()
        ctx['total_products'] = Product.objects.filter(is_active=True).count()
        ctx['top_products'] = (
            OrderItem.objects.filter(order__created_at__gte=d30)
            .values('product_name').annotate(total=Sum('quantity')).order_by('-total')[:10]
        )
        ctx['segments'] = User.objects.filter(is_staff=False).values('segment').annotate(count=Count('id'))
        return ctx


@method_decorator(staff_member_required, name='dispatch')
class DashboardProductsView(TemplateView):
    """
    Quản lý danh sách nông sản và tồn kho.
    """
    template_name = 'dashboard/products.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['products'] = Product.objects.all().order_by('-created_at')
        return ctx


@method_decorator(staff_member_required, name='dispatch')
class DashboardOrdersView(TemplateView):
    """
    Quản lý và theo dõi 100 đơn hàng mới nhất.
    """
    template_name = 'dashboard/orders.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['orders'] = Order.objects.all().order_by('-created_at')[:100]
        return ctx


@method_decorator(staff_member_required, name='dispatch')
class DashboardCustomersView(TemplateView):
    """
    Quản lý danh sách người dùng và phân loại nhóm hành vi.
    """
    template_name = 'dashboard/customers.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['customers'] = User.objects.filter(is_staff=False).order_by('-date_joined')
        return ctx


@method_decorator(staff_member_required, name='dispatch')
class DashboardBehaviorView(TemplateView):
    """
    Thống kê tần suất sự kiện hành vi trong 30 ngày và 50 sự kiện mới nhất.
    """
    template_name = 'dashboard/behavior.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        d30 = timezone.now() - timedelta(days=30)
        ctx['event_counts'] = (
            UserEvent.objects.filter(created_at__gte=d30)
            .values('event_type').annotate(count=Count('id'))
        )
        ctx['recent_events'] = UserEvent.objects.all().order_by('-created_at')[:50]
        return ctx


@method_decorator(staff_member_required, name='dispatch')
class DashboardTraceabilityView(TemplateView):
    """
    Quản lý lô hàng nông sản và danh sách mã QR truy xuất.
    """
    template_name = 'dashboard/traceability.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['batches'] = ProductBatch.objects.all().order_by('-created_at')
        return ctx
