from django import forms
from apps.xfzauth.forms import BaseForm
from .models import Teacher, CourseCategory, Course


class EditCourseCategoryForm(BaseForm):
    pk = forms.IntegerField()
    name = forms.CharField(max_length=100)


class DelCourseCategoryForm(BaseForm):
    pk = forms.IntegerField()


class PublishCourseForm(forms.ModelForm, BaseForm):
    category = forms.IntegerField()
    teacher = forms.IntegerField()

    class Meta:
        model = Course
        exclude = ['category', 'teacher']


class AddTeacherForm(forms.ModelForm, BaseForm):

    class Meta:
        model = Teacher
        fields = '__all__'