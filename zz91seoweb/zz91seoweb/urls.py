from django.conf.urls import *
import settings,sys
reload(sys)
sys.setdefaultencoding('UTF-8')
# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'zz91seoweb.views.home', name='home'),
    # url(r'^zz91seoweb/', include('zz91seoweb.foo.urls')),
    (r'^$', 'zz91seoweb.views.default'),
    (r'^about.html$', 'zz91seoweb.views.about'),
    (r'^products-(?P<seriesid>\d+)-(?P<page>\d+).html$', 'zz91seoweb.views.products'),
    (r'^news-(?P<page>\d+).html$', 'zz91seoweb.views.news'),
    (r'^n(?P<id>\d+).html$', 'zz91seoweb.views.newsdetail'),
    (r'^p(?P<id>\d+).html$', 'zz91seoweb.views.productsdetail'),
    (r'^contact.html$', 'zz91seoweb.views.contact'),
    (r'^certificate.html$', 'zz91seoweb.views.certificate'),
    (r'^leavewords.html$', 'zz91seoweb.views.leavewords'),
    (r'^leavewords_save.html$', 'zz91seoweb.views.leavewords_save'),
    (r'^robots.txt$', 'zz91seoweb.views.robots'),

    #----2014ppc
    (r'^ppc/$', 'zz91seoweb.views_ppc.index'),
    (r'^ppc/404.xml', 'zz91seoweb.views.page404'),
    (r'^ppc/ppctrade.htm$', 'zz91seoweb.views_ppc.ppctrade'),
    (r'^ppc/ppcexperience.htm$', 'zz91seoweb.views_ppc.ppcexperience'),
    (r'^ppc/ppcexperience2.htm$', 'zz91seoweb.views_ppc.ppcexperience2'),
    (r'^ppc/ppcexperience3.htm$', 'zz91seoweb.views_ppc.ppcexperience3'),
    (r'^ppc/ppcexperience4.htm$', 'zz91seoweb.views_ppc.ppcexperience4'),
    (r'^ppc/ppcexperience5.htm$', 'zz91seoweb.views_ppc.ppcexperience5'),
    (r'^ppc/ppcexperience6.htm$', 'zz91seoweb.views_ppc.ppcexperience6'),
    (r'^ppc/ppcexperience7.htm$', 'zz91seoweb.views_ppc.ppcexperience7'),
    
    (r'^ppc/index(?P<company_id>\d+).htm$', 'zz91seoweb.views_ppc.default'),
    (r'^ppc/gsjj(?P<company_id>\d+).htm$', 'zz91seoweb.views_ppc.about'),
    (r'^ppc/contact(?P<company_id>\d+).htm$', 'zz91seoweb.views_ppc.contact'),
    (r'^ppc/zxgq(?P<company_id>\d+).htm$', 'zz91seoweb.views_ppc.productsmain'),
    (r'^ppc/products(?P<company_id>\d+)-(?P<seriesid>\d+)-(?P<page>\d+).htm$', 'zz91seoweb.views_ppc.products'),
    (r'^ppc/productdetail(?P<id>\d+).htm$', 'zz91seoweb.views_ppc.productsdetail'),
    (r'^ppc/yuanliaodetail(?P<id>\d+).htm$', 'zz91seoweb.views_ppc.yuanliaodetail'),#原料详细页
    (r'^ppc/newsdetail(?P<id>\d+).htm$', 'zz91seoweb.views_ppc.newsdetail'),
    (r'^ppc/gsdt(?P<company_id>\d+).htm$', 'zz91seoweb.views_ppc.newsmain'),
    (r'^ppc/gsxc(?P<company_id>\d+).htm$', 'zz91seoweb.views_ppc.companypic'),
    (r'^ppc/news(?P<company_id>\d+)-(?P<page>\d+).htm$', 'zz91seoweb.views_ppc.news'),
    (r'^ppc/news-(?P<page>\d+).htm$', 'zz91seoweb.views.news'),
    (r'^ppc/renzheng(?P<company_id>\d+).htm$', 'zz91seoweb.views_ppc.renzheng'),
    
    #手机站
    (r'^mobile/index(?P<company_id>\d+).htm$', 'zz91seoweb.views_mobile.mobiledefault'),
    (r'^mobile/about(?P<company_id>\d+).htm$', 'zz91seoweb.views_mobile.about'),
    (r'^gsjs.htm$', 'zz91seoweb.views_mobile.mabout'),
    (r'^lxfs.htm$', 'zz91seoweb.views_mobile.mcontact'),
    (r'^zxgq.htm$', 'zz91seoweb.views_mobile.mproductsmain'),
    (r'^products(?P<id>\d+).htm$', 'zz91seoweb.views_mobile.productsdetail'),
    
    (r'^mobile/contact(?P<company_id>\d+).htm$', 'zz91seoweb.views_mobile.contact'),
    (r'^mobile/productsmore(?P<company_id>\d+)-(?P<page>\d+).htm$', 'zz91seoweb.views_mobile.productsmore'),
    (r'^mobile/zxgq(?P<company_id>\d+).htm$', 'zz91seoweb.views_mobile.productsmain'),
    (r'^mobile/products(?P<company_id>\d+)-(?P<seriesid>\d+)-(?P<page>\d+).htm$', 'zz91seoweb.views_mobile.products'),
    (r'^mobile/products(?P<company_id>\d+)-(?P<page>\d+).htm$', 'zz91seoweb.views_mobile.productslist'),
    (r'^mobile/productdetail(?P<id>\d+).htm$', 'zz91seoweb.views_mobile.productsdetail'),
    (r'^news(?P<id>\d+).htm$', 'zz91seoweb.views_mobile.newsdetail'),
    (r'^mobile/newsdetail(?P<id>\d+).htm$', 'zz91seoweb.views_mobile.newsdetail'),
    (r'^mobile/credit(?P<company_id>\d+).htm$', 'zz91seoweb.views_mobile.credit'),
    (r'^mobile/company_profile(?P<company_id>\d+).htm$', 'zz91seoweb.views_mobile.company_profile'),
    (r'^mobile/gsdt(?P<company_id>\d+).htm$', 'zz91seoweb.views_mobile.newsmain'),
    (r'^mobile/news(?P<page>\d+).htm$', 'zz91seoweb.views.news'),

    # 新版手机站
    (r'^m/(?P<company_id>\d+).html$', 'zz91seoweb.new_mobile_2017.index'), # 手机站首页
    (r'^m/about(?P<company_id>\d+).html$', 'zz91seoweb.new_mobile_2017.about'), # 手机站-公司简介
    (r'^m/contact(?P<company_id>\d+).html$', 'zz91seoweb.new_mobile_2017.contact'), # 手机站-联系我们
    (r'^m/news(?P<company_id>\d+)-(?P<page>\d+).html$', 'zz91seoweb.new_mobile_2017.news'), # 手机站-公司动态
    (r'^m/newsdetail(?P<nid>\d+).html$', 'zz91seoweb.new_mobile_2017.news_detail'), # 手机站-公司动态详细页面
    (r'^m/products(?P<company_id>\d+)-(?P<page>\d+).html$', 'zz91seoweb.new_mobile_2017.products'), # 手机站-供求信息列表页
    (r'^m/products(?P<company_id>\d+)-(?P<seriesid>\d+)-(?P<page>\d+).html$', 'zz91seoweb.new_mobile_2017.products'),
    (r'^m/productdetail(?P<pid>\d+).html$', 'zz91seoweb.new_mobile_2017.products_detail'), # 手机站-供求信息详细页面
    (r'^m/address(?P<company_id>\d+).html$', 'zz91seoweb.new_mobile_2017.address'),  # 手机站-显示地址的地图

    
    # 推荐页面
    (r'^ppc/(?P<pinyin>\w+)/$', 'zz91seoweb.views_ppc.tuijian'),
    (r'^ppc/(?P<pinyin>\w+)$', 'zz91seoweb.views_ppc.tuijian'),
    (r'^ppc/(?P<pinyin>\w+)/p(?P<page>\d+).htm$', 'zz91seoweb.views_ppc.tuijian'),
    (r'^ppc/(?P<pinyin>\w+)/t(?P<pdt_type>\d*).htm$', 'zz91seoweb.views_ppc.tuijian'),
    (r'^ppc/(?P<pinyin>\w+)/t(?P<pdt_type>\d*)-p(?P<page>\d+).htm$', 'zz91seoweb.views_ppc.tuijian'),
    (r'^ppc/s-(?P<keyword>\w+)/$', 'zz91seoweb.views_ppc.tuijian'),
    (r'^ppc/s-(?P<keyword>\w+)$', 'zz91seoweb.views_ppc.tuijian'),
    (r'^ppc/s-(?P<keyword>\w+)/p(?P<page>\d+).htm$', 'zz91seoweb.views_ppc.tuijian'),
    (r'^ppc/s-(?P<keyword>\w+)/t(?P<pdt_type>\d*).htm$', 'zz91seoweb.views_ppc.tuijian'),
    (r'^ppc/s-(?P<keyword>\w+)/t(?P<pdt_type>\d*)-p(?P<page>\d+).htm$', 'zz91seoweb.views_ppc.tuijian'),
    
    # 搜索中间跳转页
    (r'^ppc/s/searchfirst/$', 'zz91seoweb.views_ppc.searchfirst'),
    
    (r'^weixin.htm$', 'zz91seoweb.weixin.default'),
    #企业秀
    (r'^xiu/(?P<company_id>\d+).html$', 'zz91seoweb.views.mobileqiyexiu'),
    #访问来源
    (r'^ppc/tongji.html$', 'zz91seoweb.views_ppc.tongji'),
    #seo客户推广
    (r'^comp/(?P<pingyin>\w+).html$', 'zz91seoweb.seo.company'),
    (r'^c-(?P<pingyin>\w+).html$', 'zz91seoweb.seo.companynew'),
    (r'^comp/jsproducts.js$', 'zz91seoweb.seo.jsproducts'),
    
    (r'^(?!admin)(?P<path>.*)$','django.views.static.serve',{'document_root':settings.STATIC_ROOT}),
)
handler404 = 'zz91seoweb.views.viewer_404'
handler500 = 'zz91seoweb.views.viewer_500'
