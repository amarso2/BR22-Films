from django.shortcuts import render, get_object_or_404

from services.models import Services
from package.models import Package
from portfolio.models import Portfolio


# Create your views here.
def services(request):
    services = Services.objects.all().filter(is_available=True)
    context = {
        'services': services,
    }
    return render(request, 'services/services.html', context)


def service_detail(request, pk):
    service = get_object_or_404(Services, pk=pk, is_available=True)
    # pick a featured portfolio (most recent) to show city/date info
    portfolio = Portfolio.objects.all().order_by('-created_at').first()
    packages = Package.objects.all()

    context = {
        'service': service,
        'portfolio': portfolio,
        'packages': packages,
    }
    return render(request, 'services/services_detail.html', context)
