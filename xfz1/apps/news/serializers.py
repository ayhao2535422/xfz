from rest_framework import serializers
from .models import News, NewsCategory, Comment, Banner
from apps.xfzauth.serialisers import UserSerializers


class NewsCategorySerializers(serializers.ModelSerializer):
    class Meta:
        model = NewsCategory
        fields = ['id', 'name']


class NewsSerializers(serializers.ModelSerializer):
    category = NewsCategorySerializers()
    author = UserSerializers()

    class Meta:
        model = News
        fields = ['id', 'title', 'desc', 'thumbnail', 'pub_time', 'author', 'category']


class CommentSerializers(serializers.ModelSerializer):
    author = UserSerializers()

    class Meta:
        model = Comment
        fields = ['id', 'content', 'pub_time', 'author']


class BannerListSerializers(serializers.ModelSerializer):
    class Meta:
        model = Banner
        fields = ['id', 'priority', 'image_url', 'link_to']