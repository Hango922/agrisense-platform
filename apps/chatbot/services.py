# File: apps/chatbot/services.py
"""
Dịch vụ gọi API trí tuệ nhân tạo (Gemini Flash / Groq) và tự động fallback rule-based khi gặp sự cố.
"""
import time
from django.conf import settings
from .prompts import SYSTEM_PROMPT, CONTEXT_TEMPLATE
from .fallback import get_fallback_response


def call_ai(user_message, product_context=""):
    """
    Gửi câu hỏi tới AI Provider (Gemini / Groq) với ngữ cảnh sản phẩm.
    Nếu API lỗi, vượt timeout (10s) hoặc chưa cấu hình API key, tự động chuyển sang Fallback Rule-based.
    """
    start = time.time()
    try:
        api_provider = getattr(settings, 'AI_PROVIDER', 'gemini')

        if api_provider == 'gemini':
            import google.generativeai as genai
            api_key = getattr(settings, 'GEMINI_API_KEY', None)
            if not api_key or api_key in ('your-gemini-api-key', 'your-gemini-key', ''):
                raise ValueError("Chưa thiết lập GEMINI_API_KEY hợp lệ, chuyển sang fallback rule-based.")
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel('gemini-1.5-flash')
            prompt = f"{SYSTEM_PROMPT}\n\n{CONTEXT_TEMPLATE.format(product_context=product_context, user_message=user_message)}"
            response = model.generate_content(prompt, request_options={'timeout': getattr(settings, 'CHATBOT_TIMEOUT', 10)})
            text = response.text
        elif api_provider == 'groq':
            from groq import Groq
            api_key = getattr(settings, 'GROQ_API_KEY', None)
            if not api_key or api_key in ('your-groq-api-key', 'your-groq-key', ''):
                raise ValueError("Chưa thiết lập GROQ_API_KEY hợp lệ, chuyển sang fallback rule-based.")
            client = Groq(api_key=api_key)
            completion = client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": user_message},
                ],
                timeout=getattr(settings, 'CHATBOT_TIMEOUT', 10),
            )
            text = completion.choices[0].message.content
        else:
            raise ValueError(f"Unknown AI provider: {api_provider}")

        elapsed = int((time.time() - start) * 1000)
        return text, False, elapsed
    except Exception as e:
        text, _ = get_fallback_response(user_message)
        elapsed = int((time.time() - start) * 1000)
        return text, True, elapsed
