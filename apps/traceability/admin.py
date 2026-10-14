# File: apps/traceability/admin.py
"""
Đăng ký giao diện quản trị Django Admin cho phân hệ Truy xuất nguồn gốc & Mã QR.
"""
from django.contrib import admin
from .models import ProductBatch, TraceabilityRecord


class TraceabilityRecordInline(admin.TabularInline):
    model = TraceabilityRecord
    extra = 0
    readonly_fields = ('field_changed', 'old_value', 'new_value', 'changed_by', 'changed_at')


@admin.register(ProductBatch)
class ProductBatchAdmin(admin.ModelAdmin):
    list_display = (
        'batch_code', 'product', 'planting_location',
        'harvest_date', 'packaging_date', 'expiry_date', 'certification', 'created_at'
    )
    list_filter = ('certification', 'harvest_date', 'created_at')
    search_fields = ('batch_code', 'product__name', 'planting_location', 'certification')
    inlines = [TraceabilityRecordInline]


@admin.register(TraceabilityRecord)
class TraceabilityRecordAdmin(admin.ModelAdmin):
    list_display = ('batch', 'field_changed', 'changed_by', 'changed_at')
    list_filter = ('field_changed', 'changed_at')
    search_fields = ('batch__batch_code', 'field_changed', 'changed_by__username')
    readonly_fields = ('changed_at',)
