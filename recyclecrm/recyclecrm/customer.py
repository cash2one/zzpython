# -*- coding:utf-8 -*-
from django.shortcuts import render,render_to_response
from django.http import HttpResponse,HttpResponseRedirect
import simplejson,sys,os,urllib,re,datetime,time,md5,hashlib,random,calendar
from django.core.handlers.wsgi import WSGIRequest
from zz91db_recyclecrm import recyclecrmdb
from zz91page import *
from sphinxapi import *
from zz91settings import SPHINXCONFIG
db=recyclecrmdb(1)
reload(sys)
sys.setdefaultencoding('UTF-8')
nowpath=os.path.dirname(__file__)
execfile(nowpath+"/func/customer_function.py")
execfile(nowpath+"/func/crmtools.py")
zzs=zzcustomer()
#我的客户
def list(request):
    username=request.session.get('username',default=None)
    user_id=request.session.get('user_id',default=None)
    if not username or not user_id:
        return HttpResponseRedirect("/crm/login.html")
    userall=zzs.list(request)
    listall=userall['listall']
    return render_to_response('customer/list.html',locals())
#管理我的客户
def manage(request):
    username=request.session.get('username',default=None)
    user_id=request.session.get('user_id',default=None)
    if not username or not user_id:
        return HttpResponseRedirect("/crm/login.html")
    userall=zzs.list(request)
    listall=userall['listall']
    return render_to_response('customer/manage.html',locals())
#批量处理我的客户
def all(request):
    username=request.session.get('username',default=None)
    user_id=request.session.get('user_id',default=None)
    if not username or not user_id:
        return HttpResponseRedirect("/crm/login.html")
    result=zzs.all(request)
    date={"answer":"answer"}
    return HttpResponse(simplejson.dumps(data), ensure_ascii=False)
#联系我的客户
def contact(request):
    username=request.session.get('username',default=None)
    user_id=request.session.get('user_id',default=None)
    if not username or not user_id:
        return HttpResponseRedirect("/crm/login.html")
    value=request.GET.get('dotype')
    user_id=request.GET.get('user_id')
    mobile=request.GET.get('mobile')
    if not value:
        return render_to_response('customer/contactnow.html',locals())
    elif value=='call':
        return render_to_response('customer/call.html',locals())
    elif value=='text':
        return render_to_response('customer/text.html',locals())
    elif value=='date':
        return render_to_response('customer/date.html',locals())
#操作记录
def remark(request):
    username=request.session.get('username',default=None)
    user_id=request.session.get('user_id',default=None)
    if not username or not user_id:
        return HttpResponseRedirect("/crm/login.html")
    result=zzs.remark(request)
    return HttpResponseRedirect('list.html')
#丢公海
def throw(request):
    username=request.session.get('username',default=None)
    user_id=request.session.get('user_id',default=None)
    if not username or not user_id:
        return HttpResponseRedirect("/crm/login.html")
    result=zzs.throw(request)
    return HttpResponseRedirect('list.html')
#+行动
def action(request):
    username=request.session.get('username',default=None)
    user_id=request.session.get('user_id',default=None)
    if not username or not user_id:
        return HttpResponseRedirect("/crm/login.html")
    if request.method=='GET':
        user_id=request.GET.get('user_id')
        return render_to_response('customer/action.html')
    else:
        result=zzs.action(request)
        return HttpResponseRedirect('list.html')