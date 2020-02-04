"""activity URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from activities import views as activity_views
from . import views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls.static import static

from . import settings

app_name = 'activity'
urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.home,name="home"),
    path('activities/',include('activities.urls')),
    path('accounts/', include('Accounts.urls')),
    path('video/',include('home.urls')),
    path('articles/',include('articles.urls')),
    path('trainer/',include('Trainers.urls')),
    path('auth/',include('social_django.urls',namespace='social')),
    path('ecomm/',include('ecomm.urls'))
]


urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)


