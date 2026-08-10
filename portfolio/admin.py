from django.contrib import admin
from .models import Portfolio

# Register your models here.
class PortfolioAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'city', 'heading', 'date', 'image1', 'image2', 'image3', 'created_at')
    list_filter = ('city', 'date')
    search_fields = ('title', 'description', 'city', 'heading')
    ordering = ('-created_at',)
    
admin.site.register(Portfolio)

