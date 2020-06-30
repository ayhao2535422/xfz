from django import forms
from apps.xfzauth.models import User
from redis import Redis
import redis

cache = redis.StrictRedis(host='192.168.159.130', port='6379', decode_responses=True)


class BaseForm(forms.Form):
    def get_errors(self):
        if hasattr(self, 'errors'):
            errors = self.errors.get_json_data()
            new_errors = {}
            for key, value in errors.items():
                messages = []
                for message in value:
                    messages.append(message['message'])
                new_errors[key] = messages
            return new_errors
        else:
            return {}


class LoginForm(BaseForm):
    telephone = forms.CharField(max_length=11)
    password = forms.CharField(max_length=20, min_length=6, error_messages={
        'max_length': '密码最多不能超过20个字符',
        'min_length': '密码最少不能少于6个字符',
    })
    remember = forms.IntegerField(required=False)


class RegisterForm(BaseForm):
    telephone = forms.CharField(max_length=11)
    username = forms.CharField(max_length=20)
    password = forms.CharField(max_length=20, min_length=6, error_messages={
        'max_length': '密码最多不能超过20个字符',
        'min_length': '密码最少不能少于6个字符',
    })
    password1 = forms.CharField(max_length=20, min_length=6, error_messages={
        'max_length': '密码最多不能超过20个字符',
        'min_length': '密码最少不能少于6个字符',
    })
    img_captcha = forms.CharField(max_length=4, min_length=4)
    sms_captcha = forms.CharField(max_length=4, min_length=4)

    def clean(self):
        cleaned_data = super().clean()

        # 验证手机号码是否相等
        telephone = cleaned_data.get('telephone')
        exists = User.objects.filter(telephone=telephone).exists()
        if exists:
            raise forms.ValidationError('手机号码已存在')

        # 验证密码是否相等
        password = cleaned_data.get('password')
        password1 = cleaned_data.get('password1')
        if password != password1:
            raise forms.ValidationError('两次密码输入不一致')

        # 验证图形验证码是否相等
        img_captcha = cleaned_data.get('img_captcha')
        cache_img_captcha = cache.get(img_captcha)
        if not img_captcha or img_captcha != cache_img_captcha:
            raise forms.ValidationError('图形验证码错误')

        # 验证短信验证码是否相等
        sms_captcha = cleaned_data.get('sms_captcha')
        cache_sms_captcha = cache.get(telephone)
        if not sms_captcha or sms_captcha != cache_sms_captcha:
            raise forms.ValidationError('短信验证码错误')
        return cleaned_data

