from django.conf.urls import *
import settings

urlpatterns = patterns('bsteelmanagement.views',
	(r'^bssteel/$', 'default'),
	(r'^bssteel/tokeninfo.html$', 'tokeninfo'),
	(r'^bssteel/get_token.html$', 'get_token'),
	
	(r'^bssteel/adminindex.html$', 'adminindex'),
	(r'^bssteel/upload.html$', 'upload'),
	(r'^dialogs/image/image.html$', 'uploadimg'),
	(r'^bssteel/returnpage.html$', 'returnpage'),
	(r'^bssteel/arttype.html$', 'arttype'),
	(r'^bssteel/addarttype.html$', 'addarttype'),
	(r'^bssteel/artical.html$', 'artical'),
	(r'^bssteel/reduction.html$', 'reduction'),
	(r'^bssteel/redelartical.html$', 'redelartical'),
	(r'^bssteel/delartical.html$', 'delartical'),
	(r'^bssteel/addarttypeok.html$', 'addarttypeok'),
	(r'^bssteel/updatetype.html$', 'updatetype'),
	(r'^bssteel/updatetypeok.html$', 'updatetypeok'),
	(r'^bssteel/deletetype.html$', 'deletetype'),
	(r'^bssteel/addartical.html$', 'addartical'),
	(r'^bssteel/updateartical.html$', 'updateartical'),
	(r'^bssteel/addarticalok.html$', 'addarticalok'),
	(r'^bssteel/articallist.html$', 'articallist'),
	(r'^bssteel/p(?P<page>\w+).htm$', 'articallist'),
	(r'^bssteel/articaldetail(?P<id>\d+).htm$', 'articaldetail'),
    (r'^bssteel/articaldetail(?P<id>\d+)-(?P<page>\w+).htm$', 'articaldetail'),
    
)
urlpatterns += patterns('bsteelmanagement.useradmin',
	(r'^bssteel/login.html$', 'login'),
	(r'^bssteel/logout.html$', 'logout'),
	(r'^bssteel/loginpage.html$', 'loginpage'),
)

urlpatterns += patterns('',
	(r'^(?!admin)(?P<path>.*)$','django.views.static.serve',{'document_root':settings.STATIC_ROOT}),
)