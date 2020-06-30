from django.urls import path
from . import views

app_name = 'course'

urlpatterns = [
    path('', views.CourseIndexView.as_view(), name='course_index'),
    path('course_list/', views.CourseListView.as_view(), name='course_list'),
    path('<int:course_id>/', views.CourseDetailView.as_view(), name='course_detail'),
    path('course_token/', views.CourseTokenView.as_view(), name='course_token'),
    path('course_order/<int:course_id>/', views.CourseOrderView.as_view(), name='course_order'),
]