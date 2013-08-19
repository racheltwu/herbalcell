from os import path

from django.conf import settings
from django import template

from herbalcell.utils import get_exif_title, get_files


register = template.Library()

@register.inclusion_tag('fragments/gallery.html', takes_context=True)
def gallery(context, dir):
    gallery_path = path.join('galleries', dir)
    images = get_files(path.join(settings.STATIC_ROOT, 'images', gallery_path))
    images = [path.join(gallery_path, path.basename(i)) for i in images]
    images.sort()
    context.update({'images': images, 'gallery': dir})
    return context


@register.inclusion_tag('fragments/fancybox.html', takes_context=True)
def fancybox(context, image_path, title='', group='', image_class='float-right'):
    image_path = path.join('singles', image_path) if path.basename(image_path) == image_path else image_path
    thumb_path = path.join(path.dirname(image_path), 'thumbs', '%s.jpg' % path.splitext(path.basename(image_path))[0])
    image_url = path.join(settings.STATIC_URL, 'images', image_path)
    thumb_url = path.join(settings.STATIC_URL, 'images', thumb_path)
    title = title or get_exif_title(path.join(settings.STATIC_ROOT, 'images', image_path))
    context.update({'image_url': image_url, 'thumb_url': thumb_url, 'title': title, 'group': group, 'image_class': image_class})
    return context