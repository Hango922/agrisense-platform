from decimal import Decimal
from uuid import uuid4

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core import signing
from django.db import transaction
from django.http import HttpResponseBadRequest
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from apps.cart_orders.models import BasketProposalUse, Cart, Order
from apps.cart_orders.services import calculate_shipping_fee
from apps.traceability.inventory import available_stock

from .ai_planner import make_ai_plan
from .discovery import PlannerForm, add_selection
from .models import Product, SeasonalCombo


def planner(request):
    form = PlannerForm(request.POST if request.method == 'POST' else None,
                       initial={'wish': request.GET.get('wish', '')[:300]})
    context: dict[str, object] = {'form': form}
    if request.method == 'POST' and form.is_valid():
        plan = make_ai_plan(**form.cleaned_data)
        token = signing.dumps({'budget': plan['budget'], 'nonce': uuid4().hex,
                              'products': {str(r['product'].pk): str(r['product'].price) for r in plan['rows']}}, salt='basket')
        request.session['basket_token'] = token
        context.update(plan=plan, basket_token=token)
    return render(request, 'products/planner.html', context, status=400 if form.is_bound and not form.is_valid() else 200)


@login_required
@require_POST
@transaction.atomic()
def add_plan(request):
    token = request.POST.get('basket_token', '')
    if not token or request.session.get('basket_token') != token:
        return HttpResponseBadRequest('Gợi ý đã dùng hoặc hết hiệu lực. Hãy tạo gợi ý mới.')
    try:
        data = signing.loads(token, salt='basket', max_age=900)
        cart, _ = Cart.objects.get_or_create(user=request.user)
        Cart.objects.select_for_update().get(pk=cart.pk)
        if BasketProposalUse.objects.filter(nonce=data['nonce']).exists():
            raise ValueError('Giỏ gợi ý này đã được thêm trước đó.')
        selection = {}
        total = Decimal(0)
        for product in Product.objects.select_for_update().filter(pk__in=data['products']).order_by('pk'):
            qty = int(request.POST.get(f'quantity_{product.pk}', '0'))
            if not 0 <= qty <= 1000:
                raise ValueError('Số lượng không hợp lệ.')
            if qty:
                if product.price != Decimal(data['products'][str(product.pk)]):
                    raise ValueError('Giá đã thay đổi. Hãy tạo lại giỏ gợi ý.')
                selection[product.pk] = qty
                total += product.price * qty
        if total + calculate_shipping_fee(total) > data['budget']:
            raise ValueError('Giỏ đã chỉnh vượt ngân sách, gồm phí giao hàng.')
        add_selection(request.user, selection)
        BasketProposalUse.objects.create(user=request.user, nonce=data['nonce'])
    except (signing.BadSignature, ValueError) as error:
        messages.error(request, str(error))
        return redirect('products:planner')
    del request.session['basket_token']
    messages.success(request, 'Đã thêm giỏ gợi ý. Bạn có thể xem lại trước khi đặt hàng.')
    return redirect('cart_orders:cart')


def combos(request):
    entries = []
    for combo in SeasonalCombo.objects.filter(is_active=True).prefetch_related('items__product'):
        items = list(combo.items.all())
        total = sum(i.product.price * i.quantity for i in items)
        entries.append({'combo': combo, 'items': items, 'total': total,
                        'available': bool(items) and all(i.quantity <= available_stock(i.product) for i in items)})
    return render(request, 'products/combos.html', {'entries': entries})


@login_required
@require_POST
def add_combo(request, slug):
    combo = get_object_or_404(SeasonalCombo, slug=slug, is_active=True)
    try:
        add_selection(request.user, {i.product_id: i.quantity for i in combo.items.all()})
        messages.success(request, f'Đã thêm {combo.name}. Giá được tính theo sản phẩm hiện tại.')
    except ValueError as error:
        messages.error(request, str(error))
    return redirect('cart_orders:cart')


@login_required
@require_POST
def reorder(request, order_code):
    order = get_object_or_404(Order, user=request.user, order_code=order_code)
    selection = {}
    for item in order.items.all():
        selection[item.product_id] = selection.get(item.product_id, 0) + item.quantity
    try:
        add_selection(request.user, selection)
        messages.success(request, 'Đã thêm vào giỏ theo giá hiện tại. Vui lòng xem lại trước khi đặt hàng.')
    except ValueError as error:
        messages.error(request, str(error))
    return redirect('cart_orders:cart')
