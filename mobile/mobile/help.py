#-*- coding:utf-8 -*-
from django.shortcuts import render_to_response
from django.http import HttpResponse,HttpResponseRedirect
import urllib,sys,os
from zz91page import *
from zz91db_help import helpdb
from zz91db_ast import companydb
from django.core.cache import cache
dbh=helpdb()
reload(sys)
sys.setdefaultencoding('UTF-8')
nowpath=os.path.dirname(__file__)
execfile(nowpath+"/func/help_function.py")
execfile(nowpath+"/commfunction.py")
dbc=companydb()
zzhelp=zhelp()
#服务中心首页
def index(request):
    #未读工单信息
    company_id=request.session.get("company_id",None)
    if company_id:
        sql="select count(0) from gd_question as a left join gd_answer as b on a.id=b.question_id where b.isview=0 and a.company_id=%s"
        result=dbc.fetchonedb(sql,[company_id])
        noviewanwer=result[0]
        if noviewanwer>0:
            gdshow=1
    hlist=zzhelp.getarticallist(0,20,pid=63)
    kclist=zzhelp.getarticallist(0,20,typeid=72,company_id=company_id,ordasc=1)
    return render_to_response('aui/help/index.html',locals())
#-----帮助列表页
def list(request):
    page=request.GET.get('page')
    subject=request.GET.get('subject')
    typeid=request.GET.get('typeid')
    if typeid:
        typename=zzhelp.getcatname(typeid)
    searchlist={}
    if not page:
        page=1
    if typeid:
        searchlist['typeid']=typeid
    if subject:
        searchlist['subject']=subject
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
    return render_to_response('aui/help/help_list.html',locals())

#详细页
def detail(request):
    id=request.GET.get('id')
    company_id=request.session.get("company_id",None)
    if company_id:
        sql="replace into bz_kechengread(article_id,company_id) values(%s,%s)"
        dbh.updatetodb(sql,[id,company_id])
    if id:
        helpdetail=zzhelp.gethelpdetail(id)
        u_aid=helpdetail['aid']
        cat_id=helpdetail['cat_id']
        subject=helpdetail['subject']
        content=helpdetail['content']
        content=remove_script(content)
        content=remove_content_a(content)
        content=remove_content_value(content)
    return render_to_response('aui/help/help_detail.html',locals())




