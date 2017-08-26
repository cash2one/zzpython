#-*- coding:utf-8 -*-
from django.shortcuts import render_to_response
import simplejson
from django.http import HttpResponse,HttpResponseRedirect,HttpResponsePermanentRedirect
import MySQLdb,sys,os,memcache,settings,urllib,re,time,datetime,random,hashlib,requests
from datetime import  * 
from django.core.cache import cache
from settings import spconfig,appurl
from zz91tools import subString,filter_tags,formattime,getYesterday,getpastoneday
from zz91page import *
from zz91db_ast import companydb
from sphinxapi import *

dbc=companydb()

reload(sys)
sys.setdefaultencoding('UTF-8')
nowpath=os.path.dirname(__file__)
execfile(nowpath+"/func/public_function.py")
execfile(nowpath+"/func/trust_function.py")

zztrst=zztrust()

#采购列表
def listcaigou(request):
    page=request.GET.get('page')
    keywords=request.GET.get('keywords')
    if not page:
        page=1
    funpage=zz91page()
    limitNum=funpage.limitNum(15)
    nowpage=funpage.nowpage(int(page))
    frompageCount=funpage.frompageCount()
    after_range_num = funpage.after_range_num(3)
    before_range_num = funpage.before_range_num(6)
    if not keywords:
        hunshayuyue=zztrst.getcaigou(frompageCount,limitNum)
    else:
        hunshayuyue=zztrst.getcaigoulist(keywords=keywords,frompageCount=frompageCount,limitNum=limitNum)
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
    resultlist={"error_code":0,"reason":"","result":listall,"lastpage":page_listcount,'listcount':listcount}
    response = HttpResponse(simplejson.dumps(resultlist, ensure_ascii=False))
    #response['Access-Control-Allow-Origin'] = '*'
    #response['Access-Control-Allow-Headers'] = 'Access-Control-Allow-Origin, x-requested-with, content-type'
    
    return response
    return render_to_response('trust/listcaigou2.html',locals())

#免费发布
def supplyPub(request):
    return render_to_response('trust/supplyPub.html',locals())
def supplyPubok(request):
    #company_id=request.session.get("company_id",None)
    company_id=request.POST.get("company_id")
    if not company_id:
        company_id=request.GET.get("company_id")
    usertoken=request.POST.get("usertoken")
    if not getloginstatus(company_id,usertoken):
        errlist={'tokenerr':'true'}
        return HttpResponse(simplejson.dumps(errlist, ensure_ascii=False))
    if not company_id or str(company_id)=="0":
        return HttpResponse("err")
    #获得当前日期，格式如‘150708’
    a=datetime.datetime.now()
    date_time1=a.strftime('%Y%m%d' )
    date_time=date_time1[-6:]
    #从表trust_buy获取最大的id号
    maxid=zztrst.getmaxid('trust_buy',company_id=company_id)
    buy_no=date_time+str(maxid+1)
    
    title=request.POST.get('title')
    if not title:
        title=request.GET.get('title')
    quantity=request.POST.get('quantity')
    if not quantity:
        quantity=request.GET.get('quantity')
    price=request.POST.get('price')
    if not price:
        price=request.GET.get('price')
    color=request.POST.get('color')
    if not color:
        color=request.GET.get('color')
    useful=request.POST.get('useful')
    if not useful:
        useful=request.GET.get('useful')
    level=request.POST.get('level')
    if not level:
        level=request.GET.get('level')
    area_code=request.POST.get('area_code')
    if not area_code:
        area_code=request.GET.get('area_code')
    detail=request.POST.get('detail')
    if not detail:
        detail=request.GET.get('detail')
    detail_all="产品:"+title+','+"采购量:"+quantity+','+"价格:"+price+','+"颜色:"+color+','+"用途:"+useful+','+"级别:"+level+','+"所在地:"+area_code+','+"求购详情:"+detail
    status='00'  #默认为未审
    gmt_created=datetime.datetime.now()
    gmt_modified=datetime.datetime.now()
    gmt_refresh=datetime.datetime.now()
    #获得companyName,companyContact,mobile 
    #插入trust_buy
    sql='insert into trust_buy (company_id,buy_no,status,detail,gmt_created,gmt_modified,gmt_refresh)values(%s,%s,%s,%s,%s,%s,%s)'
    dbc.updatetodb(sql,[company_id,buy_no,status,detail_all,gmt_created,gmt_modified,gmt_refresh])
    resultlist={"error_code":0,"reason":"","result":"","lastpage":0}
    response = HttpResponse(simplejson.dumps(resultlist, ensure_ascii=False))
    return response
    return render_to_response('trust/supplyPubok.html',locals())

#我要供货
def supplyForm(request):
    buy_id=request.GET.get('id')
    return render_to_response('trust/supplyForm.html',locals())
def supplyFormok(request):
    #company_id=request.session.get("company_id",None)
    company_id=request.POST.get("company_id")
    if not company_id:
        company_id=request.GET.get("company_id")
    usertoken=request.POST.get("usertoken")
    if not getloginstatus(company_id,usertoken):
        errlist={'tokenerr':'true'}
        return HttpResponse(simplejson.dumps(errlist, ensure_ascii=False))
    if not company_id or str(company_id)=="0":
        return HttpResponse("err")
    buy_id=request.POST.get('buy_id')
    if not buy_id:
        buy_id=request.GET.get('buy_id')
    #buy_no=request.GET.get('buy_no')
    content=request.POST.get('content')
    if not content:
        content=request.GET.get('content')
    gmt_created=datetime.datetime.now()
    gmt_modified=datetime.datetime.now()
    status='00'#默认报价已报
    sql='insert into trust_sell (company_id,status,content,gmt_created,gmt_modified)values(%s,%s,%s,%s,%s)'
    result=dbc.updatetodb(sql,[company_id,status,content,gmt_created,gmt_modified])
    if result:
        sell_id=result[0]
        #插入供需关系表trust_relate_sell
        #sell_id=zztrst.getmaxid('trust_sell',company_id=company_id)
        sql1='insert into trust_relate_sell (buy_id,sell_id,gmt_created,gmt_modified)values(%s,%s,%s,%s)'
        dbc.updatetodb(sql1,[buy_id,sell_id,gmt_created,gmt_modified])
        resultlist={"error_code":0,"reason":"","result":"","lastpage":0}
        response = HttpResponse(simplejson.dumps(resultlist, ensure_ascii=False))
    else:
        resultlist={"error_code":1,"reason":"","result":"","lastpage":0}
        response = HttpResponse(simplejson.dumps(resultlist, ensure_ascii=False))
    return response

def listmycaigou(request):
    #company_id=request.session.get("company_id",None)
    company_id=request.GET.get("company_id")
    usertoken=request.GET.get("usertoken")
    """
    if not getloginstatus(company_id,usertoken):
        errlist={'tokenerr':'true'}
        return HttpResponse(simplejson.dumps(errlist, ensure_ascii=False))
    """
    if not company_id or str(company_id)=="0":
        return HttpResponse("err")
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
    resultlist={"error_code":0,"reason":"","result":listall,"lastpage":page_listcount,'listcount':listcount}
    response = HttpResponse(simplejson.dumps(resultlist, ensure_ascii=False))
    return response
    return render_to_response('trust/listmycaigou.html',locals())

def listmysupply(request):
    #company_id=request.session.get("company_id",None)
    company_id=request.GET.get("company_id")
    usertoken=request.GET.get("usertoken")
    """
    if not getloginstatus(company_id,usertoken):
        errlist={'tokenerr':'true'}
        return HttpResponse(simplejson.dumps(errlist, ensure_ascii=False))
    """
    if not company_id or str(company_id)=="0":
        return HttpResponse("err")
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
    resultlist={"error_code":0,"reason":"","result":listall,"lastpage":page_listcount,'listcount':listcount}
    response = HttpResponse(simplejson.dumps(resultlist, ensure_ascii=False))
    return response
    return render_to_response('trust/listmysupply.html',locals())


