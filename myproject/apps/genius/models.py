import datetime

import jwt
from django.contrib.auth import get_user_model
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.db.models import ForeignKey, ManyToManyField


class ActionType(models.TextChoices):
    '''type action'''

    WORK = 'work'
    REST = 'rest'


class MyUserManager(BaseUserManager):
    def create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)

class MyUser(AbstractBaseUser, PermissionsMixin):
    name = models.CharField(max_length=15)
    email = models.EmailField(unique=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    objects = MyUserManager()

    def __str__(self):
        return self.email

User = get_user_model()

class Action(models.Model):
    # id = models.IntegerField(verbose_name='id', primary_key=True, auto_created=True)
    type_action = models.CharField(choices=ActionType.choices, max_length=255, default=ActionType.WORK, verbose_name='type_action')
    name = models.TextField(verbose_name='name', db_index=True)
    description = models.TextField(blank=True, null=False, verbose_name='description')
    time = models.TimeField(verbose_name='time')
    date = models.DateField(verbose_name='date')
    user = models.ManyToManyField(User, null=True)

    class Meta:
        db_table = 'Action'
        verbose_name = "Action"
        verbose_name_plural = "Actions"

    def __str__(self):
        return f'{self.name}'

    # @property
    # def token(self):
    #     return self._generate_jwt_token()
    #
    # def _generate_jwt_token(self):
    #     """
    #     Генерирует веб-токен JSON, в котором хранится идентификатор этого
    #     пользователя, срок действия токена составляет 1 день от создания
    #     """
    #     dt = datetime.now() + datetime.timedelta(days=1)
    #
    #     token = jwt.encode({
    #         'id': self.pk,
    #         'exp': int(dt.strftime('%s'))
    #     }, settings.SECRET_KEY, algorithm='HS256')
    #
    #     return token.decode('utf-8')

# qs_date_now = Action.objects.filter(date=str(datetime.date.today())).order_by('-id')

