#-*- coding:utf-8 -*-
from django.shortcuts import render_to_response
from django.http import HttpResponse,HttpResponseRedirect
from zz91page import *
from zz91db_mobile import payorder
from zz91db_ast import companydb
from zz91settings import SPHINXCONFIG,logpath
from zz91tools import formattime,getoptionlist,date_to_strall,date_to_str,filter_tags
import os,datetime,time,re,urllib,md5,json,sys,random,hashlib,simplejson
from zz91db_work import workdb
from conn import dictzz91astdb
from django.core.cache import cache
dict_dbc=dictzz91astdb()
reload(sys)
sys.setdefaultencoding('UTF-8')
nowpath=os.path.dirname(__file__)
execfile(nowpath+"/func/zsh_function.py")
zzh=zzsh()
def zshlist(request):
    username=request.session.get('username')
    if not username:
        return HttpResponseRedirect('/adminmobile/login.html')
    page=request.GET.get('page')
    searchlist={}
    mobile=request.GET.get('mobile')
    if mobile:
        searchlist['mobile']=mobile
    else:
        mobile=''
    contact=request.GET.get('contact')
    if contact:
        searchlist['contact']=contact
    else:
        contact=''
    companyname=request.GET.get('companyname')
    if companyname:
        searchlist['companyname']=companyname
    else:
        companyname=''
    zheng_no=request.GET.get('zheng_no')
    if zheng_no:
        searchlist['zheng_no']=zheng_no
    else:
        zheng_no=''
    ispay=request.GET.get('ispay')
    if ispay:
        searchlist['ispay']=ispay
    else:
        ispay=''
    getzheng=request.GET.get('getzheng')
    if getzheng:
        searchlist['getzheng']=getzheng
    else:
        getzheng=''
    isnowin=request.GET.get('isnowin')
    if isnowin:
        searchlist['isnowin']=isnowin
    searchurl=urllib.urlencode(searchlist)
    if not page:
        page=1
    funpage=zz91page()
    limitNum=funpage.limitNum(1000)
    nowpage=funpage.nowpage(int(page))
    frompageCount=funpage.frompageCount()
    after_range_num = funpage.after_range_num(3)
    before_range_num = funpage.before_range_num(6)
    messagelist=zzh.getzshlist(frompageCount,limitNum,searchlist=searchlist)
    listcount=0
    listall=messagelist['list']
    listcount=messagelist['count']
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
    
    sqlm="select max(id) as maxid from zsh_list"
    result=dict_dbc.fetchonedb(sqlm)
    maxid=result['maxid']
    if not maxid:
        maxid=0
    sqlm="select UNIX_TIMESTAMP(max(gmt_modified)) as maxmodtime from zsh_list"
    result=dict_dbc.fetchonedb(sqlm)
    maxmodtime=result['maxmodtime']
    if not maxmodtime:
        maxmodtime=1496266708
    sql="update update_log set maxid=%s where utype='621company'"
    #dict_dbc.updatetodb(sql,[maxmodtime])
    return render_to_response('zsh/index.html',locals())
#更新支付
def changepay(request):
    request_url=request.META.get('HTTP_REFERER','/')
    username=request.session.get('username')
    if not username:
        return HttpResponseRedirect('/adminmobile/login.html')
    id=request.GET.get("id")
    fee=request.GET.get("fee")
    paytime=datetime.datetime.now()
    sql="update zsh_list set ispay=%s,fee=%s,paytime=%s,gmt_modified=%s where id=%s"
    result=dict_dbc.updatetodb(sql,[1,fee,paytime,paytime,id])
    return HttpResponse("var _suggest_result_={'err':'false'}")
    #return HttpResponseRedirect(request_url)
#更新支付
def changezheng(request):
    request_url=request.META.get('HTTP_REFERER','/')
    username=request.session.get('username')
    if not username:
        return HttpResponseRedirect('/adminmobile/login.html')
    id=request.GET.get("id")
    paytime=datetime.datetime.now()
    sql="update zsh_list set getzheng=%s,getzheng_time=%s,gmt_modified=%s where id=%s"
    result=dict_dbc.updatetodb(sql,[1,paytime,paytime,id])
    return HttpResponse("var _suggest_result_={'err':'false'}")
    #return HttpResponseRedirect(request_url)
#新增数据
def addcompany(request):
    maxid=request.GET.get("maxid")
    sql="select id,zheng_no,companyname,area,contact,mobile,business,fee,personnum,paytype,paytime,salesperson,membertype,sales_bm,ispay,isqiandao,qiandaotime,company_id,getzheng from zsh_list where id>%s"
    result=dict_dbc.fetchalldb(sql,[maxid])
    for list in result:
        if not list['zheng_no']:
            list['zheng_no']=''
        list['qiandaotime']=formattime(list['qiandaotime'],0)
        list['paytime']=formattime(list['paytime'],0)
    return HttpResponse(simplejson.dumps(result, ensure_ascii=False))
#数据修改
def modify(request):
    maxmodtime=request.GET.get("maxmodtime")
    sql="select id,companyname,area,fee,paytime,ispay,isqiandao,qiandaotime,getzheng,UNIX_TIMESTAMP(gmt_modified) as maxmodtime from zsh_list where UNIX_TIMESTAMP(gmt_modified)>(SELECT maxid FROM update_log WHERE utype='621company') and UNIX_TIMESTAMP(gmt_modified)>%s order by gmt_modified asc"
    result=dict_dbc.fetchalldb(sql,[maxmodtime])
    for list in result:
        list['qiandaotime']=formattime(list['qiandaotime'],0)
        list['paytime']=formattime(list['paytime'],0)
    return HttpResponse(simplejson.dumps(result, ensure_ascii=False))
def zshadd(request):
    request_url=request.META.get('HTTP_REFERER','/')
    username=request.session.get('username')
    if not username:
        return HttpResponseRedirect('/adminmobile/login.html')
    return render_to_response('zsh/add.html',locals())
def zshdel(request):
    request_url=request.META.get('HTTP_REFERER','/')
    username=request.session.get('username')
    if not username:
        return HttpResponseRedirect('/adminmobile/login.html')
    id=request.GET.get("id")
    sql="delete from zsh_list where id=%s"
    dict_dbc.updatetodb(sql,[id])
    return HttpResponse("删除成功！")

def zshmod(request):
    request_url=request.META.get('HTTP_REFERER','/')
    username=request.session.get('username')
    if not username:
        return HttpResponseRedirect('/adminmobile/login.html')
    id=request.GET.get("id")
    sql="select * from zsh_list where id=%s"
    result=dict_dbc.fetchonedb(sql,[id])
    if result:
        result['qiandaotime']=formattime(result['qiandaotime'],0)
        result['paytime']=formattime(result['paytime'],0)
        if result['ispay']==0:
            result['fee']=0
        if result['ispay']==1 and result['fee']==0:
            result['fee']=1
        if not result['salesperson']:
            result['salesperson']=''
        if not result['paytype']:
            result['paytype']=''
        if not result['business']:
            result['business']=''
        if not result['area']:
            result['area']=''
        return render_to_response('zsh/mod.html',locals())
    else:
        return HttpResponse("该客户已经删除！")
    
#再生会修改
def zshsave(request):
    request_url=request.META.get('HTTP_REFERER','/')
    username=request.session.get('username')
    if not username:
        return HttpResponseRedirect('/adminmobile/login.html')
    ztype="20170621"
    companyname=request.GET.get("companyname")
    contact=request.GET.get("contact")
    mobile=request.GET.get("mobile")
    business=request.GET.get("business")
    area=request.GET.get("area")
    company_id=request.GET.get("company_id")
    fee=request.GET.get("fee")
    if fee:
        fee=int(fee)
    ispay=0
    if fee==1:
        ispay=1
    if fee in [300,500]:
        ispay=1
    if fee==300:
        membertype='高会'
    else:
        membertype='普会'
    personnum=1
    paytype=request.GET.get("paytype")
    isqiandao=0
    isnowin=0
    paytime=request.GET.get("paytime")
    salesperson=request.GET.get("salesperson")
    sales_bm=request.GET.get("sales_bm")
    gmt_modified=datetime.datetime.now()
    mod=request.GET.get("mod")
    isqiandao=request.GET.get("isqiandao")
    if not mod:
        zheng_no=1000
        sql="select max(zheng_no)+1 as zheng_no from zsh_list"
        result=dict_dbc.fetchonedb(sql)
        if result:
            zheng_no=result['zheng_no']
        sql="insert into zsh_list(zheng_no,ztype,companyname,area,contact,mobile,business,fee,personnum,paytype,paytime,isqiandao,isnowin,company_id,gmt_modified,salesperson,sales_bm,ispay) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        result=dict_dbc.updatetodb(sql,[zheng_no,ztype,companyname,area,contact,mobile,business,fee,personnum,paytype,paytime,isqiandao,isnowin,company_id,gmt_modified,salesperson,sales_bm,ispay])
    else:
        id=request.GET.get("id")
        sql="update zsh_list set companyname=%s,area=%s,contact=%s,mobile=%s,business=%s,fee=%s,paytype=%s,paytime=%s,gmt_modified=%s,salesperson=%s,sales_bm=%s,isqiandao=%s where id=%s"
        dict_dbc.updatetodb(sql,[companyname,area,contact,mobile,business,fee,paytype,paytime,gmt_modified,salesperson,sales_bm,isqiandao,id])
    res={'err':'false','errkey':''}
    res=simplejson.dumps(res,ensure_ascii=False)
    return HttpResponse(res)
    
#签到电视机
def qiandaotv(request):
    sql="select UNIX_TIMESTAMP(max(qiandaotime)) as qiandaotime from zsh_list where isqiandao=1"
    result=dict_dbc.fetchonedb(sql)
    qiandaotime=result['qiandaotime']
    if not qiandaotime:
        qiandaotime=0
    return render_to_response('zsh/tv.html',locals())

#签到列表
def qiandaolist(request):
    l=request.GET.get("l")
    sql="select id,zheng_no,contact,companyname,business from zsh_list where isqiandao=1 order by qiandaotime desc"
    if l:
        sql+=" limit 0,15"
    resultall=dict_dbc.fetchalldb(sql)
    for list in resultall:
        if not list['zheng_no']:
            list['zheng_no']=''
    sql="select UNIX_TIMESTAMP(max(qiandaotime)) as qiandaotime from zsh_list where isqiandao=1"
    result=dict_dbc.fetchonedb(sql)
    qiandaotime=result['qiandaotime']
    return HttpResponse(simplejson.dumps({'list':resultall,'qiandaotime':qiandaotime}, ensure_ascii=False))
#最新签到数据
def newqiandao(request):
    qiandaotime=request.GET.get("qiandaotime")
    sql="select id,zheng_no,contact,companyname,business,UNIX_TIMESTAMP(qiandaotime) as qiandaotime from zsh_list where UNIX_TIMESTAMP(qiandaotime)>(SELECT maxid FROM update_log WHERE utype='621qiandao') and UNIX_TIMESTAMP(qiandaotime)>%s and isqiandao=1 order by gmt_modified asc"
    resultall=dict_dbc.fetchalldb(sql,[qiandaotime])
    for list in resultall:
        if not list['zheng_no']:
            list['zheng_no']=''
    sql="select UNIX_TIMESTAMP(max(qiandaotime)) as qiandaotime from zsh_list where isqiandao=1"
    result=dict_dbc.fetchonedb(sql)
    qiandaotime=result['qiandaotime']
    return HttpResponse(simplejson.dumps({'list':resultall,'qiandaotime':qiandaotime}, ensure_ascii=False))
    