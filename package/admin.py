from django.contrib import admin
from .models import Package

# Register your models here.
class PackageAdmin(admin.ModelAdmin):
    list_display = ('title', 'price1', 'price2', 't1', 't2', 't3', 't4', 't5', 't6', 't7', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('title',)
    ordering = ('-created_at',)

admin.site.register(Package, PackageAdmin)
