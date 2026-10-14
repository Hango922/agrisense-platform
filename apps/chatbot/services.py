# File: apps/chatbot/services.py
"""
Dịch vụ gọi API trí tuệ nhân tạo (Gemini / Groq) và tự động fallback rule-based khi gặp sự cố,
hỗ trợ trích xuất số lượng token tiêu thụ thực tế (tokens_used) và thời gian phản hồi (response_time_ms).
"""
import time
import requests
from django.conf import settings
from .prompts import SYSTEM_PROMPT, CONTEXT_TEMPLATE
from .fallback import get_fallback_response


def build_product_context():
    """
    Tạo ngữ cảnh dữ liệu sản phẩm nông sản thực tế từ cơ sở dữ liệu để nạp vào Prompt cho AI LLM.
    """
    try:
        from apps.products.models import Product
        products = list(Product.objects.filter(is_active=True).select_related('supplier', 'category')[:25])
        lines = []
        for p in products:
            sup = p.supplier.name if p.supplier else "Nông trại Việt"
            cert = p.supplier.certification if (p.supplier and p.supplier.certification) else "VietGAP"
            lines.append(f"- {p.name}: Giá {int(p.price):,} đ/{p.unit}, Tồn kho: {p.stock} {p.unit}, Xuất xứ: {p.origin or 'Việt Nam'}, Nhà cung cấp: {sup} ({cert})")
        return "\n".join(lines)
    except Exception:
        return ""


def call_ai(user_message, product_context="", user=None):
    """
    Gửi câu hỏi tới AI Provider (Gemini / Groq) với ngữ cảnh sản phẩm.
    Nếu API lỗi, vượt timeout (10s) hoặc chưa cấu hình API key, tự động chuyển sang Fallback Rule-based.
    Trả về: (text, is_fallback, elapsed_ms, tokens_used)
    """
    start = time.time()
    try:
        if not product_context:
            product_context = build_product_context()

        api_provider = getattr(settings, 'AI_PROVIDER', 'gemini')

        if api_provider == 'gemini':
            api_key = getattr(settings, 'GEMINI_API_KEY', None)
            if not api_key or api_key in ('your-gemini-api-key', 'your-gemini-key', ''):
                raise ValueError("Chưa thiết lập GEMINI_API_KEY hợp lệ, chuyển sang fallback rule-based.")

            prompt = f"{SYSTEM_PROMPT}\n\n{CONTEXT_TEMPLATE.format(product_context=product_context, user_message=user_message)}"
            timeout_sec = getattr(settings, 'CHATBOT_TIMEOUT', 10)

            # Danh sách các mô hình Gemini được ưu tiên thử nghiệm tuần tự (fallback theo độ khả dụng)
            model_candidates = [
                'gemini-3.1-flash-lite',
                'gemini-3.1-flash-lite-preview',
                'gemini-3.8-flash',
                'gemini-flash-latest'
            ]
            text = None
            tokens_used = 0

            for m in model_candidates:
                url = f"https://generativelanguage.googleapis.com/v1beta/models/{m}:generateContent?key={api_key}"
                try:
                    resp = requests.post(
                        url,
                        json={'contents': [{'parts': [{'text': prompt}]}]},
                        timeout=timeout_sec
                    )
                    if resp.status_code == 200:
                        data = resp.json()
                        text = data['candidates'][0]['content']['parts'][0]['text']
                        usage = data.get('usageMetadata', {})
                        tokens_used = usage.get('totalTokenCount') or usage.get('total_token_count') or max(1, (len(prompt) + len(text)) // 4)
                        break
                except Exception:
                    continue

            if not text:
                raise ValueError("Không thể nhận phản hồi thành công từ các mô hình Gemini.")

        elif api_provider == 'groq':
            from groq import Groq
            api_key = getattr(settings, 'GROQ_API_KEY', None)
            if not api_key or api_key in ('your-groq-api-key', 'your-groq-key', ''):
                raise ValueError("Chưa thiết lập GROQ_API_KEY hợp lệ, chuyển sang fallback rule-based.")
            client = Groq(api_key=api_key)
            full_system_prompt = f"{SYSTEM_PROMPT}\n\nDữ liệu sản phẩm thực tế trong cửa hàng:\n{product_context}"
            completion = client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=[
                    {"role": "system", "content": full_system_prompt},
                    {"role": "user", "content": user_message},
                ],
                timeout=getattr(settings, 'CHATBOT_TIMEOUT', 10),
            )
            text = completion.choices[0].message.content

            # Trích xuất số token thực tế từ Groq API
            tokens_used = 0
            if hasattr(completion, 'usage') and completion.usage:
                tokens_used = getattr(completion.usage, 'total_tokens', 0)
            if not tokens_used:
                tokens_used = max(1, (len(full_system_prompt) + len(user_message) + len(text)) // 4)

        else:
            raise ValueError(f"Unknown AI provider: {api_provider}")

        elapsed = int((time.time() - start) * 1000)
        return text, False, elapsed, tokens_used

    except Exception as e:
        text, _ = get_fallback_response(user_message, user=user)
        elapsed = int((time.time() - start) * 1000)
        tokens_used = max(1, (len(user_message) + len(text)) // 4)
        return text, True, elapsed, tokens_used
