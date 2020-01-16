from django.contrib.auth.validators import UnicodeUsernameValidator
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.utils.translation import gettext_lazy
from django.db import models
from utils.storage import OverwriteStorage


class MyAccountManager(BaseUserManager):
    def create_user(self, email, username, password):
        if not email:
            raise ValueError('email must be provided')
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
    username = models.CharField(
        max_length=40,
        unique=True,
        validators=[UnicodeUsernameValidator()],
        help_text=gettext_lazy('Required. 40 characters or fewer. Letters, digits and @/./+/-/_ only.')
    )
    avatar = models.ImageField(upload_to=avatar_location,
                               storage=OverwriteStorage(),
                               null=True, blank=True)
    email = models.EmailField(max_length=254, unique=True)
    about = models.TextField(max_length=300, blank=True, null=True)

    date_joined = models.DateTimeField(verbose_name='date joined', auto_now_add=True)
    last_login = models.DateTimeField(verbose_name='last login', auto_now=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = MyAccountManager()

    USERNAME_FIELD = 'username'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ['email']

    DEFAULT_AVATAR_URL = 'static/img/default_avatar.svg'

    def __str__(self):
        return self.username

    @property
    def avatar_url(self):
        try:
            return self.avatar.url
        except ValueError:
            return self.DEFAULT_AVATAR_URL
