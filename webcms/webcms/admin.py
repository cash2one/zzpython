#-*- coding:utf-8 -*-
from django.shortcuts import render_to_response
from django.http import HttpResponse,HttpResponseRedirect
from django.core.cache import cache
from zz91tools import getToday,getYesterday,date_to_str,getnowurl
from zz91db_130 import pycmsdb
from zz91page import *
import os,datetime,time,sys,calendar,urllib
dbp=pycmsdb()
reload(sys)
sys.setdefaultencoding('UTF-8')
nowpath=os.path.dirname(__file__)
execfile(nowpath+"/func/admin_function.py")
zzp=zpycms()

#---后台首页
def default(request):
    username=request.session.get('username')
    if not username:
        return HttpResponseRedirect('/loginpage.html')
    sortrank=request.session.get('sortrank')
    if sortrank=='0':
        return HttpResponseRedirect('/loginpage.html')
    return render_to_response('admin/default.html',locals())
def returnpage(request):
    request_url=request.GET.get('request_url')
    return HttpResponseRedirect(request_url)
def userlist(request):
    page=request.GET.get('page')
    if not page:
        page=1
    funpage=zz91page()
    limitNum=funpage.limitNum(20)
    nowpage=funpage.nowpage(int(page))
    frompageCount=funpage.frompageCount()
    after_range_num = funpage.after_range_num(3)
    before_range_num = funpage.before_range_num(6)
    userlist=zzp.getuserlist(frompageCount,limitNum,'0')
    listcount=0
    listall=userlist['list']
    listcount=userlist['count']
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
    return render_to_response('admin/userlist.html',locals())
def adduser(request,typeid=''):
    nowurl=getnowurl(request)
    username=request.session.get('username')
    if not username:
        return HttpResponseRedirect('/loginpage.html?backurl='+nowurl)
    request_url=request.META.get('HTTP_REFERER','/')
    return render_to_response('admin/adduser.html',locals())
def updateuser(request,typeid=''):
    username=request.session.get('username')
    if not username:
        return HttpResponseRedirect('/loginpage.html?backurl='+nowurl)
    request_url=request.META.get('HTTP_REFERER','/')
    uid=request.GET.get('uid')
    if uid:
        sql='select username,password from py_user where id=%s'
        result=dbp.fetchonedb(sql,uid)
        if result:
            uname=result[0]
            pword=result[1]
    return render_to_response('admin/adduser.html',locals())
def deluser(request,typeid=''):
    nowurl=getnowurl(request)
    username=request.session.get('username')
    if not username:
        return HttpResponseRedirect('/loginpage.html?backurl='+nowurl)
    request_url=request.META.get('HTTP_REFERER','/')
    uid=request.GET.get('uid')
    sql='delete from py_user where id=%s'
    dbp.updatetodb(sql,[uid])
    return HttpResponseRedirect(request_url)
def adduserok(request,typeid=''):
    nowurl=getnowurl(request)
    username=request.session.get('username')
    if not username:
        return HttpResponseRedirect('/loginpage.html?backurl='+nowurl)
    user_id=request.session.get('user_id')
    request_url=request.GET.get('request_url')
    uname=request.GET.get('uname')
    pword=request.GET.get('pword')
    uid=request.GET.get('uid')
    error1=''
    error2=''
    notuser=''
    if uname:
        sql='select id from py_user where username=%s and sortrank=%s'
        result=dbp.fetchonedb(sql,[uname,0])
        if result:
            error1='帐号已存在'
            if uid:
                error1=''
                notuser=1
    else:
        error1='不能为空'
    if not pword:
        error2='不能为空'
    if error1 or error2:
        return render_to_response('admin/adduser.html',locals())
    if uid:
        if notuser:
            sql='update py_user set password=%s where id=%s'
            dbp.updatetodb(sql,[pword,uid])
        else:
            sql='update py_user set username=%s,password=%s where id=%s'
            dbp.updatetodb(sql,[uname,pword,uid])
    else:
        sql='insert into py_user(username,password,sortrank,admin_id) values(%s,%s,%s,%s)'
        dbp.updatetodb(sql,[uname,pword,0,user_id])
    return HttpResponseRedirect(request_url)


def usertemplist(request):
    page=request.GET.get('page')
    if not page:
        page=1
    funpage=zz91page()
    limitNum=funpage.limitNum(20)
    nowpage=funpage.nowpage(int(page))
    frompageCount=funpage.frompageCount()
    after_range_num = funpage.after_range_num(3)
    before_range_num = funpage.before_range_num(6)
    usertemplist=zzp.getusertemplist(frompageCount,limitNum)
    listcount=0
    listall=usertemplist['list']
    listcount=usertemplist['count']
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
    return render_to_response('admin/usertemplist.html',locals())

def usertypelist(request):
    page=request.GET.get('page')
    if not page:
        page=1
    funpage=zz91page()
    limitNum=funpage.limitNum(20)
    nowpage=funpage.nowpage(int(page))
    frompageCount=funpage.frompageCount()
    after_range_num = funpage.after_range_num(3)
    before_range_num = funpage.before_range_num(6)
    usertypelist=zzp.getusertypelist(frompageCount,limitNum)
    listcount=0
    listall=usertypelist['list']
    listcount=usertypelist['count']
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
    return render_to_response('admin/usertypelist.html',locals())