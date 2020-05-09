from rest_framework.pagination import PageNumberPagination
from rest_framework import generics


from integrations_youtube.serializers import YoutubeVideoDetailsSerializer
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
