from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from .models import Wine
from .serializers import WineSerializer
from urllib.parse import parse_qs

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

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

class AuthTestView(APIView):
    http_method_names = 'get'
    permission_classes = [IsAuthenticated]
    def get(self, request):
        # user = request.user
        print(dir(request.user))
        response_data = {
            'result': 'Restricted access test ok',
            'user': str(request.user),
        }
        return Response(data=response_data)


class GetParams(APIView):
    def get(self, request, format=None):
        countries = [wine.country for wine in Wine.objects.distinct('country')]
        colors = [wine.color for wine in Wine.objects.distinct('color')]
        return Response({
            'countries': countries,
            'colors': colors,
            })

class WineList(APIView):
    def post(self, request, format=None):
        query = request.data.get('query', '')
        if query:
            search = parse_qs(query)
            countries = [wine.country for wine in Wine.objects.distinct('country')]
            colors = [wine.color for wine in Wine.objects.distinct('color')]
            wines = Wine.objects.filter(price_incvat__range=(search['price'][0].split()[0], search['price'][0].split()[1]))
            if search['country'][0] in countries:
                wines = wines.filter(country=search['country'][0])
            if search['color'][0] in colors:
                wines = wines.filter(color=search['color'][0])
        else:
            wines = Wine.objects.all()
        serializer = WineSerializer(wines, many=True)
        return Response(serializer.data)

class CartDetails(APIView):
    def post(self, request, format=None):
        cart = request.data.get('cart', [])
        wines = Wine.objects.filter(id__in=cart)
        serializer = WineSerializer(wines, many=True)
        print(wines)
        print(serializer)
        return Response(serializer.data)

class WineDetails(APIView):
    def get(self, request, wine_slug, format=None):
        wine = get_object_or_404(Wine, id=wine_slug)
        serializer = WineSerializer(wine)
        return Response(serializer.data)
    # def get_object(self, category_slug):
    #     try:
    #         return Category.objects.get(slug=category_slug)
    #     except Category.DoesNotExist:
    #         raise Http404

    # def get(self, request, category_slug, format=None):
    #     category = self.get_object(category_slug)
    #     serializer = CategorySerializer(category)
    #     return Response(serializer.data)

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
    if quantity > wine.stock_level:
        error = 'Insufficient stock.'
    if error is not None:
        messages.warning(request, error)
    else:
        request.session['shopping_cart'].update({item_id: quantity})
        request.session.modified = True
    try:
        return HttpResponseRedirect(request.headers['REFERER'])
    except:
        return redirect('index')

