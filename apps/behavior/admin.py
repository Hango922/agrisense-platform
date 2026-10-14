# File: apps/behavior/admin.py
"""
Đăng ký giao diện quản trị Django Admin cho phân hệ Hành vi người dùng & Phân nhóm AI.
"""
from django.contrib import admin
from .models import UserEvent, UserSegment, RecommendationLog


@admin.register(UserEvent)
class UserEventAdmin(admin.ModelAdmin):
    list_display = ('user', 'session_key', 'event_type', 'product', 'category', 'keyword', 'created_at')
    list_filter = ('event_type', 'created_at')
    search_fields = ('user__username', 'session_key', 'keyword', 'product__name')
    readonly_fields = ('created_at',)


@admin.register(UserSegment)
class UserSegmentAdmin(admin.ModelAdmin):
    list_display = ('user', 'segment', 'reason', 'created_at')
    list_filter = ('segment', 'created_at')
    search_fields = ('user__username', 'reason')
    readonly_fields = ('created_at',)


@admin.register(RecommendationLog)
class RecommendationLogAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'score', 'algorithm', 'reason', 'created_at')
    list_filter = ('algorithm', 'created_at')
    search_fields = ('user__username', 'product__name', 'reason')
    readonly_fields = ('created_at',)
