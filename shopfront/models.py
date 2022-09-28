from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    pass

class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    email = models.TextField()
