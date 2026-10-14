# File: apps/chatbot/views.py
"""
Views xử lý endpoint API Chatbot và giao diện xem lịch sử hội thoại.
"""
import json
from django.http import JsonResponse
from django.views import View
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import ChatSession, ChatMessage
from .services import call_ai


class ChatbotAPIView(View):
    """
    API tiếp nhận tin nhắn từ widget chat, gọi AI/fallback và phản hồi định dạng JSON.
    """
    def post(self, request):
        try:
            data = json.loads(request.body)
            message = data.get('message', '').strip()
        except (json.JSONDecodeError, AttributeError):
            return JsonResponse({'error': 'Invalid JSON'}, status=400)

        if not message:
            return JsonResponse({'error': 'Empty message'}, status=400)

        # Đảm bảo session key luôn tồn tại cho cả khách vãng lai và user đăng nhập
        if not request.session.session_key:
            request.session.create()
        session_key = request.session.session_key
        user = request.user if request.user.is_authenticated else None

        # Lấy hoặc tạo ChatSession tách biệt cho user vs anonymous
        if user:
            session, _ = ChatSession.objects.get_or_create(
                user=user,
                defaults={'session_key': session_key}
            )
        else:
            session, _ = ChatSession.objects.get_or_create(
                session_key=session_key,
                user=None
            )

        # Lưu tin nhắn người dùng
        ChatMessage.objects.create(session=session, role='user', content=message)

        # Gọi xử lý AI thông minh / Fallback
        text, is_fallback, elapsed = call_ai(message)

        # Lưu tin nhắn phản hồi của trợ lý
        ChatMessage.objects.create(
            session=session,
            role='assistant',
            content=text,
            is_fallback=is_fallback,
            response_time_ms=elapsed,
        )

        return JsonResponse({
            'reply': text,
            'is_fallback': is_fallback,
            'response_time_ms': elapsed,
        })


class ChatHistoryView(LoginRequiredMixin, TemplateView):
    """
    Trang xem lịch sử các phiên chat của người dùng đã đăng nhập.
    """
    template_name = 'chatbot/history.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['sessions'] = ChatSession.objects.filter(user=self.request.user).prefetch_related('messages')
        return ctx
