from django.conf.urls.defaults import patterns
from expendables.views import all as all_exp

urlpatterns = patterns('',
    (r'^$', all_exp),
)
