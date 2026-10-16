# File: apps/traceability/qr_generator.py
"""
Hàm sinh mã QR tự động cho lô hàng nông sản trỏ về trang truy xuất công khai.
Tự động phát hiện IP mạng LAN (192.168.x.x) để điện thoại di động quét và mở được trang web khi kết nối cùng mạng Wi-Fi.
"""
import socket
import os
import qrcode
from io import BytesIO
from django.core.files.base import ContentFile
from django.conf import settings


def get_local_lan_ip():
    """Lấy địa chỉ IPv4 thực tế của máy tính trong mạng nội bộ (Wi-Fi/LAN)"""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return "127.0.0.1"


def generate_qr_code(batch, base_url=None):
    """
    Sinh hình ảnh mã QR định dạng PNG chứa đường dẫn URL tra cứu lô hàng.
    Ưu tiên:
    1. base_url truyền vào (nếu không phải loopback 127.0.0.1)
    2. settings.QR_BASE_URL (nếu có cấu hình trong .env)
    3. http://<LAN_IP>:8000 (cho phép điện thoại quét mở trực tiếp qua Wi-Fi)
    """
    if not base_url or base_url in ("http://127.0.0.1:8000", "http://localhost:8000"):
        configured_url = getattr(settings, 'QR_BASE_URL', None) or os.getenv('QR_BASE_URL')
        if configured_url:
            base_url = configured_url.rstrip('/')
        else:
            lan_ip = get_local_lan_ip()
            base_url = f"http://{lan_ip}:8000"

    trace_url = f"{base_url}/trace/{batch.batch_code}/"
    qr = qrcode.QRCode(
        version=None,
        error_correction=qrcode.constants.ERROR_CORRECT_M,
        box_size=10,
        border=4,
    )
    qr.add_data(trace_url)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    buffer = BytesIO()
    img.save(buffer, format='PNG')
    return ContentFile(buffer.getvalue(), name=f"qr_{batch.batch_code}.png")
