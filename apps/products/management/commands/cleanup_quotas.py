"""Remove expired rate-limit counters without touching users or orders."""
from django.core.management.base import BaseCommand
from django.utils import timezone

from apps.accounts.models import RequestQuota


class Command(BaseCommand):
    help = 'Delete expired request quotas (run daily).'

    def handle(self, *args, **options):
        count, _ = RequestQuota.objects.filter(expires_at__lt=timezone.now()).delete()
        self.stdout.write(f'Removed {count} expired counters.')
