from django.db import models
from utils.image_optimizer import WebPImageModelMixin

# Create your models here.

class Package(models.Model):
    title = models.CharField(max_length=100)
    price1 = models.DecimalField(max_digits=10, decimal_places=2)
    price2 = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    t1 = models.CharField(max_length=100, blank=True, null=True)
    t2 = models.CharField(max_length=100, blank=True, null=True)
    t3 = models.CharField(max_length=100, blank=True, null=True)
    t4 = models.CharField(max_length=100, blank=True, null=True)
    t5 = models.CharField(max_length=100, blank=True, null=True)
    t6 = models.CharField(max_length=100, blank=True, null=True)
    t7 = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)


    class Meta:
        verbose_name = 'package'
        verbose_name_plural = 'packages'

    def __str__(self):
        return self.title

    

class Package_details(WebPImageModelMixin, models.Model):
    title1 =models.CharField()
    image1 = models.ImageField(upload_to='photos/package_details/')
    image2 = models.ImageField(upload_to='photos/package_details/', blank=True, null=True)
    image3 = models.ImageField(upload_to='photos/package_details/', blank=True, null=True)
    about =models.TextField(max_length=500)
    cover =models.TextField(max_length=500)
    photographer = models.TextField(max_length=500)
    videographer = models.TextField(max_length=500)
    drone = models.TextField(max_length=500)
    Deliverables = models.TextField(max_length=500)
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title1
