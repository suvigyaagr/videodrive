from django.core.exceptions import ObjectDoesNotExist

from integrations_youtube.client import YoutubeClient
from integrations_youtube.models import YoutubeCredentials
from integrations_youtube.serializers import YoutubeDataVideoObjectSerializer
from utils.models import Setting

KEY_CRON_FETCH_VIDEO_KEYWORDS = 'CRON_FETCH_VIDEO_KEYWORDS'
KEY_CRON_FETCH_VIDEO_MAX_RESULTS = 'CRON_FETCH_VIDEO_MAX_RESULTS'
KEY_CRON_FETCH_VIDEO_PUBLISHED_BEFORE = 'CRON_FETCH_VIDEO_PUBLISHED_BEFORE'
KEY_CRON_FETCH_VIDEO_PUBLISHED_AFTER = 'CRON_FETCH_VIDEO_PUBLISHED_AFTER'


def fetch_and_store_video_details():
    creds = YoutubeCredentials.active_objects.first()
    try:
        keywords = Setting.objects.get(key=KEY_CRON_FETCH_VIDEO_KEYWORDS).value
    except ObjectDoesNotExist:
        keywords = ''
    try:
        max_results = Setting.objects.get(key=KEY_CRON_FETCH_VIDEO_MAX_RESULTS).value
    except ObjectDoesNotExist:
            max_results = 50

    _keywords = keywords.split(',')
    if int(max_results) > 50:
        _max_results = 50
    else:
        _max_results = int(max_results)

    response = YoutubeClient(creds).fetch(
        keywords=_keywords,
        max_results=_max_results,
        order_by='date',
    )

    serializer = YoutubeDataVideoObjectSerializer(data=response, many=True)
    if serializer.is_valid():
        serializer.save()
    else:
        # Soft Deleting the credential as no longer the date was successfully captured.
        # Next time YoutubeCredentialsManager will pick the next active credentials.
        creds.is_active = False
        creds.save()
