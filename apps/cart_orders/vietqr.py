# File: apps/cart_orders/vietqr.py
"""
Tiện ích sinh mã thanh toán VietQR chuẩn Napas 247 động cho từng đơn hàng nông sản.
Hỗ trợ tạo mã QR tự động nhúng số tiền và mã đơn hàng (ORDxxxxxxxx) giúp khách hàng
quét thanh toán nhanh qua mọi ứng dụng ngân hàng di động (Mobile Banking).
"""
from urllib.parse import quote
from django.conf import settings

DEFAULT_BANK_ID = getattr(settings, 'VIETQR_BANK_ID', 'TCB')
DEFAULT_ACCOUNT_NO = getattr(settings, 'VIETQR_ACCOUNT_NO', '7979798950')
DEFAULT_ACCOUNT_NAME = getattr(settings, 'VIETQR_ACCOUNT_NAME', 'NGUYEN HONG HOANG')
DEFAULT_BANK_NAME = getattr(settings, 'VIETQR_BANK_NAME', 'Techcombank')


def get_vietqr_url(order, template='compact2'):
    """
    Sinh đường dẫn hình ảnh mã VietQR động trực tiếp từ cổng Napas VietQR.
    Tự động điền: Số tiền chính xác của đơn hàng, Nội dung chuyển khoản là Mã đơn hàng.
    """
    bank_id = getattr(settings, 'VIETQR_BANK_ID', DEFAULT_BANK_ID)
    account_no = getattr(settings, 'VIETQR_ACCOUNT_NO', DEFAULT_ACCOUNT_NO)
    account_name_raw = getattr(settings, 'VIETQR_ACCOUNT_NAME', DEFAULT_ACCOUNT_NAME)

    amount = int(order.final_amount)
    memo = order.order_code
    account_name = quote(account_name_raw)
    encoded_memo = quote(memo)

    url = (
        f"https://img.vietqr.io/image/{bank_id}-{account_no}-{template}.png"
        f"?amount={amount}&addInfo={encoded_memo}&accountName={account_name}"
    )
    return url


def get_vietqr_info(order):
    """
    Trả về thông tin chi tiết chuyển khoản ngân hàng phục vụ hiển thị trên giao diện đơn hàng và Chatbot.
    """
    bank_id = getattr(settings, 'VIETQR_BANK_ID', DEFAULT_BANK_ID)
    bank_name = getattr(settings, 'VIETQR_BANK_NAME', DEFAULT_BANK_NAME)
    account_no = getattr(settings, 'VIETQR_ACCOUNT_NO', DEFAULT_ACCOUNT_NO)
    account_name = getattr(settings, 'VIETQR_ACCOUNT_NAME', DEFAULT_ACCOUNT_NAME)

    return {
        'bank_id': bank_id,
        'bank_name': bank_name,
        'account_no': account_no,
        'account_name': account_name,
        'amount': int(order.final_amount),
        'transfer_content': order.order_code,
        'memo': order.order_code,
        'qr_image_url': get_vietqr_url(order),
        'user_qr_card': '/static/images/techcombank_qr.png',
    }
