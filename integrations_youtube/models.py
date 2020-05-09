from django.db import models

from utils.models import BaseModel


class YoutubeCredentials(BaseModel):
    name = models.CharField(
        max_length=40
    )
    api_key = models.CharField(
        max_length=40
    )
    is_active = models.BooleanField(
        default=False
    )
