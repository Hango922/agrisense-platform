"""Local presentation environment: python manage.py runserver --settings=..."""
from .settings import *  # noqa: F403, RUF100

DEBUG = True
DEMO_MODE = True
ALLOWED_HOSTS = ['127.0.0.1', 'localhost', 'testserver']
DATABASES = {'default': {'ENGINE': 'django.db.backends.sqlite3', 'NAME': BASE_DIR / 'demo.sqlite3'}}  # noqa: F405, RUF100
MEDIA_ROOT = BASE_DIR / 'media' / 'demo'  # noqa: F405, RUF100
QR_BASE_URL = 'http://127.0.0.1:8001'
PAYMENT_WEBHOOK_SECRET = ''
GEMINI_API_KEY = ''
GROQ_API_KEY = ''
