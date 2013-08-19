from django.conf.urls import *
from django.contrib import admin
from django.views.generic.base import RedirectView, TemplateView

from herbalcell.views import UpdatesFeed

admin.autodiscover()

urlpatterns = patterns('',
    (r'^admin/?', include(admin.site.urls)),
    (r'^errors/?$', 'prettylog.views.error_log', {}, 'errors'),
    (r'^blog/?(?P<article>.*)$', RedirectView.as_view(url='/%(article)s')),
    (r'^about-me/?$', TemplateView.as_view(template_name='about_me.html'), {}, 'about_me'),
    (r'^feed/?$', UpdatesFeed(), {}, 'feed'),
    (r'^feed.xml$', RedirectView.as_view(url='/feed')),
    (r'^validation', include('django_w3c_validator.urls')),
)

urlpatterns += patterns('herbalcell.views',
    (r'^$', 'blog', {}, 'blog'),
    (r'^free-sheet-music/(?P<subgroup>.*?)/?$', 'blog', {'article_filename': 'free-sheet-music'}, 'sheet'),
    (r'^video-game-soundtracks/(?P<subgroup>.*?)/?$', 'blog', {'article_filename': 'video-game-soundtracks'}, 'soundtrack'),
    (r'^zelda-wallpapers/(?P<subgroup>.*?)/?$', 'blog', {'article_filename': 'zelda-wallpapers'}, 'wallpaper'),
    (r'^(?P<article_filename>.*?)/?$', 'blog', {}, 'article'),
)

from django.contrib.staticfiles.urls import staticfiles_urlpatterns
urlpatterns += staticfiles_urlpatterns()