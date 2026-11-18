"""Regression checks for the isolated Django test runtime."""

import json
import os
import subprocess
import sys
import textwrap
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


class TestRuntimeTests(unittest.TestCase):
    def run_python(self, source):
        env = os.environ.copy()
        env.update({
            'DJANGO_SETTINGS_MODULE': 'nongsan_project.test_settings',
            'SECRET_KEY': 'test-runtime-key-not-for-deployment',
            'DB_NAME': 'bootstrap_source_must_not_be_modified',
            'GEMINI_API_KEY': 'configured-key-must-not-be-used',
            'GROQ_API_KEY': 'configured-key-must-not-be-used',
        })
        result = subprocess.run(
            [sys.executable, '-B', '-c', textwrap.dedent(source)],
            cwd=ROOT, env=env, capture_output=True, text=True,
            encoding='utf-8', timeout=30,
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        return result.stdout.strip()

    def test_each_run_uses_a_distinct_mysql_test_database(self):
        source = '''
            import json
            from django.conf import settings
            db = settings.DATABASES['default']
            print(json.dumps([db['ENGINE'], db['NAME'], db['TEST']['NAME']]))
        '''
        first = json.loads(self.run_python(source))
        second = json.loads(self.run_python(source))
        self.assertEqual(first[0], 'django.db.backends.mysql')
        self.assertEqual(first[1], 'bootstrap_source_must_not_be_modified')
        self.assertTrue(first[2].startswith('test_agrisense_'))
        self.assertNotEqual(first[2], first[1])
        self.assertNotEqual(first[2], second[2])

    def test_ai_falls_back_even_when_real_keys_are_configured(self):
        self.run_python('''
            import django
            django.setup()
            from unittest.mock import patch
            from apps.chatbot.services import call_ai
            with patch('apps.chatbot.fallback.find_matching_products', return_value=[]):
                with patch('requests.sessions.Session.request') as network:
                    reply, fallback, _, _ = call_ai('hello', product_context='Test catalog')
                    assert reply and fallback
                    network.assert_not_called()
        ''')

    def test_uploaded_test_files_do_not_touch_media_directory(self):
        self.run_python('''
            import django
            django.setup()
            from pathlib import Path
            from uuid import uuid4
            from django.conf import settings
            from django.core.files.base import ContentFile
            from django.core.files.storage import default_storage
            name = 'phase1-tests/' + uuid4().hex + '.txt'
            saved = default_storage.save(name, ContentFile(b'isolated test upload'))
            try:
                with default_storage.open(saved) as uploaded:
                    assert uploaded.read() == b'isolated test upload'
                assert not (Path(settings.MEDIA_ROOT) / saved).exists()
            finally:
                default_storage.delete(saved)
        ''')
