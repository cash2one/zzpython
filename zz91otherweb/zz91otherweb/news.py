#-*- coding:utf-8 -*-
from django.shortcuts import render_to_response
from django.http import HttpResponse,HttpResponseRedirect
import simplejson,sys
from zz91page import *
from sphinxapi import *
import os,urllib,time,xlwt,re
from zz91tools import int_to_str,get_str_timeall,str_to_int
from zz91db_130 import otherdb
from zz91db_2_news import newsdb
from settings import spconfig

dbo=otherdb()
dbn=newsdb()


nowpath=os.path.dirname(__file__)
execfile(nowpath+"/func/news_function.py")
source=newsource()
zzn=zz91news()

reload(sys) 
sys.setdefaultencoding("utf8")


def addnews(request):
    request_url=request.META.get('HTTP_REFERER','/')
    writer='admin'
    typelist=zzn.gettypelist()
    pubdate=get_str_timeall()
    return render_to_response('newsadmin/updateartical.html',locals())
def addnewsok(request):
    if request.POST.has_key('artid'):
        artid=request.POST['artid']
    request_url=request.POST['request_url']
    title=request.POST['title']
    shorttitle=request.POST['shorttitle']
    litpic=request.POST['litpic']
    click=request.POST['click']
    writer=request.POST['writer']
    body=request.POST['myEditor']
    pubdate=request.POST['pubdate']
    if pubdate:
        pubdate=str_to_int(pubdate)
    typeid=request.POST['typeid']
    typeid2=request.POST['typeid2']
    redirecturl=request.POST.get('redirecturl')
    if title and body:
        if artid:
            zzn.updatenews(title,shorttitle,pubdate,litpic,click,writer,typeid,typeid2,body,redirecturl,artid)
        else:
            zzn.addnews(title,shorttitle,litpic,click,writer,typeid,typeid2,body,pubdate,redirecturl)
    return HttpResponseRedirect(request_url)
def delete_newstype(request):
    request_url=request.META.get('HTTP_REFERER','/')
    typeid=request.GET.get('typeid')
    zzn.delnewstype(typeid)
    return HttpResponseRedirect(request_url)
def delnews(request):
    request_url=request.META.get('HTTP_REFERER','/')
    artid=request.GET.get('artid')
    zzn.delnews(artid)
    return HttpResponseRedirect(request_url)
def addnewstype(request):
    request_url=request.META.get('HTTP_REFERER','/')
    return render_to_response('newsadmin/addnewstype.html',locals())
def addnewstypeok(request):
    request_url=request.GET.get('request_url')
    typeid=request.GET.get('typeid')
    typename=request.GET.get('typename')
    sortrank=request.GET.get('sortrank')
    if not typename:
        error1='此处不能为空'
        return render_to_response('newsadmin/addnewstype.html',locals())
    if sortrank:
        sortrank=int(sortrank)
    else:
        sortrank=50
    if typeid:
        zzn.updatetype(typename,sortrank,typeid)
    else:
        zzn.addtype(typename,sortrank,0,0)
    return HttpResponseRedirect(request_url)
#----修改资讯
def updateartical(request):
    typelist=zzn.gettypelist()
    request_url=request.META.get('HTTP_REFERER','/')
    artid=int(request.GET.get('artid'))
    pubdate=get_str_timeall()
    newsdetail=zzn.getnewsdetail(artid)
    title=newsdetail['title']
    shorttitle=newsdetail['shorttitle']
    litpic=newsdetail['litpic']
    click=newsdetail['click']
    writer=newsdetail['writer']
    body=newsdetail['body']
    typeid=newsdetail['typeid']
    typeid2=newsdetail['typeid2']
    typename=newsdetail['typename']
    typename2=newsdetail['typename2']
    redirecturl=newsdetail['redirecturl']
    return render_to_response('newsadmin/updateartical.html',locals())
#----资讯栏目
def newstype(request):
    typelist=zzn.gettypelist()
    listall=typelist['list']
    reid=request.GET.get('reid')
    if reid:
        listall=zzn.getnexttype(reid)
        retypename=zzn.gettypename(reid)
    return render_to_response('newsadmin/newstype.html',locals())
def update_newstype(request):
    request_url=request.META.get('HTTP_REFERER','/')
    typeid=request.GET.get('typeid')
    typedetail=zzn.gettypedetail(typeid)
    typename=typedetail['typename']
    sortrank=typedetail['sortrank']
    return render_to_response('newsadmin/addnewstype.html',locals())
def getquickart(request):
    artid=request.GET.get('artid')
    sql='select title,shorttitle,flag,keywords,typeid,typeid2 from dede_archives where id=%s'
    result=dbn.fetchonedb(sql,artid)
    if result:
        title=result[0]
        shorttitle=result[1]
        flag=result[2]
        if not flag:
            flag=''
        keywords=result[3]
        typeid=result[4]
        typeid2=result[5]
        listdata={'title':title,'shorttitle':shorttitle,'flag':flag,'keywords':keywords,'typeid':typeid,'typeid2':typeid2}
    return HttpResponse(simplejson.dumps(listdata, ensure_ascii=False))
def updatequickok(request):
    title=request.GET.get('title')
    shorttitle=request.GET.get('shorttitle')
    flag=request.GET.get('chk_value')
    keywords=request.GET.get('keywords')
    artid=request.GET.get('artid')
    typeid_quick=request.GET.get('typeid_quick')
    typeid2_quick=request.GET.get('typeid2_quick')
    sql='update dede_archives set typeid=%s,typeid2=%s,title=%s,shorttitle=%s,flag=%s,keywords=%s where id=%s'
    dbn.updatetodb(sql,[typeid_quick,typeid2_quick,title,shorttitle,flag,keywords,artid])
    return HttpResponse('1')
#----资讯管理
def newsadmin(request):
    artid=request.GET.get('artid')
    isdel=request.GET.get('isdel')
    if artid:
        request_url=request.META.get('HTTP_REFERER','/')
        upattlist=request.GET.getlist('att')
        if upattlist:
            upattlist=','.join(upattlist)
        else:
            upattlist=''
        title=request.GET.get('title')
        keywords=request.GET.get('keywords')
        shorttitle=request.GET.get('shorttitle')
        zzn.quickupdate(upattlist,title,keywords,shorttitle,int(artid))
        return HttpResponseRedirect(request_url)
    typelist=zzn.gettypelist()
    page=request.GET.get('page')
    page_listcount=request.GET.get('page_listcount')
    typeid=request.GET.get('typeid')
    typeid2=request.GET.get('typeid2')
    urllist=request.GET.get('urllist')
    if typeid:
        typename=zzn.gettypename(typeid)
    if typeid2:
        typename2=zzn.gettypename(typeid2)
    title=request.GET.get('title')
    writer=request.GET.get('writer')
    flag=request.GET.get('flag')
    if flag:
        flagname=zzn.getflagname(flag)
    attlist=zzn.getattlist()
    searchlist={}
    if writer:
        searchlist['writer']=writer.encode('utf8')
    if typeid:
        searchlist['typeid']=typeid
    if typeid2:
        searchlist['typeid2']=typeid2
    if title:
        searchlist['title']=title.encode('utf8')
    if flag:
        searchlist['flag']=flag
    if isdel:
        searchlist['isdel']=isdel
    searchurl=urllib.urlencode(searchlist)
    if (page==None or page=='' or page=='0'):
        page=1
    elif page.isdigit()==False:
        page=1
    if page_listcount and int(page)>int(page_listcount):
        page=page_listcount
    funpage=zz91page()
    limitNum=funpage.limitNum(30)
    nowpage=funpage.nowpage(int(page))
    frompageCount=funpage.frompageCount()
    after_range_num = funpage.after_range_num(3)
    before_range_num = funpage.before_range_num(6)
    newslist=zzn.get_news_all(frompageCount,limitNum,'','',writer,flag,title,typeid,typeid2,isdel=isdel)
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
    if len(page_range)>7:
        page_range=page_range[:7]
    nextpage = funpage.nextpage()
    prvpage = funpage.prvpage()
    return render_to_response('newsadmin/list.html',locals())
#----资讯管理
def newsadmin2(request):
    artid=request.GET.get('artid')
    if artid:
        request_url=request.META.get('HTTP_REFERER','/')
        upattlist=request.GET.getlist('att')
        if upattlist:
            upattlist=','.join(upattlist)
        else:
            upattlist=''
        title=request.GET.get('title')
        shorttitle=request.GET.get('shorttitle')
        zzn.quickupdate(upattlist,title,shorttitle,int(artid))
        return HttpResponseRedirect(request_url)
    typelist=zzn.gettypelist()
    page=request.GET.get('page')
    page_listcount=request.GET.get('page_listcount')
    typeid=request.GET.get('typeid')
    typeid2=request.GET.get('typeid2')
    urllist=request.GET.get('urllist')
    if typeid:
        typename=zzn.gettypename(typeid)
    if typeid2:
        typename2=zzn.gettypename(typeid2)
    title=request.GET.get('title')
    writer=request.GET.get('writer')
    flag=request.GET.get('flag')
    if flag:
        flagname=zzn.getflagname(flag)
    attlist=zzn.getattlist()
    searchlist={}
    if writer:
        searchlist['writer']=writer.encode('utf8')
    if typeid:
        searchlist['typeid']=typeid
    if typeid2:
        searchlist['typeid2']=typeid2
    if title:
        searchlist['title']=title.encode('utf8')
    if flag:
        searchlist['flag']=flag
    searchurl=urllib.urlencode(searchlist)
    if (page==None or page=='' or page=='0'):
        page=1
    elif page.isdigit()==False:
        page=1
    if page_listcount and int(page)>int(page_listcount):
        page=page_listcount
    funpage=zz91page()
    limitNum=funpage.limitNum(30)
    nowpage=funpage.nowpage(int(page))
    frompageCount=funpage.frompageCount()
    after_range_num = funpage.after_range_num(3)
    before_range_num = funpage.before_range_num(6)
    newslist=zzn.get_news_all(frompageCount,limitNum,'','',writer,flag,title,typeid,typeid2)
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
    if len(page_range)>7:
        page_range=page_range[:7]
    nextpage = funpage.nextpage()
    prvpage = funpage.prvpage()
    return render_to_response('newsadmin/list2.html',locals())
#----资讯导出
def newsout(request):
    pubdate=request.GET.get('pubdate')
    writer=request.GET.get('writer')
    arg=request.GET.get('arg')
    if pubdate:
        pubdatearg=pubdate+' 00:00:00'
        timeArray = time.strptime(pubdatearg, "%Y-%m-%d %H:%M:%S")
        timeStamp = int(time.mktime(timeArray))
        pubdate1=timeStamp
        pubdate2=timeStamp+3600*24
        newslist=zzn.get_news_all('','',pubdate1,pubdate2,writer)
        #return HttpResponse(pubdate2)
        if newslist:
            listall=newslist['list']
            listcount=newslist['count']
            wb =xlwt.Workbook()
            ws = wb.add_sheet(u'Sheetname')
            style_k=xlwt.easyxf('align: wrap off')
            ws.col(0).width = 0x0d00 + 1000
            ws.col(1).width = 0x0d00 + 8000
            ws.col(2).width = 0x0d00 - 500
            ws.col(3).width = 0x0d00 - 500
            ws.col(4).width = 0x0d00 + 11000
            
            ws.write(0, 0, u'日期')
            ws.write(0, 1, u'标题')
            ws.write(0, 2, u'点击数')
            ws.write(0, 3, u'发布人')
            ws.write(0, 4, u'链接')
            ws.write(0, 5, u'总数:'+str(listcount))
            
            js=0
            newsurl=''
            for all in listall:
                id=all['id']
                pubdate=all['pubdate']
                title=all['title']
                click=all['click']
                writer=all['writer']
                weburl=all['weburl']
                js=js+1
                ws.write(js, 0, pubdate)
                ws.write(js, 1, title.decode('utf-8','ignore'))
                ws.write(js, 2, click)
                ws.write(js, 3, writer)
                ws.write(js, 4, weburl)
            fname = pubdate+'.xls'
            agent=request.META.get('HTTP_USER_AGENT') 
            if agent and re.search('MSIE',agent):
                response =HttpResponse(content_type="application/vnd.ms-excel") #解决ie不能下载的问题
                response['Content-Disposition'] ='attachment; filename=%s' % fname #解决文件名乱码/不显示的问题
            else:
                response =HttpResponse(content_type="application/vnd.ms-excel")#解决ie不能下载的问题
                response['Content-Disposition'] ='attachment; filename=%s' % fname #解决文件名乱码/不显示的问题
            wb.save(response)
            return response
    return HttpResponse('无数据')



def source_type(request):
    source_type=source.getsource_type()
    return render_to_response('news/source_type.html',locals())
def source_list(request):
    source_list=source.getsource_list()
    return render_to_response('news/source_list.html',locals())

#一键删除zz91资讯列表
def del_all_zz91(request):
    checkid=request.GET.getlist('checkid')
    dels=zzn.delallzz91(checkid)
    #if dels:
        #return HttpResponse(dels)
    request_url=request.META.get('HTTP_REFERER','/')
    return HttpResponseRedirect(request_url)
def back_newsall(request):
    checkid=request.GET.getlist('checkid')
    zzn.backallnews(checkid)
    request_url=request.META.get('HTTP_REFERER','/')
    return HttpResponseRedirect(request_url)



