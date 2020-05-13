from django.conf.urls import url

from library.views import get_saved_video_results, get_search_video_results

app_name = 'library'


urlpatterns = [
    url(r'^videos/$', get_saved_video_results, name='video-list-view'),
    url(r'^videos/search/$', get_search_video_results, name='video-search-view'),
]
