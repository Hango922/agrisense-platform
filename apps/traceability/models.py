# File: apps/traceability/models.py
"""
Quản lý lô hàng nông sản, mã QR truy xuất và lịch sử cập nhật nguồn gốc.
"""
from django.db import models
from django.conf import settings


class ProductBatch(models.Model):
    """
    Bảng traceability_productbatch: Lô hàng nông sản được gán mã truy xuất nguồn gốc.
    """
    product = models.ForeignKey(
        'products.Product',
        on_delete=models.CASCADE,
        related_name='batches',
        verbose_name='Sản phẩm'
    )
    batch_code = models.CharField(max_length=50, unique=True, db_index=True, verbose_name='Mã lô hàng')
    qr_code = models.ImageField(upload_to='qr_codes/', blank=True, null=True, verbose_name='Ảnh mã QR')
    planting_location = models.CharField(max_length=200, verbose_name='Vùng trồng / Địa chỉ nông trại')
    harvest_date = models.DateField(verbose_name='Ngày thu hoạch')
    packaging_date = models.DateField(verbose_name='Ngày đóng gói')
    expiry_date = models.DateField(null=True, blank=True, verbose_name='Hạn sử dụng')
    certification = models.CharField(max_length=200, blank=True, verbose_name='Chứng nhận an toàn')
    quantity = models.CharField(max_length=50, blank=True, verbose_name='Sản lượng lô hàng')
    notes = models.TextField(blank=True, verbose_name='Nhật ký chăm sóc / Ghi chú')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Ngày tạo')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Ngày cập nhật')

    class Meta:
        db_table = 'traceability_productbatch'
        ordering = ['-created_at']
        verbose_name = 'Lô hàng nông sản'
        verbose_name_plural = 'Danh sách lô hàng'

    def __str__(self):
        return f"{self.batch_code} - {self.product.name}"


class TraceabilityRecord(models.Model):
    """
    Bảng traceability_traceabilityrecord: Lưu nhật ký kiểm định hoặc thay đổi trạng thái của lô hàng.
    """
    batch = models.ForeignKey(
        ProductBatch,
        on_delete=models.CASCADE,
        related_name='history',
        verbose_name='Lô hàng'
    )
    field_changed = models.CharField(max_length=100, verbose_name='Thuộc tính thay đổi')
    old_value = models.TextField(blank=True, verbose_name='Giá trị cũ')
    new_value = models.TextField(blank=True, verbose_name='Giá trị mới')
    changed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        verbose_name='Người thực hiện'
    )
    changed_at = models.DateTimeField(auto_now_add=True, verbose_name='Thời gian thay đổi')

    class Meta:
        db_table = 'traceability_traceabilityrecord'
        ordering = ['-changed_at']
        verbose_name = 'Lịch sử truy xuất lô hàng'
        verbose_name_plural = 'Danh sách lịch sử truy xuất'

    def __str__(self):
        return f"{self.batch.batch_code} - Thay đổi {self.field_changed} ({self.changed_at:%d/%m/%Y})"
