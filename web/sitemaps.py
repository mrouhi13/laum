from django.contrib.sitemaps import Sitemap
from django.urls import reverse

from .models import Page


class PageSitemap(Sitemap):
    changefreq = 'daily'
    priority = 0.9
    protocol = 'https'

    def items(self):
        return Page.objects.filter(is_active=True)

    @staticmethod
    def lastmod(obj):
        return obj.updated_on

    def location(self, obj):
        return '/{}/'.format(obj.pid)


class StaticViewSitemap(Sitemap):
    priority = 0.5
    changefreq = 'daily'
    protocol = 'https'

    def items(self):
        return ['web:index', 'web:page-list']

    def location(self, item):
        return reverse(item)
