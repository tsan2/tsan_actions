from rest_framework import serializers
from .models import Action, User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

class ActionSerializer(serializers.ModelSerializer):
    user_action = UserSerializer(many=True, read_only=True)

    class Meta:
        model = Action
        fields = '__all__'


