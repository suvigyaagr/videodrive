from django.db import models

# Create your models here.
class YoutubeVideoDetials(models.Model):
    link = models.URLField()
    