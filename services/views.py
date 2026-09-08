from django.shortcuts import render, get_object_or_404

from services.models import Services
from package.models import Package
from portfolio.models import Portfolio
from services.models import Services_details


def split_detail_items(value):
    if not value:
        return []
    items = []
    for line in str(value).replace('\r\n', '\n').split('\n'):
        clean_line = line.strip()
        if clean_line and clean_line.lower() not in {'what we cover', 'photography', 'videography', 'drone', 'deliverables'}:
            items.append(clean_line)
    return items


# Create your views here.
def services(request):
    services = Services.objects.all().filter(is_available=True)
    context = {
        'services': services,
    }
    return render(request, 'services/services.html', context)


def services_details(request, pk):
    service = get_object_or_404(Services, pk=pk, is_available=True)
    # match the service detail content to the service title when available
    service_detail = Services_details.objects.filter(title__iexact=service.service_name).order_by('-created_date').first()
    if service_detail is None:
        service_detail = Services_details.objects.filter(pk=pk).first()

    portfolio = Portfolio.objects.all().order_by('-created_at').first()
    packages = Package.objects.all()

    cover_items = split_detail_items(service_detail.cover) if service_detail else []
    photographer_items = split_detail_items(service_detail.photographer) if service_detail else []
    videographer_items = split_detail_items(service_detail.videographer) if service_detail else []
    drone_items = split_detail_items(service_detail.drone) if service_detail else []
    deliverables_items = split_detail_items(service_detail.Deliverables) if service_detail else []

    context = {
        'service': service,
        'service_detail': service_detail,
        'portfolio': portfolio,
        'packages': packages,
        'cover_items': cover_items,
        'photographer_items': photographer_items,
        'videographer_items': videographer_items,
        'drone_items' : drone_items,
        'deliverables_items': deliverables_items,
    }
    return render(request, 'services/services_detail.html', context)
