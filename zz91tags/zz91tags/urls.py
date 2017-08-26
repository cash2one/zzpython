from django.conf.urls import patterns, include, url
from zz91tags import views
import settings

urlpatterns = patterns('',
	(r'^$', 'zz91tags.views.default'),
	
	#-----------------------
	
	(r'^tagsInfoList/(?P<tags_id>\d+)/$', 'zz91tags.views.tagsInfoList'),
	(r'^tagsInfoList/(?P<tags_id>\d+)$', 'zz91tags.views.tagsInfoList'),
	(r'^tagsInfoList/(?P<tags_id>\d+)-(?P<page>\d+)/$', 'zz91tags.views.tagsInfoListMore'),
	(r'^tagsInfoList/(?P<tags_id>\d+)-(?P<page>\d+)$', 'zz91tags.views.tagsInfoListMore'),
	(r'^tagsinfolist/(?P<tags_id>\d+)/$', 'zz91tags.views.tagsInfoList'),
	(r'^tagsinfolist/(?P<tags_id>\d+)$', 'zz91tags.views.tagsInfoList'),
	(r'^tagsinfolist/(?P<tags_id>\d+)-(?P<page>\d+)/$', 'zz91tags.views.tagsInfoListMore'),
	(r'^tagsinfolist/(?P<tags_id>\d+)-(?P<page>\d+)$', 'zz91tags.views.tagsInfoListMore'),
	
	(r'^tagssearchList/(?P<keywords>\w+)/$', 'zz91tags.views.tagssearchName'),
	(r'^tagssearchList/(?P<keywords>\w+)$', 'zz91tags.views.tagssearchName'),
	(r'^tagssearchlist/(?P<keywords>\w+)/$', 'zz91tags.views.tagssearchName'),
	(r'^tagssearchlist/(?P<keywords>\w+)$', 'zz91.views.tagssearchName'),
	(r'^tagssearchList/(?P<keywords>\w+)-(?P<page>\d+)/$', 'zz91tags.views.tagssearchList'),
	(r'^tagssearchList/(?P<keywords>\w+)-(?P<page>\d+)$', 'zz91tags.views.tagssearchList'),
	(r'^tagssearchlist/(?P<keywords>\w+)-(?P<page>\d+)/$', 'zz91tags.views.tagssearchList'),
	(r'^tagssearchlist/(?P<keywords>\w+)-(?P<page>\d+)$', 'zz91tags.views.tagssearchList'),
	
	
	
	(r'^tagspriceList/(?P<keywords>\w+)-(?P<page>\d+)/$', 'zz91tags.views.tagspricelistMore'),
	(r'^tagspriceList/(?P<keywords>\w+)-(?P<page>\d+)$', 'zz91tags.views.tagspricelistMore'),
	(r'^tagsbbsList/(?P<keywords>\w+)-(?P<page>\d+)/$', 'zz91tags.views.tagsbbslistMore'),
	(r'^tagsbbsList/(?P<keywords>\w+)-(?P<page>\d+)$', 'zz91tags.views.tagsbbslistMore'),
	(r'^tagspricelist/(?P<keywords>\w+)-(?P<page>\d+)/$', 'zz91tags.views.tagspricelistMore'),
	(r'^tagspricelist/(?P<keywords>\w+)-(?P<page>\d+)$', 'zz91tags.views.tagspricelistMore'),
	(r'^tagsbbslist/(?P<keywords>\w+)-(?P<page>\d+)/$', 'zz91tags.views.tagsbbslistMore'),
	(r'^tagsbbslist/(?P<keywords>\w+)-(?P<page>\d+)$', 'zz91tags.views.tagsbbslistMore'),
	

	
	(r'^a/(?P<keywords>\w+)-(?P<page>\d+)/$', 'zz91tags.views.tagsPriceList'),
	(r'^b/(?P<keywords>\w+)-(?P<page>\d+)/$', 'zz91tags.views.tagsHuzhuList'),
	(r'^d/(?P<keywords>\w+)-(?P<page>\d+)/$', 'zz91tags.views.tagsnewsList'),
	(r'^a/(?P<keywords>\w+)-(?P<page>\d+)$', 'zz91tags.views.tagsPriceList'),
	(r'^b/(?P<keywords>\w+)-(?P<page>\d+)$', 'zz91tags.views.tagsHuzhuList'),
	(r'^d/(?P<keywords>\w+)-(?P<page>\d+)$', 'zz91tags.views.tagsnewsList'),
	(r'^c/(?P<keywords>\w+)-(?P<page>\d+)', 'zz91tags.views.tagsPriceCompanyList'),
	(r'^c/(?P<keywords>\w+)-(?P<page>\d+)/$', 'zz91tags.views.tagsPriceCompanyList'),
	(r'^e/(?P<keywords>\w+)-(?P<page>\d+)$', 'zz91tags.views.tagscompanyList'),
	(r'^e/(?P<keywords>\w+)-(?P<page>\d+)/$', 'zz91tags.views.tagscompanyList'),
	
	(r'^search/a/$', 'zz91tags.views.searckkeyword_hex'),
	(r'^index/(?P<code>\d+)/$', 'zz91tags.views.tagscategory'),
	
	(r'^s/(?P<keywords>\w+)-(?P<page>\d+)/$', 'zz91tags.views.tagsTradeList'),
	(r'^s/(?P<keywords>\w+)-(?P<page>\d+)$', 'zz91tags.views.tagsTradeList'),
	
	(r'^s/(?P<keywords>\w+)-(?P<kind>\d+)-(?P<page>\d+)/$', 'zz91tags.views.tagsTradeList'),
	(r'^s/(?P<keywords>\w+)-(?P<kind>\d+)-(?P<page>\d+)$', 'zz91tags.views.tagsTradeList'),
	(r'^s/(?P<keywords>\w+)/$', 'zz91tags.views.tagsmain'),
	(r'^s/(?P<keywords>\w+)$', 'zz91tags.views.tagsmain'),
	
	(r'^keywordsearch/$', 'zz91tags.views.keywordsearch'),
	(r'^(?!admin)(?P<path>.*)$','django.views.static.serve',{'document_root':settings.STATIC_ROOT}),
)
