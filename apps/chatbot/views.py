# File: apps/chatbot/views.py
"""
Views xử lý endpoint API Chatbot và giao diện xem lịch sử hội thoại.
"""
import json

from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.sessions.backends.db import SessionStore
from django.db import transaction
from django.http import JsonResponse
from django.views import View
from django.views.generic import TemplateView

from .models import ChatMessage, ChatSession
from .services import call_ai


class ChatbotAPIView(View):
    """
    API tiếp nhận tin nhắn từ widget chat, gọi AI/fallback và phản hồi định dạng JSON.
    """
    def post(self, request):
        if request.user.is_authenticated:
            with transaction.atomic():
                get_user_model().objects.select_for_update().get(pk=request.user.pk)
                request.session = SessionStore(session_key=request.session.session_key)
                response = self.handle_message(request)
                request.session.save()
                return response
        return self.handle_message(request)

    def handle_message(self, request):
        try:
            data = json.loads(request.body)
            message = data.get('message', '').strip()
        except (json.JSONDecodeError, AttributeError):
            return JsonResponse({'error': 'Invalid JSON'}, status=400)

        if not message or len(message) > 4000:
            return JsonResponse({'error': 'Empty message'}, status=400)

        request_id = data.get('request_id')
        if request_id is not None and (not isinstance(request_id, str) or not 1 <= len(request_id) <= 64):
            return JsonResponse({'error': 'Invalid request_id'}, status=400)
        if request_id and request.user.is_authenticated:
            from .models import ChatRequest
            previous = ChatRequest.objects.filter(user=request.user, request_id=request_id).first()
            if previous:
                if previous.message != message:
                    return JsonResponse({'error': 'request_id already used'}, status=409)
                return JsonResponse(previous.response)

        # Đảm bảo session key luôn tồn tại cho cả khách vãng lai và user đăng nhập
        if not request.session.session_key:
            request.session.create()
        session_key = request.session.session_key
        user = request.user if request.user.is_authenticated else None

        # Lấy hoặc tạo ChatSession tách biệt cho user vs anonymous
        if user:
            session = ChatSession.objects.filter(user=user).order_by('-updated_at', '-pk').first()
            if session is None:
                session = ChatSession.objects.create(user=user, session_key=session_key)
        else:
            session, _ = ChatSession.objects.get_or_create(
                session_key=session_key,
                user=None
            )

        # Lưu tin nhắn người dùng
        from apps.behavior.models import UserEvent
        UserEvent.objects.create(user=user, session_key=session_key, event_type='chat')
        user_tokens = max(1, len(message) // 4)
        ChatMessage.objects.create(session=session, role='user', content=message, tokens_used=user_tokens)

        # 1. Kiểm tra xử lý ý định LÊN ĐƠN HÀNG TRỰC TIẾP qua Chatbot AI
        from apps.products.discovery import budget_chat_reply

        from .order_assistant import handle_order_conversation
        budget_reply = budget_chat_reply(message)
        if budget_reply:
            order_handled, order_reply = True, budget_reply
        else:
            order_handled, order_reply = handle_order_conversation(message, user=user, session_dict=request.session)

        if order_handled:
            request.session.modified = True
            text = order_reply
            is_fallback = False
            elapsed = 50
            tokens_used = user_tokens + max(1, len(text) // 4)
        else:
            # 2. Gọi xử lý AI thông minh (Gemini/Groq) / Fallback rule-based
            text, is_fallback, elapsed, tokens_used = call_ai(message, user=user)

        # Lưu tin nhắn phản hồi của trợ lý
        ChatMessage.objects.create(
            session=session,
            role='assistant',
            content=text,
            is_fallback=is_fallback,
            tokens_used=tokens_used,
            response_time_ms=elapsed,
        )

        payload = {
            'reply': text,
            'is_fallback': is_fallback,
            'response_time_ms': elapsed,
            'tokens_used': tokens_used,
        }
        if request_id and user:
            from .models import ChatRequest
            ChatRequest.objects.create(user=user, request_id=request_id, message=message, response=payload)
        return JsonResponse(payload)


class ChatHistoryView(LoginRequiredMixin, TemplateView):
    """
    Trang xem lịch sử các phiên chat của người dùng đã đăng nhập.
    """
    template_name = 'chatbot/history.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['sessions'] = ChatSession.objects.filter(user=self.request.user).prefetch_related('messages')
        return ctx


class ChatSessionMessagesAPIView(View):
    """
    API lấy toàn bộ lịch sử tin nhắn của phiên chat hiện tại (hỗ trợ cả user đăng nhập lẫn khách vãng lai).
    """
    def get(self, request):
        user = request.user if request.user.is_authenticated else None
        session = None
        if user:
            session = ChatSession.objects.filter(user=user).order_by('-updated_at').first()
        elif request.session.session_key:
            session = ChatSession.objects.filter(session_key=request.session.session_key, user=None).order_by('-updated_at').first()

        if not session:
            return JsonResponse({'messages': []})

        msgs = session.messages.order_by('created_at')
        data = [{
            'id': m.id,
            'role': m.role,
            'content': m.content,
            'is_fallback': m.is_fallback,
            'created_at': m.created_at.strftime('%H:%M'),
        } for m in msgs]

        return JsonResponse({'messages': data})


class ChatSessionClearAPIView(View):
    """
    API xóa lịch sử chat của phiên hiện tại để bắt đầu cuộc trò chuyện mới.
    """
    @transaction.atomic
    def post(self, request):
        if request.user.is_authenticated:
            get_user_model().objects.select_for_update().get(pk=request.user.pk)
            request.session = SessionStore(session_key=request.session.session_key)
        user = request.user if request.user.is_authenticated else None
        if user:
            ChatSession.objects.filter(user=user).delete()
        elif request.session.session_key:
            ChatSession.objects.filter(session_key=request.session.session_key, user=None).delete()

        # Xóa cả dữ liệu đơn hàng nháp dở dang nếu có
        request.session.pop('chatbot_order_draft', None)
        request.session.modified = True
        request.session.save()

        return JsonResponse({'success': True})
