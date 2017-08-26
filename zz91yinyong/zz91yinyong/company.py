#-*- coding:utf-8 -*-
from django.shortcuts import render_to_response
from django.http import HttpResponse,HttpResponseRedirect,HttpResponsePermanentRedirect
import MySQLdb,sys,os,memcache,settings,urllib,re,time,datetime,requests
from django.core.cache import cache
from sphinxapi import *
from zz91page import *

from settings import spconfig
#from commfunction import subString,filter_tags,replacepic,
#from commfunction import filter_tags,formattime,subString
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
execfile(nowpath+"/func/company_function.py")
execfile(nowpath+"/func/qianbao_function.py")
execfile(nowpath+"/func/trade_function.py")
execfile(nowpath+"/func/weixin_function.py")
execfile(nowpath+"/func/ldb_weixin_function.py")

zzcompany=zcompany()
zzqianbao=qianbao()
zztrade=ztrade()
ldb_weixin=ldbweixin()

def companyinfo(request):
    host=getnowurl(request)
    #alijsload="1"
    showpost=1
    nowlanmu="<a href='/company/'>公司列表</a>"
    forcompany_id=request.GET.get("company_id")
    company_id=request.session.get("company_id",None)
    username=request.session.get("username",None)
    if username and (company_id==None or str(company_id)=="0"):
        company_id=zztrade.getcompanyid(username)
        request.session['company_id']=company_id
    iszstflag=zztrade.getiszstcompany(forcompany_id)
    pdtid=request.GET.get("pdtid")
    list=zzcompany.getcompanydetail(forcompany_id)
    
    compzstflag=list['viptype']['vipcheck']
    weixinviewcontactflag=None
    if username:
        scoreopt=weixinscore()
        weixinviewflag=scoreopt.getviewcontact(username)
        if weixinviewflag and compzstflag==None:
            weixinviewcontactflag=1
            scoreopt.saveviewcontact(username,company_id=list['company_id'])
            
    if iszstflag==1 or compzstflag==1 or weixinviewcontactflag==1:
        viewflag=1
    else:
        viewflag=None
        
    webtitle=list['name']
    backurl=request.META.get('HTTP_REFERER','/')
    
    
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
    
    if viptype=='10051003':
        isldb=1
        ldbblance=ldb_weixin.getldblaveall(company_id)
        qianbaoblance=ldbblance
    else:
        qianbaoblance=zzqianbao.getqianbaoblance2(company_id)
    
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
                isseecompany=None
    isseecompany=zzqianbao.getisseecompany(company_id,forcompany_id)
    if list:
        compzstflag=list['viptype']['vipcheck']
        if iszstflag==1 or compzstflag==1:
            viewflag=1
        else:
            viewflag=None
    
    
    
    #钱包充值广告词
    ggc=dbc.fetchnumberdb('select txt from qianbao_gg where id=1')
    return render_to_response('company/companyinfo.html',locals())