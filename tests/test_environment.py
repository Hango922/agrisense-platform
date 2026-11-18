"""Bootstrap checks that also run before Django can initialize."""

import os
from pathlib import Path
import subprocess
import sys
import unittest

from dotenv import dotenv_values


ROOT = Path(__file__).resolve().parent.parent


class EnvironmentTests(unittest.TestCase):
    def test_application_urls_boot_with_example_environment(self):
        env = os.environ.copy()
        env.update({key: value or '' for key, value in dotenv_values(ROOT / '.env.example').items()})
        env['SECRET_KEY'] = 'bootstrap-test-only-key-not-for-deployment'
        result = subprocess.run(
            [
                sys.executable, '-B', 'manage.py', 'check', '--tag=urls',
                '--settings=nongsan_project.settings',
            ],
            cwd=ROOT,
            env=env,
            capture_output=True,
            text=True,
            encoding='utf-8',
            timeout=30,
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
