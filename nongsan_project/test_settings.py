"""Use with manage.py test --settings=nongsan_project.test_settings."""

from copy import deepcopy
from uuid import uuid4

from .settings import *  # noqa: F403

# Preserve configured MySQL credentials while isolating each test invocation.
DATABASES = deepcopy(DATABASES)  # noqa: F405
DATABASES['default']['TEST'] = {'NAME': 'test_agrisense_' + uuid4().hex[:12]}

AI_PROVIDER = 'gemini'
GEMINI_API_KEY = ''
GROQ_API_KEY = ''
QR_BASE_URL = 'http://testserver'

STORAGES = {
    'default': {'BACKEND': 'django.core.files.storage.InMemoryStorage'},
    'staticfiles': {'BACKEND': 'django.contrib.staticfiles.storage.StaticFilesStorage'},
}

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {'console': {'class': 'logging.StreamHandler'}},
    'loggers': {
        'django': {'handlers': ['console'], 'level': 'WARNING'},
        'apps': {'handlers': ['console'], 'level': 'WARNING'},
    },
}
