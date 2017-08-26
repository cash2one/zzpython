from django.conf.urls import patterns, include, url
import settings

urlpatterns = patterns('',
	(r'^$', 'zz91daohang.daohang.index'),
	(r'^index1.html', 'zz91daohang.daohang.index'),
	(r'^tags-(?P<code>\w+)/(?P<tags_id>\w+)/$', 'zz91daohang.daohang.detail'),
	(r'^tags-(?P<code>\w+)/(?P<tags_id>\w+)$', 'zz91daohang.daohang.detail'),
	(r'^tags-(?P<code>\w+)/$', 'zz91daohang.daohang.tagslist'),
	(r'^tags-(?P<code>\w+)$', 'zz91daohang.daohang.tagslist'),
	(r'^tags-(?P<code>\w+)/(?P<page>\d+).html$', 'zz91daohang.daohang.tagslist'),
	(r'^(?P<pingyin>\w+)/$', 'zz91daohang.daohang.daohangdetail'),
	(r'^(?P<pingyin>\w+)$', 'zz91daohang.daohang.daohangdetail'),
	(r'^(?P<pingyin>\w+)/(?P<path>.*)$', 'zz91daohang.daohang.daohangdetail_o'),
	(r'^(?!admin)(?P<path>.*)$','django.views.static.serve',{'document_root':settings.STATIC_ROOT}),
)
