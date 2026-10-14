# File: apps/traceability/urls.py
"""
Định tuyến URL cho phân hệ Truy xuất nguồn gốc QR (apps.traceability).
"""
from django.urls import path
from . import views

app_name = 'traceability'

urlpatterns = [
    path('<str:batch_code>/', views.PublicTraceView.as_view(), name='public_trace'),
]
