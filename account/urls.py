from account.views import login, logout
from django.conf.urls.defaults import patterns

urlpatterns = patterns('',
    (r'^login/$', login),
    (r'^logout/$', logout),
)