from django.conf import settings
from django.contrib.auth.models import User
from django.db import models

from django.db.models.signals import post_save
from django.dispatch import receiver


class UserProfile(models.Model):
    class Meta:
        db_table = 'user_profile'

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='profile',
        related_query_name='profile',
        db_index=True)

    display_name = models.CharField(max_length=255, blank=True)

    VOLUNTEER = 'VO'
    SHELTERED = 'SH'
    USER_KIND_CHOICES = (
        (VOLUNTEER, 'Volunteer'),
        (SHELTERED, 'At-Risk Sheltered')
    )
    kind = models.CharField(
        max_length=2,
        choices=USER_KIND_CHOICES,
        blank=True
    )

    is_publicly_visible = models.BooleanField(default=True)

    EMAIL = 'EM'
    PHONE = 'PH'
    CONTACT_CHOICES = (
        (EMAIL, "Email"),
        (PHONE, "Phone"),
    )
    contact_preference = models.CharField(
        max_length=2,
        choices=CONTACT_CHOICES,
        blank=True
    )
    contact_details = models.CharField(max_length=255, blank=True)
    description = models.TextField(default='', blank=True)


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


class UserLocation(models.Model):
    class Meta:
        db_table = 'user_location'

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='locations',
        related_query_name='location')
    google_place_id = models.CharField(max_length=512, db_index=True)