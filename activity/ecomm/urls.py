from django.urls import path
from ecomm import views

app_name = 'ecomm'

urlpatterns = [
    path('', views.home, name="home"),
    path('check/<int:eq_id>/', views.check, name='check'),
    path('api/userpro/', views.UserProfile.as_view()),
    path('redirect/', views.redirect1, name='redirect'),
    path('api/clicks/', views.ClickCal.as_view()),
    path('add_to_cart/<int:item_id>/', views.add_to_cart, name="add_to_cart"),
    path('items/', views.product_list, name="product_list"),
    path('item/delete/<int:item_id>/', views.delete_from_cart, name="delete_item"),
    path('order_summary/', views.order_summary, name="order_summary"),
    path('checkout/', views.checkout, name="checkout"),
    path('api/owned/', views.AmountPayed.as_view()),

]
