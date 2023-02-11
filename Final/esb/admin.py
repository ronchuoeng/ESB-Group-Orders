from django.contrib import admin
from .models import User, Product, Purchases, Category, Customer

# Register your models here.

admin.site.register(User)
admin.site.register(Customer)
admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Purchases)
