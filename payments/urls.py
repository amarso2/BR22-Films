from django.urls import path
from . import views

urlpatterns = [
    path("<str:booking_type>/<int:item_id>/", views.booking_page, name="booking_page"),

    path("method/<str:booking_id>/", views.payment_method, name="payment_method"),

    path("offline/<str:booking_id>/", views.offline_payment, name="offline_payment"),

    path("offline-success/<str:booking_id>/", views.offline_success, name="offline_success"),
    path(
    "success/<str:booking_id>/",
    views.payment_success,
    name="payment_success"),
]