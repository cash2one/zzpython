from django.conf.urls import patterns, include, url
#from zz91cp import views
import settings
# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
	(r'^index.html$', 'zz91cp.views.index'),#微门户首页
	(r'^cp/$', 'zz91cp.views.default'),
	(r'^cp/reg.html$', 'zz91cp.views.reg'),
	(r'^cp/(?P<pingyin>\w+)$', 'zz91cp.views.cp'),
	(r'^cp/(?P<pingyin>\w+)/$', 'zz91cp.views.cp'),
	(r'^cp/(?P<pingyin>\w+)/price.html$', 'zz91cp.views.price'),#价格
	(r'^cp/(?P<pingyin>\w+)/pricemore-(?P<page>\d+).html$', 'zz91cp.views.pricemore'),#更多价格
	(r'^cp/(?P<pingyin>\w+)/company.html$', 'zz91cp.views.company'),#商家
	(r'^cp/(?P<pingyin>\w+)/companymore-(?P<page>\d+).html$', 'zz91cp.views.companymore'),#更多商家
	(r'^cp/(?P<pingyin>\w+)/trade.html$', 'zz91cp.views.trade'),#供求
	(r'^cp/(?P<pingyin>\w+)/trademore-(?P<page>\d+).html$', 'zz91cp.views.trademore'),#更多供求
	(r'^cp/(?P<pingyin>\w+)/picture.html$', 'zz91cp.views.picture'),#图片
	(r'^cp/(?P<pingyin>\w+)/picturemore-(?P<page>\d+).html$', 'zz91cp.views.picturemore'),#更多图片
	(r'^cp/(?P<pingyin>\w+)/huzhu.html$', 'zz91cp.views.huzhu'),#互助
	(r'^cp/(?P<pingyin>\w+)/huzhumore-(?P<page>\d+).html$', 'zz91cp.views.huzhumore'),#更多互助
	(r'^cp/(?P<pingyin>\w+)/news.html$', 'zz91cp.views.news'),#资讯
	(r'^cp/(?P<pingyin>\w+)/news-(?P<page>\d+).html$', 'zz91cp.views.news'),#更多资讯
	(r'outzstcomplist/a/$', 'zz91cp.views.outzstcomplist'),
	#老站新闻
	(r'^news/news(?P<newsid>\d+).html$', 'zz91cp.news.newsdetail'),
	(r'^news/bbs(?P<newsid>\d+).html$', 'zz91cp.news.bbsdetail'),
	(r'^news/guanzhu(?P<newsid>\d+).html$', 'zz91cp.news.guanzhudetail'),
	(r'^news/newslist-(?P<keywords>\w+)-(?P<page>\d+).html$', 'zz91cp.news.newslist'),
	(r'^news/newssearchfirst.html$', 'zz91cp.news.newssearchfirst'),
	(r'^news/newsindex.html$', 'zz91cp.news.newsindex'),
	(r'^news/$', 'zz91cp.news.newsindex'),
	(r'^cp/prosearch.html$', 'zz91cp.views.prosearch'),
	(r'^cp/pro-(?P<keywords>\w+).html$', 'zz91cp.views.prolist'),
	(r'^cp/pro-(?P<keywords>\w+)-(?P<page>\d+).html$', 'zz91cp.views.prolist'),
	(r'^cp/firm-(?P<keywords>\w+).html$', 'zz91cp.views.firm'),
	(r'^cp/firm-(?P<keywords>\w+)-(?P<page>\d+).html$', 'zz91cp.views.firm'),
	(r'^cp/price-(?P<keywords>\w+).html$', 'zz91cp.views.pro_price'),
	(r'^cp/price-(?P<keywords>\w+)-(?P<page>\d+).html$', 'zz91cp.views.pro_price'),
	#优质客户推荐
	(r'^carveout/$', 'zz91cp.views.carveout'),
	(r'^carveout/plastic.html$', 'zz91cp.views.carveout'),
	(r'^carveout/c-(?P<keywords>\w+)-(?P<page>\d+).html$', 'zz91cp.views.carveoutmore'),
	#微信开春推广
	(r'^weixin2014/$', 'zz91cp.views.weixin2014'),
	(r'^cp/pricetable.html$', 'zz91cp.views.pricetable'),
	#普通客户推荐
	(r'^common/$', 'zz91cp.views.commoncustomer'),
	(r'^common/plastic.html$', 'zz91cp.views.commoncustomer'),
	# 商机排行榜
	(r'^cp/sj-index.html$', 'zz91cp.shangji.index'),
	(r'^cp/sj-hotcp.html$', 'zz91cp.shangji.hot_cp'),
	(r'^cp/sj-sjbd.html$', 'zz91cp.shangji.sj_billboard'),
	(r'^cp/sj-spbd.html$', 'zz91cp.shangji.esite_billboard'),
	(r'^cp/sj-sjbd-more.html', 'zz91cp.shangji.sj_bd_more'),
	(r'^cp/sj-sjbd-more-(?P<page>\d+).html$', 'zz91cp.shangji.sj_bd_more_2'),
	(r'^cp/sj-spbd-more.html', 'zz91cp.shangji.sp_bd_more'),
	(r'^cp/sj-spbd-more-(?P<page>\d+).html$', 'zz91cp.shangji.sp_bd_more_2'),

	(r'^common/c-(?P<keywords>\w+)-(?P<page>\d+).html$', 'zz91cp.views.commoncustomermore'),
	(r'^cp/(?!admin)(?P<path>.*)$','django.views.static.serve',{'document_root':settings.STATIC_ROOT}),
	(r'^(?!admin)(?P<path>.*)$','django.views.static.serve',{'document_root':settings.STATIC_ROOT}),
	
)


handler404 = 'zz91cp.views.viewer_404'
handler500 = 'zz91cp.views.viewer_500'
