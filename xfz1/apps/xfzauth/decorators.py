from utils import restful
from django.shortcuts import redirect
from django.shortcuts import reverse


def xfz_login_required(func):
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated:
            return func(request, *args, **kwargs)
        else:
            if request.is_ajax():
                return restful.no_auth(message='请先登录')
            else:
                return redirect('/')
    return wrapper


def xfz_superuser_required(func):
    def wrapper(request, *args, **kwargs):
        if request.user.is_superuser:
            return func(request, *args, **kwargs)
        else:
            return redirect(reverse('index'))
    return wrapper