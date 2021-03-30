import os

from django.db import models

from apps.user.models.user import User
from django.utils.timezone import now


def get_upload_path(instance, filename):
    return os.path.join(f'post/{instance.user.id}', filename)


class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField(blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created = models.DateTimeField(default=now)
    like = models.ManyToManyField(User, related_name='l')

    post_pic = models.ImageField(upload_to=get_upload_path,null=True, blank=True)

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return self.title + str(self.user)
