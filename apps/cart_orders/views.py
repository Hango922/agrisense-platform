# File: apps/cart_orders/views.py
"""
Views xử lý xem giỏ hàng, thêm/sửa/xóa sản phẩm, thanh toán COD và lịch sử đơn hàng.
"""
from django.views.generic import View, TemplateView
from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from .models import Cart, CartItem, Order
from .services import create_order_from_cart, cancel_order
from apps.products.models import Product
from apps.behavior.models import UserEvent


class CartView(LoginRequiredMixin, TemplateView):
    """
    Trang xem chi tiết giỏ hàng và tổng tiền dự kiến.
    """
    template_name = 'cart_orders/cart.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        cart, _ = Cart.objects.get_or_create(user=self.request.user)
        ctx['cart'] = cart
        return ctx


class AddToCartView(LoginRequiredMixin, View):
    """
    Thêm sản phẩm vào giỏ hàng và ghi nhận sự kiện add_to_cart.
    """
    def post(self, request, product_id):
        product = get_object_or_404(Product, id=product_id, is_active=True)
        qty = int(request.POST.get('quantity', 1))
        if qty > product.stock:
            messages.error(request, f"Chỉ còn {product.stock} {product.unit}")
            return redirect('products:detail', slug=product.slug)

        cart, _ = Cart.objects.get_or_create(user=request.user)
        item, created = CartItem.objects.get_or_create(cart=cart, product=product)
        if not created:
            if item.quantity + qty > product.stock:
                messages.error(request, f"Không thể thêm. Tồn kho chỉ còn {product.stock} {product.unit}")
                return redirect('cart_orders:cart')
            item.quantity += qty
        else:
            item.quantity = qty
        item.save()

        UserEvent.objects.create(
            user=request.user, event_type='add_to_cart',
            product=product, category=product.category,
        )
        messages.success(request, f"Đã thêm {product.name} vào giỏ hàng")
        return redirect('cart_orders:cart')


class UpdateCartItemView(LoginRequiredMixin, View):
    """
    Cập nhật số lượng mặt hàng trong giỏ hàng.
    """
    def post(self, request, item_id):
        item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
        qty = int(request.POST.get('quantity', 1))
        if qty > item.product.stock:
            messages.error(request, f"Chỉ còn {item.product.stock} {item.product.unit}")
            return redirect('cart_orders:cart')
        if qty <= 0:
            item.delete()
        else:
            item.quantity = qty
            item.save()
        return redirect('cart_orders:cart')


class RemoveCartItemView(LoginRequiredMixin, View):
    """
    Xóa mặt hàng khỏi giỏ hàng.
    """
    def post(self, request, item_id):
        item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
        item.delete()
        messages.info(request, "Đã xóa sản phẩm khỏi giỏ hàng")
        return redirect('cart_orders:cart')


class CheckoutView(LoginRequiredMixin, TemplateView):
    """
    Trang xác nhận thông tin nhận hàng và thanh toán COD.
    """
    template_name = 'cart_orders/checkout.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        cart, _ = Cart.objects.get_or_create(user=self.request.user)
        ctx['cart'] = cart
        default_address = self.request.user.addresses.filter(is_default=True).first()
        ctx['default_address'] = default_address
        return ctx

    def post(self, request):
        cart, _ = Cart.objects.get_or_create(user=request.user)
        try:
            order = create_order_from_cart(request.user, cart, {
                'full_name': request.POST['full_name'],
                'phone': request.POST['phone'],
                'address': request.POST['address'],
            }, note=request.POST.get('note', ''))

            for item in order.items.all():
                UserEvent.objects.create(
                    user=request.user, event_type='purchase',
                    product=item.product, category=item.product.category,
                )

            messages.success(request, f"Đặt hàng thành công! Mã đơn hàng: {order.order_code}")
            return redirect('cart_orders:order_detail', order_code=order.order_code)
        except ValueError as e:
            messages.error(request, str(e))
            return redirect('cart_orders:cart')


class OrderHistoryView(LoginRequiredMixin, TemplateView):
    """
    Lịch sử các đơn hàng đã đặt của khách hàng.
    """
    template_name = 'cart_orders/order_history.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['orders'] = Order.objects.filter(user=self.request.user)
        return ctx


class OrderDetailView(LoginRequiredMixin, TemplateView):
    """
    Xem chi tiết tiến trình vận chuyển và thông tin đơn hàng.
    """
    template_name = 'cart_orders/order_detail.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['order'] = get_object_or_404(Order, order_code=kwargs['order_code'], user=self.request.user)
        return ctx


class CancelOrderView(LoginRequiredMixin, View):
    """
    Hủy đơn hàng đang chờ xác nhận và hoàn lại số lượng tồn kho.
    """
    def post(self, request, order_code):
        order = get_object_or_404(Order, order_code=order_code, user=request.user)
        try:
            cancel_order(order)
            messages.success(request, "Đã hủy đơn hàng thành công")
        except ValueError as e:
            messages.error(request, str(e))
        return redirect('cart_orders:order_detail', order_code=order_code)
