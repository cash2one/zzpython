# -*- coding: utf-8 -*-
from django.conf.urls.defaults import *
import settings

urlpatterns = patterns('huanbao.news',
    #---客户界面
    (r'^news/list.html$','news_list'),
    (r'^news/details.html$','news_details'),
)

urlpatterns += patterns('huanbao.news_admin',
    #---后台
    (r'^news/add_admin.html$','news_add_admin'),
    (r'^news/save_admin.html$','news_save_admin'),
    (r'^news/list_admin.html$','news_list'),
    (r'^news/del_admin.html$','news_del_admin'),
     (r'^news/mod_admin.html$','news_mod_admin'),
)
urlpatterns += patterns('huanbao.caigou',
    (r'^caigou/list.html$','caigoulist'),
)

urlpatterns += patterns('huanbao.trade_buy',
    (r'^trade_buy/list.html$','trade_buy_list'),
)

urlpatterns += patterns('huanbao.trade_supply',
    (r'^trade_supply/list.html$','trade_supply_list'),
)

urlpatterns += patterns('huanbao.comp_account',
    (r'^comp_account/list.html$','comp_account_list'),
)

urlpatterns += patterns('huanbao.comp_news',
    (r'^comp_news/list.html$','comp_news_list'),
)

urlpatterns += patterns('huanbao.comp_profile',
    (r'^comp_profile/list.html$','comp_profile_list'),
)
urlpatterns += patterns('',
    (r'^(?!admin)(?P<path>.*)$','django.views.static.serve',{'document_root':settings.STATIC_ROOT}),
)