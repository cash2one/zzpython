from django.conf.urls import patterns, include, url
import settings
# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
	(r'^$', 'adminasto.views.default'),
	(r'searchcomplist/$', 'adminasto.views.searchcomplist'),
	(r'sms_searchcomp/$', 'adminasto.views.sms_searchcomp'),
	(r'serverhistory/$', 'adminasto.views.serverhistory'),
	
	(r'service/main.html$', 'adminasto.views.servicemain'),
	(r'service/ad.html$', 'adminasto.views.servicead'),
	(r'service/other.html$', 'adminasto.views.serviceother'),
	
	
	(r'companyadd/$', 'adminasto.views.companyadd'),
	(r'companysave/$', 'adminasto.views.companysave'),
	(r'compsq/$', 'adminasto.views.companysq'),
	(r'openConfirm/$', 'adminasto.views.openConfirm'),
	(r'openConfirm1/$', 'adminasto.views.openConfirm1'),
	(r'openConfirmsave/$', 'adminasto.views.openConfirmsave'),
	(r'openConfirmsave1/$', 'adminasto.views.openConfirmsave1'),
	(r'daohangadd/$', 'adminasto.daohang_admin.daohangadd'),
	(r'daohangsave/$', 'adminasto.daohang_admin.daohangsave'),
	(r'daohangdel/$', 'adminasto.daohang_admin.daohangdel'),
	(r'cscomp/$', 'adminasto.daohang_admin.cscomp'),
	(r'directupload/$', 'adminasto.daohang_admin.directupload'),
	(r'getCsuserName/$', 'adminasto.views.getCsuserName'),
	(r'tomcatmanager/$', 'adminasto.views.tomcatmanager'),
	(r'tomcatadd/$', 'adminasto.views.tomcatadd'),
	(r'tomcatsave/$', 'adminasto.views.tomcatsave'),
	(r'subjectbaoming9090/$', 'adminasto.views.subjectbaoming'),
	(r'subjectbaoming_ldb/$', 'adminasto.views.subjectbaoming2'),
	(r'crm_offerlist/$', 'adminasto.views.crm_offerlist'),
	(r'getesitecount/$', 'adminasto.views.getesitecount'),
	(r'saveseocompany/$', 'adminasto.views.saveseocompany'),
	(r'tongji.html$', 'adminasto.views.tongji'),
	(r'tongji_chart.html$', 'adminasto.views.tongji_chart'),
	(r'shuliaozst/$', 'adminasto.views.shuliaozst'),
	(r'outmobilelist/$', 'adminasto.views.outmobilelist'),
	(r'outzstcomplist/$', 'adminasto.views.outzstcomplist'),
	
	#微信点击统计
	(r'weixintongji/$', 'adminasto.views.weixintongji'),
	
	(r'companylist/$', 'adminasto.views.companylist'),
	
	
	(r'ppcindex/$', 'adminasto.views.ppcindex'),
	(r'ppc/plist/$', 'adminasto.views.ppcproducts'),
	(r'ppc/sendlist/$', 'adminasto.views.sendlist'),
	(r'ppc/sendadd/$', 'adminasto.views.sendadd'),
	(r'ppc/sendsave/$', 'adminasto.views.sendsave'),
	(r'ppc/senddetail/$', 'adminasto.views.senddetail'),
	
	(r'indexdata/$', 'adminasto.daohang_admin.indexdata'),
	(r'indexdatamain/$', 'adminasto.daohang_admin.indexdatamain'),
	(r'index-data-add/$', 'adminasto.daohang_admin.indexdataadd'),
	(r'index-data-add-more/$', 'adminasto.daohang_admin.indexdatamoreadd'),
	
	(r'pricecategorymain/$', 'adminasto.daohang_admin.pricecategorymain'),
	(r'pricecategorysave/$', 'adminasto.daohang_admin.pricecategorysave'),
	
	(r'seo/seotempmanager/$', 'adminasto.views.seotempmanager'),
	(r'seo/templatesave/$', 'adminasto.views.templatesave'),
	
	(r'sendsms.html$', 'adminasto.views.sendsms'),
	(r'sendsmsflag.html$', 'adminasto.views.sendsmsflag'),
	(r'saveactive_flag.html$', 'adminasto.views.saveactive_flag'),
	
	
	(r'^(?!admin)(?P<path>.*)$','django.views.static.serve',{'document_root':settings.STATIC_ROOT}),
	
)
