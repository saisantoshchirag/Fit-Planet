from django.urls import path
from . import views

app_name = 'activities'
urlpatterns = [
    # path('',views.article_list,name="list"),
    path('create/',views.createActivity,name="create"),
    path('view/',views.activityView,name="view"),
    # path('<slug>/',views.article_detail,name="detail"),
]