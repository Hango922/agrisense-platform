from datetime import timedelta

from django import forms
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.db import IntegrityError
from django.shortcuts import redirect, render
from django.utils import timezone

from apps.cart_orders.models import Order
from apps.products.models import Product
from apps.traceability.inventory import available_stock, receive_batch
from apps.traceability.models import ProductBatch


class ReceiptForm(forms.Form):
    product = forms.ModelChoiceField(queryset=Product.objects.all(), label='Sản phẩm')
    batch_code = forms.RegexField(r'^[A-Za-z0-9_-]{1,50}$', label='Mã lô', max_length=50)
    quantity = forms.IntegerField(min_value=1, max_value=1000000, label='Số lượng theo đơn vị sản phẩm')
    existing_stock = forms.BooleanField(required=False, label='Phân bổ tồn kho hiện có vào lô đầu tiên (không nhập thêm)')
    planting_location = forms.CharField(max_length=200, label='Vùng trồng')
    certification = forms.CharField(max_length=200, required=False, label='Chứng nhận (nếu có)')
    harvest_date = forms.DateField(label='Ngày thu hoạch', widget=forms.DateInput(attrs={'type': 'date'}))
    packaging_date = forms.DateField(label='Ngày đóng gói', widget=forms.DateInput(attrs={'type': 'date'}))
    expiry_date = forms.DateField(label='Hạn sử dụng', widget=forms.DateInput(attrs={'type': 'date'}))


def operational_context():
    today = timezone.localdate()
    batches = ProductBatch.objects.filter(remaining_quantity__gt=0, product__track_batches=True).select_related('product')
    low_products = []
    for product in Product.objects.filter(is_active=True):
        product.available_quantity = available_stock(product)
        if product.available_quantity < 10:
            low_products.append(product)
    return {
        'expiring_batches': batches.filter(expiry_date__range=(today, today + timedelta(days=3))).order_by('expiry_date'),
        'expired_batches': batches.filter(expiry_date__lt=today).order_by('expiry_date'),
        'low_products': sorted(low_products, key=lambda product: product.available_quantity),
        'stale_orders': Order.objects.filter(status='pending', created_at__lt=timezone.now() - timedelta(hours=24)).order_by('created_at'),
    }


@staff_member_required
def operations(request):
    return render(request, 'dashboard/operations.html', operational_context())


@staff_member_required
def receive(request):
    form = ReceiptForm(request.POST if request.method == 'POST' else None)
    if request.method == 'POST' and form.is_valid():
        try:
            batch = receive_batch(**form.cleaned_data)
        except (ValueError, IntegrityError) as error:
            form.add_error(None, str(error) if isinstance(error, ValueError) else 'Mã lô đã tồn tại. Hãy chọn mã khác.')
        else:
            messages.success(request, f'Đã ghi nhận lô {batch.batch_code}.')
            return redirect('dashboard:operations')
    return render(request, 'dashboard/receive.html', {'form': form}, status=400 if form.is_bound and form.errors else 200)
