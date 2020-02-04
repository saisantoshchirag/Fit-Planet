from django.contrib import admin
from ecomm.models import UserPro, ClickCost, Products, Order, OrderItem, Owned

# Register your models here.
admin.site.register(UserPro)
admin.site.register(ClickCost)
admin.site.register(Products)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(Owned)