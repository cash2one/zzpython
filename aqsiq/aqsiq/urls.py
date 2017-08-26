from django.conf.urls import *
import settings

urlpatterns = patterns('aqsiq.views',
    ('^$', 'index2'),
    ('^newsdetail(?P<newsid>\d+).html$', 'detail'),
    ('^list(?P<typeid>\d+).html$', 'aqsiq_list2'),
    ('^list(?P<typeid>\d+)-(?P<page>\d+).html$', 'aqsiq_list2'),
    ('^aqsiq_detail(?P<newsid>\d+).html$', 'aqsiq_detail2'),
    ('^aqsiq_detail(?P<newsid>\d+)-(?P<page>\d+).html$', 'aqsiq_detail2'),
    ('^aqsiq_about.html$', 'aqsiq_about'),
    ('^aqsiq_success.html$', 'aqsiq_success'),
    ('^aqsiq_comp.html$', 'aqsiq_comp'),
    ('^aqsiq_compl(?P<newsid>\d+).html$', 'aqsiq_compl'),
    
)

urlpatterns += patterns('',
    (r'^(?!admin)(?P<path>.*)$','django.views.static.serve',{'document_root':settings.STATIC_ROOT}),
)