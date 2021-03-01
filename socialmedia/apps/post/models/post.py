from django.db import models

from apps.user.models.user import User
from django.utils.timezone import now


class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created = models.DateTimeField(default=now)

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return self.title + str(self.user)
