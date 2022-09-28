from django.db import models


class Wine(models.Model):
    name = models.CharField(max_length=200)
    year = models.IntegerField()
    color = models.CharField(max_length=20)
    variety = models.CharField(max_length=200)
    country = models.CharField(max_length=100)
    price_exvat = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    vat = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    price_incvat = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    stock_level = models.PositiveIntegerField()
    description = models.TextField(default="This wine has no description.")
    image_filename = models.CharField(max_length=100, default="wine_placeholder.png")

    def save(self):
        self.vat = float(self.price_exvat) * 0.2
        self.price_incvat = float(self.price_exvat) + float(self.vat)
        return super().save()

    def __str__(self):
        return f"{self.name} {self.year}"
