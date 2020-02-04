from django.db import models
import django.utils.timezone

from datetime import datetime as datetime
from django.contrib.auth.models import User
# Create your models here.
class Activity(models.Model):
    title = models.CharField(max_length=100)
    type = models.CharField(max_length=100)
    from_time = models.DateTimeField(blank=True,null=True)
    to_time = models.DateTimeField(blank=True,null=True)
    calories = models.IntegerField(blank=True,null=True)
    # from_time = models.TimeField(blank=True,null=True)
    # to_time = models.TimeField(blank=True,null=True)
    user = models.ForeignKey(User,default=None,on_delete=models.PROTECT)
