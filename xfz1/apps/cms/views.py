from django.views.generic import View
from django.shortcuts import render
from django.contrib.admin.views.decorators import staff_member_required
from django.utils.decorators import method_decorator
from apps.news.models import NewsCategory, News, Banner
from utils import restful
from .forms import EditNewsCategoryForm, AddNewsCategoryForm, DelNewsCategoryForm, PublishNewsForm, AddBannerForm,\
    EditBannerForm, EditNewsForm
from django.core.paginator import Paginator
from django.conf import settings
from apps.news.serializers import BannerListSerializers
from django.contrib.auth.decorators import permission_required
from datetime import datetime
from django.utils.timezone import make_aware
from urllib import parse
import os
import qiniu


@method_decorator(staff_member_required(login_url='index'), name='dispatch')
class IndexView(View):
    def get(self, request):
        return render(request, 'cms/index.html')


@method_decorator(permission_required(perm="news.change_news", login_url='/'), name='dispatch')
class PublishNewsView(View):
    def get(self, request):
        categories = NewsCategory.objects.all()
        context = {
            'categories': categories
        }
        return render(request, 'cms/publish_news.html', context=context)

    def post(self, request):
        form = PublishNewsForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data.get('title')
            desc = form.cleaned_data.get('desc')
            thumbnail = form.cleaned_data.get('thumbnail')
            content = form.cleaned_data.get('content')
            category_id = form.cleaned_data.get('category')
            category = NewsCategory.objects.get(pk=category_id)
            title1 = request.POST.get('title')
            print(title1)
            News.objects.create(title=title, desc=desc, thumbnail=thumbnail, content=content, category=category)
            return restful.ok()
        else:
            return restful.params_errors(message=form.get_errors())


@method_decorator(permission_required(perm="news.change_news", login_url='/'), name='dispatch')
class EditNewsView(View):
    def get(self, request):
        news_id = request.GET.get('news_id')
        news = News.objects.get(pk=news_id)
        context = {
            'news': news,
            'categories': NewsCategory.objects.all()
        }
        return render(request, 'cms/publish_news.html', context=context)

    def post(self, request):
        form = EditNewsForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data.get('title')
            desc = form.cleaned_data.get('desc')
            thumbnail = form.cleaned_data.get('thumbnail')
            content = form.cleaned_data.get('content')
            category_id = form.cleaned_data.get('category')
            category = NewsCategory.objects.get(pk=category_id)
            pk = form.cleaned_data.get('pk')
            News.objects.filter(pk=pk).update(title=title, desc=desc, thumbnail=thumbnail, content=content, category=category)
            return restful.ok()
        else:
            return restful.params_errors(message=form.get_errors())


@method_decorator(permission_required(perm="news.change_news", login_url='/'), name='dispatch')
class DeleteNewsView(View):
    def post(self, request):
        news_id = request.POST.get('news_id')
        News.objects.filter(pk=news_id).delete()
        return restful.ok()


@method_decorator(permission_required(perm="news.change_news", login_url='/'), name='dispatch')
class NewsCategoryView(View):
    def get(self, request):
        categories = NewsCategory.objects.all()
        context = {
            'categories': categories
        }
        return render(request, 'cms/news_category.html', context=context)


@method_decorator(permission_required(perm="news.change_news", login_url='/'), name='dispatch')
class AddNewsCategoryView(View):
    def post(self, request):
        form = AddNewsCategoryForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data.get('name')
            exists = NewsCategory.objects.filter(name=name).exists()
            if not exists:
                NewsCategory.objects.create(name=name)
                return restful.ok()
            else:
                return restful.params_errors(message='该分类已存在')
        else:
            return restful.params_errors(message=form.get_errors())


@method_decorator(permission_required(perm="news.change_news", login_url='/'), name='dispatch')
class EditNewsCategoryView(View):
    def post(self, request):
        form = EditNewsCategoryForm(request.POST)
        if form.is_valid():
            pk = form.cleaned_data.get('pk')
            name = form.cleaned_data.get('name')
            try:
                category = NewsCategory.objects.filter(pk=pk)
                if category:
                    return restful.params_errors(message='该分类已存在')
                else:
                    category.update(name=name)
            except:
                return restful.params_errors(message='该分类不存在')
        else:
            return restful.params_errors(message=form.get_errors())


@method_decorator(permission_required(perm="news.change_newscategory", login_url='/'), name='dispatch')
class DelNewsCategoryView(View):
    def post(self, request):
        form = DelNewsCategoryForm(request.POST)
        if form.is_valid():
            pk = form.cleaned_data.get('pk')
            try:
                NewsCategory.objects.filter(pk=pk).delete()
                return restful.ok()
            except:
                return restful.params_errors(message='该分类不存在')
        else:
            return restful.params_errors(message=form.get_errors())


@method_decorator(permission_required(perm="news.change_banners", login_url='/'), name='dispatch')
class BannersView(View):
    def get(self, request):
        return render(request, 'cms/banners.html')


@method_decorator(permission_required(perm="news.change_banners", login_url='/'), name='dispatch')
class BannerListView(View):
    def get(self, request):
        banners = Banner.objects.all()
        serializers = BannerListSerializers(banners, many=True)
        data = serializers.data
        return restful.result(data=data)


@method_decorator(permission_required(perm="news.change_banners", login_url='/'), name='dispatch')
class AddBannerView(View):
    def post(self, request):
        form = AddBannerForm(request.POST)
        if form.is_valid():
            priority = form.cleaned_data.get('priority')
            link_to = form.cleaned_data.get('link_to')
            image_url = form.cleaned_data.get('image_url')
            banner = Banner.objects.create(priority=priority, link_to=link_to, image_url=image_url)
            return restful.result(data={'banner_id': banner.pk})
        else:
            return restful.params_errors(message=form.get_errors())


@method_decorator(permission_required(perm="news.change_banners", login_url='/'), name='dispatch')
class DelBannerView(View):
    def post(self, request):
        banner_id = request.POST.get('banner_id')
        Banner.objects.filter(pk=banner_id).delete()
        return restful.ok()


@method_decorator(permission_required(perm="news.change_banners", login_url='/'), name='dispatch')
class EditBannerView(View):
    def post(self, request):
        form = EditBannerForm(request.POST)
        if form.is_valid():
            priority = form.cleaned_data.get('priority')
            link_to = form.cleaned_data.get('link_to')
            image_url = form.cleaned_data.get('image_url')
            pk = form.cleaned_data.get('pk')
            Banner.objects.filter(pk=pk).update(priority=priority, link_to=link_to, image_url=image_url)
            return restful.ok()
        else:
            return restful.params_errors(message=form.get_errors())


@method_decorator(permission_required(perm="news.change_news", login_url='/'), name='dispatch')
class NewsListView(View):
    def get(self, request):
        page = int(request.GET.get('p', 1))
        start = request.GET.get('start')
        end = request.GET.get('end')
        title = request.GET.get('title')
        category_id = int(request.GET.get('category', 0) or 0)

        newses = News.objects.select_related('category', 'author')

        if start or end:
            if start:
                start_date = datetime.strptime(start, '%Y/%m/%d')
            else:
                start_date = datetime(year=2020, month=1, day=1)
            if end:
                end_date = datetime.strptime(end, '%Y/%m/%d')
            else:
                end_date = datetime.today()
            newses = newses.filter(pub_time__range=(make_aware(start_date), make_aware(end_date)))

        if title:
            newses = newses.filter(title__icontains=title)

        if category_id:
            newses = newses.filter(category=category_id)

        paginator = Paginator(newses, 2)
        page_obj = paginator.page(page)
        context = {
            'newses': page_obj.object_list,
            'categories': NewsCategory.objects.all(),
            'paginator': paginator,
            'page_obj': page_obj,
            'start': start,
            'end': end,
            'title': title,
            'category_id': category_id,
            'url_query': '&' + parse.urlencode({
                'start': start or '',
                'end': end or '',
                'title': title or '',
                'category': category_id or '',
            })
        }
        pagination_data = self.get_pagination_data(paginator, page_obj)
        context.update(pagination_data)
        return render(request, 'cms/news_list.html', context=context)

    def get_pagination_data(self, paginator, page_obj, around_number=2):
        current_page = page_obj.number
        left_has_more = False
        right_has_more = False

        if current_page <= around_number + 2:
            left_pages = range(1, current_page)
        else:
            left_has_more = True
            left_pages = range(current_page-around_number, current_page)
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


class UploadFileView(View):
    def post(self, request):
        file = request.FILES.get('file')
        name = file.name
        with open(os.path.join(settings.MEDIA_ROOT, name), 'wb') as fp:
            for chunk in file.chunks():
                fp.write(chunk)
        url = request.build_absolute_uri(settings.MEDIA_URL + name)
        return restful.result(data={'url': url})


class QiniuTokenView(View):
    def get(self, request):
        access_key = settings.QINIU_ACCESS_KEY
        secret_key = settings.QINIU_SECRET_KEY
        q = qiniu.Auth(access_key, secret_key)
        bucket = settings.QINIU_BUCKET_NAME
        token = q.upload_token(bucket)
        return restful.result(data={'token': token})