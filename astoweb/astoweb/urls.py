#from django.conf.urls.defaults import *
from django.conf.urls import patterns, include, url
import settings
# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'astoweb.views.home', name='home'),
    # url(r'^astoweb/', include('astoweb.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
	(r'^$', 'astoweb.views.default'),
	(r'^about.html$', 'astoweb.views.about'),
	(r'^cluster.html$', 'astoweb.views.cluster'),
	(r'^astoer.html$', 'astoweb.views.astoer'),
	(r'^public.html$', 'astoweb.views.public'),
	(r'^footprint.html$', 'astoweb.views.footprint'),
	(r'^b2c_cluster.html$', 'astoweb.views.b2c_cluster'),
	(r'^contact.html$', 'astoweb.views.contact'),
	(r'^focusing.html$', 'astoweb.views.focusing'),
	(r'^honor.html$', 'astoweb.views.honor'),
	(r'^knowledge.html$', 'astoweb.views.knowledge'),
	(r'^knowledge1.html$', 'astoweb.views.knowledge1'),
	(r'^knowledge2.html$', 'astoweb.views.knowledge2'),
	(r'^opportunity.html$', 'astoweb.views.opportunity'),
	(r'^stronghold.html$', 'astoweb.views.stronghold'),
	(r'^culture.html$', 'astoweb.views.culture'),
	(r'^mr_cluster.html$', 'astoweb.views.mr_cluster'),
	(r'^opportunity_school.html$', 'astoweb.views.opportunity_school'),
    (r'^ybpjob.html$', 'astoweb.views.ybpjob'),
	(r'^news(?P<newsid>\d+).html$', 'astoweb.views.news'),
	(r'^(?!admin)(?P<path>.*)$','django.views.static.serve',{'document_root':settings.STATIC_ROOT}),
)
