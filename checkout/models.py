from django.db import models
from accounts.models import Customer
from shopfront.models import Wine


class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT)
    placed = models.DateTimeField(auto_now_add=True)
    sub_total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    vat = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    grand_total = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def save(self):
        for orderpart in self.orderpart_set.all():
            self.sub_total += orderpart.total_price
        self.vat = float(self.sub_total) * 0.2
        self.grand_total = self.sub_total + self.vat
        return super().save()

class OrderPart(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    wine = models.ForeignKey(Wine, on_delete=models.PROTECT)
    quantity = models.IntegerField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def save(self):
        self.total_price = self.item.price * quantity
        return super().save()
