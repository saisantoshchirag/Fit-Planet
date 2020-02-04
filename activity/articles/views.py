from django.shortcuts import render,redirect
from rest_framework import generics
from .serialisers import article_serialiser,AnswerSerializer,PaymentSerializer,UserSerializer
from django.contrib.auth.models import User
import requests
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import get_object_or_404
import json
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.template.loader import get_template
from django.http import HttpResponse,HttpResponseRedirect

from .models import article,answered
from .forms import postarticle#,answerform
from django.contrib.auth.decorators import login_required

@login_required(login_url='/accounts/login/')
def answer_request(request,slug):
    # CALLED WHEN ANSWER BUTTON IS CLICKED
    response = requests.get('http://10.0.54.227:8005/qapi/')
    data = response.json()
    #print(data)
    for i in range(len(data)):
        data[i]['id'] = i + 1
    print('\n\n\n\n\n',data,'\n\n\n\n')
    for i in range(len(data)):
        if data[i]['id']==slug:
            q=data[i]['question']
    #print(q)
    #form = answerform()
    # l = article.objects.filter(title=slug)
    return render(request, "ans.html", {"context": q})

@login_required(login_url='/accounts/login/')

def list_view(request):
    l = article.objects.all().order_by('-published_on')
    page = request.GET.get('page', 1)
    paginator = Paginator(l,2)
    try:
        blogs = paginator.page(page)
    except PageNotAnInteger:
        blogs = paginator.page(1)
    except EmptyPage:
        blogs = paginator.page(paginator.num_pages)

    popular_list = article.objects.order_by('-upvoted_by')
    context = {"myobjects":blogs,"likesort":popular_list}


    #print('\n\n\n',[context['myobjects'][i].trainer_name for i in range(len(context['myobjects']))],'\n\n')
    return render(request,"list_all.html",context)


def detail_view(request,slug):
    l = article.objects.filter(title=slug)
    print(l)
    is_liked = False
    is_bookmarked = False
    if l[0].upvoted_by.filter(id = request.user.id).exists():
        is_liked = True
    if l[0].bookmarked_by.filter(id = request.user.id).exists():
        is_bookmarked = True
    count = l[0].total_upvotes()
    print(count)
    return render(request,"details.html",{"context":l,"is_liked":is_liked,"is_bookmarked":is_bookmarked,"count":count})

def favourites(request,id):
    art = get_object_or_404(article,id=id)
    if art.upvoted_by.filter(id=request.user.id).exists():
        art.upvoted_by.remove(request.user)
    else:
        art.upvoted_by.add(request.user)


    return HttpResponseRedirect(art.get_absolute_url())

def bookmarks(request,id):
    art = get_object_or_404(article, id=id)
    if art.bookmarked_by.filter(id=request.user.id).exists():
        art.bookmarked_by.remove(request.user)
    else:
        art.bookmarked_by.add(request.user)
    return HttpResponseRedirect(art.get_absolute_url())

def get_bookmarks(request):
    print("check....")
    all = article.objects.all()
    bookmark_array=[]
    for obj in all:
        print(obj)
        print(obj.bookmarked_by.filter(id=request.user.id).exists())
        if obj.bookmarked_by.filter(id=request.user.id).exists():
            bookmark_array.append(obj)

    return render(request,"list_all.html",{"myobjects":bookmark_array})






@login_required(login_url='login_trainer')
def create_view(request):
    form = postarticle(request.POST,request.FILES)
    if form.is_valid():
        print(form.cleaned_data)
        instance = form.save(commit=False)# can pass arg commit =false and later manipulate the dictionary data
        #article.objects.create(**form.cleaned_data)
        instance.trainer_name = request.user
        instance.save()
        return redirect("trainer_home")

    form = postarticle()
    context = {"form":form}
    return render(request, "create.html",context)

@login_required(login_url='login_trainer')
def quest(request):
    # DISPLAYS QUESTIONS
    response =requests.get('http://10.0.54.227:8005/qapi/')
    data = response.json()
    #print(data)
    for i in range(len(data)):
        data[i]['id'] = i+1
    context = {"jdata": data}
    return render(request, "questions.html", context)

@login_required(login_url='login_trainer')
def ans(request):
    # CALLED WHEN ANSWER IS SUBMITTED
    if request.method=="POST":
        question  = request.POST.get("question")
        answer = request.POST.get("answer")
        answered_by = User.objects.filter(username=request.user)[0]
        #print(answered_by)
       # print("\n\n\n",question,answer,"\n\n\n\n")
        modell = answered()
        modell.name = answered_by
        modell.question = question
        modell.answer = answer
        modell.save()

        return redirect('articles:questions')

# @login_required(login_url='login')
class api_list_answers(generics.ListAPIView):
    queryset = answered.objects.all()
    serializer_class = AnswerSerializer


# @login_required(login_url='login')
class api_list_articles(generics.ListAPIView):
    queryset = article.objects.all()
    serializer_class = article_serialiser

    def perform_create(self, serializer):
        serializer.save(trainer_name=self.request.user)



# @login_required(login_url='login')
class UserList(generics.ListAPIView):

    queryset = User.objects.all()
    serializer_class = UserSerializer


# @login_required(login_url='login')
class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

# @login_required(login_url='login')
class countblogs(generics.ListAPIView):
    queryset = article.objects.all()
    serializer_class = PaymentSerializer
