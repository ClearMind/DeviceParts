from django.conf.urls.defaults import patterns, include, url
from parts.views import home, install, devices, installed, installed_in_device, prnt, change_store, cancel

urlpatterns = patterns('',
    (r'^$', home),
    (r'^install/$', install),
    (r'^devices/$', devices),
    (r'^installed/$', installed),
    (r'^installed/(\S+)/$', installed_in_device),
    (r'^print/$', prnt),
    (r'^change/$', change_store),
    (r'^cancel/(\d+)/$', cancel),
)