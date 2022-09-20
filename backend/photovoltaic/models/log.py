from django.db import models
from django.contrib.auth.models import User


class Log(models.Model):
    message = models.CharField(max_length=5000)
    title = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)

    @classmethod
    def create(cls, title, message):
        log = cls(title=title, message=message)

        return log