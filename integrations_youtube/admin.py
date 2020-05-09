from django.contrib import admin

from integrations_youtube.models import YoutubeCredentials


@admin.register(YoutubeCredentials)
class YoutubeCredentialsAdmin(admin.ModelAdmin):
    pass
