from django.conf.urls import *
import settings
#系统管理
urlpatterns = patterns('bestjoy.useradmin',
	(r'^main.html$', 'main'),#主框架页面
	#---员工列表
	(r'^userlist.html$','userlist'),
	(r'^adduser1.html$','adduser'),
	(r'^adduserok.html$','adduserok'),
	(r'^edituser1.html$','edituser'),#编辑用户
	(r'^deluser.html$','deluser'),#删除用户
	(r'^del_alluser.html$','del_alluser'),#一键删除所选用户
	(r'^changestatus_user.html$','changestatus_user'),#改变用户状态，开通还是冻结
	#---角色权限管理
)
#系统管理
urlpatterns += patterns('bestjoy.views',
	(r'^index.html$', 'index'),#欢迎
	(r'^addorder.html$', 'addorder'),
	(r'^addorder_save.html$', 'addorder_save'),
	(r'^order_del.html$', 'order_del'),
	(r'^orderlist.html$', 'orderlist'),
	(r'^modorder.html$', 'modorder'),
	(r'^province.html$', 'province'),
	
	
	(r'^assign.html$', 'assign'),
	(r'^assign_save.html$', 'assign_save'),
	(r'^reassign.html$', 'reassign'),
	(r'^agentlist.html$', 'agentlist'),
	(r'^addagent.html$', 'addagent'),
	(r'^addagent_save.html$', 'addagent_save'),
	(r'^agent_del.html$', 'agent_del'),
	(r'^modagent.html$', 'modagent'),
	
	(r'^getbind.html$', 'getbind'),
	(r'^getewm.html$', 'getewm'),
	
	(r'^orderout.html$', 'orderout'),
	(r'^arealist.html$', 'arealist'),
	(r'^agent_unweixin.html$', 'agent_unweixin'),
	
)
#登录模块
urlpatterns += patterns('bestjoy.login',
	(r'^$','login'),#用户登录
	(r'^login.html$','login'),#用户登录
	(r'^logincheck.html$','logincheck'),#核对
	(r'^logout.html$','logout'),#退出
)

#代理商微信登录模块
urlpatterns += patterns('bestjoy.agent',
	(r'^agent/binding.html$', 'binding'),
	(r'^agent/bindsuc.html$', 'bindsuc'),
	(r'^agent/auth_login.html$', 'auth_login'),
	(r'^agent/redirect_uri.html$', 'redirect_uri'),
	(r'^agent/agent_orderlist.html$', 'agent_orderlist'),
	(r'^agent/agent_ordershow.html$', 'agent_ordershow'),
	(r'^agent/completeorder.html$', 'completeorder'),
	
	(r'^err.html$','errfun'),
)

#---css引入
urlpatterns += patterns('',
	(r'^(?!admin)(?P<path>.*)$','django.views.static.serve',{'document_root':settings.STATIC_ROOT}),
)