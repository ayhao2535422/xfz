from django.shortcuts import render
from django.views.generic import View
from .models import PayInfo
from apps.news.models import News
from apps.course.models import Course
from utils import restful


class AboutMeView(View):
    def get(self, request):
        hotNewses = News.objects.filter(category__name='热点')
        course = Course.objects.filter(price=0).first()
        context = {
            'hotNewses': hotNewses,
            'course': course
        }
        return render(request, 'aboutme/aboutme.html', context=context)


from rest_framework import serializers
from apps.course.models import Course
class AboutSerializers(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ['id', 'title', 'price', 'pub_time']
class TestView(View):
    def get(self, request):
        data = Course.objects.values()
        serializer = AboutSerializers(data, many=True)
        data = serializer.data
        # return restful.result(data=data)
        context = {'data': data}
        return render(request, 'cms/111.html', context=context)