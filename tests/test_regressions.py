import json
from datetime import date

from django.test import Client, TestCase

from apps.accounts.models import User
from apps.cart_orders.models import Cart, CartItem, Order
from apps.cart_orders.services import cancel_order, create_direct_order
from apps.products.models import Category, Product, Supplier
from apps.traceability.models import ProductBatch


class WorkflowRegressionTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='owner', password='Password123!')
        self.other = User.objects.create_user(username='other', password='Password123!')
        self.staff = User.objects.create_user(username='staff', is_staff=True)
        category = Category.objects.create(name='Test', slug='test')
        supplier = Supplier.objects.create(name='Test', address='Test')
        self.product = Product.objects.create(name='Test', slug='test', category=category,
                                              supplier=supplier, price=10000, stock=5)
        self.address = {'full_name': 'Private Name', 'phone': '0901234567', 'address': 'Private Address'}
        self.client.force_login(self.user)

    def order(self):
        return create_direct_order(self.user, [{'product': self.product, 'quantity': 2}], self.address)

    def test_stale_stock_cannot_oversell(self):
        stale = Product.objects.get(pk=self.product.pk)
        self.order()
        with self.assertRaises(ValueError):
            create_direct_order(self.user, [{'product': stale, 'quantity': 4}], self.address)
        self.product.refresh_from_db()
        self.assertEqual(self.product.stock, 3)

    def test_stale_cancel_does_not_restore_twice(self):
        order = self.order()
        stale = Order.objects.get(pk=order.pk)
        cancel_order(order)
        with self.assertRaises(ValueError):
            cancel_order(stale)
        self.product.refresh_from_db()
        self.assertEqual(self.product.stock, 5)

    def test_chat_order_is_private(self):
        order = self.order()
        for user in (None, self.other):
            client = Client()
            if user:
                client.force_login(user)
            response = client.post('/chatbot/send/', json.dumps({'message': 'don hang ' + order.order_code}), content_type='application/json')
            self.assertNotIn('Private Address', response.json()['reply'])

    def test_chat_requires_csrf(self):
        client = Client(enforce_csrf_checks=True)
        client.force_login(self.user)
        self.assertEqual(client.post('/chatbot/clear/').status_code, 403)

    def test_invalid_quantity_and_checkout_are_rejected(self):
        for quantity in ('abc', '0', '-1'):
            self.assertEqual(self.client.post(f'/cart/add/{self.product.pk}/', {'quantity': quantity}).status_code, 400)
        self.assertEqual(self.client.post('/cart/checkout/', {}).status_code, 400)
        self.assertFalse(Order.objects.exists())

    def test_invalid_product_input_is_rejected(self):
        self.assertEqual(self.client.get('/products/?min_price=abc').status_code, 400)
        self.assertEqual(self.client.post('/products/test/review/', {'rating': 99}).status_code, 400)

    def test_cancelled_order_cannot_reopen(self):
        order = self.order()
        cancel_order(order)
        self.client.force_login(self.staff)
        self.client.post(f'/dashboard/orders/{order.pk}/update-status/', {'status': 'confirmed'})
        order.refresh_from_db()
        self.assertEqual(order.status, 'cancelled')

    def test_unknown_status_is_rejected(self):
        order = self.order()
        self.client.force_login(self.staff)
        self.client.post(f'/dashboard/orders/{order.pk}/update-status/', {'status': 'garbage'})
        order.refresh_from_db()
        self.assertEqual(order.status, 'pending')

    def test_renamed_batch_regenerates_qr(self):
        batch = ProductBatch.objects.create(product=self.product, batch_code='OLD', planting_location='Test', harvest_date=date.today(), packaging_date=date.today())
        old_name = batch.qr_code.name
        batch.batch_code = 'NEW'
        batch.save()
        self.assertNotEqual(batch.qr_code.name, old_name)

    def test_excel_untrusted_text_is_not_a_formula(self):
        import io
        import openpyxl
        order = self.order()
        order.full_name = '=1+1'
        order.save()
        self.client.force_login(self.staff)
        response = self.client.get('/dashboard/orders/export-excel/')
        sheet = openpyxl.load_workbook(io.BytesIO(response.content)).active
        self.assertEqual(sheet['D2'].data_type, 's')

    def test_bill_rejects_non_image(self):
        from django.core.files.uploadedfile import SimpleUploadedFile
        order = self.order()
        order.payment_method = 'vietqr'
        order.save()
        self.client.post(f'/orders/{order.order_code}/upload-proof/', {
            'payment_proof': SimpleUploadedFile('bill.txt', b'not an image')})
        order.refresh_from_db()
        self.assertFalse(order.payment_proof)

    def test_bank_proof_is_private(self):
        from django.core.files.base import ContentFile
        order = self.order()
        order.payment_proof.save('private.png', ContentFile(b'private'), save=True)
        self.assertEqual(Client().get(order.payment_proof.url).status_code, 302)
        client = Client()
        client.force_login(self.other)
        self.assertEqual(client.get(order.payment_proof.url).status_code, 404)
        response = self.client.get(order.payment_proof.url)
        self.assertEqual(response.status_code, 200)
        response.close()

    def test_ai_timeout_does_not_try_six_models(self):
        from requests.exceptions import Timeout
        from unittest.mock import patch
        from apps.chatbot.services import call_ai
        with self.settings(AI_PROVIDER='gemini', GEMINI_API_KEY='test-key'):
            with patch('apps.chatbot.services.requests.post', side_effect=Timeout) as request:
                self.assertTrue(call_ai('hello', product_context='test')[1])
                self.assertEqual(request.call_count, 1)

    def test_duplicate_chat_request_creates_one_exchange(self):
        from apps.chatbot.models import ChatMessage
        data = json.dumps({'message': 'xin chao', 'request_id': 'request-123'})
        first = self.client.post('/chatbot/send/', data, content_type='application/json')
        second = self.client.post('/chatbot/send/', data, content_type='application/json')
        self.assertEqual(first.json(), second.json())
        self.assertEqual(ChatMessage.objects.count(), 2)
