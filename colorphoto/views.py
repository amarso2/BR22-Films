from datetime import date

from django.shortcuts import render

from contact.models import Contact
from services.models import Services
from portfolio.models import Portfolio
from package.models import Package
from gallery.models import Gallery
from video.models import Video
from reviews.models import Review
from reviews.forms import ReviewForm
# from package.models import package_details



def home(request):
    services = Services.objects.all().filter(is_available=True)
    portfolios = Portfolio.objects.all().order_by('-created_at')
    packages = Package.objects.all().order_by('-created_at')
    galleries = Gallery.objects.all().order_by('-created_at')
    videos = Video.objects.all().order_by('-created_at')
    reviews = Review.objects.filter(is_approved=True).order_by("-created_at")
    review_form = ReviewForm()
    context = {
        'services': services,
        'portfolios': portfolios,
        'packages': packages,
        'galleries': galleries,
        'videos': videos,
        'reviews': reviews,
        'review_form': review_form,
        'events': Contact.Event.choices,
        'today': date.today(),
    }
    return render(request, 'home.html', context)

def about(request):
    return render(request, 'contact/about.html')


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
        # 'package_details' : package_details, 
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

def terms(request):
    return render(request, "contact/terms.html")

def scanner(request):
    return render(request, "scanner.html")

def privacy(request):
    return render(request, "contact/privacy.html")