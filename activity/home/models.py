
from django.db import models
import uuid
from django.contrib.auth.models import User

# Create your models here.
class Video(models.Model):
    video = models.FileField(upload_to='videos1/')
    muscle_type = models.CharField(max_length=100)
    video_id = models.UUIDField(default=uuid.uuid4)
    equipment = models.CharField(max_length=25)
    image1 = models.FileField(blank=True)
    image2 = models.FileField(blank=True)
    name = models.CharField(max_length=40)
    description = models.TextField()
    count = models.IntegerField(default=0)

class Count(models.Model):
    video = models.CharField(max_length=40)
    user = models.ForeignKey(User,on_delete=models.PROTECT)
