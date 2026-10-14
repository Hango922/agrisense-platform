# File: nongsan_project/urls.py
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from apps.products.views import HomeView
from apps.cart_orders.views import OrderHistoryView, OrderDetailView, CancelOrderView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', HomeView.as_view(), name='home'),
    path('accounts/', include('apps.accounts.urls')),
    path('products/', include('apps.products.urls')),
    path('cart/', include('apps.cart_orders.urls')),
    path('orders/', OrderHistoryView.as_view(), name='orders_history_direct'),
    path('orders/<str:order_code>/', OrderDetailView.as_view(), name='orders_detail_direct'),
    path('orders/<str:order_code>/cancel/', CancelOrderView.as_view(), name='orders_cancel_direct'),
    path('chatbot/', include('apps.chatbot.urls')),
    path('trace/', include('apps.traceability.urls')),
    path('dashboard/', include('apps.dashboard.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = 'django.views.defaults.page_not_found'
handler500 = 'django.views.defaults.server_error'
