# File: apps/traceability/qr_generator.py
"""
Hàm sinh mã QR tự động cho lô hàng nông sản trỏ về trang truy xuất công khai.
"""
import qrcode
from io import BytesIO
from django.core.files.base import ContentFile


def generate_qr_code(batch, base_url="http://127.0.0.1:8000"):
    """
    Sinh hình ảnh mã QR định dạng PNG chứa đường dẫn URL tra cứu lô hàng http://127.0.0.1:8000/trace/<batch_code>/
    """
    trace_url = f"{base_url}/trace/{batch.batch_code}/"
    qr = qrcode.QRCode(
        version=1,
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
