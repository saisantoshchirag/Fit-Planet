from django.db import models
from django.core.validators import RegexValidator
from django.contrib.auth.models import User
from home.models import Video
# Create your models here.

class Workouts(models.Model):
    workout_name= models.CharField(max_length=500)
    workout_videofile= models.FileField(upload_to='videos1/', null=True, verbose_name="")


    def __str__(self):
        return self.workout_name + ": " + str(self.workout_videofile)
class Trainerprofile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    Age = models.IntegerField()
    experience=models.IntegerField()
    address=models.TextField(max_length=250)
    phone_regex = RegexValidator(regex=r'^[1-9]\d{9}$', message="enter a valid phone number")
    phone_number = models.CharField(validators=[phone_regex], max_length=10, blank=True)
    profile_pic = models.ImageField(default='prof1.jpg', upload_to="profile_pics", null=True)
    my_trainees=models.CharField(default='',max_length=40,blank=True,null=True)
    description=models.TextField(max_length=250,default='I am a very good trainer')
    def __str__(self):
        return self.user.username

    # def createProfile(sender, **kwargs):
    #     if kwargs['created']:
    #         user_profile = Userprofile.objects.created(user=kwargs['instance'])
    #
    #     post_save.connect(createProfile, sender=User)

