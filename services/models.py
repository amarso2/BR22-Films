from django.db import models
from utils.image_optimizer import WebPImageModelMixin
from utils.storage import media_storage

# Create your models here.
class Services(WebPImageModelMixin, models.Model):
    service_name = models.CharField(max_length=100)
    description = models.TextField(max_length=250, blank=True, null=True)
    price1 = models.DecimalField(max_digits=10, decimal_places=2)
    price2 = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    image = models.ImageField(upload_to='photo/services/',storage=media_storage, blank=True, null=True)
    stock = models.BooleanField(default=True)
    is_available = models.BooleanField(default=True)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'services'
        verbose_name_plural = 'services'
    def __str__(self):
            return self.service_name

class Services_details(WebPImageModelMixin, models.Model):
    title =models.CharField()
    image1 = models.ImageField(upload_to='photos/services_details/',storage=media_storage)
    image2 = models.ImageField(upload_to='photos/services_details/',storage=media_storage, blank=True, null=True)
    image3 = models.ImageField(upload_to='photos/services_details/', storage=media_storage, blank=True, null=True)
    about =models.TextField(max_length=500)
    cover =models.TextField(max_length=500)
    photographer = models.TextField(max_length=500)
    videographer = models.TextField(max_length=500)
    drone = models.TextField(max_length=500)
    Deliverables = models.TextField(max_length=500)
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    
    