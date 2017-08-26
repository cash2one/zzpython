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
execfile(nowpath+"/func/my_function.py")
execfile(nowpath+"/func/crmtools.py")
zzs=zzmy()
#首页
def index(request):
    username=request.session.get('username',default=None)
    user_id=request.session.get('user_id',default=None)
    if not username or not user_id:
        return HttpResponseRedirect("/crm/login.html")
    result=zzs.getmyinfo(request)
    return render_to_response('my/index.html',locals())
#公司资料
def company_info(request):
    username=request.session.get('username',default=None)
    user_id=request.session.get('user_id',default=None)
    if not username or not user_id:
        return HttpResponseRedirect("/crm/login.html")
    result=zzs.getcompinfo(request)
    company_id=request.GET.get('company_id')
    return render_to_response('my/company_info.html',locals())
#保存公司资料
def compinfo_save(request):
    username=request.session.get('username',default=None)
    user_id=request.session.get('user_id',default=None)
    if not username or not user_id:
        return HttpResponseRedirect("/crm/login.html")
    result=zzs.compinfo_save(request)
    return HttpResponseRedirect('index.html',locals())
#我的联系人
def contact(request):
    username=request.session.get('username',default=None)
    user_id=request.session.get('user_id',default=None)
    if not username or not user_id:
        return HttpResponseRedirect("/crm/login.html")
    result=zzs.getmycontact(request)
    return render_to_response('my/contact.html',locals())
#修改联系人
def contact_mod(request):
    username=request.session.get('username',default=None)
    user_id=request.session.get('user_id',default=None)
    if not username or not user_id:
        return HttpResponseRedirect("/crm/login.html")
    result=zzs.contact_mod(request)
    user_id=request.GET.get('user_id')
    return render_to_response('my/contact_mod.html',locals())
#保存联系人
def contact_save(request):
    username=request.session.get('username',default=None)
    user_id=request.session.get('user_id',default=None)
    if not username or not user_id:
        return HttpResponseRedirect("/crm/login.html")
    result=zzs.contact_save(request)
    return HttpResponseRedirect('contact.html',locals())
#修改密码
def security_mod(request):
    username=request.session.get('username',default=None)
    user_id=request.session.get('user_id',default=None)
    if not username or not user_id:
        return HttpResponseRedirect("/crm/login.html")
    sql='select name from user where id=%s'
    name=db.fetchonedb(sql,[user_id])['name']
    return render_to_response('my/security_mod.html',locals())
#保存修改密码
def security_save(request):
    username=request.session.get('username',default=None)
    user_id=request.session.get('user_id',default=None)
    if not username or not user_id:
        return HttpResponseRedirect("/crm/login.html")
    result=zzs.security_save(request)
    return HttpResponseRedirect('index.html',locals())
#退出登录
def logout(request):
    username=request.session.get('username',default=None)
    user_id=request.session.get('user_id',default=None)
    if not username or not user_id:
        return HttpResponseRedirect("/crm/login.html")
    request.session.delete()
    return HttpResponseRedirect("/crm/login.html")