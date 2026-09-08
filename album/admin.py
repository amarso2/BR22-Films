from django.contrib import admin
from .models import Album, AlbumPage


class AlbumPageInline(admin.TabularInline):
    model = AlbumPage
    extra = 1


@admin.register(Album)
class AlbumAdmin(admin.ModelAdmin):
    list_display = ( "title", "created_at", "expires_at", "is_active"
    )

    list_filter = ("is_active",)

    filter_horizontal = ("allowed_users",)

    inlines = [AlbumPageInline]