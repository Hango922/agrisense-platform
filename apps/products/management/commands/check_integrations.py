"""Probe the configured AI provider without customer data or secret output."""
import requests
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    help = 'Check Gemini with a synthetic prompt; never print credentials or response bodies.'

    def handle(self, *args, **options):
        if settings.AI_PROVIDER != 'gemini' or not settings.GEMINI_API_KEY:
            raise CommandError('Gemini is not configured in the environment.')
        try:
            response = requests.post(
                f'https://generativelanguage.googleapis.com/v1beta/models/{settings.GEMINI_MODEL}:generateContent',
                headers={'x-goog-api-key': settings.GEMINI_API_KEY},
                json={'contents': [{'parts': [{'text': 'Reply with OK.'}]}]},
                timeout=settings.CHATBOT_TIMEOUT,
            )
            if response.status_code != 200:
                raise CommandError(f'Gemini FAIL: HTTP {response.status_code}. Check key, model and quota.')
            data = response.json()
            if not data['candidates'][0]['content']['parts'][0]['text'].strip():
                raise ValueError('Empty reply')
        except (requests.RequestException, ValueError, KeyError, IndexError, TypeError) as error:
            raise CommandError(f'Gemini FAIL: {type(error).__name__}. No response details logged.') from None
        self.stdout.write(self.style.SUCCESS('Gemini PASS: received a non-empty live response.'))
