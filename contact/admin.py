from django.contrib import admin
from .models import Contact


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "phone",
        "email",
        "city",
        "event",
        "event_date",
        "message",
        "created_at",
    )

    list_filter = ("event", "city", "event_date")
    search_fields = ("name", "phone", "email", "city")
    ordering = ("-created_at",)