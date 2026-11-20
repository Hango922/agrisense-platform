"""Lot inventory: product locks always precede batch locks."""
from django.db import transaction
from django.db.models import Exists, F, OuterRef, Q, Sum
from django.utils import timezone

from apps.products.models import Product

from .models import ProductBatch


def available_products():
    batches = ProductBatch.objects.filter(product_id=OuterRef('pk'), remaining_quantity__gt=0).filter(
        Q(expiry_date__isnull=True) | Q(expiry_date__gte=timezone.localdate()))
    return Product.objects.filter(is_active=True, stock__gt=0).annotate(
        has_sellable_batch=Exists(batches)).filter(Q(track_batches=False) | Q(has_sellable_batch=True))


def sellable_batches(product):
    return product.batches.filter(remaining_quantity__gt=0).filter(
        Q(expiry_date__isnull=True) | Q(expiry_date__gte=timezone.localdate())
    ).order_by(F('expiry_date').asc(nulls_last=True), 'harvest_date', 'pk')


def available_stock(product):
    if not product.is_active:
        return 0
    if not product.track_batches:
        return max(0, product.stock)
    quantity = sellable_batches(product).aggregate(total=Sum('remaining_quantity'))['total'] or 0
    return max(0, min(product.stock, quantity))


@transaction.atomic()
def receive_batch(product, *, quantity, batch_code, harvest_date, packaging_date,
                  expiry_date, planting_location, existing_stock=False, certification=''):
    product = Product.objects.select_for_update().get(pk=product.pk)
    if not isinstance(quantity, int) or isinstance(quantity, bool) or not 1 <= quantity <= 1000000:
        raise ValueError('Số lượng phải từ 1 đến 1.000.000.')
    if not harvest_date <= packaging_date <= timezone.localdate() <= expiry_date:
        raise ValueError('Ngày thu hoạch, đóng gói và hạn sử dụng không hợp lệ.')
    if not product.track_batches:
        from apps.cart_orders.models import OrderItem
        if OrderItem.objects.filter(product=product, order__status='pending', allocations__isnull=True).exists():
            raise ValueError('Hãy xác nhận hoặc hủy các đơn cũ đang chờ trước khi chuyển sản phẩm sang kho theo lô.')
    if existing_stock:
        if product.track_batches or quantity != product.stock:
            raise ValueError('Lô đầu tiên phải khớp toàn bộ tồn kho hiện có và chưa quản lý theo lô.')
    elif not product.track_batches and product.stock != 0:
        raise ValueError('Hãy phân bổ tồn kho hiện có vào lô đầu tiên trước khi nhập thêm.')
    if ProductBatch.objects.filter(batch_code=batch_code).exists():
        raise ValueError('Mã lô đã tồn tại.')
    batch = ProductBatch.objects.create(
        product=product, batch_code=batch_code, remaining_quantity=quantity,
        quantity=f'{quantity} {product.unit}', harvest_date=harvest_date,
        packaging_date=packaging_date, expiry_date=expiry_date,
        planting_location=planting_location, certification=certification,
    )
    product.track_batches = True
    if not existing_stock:
        product.stock += quantity
    product.save(update_fields=['track_batches', 'stock', 'updated_at'])
    return batch


def allocate_batches(item, product, quantity):
    if not product.track_batches:
        return
    from apps.cart_orders.models import BatchAllocation
    batches = list(sellable_batches(product).select_for_update())
    if sum(batch.remaining_quantity for batch in batches) < quantity:
        raise ValueError(f'{product.name}: không đủ hàng còn hạn sử dụng.')
    for batch in batches:
        taken = min(quantity, batch.remaining_quantity)
        BatchAllocation.objects.create(item=item, batch=batch, quantity=taken)
        ProductBatch.objects.filter(pk=batch.pk).update(remaining_quantity=F('remaining_quantity') - taken)
        quantity -= taken
        if not quantity:
            break
