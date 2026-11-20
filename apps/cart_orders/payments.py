"""Authenticated payment notifications and an explicitly isolated demo path."""
import hashlib
import hmac
import json
import time
from decimal import Decimal, InvalidOperation

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError, transaction
from django.http import HttpResponseBadRequest, HttpResponseForbidden, JsonResponse
from django.shortcuts import get_object_or_404, redirect
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from .models import Order, PaymentEvent


@transaction.atomic()
def record_payment(order_code: str, transaction_id: str, amount: Decimal, *, demo: bool = False) -> Order:
    order = Order.objects.select_for_update().get(order_code=order_code)
    provider = 'demo' if demo else 'gateway'
    if demo != order.is_demo:
        raise ValueError('Môi trường thanh toán không khớp đơn hàng.')
    event = PaymentEvent.objects.filter(provider=provider, transaction_id=transaction_id).first()
    if event:
        if event.order_id != order.pk or event.amount != amount:
            raise ValueError('Mã giao dịch đã được sử dụng.')
        return order
    if order.payment_method != 'vietqr' or order.status != 'pending' or order.has_verified_payment:
        raise ValueError('Đơn hàng không còn chờ thanh toán chuyển khoản.')
    if amount != order.final_amount:
        raise ValueError('Số tiền không khớp tổng thanh toán.')
    PaymentEvent.objects.create(provider=provider, transaction_id=transaction_id, order=order, amount=amount)
    order.payment_status = 'demo_paid' if demo else 'paid'
    order.paid_at = timezone.now()
    order.status = 'confirmed'
    order.save(update_fields=['payment_status', 'paid_at', 'status', 'updated_at'])
    return order


@csrf_exempt
@require_POST
def payment_webhook(request):
    secret = settings.PAYMENT_WEBHOOK_SECRET
    if len(secret) < 32:
        return JsonResponse({'error': 'Payment gateway not configured'}, status=503)
    if len(request.body) > 8192:
        return HttpResponseBadRequest('Payload too large')
    timestamp = request.headers.get('X-Payment-Timestamp', '')
    signature = request.headers.get('X-Payment-Signature', '')
    try:
        if abs(time.time() - int(timestamp)) > 300:
            raise ValueError
    except ValueError:
        return HttpResponseForbidden('Invalid timestamp')
    digest = hmac.new(secret.encode(), timestamp.encode() + b'.' + request.body, hashlib.sha256).hexdigest()
    if not hmac.compare_digest(digest, signature):
        return HttpResponseForbidden('Invalid signature')
    try:
        data = json.loads(request.body)
        if not isinstance(data, dict) or data.get('currency') != 'VND':
            raise ValueError('Invalid currency or payload')
        tx = data['transaction_id']
        code = data['order_code']
        if not isinstance(tx, str) or not 1 <= len(tx) <= 100 or not isinstance(code, str) or len(code) > 20:
            raise ValueError('Invalid transaction')
        amount = Decimal(str(data['amount']))
        if not amount.is_finite() or amount <= 0 or amount > 999999999999 or amount != amount.to_integral_value():
            raise ValueError('Invalid amount')
        order = record_payment(code, tx, amount)
    except (ValueError, KeyError, TypeError, InvalidOperation, UnicodeDecodeError):
        return HttpResponseBadRequest('Invalid payment notification')
    except Order.DoesNotExist:
        return JsonResponse({'error': 'Order not found'}, status=404)
    except IntegrityError:
        return JsonResponse({'error': 'Transaction already used'}, status=409)
    return JsonResponse({'accepted': True, 'order_code': order.order_code})


@login_required
@require_POST
def demo_payment(request, order_code):
    if not settings.DEMO_MODE or not settings.DEBUG:
        return HttpResponseForbidden('Chế độ mô phỏng đang tắt.')
    order = get_object_or_404(Order, order_code=order_code, user=request.user, is_demo=True)
    try:
        record_payment(order.order_code, 'demo-' + order.order_code, order.final_amount, demo=True)
        messages.success(request, 'Đã mô phỏng nhận tiền. Đây không phải giao dịch ngân hàng thật.')
    except ValueError as error:
        messages.error(request, str(error))
    return redirect('cart_orders:order_detail', order_code=order.order_code)
