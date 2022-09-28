from django.http import HttpResponse
from django.shortcuts import render
from .models import Wine

# Create your views here.
def index(request):
    context = {
        'countries': [wine.country for wine in Wine.objects.distinct('country')],
        'colors': [wine.color for wine in Wine.objects.distinct('color')],
    }
    return render(request, 'shopfront/index.html', context)
