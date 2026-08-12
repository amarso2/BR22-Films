from django.db import models

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
