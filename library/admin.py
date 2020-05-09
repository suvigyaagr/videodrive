from django.contrib import admin

from library.models import YoutubeChannelDetails, YoutubeVideoDetails


@admin.register(YoutubeChannelDetails)
class YoutubeChannelDetailsAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'channel_id',
        'channel_title',
    )


@admin.register(YoutubeVideoDetails)
class YoutubeVideoDetailsAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'video_id',
        'video_title',
        'video_publish_date',
    )
