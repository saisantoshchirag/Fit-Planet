# Generated by Django 2.1.1 on 2019-12-10 08:55

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Trainerprofile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Age', models.IntegerField()),
                ('experience', models.IntegerField()),
                ('address', models.TextField(max_length=250)),
                ('phone_number', models.CharField(blank=True, max_length=10, validators=[django.core.validators.RegexValidator(message='enter a valid phone number', regex='^[1-9]\\d{9}$')])),
                ('profile_pic', models.ImageField(default='prof1.jpg', null=True, upload_to='profile_pics')),
                ('my_trainees', models.CharField(blank=True, default='', max_length=40, null=True)),
                ('description', models.TextField(default='I am a very good trainer', max_length=250)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Workouts',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('workout_name', models.CharField(max_length=500)),
                ('workout_videofile', models.FileField(null=True, upload_to='videos1/', verbose_name='')),
            ],
        ),
    ]
