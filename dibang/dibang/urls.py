from django.conf.urls import patterns, include, url
import settings
#分站管理
urlpatterns = patterns('dibang.views',
	(r'^main.html$', 'main'),#
	(r'^index.html$', 'index'),#首页
	(r'^company.html$', 'company'),#
	(r'^company_data.html$', 'company_data'),#
	(r'^company_add.html$', 'company_add'),
	(r'^company_mod.html$', 'company_mod'),
	(r'^company_save.html$', 'company_save'),
	(r'^company_del.html$', 'company_del'),
)
#人员管理
urlpatterns += patterns('dibang.views',
)
#供应商管理
urlpatterns += patterns('dibang.views',
	(r'^supplier.html$', 'supplier'),#
	(r'^supplier_data.html$', 'supplier_data'),#
	(r'^supplier_add.html$', 'supplier_add'),
	(r'^supplier_mod.html$', 'supplier_mod'),
	(r'^supplier_save.html$', 'supplier_save'),
	(r'^supplier_del.html$', 'supplier_del'),
)
#产品类别管理
urlpatterns += patterns('dibang.views',
	(r'^category.html$', 'category'),#
	(r'^category_data.html$', 'category_data'),#
	(r'^category_add.html$', 'category_add'),
	(r'^category_mod.html$', 'category_mod'),
	(r'^category_save.html$', 'category_save'),
	(r'^category_del.html$', 'category_del'),
)
#登录模块
urlpatterns += patterns('dibang.login',
	(r'^$','login'),#用户登录
	(r'^login.html$','login'),#用户登录
	(r'^logincheck.html$','logincheck'),#核对
	(r'^logout.html$','logout'),#退出
)
#API模块
urlpatterns += patterns('dibang.api',
	(r'^api/loginsave.html$', 'api_loginsave'),
	(r'^api/searchsuppliers.html$', 'api_searchsuppliers'),
)
#---css引入
urlpatterns += patterns('',
	(r'^(?!admin)(?P<path>.*)$','django.views.static.serve',{'document_root':settings.STATIC_ROOT}),
)

handler404 = 'dibang.views.viewer_404'
handler500 = 'dibang.views.viewer_500'
