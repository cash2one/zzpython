#-*- coding:utf-8 -*-
#from django.conf.urls.defaults import *
#from django.conf.urls.defaults import patterns,include,url
from django.conf.urls import patterns, include, url
import settings
urlpatterns = patterns('',
	(r'^trade/$', 'zz91search.java_productslist.default'),
	(r'^trade$', 'zz91search.java_productslist.default'),
	(r'^trade/companyinfo.htm$', 'zz91search.java_productslist.companyinfo'),
	(r'^trade/key(?P<code>\w+).html$', 'zz91search.java_productslist.procode'),
	(r'^trade/companyinfos.htm$', 'zz91search.java_productslist.companyinfos'),
	(r'^trade/categoryinfo.htm$', 'zz91search.java_productslist.categoryinfo'),
	(r'^trade/metal.htm$', 'zz91search.java_productslist.metal'),
	(r'^trade/plastic.htm$', 'zz91search.java_productslist.plastic'),
	(r'^trade/comprehensive.htm$', 'zz91search.java_productslist.comprehensive'),
	(r'^trade/searchfirst/$', 'zz91search.java_productslist.searchfirst'),
	(r'^trade/commoncustomer.html$', 'zz91search.java_productslist.commoncustomer'),
	(r'^trade/searchfirstcommon/$', 'zz91search.java_productslist.searchfirstcommon'),
	(r'^trade/commonlist/c-(?P<keywords>\w+)-(?P<page>\d+).html$', 'zz91search.java_productslist.commoncustomermore'),
	(r'^trade/s-(?P<keywords>\w+).html$', 'zz91search.java_productslist.tradelist'),
	(r'^trade/offerlist.html$', 'zz91search.java_productslist.offerlist'),
	(r'^trade/hiturl.html$', 'zz91search.java_productslist.hiturl'),
	(r'^trade/yuanliaolist.html$', 'zz91search.java_productslist.yuanliaolist'),#测试获得当前供求关键字下的原料供求
	(r'^pic/(?P<products_id>\d+).html$', 'zz91search.java_productslist.tradepic'),
	(r'^(?!admin)(?P<path>.*)$','django.views.static.serve',{'document_root':settings.STATIC_ROOT}),
	
) 
