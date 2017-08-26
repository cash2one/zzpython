# -*- coding:utf-8 -*-
from django.shortcuts import render,render_to_response
from django.http import HttpResponse,HttpResponseRedirect
import simplejson,sys,os,urllib,urllib2,re,datetime,time,md5,hashlib,random,calendar
import json
import random
import time
from django.core.handlers.wsgi import WSGIRequest
from zz91db_recyclecrm import recyclecrmdb
from zz91db_ast import companydb
from zz91page import *
from sphinxapi import *
from zz91settings import SPHINXCONFIG


db=recyclecrmdb(1)
dbc=companydb(1)
reload(sys)
sys.setdefaultencoding('UTF-8')
nowpath=os.path.dirname(__file__)
execfile(nowpath+"/func/message_function.py")
execfile(nowpath+"/func/crmtools.py")
zzs=zzmessage()
#首页
def index(request):
    username=request.session.get('username',default=None)
    user_id=request.session.get('user_id',default=None)
    if not username or not user_id:
        return HttpResponseRedirect("/crm/login.html")
    result=zzs.getnumber(request)
    return render_to_response('message/index.html',locals())

#消息留言
def leave(request):
    username=request.session.get('username',default=None)
    user_id=request.session.get('user_id',default=None)
    if not username or not user_id:
        return HttpResponseRedirect("/crm/login.html")
    listall=zzs.leavemessage(request)
    return render_to_response('message/leave.html', locals())
#消息留言列表
def leave_list(request):
    username=request.session.get('username',default=None)
    user_id=request.session.get('user_id',default=None)
    if not username or not user_id:
        return HttpResponseRedirect("/crm/login.html")
    listall=zzs.leave_list(request)['result']
    user_id=zzs.leave_list(request)['user_id']
    return render_to_response('message/leave_list.html', locals())
#消息留言回复最终页
def leave_last(request):
    username=request.session.get('username',default=None)
    user_id=request.session.get('user_id',default=None)
    if not username or not user_id:
        return HttpResponseRedirect("/crm/login.html")
    user_id=request.GET.get('user_id')
    return render_to_response('message/leave_last.html', locals())
#回复客户消息
def reply(request):
    username=request.session.get('username',default=None)
    user_id=request.session.get('user_id',default=None)
    if not username or not user_id:
        return HttpResponseRedirect("/crm/login.html")
    result=zzs.reply(request)
    my_user_id=request.session.get('user_id',default=None)
    listall=zzs.leave_list(request)['result']
    return render_to_response('message/leave_list.html', locals())
#消息通知_我的
def notification1(request):
    username=request.session.get('username',default=None)
    user_id=request.session.get('user_id',default=None)
    if not username or not user_id:
        return HttpResponseRedirect("/crm/login.html")
    return render_to_response('message/notification1.html', locals())
#消息通知_系统消息
def notification2(request):
    username=request.session.get('username',default=None)
    user_id=request.session.get('user_id',default=None)
    if not username or not user_id:
        return HttpResponseRedirect("/crm/login.html")
    return render_to_response('message/notification2.html', locals())
#消息代办
def commission(request):
    username=request.session.get('username',default=None)
    user_id=request.session.get('user_id',default=None)
    if not username or not user_id:
        return HttpResponseRedirect("/crm/login.html")
    return render_to_response('message/commission.html', locals())