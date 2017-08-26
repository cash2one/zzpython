#-*- coding:utf-8 -*-
from django.http import HttpResponse,HttpResponseRedirect,HttpResponsePermanentRedirect,HttpResponseNotFound
from django.shortcuts import render_to_response
from django.core.cache import cache
from django.template.loader import get_template
from django.template import Context
from datetime import date,timedelta
from zz91tools import int_to_str,formattime,int_to_str2,date_to_int,getjiami,getjiemi
from news import zzn

def zhuanti(request):
    return HttpResponsePermanentRedirect("http://news.zz91.com")
def newsalllist(request,kltype='',tags_hex='',page=''):
    tags=getjiemi(tags_hex)
    return HttpResponsePermanentRedirect("http://news.zz91.com/search/?keywords="+tags)
def newsdetail(request,kltype='',mltype='',newsid=''):
    newsurl=zzn.get_newstype(id=newsid)
    weburl="http://news.zz91.com"
    if newsurl:
        weburl="/"+newsurl["url"]+"/"+str(newsid)+".html"
    else:
        weburl="/search/"+str(newsid)+".html"
    return HttpResponsePermanentRedirect(weburl)

def search(request):
    title=request.GET.get("title")
    weburl="/search/?keywords="+str(title)
    return HttpResponsePermanentRedirect(weburl)