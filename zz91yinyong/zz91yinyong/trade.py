#-*- coding:utf-8 -*-
from django.shortcuts import render_to_response
from django.http import HttpResponse,HttpResponseRedirect,HttpResponsePermanentRedirect
import MySQLdb,sys,os,memcache,settings,urllib,re,time,datetime,requests
from django.core.cache import cache
from datetime import timedelta,date
from sphinxapi import *
from zz91page import *

from settings import spconfig
#from commfunction import subString,filter_tags,replacepic,
from commfunction import filter_tags,formattime,subString
from function import getnowurl
from zz91db_ast import companydb
from zz91db_sms import smsdb
from zz91db_2_news import newsdb
dbc=companydb()
dbsms=smsdb()
dbn=newsdb()

reload(sys)
sys.setdefaultencoding('UTF-8')
nowpath=os.path.dirname(__file__)
execfile(nowpath+"/func/trade_function.py")
execfile(nowpath+"/func/qianbao_function.py")
execfile(nowpath+"/func/ldb_weixin_function.py")

zzqianbao=qianbao()
zztrade=ztrade()
ldb_weixin=ldbweixin()

#----供求最终页
def detail(request):
    host=getnowurl(request)
    showpost=1
    backurl=request.META.get('HTTP_REFERER','/')
    username=request.session.get("username",None)
    company_id=request.session.get("company_id",None)
    if username and (company_id==None or str(company_id)=="0"):
        company_id=zztrade.getcompanyid(username)
        request.session['company_id']=company_id
    alijsload="1"
    nowlanmu='<a href="/category/">交易中心 </a>'
    nowlanmu2='<a href="/category/">交易中心 </a> > '
    keywords1=''
    keywords=request.GET.get("keywords")
    if not keywords:
        if '&' in backurl:
            keywords1=re.findall('keywords=(.*?)&',backurl)
        else:
            keywords1=re.findall('keywords=(.*)',backurl)
        #if keywords1:
          # keywords=urllib.unquote(keywords1[0])
    if keywords:
        nowlanmu2+='<a href="/offerlist/?keywords='+str(keywords)+'">'+str(keywords)+'</a>&nbsp;>'
    id=request.GET.get("id")
    done = request.path
    iszstflag=zztrade.getiszstcompany(company_id)
    list=zztrade.getproductdetail(id)
    forcompany_id=0
    if list:
        forcompany_id=list['company_id']
    if forcompany_id==0:
        return render_to_response('404.html',locals())
    
    foriszstflag=zztrade.getiszstcompany(forcompany_id)
    #----判断举报状态
    reportcheck=zztrade.getreportcheck(company_id,forcompany_id)
    if reportcheck==0:
        idcheck=1
        idchecktxt='举报处理中'
    if reportcheck==1:
        idcheck=1
        idchecktxt='举报已处理'
    if reportcheck==2:
        idcheck=1
        idchecktxt='举报退回'
    #该公司是否被举报成功过
    isjubao=zztrade.getreportischeck(forcompany_id)
    #----判断是否为来电宝用户,获取来电宝余额
    isldb=None
    viptype=zzqianbao.getviptype(company_id)
#    if company_id==969597:#----测试信息
#        viptype='10051003'#----测试信息
    if viptype=='10051003':
        isldb=1
        ldbblance=ldb_weixin.getldblaveall(company_id)
        qianbaoblance=ldbblance
    else:
        qianbaoblance=zzqianbao.getqianbaoblance2(company_id)
    
#    if company_id==969597:#----测试信息
#        qianbaoblance=999999#----测试信息
    isseecompany=zzqianbao.getisseecompany(company_id,forcompany_id)
    if not isseecompany:
        paytype=request.GET.get("paytype")
        if paytype:
            if qianbaoblance>=5:
                if isldb:
                    ldb_weixin.getpayfee(company_id,forcompany_id,5)
                else:
                    zzqianbao.getpayfee(company_id,forcompany_id,id,paytype)
            else:
                isseecompany==None
    #isseecompany=zzqianbao.getisseecompany(company_id,forcompany_id)
    forviptype=zzqianbao.getviptype(forcompany_id)
    forvipflag=1
    if forviptype:
        if forviptype=="100510021001" or forviptype=="100510021002":
            isseecompany=1
            forvipflag=None
    #z置顶客户显示联系方式
    keywordstopcompanyflag=zztrade.keywordstopcompany(id)
    if keywordstopcompanyflag:
        isseecompany=1
        forvipflag=None
    if list:
        compzstflag=list['viptype']['vipcheck']
        if iszstflag==1 or compzstflag==1:
            viewflag=1
        else:
            viewflag=None
        webtitle=list['title']
        nowlanmu2+='&nbsp;'+str(webtitle)
        products_type_code=list['products_type_code']
    #钱包充值广告词
    ggc=dbc.fetchnumberdb('select txt from qianbao_gg where id=1')
    return render_to_response('trade/detail.html',locals())

def pro_report(request):
    company_id=request.GET.get("company_id")
    forcompany_id=request.GET.get("forcompany_id")
    product_id=request.GET.get("product_id")
    content=request.GET.get("chk_value")
    if content:
        #----一家公司只能被一个客户投诉一次
        sql='select id from pay_report where company_id=%s and forcompany_id=%s'
        result=dbc.fetchonedb(sql,[company_id,forcompany_id])
        if not result:
            zztrade.getpro_report(company_id,forcompany_id,product_id,content)
    return HttpResponse('1')

#拨打电话记录
def telclicklog(request):
    username=request.session.get("username",None)
    company_id=request.session.get("company_id",None)
    backurl = request.META.get('HTTP_REFERER','/')
    if not company_id:
        company_id=request.GET.get("company_id",None)
    gmt_created=datetime.datetime.now()
    tel=request.GET.get("tel")
    pagefrom=request.GET.get("pagefrom")
    if username and (company_id==None or str(company_id)=="0"):
        company_id=zztrade.getcompanyid(username)
        request.session['company_id']=company_id
    if (company_id==None or str(company_id)=="0"):
        company_id=0
    sql="select id from phone_telclick_log where tel=%s and company_id=%s"
    result=dbc.fetchonedb(sql,[tel,company_id])
    if not result:
        sqlp="insert into phone_telclick_log(company_id,tel,pagefrom,gmt_created,url) values(%s,%s,%s,%s,%s)"
        dbc.updatetodb(sqlp,[company_id,tel,pagefrom,gmt_created,backurl])
    else:
        sqlp="update phone_telclick_log set num=num+1 where id=%s"
        dbc.updatetodb(sqlp,[result[0]])
    return HttpResponse('1')

def pricelist(request):
    keywords=request.GET.get("keywords")
    type=request.GET.get("type")
    page=request.GET.get("page")
    nowlanmu='<a href="/category/">交易中心 </a>'
    if keywords:
        if type=="0":
            webtitle=keywords+"行情报价"
        else:
            webtitle=keywords+"商家报价"
    else:
        webtitle="行情报价"
    if not page:
        page=1
    funpage=zz91page()
    limitNum=funpage.limitNum(20)
    nowpage=funpage.nowpage(int(page))
    frompageCount=funpage.frompageCount()
    after_range_num = funpage.after_range_num(8)
    before_range_num = funpage.before_range_num(9)
    if type=='0':
        pricelist=zztrade.getprlist(frompageCount=frompageCount,limitNum=limitNum,kname=keywords)
    else:
        pricelist=zztrade.getpricelist_company(kname=keywords,frompageCount=frompageCount,limitNum=limitNum)
    listall=pricelist['list']
    listcount=pricelist['count']
    if (int(listcount)>1000000):
        listcount=1000000-1
    listcount = funpage.listcount(listcount)
    page_listcount=funpage.page_listcount()
    firstpage = funpage.firstpage()
    lastpage = funpage.lastpage()
    page_range  = funpage.page_range()
    nextpage = funpage.nextpage()
    prvpage = funpage.prvpage()
    return render_to_response('trade/pricelist.html',locals())