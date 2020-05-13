from django.core.exceptions import ObjectDoesNotExist
from rest_framework import generics, status
from rest_framework.decorators import api_view
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

from integrations_youtube.client import YoutubeClient
from integrations_youtube.models import YoutubeCredentials
from integrations_youtube.serializers import (YoutubeDataVideoObjectSerializer,
                                              YoutubeVideoDetailsSerializer)
from library.models import YoutubeVideoDetails

KEY_PER_PAGE = 2


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 2
    page_size_query_param = 'page_size'
    max_page_size = 5


class VideoListView(generics.ListAPIView):
    queryset = YoutubeVideoDetails.objects.order_by('-video_publish_date')
    serializer_class = YoutubeVideoDetailsSerializer
    pagination_class = StandardResultsSetPagination


@api_view(('GET',))
def get_search_video_results(request):
        keywords = request.GET.get('q')
        if not keywords:
            return Response(data={"q": ["This field may not be null."]},
                            status=status.HTTP_400_BAD_REQUEST)
        _keywords = keywords.split(',')
        try:
            credentials_key = request.GET.get('key')
            if not credentials_key:
                credentials = YoutubeCredentials.active_objects.first()
                if not credentials:
                    return Response(data={"key": ["No active credentials currently exist."]},
                                    status=status.HTTP_503_SERVICE_UNAVAILABLE)
            else:
                credentials = YoutubeCredentials.active_objects.get(id=int(credentials_key))
        except ObjectDoesNotExist:
            return Response(data={"key": ["This field is not correct."]},
                            status=status.HTTP_400_BAD_REQUEST)

        yt = YoutubeClient(credentials).fetch(keywords=_keywords)
        serializer = YoutubeDataVideoObjectSerializer(data=yt, many=True)
        if not serializer.is_valid():
            # Soft Deleting the credential as no longer the date was successfully captured.
            # Next time YoutubeCredentialsManager will pick the next active credentials.
            credentials.is_active = False
            credentials.save()
            return Response(data={"key": ["Please try again in some time."]},
                            status=status.HTTP_503_SERVICE_UNAVAILABLE)
        else:
            return Response(serializer.data, status=status.HTTP_200_OK)
