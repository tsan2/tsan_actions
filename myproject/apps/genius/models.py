import datetime

from django.db import models
from django.db.models import ForeignKey, ManyToManyField


class ActionType(models.TextChoices):
    '''type action'''

    WORK = 'work'
    REST = 'rest'

class ActionManager(models.Manager):
    def Action(self):
        return self

class User(models.Model):
    id = models.IntegerField(verbose_name='id', primary_key=True, null=False)
    name = models.TextField(verbose_name='name', max_length=15, db_index=True, null=False)
    email = models.EmailField(verbose_name='email', null=False)
    password = models.TextField(verbose_name='password', null=False)

    class Meta:
        db_table = 'User'
        verbose_name = "User"
        verbose_name_plural = "Users"


class Action(models.Model):
    id = models.IntegerField(verbose_name='id', primary_key=True, null=False)
    type_action = models.CharField(choices=ActionType.choices, max_length=255, default=ActionType.WORK, verbose_name='type_action')
    name = models.TextField(verbose_name='name', db_index=True)
    description = models.TextField(blank=True, null=False, verbose_name='description')
    time = models.TimeField(verbose_name='time')
    date = models.DateField(verbose_name='date')
    user_action = models.ManyToManyField('User', null=True)

    object = ActionManager()

    class Meta:
        db_table = 'Action'
        verbose_name = "Action"
        verbose_name_plural = "Actions"

    def __str__(self):
        return f'{self.name}'

# qs_date_now = Action.objects.filter(date=str(datetime.date.today())).order_by('-id')

