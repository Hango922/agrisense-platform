# File: apps/chatbot/fallback.py
"""
Bộ quy tắc nhận diện từ khóa (Rule-based Fallback) hỗ trợ cả tiếng Việt có dấu và không dấu
khi API AI gặp sự cố, timeout hoặc chưa có API key.
"""
import re
from .prompts import FALLBACK_RESPONSES

FALLBACK_RULES = [
    (r'\b(đơn hàng|don hang|order|giao chưa|giao chua|ship|vận chuyển|van chuyen)\b', 'order'),
    (r'\b(nguồn gốc|nguon goc|xuất xứ|xuat xu|ở đâu|o dau|vùng trồng|vung trong|trang trại|trang trai)\b', 'origin'),
    (r'\b(bảo quản|bao quan|hạn sử dụng|han su dung|tủ lạnh|tu lanh|để được bao lâu|de duoc bao lau)\b', 'storage'),
    (r'\b(giá|gia|bao nhiêu|bao nhieu|tiền|tien|price|cost)\b', 'price'),
]


def get_fallback_response(message):
    """
    So khớp câu hỏi với các mẫu biểu thức chính quy (Regex) không phân biệt hoa thường,
    sử dụng boundary ranh giới từ để tránh nhầm lẫn giữa các từ như 'gia' và 'giao'.
    """
    msg = message.lower()
    for pattern, key in FALLBACK_RULES:
        if re.search(pattern, msg, re.IGNORECASE):
            return FALLBACK_RESPONSES[key], key
    return FALLBACK_RESPONSES['default'], 'default'
