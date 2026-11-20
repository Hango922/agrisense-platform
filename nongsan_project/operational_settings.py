"""Windows loopback operation with Waitress. Public hosting uses production_settings."""
import os

from .settings import *

DEBUG = False
DEMO_MODE = False
OPERATIONAL_MODE = True
RATE_LIMIT_ENABLED = True
ALLOWED_HOSTS = ['127.0.0.1', 'localhost']
VIETQR_BANK_ID = os.getenv('VIETQR_BANK_ID', '')
VIETQR_BANK_NAME = os.getenv('VIETQR_BANK_NAME', '')
VIETQR_ACCOUNT_NO = os.getenv('VIETQR_ACCOUNT_NO', '')
VIETQR_ACCOUNT_NAME = os.getenv('VIETQR_ACCOUNT_NAME', '')
MIDDLEWARE = [MIDDLEWARE[0], 'whitenoise.middleware.WhiteNoiseMiddleware', *MIDDLEWARE[1:]]
MIDDLEWARE += ['apps.accounts.rate_limit.RequestLimitMiddleware']
STORAGES = {
    'default': {'BACKEND': 'django.core.files.storage.FileSystemStorage'},
    'staticfiles': {'BACKEND': 'whitenoise.storage.CompressedManifestStaticFilesStorage'},
}
DATA_UPLOAD_MAX_MEMORY_SIZE = 6 * 1024 * 1024
FILE_UPLOAD_MAX_MEMORY_SIZE = 1024 * 1024
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SAMESITE = 'Lax'
CSRF_COOKIE_SAMESITE = 'Lax'
SESSION_COOKIE_AGE = 12 * 3600
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_REFERRER_POLICY = 'same-origin'
DATABASES['default']['CONN_MAX_AGE'] = 60
DATABASES['default']['CONN_HEALTH_CHECKS'] = True
LOGGING['handlers']['file'].update({
    'class': 'logging.handlers.RotatingFileHandler', 'maxBytes': 10 * 1024 * 1024,
    'backupCount': 5, 'encoding': 'utf-8',
})
