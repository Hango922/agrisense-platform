# File: apps/dashboard/urls.py
"""
Định tuyến URL cho bảng điều khiển quản trị riêng (apps.dashboard).
"""
from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    path('', views.DashboardHomeView.as_view(), name='home'),
    path('products/', views.DashboardProductsView.as_view(), name='products'),
    path('orders/', views.DashboardOrdersView.as_view(), name='orders'),
    path('customers/', views.DashboardCustomersView.as_view(), name='customers'),
    path('behavior/', views.DashboardBehaviorView.as_view(), name='behavior'),
    path('traceability/', views.DashboardTraceabilityView.as_view(), name='traceability'),
]
