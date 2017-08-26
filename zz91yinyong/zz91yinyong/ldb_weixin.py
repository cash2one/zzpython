#-*- coding:utf-8 -*-
from django.shortcuts import render_to_response
from django.http import HttpResponse,HttpResponseRedirect,HttpResponsePermanentRedirect
from sphinxapi import *

from datetime import timedelta,date 
import MySQLdb,sys,os,memcache,settings,time,datetime,requests

from zz91db_ast import companydb
from zz91db_2_news import newsdb

from zz91tools import formattime,getpastoneday,subString,getnowurl,filter_tags,getjiemi
from settings import spconfig
from zz91page import *
from django.core.cache import cache
dbc=companydb()
dbn=newsdb()

reload(sys)
sys.setdefaultencoding('UTF-8')
nowpath=os.path.dirname(__file__)
execfile(nowpath+"/func/ldb_weixin_function.py")
ldb_weixin=ldbweixin()

#----来电宝首页
def laidianbao(request,page=''):
    webtitle="来电宝"
    nowlanmu="<a href='/laidianbao/'>来电宝客户</a>"
    host=getnowurl(request)
    username=request.session.get("username",None)
    kname=request.GET.get('kname')
    if not kname:
        knamehex=request.GET.get('knamehex')
        if knamehex:
            kname=getjiemi(knamehex)
    if not page:
        page=1
    funpage=zz91page()
    limitNum=funpage.limitNum(8)
    nowpage=funpage.nowpage(int(page))
    frompageCount=funpage.frompageCount()
    after_range_num = funpage.after_range_num(5)
    before_range_num = funpage.before_range_num(4)
    newslist=ldb_weixin.getcompanylist(frompageCount,limitNum,kname=kname,ldb=1)
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
    return render_to_response('ldb_weixin/laidianbao.html',locals())


def index(request):
    return render_to_response('ldb_weixin/index.html',locals())

def product_introduction(request):
    return render_to_response('ldb_weixin/product_introduction.html',locals())

def about(request):
    return render_to_response('ldb_weixin/about.html',locals())

def contact(request):
    return render_to_response('ldb_weixin/contact.html',locals())
#----商机搜索
def businessearch(request):
    return HttpResponseRedirect("/company/?ldb=1")
    companyname=request.GET.get('companyname')
    if companyname==None:
        companyname=''
    
    laidianbao=ldb_weixin.getppccomplist(companyname,0,30)
    if laidianbao:
        listall=laidianbao['list']
    
    return render_to_response('ldb_weixin/businessearch.html',locals())
def businessearchmore(request):
    companyname=request.GET.get('companyname')
    if companyname==None:
        companyname=''
    page=request.GET.get('page')
    if page==None:
        page=1
    laidianbao=ldb_weixin.getppccomplist(companyname,(int(page)-1)*30,30)
    if laidianbao:
        listall=laidianbao['list']
    return render_to_response('ldb_weixin/businessearchmore.html',locals())
#----来电分析
def callanalysis(request):
    company_id=request.session.get("company_id",None)
    username=request.session.get("username",None)
    if username and company_id==None:
        company_id=ldb_weixin.getcompanyid(username)
        request.session['company_id']=company_id
    if (username==None or company_id==None):
        return HttpResponseRedirect("/login/?done=/ldb_weixin/callanalysis.html")
    area_custom=ldb_weixin.getarea_custom2(company_id)
    time_custom=ldb_weixin.gettime_custom2(company_id)
    nowmonthstate=ldb_weixin.getnowmonthstate(company_id)
    return render_to_response('ldb_weixin/callanalysis.html',locals())

#----余额查询
def balance(request):
    backurl=request.GET.get('backurl')
    company_id=request.session.get("company_id",None)
    username=request.session.get("username",None)
    if username and company_id==None:
        company_id=ldb_weixin.getcompanyid(username)
        request.session['company_id']=company_id
    if (username==None or company_id==None):
        return HttpResponseRedirect("/login/?done=/ldb_weixin/balance.html")
    contactuser=ldb_weixin.getcompanymobile(company_id)
    if contactuser:
        mobile=contactuser['mobile']
        contact=contactuser['contact']
    ldbbalance=ldb_weixin.getldbbalance(company_id)
    return render_to_response('ldb_weixin/balance.html',locals())
#----400来电记录
def phonerecordsmore(request):
    company_id=request.session.get("company_id",None)
    if company_id==None:
        company_id=0
    page=request.GET.get('page')
    datearg=request.GET.get('datearg')
    if page==None:
        page=1
    phonerecords=ldb_weixin.getphonerecords((int(page)-1)*10,10,company_id,datearg)
    if phonerecords:
        listall=phonerecords['list']
    return render_to_response('ldb_weixin/phonerecordsmore.html',locals())
def phonerecords(request,datearg=''):
    company_id=request.session.get("company_id",None)
    username=request.session.get("username",None)
    if username and company_id==None:
        company_id=ldb_weixin.getcompanyid(username)
        request.session['company_id']=company_id
    if (username==None or company_id==None):
        return HttpResponseRedirect("/login/?done=/ldb_weixin/phonerecords.html")
    phonerecords=ldb_weixin.getphonerecords(0,10,company_id,datearg)
    if phonerecords:
        listall=phonerecords['list']
        count=phonerecords['count']
    
    return render_to_response('ldb_weixin/phonerecords.html',locals())
def lookcontact(request):
    id=request.GET.get('id')
    company_id=request.session.get("company_id",None)
    username=request.session.get("username",None)
    if username and company_id==None:
        company_id=ldb_weixin.getcompanyid(username)
        request.session['company_id']=company_id
    if (username==None or company_id==None):
        return HttpResponseRedirect("/login/?done=/ldb_weixin/phonerecords.html")
    
    contact=ldb_weixin.getcontact(id,company_id)
    
    return HttpResponse(contact)
    
def phoneclickmore(request):
    company_id=request.session.get("company_id",None)
    if company_id==None:
        company_id=0
    page=request.GET.get('page')
    if page==None:
        page=1
    phonerecords=ldb_weixin.getphoneclick((int(page)-1)*10,10,company_id)
    if phonerecords:
        listall=phonerecords['list']
    return render_to_response('ldb_weixin/phoneclickmore.html',locals())
def phoneclick(request):
    company_id=request.session.get("company_id",None)
    username=request.session.get("username",None)
    if username and company_id==None:
        company_id=ldb_weixin.getcompanyid(username)
        request.session['company_id']=company_id
    if (username==None or company_id==None):
        return HttpResponseRedirect("/login/?done=/ldb_weixin/phoneclick.html")
    phonerecords=ldb_weixin.getphoneclick(0,10,company_id)
    if phonerecords:
        listall=phonerecords['list']
    
    return render_to_response('ldb_weixin/phoneclick.html',locals())
