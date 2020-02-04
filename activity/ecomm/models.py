from django.conf import settings
from django.db import models
from Accounts.models import Userprofile

# Create your models here.
from django.db.models.signals import post_save
from django.contrib.auth import get_user_model


class Products(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.TextField(max_length=200)
    image_url = models.URLField(max_length=250)
    type = models.TextField(max_length=50, null=True)
    cost = models.PositiveIntegerField()

    def __str__(self):
        return self.name

class UserPro(models.Model):
    user_name = models.TextField(max_length=100)
    equipments = models.ManyToManyField(Products, blank=True, default=None)

    def __str__(self):
        return self.user_name

# def post_save_profile_create(sender, instance, created, *args, **kwargs):
#     if created:
#         UserPro.objects.get_or_create(user_name=instance)
#
# post_save(post_save_profile_create, sender=settings.AUTH_USER_MODEL)

class ClickCost(models.Model):
    id = models.AutoField(primary_key=True)
    user_id = models.IntegerField(default=0)
    clicks = models.IntegerField(default=0)

    def __str__(self):
        return str(self.id)

class OrderItem(models.Model):
    product = models.OneToOneField(Products, on_delete=models.SET_NULL, null=True)
    is_ordered = models.BooleanField(default=False)
    date_added = models.DateTimeField(auto_now=True)
    date_ordered = models.DateTimeField(null=True)

class Order(models.Model):
    ref_code = models.TextField(max_length=20)
    owner = models.ForeignKey(UserPro, on_delete=models.SET_NULL, null=True)
    is_ordered = models.BooleanField(default=False)
    items = models.ManyToManyField(OrderItem)
    date_ordered = models.DateTimeField(auto_now=True)

    def get_cart_items(self):
        return self.items.all()

    def get_cart_total(self):
        return sum([item.product.cost for item in self.items.all()])

    def __str__(self):
        return '{0} - {1}'.format(self.owner, self.ref_code)

class Owned(models.Model):
    ref_code = models.TextField(max_length=20)
    user_name = models.TextField(max_length=100)
    equip_id = models.IntegerField()
    is_ordered = models.BooleanField(default=False)

class Amount_Payed(models.Model):
    ref_code = models.TextField(max_length=20)
    cost = models.PositiveIntegerField()


