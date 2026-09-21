from django.http import JsonResponse
from django.conf import settings
from django.views.decorators.http import require_GET
from django.apps import apps
from django.db.models import FileField, ImageField


@require_GET
def media_changes(request):
    token = request.headers.get("X-MEDIA-TOKEN")

    if token != settings.MEDIA_SYNC_TOKEN:
        return JsonResponse({"error": "Unauthorized"}, status=401)

    files = []
    seen = set()

    # Project ke saare models scan karo
    for model in apps.get_models():
        try:
            for obj in model.objects.all():
                for field in model._meta.get_fields():
                    if isinstance(field, (FileField, ImageField)):
                        f = getattr(obj, field.name, None)
                        if f and getattr(f, "name", "") and f.name not in seen:
                            seen.add(f.name)
                            files.append({
                                "path": f.name,
                                "url": f.url,
                            })
        except Exception:
            # Agar koi model read na ho sake to skip kar do
            continue

    return JsonResponse(files, safe=False)