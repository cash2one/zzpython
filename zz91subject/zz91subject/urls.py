from django.conf.urls import *
from zz91subject import views
import settings
# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
	(r'^zt/addclick/$', 'zz91subject.views.addclick'),
	(r'^zt/$', 'zz91subject.views.default1'),
	(r'zhuantimore(?P<typeid>\w+).html$', 'zz91subject.views.zhuantimore'),
	(r'zhuantimore(?P<typeid>\w+)-(?P<page>\w+).html$', 'zz91subject.views.zhuantimore'),

	(r'zt/baomingsave_get/$', 'zz91subject.views.baomingsave_get'),
	(r'zt/baomingsave/$', 'zz91subject.views.baomingsave'),
	(r'zt/baomingsave.html$', 'zz91subject.views.baomingsave'),
	(r'zt/miaosha_save/$', 'zz91subject.views.miaosha_save'),
	(r'zt/baoming_save/$', 'zz91subject.views.baoming_save'),
	(r'zt/huangye_save/$', 'zz91subject.views.huangye_save'),
	
	(r'zt/zhibo.html$', 'zz91subject.subject.zhibo'),
	(r'zt/zhibo_more.html$', 'zz91subject.subject.zhibo_more'),
	(r'zt/zhibo_pinlun_save.html$', 'zz91subject.subject.zhibo_pinlun_save'),
	(r'zt/zhibo_pinlun_more.html$', 'zz91subject.subject.zhibo_pinlun_more'),
	(r'zt/zhibo_pinluncount.html$', 'zz91subject.subject.zhibo_pinluncount'),
	
	#621峰会数据
	(r'zt/fh621_index.html$', 'zz91subject.subject.fh621_index'),
	(r'zt/fh621_news.html$', 'zz91subject.subject.fh621_news'),
	(r'zt/fh621_luck.html$', 'zz91subject.subject.fh621_luck'),
	(r'zt/fh621_luck_save.html$', 'zz91subject.subject.fh621_luck_save'),
	(r'zt/fh621_zajindan.html$', 'zz91subject.subject.fh621_zajindan'),
	(r'zt/fh621_zajindanlist.html$', 'zz91subject.subject.fh621_zajindanlist'),
	(r'zt/chcompanylist.html$', 'zz91subject.subject.chcompanylist'),
	
	(r'zt/comm_newslist.html$', 'zz91subject.subject.comm_newslist'),
	(r'zt/comm_zhibolist.html$', 'zz91subject.subject.comm_zhibolist'),
	
	(r'^(?P<subjectname>\w+)/(?P<pagename>\w+)/$', 'zz91subject.views.subject'),
	(r'^(?P<subjectname>\w+)/(?P<pagename>\w+)$', 'zz91subject.views.subject'),
	(r'^(?P<subjectname>\w+)/(?P<pagename>\w+).html$', 'zz91subject.views.subject'),
    
    (r'^zt/(?P<subjectname>\w+)/(?P<pagename>\w+)/$', 'zz91subject.views.subject'),
    (r'^zt/(?P<subjectname>\w+)/(?P<pagename>\w+)$', 'zz91subject.views.subject'),
    (r'^zt/(?P<subjectname>\w+)/(?P<pagename>\w+).html$', 'zz91subject.views.subject'),
    
    (r'^zt/(?!admin)(?P<path>.*)$','django.views.static.serve',{'document_root':settings.STATIC_ROOT}),
	(r'^(?!admin)(?P<path>.*)$','django.views.static.serve',{'document_root':settings.MAIN_STATIC_ROOT}),
	
)
