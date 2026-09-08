from django.shortcuts import render, get_object_or_404
from package.models import Package
from package.models import Package_details
# Create your views here.

def split_detail_items(value):
    if not value:
        return []
    items = []
    for line in str(value).replace('\r\n', '\n').split('\n'):
        clean_line = line.strip()
        if clean_line and clean_line.lower() not in {'what we cover', 'photography', 'videography', 'drone', 'deliverables'}:
            items.append(clean_line)
    return items

def package(request):
    packages = Package.objects.all().order_by('-created_at')
    context = {
        'packages': packages,
    }
    return render(request, 'package/package.html', context)


def package_details(request, pk):
    package = get_object_or_404(Package, pk=pk)
    # match the package detail content to the package title when available
    package_detail = Package_details.objects.filter(title1__iexact=package.title).order_by('-created_date').first()
    if package_detail is None:
        package_detail = Package_details.objects.filter(pk=pk).first()

    cover_items = split_detail_items(package_detail.cover) if package_detail else []
    photographer_items = split_detail_items(package_detail.photographer) if package_detail else []
    videographer_items = split_detail_items(package_detail.videographer) if package_detail else []
    drone_items = split_detail_items(package_detail.drone) if package_detail else []
    deliverables_items = split_detail_items(package_detail.Deliverables) if package_detail else []

    context = {
        'package': package,
        'package_detail': package_detail,
        'cover_items': cover_items,
        'photographer_items': photographer_items,
        'videographer_items': videographer_items,
        'drone_items': drone_items,
        'deliverables_items': deliverables_items,
    }
    return render(request, 'package/package_details.html', context)
