from django.contrib import admin
from .models import Package
from .models import Package_details

# Register your models here.
class PackageAdmin(admin.ModelAdmin):
    list_display = ('title', 'price1', 'price2', 't1', 't2', 't3', 't4', 't5', 't6', 't7', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('title',)
    ordering = ('-created_at',)

admin.site.register(Package, PackageAdmin)


class Package_detailsAdmin(admin.ModelAdmin):
    list_display = ('title1', 'image1', 'image2', 'image2', 'about', 'cover', 'photographer', 'videographer', 'drone', 'Deliverables', 'created_date')
    search_fields = ('title1','created_date')
    ordering = ('title1',)
admin.site.register(Package_details, Package_detailsAdmin)
