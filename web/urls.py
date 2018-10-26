from django.conf import settings
from django.conf.urls.static import static
from django.urls.conf import path

from . import views

app_name = 'web'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('search/', views.PageListView.as_view(), name='page-list'),
    path('<str:slug>/', views.PageDetailView.as_view(), name='page-detail'),
    path('page/create/', views.PageCreateView.as_view(), name='page-create'),
    path('report/create/', views.ReportCreateView.as_view(), name='report-create'),
]

# This is only needed when using runserver.
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
