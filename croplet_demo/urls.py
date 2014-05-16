from django.conf.urls import patterns, include, url
from django.contrib import admin
from apps.models import AccessToken

admin.autodiscover()
admin.site.register(AccessToken)

urlpatterns = patterns('',
    url(r'^', include('apps.urls')),
    url(r'^admin/', include(admin.site.urls)),
    (r'^accounts/login/$', 'django.contrib.auth.views.login'),
)
