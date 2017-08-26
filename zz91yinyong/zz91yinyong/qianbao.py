#-*- coding:utf-8 -*-
from django.shortcuts import render_to_response
from django.http import HttpResponse,HttpResponseRedirect,HttpResponsePermanentRedirect
import MySQLdb,sys,os,memcache,settings,urllib,re,time,datetime,requests
from django.core.cache import cache

from commfunction import subString,filter_tags,replacepic
from function import getnowurl
from zz91page import *
from zz91db_ast import companydb
from zz91db_130 import otherdb
from zz91db_sms import smsdb
from zz91db_2_news import newsdb
from sphinxapi import *
from settings import spconfig
from zz91tools import getYesterday,getpastoneday,int_to_str,formattime,int_to_datetime
dbc=companydb()
dbn=newsdb()
reload(sys)
sys.setdefaultencoding('UTF-8')
nowpath=os.path.dirname(__file__)
execfile(nowpath+"/func/qianbao_function.py")
execfile(nowpath+"/func/trade_function.py")
execfile(nowpath+"/func/ldb_weixin_function.py")

ldb_weixin=ldbweixin()
zzq=qianbao()
zzms=mshop()
zzt=ztrade()
dbsms=smsdb()

#----首页
def index(request):
    host=getnowurl(request)
    username=request.session.get("username",None)
    company_id=request.session.get("company_id",None)
    if username and (company_id==None or str(company_id)=="0"):
        company_id=getcompanyid(username)
        request.session['company_id']=company_id
    if (username==None or (company_id==None or str(company_id)=="0")):
        return HttpResponseRedirect("/login/?done="+host)
    
    #----判断是否为来电宝,跳转到来电宝钱包
#    viptype=zzq.getviptype(company_id)
#    if viptype=='10051003':
#        isldb=1
#        return HttpResponseRedirect('/ldb_weixin/index.html')

    #----第一次登录钱包送20
#    getfee20=zzq.getsendfee(company_id,20,6)
    
    outfeeall2=zzq.getoutfeeall(company_id)
    #----余额
    blance=zzq.getqianbaoblance(company_id)
    #----昨日进账
    infeeyd=zzq.getinfeeyd(company_id)
    #----总进账
    infeeall=zzq.getinfeeall(company_id)
    #----昨日消费
    outfeeyd=zzq.getoutfeeyd(company_id)
    #----总消费
    outfeeall=zzq.getoutfeeall(company_id)
    return render_to_response('qianbao/index.html',locals())

def zhangdannore(request):
    timarg=request.GET.get('timarg')
    page=request.GET.get('page')
    if page:
        page=int(page)
    else:
        page=1
    company_id=request.session.get("company_id",None)
    payfeelist=zzq.getpayfeelist(company_id,(page-1)*20,20,timarg)
    listall=payfeelist['list']
    return render_to_response('qianbao/zhangdannore.html',locals())

#----账单
def zhangdan(request):
    host=getnowurl(request)
    backurl=request.META.get('HTTP_REFERER','/')
    username=request.session.get("username",None)
    company_id=request.session.get("company_id",None)
    if username and (company_id==None or str(company_id)=="0"):
        company_id=getcompanyid(username)
        request.session['company_id']=company_id
    if (username==None or (company_id==None or str(company_id)=="0")):
        return HttpResponseRedirect("/login/?done="+host)
    
    timarg=request.GET.get('timarg')
    payfeelist=zzq.getpayfeelist(company_id,0,20,timarg)
    listall=payfeelist['list']
    count=payfeelist['count']
    gmtdate=time.strftime('%Y-%m-01 00:00:',time.localtime(time.time()))
    #----本月进账
    infeegmtnowmonth=zzq.getinfeegmt(company_id,gmtdate)
    #----本月消费
    outfeegmtnowmonth=zzq.getoutfeegmt(company_id,gmtdate)
    #----本月充值
    outfee5gmtnowmonth=zzq.getinfeegmt(company_id,gmtdate,'','(5,6)')
    
    return render_to_response('qianbao/zhangdan.html',locals())
#----充值
def chongzhi(request,id=''):
    backurl=request.META.get('HTTP_REFERER','/')
    host=getnowurl(request)
    username=request.session.get("username",None)
    company_id=request.session.get("company_id",None)
    if username and (company_id==None or str(company_id)=="0"):
        company_id=getcompanyid(username)
        request.session['company_id']=company_id
    if (username==None or (company_id==None or str(company_id)=="0")):
        return HttpResponseRedirect("/login/?done="+host)
    
    companycontact=zzq.getcompanycontact(company_id)
    mobile=companycontact['mobile']
    contact=companycontact['contact']
    #钱包充值广告词
    #ggc=dbc.fetchnumberdb('select txt from qianbao_gg where id=1')
    return render_to_response('qianbao/chongzhi.html',locals())
#----进账说明
def intxt(request):
    backurl=request.META.get('HTTP_REFERER','/')
    return render_to_response('qianbao/intxt.html',locals())
#----消费说明
def outtxt(request):
    backurl=request.META.get('HTTP_REFERER','/')
    return render_to_response('qianbao/outtxt.html',locals())
#----商城
def shop(request):
    backurl=request.META.get('HTTP_REFERER','/')
    host=getnowurl(request)
    username=request.session.get("username",None)
    company_id=request.session.get("company_id",None)
    if username and (company_id==None or str(company_id)=="0"):
        company_id=getcompanyid(username)
        request.session['company_id']=company_id
    if (username==None or (company_id==None or str(company_id)=="0")):
        return HttpResponseRedirect("/login/?done="+host)
    listall=zzt.getmyproductslist(frompageCount=0,limitNum=1,company_id=company_id)
    offerlist=listall['list']
    if offerlist:
        offid1=offerlist[0]['proid']
    #----获取用户余额
    qianbaoblance=zzq.getqianbaoblance2(company_id)
    #----判断是否在微信推广中
    gmt_created=datetime.datetime.now()
#    is_wxtg=zzms.getis_wxtg(company_id,gmt_created,paytype=10)
    is_wxtg=''
    return render_to_response('qianbao/shop.html',locals())
def qianbaopay(request):
    company_id=request.session.get("company_id",None)
    if company_id:
        paytype=request.GET.get('paytype')
        money=request.GET.get('money')
        proid=request.GET.get('proid')
        mobile=request.GET.get('mobile')
        if money:
            money=int('-'+money)
        #----手机钱包付费
        gmt_end=''
        gmt_created=datetime.datetime.now()
        gmt_date=datetime.date.today()
        if paytype=='9':
#            result=1
            type='10431004'
            sql2='select id from products_keywords_rank where product_id=%s and type=%s and is_checked=0'
            result2=dbc.fetchonedb(sql2,[proid,type])
            if result2:
                return HttpResponse('2')
            else:
                result=zzq.getpayfee(company_id=company_id,product_id=proid,ftype=paytype,fee=-15)
                if result==1:
                    company_account=zzq.getcompany_account(company_id)
                    sql='insert into products_keywords_rank(product_id,is_checked,gmt_created,gmt_modified,company_id,apply_account,type,bz) values(%s,%s,%s,%s,%s,%s,%s,%s)'
                    dbc.updatetodb(sql,[proid,0,gmt_created,gmt_created,company_id,company_account,type,mobile])
                return HttpResponse('1')
        elif paytype=='10' and money==-300:
#            result=1
            sql2='select id from shop_product_wxtg where company_id=%s and is_check=0'
            result2=dbc.fetchonedb(sql2,[company_id])
            if result2:
                return HttpResponse('2')
            else:
                result=zzq.getpayfee(company_id=company_id,product_id=proid,ftype=paytype,fee=-300)
                if result==1:
                    sql='insert into shop_product_wxtg(company_id,mobile,is_check,gmt_date,gmt_created,gmt_modified) values(%s,%s,%s,%s,%s,%s)'
                    dbc.updatetodb(sql,[company_id,mobile,'0',gmt_date,gmt_created,gmt_created])
                    return HttpResponse('1')
        elif paytype=='11':
            sql2='select id from shop_showphone where company_id=%s and gmt_end>=%s order by id desc'
            result=dbc.fetchonedb(sql2,[company_id,gmt_created])
            if result:
                return HttpResponse('2')
            result=zzq.getpayfee(company_id=company_id,ftype=paytype,fee=money)
            if result==1:
                gmt_begin=int(time.time())
                if money==-5:
                    gmt_end=gmt_begin+(3600*24)
                if money==-120:
                    gmt_end=gmt_begin+(3600*24*30)
                if money==-1200:
                    gmt_end=gmt_begin+(3600*24*365)
                gmt_begin=int_to_datetime(gmt_begin)
                gmt_end=int_to_datetime(gmt_end)
                sql='insert into shop_showphone(company_id,gmt_begin,gmt_end,gmt_created,gmt_date) values(%s,%s,%s,%s,%s)'
                dbc.updatetodb(sql,[company_id,gmt_begin,gmt_end,gmt_created,gmt_date])
                return HttpResponse('1')
        elif paytype=='16':
            baoming=request.GET.get('baoming')
            result=zzq.getpayfee(company_id=company_id,ftype=paytype,fee=-300)
            if str(result)=="1":
                sql='insert into shop_baoming(company_id,content,gmt_created,paytype) values(%s,%s,%s,%s)'
                dbc.updatetodb(sql,[company_id,baoming,gmt_created,paytype])
                return HttpResponse('baoming')
            elif result=="nomoney":
                return HttpResponse('nomoney')
        elif paytype=='17':
            baoming=request.GET.get('baoming')
            result=zzq.getpayfee(company_id=company_id,ftype=paytype,fee=-1200)
            if result==1:
                sql='insert into shop_baoming(company_id,content,gmt_created,paytype) values(%s,%s,%s,%s)'
                dbc.updatetodb(sql,[company_id,baoming,gmt_created,paytype])
                return HttpResponse('baoming')
            elif result=="nomoney":
                return HttpResponse('nomoney')
    return HttpResponse('0')
#----商城简介
def simptxt(request):
    backurl=request.META.get('HTTP_REFERER','/')
    host=getnowurl(request)
    username=request.session.get("username",None)
    company_id=request.session.get("company_id",None)
    if username and (company_id==None or str(company_id)=="0"):
        company_id=getcompanyid(username)
        request.session['company_id']=company_id
    if (username==None or (company_id==None or str(company_id)=="0")):
        return HttpResponseRedirect("/login/?done="+host)
    return render_to_response('qianbao/simptxt.html',locals())
def oflist(request):
    host=getnowurl(request)
    username=request.session.get("username",None)
    company_id=request.session.get("company_id",None)
    if username and (company_id==None or str(company_id)=="0"):
        company_id=getcompanyid(username)
        request.session['company_id']=company_id
    if (username==None or (company_id==None or str(company_id)=="0")):
        return HttpResponseRedirect("/login/?done="+host)
    limitNum=7
    listall=zzt.getmyproductslist(frompageCount=0,limitNum=limitNum,company_id=company_id)
    count=listall['count']
    offerlist=listall['list']
#    if offerlist:
#        offid1=offerlist[0]['id']
    return render_to_response('qianbao/oflist.html',locals())
def offmore(request):
    company_id=request.session.get("company_id",None)
    if company_id:
        page=request.GET.get('page')
        if page:
            page=int(page)
        else:
            page=1
        limitNum=7
        listall=zzt.getmyproductslist(frompageCount=(page-1)*limitNum,limitNum=limitNum,company_id=company_id)
        offerlist=listall['list']
        return render_to_response('qianbao/offmore.html',locals())