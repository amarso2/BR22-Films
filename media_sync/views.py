from django.http import JsonResponse
from django.conf import settings
from django.views.decorators.http import require_GET

from gallery.models import Gallery
from services.models import Portfolio, ServiceDetail
from package_details.models import PackageDetails

@require_GET
def media_changes(request):
    token = request.headers.get("X-MEDIA-TOKEN")

    if token != settings.MEDIA_SYNC_TOKEN:
        return JsonResponse({"error": "Unauthorized"}, status=401)

    files = []

    def add_file(field):
        if field and getattr(field, "name", ""):
            files.append({
                "path": field.name,
                "url": field.url
            })

    # Gallery
    for obj in Gallery.objects.all():
        add_file(obj.image)

    # Portfolio
    for obj in Portfolio.objects.all():
        add_file(obj.image)

    # Service Detail
    for obj in ServiceDetail.objects.all():
        add_file(obj.image1)
        add_file(obj.image2)
        add_file(obj.image3)

    # Package images (agar field image hai)
    for obj in PackageDetails.objects.all():
        if hasattr(obj, "image"):
            add_file(obj.image)

    return JsonResponse(files, safe=False)