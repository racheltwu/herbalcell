from django.core.management.base import BaseCommand
from django.core.cache import get_cache


class Command(BaseCommand):
    help = 'Clears the cache.'
    def handle(self, *args, **options):
        get_cache('default').clear()