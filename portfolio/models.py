from django.db import models

# Create your models here.

class Portfolio(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    city = models.CharField(max_length=100)
    heading = models.CharField(max_length=100)
    date = models.DateField()
    image1 = models.ImageField(upload_to='photos/portfolio')
    image2 = models.ImageField(upload_to='photos/portfolio', blank=True, null=True)
    image3 = models.ImageField(upload_to='photos/portfolio', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'portfolio'
        verbose_name_plural = 'portfolio'

    def __str__(self):
        return self.title
