from django.core.management.base import BaseCommand
from django.core import management


class Command(BaseCommand):
    help = 'Runs all update scripts.'
    def handle(self, *args, **options):
        management.call_command('update-blog')
        management.call_command('update-sheets')
        management.call_command('update-soundtracks')
        management.call_command('update-wallpapers')