from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from .models import Task, MyUser, User


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
        validated_data['balance'] = 0
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
    balance = serializers.FloatField()
    is_superuser = serializers.BooleanField()
    is_staff = serializers.BooleanField()
    is_active = serializers.BooleanField

    def create(self, **validated_data):
        pass

    def update(self, instance, validated_data):
        pass

class TaskSerializer(serializers.Serializer):
    userFor_id = serializers.IntegerField()
    # userFrom = UserSerializer(many=True, allow_null=True)
    name = serializers.CharField()
    description = serializers.CharField()
    price = serializers.FloatField()
    time = serializers.TimeField()
    date = serializers.DateField()


    def create(self, validated_data):
        return Task.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.userFor_id = validated_data.get('userFor_id', instance.userFor_id)
        instance.name = validated_data.get('name', instance.name)
        instance.description = validated_data.get('description', instance.description)
        instance.price = validated_data.get('price', instance.price)
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

class MegaTaskSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    userFrom = UserSerializerMini(many=True, allow_null=True)
    userFor = UserSerializerMini(many=True, allow_null=True)
    name = serializers.CharField()
    description = serializers.CharField()
    price = serializers.FloatField()
    time = serializers.TimeField()
    date = serializers.DateField()
    done = serializers.BooleanField()

    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass

class TaskSerializerMini(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()
    description = serializers.CharField()
    price = serializers.FloatField()
    time = serializers.TimeField()
    userFor_id = serializers.IntegerField()
    date = serializers.DateField()
    done = serializers.BooleanField()

    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        token['email'] = user.email
        token['name'] = user.name

        return token

