# File: nongsan_project/urls.py
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from django.views.generic import RedirectView

from apps.cart_orders.views import (
    CancelOrderView,
    OrderDetailView,
    OrderHistoryView,
    PaymentProofView,
    UploadPaymentProofView,
)
from apps.products.views import HomeView

from .runtime_views import health, public_image

urlpatterns = [
    path('health/', health, name='health'),
    path('media/products/<path:filename>', public_image, {'directory': 'products'}, name='product_image'),
    path('media/qr_codes/<path:filename>', public_image, {'directory': 'qr_codes'}, name='qr_image'),
    path('media/payment_proofs/<path:filename>', PaymentProofView.as_view(), name='payment_proof'),
    path('admin/', admin.site.urls),
    path('', HomeView.as_view(), name='home'),
    path('COD/', RedirectView.as_view(pattern_name='home', permanent=False)),
    path('COD', RedirectView.as_view(pattern_name='home', permanent=False)),
    path('cod/', RedirectView.as_view(pattern_name='home', permanent=False)),
    path('cod', RedirectView.as_view(pattern_name='home', permanent=False)),
    path('accounts/', include('apps.accounts.urls')),
    path('products/', include('apps.products.urls')),
    path('cart/', include('apps.cart_orders.urls')),
    path('orders/', OrderHistoryView.as_view(), name='orders_history_direct'),
    path('orders/<str:order_code>/', OrderDetailView.as_view(), name='orders_detail_direct'),
    path('orders/<str:order_code>/upload-proof/', UploadPaymentProofView.as_view(), name='orders_upload_proof_direct'),
    path('orders/<str:order_code>/cancel/', CancelOrderView.as_view(), name='orders_cancel_direct'),
    path('chatbot/', include('apps.chatbot.urls')),
    path('trace/', include('apps.traceability.urls')),
    path('dashboard/', include('apps.dashboard.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = 'django.views.defaults.page_not_found'
handler500 = 'django.views.defaults.server_error'
