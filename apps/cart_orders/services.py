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
def create_direct_order(user, items_data, address_data, note="Đặt hàng qua Chatbot AI", payment_method="cod"):
    """
    Tạo đơn hàng trực tiếp (ví dụ qua Chatbot AI) mà không cần qua giỏ hàng:
    items_data: list of dicts [{'product': Product instance, 'quantity': int}]
    address_data: {'full_name': str, 'phone': str, 'address': str}
    payment_method: 'cod' hoặc 'vietqr'
    """
    if payment_method not in ('cod', 'vietqr'):
        payment_method = 'cod'

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

    # Đảm bảo độ dài các trường khớp với ràng buộc cơ sở dữ liệu
    raw_name = str(address_data.get('full_name') or (user.get_full_name() or user.username if user else 'Khách hàng')).strip()
    full_name = raw_name[:100] if raw_name else 'Khách hàng'

    raw_phone = str(address_data.get('phone') or getattr(user, 'phone', '') or '0900000000').strip()
    phone = raw_phone[:15] if raw_phone else '0900000000'

    raw_address = str(address_data.get('address') or 'Địa chỉ giao hàng').strip()

    order = Order.objects.create(
        user=user,
        order_code='ORD' + get_random_string(8, '0123456789'),
        full_name=full_name,
        phone=phone,
        address=raw_address,
        total_amount=total,
        shipping_fee=shipping_fee,
        final_amount=final,
        note=note,
        status='pending',
        payment_method=payment_method,
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


def generate_admin_verification_bill(order_code, admin_username=None):
    """
    Tạo chứng từ đối soát nội bộ dạng ảnh PNG hợp lệ để gán vào payment_proof khi
    Admin xác nhận đã nhận tiền chuyển khoản trực tiếp qua ngân hàng.
    """
    import io
    from PIL import Image, ImageDraw
    from django.core.files.base import ContentFile
    from django.utils import timezone

    width, height = 650, 400
    img = Image.new('RGB', (width, height), color='#f8fafc')
    draw = ImageDraw.Draw(img)

    # Khung viền và header
    draw.rectangle([(15, 15), (width - 15, height - 15)], outline='#059669', width=3)
    draw.rectangle([(20, 20), (width - 20, 85)], fill='#059669')

    # Header text
    draw.text((35, 30), "AGRISENSE PLATFORM - XAC NHAN DOI SOAT", fill='#ffffff')
    draw.text((35, 55), "CHUNG TU THANH TOAN NGAN HANG (ADMIN VERIFIED)", fill='#a7f3d0')

    # Nội dung chứng từ
    now_str = timezone.now().strftime("%d/%m/%Y %H:%M:%S")
    admin_str = admin_username or "Quan Tri Vien He Thong"

    lines = [
        f"Ma don hang: #{order_code}",
        "Phuong thuc: Chuyen khoan VietQR (Techcombank)",
        "Trang thai: DA DOI SOAT KHOP LENH TAI KHOAN",
        f"Nguoi doi soat: {admin_str}",
        f"Thoi gian xac nhan: {now_str}",
        "Ghi chu: Tien da vao tai khoan thuc te. Don hang du dieu kien xuat kho."
    ]

    y = 110
    for line in lines:
        draw.text((40, y), line, fill='#1e293b')
        y += 38

    # Footer
    draw.line([(35, height - 55), (width - 35, height - 55)], fill='#cbd5e1', width=1)
    draw.text((40, height - 42), "Chung tu xac thuc noi bo - AgriSense Safe Agriculture System", fill='#64748b')

    buf = io.BytesIO()
    img.save(buf, format='PNG')
    return ContentFile(buf.getvalue(), name=f"admin_verified_{order_code}.png")

