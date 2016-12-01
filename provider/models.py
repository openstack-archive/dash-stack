from __future__ import unicode_literals

from django.db import models


class Provider(models.Model):
    provider = models.CharField(max_length=64)
    name = models.CharField(max_length=128)
