# File: apps/chatbot/fallback.py
"""
Bộ quy tắc nhận diện từ khóa (Rule-based Fallback) hỗ trợ cả tiếng Việt có dấu và không dấu
kết hợp truy vấn trực tiếp cơ sở dữ liệu nông sản thực tế (giá cả, tồn kho, xuất xứ, bảo quản, đơn hàng)
khi API AI gặp sự cố, timeout hoặc chưa có API key.
"""
import re
import unicodedata
from .prompts import FALLBACK_RESPONSES

FALLBACK_RULES = [
    (r'\b(đơn hàng|don hang|order|giao chưa|giao chua|ship|vận chuyển|van chuyen)\b', 'order'),
    (r'\b(nguồn gốc|nguon goc|xuất xứ|xuat xu|ở đâu|o dau|vùng trồng|vung trong|trang trại|trang trai)\b', 'origin'),
    (r'\b(bảo quản|bao quan|hạn sử dụng|han su dung|tủ lạnh|tu lanh|để được bao lâu|de duoc bao lau)\b', 'storage'),
    (r'\b(giá|gia|bao nhiêu|bao nhieu|tiền|tien|price|cost)\b', 'price'),
]

RECOMMEND_PATTERNS = r'\b(tư vấn|tu van|gợi ý|goi y|nên mua|nen mua|bán chạy|ban chay|món ngon|mon ngon|loại nào ngon|loai nao ngon|nông sản hot|nong san hot|mua gì|mua gi)\b'
GREETING_PATTERNS = r'^(xin chào|xin chao|chào|chao|hello|hi|hey|alo)\b'


def remove_accents(input_str):
    """Chuyển chuỗi tiếng Việt có dấu thành không dấu và chữ thường."""
    if not input_str:
        return ""
    s1 = unicodedata.normalize('NFD', str(input_str))
    s2 = ''.join(c for c in s1 if unicodedata.category(c) != 'Mn')
    return s2.replace('đ', 'd').replace('Đ', 'D').lower()


def find_matching_products(message):
    """
    Tìm kiếm sản phẩm liên quan trong cơ sở dữ liệu dựa trên tên và từ khóa,
    hỗ trợ cả tiếng Việt có dấu và không dấu (kể cả lỗi gõ như GiGia cam sanh).
    """
    try:
        from apps.products.models import Product
    except ImportError:
        return []

    clean_msg = remove_accents(message)
    # Loại bỏ các từ hỏi giá, hỏi thông tin phổ biến để tránh làm nhiễu từ khóa sản phẩm
    noise_words = [
        'gigia', 'gia', 'bao', 'nhieu', 'tien', 'la', 'hien', 'tai', 'the', 'nao',
        'co', 'ngon', 'khong', 'mua', 'o', 'dau', 'xuat', 'xu', 'nguon', 'goc',
        'cach', 'bao', 'quan', 'xin', 'chao', 'cho', 'hoi', 'toi', 'minh', 'ban'
    ]
    words_in_msg = [w for w in clean_msg.split() if w not in noise_words and len(w) > 1]
    filtered_clean_msg = " ".join(words_in_msg)

    try:
        products = list(Product.objects.filter(is_active=True).select_related('supplier', 'category'))
    except Exception:
        return []

    scored = []
    for p in products:
        p_clean = remove_accents(p.name)
        # 1. Trùng khớp trực tiếp cụm từ đầy đủ
        if p_clean in clean_msg:
            scored.append((len(p_clean) * 3, p))
            continue

        # 2. Kiểm tra n-gram từ tên sản phẩm (vd: "cam sanh" trong "Cam sành Hà Giang")
        p_words = p_clean.split()
        matched_ngram_len = 0
        for i in range(len(p_words)):
            for j in range(i + 2, len(p_words) + 1):
                ngram = " ".join(p_words[i:j])
                if ngram in clean_msg or ngram in filtered_clean_msg:
                    matched_ngram_len = max(matched_ngram_len, len(ngram))
        if matched_ngram_len > 0:
            scored.append((matched_ngram_len * 2, p))
            continue

        # 3. Trùng khớp từng từ khóa riêng lẻ
        hits = 0
        for w in words_in_msg:
            if w in p_clean:
                hits += 1
        if hits >= 2 or (len(words_in_msg) == 1 and hits == 1):
            scored.append((hits, p))

    scored.sort(key=lambda x: x[0], reverse=True)
    results = []
    seen = set()
    for _, p in scored:
        if p.id not in seen:
            seen.add(p.id)
            results.append(p)
    return results


def format_currency(amount):
    """Định dạng tiền tệ theo chuẩn Việt Nam (vd: 45.000 đ)."""
    return f"{int(amount):,} đ".replace(',', '.')


def get_fallback_response(message, user=None):
    """
    So khớp câu hỏi với các mẫu biểu thức chính quy (Regex) không phân biệt hoa thường,
    kết hợp truy vấn dữ liệu thời gian thực từ cơ sở dữ liệu để tư vấn thông minh.
    """
    msg = message.strip()
    msg_lower = msg.lower()

    # Xác định intent chính từ FALLBACK_RULES
    matched_key = None
    for pattern, key in FALLBACK_RULES:
        if re.search(pattern, msg_lower, re.IGNORECASE):
            matched_key = key
            break

    # Tìm sản phẩm liên quan
    products = find_matching_products(msg)

    # 1. Xử lý câu hỏi về GIÁ
    if matched_key == 'price':
        if products:
            if len(products) == 1:
                p = products[0]
                price_str = format_currency(p.price)
                stock_str = f"còn {p.stock} {p.unit} trong kho" if p.stock > 0 else "hiện tạm hết hàng"
                origin_str = f", xuất xứ từ {p.origin}" if p.origin else ""
                cert_str = f", chuẩn an toàn {p.supplier.certification}" if (p.supplier and p.supplier.certification) else ""
                return (
                    f"🌾 **{p.name}** hiện có giá **{price_str}/{p.unit}** ({stock_str}){origin_str}{cert_str}.\n"
                    f"Sản phẩm tươi sạch và có sẵn giao nhanh. Bạn có thể thêm ngay vào giỏ hàng nhé!",
                    'price'
                )
            else:
                lines = ["🌾 Hiện tại AgriSense có các sản phẩm phù hợp với bạn:"]
                for p in products[:4]:
                    p_price = format_currency(p.price)
                    lines.append(f"• **{p.name}**: **{p_price}/{p.unit}** (Kho: {p.stock} {p.unit})")
                lines.append("Bạn vui lòng xem giá chi tiết tại trang sản phẩm hoặc chọn loại bạn muốn đặt nhé!")
                return ("\n".join(lines), 'price')
        else:
            return (
                "Bạn vui lòng xem giá chi tiết tại trang sản phẩm hoặc cho tôi biết tên cụ thể nông sản bạn quan tâm (ví dụ: cam sành, hành tây, gạo ST25,...) để tôi báo giá chính xác nhé!",
                'price'
            )

    # 2. Xử lý câu hỏi về NGUỒN GỐC / XUẤT XỨ
    if matched_key == 'origin':
        if products:
            p = products[0]
            sup_name = p.supplier.name if p.supplier else "Nông trại liên kết AgriSense"
            cert = p.supplier.certification if (p.supplier and p.supplier.certification) else "VietGAP"
            origin = p.origin or (p.supplier.address if p.supplier else "Việt Nam")
            return (
                f"🌾 **{p.name}** có nguồn gốc xuất xứ từ **{origin}**, được cung cấp bởi **{sup_name}** theo tiêu chuẩn an toàn **{cert}**.\n"
                f"Bạn có thể quét mã QR trên bao bì lô hàng để xem nguồn gốc chi tiết và quy trình canh tác minh bạch!",
                'origin'
            )
        else:
            return (
                "Tất cả nông sản tại AgriSense đều có nguồn gốc rõ ràng từ các nông trại sạch trên toàn quốc đạt chuẩn VietGAP/GlobalGAP. "
                "Bạn có thể quét mã QR trên bao bì để xem nguồn gốc chi tiết.",
                'origin'
            )

    # 3. Xử lý câu hỏi về BẢO QUẢN
    if matched_key == 'storage':
        if products:
            p = products[0]
            storage_text = p.storage.strip() if p.storage else "Bảo quản nơi khô ráo, thoáng mát hoặc trong ngăn mát tủ lạnh (1-4°C)."
            usage_text = f"\n💡 **Gợi ý sử dụng**: {p.usage.strip()}" if p.usage else ""
            return (
                f"🌾 **Cách bảo quản {p.name}**:\n"
                f"{storage_text}{usage_text}\n"
                f"Bảo quản đúng cách sẽ giúp nông sản giữ trọn độ tươi ngon và dưỡng chất tự nhiên!",
                'storage'
            )
        else:
            return (
                "Bảo quản nông sản nên để nơi khô ráo, thoáng mát hoặc bảo quản trong ngăn mát tủ lạnh (1-4°C) có bọc màng thực phẩm hoặc túi giấy để giữ độ tươi ngon.",
                'storage'
            )

    # 4. Xử lý câu hỏi về ĐƠN HÀNG
    if matched_key == 'order':
        try:
            from apps.cart_orders.models import Order
            code_match = re.search(r'\b(ORD[A-Za-z0-9_-]+)\b', msg, re.IGNORECASE)
            if code_match:
                code = code_match.group(1)
                order = Order.objects.filter(order_code__iexact=code).first()
                if order:
                    status_dict = {
                        'pending': 'Chờ xác nhận',
                        'confirmed': 'Đã xác nhận (đang chuẩn bị hàng)',
                        'shipping': 'Đang vận chuyển giao hàng',
                        'delivered': 'Đã giao thành công',
                        'cancelled': 'Đã hủy',
                    }
                    st = status_dict.get(order.status, order.status)
                    amount_str = format_currency(order.final_amount)
                    return (
                        f"📦 **Thông tin đơn hàng {order.order_code}**:\n"
                        f"• Người nhận: {order.full_name} ({order.phone})\n"
                        f"• Trạng thái: **{st}**\n"
                        f"• Tổng thanh toán: **{amount_str}**\n"
                        f"• Địa chỉ: {order.address}\n"
                        f"Bạn có thể vào mục 'Đơn hàng của tôi' để theo dõi tiến độ chi tiết.",
                        'order'
                    )
            if user and getattr(user, 'is_authenticated', False):
                last_order = Order.objects.filter(user=user).order_by('-created_at').first()
                if last_order:
                    status_dict = {
                        'pending': 'Chờ xác nhận',
                        'confirmed': 'Đã xác nhận',
                        'shipping': 'Đang giao hàng',
                        'delivered': 'Đã giao thành công',
                        'cancelled': 'Đã hủy',
                    }
                    st = status_dict.get(last_order.status, last_order.status)
                    return (
                        f"📦 Đơn hàng gần nhất của bạn là **{last_order.order_code}** (Trạng thái: **{st}**, "
                        f"Tổng tiền: {format_currency(last_order.final_amount)}).\n"
                        f"Bạn vui lòng vào mục 'Đơn hàng của tôi' để kiểm tra chi tiết.",
                        'order'
                    )
        except Exception:
            pass
        return (
            "Bạn vui lòng vào mục 'Đơn hàng của tôi' để kiểm tra hoặc gửi kèm mã đơn hàng (ví dụ: ORD84630304) để tôi tra cứu giúp bạn nhé!",
            'order'
        )

    # 5. Xử lý câu hỏi TƯ VẤN / GỢI Ý MUA SẮM
    if re.search(RECOMMEND_PATTERNS, msg_lower, re.IGNORECASE):
        try:
            from apps.products.models import Product
            featured = list(Product.objects.filter(is_active=True).order_by('-created_at')[:4])
            if featured:
                lines = ["🌾 **AgriSense gợi ý những nông sản sạch thơm ngon, được yêu thích nhất hôm nay**:"]
                for p in featured:
                    p_price = format_currency(p.price)
                    cert_note = f" (Chuẩn {p.supplier.certification})" if (p.supplier and p.supplier.certification) else ""
                    lines.append(f"• **{p.name}**: **{p_price}/{p.unit}** (Kho: {p.stock} {p.unit}){cert_note}")
                lines.append("Bạn muốn tư vấn thêm về món nào hoặc cần cách chế biến loại nào ạ?")
                return ("\n".join(lines), 'default')
        except Exception:
            pass

    # 6. Xử lý CHÀO HỎI
    if re.search(GREETING_PATTERNS, msg_lower, re.IGNORECASE):
        return (
            "Xin chào bạn! Tôi là Trợ lý Nông Sản AI của AgriSense 🌾.\n"
            "Tôi có thể tư vấn giá bán, xuất xứ trang trại, cách bảo quản, gợi ý nông sản sạch và tra cứu đơn hàng giúp bạn.\n"
            "Hôm nay bạn đang muốn tìm nông sản hay món ăn gì ạ?",
            'default'
        )

    # 7. Xử lý khi người dùng NHẮC ĐẾN MỘT SẢN PHẨM CỤ THỂ
    if products:
        p = products[0]
        price_str = format_currency(p.price)
        cert_str = f" theo tiêu chuẩn {p.supplier.certification}" if (p.supplier and p.supplier.certification) else ""
        desc_str = f"\n• **Mô tả**: {p.description.strip()}" if p.description else ""
        storage_str = f"\n• **Bảo quản**: {p.storage.strip()}" if p.storage else ""
        return (
            f"🌾 **Tư vấn nông sản: {p.name}**\n"
            f"• **Giá bán**: **{price_str}/{p.unit}** (Còn {p.stock} {p.unit} trong kho)\n"
            f"• **Xuất xứ**: {p.origin or 'Việt Nam'}{cert_str}"
            f"{desc_str}"
            f"{storage_str}\n"
            f"Bạn có muốn thêm {p.name} vào giỏ hàng ngay hôm nay không ạ?",
            'default'
        )

    # 8. Mặc định
    return (FALLBACK_RESPONSES['default'], 'default')
