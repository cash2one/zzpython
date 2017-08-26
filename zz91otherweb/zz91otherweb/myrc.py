#-*- coding:utf-8 -*-
from django.shortcuts import render_to_response
from django.http import HttpResponse,HttpResponseRedirect
from zz91page import *
from zz91tools import getToday,getYesterday,date_to_str
from zz91db_data import myrc
import datetime,time,urllib
zzmyrc=myrc()

def operatype(request):
    operatypelist=zzmyrc.getmyrc_operatypelist()
    return render_to_response('myrc/operatype.html',locals())

def delopera(request):
    request_url=request.META.get('HTTP_REFERER','/')
    gmt_begin=request.GET.get('gmt_begin')
    zzmyrc.delopera(gmt_begin)
    return HttpResponseRedirect(request_url)
#----生意管家行为统计
def operadata(request):
    page=request.GET.get('page')
    operatype_id=request.GET.get('operatype_id')
    gmt_begin=request.GET.get('gmt_begin')
    if operatype_id:
        operatype=zzmyrc.getoperatype(operatype_id)
    account=request.GET.get('account')
    operatypelist=zzmyrc.getmyrc_operatypelist()
    searchlist={}
    if operatype_id:
        searchlist['operatype_id']=operatype_id
    if account:
        searchlist['account']=account
    searchurl=urllib.urlencode(searchlist)
    if not page:
        page=1
    funpage=zz91page()
    limitNum=funpage.limitNum(30)
    nowpage=funpage.nowpage(int(page))
    frompageCount=funpage.frompageCount()
    after_range_num = funpage.after_range_num(3)
    before_range_num = funpage.before_range_num(6)
    operalist=zzmyrc.getmyrc_operalist(frompageCount,limitNum,operatype_id,account,gmt_begin)
    listcount=0
    listall=operalist['list']
    listcount=operalist['count']
    if (int(listcount)>1000000):
        listcount=1000000-1
    listcount = funpage.listcount(listcount)
    page_listcount=funpage.page_listcount()
    firstpage = funpage.firstpage()
    lastpage = funpage.lastpage()
    page_range  = funpage.page_range()
    if len(page_range)>7:
        page_range=page_range[:7]
    nextpage = funpage.nextpage()
    prvpage = funpage.prvpage()
    return render_to_response('myrc/operadata.html',locals())
