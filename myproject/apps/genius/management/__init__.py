from django.core.management import CommandError

try:
    from .commands import Command
except ImportError:
    raise CommandError('Error importing command')

__all__ = ['Command']