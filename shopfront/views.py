from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from .models import Wine

def index(request):
    context = {
        'countries': [wine.country for wine in Wine.objects.distinct('country')],
        'colors': [wine.color for wine in Wine.objects.distinct('color')],
    }
    return render(request, 'shopfront/index.html', context)

def product_details(request, pk):
    context = {
        'wine': get_object_or_404(Wine, id=pk),
    }
    return render(request, 'shopfront/product.html', context)
