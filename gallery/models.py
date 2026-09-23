from django.db import models
from utils.image_optimizer import WebPImageModelMixin
from utils.storage import media_storage

# Create your models here.
class Gallery(WebPImageModelMixin, models.Model):
    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to='photos/gallery', storage=media_storage) 
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'gallery'
        verbose_name_plural = 'galleries'

    def __str__(self):
        return self.title
