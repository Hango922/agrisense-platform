# File: apps/chatbot/urls.py
"""
Định tuyến URL cho phân hệ Chatbot AI (apps.chatbot).
"""
from django.urls import path
from . import views

app_name = 'chatbot'

urlpatterns = [
    path('send/', views.ChatbotAPIView.as_view(), name='send'),
    path('messages/', views.ChatSessionMessagesAPIView.as_view(), name='messages'),
    path('clear/', views.ChatSessionClearAPIView.as_view(), name='clear'),
    path('history/', views.ChatHistoryView.as_view(), name='history'),
]
