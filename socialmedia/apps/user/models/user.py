from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django_extensions.db.fields import AutoSlugField

from apps.user.managers import UserManager


class User(AbstractBaseUser, PermissionsMixin):
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    date_of_birth = models.DateField(blank=True, null=True)
    email = models.EmailField("email address", unique=True, null=False)
    friends = models.ManyToManyField('User', through='FollowerFollowing')
    link = models.URLField('link', max_length=200, blank=True)
    bio = models.TextField('bio', blank=True)
    gender = models.CharField(choices=(('F', 'Female'), ('M', 'Male')), default='d', max_length=1)
    slug = AutoSlugField(populate_from=['email'], unique=True, )
    profile_pic = models.ImageField(default='default_prof.png', null=True, blank=True)
    is_active = models.BooleanField(('active'), default=True)
    is_superuser = models.BooleanField(('superuser'), default=False)
    is_staff = models.BooleanField(('staff'), default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = ('myuser')
        verbose_name_plural = ('myusers')
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
        return User.objects.all()
