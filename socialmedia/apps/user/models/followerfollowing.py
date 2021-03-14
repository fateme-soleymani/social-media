from django.db import models


class FollowerFollowing(models.Model):
    from_user = models.ForeignKey('User', on_delete=models.CASCADE, related_name='from_user')
    to_user = models.ForeignKey('User', on_delete=models.CASCADE, related_name='to_user')
    accept = models.BooleanField(default=False)
