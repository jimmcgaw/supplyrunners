from django.conf import settings
from django.db import models


class UserLocation(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='locations',
        related_query_name='location')
    google_place_id = models.CharField(max_length=512, db_index=True)