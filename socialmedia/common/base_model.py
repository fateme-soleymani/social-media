from datetime import datetime

from django.db import models
from django.utils.timezone import now


class BaseModel(models.Model):
    created = models.DateTimeField(default=now)

    class Meta:
        abstract = True
