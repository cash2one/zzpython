"""seocrm URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import patterns

urlpatterns = patterns('seo.views',
                       (r'^seolist\.html$', "seo_list"),
                       (r'^seo_dolist\.html$', "seo_dolist"),
                       (r'^add_seokh\.html$', "add_seokh"),
                       (r'^save_seokh\.html', "save_seokh"),
                       (r'^modify_seokh\.html$', "modify_seokh"),
                       (r'^del_seokh\.html$', "del_seokh"),
                       (r'^fp_seokh', "fp_kh"),
                       (r'^get_sl\.html$', "sl_gx"),
                       (r'^get_fl\.html$', "fl_gx"),
                       (r'^get_pm\.html$', "pm_gx"),
                       (r'^k_history\.html$', "k_history"),
                       (r'^pl_sl\.html', "pl_sl"),
                       (r'^pl_sl2\.html', "pl_sl2"),
                       (r'^get_plsl\.html', "get_plsl"),
                       (r'^ex_excel\.html', "export_excel"),
                       (r'^pl_ts2\.html', "pl_ts2"),
                       (r'^get_plts\.html', "get_plts"),
                       (r'^moban\.html', "xz_mb"),
                       (r'^ciku\.html', "ci_ku"),
                       (r'^pl_ciku\.html', "ci_ku_tj"),
                       (r'^get_pl_cc\.html', "get_pl_cc"),
                       (r'^cx_jl\.html', "gjc_cx_jl"),
                       (r'^yuebao\.html', "yue_bao")
                       )
