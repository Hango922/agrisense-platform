# File: apps/products/tests/test_visual_inspector.py
"""
Kiểm thử tính năng thẩm định độ tươi & chất lượng nông sản qua ảnh bằng Gemini Multimodal Vision.
"""
import json
from unittest.mock import MagicMock, patch

from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import Client, TestCase, override_settings
from django.urls import reverse

from apps.products.models import Category, Product, Supplier
from apps.products.visual_inspector import (
    get_rule_based_fallback,
    inspect_produce_image,
    match_catalog_products,
)


class VisualInspectorTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.category = Category.objects.create(name='Rau củ', slug='rau-cu')
        cls.supplier = Supplier.objects.create(name='HTX Nông Nghiệp Xanh', address='Đà Lạt')
        cls.product = Product.objects.create(
            name='Cà chua bi tươi',
            slug='ca-chua-bi-tuoi',
            category=cls.category,
            supplier=cls.supplier,
            price=35000,
            stock=50,
            origin='Đà Lạt, Lâm Đồng',
            is_active=True
        )

    def test_get_inspect_page(self):
        """Kiểm tra trang giám định GET load thành công và hiển thị ảnh mẫu."""
        client = Client()
        url = reverse('products:inspect')
        response = client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Thẩm định độ tươi')
        self.assertContains(response, 'Cà chua bi')

    def test_match_catalog_products(self):
        """Kiểm tra chức năng liên kết danh mục tìm thấy sản phẩm trong kho."""
        matched = match_catalog_products(['cà chua', 'ca chua'], 'Cà chua bi', limit=4)
        self.assertGreaterEqual(len(matched), 1)
        self.assertEqual(matched[0]['name'], 'Cà chua bi tươi')
        self.assertEqual(matched[0]['price'], 35000)

    def test_rule_based_fallback(self):
        """Kiểm tra fallback quy tắc hoạt động ổn định khi offline."""
        result = get_rule_based_fallback('ca_chua_bi.jpg')
        self.assertTrue(result.get('is_fallback'))
        self.assertEqual(result.get('category'), 'Củ quả')
        self.assertIn('cà chua', result.get('produce_name').lower())
        self.assertGreaterEqual(result.get('freshness_score'), 80)

    def test_inspect_rejects_empty_data(self):
        """Từ chối dữ liệu ảnh rỗng."""
        with self.assertRaises(ValueError):
            inspect_produce_image(b'')

    def test_inspect_rejects_invalid_mime(self):
        """Từ chối định dạng mime không hỗ trợ."""
        with self.assertRaises(ValueError):
            inspect_produce_image(b'fake content', mime_type='application/pdf')

    def test_inspect_rejects_oversized_image(self):
        """Từ chối ảnh vượt quá giới hạn 10MB."""
        oversized = b'x' * (11 * 1024 * 1024)
        with self.assertRaises(ValueError):
            inspect_produce_image(oversized, mime_type='image/jpeg')

    @override_settings(GEMINI_API_KEY='')
    def test_inspect_falls_back_when_missing_key(self):
        """Khi GEMINI_API_KEY rỗng, tự động chuyển fallback quy tắc."""
        fake_jpeg = b'\xff\xd8\xff\xe0\x00\x10JFIF' + b'\x00' * 100
        result = inspect_produce_image(fake_jpeg, mime_type='image/jpeg', filename='ca_chua.jpg')
        self.assertTrue(result['is_fallback'])
        self.assertIn('Cà chua', result['produce_name'])

    @patch('google.genai.Client')
    def test_inspect_produce_image_gemini_success(self, mock_client_cls):
        """Kiểm tra gọi Gemini Vision thành công và xử lý JSON trả về."""
        mock_response = MagicMock()
        mock_response.text = json.dumps({
            "produce_name": "Cà chua bi",
            "category": "Củ quả",
            "freshness_score": 94,
            "quality_grade": "Loại 1 (Xuất sắc)",
            "visual_assessment": "Quả căng mọng, cuống xanh tươi.",
            "defect_analysis": "Không có khuyết tật.",
            "shelf_life_days": 6,
            "storage_tips": "Bảo quản nhiệt độ 20°C.",
            "recommended_dishes": ["Salad sốt mè", "Canh chua"],
            "search_keywords": ["cà chua", "ca chua"]
        })

        mock_client = MagicMock()
        mock_client.models.generate_content.return_value = mock_response
        mock_client_cls.return_value = mock_client

        with override_settings(GEMINI_API_KEY='valid-key-for-test'):
            fake_jpeg = b'\xff\xd8\xff\xe0\x00\x10JFIF' + b'\x00' * 100
            result = inspect_produce_image(fake_jpeg, mime_type='image/jpeg', filename='test.jpg')

            self.assertFalse(result['is_fallback'])
            self.assertEqual(result['produce_name'], 'Cà chua bi')
            self.assertEqual(result['freshness_score'], 94)
            self.assertEqual(result['shelf_life_days'], 6)
            self.assertGreaterEqual(len(result['matching_products']), 1)

    @patch('apps.products.views.inspect_produce_image')
    def test_post_upload_inspect_view(self, mock_inspect):
        """Kiểm tra view POST tải ảnh lên thành công."""
        mock_inspect.return_value = {
            "produce_name": "Cải thìa",
            "category": "Rau lá",
            "freshness_score": 90,
            "quality_grade": "Loại 1 (Xuất sắc)",
            "visual_assessment": "Lá tươi xanh, bẹ mọng nước.",
            "defect_analysis": "Không có sâu bệnh.",
            "shelf_life_days": 4,
            "storage_tips": "Bảo quản ngăn mát.",
            "recommended_dishes": ["Cải xào tỏi"],
            "matching_products": [],
            "is_fallback": False,
        }

        client = Client()
        fake_file = SimpleUploadedFile(
            'cai_thia.jpg',
            b'\xff\xd8\xff\xe0\x00\x10JFIF' + b'\x00' * 50,
            content_type='image/jpeg'
        )
        url = reverse('products:inspect')
        response = client.post(url, {'image': fake_file})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Cải thìa')
        self.assertContains(response, '90%')
