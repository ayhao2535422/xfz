from django.urls import path
from . import views

app_name = 'aboutme'

urlpatterns = [
    path('', views.AboutMeView.as_view(), name='aboutme'),
    path('test/', views.TestView.as_view(), name='test')
]