# File: apps/cart_orders/admin.py
"""
Đăng ký giao diện quản trị Django Admin cho phân hệ Giỏ hàng & Đơn hàng.
"""
from django import forms
from django.contrib import admin
from django.utils.html import format_html
from django.utils.safestring import mark_safe

from .models import Cart, CartItem, Order, OrderItem


class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 0
    readonly_fields = ('product', 'quantity', 'subtotal')

    def subtotal(self, obj):
        return f"{obj.subtotal():,} đ"
    subtotal.short_description = 'Thành tiền'


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('user', 'get_total_items', 'get_total_price', 'created_at', 'updated_at')
    inlines = [CartItemInline]

    def get_total_items(self, obj):
        return obj.total_items()
    get_total_items.short_description = 'Tổng số lượng'

    def get_total_price(self, obj):
        return f"{obj.total_price():,} đ"
    get_total_price.short_description = 'Tổng tiền hàng'


class OrderItemInline(admin.TabularInline):
    can_delete = False

    def has_add_permission(self, request, obj=None):
        return False

    model = OrderItem
    extra = 0
    readonly_fields = ('product', 'product_name', 'price', 'quantity', 'subtotal')




class OrderAdminForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = '__all__'

    def clean_payment_proof(self):
        from django.core.files.uploadedfile import UploadedFile

        from .forms import PaymentProofForm
        proof = self.cleaned_data.get('payment_proof')
        if isinstance(proof, UploadedFile):
            if self.instance.status != 'pending' or self.instance.payment_method != 'vietqr':
                raise forms.ValidationError('Chỉ tải bill cho đơn VietQR đang chờ xác nhận.')
            check = PaymentProofForm(files={'payment_proof': proof})
            if not check.is_valid():
                raise forms.ValidationError('Ảnh bill không hợp lệ.')
        elif proof is False and self.instance.status != 'pending':
            raise forms.ValidationError('Không thể xóa bill của đơn đã duyệt.')
        return proof


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    form = OrderAdminForm
    list_display = (
        'order_code', 'user', 'full_name', 'phone',
        'final_amount_formatted', 'payment_method', 'payment_proof_display', 'status', 'created_at'
    )
    list_filter = ('status', 'payment_method', 'created_at')
    search_fields = ('order_code', 'full_name', 'phone', 'user__username')
    inlines = [OrderItemInline]
    readonly_fields = ('user', 'order_code', 'full_name', 'phone', 'address', 'total_amount', 'discount_amount', 'shipping_fee', 'final_amount', 'payment_method', 'status', 'payment_proof_preview', 'payment_proof_uploaded_at', 'created_at', 'updated_at')
    actions = ['approve_orders_action']

    def final_amount_formatted(self, obj):
        return f"{obj.final_amount:,} đ"
    final_amount_formatted.short_description = 'Tổng thanh toán'

    def payment_proof_display(self, obj):
        if obj.payment_method == 'vietqr':
            if obj.payment_proof and hasattr(obj.payment_proof, 'url'):
                try:
                    url = obj.payment_proof.url
                    return format_html(
                        '<a href="{}" target="_blank" style="color: #059669; font-weight: 600; text-decoration: none;">'
                        '📸 Đã có bill <span style="font-size: 11px;">(Xem)</span></a>',
                        url
                    )
                except ValueError:
                    pass
            return mark_safe('<span style="color: #dc2626; font-weight: 600;">⚠️ Chưa có bill</span>')
        return mark_safe('<span style="color: #64748b;">COD (Tiền mặt)</span>')
    payment_proof_display.short_description = 'Bill chuyển khoản'

    def payment_proof_preview(self, obj):
        if obj.payment_proof and hasattr(obj.payment_proof, 'url'):
            try:
                url = obj.payment_proof.url
                return format_html(
                    '<a href="{0}" target="_blank">'
                    '<img src="{0}" style="max-height: 240px; border-radius: 8px; border: 1px solid #cbd5e1; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1);" />'
                    '</a><br><small style="color: #64748b;">Nhấn vào ảnh để xem kích thước đầy đủ</small>',
                    url
                )
            except ValueError:
                pass
        return "Chưa có ảnh bill chuyển khoản"
    payment_proof_preview.short_description = 'Xem trước bill chuyển khoản'

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def get_object(self, request, object_id, from_field=None):
        obj = super().get_object(request, object_id, from_field)
        if obj is not None and request.method == 'POST':
            return Order.objects.select_for_update().get(pk=obj.pk)
        return obj

    def save_model(self, request, obj, form, change):
        from django.utils import timezone
        if 'payment_proof' in form.changed_data:
            obj.payment_proof_uploaded_at = timezone.now() if obj.payment_proof else None
        super().save_model(request, obj, form, change)

    @admin.action(description='Duyệt đơn đã đối soát ngân hàng (hoặc COD)')
    def approve_orders_action(self, request, queryset):
        from django.db import transaction

        from .services import transition_order
        count = 0
        with transaction.atomic():
            for order in queryset.order_by('pk'):
                if order.status != 'pending':
                    continue
                try:
                    transition_order(order, 'confirmed', admin_verified=True, actor=request.user)
                    count += 1
                except ValueError as error:
                    self.message_user(request, str(error), level='ERROR')
        self.message_user(request, f'Đã duyệt {count} đơn hàng.')
