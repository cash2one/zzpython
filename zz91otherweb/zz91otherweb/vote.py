#-*- coding:utf-8 -*-
from django.shortcuts import render_to_response
from django.http import HttpResponse,HttpResponseRedirect
from zz91page import *
from zz91db_ast import companydb
from zz91settings import SPHINXCONFIG,logpath
from zz91tools import formattime,getoptionlist,date_to_strall,date_to_str,filter_tags
import time,urllib,sys,os,datetime,simplejson
dbc=companydb()
reload(sys)
sys.setdefaultencoding('UTF-8')
nowpath=os.path.dirname(__file__)
execfile(nowpath+"/func/vote_function.py")
zzv=zvote()

def ybp_admin_userlist(request):
    page=request.GET.get('page')
    vote_cid=request.GET.get('vote_cid')
    if not page:
        page=1
    funpage=zz91page()
    limitNum=funpage.limitNum(10)
    nowpage=funpage.nowpage(int(page))
    frompageCount=funpage.frompageCount()
    after_range_num = funpage.after_range_num(3)
    before_range_num = funpage.before_range_num(6)
    ybpuserlist=zzv.ybp_vote_userlist(frompageCount,limitNum,vote_cid=vote_cid)
    listcount=0
    listall=ybpuserlist['list']
    listcount=ybpuserlist['count']
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
    return render_to_response('vote/ybp_admin_userlist.html',locals())
def ybp_vote_detail(request):
    openid=request.GET.get('openid')
    ybp_selectlist=zzv.ybp_vote_select(openid=openid)
    votelist=zzv.ybp_vote_detail(forno="yuanbaopu")
    
    return render_to_response('vote/ybp_vote_detail.html',locals())
def vote_list(request):
    page=request.GET.get('page')
    vtype=request.GET.get('vtype')
    company_name=request.GET.get('company_name')
    if not page:
        page=1
    searchlist={}
    if not vtype:
        vtype=request.session.get("vtype",None)
        if not vtype:
            vtype="1"
    if vtype:
        searchlist['vtype']=vtype
        request.session['vtype']=vtype
        
    if company_name:
        searchlist['company_name']=company_name
        
    searchurl=urllib.urlencode(searchlist)
    funpage=zz91page()
    limitNum=funpage.limitNum(10)
    nowpage=funpage.nowpage(int(page))
    frompageCount=funpage.frompageCount()
    after_range_num = funpage.after_range_num(3)
    before_range_num = funpage.before_range_num(6)
    qianbao_gglist=zzv.votelist(frompageCount,limitNum,searchlist=searchlist)
    listcount=0
    listall=qianbao_gglist['list']
    listcount=qianbao_gglist['count']
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
    return render_to_response('vote/vote_list.html',locals())

def vote_log(request):
    page=request.GET.get('page')
    if not page:
        page=1
    vtype=request.GET.get('vtype')
    searchlist={}
    if not vtype:
        vtype=request.session.get("vtype",None)
        if not vtype:
            vtype="1"
    if vtype:
        searchlist['vtype']=vtype
        
    searchurl=urllib.urlencode(searchlist)
    funpage=zz91page()
    limitNum=funpage.limitNum(10)
    nowpage=funpage.nowpage(int(page))
    frompageCount=funpage.frompageCount()
    after_range_num = funpage.after_range_num(3)
    before_range_num = funpage.before_range_num(6)
    qianbao_gglist=zzv.votelog(frompageCount,limitNum,searchlist=searchlist)
    listcount=0
    listall=qianbao_gglist['list']
    listcount=qianbao_gglist['count']
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
    return render_to_response('vote/vote_log.html',locals())

def vote_add(request):
    account=""
    request_url=request.META.get('HTTP_REFERER','/')
    return render_to_response('vote/vote_add.html',locals())
def vote_edit(request):
    id=request.GET.get("id")
    request_url=request.META.get('HTTP_REFERER','/')
    sql="select orderid,company_id,company_name,business,votecount,gmt_created,gmt_modified,checked,vtype from vote_list where id=%s"
    result=dbc.fetchonedb(sql,[id])
    if result:
        orderid=result[0]
        company_id=result[1]
        company_name=result[2]
        business=result[3]
        votecount=result[4]
        vtype=result[8]
    return render_to_response('vote/vote_edit.html',locals())
def vote_addnum(request):
    forcompany_id=request.GET.get("forcompany_id")
    clientid=request.GET.get("clientid")
    vtype=request.GET.get("vtype")
    votenum=request.GET.get("votenum")
    gmt_created=datetime.datetime.now()
    gmt_date=formattime(gmt_created,1)
    nlist=range(0,int(votenum))
    for n in nlist:
        sql="insert into vote_log (forcompany_id,clientid,vtype,gmt_created,gmt_date) values(%s,%s,%s,%s,%s)"
        dbc.updatetodb(sql,[forcompany_id,clientid,vtype,gmt_created,gmt_date])
    sql="select count(0) from vote_log where forcompany_id=%s and vtype=%s"
    result=dbc.fetchonedb(sql,[forcompany_id,vtype])
    if result:
        vcount=result[0]
        sql="update vote_list set votecount=%s where company_id=%s and vtype=%s"
        dbc.updatetodb(sql,[vcount,forcompany_id,vtype])
    list={'err':'false','votecount':vcount}
    return HttpResponse(simplejson.dumps(list, ensure_ascii=False))
    
def vote_save(request):
    #修改
    id=request.POST.get("id")
    if id:
        orderid=request.POST.get("orderid")
        vtype=request.POST.get("vtype")
        votecount=request.POST.get("votecount")
        company_name=request.POST.get("company_name")
        business=request.POST.get("business")
        sql="update vote_list set orderid=%s,votecount=%s,company_name=%s,business=%s,vtype=%s where id=%s"
        dbc.updatetodb(sql,[orderid,votecount,company_name,business,vtype,id])
        request_url=request.POST.get('request_url')
        return HttpResponseRedirect(request_url)
    #添加
    account=request.POST.get("account")
    orderid=request.POST.get("orderid")
    votecount=request.POST.get("votecount")
    vtype=request.POST.get("vtype")
    gmt_created=gmt_modified=datetime.datetime.now()
    sql="select company_id from company_account where account=%s"
    result=dbc.fetchonedb(sql,[account])
    if result:
        company_id=result[0]
        sql="select name,business from company where id=%s"
        result=dbc.fetchonedb(sql,[company_id])
        if result:
            company_name=result[0]
            business=result[1]
            checked=1
            sql="select id from vote_list where company_id=%s and vtype=%s"
            result=dbc.fetchonedb(sql,[company_id,vtype])
            if not result:
                sql="insert into vote_list(orderid,company_id,company_name,business,votecount,gmt_created,gmt_modified,checked,vtype) values(%s,%s,%s,%s,%s,%s,%s,%s,%s)"
                dbc.updatetodb(sql,[orderid,company_id,company_name,business,votecount,gmt_created,gmt_modified,checked,vtype])
    else:
        request_url=request.POST.get('request_url')
        error1="该账号不存在"
        return render_to_response('vote/vote_add.html',locals())
    request_url=request.POST.get('request_url')
    return HttpResponseRedirect(request_url)
            
def vote_del(request):
    id=request.GET.get("id")
    sql="delete from vote_list where id=%s"
    dbc.updatetodb(sql,[id])
    request_url=request.META.get('HTTP_REFERER','/')
    return HttpResponseRedirect(request_url)