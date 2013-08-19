from os import path
from glob import glob

from django.core.management.base import BaseCommand
from mutagen.easyid3 import EasyID3

from django.conf import settings
from herbalcell.models import Song, Soundtrack
from herbalcell.utils import title_to_filename, zip


class Command(BaseCommand):
    help = 'Indexes soundtracks directory.'
    def handle(self, *args, **options):

        soundtracks = (
            'Legend of Zelda: Skyward Sword',
            'Legend of Zelda: Twilight Princess',
            'Legend of Zelda: Wind Waker',
            'Legend of Zelda: Majora\'s Mask',
            'Legend of Zelda: Majora\'s Mask Orchestrated',
            'Legend of Zelda: Ocarina of Time',
            'Legend of Zelda: Ocarina of Time Orchestrated',
            'Legend of Zelda: Ocarina of Time Rearranged',
            'Super Mario Galaxy',
            'Super Mario 64',
            'Earthbound',
            'Grim Fandango',
            'Katamari Damacy',
        )

        Soundtrack.objects.all().delete()

        for title in soundtracks:

            filename = title_to_filename(title)
            soundtrack_path = path.join(settings.STATIC_ROOT, 'soundtracks', filename)
            soundtrack = Soundtrack(title=title, filename=filename)
            soundtrack.save()
            for song in glob(path.join(soundtrack_path, '*.mp3')):
                song_url = path.join(settings.STATIC_URL, 'soundtracks', soundtrack.filename, path.basename(song))
                title = EasyID3(song)['title'][0]
                Song(url=song_url, title=title, soundtrack=soundtrack).save()
            zip_filename = path.join(soundtrack_path, 'all.zip')
            zip_files = glob(path.join(soundtrack_path, '*.mp3'))
            zip(zip_filename, zip_files)