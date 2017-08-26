# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response,render
from django.http import HttpResponse,HttpResponseRedirect
import simplejson,sys,os,urllib,re,datetime,time,md5,hashlib,random,calendar
from django.core.handlers.wsgi import WSGIRequest
from conn import crmdb
from zz91page import *
from sphinxapi import *
from settings import searchconfig
db = crmdb()
reload(sys)
sys.setdefaultencoding('UTF-8')
nowpath=os.path.dirname(__file__)
execfile(nowpath+"/func/news_function.py")
execfile(nowpath+"/func/crmtools.py")
zzs=zznews()

def news_list(request):
    username=request.session.get('username',default=None)
    user_id=request.session.get('user_id',default=None)
    if not username or not user_id:
        return HttpResponseRedirect("/")
    page=request.GET.get('page')
    if not page:
        page=1
    index=request.GET.get('index')
    funpage=zz91page()
    limitNum=funpage.limitNum(15)
    nowpage=funpage.nowpage(int(page))
    frompageCount=funpage.frompageCount()
    after_range_num = funpage.after_range_num(3)
    before_range_num = funpage.before_range_num(6)
    userallr=zzs.getnewslist(frompageCount=frompageCount,limitNum=limitNum,index=index)
    listcount=userallr['count']
    listall=userallr['list']
    type=userallr['type']
    listcount = funpage.listcount(listcount)
    page_listcount=funpage.page_listcount()
    firstpage = funpage.firstpage()
    lastpage = funpage.lastpage()
    page_range  = funpage.page_range()
    nextpage = funpage.nextpage()
    prvpage = funpage.prvpage()
    return render_to_response('news/news_list_admin.html',locals())

def news_add_admin(request):
    username=request.session.get('username',default=None)
    user_id=request.session.get('user_id',default=None)
    if not username or not user_id:
        return HttpResponseRedirect("/")
    result=zzs.addnews(request)
    return render_to_response('news/news_add_admin.html',locals())

def news_mod_admin(request):
    username=request.session.get('username',default=None)
    user_id=request.session.get('user_id',default=None)
    if not username or not user_id:
        return HttpResponseRedirect("/")
    userallr=zzs.modnews(request)
    result=userallr['result']
    result1=userallr['result1']
    return render_to_response('news/news_mod_admin.html',locals())

def news_del_admin(request):
    username=request.session.get('username',default=None)
    user_id=request.session.get('user_id',default=None)
    if not username or not user_id:
        return HttpResponseRedirect("/")
    check_box_list = request.REQUEST.getlist("check_box_list")
    result=zzs.delnews(request,check_box_list)
    return HttpResponseRedirect('list_admin.html')

def news_save_admin(request):
    username=request.session.get('username',default=None)
    user_id=request.session.get('user_id',default=None)
    if not username or not user_id:
        return HttpResponseRedirect("/")
    result=zzs.savenews(request)
    return HttpResponseRedirect('list_admin.html')