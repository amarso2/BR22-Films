from django.db import models
from utils.image_optimizer import WebPImageModelMixin
from utils.storage import media_storage

# Create your models here.

class Portfolio(WebPImageModelMixin, models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    city = models.CharField(max_length=100)
    heading = models.CharField(max_length=100)
    date = models.DateField()
    image1 = models.ImageField(upload_to='photos/portfolio', storage=media_storage)
    image2 = models.ImageField(upload_to='photos/portfolio', storage=media_storage, blank=True, null=True)
    image3 = models.ImageField(upload_to='photos/portfolio', storage=media_storage, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'portfolio'
        verbose_name_plural = 'portfolio'

    def __str__(self):
        return self.title
