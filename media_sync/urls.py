
from django.urls import path
from .views import media_changes, media_download

urlpatterns = [
    path("changes/", media_changes, name="media_changes"),
    path("download/", media_download, name="media_download"),
]
