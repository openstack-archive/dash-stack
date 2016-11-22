from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.FileField(upload_to='static/avatar/%Y-%m-%d')
    provider_password = models.CharField(max_length=50)
    selected_provider = models.IntegerField()