from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.db import models
from shortuuidfield import ShortUUIDField


class UserManager(BaseUserManager):
    def _create_user(self, telephone, password, username, **kwargs):
        if not telephone:
            raise ValueError('请传入手机号码')
        if not password:
            raise ValueError('请传入密码')
        if not username:
            raise ValueError('请传入用户名')
        user = self.model(telephone=telephone, username=username, **kwargs)
        user.set_password(password)
        user.save()
        return user

    def create_user(self, telephone, password, username, **kwargs):
        kwargs['is_superuser'] = False
        return self._create_user(telephone, password, username, **kwargs)

    def create_superuser(self, telephone, password, username, **kwargs):
        kwargs['is_superuser'] = True
        kwargs['is_staff'] = True
        return self._create_user(telephone, password, username, **kwargs)


class User(AbstractBaseUser, PermissionsMixin):
    uid = ShortUUIDField(primary_key=True)
    telephone = models.CharField(max_length=11, unique=True)
    username = models.CharField(max_length=100)
    email = models.EmailField(unique=True, null=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)

    REQUIRED_FIELDS = ['username']
    USERNAME_FIELD = 'telephone'
    EMAIL_FIELD = 'email'

    objects = UserManager()

    def get_full_name(self):
        return self.username

    def get_short_name(self):
        return self.username