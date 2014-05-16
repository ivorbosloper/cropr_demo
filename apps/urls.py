from django.conf.urls import patterns, url
from views import Home, MapView, callback

urlpatterns = patterns('',
    url(r'^$', Home.as_view(), name="home"),
    url(r'map/$', MapView.as_view(), name="map"),
    url(r'cropr/callback/$', callback, name="callback"),
)