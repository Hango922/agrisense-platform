# File: apps/traceability/views.py
"""
Views hiển thị trang truy xuất nguồn gốc công khai cho người tiêu dùng:
- Tra cứu danh sách lô hàng hoặc tìm theo mã lô tại /trace/
- Xem chi tiết Hộ Chiếu Nông Sản Số của từng lô tại /trace/<batch_code>/
"""
from django.views.generic import DetailView, ListView
from django.shortcuts import get_object_or_404
from django.db.models import Q
from .models import ProductBatch


class TraceIndexView(ListView):
    """
    Trung tâm Tra Cứu Hộ Chiếu Nông Sản Số dành cho khách hàng:
    - Tìm kiếm theo mã lô, tên nông sản, vùng trồng
    - Duyệt danh sách các lô hàng đang lưu hành
    """
    model = ProductBatch
    template_name = 'traceability/trace_index.html'
    context_object_name = 'batches'
    paginate_by = 12

    def get_queryset(self):
        q = self.request.GET.get('q', '').strip()
        qs = ProductBatch.objects.select_related('product', 'product__supplier', 'product__category').all().order_by('-created_at')
        if q:
            qs = qs.filter(
                Q(batch_code__icontains=q) |
                Q(product__name__icontains=q) |
                Q(planting_location__icontains=q)
            )
        return qs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['query'] = self.request.GET.get('q', '')
        ctx['total_count'] = ProductBatch.objects.count()
        return ctx


class PublicTraceView(DetailView):
    """
    Trang thông tin minh bạch nguồn gốc lô hàng khi quét mã QR từ bao bì hoặc xem từ web.
    """
    model = ProductBatch
    template_name = 'traceability/public_trace.html'
    context_object_name = 'batch'

    def get_object(self):
        return get_object_or_404(ProductBatch, batch_code=self.kwargs['batch_code'])

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['history'] = self.object.history.all()
        return ctx
