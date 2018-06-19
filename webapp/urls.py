from django.urls.conf import path

from . import views

app_name = 'webapp'
urlpatterns = [
    path('', views.DataListView.as_view(), name='list'),
    path('<int:pk>/', views.DataDetailView.as_view(), name='detail'),
]
