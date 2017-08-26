#-*- coding:utf-8 -*-
import MySQLdb   
import settings
import codecs
from django.utils.http import urlquote
from django.shortcuts import render_to_response
from django.http import HttpResponse,HttpResponseRedirect
from django.core.paginator import Paginator,InvalidPage,EmptyPage,PageNotAnInteger
import time
import sys
import datetime
from datetime import timedelta, date 
from django.views.decorators.cache import cache_control
import os
from django.core.cache import cache
import random
import shutil
try:
    import cPickle as pickle
except ImportError:
    import pickle

from math import ceil
from sphinxapi import *
from zz91conn import database_comp
reload(sys)
sys.setdefaultencoding('UTF-8')
conn = database_comp()   
cursor = conn.cursor()
#返回高会
def getcomplist():
    #-------------供求列表
    port = settings.SPHINXCONFIG['port']
    cl = SphinxClient()
    cl.SetServer ( settings.SPHINXCONFIG['serverid'], port )
    cl.SetMatchMode ( SPH_MATCH_BOOLEAN )
    cl.SetSortMode( SPH_SORT_EXTENDED," gmt_start desc" )
    cl.SetLimits (0,300)
    cl.SetFilter('apply_status',[1])
    nowdate=date.today()-timedelta(days=90)
    nextday=date.today()+timedelta(days=1)
    formatnowdate=time.mktime(nowdate.timetuple())
    formatnextday=time.mktime(nextday.timetuple())
    cl.SetFilterRange('gmt_start',int(formatnowdate),int(formatnextday))
    
    res = cl.Query ('','company')
    if res:
        if res.has_key('matches'):
            itemlist=res['matches']
            listall_company=[]
            for match in itemlist:
                id=match['id']
                attrs=match['attrs']
                comname=attrs['compname']
                business=attrs['pbusiness']
                area_province=attrs['parea_province']
                domain_zz91=attrs['domain_zz91']
                list={'id':id,'comname':comname,'business':business,'area_province':area_province,'domain_zz91':domain_zz91}
                listall_company.append(list)
            return listall_company
def default(request):
    companylist=getcomplist()
    return render_to_response('default.html',locals())
def about(request):
    return render_to_response('about.html',locals())
def apply(request):
    return render_to_response('apply.html',locals())
def payment(request):
    return render_to_response('payment.html',locals())
    
def apply_save(request):
    title=request.GET.get("title")
    contents=request.GET.get("contents")
    requestType=request.GET.get("requestType")
    if (requestType=='7'):
        sutype=1
    else:
        sutype=None
    gmt_creatdate=datetime.datetime.now()
    value=[title,contents,gmt_creatdate]
    sql="insert into subject_baoming(title,contents,gmt_created) values(%s,%s,%s)"
    cursor.execute(sql,value)
    conn.commit()
    return render_to_response('apply_save.html',locals())