#-*- coding:utf-8 -*-
from django.shortcuts import render_to_response
from django.http import HttpResponse,HttpResponseRedirect,HttpResponsePermanentRedirect
import MySQLdb,sys,os,memcache,settings,urllib,re,time,datetime
from django.core.cache import cache
from sphinxapi import *
from zz91page import *

from settings import spconfig,appurl
#from commfunction import subString,filter_tags,replacepic,
#from commfunction import filter_tags,formattime,subString
from zz91tools import subString,filter_tags
from zz91db_ast import companydb
dbc=companydb()

reload(sys)
sys.setdefaultencoding('UTF-8')
nowpath=os.path.dirname(__file__)
execfile(nowpath+"/func/public_function.py")
execfile(nowpath+"/func/ldb_function.py")

zzl=zzldb()

#----来电宝列表
def laidianbao(request,page=''):
    webtitle="来电宝"
    nowlanmu="<a href='/laidianbao/'>来电宝客户</a>"
    host=getnowurl(request)
    username=request.session.get("username",None)
    if (page=='' or page==0):
        page=1
    funpage=zz91page()
    limitNum=funpage.limitNum(8)
    nowpage=funpage.nowpage(int(page))
    frompageCount=funpage.frompageCount()
    after_range_num = funpage.after_range_num(5)
    before_range_num = funpage.before_range_num(4)
    newslist=zzl.getlaidianbao(frompageCount,limitNum)
    listcount=0
    if (newslist):
        listall=newslist['list']
        listcount=newslist['count']
        if (int(listcount)>1000000):
            listcount=1000000-1
    listcount = funpage.listcount(listcount)
    page_listcount=funpage.page_listcount()
    firstpage = funpage.firstpage()
    lastpage = funpage.lastpage()
    page_range  = funpage.page_range()
    nextpage = funpage.nextpage()
    prvpage = funpage.prvpage()
    return render_to_response('new/laidianbao.html',locals())