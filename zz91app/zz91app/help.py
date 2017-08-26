#-*- coding:utf-8 -*-
from django.shortcuts import render_to_response
from django.http import HttpResponse,HttpResponseRedirect,HttpResponsePermanentRedirect
import sys,os,memcache,settings,urllib,re,datetime,time,random,hashlib,simplejson
from django.core.cache import cache
from zz91page import *
from zz91db_help import helpdb
from zz91db_ast import companydb
dbh=helpdb()
dbc=companydb()
reload(sys)
sys.setdefaultencoding('UTF-8')
nowpath=os.path.dirname(__file__)
execfile(nowpath+"/func/help_function.py")
execfile(nowpath+"/func/public_function.py")
zzhelp=zhelp()
#服务中心首页
def index(request):
    company_id = request.GET.get('company_id')
    hlist=zzhelp.getarticallist(0,20,pid=63)
    kclist=zzhelp.getarticallist(0,20,typeid=72,company_id=company_id,ordasc=1)
    hlist['noviewanwer']=0
    hlist['kclist']=kclist
    #未读工单
    if company_id:
        sql="select count(0) from gd_question as a left join gd_answer as b on a.id=b.question_id where b.isview=0 and a.company_id=%s"
        result=dbc.fetchonedb(sql,[company_id])
        noviewanwer=result[0]
        hlist['noviewanwer']=noviewanwer
    return HttpResponse(simplejson.dumps(hlist, ensure_ascii=False))
#-----帮助列表页
def list(request):
    page=request.GET.get('page')
    subject=request.GET.get('subject')
    typeid=request.GET.get('typeid')
    searchlist={}
    if not page:
        page=1
    searchurl=urllib.urlencode(searchlist)
    funpage=zz91page()
    limitNum=funpage.limitNum(20)
    nowpage=funpage.nowpage(int(page))
    frompageCount=funpage.frompageCount()
    after_range_num = funpage.after_range_num(3)
    before_range_num = funpage.before_range_num(6)
    articallist=zzhelp.getarticallist(frompageCount,limitNum,subject=subject,typeid=typeid)
    listcount=0
    listall=articallist['list']
    listcount=articallist['count']
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
    
    return HttpResponse(simplejson.dumps(listall, ensure_ascii=False))

#详细页
def detail(request):
    company_id = request.GET.get('company_id')
    id=request.GET.get('id')
    if company_id and company_id!='0':
        sql="replace into bz_kechengread(article_id,company_id) values(%s,%s)"
        dbh.updatetodb(sql,[id,company_id])
    if id:
        helpdetail=zzhelp.gethelpdetail(id)
        content=helpdetail['content']
        content=remove_script(content)
        content=remove_content_a(content)
        content=remove_content_value(content)
        helpdetail['content']=content
    return HttpResponse(simplejson.dumps(helpdetail, ensure_ascii=False))




