import logging
import requests
from django.db.models.signals import post_save
from django.dispatch import receiver, Signal
from django.core.mail import send_mail
from .models import Action

API_URL = 'https://api.telegram.org/bot'
BOT_TOKEN = '5891854704:AAFHSndInSqJHP8Wam9wSOVUDFVkHbA2j5I'
chat_id = 545106374

@receiver(post_save, sender=Action)
def send_action_notification(created, instance, **kwargs):
    if created:
        text = f'Кто-то создал дело №{instance.id}'
        requests.get(f'{API_URL}{BOT_TOKEN}/sendMessage?chat_id={chat_id}&text={text}')

