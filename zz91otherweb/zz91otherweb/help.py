#-*- coding:utf-8 -*-
from django.shortcuts import render_to_response
from django.http import HttpResponse,HttpResponseRedirect
import urllib,sys,os
from zz91page import *
from zz91db_help import helpdb
dbh=helpdb()
reload(sys)
sys.setdefaultencoding('UTF-8')
nowpath=os.path.dirname(__file__)
execfile(nowpath+"/func/help_function.py")
zzhelp=zhelp()

#-----帮助栏目
def help_column(request):
    request_url=request.META.get('HTTP_REFERER','/')
    pid=request.GET.get('pid')
    page=request.GET.get('page')
    searchlist={}
    if not page:
        page=1
    if pid:
        searchlist['pid']=pid
    searchurl=urllib.urlencode(searchlist)
    funpage=zz91page()
    limitNum=funpage.limitNum(20)
    nowpage=funpage.nowpage(int(page))
    frompageCount=funpage.frompageCount()
    after_range_num = funpage.after_range_num(3)
    before_range_num = funpage.before_range_num(6)
    columnlist=zzhelp.getcolumn(pid=pid)
    listcount=0
    listall=columnlist['list']
    listcount=columnlist['count']
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
    return render_to_response('help/help_column.html',locals())

#更新与增加操作
def add_father_column(request):
    request_url=request.META.get('HTTP_REFERER','/')
    cid=request.GET.get('cid')
    pid=request.GET.get('pid')
    if pid:
        if int(pid)==0:
            addson=1
            #sql1=
    sql='select cid,cat_name,pid from bz_category where cid=%s'
    result=dbh.fetchonedb(sql,[cid])
    if result:
        cid=result[0]
        cat_name=result[1]
        pid=result[2]
    return render_to_response('help/add_father_column.html',locals())
def add_father_columnok(request):
    request_url=request.GET.get('request_url')
    cat_name=request.GET.get('cat_name')
    cid=request.GET.get('cid')
    pid=request.GET.get('pid')
    if cid and cid!='':
        if pid and int(pid)==0:
            sql='insert into bz_category (cat_name,pid) values (%s,%s)'
            dbh.updatetodb(sql,[cat_name,cid])
        else:
            sql='update bz_category set CAT_NAME=%s where cid=%s'
            dbh.updatetodb(sql,[cat_name,cid])
    else:
        sql='insert into bz_category (cat_name) values (%s)'
        dbh.updatetodb(sql,[cat_name])
    return HttpResponseRedirect(request_url)

#删除
def delete_column(request):
    cid=request.GET.get('cid')
    now=request.GET.get('now')
    if now:
        if int(now)==0:
        #删除父
            sql='delete from bz_category where pid=%s'
            dbh.updatetodb(sql,[cid])
            sql1='delete from bz_category where cid=%s'
            dbh.updatetodb(sql1,[cid])
            #删除旗下所有内
            #sql2='delete from bz_article where '
        if int(now)==1:
        #删除子    
            sql='delete from bz_category where cid=%s'
            dbh.updatetodb(sql,[cid])
            #删除旗下所有内容
    request_url=request.META.get('HTTP_REFERER','/')
    return HttpResponseRedirect(request_url)

#返回列表页
def help_returnpage(request):
    request_url=request.GET.get('request_url')
    #request_url=request.META.get('HTTP_REFERER','/')
    return HttpResponseRedirect(request_url)

#-----帮助列表页
def help_artical(request):
    #获得所有父栏目
    columnlist=zzhelp.getcolumnlist()
    #获得所有子栏目
    #soncolumn
    page=request.GET.get('page')
    subject=request.GET.get('subject')
    typeid=request.GET.get('typeid')
    if typeid:
        typename=zzhelp.getcatname(typeid)
    searchlist={}
    if not page:
        page=1
    if typeid:
        searchlist['typeid']=typeid
    if subject:
        searchlist['subject']=subject
    searchurl=urllib.urlencode(searchlist)
    funpage=zz91page()
    limitNum=funpage.limitNum(20)
    nowpage=funpage.nowpage(int(page))
    frompageCount=funpage.frompageCount()
    after_range_num = funpage.after_range_num(3)
    before_range_num = funpage.before_range_num(6)
    articallist=zzhelp.getarticallist(frompageCount,limitNum,subject,typeid)
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
    return render_to_response('help/help_artical.html',locals())

#增加或修改页面
def addhelpartical(request):
    request_url=request.META.get('HTTP_REFERER','/')
    writer='admin'
    columnlist=zzhelp.getcolumnlist()
    aid=request.GET.get('aid')
    if aid:
        helpdetail=zzhelp.gethelpdetail(aid)
        u_aid=helpdetail['aid']
        cat_id=helpdetail['cat_id']
        typename=zzhelp.getcatname(cat_id)
        subject=helpdetail['subject']
        content=helpdetail['content']
    return render_to_response('help/addhelpartical.html',locals())
#增加或修改页面确认
def addhelparticalok(request):
    request_url=request.POST.get('request_url')
    aid=request.POST.get('aid')
    cat_id=request.POST.get('cat_id')
    subject=request.POST.get('subject')
    content=request.POST.get('myEditor')
    if subject and content and cat_id:
        if aid:
            zzhelp.updatehelpartical(cat_id,subject,content,aid)
        else:
            zzhelp.addhelpartical(cat_id,subject,content)
    return HttpResponseRedirect(request_url)

def deletehelpartical(request):
    aid=request.GET.get('aid')
    sql='delete from bz_article where aid=%s'
    dbh.updatetodb(sql,[aid])
    request_url=request.META.get('HTTP_REFERER','/')
    return HttpResponseRedirect(request_url)




