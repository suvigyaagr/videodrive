from datetime import datetime

from integrations_youtube.models import YoutubeCredentials
from utils.models import Setting
from youtube_api import YouTubeDataAPI

KEY_YOUTUBE_PUBLISHED_DATE = 'YOUTUBE_PUBLISHED_DATE'


class YoutubeClient:
    def __init__(self, credentials: YoutubeCredentials):
        self.credentials = credentials

    def fetch(self, keywords, published_after=None, max_results=5, order_by='date'):
        yt = YouTubeDataAPI(self.credentials.api_key)
        if not published_after:
            _published_after = Setting.objects.get(key=KEY_YOUTUBE_PUBLISHED_DATE).value
            published_after = datetime.strptime(_published_after, '%Y-%m-%dT%H:%M:%S%z').date()
        response = yt.search(
            keywords,
            max_results=max_results,
            order_by=order_by,
            published_after=published_after,
        )
        print(response)
        return response
