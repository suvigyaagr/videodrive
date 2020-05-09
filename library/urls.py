from django.conf.urls import url

from library.views import VideoListView, get_search_video_results

app_name = 'library'


urlpatterns = [
    url(r'^videos/$', VideoListView.as_view(), name='video-list-view'),
    url(r'^videos/search/$', get_search_video_results, name='video-search-view'),
]
