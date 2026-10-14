# File: apps/chatbot/views.py
"""
Views xử lý endpoint API Chatbot và giao diện xem lịch sử hội thoại.
"""
import json
from django.http import JsonResponse
from django.views import View
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from .models import ChatSession, ChatMessage
from .services import call_ai


@method_decorator(csrf_exempt, name='dispatch')
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
        user_tokens = max(1, len(message) // 4)
        ChatMessage.objects.create(session=session, role='user', content=message, tokens_used=user_tokens)

        # 1. Kiểm tra xử lý ý định LÊN ĐƠN HÀNG TRỰC TIẾP qua Chatbot AI
        from .order_assistant import handle_order_conversation
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

        return JsonResponse({
            'reply': text,
            'is_fallback': is_fallback,
            'response_time_ms': elapsed,
            'tokens_used': tokens_used,
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


@method_decorator(csrf_exempt, name='dispatch')
class ChatSessionClearAPIView(View):
    """
    API xóa lịch sử chat của phiên hiện tại để bắt đầu cuộc trò chuyện mới.
    """
    def post(self, request):
        user = request.user if request.user.is_authenticated else None
        if user:
            ChatSession.objects.filter(user=user).delete()
        elif request.session.session_key:
            ChatSession.objects.filter(session_key=request.session.session_key, user=None).delete()

        # Xóa cả dữ liệu đơn hàng nháp dở dang nếu có
        request.session.pop('chatbot_order_draft', None)
        request.session.modified = True

        return JsonResponse({'success': True})
