# File: apps/products/models.py
"""
Quản lý danh mục, nhà cung cấp, sản phẩm nông sản và đánh giá chất lượng.
"""
from django.db import models
from django.utils.text import slugify
from django.core.validators import FileExtensionValidator


class Category(models.Model):
    """
    Bảng products_category: Phân loại danh mục nông sản (rau củ, trái cây, gạo, nấm,...).
    """
    name = models.CharField(max_length=100, verbose_name='Tên danh mục')
    slug = models.SlugField(unique=True, blank=True, verbose_name='Slug URL')
    parent = models.ForeignKey(
        'self',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='children',
        verbose_name='Danh mục cha'
    )
    description = models.TextField(blank=True, verbose_name='Mô tả danh mục')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Ngày tạo')

    class Meta:
        db_table = 'products_category'
        verbose_name = 'Danh mục'
        verbose_name_plural = 'Categories'

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Supplier(models.Model):
    """
    Bảng products_supplier: Hợp tác xã, nông trại và nhà cung ứng nông sản.
    """
    name = models.CharField(max_length=200, verbose_name='Tên nhà cung cấp / Trang trại')
    address = models.TextField(verbose_name='Địa chỉ vùng trồng')
    phone = models.CharField(max_length=15, blank=True, verbose_name='Số điện thoại liên hệ')
    certification = models.CharField(max_length=200, blank=True, verbose_name='Chứng nhận (VietGAP, GlobalGAP,...)')
    description = models.TextField(blank=True, verbose_name='Giới thiệu trang trại')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Ngày tạo')

    class Meta:
        db_table = 'products_supplier'
        verbose_name = 'Nhà cung cấp'
        verbose_name_plural = 'Danh sách nhà cung cấp'

    def __str__(self):
        return self.name


class Product(models.Model):
    """
    Bảng products_product: Thông tin chi tiết sản phẩm nông sản sạch.
    """
    UNIT_CHOICES = [
        ('kg', 'Kilogram'),
        ('g', 'Gram'),
        ('bó', 'Bó'),
        ('hộp', 'Hộp'),
        ('túi', 'Túi'),
    ]
    name = models.CharField(max_length=200, verbose_name='Tên nông sản')
    slug = models.SlugField(unique=True, blank=True, verbose_name='Slug URL')
    category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,
        related_name='products',
        verbose_name='Danh mục'
    )
    supplier = models.ForeignKey(
        Supplier,
        on_delete=models.PROTECT,
        related_name='products',
        verbose_name='Nhà cung cấp'
    )
    price = models.DecimalField(max_digits=12, decimal_places=0, verbose_name='Giá bán (VNĐ)')
    unit = models.CharField(max_length=20, choices=UNIT_CHOICES, default='kg', verbose_name='Đơn vị tính')
    stock = models.IntegerField(default=0, verbose_name='Số lượng tồn kho')
    image = models.ImageField(
        upload_to='products/',
        blank=True,
        null=True,
        validators=[FileExtensionValidator(['jpg', 'jpeg', 'png', 'webp'])],
        verbose_name='Hình ảnh sản phẩm'
    )
    description = models.TextField(blank=True, verbose_name='Mô tả sản phẩm')
    usage = models.TextField(blank=True, verbose_name='Hướng dẫn sử dụng / Chế biến')
    storage = models.TextField(blank=True, verbose_name='Cách thức bảo quản')
    season = models.CharField(max_length=50, blank=True, verbose_name='Mùa vụ thu hoạch')
    origin = models.CharField(max_length=200, blank=True, verbose_name='Xuất xứ / Vùng trồng')
    is_active = models.BooleanField(default=True, db_index=True, verbose_name='Đang kinh doanh')
    created_at = models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='Ngày tạo')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Ngày cập nhật')

    class Meta:
        db_table = 'products_product'
        ordering = ['-created_at']
        verbose_name = 'Sản phẩm nông sản'
        verbose_name_plural = 'Danh sách sản phẩm'
        indexes = [
            models.Index(fields=['category', 'is_active']),
            models.Index(fields=['price']),
        ]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class ProductReview(models.Model):
    """
    Bảng products_productreview: Đánh giá chất lượng và phản hồi từ khách hàng.
    """
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Sản phẩm'
    )
    user = models.ForeignKey(
        'accounts.User',
        on_delete=models.CASCADE,
        verbose_name='Người đánh giá'
    )
    rating = models.PositiveSmallIntegerField(
        choices=[(i, i) for i in range(1, 6)],
        verbose_name='Số sao đánh giá (1-5)'
    )
    comment = models.TextField(blank=True, verbose_name='Nội dung nhận xét')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Thời gian đánh giá')

    class Meta:
        db_table = 'products_productreview'
        unique_together = ('product', 'user')
        ordering = ['-created_at']
        verbose_name = 'Đánh giá sản phẩm'
        verbose_name_plural = 'Danh sách đánh giá'

    def __str__(self):
        return f"{self.user.username} - {self.product.name} - {self.rating}★"
