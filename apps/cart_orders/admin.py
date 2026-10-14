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


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        'order_code', 'user', 'full_name', 'phone',
        'final_amount_formatted', 'payment_method', 'status', 'created_at'
    )
    list_filter = ('status', 'payment_method', 'created_at')
    search_fields = ('order_code', 'full_name', 'phone', 'user__username')
    inlines = [OrderItemInline]
    readonly_fields = ('order_code', 'created_at', 'updated_at')

    def final_amount_formatted(self, obj):
        return f"{obj.final_amount:,} đ"
    final_amount_formatted.short_description = 'Tổng thanh toán'
