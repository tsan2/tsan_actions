import logging

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from .models import Action




@receiver(post_save)
def send_action_notification(sender, instance, created, **kwargs):
    logging.info("1.")
    if created:
        logging.info("2")
        send_mail('Новое дело',
                  f'Кто-то создал дело №{instance.id}',
                  'tsan_actions@lamba.gk',
                  ['nastabutcher.myasn@gmail.com'],
                  fail_silently=False)
