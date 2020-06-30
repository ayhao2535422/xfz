from django.shortcuts import render
from django.views.generic import View
from .models import Course, CourseCategory, CourseOrder
from utils import restful
import time,hmac,os,hashlib
from django.conf import settings
from django.utils.decorators import method_decorator
from apps.xfzauth.decorators import xfz_login_required
from .serializers import CourseSerializers


class CourseIndexView(View):
    def get(self, request):
        course = Course.objects.select_related('teacher', 'category')

        context = {
            'courses': course,
            'categories': CourseCategory.objects.all()
        }
        return render(request, 'course/course_index.html', context=context)


class CourseListView(View):
    def get(self, request):
        category_id = request.GET.get('pk')
        courses = Course.objects.select_related('category', 'teacher').filter(category_id=category_id)
        serializers = CourseSerializers(courses, many=True)
        data = serializers.data
        return restful.result(data=data)


class CourseDetailView(View):
    def get(self, request, course_id):
        try:
            course = Course.objects.get(pk=course_id)
        except:
            return restful.params_errors(message='该课程不存在')
        context = {
            'course': course,
            'categories': CourseCategory.objects.all()
        }
        return render(request, 'course/course_detail.html', context=context)


class CourseTokenView(View):
    def get(self, request):
        # video：是视频文件的完整链接
        file = request.GET.get('video')

        expiration_time = int(time.time()) + 2 * 60 * 60

        USER_ID = settings.BAIDU_CLOUD_USER_ID
        USER_KEY = settings.BAIDU_CLOUD_USER_KEY

        # file=http://hemvpc6ui1kef2g0dd2.exp.bcevod.com/mda-igjsr8g7z7zqwnav/mda-igjsr8g7z7zqwnav.m3u8
        extension = os.path.splitext(file)[1]
        media_id = file.split('/')[-1].replace(extension, '')

        # unicode->bytes=unicode.encode('utf-8')bytes
        key = USER_KEY.encode('utf-8')
        message = '/{0}/{1}'.format(media_id, expiration_time).encode('utf-8')
        signature = hmac.new(key, message, digestmod=hashlib.sha256).hexdigest()
        token = '{0}_{1}_{2}'.format(signature, USER_ID, expiration_time)
        return restful.result(data={'token': token})


@method_decorator(xfz_login_required, name='dispatch')
class CourseOrderView(View):
    def get(self, request, course_id):
        try:
            course = Course.objects.get(pk=course_id)
        except:
            return restful.params_errors(message='该分类不存在')
        order = CourseOrder.objects.create(course=course, buyer=request.user, amount=course.price)
        context = {
            'course': course,
            'order': order
        }
        return render(request, 'course/course_order.html', context=context)
