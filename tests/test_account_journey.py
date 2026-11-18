"""Customer account entry points used before checkout."""

from django.test import TestCase

from apps.accounts.models import User


class AccountJourneyTests(TestCase):
    def test_registration_profile_logout_and_login(self):
        self.assertEqual(self.client.get('/accounts/register/').status_code, 200)
        response = self.client.post('/accounts/register/', {
            'username': 'new-customer', 'email': 'customer@example.com', 'phone': '0901234567',
            'password1': 'SafeCustomerPass!2026', 'password2': 'SafeCustomerPass!2026',
        })
        self.assertRedirects(response, '/')
        self.assertEqual(User.objects.filter(username='new-customer').count(), 1)
        self.assertEqual(self.client.get('/accounts/profile/').status_code, 200)
        self.assertRedirects(self.client.post('/accounts/logout/'), '/')
        self.assertEqual(self.client.get('/accounts/profile/').status_code, 302)
        self.assertRedirects(self.client.post('/accounts/login/', {
            'username': 'new-customer', 'password': 'SafeCustomerPass!2026',
        }), '/')

    def test_registration_rejects_mismatched_passwords(self):
        response = self.client.post('/accounts/register/', {
            'username': 'invalid', 'email': 'customer@example.com',
            'password1': 'SafeCustomerPass!2026', 'password2': 'DifferentPassword!2026',
        })
        self.assertEqual(response.status_code, 200)
        self.assertFalse(User.objects.filter(username='invalid').exists())
