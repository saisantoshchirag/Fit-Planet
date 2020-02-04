from django.urls import path,re_path
from django.conf.urls import include
from . import views

app_name = 'Accounts'

urlpatterns = [

    path('login/', views.login_view,name = 'signin'),
    path('logout/', views.logout_view , name = 'logout'),
    # path('signup/', views.signup_view,name = 'signup'),
    path('register/', views.register,name = 'register'),
    path('booknow/',views.book_now,name="booknow"),
    re_path('^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',views.activate,name='activate'),
    # path('profile_new/', views.profile_form,name = 'profile_new'),
    path('profile/',views.profile_view,name = 'profile'),
    path('profile/edit/',views.edit_profile,name = 'editprofile'),
    path('', include('django.contrib.auth.urls')),
    path('trainers/',views.trainers,name="mytrainers"),
    path('api/', views.bmi_api.as_view(), name='bmiapi'),
    path('diet_plan/', views.diet_plan_view, name='diet_plan'),
    path('service_data/', views.service_data.as_view(), name='service_data'),
    path('maps/<str:slug>',views.maps,name='maps')
]


