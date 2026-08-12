from django.shortcuts import render

from portfolio.models import Portfolio

# Create your views here.

def portfolio(request):
    portfolios = Portfolio.objects.all().order_by('-created_at')
    context = {
        'portfolios': portfolios,
    }
    return render(request, 'portfolio/portfolio.html', context)