# File: apps/chatbot/tests/test_fallback.py
"""
Kiểm thử bộ luật phản hồi Fallback rule-based của Chatbot AI khi mất kết nối hoặc câu hỏi phổ biến.
"""
from django.test import TestCase
from apps.chatbot.fallback import get_fallback_response


class FallbackTests(TestCase):
    def test_price_question(self):
        text, key = get_fallback_response('Cà rốt giá bao nhiêu?')
        self.assertEqual(key, 'price')

    def test_price_question_unaccented(self):
        text, key = get_fallback_response('Gia ca chua bao nhieu?')
        self.assertEqual(key, 'price')

    def test_origin_question(self):
        text, key = get_fallback_response('Nguồn gốc xuất xứ của rau này ở đâu?')
        self.assertEqual(key, 'origin')

    def test_storage_question(self):
        text, key = get_fallback_response('Bảo quản súp lơ xanh thế nào?')
        self.assertEqual(key, 'storage')

    def test_order_question(self):
        text, key = get_fallback_response('Đơn hàng của tôi đã được giao chưa?')
        self.assertEqual(key, 'order')

    def test_unknown_question(self):
        text, key = get_fallback_response('abcxyz')
        self.assertEqual(key, 'default')
