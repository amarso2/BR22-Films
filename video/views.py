from django.shortcuts import render
from video.models import Video

# Create your views here.

def video(request):
    videos = Video.objects.all().order_by('-created_at')
    context = {
        'videos': videos,
    }
    return render(request, 'gallery/gallery.html', context)
