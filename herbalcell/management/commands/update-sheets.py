from os import path

from django.core.management.base import BaseCommand
from django.conf import settings

from herbalcell.models import Sheet, SheetGroup
from herbalcell.utils import title_to_filename, zip


class Command(BaseCommand):
    help = 'Indexes sheets directory.'
    def handle(self, *args, **options):

        SheetGroup.objects.all().delete()

        groups = open(path.join(settings.TEMPLATE_DIRS[0], 'lists', 'sheets.txt'), 'r').read().split('\n\n\n')
        for group in groups:
            sheets = group.split('\n')
            group = SheetGroup(
                title = sheets[0],
                filename = title_to_filename(sheets[0])
            )
            group.save()
            group_path = path.join(settings.STATIC_ROOT, 'sheets', group.filename)
            sheets = sheets[2:]
            zips = {
                'sheets-classic': ([], '.pdf'),
                'sheets-labeled': ([], '-labels.pdf'),
                'midis': ([], '.mid'),
                'mp3s': ([], '.mp3'),
            }
            for sheet in sheets:
                title = sheet[:-4]
                filename = title_to_filename(title)
                Sheet(
                    title = title,
                    url = path.join(group.url, filename),
                    group = group,
                    rating = sheet[-1:]
                ).save()
                filepath = path.join(group_path, filename)
                for zip_group in zips:
                    zips[zip_group][0].append('%s%s' % (filepath, zips[zip_group][1]))

            if len(sheets) > 1:
                for zip_group in zips:
                    zip_filename = '%s.zip' % path.join(group_path, zip_group)
                    zip(zip_filename, zips[zip_group][0])