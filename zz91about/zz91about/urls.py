#-*- coding:utf-8 -*-
from django.conf.urls import *
import settings
# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'zz91about.views.home', name='home'),
    # url(r'^zz91about/', include('zz91about.foo.urls')),
	(r'^$', 'zz91about.views.default'),
	(r'^linkus.html$', 'zz91about.views.linkus'),
	(r'^about.html$', 'zz91about.views.about'),
	(r'^jobs.html$', 'zz91about.views.jobs'),
	(r'^honor.html$', 'zz91about.views.honor'),
	(r'^events.html$', 'zz91about.views.events'),
	(r'^cooperation.html$', 'zz91about.views.cooperation'),
	(r'^contact.html$', 'zz91about.views.contact'),
	(r'^team.html$', 'zz91about.views.team'),
    (r'^yssm.html$', 'zz91about.views.yssm'),
	(r'^public.html$', 'zz91about.views.public'),
	#(r'^qq.html$', 'zz91about.views.qqcontact'),#废塑料QQ群
    #(r'^qq1.html$', 'zz91about.views.qqcontact1'),#废金属QQ群
    #(r'^qq2.html$', 'zz91about.views.qqcontact2'),#废纸QQ群
	(r'^news(?P<newsid>\d+).html$', 'zz91about.views.news'),
    
    (r'^pay.html$', 'zz91about.views.zz91payfirst'),
    (r'^pay11.html$', 'zz91about.views.pay11'),
    (r'^paysave.html$', 'zz91about.views.zz91pay'),
    (r'^zz91payreturn_url.html$', 'zz91about.views.zz91payreturn_url'),
    (r'^zz91payverify_notify.html$', 'zz91about.views.zz91payverify_notify'),
    
    
	(r'^(?!admin)(?P<path>.*)$','django.views.static.serve',{'document_root':settings.STATIC_ROOT}),
)
