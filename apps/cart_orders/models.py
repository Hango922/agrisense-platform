# File: apps/cart_orders/models.py
"""
Quản lý giỏ hàng, đặt hàng thanh toán COD và chi tiết đơn hàng nông sản.
"""
from typing import TYPE_CHECKING, ClassVar

from django.conf import settings
from django.db import models


class Cart(models.Model):
    """
    Bảng cart_orders_cart: Giỏ hàng của người dùng.
    """
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='cart',
        verbose_name='Người dùng'
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Ngày tạo')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Ngày cập nhật')

    class Meta:
        db_table = 'cart_orders_cart'
        verbose_name = 'Giỏ hàng'
        verbose_name_plural = 'Danh sách giỏ hàng'

    def total_items(self):
        """
        Tính tổng số lượng mặt hàng trong giỏ.
        """
        return sum(item.quantity for item in self.items.all())

    def total_price(self):
        """
        Tính tổng tiền giỏ hàng trước phí ship và giảm giá.
        """
        return sum(item.subtotal() for item in self.items.all())

    def __str__(self):
        return f"Giỏ hàng của {self.user.username}"


class CartItem(models.Model):
    """
    Bảng cart_orders_cartitem: Từng mặt hàng trong giỏ hàng.
    """
    cart = models.ForeignKey(
        Cart,
        on_delete=models.CASCADE,
        related_name='items',
        verbose_name='Giỏ hàng'
    )
    product = models.ForeignKey(
        'products.Product',
        on_delete=models.CASCADE,
        verbose_name='Sản phẩm'
    )
    quantity = models.PositiveIntegerField(default=1, verbose_name='Số lượng')
    added_at = models.DateTimeField(auto_now_add=True, verbose_name='Thời gian thêm')

    class Meta:
        db_table = 'cart_orders_cartitem'
        unique_together = ('cart', 'product')
        verbose_name = 'Mặt hàng trong giỏ'
        verbose_name_plural = 'Danh sách mặt hàng trong giỏ'

    def subtotal(self):
        """
        Thành tiền của từng dòng mặt hàng.
        """
        return self.product.price * self.quantity

    def __str__(self):
        return f"{self.product.name} x {self.quantity}"


class Order(models.Model):
    """
    Bảng cart_orders_order: Quản lý thông tin và trạng thái đơn hàng.
    """
    if TYPE_CHECKING:
        items: models.QuerySet['OrderItem']

    STATUS_CHOICES = [
        ('pending', 'Chờ xác nhận'),
        ('confirmed', 'Đã xác nhận'),
        ('shipping', 'Đang giao'),
        ('delivered', 'Đã giao'),
        ('cancelled', 'Đã hủy'),
    ]
    PAYMENT_CHOICES = [
        ('cod', 'Thanh toán khi nhận hàng (COD)'),
        ('vietqr', 'Chuyển khoản qua mã QR (VietQR / Techcombank)'),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name='orders',
        verbose_name='Người đặt'
    )
    order_code = models.CharField(max_length=20, unique=True, db_index=True, verbose_name='Mã đơn hàng')
    full_name = models.CharField(max_length=100, verbose_name='Tên người nhận')
    phone = models.CharField(max_length=15, verbose_name='Số điện thoại nhận')
    address = models.TextField(verbose_name='Địa chỉ giao hàng')
    total_amount = models.DecimalField(max_digits=12, decimal_places=0, verbose_name='Tiền hàng')
    discount_amount = models.DecimalField(max_digits=12, decimal_places=0, default=0, verbose_name='Giảm giá')
    shipping_fee = models.DecimalField(max_digits=12, decimal_places=0, default=0, verbose_name='Phí vận chuyển')
    final_amount = models.DecimalField(max_digits=12, decimal_places=0, verbose_name='Tổng thanh toán')
    payment_method = models.CharField(max_length=20, choices=PAYMENT_CHOICES, default='cod', verbose_name='Phương thức thanh toán')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', db_index=True, verbose_name='Trạng thái')
    payment_proof = models.ImageField(upload_to='payment_proofs/', null=True, blank=True, verbose_name='Ảnh bill chuyển khoản')
    payment_proof_uploaded_at = models.DateTimeField(null=True, blank=True, verbose_name='Thời gian tải bill')
    payment_status = models.CharField(max_length=20, default='unpaid', choices=[
        ('unpaid', 'Chưa xác nhận thanh toán'), ('paid', 'Đã nhận tiền'),
        ('demo_paid', 'Thanh toán mô phỏng'),
    ], editable=False)
    is_demo = models.BooleanField(default=False, editable=False)
    paid_at = models.DateTimeField(null=True, blank=True, editable=False)
    note = models.TextField(blank=True, verbose_name='Ghi chú đơn hàng')
    created_at = models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='Thời gian đặt')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Thời gian cập nhật')

    class Meta:
        db_table = 'cart_orders_order'
        ordering = ['-created_at']
        verbose_name = 'Đơn hàng'
        verbose_name_plural = 'Danh sách đơn hàng'

    def clean(self):
        super().clean()
        if self.payment_method == 'vietqr' and self.status in ('confirmed', 'shipping', 'delivered') and not self.payment_proof and not self.has_verified_payment:
            from django.core.exceptions import ValidationError
            raise ValidationError({
                'status': "Đơn hàng thanh toán VietQR bắt buộc phải có ảnh bill chuyển khoản trước khi Admin xác nhận đơn hàng!"
            })

    def save(self, *args, **kwargs):
        if self.payment_method == 'vietqr' and self.status in ('confirmed', 'shipping', 'delivered') and not self.payment_proof and not self.has_verified_payment:
            from django.core.exceptions import ValidationError
            raise ValidationError("Đơn hàng thanh toán VietQR bắt buộc phải có ảnh bill chuyển khoản trước khi Admin xác nhận đơn hàng!")
        super().save(*args, **kwargs)

    def can_be_confirmed(self):
        """Kiểm tra điều kiện để admin có thể xác nhận đơn hàng: Đơn VietQR bắt buộc phải có bill."""
        if self.status != 'pending':
            return False
        if self.payment_method == 'vietqr' and not self.payment_proof and not self.has_verified_payment:
            return False
        return True

    def __str__(self):
        return self.order_code

    @property
    def has_verified_payment(self):
        return self.payment_status == 'paid' or (self.is_demo and self.payment_status == 'demo_paid')


class OrderItem(models.Model):
    """
    Bảng cart_orders_orderitem: Chi tiết từng nông sản trong đơn hàng.
    """
    if TYPE_CHECKING:
        allocations: models.QuerySet['BatchAllocation']
        product_id: int

    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name='items',
        verbose_name='Đơn hàng'
    )
    product = models.ForeignKey(
        'products.Product',
        on_delete=models.PROTECT,
        verbose_name='Sản phẩm'
    )
    product_name = models.CharField(max_length=200, verbose_name='Tên sản phẩm tại thời điểm mua')
    price = models.DecimalField(max_digits=12, decimal_places=0, verbose_name='Đơn giá')
    quantity = models.PositiveIntegerField(verbose_name='Số lượng')
    subtotal = models.DecimalField(max_digits=12, decimal_places=0, verbose_name='Thành tiền')

    class Meta:
        db_table = 'cart_orders_orderitem'
        verbose_name = 'Mặt hàng đơn hàng'
        verbose_name_plural = 'Danh sách mặt hàng đơn hàng'

    def __str__(self):
        return f"{self.product_name} x {self.quantity}"


class BatchAllocation(models.Model):
    if TYPE_CHECKING:
        batch_id: int

    item = models.ForeignKey(OrderItem, on_delete=models.CASCADE, related_name='allocations')
    batch = models.ForeignKey('traceability.ProductBatch', on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField()

    class Meta:
        constraints: ClassVar[list] = [models.CheckConstraint(condition=models.Q(quantity__gt=0), name='allocation_positive_quantity')]


class PaymentEvent(models.Model):
    if TYPE_CHECKING:
        order_id: int

    provider = models.CharField(max_length=20)
    transaction_id = models.CharField(max_length=100)
    order = models.ForeignKey(Order, on_delete=models.PROTECT, related_name='payment_events')
    amount = models.DecimalField(max_digits=12, decimal_places=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints: ClassVar[list] = [models.UniqueConstraint(fields=['provider', 'transaction_id'], name='unique_payment_transaction')]


class BasketProposalUse(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    nonce = models.CharField(max_length=32, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
