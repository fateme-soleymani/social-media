import hashlib

from django.db import models


class User(models.Model):
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    date_of_birth = models.DateField(blank=True, null=True)
    user_name = models.CharField(max_length=200, unique=True)
    hash_pass = models.CharField(max_length=64)
    friends = models.ManyToManyField('User', related_name='following')
    login_status = models.BooleanField(default=False)

    def __str__(self):
        return self.first_name

    # def save(self, *args, **kwargs):
    #     """
    #     save hash pass in database
    #     """
    #     self.hash_pass = hashlib.sha256(str(self.hash_pass).encode()).hexdigest()
    #     super(User, self).save(*args, **kwargs)
