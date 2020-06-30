from rest_framework import serializers
from .models import Course, CourseCategory, Teacher


class TeacherSerializers(serializers.ModelSerializer):
    class Meta:
        model = Teacher
        fields = ['id', 'username']


class CourseCategorySerializers(serializers.ModelSerializer):
    class Meta:
        model = CourseCategory
        fields = ['id', 'name']


class CourseSerializers(serializers.ModelSerializer):
    category = CourseCategorySerializers()
    teacher = TeacherSerializers()

    class Meta:
        model = Course
        fields = ['id', 'title', 'video_url', 'cover_url', 'price', 'pub_time', 'category', 'teacher', 'profile', 'duration']