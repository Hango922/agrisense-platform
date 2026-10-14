# File: apps/chatbot/order_assistant.py
"""
Phân hệ Trợ lý Đặt hàng Thông minh (Conversational Ordering Assistant) cho Chatbot AI:
- Nhận diện ý định mua hàng / lên đơn trực tiếp từ câu chat tự nhiên.
- Trích xuất sản phẩm, số lượng, họ tên, số điện thoại và địa chỉ giao hàng.
- Hỗ trợ hội thoại đa lượt (multi-turn) lưu trạng thái qua session.
- Tự động tận dụng sổ địa chỉ mặc định của tài khoản nếu có.
- Tạo đơn hàng COD chuẩn hóa và giảm trừ tồn kho an toàn trong cơ sở dữ liệu.
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

PHONE_PATTERN = r'\b(0[3|5|7|8|9]\d{8})\b'


def extract_phone(text):
    """Trích xuất số điện thoại di động Việt Nam (10 số bắt đầu bằng 03, 05, 07, 08, 09)."""
    match = re.search(PHONE_PATTERN, text)
    if match:
        return match.group(1)
    # Tìm kiếm chuỗi số có dấu chấm hoặc khoảng trắng
    clean_digits = re.sub(r'[^\d]', '', text)
    match_clean = re.search(r'(0[3|5|7|8|9]\d{8})', clean_digits)
    return match_clean.group(1) if match_clean else None


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


def extract_address_and_name(text, phone=None):
    """
    Trích xuất tên người nhận và địa chỉ từ văn bản.
    """
    cleaned = text
    if phone:
        # Xóa số điện thoại và cụm từ khóa đứng trước số điện thoại
        cleaned = re.sub(rf'(?:sđt|sdt|đt|dt|số đt|số điện thoại|so dien thoai|tel|phone)?\s*[:\s]*{phone}', '', cleaned, flags=re.IGNORECASE)

    # Tìm tên người nhận nếu có
    name_match = re.search(r'(?:tên|người nhận|anh|chị|em|bác|cô)\s*[:\s]+([^\n,]+)', cleaned, re.IGNORECASE)
    extracted_name = name_match.group(1).strip() if name_match else None
    if extracted_name:
        cleaned = cleaned.replace(name_match.group(0), '')

    # Tìm địa chỉ nếu có
    addr_match = re.search(r'(?:địa chỉ|ở|tại|giao đến|giao về|giao tại|dc|đc)\s*[:\s]+([^\n]+)', cleaned, re.IGNORECASE)
    if addr_match:
        extracted_addr = addr_match.group(1).strip()
    else:
        # Nếu không có từ khóa địa chỉ, kiểm tra xem câu có chứa từ chỉ đường/phố/ngõ/huyện/quận/tỉnh/thành phố không
        addr_cues = ['đường', 'phố', 'ngõ', 'ngách', 'số', 'quận', 'huyện', 'phường', 'xã', 'thành phố', 'hà nội', 'hcm', 'đà nẵng', 'hải phòng', 'cần thơ']
        cleaned_lower = cleaned.lower()
        if any(cue in cleaned_lower for cue in addr_cues):
            # Cắt các từ rác đầu câu
            junk_pattern = r'^(?:sđt|sdt|đt|dt|số điện thoại|so dien thoai|giao|gui|ship|đến|den|về|ve|cho)\s*[:\s]*'
            extracted_addr = re.sub(junk_pattern, '', cleaned.strip(), flags=re.IGNORECASE)
        else:
            extracted_addr = None

    if extracted_addr:
        # Xóa từ rác cuối câu như ", sđt", ", sdt", dấu phẩy, chấm thừa
        extracted_addr = re.sub(r'[,.\s]*(?:sđt|sdt|đt|dt|số đt|số điện thoại|phone|tel)?\s*$', '', extracted_addr, flags=re.IGNORECASE)
        extracted_addr = extracted_addr.strip(',. ')

    return extracted_name, extracted_addr


def format_order_success_message(order, product, qty, extra_note=None):
    """Định dạng câu trả lời hoàn tất đặt hàng kèm thông tin chuyển khoản VietQR Napas 247."""
    subtotal = product.price * qty
    ship_txt = "Miễn phí vận chuyển" if order.shipping_fee == 0 else f"{format_currency(order.shipping_fee)}"
    qr_url = get_vietqr_url(order)
    qr_info = get_vietqr_info(order)

    note_line = f"\n• Ghi chú: {extra_note}" if extra_note else ""

    return (
        f"🎉 **ĐẶT HÀNG THÀNH CÔNG QUA CHATBOT AI!**\n\n"
        f"• Mã đơn hàng: **{order.order_code}**\n"
        f"• Sản phẩm: **{qty} {product.unit} {product.name}** ({format_currency(subtotal)})\n"
        f"• Phí giao hàng: **{ship_txt}** (Miễn phí từ 500.000 đ)\n"
        f"• Tổng thanh toán: **{format_currency(order.final_amount)}**\n"
        f"• Người nhận: **{order.full_name}** - {order.phone}\n"
        f"• Địa chỉ: {order.address}{note_line}\n\n"
        f"💳 **Thanh toán chuyển khoản VietQR (Napas 247):**\n"
        f"![Mã VietQR thanh toán {order.order_code}]({qr_url})\n"
        f"• Ngân hàng: **{qr_info['bank_name']}** ({qr_info['bank_id']})\n"
        f"• Số tài khoản: **{qr_info['account_no']}** ({qr_info['account_name']})\n"
        f"• Số tiền: **{format_currency(order.final_amount)}**\n"
        f"• Nội dung CK: **{qr_info['memo']}**\n\n"
        f"👉 [Bấm vào đây để xem chi tiết đơn hàng & quét mã QR](/orders/{order.order_code}/)\n\n"
        f"Cảm ơn bạn đã tin chọn nông sản sạch tại AgriSense! Đơn hàng sẽ được nhân viên chuẩn bị và giao sớm nhất."
    )


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

        # A. Đang chờ XÁC NHẬN đơn với địa chỉ có sẵn
        if step == 'awaiting_confirm':
            # Kiểm tra nếu khách xác nhận đồng ý
            if any(re.search(pat, msg_lower, re.IGNORECASE) for pat in CONFIRM_TRIGGERS):
                address_data = {
                    'full_name': draft.get('full_name') or user.username,
                    'phone': draft.get('phone') or '0900000000',
                    'address': draft.get('address') or 'Địa chỉ giao hàng',
                }
                try:
                    order = create_direct_order(
                        user=user,
                        items_data=[{'product': product, 'quantity': qty}],
                        address_data=address_data,
                        note="Đặt hàng tự động qua Chatbot AI (Xác nhận địa chỉ mặc định)"
                    )
                    session_dict.pop('chatbot_order_draft', None)
                    return True, format_order_success_message(order, product, qty)
                except Exception as e:
                    return True, f"⚠️ Rất tiếc, có lỗi xảy ra khi tạo đơn hàng: {str(e)}. Bạn vui lòng thử lại nhé!"

            # Khách không bấm đồng ý mà cung cấp SĐT / Địa chỉ mới
            new_phone = extract_phone(msg)
            new_name, new_addr = extract_address_and_name(msg, new_phone)
            if new_phone:
                draft['phone'] = new_phone
            if new_addr:
                draft['address'] = new_addr
            if new_name:
                draft['full_name'] = new_name

            if draft.get('phone') and draft.get('address'):
                address_data = {
                    'full_name': draft.get('full_name') or user.username,
                    'phone': draft.get('phone'),
                    'address': draft.get('address'),
                }
                try:
                    order = create_direct_order(
                        user=user,
                        items_data=[{'product': product, 'quantity': qty}],
                        address_data=address_data,
                        note="Đặt hàng tự động qua Chatbot AI (Địa chỉ chỉ định)"
                    )
                    session_dict.pop('chatbot_order_draft', None)
                    return True, format_order_success_message(order, product, qty)
                except Exception as e:
                    return True, f"⚠️ Có lỗi khi tạo đơn: {str(e)}. Bạn vui lòng thử lại!"

        # B. Đang chờ BỔ SUNG thông tin người nhận (SĐT & Địa chỉ)
        if step == 'awaiting_info':
            phone = extract_phone(msg) or draft.get('phone')
            name, addr = extract_address_and_name(msg, phone)
            addr = addr or draft.get('address')
            name = name or draft.get('full_name') or (user.get_full_name() or user.username if user else 'Khách hàng')

            if phone:
                draft['phone'] = phone
            if addr:
                draft['address'] = addr
            if name:
                draft['full_name'] = name

            if phone and addr:
                address_data = {'full_name': name, 'phone': phone, 'address': addr}
                try:
                    order = create_direct_order(
                        user=user,
                        items_data=[{'product': product, 'quantity': qty}],
                        address_data=address_data,
                        note="Đặt hàng tự động qua Chatbot AI"
                    )
                    session_dict.pop('chatbot_order_draft', None)
                    return True, format_order_success_message(order, product, qty)
                except Exception as e:
                    return True, f"⚠️ Có lỗi khi tạo đơn: {str(e)}. Bạn vui lòng thử lại!"
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
            "🌾 Để lên đơn hàng tự động và theo dõi lộ trình giao hàng COD, bạn vui lòng "
            "**[Đăng nhập tại đây](/accounts/login/)** hoặc **[Đăng ký tài khoản](/accounts/register/)** nhé!\n"
            "Sau khi đăng nhập, bạn chỉ cần nhắn tên nông sản và số lượng, tôi sẽ tạo đơn ngay lập tức!"
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

    # Trích xuất số điện thoại và địa chỉ nếu khách đã gõ sẵn trong câu lệnh (1-Turn Order)
    phone = extract_phone(msg) or getattr(user, 'phone', '')
    name, addr = extract_address_and_name(msg, phone)
    name = name or (user.get_full_name() or user.username)

    subtotal = product.price * qty

    # Nếu khách đã cung cấp đầy đủ cả SĐT và Địa chỉ ngay trong 1 tin nhắn
    if phone and addr:
        address_data = {'full_name': name, 'phone': phone, 'address': addr}
        try:
            order = create_direct_order(
                user=user,
                items_data=[{'product': product, 'quantity': qty}],
                address_data=address_data,
                note="Đặt hàng tự động qua Chatbot AI (Trực tiếp)"
            )
            return True, format_order_success_message(order, product, qty)
        except Exception as e:
            return True, f"⚠️ Có lỗi xảy ra khi tạo đơn hàng: {str(e)}. Bạn vui lòng thử lại nhé!"

    # Nếu chưa có đủ SĐT hoặc Địa chỉ, kiểm tra xem user có địa chỉ mặc định trong sổ địa chỉ không
    def_addr = None
    if hasattr(user, 'addresses'):
        def_addr = user.addresses.filter(is_default=True).first() or user.addresses.first()

    if def_addr:
        session_dict['chatbot_order_draft'] = {
            'product_id': product.id,
            'quantity': qty,
            'full_name': def_addr.full_name,
            'phone': def_addr.phone,
            'address': def_addr.address,
            'step': 'awaiting_confirm',
        }
        return True, (
            f"🌾 Bạn muốn đặt mua: **{qty} {product.unit} {product.name}**\n"
            f"• Đơn giá: **{format_currency(product.price)}/{product.unit}**\n"
            f"• Tạm tính: **{format_currency(subtotal)}**\n\n"
            f"📍 Tôi thấy bạn có địa chỉ giao hàng sẵn có:\n"
            f"• Người nhận: **{def_addr.full_name}** ({def_addr.phone})\n"
            f"• Địa chỉ: **{def_addr.address}**\n\n"
            f"👉 Bạn hãy nhắn **'Đồng ý'** để tạo đơn ngay, hoặc nhắn SĐT và Địa chỉ mới để tôi giao đến nơi khác nhé!"
        )
    else:
        session_dict['chatbot_order_draft'] = {
            'product_id': product.id,
            'quantity': qty,
            'full_name': name,
            'phone': phone,
            'address': addr,
            'step': 'awaiting_info',
        }
        phone_note = f" (SĐT: {phone})" if phone else ""
        return True, (
            f"🌾 Bạn muốn đặt mua: **{qty} {product.unit} {product.name}**\n"
            f"• Đơn giá: **{format_currency(product.price)}/{product.unit}**\n"
            f"• Tạm tính: **{format_currency(subtotal)}**\n\n"
            f"📦 Để hoàn tất đơn hàng giao tận nơi thanh toán khi nhận (COD), bạn vui lòng cung cấp:\n"
            f"• 📞 **Số điện thoại nhận hàng**{phone_note}\n"
            f"• 🏠 **Địa chỉ nhận hàng chi tiết**\n"
            f"*(Ví dụ: 0912345678, số 15 Hai Bà Trưng, Hà Nội)*"
        )
