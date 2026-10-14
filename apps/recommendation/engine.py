# File: apps/recommendation/engine.py
"""
Thuật toán gợi ý nông sản cá nhân hóa (Content-based filtering)
dựa trên vector sở thích danh mục từ UserEvent và fallback sang sản phẩm bán chạy nhất.
"""
from datetime import timedelta
from django.utils import timezone
from django.db.models import Sum
from apps.behavior.models import UserEvent
from apps.products.models import Product

# Trọng số hành vi người dùng
EVENT_WEIGHTS = {
    'view': 1.0,
    'search': 2.0,
    'add_to_cart': 3.0,
    'purchase': 5.0,
    'review': 4.0,
}


def build_user_vector(user, days=30):
    """
    Xây dựng vector sở thích danh mục của người dùng dựa trên các sự kiện tương tác trong N ngày qua.
    """
    since = timezone.now() - timedelta(days=days)
    events = UserEvent.objects.filter(user=user, created_at__gte=since).select_related('category', 'product__category')
    scores = {}
    for e in events:
        w = EVENT_WEIGHTS.get(e.event_type, 1.0)
        cat_id = e.category_id or (e.product.category_id if e.product else None)
        if cat_id:
            scores[cat_id] = scores.get(cat_id, 0) + w
    return scores


def recommend_for_user(user, limit=10):
    """
    Gợi ý sản phẩm cho người dùng theo danh mục quan tâm nhiều nhất:
    - Loại trừ các sản phẩm đã mua trước đó.
    - Fallback sang sản phẩm bán chạy nhất nếu chưa đủ dữ liệu tương tác.
    """
    scores = build_user_vector(user)
    if not scores or sum(scores.values()) < 3:
        return _fallback_bestsellers(limit)

    from apps.cart_orders.models import OrderItem
    purchased_ids = set(OrderItem.objects.filter(order__user=user).values_list('product_id', flat=True))
    results = []
    top_cats = sorted(scores.items(), key=lambda x: -x[1])[:3]

    for cat_id, score in top_cats:
        products = Product.objects.filter(
            category_id=cat_id,
            is_active=True,
            stock__gt=0
        ).exclude(id__in=purchased_ids)[:limit]

        for p in products:
            results.append({
                'product': p,
                'score': score,
                'reason': f"Vì bạn quan tâm đến {p.category.name}",
            })

    results.sort(key=lambda x: -x['score'])
    return results[:limit]


def _fallback_bestsellers(limit=10):
    """
    Phương án dự phòng: Gợi ý các sản phẩm nông sản bán chạy hoặc mới nhất trên hệ thống.
    """
    since = timezone.now() - timedelta(days=30)
    from apps.cart_orders.models import OrderItem
    best = (
        OrderItem.objects.filter(
            order__created_at__gte=since,
            order__status__in=['confirmed', 'shipping', 'delivered']
        )
        .values('product_id')
        .annotate(total=Sum('quantity'))
        .order_by('-total')[:limit]
    )
    ids = [b['product_id'] for b in best]
    products = list(Product.objects.filter(id__in=ids, is_active=True, stock__gt=0))

    if len(products) < limit:
        exclude_ids = [p.id for p in products]
        more = Product.objects.filter(
            is_active=True,
            stock__gt=0
        ).exclude(id__in=exclude_ids).order_by('-created_at')[:(limit - len(products))]
        products.extend(list(more))

    return [{'product': p, 'score': 0, 'reason': 'Sản phẩm đang thịnh hành'} for p in products]
