from io import StringIO
from unittest.mock import Mock, patch

from django.core.management import call_command
from django.core.management.base import CommandError
from django.db import DatabaseError
from django.http import Http404, HttpResponse
from django.test import RequestFactory, TestCase, override_settings
from django.utils import timezone

from apps.accounts.models import RequestQuota, User
from apps.accounts.rate_limit import RequestLimitMiddleware, consume_quota
from apps.cart_orders.forms import CheckoutForm
from apps.cart_orders.vietqr import get_vietqr_url
from nongsan_project.runtime_views import health, public_image


class OperationTests(TestCase):
    def test_preflight_blocks_known_demo_staff_password(self):
        User.objects.create_user('weak-staff', password='Demo@123', is_staff=True)
        with self.assertRaises(CommandError):
            call_command('check_operations', stdout=StringIO())

    def test_quota_limit_and_window(self):
        with patch('apps.accounts.rate_limit.time.time', return_value=120):
            self.assertTrue(consume_quota('test', 'ip', 1))
            self.assertFalse(consume_quota('test', 'ip', 1))
        with patch('apps.accounts.rate_limit.time.time', return_value=180):
            self.assertTrue(consume_quota('test', 'ip', 1))

    @override_settings(RATE_LIMIT_ENABLED=True)
    def test_login_throttle(self):
        middleware = RequestLimitMiddleware(lambda request: HttpResponse())
        request = RequestFactory().post('/accounts/login/', {'username': 'test'})
        for _ in range(10):
            self.assertEqual(middleware(request).status_code, 200)
        response = middleware(request)
        self.assertEqual(response.status_code, 429)
        self.assertEqual(response['Retry-After'], '60')

    def test_cleanup_only_expired(self):
        RequestQuota.objects.create(key='expired', expires_at=timezone.now())
        consume_quota('test', 'live', 1)
        call_command('cleanup_quotas', stdout=StringIO())
        self.assertEqual(RequestQuota.objects.count(), 1)

    def test_health_and_database_failure(self):
        request = RequestFactory().get('/health/')
        self.assertEqual(health(request).status_code, 200)
        with patch('nongsan_project.runtime_views.connection.cursor', side_effect=DatabaseError):
            self.assertEqual(health(request).status_code, 503)

    def test_public_media_rejects_private_and_traversal(self):
        request = RequestFactory().get('/')
        for directory, filename in [('payment_proofs', 'a.png'), ('products', '../a.png'),
                                    ('products', 'a.html'), ('products', 'x\\a.png')]:
            with self.assertRaises(Http404):
                public_image(request, directory, filename)

    def test_logout_requires_post(self):
        self.assertEqual(self.client.get('/accounts/logout/').status_code, 405)

    @override_settings(OPERATIONAL_MODE=True)
    def test_seed_blocked(self):
        with self.assertRaises(CommandError):
            call_command('seed_data', stdout=StringIO())

    @override_settings(VIETQR_BANK_ID='', VIETQR_ACCOUNT_NO='', VIETQR_ACCOUNT_NAME='')
    def test_no_unconfigured_payment_qr(self):
        self.assertEqual(get_vietqr_url(Mock(is_demo=False)), '')

    @override_settings(OPERATIONAL_MODE=True, VIETQR_BANK_ID='', VIETQR_ACCOUNT_NO='', VIETQR_ACCOUNT_NAME='')
    def test_unconfigured_bank_payment_rejected(self):
        form = CheckoutForm({'full_name': 'Test', 'phone': '0901234567',
                             'address': 'Test address', 'payment_method': 'vietqr'})
        self.assertFalse(form.is_valid())
        self.assertIn('payment_method', form.errors)

    @override_settings(AI_PROVIDER='gemini', GEMINI_API_KEY='test-key', GEMINI_MODEL='test-model')
    @patch('apps.products.management.commands.check_integrations.requests.post')
    def test_gemini_probe_hides_key_and_checks_response(self, post):
        post.return_value.status_code = 200
        post.return_value.json.return_value = {'candidates': [{'content': {'parts': [{'text': 'OK'}]}}]}
        output = StringIO()
        call_command('check_integrations', stdout=output)
        self.assertIn('PASS', output.getvalue())
        self.assertNotIn('test-key', output.getvalue())
        self.assertNotIn('test-key', post.call_args.args[0])
        self.assertEqual(post.call_args.kwargs['headers']['x-goog-api-key'], 'test-key')
        post.return_value.status_code = 403
        with self.assertRaises(CommandError):
            call_command('check_integrations', stdout=output)
