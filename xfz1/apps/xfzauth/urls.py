from django.urls import path
from . import views

app_name = 'xfzauth'

urlpatterns = [
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('register/', views.RegisterView.as_view(), name='register'),
    path('captcha/', views.ImgCaptchaView.as_view(), name='img_captcha'),
    path('sms_captcha/', views.SmsCaptchaView.as_view(), name='sms_captcha'),
]