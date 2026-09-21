from django.urls import path
from .views import media_changes

urlpatterns = [
    path("changes/", media_changes, name="media_changes"),
]