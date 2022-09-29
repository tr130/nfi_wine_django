from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from .models import Wine

def index(request):
    countries = [wine.country for wine in Wine.objects.distinct('country')]
    colors = [wine.color for wine in Wine.objects.distinct('color')]
    if request.method == 'POST':
        request.session['last_search'] = request.POST
        return redirect('search')
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
    context = {
        'wines': wines,
        'sort': search['sort'],
    }
    return render(request, 'shopfront/winelist.html', context)

def update_cart(request):
    error = None
    try:
        item_id = request.POST['item_id']
    except:
        error = 'Something hasn\'t worked.'
    try:
        quantity = int(request.POST['quantity'])
    except:
        error = 'You can only buy whole bottles of wine.'
    if quantity < 0:
        error = 'You can\'t buy a negative quantity of wine.'
    if not quantity:
        error = 'Please specify a quantity to add to the basket.'
    wine = get_object_or_404(Wine, id=item_id)
    if 'shopping_cart' not in request.session:
        request.session['shopping_cart'] = {}
    if item_id in request.session['shopping_cart']:
        quantity += request.session['shopping_cart'][item_id]
    if quantity > wine.stock_level:
        error = 'Insufficient stock.'
    if error is not None:
        messages.warning(request, error)
    else:
        request.session['shopping_cart'].update({item_id: quantity}) 
        request.session.modified = True
    try:
        print(request.headers['REFERER'])
        return HttpResponseRedirect(request.headers['REFERER'])
    except:
        print('something wrong')
        return redirect('index')

