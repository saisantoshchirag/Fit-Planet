from rest_framework import serializers
from .models import Video,Count

class Count_Serializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    class Meta:
        model = Count
        fields = ['video','user']


class VideoInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Video
        fields = ['name','muscle_type','equipment','count']

