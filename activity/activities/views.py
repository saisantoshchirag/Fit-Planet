from django.shortcuts import render,redirect,HttpResponse
from .models import Activity
from . import forms
from django.contrib.auth.decorators import login_required
import pandas as pd
from datetime import datetime
from calendar import monthrange
import numpy as np
import matplotlib
matplotlib.use('Agg')
from matplotlib import pyplot as plt
import os
from Accounts.models import Userprofile
# Create your views here.

@login_required(login_url='login')
def activityView(request):
    total_calories,today = [],datetime.now().day
    activity = Activity.objects.filter(user=request.user).order_by("-from_time")
    x = []
    print(request.user)
    for i in range(20):
        if datetime.now().day - i >0 :
            print(i,datetime.now().day-i)
            act4 = Activity.objects.filter(user=request.user,from_time__gte=datetime(2019,datetime.now().month,today-i),from_time__lte=datetime(2019,datetime.now().month,today-i+1))
            print('act4',act4)
            calories2 = [int(act.calories) for act in act4]
            x.append(str(datetime.now().month)+'-'+str(today-i))
        elif datetime.now().day - i <= 0:
            days = monthrange(2019,datetime.now().month-1)[1]
            activity1 = Activity.objects.filter(user=request.user,from_time__gte=datetime(2019,datetime.now().month-1,days-i+today-1),from_time__lte=datetime(2019,datetime.now().month-1,days-i+today))
            x.append(str(datetime.now().month-1)+'-'+str(days-i+today))
            calories2 = [int(act.calories) for act in activity1]
        total_calories.append(sum(calories2))
    plt.figure()
    plt.plot(np.array(total_calories), marker='.', markerfacecolor='blue', markersize=12, color='skyblue', linewidth=4)
    plt.xticks(np.arange(len(x)),x)
    plt.title('Calories burnt in the last 20 days')
    plt.xticks(rotation=30)
    path = os.path.join(r'C:\sem-5\SOAD\project\activity\static','1.png')
    plt.savefig(path)
    return render(request,'activities/activity_view.html',{'activity':activity})


@login_required(login_url='Accounts:login')
def createActivity(request):
    file = pd.read_csv(r'C:\sem-5\SOAD\project\activity\activities\exercises.csv',encoding = 'unicode_escape',index_col=False)
    types = file['Activity']
    if request.method == 'POST':
        form = forms.CreateActivity(request.POST,request.FILES)
        weight = [int(user.weight) for user in Userprofile.objects.filter(user=request.user)]
        type = request.POST.get('type1')
        if form.is_valid():
            instance = form.save(commit=False)
            diff = instance.to_time - instance.from_time
            dur_in_s = diff.total_seconds()
            calories_1hr = (file[file['Activity']==type]['130 lb/58.967kgs'])*weight[0]/58.967
            calories = calories_1hr * dur_in_s/3600
            instance.type = type
            instance.calories = calories
            instance.user = request.user
            if instance.from_time > instance.to_time:
                return HttpResponse('<html><head><script>alert("Start time should be before end time");window.location="/activities/create";</script></head></html>')
            if instance.from_time > datetime.now() or instance.to_time > datetime.now():
                return HttpResponse('<html><head><script>alert("Start time or end time cant be after current time");window.location="/activities/create";</script></head></html>')
            instance.save()
            return redirect('activities:view')
    else:
        form = forms.CreateActivity()
    return render(request, "activities/create_activity.html", {'form': form,'types':types})
