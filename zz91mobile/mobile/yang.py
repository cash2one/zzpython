#-*- coding:utf-8 -*-
from django.shortcuts import render_to_response
from django.http import HttpResponse,HttpResponseRedirect,HttpResponsePermanentRedirect
import MySQLdb,sys,os,memcache,settings,urllib,re,time,datetime,requests
from django.core.cache import cache

from commfunction import subString,filter_tags,replacepic,formattime,getjiami
from function import getnowurl
from zz91page import *
from zz91db_ast import companydb
from zz91db_sms import smsdb
from sphinxapi import *
from settings import spconfig

reload(sys)
sys.setdefaultencoding('UTF-8')
nowpath=os.path.dirname(__file__)
execfile(nowpath+"/func/yang_function.py")
dbc=companydb()
zzyang=yang()
dbsms=smsdb()


#----交易中心列表页广告
def yangad(request):
    keywords=request.GET.get("keywords")
    adposition=request.GET.get("adposition")
    w=request.GET.get("w")
    l=request.GET.get("l")
    if not l:
        l=6
    if not w:
        w=170
    if w:
        w1=int(w)-2
    adlistall=zzyang.yangprolist(limit=int(l),keywords=keywords,adposition=adposition)
    adlist=adlistall["listall"]
    adcount=adlistall['listcount']
    if w:
        w_all=adcount*int(w)+100
    return render_to_response('yang/yangad_js.html',locals())


def yangad_long(request):
    keywords = request.GET.get("keywords")
    adposition=request.GET.get("adposition")
    page = request.GET.get("page")
    if (page==None or page==""):
        page=1
    w=request.GET.get("w")
    num=request.GET.get("num")
    if (num==None or str(num)==""):
        num=1
    if (w==None):
        w=430
    if (int(w)<200):
        pw=170
    else:
        pw=(int(w)-5*int(num)-2*int(num))/int(num)
        
    
    adlistall=zzyang.yangprolist(limit=int(num),keywords=keywords,adposition=adposition,imgsize="100x100")
    listall=adlistall["listall"]
    
    adcount=adlistall['listcount']
    
    lastpage=1
    return render_to_response('yang/yangad_long.html',locals())

