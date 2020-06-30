from django import forms
from apps.xfzauth.forms import BaseForm


class PublicCommentForm(BaseForm):
    content = forms.CharField()
    news_id = forms.IntegerField()