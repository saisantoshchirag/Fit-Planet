from django.urls import path,re_path
from django.conf.urls import include
from . import views

urlpatterns = [

    path('add/workout/', views.addworkout_view,name = 'add_workout'),
    path('show/workouts/', views.showworkouts_view, name= 'show_all_workouts'),
    path('signup/',views.add_trainer,name='add_trainer'),
    path('login/',views.login_trainer,name='login_trainer'),
    path('edit_profile',views.edit_profile,name='edit_profile'),
    path('',views.trainer_home,name="trainer_home"),
    path('logout',views.logout_trainer,name="logout_trainer"),
    path('',include('django.contrib.auth.urls')),
    path('show_all_trainers',views.show_all_trainers,name='show_all_trainers'),
    path('my_trainees',views.my_trainees,name="my_trainees")


]

