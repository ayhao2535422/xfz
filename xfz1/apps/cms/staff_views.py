from django.views import View
from django.shortcuts import render, reverse, redirect
from apps.xfzauth.models import User
from django.contrib.auth.models import Group
from utils import restful
from .forms import AddStaffForm
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import permission_required
from apps.xfzauth.decorators import xfz_superuser_required


@method_decorator(xfz_superuser_required, name='dispatch')
class StaffView(View):
    def get(self, request):
        staffs = User.objects.filter(is_staff=True)
        context = {
            'staffs': staffs
        }
        return render(request, 'cms/staffs.html', context=context)


@method_decorator(xfz_superuser_required, name='dispatch')
class AddStaffView(View):
    def get(self, request):
        groups = Group.objects.all()
        context = {
            'groups': groups
        }
        return render(request, 'cms/add_staff.html', context=context)

    def post(self, request):
        form = AddStaffForm(request.POST)
        if form.is_valid():
            telephone = form.cleaned_data.get('telephone')
            user = User.objects.filter(telephone=telephone).first()
            group_ids = request.POST.getlist('groups')
            user.is_staff = True
            groups = Group.objects.filter(pk__in=group_ids)
            user.groups.set(groups)
            user.save()
            return redirect(reverse('cms:cms_staff'))
        else:
            return restful.params_errors(message=form.get_errors())