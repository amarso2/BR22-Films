from django.contrib import admin
from .models import Services

# Register your models here.
class ServicesAdmin(admin.ModelAdmin):
    list_display = ('service_name', 'description', 'price1', 'price2', 'image', 'stock', 'is_available', 'created_date', 'modified_date')
    list_filter = ('is_available', 'stock')
    search_fields = ('service_name', 'description')
    ordering = ('service_name',)

admin.site.register(Services, ServicesAdmin)
