from django.conf.urls.defaults import *
import settings

urlpatterns = patterns('zz91pay.views',
    (r'^$', 'default'),
)