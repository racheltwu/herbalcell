from os import path
from glob import glob

from django.core.management.base import BaseCommand
from django.conf import settings

from herbalcell.models import Wallpaper, WallpaperGroup
from herbalcell.utils import create_thumbnails, zip


class Command(BaseCommand):
    help = 'Indexes wallpapers directory.'
    def handle(self, *args, **options):

        WallpaperGroup.objects.all().delete()

        group_paths = glob(path.join(settings.STATIC_ROOT, 'images', 'wallpapers', '*'))
        for group_path in group_paths:
            group = WallpaperGroup(
                filename = path.basename(group_path),
                title = open(path.join(group_path, 'title.txt'), 'r').read()
            )
            group.save()
            wallpapers = glob(path.join(group_path, '*.jpg'))
            for wallpaper in wallpapers:
                Wallpaper(
                    filename = path.basename(wallpaper),
                    group = group
                ).save()
            create_thumbnails(path.join('wallpapers', group.filename), 150, 100)
            zip(path.join(group_path, 'all.zip'), wallpapers)