from django.db import models

from utils.models import BaseModel


class YoutubeCredentialsManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_active=True)


class YoutubeCredentials(BaseModel):
    objects = models.Manager()
    active_objects = YoutubeCredentialsManager()

    name = models.CharField(
        max_length=40
    )
    api_key = models.CharField(
        max_length=40
    )
    is_active = models.BooleanField(
        default=False
    )
