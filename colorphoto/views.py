from django.shortcuts import render
from services.models import Services
from portfolio.models import Portfolio
from package.models import Package
from gallery.models import Gallery
from video.models import Video


def home(request):
    services = Services.objects.all().filter(is_available=True)
    portfolios = Portfolio.objects.all().order_by('-created_at')
    packages = Package.objects.all().order_by('-created_at')
    galleries = Gallery.objects.all().order_by('-created_at')
    videos = Video.objects.all().order_by('-created_at')
    context = {
        'services': services,
        'portfolios': portfolios,
        'packages': packages,
        'galleries': galleries,
        'videos': videos,

    }
    return render(request, 'home.html', context)

def portfolio(request):
    portfolios = Portfolio.objects.all().order_by('-created_at')
    galleries = Gallery.objects.all().order_by('-created_at')
    context = {
        'portfolios': portfolios,
        'galleries': galleries,
    }
    return render(request, 'home.html', context)


def package(request):
    packages = Package.objects.all().order_by('-created_at')
    context = {
        'packages': packages,
    }
    return render(request, 'package/package.html', context)

def gallery(request):
    galleries = Gallery.objects.all().order_by('-created_at')
    context = {
        'galleries': galleries, 
    }
    return render(request, 'gallery/gallery.html', context)

def video(request):
    videos = Video.objects.all().order_by('-created_at')
    context = {
        'videos': videos,
    }
    return render(request, 'gallery/fallery.html', context)