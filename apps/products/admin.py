# File: apps/products/admin.py
"""
Đăng ký giao diện quản trị Django Admin cho phân hệ Sản phẩm & Danh mục.
"""
from django.contrib import admin
from .models import Category, Supplier, Product, ProductReview


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


@admin.register(ProductReview)
class ProductReviewAdmin(admin.ModelAdmin):
    list_display = ('product', 'user', 'rating', 'created_at')
    list_filter = ('rating', 'created_at')
    search_fields = ('product__name', 'user__username', 'comment')
