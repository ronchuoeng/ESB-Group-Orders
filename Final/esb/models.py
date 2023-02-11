from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
from datetime import timedelta

# Create your models here.


class User(AbstractUser):
    email_token = models.CharField(max_length=200)
    email_is_verified = models.BooleanField(default=False)


class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, unique=True)
    name = models.CharField(max_length=100, null=True)
    phone = models.CharField(max_length=100, null=True)
    address = models.CharField(max_length=200, null=True)

    def __str__(self):
        return self.name


class Category(models.Model):
    title = models.CharField(max_length=32)
    # Type is not necessary.
    type = models.CharField(max_length=32, null=True, blank=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = "Categories"
        ordering = ["type", "title"]


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
        ordering = ["-active", "title"]


class Purchases(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="products"
    )
    date_time = models.DateTimeField(null=True)
    quantity = models.IntegerField()
    buyer = models.ManyToManyField(Customer, blank=True, related_name="buyers")

    def __str__(self):
        return f"{self.id}: {self.product}"

    @property
    def is_expired(self):
        return timezone.now() >= self.date_time

    @property
    def reach_target(self):
        total_quantity = sum(
            [purchase.quantity for purchase in self.customer_purchases.all()]
        )
        return total_quantity >= self.quantity

    class Meta:
        verbose_name_plural = "Purchases"


class CustomerPurchase(models.Model):
    customer = models.ForeignKey(
        Customer, on_delete=models.CASCADE, related_name="customer_purchases"
    )
    purchase = models.ForeignKey(
        Purchases, on_delete=models.CASCADE, related_name="customer_purchases"
    )
    quantity = models.IntegerField()

    def __str__(self):
        return f"{self.customer} - {self.purchase} ({self.quantity})"
