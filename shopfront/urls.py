from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('product/<str:pk>/', views.product_details, name='product-details'),
]
