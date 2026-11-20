# File: apps/products/admin.py
"""
Đăng ký giao diện quản trị Django Admin cho phân hệ Sản phẩm & Danh mục.
"""
from django.contrib import admin

from .models import Category, ComboItem, Product, ProductReview, SeasonalCombo, Supplier


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'created_at')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name',)


@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'certification', 'created_at')
    search_fields = ('name', 'phone', 'certification')


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'unit', 'stock', 'is_active')
    list_filter = ('category', 'is_active', 'season')
    search_fields = ('name', 'origin', 'description')
    prepopulated_fields = {'slug': ('name',)}

    def get_readonly_fields(self, request, obj=None):
        return ('stock',) if obj and obj.track_batches else ()


class ComboItemInline(admin.TabularInline):
    model = ComboItem
    extra = 1


@admin.register(SeasonalCombo)
class SeasonalComboAdmin(admin.ModelAdmin):
    list_display = ('name', 'season_label', 'is_active')
    prepopulated_fields = {'slug': ('name',)}
    inlines = (ComboItemInline,)


@admin.register(ProductReview)
class ProductReviewAdmin(admin.ModelAdmin):
    list_display = ('product', 'user', 'rating', 'created_at')
    list_filter = ('rating', 'created_at')
    search_fields = ('product__name', 'user__username', 'comment')
