from django.shortcuts import render,redirect
from django.http import HttpResponse,HttpResponseRedirect
from django.conf import settings
from .forms import AddworkoutForm,LoginForm,EditProfileForm,ProfileForm
from .models import Workouts,Trainerprofile
from Accounts.models import Userprofile
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
# Create your views here.

def trainer_home(request):

    return render(request,'Trainers/trainer_homepage.html')

@login_required(login_url='login_trainer')
def addworkout_view(request):
    if request.method=='POST':
        awform =AddworkoutForm(request.POST or None, request.FILES or None)
        if awform.is_valid():
            awform.save()

        return redirect('trainer_home')
    else:
        awform=AddworkoutForm()
    return render(request, 'Trainers/add_workout.html', {'awform': awform})
   # return HttpResponse("Add workout page")

def showworkouts_view(request):
    all_workouts=Workouts.objects.all()
    # for i in all_workouts:
    #     i.workout_videofile= settings.MEDIA_URL+str(i.workout_videofile)

    return render(request, 'Trainers/show_all_workouts.html', {'all_workouts':all_workouts})


def add_trainer(request):
    if request.method == "POST": #and request.FILES['image1']:
        name=request.POST.get('name')
        name='_trainer_'+name
        email=request.POST.get('email')
        password=request.POST.get('pass')
        confirm_pass=request.POST.get('pass1')
        Age=request.POST.get('Age')
        experience=request.POST.get('experience')
        address=request.POST.get('address')
        ph_number=request.POST.get('number')
        image=request.POST.get('image')
        description=request.POST.get('description')
        user1=User.objects.create(username=name,email=email)
        user1.set_password(password)
        user1.save()
        print("\n",password,"\n")
        Trainerprofile.objects.create(user=user1,Age=Age,experience=experience,address=address,phone_number=ph_number,profile_pic=image,description=description)
        return redirect('trainer_home')
    else:
        return render(request,'Trainers/new_login.html')

def login_trainer(request):
    if request.method == "POST":
        print("\n\npost = ",request.POST)
        form=LoginForm(data=request.POST)
        if form.is_valid():
            user=form.login(request)
            # user=form.save()
            print("\n\nuser=",user)
            print('\nabt to login\n\n')
            login(request,user,backend='django.contrib.auth.backends.ModelBackend')
            print('\n\nuser= ',request.user)
            if 'next' in request.POST:
                return redirect(request.POST.get('next'))
            else:
                return redirect('trainer_home')
    else:
        form=LoginForm()

    return render(request,'Trainers/login.html',{'form':form})

def logout_trainer(request):
    if request.method == 'POST':
        logout(request)
        return redirect('trainer_home')

def edit_profile(request):
    if request.method == 'POST':
        form = EditProfileForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, request.FILES, instance=request.user.trainerprofile)

        if form.is_valid() and profile_form.is_valid():
            user_form = form.save()
            custom_form = profile_form.save(False)
            custom_form.user = user_form
            custom_form.save()
            return redirect('edit_profile')
    else:
        form = EditProfileForm(instance=request.user)
        profile_form = ProfileForm(instance=request.user.trainerprofile)
        args = {}
        # args.update(csrf(request))
        args['form'] = form
        args['profile_form'] = profile_form
        return render(request, 'Trainers/trainer_profile.html', args)

@login_required(login_url='Accounts:signin')
def show_all_trainers(request):
    users = Trainerprofile.objects.all()
    return render(request,'Trainers/all_trainers.html',{'users':users})

@login_required(login_url='login_trainer')
def my_trainees(request):
    user1 = User.objects.get(username=request.user.username)
    trainees = Trainerprofile.objects.get(user=user1).my_trainees
    trainees = trainees.split('+')
    print(trainees,len(trainees))
    if trainees[0] == '':
        users = []
        return render(request, 'Trainers/my_trainees.html', {'users': users})
    else:
        users = []
        for trainee in trainees:
            print("\n\n",trainee,"\n\n\n")
            user2 = User.objects.get(username=trainee)

            user_data = Userprofile.objects.get(user=user2)
            users.append(user_data)

        return render(request,'Trainers/my_trainees.html',{'users':users})



