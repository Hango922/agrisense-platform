# File: apps/cart_orders/urls.py
"""
Định tuyến URL cho phân hệ Giỏ hàng & Đơn hàng (apps.cart_orders).
"""
from django.urls import path

from apps.products.discovery_views import reorder

from . import views
from .payments import demo_payment, payment_webhook

app_name = 'cart_orders'

urlpatterns = [
    path('orders/<str:order_code>/reorder/', reorder, name='reorder'),
    path('payments/webhook/', payment_webhook, name='payment_webhook'),
    path('orders/<str:order_code>/demo-payment/', demo_payment, name='demo_payment'),
    path('', views.CartView.as_view(), name='cart'),
    path('add/<int:product_id>/', views.AddToCartView.as_view(), name='add'),
    path('update/<int:item_id>/', views.UpdateCartItemView.as_view(), name='update'),
    path('remove/<int:item_id>/', views.RemoveCartItemView.as_view(), name='remove'),
    path('checkout/', views.CheckoutView.as_view(), name='checkout'),
    path('orders/', views.OrderHistoryView.as_view(), name='order_history'),
    path('orders/<str:order_code>/', views.OrderDetailView.as_view(), name='order_detail'),
    path('orders/<str:order_code>/upload-proof/', views.UploadPaymentProofView.as_view(), name='upload_payment_proof'),
    path('orders/<str:order_code>/cancel/', views.CancelOrderView.as_view(), name='cancel_order'),
]
