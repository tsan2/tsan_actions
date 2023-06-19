from django.apps import AppConfig

class GeniusConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'myproject.apps.genius'
    verbose_name = 'Actions from tsan'

    def ready(self):
        from . import signals

