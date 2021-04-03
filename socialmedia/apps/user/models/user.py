from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django_extensions.db.fields import AutoSlugField

from apps.user.managers import UserManager

import os

from apps.user.validator import mobile_validator, mobile_length_validator


def get_upload_path(instance, filename):
    return os.path.join(f'user/{instance.id}', filename)


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=100, unique=True)
    username_media = models.CharField(max_length=30, unique=True)
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    date_of_birth = models.DateField(blank=True, null=True)
    email = models.EmailField("email address", unique=True, blank=True, null=True)
    phone = models.CharField("mobile number", max_length=11, unique=True, null=True, blank=True, validators=[mobile_validator, mobile_length_validator])

    friends = models.ManyToManyField('User', through='FollowerFollowing')

    link = models.URLField('link', max_length=200, blank=True)
    bio = models.TextField('bio', blank=True)
    gender = models.CharField(choices=(('F', 'Female'), ('M', 'Male')), default='d', max_length=1)
    slug = AutoSlugField(populate_from=['username_media'], unique=True, )

    profile_pic = models.ImageField(default='default_prof.png', upload_to=get_upload_path, null=True, blank=True)

    sms_verify = models.CharField(max_length=3)


    is_active = models.BooleanField('active', default=True)
    is_superuser = models.BooleanField('superuser', default=False)
    is_staff = models.BooleanField('staff', default=False)
    objects = UserManager()
    USERNAME_FIELD = 'username'

    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = 'my user'
        verbose_name_plural = 'my users'
        app_label = 'user'

    def get_user_list(self):
        user_friends = self.friends.all()
        user_except_you = User.objects.exclude(id=self.id)
        user_list = set(user_except_you) - set(user_friends)
        return user_list

    def get_full_name(self):
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        return self.first_name

    def __str__(self):
        return self.first_name

    def all_user(self):
        return User.objects.exclude(id=self.id)

