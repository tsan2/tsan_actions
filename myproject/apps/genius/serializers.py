from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from .models import Action, MyUser, ActionType, User


class UserSerializer2(serializers.ModelSerializer):
    class Meta:
        model = MyUser
        fields = '__all__'

class UserSerializer(serializers.Serializer):
    name = serializers.CharField()
    email = serializers.EmailField()
    password = serializers.CharField()


    def create(self, **validated_data):
        validated_data['last_login'] = None
        validated_data['is_superuser'] = False
        validated_data['is_staff'] = False
        validated_data['is_active'] = False
        validated_data['user_permissions'] = [0]
        validated_data['groups'] = [0]
        validated_data['last_login'] = None
        return User.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.email = validated_data.get('email', instance.email)
        instance.name = validated_data.get('name', instance.name)
        instance.password = validated_data.get('password', instance.password)
        instance.save()
        return instance

class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    def create(self, **validated_data):
        pass

    def update(self, instance, validated_data):
        pass

class UserSerializerMini(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()
    email = serializers.EmailField()
    is_superuser = serializers.BooleanField()
    is_staff = serializers.BooleanField()
    is_active = serializers.BooleanField

    def create(self, **validated_data):
        pass

    def update(self, instance, validated_data):
        pass

class ActionSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    type_action = serializers.CharField(max_length=255)
    name = serializers.CharField()
    description = serializers.CharField()
    time = serializers.TimeField()
    date = serializers.DateField()


    def create(self, validated_data):
        return Action.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.type_action = validated_data.get('type_action', instance.type_action)
        instance.name = validated_data.get('name', instance.name)
        instance.description = validated_data.get('description', instance.description)
        instance.time = validated_data.get('time', instance.time)
        instance.date = validated_data.get('date', instance.date)
        instance.save()
        return instance

    # user = serializers.ManyToManyField(User, null=True)
    # user_action = UserSerializer(many=True, read_only=True)
    #
    # class Meta:
    #     model = Action
    #     fields = '__all__'

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        token['email'] = user.email
        token['name'] = user.name

        return token

