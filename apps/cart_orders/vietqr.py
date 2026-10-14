# File: apps/cart_orders/vietqr.py
"""
Tiện ích sinh mã thanh toán VietQR chuẩn Napas 247 động cho từng đơn hàng nông sản.
Hỗ trợ tạo mã QR tự động nhúng số tiền và mã đơn hàng (ORDxxxxxxxx) giúp khách hàng
quét thanh toán nhanh qua mọi ứng dụng ngân hàng di động (Mobile Banking).
"""
from urllib.parse import quote
from django.conf import settings

DEFAULT_BANK_ID = getattr(settings, 'VIETQR_BANK_ID', 'MB')
DEFAULT_ACCOUNT_NO = getattr(settings, 'VIETQR_ACCOUNT_NO', '0922334455')
DEFAULT_ACCOUNT_NAME = getattr(settings, 'VIETQR_ACCOUNT_NAME', 'NGUYEN HONG HOANG')
DEFAULT_BANK_NAME = getattr(settings, 'VIETQR_BANK_NAME', 'Ngân hàng Quân Đội (MBBank)')


def get_vietqr_url(order, template='compact2'):
    """
    Sinh đường dẫn hình ảnh mã VietQR động trực tiếp từ cổng Napas VietQR.
    Tự động điền: Số tiền chính xác của đơn hàng, Nội dung chuyển khoản là Mã đơn hàng.
    """
    amount = int(order.final_amount)
    memo = order.order_code
    account_name = quote(DEFAULT_ACCOUNT_NAME)
    encoded_memo = quote(memo)

    url = (
        f"https://img.vietqr.io/image/{DEFAULT_BANK_ID}-{DEFAULT_ACCOUNT_NO}-{template}.png"
        f"?amount={amount}&addInfo={encoded_memo}&accountName={account_name}"
    )
    return url


def get_vietqr_info(order):
    """
    Trả về thông tin chi tiết chuyển khoản ngân hàng phục vụ hiển thị trên giao diện đơn hàng và Chatbot.
    """
    return {
        'bank_id': DEFAULT_BANK_ID,
        'bank_name': DEFAULT_BANK_NAME,
        'account_no': DEFAULT_ACCOUNT_NO,
        'account_name': DEFAULT_ACCOUNT_NAME,
        'amount': int(order.final_amount),
        'transfer_content': order.order_code,
        'memo': order.order_code,
        'qr_image_url': get_vietqr_url(order),
    }
