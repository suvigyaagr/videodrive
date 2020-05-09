from datetime import datetime

from rest_framework import serializers
from rest_framework.fields import empty

from library.models import YoutubeChannelDetails, YoutubeVideoDetails


class YoutubeDataVideoListSerializer(serializers.ListSerializer):

    def create(self, validated_data):
        videos = []
        for item in validated_data:
            channel, _ = YoutubeChannelDetails.objects.get_or_create(
                channel_id=item['channel_id'],
                defaults={
                    'channel_title': item['channel_title'],
                }
            )
            video, _ = YoutubeVideoDetails.objects.get_or_create(
                video_id=item['video_id'],
                defaults={
                    'channel': channel,
                    'video_title': item['video_title'],
                    'video_description': item['video_description'],
                    'video_thumbnail': item['video_thumbnail'],
                    'video_publish_date': item['video_publish_date'],
                }
            )
            videos.append(video)
        return videos


class YoutubeDataVideoObjectSerializer(serializers.Serializer):
    channel_id = serializers.CharField(max_length=30)
    channel_title = serializers.CharField(max_length=300)
    video_id = serializers.CharField(max_length=30)
    video_title = serializers.CharField(max_length=300)
    video_description = serializers.CharField(max_length=1000, allow_blank=True)
    video_publish_date = serializers.DateTimeField()
    video_thumbnail = serializers.URLField(allow_blank=True)

    class Meta:
        list_serializer_class = YoutubeDataVideoListSerializer

    def __init__(self, data=empty, *args, **kwargs):
        for item in data:
            item['video_publish_date'] = datetime.fromtimestamp(item.get('video_publish_date'))
        super().__init__(data=data, *args, **kwargs)


class YoutubeVideoDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = YoutubeVideoDetails
        fields = '__all__'
