# File: apps/products/views.py
"""
Views xử lý trang chủ, danh sách sản phẩm, bộ lọc, tìm kiếm và đánh giá chất lượng.
"""
import base64
import os
from decimal import Decimal, InvalidOperation

from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Avg, Q
from django.http import HttpResponseBadRequest, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import DetailView, ListView, TemplateView, View

from apps.behavior.models import UserEvent
from apps.recommendation.engine import recommend_for_user
from apps.traceability.inventory import available_products, sellable_batches

from .models import Category, Product, ProductReview
from .visual_inspector import inspect_produce_image


class HomeView(TemplateView):
    """
    Trang chủ AgriSense hiển thị sản phẩm mới nhất, danh mục và gợi ý AI cá nhân hóa.
    """
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['featured_products'] = available_products().order_by('-created_at')[:8]
        ctx['categories'] = Category.objects.all()
        if self.request.user.is_authenticated:
            ctx['recommendations'] = recommend_for_user(self.request.user, limit=6)
        else:
            from apps.recommendation.engine import _fallback_bestsellers
            ctx['recommendations'] = _fallback_bestsellers(limit=6)
        return ctx


class ProductListView(ListView):
    """
    Trang danh mục và lọc sản phẩm theo loại nông sản, khoảng giá, có phân trang.
    """
    model = Product
    template_name = 'products/list.html'
    context_object_name = 'products'
    paginate_by = 12

    def get(self, request, *args, **kwargs):
        try:
            prices = [Decimal(request.GET[key]) for key in ('min_price', 'max_price') if request.GET.get(key)]
            if any(not value.is_finite() or value < 0 or value > 999999999999 for value in prices):
                raise ValueError
            if len(prices) == 2 and prices[0] > prices[1]:
                raise ValueError
        except (InvalidOperation, ValueError):
            return HttpResponseBadRequest('Khoảng giá không hợp lệ.')
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        qs = available_products()
        cat_slug = self.request.GET.get('category')
        if cat_slug:
            qs = qs.filter(category__slug=cat_slug)
        min_price = self.request.GET.get('min_price')
        max_price = self.request.GET.get('max_price')
        if min_price:
            qs = qs.filter(price__gte=min_price)
        if max_price:
            qs = qs.filter(price__lte=max_price)
        query = self.request.GET.get('q', '').strip()
        if query:
            qs = qs.filter(Q(name__icontains=query) | Q(origin__icontains=query))
        sort = self.request.GET.get('sort', '')
        return qs.order_by(sort if sort in ('price', '-price', 'name') else '-created_at', 'pk')

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['categories'] = Category.objects.all()
        ctx['current_category'] = self.request.GET.get('category', '')
        return ctx


class SearchView(ListView):
    """
    Tìm kiếm sản phẩm theo tên, xuất xứ và mô tả; tự động ghi nhận sự kiện tìm kiếm.
    """
    model = Product
    template_name = 'products/search.html'
    context_object_name = 'products'
    paginate_by = 12

    def get_queryset(self):
        q = self.request.GET.get('q', '').strip()
        if q:
            return available_products().filter(
                Q(name__icontains=q) | Q(description__icontains=q) | Q(origin__icontains=q),
                is_active=True
            )
        return Product.objects.none()

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['query'] = self.request.GET.get('q', '')
        return ctx


class ProductDetailView(DetailView):
    """
    Chi tiết sản phẩm, xuất xứ vùng trồng, hướng dẫn sử dụng và tự động ghi sự kiện view.
    """
    model = Product
    template_name = 'products/detail.html'
    context_object_name = 'product'

    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)
        UserEvent.objects.create(
            user=request.user if request.user.is_authenticated else None,
            session_key=request.session.session_key or '',
            event_type='view',
            product=self.object,
            category=self.object.category,
        )
        return response

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['reviews'] = self.object.reviews.all()[:10]
        ctx['avg_rating'] = self.object.reviews.aggregate(Avg('rating'))['rating__avg'] or 0
        ctx['related_products'] = Product.objects.filter(
            category=self.object.category, is_active=True
        ).exclude(id=self.object.id)[:4]
        ctx['latest_batch'] = sellable_batches(self.object).first() if self.object.track_batches else self.object.batches.order_by('-created_at').first()
        return ctx


class AddReviewView(LoginRequiredMixin, View):
    """
    Khách hàng gửi đánh giá sao và nhận xét cho nông sản sau khi trải nghiệm.
    """
    def post(self, request, slug):
        product = get_object_or_404(Product, slug=slug)
        try:
            rating = int(request.POST.get('rating', 5))
            if not 1 <= rating <= 5:
                raise ValueError
        except (ValueError, TypeError):
            return HttpResponseBadRequest('Điểm đánh giá phải từ 1 đến 5.')
        comment = request.POST.get('comment', '')
        ProductReview.objects.update_or_create(
            product=product, user=request.user,
            defaults={'rating': rating, 'comment': comment}
        )
        UserEvent.objects.create(
            user=request.user, event_type='review',
            product=product, category=product.category,
        )
        return redirect('products:detail', slug=slug)


def inspect_produce_view(request):
    """
    Trang thẩm định chất lượng & độ tươi nông sản qua ảnh bằng Gemini Multimodal Vision.
    Hỗ trợ cả tải ảnh trực tiếp, chụp ảnh trên di động và thử nghiệm nhanh với ảnh mẫu.
    """
    preset_samples = [
        {
            'name': 'Cà chua bi',
            'filename': 'ca_chua_bi.jpg',
            'image_url': f"{settings.MEDIA_URL}products/ca_chua_bi.jpg",
            'desc': 'Cà chua đỏ căng mọng, cuống xanh tươi',
        },
        {
            'name': 'Cải thìa hữu cơ',
            'filename': 'cai_thia_huu_co.jpg',
            'image_url': f"{settings.MEDIA_URL}products/cai_thia_huu_co.jpg",
            'desc': 'Rau cải xanh giòn bẹ, canh tác VietGAP',
        },
        {
            'name': 'Cà rốt Đà Lạt',
            'filename': 'ca_rot_da_lat.jpg',
            'image_url': f"{settings.MEDIA_URL}products/ca_rot_da_lat.jpg",
            'desc': 'Củ cam tươi ngon, ngọt bùi tự nhiên',
        },
        {
            'name': 'Dưa lưới Huỳnh Long',
            'filename': 'dua_luoi_huynh_long.jpg',
            'image_url': f"{settings.MEDIA_URL}products/dua_luoi_huynh_long.jpg",
            'desc': 'Vân lưới đều, hương thơm dịu mát',
        },
    ]

    sample_param = request.GET.get('sample')
    result = None
    image_preview = None
    error_message = None

    if request.method == 'GET' and sample_param:
        sample_filename = os.path.basename(sample_param)
        sample_path = os.path.join(settings.MEDIA_ROOT, 'products', sample_filename)
        if os.path.exists(sample_path):
            try:
                with open(sample_path, 'rb') as f:
                    img_bytes = f.read()
                mime = 'image/jpeg' if sample_filename.lower().endswith(('.jpg', '.jpeg')) else 'image/png'
                result = inspect_produce_image(img_bytes, mime, sample_filename)
                image_preview = f"{settings.MEDIA_URL}products/{sample_filename}"
            except Exception as e:  # noqa: BLE001
                error_message = str(e)

    elif request.method == 'POST':
        img_bytes = None
        mime = 'image/jpeg'
        filename = ''

        sample_name = request.POST.get('sample_image')
        if sample_name:
            sample_filename = os.path.basename(sample_name)
            sample_path = os.path.join(settings.MEDIA_ROOT, 'products', sample_filename)
            if os.path.exists(sample_path):
                with open(sample_path, 'rb') as f:
                    img_bytes = f.read()
                mime = 'image/jpeg' if sample_filename.lower().endswith(('.jpg', '.jpeg')) else 'image/png'
                filename = sample_filename
                image_preview = f"{settings.MEDIA_URL}products/{sample_filename}"

        elif 'image' in request.FILES:
            uploaded_file = request.FILES['image']
            img_bytes = uploaded_file.read()
            mime = uploaded_file.content_type or 'image/jpeg'
            filename = uploaded_file.name
            b64_str = base64.b64encode(img_bytes).decode('utf-8')
            image_preview = f"data:{mime};base64,{b64_str}"

        if img_bytes:
            try:
                result = inspect_produce_image(img_bytes, mime, filename)
            except Exception as e:  # noqa: BLE001
                error_message = str(e)
        else:
            error_message = 'Vui lòng chọn hoặc tải lên một hình ảnh nông sản.'

        if request.headers.get('x-requested-with') == 'XMLHttpRequest' or 'application/json' in request.headers.get('Accept', ''):
            if error_message:
                return JsonResponse({'success': False, 'error': error_message}, status=400)
            return JsonResponse({'success': True, 'data': result, 'image_preview': image_preview})

    context = {
        'preset_samples': preset_samples,
        'result': result,
        'image_preview': image_preview,
        'error_message': error_message,
    }
    return render(request, 'products/inspect.html', context)

