from __future__ import unicode_literals

from django.db import models


class Provider(models.Model):
    id = models.AutoField(primary_key=True)
    provider = models.CharField(max_length=64)
    name = models.CharField(
        max_length=255,
        unique=True,
        db_index=True
    )
    region = models.CharField(
        max_length=255,
        unique=True,
        db_index=True
    )
    project_id = models.CharField(
        max_length=255,
        db_index=True
    )
    default_role = models.CharField(max_length=255)
    default_domain_id = models.CharField(max_length=255)
    username = models.CharField(
        max_length=255,
        unique=True,
        db_index=True
    )
    password = models.CharField(max_length=255)
    api_version = models.CharField(max_length=255)
    url = models.TextField()
    created_at = models.DateField()
    enabled = models.BooleanField(default=True)
    validated = models.BooleanField(default=False)

    def __unicode__(self):
        return self.name


class Type(models.Model):
    types = (
        ('1', 'Public Cloud Provider'),
        ('2', 'Private Cloud Provider'),
        ('3', 'Container Provider'),
        ('4', 'VPS Provider'),
    )
    id = models.AutoField(primary_key=True)
    name = models.CharField(
        max_length=255,
        unique=True,
        db_index=True
    )
    type = models.CharField(
        max_length=1,
        choices=types
    )
    logo = models.FileField(upload_to='static/provider-logo/')

    def __unicode__(self):
        return  self.name

