from django.conf.urls import patterns,include,url
import settings

urlpatterns = patterns('webcms.views',
	#----统一删除函数
	(r'^user/delfromdb.html$', 'delfromdb'),
	#----首页
	(r'^$', 'index'),
	(r'^user/$', 'default'),
	(r'^user/returnpage.html$', 'returnpage'),
	#----栏目管理
	(r'^user/nexttypelist.html$', 'nexttypelist'),
	(r'^user/arttype.html$', 'arttype'),
	(r'^user/addarttype.html$', 'addarttype'),
	(r'^user/addarttypeok.html$', 'addarttypeok'),
	(r'^user/addlastpage.html$', 'addlastpage'),
#	(r'^user/delarttype.html$', 'delarttype'),
	(r'^user/updatearttype.html$', 'updatearttype'),
	#----内容管理
	(r'^user/artical.html$', 'artical'),
	(r'^user/addartical.html$', 'addartical'),
	(r'^user/addarticalok.html$', 'addarticalok'),
	(r'^user/updateartical.html$', 'updateartical'),
	(r'^user/delartical.html$', 'delartical'),
	#清除缓存
	(r'^user/cleararthtml.html$', 'cleararthtml'),
	(r'^user/cleararthtmlall.html$', 'cleararthtmlall'),
	#----生成静态
	(r'^user/buildindexhtml.html$', 'buildindexhtml'),
	(r'^user/buildarttypehtml.html$', 'buildarttypehtml'),
	(r'^user/buildarticalhtml.html$', 'buildarticalhtml'),
	(r'^user/buildhtmlok.html$', 'buildhtmlok'),
	#获得未生成html条数
	(r'^user/noarticalhtmlnum.html$', 'noarticalhtmlnum'),
	#----url地址
	(r'^user/htmlurl.html$', 'htmlurl'),
	#----模版管理
	(r'^user/template.html$', 'template'),
	(r'^user/choicetemp.html$', 'choicetemp'),
	(r'^user/addusertemp.html$', 'addusertemp'),
	(r'^user/delusertemp.html$', 'delusertemp'),
	#----扩展
	(r'^user/usermessage.html$', 'usermessage'),
	(r'^user/sendliuyan.html$', 'sendliuyan'),
	(r'^user/changehand.html$', 'changehand'),
	#友情链接
	(r'^user/friendlink.html$', 'friendlink'),
	(r'^user/addfrinedlink.html$', 'addfrinedlink'),
	(r'^user/addfrinedlinkok.html$', 'addfrinedlinkok'),
	(r'^user/updatefriendlink.html$', 'updatefriendlink'),
	#修改密码
	(r'^user/updatekwd.html$', 'updatekwd'),
	#----图片上传
	(r'^bootstrap/dialogs/image/image.html$', 'mailimg'),
	(r'^user/mailloadimg.html$', 'mailloadimg'),
	#----用户管理
	(r'^user/userlist.html$', 'userlist'),
	(r'^user/adduser.html$', 'adduser'),
	(r'^user/adduserok.html$', 'adduserok'),
	(r'^user/updateuser.html$', 'updateuser'),
)

urlpatterns += patterns('webcms.admin',
	(r'^admin/$', 'default'),
	(r'^admin/returnpage.html$', 'returnpage'),
	(r'^admin/userlist.html$', 'userlist'),
	(r'^admin/adduser.html$', 'adduser'),
	(r'^admin/adduserok.html$', 'adduserok'),
	(r'^admin/updateuser.html$', 'updateuser'),
	(r'^admin/deluser.html$', 'deluser'),
	(r'^admin/usertemplist.html$', 'usertemplist'),
	(r'^admin/usertypelist.html$', 'usertypelist'),
)

urlpatterns += patterns('webcms.login',
	(r'^login.html$', 'login'),
	(r'^logout.html$$', 'logout'),
	(r'^loginpage.html$', 'loginpage'),
)
urlpatterns += patterns('webcms.frontweb',
	(r'^(?P<pinyin>\w+)/$', 'weblist'),
	(r'^(?P<pinyin>\w+)/(?P<pinyin1>\w+)/$', 'weblist'),
	(r'^(?P<pinyin>\w+)/(?P<pinyin1>\w+)/(?P<pinyin2>\w+)/$', 'weblist'),
	
	(r'^(?P<pinyin>\w+)/w(?P<webid>\w+).html$', 'weblist'),
	(r'^(?P<pinyin>\w+)/list_(?P<page>\d+).html$', 'weblist'),
	(r'^(?P<pinyin>\w+)/(?P<pinyin1>\w+)/w(?P<webid>\w+).html$', 'weblist'),
	(r'^(?P<pinyin>\w+)/(?P<pinyin1>\w+)/list_(?P<page>\w+).html$', 'weblist'),
	(r'^(?P<pinyin>\w+)/(?P<pinyin1>\w+)/(?P<pinyin2>\w+)/w(?P<webid>\w+).html$', 'weblist'),
	(r'^(?P<pinyin>\w+)/(?P<pinyin1>\w+)/(?P<pinyin2>\w+)/list_(?P<page>\d+).html$', 'weblist'),
)

urlpatterns += patterns('',
	(r'^(?!admin)(?P<path>.*)$','django.views.static.serve',{'document_root':settings.STATIC_ROOT}),
)