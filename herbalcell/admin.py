from django.contrib import admin
from herbalcell.models import Article


class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'filename', 'created_on', 'views', 'is_static')


admin.site.register(Article, ArticleAdmin)