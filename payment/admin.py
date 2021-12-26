from django.contrib import admin
from .models import Member, Company, CompanyAdmin, Product, Cart, CartItem, Pay


# Register your models here.

admin.site.register(Member)
admin.site.register(Company)
admin.site.register(CompanyAdmin)
admin.site.register(Product)
admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(Pay)