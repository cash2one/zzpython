from django.conf.urls.defaults import patterns, include, url
import settings
urlpatterns = patterns('zz91yang.views',
    (r'^(?P<path>.*)$', 'default'),
)