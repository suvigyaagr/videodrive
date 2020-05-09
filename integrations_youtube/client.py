from youtube_api import YouTubeDataAPI

from integrations_youtube.models import YoutubeCredentials
from integrations_youtube.serializers import YoutubeDataVideoObjectSerializer


class YoutubeClient:
    def __init__(self, credentials: YoutubeCredentials):
        self.credentials = credentials

    def fetch(self, keyword, max_results=5, order_by='date'):
        yt = YouTubeDataAPI(self.credentials.api_key)
        response = yt.search(keyword, max_results=max_results, order_by=order_by)
        serializer = YoutubeDataVideoObjectSerializer(data=response, many=True)
        if serializer.is_valid():
            serializer.save()
        else:
            print(serializer.errors)
