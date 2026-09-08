from django.contrib import admin
from .models import Booking


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):

    list_display = (
        "booking_id",
        "full_name",
        "selected_item",
        "event_date",
        "payment_method",
        "payment_status",
        "created_at",
    )

    list_filter = (
        "payment_status",
        "payment_method",
        "booking_type",
    )

    search_fields = (
        "booking_id",
        "full_name",
        "phone",
        "email",
    )