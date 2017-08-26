from django.conf.urls import *
from huanbaosubject import views
import settings
# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    # (r'^subject/', include('subject.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # (r'^admin/', include(admin.site.urls)),
	(r'^(?P<subjectname>\w+)/$', 'huanbaosubject.views.default'),
	(r'^(?P<subjectname>\w+)/(?P<pagename>\w+)/$', 'huanbaosubject.views.subject'),
	(r'^(?P<subjectname>\w+)/(?P<pagename>\w+).html$', 'huanbaosubject.views.subject'),
	(r'^(?P<subjectname>\w+)/(?P<pagename>\w+)$', 'huanbaosubject.views.subject'),	
	(r'^(?!admin)(?P<path>.*)$','django.views.static.serve',{'document_root':settings.STATIC_ROOT}),
)
