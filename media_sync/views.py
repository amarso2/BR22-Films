
from django.http import JsonResponse
from django.conf import settings
from django.views.decorators.http import require_GET
from django.apps import apps
from django.db.models import FileField, ImageField


@require_GET
def media_changes(request):
    token = request.headers.get("X-MEDIA-TOKEN")

    if not token or token != settings.MEDIA_SYNC_TOKEN:
        return JsonResponse({"error": "Unauthorized"}, status=401)

    files = []
    seen = set()

    for model in apps.get_models():
        for field in model._meta.fields:
            if not isinstance(field, (FileField, ImageField)):
                continue

            try:
                for obj in model.objects.exclude(
                    **{f"{field.name}": ""}
                ).iterator():
                    f = getattr(obj, field.name, None)

                    if not f or not f.name or f.name in seen:
                        continue

                    seen.add(f.name)
                    files.append({
                        "path": f.name,
                        "url": f.storage.url(f.name),
                    })
            except Exception:
                continue

    return JsonResponse(files, safe=False)
