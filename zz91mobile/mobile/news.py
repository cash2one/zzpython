#-*- coding:utf-8 -*-
from django.shortcuts import render_to_response
from django.http import HttpResponse,HttpResponseRedirect,HttpResponseNotFound,HttpResponsePermanentRedirect
import MySQLdb,sys,os,memcache,settings,urllib,re,time,datetime,requests,random,string,md5,hashlib
from django.core.cache import cache
from sphinxapi import *
from zz91page import *
from settings import spconfig
from zz91settings import SPHINXCONFIG
from commfunction import filter_tags,formattime,havepicflag,subString,getjiami,getIPFromDJangoRequest,validateEmail
from zz91tools import int_to_str
from datetime import timedelta, date 
from zz91db_ast import companydb
from zz91db_2_news import newsdb
dbc=companydb()
dbn=newsdb()

reload(sys)
sys.setdefaultencoding('UTF-8')
nowpath=os.path.dirname(__file__)
execfile(nowpath+"/commfunction.py")
execfile(nowpath+"/function.py")

#----资讯首页(一期)
def newsindex(request):
    keywords=request.GET.get("keywords")
    if keywords:
        return news_list(request,keywords=keywords)
    webtitle="资讯中心"
    nowlanmu="<a href='/news/'>资讯中心</a>"
    host=getnowurl(request)
    #cursor_news = conn_news.cursor()
    #newscolumn=getnewscolumn(cursor_news)
    newscolumn=getnewscolumn()
    #useragent=str(request.META)
    username=request.session.get("username",None)
    #cursor_news.close()
    return render_to_response('news/index.html',locals())
#资讯列表页(一期)
def news_list301(request,typeid='',page=''):
    keywords=request.GET.get("keywords")
    tourl="/news/"
    if typeid:
        pinyin=getnewscolumnpinyin(typeid)
        tourl+=pinyin+"/"
    if page:
        tourl+="p"+str(page)+".html"
    if keywords:
        tourl+="?keywords="+keywords
    return HttpResponsePermanentRedirect(tourl)
def news_list(request,typeid='',page='',pinyin='',keywords=''):
    host=getnowurl(request)
    seohost=host.replace("/news/","")
    if pinyin:
        typeid=getnewscolumnid(pinyin)
        if not typeid:
            return page404(request)
    if not typeid:
        typeid=0
    #columnid=getcolumnid()
    typename=get_typename(typeid)
    
    keywords=request.GET.get("keywords")
    if typeid==0:
       typename= keywords
    username=request.session.get("username",None)
    nowlanmu="<a href='/news/'>资讯中心</a>"
#    page=request.GET.get("page")
    if (keywords!=None):
        keywords=keywords.replace("资讯","")
        keywords=keywords.replace("价格","")
        webtitle=keywords
    if (str(keywords)=='None'):    
        keywords=None
        webtitle="资讯中心"
        
    if (page=='' or page==0):
        page=1
    funpage=zz91page()
    limitNum=funpage.limitNum(20)
    nowpage=funpage.nowpage(int(page))
    frompageCount=funpage.frompageCount()
    after_range_num = funpage.after_range_num(5)
    before_range_num = funpage.before_range_num(4)
    if str(typeid)=='196':
        newslist=getnewslist(keywords="p",frompageCount=frompageCount,limitNum=limitNum,typeid='',allnum='',typeid2="")
    elif str(typeid)=='195':
        newslist=getcompanynews(frompageCount,limitNum)
    else:
        newslist=getnewslist(keywords=keywords,frompageCount=frompageCount,limitNum=limitNum,typeid=[int(typeid)],allnum='',typeid2="")
    listcount=0
    if (newslist):
        listall=newslist['list']
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
#    newsnav=getnewsnav()
#    listall=listalla['list']
#    newslistcount=listalla['count']
    
    if (listcount==1):
        morebutton='style=display:none'
    else:
        morebutton=''
    #cursor_news.close()
    return render_to_response('news/list.html',locals())

#----资讯最终页(一期)
def newsdetail(request,id=''):
    host=getnowurl(request)
    seohost=host.replace("/news/","")
    #cursor_news = conn_news.cursor()
    typeid=request.GET.get("typeid")
    webtitle="资讯中心"
    nowlanmu="<a href='/news/'>资讯中心</a>"
    username=request.session.get("username",None)
    showpost=1
    if typeid=='195':
        content=getshowcompanynews(id)
        typename='企业新闻'
        articalup=getcompanyup(id)
        articalnx=getcompanynx(id)
    else:
        newsclick_add(id)
        content=getnewscontent(id)
#        content=content.replace('uploads/uploads','http://newsimg.zz91.com/uploads/uploads')
        webtitle=content['title']
        #获得当前新闻栏目
        newstype=get_newstype(id)
        if newstype:
            typename=newstype['typename']
            typeid=newstype['typeid']
            typeid2=newstype['typeid2']
            typeurl1=newstype['url']
            typeurl2=newstype['url2']
            if typeurl1==typeurl2:
                typeurl1=None
            seohost=""
            if typeurl2:
                seohost+=typeurl2+"/"
            if typeurl1:
                seohost+=typeurl1+"/"
            seohost+="newsdetail1"+str(id)+".htm"
            #相关阅读
            typenews=get_typenews(typeid,typeid2,'')
            #上一篇文章
            #articalup=getarticalup(id,typeid)
            #下一篇文章
            #articalnx=getarticalnx(id,typeid)
    #cursor_news.close()
    return render_to_response('2016new/news/detail.html',locals())