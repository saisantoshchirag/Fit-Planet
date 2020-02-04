from rest_framework import serializers
from .models import article,answered
from django.contrib.auth.models import User


class article_serialiser(serializers.ModelSerializer):
    trainer_name = serializers.ReadOnlyField(source='trainer_name.username')
    class Meta:
        model = article
        fields = ['trainer_name','title','image','content','published_on']
        depth = 1

class UserSerializer(serializers.ModelSerializer):
    articles = serializers.PrimaryKeyRelatedField(many=True, queryset=article.objects.all())
    class Meta:
        model = User
        fields = ['id', 'username', 'article']
# <form action={% url 'lview' %}  method='GET'>
#  <button type='submit' name="{{ object.id }}"> answer </button>
# </form>
#     <p><a href='{% url 'ans'%}'>Answer</a></p>


class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = answered
        fields = ['name','question','answer']

class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = article
        fields = ['title']