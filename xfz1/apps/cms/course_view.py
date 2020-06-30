from django.views import View
from django.shortcuts import render
from apps.course.models import CourseCategory, Course, Teacher
from utils import restful
from apps.course.forms import AddTeacherForm, EditCourseCategoryForm, DelCourseCategoryForm, PublishCourseForm
from django.utils.timezone import make_aware
from datetime import datetime
from django.core.paginator import Paginator
from urllib import parse


class CourseCategoryView(View):
    def get(self, request):
        context = {
            'categories': CourseCategory.objects.all()
        }
        return render(request, 'cms/course_category.html', context=context)


class AddCourseCategoryView(View):
    def post(self, request):
        category = request.POST.get('category')
        exists = CourseCategory.objects.filter(name=category).exists()
        if exists:
            return restful.params_errors(message='该分类已存在')
        else:
            CourseCategory.objects.create(name=category)
        return restful.ok()


class EditCourseCategoryView(View):
    def post(self, request):
        form = EditCourseCategoryForm(request.POST)
        if form.is_valid():
            pk = form.cleaned_data.get('pk')
            name = form.cleaned_data.get('name')
            CourseCategory.objects.filter(pk=pk).update(name=name)
            return restful.ok()
        else:
            return restful.params_errors(message=form.get_errors())


class DelCourseCategoryView(View):
    def post(self, request):
        form = DelCourseCategoryForm(request.POST)
        if form.is_valid():
            pk = form.cleaned_data.get('pk')
            try:
                CourseCategory.objects.filter(pk=pk).delete()
                return restful.ok()
            except:
                return restful.params_errors(message='该分类不存在')
        else:
            return restful.params_errors(message=form.get_errors())


class CourseListView(View):
    def get(self, request):
        page = request.GET.get('p', 1)
        start = request.GET.get('start')
        end = request.GET.get('end')
        title = request.GET.get('title')
        category_id = int(request.GET.get('category', 0) or 0)

        courses = Course.objects.select_related('category', 'teacher')

        if start or end:
            if start:
                start_date = datetime.strptime(start, '%Y/%m/%d')
            else:
                start_date = datetime(year=2020, month=1, day=1)
            if end:
                end_date = datetime.strptime(end, '%Y/%m/%d')
            else:
                end_date = datetime.today()
            courses = courses.filter(pub_time__range=(make_aware(start_date), make_aware(end_date)))

        if title:
            courses = courses.filter(title__icontains=title)

        if category_id:
            courses = courses.filter(category=category_id)

        paginator = Paginator(courses, 2)
        page_obj = paginator.page(page)
        context = {
            'courses': courses,
            'categories': CourseCategory.objects.all(),
            'paginator': paginator,
            'page_obj': page_obj,
            'start': start,
            'end': end,
            'title': title,
            'url_query': '&' + parse.urlencode({
                'start': start or '',
                'end': end or '',
                'title': title or '',
                'category': category_id or ''
            })
        }
        pagination_data = self.get_pagination_data(paginator, page_obj)
        context.update(pagination_data)
        return render(request, 'cms/course_list.html', context=context)

    def get_pagination_data(self, paginator, page_obj, around_number=2):
        current_page = page_obj.number
        left_has_more = False
        right_has_more = False

        if current_page <= around_number + 2:
            left_pages = range(1, current_page)
        else:
            left_has_more = True
            left_pages = range(current_page - around_number, current_page)
        if current_page >= paginator.num_pages - around_number - 1:
            right_pages = range(current_page + 1, paginator.num_pages + 1)
        else:
            right_has_more = True
            right_pages = range(current_page + 1, current_page + around_number + 1)
        return {
            'current_page': current_page,
            'left_has_more': left_has_more,
            'right_has_more': right_has_more,
            'left_pages': left_pages,
            'right_pages': right_pages,
        }


class EditCourseView(View):
    def get(self, request):
        course_id = request.GET.get('course_id')
        course = Course.objects.get(pk=course_id)
        context = {
            'course': course,
            'categories': CourseCategory.objects.all()
        }
        return render(request, 'cms/publish_course.html', context=context)


class PublishCourseView(View):
    def get(self, request):
        context = {
            'categories': CourseCategory.objects.all(),
            'teachers': Teacher.objects.all()
        }
        return render(request, 'cms/publish_course.html', context=context)

    def post(self, request):
        form = PublishCourseForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data.get('title')
            video_url = form.cleaned_data.get('video_url')
            cover_url = form.cleaned_data.get('cover_url')
            price = form.cleaned_data.get('price')
            duration = form.cleaned_data.get('duration')
            profile = form.cleaned_data.get('profile')
            category_id = form.cleaned_data.get('category')
            teacher_id = form.cleaned_data.get('teacher')

            category = CourseCategory.objects.get(pk=category_id)
            teacher = Teacher.objects.get(pk=teacher_id)

            Course.objects.create(title=title, video_url=video_url, cover_url=cover_url, price=price, duration=duration\
                                  , profile=profile, category=category, teacher=teacher)
            return restful.ok()
        else:
            print(form.get_errors())
            return restful.params_errors(message=form.get_errors())


class AddTeacherView(View):
    def get(self, request):
        return render(request, 'cms/add_teacher.html')

    def post(self, request):
        form = AddTeacherForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            avatar = form.cleaned_data.get('avatar')
            jobtitle = form.cleaned_data.get('jobtitle')
            profile = form.cleaned_data.get('profile')
            Teacher.objects.create(username=username, avatar=avatar, jobtitle=jobtitle, profile=profile)
            return restful.ok()
        else:
            return restful.params_errors(message=form.get_errors())