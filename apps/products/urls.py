# File: apps/products/urls.py
"""
Định tuyến URL cho phân hệ Sản phẩm & Danh mục (apps.products).
"""
from django.urls import path
from . import views

app_name = 'products'

urlpatterns = [
    path('', views.ProductListView.as_view(), name='list'),
    path('search/', views.SearchView.as_view(), name='search'),
    path('<slug:slug>/', views.ProductDetailView.as_view(), name='detail'),
    path('<slug:slug>/review/', views.AddReviewView.as_view(), name='add_review'),
]
