# File: apps/cart_orders/urls.py
"""
Định tuyến URL cho phân hệ Giỏ hàng & Đơn hàng (apps.cart_orders).
"""
from django.urls import path
from . import views

app_name = 'cart_orders'

urlpatterns = [
    path('', views.CartView.as_view(), name='cart'),
    path('add/<int:product_id>/', views.AddToCartView.as_view(), name='add'),
    path('update/<int:item_id>/', views.UpdateCartItemView.as_view(), name='update'),
    path('remove/<int:item_id>/', views.RemoveCartItemView.as_view(), name='remove'),
    path('checkout/', views.CheckoutView.as_view(), name='checkout'),
    path('orders/', views.OrderHistoryView.as_view(), name='order_history'),
    path('orders/<str:order_code>/', views.OrderDetailView.as_view(), name='order_detail'),
    path('orders/<str:order_code>/cancel/', views.CancelOrderView.as_view(), name='cancel_order'),
]
