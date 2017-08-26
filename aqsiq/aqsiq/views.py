#-*- coding:utf-8 -*- 
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
#from function import getnewslist,hand_content
from zz91page import *
from zz91db import aqsiq,zz91company,zz91news
from zz91settings import SPHINXCONFIG_news,SPHINXCONFIG
import re,urllib
zzaqsiq=aqsiq()
zzcomp=zz91company()
zznews=zz91news()

def index2(request):
    typelist=zzaqsiq.gettypelist(4)
    return render_to_response('index2.html',locals())


def aqsiq_list2(request,typeid='',page=''):
    pricelist=zzcomp.getpricelist(SPHINXCONFIG,kname='废塑料',frompageCount=0,limitNum=8)
    newslist1=zznews.getnewslist(SPHINXCONFIG,keywords='',frompageCount=0,limitNum=1,typeid="",typeid2="",allnum=1,arg='',flag='p',MATCH=1)
    newslist2=zznews.getnewslist(SPHINXCONFIG,'',0,5)
    ntitle=request.GET.get('ntitle')
    isdelete=request.GET.get('isdelete')
    searchlist={}
    if typeid:
        searchlist['typeid']=typeid
        typename=zzaqsiq.getaqsiqtypename(typeid)
    searchurl=urllib.urlencode(searchlist)
    if not page:
        page=1
    funpage=zz91page()
    limitNum=funpage.limitNum(15)
    nowpage=funpage.nowpage(int(page))
    frompageCount=funpage.frompageCount()
    after_range_num = funpage.after_range_num(3)
    before_range_num = funpage.before_range_num(6)
    resultlist=zzaqsiq.getaqsiqnews(frompageCount,limitNum,ntitle,typeid,isdelete)
    listcount=0
    listall=resultlist['list']
    listcount=resultlist['count']
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
    return render_to_response('news/aqsiq_list2.html',locals())

def aqsiq_detail2(request,newsid='',page=''):
    aqsiqnews=zzaqsiq.getaqsiqnews(0,10,'','','',order='ncount desc')
    offerlist=zzcomp.offerlist(SPHINXCONFIG,kname="aqsiq",pdt_type="",limitcount=6,havepic="",fromlimit=0)
    aqsiqdetail=zzaqsiq.getaqsiqdetail(newsid)
    if aqsiqdetail:
        title=aqsiqdetail['ntitle']
        content=aqsiqdetail['ncontent']
        if '_ueditor_page_break_tag_' in content:
            contentlist=content.split('_ueditor_page_break_tag_')
            allnumb=len(contentlist)
            if page:
                page=int(page)
                page2=page-1
                content=contentlist[page2]
            else:
                content=contentlist[0]
            rangelist=range(1,allnumb+1)
        pubdate=aqsiqdetail['ndate']
        typeid=aqsiqdetail['ntype']
        typename=aqsiqdetail['typename']
        articalup=zzaqsiq.getarticalup(newsid,typeid)
        articalnx=zzaqsiq.getarticalnx(newsid,typeid)
    return render_to_response('news/aqsiq_detail.html',locals())

#首页
def index(request):
    list10=getnewslist(10,3)
    list1703=getnewslist(1703,5)
    list11=getnewslist(11,3)
    list13=getnewslist(13,4)
    list12=getnewslist(12,5)
    list1704=getnewslist(1704,5)
    cursor=database()
    sql="select scode,sgj,scom_name from aqsiq_comp order by scode limit 0,50"
    cursor.execute(sql)
    resultlist=cursor.fetchall()
    listall=[]
    if resultlist:
        for list in resultlist:
           list={'scode':list[0],'sgj':list[1],'scom_name':list[2]}
           listall.append(list)
    closedatabase(cursor)
    return render_to_response('index.html',locals())

def detail(request,newsid):
    cursor=database()
    sql="select ntitle,ncontent from aqsiq_news where id=%s"
    cursor.execute(sql, [newsid])
    resultlist=cursor.fetchone()
    if resultlist:
        ntitle=resultlist[0]
        ncontent=resultlist[1]
        
    closedatabase(cursor)
    return render_to_response('detail.html',locals())

def aqsiq_detail(request,newsid=''):
    cursor=database()
    sql="select scode,scom_name,sstat,sfw,sgj from aqsiq_comp where id=%s"
    cursor.execute(sql, [newsid])
    resultlist=cursor.fetchone()
    if resultlist:
        scode=resultlist[0]
        scom_name=resultlist[1]
        sstat=resultlist[2]
        sfw=resultlist[3]
        sgj=resultlist[4]
    closedatabase(cursor)
    return render_to_response('news/aqsiq_compl.html',locals())

def aqsiq_list(request,ntype):
    list=getnewslist(ntype,30)
    cursor=database()
    sql="select count(id) from aqsiq_news where ntype=%s"
    cursor.execute(sql,ntype)
    pages=cursor.fetchone()
    pages=pages[0]
    closedatabase(cursor)
    return render_to_response('news/aqsiq_list.html',locals())

def aqsiq_about(request):
    return render_to_response('news/aqsiq_about.html',locals())

def aqsiq_success(request):
    return render_to_response('news/aqsiq_success.html',locals())

def aqsiq_comp(request):
#分页
    cursor=database()
    page=request.GET.get("page")
    if (page==None):
        page=1
    else:
        page=int(page)
    pagenumber=20
    pagenumberf=(page-1)*pagenumber
    limitvalue=[(page-1)*pagenumber,pagenumber]
#搜索结果
    sgj=request.GET.get('sgj')
    scode=request.GET.get('scode')
    sstat=request.GET.get('sstat')
    scom_name=request.GET.get('scom_name')
    searmore="id>0 "
    searmorefild=[]
    searlink=""
    if (sgj and sgj!=""):
        searmore+=" and sgj=%s"
        searlink+="&sgj="+sgj
        searmorefild.append(sgj)
    if (scode and scode!=""):
        searmore+=" and scode=%s"
        searlink+="&scode="+scode
        searmorefild.append(scode)
    if (sstat and sstat!=""):
        searmore+=" and sstat=%s"
        searlink+="&sstat="+sstat
        searmorefild.append(sstat)
    if (scom_name and scom_name!=""):
        searmore+=" and scom_name = %s"
        searlink+="&scom_name="+scom_name
        searmorefild.append(scom_name)
    searmorefild.append(pagenumberf)
    searmorefild.append(pagenumber)
    sqlc="select count(0) from aqsiq_comp where "+searmore
    cursor.execute(sqlc,searmorefild[0:len(searmorefild)-2])
    resultcount=cursor.fetchone()[0]
    sql="select id,scode,scom_name,sstat,sgj from aqsiq_comp where "+searmore+" limit %s,%s"
    
    cursor.execute(sql,searmorefild)
    resultlist=cursor.fetchall()
    if resultlist:
        pages=resultcount
        pages_number=(pages/20)+1
        if (page=="" or page==None):
            page=1
        else:
            page=int(page)
     
        if (page==pages_number):
            pagenext=pages_number
        else:
            pagenext=page+1
        if (page==1):
            pageprv=1
        else:
            pageprv=page-1
        listall=[]
        for list in resultlist:
           list={'id':list[0],'scode':list[1],'scom_name':list[2],'sstat':list[3],'sgj':list[4]}
           listall.append(list)
    closedatabase(cursor)
    return render_to_response('news/aqsiq_comp.html',locals())

