#-*- coding:utf-8 -*-
from django.shortcuts import render_to_response
from django.http import HttpResponse,HttpResponseRedirect,HttpResponsePermanentRedirect
import MySQLdb,sys,os,memcache,settings,urllib,re,time,datetime,requests
from django.core.cache import cache
from sphinxapi import *
from zz91page import *

from settings import spconfig
from function import getnowurl
from zz91db_ast import companydb
from zz91db_sms import smsdb
from zz91db_2_news import newsdb
dbc=companydb()
dbsms=smsdb()
dbn=newsdb()

reload(sys)
sys.setdefaultencoding('UTF-8')
nowpath=os.path.dirname(__file__)
execfile(nowpath+"/func/company_function.py")
execfile(nowpath+"/func/qianbao_function.py")
execfile(nowpath+"/func/trade_function.py")
execfile(nowpath+"/func/weixin_function.py")
execfile(nowpath+"/func/ldb_weixin_function.py")
execfile(nowpath+"/commfunction.py")
execfile(nowpath+"/function.py")

zzcompany=zcompany()
zzqianbao=qianbao()
zztrade=ztrade()
ldb_weixin=ldbweixin()
def companyinfo301(request):
    forcompany_id=request.GET.get("company_id")
    return HttpResponsePermanentRedirect("/company/detail"+str(forcompany_id)+".html")

def companyinfo(request,forcompany_id=""):
    host=getnowurl(request)
    #alijsload="1"
    showpost=1
    nowlanmu="<a href='/company/'>公司列表</a>"
    if not forcompany_id:
        forcompany_id=request.GET.get("company_id")
    
    company_id=request.session.get("company_id",None)
    username=request.session.get("username",None)
    if username and (company_id==None or str(company_id)=="0"):
        company_id=zztrade.getcompanyid(username)
        request.session['company_id']=company_id
    iszstflag=zztrade.getiszstcompany(forcompany_id)
    pdtid=request.GET.get("pdtid")
    list=zzcompany.getcompanydetail(forcompany_id)
    
    compzstflag=list['viptype']['vipcheck']
    weixinviewcontactflag=None
    if username:
        scoreopt=weixinscore()
        weixinviewflag=scoreopt.getviewcontact(username)
        if weixinviewflag and compzstflag==None:
            weixinviewcontactflag=1
            scoreopt.saveviewcontact(username,company_id=list['company_id'])
            
    if iszstflag==1 or compzstflag==1 or weixinviewcontactflag==1:
        viewflag=1
    else:
        viewflag=None
        
    webtitle=list['name']
    backurl=request.META.get('HTTP_REFERER','/')
    
    
    #----判断举报状态
    reportcheck=zztrade.getreportcheck(company_id,forcompany_id,0)
    if reportcheck==0:
        idcheck=1
        idchecktxt='举报处理中'
    if reportcheck==1:
        idcheck=1
        idchecktxt='举报已处理'
    if reportcheck==2:
        idcheck=1
        idchecktxt='举报退回'
    now = int(time.time())
    if now>1459440000:
        paymoney=10
    else:
        paymoney=5
    #该公司是否被举报成功过
    isjubao=zztrade.getreportischeck(forcompany_id,0)
        
    #----判断是否为来电宝用户,获取来电宝余额
    isldb=None
    viptype=zzqianbao.getviptype(company_id)
    
    if viptype=='10051003':
        isldb=1
        paymoney=5
        ldbblance=ldb_weixin.getldblaveall(company_id)
        qianbaoblance=ldbblance
    else:
        qianbaoblance=zzqianbao.getqianbaoblance2(company_id)
    
    isseecompany=zzqianbao.getisseecompany(company_id,forcompany_id)
    if not isseecompany:
        paytype=request.GET.get("paytype")
        id=0
        if paytype:
            if qianbaoblance>=paymoney:
                if isldb:
                    ldb_weixin.getpayfee(company_id,forcompany_id,paymoney)
                else:
                    zzqianbao.getpayfee(company_id,forcompany_id,id,paytype)
            else:
                isseecompany=None
    #高会查看联系方式
    isseecompany=zzqianbao.getisseecompany(company_id,forcompany_id)
    if list:
        compzstflag=list['viptype']['vipcheck']
        if iszstflag==1 or compzstflag==1:
            viewflag=1
        else:
            viewflag=None
    #高会联系方式公开
    forviptype=zzqianbao.getviptype(forcompany_id)
    forvipflag=1
    if forviptype:
        if forviptype=="100510021001" or forviptype=="100510021002" or forviptype=="100510021000" or forviptype=="10051001":
            isseecompany=1
            forvipflag=None
    
    #钱包充值广告词
    #ggc=dbc.fetchnumberdb('select txt from qianbao_gg where id=1')
    return render_to_response('company/companyinfo.html',locals())
#来电宝客户
def companyldb(request,page=""):
    return company(request,page=page,ldb="ldb")
#公司列表
def company(request,page="",ldb=""):
    host=getnowurl(request)
    alijsload="1"
    webtitle="公司列表"
    nowlanmu="<a href='/company/'>公司列表</a>"
    if not ldb:
        ldb=request.GET.get("ldb")
    else:
        nowlanmu="<a href='/company/ldb/'>来电宝公司列表</a>"
    
    keywords=request.GET.get("keywords")
    if not page:
        page=request.GET.get("page")
    username=request.session.get("username",None)
    
    if (page==None):
        page=1
    funpage = zz91page()
    limitNum=funpage.limitNum(20)
    nowpage=funpage.nowpage(int(page))
    frompageCount=funpage.frompageCount()
    after_range_num = funpage.after_range_num(5)
    before_range_num = funpage.before_range_num(4)
    
    if (str(keywords)=='None'):    
        keywords=None
    companylistall=getcompanylist(keywords,frompageCount,limitNum,ldb=ldb)
    companylist=companylistall['list']
    companylistcount=companylistall['count']
    listcount=companylistcount
    if (int(listcount)>100000):
        listcount=100000
    listcount = funpage.listcount(listcount)
    page_listcount=funpage.page_listcount()
    firstpage = funpage.firstpage()
    lastpage = funpage.lastpage()
    page_range  = funpage.page_range()
    nextpage = funpage.nextpage()
    prvpage = funpage.prvpage()
    
    if (companylistcount==1):
        morebutton='style=display:none'
    else:
        morebutton=''
    return render_to_response('company/company.html',locals())
#公司详情
def companydetail(request,company_id=""):
    host=getnowurl(request)
    alijsload="1"
    nowlanmu="<a href='/company/'>公司列表</a>"
    if not company_id:
        company_id=request.GET.get("company_id")
    username=request.session.get("username",None)
    pdtid=request.GET.get("pdtid")
    if pdtid:
        return HttpResponsePermanentRedirect("/trade/detail"+str(pdtid)+".html")
    else:
        return HttpResponseRedirect("/companyinfo/?company_id="+str(company_id))
    iszstflag=getiszstcompany(company_id)
    
    
    list=getcompanydetail(company_id)
    
    compzstflag=list['viptype']['vipcheck']
    weixinviewcontactflag=None
    if username:
        scoreopt=weixinscore()
        weixinviewflag=scoreopt.getviewcontact(username)
        if weixinviewflag and compzstflag==None:
            weixinviewcontactflag=1
            scoreopt.saveviewcontact(username,company_id=list['company_id'])
            
    if iszstflag==1 or compzstflag==1 or weixinviewcontactflag==1:
        viewflag=1
    else:
        viewflag=None
    webtitle=list['name']
    backurl=request.META.get('HTTP_REFERER','/')
    return render_to_response('company/companydetail.html',locals())

def companyproducts301(request):
    company_id=request.GET.get("company_id")
    return HttpResponsePermanentRedirect("/company/products/"+str(company_id)+"/")
#公司供求列表
def companyproducts(request,company_id="",page=""):
    host=getnowurl(request)
    alijsload="1"
    nowlanmu="<a href='/company/'>公司列表</a>"
    username=request.session.get("username",None)
    keywords=request.GET.get("keywords")
    if not company_id:
        company_id=request.GET.get("company_id")
    if not page:
        page=request.GET.get("page")
    pdt_kind = request.GET.get("ptype")
    #公司信息
    pcompinfo=getppccompanyinfo(company_id)
    if pcompinfo:
        webtitle=pcompinfo['companyname']+"供求信息"
    if (page==None):
        page=1
    funpage = zz91page()
    limitNum=funpage.limitNum(20)
    nowpage=funpage.nowpage(int(page))
    frompageCount=funpage.frompageCount()
    after_range_num = funpage.after_range_num(2)
    before_range_num = funpage.before_range_num(9)
    
    if (pdt_kind == '' or pdt_kind == None or pdt_kind=="0"):
        pdt_type=''
        pdt_kind='0'
        stab1="offerselect"
        stab2=""
        stab3=""
    if (pdt_kind =='1'):
        pdt_type='0'
        stab1=""
        stab2="offerselect"
        stab3=""
    if (pdt_kind=='2'):
        pdt_type='1'
        stab1=""
        stab2=""
        stab3="offerselect"
    
    if (str(keywords)=='None'):    
        keywords=None
    listall=getcompanyproductslist(keywords,frompageCount,limitNum,company_id,pdt_type)
    productslist=listall['list']
    productslistcount=listall['count']
    listcount=productslistcount
    if (int(listcount)>100000):
        listcount=100000
    listcount = funpage.listcount(listcount)
    page_listcount=funpage.page_listcount()
    firstpage = funpage.firstpage()
    lastpage = funpage.lastpage()
    page_range  = funpage.page_range()
    nextpage = funpage.nextpage()
    prvpage = funpage.prvpage()
    
    if (productslistcount==1):
        morebutton='style=display:none'
    else:
        morebutton=''
    return render_to_response('company/companyofferlist.html',locals())
