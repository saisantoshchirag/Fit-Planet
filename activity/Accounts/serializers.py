from rest_framework import serializers
from .models import User,Userprofile,Servicelog

class UserprofileSerializer(serializers.ModelSerializer):
    user= serializers.ReadOnlyField(source='user.username')
    class Meta:
        model= Userprofile
        fields = ['user','height', 'weight', 'age','exc_lvl','gender']

class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Servicelog
        fields = ['count','timestamp']