from django.db import models


class Comment(models.Model):
    text = models.TextField()
    user = models.ForeignKey('user.User', on_delete=models.CASCADE)
    post = models.ForeignKey('post.Post', on_delete=models.CASCADE)

    def __str__(self):
        return self.text


