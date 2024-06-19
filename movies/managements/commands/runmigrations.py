from django.core.management import call_command
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = 'Run migrations'

    def handle(self, *args, **kwargs):
        call_command('migrate')
