from django.conf import settings
from django.conf.urls.static import static
from django.urls.conf import path

from . import views

app_name = 'webapp'
urlpatterns = [
                  path('', views.index, name='index'),
                  path('search/', views.DataListView.as_view(), name='list'),
                  path('<int:pk>/', views.DataDetailView.as_view(), name='detail'),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
