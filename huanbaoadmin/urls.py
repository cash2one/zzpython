from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    (r'^$', 'huanbaoadmin.views.default'),
	(r'tomcatmanager/$', 'huanbaoadmin.views.tomcatmanager'),
	(r'test/$', 'huanbaoadmin.views.test'),
)
