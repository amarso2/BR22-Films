from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from .models import Album


@login_required
def album_list(request):

    if request.user.is_superuser:
        albums = Album.objects.all().order_by("-created_at")
    else:
        albums = request.user.shared_albums.all().order_by("-created_at")

    return render(request, "album/album_list.html", {
        "albums": albums
    })


@login_required
def album_detail(request, id):

    album = get_object_or_404(Album, id=id)

    if not request.user.is_superuser:
        if request.user not in album.allowed_users.all():
            return HttpResponseForbidden("Access Denied")

        if album.is_expired() or not album.is_active:
            return render(request, "album/expired.html", {
                "album": album
            })

    return render(request, "album/album_detail.html", {
        "album": album,
        "pages": album.pages.all()
    })