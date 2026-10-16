# File: apps/products/views.py
"""
Views xử lý trang chủ, danh sách sản phẩm, bộ lọc, tìm kiếm và đánh giá chất lượng.
"""
from django.views.generic import ListView, DetailView, TemplateView, View
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q, Avg
from .models import Product, Category, ProductReview
from apps.behavior.models import UserEvent
from apps.recommendation.engine import recommend_for_user


class HomeView(TemplateView):
    """
    Trang chủ AgriSense hiển thị sản phẩm mới nhất, danh mục và gợi ý AI cá nhân hóa.
    """
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['featured_products'] = Product.objects.filter(is_active=True, stock__gt=0).order_by('-created_at')[:8]
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

    def get_queryset(self):
        qs = Product.objects.filter(is_active=True, stock__gt=0)
        cat_slug = self.request.GET.get('category')
        if cat_slug:
            qs = qs.filter(category__slug=cat_slug)
        min_price = self.request.GET.get('min_price')
        max_price = self.request.GET.get('max_price')
        if min_price:
            qs = qs.filter(price__gte=min_price)
        if max_price:
            qs = qs.filter(price__lte=max_price)
        return qs

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
            return Product.objects.filter(
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
        ctx['latest_batch'] = self.object.batches.order_by('-created_at').first()
        return ctx


class AddReviewView(LoginRequiredMixin, View):
    """
    Khách hàng gửi đánh giá sao và nhận xét cho nông sản sau khi trải nghiệm.
    """
    def post(self, request, slug):
        product = get_object_or_404(Product, slug=slug)
        rating = int(request.POST.get('rating', 5))
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
