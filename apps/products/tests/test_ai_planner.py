import json
from unittest.mock import Mock, patch

import requests
from django.test import TestCase, override_settings
from django.urls import reverse

from apps.products.ai_planner import make_ai_plan, request_proposal, validate_proposal
from apps.products.models import Category, Product, Supplier


class AIPlannerTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        category = Category.objects.create(name='Rau củ', slug='rau')
        supplier = Supplier.objects.create(name='Farm', address='Test')
        cls.product = Product.objects.create(name='Cà rốt', slug='carrot', category=category,
                                             supplier=supplier, price=25000, stock=20)

    def proposal(self, **overrides):
        result = {'items': [{'product_id': self.product.pk, 'quantity': 2, 'reason': 'Nấu canh và xào.'}],
                  'meals': ['Ngày 1: canh rau củ.'], 'note': 'Cần mua thêm nguồn đạm; giả định 3 bữa.'}
        result.update(overrides)
        return result

    @patch('apps.products.ai_planner.request_proposal')
    def test_live_catalog_and_wish_sent_and_server_computes_totals(self, request):
        request.return_value = self.proposal(total=1)
        plan = make_ai_plan(500000, 4, 1, wish='Bữa chay cho 4 người')
        self.assertTrue(plan['is_ai'])
        self.assertEqual(plan['grand_total'], 80000)
        payload = request.call_args.args[0]
        self.assertEqual(payload['wish'], 'Bữa chay cho 4 người')
        self.assertEqual(payload['catalog'][0]['stock'], 20)
        self.assertEqual(payload['catalog'][0]['unit'], 'kg')

    def test_rejects_unknown_duplicate_fractional_negative_and_boolean_items(self):
        valid = self.proposal()['items'][0]
        variants = [
            [{**valid, 'product_id': 99999}], [valid, valid],
            [{**valid, 'quantity': 1.5}], [{**valid, 'quantity': -1}],
            [{**valid, 'quantity': True}], [{**valid, 'product_id': True}],
            [{**valid, 'quantity': 21}], [{'product_id': self.product.pk}], [None],
        ]
        for items in variants:
            with self.subTest(items=items), self.assertRaises((ValueError, TypeError)):
                validate_proposal(self.proposal(items=items), [self.product.pk], 500000, 4, 1)

    def test_shipping_included_in_budget_validation(self):
        with self.assertRaises(ValueError):
            validate_proposal(self.proposal(), [self.product.pk], 60000, 4, 1)

    def test_ai_money_claims_are_not_displayed(self):
        plan = validate_proposal(self.proposal(note='Giả định 3 bữa. Tổng tiền là 1.000đ. Cần mua thêm đạm.'),
                                 [self.product.pk], 500000, 4, 1)
        self.assertNotIn('1.000', plan['ai_note'])
        self.assertIn('Cần mua thêm đạm', plan['ai_note'])
        self.assertEqual(plan['grand_total'], 80000)

    def test_price_and_active_status_rechecked(self):
        Product.objects.filter(pk=self.product.pk).update(price=300000)
        with self.assertRaises(ValueError):
            validate_proposal(self.proposal(), [self.product.pk], 500000, 4, 1)
        Product.objects.filter(pk=self.product.pk).update(is_active=False)
        with self.assertRaises(ValueError):
            validate_proposal(self.proposal(), [self.product.pk], 500000, 4, 1)

    def test_stock_rechecked(self):
        Product.objects.filter(pk=self.product.pk).update(stock=1)
        with self.assertRaises(ValueError):
            validate_proposal(self.proposal(), [self.product.pk], 500000, 4, 1)

    def test_invalid_metadata_rejected(self):
        for changes in [{'items': None}, {'note': ''}, {'meals': 'text'}, {'meals': [None]}]:
            with self.subTest(changes=changes), self.assertRaises(ValueError):
                validate_proposal(self.proposal(**changes), [self.product.pk], 500000, 4, 1)

    @patch('apps.products.ai_planner.request_proposal', side_effect=requests.Timeout)
    def test_timeout_fallback_explicitly_not_ai(self, request):
        plan = make_ai_plan(500000, 4, 1)
        self.assertFalse(plan['is_ai'])
        self.assertIn('giỏ cơ bản', plan['ai_note'])
        self.assertLessEqual(plan['grand_total'], 500000)

    @patch('apps.products.ai_planner.request_proposal')
    def test_view_displays_ai_and_escapes_provider_text(self, request):
        request.return_value = self.proposal(note='<script>alert(1)</script>')
        response = self.client.post(reverse('products:planner'), {'wish': 'mua đồ ăn', 'budget': 500000,
                                                                 'people': 4, 'days': 1, 'preference': ''})
        self.assertContains(response, 'Gợi ý từ AI')
        self.assertContains(response, '&lt;script&gt;')
        self.assertNotContains(response, '<script>alert(1)</script>')

    @patch('apps.products.ai_planner.request_proposal', side_effect=ValueError)
    def test_view_displays_fallback_warning(self, request):
        response = self.client.post(reverse('products:planner'), {'budget': 500000, 'people': 4, 'days': 1})
        self.assertContains(response, 'Đang dùng gợi ý cơ bản')
        self.assertNotContains(response, 'Gợi ý từ AI')

    @override_settings(AI_PROVIDER='gemini', GEMINI_API_KEY='test-key')
    @patch('apps.products.ai_planner.requests.post')
    def test_gemini_json_transport_and_key_in_header_only(self, post):
        post.return_value = Mock(json=lambda: {'candidates': [{'content': {'parts': [{'text': json.dumps(self.proposal())}]}}]})
        self.assertEqual(request_proposal({}), self.proposal())
        self.assertNotIn('test-key', post.call_args.args[0])
        self.assertEqual(post.call_args.kwargs['headers']['x-goog-api-key'], 'test-key')
        self.assertEqual(post.call_args.kwargs['timeout'], (5, 30))

    @override_settings(AI_PROVIDER='groq', GROQ_API_KEY='test-key')
    @patch('apps.products.ai_planner.requests.post')
    def test_groq_json_transport(self, post):
        post.return_value = Mock(json=lambda: {'choices': [{'message': {'content': json.dumps(self.proposal())}}]})
        self.assertEqual(request_proposal({}), self.proposal())
        self.assertEqual(post.call_args.kwargs['json']['response_format'], {'type': 'json_object'})

    @override_settings(GEMINI_API_KEY='', AI_PROVIDER='gemini')
    @patch('apps.products.ai_planner.requests.post')
    def test_missing_key_does_not_call_network(self, post):
        with self.assertRaises(ValueError):
            request_proposal({})
        post.assert_not_called()
