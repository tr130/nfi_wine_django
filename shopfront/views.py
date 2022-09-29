from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from .models import Wine

def index(request):
    countries = [wine.country for wine in Wine.objects.distinct('country')]
    colors = [wine.color for wine in Wine.objects.distinct('color')]
    if request.method == 'POST':
        request.session['last_search'] = request.POST
        print(request.session['last_search']) 
        return search(request)
    context = {
        'countries': countries,
        'colors': colors,
        }
    return render(request, 'shopfront/index.html', context)

def product_details(request, pk):
    context = {
        'wine': get_object_or_404(Wine, id=pk),
    }
    return render(request, 'shopfront/product.html', context)

def search(request):
    countries = [wine.country for wine in Wine.objects.distinct('country')]
    colors = [wine.color for wine in Wine.objects.distinct('color')]
    search = request.session['last_search']
    wines = Wine.objects.filter(price_incvat__range=(search['price'].split()[0], search['price'].split()[1]))
    if search['country'] in countries:
        wines = wines.filter(country=search['country'])
    if search['color'] in colors:
        wines = wines.filter(color=search['color'])
    print(wines) 
    context = {
        'wines': wines,
        'sort': search['sort'],
    }
    return render(request, 'shopfront/winelist.html', context)
