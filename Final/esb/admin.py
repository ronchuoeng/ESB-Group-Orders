from django.contrib import admin
from .models import User, Product, PurchaseOrder, Category, Customer, CustomerPurchase, ProductImage

# Register your models here.

admin.site.register(User)
admin.site.register(Customer)
admin.site.register(Category)
admin.site.register(Product)
admin.site.register(PurchaseOrder)
admin.site.register(CustomerPurchase)
admin.site.register(ProductImage)
