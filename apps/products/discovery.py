"""Budget-aware basket suggestions computed from live catalog data."""
import re
import unicodedata
from decimal import Decimal

from django import forms
from django.db import transaction

from apps.cart_orders.models import Cart, CartItem
from apps.cart_orders.services import calculate_shipping_fee
from apps.traceability.inventory import available_stock

from .models import Product


def normalized(text):
    return ''.join(c for c in unicodedata.normalize('NFD', text.lower().replace('đ', 'd'))
                   if unicodedata.category(c) != 'Mn')


class PlannerForm(forms.Form):
    wish = forms.CharField(label='Bạn muốn chuẩn bị gì?', max_length=300, required=False,
                          widget=forms.Textarea(attrs={'rows': 2, 'placeholder': '300k mua rau củ cho 2 người trong 3 ngày'}))
    budget = forms.IntegerField(label='Ngân sách gồm phí giao hàng (đ)', min_value=30000, max_value=5000000, initial=300000)
    people = forms.IntegerField(label='Số người', min_value=1, max_value=10, initial=2)
    days = forms.IntegerField(label='Số ngày', min_value=1, max_value=14, initial=3)
    preference = forms.ChoiceField(label='Ưu tiên', choices=[('', 'Đa dạng'), ('vegetables', 'Rau củ'), ('fruit', 'Trái cây')], required=False)

    def clean(self):
        data = super().clean() or {}
        wish = normalized(data.get('wish', ''))
        match = re.search(r'(\d+(?:[.,]\d+)*)\s*(trieu|tr|k|nghin|ngan|dong|vnd|d\b)', wish)
        if match:
            number, unit = match.groups()
            multiplier = 1000000 if unit in ('trieu', 'tr') else 1000 if unit in ('k', 'nghin', 'ngan') else 1
            raw = number.replace('.', '').replace(',', '') if multiplier == 1 else number.replace(',', '.')
            try:
                budget = int(Decimal(raw) * multiplier)
                if not 30000 <= budget <= 5000000:
                    raise ValueError
                data['budget'] = budget
            except (ValueError, ArithmeticError):
                self.add_error('wish', 'Ngân sách phải từ 30.000đ đến 5.000.000đ.')
        for key, word, maximum in [('people', 'nguoi', 10), ('days', 'ngay', 14)]:
            match = re.search(r'(\d+)\s*' + word, wish)
            if match:
                value = int(match.group(1))
                if not 1 <= value <= maximum:
                    self.add_error('wish', f'{word}: chỉ hỗ trợ từ 1 đến {maximum}.')
                else:
                    data[key] = value
        if 'rau' in wish or 'cu qua' in wish:
            data['preference'] = 'vegetables'
        elif 'trai cay' in wish or 'hoa qua' in wish:
            data['preference'] = 'fruit'
        return data


def make_plan(budget, people, days, preference='', **kwargs):
    products = list(Product.objects.filter(is_active=True, stock__gt=0, price__gt=0).select_related('category').order_by('price', 'pk'))
    keywords = {'vegetables': ('rau', 'cu', 'nam'), 'fruit': ('trai cay', 'hoa qua')}.get(preference, ())
    if keywords:
        products = [p for p in products if any(word in normalized(p.category.name) for word in keywords)]
    stocks = {p.pk: available_stock(p) for p in products}
    products = [p for p in products if stocks[p.pk] > 0]
    # Diversify categories before repeating; household size caps the suggested basket.
    seen = set()
    diverse, rest = [], []
    for product in products:
        (rest if product.category_id in seen else diverse).append(product)
        seen.add(product.category_id)
    products = diverse + rest
    target = min(30, max(3, people * days))
    rows = {}
    total = Decimal(0)
    for _ in range(target):
        added = False
        for product in products:
            current = rows.get(product.pk, {}).get('quantity', 0)
            if current >= min(stocks[product.pk], max(1, (people * days + 2) // 3)):
                continue
            candidate = total + product.price
            if candidate + calculate_shipping_fee(candidate) > budget:
                continue
            rows[product.pk] = {'product': product, 'quantity': current + 1,
                                'subtotal': product.price * (current + 1)}
            total = candidate
            added = True
            if sum(row['quantity'] for row in rows.values()) >= target:
                break
        if not added or sum(row['quantity'] for row in rows.values()) >= target:
            break
    shipping = calculate_shipping_fee(total) if rows else 0
    return {'rows': list(rows.values()), 'total': total, 'shipping': shipping,
            'grand_total': total + shipping, 'remaining': budget - total - shipping,
            'budget': budget, 'people': people, 'days': days}


@transaction.atomic()
def add_selection(user, selection):
    from apps.behavior.models import UserEvent
    cart, _ = Cart.objects.get_or_create(user=user)
    cart = Cart.objects.select_for_update().get(pk=cart.pk)
    products = list(Product.objects.select_for_update().filter(pk__in=selection).order_by('pk'))
    if not selection or len(products) != len(selection):
        raise ValueError('Danh sách sản phẩm không còn hợp lệ.')
    for product in products:
        quantity = selection[product.pk]
        if not isinstance(quantity, int) or isinstance(quantity, bool) or not 1 <= quantity <= 1000:
            raise ValueError('Số lượng phải từ 1 đến 1.000.')
        item = CartItem.objects.filter(cart=cart, product=product).first()
        combined = quantity + (item.quantity if item else 0)
        if combined > available_stock(product):
            raise ValueError(f'{product.name}: không đủ tồn kho còn hạn cho giỏ hàng hiện tại.')
        CartItem.objects.update_or_create(cart=cart, product=product, defaults={'quantity': combined})
        UserEvent.objects.create(user=user, event_type='add_to_cart', product=product, category=product.category)
    return cart


def budget_chat_reply(message):
    from urllib.parse import quote
    text = normalized(message)
    if not (re.search(r'\d\s*(k\b|nghin|ngan|trieu|tr\b|dong|vnd)', text) or 'ngan sach' in text):
        return None
    if not any(word in text for word in ('nguoi', 'ngay', 'ngan sach', 'di cho', 'goi y', 'rau cu', 'trai cay')):
        return None
    form = PlannerForm({'wish': message[:300], 'budget': 300000, 'people': 2, 'days': 3, 'preference': ''})
    if not form.is_valid():
        return 'Bạn hãy chọn ngân sách 30.000–5.000.000đ, tối đa 10 người và 14 ngày. [Mở Đi chợ thông minh](/products/planner/).'
    plan = make_plan(**form.cleaned_data)
    if not plan['rows']:
        return 'Chưa có giỏ phù hợp với ngân sách và tồn kho. [Điều chỉnh nhu cầu](/products/planner/).'
    lines = [f"Gợi ý trong ngân sách {plan['budget']:,}đ (gồm phí giao hàng):"]
    lines.extend(f"• {row['product'].name}: {row['quantity']} {row['product'].unit} — {row['subtotal']:,}đ" for row in plan['rows'])
    lines.append(f"Tổng dự kiến: **{plan['grand_total']:,}đ**. Đây là gợi ý mua sắm, chưa tạo đơn.")
    lines.append(f"[Xem và chỉnh giỏ theo ngân sách](/products/planner/?wish={quote(message[:300])})")
    return '\n\n'.join(lines)
