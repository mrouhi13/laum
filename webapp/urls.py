from django.conf import settings
from django.conf.urls.static import static
from django.urls.conf import path, include

from . import views

app_name = 'webapp'
urlpatterns = [
                  path('', views.index, name='index'),
                  path('search/', views.DataListView.as_view(), name='list'),
                  path('<str:slug>/', views.DataDetailView.as_view(), name='detail'),

                  # API
                  path('webapp/v1/', include('webapp.api.v1.urls', namespace='default')),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
