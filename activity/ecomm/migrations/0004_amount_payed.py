# Generated by Django 2.1.1 on 2019-12-11 18:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ecomm', '0003_auto_20191211_1945'),
    ]

    operations = [
        migrations.CreateModel(
            name='Amount_Payed',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ref_code', models.TextField(max_length=20)),
                ('cost', models.PositiveIntegerField()),
            ],
        ),
    ]
