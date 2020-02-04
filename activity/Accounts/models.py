from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.
class Userprofile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    gender = models.CharField(max_length=1 ,default='M' ,choices=( ('M' , 'Male'),('F' , 'Female') ),null=True,blank=True )
    height = models.IntegerField(default=167,null=True,blank=True)
    weight = models.IntegerField(default=65,null=True,blank=True)

    age = models.IntegerField(default=25,null=True,blank=True)
    exc_lvl = models.CharField(max_length=100,default=0,null=True,blank=True,choices=(('0','Little to no exercise'),('1','Light exercise (1?3 days per week)'),('2','Moderate exercise (3?5 days per week)'),('3','Heavy exercise (6?7 days per week)'),('4','Very heavy exercise (twice per day, extra heavy workouts)')))
    phone_regex = RegexValidator(regex=r'^[1-9]\d{9}$', message="enter a valid phone number")
    phone_number = models.CharField(validators=[phone_regex],max_length=10, blank=True)
    profile_pic = models.ImageField(default='prof1.jpg', upload_to="profile_pics", null=True,blank=True)
    my_trainers = models.CharField(default='',max_length=50,null=True,blank=True)
    def __str__(self):
        return self.user.username


class Userlog(models.Model):
    username=models.CharField(max_length=200)

    def __str__(self):
        return self.username
    # @receiver(post_save, sender = User)
    # def create_profile(sender,instance,created, **kwargs):
    #
    #     if created:
    #         Userprofile.objects.create(user = instance)
    #     instance.userprofile.save()
class Servicelog(models.Model):
    count=models.IntegerField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.timestamp)