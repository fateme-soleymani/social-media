from django.db import models


class User(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    date_of_birth = models.DateField(blank=True, null=True)
    user_name = models.CharField(max_length=200, unique=True)
    hash_pass = models.CharField(max_length=64)

    def __str__(self):
        return self.first_name
