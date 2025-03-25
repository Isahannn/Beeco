from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from .managers import CustomUserManager


class User(AbstractUser):

    username = None

    name = models.CharField(_('name'), max_length=100)
    email = models.EmailField(_('email address'), unique=True)
    last_Name=models.CharField(_('lastName'),max_length=100)
    nick_Name=models.CharField(_('nickname'),max_length=100)
    location = models.CharField(_('location'),max_length=30, blank=True)
    date_of_birth = models.DateField(_('dateOfBirth'), null=True, blank=True)
    avatar = models.ImageField(_('avatar'), upload_to='avatars/', null=True, blank=True)

    date_joined = models.DateTimeField(_('joined'),default=timezone.now)

    is_staff = models.BooleanField(_('isStaff'),default=False)
    is_active = models.BooleanField(_('isActive'),default=True)


    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['nick_Name','name','password']

    objects = CustomUserManager()

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'

# Create your models here.
