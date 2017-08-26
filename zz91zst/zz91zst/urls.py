from django.conf.urls import *
from zz91zst import views
import settings
# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
	(r'^zst/$', 'zz91zst.views.default'),
	(r'^zst/about.html$', 'zz91zst.views.about'),
	(r'^zst/apply.html$', 'zz91zst.views.apply'),
	(r'^zst/apply_save.html$', 'zz91zst.views.apply_save'),
	(r'^zst/payment.html$', 'zz91zst.views.payment'),
    # Example:
    # (r'^astoabout/', include('astoabout.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # (r'^admin/', include(admin.site.urls)),
	(r'^(?!admin)(?P<path>.*)$','django.views.static.serve',{'document_root':settings.STATIC_ROOT}),
)
