from django.contrib.auth import get_user_model
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.db import models



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
    balance = models.FloatField(default=0)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    objects = MyUserManager()

    def __str__(self):
        return self.email


User = get_user_model()

class Task(models.Model):
    name = models.TextField(verbose_name='name', db_index=True)
    description = models.TextField(blank=True, null=False, verbose_name='description')
    time = models.TimeField(verbose_name='time')
    date = models.DateField(verbose_name='date')
    price = models.FloatField(verbose_name='price')
    userFor = models.ManyToManyField(User, related_name='userFor', null=True)
    userFrom = models.ManyToManyField(User, related_name='userFrom', null=True)
    userFor_id = models.IntegerField(verbose_name='userFor_id')
    done = models.BooleanField(verbose_name='done', default=False)


    class Meta:
        db_table = 'Task'
        verbose_name = "Task"
        verbose_name_plural = "Tasks"

    def __str__(self):
        return f'{self.name}'

