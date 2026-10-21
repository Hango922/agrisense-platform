# File: apps/chatbot/order_assistant.py
"""
Phân hệ Trợ lý Đặt hàng Thông minh (Conversational Ordering Assistant) cho Chatbot AI:
- Nhận diện ý định mua hàng / lên đơn trực tiếp từ câu chat tự nhiên.
- Trích xuất sản phẩm, số lượng, họ tên, số điện thoại, địa chỉ giao hàng và phương thức thanh toán.
- BẮT BUỘC hỏi và cho phép khách hàng lựa chọn hình thức thanh toán (COD hoặc chuyển khoản VietQR).
- Hỗ trợ hội thoại đa lượt (multi-turn) lưu trạng thái qua session.
- Tự động tận dụng sổ địa chỉ mặc định của tài khoản nếu có.
- Tạo đơn hàng chuẩn hóa và giảm trừ tồn kho an toàn trong cơ sở dữ liệu.
"""
import re
from decimal import Decimal
from apps.products.models import Product
from apps.cart_orders.services import create_direct_order
from apps.cart_orders.vietqr import get_vietqr_url, get_vietqr_info
from apps.chatbot.fallback import find_matching_products, format_currency, remove_accents


ORDER_TRIGGERS = [
    r'\b(mua|đặt|dat|lên đơn|len don|tạo đơn|tao don|order|mua hàng|mua hang|đặt hàng|dat hang|ship cho|gửi cho|gui cho|lấy cho|lay cho|giao cho)\b'
]

CANCEL_TRIGGERS = [
    r'\b(hủy|huy|thôi|thoi|không mua|khong mua|dừng|dung|bỏ qua|bo qua|hủy đơn|huy don)\b'
]

CONFIRM_TRIGGERS = [
    r'\b(đồng ý|dong y|ok|okie|xác nhận|xac nhan|đúng rồi|dung roi|chuẩn|chuan|yes|giao đi|giao di|tạo luôn|tao luon|được|duoc|chốt|chot)\b'
]

PHONE_PATTERN = r'(?:\b(?:\+84|0)[35789](?:[\s.-]?\d){8}\b)'

PAYMENT_COD_PATTERN = r'\b(cod|tiền mặt|tien mat|trả sau|tra sau|khi nhận|khi nhan|nhận hàng mới trả|nhan hang moi tra|nhận hàng thanh toán|nhan hang thanh toan)\b'
PAYMENT_VIETQR_PATTERN = r'\b(vietqr|qr|chuyển khoản|chuyen khoan|ck|ngân hàng|ngan hang|chuyển tiền|chuyen tien|banking|napas|quét mã|quet ma|bằng qr|bang qr)\b'


def sanitize_name(name, default_name="Khách hàng"):
    """
    Chuẩn hóa và làm sạch tên người nhận:
    - Loại bỏ khoảng trắng thừa.
    - Giới hạn tối đa 50 ký tự (chuẩn an toàn cho trường CharField 100 của Order).
    - Loại bỏ nếu chứa giá tiền, dấu phân cách đặc biệt, danh sách sản phẩm.
    """
    if not name or not isinstance(name, str):
        return default_name
    cleaned = name.strip()
    if len(cleaned) < 2 or len(cleaned) > 50:
        return default_name
    # Không thể chứa các ký tự đặc biệt của bảng kê hàng hóa
    if any(ch in cleaned for ch in [':', '/', '\\', '$', '%', '^', '*', '{', '}', '[', ']', '|', '<', '>']):
        return default_name
    # Không thể chứa các từ đơn vị tính hoặc giá
    blacklist = {'đ', 'kg', 'vnd', 'vnđ', 'kilo', 'k', 'đồng'}
    words = set(cleaned.lower().split())
    if words & blacklist:
        return default_name
    return cleaned


def extract_phone(text):
    """
    Trích xuất số điện thoại di động Việt Nam:
    - Chấp nhận 10 chữ số bắt đầu bằng 03, 05, 07, 08, 09 (hoặc +843, +845, +847, +848, +849).
    - Hỗ trợ các định dạng phân cách như: 0912.345.678, 0912 345 678, 0912-345-678, +84912345678.
    """
    # 1. Tìm chuỗi số điện thoại định dạng chuẩn có thể chứa khoảng trắng, dấu chấm hoặc gạch nối
    match = re.search(PHONE_PATTERN, text)
    if match:
        clean = re.sub(r'[^\d]', '', match.group(0))
        if clean.startswith('84'):
            clean = '0' + clean[2:]
        if len(clean) == 10 and clean.startswith(('03', '05', '07', '08', '09')):
            return clean

    # 2. Dự phòng: tìm từ khóa "sđt", "sdt", "phone", "đt" theo sau bởi dãy số
    keyword_match = re.search(r'(?:sđt|sdt|đt|dt|phone|tel|số đt|số điện thoại)\s*[:\s]*((?:\+84|0)[\d\s.-]{9,13})', text, re.IGNORECASE)
    if keyword_match:
        clean = re.sub(r'[^\d]', '', keyword_match.group(1))
        if clean.startswith('84'):
            clean = '0' + clean[2:]
        if len(clean) == 10 and clean.startswith(('03', '05', '07', '08', '09')):
            return clean

    return None


def extract_quantity(text, product_name=""):
    """
    Trích xuất số lượng mua từ văn bản (ví dụ: '2kg', '3 bó', '10 hộp', 'mua 5').
    Mặc định là 1 nếu không tìm thấy.
    """
    text_lower = text.lower()
    # 1. Tìm số đứng trước đơn vị (kg, g, bó, hộp, túi, cân, ký, quả, trái)
    unit_match = re.search(r'(\d+)\s*(kg|kilo|ký|ky|cân|can|g|gram|bó|bo|hộp|hop|gói|goi|túi|tui|trái|trai|quả|qua)\b', text_lower)
    if unit_match:
        try:
            return max(1, int(unit_match.group(1)))
        except ValueError:
            pass

    # 2. Tìm số đứng sau từ khóa mua/lấy/đặt (vd: "mua 2 cà rốt")
    action_match = re.search(r'(?:mua|lấy|đặt|cho|order)\s+(\d+)\b', text_lower)
    if action_match:
        try:
            return max(1, int(action_match.group(1)))
        except ValueError:
            pass

    # 3. Tìm số nguyên bất kỳ trong câu ngắn
    any_num = re.search(r'\b(\d+)\b', text_lower)
    if any_num and len(text.split()) <= 10:
        try:
            val = int(any_num.group(1))
            if 1 <= val <= 1000:
                return val
        except ValueError:
            pass

    return 1


def extract_payment_method(text):
    """
    Trích xuất hình thức thanh toán từ câu chat:
    - 'cod': Thanh toán tiền mặt khi nhận hàng (COD)
    - 'vietqr': Chuyển khoản VietQR qua ngân hàng (Napas 247)
    - Trả về None nếu không phát hiện hoặc người dùng chưa chọn.
    """
    text_lower = text.lower().strip()
    # Kiểm tra lựa chọn theo phím số ngắn gọn "1" hoặc "2"
    stripped = text_lower.strip(' .!?,;:()[]{}')
    if stripped in ('1', 'chọn 1', 'chon 1', 'phương thức 1', 'phuong thuc 1', 'hình thức 1', 'hinh thuc 1', 'số 1', 'so 1'):
        return 'cod'
    if stripped in ('2', 'chọn 2', 'chon 2', 'phương thức 2', 'phuong thuc 2', 'hình thức 2', 'hinh thuc 2', 'số 2', 'so 2'):
        return 'vietqr'

    has_vietqr = bool(re.search(PAYMENT_VIETQR_PATTERN, text_lower))
    has_cod = bool(re.search(PAYMENT_COD_PATTERN, text_lower))

    if has_vietqr and not has_cod:
        return 'vietqr'
    if has_cod and not has_vietqr:
        return 'cod'

    if has_vietqr and has_cod:
        m_vqr = re.search(PAYMENT_VIETQR_PATTERN, text_lower)
        m_cod = re.search(PAYMENT_COD_PATTERN, text_lower)
        if m_vqr.start() > m_cod.start():
            return 'vietqr'
        return 'cod'

    return None


def extract_address_and_name(text, phone=None):
    """
    Trích xuất tên người nhận và địa chỉ từ văn bản.
    """
    cleaned = text
    if phone:
        # Xóa số điện thoại và cụm từ khóa đứng trước số điện thoại
        cleaned = re.sub(rf'(?:sđt|sdt|đt|dt|số đt|số điện thoại|so dien thoai|tel|phone)?\s*[:\s]*{phone}', '', cleaned, flags=re.IGNORECASE)

    # Tìm tên người nhận nếu có
    name_match = re.search(
        r'\b(?:tên\s*(?:người\s*nhận|là)?|người\s*nhận|nguoi\s*nhan|anh|chị|chi|em|bác|bac|cô|co)\s*[:\s]+([^\n,.;]+?)(?=\s+(?:ở|tại|sđt|sdt|đt|dt|phone|số|so\b)|[,\n.;]|$)',
        cleaned,
        re.IGNORECASE
    )
    extracted_name = None
    if name_match:
        candidate = name_match.group(1).strip()
        if 2 <= len(candidate) <= 40 and re.match(r'^[A-Za-zÀ-ỹ\s]+$', candidate):
            blacklist = {'đ', 'kg', 'vnd', 'vnđ', 'dong', 'giao', 'ship', 'mua', 'dat', 'xanh', 'do', 'trang', 'don', 'hang'}
            if not (set(candidate.lower().split()) & blacklist):
                extracted_name = candidate
                cleaned = cleaned.replace(name_match.group(0), '')

    # Tìm địa chỉ nếu có
    addr_match = re.search(r'(?:địa chỉ|ở|tại|giao đến|giao về|giao tại|dc|đc)\s*[:\s]+([^\n]+)', cleaned, re.IGNORECASE)
    if addr_match:
        extracted_addr = addr_match.group(1).strip()
    else:
        addr_cues = ['đường', 'phố', 'ngõ', 'ngách', 'số', 'quận', 'huyện', 'phường', 'xã', 'thành phố', 'hà nội', 'hcm', 'đà nẵng', 'hải phòng', 'cần thơ']
        cleaned_lower = cleaned.lower()
        if any(cue in cleaned_lower for cue in addr_cues):
            junk_pattern = r'^(?:sđt|sdt|đt|dt|số điện thoại|so dien thoai|giao|gui|ship|đến|den|về|ve|cho)\s*[:\s]*'
            extracted_addr = re.sub(junk_pattern, '', cleaned.strip(), flags=re.IGNORECASE)
        else:
            extracted_addr = None

    if extracted_addr:
        # Xóa từ rác cuối câu như ", sđt", ", sdt", dấu phẩy, chấm thừa, từ khóa thanh toán
        extracted_addr = re.sub(r'[,.\s]*(?:sđt|sdt|đt|dt|số đt|số điện thoại|phone|tel)?\s*$', '', extracted_addr, flags=re.IGNORECASE)
        extracted_addr = re.sub(r'[,.\s]*(?:thanh toán|tt|pttt)?\s*(?:cod|tiền mặt|chuyển khoản|vietqr).*$', '', extracted_addr, flags=re.IGNORECASE)
        extracted_addr = extracted_addr.strip(',. ')
        if len(extracted_addr) > 255:
            extracted_addr = extracted_addr[:255]

    return extracted_name, extracted_addr


def format_payment_method_prompt(product, qty, name, phone, address, is_update=False):
    """
    Định dạng câu hỏi yêu cầu người dùng chọn hình thức thanh toán kèm tóm tắt đơn:
    Cung cấp cả nút bấm nhanh [button:...] lẫn hướng dẫn gõ phím.
    """
    subtotal = product.price * qty
    shipping_fee = 0 if subtotal >= 500000 else 30000
    final_amount = subtotal + shipping_fee
    ship_txt = "Miễn phí vận chuyển" if shipping_fee == 0 else f"{format_currency(shipping_fee)}"

    header = "🌾 **Đã cập nhật thông tin nhận hàng:**" if is_update else "🌾 **Xác nhận thông tin đặt hàng:**"

    return (
        f"{header}\n"
        f"• Sản phẩm: **{qty} {product.unit} {product.name}** ({format_currency(subtotal)})\n"
        f"• Phí giao hàng: **{ship_txt}** (Miễn phí từ 500.000 đ)\n"
        f"• Tổng thanh toán: **{format_currency(final_amount)}**\n"
        f"• Người nhận: **{name}** - {phone}\n"
        f"• Địa chỉ: **{address}**\n\n"
        f"👉 **Bạn muốn thanh toán theo hình thức nào ạ?**\n"
        f"1️⃣ [button:💵 Thanh toán khi nhận hàng (COD)](COD) — Trả tiền mặt khi nhận hàng\n"
        f"2️⃣ [button:💳 Chuyển khoản VietQR](Chuyển khoản VietQR) — Quét mã QR Napas 247\n\n"
        f"*(Bạn hãy bấm nút ở trên hoặc nhắn **'COD'** / **'Chuyển khoản'** để hoàn tất đơn hàng nhé!)*"
    )


def format_order_success_message(order, product, qty, extra_note=None):
    """
    Định dạng câu trả lời hoàn tất đặt hàng tùy theo hình thức thanh toán đã chọn:
    - Nếu là VietQR: Hiển thị mã QR, thông tin ngân hàng Napas 247 và link tải bill.
    - Nếu là COD: Hiển thị xác nhận giao hàng tiền mặt, lời nhắc chuẩn bị tiền, KHÔNG hiển thị mã QR.
    """
    subtotal = product.price * qty
    ship_txt = "Miễn phí vận chuyển" if order.shipping_fee == 0 else f"{format_currency(order.shipping_fee)}"
    note_line = f"\n• Ghi chú: {extra_note}" if extra_note else ""

    base_info = (
        f"🎉 **ĐẶT HÀNG THÀNH CÔNG QUA CHATBOT AI!**\n\n"
        f"• Mã đơn hàng: **{order.order_code}**\n"
        f"• Sản phẩm: **{qty} {product.unit} {product.name}** ({format_currency(subtotal)})\n"
        f"• Phí giao hàng: **{ship_txt}** (Miễn phí từ 500.000 đ)\n"
        f"• Tổng thanh toán: **{format_currency(order.final_amount)}**\n"
        f"• Người nhận: **{order.full_name}** - {order.phone}\n"
        f"• Địa chỉ: {order.address}{note_line}\n\n"
    )

    if order.payment_method == 'vietqr':
        qr_url = get_vietqr_url(order)
        qr_info = get_vietqr_info(order)
        payment_section = (
            f"💳 **Hình thức thanh toán: Chuyển khoản VietQR (Napas 247)**\n\n"
            f"![Mã VietQR thanh toán {order.order_code}]({qr_url})\n"
            f"• Ngân hàng: **{qr_info['bank_name']}** ({qr_info['bank_id']})\n"
            f"• Số tài khoản: **{qr_info['account_no']}** ({qr_info['account_name']})\n"
            f"• Số tiền: **{format_currency(order.final_amount)}**\n"
            f"• Nội dung CK: **{qr_info['memo']}**\n\n"
            f"👉 [Bấm vào đây để xem chi tiết đơn hàng & quét mã QR](/orders/{order.order_code}/)\n\n"
            f"*(Sau khi chuyển khoản, bạn có thể tải ảnh chụp bill lên trang chi tiết đơn hàng để được xác nhận nhanh nhất nhé!)*\n\n"
            f"Cảm ơn bạn đã tin chọn nông sản sạch tại AgriSense! Đơn hàng sẽ được nhân viên chuẩn bị và giao sớm nhất."
        )
    else:  # COD
        payment_section = (
            f"💵 **Hình thức thanh toán: Thanh toán tiền mặt khi nhận hàng (COD)**\n"
            f"• Trạng thái đơn: **Chờ xác nhận & chuẩn bị hàng**\n"
            f"• Shipper sẽ liên hệ số điện thoại **{order.phone}** trước khi phát hàng.\n"
            f"• Quý khách vui lòng chuẩn bị số tiền **{format_currency(order.final_amount)}** khi nhận nông sản nhé.\n\n"
            f"👉 [Bấm vào đây để xem chi tiết đơn hàng](/orders/{order.order_code}/)\n\n"
            f"Cảm ơn bạn đã tin chọn nông sản sạch tại AgriSense! Nông sản tươi ngon sẽ được giao đến bạn trong thời gian sớm nhất! 🌾"
        )

    return base_info + payment_section


def handle_order_conversation(message, user=None, session_dict=None):
    """
    Hàm điều phối xử lý ý định đặt hàng trong Chatbot:
    Trả về tuple: (handled: bool, reply_text: str)
    Nếu handled == True, câu trả lời sẽ được gửi ngay cho người dùng mà không cần gọi API LLM.
    """
    if session_dict is None:
        session_dict = {}

    msg = message.strip()
    msg_lower = msg.lower()
    draft = session_dict.get('chatbot_order_draft')

    # 1. Kiểm tra ý định HỦY nếu đang có đơn nháp dở dang
    if draft and any(re.search(pat, msg_lower, re.IGNORECASE) for pat in CANCEL_TRIGGERS):
        session_dict.pop('chatbot_order_draft', None)
        return True, "Dạ vâng, tôi đã hủy yêu cầu lên đơn hàng. Bạn có muốn tư vấn thêm nông sản nào khác không ạ? 🌾"

    # 2. Xử lý khi ĐANG CÓ ĐƠN NHÁP DỞ DANG
    if draft:
        step = draft.get('step')
        prod_id = draft.get('product_id')
        qty = draft.get('quantity', 1)

        product = Product.objects.filter(id=prod_id, is_active=True).first()
        if not product:
            session_dict.pop('chatbot_order_draft', None)
            return True, "Rất tiếc, sản phẩm bạn chọn hiện không còn khả dụng trên hệ thống. Bạn vui lòng chọn lại sản phẩm nhé!"

        user_default_name = (user.get_full_name() or user.username if user else 'Khách hàng')

        # A. Đang ở bước CHỜ CHỌN HÌNH THỨC THANH TOÁN (awaiting_payment_method hoặc awaiting_confirm)
        if step in ('awaiting_payment_method', 'awaiting_confirm'):
            # Kiểm tra xem khách có chọn hình thức thanh toán không (COD hoặc VietQR)
            pm = extract_payment_method(msg)
            if pm:
                address_data = {
                    'full_name': sanitize_name(draft.get('full_name'), user_default_name),
                    'phone': draft.get('phone') or '0900000000',
                    'address': draft.get('address') or 'Địa chỉ giao hàng',
                }
                note_suffix = "COD" if pm == 'cod' else "VietQR"
                try:
                    order = create_direct_order(
                        user=user,
                        items_data=[{'product': product, 'quantity': qty}],
                        address_data=address_data,
                        note=f"Đặt hàng tự động qua Chatbot AI ({note_suffix})",
                        payment_method=pm
                    )
                    session_dict.pop('chatbot_order_draft', None)
                    return True, format_order_success_message(order, product, qty)
                except Exception as e:
                    return True, f"⚠️ Rất tiếc, có lỗi xảy ra khi tạo đơn hàng: {str(e)}. Bạn vui lòng thử lại nhé!"

            # Khách có thể gửi SĐT hoặc Địa chỉ mới để đổi nơi nhận
            new_phone = extract_phone(msg)
            new_name, new_addr = extract_address_and_name(msg, new_phone)
            if new_phone:
                draft['phone'] = new_phone
            if new_addr:
                draft['address'] = new_addr
            if new_name:
                draft['full_name'] = sanitize_name(new_name, user_default_name)

            if new_phone or new_addr:
                return True, format_payment_method_prompt(
                    product, qty,
                    draft.get('full_name', user_default_name),
                    draft.get('phone', ''),
                    draft.get('address', ''),
                    is_update=True
                )

            # Khách nhắn "Đồng ý" / "Xác nhận" nhưng chưa chọn hình thức thanh toán cụ thể
            if any(re.search(pat, msg_lower, re.IGNORECASE) for pat in CONFIRM_TRIGGERS):
                return True, (
                    f"🌾 Cảm ơn bạn! Để hoàn tất đơn hàng **{qty} {product.unit} {product.name}**, bạn vui lòng chọn hình thức thanh toán:\n"
                    f"1️⃣ [button:💵 Thanh toán khi nhận hàng (COD)](COD) — Trả tiền mặt cho shipper\n"
                    f"2️⃣ [button:💳 Chuyển khoản VietQR](Chuyển khoản VietQR) — Quét mã QR Napas 247\n\n"
                    f"*(Bạn chỉ cần bấm nút ở trên hoặc nhắn **'COD'** / **'Chuyển khoản'** nhé!)*"
                )

            # Nhắc nhở người dùng chọn phương thức thanh toán
            return True, (
                f"🌾 Bạn vui lòng chọn hình thức thanh toán để tôi hoàn tất đơn ngay nhé:\n"
                f"1️⃣ [button:💵 Thanh toán khi nhận hàng (COD)](COD) — Trả tiền mặt cho shipper khi nhận hàng\n"
                f"2️⃣ [button:💳 Chuyển khoản VietQR](Chuyển khoản VietQR) — Quét mã QR Napas 247\n\n"
                f"*(Hoặc nhắn 'Hủy' nếu bạn muốn đổi ý không mua nữa)*"
            )

        # B. Đang chờ BỔ SUNG thông tin người nhận (SĐT & Địa chỉ)
        if step == 'awaiting_info':
            phone = extract_phone(msg) or draft.get('phone')
            name, addr = extract_address_and_name(msg, phone)
            addr = addr or draft.get('address')
            name = sanitize_name(name or draft.get('full_name'), user_default_name)
            pm = extract_payment_method(msg) or draft.get('payment_method')

            if phone:
                draft['phone'] = phone
            if addr:
                draft['address'] = addr
            draft['full_name'] = name
            if pm:
                draft['payment_method'] = pm

            if phone and addr:
                # Nếu đã có cả phương thức thanh toán trong tin nhắn này (hoặc đã lưu từ trước)
                if pm:
                    address_data = {'full_name': name, 'phone': phone, 'address': addr}
                    note_suffix = "COD" if pm == 'cod' else "VietQR"
                    try:
                        order = create_direct_order(
                            user=user,
                            items_data=[{'product': product, 'quantity': qty}],
                            address_data=address_data,
                            note=f"Đặt hàng tự động qua Chatbot AI ({note_suffix})",
                            payment_method=pm
                        )
                        session_dict.pop('chatbot_order_draft', None)
                        return True, format_order_success_message(order, product, qty)
                    except Exception as e:
                        return True, f"⚠️ Có lỗi khi tạo đơn: {str(e)}. Bạn vui lòng thử lại!"
                else:
                    # Đã có đủ phone & address, CHUYỂN BƯỚC HỎI HÌNH THỨC THANH TOÁN
                    draft['step'] = 'awaiting_payment_method'
                    return True, format_payment_method_prompt(product, qty, name, phone, addr)
            elif not phone:
                return True, (
                    f"🌾 Tôi đã ghi nhận địa chỉ giao hàng: **{addr}**.\n"
                    f"Bạn vui lòng cung cấp thêm **Số điện thoại nhận hàng** để tôi hoàn tất đơn ngay nhé!"
                )
            else:
                return True, (
                    f"🌾 Tôi đã ghi nhận số điện thoại: **{phone}**.\n"
                    f"Bạn vui lòng cung cấp thêm **Địa chỉ giao hàng chi tiết** để tôi chốt đơn nhé!"
                )

    # 3. KIỂM TRA Ý ĐỊNH ĐẶT HÀNG MỚI (New Order Intent)
    is_order_intent = any(re.search(pat, msg_lower, re.IGNORECASE) for pat in ORDER_TRIGGERS)
    if not is_order_intent:
        return False, ""

    # Kiểm tra xác thực tài khoản
    if not user or not user.is_authenticated:
        return True, (
            "🌾 Để lên đơn hàng tự động và theo dõi lộ trình giao hàng, bạn vui lòng "
            "**[Đăng nhập tại đây](/accounts/login/)** hoặc **[Đăng ký tài khoản](/accounts/register/)** nhé!\n"
            "Sau khi đăng nhập, bạn chỉ cần nhắn tên nông sản và số lượng, tôi sẽ hỗ trợ tạo đơn ngay lập tức!"
        )

    # Tìm sản phẩm khách hàng muốn đặt
    products = find_matching_products(msg)
    if not products:
        return True, (
            "🌾 Bạn muốn đặt mua nông sản nào ạ? Hiện AgriSense có sẵn các loại rau củ Đà Lạt, trái cây nhiệt đới, gạo ST25, đặc sản vùng miền...\n"
            "Bạn hãy nhắn: **'Mua [Số lượng] [Tên nông sản]'** (ví dụ: *Mua 2kg Cà rốt Đà Lạt* hoặc *Lên đơn 3kg Gạo ST25*) để tôi hỗ trợ lên đơn ngay nhé!"
        )

    product = products[0]
    qty = extract_quantity(msg, product.name)

    # Kiểm tra tồn kho
    if product.stock <= 0:
        return True, (
            f"🌾 Rất tiếc, sản phẩm **{product.name}** hiện tại đang tạm hết hàng trong kho.\n"
            f"Bạn có muốn tham khảo loại nông sản tương tự cùng danh mục {product.category.name if product.category else ''} không ạ?"
        )

    if qty > product.stock:
        return True, (
            f"🌾 Sản phẩm **{product.name}** hiện chỉ còn **{product.stock} {product.unit}** trong kho.\n"
            f"Bạn có muốn đặt với số lượng **{product.stock} {product.unit}** không ạ?"
        )

    # Trích xuất thông tin nếu khách đã gõ sẵn trong câu lệnh
    user_default_name = (user.get_full_name() or user.username if user else 'Khách hàng')
    phone = extract_phone(msg)
    name, addr = extract_address_and_name(msg, phone)
    name = sanitize_name(name, user_default_name)
    pm = extract_payment_method(msg)

    # Trường hợp A: Khách cung cấp đầy đủ SĐT, Địa chỉ VÀ Phương thức thanh toán ngay trong 1 tin nhắn
    if phone and addr and pm:
        address_data = {'full_name': name, 'phone': phone, 'address': addr}
        note_suffix = "COD" if pm == 'cod' else "VietQR"
        try:
            order = create_direct_order(
                user=user,
                items_data=[{'product': product, 'quantity': qty}],
                address_data=address_data,
                note=f"Đặt hàng tự động qua Chatbot AI ({note_suffix})",
                payment_method=pm
            )
            return True, format_order_success_message(order, product, qty)
        except Exception as e:
            return True, f"⚠️ Có lỗi xảy ra khi tạo đơn hàng: {str(e)}. Bạn vui lòng thử lại nhé!"

    # Trường hợp B: Khách cung cấp đủ SĐT và Địa chỉ, nhưng CHƯA chọn phương thức thanh toán
    if phone and addr and not pm:
        session_dict['chatbot_order_draft'] = {
            'product_id': product.id,
            'quantity': qty,
            'full_name': name,
            'phone': phone,
            'address': addr,
            'step': 'awaiting_payment_method',
        }
        return True, format_payment_method_prompt(product, qty, name, phone, addr)

    # Trường hợp C: Kiểm tra nếu khách có địa chỉ mặc định trong sổ địa chỉ
    def_addr = None
    if hasattr(user, 'addresses'):
        def_addr = user.addresses.filter(is_default=True).first() or user.addresses.first()

    if def_addr:
        # Nếu khách có địa chỉ mặc định VÀ đã nói rõ phương thức thanh toán trong tin nhắn
        if pm:
            address_data = {
                'full_name': sanitize_name(def_addr.full_name, user_default_name),
                'phone': def_addr.phone,
                'address': def_addr.address,
            }
            note_suffix = "COD" if pm == 'cod' else "VietQR"
            try:
                order = create_direct_order(
                    user=user,
                    items_data=[{'product': product, 'quantity': qty}],
                    address_data=address_data,
                    note=f"Đặt hàng tự động qua Chatbot AI ({note_suffix})",
                    payment_method=pm
                )
                return True, format_order_success_message(order, product, qty)
            except Exception as e:
                return True, f"⚠️ Có lỗi xảy ra khi tạo đơn hàng: {str(e)}. Bạn vui lòng thử lại nhé!"

        # Có địa chỉ mặc định nhưng CHƯA chọn phương thức thanh toán -> HỎI PHƯƠNG THỨC THANH TOÁN
        session_dict['chatbot_order_draft'] = {
            'product_id': product.id,
            'quantity': qty,
            'full_name': sanitize_name(def_addr.full_name, user_default_name),
            'phone': def_addr.phone,
            'address': def_addr.address,
            'step': 'awaiting_payment_method',
        }
        return True, format_payment_method_prompt(
            product, qty,
            sanitize_name(def_addr.full_name, user_default_name),
            def_addr.phone,
            def_addr.address
        )
    else:
        # Chưa có địa chỉ mặc định và chưa đủ SĐT/Địa chỉ -> Yêu cầu người dùng cung cấp
        session_dict['chatbot_order_draft'] = {
            'product_id': product.id,
            'quantity': qty,
            'full_name': sanitize_name(name, user_default_name),
            'phone': phone,
            'address': addr,
            'payment_method': pm,
            'step': 'awaiting_info',
        }
        phone_note = f" (SĐT: {phone})" if phone else ""
        subtotal = product.price * qty
        return True, (
            f"🌾 Bạn muốn đặt mua: **{qty} {product.unit} {product.name}**\n"
            f"• Đơn giá: **{format_currency(product.price)}/{product.unit}**\n"
            f"• Tạm tính: **{format_currency(subtotal)}**\n\n"
            f"📦 Để hoàn tất đơn hàng giao tận nơi, bạn vui lòng cung cấp:\n"
            f"• 📞 **Số điện thoại nhận hàng**{phone_note}\n"
            f"• 🏠 **Địa chỉ nhận hàng chi tiết**\n"
            f"*(Ví dụ: 0912345678, số 15 Hai Bà Trưng, Hà Nội)*"
        )
