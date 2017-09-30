from django.conf.urls import patterns, include, url
import settings
#---PC端---#
#分站管理
urlpatterns = patterns('dibang.views',
	(r'^main.html$', 'main'),
	(r'^index.html$', 'index'),
	(r'^company.html$', 'company'),
	(r'^company_data.html$', 'company_data'),
	(r'^company_add.html$', 'company_add'),
	(r'^company_mod.html$', 'company_mod'),
	(r'^company_save.html$', 'company_save'),
	(r'^company_del.html$', 'company_del'),
)

#供应商管理
urlpatterns += patterns('dibang.views',
	(r'^supplier.html$', 'supplier'),
	(r'^supplier_data.html$', 'supplier_data'),
	(r'^supplier_add.html$', 'supplier_add'),
	(r'^supplier_mod.html$', 'supplier_mod'),
	(r'^supplier_save.html$', 'supplier_save'),
	(r'^supplier_del.html$', 'supplier_del'),
)
#产品类别管理
urlpatterns += patterns('dibang.views',
	(r'^category.html$', 'category'),
	(r'^category_data.html$', 'category_data'),
	(r'^category_add.html$', 'category_add'),
	(r'^category_mod.html$', 'category_mod'),
	(r'^category_save.html$', 'category_save'),
	(r'^category_del.html$', 'category_del'),
)
#产品管理
urlpatterns += patterns('dibang.views',
	(r'^product.html$', 'product'),
	(r'^product_data.html$', 'product_data'),
	(r'^product_add.html$', 'product_add'),
	(r'^product_mod.html$', 'product_mod'),
	(r'^product_save.html$', 'product_save'),
	(r'^product_del.html$', 'product_del'),
)
#入库单管理
urlpatterns += patterns('dibang.views',
	(r'^storage.html$', 'storage'),
	(r'^storage_data.html$', 'storage_data'),
	(r'^storage_add.html$', 'storage_add'),
	(r'^storage_mod.html$', 'storage_mod'),
	(r'^storage_save.html$', 'storage_save'),
	(r'^storage_del.html$', 'storage_del'),
)
#人员管理
urlpatterns += patterns('dibang.views',
	(r'^user.html$', 'user'),
	(r'^user_data.html$', 'user_data'),
	(r'^user_add.html$', 'user_add'),
	(r'^user_mod.html$', 'user_mod'),
	(r'^user_save.html$', 'user_save'),
	(r'^user_del.html$', 'user_del'),
)
#财务数据明细
urlpatterns += patterns('dibang.views',
	(r'^finance.html$','finance'),
	(r'^finance_data.html$','finance_data'),
)
#每日账目清单
urlpatterns += patterns('dibang.views',
	(r'^finance_everyday.html$', 'finance_everyday'),
	(r'^finance_everyday_data.html$', 'finance_everyday_data'),
	(r'^finance_productstotal_data.html$', 'finance_productstotal_data'),
)
#登录模块
urlpatterns += patterns('dibang.login',
	(r'^$','login'),
	(r'^login.html$','login'),
	(r'^logincheck.html$','logincheck'),
	(r'^logout.html$','logout'),
)
#API模块
urlpatterns += patterns('dibang.api',
	(r'^api/loginsave.html$', 'api_loginsave'),
	(r'^api/searchsuppliers.html$', 'api_searchsuppliers'),
	(r'^api/datatable_update.html$', 'api_datatable_update'),
	(r'^api/getstoragedate.html$', 'api_getstoragedate'),
	(r'^api/updatestorage.html$', 'api_updatestorage'),
	(r'^api/getsuppliersdate.html$', 'api_getsuppliersdate'),
	(r'^api/updatesuppliers.html$', 'api_updatesuppliers'),
	(r'^api/weixinget.html$', 'api_weixinget'),
)

#---手机端---#
urlpatterns += patterns('dibang.mobile',
	(r'^mobile$','login'),#用户登录
	(r'^mobile/login.html$','login'),#用户登录
	(r'^mobile/index.html$','index'),#首页
	(r'^mobile/logincheck.html$','logincheck'),#核对
	(r'^mobile/logout.html$','logout'),#退出
)
#待定价榜单
urlpatterns += patterns('dibang.mobile',
	(r'^mobile/pricing.html$','pricing'),#待定价榜单
	(r'^mobile/pricing_today.html$','pricing_today'),#今日已定价
	(r'^mobile/pricing_now_save.html$','pricing_now_save'),#立即定价保存
)
#供应商管理
urlpatterns += patterns('dibang.mobile',
	(r'^mobile/supplier.html$','supplier'),#供应商列表
	(r'^mobile/supplier_add.html$','supplier_add'),#添加供货商
	(r'^mobile/supplier_mod.html$','supplier_mod'),#修改供货商
	(r'^mobile/supplier_save.html$','supplier_save'),#供应商保存
)
#数据汇总
urlpatterns += patterns('dibang.mobile',
	(r'^mobile/alldata.html$','alldata'),#数据汇总
)
#入库明细
urlpatterns += patterns('dibang.mobile',
	(r'^mobile/storage.html$','storage'),#入库明细
)
#分站管理
urlpatterns += patterns('dibang.mobile',
	(r'^mobile/company.html$','company'),#分站列表
	(r'^mobile/company_add.html$','company_add'),#添加分站
	(r'^mobile/company_mod.html$','company_mod'),#修改分站
	(r'^mobile/company_save.html$','company_save'),#保存分站
)
#产品类别
urlpatterns += patterns('dibang.mobile',
	(r'^mobile/category.html$','category'),#类别列表
	(r'^mobile/category_add.html$','category_add'),#添加类别
	(r'^mobile/category_mod.html$','category_mod'),#修改类别
	(r'^mobile/category_save.html$','category_save'),#保存类别
	(r'^mobile/category_del.html$','category_del'),
)
#产品管理
urlpatterns += patterns('dibang.mobile',
	(r'^mobile/product.html$','product'),#产品列表
	(r'^mobile/product_add.html$','product_add'),#添加产品
	(r'^mobile/product_mod.html$','product_mod'),#修改产品
	(r'^mobile/product_save.html$','product_save'),#保存产品
	(r'^mobile/product_del.html$','product_del'),
)
#人员管理
urlpatterns += patterns('dibang.mobile',
	(r'^mobile/user.html$','user'),#人员列表
	(r'^mobile/user_add.html$','user_add'),#添加人员
	(r'^mobile/user_mod.html$','user_mod'),#修改人员
	(r'^mobile/user_save.html$','user_save'),#保存人员
	(r'^mobile/user_del.html$','user_del'),
)
#个人信息管理
urlpatterns += patterns('dibang.mobile',
	(r'^mobile/myinfo.html$','myinfo'),#人员列表
	(r'^mobile/myinfo_save.html$','myinfo_save'),#人员保存
)
#自动获取供货人编码iccode
urlpatterns += patterns('dibang.mobile',
	(r'^mobile/get_iccode.html$','get_iccode'),#自动获取编码
)

#---APP---#
urlpatterns += patterns('dibang.app',
	(r'^app/logincheck.html$','logincheck'),#登录核对
	(r'^app/logout.html$','logout'),#退出
)
#个人信息
urlpatterns += patterns('dibang.app',
	(r'^app/myinfo.html$','myinfo'),#个人信息
	(r'^app/myinfo_save.html$','myinfo_save'),#个人信息保存
)
#待定价榜单数量
urlpatterns += patterns('dibang.app',
	(r'^app/get_num.html$','get_num'),#待定价榜单数量
)
#待定价榜单
urlpatterns += patterns('dibang.app',
	(r'^app/pricing.html$','pricing'),#待定价
	(r'^app/pricing_now_save.html$','pricing_now_save'),#立即定价保存
)
#供应商管理
urlpatterns += patterns('dibang.app',
	(r'^app/supplier.html$','supplier'),#供应商列表
	(r'^app/supplier_mod.html$','supplier_mod'),#修改供应商
	(r'^app/supplier_save.html$','supplier_save'),#供应商保存
)
#数据汇总
urlpatterns += patterns('dibang.app',
	(r'^app/alldata.html$','alldata'),#数据汇总
)
#入库明细
urlpatterns += patterns('dibang.app',
	(r'^app/storage.html$','storage'),#入库明细
)
#分站管理
urlpatterns += patterns('dibang.app',
	(r'^app/company.html$','company'),#分站列表
	(r'^app/company_save.html$','company_save'),#分站列表
	
)
#产品类别
urlpatterns += patterns('dibang.app',
	(r'^app/category.html$','category'),#产品类别
	(r'^app/category_save.html$','category_save'),#产品类别
)
#产品管理
urlpatterns += patterns('dibang.app',
	(r'^app/product.html$','product'),#产品列表
	(r'^app/product_save.html$','product_save'),#保存产品
)
#人员管理
urlpatterns += patterns('dibang.app',
	(r'^app/user.html$','user'),#人员列表
	(r'^app/user_save.html$','user_save'),#保存人员
)

#自动获取供货人编码iccode
urlpatterns += patterns('dibang.app',
	(r'^app/get_iccode.html$','get_iccode'),#获取供应上编码
)

urlpatterns += patterns('dibang.wechat',
	(r'^wechat/auth_login.html$','auth_login'),#
	(r'^wechat/redirect_uri.html$','redirect_uri'),
)
#---css引入
urlpatterns += patterns('',
	(r'^(?!admin)(?P<path>.*)$','django.views.static.serve',{'document_root':settings.STATIC_ROOT}),
)


handler404 = 'dibang.views.viewer_404'
handler500 = 'dibang.views.viewer_500'
