from django.shortcuts import render
from services.models import Services

def home(request):
    services = Services.objects.all().filter(is_available=True)
    context = {
        'services': services,
    }
    return render(request, 'home.html', context)