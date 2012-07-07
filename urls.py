from django.conf.urls.defaults import patterns, include, url

from django.contrib import admin
from account.views import login, logout
from app.views import root


admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^parts/', include('parts.urls')),
    url(r'^accounts/', include('account.urls')),
    url(r'^expendables/$', include('expendables.urls')),

    (r'^$', root)
)
