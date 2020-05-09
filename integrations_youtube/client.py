from youtube_api import YouTubeDataAPI

from integrations_youtube.models import YoutubeCredentials
from integrations_youtube.serializers import YoutubeDataVideoObjectSerializer


class YoutubeClient:
    def __init__(self, credentials: YoutubeCredentials):
        self.credentials = credentials

    def fetch(self):
        yt = YouTubeDataAPI(self.credentials.api_key)
        response = yt.search('official')
        serializer = YoutubeDataVideoObjectSerializer(data=response, many=True)
        if serializer.is_valid():
            serializer.save()
        else:
            print(serializer.errors)
