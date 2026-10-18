# File: apps/cart_orders/admin.py
"""
Đăng ký giao diện quản trị Django Admin cho phân hệ Giỏ hàng & Đơn hàng.
"""
from django.contrib import admin
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
    model = OrderItem
    extra = 0
    readonly_fields = ('product', 'product_name', 'price', 'quantity', 'subtotal')


from django.utils.html import format_html


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        'order_code', 'user', 'full_name', 'phone',
        'final_amount_formatted', 'payment_method', 'payment_proof_display', 'status', 'created_at'
    )
    list_filter = ('status', 'payment_method', 'created_at')
    search_fields = ('order_code', 'full_name', 'phone', 'user__username')
    inlines = [OrderItemInline]
    readonly_fields = ('order_code', 'payment_proof_preview', 'payment_proof_uploaded_at', 'created_at', 'updated_at')
    actions = ['approve_orders_action']

    def final_amount_formatted(self, obj):
        return f"{obj.final_amount:,} đ"
    final_amount_formatted.short_description = 'Tổng thanh toán'

    def payment_proof_display(self, obj):
        if obj.payment_method == 'vietqr':
            if obj.payment_proof:
                return format_html(
                    '<a href="{}" target="_blank" style="color: #059669; font-weight: 600; text-decoration: none;">'
                    '📸 Đã có bill <span style="font-size: 11px;">(Xem)</span></a>',
                    obj.payment_proof.url
                )
            return format_html('<span style="color: #dc2626; font-weight: 600;">⚠️ Chưa có bill</span>')
        return format_html('<span style="color: #64748b;">COD (Tiền mặt)</span>')
    payment_proof_display.short_description = 'Bill chuyển khoản'

    def payment_proof_preview(self, obj):
        if obj.payment_proof:
            return format_html(
                '<a href="{0}" target="_blank">'
                '<img src="{0}" style="max-height: 240px; border-radius: 8px; border: 1px solid #cbd5e1; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1);" />'
                '</a><br><small style="color: #64748b;">Nhấn vào ảnh để xem kích thước đầy đủ</small>',
                obj.payment_proof.url
            )
        return "Chưa có ảnh bill chuyển khoản"
    payment_proof_preview.short_description = 'Xem trước bill chuyển khoản'

    def save_model(self, request, obj, form, change):
        from django.utils import timezone
        if obj.payment_method == 'vietqr' and obj.status in ('confirmed', 'shipping', 'delivered') and not obj.payment_proof:
            from .services import generate_admin_verification_bill
            proof_file = generate_admin_verification_bill(obj.order_code, admin_username=request.user.username)
            obj.payment_proof.save(f"admin_verified_{obj.order_code}.png", proof_file, save=False)
            obj.payment_proof_uploaded_at = timezone.now()
            note_line = f"[Admin {request.user.username} đã đối soát ngân hàng qua Django Admin lúc {timezone.now().strftime('%d/%m/%Y %H:%M')}]"
            obj.note = (obj.note + "\n" + note_line).strip() if obj.note else note_line
        super().save_model(request, obj, form, change)

    @admin.action(description="Duyệt các đơn hàng đã chọn (Admin đối soát thành công)")
    def approve_orders_action(self, request, queryset):
        from django.utils import timezone
        from .services import generate_admin_verification_bill
        count = 0
        for order in queryset:
            if order.status == 'pending':
                if order.payment_method == 'vietqr' and not order.payment_proof:
                    proof_file = generate_admin_verification_bill(order.order_code, admin_username=request.user.username)
                    order.payment_proof.save(f"admin_verified_{order.order_code}.png", proof_file, save=False)
                    order.payment_proof_uploaded_at = timezone.now()
                    note_line = f"[Admin {request.user.username} duyệt hàng loạt lúc {timezone.now().strftime('%d/%m/%Y %H:%M')}]"
                    order.note = (order.note + "\n" + note_line).strip() if order.note else note_line
                order.status = 'confirmed'
                order.save()
                count += 1
        self.message_user(request, f"✅ Đã duyệt thành công {count} đơn hàng!")

