"""Public HTTPS deployment. Fail closed when required configuration is missing."""
import os
from urllib.parse import urlparse

from django.core.exceptions import ImproperlyConfigured

from .operational_settings import *

ALLOWED_HOSTS = [h.strip() for h in os.getenv('PUBLIC_HOSTS', '').split(',') if h.strip()]
if not ALLOWED_HOSTS or any(h in ('*', 'localhost', '127.0.0.1') or '/' in h for h in ALLOWED_HOSTS):
    raise ImproperlyConfigured('Set PUBLIC_HOSTS to explicit public hostnames.')
if not SECRET_KEY or len(SECRET_KEY) < 50 or SECRET_KEY.startswith('django-insecure-'):
    raise ImproperlyConfigured('Production requires a strong SECRET_KEY of at least 50 characters.')
if urlparse(QR_BASE_URL).scheme != 'https' or urlparse(QR_BASE_URL).hostname not in ALLOWED_HOSTS:
    raise ImproperlyConfigured('QR_BASE_URL must be HTTPS on a configured PUBLIC_HOSTS hostname.')
if DATABASES['default']['USER'] == 'root':
    raise ImproperlyConfigured('Use a dedicated non-root database account for production.')
CSRF_TRUSTED_ORIGINS = ['https://' + host for host in ALLOWED_HOSTS]
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = False
# Enable only behind a proxy that overwrites this header and blocks direct access.
if os.getenv('TRUST_HTTPS_PROXY') == 'True':
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
