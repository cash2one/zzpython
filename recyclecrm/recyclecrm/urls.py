# -*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url
import settings
#后台管理
urlpatterns = patterns('recyclecrm.admin',
    #---主页面
    (r'^crm/admin/list.html$','list'),
    #---添加/保存/批处理
    (r'^crm/admin/add.html$','add'),
    (r'^crm/admin/save.html$','save'),
    (r'^crm/admin/all.html$','all'),
    #---详情页
    (r'^crm/admin/details.html$','details'),#详情页主页面
    (r'^crm/admin/company.html$','company'),#公司信息
    (r'^crm/admin/picture.html$','picture'),#公司图片
    (r'^crm/admin/user.html$','user'),#用户信息
    (r'^crm/admin/activity.html$','activity'),#活动记录
    (r'^crm/admin/user_activity.html$','user_activity'),#用户活动情况
    (r'^crm/admin/message.html$','user_message'),#用户留言
    (r'^crm/admin/del_message.html$','del_message'),#删除留言
    (r'^crm/admin/add_user.html$','add_user'),#添加用户
    (r'^crm/admin/save_user.html$','save_user')#添加用户
)
#工作台
urlpatterns += patterns('recyclecrm.main',
    (r'^crm/$','index'),#主页面
    (r'^crm/index.html$','index'),#主页面
    (r'^$','index'),#主页面
    (r'^crm/getcode.html$','getcode'),#获取验证码
    (r'^crm/login.html$','login'),#登录
    (r'^crm/loginsave.html$','loginsave'),#登录保存
    (r'^crm/reg_one.html$','reg_one'),#注册第一步
    (r'^crm/reg_two.html$','reg_two'),#注册第二步
    (r'^crm/reg_save.html$','reg_save'),#保存注册信息
    (r'^crm/main/list.html$','main'),#云线索主页面
    (r'^crm/main/categoryinfo.html$','categoryinfo'),#获取行业类别
    (r'^crm/main/company.html$','company'),#公司资料
    (r'^crm/main/company_modify.html$','company_modify'),#修改公司资料
    (r'^crm/main/contact_list.html$','contact_list'),#我的联系人
    (r'^crm/main/contact_add.html$','contact_add'),#添加公司联系人
    (r'^crm/main/contact_mod.html$','contact_mod'),#修改公司联系人
    (r'^crm/main/details.html$','details'),#公司详情
    (r'^crm/main/history.html$','history'),#跟进记录
    (r'^crm/main/addto.html$','addto'),#加入我的客户库
    (r'^crm/main/contact.html$','contact'),#立即联系
    (r'^crm/main/action.html$','action'),#立即行动
    (r'^crm/main/bz.html$','bz'),#客户小计
    (r'^crm/main/remark.html$','remark'),#管理记录
)
#消息
urlpatterns += patterns('recyclecrm.message',
    (r'^crm/message/index.html$','index'),#消息主界面
    (r'^crm/message/leave.html$','leave'),#消息留言
    (r'^crm/message/leave_list.html$','leave_list'),#消息留言列表
    (r'^crm/message/leave_last.html$','leave_last'),#消息留言回复最终页
    (r'^crm/message/reply.html$','reply'),#回复客户信息
    (r'^crm/message/notification1.html$','notification1'),#消息通知——我的
    (r'^crm/message/notification2.html$','notification2'),#消息通知_系统消息
    (r'^crm/message/commission.html$','commission'),#消息代办
)
#发现
urlpatterns += patterns('recyclecrm.found',
    (r'^crm/found/index.html', 'index')#发现主界面
)
#我的
urlpatterns += patterns('recyclecrm.my',
    (r'^crm/my/index.html', 'index'),#我的主界面
    (r'^crm/my/company_info.html', 'company_info'),#公司资料
    (r'^crm/my/compinfo_save.html', 'compinfo_save'),#保存公司资料
    (r'^crm/my/contact.html', 'contact'),#我的联系人
    (r'^crm/my/contact_mod.html', 'contact_mod'),#修改联系人
    (r'^crm/my/contact_save.html', 'contact_save'),#保存联系人
    (r'^crm/my/security_mod.html', 'security_mod'),#修改密码
    (r'^crm/my/security_save.html', 'security_save'),#保存密码
    (r'^crm/my/logout.html', 'logout')#退出登录
)
#我的客户
urlpatterns += patterns('recyclecrm.customer',
    (r'^crm/customer/list.html$','list'),#我的所有客户
    (r'^crm/customer/manage.html$','manage'),#管理我的客户
    (r'^crm/customer/all.html$','all'),#批量处理我的客户
    (r'^crm/customer/contact.html$','contact'),#联系我的客户
    (r'^crm/customer/remark.html$','remark'),#客户记录
    (r'^crm/customer/throw.html$','throw'),#客户记录
    (r'^crm/customer/action.html$','action'),#+行动
)
urlpatterns += patterns('',
    (r'^(?!admin)(?P<path>.*)$','django.views.static.serve',{'document_root':settings.STATIC_ROOT}),
)