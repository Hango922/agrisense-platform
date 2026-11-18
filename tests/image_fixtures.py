from io import BytesIO

from django.core.files.uploadedfile import SimpleUploadedFile
from PIL import Image


def png_upload(name='bill.png'):
    output = BytesIO()
    Image.new('RGB', (8, 8), 'white').save(output, format='PNG')
    return SimpleUploadedFile(name, output.getvalue(), content_type='image/png')
