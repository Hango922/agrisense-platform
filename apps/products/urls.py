# File: apps/products/urls.py
"""
Định tuyến URL cho phân hệ Sản phẩm & Danh mục (apps.products).
"""
from django.urls import path

from . import discovery_views, views

app_name = 'products'

urlpatterns = [
    path('planner/', discovery_views.planner, name='planner'),
    path('planner/add/', discovery_views.add_plan, name='add_plan'),
    path('combos/', discovery_views.combos, name='combos'),
    path('combos/<slug:slug>/add/', discovery_views.add_combo, name='add_combo'),
    path('inspect/', views.inspect_produce_view, name='inspect'),
    path('', views.ProductListView.as_view(), name='list'),
    path('search/', views.SearchView.as_view(), name='search'),
    path('<slug:slug>/', views.ProductDetailView.as_view(), name='detail'),
    path('<slug:slug>/review/', views.AddReviewView.as_view(), name='add_review'),
]
