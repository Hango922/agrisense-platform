# File: apps/behavior/management/commands/update_segments.py
"""
Lệnh quản trị (Management Command) cập nhật phân nhóm khách hàng tự động:
Chạy bằng: python manage.py update_segments
"""
from django.core.management.base import BaseCommand
from apps.behavior.segmentation import update_all_segments


class Command(BaseCommand):
    help = 'Cập nhật phân nhóm khách hàng tự động dựa trên hành vi và lịch sử mua sắm'

    def handle(self, *args, **kwargs):
        update_all_segments()
        self.stdout.write(self.style.SUCCESS('✅ Đã cập nhật phân nhóm khách hàng thành công.'))
