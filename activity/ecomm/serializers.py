from ecomm.models import UserPro, ClickCost, Owned, Amount_Payed
from rest_framework import serializers

class UserProSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserPro
        fields = ['user_name']

class ClickCostSerailizer(serializers.ModelSerializer):
    class Meta:
        model = ClickCost
        fields = ['user_id', 'clicks']

class OwnedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Owned
        fields = "__all__"

class AmountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Amount_Payed
        fields = "__all__"
