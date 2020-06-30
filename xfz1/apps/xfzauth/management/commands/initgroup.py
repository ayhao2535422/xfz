from django.core.management import BaseCommand
from django.contrib.auth.models import Group, ContentType, Permission
from apps.news.models import News, NewsCategory, Banner, Comment
from apps.course.models import Course, CourseCategory, Teacher
from apps.aboutme.models import PayInfo
from apps.course.models import CourseOrder


class Command(BaseCommand):
    def handle(self, *args, **options):
        # 1. 编辑组（管理新闻/管理课程/管理评论/管理轮播图等）
        edit_content_types = [
            ContentType.objects.get_for_model(News),
            ContentType.objects.get_for_model(NewsCategory),
            ContentType.objects.get_for_model(Banner),
            ContentType.objects.get_for_model(Course),
            ContentType.objects.get_for_model(CourseCategory),
            ContentType.objects.get_for_model(Teacher),
            ContentType.objects.get_for_model(PayInfo),
        ]
        edit_group = Group.objects.create(name='编辑')
        edit_permissions = Permission.objects.filter(content_type__in=edit_content_types)
        edit_group.permissions.set(edit_permissions)
        edit_group.save()
        self.stdout.write(self.style.SUCCESS('编辑组创建完成'))

        # 2. 财务组（课程订单/付费资讯订单）
        finance_content_types = [
            ContentType.objects.get_for_model(CourseOrder),
        ]
        finance_group = Group.objects.create(name='财务')
        finance_permissions = Permission.objects.filter(content_type__in=finance_content_types)
        finance_group.permissions.set(finance_permissions)
        finance_group.save()
        self.stdout.write(self.style.SUCCESS('财务组创建成功'))

        # 3.管理组
        admin_permissions = edit_permissions.union(finance_permissions)
        admin_group = Group.objects.create(name='管理员')
        admin_group.permissions.set(admin_permissions)
        admin_group.save()
        self.stdout.write(self.style.SUCCESS('管理员组创建成功'))