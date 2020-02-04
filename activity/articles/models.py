from django.db import models
import datetime
from django.conf import settings
from django.urls import reverse
# Create your models here.

User = settings.AUTH_USER_MODEL

class article(models.Model):
    trainer_name = models.ForeignKey(User,null=True,on_delete=models.SET_NULL)
    title = models.CharField(max_length=70)
    image = models.ImageField(upload_to='image/')
    #slug = models.SlugField(unique=True,null=True)
    content = models.TextField(max_length=1000)
    published_on = models.DateTimeField(default=datetime.datetime.now)
    upvoted_by = models.ManyToManyField(User,related_name='upvotes',blank=True)
    bookmarked_by = models.ManyToManyField(User,related_name='bookmark',blank=True)

    def total_upvotes(self):
        return self.upvoted_by.count()

    def get_absolute_url(self):
        return reverse("articles:dview",args=[self.title])
    #
    # def __str__(self):
    #     return self.trainer_name


# removed defaut=1 from trainer_name
class answered(models.Model):
    name = models.TextField(max_length=14)
    question = models.TextField(max_length=60)
    answer = models.TextField(max_length=1000)





