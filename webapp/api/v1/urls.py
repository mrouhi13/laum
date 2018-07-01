from django.urls import path

from . import views

app_name = 'api.v1'

urlpatterns = [
    path('data/create/', views.DataCreateView.as_view(), name='create-data'),
]
