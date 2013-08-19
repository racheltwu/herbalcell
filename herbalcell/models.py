from os import path
from datetime import datetime

from django.db import models
from django.conf import settings


class Article(models.Model):
    filename = models.CharField(max_length=255, unique=True)
    title = models.CharField(max_length=300)
    created_on = models.DateTimeField(default=datetime.now())
    views = models.IntegerField(default=0)
    is_static = models.BooleanField(default=False)
    class Meta:
        ordering = ['created_on']

#---------------------------------------------


RATINGS = (
    ('e', 'easy'),
    ('m', 'medium'),
    ('d', 'difficult'),
    ('n', 'not rated yet'),
)

class SheetGroup(models.Model):
    filename = models.CharField(max_length=300)
    title = models.CharField(max_length=300)
    class Meta:
        ordering = ['id']
    @property
    def count(self):
        return Sheet.objects.filter(group=self).count()
    @property
    def url(self):
        return path.join(settings.STATIC_URL, 'sheets', self.filename)

class Sheet(models.Model):
    url = models.CharField(max_length=300)
    title = models.CharField(max_length=300)
    group = models.ForeignKey(SheetGroup)
    rating = models.CharField(max_length=300, choices=RATINGS)
    class Meta:
        ordering = ['id']

#---------------------------------------------

class Soundtrack(models.Model):
    filename = models.CharField(max_length=300)
    title = models.CharField(max_length=300)
    class Meta:
        ordering = ['id']

class Song(models.Model):
    url = models.CharField(max_length=300)
    title = models.CharField(max_length=300)
    soundtrack = models.ForeignKey(Soundtrack)
    class Meta:
        ordering = ['id']

#---------------------------------------------

class WallpaperGroup(models.Model):
    filename = models.CharField(max_length=300)
    title = models.CharField(max_length=300)
    class Meta:
        ordering = ['id']

class Wallpaper(models.Model):
    filename = models.CharField(max_length=300)
    group = models.ForeignKey(WallpaperGroup)
    class Meta:
        ordering = ['id']