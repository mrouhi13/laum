from django.conf import settings
from django.conf.urls.static import static
from django.urls.conf import path, include

from . import views

app_name = 'web_app'
urlpatterns = [
                  path('', views.index, name='index'),
                  path('search/', views.DataListView.as_view(), name='list'),
                  path('<str:slug>/', views.DataDetailView.as_view(), name='detail'),

                  # API
                  path('web_app/v1/', include('web_app.api.v1.urls', namespace='default')),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
