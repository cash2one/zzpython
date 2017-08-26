#-*- coding:utf-8 -*-

from django.shortcuts import render_to_response
from django.http import HttpResponse,HttpResponseRedirect,HttpResponsePermanentRedirect
import MySQLdb,sys,os,memcache,settings,urllib,re,time,datetime,requests,random,string,md5,hashlib
from django.core.cache import cache
from sphinxapi import *
from zz91page import *
from settings import spconfig
from zz91settings import SPHINXCONFIG
from zz91tools import int_to_str
from datetime import timedelta, date 
from zz91db_ast import companydb
from zz91db_2_news import newsdb
from zz91db_ads import adsdb
from zz91db_sms import smsdb
from zz91conn import database_mongodb

dbc=companydb()
dbn=newsdb()
dbads=adsdb()
dbsms=smsdb()
#连接loginfo集合（表）
dbmongo=database_mongodb()

reload(sys)
sys.setdefaultencoding('UTF-8')
nowpath=os.path.dirname(__file__)
execfile(nowpath+"/conn.py")
execfile(nowpath+"/commfunction.py")
execfile(nowpath+"/function.py")


execfile(nowpath+"/func/weixin_function.py")
execfile(nowpath+"/func/qianbao_function.py")
execfile(nowpath+"/func/main_function.py")
execfile(nowpath+"/func/company_function.py")
execfile(nowpath+"/func/apps_function.py")
#from SmsWap.SmsWap import MerchantAPI
#import SmsWap.Gl as Gl

from zzwx.client import Client
zzmain=zmain()
zzcompany=zcompany()
zzapps=zapps()
def showadscript(request):
    code = request.GET.get("code")
    type = request.GET.get("type")
    position=[1]
    if (type=="index1"):
        position=[1,2,3,4,5,6,7]
        picaddress="http://pyapp.zz91.com/images/noad1.jpg"
    if (type=="index2"):
        position=[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21]
        picaddress="http://pyapp.zz91.com/images/noad.jpg"

        
    adlist=[]
    for a in position:
        list=zzapps.getadlist(code,str(a))
        if (list==None):
            list={'url':'http://www.zz91.com/zst/','picaddress':'http://pyapp.zz91.com/images/noad.jpg'}
        adlist.append(list)
    return render_to_response('script.html',locals())
def showcommadscript(request):
    code = request.GET.get("code")
    adnum=zzapps.getadnum(code)
    adlist=zzapps.getadlistnew(code)
    return render_to_response('scripth.html',locals())
def showcompanyadscript(request):
    code = request.GET.get("code")
    position="1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20"
    adlist=[]
    for a in position.split(","):
        list=zzapps.getadlist(code,a)
        if (list==None):
            list={'url':'http://www.zz91.com/zst/','picaddress':'http://pyapp.zz91.com/images/noadc.jpg'}
        adlist.append(list)
    return render_to_response('scriptc.html',locals())
def showppctxtadscript(request):
    num=request.GET.get("num")
    if (num==None or str(num)==""):
        num=1
    adtype=request.GET.get("adtype")
    if adtype==None:
        adtype="3"
    if num==1:
        adtype="2"
        
    if adtype=="2":
        return showppcscript(request)
    if adtype=="3":
        return showppcscript_pic(request)
#----来电宝全网广告
def showppcscript_pic(request):
    adposition=request.GET.get("adposition")
    keywords = request.GET.get("keywords")
    page = request.GET.get("page")
    lastpage=0
    if (page==None or page==""):
        page=1
    showposition = request.GET.get("showposition")
    w=request.GET.get("w")
    num=request.GET.get("num")
    if (num==None or str(num)==""):
        num=1
    if int(num)>1:
        boxright=1
    padding=request.GET.get("padding")
    if (padding==None or str(padding)==""):
        padding=0
    showborder=request.GET.get("showborder")
    if (w==None):
        w=430
    h=request.GET.get("h")
    if (h==None):
        h=100
    m=request.GET.get("m")
    if (m==None):
        m=20
    if (int(w)<200):
        pw=170
    else:
        pw=(int(w)-5*int(num)-2*int(num))/int(num)
        
    
    ppclist=zzapps.getppccomplist(int(m),keywords,int(page),adposition=adposition)
    listall=ppclist['listall']
    lastpage=ppclist['lastpage']
    return render_to_response('app/ppc_ad_pic.html',locals())
def showppcscript(request):
    adposition=request.GET.get("adposition")
    keywords = request.GET.get("keywords")
    page = request.GET.get("page")
    lastpage=0
    if (page==None or page==""):
        page=1
    showposition = request.GET.get("showposition")
    w=request.GET.get("w")
    num=request.GET.get("num")
    if (num==None or str(num)==""):
        num=1
    if int(num)>1:
        boxright=1
    padding=request.GET.get("padding")
    if (padding==None or str(padding)==""):
        padding=0
    showborder=request.GET.get("showborder")
    if (w==None):
        w=430
    h=request.GET.get("h")
    if (h==None):
        h=100
    m=request.GET.get("m")
    if (m==None):
        m=20
    if (int(w)<200):
        pw=170
    else:
        pw=(int(w)-5*int(num))/int(num)
    
    ppclist=zzapps.getppccomplist(int(m),keywords,int(page),adposition=adposition)
    listall=ppclist['listall']
    lastpage=ppclist['lastpage']
    return render_to_response('app/ppc_ad.html',locals())
#----翻页
def showppccomplist(request):
    adposition=request.GET.get("adposition")
    page = request.GET.get("page")
    if (page=="" or page==None):
        page=1
    mm=request.GET.get("mm")
    keywords = request.GET.get("keywords")
    listall=zzapps.getppccomplist(int(mm),keywords,int(page),adposition=adposition)['listall']
    return render_to_response('script_showppccomplist.html',locals())
def showppccomplist_pic(request):
    adposition=request.GET.get("adposition")
    page = request.GET.get("page")
    if (page=="" or page==None or page=="0"):
        page=1
    mm=request.GET.get("mm")
    keywords = request.GET.get("keywords")
    listall=zzapps.getppccomplist(int(mm),keywords,int(page),adposition=adposition)['listall']
    return render_to_response('script_showppccomplist_pic.html',locals())
#来电宝广告点击跳转
def ppchit(request):
    company_id=request.GET.get("company_id")
    adposition=request.GET.get("adposition")
    adtype="2"
    rd=request.GET.get("rd")
    url=getjiemi(rd)
    saveshowppc(company_id,adposition,adtype="2")
    return HttpResponseRedirect(url)


