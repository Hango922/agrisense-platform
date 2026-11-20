"""Fail startup on known unsafe local operator configuration."""
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError

from apps.accounts.models import User


class Command(BaseCommand):
    help = 'Check local operator credentials without printing passwords.'

    def handle(self, *args, **options):
        weak = []
        for user in User.objects.filter(is_active=True, is_staff=True):
            if any(user.check_password(password) for password in (
                    'admin123', 'Admin@123', 'Demo@123', '123456', 'admin')):
                weak.append(user.username)
        if weak:
            raise CommandError('Change known demo passwords using manage.py changepassword: ' + ', '.join(weak))
        if not settings.SECRET_KEY or len(settings.SECRET_KEY) < 50 or settings.SECRET_KEY.startswith('django-insecure-'):
            raise CommandError('Set a random SECRET_KEY of at least 50 characters in .env.')
        if settings.DATABASES['default']['USER'] == 'root':
            self.stderr.write('WARNING: use a dedicated MySQL account with access only to this database.')
        self.stdout.write(self.style.SUCCESS('Local operation preflight PASS.'))
