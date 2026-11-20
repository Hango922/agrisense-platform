"""Run the Windows operational instance on loopback with a production WSGI server."""
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'nongsan_project.operational_settings')

from django.core.management import call_command
from waitress import serve

from nongsan_project.wsgi import application

if __name__ == '__main__':
    call_command('check_operations')
    serve(application, host='127.0.0.1', port=int(os.getenv('PORT', '8000')),
          threads=8, channel_timeout=60, max_request_body_size=6 * 1024 * 1024,
          expose_tracebacks=False)
