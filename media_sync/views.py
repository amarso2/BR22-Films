
from django.http import JsonResponse, FileResponse, Http404
from django.conf import settings
from django.views.decorators.http import require_GET
from django.apps import apps
from django.db.models import FileField, ImageField
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes


def check_token(request):
    token = request.headers.get("X-MEDIA-TOKEN")
    return bool(token and token == settings.MEDIA_SYNC_TOKEN)


@require_GET
def media_changes(request):
    if not check_token(request):
        return JsonResponse({"error": "Unauthorized"}, status=401)

    files = []
    seen = set()

    for model in apps.get_models():
        for field in model._meta.fields:
            if not isinstance(field, (FileField, ImageField)):
                continue

            try:
                for obj in model.objects.exclude(
                    **{field.name: ""}
                ).iterator():
                    f = getattr(obj, field.name, None)
                    if not f or not f.name or f.name in seen:
                        continue

                    seen.add(f.name)

                    files.append({
                        "path": f.name,
                        "url": (
                            "https://br22films.com/media-sync/download/"
                            "?path=" + urlsafe_base64_encode(
                                force_bytes(f.name)
                            )
                        ),
                    })
            except Exception:
                continue

    return JsonResponse(files, safe=False)


@require_GET
def media_download(request):
    if not check_token(request):
        return JsonResponse({"error": "Unauthorized"}, status=401)

    from django.utils.http import urlsafe_base64_decode
    from django.core.files.storage import default_storage

    encoded = request.GET.get("path", "")

    try:
        name = urlsafe_base64_decode(encoded).decode("utf-8")
    except Exception:
        raise Http404("Invalid file path")

    # File must belong to a database FileField/ImageField.
    allowed = False
    for model in apps.get_models():
        for field in model._meta.fields:
            if not isinstance(field, (FileField, ImageField)):
                continue
            try:
                if model.objects.filter(**{field.name: name}).exists():
                    allowed = True
                    break
            except Exception:
                continue
        if allowed:
            break

    if not allowed:
        raise Http404("File path not found in database")

    if not default_storage.exists(name):
        raise Http404("File missing from Render storage")

    return FileResponse(default_storage.open(name, "rb"))