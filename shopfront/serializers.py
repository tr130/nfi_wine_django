from rest_framework import serializers

from .models import Wine

class WineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wine
        fields = (
            "id",
            "name",
            "year",
            "color",
            "variety",
            "country",
            "price_exvat",
            "vat",
            "price_incvat",
            "stock_level",
            "description",
            "get_image",
            "get_thumbnail",
        )
