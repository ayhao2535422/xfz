from django.urls import path
from . import views, course_view, staff_views

app_name = 'cms'

urlpatterns = [
    path('index/', views.IndexView.as_view(), name='cms_index'),
    path('publish/', views.PublishNewsView.as_view(), name='cms_publish'),
    path('edit_news/', views.EditNewsView.as_view(), name='cms_edit_news'),
    path('category/', views.NewsCategoryView.as_view(), name='cms_news_category'),
    path('add_category/', views.AddNewsCategoryView.as_view(), name='cms_add_category'),
    path('edit_category/', views.EditNewsCategoryView.as_view(), name='cms_edit_category'),
    path('delete_news/', views.DeleteNewsView.as_view(), name='cms_delete_news'),
    path('del_category/', views.DelNewsCategoryView.as_view(), name='cms_del_category'),
    path('banners/', views.BannersView.as_view(), name='cms_banners'),
    path('add_banner/', views.AddBannerView.as_view(), name='cms_add_banner'),
    path('banner_list/', views.BannerListView.as_view(), name='cms_banner_list'),
    path('del_banner/', views.DelBannerView.as_view(), name='cms_del_banner'),
    path('edit_banner/', views.EditBannerView.as_view(), name='cms_edit_banner'),
    path('news_list/', views.NewsListView.as_view(), name='cms_news_list'),
    path('upload_file/', views.UploadFileView.as_view(), name='cms_upload_file'),
    path('qiniutoken/', views.QiniuTokenView.as_view(), name='cms_qiniutoken'),
]

urlpatterns += [
    path('course_list/', course_view.CourseListView.as_view(), name='cms_course_list'),
    path('course_category/', course_view.CourseCategoryView.as_view(), name='cms_course_category'),
    path('add_course_category/', course_view.AddCourseCategoryView.as_view(), name='cms_add_course_category'),
    path('edit_course_category/', course_view.EditCourseCategoryView.as_view(), name='cms_edit_course_category'),
    path('del_course_category/', course_view.DelCourseCategoryView.as_view(), name='cms_del_course_category'),
    path('publish_course/', course_view.PublishCourseView.as_view(), name='cms_publish_course'),
    path('edit_course/', course_view.EditCourseView.as_view(), name='cms_edit_course'),
    path('add_teacher/', course_view.AddTeacherView.as_view(), name='cms_add_teacher'),
]

urlpatterns += [
    path('staffs/', staff_views.StaffView.as_view(), name='cms_staff'),
    path('add_staff/', staff_views.AddStaffView.as_view(), name='cms_add_staff'),
]