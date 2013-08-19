from glob import glob
from os import path
import re
import datetime
import httplib2
from apiclient.discovery import build
from oauth2client.client import SignedJwtAssertionCredentials

from django.core.management.base import BaseCommand
from django.conf import settings

from herbalcell.models import Article
from herbalcell.utils import create_thumbnails, get_dirs


TITLE_CHANGES = { # new: (old, old2, old3)
    'games-i-like': ['my-favorite-video-games'],
}


class Command(BaseCommand):
    help = 'Updates database after modifying templates directory.'
    def handle(self, *args, **options):

        Article.objects.all().delete()

        articles = glob(path.join(settings.TEMPLATE_DIRS[0], 'articles', '*.html'))
        for article in articles:
            path_prefix, filename = path.split(article)
            filename = re.sub('.html', '', filename)
            file_contents = open(article, 'r').read()
            date = re.search('{% block date %}(.*?){% endblock %}', file_contents)
            date = datetime.datetime.strptime(date.group(1), '%Y-%m-%d') if date else None
            Article(
                filename = filename,
                created_on = date if date else datetime.datetime(1990,1,1),
                title = re.search('{% block title %}(.*?){% endblock %}', file_contents).group(1),
                views = get_view_count_from_google_analytics(filename),
                is_static = True if not date else False
            ).save()

        create_thumbnails('singles', 200, 900)
        for gallery in get_dirs(path.join(settings.STATIC_ROOT, 'images', 'galleries')):
            create_thumbnails(path.join('galleries', path.basename(gallery)), 900, 250)


def get_view_count_from_google_analytics(filename):
    credentials = SignedJwtAssertionCredentials(
        '###@developer.gserviceaccount.com',
        file(keypath, 'rb').read(),
        scope='https://www.googleapis.com/auth/analytics.readonly'
    )
    pages = build('analytics', 'v3', http=credentials.authorize(httplib2.Http())).data().ga().get(
        ids = '###',
        start_date = (datetime.date.today() - datetime.timedelta(30)).isoformat(), # 30 days ago
        end_date = datetime.date.today().isoformat(),
        metrics = 'ga:uniquePageviews',
        dimensions = 'ga:pagePath',
        filters = 'ga:pagePath=~^/blog/[^/?]+$',
    ).execute().get('rows')
    view_counts = {}
    for page in pages:
        view_counts[re.sub('/blog/', '', page[0])] = int(page[1])
    views = view_counts.get(filename, 0)
    if filename in TITLE_CHANGES:
        for alternate_name in TITLE_CHANGES[filename]:
            views += view_counts.get(alternate_name, 0)
    return views