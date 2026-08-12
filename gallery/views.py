from django.shortcuts import render
from gallery.models import Gallery

# Create your views here.

def gallery(request):
    galleries = Gallery.objects.all().order_by('-created_at')
    context = {
        'galleries': galleries, 
    }
    return render(request, 'gallery/gallery.html', context)
