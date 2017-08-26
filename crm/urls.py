from django.conf.urls.defaults import *
from crm import views
import settings
# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
	(r'^complist/$', 'crm.views.complist'),
	(r'^zhuandan/$', 'crm.views.zhuandan'),
	(r'^getCompcountlist/$', 'crm.views.getCompcountlist'),
	(r'^huangye/$', 'crm.views.huangye'),
	(r'^huangye2013/$', 'crm.views.huangye2013'),
	(r'^huangye2014/$', 'crm.views.huangye2014'),
	(r'^huangye2015/$', 'crm.views.huangye2015'),
	(r'^huangye2016/$', 'crm.views.huangye2016'),
	(r'^huangye2017.html$', 'crm.views.huangye2017'),
	(r'^huangyeadd/$', 'crm.views.huangyeadd'),
	(r'^searchcomlist/$', 'crm.views.searchcomlist'),
	(r'^Sphinxstaus/$', 'crm.views.Sphinxstaus'),
	(r'^getwebconnect/$', 'crm.views.getwebconnect'),
	(r'^gonghaicomlist/$', 'crm.views.gonghaicomlist'),
	(r'^bbslist/$', 'crm.views.bbslist'),
	(r'^getusername/$', 'crm.views.getusername'),
	(r'^zqweb/$', 'crm.views.zqweb'),
	(r'^icdassign/$', 'crm.views.icdassign'),
	(r'openConfirm1/$', 'crm.views.openConfirm1'),
	(r'openConfirmsave1/$', 'crm.views.openConfirmsave1'),
	(r'recordlist.html$', 'crm.record.getrecord'),
	
	#(r'^css/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT+'/css'}),
	#(r'^js/(?P</path><path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT+'/js'}),
	#(r'^images/(?P<path>.*)$', 'django.views.static.serve', {'document_root':settings.STATIC_ROOT+'/images'}),
	(r'^(?!admin)(?P<path>.*)$','django.views.static.serve',{'document_root':settings.STATIC_ROOT}),
    # Examples:
    # url(r'^$', 'crm.views.home', name='home'),
    # url(r'^crm/', include('crm.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

)
