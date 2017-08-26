#from django.conf.urls import *
from django.conf.urls.defaults import *
import settings
#系统管理
urlpatterns = patterns('zz91crm.useradmin',
	(r'^main.html$', 'main'),#主框架页面
	
	#---团队管理
	(r'^user_category.html$','user_category'),#团队管理列表页
	(r'^user_category_data.html$','user_category_data'),#团队管理数据
	(r'^user_category_add.html$','user_category_add'),#新建团队
	(r'^user_category_del.html$','user_category_del'),#删除团队新
	(r'^usercategoryedit.html$','usercategoryedit'),#编辑团队
	(r'^usercategoryeditok.html$','usercategoryeditok'),#编辑团队确认
	(r'^changestatus_usercate.html$','changestatus_usercate'),#改变菜单状态，开通还是冻结
	#---员工列表
	(r'^userlist.html$','userlist'),
	(r'^adduser1.html$','adduser'),
	(r'^adduserok.html$','adduserok'),
	(r'^edituser1.html$','edituser'),#编辑用户
	(r'^deluser.html$','deluser'),#删除用户
	(r'^del_alluser.html$','del_alluser'),#一键删除所选用户
	(r'^changestatus_user.html$','changestatus_user'),#改变用户状态，开通还是冻结
	#---角色权限管理
	(r'^auth.html$','auth'),
	(r'^addauth.html$','addauth'),
	(r'^addauthok.html$','addauthok'),
	(r'^auth_category_del.html$','auth_category_del'),
	(r'^auth_category_set.html$','auth_category_set'),#编辑拥有权限
	(r'^auth_category_setok.html$','auth_category_setok'),#编辑拥有权限确认
	#---菜单管理
	(r'^menu.html$','menu'),#菜单列表
	(r'^addmenu_all.html$','addmenu_all'),#添加菜单
	(r'^addmenuok.html$','addmenuok'),#添加菜单成功
	(r'^editmenu.html$','editmenu'),#编辑菜单
	(r'^delmenu.html$','delmenu'),#编辑菜单
	(r'^changestatus_menu.html$','changestatus_menu'),#改变菜单状态，开通还是冻结
)
#登录模块
urlpatterns += patterns('zz91crm.login',
	(r'^$','login'),#用户登录
	(r'^login.html$','login'),#用户登录
	(r'^logincheck.html$','logincheck'),#核对
	(r'^logout.html$','logout'),#退出
	(r'^socketchat.html$','socketchat'),
)
#黄页录入模块
urlpatterns += patterns('zz91crm.huangye',
	(r'^huangye/add.html$','hy_add'),
	(r'^huangye/edit.html$','hy_edit'),
	(r'^huangye/save.html$','hy_save'),
	(r'^huangye/list.html$','hy_list'),
	(r'^huangye/del.html$','hy_del'),
	(r'^huangye/hy_out.html$','hy_out'),
)
urlpatterns += patterns('seo.views',
	url(r'^seo/', include("seo.urls")),
)
#seo模块
#人事模块
urlpatterns += patterns('zz91crm.hr',
	(r'^hr/add.html$','hr_add'),#添加
	(r'^hr/save.html$','hr_save'),#添加
	(r'^hr/list.html$','hr_list'),#列出所有数据
	(r'^hr/mod.html$','hr_mod'),#修改数据
	(r'^hr/all.html$','hr_all'),#批量处理
	(r'^hr/usershow.html$','hr_usershow'),#单独界面显示个人信息
	(r'^hr/usershow_history.html$','hr_usershow_history'),#面试记录
	#---人事基础数据	
	(r'^hr/basic.html$','hr_basic'),#人事基础数据
	(r'^hr/basic_add.html$','hr_basic_add'),#添加数据
	(r'^hr/basic_mod.html$','hr_basic_mod'),#修改数据
	(r'^hr/basic_del.html$','hr_basic_del'),#删除数据
	(r'^hr/hr_categorylist.html$','hr_categorylist'),
	(r'^hr/hr_list_save.html$','hr_list_save'),
	
)

#物流客户
urlpatterns += patterns('zz91crm.wl',
	(r'^wl/list.html$','wl_list'),#所有物流客户
	(r'^wl/add.html$','wl_add'),#添加物流客户
	(r'^wl/save.html$','wl_save'),#保存物流客户
	(r'^wl/mod.html$','wl_mod'),#修改物流客户
	(r'^wl/all.html$','wl_all'),#批量处理
	(r'^wl/customershow.html$','wl_customershow'),#单独界面显示客户信息
	(r'^wl/customershow_history.html$','wl_customer_history'),#过程记录
)
#我的客户（再生通）
urlpatterns += patterns('zz91crm.icdlist',
	#---我的所有客户（再生通）
	(r'^icd/index.html$','index'),#客户列表
	(r'^icd/icdlist.html$','icdlist'),#客户列表
	(r'^icd/addnew_assign.html$','addnew_assign'),#新的分配
	(r'^icd/addnew_assign.html$','addnew_assign'),#拉黑
	(r'^icd/crm_cominfoedit.html$','crm_cominfoedit'),#编辑该公司详情
	(r'^icd/save_crm_cominfoedit.html$','save_crm_cominfoedit'),#保存公司详情
	(r'^icd/getsite.html$','getsite'),#获得地点
	(r'^icd/relogin.html$','relogin'),#重新登录
	(r'^icd/returnpage.html$','returnpage'),#返回
	(r'^icd/otherperson.html$','otherperson'),#其他联系人显示框
	(r'^icd/add_otherperson.html$','add_otherperson'),#添加与编辑其他联系人
	(r'^icd/del_otherperson.html$','del_otherperson'),#删除其他联系人
	(r'^icd/tellist.html$','tellist'),#销售记录列表(iframe)
	(r'^icd/addtellist.html$','addtellist'),#添加销售记录
	(r'^icd/admin_telsave.html$','admin_telsave'),
	(r'^icd/assign_putmy.html$','assign_putmy'),
	(r'^icd/droptogonghai.html$','droptogonghai'),#放入公海
	(r'^icd/companychecked.html$','companychecked'),#录入公司审核
	(r'^icd/companysqchecked.html$','companysqchecked'),#预分配公司审核
	(r'^icd/set_emphases.html$','set_emphases'),
	(r'^icd/khloglist.html$','khloglist'),
	(r'^icd/tj_contact.html$','tj_contact'),
	(r'^icd/tj_contactvap.html$','tj_contactvap'),
	(r'^icd/tj_contactzsh.html$','tj_contactzsh'),
	(r'^icd/tj_contactvalue.html$','tj_contactvalue'),
	(r'^icd/tj_contactlist.html$','tj_contactlist'),
	(r'^icd/tj_company.html$','tj_company'),
	(r'^icd/tj_companyvap.html$','tj_companyvap'),
	(r'^icd/tj_companyzsh.html$','tj_companyzsh'),
	(r'^icd/tj_companyvalue.html$','tj_companyvalue'),
	(r'^icd/tj_companylist.html$','tj_companylist'),
	(r'^icd/tj_changestar.html$','tj_changestar'),
	(r'^icd/tj_changestarzsh.html$','tj_changestarzsh'),
	(r'^icd/tj_changestarvalue.html$','tj_changestarvalue'),
	(r'^icd/tj_changestarlist.html$','tj_changestarlist'),
	(r'^icd/tj_changestarvap.html$','tj_changestarvap'),
	(r'^icd/order.html$','order'),
	(r'^icd/orderlist.html$','orderlist'),
	(r'^icd/ordercompany.html$','ordercompany'),
	(r'^icd/ordersave.html$','ordersave'),
	(r'^icd/order_del.html$','order_del'),
	(r'^icd/order_value.html$','order_value'),
	(r'^icd/order_value_save.html$','order_value_save'),
	(r'^icd/ordertongji.html$','ordertongji'),
	(r'^icd/assigntoicd.html$','assigntoicd'),
	(r'^icd/companyadd.html$','companyadd'),
	(r'^icd/companysave.html$','companysave'),
	(r'^icd/user_assign.html$','user_assign'),
	(r'^icd/user_assign_ok.html$','user_assign_ok'),
	(r'^icd/user_assign_vap.html$','user_assign_vap'),
	(r'^icd/user_assign_vap_ok.html$','user_assign_vap_ok'),
	(r'^icd/user_drop.html$','user_drop'),
	(r'^icd/user_drop_ok.html$','user_drop_ok'),
	(r'^icd/sqcompany.html$','sqcompany'),
	(r'^icd/company_offercount.html$','company_offercount'),
	(r'^icd/getnewcompanycount.html$','getnewcompanycount'),
	(r'^icd/getcompanyid.html$','getcompanyid'),
	(r'^icd/qianbaobalancelist.html$','qianbaobalancelist'),
	(r'^icd/orderly.html$','orderly'),
	(r'^icd/ordercp.html$','ordercp'),
	(r'^icd/ordercp2.html$','ordercp2'),
	
)
#---css引入
urlpatterns += patterns('',
	(r'^(?!admin)(?P<path>.*)$','django.views.static.serve',{'document_root':settings.STATIC_ROOT}),
)
