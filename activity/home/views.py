from django.shortcuts import render,HttpResponse
import os
from .models import Video,Count
from django.core.paginator import Paginator, EmptyPage,PageNotAnInteger
import pandas as pd
import requests
from django.contrib.auth.models import User
from .serialisers import Count_Serializer,VideoInfoSerializer
from rest_framework import generics
# Create your views here.

def  get_media(path,index):
    files,i,names = [],1,[]
    img1,img2 = [],[]
    dirs = []
    for root, dir, _ in os.walk(path):
        for d in dir:
            cur_path = os.path.join(root, d)
            for r, k, f in os.walk(cur_path):
                for file in f:
                    if '.mp4' in file:
                        cur_file = os.path.join(cur_path,file)
                        files.append(cur_file)
                        names.append(file.replace('.mp4',""))
                    elif '.jpg' in file and '_1.jpg' in file:
                        cur_file = os.path.join(cur_path,file)
                        img1.append(cur_file)
                    elif '.jpg' in file and '_2.jpg' in file:
                        cur_file = os.path.join(cur_path,file)
                        img2.append(cur_file)
                    dirs.append(d)
    if 'video' in path:
        return files,dirs,names
    elif 'images' in path and index==1:
        return img1
    else:
        return img2

def video(request):
    files,i = [],1
    path2 = r'C:\sem-5\SOAD\project\activity\media\videos\data'
    path1 = r'C:\sem-5\SOAD\project\activity\media\images\data'
    path = os.path.join(r'C:\sem-5\SOAD\project\activity\home','FINAL.csv')
    file = pd.read_csv(path)
    videos = [str(videos.name) for videos in Video.objects.all()]
    files1,mtype,names = get_media(path2,1)
    imgs1 = get_media(path1,1)
    imgs2 = get_media(path1,0)
    print(len(imgs2),len(imgs1))
    print(len(files1))
    print(len(names))
    print(len(mtype))
    for i in range(len(files1)):
        print(files1[i],'\t',mtype[i],'\t',names[i])
    vnames = [str(video.name) for video in Video.objects.all()]
    print(vnames)
    print(len(vnames))
    for i in range(len(vnames)):
        if vnames[i] == names[i]:
            print(True)
    for i in range(len(vnames)):
        print(vnames[i])
        print(imgs2[i])
        print(imgs1[i])
        print(files1[i])
    # for i in range(len(imgs1)):
    #     print(imgs1[i],'\t',imgs2[i])
    for i in range(len(vnames)):
        try:
            # Video.objects.filter(name=vnames[i]).update(video = files1[i])
            # Video.objects.filter(name=vnames[i]).update(image1 = imgs1[i])
            Video.objects.filter(name=vnames[i]).update(image2 = imgs2[i])
        except:
            print("error")
            print(vnames[i])
            print(files1[i])
    # for i in range(len(videos)):
    #     print(i)
    #     try:
    #         print(file.loc[file['Name']==videos[i],'Equipment'].values[0])
    #         equipment.append(file.loc[file['Name']==videos[i],'Equipment'].values[0])
    #     except:
    #         equipment.append("error")
    #         print("error")

    # for i in range(len(equipment)):
    #     Video.objects.filter(name=videos[i]).update(equipment=equipment[i])
    return HttpResponse('yes')

def video_display(request):
    checklist = request.POST.get('options[]')
    print(checklist)
    if checklist==None:
        videos = Video.objects.all()
    else:
        videos = Video.objects.all().filter(muscle_type=checklist)
    page = request.GET.get('page', 1)

    paginator = Paginator(videos,30)
    try:
        video_list = paginator.page(page)
    except PageNotAnInteger:
        video_list = paginator.page(1)
    except EmptyPage:
        video_list = paginator.page(paginator.num_pages)
    return render(request,'home/display.html',{'video_list':video_list})

def video_render(request,name):
    videos = Video.objects.filter(name=name)
    counts = Count.objects.all()
    existing = [(str(count.video),str(count.user)) for count in counts ]
    count = [str(video.count) for video in videos]
    print(count[0])
    Video.objects.filter(name=name).update(count=int(count[0])+1)
    if (str(name),str(request.user)) not in existing:
        Count.objects.create(video=str(name),user=request.user)

    return render(request,'home/video_display.html',{'videos':videos})

class apicount(generics.ListAPIView):
    queryset = Count.objects.all()
    serializer_class = Count_Serializer


class apivideoinfo(generics.ListAPIView):
    queryset = Video.objects.all().order_by('-count')[:15]
    serializer_class = VideoInfoSerializer




