from django.shortcuts import render
from django.views.generic import View
from .models import NewsCategory, News, Comment, Banner
from django.conf import settings
from utils import restful
from.serializers import NewsSerializers, CommentSerializers
from django.http import Http404
from .forms import PublicCommentForm
from apps.xfzauth.decorators import xfz_login_required
from django.utils.decorators import method_decorator
from django.db.models import Q
from apps.course.models import Course


class IndexView(View):
    def get(self, request):
        count = settings.ONE_PAGE_NEWS_COUNT
        categories = NewsCategory.objects.all()
        newses = News.objects.select_related('category', 'author').all()[0:count]
        banners = Banner.objects.all()
        hotNewses = News.objects.filter(category__name='热点')
        course = Course.objects.filter(price=0).first()
        context = {
            'categories': categories,
            'newses': newses,
            'banners': banners,
            'hotNewses': hotNewses,
            'course': course
        }
        return render(request, 'news/index.html', context=context)


class NewsListView(View):
    def get(self, request):
        page = int(request.GET.get('p', 1))
        category_id = int(request.GET.get('category_id', 0))
        start = (page - 1)*settings.ONE_PAGE_NEWS_COUNT
        end = start + settings.ONE_PAGE_NEWS_COUNT
        if category_id == 0:
            newses = News.objects.select_related('category', 'author').all()[start:end]
            print(newses)
        else:
            newses = News.objects.select_related('category', 'author').filter(category_id=category_id)[start:end]
        serializers = NewsSerializers(newses, many=True)
        data = serializers.data
        return restful.result(data=data)


class NewsDetailView(View):
    def get(self, request, news_id):

            news = News.objects.prefetch_related('comments__author').select_related('category', 'author').get(pk=news_id)
            context = {
                'news': news,
            }
            return render(request, 'news/news_detail.html', context=context)


@method_decorator(xfz_login_required, name='dispatch')
class PublicCommentView(View):
    def post(self, request):
        form = PublicCommentForm(request.POST)
        if form.is_valid():
            content = form.cleaned_data.get('content')
            news_id = form.cleaned_data.get('news_id')
            news = News.objects.get(pk=news_id)
            comment = Comment.objects.create(content=content, news=news, author=request.user)
            serializers = CommentSerializers(comment)
            data = serializers.data
            return restful.result(data=data)
        else:
            return restful.params_errors(message=form.get_errors())


class SearchView(View):
    def get(self, request):
        q = request.GET.get('q')
        course = Course.objects.filter(price=0).first()
        hotNewses = News.objects.filter(category__name='热点')
        context = {
            'course': course,
            'hotNewses': hotNewses
        }
        if q:
            newses = News.objects.filter(Q(content__icontains=q)|Q(title__icontains=q))
            context['newses'] = newses
        else:
            newses = News.objects.filter(category__name='热点')
            context['newses'] = newses
        return render(request, 'search/search.html', context=context)