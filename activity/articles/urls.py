from django.urls import path
from django.conf.urls import url
from . import views
from .views import api_list_articles,api_list_answers,countblogs,UserList

app_name = 'articles'
urlpatterns = [

    path('all/', views.list_view, name='lview'),
    path('all/<str:slug>/', views.detail_view, name='dview'),
    url(r'(?P<id>\d+)/favourite/$',views.favourites,name='favourite_article'),
    url(r'(?P<id>\d+)/bookmark/$',views.bookmarks,name='bookmark_article'),
    url('mybookmarks/',views.get_bookmarks,name="my_bookmarks"),
    path('create/', views.create_view, name='cview'),
    #path('api/', api_list_articles, name="all_articles"),
    path('api/', api_list_articles.as_view(), name="all_articles"),
    path('users/', views.UserList.as_view()),
    path('questions/',views.quest,name='questions'),
    path('questions/<int:slug>/', views.answer_request, name='ansreq'),
    path('answers/',views.ans,name='ans'),
    path('ansapi/',api_list_answers.as_view(),name='name'),
    path('count/',countblogs.as_view()),
    #path('uapi/',UserList.as_view())
    #path('new/',views.example)
]