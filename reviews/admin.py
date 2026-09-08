from django.contrib import admin
from .models import Review

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ("user", "event", "rating", "is_approved", "created_at")
    list_filter = ("is_approved", "event", "rating")
    list_editable = ("is_approved",)