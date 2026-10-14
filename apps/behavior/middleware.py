# File: apps/behavior/middleware.py
"""
Middleware tự động ghi nhận hành vi tìm kiếm và tương tác của người dùng.
"""
from .models import UserEvent


class BehaviorTrackingMiddleware:
    """
    Tự động ghi nhận sự kiện tìm kiếm khi khách hàng truy cập endpoint /products/search/?q=...
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        if request.method != 'GET' or response.status_code != 200:
            return response

        user = request.user if request.user.is_authenticated else None
        session_key = request.session.session_key or ''

        if request.path.startswith('/products/search/') and request.GET.get('q'):
            UserEvent.objects.create(
                user=user,
                session_key=session_key,
                event_type='search',
                keyword=request.GET['q'][:200],
            )
        return response
