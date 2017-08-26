from django.conf.urls.defaults import *
from zz91 import views
import settings

urlpatterns = patterns('',
	(r'^$', 'zz91.daohang.default'),
	(r'^index1.html$', 'zz91.daohang.newdefault'),
	(r'^(?P<pingyin>\w+)/$', 'zz91.daohang.daohangdetail'),
	(r'^(?P<pingyin>\w+)$', 'zz91.daohang.daohangdetail'),
	(r'^vblogin/login/$', 'zz91.daohang.vblogin'),
	(r'^jgjmsginfo/msg/$', 'zz91.daohang.jgjmsginfo'),
	(r'^guijinshuoferlist.html$', 'zz91.daohang.guijinshuoferlist'),
	(r'^guijinshupricelist.html$', 'zz91.daohang.guijinshupricelist'),
	(r'^guijinshupricelist1.html$', 'zz91.daohang.guijinshupricelist1'),
	#photo
	
	(r'^photo/index.htm$', 'zz91.daohang.photoindex'),
	(r'^photo/searchPic-(?P<keywords>\w+).htm$', 'zz91.daohang.photolist'),
	
	
	#seo客户推广
	(r'^comp/(?P<pingyin>\w+).html$', 'zz91.seo.company'),
	(r'^c-(?P<pingyin>\w+).html$', 'zz91.seo.companynew'),
	(r'^comp/jsproducts.js$', 'zz91.seo.jsproducts'),
	
	#-----------------------
	
	(r'^tagsInfoList/(?P<tags_id>\d+)/$', 'zz91.views.tagsInfoList'),
	(r'^tagsInfoList/(?P<tags_id>\d+)$', 'zz91.views.tagsInfoList'),
	(r'^tagsInfoList/(?P<tags_id>\d+)-(?P<page>\d+)/$', 'zz91.views.tagsInfoListMore'),
	(r'^tagsInfoList/(?P<tags_id>\d+)-(?P<page>\d+)$', 'zz91.views.tagsInfoListMore'),
	(r'^tagsinfolist/(?P<tags_id>\d+)/$', 'zz91.views.tagsInfoList'),
	(r'^tagsinfolist/(?P<tags_id>\d+)$', 'zz91.views.tagsInfoList'),
	(r'^tagsinfolist/(?P<tags_id>\d+)-(?P<page>\d+)/$', 'zz91.views.tagsInfoListMore'),
	(r'^tagsinfolist/(?P<tags_id>\d+)-(?P<page>\d+)$', 'zz91.views.tagsInfoListMore'),
	
	(r'^tagssearchList/(?P<keywords>\w+)/$', 'zz91.views.tagssearchName'),
	(r'^tagssearchList/(?P<keywords>\w+)$', 'zz91.views.tagssearchName'),
	(r'^tagssearchlist/(?P<keywords>\w+)/$', 'zz91.views.tagssearchName'),
	(r'^tagssearchlist/(?P<keywords>\w+)$', 'zz91.views.tagssearchName'),
	(r'^tagssearchList/(?P<keywords>\w+)-(?P<page>\d+)/$', 'zz91.views.tagssearchList'),
	(r'^tagssearchList/(?P<keywords>\w+)-(?P<page>\d+)$', 'zz91.views.tagssearchList'),
	(r'^tagssearchlist/(?P<keywords>\w+)-(?P<page>\d+)/$', 'zz91.views.tagssearchList'),
	(r'^tagssearchlist/(?P<keywords>\w+)-(?P<page>\d+)$', 'zz91.views.tagssearchList'),
	
	
	
	(r'^tagspriceList/(?P<keywords>\w+)-(?P<page>\d+)/$', 'zz91.views.tagspricelistMore'),
	(r'^tagspriceList/(?P<keywords>\w+)-(?P<page>\d+)$', 'zz91.views.tagspricelistMore'),
	(r'^tagsbbsList/(?P<keywords>\w+)-(?P<page>\d+)/$', 'zz91.views.tagsbbslistMore'),
	(r'^tagsbbsList/(?P<keywords>\w+)-(?P<page>\d+)$', 'zz91.views.tagsbbslistMore'),
	(r'^tagspricelist/(?P<keywords>\w+)-(?P<page>\d+)/$', 'zz91.views.tagspricelistMore'),
	(r'^tagspricelist/(?P<keywords>\w+)-(?P<page>\d+)$', 'zz91.views.tagspricelistMore'),
	(r'^tagsbbslist/(?P<keywords>\w+)-(?P<page>\d+)/$', 'zz91.views.tagsbbslistMore'),
	(r'^tagsbbslist/(?P<keywords>\w+)-(?P<page>\d+)$', 'zz91.views.tagsbbslistMore'),
	
	#(r'^a/(?P<keywords>\w+)-(?P<page>\d+)/$', 'zz91.views.tagspricelistMore_hex'),
	#(r'^b/(?P<keywords>\w+)-(?P<page>\d+)/$', 'zz91.views.tagsbbslistMore_hex'),
	#(r'^a/(?P<keywords>\w+)-(?P<page>\d+)$', 'zz91.views.tagspricelistMore_hex'),
	#(r'^b/(?P<keywords>\w+)-(?P<page>\d+)$', 'zz91.views.tagsbbslistMore_hex'),
	
	(r'^a/(?P<keywords>\w+)-(?P<page>\d+)/$', 'zz91.views.tagsPriceList'),
	(r'^b/(?P<keywords>\w+)-(?P<page>\d+)/$', 'zz91.views.tagsHuzhuList'),
	(r'^d/(?P<keywords>\w+)-(?P<page>\d+)/$', 'zz91.views.tagsnewsList'),
	(r'^a/(?P<keywords>\w+)-(?P<page>\d+)$', 'zz91.views.tagsPriceList'),
	(r'^b/(?P<keywords>\w+)-(?P<page>\d+)$', 'zz91.views.tagsHuzhuList'),
	(r'^d/(?P<keywords>\w+)-(?P<page>\d+)$', 'zz91.views.tagsnewsList'),
	(r'^c/(?P<keywords>\w+)-(?P<page>\d+)/$', 'zz91.views.tagsPriceCompanyList'),
	(r'^c/(?P<keywords>\w+)-(?P<page>\d+)/$', 'zz91.views.tagsPriceCompanyList'),
	
	(r'^search/a/$', 'zz91.views.searckkeyword_hex'),
	
	#(r'^s/(?P<keywords>\w+)/$', 'zz91.views.tagssearchName_hex'),
	#(r'^s/(?P<keywords>\w+)$', 'zz91.views.tagssearchName_hex'),
	(r'^s/(?P<keywords>\w+)-(?P<page>\d+)/$', 'zz91.views.tagssearchList_hex'),
	(r'^s/(?P<keywords>\w+)-(?P<page>\d+)$', 'zz91.views.tagssearchList_hex'),
	
	(r'^s/(?P<keywords>\w+)-(?P<kind>\d+)-(?P<page>\d+)/$', 'zz91.views.tagsTradeList'),
	(r'^s/(?P<keywords>\w+)-(?P<kind>\d+)-(?P<page>\d+)$', 'zz91.views.tagsTradeList'),
	(r'^s/(?P<keywords>\w+)/$', 'zz91.views.tagsmain'),
	(r'^s/(?P<keywords>\w+)$', 'zz91.views.tagsmain'),
	
	(r'^keywordsearch/$', 'zz91.views.keywordsearch'),
	(r'^(?!admin)(?P<path>.*)$','django.views.static.serve',{'document_root':settings.STATIC_ROOT}),
)
