from django.db import models
from utils.models import BaseModel


class YoutubeChannelDetails(BaseModel):
    channel_id = models.CharField(
        max_length=30,
        unique=True,
    )
    channel_title = models.CharField(
        max_length=100,
    )


class YoutubeVideoDetails(BaseModel):
    channel = models.ForeignKey(
        YoutubeChannelDetails,
        on_delete=models.PROTECT
    )
    video_id = models.CharField(
        max_length=30,
        unique=True,
    )
    video_title = models.CharField(
        max_length=50,
    )
    video_description = models.TextField()
    video_thumbnail = models.URLField()
    video_publish_date = models.DateTimeField()
