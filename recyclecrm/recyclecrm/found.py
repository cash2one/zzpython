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

#发现
def index(request):
    username=request.session.get('username',default=None)
    user_id=request.session.get('user_id',default=None)
    if not username or not user_id:
        return HttpResponseRedirect("/crm/login.html")
    return render_to_response('found/index.html', locals())