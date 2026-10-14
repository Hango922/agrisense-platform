# File: apps/dashboard/views.py
"""
Views cho trang quản trị riêng (Dashboard) của Admin:
Thống kê doanh thu, đơn hàng, khách hàng, hành vi AI và truy xuất nguồn gốc.
Sử dụng staff_member_required để phân quyền quản trị viên / nhân viên.
"""
import io
import json
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from django.views.generic import TemplateView
from django.views import View
from django.http import HttpResponse
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
    Trang tổng quan Dashboard: Doanh thu 30 ngày, biểu đồ xu hướng Chart.js,
    phân nhóm khách hàng AI và top nông sản bán chạy.
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

        # 1. Dữ liệu biểu đồ doanh thu 30 ngày (sử dụng Python timezone để tương thích tuyệt đối MySQL trên Windows)
        today = timezone.now().date()
        daily_revenue_map = {today - timedelta(days=i): 0.0 for i in range(29, -1, -1)}
        recent_orders = (
            Order.objects.filter(created_at__gte=timezone.now() - timedelta(days=30))
            .exclude(status='cancelled')
            .values('created_at', 'final_amount')
        )
        for ord_val in recent_orders:
            dt_local = timezone.localtime(ord_val['created_at']).date()
            if dt_local in daily_revenue_map:
                daily_revenue_map[dt_local] += float(ord_val['final_amount'] or 0)

        chart_revenue_labels = [d.strftime('%d/%m') for d in daily_revenue_map.keys()]
        chart_revenue_data = list(daily_revenue_map.values())

        # 2. Phân nhóm khách hàng AI cho biểu đồ tròn (Doughnut Chart)
        segment_labels_map = {
            'new': 'Khách mới',
            'interested': 'Quan tâm',
            'loyal': 'Thường xuyên',
            'at_risk': 'Nguy cơ rời bỏ',
        }
        segments_raw = list(User.objects.filter(is_staff=False).values('segment').annotate(count=Count('id')))
        ctx['segments'] = segments_raw

        chart_segment_labels = []
        chart_segment_data = []
        for s in segments_raw:
            seg_code = s['segment'] or 'other'
            chart_segment_labels.append(segment_labels_map.get(seg_code, 'Khác' if seg_code == 'other' else seg_code))
            chart_segment_data.append(s['count'])

        # 3. Top 5 nông sản bán chạy cho biểu đồ cột (Bar Chart)
        top_items = list(ctx['top_products'][:5])
        chart_top_labels = [item['product_name'] for item in top_items]
        chart_top_data = [int(item['total'] or 0) for item in top_items]

        # Truyền dạng chuỗi JSON an toàn cho JavaScript
        ctx['chart_revenue_labels'] = json.dumps(chart_revenue_labels)
        ctx['chart_revenue_data'] = json.dumps(chart_revenue_data)
        ctx['chart_segment_labels'] = json.dumps(chart_segment_labels)
        ctx['chart_segment_data'] = json.dumps(chart_segment_data)
        ctx['chart_top_labels'] = json.dumps(chart_top_labels)
        ctx['chart_top_data'] = json.dumps(chart_top_data)

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


@method_decorator(staff_member_required, name='dispatch')
class ExportOrdersExcelView(View):
    """
    Xuất báo cáo toàn bộ danh sách đơn hàng ra file Excel (.xlsx) chuẩn chỉnh.
    Được định dạng chuyên nghiệp với Header màu thương hiệu, viền ô và căn lề tự động.
    """
    def get(self, request, *args, **kwargs):
        wb = openpyxl.Workbook()
        ws = wb.active
        ws.title = "Báo Cáo Đơn Hàng"

        # Định dạng Header
        header_font = Font(name="Segoe UI", size=11, bold=True, color="FFFFFF")
        header_fill = PatternFill(start_color="10B981", end_color="10B981", fill_type="solid")
        header_align = Alignment(horizontal="center", vertical="center", wrap_text=True)

        headers = [
            "STT", "Mã đơn hàng", "Ngày đặt", "Khách hàng", "SĐT nhận hàng",
            "Địa chỉ giao hàng", "Tiền hàng (đ)", "Phí vận chuyển (đ)", "Tổng thanh toán (đ)",
            "Trạng thái", "Phương thức", "Ghi chú"
        ]
        ws.append(headers)

        for col_idx in range(1, len(headers) + 1):
            cell = ws.cell(row=1, column=col_idx)
            cell.font = header_font
            cell.fill = header_fill
            cell.alignment = header_align

        status_map = dict(Order.STATUS_CHOICES)
        pay_map = dict(Order.PAYMENT_CHOICES)

        orders = Order.objects.all().order_by('-created_at')
        thin_border = Border(
            left=Side(style='thin', color='E2E8F0'),
            right=Side(style='thin', color='E2E8F0'),
            top=Side(style='thin', color='E2E8F0'),
            bottom=Side(style='thin', color='E2E8F0')
        )

        for idx, ord in enumerate(orders, 1):
            created_str = timezone.localtime(ord.created_at).strftime('%d/%m/%Y %H:%M') if ord.created_at else ''
            row = [
                idx,
                ord.order_code,
                created_str,
                ord.full_name or (ord.user.username if ord.user else 'Khách'),
                ord.phone,
                ord.address,
                float(ord.total_amount),
                float(ord.shipping_fee),
                float(ord.final_amount),
                status_map.get(ord.status, ord.status),
                pay_map.get(ord.payment_method, ord.payment_method),
                ord.note or ''
            ]
            ws.append(row)
            row_idx = idx + 1
            for col_idx in range(1, len(row) + 1):
                cell = ws.cell(row=row_idx, column=col_idx)
                cell.border = thin_border
                if col_idx in [7, 8, 9]:
                    cell.number_format = '#,##0'
                    cell.alignment = Alignment(horizontal='right')
                elif col_idx in [1, 3, 5, 10, 11]:
                    cell.alignment = Alignment(horizontal='center')

        # Tự động căn chỉnh độ rộng cột
        for col in ws.columns:
            max_len = max(len(str(cell.value or '')) for cell in col)
            col_letter = openpyxl.utils.get_column_letter(col[0].column)
            ws.column_dimensions[col_letter].width = max(max_len + 3, 12)

        buffer = io.BytesIO()
        wb.save(buffer)
        buffer.seek(0)

        filename = f"AgriSense_Orders_{timezone.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
        response = HttpResponse(
            buffer.getvalue(),
            content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
        response['Content-Disposition'] = f'attachment; filename="{filename}"'
        return response
