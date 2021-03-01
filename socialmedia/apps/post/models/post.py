from django.db import models

from apps.user.models.user import User
from common.base_model import BaseModel


class Post(BaseModel):
    title = models.CharField(max_length=100)
    content = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return self.title + str(self.user)
