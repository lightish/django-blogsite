from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from utils.storage import OverwriteStorage


class MyAccountManager(BaseUserManager):
    def create_user(self, email, username, password):
        if not email:
            raise ValueError('email must be provided')
        if not username:
            raise ValueError('username must be provided')
        if not password:
            raise ValueError('password must be provided')

        user = self.model(
            email=self.normalize_email(email),
            username=username
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password):
        user = self.create_user(email, username, password)
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


def avatar_location(instance, *args, **kwargs):
    return f'avatars/{instance.id}'


class Account(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=255, unique=True)
    username = models.CharField(max_length=200)
    avatar = models.ImageField(upload_to=avatar_location,
                               storage=OverwriteStorage(),
                               null=True, blank=True)
    about = models.TextField(max_length=300, blank=True, null=True)

    date_joined = models.DateTimeField(verbose_name='date joined',
                                       auto_now_add=True)
    last_login = models.DateTimeField(verbose_name='last login',
                                      auto_now=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = MyAccountManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    DEFAULT_AVATAR_URL = 'static/img/default_avatar.svg'

    def __str__(self):
        return self.username

    @property
    def avatar_url(self):
        if self.avatar.storage.exists(avatar_location(self)):
            return self.avatar.url
        else:
            return self.DEFAULT_AVATAR_URL
