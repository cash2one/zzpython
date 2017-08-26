#from django.conf.urls import patterns, include, url
from django.conf.urls import *
import settings
#----dacong
urlpatterns = patterns('daconglaile.views',
    (r'^$', 'index'),
    (r'^list(?P<typeid>\d+).html$', 'index'),
    (r'^(?P<typedir>\w+)/$', 'index'),
    (r'^(?P<typedir>\w+)/(?P<typedir1>\w+)/$', 'index'),
    (r'^(?P<typedir>\w+)/(?P<typedir1>\w+)/(?P<typedir2>\w+)/$', 'index'),
    (r'^(?P<typedir>\w+)$', 'index'),
    (r'^(?P<typedir>\w+)/(?P<typedir1>\w+)$', 'index'),
    (r'^(?P<typedir>\w+)/(?P<typedir1>\w+)/(?P<typedir2>\w+)$', 'index'),
    (r'^(?P<typedir>\w+)/(?P<id>\d+).html$', 'detail'),
    (r'^(?P<typedir>\w+)/(?P<typedir1>\w+)/(?P<id>\d+).html$', 'detail'),
    (r'^(?P<typedir>\w+)/(?P<typedir1>\w+)/(?P<typedir2>\w+)/(?P<id>\d+).html$', 'detail'),
    (r'^detail/(?P<id>\d+).html$', 'detail'),
    (r'^detail(?P<id>\d+).html$', 'detail'),
    (r'^apps/download.html$', 'download'),
)
#----dacong
urlpatterns += patterns('daconglaile.app',
    (r'^app/$', 'newsindex'),
    (r'^app/columnall.html$', 'columnall'),
    (r'^app/mycolumlist.html$', 'mycolumlist'),
    (r'^app/list.html$', 'news_list'),
    (r'^app/navlist.html$', 'navlist'),
    (r'^app/mynavlist.html$', 'mynavlist'),
    (r'^app/order.html$', 'order'),
    (r'^app/list.html$', 'news_list'),
    (r'^app/search.html$', 'news_search'),
    (r'^app/newsdetail(?P<id>\d+).html$', 'newsdetail'),
    (r'^app/newstitlecount.html$', 'newstitlecount'),
    (r'^app/savesearchkey.html$', 'savesearchkey'),
    (r'^app/searchhistory.html$', 'searchhistory'),
    (r'^app/regsuc.html$', 'regsuc'),
    (r'^app/get_token.html$', 'get_token'),
    (r'^app/tokeninfo.html$', 'tokeninfo'),
    (r'^app/find.html$', 'find'),

    #dedecms测试
    (r'^app/show_memebe_stom.html$', 'show_memebe_stom'),#收藏夹显示
    (r'^app/del_memebe_stom.html$', 'del_memebe_stom'),#
    (r'^app/feedback.html$', 'feedback'),#
    (r'^app/appversion.html$', 'appversion'),#
    
    
    (r'^app/show_feedback.html$','show_feedback'),#评论表显示
    (r'^app/show_myorder.html$', 'show_myorder'),#我的订阅显示
    (r'^app/show_view_history.html$', 'show_view_history'),#最近浏览
    (r'^app/hot_tagslist.html$', 'hot_tagslist'),#最近浏览
    
    (r'^app/show_member.html$', 'show_member'),
    (r'^app/insert_member_guestbook.html$', 'insert_member_guestbook'),#插入至留言溥
    (r'^app/insert_view_history.html$', 'insert_view_history'),#插入至浏览历史
    (r'^app/insert_dede_feedback.html$', 'insert_dede_feedback'),
    (r'^app/insert_myorder.html$', 'insert_myorder'),
    (r'^app/insert_dede_member_stow.html$', 'insert_dede_member_stow'),
    (r'^app/insert_myguanzhu.html$', 'insert_myguanzhu'),
    (r'^app/login.html$', 'login'),#登录
    (r'^app/reg.html$', 'reg'),#注册
    (r'^app/modinfo.html$', 'modinfo'),#
    (r'^app/insert_feedback_goodbad.html$', 'insert_feedback_goodbad'),#
    (r'^app/uploadface.html$', 'upload'),
    (r'^app/auth_yzmcode.html$', 'auth_yzmcode'),
    (r'^app/urlencode.html$', 'urlencode'),
    
    
)
urlpatterns += patterns('',
    (r'^(?!admin)(?P<path>.*)$','django.views.static.serve',{'document_root':settings.STATIC_ROOT}),
)
