from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from rest_framework.authtoken.models import Token


class User(AbstractUser):
    def __str__(self):
        return self.username

    ROLE_CHOICES = [
        ('PI', 'Principal Investigator'),
        ('AP', 'Additional Participant'),
    ]

    phone_number = PhoneNumberField()
    organization_name = models.CharField()
    organization_address = models.CharField()
    role = models.CharField(max_length=2, choices=ROLE_CHOICES, default='PI')


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
