from datetime import datetime

from django.contrib import messages

import requests
import json

from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.views.generic import ListView
from django.http import HttpResponse
from ecomm.models import UserPro, ClickCost, Products, OrderItem, Order, Owned, Amount_Payed
from ecomm.serializers import UserProSerializer, ClickCostSerailizer, OwnedSerializer, AmountSerializer
from ecomm.extras import generate_order_id
from django.contrib.auth.decorators import login_required
# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from Accounts.models import Userprofile


@login_required(login_url='Accounts:login')
def home(request):
    response = requests.get("http://10.0.54.227:8000/ecomm/api/equip/")
    global all_data
    all_data = response.json()
    if Products.objects.all() is not None:
        Products.objects.all().delete()
    for item in all_data:
        data = list(item.values())
        product = Products(id=data[0], name=data[1], image_url=data[2], type=data[3], cost=data[4])
        product.save()
    # current_order_products = []
    # return render(request, "ecomm/index.html", {'all_data':all_data, 'current_order_products': current_order_products})
    return redirect(reverse('ecomm:product_list'))

@login_required(login_url='Accounts:login')
def product_list(request):
    all_data = Products.objects.all()
    user_name = UserPro.objects.last()

    filtered_orders = Order.objects.filter(owner=user_name, is_ordered=False)
    current_order_products = []
    if filtered_orders.exists():
        user_order = filtered_orders[0]
        user_order_items = user_order.items.all()
        current_order_products = [product.product for product in user_order_items]
    own = Owned.objects.filter(user_name=user_name, is_ordered=True).values('equip_id')
    ids = []
    for each_id in own:
        ids.append(each_id['equip_id'])
    print(ids)
    return render(request, "ecomm/index.html", {'all_data': all_data, 'current_order_products': current_order_products, 'ids':ids})

@login_required(login_url='Accounts:login')
def check(request, eq_id):
    #response = requests.get("http://10.0.33.60:8000/ecomm/api/equip/")
    #items = response.json()
    items = all_data
    print(items)
    for item in items:
        equip = list(item.values())
        if eq_id == int(equip[0]):
            return render(request, "ecomm/check.html", {'item':item})
    return HttpResponse("Item not found")

def redirect1(request):
    user = request.user.username
    uid = request.user.id
    print(uid)
    s = ClickCost.objects.all()
    print(s)

    instance, status = ClickCost.objects.get_or_create(user_id=uid)

    try:
        instance = ClickCost.objects.get(user_id=uid)
        print(instance)
        click = int(instance.clicks) + 1
        print(click)
        instance.clicks = click
        instance.save()
    except:
        ClickCost.objects.create(user_id=uid, clicks=1)
        #instance.save()
    return redirect('http://10.0.54.227:8000/ecomm/')

@login_required(login_url='Accounts:login')
def add_to_cart(request, **kwargs):
    user_name = UserPro.objects.last()
    product = Products.objects.filter(id=kwargs.get('item_id')).first()
    curr_list = UserPro.objects.filter(user_name=user_name).values('equipments__name')
    alr_equip = []
    for item in curr_list:
        alr_equip.append(item['equipments__name'])
    if product in alr_equip:
        messages.info(request, 'You already own this item')
        return redirect(reverse('ecomm:product_list'))
        # return render(request, "ecomm/index.html", {'all_data':all_data})
    order_item, status = OrderItem.objects.get_or_create(product=product)
    user_order, status = Order.objects.get_or_create(owner=user_name, is_ordered=False)
    user_order.items.add(order_item)
    user_order.ref_code = generate_order_id()
    user_order.save()
    # if status:
    #     user_order.ref_code = generate_order_id()
    #     user_order.save()
    messages.info(request, 'Item added to the cart')
    # return render(request, "ecomm/index.html", {'all_data':all_data})
    return redirect(reverse('ecomm:product_list'))

def delete_from_cart(request, item_id):
    item_to_delete = OrderItem.objects.filter(pk=item_id)
    if item_to_delete.exists():
        item_to_delete[0].delete()
        messages.info(request, "Item has been deleted")
    return redirect(reverse('ecomm:order_summary'))

def get_user_pending_order(request):
    user_name = UserPro.objects.last()
    # user_profile = get_object_or_404(UserPro, user=request.user).values('user_name')
    order = Order.objects.filter(owner=user_name, is_ordered=False)
    if order.exists():
        return order[0]
    return 0

@login_required(login_url='Accounts:login')
def order_summary(request):
    order = get_user_pending_order(request)
    return render(request, 'ecomm/order_summary.html', {'order':order})

@login_required(login_url='Accounts:login')
def checkout(request):
    user_name = UserPro.objects.last()
    code = Order.objects.filter(owner=user_name, is_ordered=False).values('ref_code').last()
    pid = Order.objects.filter(owner=user_name, is_ordered=False).values('items__product__id')
    cost = Order.objects.filter(owner=user_name, is_ordered=False).values('items__product__cost')

    # print("abc", pid[0]['items__product__id'])
    tot_cost=0
    for i in range(len(pid)):
        print(code['ref_code'])
        tot_cost += cost[i]['items__product__cost']
        own = Owned(ref_code=code['ref_code'], user_name=user_name, equip_id=pid[i]['items__product__id'], is_ordered=True)
        own.save()

    if Order.objects.all() is not None:
        Order.objects.all().delete()
    if OrderItem.objects.all() is not None:
        OrderItem.objects.all().delete()
    payment = Amount_Payed(ref_code=code['ref_code'], cost=tot_cost)
    payment.save()
    return redirect('http://10.0.54.227:8000/ecomm/pay')

class UserProfile(APIView):

    def get(self, request):
        user = UserPro.objects.last()
        serializer = UserProSerializer(user)
        return Response(serializer.data)

class ClickCal(APIView):

    def get(self, request):
        costs = ClickCost.objects.all()
        serializer = ClickCostSerailizer(costs, many=True)
        return Response(serializer.data)

class OwnedItems(APIView):

    def get(self, request):
        costs = Owned.objects.all()
        serializer = OwnedSerializer(costs, many=True)
        return Response(serializer.data)

class AmountPayed(APIView):

    def get(self, request):
        amount = Amount_Payed.objects.last()
        serializer = AmountSerializer(amount)
        return Response(serializer.data)
