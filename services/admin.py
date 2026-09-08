from django.contrib import admin
from .models import Services, Services_details

# Register your models here.
class ServicesAdmin(admin.ModelAdmin):
    list_display = ('service_name', 'description', 'price1', 'price2', 'image', 'stock', 'is_available', 'created_date', 'modified_date')
    list_filter = ('is_available', 'stock')
    search_fields = ('service_name', 'description')
    ordering = ('service_name',)

admin.site.register(Services, ServicesAdmin)

class Services_detailsAdmin(admin.ModelAdmin):
    list_display = ('title', 'image1', 'image2', 'image2', 'about', 'cover', 'photographer', 'videographer', 'drone', 'Deliverables', 'created_date')
    search_fields = ('title','created_date')
    ordering = ('title',)
admin.site.register(Services_details, Services_detailsAdmin)
