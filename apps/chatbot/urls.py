# File: apps/chatbot/urls.py
"""
Định tuyến URL cho phân hệ Chatbot AI (apps.chatbot).
"""
from django.urls import path
from . import views

app_name = 'chatbot'

urlpatterns = [
    path('send/', views.ChatbotAPIView.as_view(), name='send'),
    path('history/', views.ChatHistoryView.as_view(), name='history'),
]
