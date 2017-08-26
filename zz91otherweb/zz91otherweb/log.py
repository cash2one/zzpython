#-*- coding:utf-8 -*-
from django.shortcuts import render_to_response
from django.http import HttpResponse,HttpResponseRedirect
from zz91page import *
from zz91tools import *
from zz91db_log import getlog
from zz91conn import database_mongodb
import urllib,sys,os
import pymongo
reload(sys)
sys.setdefaultencoding('UTF-8')
nowpath=os.path.dirname(__file__)
zzlog=getlog()
execfile(nowpath+"/func/log_function.py")
zz91log=zz91log()
#连接loginfo集合（表）
dbmongo=database_mongodb()

def lognews(request):
    logtypelist=zzlog.getlogtypelist()
    typeid=request.GET.get('typeid')
    title=request.GET.get('title')
    details=request.GET.get('details')
    page=request.GET.get('page')
    searchlist={}
    if typeid:
        typename=zzlog.getlogtypename(typeid)
        searchlist['typeid']=typeid
    if title:
        searchlist['title']=title
    if details:
        searchlist['details']=details
    searchurl=urllib.urlencode(searchlist)
    if not page:
        page=1
    funpage=zz91page()
    limitNum=funpage.limitNum(10)
    nowpage=funpage.nowpage(int(page))
    frompageCount=funpage.frompageCount()
    after_range_num = funpage.after_range_num(3)
    before_range_num = funpage.before_range_num(6)
    lognewslist=zzlog.getlognewslist(frompageCount,limitNum,typeid,title,details)
    listcount=0
    listall=lognewslist['list']
    listcount=lognewslist['count']
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
    return render_to_response('log/lognews.html',locals())

def addlognews(request):
    request_url=request.META.get('HTTP_REFERER','/')
    logtypelist=zzlog.getlogtypelist()
    return render_to_response('log/addlognews.html',locals())

def updlog_isok(request):
    request_url=request.META.get('HTTP_REFERER','/')
    is_ok=request.GET.get('is_ok')
    auto_id=request.GET.get('auto_id')
    sql='update log_auto set is_ok=%s where id=%s'
    zzlog.db.updatetodb(sql,[is_ok,auto_id])
    return HttpResponseRedirect(request_url)

def updlog_isok2(request):
    is_ok=request.GET.get('is_ok')
    auto_id=request.GET.get('auto_id')
    if is_ok=='1':
        is_ok='0'
    else:
        is_ok='1'
    sql='update log_auto set is_ok=%s where id=%s'
    zzlog.db.updatetodb(sql,[is_ok,auto_id])
    return HttpResponse('1')
    
    
def updatelognews(request):
    request_url=request.META.get('HTTP_REFERER','/')
    newsid=request.GET.get('newsid')
    newsdatail=zzlog.getnewsdatail(newsid)
    if newsdatail:
        logtypelist=zzlog.getlogtypelist()
        title=newsdatail['title']
        get_time=newsdatail['get_time']
        typeid=newsdatail['typeid']
        typename=newsdatail['typename']
        details=newsdatail['details']
        sortrank=newsdatail['sortrank']
    return render_to_response('log/addlognews.html',locals())

def addlognewsok(request):
    request_url=request.GET.get('request_url')
    title=request.GET.get('title')
    get_time=request.GET.get('get_time')
    typeid=request.GET.get('typeid')
    if typeid:
        typename=zzlog.getlogtypename(typeid)
    details=request.GET.get('details')
    sortrank=request.GET.get('sortrank')
    newsid=request.GET.get('newsid')
    error1=''
    error2=''
    error3=''
    if not title:
        error1='此处不能为空'
    if not details:
        error2='此处不能为空'
    if not get_time:
        error3='此处不能为空'
    if error1 or error2 or error3:
        logtypelist=zzlog.getlogtypelist()
        return render_to_response('log/addlognews.html',locals())
    if sortrank:
        sortrank=int(sortrank)
    else:
        sortrank=50
    if newsid:
        zzlog.updatelognews(title,get_time,typeid,details,sortrank,newsid)
    else:
        zzlog.addlognews(title,get_time,typeid,details,sortrank)
    return HttpResponseRedirect(request_url)

def log_type(request):
    logtypelist=zzlog.getlogtypelist()
    return render_to_response('log/log_type.html',locals())

def addlogtype(request):
    request_url=request.META.get('HTTP_REFERER','/')
    return render_to_response('log/addlogtype.html',locals())

def updatelogtype(request):
    request_url=request.META.get('HTTP_REFERER','/')
    typeid=request.GET.get('typeid')
    typedatail=zzlog.gettypedatail(typeid)
    if typedatail:
        typename=typedatail['name']
        sortrank=typedatail['sortrank']
    return render_to_response('log/addlogtype.html',locals())

def addlogtypeok(request):
    request_url=request.GET.get('request_url')
    typename=request.GET.get('typename')
    sortrank=request.GET.get('sortrank')
    typeid=request.GET.get('typeid')
    error1=''
    if not typename:
        error1='此处不能为空'
        return render_to_response('log/addlogtype.html',locals())
    if sortrank:
        sortrank=int(sortrank)
    else:
        sortrank=50
    if typeid:
        zzlog.updatelogtype(typename,sortrank,typeid)
    else:
        zzlog.addlogtype(typename,sortrank)
    return HttpResponseRedirect(request_url)

def del_log(request):
    request_url=request.META.get('HTTP_REFERER','/')
    gmt_begin=request.GET.get('gmt_begin')
    gmt_end=request.GET.get('gmt_end')
    if gmt_begin and gmt_end:
        zzlog.dellog(gmt_begin,gmt_end)
    return HttpResponseRedirect(request_url)

def log_list(request):
    logtypelist=zzlog.getlogtypelist()
    typeid=request.GET.get('typeid')
    title=request.GET.get('title')
    details=request.GET.get('details')
    is_ok=request.GET.get('is_ok')
    page=request.GET.get('page')
    gmt_begin=request.GET.get('gmt_begin')
    gmt_end=request.GET.get('gmt_end')
    searchlist={}
    if typeid:
        typename=zzlog.getlogtypename(typeid)
        searchlist['typeid']=typeid
    if title:
        searchlist['title']=title
    if details:
        searchlist['details']=details
    if is_ok:
        searchlist['is_ok']=is_ok
    if gmt_begin:
        searchlist['gmt_begin']=gmt_begin
    if gmt_end:
        searchlist['gmt_end']=gmt_end
    if is_ok:
        if is_ok=='1':
            is_name='成功'
        else:
            is_name='未抓'
        searchlist['is_ok']=is_ok
    searchurl=urllib.urlencode(searchlist)
    if not page:
        page=1
    funpage=zz91page()
    limitNum=funpage.limitNum(30)
    nowpage=funpage.nowpage(int(page))
    frompageCount=funpage.frompageCount()
    after_range_num = funpage.after_range_num(3)
    before_range_num = funpage.before_range_num(6)
    logpricelist=zzlog.getloglist(frompageCount,limitNum,gmt_begin,gmt_end,typeid,is_ok,title,details)
    listcount=0
    listall=logpricelist['list']
    listcount=logpricelist['count']
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
    return render_to_response('log/log_list.html',locals())
#来电宝日志分析
def ppc_log(request):
    page=request.GET.get('page')
    website=request.GET.get('website')
    status=request.GET.get('status')
    gmt_begin=request.GET.get('gmt_begin')
    gmt_end=request.GET.get('gmt_end')
    ip=request.GET.get('ip')
    searchlist={}
    if status:
        searchlist['status']=status
    if ip:
        searchlist['ip']=ip
    if website:
        searchlist['website']=website
    if gmt_begin:
        searchlist['gmt_begin']=gmt_begin
    if gmt_end:
        searchlist['gmt_end']=gmt_end
    searchurl=urllib.urlencode(searchlist)
    if not page:
        page=1
    funpage=zz91page()
    limitNum=funpage.limitNum(20)
    nowpage=funpage.nowpage(int(page))
    frompageCount=funpage.frompageCount()
    after_range_num = funpage.after_range_num(3)
    before_range_num = funpage.before_range_num(6)
    loglist=zz91log.getloglist(frompageCount,limitNum,status=status,ip=ip,website=website,gmt_begin=gmt_begin,gmt_end=gmt_end)

    listcount=0
    if (loglist):
        listall=loglist['list']
        listcount=loglist['count']
        if (int(listcount)>1000000):
            listcount=1000000-1
    listcount = funpage.listcount(listcount)
    page_listcount=funpage.page_listcount()
    firstpage = funpage.firstpage()
    lastpage = funpage.lastpage()
    page_range  = funpage.page_range()
    nextpage = funpage.nextpage()
    prvpage = funpage.prvpage()
    return render_to_response('log/ppc/log.html',locals())
#app用户日志
def zz91logall(request):
    collection=dbmongo.zzlogall
    #-----输出所有数据并分页
    #分页        
    page=request.GET.get("page")
    company_id=request.GET.get('com_id')
    clientid=request.GET.get('clientid')
    if (page==None):
        page=1
    funpage = zz91page()
    limitNum=funpage.limitNum(20)  #每页限制条数
    nowpage=funpage.nowpage(int(page))
    frompageCount=funpage.frompageCount()
    after_range_num = funpage.after_range_num(2)
    before_range_num = funpage.before_range_num(9)  
    
    #如果查询框有输入
    if company_id:
        listcount=collection.find({"company_id":company_id}).count()  #搜索的记录数
        result=collection.find({"company_id":company_id}).skip(frompageCount).limit(limitNum)
    elif clientid:
        listcount=collection.find({"clientid":clientid}).count()  #搜索的记录数
        result=collection.find({"clientid":clientid}).skip(frompageCount).limit(limitNum)
    else:        
        listcount=collection.count()    #总记录数
        result=collection.find().sort("_id",-1).skip(frompageCount).limit(limitNum)  #每页的记录和限制数
    listcount1 = funpage.listcount(listcount)
    page_listcount=funpage.page_listcount()  
    firstpage = funpage.firstpage()
    lastpage = funpage.lastpage()
    page_range  = funpage.page_range()
    nextpage = funpage.nextpage()
    prvpage = funpage.prvpage()
    
    return render_to_response('app/zz91logall.html',locals())
#错误日志
def errlog(request):
    #导入mangodb
    conn = pymongo.Connection("182.254.148.31",27017)
    #-----连接mydb库
    db = conn.zz91log
    #-----链接表
    collection=db.wwwlog
    #-----输出所有数据并分页
    #分页        
    page=request.GET.get("page")
    status=request.GET.get('status')
    website=request.GET.get('website')
    if (page==None):
        page=1
    funpage = zz91page()
    limitNum=funpage.limitNum(20)  #每页限制条数
    nowpage=funpage.nowpage(int(page))
    frompageCount=funpage.frompageCount()
    after_range_num = funpage.after_range_num(2)
    before_range_num = funpage.before_range_num(9)  
    searchlist={}
    #如果查询框有输入
    if status:
        searchlist['status']=status
    if website:
        searchlist['website']=website
    if searchlist:
        searchurl=urllib.urlencode(searchlist)
        listcount=collection.find(searchlist).count()  #搜索的记录数
        result=collection.find(searchlist).sort("_id",-1).skip(frompageCount).limit(limitNum)
    else:        
        listcount=collection.count()    #总记录数
        result=collection.find().sort("_id",-1).skip(frompageCount).limit(limitNum)  #每页的记录和限制数
    listcount1 = funpage.listcount(listcount)
    page_listcount=funpage.page_listcount()  
    firstpage = funpage.firstpage()
    lastpage = funpage.lastpage()
    page_range  = funpage.page_range()
    nextpage = funpage.nextpage()
    prvpage = funpage.prvpage()
    
    return render_to_response('log/errlog.html',locals())
#app用户日志
def appUserlog(request):
    collection=dbmongo.loginfo
    #-----输出所有数据并分页
    #分页        
    page=request.GET.get("page")
    company_id=request.GET.get('com_id')
    clientid=request.GET.get('clientid')
    visitoncode=request.GET.get('visitoncode')
    if (page==None):
        page=1
    funpage = zz91page()
    limitNum=funpage.limitNum(20)  #每页限制条数
    nowpage=funpage.nowpage(int(page))
    frompageCount=funpage.frompageCount()
    after_range_num = funpage.after_range_num(2)
    before_range_num = funpage.before_range_num(9)  
    searchlist={}
    #如果查询框有输入
    if company_id:
        searchlist['company_id']=company_id
        listcount=collection.find({"company_id":company_id}).count()  #搜索的记录数
        result=collection.find({"company_id":company_id}).skip(frompageCount).limit(limitNum)
    elif clientid:
        searchlist['clientid']=clientid
        listcount=collection.find({"clientid":clientid}).count()  #搜索的记录数
        result=collection.find({"clientid":clientid}).skip(frompageCount).limit(limitNum)
    elif visitoncode:
        searchlist['visitoncode']=visitoncode
        listcount=collection.find({"visitoncode":visitoncode}).count()  #搜索的记录数
        result=collection.find({"visitoncode":visitoncode}).skip(frompageCount).limit(limitNum)
    else:        
        listcount=collection.count()    #总记录数
        result=collection.find().sort("_id",-1).skip(frompageCount).limit(limitNum)  #每页的记录和限制数
    searchurl=urllib.urlencode(searchlist)
    
    listcount1 = funpage.listcount(listcount)
    page_listcount=funpage.page_listcount()  
    firstpage = funpage.firstpage()
    lastpage = funpage.lastpage()
    page_range  = funpage.page_range()
    nextpage = funpage.nextpage()
    prvpage = funpage.prvpage()
    
    return render_to_response('app/appUserlog.html',locals())
