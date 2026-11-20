"""Database-backed fixed-window quotas shared by all WSGI workers."""
import hashlib
import hmac
import time
from datetime import timedelta

from django.conf import settings
from django.db import transaction
from django.http import JsonResponse
from django.utils import timezone

from .models import RequestQuota


@transaction.atomic()
def consume_quota(scope, identity, limit, seconds=60):
    bucket = int(time.time()) // seconds
    key = hmac.new(settings.SECRET_KEY.encode(), f'{scope}:{identity}:{bucket}'.encode(), hashlib.sha256).hexdigest()
    quota, _ = RequestQuota.objects.get_or_create(key=key, defaults={'expires_at': timezone.now() + timedelta(seconds=seconds * 2)})
    quota = RequestQuota.objects.select_for_update().get(pk=key)
    if quota.count >= limit:
        return False
    quota.count += 1
    quota.save(update_fields=['count'])
    return True


class RequestLimitMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        policies = {'/accounts/login/': 10, '/admin/login/': 10, '/accounts/register/': 5, '/chatbot/send/': 20,
                    '/products/planner/': 5}
        limit = policies.get(request.path)
        if settings.RATE_LIMIT_ENABLED and request.method == 'POST' and limit:
            # Ignore forwarded headers: the local listener is not a trusted public proxy.
            identity = request.META.get('REMOTE_ADDR', 'unknown')
            allowed = consume_quota(request.path, identity, limit)
            if allowed and request.path.endswith('/login/'):
                allowed = consume_quota('login-account', request.POST.get('username', '').casefold()[:150], 20)
            if not allowed:
                response = JsonResponse({'error': 'Quá nhiều yêu cầu. Vui lòng thử lại sau một phút.'}, status=429)
                response['Retry-After'] = '60'
                return response
        return self.get_response(request)
