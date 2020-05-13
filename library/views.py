import datetime

import pytz
from django.core.paginator import Paginator
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

from integrations_youtube.client import YoutubeClient
from integrations_youtube.models import YoutubeCredentials
from integrations_youtube.serializers import (YoutubeDataVideoObjectSerializer,
                                              YoutubeVideoDetailsSerializer)
from library.helpers import (convert_last_video_dt_to_page_token,
                             get_last_video_dt_from_page_token)
from library.models import YoutubeVideoDetails

KEY_PER_PAGE = 4


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 2
    page_size_query_param = 'page_size'
    max_page_size = 5


@api_view(('GET',))
def get_saved_video_results(request):
    first_jan_1970_datetime = datetime.datetime(year=1970, month=1, day=1, tzinfo=pytz.UTC)
    page_token = request.GET.get('pageToken')
    try:
        last_video_epoch = get_last_video_dt_from_page_token(page_token)
        assert last_video_epoch > 0
    except AttributeError:
        last_video_epoch = None
    except AssertionError:
        return Response(data={"pageToken": ["Please enter a valid page token."]},
                        status=status.HTTP_400_BAD_REQUEST)
    if last_video_epoch:
        last_video_datetime = first_jan_1970_datetime + datetime.timedelta(seconds=last_video_epoch)
        videos = YoutubeVideoDetails.objects.filter(video_publish_date__lt=last_video_datetime).\
            order_by('-video_publish_date')
    else:
        videos = YoutubeVideoDetails.objects.order_by('-video_publish_date')
    paginator = Paginator(videos, KEY_PER_PAGE)
    paginated_videos_list = paginator.page(1).object_list
    serializer = YoutubeVideoDetailsSerializer(paginated_videos_list, many=True)
    serializer_data = serializer.data

    new_last_video_epoch = \
        (datetime.datetime.fromisoformat(serializer_data[len(serializer_data)-1].get('video_publish_date')[:-1]+'+00:00') -
         first_jan_1970_datetime).total_seconds()
    next_page_token = convert_last_video_dt_to_page_token(int(new_last_video_epoch))
    data = {
        'next': next_page_token,
        'videos': serializer_data,
    }
    return Response(data=data, status=status.HTTP_200_OK)


@api_view(('GET',))
def get_search_video_results(request):
        keywords = request.GET.get('q')
        if not keywords:
            return Response(data={"q": ["This field may not be null."]},
                            status=status.HTTP_400_BAD_REQUEST)
        _keywords = keywords.split(',')
        try:
            credentials = YoutubeCredentials.active_objects.first()
        except IndexError:
            return Response(data={"key": ["No active credentials currently exist."]},
                            status=status.HTTP_503_SERVICE_UNAVAILABLE)

        yt = YoutubeClient(credentials).fetch(keywords=_keywords)
        serializer = YoutubeDataVideoObjectSerializer(data=yt, many=True)
        if not serializer.is_valid():
            # Soft Deleting the credential as no longer the date was successfully captured.
            # Next time YoutubeCredentialsManager will pick the next active credentials.
            credentials.last_expired_at = datetime.now()
            credentials.save()
            return Response(data={"key": ["Please try again in some time."]},
                            status=status.HTTP_503_SERVICE_UNAVAILABLE)
        else:
            return Response(serializer.data, status=status.HTTP_200_OK)
