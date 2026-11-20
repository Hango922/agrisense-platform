from django.conf import settings


def demo_context(request):
    return {'demo_mode': settings.DEMO_MODE,
            'bank_payment_enabled': not settings.OPERATIONAL_MODE or all((
                settings.VIETQR_BANK_ID, settings.VIETQR_ACCOUNT_NO, settings.VIETQR_ACCOUNT_NAME))}
