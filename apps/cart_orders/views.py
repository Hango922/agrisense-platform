# File: apps/cart_orders/views.py
"""
Views xử lý xem giỏ hàng, thêm/sửa/xóa sản phẩm, thanh toán COD và lịch sử đơn hàng.
"""
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.http import HttpResponseBadRequest
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import TemplateView, View

from apps.behavior.models import UserEvent
from apps.products.models import Product
from apps.traceability.inventory import available_stock

from .forms import CheckoutForm, PaymentProofForm
from .models import Cart, CartItem, Order
from .services import cancel_order, create_order_from_cart


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
    @transaction.atomic
    def post(self, request, product_id):
        product = get_object_or_404(Product, id=product_id, is_active=True)
        try:
            qty = int(request.POST.get('quantity', 1))
            if qty < 0 or qty > 2147483647:
                raise ValueError
        except (ValueError, TypeError):
            return HttpResponseBadRequest('Số lượng không hợp lệ.')
        if qty == 0:
            return HttpResponseBadRequest('Số lượng phải lớn hơn 0.')
        if qty > available_stock(product):
            messages.error(request, f"Chỉ còn {available_stock(product)} {product.unit}")
            return redirect('products:detail', slug=product.slug)

        cart, _ = Cart.objects.get_or_create(user=request.user)
        cart = Cart.objects.select_for_update().get(pk=cart.pk)
        item, created = CartItem.objects.get_or_create(cart=cart, product=product)
        if not created:
            if item.quantity + qty > available_stock(product):
                messages.error(request, f"Không thể thêm. Tồn kho chỉ còn {available_stock(product)} {product.unit}")
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
    @transaction.atomic
    def post(self, request, item_id):
        cart = get_object_or_404(Cart.objects.select_for_update(), user=request.user)
        item = get_object_or_404(CartItem, id=item_id, cart=cart)
        try:
            qty = int(request.POST.get('quantity', 1))
            if qty < 0 or qty > 2147483647:
                raise ValueError
        except (ValueError, TypeError):
            return HttpResponseBadRequest('Số lượng không hợp lệ.')
        if qty > available_stock(item.product):
            messages.error(request, f"Chỉ còn {available_stock(item.product)} {item.product.unit}")
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
    @transaction.atomic
    def post(self, request, item_id):
        cart = get_object_or_404(Cart.objects.select_for_update(), user=request.user)
        item = get_object_or_404(CartItem, id=item_id, cart=cart)
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
        data = request.POST.copy()
        data.setdefault('payment_method', 'cod')
        form = CheckoutForm(data)
        if not form.is_valid():
            return self.render_to_response({**self.get_context_data(), 'form_errors': form.errors, 'submitted': data}, status=400)
        cart, _ = Cart.objects.get_or_create(user=request.user)
        try:
            payment_method = request.POST.get('payment_method', 'cod')
            order = create_order_from_cart(
                request.user, cart, {
                    'full_name': request.POST['full_name'],
                    'phone': request.POST['phone'],
                    'address': request.POST['address'],
                },
                note=request.POST.get('note', ''),
                payment_method=payment_method
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
    Xem chi tiết tiến trình vận chuyển và thông tin đơn hàng kèm mã VietQR thanh toán.
    """
    template_name = 'cart_orders/order_detail.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        order = get_object_or_404(Order, order_code=kwargs['order_code'], user=self.request.user)
        ctx['order'] = order
        from .vietqr import get_vietqr_info
        ctx['vietqr'] = get_vietqr_info(order)
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


class UploadPaymentProofView(LoginRequiredMixin, View):
    """
    Khách hàng tải lên ảnh biên lai chuyển khoản ngân hàng (bill chuyển khoản).
    """
    @transaction.atomic
    def post(self, request, order_code):
        order = get_object_or_404(Order.objects.select_for_update(), order_code=order_code, user=request.user)
        if order.status != 'pending' or order.payment_method != 'vietqr':
            messages.error(request, "Chỉ có thể tải bill cho đơn hàng đang ở trạng thái 'Chờ xác nhận'.")
            return redirect('cart_orders:order_detail', order_code=order_code)

        form = PaymentProofForm(files=request.FILES)
        if not form.is_valid():
            messages.error(request, 'Bill phải là ảnh hợp lệ, tối đa 5 MB.')
            return redirect('cart_orders:order_detail', order_code=order_code)
        proof_file = form.cleaned_data['payment_proof']

        from django.utils import timezone
        order.payment_proof = proof_file
        order.payment_proof_uploaded_at = timezone.now()
        order.save()
        messages.success(request, "Đã tải lên bill chuyển khoản thành công! Admin sẽ đối soát và xác nhận đơn hàng cho bạn.")
        return redirect('cart_orders:order_detail', order_code=order_code)


class PaymentProofView(LoginRequiredMixin, View):
    def get(self, request, filename):
        from django.http import FileResponse, Http404
        orders = Order.objects.all() if request.user.is_staff else Order.objects.filter(user=request.user)
        order = get_object_or_404(orders, payment_proof='payment_proofs/' + filename)
        try:
            response = FileResponse(order.payment_proof.open('rb'), as_attachment=True)
        except FileNotFoundError as error:
            raise Http404 from error
        response['Cache-Control'] = 'private, no-store'
        return response
