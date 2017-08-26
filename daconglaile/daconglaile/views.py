#-*- coding:utf-8 -*-
from django.shortcuts import render_to_response
import simplejson
from django.http import HttpResponse,HttpResponseRedirect,HttpResponsePermanentRedirect
import MySQLdb,sys,os,memcache,settings,urllib,re,time,requests,hashlib,StringIO,Image,ImageDraw,ImageFont,ImageFilter,random
from django.core.cache import cache
from zz91db_dacong import dacongdb
from zz91tools import int_to_strall
from settings import spconfig,appurl,pyuploadpath,pyimgurl
spconfig=settings.SPHINXCONFIG
from sphinxapi import *
from zz91page import *

dbn=dacongdb()
reload(sys)
sys.setdefaultencoding('UTF-8')
nowpath=os.path.dirname(__file__)
execfile(nowpath+"/func/public_function.py")
execfile(nowpath+"/func/dacong_function.py")

zzn=zznews()

def index(request,typedir="",typedir1="",typedir2="",typeid=""):
    page=request.GET.get("page")
    typeid=None
    if typedir1:
        typedir=typedir+"/"+typedir1
    if typedir2:
        typedir=typedir+"/"+typedir2
    if typedir:
        typeid=zzn.get_typeid(typedir)
    if typeid:
        typename=zzn.get_typename(typeid)
        
    nreid=None
    litilecolumn=None
    if typeid:
        nreid=typeid
        if typedir:
            nreid=typeid
        if typedir1:
            nreid=zzn.get_typereid(typeid)
        litilecolumn=zzn.getnewscolumn(reid=nreid,typeid=typeid)
    newscolumn=zzn.getnewscolumn(reid=0,typeid=nreid)
    stypeid=[]
    if litilecolumn:
        if nreid:
            stypeid.append(nreid)
        if typedir1:
            stypeid=[typeid]
        else:
            for co in litilecolumn:
                stypeid.append(co['id'])
    else:
        if nreid:
            stypeid.append(nreid)
    keywords=request.GET.get("keywords")
    if (str(keywords)=='None'):    
        keywords=None
        
    if (page=='' or page==0 or page==None):
        page=1
    funpage=zz91page()
    limitNum=funpage.limitNum(20)
    nowpage=funpage.nowpage(int(page))
    frompageCount=funpage.frompageCount()
    after_range_num = funpage.after_range_num(5)
    before_range_num = funpage.before_range_num(4)
    if not typeid:
        typeidarr=None
    else:
        typeidarr=stypeid
    newslist=zzn.getnewslist(keywords=keywords,frompageCount=frompageCount,limitNum=limitNum,allnum='',typeid=typeidarr,typeid2="")
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
    if (listcount==1):
        morebutton='style=display:none'
    else:
        morebutton=''
    if int(page)>1:
        return render_to_response('listmore.html',locals())
    return render_to_response('list.html',locals())

def detail(request,typedir="",typedir1="",typedir2="",id=""):
    newscolumn=zzn.getnewscolumn()
    typeid=request.GET.get("typeid")
    mid=request.GET.get("mid")
    webtitle="资讯中心"
    listall=[]
    zzn.newsclick_add(id)
    #记录最近浏览
    if mid and id:
        zzn.insert_viewhistory(mid,id)
    content=zzn.getnewscontent(id)
    subcontent=zzn.getsubcontent(id,200)
    cstyle=content.get("cstyle")
    detail=content['content'].lower()
    detail=remove_script(detail)
    title=filter_tags(content['title'])
    detail=qqvadio(detail)
    #detail=re.sub('<iframe.*?>','',detail)
    if str(cstyle)=="1":
        content['content']=remove_content_value(detail)
    else:
        content['content']=detail
    content['title']=title
    webtitle=content['title']
    listall.append(content)
    
    return render_to_response('detail.html',locals())
def download(request):
    return render_to_response('download.html',locals())