from django.urls import path
from . import views

urlpatterns = [
    path("", views.album_list, name="album_list"),
    path("<int:id>/", views.album_detail, name="album_detail"),
]