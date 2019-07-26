from django.conf import settings
from django.conf.urls.static import static
from django.contrib.sitemaps.views import sitemap
from django.urls.conf import path
from django.views.generic import TemplateView

from . import views
from .sitemaps import PageSitemap, StaticViewSitemap

sitemaps = {
    'pages': PageSitemap,
    'statics': StaticViewSitemap
}

app_name = 'web'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('search/', views.PageListView.as_view(), name='page-list'),
    path('<str:slug>/', views.PageDetailView.as_view(), name='page-detail'),
    path('page/create/', views.PageCreateView.as_view(), name='page-create'),
    path('report/create/', views.ReportCreateView.as_view(), name='report-create'),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='sitemap'),
    path('robots.txt', TemplateView.as_view(template_name='web/robots.txt',
                                            content_type='text/plain')),
]

# This is only needed when using runserver.
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
