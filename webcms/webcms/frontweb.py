#-*- coding:utf-8 -*-
from django.shortcuts import render_to_response
from django.http import HttpResponse,HttpResponseRedirect
import simplejson
from django.core.cache import cache
from zz91tools import getToday,getYesterday,date_to_str,formattime,getnowurl
from zz91settings import pycmspath,ftpconn,pycmsurl,pyuploadpath,pyimgurl
from zz91db_130 import pycmsdb,otherdb
from zz91page import *
import os,datetime,time,sys,calendar,urllib,random
dbp=pycmsdb()
dbo=otherdb()
reload(sys)
sys.setdefaultencoding('UTF-8')
nowpath=os.path.dirname(__file__)
execfile(nowpath+"/func/function.py")
zzp=zzpycms()
cmspinyin = pinyin()

#from views import htmlurl

def weblist(request,pinyin="",pinyin1="",pinyin2="",webid="",page=""):
    domainlist=gethostname(request)
    subname=domainlist['subname']
    domain=domainlist['domain']
    user_id=zzp.getuseridfromsite(domain)
    if user_id:
        if pinyin1:
            pinyin=pinyin1
        list=zzp.getvaluefrompinyinsite(pinyin,user_id)
        if list:
            pageid=str(list['pageid'])
            arttypeid=list['id']
        else:
            pageid="1"
            arttypeid=None
        if webid:
            pageid="3"
        if page:
            pageid="2"
        #return HttpResponse(pageid)
        return zzp.htmlurl(request,type=pageid,user_id=user_id,artid=webid,arttypeid=arttypeid,page=page)
        if pinyin2:
            return
    return HttpResponse(domain)