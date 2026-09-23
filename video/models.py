from django.db import models
from utils.storage import media_storage

# Create your models here.

class Video(models.Model):
    title = models.CharField(max_length=255)
    video_file = models.FileField(upload_to='videos/', storage=media_storage)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'video'
        verbose_name_plural = 'videos'

    def __str__(self):
        return self.title
