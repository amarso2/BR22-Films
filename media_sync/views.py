from django.shortcuts import render

# Create your views here.
from django.http import JsonResponse
from django.conf import settings
from django.views.decorators.http import require_GET
import os

@require_GET
def media_changes(request):
    token = request.headers.get("X-MEDIA-TOKEN")

    if token != settings.MEDIA_SYNC_TOKEN:
        return JsonResponse({"error": "Unauthorized"}, status=401)

    media_root = settings.MEDIA_ROOT
    files = []

    for root, dirs, filenames in os.walk(media_root):
        for filename in filenames:
            rel_path = os.path.relpath(
                os.path.join(root, filename),
                media_root
            ).replace("\\", "/")

            files.append({
                "path": rel_path,
                "url": request.build_absolute_uri(settings.MEDIA_URL + rel_path)
            })

    return JsonResponse(files, safe=False)