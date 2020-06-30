from apps.xfzauth.forms import BaseForm
from django import forms
from apps.news.models import News
from apps.news.models import Banner


class AddNewsCategoryForm(BaseForm):
    name = forms.CharField(max_length=100)


class EditNewsCategoryForm(BaseForm):
    pk = forms.IntegerField()
    name = forms.CharField(max_length=100)


class DelNewsCategoryForm(BaseForm):
    pk = forms.IntegerField()


class PublishNewsForm(forms.ModelForm, BaseForm):
    category = forms.IntegerField()

    class Meta:
        model = News
        exclude = ['category', 'author', 'pub_time']


class EditNewsForm(forms.ModelForm, BaseForm):
    category = forms.IntegerField()
    pk = forms.IntegerField()

    class Meta:
        model = News
        exclude = ['category', 'author', 'pub_time']


class AddBannerForm(forms.ModelForm, BaseForm):
    class Meta:
        model = Banner
        fields = ['priority', 'link_to', 'image_url']


class EditBannerForm(forms.ModelForm, BaseForm):
    pk = forms.IntegerField()

    class Meta:
        model = Banner
        fields = ['priority', 'link_to', 'image_url']


class AddStaffForm(BaseForm):
    telephone = forms.CharField(max_length=11)