from django.db import models

from apps.user.models.user import User


class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    create_date = models.DateTimeField()

    class Meta:
        ordering = ['-create_date']

    def __str__(self):
        return self.title
