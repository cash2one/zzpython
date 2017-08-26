#-*- coding:utf-8 -*-
from django.shortcuts import render_to_response
from django.http import HttpResponse,HttpResponseRedirect
from zz91page import *
import os,datetime,time,re,urllib
from zz91tools import int_to_str,get_str_timeall,str_to_int,formattime,filter_tags
from zz91db_test import testdb
from zz91db_ast import companydb
dbt=testdb()
dbc=companydb()
nowpath=os.path.dirname(__file__)
execfile(nowpath+"/func/huzhu_function.py")
zzhz=huzhu_zhishi()

def detail(request):
    artid=request.GET.get('artid')
    sql='select content from bbs_zhishi where id=%s'
    result=dbt.fetchonedb(sql,[artid])
    if result:
        content=result[0]
    return render_to_response('huzhu/detail.html',locals())

def artical(request):
    page=request.GET.get('page')
    typeid=request.GET.get('typeid')
    searchlist={}
    if typeid:
        typename=zzhz.gettypename(typeid)
        searchlist['typeid']=typeid
    searchurl=urllib.urlencode(searchlist)
    typelist=zzhz.getarttypelist(frompageCount=0,limitNum=20)
    if not page:
        page=1
    funpage=zz91page()
    limitNum=funpage.limitNum(20)
    nowpage=funpage.nowpage(int(page))
    frompageCount=funpage.frompageCount()
    after_range_num = funpage.after_range_num(3)
    before_range_num = funpage.before_range_num(6)
    articallist=zzhz.getarticallist(frompageCount,limitNum,typeid)
    listcount=0
    listall=articallist['list']
    listcount=articallist['count']
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
    return render_to_response('huzhu/artical.html',locals())

def arttype(request):
    arttypelist=zzhz.getarttypelist(frompageCount=0,limitNum=20)
    return render_to_response('huzhu/arttype.html',locals())

def addartical(request):
    request_url=request.META.get('HTTP_REFERER','/')
    arttypelist=zzhz.getarttypelist(frompageCount=0,limitNum=20)
    gmt_date=time.strftime('%Y-%m-%d',time.localtime(time.time()))
    return render_to_response('huzhu/addartical.html',locals())

def updateartical(request):
    arttypelist=zzhz.getarttypelist(frompageCount=0,limitNum=20)
    request_url=request.META.get('HTTP_REFERER','/')
    artid=request.GET.get('artid')
    if artid:
        sql='select typeid,title,keywords,content,sortrank,gmt_date from bbs_zhishi where id=%s'
        result=dbt.fetchonedb(sql,[artid])
        if result:
            typeid=result[0]
            if typeid:
                typename=zzhz.gettypename(typeid)
            title=result[1]
            keywords=result[2]
            content=result[3]
            sortrank=result[4]
            gmt_date=formattime(result[5],1)
    return render_to_response('huzhu/addartical.html',locals())

def delartical(request):
    request_url=request.META.get('HTTP_REFERER','/')
    artid=request.GET.get('artid')
    sql='delete from bbs_zhishi where id=%s'
    dbt.updatetodb(sql,[artid])
    return HttpResponseRedirect(request_url)

def addarticalok(request):
    request_url=request.POST['request_url']
    artid=''
    keywords=''
    error=0
    sortrank=50
    typeid1=''
    litpic=''
    gmt_date=request.POST['gmt_date']
    title=request.POST['title']
    if request.POST.has_key('myEditor'):
        content=request.POST['myEditor']
    if request.POST.has_key('artid'):
        artid=request.POST['artid']
    if request.POST.has_key('keywords'):
        keywords=request.POST['keywords']
    if request.POST.has_key('sortrank'):
        sortrank=request.POST['sortrank']
    if request.POST.has_key('typeid1'):
        typeid1=request.POST['typeid1']
    if request.POST.has_key('litpic'):
        litpic=request.POST['litpic']
    typeid=''
    if typeid1:
        typeid=typeid1
    content_query=filter_tags(content)
    if not title:
        error=1
    if not content:
        error=1
    if error==1:
        if typeid:
            typename=zzhz.gettypename(typeid)
        arttypelist=zzhz.getarttypelist(frompageCount=0,limitNum=20)
        return render_to_response('huzhu/addartical.html',locals())
    gmt_created=datetime.datetime.now()
    if artid:
        sql='update bbs_zhishi set typeid=%s,title=%s,keywords=%s,content=%s,content_query=%s,litpic=%s,sortrank=%s,gmt_modified=%s where id=%s'
        argument=[typeid,title,keywords,content,content_query,litpic,sortrank,gmt_created,artid]
    else:
        sql='insert into bbs_zhishi(typeid,title,keywords,content,content_query,litpic,sortrank,gmt_date,gmt_created,gmt_modified) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
        argument=[typeid,title,keywords,content,content_query,litpic,sortrank,gmt_date,gmt_created,gmt_created]
    dbt.updatetodb(sql,argument)
    return HttpResponseRedirect(request_url)

