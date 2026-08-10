from django.shortcuts import render

from services.models import Services

# Create your views here.
def services(request):
    services = Services.objects.all().filter(is_available=True)
    context = {
        'services': services,
    }
    return render(request, 'services/services.html', context)
