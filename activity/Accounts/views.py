from django.shortcuts import render,redirect
from django.contrib.auth import login,logout
from .forms import CustomUserCreationForm,LoginForm,UserupdateForm,ProfileupdateForm,Createprofileform
from django.contrib.auth.models import User
from .models import Userprofile
from django.contrib import messages
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .token import account_activation_token
from django.core.mail import EmailMessage
from django.http import HttpResponse
from Trainers.models import Trainerprofile
from django.contrib.auth.decorators import login_required
from ecomm.models import UserPro
from Accounts.models import Servicelog,Userlog
from .serializers import ServiceSerializer,UserprofileSerializer
import requests,json
from rest_framework import generics

def login_view(request):

    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        print(request.POST)
        if form.is_valid():
            user = form.login(request)
            login(request,user,backend='django.contrib.auth.backends.ModelBackend')
            UserPro.objects.create(user_name=user.username)
            Userlog.objects.create(username=user.username)

            if 'next' in request.POST:
                return redirect(request.POST.get('next'))
            else:
                return redirect('home')
    else:
        form = LoginForm()
    return render(request, 'Accounts/login_new.html',{'form': form})



def register(request):
    print("\n\n",'Enter register')
    if request.method == 'POST' and request.FILES:
        print('entered if of post and files')
        u_form = CustomUserCreationForm(data=request.POST)
        p_form = Createprofileform(data=request.POST)
        print("forms are not valid")

        if u_form.is_valid():
            print('u form validation done ')
            if p_form.is_valid():
                print('p form validation done')
                print('forms are valid')
                user = u_form.save(commit=False)
                # user.is_active = False
                user.set_password(user.password)
                print('helloooo','password set')
                user.save()

                profile = p_form.save(commit=False)
                profile.user = user

                if 'profile_pic' in request.FILES:
                    profile.profile_pic = request.FILES['profile_pic']

                profile.save()
                return redirect('Accounts:login')
    else:
        u_form = CustomUserCreationForm()
        p_form = Createprofileform()

    return render(request, 'Accounts/new.html', {'u_form': u_form,'p_form':p_form})



def logout_view(request):
    if request.method == 'POST':
        logout(request)
        return redirect('home')


def profile_view(request):
    return render(request, "Accounts/profile.html",{'user':request.user})

@login_required(login_url='Accounts:signin')
def trainers(request):
    users = Trainerprofile.objects.all()
    return render(request,'Accounts/all_trainers.html',{'users':users})



def edit_profile(request):
    if request.method == 'POST':
        userupdateform = UserupdateForm(request.POST,instance=request.user)
        profileupdateform = ProfileupdateForm(request.POST,
                                              request.FILES,
                                              instance=request.user.userprofile)
        if userupdateform.is_valid() and profileupdateform.is_valid():
            userupdateform.save()
            profileupdateform.save()
            return redirect('Accounts:profile')
    else:
        user1 = User.objects.filter(username = request.user.username).first()
        if Userprofile.objects.filter(user = user1):

            userupdateform = UserupdateForm(instance=request.user)
            profileupdateform = ProfileupdateForm(instance=request.user.userprofile)
        else:
            Userprofile.objects.create(user = user1)
            userupdateform = UserupdateForm(instance=request.user)
            profileupdateform = ProfileupdateForm(instance=request.user.userprofile)

    return render(request,'Accounts/editprofile.html',{'uform':userupdateform , 'pform':profileupdateform})

def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request,user,backend='django.contrib.auth.backends.ModelBackend')
        # return redirect('home')
        return render(request,'Accounts/after_active.html')
    else:
        return HttpResponse('Activation link is invalid!')


@login_required(login_url='Accounts:signin')
def book_now(request):
    if request.method=='POST':
        count=request.POST.get('submit')
        print(count)
        trainer_username=request.POST.get(count)
        print(trainer_username)
        user1=User.objects.get(username=request.user.username)
        user2=User.objects.get(username=trainer_username)
        trainees=Trainerprofile.objects.get(user=user2).my_trainees
        trainer_email=user2.email
        trainer_experience=Trainerprofile.objects.get(user=user2).experience
        trainer_age = Trainerprofile.objects.get(user=user2).Age
        trainer_description = Trainerprofile.objects.get(user=user2).description
        trainer_profile_pic = Trainerprofile.objects.get(user=user2).profile_pic
        trainers=Userprofile.objects.get(user=user1).my_trainers
        print(user2)
        if trainees == None:trainees=''
        if request.user.username not in trainees.split('+'):
            if trainees=='':
                trainees=request.user.username
            else:
                trainees=trainees+'+'+request.user.username
        Trainerprofile.objects.filter(user=user2).update(my_trainees=trainees)
        print(trainer_username)
        print(trainers)

        if trainers== None:
            Userprofile.objects.filter(user=user1).update(my_trainers=trainer_username)
        print(trainees)
        trainer_username=trainer_username.replace('_trainer_','')
        return render(request,'Accounts/home1.html',{'trainer_username':trainer_username,'trainer_email':trainer_email,'trainer_experience':trainer_experience,'trainer_age':trainer_age,'trainer_description':trainer_description,'trainer_profile_pic':trainer_profile_pic})

# class bmi_api(generics.ListAPIView):
#     serializer_class = UserprofileSerializer
#     def get_queryset(self):
#         username=Userlog.objects.last()
#         user=User.objects.filter(username=username).first()
#         return Userprofile.objects.filter(user=user)

class bmi_api(generics.ListAPIView):
    serializer_class = UserprofileSerializer
    def get_queryset(self):
        userlogs_query=Userlog.objects.all()
        users_list=[]
        for i in userlogs_query:
            users_list.append(i.username)
        users_query=User.objects.filter(username__in=users_list)
        query=Userprofile.objects.filter(user__in=users_query)
        # user=User.objects.filter(username=username).first()
        # return Userprofile.objects.filter(user=user)
        return query

# def diet_plan_view(request):
#     response=requests.get("http://10.0.54.37:8008/planner/api_return/")
#     data=response.json()[0]
#     count = data['count']
#     print("/n/ndata",data['count'])
#     # last_count=Servicelog.objects.last().count
#     Servicelog.objects.create(count=count)
#     bmi,calories=data['bmi'],data['calories']
#     print(bmi,type(bmi),calories,type(calories))
#     return render(request,'Accounts/diet_plan.html',{'bmi':bmi,'calories':calories})

def diet_plan_view(request):
    try:
        Userlog.objects.get(username=request.user.username)
    except:
        Userlog.objects.create(username=request.user.username)

    response=requests.get("http://10.0.54.227:8008/planner/api_return/")
    print("\n\nresponse:",response,"\n\n")
    # data=response.json()[0]
    data2=response.json()
    print('\n\ncurr : ',request.user.username)
    # print(data)
    print(data2)
    q=[]
    for i in data2:
        if i['username'].replace("_fit_planet_","") == request.user.username:
            q.append(i)
    print("\n\n Q :",q)
    print("\n\n latest : ",q[0])

    # count = data['count']
    # username=data['username']
    # print("\n\ndata",data['count'])
    data=q[0]
    count = data['count']-1
    username=data['username']
    print("\n\ndata",data['count'])
    url = data['url']
    # last_count=Servicelog.objects.last().count
    Servicelog.objects.create(count=count)
    bmi,calories=data['bmi'],data['calories']
    print(bmi,type(bmi),calories,type(calories))
    return render(request,'diet_plan_service.html',{'bmi':bmi,'calories':calories,'username':username,'url':url})


class service_data(generics.ListAPIView):
    serializer_class = ServiceSerializer
    def get_queryset(self):
        object=Servicelog.objects.last().timestamp
        print("\n\nobject = ",object,type(object))
        s=Servicelog.objects.latest('timestamp')
        print(s,type(s))
        # Servicelog.objects.all().order_by('-timestamp').first()
        return Servicelog.objects.filter(timestamp=object)


class bmi_details(generics.ListAPIView):
    serializer_class = UserprofileSerializer
    # queryset = Userprofile.objects.all()
    def get_queryset(self):

        username = self.kwargs['username']
        user1= User.objects.filter(username=username).first()
        return Userprofile.objects.filter(user=user1)
def maps(request,slug):

    user2=User.objects.get(id=slug)
    address=Trainerprofile.objects.get(user=user2).address
    return render(request,'Accounts/maps.html',{'address':address})