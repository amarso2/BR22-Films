from django.shortcuts import render
from package.models import Package
# Create your views here.

def package(request):
    packages = Package.objects.all().order_by('-created_at')
    context = {
        'packages': packages,
    }
    return render(request, 'package/package.html', context)
