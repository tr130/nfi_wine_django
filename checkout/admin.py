from django.contrib import admin
from .models import Order, OrderPart


admin.site.register(Order)
admin.site.register(OrderPart)

