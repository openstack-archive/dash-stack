from __future__ import unicode_literals

from django.db import models
from django.conf import settings
from django.dispatch import receiver
from django.db.models.signals import post_save


class Profile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        related_name='profile',
        verbose_name=('user'),
        null=True,
        blank=True,
    )
    avatar = models.FileField(upload_to='static/avatar/%Y-%m-%d')
    provider_password = models.CharField(max_length=50,null=True)
    selected_provider = models.IntegerField(null=True)
    activation_key = models.CharField(max_length=64,null=True)
    key_expires = models.DateTimeField(null=True)

    class Meta:
        verbose_name=('Profile')
        verbose_name_plural=('Profiles')
        ordering=('user',)

    def __str__(self):
        return self.user.username

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_profile_for_new_user(sender, created, instance, **kwargs):
    if created:
        profile = Profile(user=instance)
        profile.save()