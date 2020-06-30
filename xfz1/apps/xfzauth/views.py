from django.shortcuts import render, redirect, reverse
from django.views.generic import View
from .forms import LoginForm, RegisterForm
from django.contrib.auth import authenticate, login, logout
from utils import restful
from utils.captcha.xfzcaptcha import Captcha
from io import BytesIO
from django.http import HttpResponse
from utils import sms_sender
from redis import Redis
from django.contrib.auth import get_user_model

User = get_user_model()

cache = Redis(host='192.168.159.130', port='6379', decode_responses=True)


class LoginView(View):
    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            telephone = form.cleaned_data.get('telephone')
            password = form.cleaned_data.get('password')
            remember = form.cleaned_data.get('remember')
            user = authenticate(request, username=telephone, password=password)
            if user:
                if user.is_active:
                    login(request, user)
                    if remember:
                        request.session.set_expiry(None)
                    else:
                        request.session.set_expiry(0)
                    return restful.ok()
                else:
                    return restful.no_auth(message='账号已被冻结')
            else:
                return restful.params_errors(message='账号或密码错误')
        else:
            return restful.params_errors(message=form.get_errors())


class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect(reverse('index'))


class RegisterView(View):
    def post(self, request):
        form = RegisterForm(request.POST)
        if form.is_valid():
            telephone = form.cleaned_data.get('telephone')
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = User.objects.create_user(telephone=telephone, username=username, password=password)
            login(request, user)
            return restful.ok()
        else:
            print(form.get_errors())
            return restful.params_errors(message=form.get_errors())


class ImgCaptchaView(View):
    def get(self, request):
        text, image = Captcha.gene_code()
        out = BytesIO()
        image.save(out, 'png')
        out.seek(0)
        response = HttpResponse(content_type='image/png')
        response.write(out.read())
        response['Content-length'] = out.tell()
        cache.set(text.lower(), text.lower(), ex=300)
        return response


class SmsCaptchaView(View):
    def get(self, request):
        telephone = request.GET.get('telephone')
        code = Captcha.gene_text()
        cache.set(telephone, code, ex=300)
        print(cache.get(telephone.lower()))
        return restful.ok()
        # result = sms_sender.send(telephone, code)
        # if result:
        #     return restful.ok()
        # else:
        #     return restful.params_errors(message='验证码发送失败')