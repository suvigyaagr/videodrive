from datetime import datetime, time, timedelta

from django.db import models

from utils.models import BaseModel


class YoutubeCredentialsManager(models.Manager):
    def get_queryset(self):
        final_creds = []
        for cred in super().get_queryset().filter(is_active=True):
            if not cred.last_expired_at:
                final_creds.append(cred)
            else:
                if cred.last_expired_at < (datetime.now() - timedelta(hours=24)):
                    final_creds.append(cred)
                elif cred.last_expired_at.time() <= cred.quota_restarts_at <= datetime.now().time():
                    final_creds.append(cred)
        return final_creds

    def first(self):
        return self.get_queryset()[0]

    def last(self):
        return self.get_queryset()[-1]


class YoutubeCredentials(BaseModel):
    objects = models.Manager()
    active_objects = YoutubeCredentialsManager()

    name = models.CharField(
        max_length=40
    )
    api_key = models.CharField(
        max_length=40
    )
    quota_restarts_at = models.TimeField(
        default=time(0, 0, 0)
    )
    last_expired_at = models.DateTimeField(
        null=True,
        blank=True
    )
    is_active = models.BooleanField(
        default=False
    )
