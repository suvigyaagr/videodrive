from django.conf.urls import url
from library.views import VideoListView


app_name = 'library'


urlpatterns = [
    url(r'^videos/$', VideoListView.as_view(), name='list-view'),
]
