# Generated by Django 2.1.1 on 2019-12-10 08:54

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Count',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('video', models.CharField(max_length=40)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Video',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('video', models.FileField(upload_to='videos1/')),
                ('muscle_type', models.CharField(max_length=100)),
                ('video_id', models.UUIDField(default=uuid.uuid4)),
                ('equipment', models.CharField(max_length=25)),
                ('image1', models.FileField(blank=True, upload_to='')),
                ('image2', models.FileField(blank=True, upload_to='')),
                ('name', models.CharField(max_length=40)),
                ('description', models.TextField()),
                ('count', models.IntegerField(default=0)),
            ],
        ),
    ]
