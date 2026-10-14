# File: apps/chatbot/models.py
"""
Quản lý phiên hội thoại và lịch sử tin nhắn Chatbot AI tư vấn nông sản.
"""
from django.db import models
from django.conf import settings


class ChatSession(models.Model):
    """
    Bảng chatbot_chatsession: Phiên chat giữa khách hàng và trợ lý AI.
    """
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='chat_sessions',
        verbose_name='Người dùng'
    )
    session_key = models.CharField(max_length=40, blank=True, db_index=True, verbose_name='Session Key')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Thời gian bắt đầu')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Thời gian cập nhật')

    class Meta:
        db_table = 'chatbot_chatsession'
        verbose_name = 'Phiên hội thoại AI'
        verbose_name_plural = 'Danh sách phiên hội thoại AI'

    def __str__(self):
        return f"Session #{self.id} ({self.user.username if self.user else 'Khách'})"


class ChatMessage(models.Model):
    """
    Bảng chatbot_chatmessage: Từng tin nhắn gửi và nhận trong phiên hội thoại.
    """
    ROLE_CHOICES = [
        ('user', 'Người dùng'),
        ('assistant', 'Chatbot'),
        ('system', 'Hệ thống'),
    ]
    session = models.ForeignKey(
        ChatSession,
        on_delete=models.CASCADE,
        related_name='messages',
        verbose_name='Phiên hội thoại'
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, verbose_name='Vai trò')
    content = models.TextField(verbose_name='Nội dung tin nhắn')
    is_fallback = models.BooleanField(default=False, verbose_name='Dùng phản hồi fallback rule-based')
    tokens_used = models.IntegerField(default=0, verbose_name='Số token tiêu thụ')
    response_time_ms = models.IntegerField(default=0, verbose_name='Thời gian phản hồi (ms)')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Thời gian gửi')

    class Meta:
        db_table = 'chatbot_chatmessage'
        ordering = ['created_at']
        verbose_name = 'Tin nhắn chat'
        verbose_name_plural = 'Danh sách tin nhắn chat'

    def __str__(self):
        return f"[{self.get_role_display()}] {self.content[:30]}..."
