from django.urls import path

from . import views

app_name = 'v1'
urlpatterns = [
    path('page/create/', views.PageCreateView.as_view(), name='create-page'),
    path('report/create/', views.ReportCreateView.as_view(), name='create-report'),
]
