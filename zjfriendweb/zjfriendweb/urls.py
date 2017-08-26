#from django.conf.urls import patterns, include, url
from django.conf.urls import *
import settings
#----sex
urlpatterns = patterns('zjfriendweb.views',
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
)
#----sex
urlpatterns += patterns('zjfriendweb.sex',
    (r'^sex/$', 'newsindex'),
    (r'^sex/list.html$', 'news_list'),
    (r'^sex/navlist.html$', 'navlist'),
    (r'^sex/mynavlist.html$', 'mynavlist'),
    (r'^sex/order.html$', 'order'),
    (r'^sex/list-(?P<typeid>\w+).html$', 'news_list'),
    (r'^sex/search.html$', 'news_search'),
    (r'^sex/search-(?P<page>\d+).html$', 'news_search'),
    (r'^sex/list-(?P<typeid>\w+)-(?P<page>\d+).html$', 'news_list'),
    (r'^sex/newsdetail(?P<id>\d+).html$', 'newsdetail'),
    #dedecms测试
    (r'^sex/show_memebe_stom.html$', 'show_memebe_stom'),#收藏夹显示
    (r'^sex/show_feedback.html$','show_feedback'),#评论表显示
    (r'^sex/show_myorder.html$', 'show_myorder'),#我的订阅显示
    (r'^sex/show_view_history.html$', 'show_view_history'),#最近浏览
    (r'^sex/show_member.html$', 'show_member'),
    (r'^sex/insert_member_guestbook.html$', 'insert_member_guestbook'),#插入至留言溥
    (r'^sex/insert_view_history.html$', 'insert_view_history'),#插入至浏览历史
    (r'^sex/insert_dede_feedback.html$', 'insert_dede_feedback'),
    (r'^sex/insert_myorder.html$', 'insert_myorder'),
    (r'^sex/insert_dede_member_stow.html$', 'insert_dede_member_stow'),
    (r'^sex/login.html$', 'login'),#登录
    (r'^sex/reg.html$', 'reg'),#注册
    (r'^sex/modinfo.html$', 'modinfo'),#
    (r'^sex/insert_feedback_goodbad.html$', 'insert_feedback_goodbad'),#
    (r'^sex/uploadface.html$', 'upload'),
)
urlpatterns += patterns('',
    (r'^(?!admin)(?P<path>.*)$','django.views.static.serve',{'document_root':settings.STATIC_ROOT}),
)
