# File: apps/traceability/views.py
"""
Views hiển thị trang truy xuất nguồn gốc công khai cho người tiêu dùng quét mã QR.
"""
from django.views.generic import DetailView
from django.shortcuts import get_object_or_404
from .models import ProductBatch


class PublicTraceView(DetailView):
    """
    Trang thông tin minh bạch nguồn gốc lô hàng khi quét mã QR từ bao bì.
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
