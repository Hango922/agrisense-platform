"""Transactional order services shared by storefront, chatbot and staff."""
from django.db import transaction
from django.db.models import F
from django.utils.crypto import get_random_string

from apps.behavior.models import UserEvent
from apps.products.models import Product
from .forms import CheckoutForm
from .models import Cart, Order, OrderItem

SHIPPING_FEE = 30000
FREE_SHIPPING_THRESHOLD = 500000
TRANSITIONS = {
    'pending': {'confirmed', 'cancelled'},
    'confirmed': {'shipping'},
    'shipping': {'delivered'},
    'delivered': set(),
    'cancelled': set(),
}


def calculate_shipping_fee(total):
    return 0 if total >= FREE_SHIPPING_THRESHOLD else SHIPPING_FEE


def validate_transition(current, target):
    if target not in TRANSITIONS or (current != target and target not in TRANSITIONS.get(current, set())):
        raise ValueError('Không thể chuyển trạng thái đơn hàng theo yêu cầu.')


@transaction.atomic
def create_order_from_cart(user, cart, address_data, note='', payment_method='cod'):
    cart = Cart.objects.select_for_update().get(pk=cart.pk, user=user)
    items = list(cart.items.select_for_update().select_related('product').order_by('product_id'))
    order = create_direct_order(user, [{'product': i.product, 'quantity': i.quantity} for i in items],
                                address_data, note=note, payment_method=payment_method)
    cart.items.filter(pk__in=[i.pk for i in items]).delete()
    return order


@transaction.atomic
def create_direct_order(user, items_data, address_data, note='Đặt hàng qua Chatbot AI', payment_method='cod'):
    form = CheckoutForm({**address_data, 'payment_method': payment_method, 'note': note})
    if not form.is_valid():
        raise ValueError('Thông tin nhận hàng hoặc phương thức thanh toán không hợp lệ.')
    if not items_data:
        raise ValueError('Giỏ hàng trống.')
    quantities = {}
    for item in items_data:
        qty = item['quantity']
        if not isinstance(qty, int) or isinstance(qty, bool) or qty <= 0:
            raise ValueError('Số lượng phải là số nguyên dương.')
        key = item['product'].pk
        quantities[key] = quantities.get(key, 0) + qty
    # Lock in a stable order and read current stock, never caller snapshots.
    products = list(Product.objects.select_for_update().filter(pk__in=quantities).order_by('pk'))
    if len(products) != len(quantities):
        raise ValueError('Sản phẩm không tồn tại.')
    for product in products:
        if not product.is_active or quantities[product.pk] > product.stock:
            raise ValueError(f"Sản phẩm '{product.name}' không đủ tồn kho hoặc đã ngừng bán.")
    total = sum(p.price * quantities[p.pk] for p in products)
    shipping = calculate_shipping_fee(total)
    data = form.cleaned_data
    order = Order.objects.create(user=user, order_code='ORD' + get_random_string(12, '0123456789'),
        full_name=data['full_name'], phone=data['phone'], address=data['address'],
        total_amount=total, shipping_fee=shipping, final_amount=total + shipping,
        note=data['note'], payment_method=payment_method, status='pending')
    for product in products:
        quantity = quantities[product.pk]
        OrderItem.objects.create(order=order, product=product, product_name=product.name,
            price=product.price, quantity=quantity, subtotal=product.price * quantity)
        Product.objects.filter(pk=product.pk).update(stock=F('stock') - quantity)
        UserEvent.objects.create(user=user, event_type='purchase', product=product, category=product.category)
    return order


@transaction.atomic
def cancel_order(order):
    locked = Order.objects.select_for_update().get(pk=order.pk)
    if locked.status != 'pending':
        raise ValueError('Chỉ có thể hủy đơn đang chờ xác nhận.')
    for item in locked.items.order_by('product_id'):
        Product.objects.filter(pk=item.product_id).update(stock=F('stock') + item.quantity)
    locked.status = 'cancelled'
    locked.save(update_fields=['status', 'updated_at'])
    order.status = locked.status
    return locked


@transaction.atomic
def transition_order(order, target, proof=None, admin_verified=False, actor=None):
    from django.utils import timezone
    locked = Order.objects.select_for_update().get(pk=order.pk)
    validate_transition(locked.status, target)
    if locked.status == target:
        return locked
    if target == 'cancelled':
        return cancel_order(locked)
    if proof is not None:
        from .forms import PaymentProofForm
        form = PaymentProofForm(files={'payment_proof': proof})
        if not form.is_valid():
            raise ValueError('Bill phải là ảnh PNG, JPEG hoặc WebP hợp lệ, tối đa 5 MB.')
        locked.payment_proof = form.cleaned_data['payment_proof']
        locked.payment_proof_uploaded_at = timezone.now()
    if locked.payment_method == 'vietqr' and not locked.payment_proof:
        if not admin_verified:
            raise ValueError('Cần bill hoặc xác nhận đối soát ngân hàng.')
        username = actor.username if actor else 'Admin'
        locked.payment_proof = generate_admin_verification_bill(locked.order_code, username)
        locked.payment_proof_uploaded_at = timezone.now()
        locked.note += f'\n[Đối soát thủ công: {username}, {timezone.now().isoformat()}]'
    locked.status = target
    locked.save()
    return locked


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

