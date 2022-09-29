from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('product/<str:pk>/', views.product_details, name='product-details'),
    path('search', views.search, name='search'),
    path('update_cart', views.update_cart, name='update-cart'),
]
