from os import path
from datetime import datetime
from time import strptime, mktime

from django.conf import settings
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404
from django.contrib.syndication.views import Feed
from annoying.decorators import render_to

from herbalcell.models import (Article, Sheet, SheetGroup,
                        Song, Soundtrack, Wallpaper, WallpaperGroup)
from herbalcell.utils import title_to_filename


def context_processor(request):
    # Must have this for error and non-article pages to have sidebar context
    articles = Article.objects.all()
    articles_by_date = Article.objects.all().order_by('-created_on', 'title')
    articles_by_popularity = articles.order_by('-views', '-created_on')
    return dict(
        articles_by_date = articles_by_date,
        articles_by_popularity = articles_by_popularity,
    )


@render_to()
def blog(request, article_filename=None, subgroup=None):
    articles_by_date = Article.objects.all().order_by('-created_on', 'title')
    article_count = articles_by_date.count()
    article = get_object_or_404(Article, filename=article_filename) if article_filename else articles_by_date[0]
    for i, a in enumerate(articles_by_date):
        if a == article:
            article.older_article = articles_by_date[i+1] if i + 1 < article_count else None
            article.newer_article = articles_by_date[i-1] if i > 0 else None
            article.index = i + 1
    context = {}
    if article_filename == 'free-sheet-music':
        context['sheet_groups'] = SheetGroup.objects.all()
        context['sheets'] = Sheet.objects.filter(group__filename=subgroup)
    if article_filename == 'video-game-soundtracks':
        context['soundtracks'] = Soundtrack.objects.all()
        context['songs'] = Song.objects.filter(soundtrack__filename=subgroup).order_by('url')
    if article_filename == 'zelda-wallpapers':
        context['wallpaper_groups'] = WallpaperGroup.objects.all()
        context['wallpapers'] = Wallpaper.objects.filter(group__filename=subgroup)
    if article_filename == 'my-piano-performances':
        context['performances'] = get_performances()
    if article_filename == 'games-i-like':
        context['games_i_like'] = get_games_i_like()
    return dict(context,
        article = article,
        TEMPLATE = 'articles/%s.html' % article.filename,
    )


def get_games_i_like():
    unprocessed_games = open(path.join(settings.TEMPLATE_DIRS[0], 'lists', 'games-i-like.txt'), 'r').read().split('\n\n')
    games = []
    for game in unprocessed_games:
        game = game.split('\n')
        amazon_link = game[3] if game[3].startswith('http') else ''
        filename = title_to_filename(game[0])
        games.append(dict(
            title = game[0],
            filename = 'seventh-guest' if filename == '7th-guest' else filename,
            platform = game[1],
            wikilink = game[2],
            amazon_link = amazon_link,
            amazon_image = game[4] if amazon_link else '',
            description = game[5:] if amazon_link else game[3:]
        ))
    return games


def get_performances():
    unprocessed_performances = open(path.join(settings.TEMPLATE_DIRS[0], 'lists', 'performances.txt'), 'r').read().split('\n\n')
    performances = []
    for performance in unprocessed_performances:
        performance = performance.split('\n')
        performances.append(dict(
            filename = performance[0],
            title = performance[1],
            video_url = performance[2] if len(performance) == 3 else '',
        ))
    return performances


class UpdatesFeed(Feed):
    unprocessed_feed_items = open(path.join(settings.TEMPLATE_DIRS[0], 'lists', 'feed.txt'), 'r').read().split('\n\n\n')
    feed_items = []
    for feed_item in unprocessed_feed_items:
        feed_item = feed_item.split('\n')
        feed_items.append(dict(
            date = datetime.fromtimestamp(mktime(strptime(feed_item[0], '%Y-%m-%d %I:%M %p'))),
            title = feed_item[1],
            description = ''.join(feed_item[2:])
        ))
    title = 'herbalcell updates'
    link = ''
    def items(self):
        return self.feed_items
    def item_title(self, item):
        return item['title']
    def item_description(self, item):
        return item['description']
    def item_pubdate(self, item):
        return item['date']
    def item_link(self, item):
        return 'http://herbalcell.com'
