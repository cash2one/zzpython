#-*- coding:utf-8 -*-
from django.shortcuts import render_to_response
import simplejson
from django.http import HttpResponse,HttpResponseRedirect,HttpResponsePermanentRedirect
import MySQLdb,sys,os,memcache,settings,urllib,re,time,datetime,random,hashlib,requests
from datetime import  * 
from django.core.cache import cache
from zz91tools import subString,filter_tags,formattime,getYesterday,getpastoneday
from zz91page import *
from zz91db_ast import companydb
from sphinxapi import *

dbc=companydb()

reload(sys)
sys.setdefaultencoding('UTF-8')
nowpath=os.path.dirname(__file__)
execfile(nowpath+"/function.py")
execfile(nowpath+"/func/trust_function.py")

zztrst=zztrust()

#采购列表
def listcaigou(request,page=""):
    webtitle="厂家直购"
    nowlanmu="<a href='/trust/'>厂家直购</a>"
    if not page:
        page=request.GET.get('page')
    showpost=1
    if not page:
        page=1
    funpage=zz91page()
    limitNum=funpage.limitNum(15)
    nowpage=funpage.nowpage(int(page))
    frompageCount=funpage.frompageCount()
    after_range_num = funpage.after_range_num(3)
    before_range_num = funpage.before_range_num(6)
    hunshayuyue=zztrst.getcaigou(frompageCount,limitNum)
    listcount=0
    listall=hunshayuyue['list']
    listcount=hunshayuyue['count']
    if int(listcount)>1000000:
        listcount=1000000-1
    listcount = funpage.listcount(listcount)
    page_listcount=funpage.page_listcount()
    firstpage = funpage.firstpage()
    lastpage = funpage.lastpage()
    page_range  = funpage.page_range()
    if len(page_range)>7:
        page_range=page_range[:7]
    nextpage = funpage.nextpage()
    prvpage = funpage.prvpage()
    return render_to_response('trust/listcaigou2.html',locals())

#免费发布
def supplyPub(request):
    webtitle="免费发布采购"
    nowlanmu="<a href='/trust/'>厂家直购</a>"
    showpost=1
    host=getnowurl(request)
    username=request.session.get("username",None)
    company_id=request.session.get("company_id",None)
    if username and (company_id==None or str(company_id)=="0"):
        company_id=getcompanyid(username)
        request.session['company_id']=company_id
    if (username==None or (company_id==None or str(company_id)=="0")):
        return HttpResponseRedirect("/login/?done="+host)
    return render_to_response('trust/supplyPub.html',locals())
def supplyPubok(request):
    merchant_url="/trust/"
    webtitle="厂家直购"
    nowlanmu="<a href='/trust/'>厂家直购</a>"
    showpost=1
    host=getnowurl(request)
    username=request.session.get("username",None)
    company_id=request.session.get("company_id",None)
    if username and (company_id==None or str(company_id)=="0"):
        company_id=getcompanyid(username)
        request.session['company_id']=company_id
    if (username==None or (company_id==None or str(company_id)=="0")):
        return HttpResponseRedirect("/login/?done="+host)
    #company_id=request.session.get("company_id",None)
    #company_id=1309958
    #获得当前日期，格式如‘150708’
    a=datetime.datetime.now()
    date_time1=a.strftime('%Y%m%d' )
    date_time=date_time1[-6:]
    #从表trust_buy获取最大的id号
    maxid=zztrst.getmaxid('trust_buy',company_id=company_id)
    buy_no=date_time+str(maxid+1)
    errflag=None
    errtext=""
    title=request.GET.get('title')
    
    
    quantity=request.GET.get('quantity')
    price=request.GET.get('price')
    color=request.GET.get('color')
    useful=request.GET.get('useful')
    level=request.GET.get('level')
    area_code=request.GET.get('area_code')
    detail=request.GET.get('detail')
    if not detail:
        errflag=1
        errtext="请输入求购详情！"
    if not title:
        errflag=1
        errtext="请填写产品名称！"
    detail_all="产品:"+title+','+"采购量:"+quantity+','+"价格:"+price+','+"颜色:"+color+','+"用途:"+useful+','+"级别:"+level+','+"所在地:"+area_code+','+"求购详情:"+detail
    status='00'  #默认为未审
    gmt_created=datetime.datetime.now()
    gmt_modified=datetime.datetime.now()
    gmt_refresh=datetime.datetime.now()
    #获得companyName,companyContact,mobile 
    #插入trust_buy
    if not errflag:
        sql='insert into trust_buy (company_id,buy_no,status,detail,gmt_created,gmt_modified,gmt_refresh)values(%s,%s,%s,%s,%s,%s,%s)'
        dbc.updatetodb(sql,[company_id,buy_no,status,detail_all,gmt_created,gmt_modified,gmt_refresh])
        return HttpResponseRedirect('/trust/supplyPubsuc.html')
    return render_to_response('trust/supplyPub.html',locals())
def supplyPubsuc(request):
    merchant_url="/trust/"
    return render_to_response('trust/supplyPubok.html',locals())
#我要供货
def supplyForm(request):
    buy_id=request.GET.get('buy_id')
    if not buy_id:
        buy_id=request.POST.get('buy_id')
    webtitle="我要供货"
    nowlanmu="<a href='/trust/'>我要供货</a>"
    showpost=1
    host=getnowurl(request)
    username=request.session.get("username",None)
    company_id=request.session.get("company_id",None)
    if username and (company_id==None or str(company_id)=="0"):
        company_id=getcompanyid(username)
        request.session['company_id']=company_id
    if (username==None or (company_id==None or str(company_id)=="0")):
        return HttpResponseRedirect("/login/?done="+host)
    
    return render_to_response('trust/supplyForm.html',locals())
def supplyFormok(request):
    webtitle="我要供货"
    nowlanmu="<a href='/trust/'>我要供货</a>"
    showpost=1
    host=getnowurl(request)
    username=request.session.get("username",None)
    company_id=request.session.get("company_id",None)
    if username and (company_id==None or str(company_id)=="0"):
        company_id=getcompanyid(username)
        request.session['company_id']=company_id
    if (username==None or (company_id==None or str(company_id)=="0")):
        return HttpResponseRedirect("/login/?done="+host)
    buy_id=request.POST.get('buy_id')
    #buy_no=request.GET.get('buy_no')
    content=request.POST.get('content')
    errflag=None
    errtext=""
    if not content:
        errflag=1
        errtext="请输入货物详情！"
    gmt_created=datetime.datetime.now()
    gmt_modified=datetime.datetime.now()
    status='00'#默认报价已报
    
    if not errflag:
    
        sql='insert into trust_sell (company_id,status,content,gmt_created,gmt_modified)values(%s,%s,%s,%s,%s)'
        dbc.updatetodb(sql,[company_id,status,content,gmt_created,gmt_modified])
        
        #插入供需关系表trust_relate_sell
        sell_id=zztrst.getmaxid('trust_sell',company_id=company_id)
        sql1='insert into trust_relate_sell (buy_id,sell_id,gmt_created,gmt_modified)values(%s,%s,%s,%s)'
        dbc.updatetodb(sql1,[buy_id,sell_id,gmt_created,gmt_modified])
        return HttpResponseRedirect('/trust/supplyFormsuc.html')
    return render_to_response('trust/supplyForm.html',locals())
def supplyFormsuc(request):
    merchant_url="/trust/"
    return render_to_response('trust/supplyFormok.html',locals())
def listmycaigou(request):
    webtitle="我的采购单"
    nowlanmu="<a href='/trust/'>我的采购单</a>"
    showpost=1
    host=getnowurl(request)
    username=request.session.get("username",None)
    company_id=request.session.get("company_id",None)
    if username and (company_id==None or str(company_id)=="0"):
        company_id=getcompanyid(username)
        request.session['company_id']=company_id
    if (username==None or (company_id==None or str(company_id)=="0")):
        return HttpResponseRedirect("/login/?done="+host)
    
    page=request.GET.get('page')
    ptype=request.GET.get('ptype')
    searchlist={}
    if ptype:
        searchlist['ptype']=ptype
    searchurl=urllib.urlencode(searchlist)
    if not page:
        page=1
    funpage=zz91page()
    limitNum=funpage.limitNum(20)
    nowpage=funpage.nowpage(int(page))
    frompageCount=funpage.frompageCount()
    after_range_num = funpage.after_range_num(3)
    before_range_num = funpage.before_range_num(6)
    keywordslist= zztrst.getmycaigou(frompageCount,limitNum,ptype=ptype,company_id=company_id)
    listcount=0
    listall=keywordslist['list']
    listcount=keywordslist['count']
    if (int(listcount)>1000000):
        listcount=1000000-1
    listcount = funpage.listcount(listcount)
    page_listcount=funpage.page_listcount()
    firstpage = funpage.firstpage()
    lastpage = funpage.lastpage()
    page_range  = funpage.page_range()
    if len(page_range)>7:
        page_range=page_range[:7]
    nextpage = funpage.nextpage()
    prvpage = funpage.prvpage()
    return render_to_response('trust/listmycaigou.html',locals())

def listmysupply(request):
    webtitle="我的供货单"
    nowlanmu="<a href='/trust/'>我的供货单</a>"
    showpost=1
    host=getnowurl(request)
    username=request.session.get("username",None)
    company_id=request.session.get("company_id",None)
    if username and (company_id==None or str(company_id)=="0"):
        company_id=getcompanyid(username)
        request.session['company_id']=company_id
    if (username==None or (company_id==None or str(company_id)=="0")):
        return HttpResponseRedirect("/login/?done="+host)
    
    page=request.GET.get('page')
    ptype=request.GET.get('ptype')
    searchlist={}
    if ptype:
        searchlist['ptype']=ptype
    searchurl=urllib.urlencode(searchlist)
    if not page:
        page=1
    funpage=zz91page()
    limitNum=funpage.limitNum(20)
    nowpage=funpage.nowpage(int(page))
    frompageCount=funpage.frompageCount()
    after_range_num = funpage.after_range_num(3)
    before_range_num = funpage.before_range_num(6)
    keywordslist= zztrst.getmysupply(frompageCount,limitNum,ptype=ptype,company_id=company_id)
    listcount=0
    listall=keywordslist['list']
    listcount=keywordslist['count']
    if (int(listcount)>1000000):
        listcount=1000000-1
    listcount = funpage.listcount(listcount)
    page_listcount=funpage.page_listcount()
    firstpage = funpage.firstpage()
    lastpage = funpage.lastpage()
    page_range  = funpage.page_range()
    if len(page_range)>7:
        page_range=page_range[:7]
    nextpage = funpage.nextpage()
    prvpage = funpage.prvpage()
    return render_to_response('trust/listmysupply.html',locals())


