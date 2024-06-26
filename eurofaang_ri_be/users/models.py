from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.db import models
from django.core.validators import RegexValidator
from rest_framework.authtoken.models import Token
from eurofaang_ri_be.constants import COUNTRIES


class User(AbstractUser):
    def __str__(self):
        return self.username

    COUNTRIES_CHOICES = [(str(i), COUNTRIES[i]) for i in range(len(COUNTRIES))]

    ROLE_CHOICES = [
        ('PI', 'Principal Investigator'),
        ('AP', 'Additional Participant'),
    ]

    phone_number = models.CharField(
        max_length=16,
        validators=[
            RegexValidator(
                regex=r'^\+\d{8,15}$',
                message="Phone number must be entered in the format: '+99999999'. Up to 15 digits is allowed."
            ),
        ],
        blank=True,
        null=True
    )

    organization_name = models.CharField(max_length=255, blank=True, null=True)
    organization_address = models.CharField(max_length=255, blank=True, null=True)
    organization_country = models.CharField(choices=COUNTRIES_CHOICES, blank=True, null=True)
    role = models.CharField(max_length=2, choices=ROLE_CHOICES, default='PI')

    def save(self, *args, **kwargs):
        if self.password and (self.pk is None or User.objects.get(pk=self.pk).password != self.password):
            self.set_password(self.password)
        super().save(*args, **kwargs)


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
