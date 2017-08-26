from django.conf.urls import *
import settings
# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    # (r'^zz91help/', include('zz91help.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # (r'^admin/', include(admin.site.urls)),
	(r'^$', 'zz91help.views.default'),
	(r'^question/$', 'zz91help.views.question'),
	(r'^question$', 'zz91help.views.question'),
	(r'^contact/$', 'zz91help.views.contact'),
	(r'^contact$', 'zz91help.views.contact'),
	(r'^list-(?P<cat_id>\d+)/$', 'zz91help.views.list'),
	(r'^list-(?P<cat_id>\d+)$', 'zz91help.views.list'),
	(r'^list-(?P<cat_id>\d+)-(?P<page>\d+)/$', 'zz91help.views.listmore'),
	(r'^list-(?P<cat_id>\d+)-(?P<page>\d+)$', 'zz91help.views.listmore'),
	(r'^searchfirst/$', 'zz91help.views.searchfirst'),
	(r'^searchfirst$', 'zz91help.views.searchfirst'),
	(r'^search-(?P<keywords>\w+)/$', 'zz91help.views.search'),
	(r'^search-(?P<keywords>\w+)$', 'zz91help.views.search'),
	(r'^search-(?P<keywords>\w+)-(?P<page>\d+)/$', 'zz91help.views.search'),
	(r'^search-(?P<keywords>\w+)-(?P<page>\d+)$', 'zz91help.views.search'),
	(r'^detail-(?P<aid>\d+)/$', 'zz91help.views.detail'),
	(r'^detail-(?P<aid>\d+)$', 'zz91help.views.detail'),
	(r'^beginner/$', 'zz91help.views.beginner'),
	(r'^beginner$', 'zz91help.views.beginner'),
	(r'^(?!admin)(?P<path>.*)$','django.views.static.serve',{'document_root':settings.STATIC_ROOT}),
)
