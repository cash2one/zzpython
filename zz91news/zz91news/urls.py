#-*- coding:utf-8 -*- 
from django.conf.urls import patterns,include,url
import settings
#----新版资讯
urlpatterns = patterns('zz91news.news',
    (r'^index.html$', 'index'),
    ('^$', 'index'),
    ('^(?P<type>\w+)/(?P<newsid>\d+).html$', 'detail'),
    (r'^dianzhan.html$', 'dianzhan'),
    (r'^isdianzhan.html$', 'isdianzhan'),
    (r'^favorite.html$', 'favorite'),
    (r'^isfavorite.html$', 'isfavorite'),
    (r'^verifycode.html$', 'verifycode'),
    (r'^myorder.html$', 'myorder'),
    (r'^insert_myguanzhu.html$', 'insert_myguanzhu'),
    (r'^myguanzhu.html$', 'myguanzhu'),
    (r'^myorderlist.html$', 'myorderlist'),
    (r'^myfavoritelist.html$', 'myfavoritelist'),
    ('^zh/$', 'zhindex'),
    ('^zh$', 'zhindex'),
    ('^zh/list(?P<type>\w+).html$', 'zhlist'),
    ('^zh/detail(?P<zhid>\d+).html$', 'zhdetail'),
    ('^(?P<type>\w+)/$', 'newslist'),
    ('^(?P<type>\w+)/p(?P<page>\d+).html$', 'newslist'),
    
    ('^(?P<type>\w+)/(?P<type1>\w+)/$', 'newslist'),
    ('^(?P<type>\w+)/(?P<type1>\w+)/p(?P<page>\d+).html$', 'newslist'),
)
urlpatterns += patterns('zz91news.301',
    ('^zhuanti/$', 'zhuanti'),
    ('^column_list/tags-(?P<tags_hex>\w+).html$', 'newsalllist'),
    ('^column_list/tags-(?P<tags_hex>\w+)-p(?P<page>\w+).html$', 'newsalllist'),
    ('^(?P<kltype>\w+)/list/tags-(?P<tags_hex>\w+).html$', 'newsalllist'),
    ('^(?P<kltype>\w+)/list/tags-(?P<tags_hex>\w+)-p(?P<page>\w+).html$', 'newsalllist'),
    ('^(?P<kltype>\w+)/newsdetail1(?P<newsid>\d+).htm$', 'newsdetail'),
    ('^(?P<kltype>\w+)/newsdetail1(?P<newsid>\d+)-(?P<page>\w+).htm$', 'newsdetail'),
    ('^(?P<kltype>\w+)/(?P<mltype>\w+)/newsdetail1(?P<newsid>\d+).htm$', 'newsdetail'),
    ('^(?P<kltype>\w+)/(?P<mltype>\w+)/newsdetail1(?P<newsid>\d+)-(?P<page>\w+).htm$', 'newsdetail'),
    ('^search.htm$', 'search'),
)

urlpatterns += patterns('',
    (r'^(?!admin)(?P<path>.*)$','django.views.static.serve',{'document_root':settings.STATIC_ROOT}),
)
