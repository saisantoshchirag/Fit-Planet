from django.urls import path,include
from . import views
from .views import apicount,apivideoinfo
app_name = 'home'
urlpatterns = [

    path('videos',views.video,name="video"),
    path('display/',views.video_display,name="display"),
    path('display/<name>',views.video_render,name="render"),
    path('countapi',apicount.as_view(),name="capi"),
    path('infoapi',apivideoinfo.as_view(),name="iapi"),
]