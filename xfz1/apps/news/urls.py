from django.urls import path
from .import views

app_name = 'news'

urlpatterns = [
    path('<int:news_id>/', views.NewsDetailView.as_view(), name='news_detail'),
    path('list/', views.NewsListView.as_view(), name='news_list'),
    path('public_comment/', views.PublicCommentView.as_view(), name='comment')
]