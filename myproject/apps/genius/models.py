import datetime

from django.db import models


class ActionType(models.TextChoices):
    '''type action'''

    WORK = 'work'
    REST = 'rest'

class ActionManager(models.Manager):
    def Action(self):
        return self



class Action(models.Model):
    type_action = models.CharField(choices=ActionType.choices, max_length=255, default=ActionType.WORK, verbose_name='type_action')
    name = models.TextField(verbose_name='name', db_index=True)
    description = models.TextField(blank=True, null=False, verbose_name='description')
    time = models.TimeField(verbose_name='time')
    date = models.DateField(verbose_name='date')

    objects = ActionManager()

    class Meta:
        db_table = 'Action'
        verbose_name = "Action"
        verbose_name_plural = "Actions"

    def __str__(self):
        return f'{self.name}'

qs_date_now = Action.objects.filter(date=datetime.date).order_by('-id')

