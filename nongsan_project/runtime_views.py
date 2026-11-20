"""Explicit public image routes; payment proofs always use the authenticated route."""
from pathlib import PurePosixPath

from django.core.files.storage import default_storage
from django.db import DatabaseError, connection
from django.http import FileResponse, Http404, JsonResponse
from django.views.decorators.http import require_GET


@require_GET
def health(request):
    try:
        with connection.cursor() as cursor:
            cursor.execute('SELECT 1')
    except DatabaseError:
        return JsonResponse({'status': 'unavailable'}, status=503)
    response = JsonResponse({'status': 'ok'})
    response['Cache-Control'] = 'no-store'
    return response


@require_GET
def public_image(request, directory, filename):
    path = PurePosixPath(filename)
    if (directory not in ('products', 'qr_codes') or path.is_absolute() or '..' in path.parts
            or '\\' in filename or path.suffix.lower() not in ('.jpg', '.jpeg', '.png', '.webp')):
        raise Http404
    try:
        response = FileResponse(default_storage.open(f'{directory}/{filename}', 'rb'))
    except (FileNotFoundError, OSError) as error:
        raise Http404 from error
    response['X-Content-Type-Options'] = 'nosniff'
    response['Cache-Control'] = 'public, max-age=3600'
    return response
