from django.db import models


class YoutubeCredentials(models.Model):
    name = models.CharField(
        max_length=40
    )
    api_key = models.CharField(
        max_length=40
    )
    is_active = models.BooleanField(
        default=False
    )
