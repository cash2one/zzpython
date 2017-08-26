from django.conf.urls import patterns,include,url
import settings

urlpatterns = patterns('zz91price.views',
	(r'^cprice/$', 'compricelist'),
	(r'^cprice/p(?P<page>\w+).html$', 'compricelist'),
	(r'^cprice/(?P<searcharg>\w+)/$', 'compricelist'),
	(r'^cprice/(?P<searcharg>\w+)/p(?P<page>\w+).html$', 'compricelist'),
	
	(r'^cprice-(?P<code>\w+)/$', 'compricelist'),
	(r'^cdetail/(?P<cid>\w+).html$', 'compricedetail'),
	(r'^cprice-(?P<code>\w+)/p(?P<page>\w+).html$', 'compricelist'),
	(r'^cprice-(?P<code>\w+)/(?P<searcharg>\w+)/$', 'compricelist'),
	(r'^cprice-(?P<code>\w+)/(?P<searcharg>\w+)/p(?P<page>\w+).html$', 'compricelist'),
	(r'^cpriceindex/$', 'cpriceindex'),
	(r'^cpriceindex$', 'cpriceindex'),
	(r'^companyprice/index.htm$', 'cpriceindex'),
	(r'^$', 'default'),
	(r'^s/pay/$', 'zz91pay'),
	(r'^s/zz91payfirst/$', 'zz91payfirst'),

	(r'^(?P<pinyin>\w+)/$', 'priceindex'),
	(r'^(?P<pinyin>\w+)$', 'priceindex'),

	(r'^(?P<pinyin>\w+)/p-(?P<page>\w+).html$', 'priceindex'),
#	(r'^(?P<pinyin>\w+)/$', 'pricelist'),
#	(r'^(?P<pinyin>\w+)$', 'pricelist'),
	
#	(r'^(?P<type>\w+)-(?P<pinyin>\w+)/$', 'pricelist'),
#	(r'^(?P<type>\w+)-(?P<pinyin>\w+)$', 'pricelist'),
	
#	(r'^(?P<type>\w+)-(?P<pinyin>\w+)/p(?P<page>\w+).html$', 'pricelist'),
	(r'^(?P<pinyin>\w+)/p(?P<page>\w+).html$', 'priceindex'),
	
	(r'^(?P<pinyin>\w+)/a-(?P<areapinyin>\w+)/$', 'pricelist'),
	(r'^(?P<pinyin>\w+)/a-(?P<areapinyin>\w+)/a-(?P<areapinyin2>\w+)/$', 'pricelist'),
	(r'^(?P<pinyin>\w+)/a-(?P<areapinyin>\w+)/a-(?P<areapinyin2>\w+)/p(?P<page>\w+).html$', 'pricelist'),
	(r'^(?P<pinyin>\w+)/a-(?P<areapinyin>\w+)-1/$', 'pricelist_txt'),
	(r'^(?P<pinyin>\w+)/x-(?P<attrpinyin>\w+)-1/$', 'pricelist_txt'),
	(r'^(?P<pinyin>\w+)/a-(?P<areapinyin>\w+)-1/p(?P<page>\w+).html$', 'pricelist_txt'),
	(r'^(?P<pinyin>\w+)/x-(?P<attrpinyin>\w+)-1/p(?P<page>\w+).html$', 'pricelist_txt'),
	(r'^(?P<pinyin>\w+)/x-(?P<attrpinyin>\w+)/$', 'pricelist'),
	(r'^(?P<pinyin>\w+)/t(?P<timedate>\w+)/$', 'pricelist'),
	
	(r'^(?P<pinyin>\w+)/a-(?P<areapinyin>\w+)-1/x-(?P<attrpinyin>\w+)-1/$', 'pricelist_txt'),
	(r'^(?P<pinyin>\w+)/a-(?P<areapinyin>\w+)-1/x-(?P<attrpinyin>\w+)-1/p(?P<page>\w+).html$', 'pricelist_txt'),
	
	(r'^(?P<pinyin>\w+)/a-(?P<areapinyin>\w+)/p(?P<page>\w+).html$', 'pricelist'),
	(r'^(?P<pinyin>\w+)/x-(?P<attrpinyin>\w+)/p(?P<page>\w+).html$', 'pricelist'),
	(r'^(?P<pinyin>\w+)/t(?P<timedate>\w+)/p(?P<page>\w+).html$', 'pricelist'),
	
	(r'^(?P<pinyin>\w+)/a-(?P<areapinyin>\w+)/t(?P<timedate>\w+)/$', 'pricelist'),
	(r'^(?P<pinyin>\w+)/a-(?P<areapinyin>\w+)/t(?P<timedate>\w+)/p(?P<page>\w+).html$', 'pricelist'),
	
	#----最终页汇率
	
	(r'^pricehuilv.html$', 'pricehuilv'),
	(r'^detail/(?P<id>\w+).html$', 'pricedetail'),
	#新版 2016，趋势图
	(r'^detailn/(?P<id>\w+).html$', 'pricedetailn'),
	
	(r'^chart/selectarealabel.html$', 'selectarealabel'),
	
	(r'^chart/(?P<id>\w+).html$', 'pricechart'),
	(r'^chart/(?P<id>\w+)-(?P<page>\w+).html$', 'pricechart'),
	(r'^pricechartdata.html$', 'pricechartdata'),
	(r'^pricecharturl.html$', 'pricecharturl'),
	#----四张走势图
#	(r'^hotchart-(?P<chartnum>\w+).html$', 'hotchart'),
	(r'^hotchart-(?P<chartcid>\w+).html$', 'hotchart'),
	(r'^hotchart-(?P<chartcid>\w+)/p(?P<page>\w+).html$', 'hotchart'),
	(r'^chartdetail.html$', 'chartdetail'),
	(r'^lmechart.html$', 'lmechart'),
	(r'^feitongchart.html$', 'feitongchart'),
	(r'^feibxgchart.html$', 'feibxgchart'),
	(r'^feiqianxinchart.html$', 'feiqianxinchart'),
	#----产品走势图(没用)
	(r'^chartlist.html$', 'default'),
	(r'^chartlist(?P<page>\w+).html$', 'default'),
	(r'^tongji_chart.html$', 'tongji_chart'),
	#----报价搜索页
	(r'^s/$', 'price_search'),
	(r'^s/searchfirst.html$', 'searchfirst'),
	(r'^s/(?P<keywords_hex>\w+)-(?P<type>\w+)/$', 'price_search'),
	(r'^s/(?P<keywords_hex>\w+)-(?P<type>\w+)$', 'price_search'),
	(r'^s/(?P<keywords_hex>\w+)-(?P<type>\w+)/(?P<page>\w+).html$', 'price_search'),
	
	#----企业报价
	(r'^gethexkwd.html$', 'gethexkwd'),
	(r'^getcitylist.html$', 'getcitylist'),
	#(r'^cprice-/$', 'compricelist'),
	#(r'^cprice-/p(?P<page>\w+).html$', 'compricelist'),
	#(r'^cprice-/(?P<searcharg>\w+)/', 'compricelist'),
	#(r'^cprice-/(?P<searcharg>\w+)/p(?P<page>\w+).html$', 'compricelist'),
	
	
	#----企业报价301
	(r'^companyprice/list.htm$', 'cprice301'),
	(r'^companyprice/priceDetails.htm$', 'cprice301'),
	(r'^companyprice/priceDetails(?P<cid>\w+).htm$', 'cprice301'),
	
	
	
	(r'^companyprice/list--(?P<kwd>\w+)--pc--area--t1413244800000--pr.htm$', 'cprice301'),
	
	
	(r'^companyprice/list----pc--area--int--pr.htm$', 'cprice301'),
	(r'^companyprice/list----pc(?P<code>\w+)--area--int--pr.htm$', 'cprice301'),
	(r'^companyprice/list--(?P<kwd>\w+)--pc--area--int--pr.htm$', 'cprice301'),
	(r'^companyprice/list----pc--area--int-(?P<numb>\w+)--pr.htm$', 'cprice301'),
	(r'^companyprice/list----pc--area--int--pr(?P<pr1>\w+)-(?P<pr2>\w+).htm$', 'cprice301'),
	
	(r'^companyprice/list--(?P<kwd>\w+)--pc(?P<code>\w+)--area--int--pr.htm$', 'cprice301'),
	(r'^companyprice/list--(?P<kwd>\w+)--pc--area--int-(?P<numb>\w+)--pr.htm$', 'cprice301'),
	(r'^companyprice/list--(?P<kwd>\w+)--pc--area--int--pr(?P<pr1>\w+)-(?P<pr2>\w+).htm$', 'cprice301'),
	(r'^companyprice/list--(?P<kwd>\w+)--pc(?P<code>\w+)--area--int--pr(?P<pr1>\w+)-(?P<pr2>\w+).htm$', 'cprice301'),
	(r'^companyprice/list----pc(?P<code>\w+)--area--int-(?P<numb>\w+)--pr.htm$', 'cprice301'),
	(r'^companyprice/list----pc(?P<code>\w+)--area--int--pr(?P<pr1>\w+)-(?P<pr2>\w+).htm$', 'cprice301'),
	(r'^companyprice/list----pc--area--int-(?P<numb>\w+)--pr(?P<pr1>\w+)-(?P<pr2>\w+).htm$', 'cprice301'),
	(r'^companyprice/list--(?P<kwd>\w+)--pc(?P<code>\w+)--area--int-(?P<numb>\w+)--pr.htm$', 'cprice301'),
	(r'^companyprice/list--(?P<kwd>\w+)--pc(?P<code>\w+)--area--int-(?P<numb>\w+)--pr(?P<pr1>\w+)-(?P<pr2>\w+).htm$', 'cprice301'),
	(r'^companyprice/list--(?P<kwd>\w+)--pc--area--int-(?P<numb>\w+)--pr(?P<pr1>\w+)-(?P<pr2>\w+).htm$', 'cprice301'),
	(r'^companyprice/list----pc(?P<code>\w+)--area--int-(?P<numb>\w+)--pr(?P<pr1>\w+)-(?P<pr2>\w+).htm$', 'cprice301'),
	#翻页
	(r'^companyprice/list----pc--area--int--pr--s(?P<page>\w+)--l20.htm$', 'cprice301'),
	(r'^companyprice/list----pc(?P<code>\w+)--area--int--pr--s(?P<page>\w+)--l20.htm$', 'cprice301'),
	(r'^companyprice/list--(?P<kwd>\w+)--pc--area--int--pr--s(?P<page>\w+)--l20.htm$', 'cprice301'),
	(r'^companyprice/list----pc--area--int-(?P<numb>\w+)--pr--s(?P<page>\w+)--l20.htm$', 'cprice301'),
	(r'^companyprice/list----pc--area--int--pr(?P<pr1>\w+)-(?P<pr2>\w+)--s(?P<page>\w+)--l20.htm$', 'cprice301'),
	
	(r'^companyprice/list--(?P<kwd>\w+)--pc(?P<code>\w+)--area--int--pr--s(?P<page>\w+)--l20.htm$', 'cprice301'),
	(r'^companyprice/list--(?P<kwd>\w+)--pc(?P<code>\w+)--area--int-(?P<numb>\w+)--pr--s(?P<page>\w+)--l20.htm$', 'cprice301'),
	(r'^companyprice/list--(?P<kwd>\w+)--pc(?P<code>\w+)--area--int--pr(?P<pr1>\w+)-(?P<pr2>\w+)--s(?P<page>\w+)--l20.htm$', 'cprice301'),
	(r'^companyprice/list--(?P<kwd>\w+)--pc(?P<code>\w+)--area--int-(?P<numb>\w+)--pr(?P<pr1>\w+)-(?P<pr2>\w+)--s(?P<page>\w+)--l20.htm$', 'cprice301'),
	(r'^companyprice/list--(?P<kwd>\w+)--pc--area--int-(?P<numb>\w+)--pr--s(?P<page>\w+)--l20.htm$', 'cprice301'),
	(r'^companyprice/list--(?P<kwd>\w+)--pc--area--int--pr(?P<pr1>\w+)-(?P<pr2>\w+)--s(?P<page>\w+)--l20.htm$', 'cprice301'),
	(r'^companyprice/list----pc(?P<code>\w+)--area--int-(?P<numb>\w+)--pr--s(?P<page>\w+)--l20.htm$', 'cprice301'),
	(r'^companyprice/list----pc(?P<code>\w+)--area--int--pr(?P<pr1>\w+)-(?P<pr2>\w+)--s(?P<page>\w+)--l20.htm$', 'cprice301'),
	(r'^companyprice/list----pc--area--int-(?P<numb>\w+)--pr(?P<pr1>\w+)-(?P<pr2>\w+)--s(?P<page>\w+)--l20.htm$', 'cprice301'),
	(r'^companyprice/list--(?P<kwd>\w+)--pc--area--int-(?P<numb>\w+)--pr(?P<pr1>\w+)-(?P<pr2>\w+)--s(?P<page>\w+)--l20.htm$', 'cprice301'),
	(r'^companyprice/list----pc(?P<code>\w+)--area--int-(?P<numb>\w+)--pr(?P<pr1>\w+)-(?P<pr2>\w+)--s(?P<page>\w+)--l20.htm$', 'cprice301'),

	#----301跳转
	(r'^charts/index.htm$', 'price301'),
	(r'^priceList_t(?P<typeid>\w+)_metal.htm$', 'price301'),
	(r'^priceList_a(?P<typeid>\w+)_metal.htm$', 'price301'),
	(r'^priceList_t40_a(?P<typeid>\w+)_metal.htm$', 'price301'),
	(r'^moreList_p3_t(?P<typeid>\w+)_metal.htm$', 'price301'),
	(r'^moreList_p17_a(?P<typeid>\w+)_metal.htm$', 'price301'),
	(r'^moreList_p(?P<typeid>\w+)_metal.htm$', 'price301'),
	
	(r'^priceList_t(?P<typeid>\w+)_plastic.htm$', 'price301'),
	(r'^priceList_a(?P<typeid>\w+)_plastic.htm$', 'price301'),
	(r'^priceList_t40_a(?P<typeid>\w+)_plastic.htm$', 'price301'),
	(r'^moreList_p(?P<typeid>\w+)_plastic.htm$', 'price301'),
	
	(r'^priceList_t(?P<typeid>\w+)_paper.htm$', 'price301'),
	(r'^moreList_p(?P<typeid>\w+)_paper.htm$', 'price301'),
	
	(r'^priceDetails_(?P<id>\w+)_paper.htm$', 'pricedetail301'),
	(r'^priceDetails_(?P<id>\w+).htm$', 'pricedetail301'),
	
	#翻页
	(r'^priceList_t_p_a(?P<typeid>\w+)_c_metal--s(?P<page>\w+)--(?P<page1>\w+).htm$', 'price301'),
	(r'^priceList_t_p_a(?P<typeid>\w+)_c_plastic--s(?P<page>\w+)--(?P<page1>\w+).htm$', 'price301'),
	(r'^priceList_t_p_a(?P<typeid>\w+)_c_paper--s(?P<page>\w+)--(?P<page1>\w+).htm$', 'price301'),
	
	(r'^priceList_t(?P<typeid>\w+)_p_a_c_metal--s(?P<page>\w+)--(?P<page1>\w+).htm$', 'price301'),
	(r'^priceList_t(?P<typeid>\w+)_p_a_c_plastic--s(?P<page>\w+)--(?P<page1>\w+).htm$', 'price301'),
	(r'^priceList_t(?P<typeid>\w+)_p_a_c_paper--s(?P<page>\w+)--(?P<page1>\w+).htm$', 'price301'),
	(r'^sitemap.html$', 'sitemap'),
	#自主报价
	(r'^selfprice.html$','selfpricelist'),
	(r'^selfprice/s(?P<page>\d*).html$','selfpricelist'),
	(r'^selfprice/c(?P<category>\w+)/$','selfpricelist'),
	(r'^selfprice/c(?P<category>\w+)/s(?P<page>\d*).html$','selfpricelist'),
	
	(r'^selfprice/k(?P<searchKey>\w+)/$','selfpricelist'),
	(r'^selfprice/k(?P<searchKey>\w+)/s(?P<page>\d*).html$','selfpricelist'),
	
	(r'^selfprice/k(?P<searchKey>\w*)/c(?P<category>\w*)/$','selfpricelist'),
	(r'^selfprice/k(?P<searchKey>\w*)/c(?P<category>\w*)/s(?P<page>\d*).html$','selfpricelist'),
	(r'^preview/(?P<id>\d+).html$','preview'),
	(r'^follow.html$','follow'),
	(r'^download/(?P<id>\d*).html$','download'),
	(r'^notice.html$','notice'),
	(r'^submitCallback.html$','submitCallback'),
	
)
#----行情研究院
urlpatterns += patterns('zz91price.study',
	(r'^study/$', 'index'),
    (r'^study/index.html$', 'index'),
    (r'^study/detail(?P<id>\d+).html$', 'detail'),
    (r'^study/(?P<type>\w+)/$', 'list'),
    (r'^study/(?P<type>\w+)/p(?P<page>\d*).html$', 'list'),
    (r'^study/(?P<type>\w+)$', 'list'),
    (r'^study/(?P<type>\w+)/(?P<type1>\w+)/p(?P<page>\d*).html$', 'list'),
    (r'^study/(?P<type>\w+)/(?P<type1>\w+)/$', 'list'),
    (r'^study/(?P<type>\w+)/(?P<type1>\w+)$', 'list'),
    (r'^study/(?P<type>\w+)/detail(?P<id>\d+).html$', 'detail'),
    (r'^study/(?P<type>\w+)/(?P<type1>\w+)/detail(?P<id>\d+).html$', 'detail'),
    
    (r'^study/indexlistjson.html$', 'indexlistjson'),
    
    
    
)
urlpatterns += patterns('',
	(r'^(?!admin)(?P<path>.*)$','django.views.static.serve',{'document_root':settings.STATIC_ROOT}),
)