#-*- coding:utf-8 -*-
import os,MySQLdb,settings,codecs,time,sys,datetime,random,shutil,requests
from django.utils.http import urlquote
from django.shortcuts import render_to_response
from django.template.loader import get_template
from django.http import HttpResponse,HttpResponseRedirect,HttpResponseNotFound,HttpResponsePermanentRedirect
from django.core.paginator import Paginator,InvalidPage,EmptyPage,PageNotAnInteger
from datetime import timedelta, date 
from zz91settings import SPHINXCONFIG
from django.core.cache import cache
try:
    import cPickle as pickle
except ImportError:
    import pickle

from math import ceil
from sphinxapi import *
from zz91page import *
reload(sys) 
sys.setdefaultencoding('utf-8') 
from zz91db_ast import companydb
dbc=companydb()

nowpath=os.path.dirname(__file__)
execfile(nowpath+"/conn.py")
execfile(nowpath+"/commfunction.py")
execfile(nowpath+"/function.py")

def newsdetail(request,newsid):
    host = request.META['HTTP_HOST']
    navlistt=getlbhex()
    listall=getnewsdetail(newsid=newsid,newszd="old_news_id")
    list=listall['list']
    if not list:
        render_to_response('404.html',locals())
   #     t = get_template('404.html')
   #     html = t.render(Context())
   #     return HttpResponseNotFound(html)
    tags=listall['tags']
    newslist=getindexbbslist(limitcount=10)
    prolist=getindexofferlist_pic(kname='废',limitcount=8)
    xgnewslist=getoldnewslist()
    xgnewslist1=getindexbbslist(kname=tags,limitcount=10)
    if tags and tags!='':
        cplist=getcplist(tags,50)
    else:
        cplist=getcplist('',50)
    return render_to_response('news/newsdetail.html',locals())
    closeconn()
def bbsdetail(request,newsid):
    host = request.META['HTTP_HOST']
    navlistt=getlbhex()
    listall=getnewsdetail(newsid=newsid,newszd="old_forum_id")
    list=listall['list']
    tags=listall['tags']
    newslist=getindexbbslist(limitcount=10)
    prolist=getindexofferlist_pic(kname='废',limitcount=8)
    xgnewslist=getoldnewslist()
    xgnewslist1=getindexbbslist(kname=tags,limitcount=10)
    if tags and tags!='':
        cplist=getcplist(tags,50)
    else:
        cplist=getcplist('',50)
    return render_to_response('news/newsdetail.html',locals())
    closeconn()
def guanzhudetail(request,newsid):
    navlistt=getlbhex()
    host = request.META['HTTP_HOST']
    listall=getnewsdetail(newsid=newsid,newszd="old_guanzhu_id")
    list=listall['list']
    tags=listall['tags']
    newslist=getindexbbslist(limitcount=10)
    prolist=getindexofferlist_pic(kname='废',limitcount=8)
    xgnewslist=getoldnewslist()
    xgnewslist1=getindexbbslist(kname=tags,limitcount=10)
    if tags and tags!='':
        cplist=getcplist(tags,50)
    else:
        cplist=getcplist('',50)
    return render_to_response('news/newsdetail.html',locals())
    closeconn()


def newslist(request,keywords,page):
    host = request.META['HTTP_HOST']
    #keywords=request.GET.get('keywords')
    navlistt=getlbhex()
    keywords_hex=keywords
    keywords=getjiemi(keywords)
    #page=request.GET.get('page')
    if (page==None):
        page=1
    funpage = zz91page()
    limitNum=funpage.limitNum(60)
    nowpage=funpage.nowpage(int(page))
    frompageCount=funpage.frompageCount()
    after_range_num = funpage.after_range_num(5)
    before_range_num = funpage.before_range_num(9)
    
    newslist=getbbslist(keywords,frompageCount,limitNum,None)
    
    listcount=newslist['count']
    if (int(listcount)>1000000):
        listcount=1000000-1
    listcount = funpage.listcount(listcount)
    page_listcount=funpage.page_listcount()
    firstpage = funpage.firstpage()
    lastpage = funpage.lastpage()
    page_range  = funpage.page_range()
    nextpage = funpage.nextpage()
    prvpage = funpage.prvpage()
    cplist=getcplist('',50)
    return render_to_response('news/list.html',locals())
    closeconn()
def newsindex(request):
    #return HttpResponsePermanentRedirect('http://news.zz91.com/')
    host = request.META['HTTP_HOST']
    offerlist1=getindexofferlist(None,1,10)
    offerlist2=getindexofferlist(None,0,10)
    navlistt=getlbhex()
    return render_to_response('news/newsindex.html',locals())
    closeconn()
def newssearchfirst(request):
    keywords=request.GET.get('keywords')
    keywords_hex=getjiami(keywords)
    nowurl="/news/newslist-"+keywords_hex+"-1.html"
    return HttpResponseRedirect(nowurl)
