﻿from django.conf.urls.defaults import patterns,include,url
import settings

urlpatterns = patterns('seocompanycrm.views',
	(r'^$', 'default'),
	(r'^returnpage/$', 'returnpage'),
	(r'^addcompany/$', 'addcompany'),
	(r'^addcompanyok/$', 'addcompanyok'),
	(r'^company/$', 'company'),
	(r'^keywords/$', 'keywords'),
	(r'^addkeywords/$', 'addkeywords'),
	(r'^addkeywordsok/$', 'addkeywordsok'),
	(r'^updatecompany/$', 'updatecompany'),
	(r'^reductionkeywords/$', 'reductionkeywords'),
	(r'^delkeywords/$', 'delkeywords'),
	(r'^updatekeywords/$', 'updatekeywords'),
	(r'^assigntoseo/$', 'assigntoseo'),
	(r'^choicedelete/$', 'choicedelete'),
	(r'^choicereduction/$', 'choicereduction'),
	(r'^updateranking/$', 'updateranking'),
	(r'^rankinghistory/$', 'rankinghistory'),
	(r'^keywordsremarks/$', 'keywordsremarks'),
	(r'^updateremarks/$', 'updateremarks'),
	(r'^updateremarksok/$', 'updateremarksok'),
	(r'^choicelostcomp/$', 'choicelostcomp'),
	(r'^choicereductioncomp/$', 'choicereductioncomp'),
	(r'^assigntoseocomp/$', 'assigntoseocomp'),
	(r'^delcompany/$', 'delcompany'),
	(r'^reductioncompany/$', 'reductioncompany'),
	(r'^choicelost/$', 'choicelost'),
	(r'^choicereductionlost/$', 'choicereductionlost'),
	(r'^seouser/$', 'addseouser'),
	(r'^addseouserok/$', 'addseouserok'),
	(r'^updateseouser/$', 'updateseouser'),
	(r'^updateseouserok/$', 'updateseouserok'),
	(r'^delseouser/$', 'delseouser'),
	(r'^salesman/$', 'addsalesman'),
	(r'^addsalesmanok/$', 'addsalesmanok'),
	(r'^updatesalesman/$', 'updatesalesman'),
	(r'^updatesalesmanok/$', 'updatesalesmanok'),
	(r'^assigntosales/$', 'assigntosales'),
	(r'^updatepassword/$', 'updatepassword'),
	(r'^updatepasswordok/$', 'updatepasswordok'),
	(r'^contact/$', 'contact'),
	(r'^uppassword/$', 'uppassword'),
)
urlpatterns += patterns('seocompanycrm.useradmin',
	(r'^login/$', 'login'),
	(r'^logout/$', 'logout'),
	(r'^loginpage/$', 'loginpage'),
)

urlpatterns += patterns('',
	(r'^(?!admin)(?P<path>.*)$','django.views.static.serve',{'document_root':settings.STATIC_ROOT}),
)