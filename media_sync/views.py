from django.http import JsonResponse
from django.conf import settings
from django.views.decorators.http import require_GET
from django.apps import apps
from django.db.models import FileField, ImageField
import os


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

                        if not f or not getattr(f, "name", ""):
                            continue

                        if f.name in seen:
                            continue

                        full_path = os.path.join(settings.MEDIA_ROOT, f.name)

                        # Sirf existing files bhejo
                        if not os.path.isfile(full_path):
                            print(f"Missing media skipped: {f.name}")
                            continue

                        seen.add(f.name)

                        files.append({
                            "path": f.name,
                            "url": settings.MEDIA_URL + f.name,
                        })

        except Exception:
            # Agar koi model read na ho sake to skip kar do
            continue

    return JsonResponse(files, safe=False)