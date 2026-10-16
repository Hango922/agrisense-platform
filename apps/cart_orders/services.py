# File: apps/cart_orders/services.py
"""
Các dịch vụ xử lý nghiệp vụ giỏ hàng, đặt hàng COD và tính phí vận chuyển.
"""
from django.db import transaction
from django.utils.crypto import get_random_string
from .models import Order, OrderItem

# Cấu hình phí ship: 30.000đ, miễn phí từ 500.000đ
SHIPPING_FEE = 30000
FREE_SHIPPING_THRESHOLD = 500000


def calculate_shipping_fee(total):
    """
    Tính phí vận chuyển: Miễn phí nếu đơn hàng >= 500.000đ, ngược lại 30.000đ.
    """
    return 0 if total >= FREE_SHIPPING_THRESHOLD else SHIPPING_FEE


@transaction.atomic
def create_order_from_cart(user, cart, address_data, note="", payment_method="cod"):
    """
    Tạo đơn hàng từ giỏ hàng trong một transaction an toàn:
    - Kiểm tra giỏ hàng không rỗng.
    - Kiểm tra tồn kho từng mặt hàng.
    - Tính toán tổng tiền, phí vận chuyển và giảm trừ tồn kho sản phẩm.
    - Hỗ trợ phương thức thanh toán: COD hoặc Chuyển khoản VietQR.
    - Xóa các mặt hàng trong giỏ sau khi đặt thành công.
    """
    if not cart.items.exists():
        raise ValueError("Giỏ hàng trống")

    for item in cart.items.select_related('product'):
        if item.quantity > item.product.stock:
            raise ValueError(f"Sản phẩm '{item.product.name}' chỉ còn {item.product.stock} {item.product.unit}")

    total = sum(item.subtotal() for item in cart.items.all())
    shipping_fee = calculate_shipping_fee(total)
    final = total + shipping_fee

    order = Order.objects.create(
        user=user,
        order_code='ORD' + get_random_string(8, '0123456789'),
        full_name=address_data['full_name'],
        phone=address_data['phone'],
        address=address_data['address'],
        total_amount=total,
        shipping_fee=shipping_fee,
        final_amount=final,
        note=note,
        status='pending',
        payment_method=payment_method,
    )

    for item in cart.items.select_related('product'):
        OrderItem.objects.create(
            order=order,
            product=item.product,
            product_name=item.product.name,
            price=item.product.price,
            quantity=item.quantity,
            subtotal=item.subtotal(),
        )
        item.product.stock -= item.quantity
        item.product.save(update_fields=['stock'])

    cart.items.all().delete()
    return order


@transaction.atomic
def cancel_order(order):
    """
    Hủy đơn hàng: Chỉ cho phép khi đơn ở trạng thái 'pending' (Chờ xác nhận).
    Tự động hoàn lại số lượng tồn kho cho các sản phẩm.
    """
    if order.status not in ('pending',):
        raise ValueError("Chỉ có thể hủy đơn ở trạng thái 'Chờ xác nhận'")

    for item in order.items.select_related('product'):
        item.product.stock += item.quantity
        item.product.save(update_fields=['stock'])

    order.status = 'cancelled'
    order.save(update_fields=['status'])
    return order


@transaction.atomic
def create_direct_order(user, items_data, address_data, note="Đặt hàng qua Chatbot AI"):
    """
    Tạo đơn hàng trực tiếp (ví dụ qua Chatbot AI) mà không cần qua giỏ hàng:
    items_data: list of dicts [{'product': Product instance, 'quantity': int}]
    address_data: {'full_name': str, 'phone': str, 'address': str}
    """
    if not items_data:
        raise ValueError("Danh sách sản phẩm trống")

    for item in items_data:
        prod = item['product']
        qty = item['quantity']
        if qty <= 0:
            raise ValueError(f"Số lượng sản phẩm '{prod.name}' không hợp lệ")
        if qty > prod.stock:
            raise ValueError(f"Sản phẩm '{prod.name}' chỉ còn {prod.stock} {prod.unit}")

    total = sum(item['product'].price * item['quantity'] for item in items_data)
    shipping_fee = calculate_shipping_fee(total)
    final = total + shipping_fee

    order = Order.objects.create(
        user=user,
        order_code='ORD' + get_random_string(8, '0123456789'),
        full_name=address_data['full_name'],
        phone=address_data['phone'],
        address=address_data['address'],
        total_amount=total,
        shipping_fee=shipping_fee,
        final_amount=final,
        note=note,
        status='pending',
        payment_method='cod',
    )

    for item in items_data:
        prod = item['product']
        qty = item['quantity']
        subtotal = prod.price * qty
        OrderItem.objects.create(
            order=order,
            product=prod,
            product_name=prod.name,
            price=prod.price,
            quantity=qty,
            subtotal=subtotal,
        )
        prod.stock -= qty
        prod.save(update_fields=['stock'])

    return order
