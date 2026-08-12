from django.contrib import admin
from .models import Video

# Register your models here.

class VideoAdmin(admin.ModelAdmin):
    list_display = ('title', 'video_file', 'created_at')
    search_fields = ('title',)
    list_filter = ('created_at',)

admin.site.register(Video, VideoAdmin)
