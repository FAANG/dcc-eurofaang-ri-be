from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.db import models
from rest_framework.authtoken.models import Token


class User(AbstractUser):
    def __str__(self):
        return self.username


class Rationale(models.Model):
    context = models.CharField(max_length=1500)
    objectives = models.CharField(max_length=500)
    impact = models.CharField(max_length=1000)


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
