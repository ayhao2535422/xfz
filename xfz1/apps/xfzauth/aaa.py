# management commands
from django.contrib.auth.models import Permission, ContentType, Group
from django.core.management import BaseCommand
from apps.news.models import NewsCategory, Comment, News, Banner


class Command(BaseCommand):
    def handle(self, *args, **options):
        edit_content_types = [
            ContentType.objects.get_for_model(News),
            ContentType.objects.get_for_model(NewsCategory),
            ContentType.objects.get_for_model(Banner),
        ]
        edit_group = Group.objects.create(name='编辑')
        edit_permission = Permission.objects.filter(content_type__in=edit_content_types)
        edit_group.permissions.set(edit_permission)
        edit_group.save()