# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response,render
from django.http import HttpResponse,HttpResponseRedirect
import simplejson,sys,os,urllib,re,datetime,time,md5,hashlib,random,calendar
from django.core.handlers.wsgi import WSGIRequest
from zz91db_recyclecrm import recyclecrmdb
from zz91page import *
from sphinxapi import *
from zz91settings import SPHINXCONFIG
db = recyclecrmdb(1)
reload(sys)
sys.setdefaultencoding('UTF-8')
nowpath=os.path.dirname(__file__)
execfile(nowpath+"/func/recyclecrm_function.py")
execfile(nowpath+"/func/crmtools.py")
zzs=zzrecyclecrm()
#主页面
def list(request):
    username=request.session.get('username',default=None)
    user_id=request.session.get('user_id',default=None)
    if not username or not user_id:
        return HttpResponseRedirect("/")
    page=request.GET.get('page')
    if not page:
        page=1
    funpage=zz91page()
    limitNum=funpage.limitNum(15)
    nowpage=funpage.nowpage(int(page))
    frompageCount=funpage.frompageCount()
    after_range_num = funpage.after_range_num(3)
    before_range_num = funpage.before_range_num(6)
    userallr=zzs.list(frompageCount=frompageCount,limitNum=limitNum)
    listcount=userallr['count']
    listall=userallr['list']
    listcount = funpage.listcount(listcount)
    page_listcount=funpage.page_listcount()
    firstpage = funpage.firstpage()
    lastpage = funpage.lastpage()
    page_range  = funpage.page_range()
    nextpage = funpage.nextpage()
    prvpage = funpage.prvpage()
    return render_to_response('admin/list.html',locals())
#添加客户
def add(request):
    username=request.session.get('username',default=None)
    user_id=request.session.get('user_id',default=None)
    if not username or not user_id:
        return HttpResponseRedirect("/")
    return render_to_response('admin/add.html',locals())
#保存客户
def save(request):
    username=request.session.get('username',default=None)
    user_id=request.session.get('user_id',default=None)
    if not username or not user_id:
        return HttpResponseRedirect("/")
    result=zzs.save(request)
    return HttpResponseRedirect('list.html')
#批处理客户
def all(request):
    username=request.session.get('username',default=None)
    user_id=request.session.get('user_id',default=None)
    if not username or not user_id:
        return HttpResponseRedirect("/")
    check_box_list = request.REQUEST.getlist("check_box_list")
    result=zzs.all(request,check_box_list)
    return HttpResponseRedirect('list.html')
#详情页主页面
def details(request):
    username=request.session.get('username',default=None)
    user_id=request.session.get('user_id',default=None)
    if not username or not user_id:
        return HttpResponseRedirect("/")
    userallr=zzs.details(request)
    result=userallr['result']
    company_id=request.GET.get('company_id')
    return render_to_response('admin/details.html',locals())
#公司信息
def company(request):
    username=request.session.get('username',default=None)
    user_id=request.session.get('user_id',default=None)
    if not username or not user_id:
        return HttpResponseRedirect("/")
    userallr=zzs.company(request)
    result=userallr['result']
    company_id=userallr['company_id']
    return render_to_response('admin/company.html',locals())
#公司图片
def picture(request):
    username=request.session.get('username',default=None)
    user_id=request.session.get('user_id',default=None)
    if not username or not user_id:
        return HttpResponseRedirect("/")
    userallr=zzs.picture(request)
    result=userallr['result']
    company_id=userallr['company_id']
    return render_to_response('admin/picture.html',locals())
#用户信息
def user(request):
    username=request.session.get('username',default=None)
    user_id=request.session.get('user_id',default=None)
    if not username or not user_id:
        return HttpResponseRedirect("/")
    id=request.GET.get('id')
    page=request.GET.get('page')
    if not page:
        page=1
    funpage=zz91page()
    limitNum=funpage.limitNum(15)
    nowpage=funpage.nowpage(int(page))
    frompageCount=funpage.frompageCount()
    after_range_num = funpage.after_range_num(3)
    before_range_num = funpage.before_range_num(6)
    userallr=zzs.user(frompageCount=frompageCount,limitNum=limitNum,request=request)
    listcount=userallr['count']
    listall=userallr['list']
    company_id=userallr['company_id']
    listcount = funpage.listcount(listcount)
    page_listcount=funpage.page_listcount()
    firstpage = funpage.firstpage()
    lastpage = funpage.lastpage()
    page_range  = funpage.page_range()
    nextpage = funpage.nextpage()
    prvpage = funpage.prvpage()
    return render_to_response('admin/user.html',locals())
#活动情况记录
def activity(request):
    username=request.session.get('username',default=None)
    user_id=request.session.get('user_id',default=None)
    if not username or not user_id:
        return HttpResponseRedirect("/")
    page=request.GET.get('page')
    id=request.GET.get('id')
    if not page:
        page=1
    funpage=zz91page()
    limitNum=funpage.limitNum(15)
    nowpage=funpage.nowpage(int(page))
    frompageCount=funpage.frompageCount()
    after_range_num = funpage.after_range_num(3)
    before_range_num = funpage.before_range_num(6)
    userallr=zzs.activity(frompageCount=frompageCount,limitNum=limitNum,request=request)
    listcount=userallr['count']
    listall=userallr['list']
    company_id=userallr['company_id']
    listcount = funpage.listcount(listcount)
    page_listcount=funpage.page_listcount()
    firstpage = funpage.firstpage()
    lastpage = funpage.lastpage()
    page_range  = funpage.page_range()
    nextpage = funpage.nextpage()
    prvpage = funpage.prvpage()
    return render_to_response('admin/activity.html',locals())
#用户活动情况记录
def user_activity(request):
    username=request.session.get('username',default=None)
    user_id=request.session.get('user_id',default=None)
    if not username or not user_id:
        return HttpResponseRedirect("/")
    page=request.GET.get('page')
    id=request.GET.get('id')
    if not page:
        page=1
    funpage=zz91page()
    limitNum=funpage.limitNum(15)
    nowpage=funpage.nowpage(int(page))
    frompageCount=funpage.frompageCount()
    after_range_num = funpage.after_range_num(3)
    before_range_num = funpage.before_range_num(6)
    userallr=zzs.user_activity(frompageCount=frompageCount,limitNum=limitNum,request=request)
    listcount=userallr['count']
    listall=userallr['list']
    company_id=userallr['company_id']
    listcount = funpage.listcount(listcount)
    page_listcount=funpage.page_listcount()
    firstpage = funpage.firstpage()
    lastpage = funpage.lastpage()
    page_range  = funpage.page_range()
    nextpage = funpage.nextpage()
    prvpage = funpage.prvpage()
    return render_to_response('admin/user_activity.html',locals())
#用户留言
def user_message(request):
    username=request.session.get('username',default=None)
    user_id=request.session.get('user_id',default=None)
    if not username or not user_id:
        return HttpResponseRedirect("/")
    page=request.GET.get('page')
    id=request.GET.get('id')
    if not page:
        page=1
    funpage=zz91page()
    limitNum=funpage.limitNum(15)
    nowpage=funpage.nowpage(int(page))
    frompageCount=funpage.frompageCount()
    after_range_num = funpage.after_range_num(3)
    before_range_num = funpage.before_range_num(6)
    userallr=zzs.user_message(frompageCount=frompageCount,limitNum=limitNum,request=request)
    listcount=userallr['count']
    listall=userallr['list']
    company_id=userallr['company_id']
    listcount = funpage.listcount(listcount)
    page_listcount=funpage.page_listcount()
    firstpage = funpage.firstpage()
    lastpage = funpage.lastpage()
    page_range  = funpage.page_range()
    nextpage = funpage.nextpage()
    prvpage = funpage.prvpage()
    return render_to_response('admin/message.html',locals())
#删除留言
def del_message(request):
    username=request.session.get('username',default=None)
    user_id=request.session.get('user_id',default=None)
    if not username or not user_id:
        return HttpResponseRedirect("/")
    result=zzs.del_message(request)
    return HttpResponseRedirect('list.html')
#添加用户
def add_user(request):
    username=request.session.get('username',default=None)
    user_id=request.session.get('user_id',default=None)
    if not username or not user_id:
        return HttpResponseRedirect("/")
    return render_to_response('admin/add_user.html',locals())
#保存用户
def save_user(request):
    username=request.session.get('username',default=None)
    user_id=request.session.get('user_id',default=None)
    if not username or not user_id:
        return HttpResponseRedirect("/")
    result=zzs.save_user(request)
    return HttpResponseRedirect('list.html')