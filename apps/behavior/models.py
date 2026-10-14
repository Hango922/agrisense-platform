# File: apps/behavior/models.py
"""
Ghi nhận hành vi người dùng, lịch sử phân nhóm khách hàng và log gợi ý nông sản AI.
"""
from django.db import models
from django.conf import settings


class UserEvent(models.Model):
    """
    Bảng behavior_userevent: Ghi nhận mọi tương tác của khách hàng trên hệ thống.
    """
    EVENT_TYPES = [
        ('view', 'Xem sản phẩm'),
        ('search', 'Tìm kiếm'),
        ('add_to_cart', 'Thêm vào giỏ'),
        ('purchase', 'Mua hàng'),
        ('review', 'Đánh giá'),
        ('chat', 'Chat với AI'),
    ]
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='events',
        verbose_name='Người dùng'
    )
    session_key = models.CharField(max_length=40, blank=True, db_index=True, verbose_name='Session Key')
    event_type = models.CharField(max_length=20, choices=EVENT_TYPES, db_index=True, verbose_name='Loại sự kiện')
    product = models.ForeignKey(
        'products.Product',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        verbose_name='Sản phẩm liên quan'
    )
    category = models.ForeignKey(
        'products.Category',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        verbose_name='Danh mục liên quan'
    )
    keyword = models.CharField(max_length=200, blank=True, verbose_name='Từ khóa tìm kiếm')
    metadata = models.JSONField(default=dict, blank=True, verbose_name='Dữ liệu phụ')
    created_at = models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='Thời gian ghi nhận')

    class Meta:
        db_table = 'behavior_userevent'
        ordering = ['-created_at']
        indexes = [models.Index(fields=['user', 'event_type', '-created_at'])]
        verbose_name = 'Sự kiện người dùng'
        verbose_name_plural = 'Danh sách sự kiện người dùng'

    def __str__(self):
        return f"{self.user or self.session_key} - {self.get_event_type_display()} - {self.created_at:%d/%m/%Y %H:%M}"


class UserSegment(models.Model):
    """
    Bảng behavior_usersegment: Lưu vết lịch sử thay đổi phân nhóm khách hàng bằng AI/rule.
    """
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='segment_history',
        verbose_name='Người dùng'
    )
    segment = models.CharField(max_length=20, verbose_name='Nhóm khách hàng')
    reason = models.CharField(max_length=200, blank=True, verbose_name='Lý do phân nhóm')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Thời gian phân nhóm')

    class Meta:
        db_table = 'behavior_usersegment'
        ordering = ['-created_at']
        verbose_name = 'Lịch sử phân nhóm'
        verbose_name_plural = 'Danh sách lịch sử phân nhóm'

    def __str__(self):
        return f"{self.user.username} -> {self.segment} ({self.created_at:%d/%m/%Y})"


class RecommendationLog(models.Model):
    """
    Bảng behavior_recommendationlog: Ghi vết kết quả gợi ý sản phẩm của thuật toán AI.
    """
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='recommendations',
        verbose_name='Người dùng'
    )
    product = models.ForeignKey(
        'products.Product',
        on_delete=models.CASCADE,
        verbose_name='Sản phẩm gợi ý'
    )
    reason = models.CharField(max_length=200, verbose_name='Lý do đề xuất')
    score = models.FloatField(default=0, verbose_name='Điểm tương đồng/độ ưu tiên')
    algorithm = models.CharField(max_length=50, default='content_based', verbose_name='Thuật toán')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Thời điểm gợi ý')

    class Meta:
        db_table = 'behavior_recommendationlog'
        ordering = ['-created_at']
        verbose_name = 'Nhật ký gợi ý AI'
        verbose_name_plural = 'Danh sách nhật ký gợi ý AI'

    def __str__(self):
        return f"Gợi ý {self.product.name} cho {self.user.username} ({self.score:.2f})"
