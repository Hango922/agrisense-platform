"""Verify provider responses offline without sending customer data."""

from unittest.mock import Mock, patch

from django.test import SimpleTestCase, override_settings

from apps.chatbot.services import call_ai


@override_settings(AI_PROVIDER='gemini', GEMINI_API_KEY='test-key', CHATBOT_TIMEOUT=3)
class AIResponseTests(SimpleTestCase):
    def test_success_preserves_response_and_usage(self):
        response = Mock(status_code=200)
        response.json.return_value = {
            'candidates': [{'content': {'parts': [{'text': 'Fresh vegetables'}]}}],
            'usageMetadata': {'totalTokenCount': 42},
        }
        with patch('apps.chatbot.services.requests.post', return_value=response) as network:
            reply, fallback, _, tokens = call_ai('hello', product_context='Catalog')
        self.assertEqual(reply, 'Fresh vegetables')
        self.assertFalse(fallback)
        self.assertEqual(tokens, 42)
        network.assert_called_once()
        self.assertEqual(network.call_args.kwargs['timeout'], 3)

    def test_malformed_and_unavailable_provider_fall_back_once(self):
        for status, payload in [(200, {}), (429, {}), (500, {})]:
            with self.subTest(status=status):
                response = Mock(status_code=status)
                response.json.return_value = payload
                with patch('apps.chatbot.services.requests.post', return_value=response) as network:
                    with patch('apps.chatbot.services.get_fallback_response', return_value=('Offline reply', True)):
                        reply, fallback, _, _ = call_ai('hello', product_context='Catalog')
                self.assertEqual(reply, 'Offline reply')
                self.assertTrue(fallback)
                network.assert_called_once()
