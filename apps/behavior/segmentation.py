# File: apps/behavior/segmentation.py
"""
Thuật toán phân loại và cập nhật phân nhóm khách hàng dựa trên hành vi (RFM-like rules):
- new: Khách mới đăng ký trong 7 ngày gần nhất chưa mua hàng.
- interested: Chưa mua nhưng có từ 5 tương tác (xem, tìm kiếm, giỏ hàng).
- loyal: Có từ 3 đơn hàng thành công trong 30 ngày qua.
- at_risk: Khách có nguy cơ rời bỏ (đơn hàng cuối cùng > 30 ngày).
- normal: Khách hàng mua sắm bình thường.
"""
from datetime import timedelta
from django.utils import timezone
from django.db.models import Max
from apps.accounts.models import User
from apps.behavior.models import UserEvent, UserSegment


def classify_user(user):
    """
    Phân loại nhóm khách hàng cho một người dùng cụ thể.
    """
    now = timezone.now()
    d30 = now - timedelta(days=30)
    d7 = now - timedelta(days=7)

    order_count = user.orders.exclude(status='cancelled').count()
    recent_orders = user.orders.exclude(status='cancelled').filter(created_at__gte=d30).count()
    last_order = user.orders.exclude(status='cancelled').aggregate(Max('created_at'))['created_at__max']
    event_count = UserEvent.objects.filter(user=user).count()

    if order_count == 0:
        if user.date_joined >= d7:
            return 'new', 'Đăng ký trong 7 ngày gần đây'
        if event_count >= 5:
            return 'interested', f'Có {event_count} tương tác nhưng chưa mua'
        return 'new', 'Chưa có đơn hàng'

    if recent_orders >= 3:
        return 'loyal', f'{recent_orders} đơn hàng trong 30 ngày'
    if last_order and last_order < d30:
        return 'at_risk', 'Không mua trong 30 ngày qua'
    return 'normal', 'Khách hàng bình thường'


def update_all_segments():
    """
    Quét toàn bộ người dùng đang kích hoạt để cập nhật phân nhóm và ghi nhận lịch sử UserSegment.
    """
    for user in User.objects.filter(is_active=True):
        new_seg, reason = classify_user(user)
        if user.segment != new_seg:
            user.segment = new_seg
            user.segment_updated_at = timezone.now()
            user.save(update_fields=['segment', 'segment_updated_at'])
            UserSegment.objects.create(user=user, segment=new_seg, reason=reason)
