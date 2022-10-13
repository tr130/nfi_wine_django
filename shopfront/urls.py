from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('details/<slug:wine_slug>', views.WineDetails.as_view()),
    path('search', views.search, name='search'),
    path('update_cart', views.update_cart, name='update-cart'),
    path('api/winelist', views.WineList.as_view()),
    path('api/getParams', views.GetParams.as_view())
]
