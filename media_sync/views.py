
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
        try:
            for obj in model.objects.all().iterator():
                for field in model._meta.get_fields():
                    if not isinstance(field, (FileField, ImageField)):
                        continue

                    try:
                        f = getattr(obj, field.name, None)

                        if not f or not getattr(f, "name", ""):
                            continue

                        name = f.name

                        if name in seen:
                            continue

                        if not f.storage.exists(name):
                            continue

                        seen.add(name)
                        files.append({
                            "path": name,
                            "url": f.storage.url(name),
                        })

                    except Exception:
                        continue

        except Exception:
            continue

    return JsonResponse(files, safe=False)
