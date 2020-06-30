"""
Django settings for xfz1 project.

Generated by 'django-admin startproject' using Django 3.0.2.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""
# import pymysql
# pymysql.install_as_MySQLdb()

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'jr83evvao_*%zt3k%r)(wv*jtr@g6(p6!9id(p9uh@9%se2egj'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['127.0.0.1', '39.99.252.177', '172.26.115.40', '47.96.60.218']

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'apps.news',
    'apps.cms',
    'apps.xfzauth',
    'apps.course',
    'apps.ueditor',
    'apps.aboutme',
    'rest_framework',
    'debug_toolbar',
]

MIDDLEWARE = [
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'xfz1.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'front', 'templates')]
        ,
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
            'builtins':[
                'django.templatetags.static'
            ],
        },
    },
]

WSGI_APPLICATION = 'xfz1.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'xfz',
        'USER': 'root',
        'PASSWORD': 'root',
        'PORT': '3306',
        'HOST': '127.0.0.1',
    }
}


# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

AUTH_USER_MODEL = 'xfzauth.User'


# Internationalization
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/

STATIC_URL = '/static/'

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'front', 'dist')
]

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

MEDIA_URL = '/media/'

# 上传文件本地配置
UEDITOR_UPLOAD_TO_SERVER = True
UEDITOR_UPLOAD_PATH = MEDIA_ROOT
UEDITOR_CONFIG_PATH = os.path.join(BASE_DIR, 'front', 'dist', 'ueditor', 'config.json')

# 上传文件七牛云配置
# QINIU_ACCESS_KEY = 'lk3kyvW7iqNoOmXoiijbAlMeu1NWv0iCVnQBe1t4'
# QINIU_SECRET_KEY = '--NIcAmsg9A7waJmO3TIlGn1Sq8K8qKjMbt-Zb1S'
# QINIU_BUCKET_NAME = 'dhspace'
# QINIU_DOMAIN = 'http://qa7m1cg3t.bkt.clouddn.com/'
#
# UEDITOR_UPLOAD_TO_QINIU = True
# UEDITOR_QINIU_ACCESS_KEY = QINIU_ACCESS_KEY
# UEDITOR_QINIU_SECRET_KEY = QINIU_SECRET_KEY
# UEDITOR_QINIU_BUCKET_NAME = QINIU_BUCKET_NAME
# UEDITOR_QINIU_DOMAIN = QINIU_DOMAIN

ONE_PAGE_NEWS_COUNT = 2

INTERNAL_IPS = ['127.0.0.1']

DEBUG_TOOLBAR_PANELS = [
    # 代表是哪个django版本
    'debug_toolbar.panels.versions.VersionsPanel',
    # 用来计时的，判断加载当前页面总共花的时间
    'debug_toolbar.panels.timer.TimerPanel',
    # 读取django中的配置信息
    'debug_toolbar.panels.settings.SettingsPanel',
    # 看到当前请求头和响应头信息
    'debug_toolbar.panels.headers.HeadersPanel',
    # 当前请求的想信息（视图函数，Cookie信息，Session信息等）
    'debug_toolbar.panels.request.RequestPanel',
    # 查看SQL语句
    'debug_toolbar.panels.sql.SQLPanel',
    # 静态文件
    'debug_toolbar.panels.staticfiles.StaticFilesPanel',
    # 模板文件
    'debug_toolbar.panels.templates.TemplatesPanel',
    # 缓存
    'debug_toolbar.panels.cache.CachePanel',
    # 信号
    'debug_toolbar.panels.signals.SignalsPanel',
    # 日志
    'debug_toolbar.panels.logging.LoggingPanel',
    # 重定向
    'debug_toolbar.panels.redirects.RedirectsPanel',
]

DEBUG_TOOLBAR_CONGIF = {
    'JQUERY': ''
}

# 百度云的配置
# 控制台->用户中心->用户ID
BAIDU_CLOUD_USER_ID = '289716d1f0834ecdaff19e48aeffc0b6'
# 点播VOD->全局设置->发布设置->安全设置->UserKey
BAIDU_CLOUD_USER_KEY = '0588393038514844'