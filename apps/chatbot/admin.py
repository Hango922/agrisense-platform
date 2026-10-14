# File: apps/chatbot/admin.py
"""
Đăng ký giao diện quản trị Django Admin cho phân hệ Chatbot AI tư vấn nông sản.
"""
from django.contrib import admin
from .models import ChatSession, ChatMessage


class ChatMessageInline(admin.TabularInline):
    model = ChatMessage
    extra = 0
    readonly_fields = ('role', 'content', 'is_fallback', 'tokens_used', 'response_time_ms', 'created_at')


@admin.register(ChatSession)
class ChatSessionAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'session_key', 'created_at', 'updated_at')
    search_fields = ('user__username', 'session_key')
    inlines = [ChatMessageInline]


@admin.register(ChatMessage)
class ChatMessageAdmin(admin.ModelAdmin):
    list_display = ('session', 'role', 'content_preview', 'is_fallback', 'tokens_used', 'response_time_ms', 'created_at')
    list_filter = ('role', 'is_fallback', 'created_at')
    search_fields = ('content', 'session__user__username')
    readonly_fields = ('created_at',)

    def content_preview(self, obj):
        return obj.content[:50] + '...' if len(obj.content) > 50 else obj.content
    content_preview.short_description = 'Nội dung tin nhắn'
