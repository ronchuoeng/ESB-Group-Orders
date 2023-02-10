from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.


class User(AbstractUser):
    email_token = models.CharField(max_length=200)
    email_is_verified = models.BooleanField(default=False)


class Category(models.Model):
    title = models.CharField(max_length=32)

    def __str__(self):
        return self.title


class Product(models.Model):
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=1000)
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="categories",
    )
    price = models.DecimalField(max_digits=10, decimal_places=2)
    active = models.BooleanField(default=False)
    img = models.ImageField(upload_to="esb/static/esb")

    def __str__(self):
        if self.active:
            return f"{self.title} |Active"
        else:
            return self.title

    class Meta:
        ordering = ["active", "title"]


class Purchases(models.Model):
    order_id = models.IntegerField()
    date_time = models.DateTimeField(null=True)
    item = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="items")
    buyer = models.ManyToManyField(User, blank=True, related_name="buyers")

    def __str__(self):
        return f"{self.order_id}: {self.item}"
