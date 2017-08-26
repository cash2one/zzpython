from django.conf.urls.defaults import patterns,include,url
import settings

urlpatterns = patterns('weddingdress.views',
	(r'^$', 'default'),
	(r'^weddingdress.html$', 'weddingdress'),
	(r'^shop.html$', 'shop'),
	(r'^wedingshow.html$', 'wedingshow'),
	(r'^marrygettogether.html$', 'marrygettogether'),
	(r'^help.html$', 'help'),
	(r'^callus.html$', 'callus'),
	(r'^dressfree.html$', 'dressfree'),
	(r'^marryenjoy.html$', 'marryenjoy'),
	(r'^marryenjoy-(?P<page>\w+).html$', 'marryenjoy'),
	
	(r'^openqqwindow.html$', 'openqqwindow'),
	(r'^sendyuyue.html$', 'sendyuyue'),
)

urlpatterns += patterns('weddingdress.admin',
	(r'^weddingdress/admin.html$', 'admin'),
	(r'^weddingdress/yuyue.html$', 'yuyue'),
	(r'^weddingdress/changehand.html$', 'changehand'),
	
	
	#----文章管理
	(r'^weddingdress/returnpage.html$', 'returnpage'),
	(r'^weddingdress/artical.html$', 'artical'),
	(r'^weddingdress/addartical.html$', 'addartical'),
	(r'^weddingdress/addarticalok.html$', 'addarticalok'),
	(r'^weddingdress/dialogs/image/image.html$', 'mailimg'),
	(r'^weddingdress/mailloadimg.html$', 'mailloadimg'),
	(r'^weddingdress/updateartical.html$', 'updateartical'),
	(r'^weddingdress/deldynamic.html$', 'deldynamic'),
	#----栏目管理
	(r'^weddingdress/arttype.html$', 'arttype'),
)

urlpatterns += patterns('weddingdress.useradmin',
	(r'^weddingdress/login.html$', 'login'),
	(r'^weddingdress/logout.html$$', 'logout'),
	(r'^weddingdress/loginpage.html$', 'loginpage'),
)

urlpatterns += patterns('',
	(r'^(?!admin)(?P<path>.*)$','django.views.static.serve',{'document_root':settings.STATIC_ROOT}),
)