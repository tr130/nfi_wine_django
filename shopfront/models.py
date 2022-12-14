from io import BytesIO
from PIL import Image

from django.core.files import File
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
    image = models.ImageField(upload_to='uploads/', blank=True, null=True)
    thumbnail = models.ImageField(upload_to='thumbs/', blank=True, null=True)

    def save(self):
        self.vat = float(self.price_exvat) * 0.2
        self.price_incvat = float(self.price_exvat) + float(self.vat)
        return super().save()

    def __str__(self):
        return f"{self.name} {self.year}"

    def get_image(self):
        if self.image:
            return 'http://127.0.0.1:8000' + self.image.url
        return ''

    def get_thumbnail(self):
        if self.thumbnail:
            return 'http://127.0.0.1:8000' + self.thumbnail.url
        else:
            if self.image:
                self.thumbnail = self.make_thumbnail(self.image)
                self.save()
                
                return 'http://127.0.0.1:8000' + self.thumbnail.url
            else:
                return ''

    def make_thumbnail(self, image, size=(300, 200)):
        img = Image.open(image)
        img.convert('RGB')
        img.thumbnail(size)

        thumb_io = BytesIO()
        img.save(thumb_io, 'JPEG', quality=85)

        thumbnail = File(thumb_io, name=f"thumb_{image.name[8:]}")

        return thumbnail
