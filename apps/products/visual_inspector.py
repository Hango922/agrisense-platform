# File: apps/products/visual_inspector.py
"""
Dịch vụ thẩm định và giám định độ tươi, chất lượng nông sản qua hình ảnh
sử dụng Gemini Multimodal Vision API (google-genai SDK).
Hỗ trợ fallback ngoại tuyến và liên kết tự động với danh mục sản phẩm của AgriSense.
"""
import json
import logging
import re
from typing import Any

from django.conf import settings
from django.db.models import Q

from apps.traceability.inventory import available_products

logger = logging.getLogger(__name__)

INSPECTOR_SYSTEM_PROMPT = """Bạn là chuyên gia giám định chất lượng và an toàn thực phẩm nông sản Việt Nam cho nền tảng AgriSense.
Nhiệm vụ của bạn là quan sát kỹ hình ảnh nông sản (rau, củ, quả, nấm, hạt...) và đưa ra đánh giá khách quan, khoa học.

Bạn PHẢI trả về duy nhất một đối tượng JSON hợp lệ (không kèm markdown ngoài JSON, không kèm giải thích thừa) theo cấu trúc sau:
{
  "produce_name": "Tên loại nông sản (ví dụ: Cà chua bi, Cải bó xôi, Xoài cát Hòa Lộc...)",
  "category": "Rau lá | Củ quả | Trái cây | Nấm | Gạo & Hạt | Nông sản chế biến",
  "freshness_score": 92,
  "quality_grade": "Loại 1 (Xuất sắc) | Loại 2 (Đạt chuẩn) | Cần dùng sớm | Hỏng / Không nên dùng",
  "visual_assessment": "Nhận xét chi tiết về màu sắc, độ căng bóng của vỏ, trạng thái cuống lá và biểu hiện cảm quan.",
  "defect_analysis": "Phát hiện khuyết tật cảm quan: vết thâm, dập nát, héo úa, dấu vết côn trùng cắn, nấm mốc hoặc đốm bệnh.",
  "shelf_life_days": 5,
  "storage_tips": "Hướng dẫn cụ thể về nhiệt độ, độ ẩm và cách bảo quản (để ngoài hay ngăn mát tủ lạnh, có cần bọc kín không).",
  "recommended_dishes": [
    "Gợi ý món ăn 1 phù hợp với nông sản này",
    "Gợi ý món ăn 2",
    "Gợi ý món ăn 3"
  ],
  "search_keywords": ["từ khóa 1", "từ khóa 2", "từ khóa 3"]
}

Lưu ý:
- freshness_score: Số nguyên từ 0 đến 100 biểu thị tỉ lệ độ tươi mới.
- shelf_life_days: Số ngày ước tính có thể bảo quản tối ưu tiếp theo (số nguyên >= 0).
- search_keywords: 2-4 từ khóa tiếng Việt ngắn gọn, không dấu hoặc có dấu (ví dụ: ["cà chua", "ca chua", "rau"]) để tìm sản phẩm tương tự trong kho hàng.
- Nếu hình ảnh không phải là nông sản hoặc thực phẩm, hãy đặt produce_name là "Không xác định", freshness_score: 0, quality_grade: "Không rõ", và giải thích trong visual_assessment.
"""

MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB
ALLOWED_MIME_TYPES = {
    'image/jpeg': 'image/jpeg',
    'image/jpg': 'image/jpeg',
    'image/png': 'image/png',
    'image/webp': 'image/webp',
}


def match_catalog_products(keywords: list[str], produce_name: str, limit: int = 4) -> list[dict[str, Any]]:
    """
    Tìm kiếm các nông sản đang có sẵn trong kho hàng AgriSense phù hợp với kết quả nhận diện.
    """
    try:
        query_parts = []
        if produce_name and produce_name != "Không xác định":
            query_parts.append(produce_name)
        if keywords:
            query_parts.extend(keywords)

        if not query_parts:
            return []

        q_filter = Q()
        for term in query_parts[:5]:
            term_clean = term.strip()
            if term_clean and len(term_clean) >= 2:
                q_filter |= Q(name__icontains=term_clean)
                q_filter |= Q(category__name__icontains=term_clean)

        matched = list(available_products().filter(q_filter).distinct()[:limit])

        # Nếu không có sản phẩm khớp trực tiếp, gợi ý các sản phẩm nổi bật
        if not matched:
            matched = list(available_products().order_by('-created_at')[:limit])

        results = []
        for p in matched:
            results.append({
                'id': p.pk,
                'name': p.name,
                'slug': p.slug,
                'price': int(p.price),
                'unit': p.unit,
                'stock': p.sellable_stock,
                'category_name': p.category.name if p.category else '',
                'origin': p.origin or 'Việt Nam',
                'image_url': p.image.url if p.image else None,
            })
        return results
    except Exception as e:  # noqa: BLE001
        logger.warning("Error matching catalog products: %s", e)
        return []


def get_rule_based_fallback(hint_name: str = "") -> dict[str, Any]:
    """
    Phương án fallback ngoại tuyến khi không thể kết nối tới Gemini API hoặc chưa có API Key.
    """
    normalized_hint = hint_name.lower().replace("_", " ").replace("-", " ")
    
    # Một số mẫu nhận diện nông sản phổ biến
    if any(k in normalized_hint for k in ["ca chua", "cà chua", "tomato"]):
        return {
            "produce_name": "Cà chua bi tươi",
            "category": "Củ quả",
            "freshness_score": 90,
            "quality_grade": "Loại 1 (Xuất sắc)",
            "visual_assessment": "Quả tròn đều, vỏ căng mọng màu đỏ tươi, tai quả còn xanh và bám chắc vào thân.",
            "defect_analysis": "Không xuất hiện vết dập nứt hay dấu hiệu nấm mốc.",
            "shelf_life_days": 5,
            "storage_tips": "Bảo quản ở nhiệt độ phòng thoáng mát 18-22°C. Chỉ nên cho vào ngăn mát tủ lạnh khi quả đã chín mọng.",
            "recommended_dishes": [
                "Salad cà chua bi sốt dầu giấm",
                "Mì Ý sốt bò băm cà chua bi",
                "Canh chua cá lóc cà chua bi thanh mát"
            ],
            "search_keywords": ["cà chua", "ca chua bi", "củ quả"],
            "is_fallback": True,
            "provider_note": "Chế độ dự phòng quy tắc (offline fallback)."
        }
    elif any(k in normalized_hint for k in ["cai", "cải", "rau", "cabbage"]):
        return {
            "produce_name": "Rau cải xanh hữu cơ",
            "category": "Rau lá",
            "freshness_score": 88,
            "quality_grade": "Loại 1 (Xuất sắc)",
            "visual_assessment": "Lá xanh mướt tự nhiên, bẹ lá giòn và mọng nước, không bị dập nát.",
            "defect_analysis": "Lá đều màu, có vài đốm tự nhiên của canh tác hữu cơ không dùng hóa chất.",
            "shelf_life_days": 4,
            "storage_tips": "Bọc bằng giấy báo hoặc túi zip có lỗ thoáng, bảo quản trong ngăn rau củ tủ lạnh (4-6°C). Không rửa trước khi cất.",
            "recommended_dishes": [
                "Cải thìa xào tỏi thơm lừng",
                "Canh cải nấu thịt băm / tôm tươi",
                "Cải luộc chấm kho quẹt Nam Bộ"
            ],
            "search_keywords": ["cải", "rau cải", "rau lá"],
            "is_fallback": True,
            "provider_note": "Chế độ dự phòng quy tắc (offline fallback)."
        }
    elif any(k in normalized_hint for k in ["ca rot", "cà rốt", "carrot"]):
        return {
            "produce_name": "Cà rốt Đà Lạt",
            "category": "Củ quả",
            "freshness_score": 93,
            "quality_grade": "Loại 1 (Xuất sắc)",
            "visual_assessment": "Củ thon dài, màu cam đậm tự nhiên, vỏ nhẵn và săn chắc.",
            "defect_analysis": "Không bị thâm đầu, không có rễ con mọc xum xuê và không bị nứt thân.",
            "shelf_life_days": 10,
            "storage_tips": "Cắt bỏ phần cuống lá thừa, bọc màng thực phẩm hoặc túi giấy và giữ trong ngăn mát tủ lạnh.",
            "recommended_dishes": [
                "Nước ép cà rốt cam tươi giàu vitamin A",
                "Canh sườn hầm cà rốt khoai tây",
                "Gỏi tai heo cà rốt dưa leo giòn rụm"
            ],
            "search_keywords": ["cà rốt", "ca rot", "củ quả"],
            "is_fallback": True,
            "provider_note": "Chế độ dự phòng quy tắc (offline fallback)."
        }
    else:
        return {
            "produce_name": "Nông sản tươi sạch",
            "category": "Rau củ quả",
            "freshness_score": 85,
            "quality_grade": "Loại 1 (Đạt chuẩn)",
            "visual_assessment": "Nông sản có hình thức đồng đều, màu sắc tươi sáng tự nhiên, cấu trúc còn săn chắc.",
            "defect_analysis": "Chưa ghi nhận dấu hiệu thâm dập lớn hay nấm mốc nghiêm trọng.",
            "shelf_life_days": 4,
            "storage_tips": "Bảo quản ở nơi râm mát hoặc ngăn mát tủ lạnh tùy thuộc vào chủng loại nông sản.",
            "recommended_dishes": [
                "Chế biến món luộc thanh mát",
                "Xào nhanh với tỏi và dầu hào",
                "Nấu canh súp dinh dưỡng cho gia đình"
            ],
            "search_keywords": ["rau", "củ", "quả"],
            "is_fallback": True,
            "provider_note": "Chế độ dự phòng quy tắc (offline fallback)."
        }


def inspect_produce_image(
    image_bytes: bytes,
    mime_type: str = 'image/jpeg',
    filename: str = '',
) -> dict[str, Any]:
    """
    Thẩm định hình ảnh nông sản bằng Gemini Multimodal Vision API.
    Trả về từ điển chứa đầy đủ kết quả giám định và danh sách sản phẩm liên kết từ AgriSense.
    """
    if not image_bytes or len(image_bytes) == 0:
        raise ValueError("Hình ảnh không được để trống.")

    if len(image_bytes) > MAX_FILE_SIZE:
        raise ValueError(f"Dung lượng ảnh vượt quá giới hạn cho phép ({MAX_FILE_SIZE // (1024*1024)}MB).")

    normalized_mime = ALLOWED_MIME_TYPES.get(mime_type.lower())
    if not normalized_mime:
        raise ValueError(f"Định dạng ảnh không được hỗ trợ ({mime_type}). Vui lòng tải file JPG, PNG hoặc WEBP.")

    api_key = getattr(settings, 'GEMINI_API_KEY', None)
    vision_model = getattr(settings, 'GEMINI_VISION_MODEL', 'gemini-3.1-flash-lite')

    # Kiểm tra tính khả dụng của API Key
    if not api_key or api_key in ('your-gemini-api-key', 'your-gemini-key', ''):
        logger.warning("GEMINI_API_KEY chưa cấu hình hoặc không hợp lệ, chuyển sang offline fallback.")
        result = get_rule_based_fallback(filename)
        result['matching_products'] = match_catalog_products(result.get('search_keywords', []), result.get('produce_name', ''))
        return result

    try:
        from google import genai
        from google.genai import types

        client = genai.Client(api_key=api_key)

        prompt = (
            f"{INSPECTOR_SYSTEM_PROMPT}\n\n"
            "Hãy thẩm định hình ảnh nông sản này và trả về JSON chuẩn xác:"
        )

        image_part = types.Part.from_bytes(data=image_bytes, mime_type=normalized_mime)
        config = types.GenerateContentConfig(
            response_mime_type="application/json",
            temperature=0.2,
        )

        response = client.models.generate_content(
            model=vision_model,
            contents=[image_part, prompt],
            config=config,
        )

        text = response.text or ""
        # Làm sạch chuỗi JSON nếu model bọc markdown codeblock
        text = re.sub(r'^```(?:json)?\s*', '', text.strip(), flags=re.MULTILINE)
        text = re.sub(r'\s*```$', '', text.strip(), flags=re.MULTILINE)

        parsed_data = json.loads(text)
        parsed_data['is_fallback'] = False
        parsed_data['model_used'] = vision_model

        # Đảm bảo các trường số học hợp lệ
        freshness = parsed_data.get('freshness_score', 80)
        try:
            parsed_data['freshness_score'] = max(0, min(100, int(freshness)))
        except (ValueError, TypeError):
            parsed_data['freshness_score'] = 80

        shelf_life = parsed_data.get('shelf_life_days', 3)
        try:
            parsed_data['shelf_life_days'] = max(0, int(shelf_life))
        except (ValueError, TypeError):
            parsed_data['shelf_life_days'] = 3

        # Tìm kiếm sản phẩm tương thích trong AgriSense
        keywords = parsed_data.get('search_keywords', [])
        produce_name = parsed_data.get('produce_name', '')
        parsed_data['matching_products'] = match_catalog_products(keywords, produce_name)

        return parsed_data

    except Exception as exc:  # noqa: BLE001
        logger.warning("Gemini Vision API error (%s): %s. Chuyển sang fallback.", type(exc).__name__, exc)
        result = get_rule_based_fallback(filename)
        result['matching_products'] = match_catalog_products(result.get('search_keywords', []), result.get('produce_name', ''))
        result['provider_error'] = type(exc).__name__
        return result
