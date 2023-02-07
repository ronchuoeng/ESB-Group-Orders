from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.


class User(AbstractUser):
    email_token = models.CharField(max_length=200)
    email_is_verified = models.BooleanField(default=False)


class Product(models.Model):
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=1000)
    price = models.DecimalField(decimal_places=2)
    active = models.BooleanField(default=False)
    img = models.ImageField(upload_to="")


class Order(models.Model):
    order_id = models.IntegerField()
    buyer = models.ManyToManyField(User, blank=True, null=True, related_name="buyers")
