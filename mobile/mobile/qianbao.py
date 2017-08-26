#-*- coding:utf-8 -*-
from django.shortcuts import render_to_response
from django.http import HttpResponse,HttpResponseRedirect,HttpResponsePermanentRedirect
import MySQLdb,sys,os,memcache,settings,urllib,re,time,datetime,requests,simplejson,random
from django.core.cache import cache

from commfunction import subString,filter_tags,replacepic
from function import getnowurl
from zz91page import *
from zz91db_ast import companydb
from zz91db_help import helpdb
from zz91db_130 import otherdb
from zz91db_sms import smsdb
from zz91db_2_news import newsdb
from sphinxapi import *
from settings import spconfig,weixinconfig
from zz91tools import getYesterday,getpastoneday,int_to_str,formattime,int_to_datetime,date_to_str
dbc=companydb()
dbn=newsdb()
dbh=helpdb()
reload(sys)
sys.setdefaultencoding('UTF-8')
nowpath=os.path.dirname(__file__)
execfile(nowpath+"/func/qianbao_function.py")
execfile(nowpath+"/func/myrc_function.py")
execfile(nowpath+"/func/trade_function.py")
execfile(nowpath+"/func/help_function.py")
execfile(nowpath+"/function.py")
execfile(nowpath+"/func/ldb_weixin_function.py")
from zzwx.client import Client
ldb_weixin=ldbweixin()
zzq=qianbao()
zzms=mshop()
zzt=ztrade()
dbsms=smsdb()
zzm=zmyrc()
zzhelp=zhelp()

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
    #4-1号调价
    #now = int(time.time())
    #paymoney=300
    #----判断是否为来电宝,跳转到来电宝钱包
#    viptype=zzq.getviptype(company_id)
#    if viptype=='10051003':
#        isldb=1
#        return HttpResponseRedirect('/ldb_weixin/index.html')

    #----第一次登录钱包送20
#    getfee20=zzq.getsendfee(company_id,20,6)
    
    #outfeeall2=zzq.getoutfeeall(company_id)
    #----余额
    blance=zzq.getqianbaoblance(company_id)
    #----昨日进账
    #infeeyd=zzq.getinfeeyd(company_id)
    #----总进账
    #infeeall=zzq.getinfeeall(company_id)
    #----昨日消费
    #outfeeyd=zzq.getoutfeeyd(company_id)
    #----总消费
    #outfeeall=zzq.getoutfeeall(company_id)
    #qianbaoblance=zzq.getqianbaoblance2(company_id)
    #我的代金券
    mydjqlist=zzms.mydaijinquanlist(company_id=company_id,qtype_id='')
    #我的服务
    serverlist=zzms.getmyservice(company_id)
    return render_to_response('aui/qianbao/index.html',locals())
    #return render_to_response('qianbao/index.html',locals())

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
    searchurl=''
    searchlist={}
    if timarg:
        searchlist['timarg']=timarg
    if searchlist:
        searchurl="?"+urllib.urlencode(searchlist)
    
    page=request.GET.get("page")
    if (not page or page=='' or page==0):
        page=1
    funpage=zz91page()
    limitNum=funpage.limitNum(20)
    nowpage=funpage.nowpage(int(page))
    frompageCount=funpage.frompageCount()
    after_range_num = funpage.after_range_num(5)
    before_range_num = funpage.before_range_num(4)
    
    payfeelist=zzq.getpayfeelist(company_id,frompageCount,limitNum,timarg)
    listcount=0
    if (payfeelist):
        listall=payfeelist['list']
        listcount=payfeelist['count']
        if (int(listcount)>1000000):
            listcount=1000000-1
    listcount = funpage.listcount(listcount)
    page_listcount=funpage.page_listcount()
    firstpage = funpage.firstpage()
    lastpage = funpage.lastpage()
    page_range  = funpage.page_range()
    nextpage = funpage.nextpage()
    prvpage = funpage.prvpage()
    
    
    gmtdate=time.strftime('%Y-%m-01 00:00:',time.localtime(time.time()))
    #----本月进账
    infeegmtnowmonth=zzq.getinfeegmt(company_id,gmtdate)
    #----本月消费
    outfeegmtnowmonth=zzq.getoutfeegmt(company_id,gmtdate)
    #----本月充值
    outfee5gmtnowmonth=zzq.getinfeegmt(company_id,gmtdate,'','(5,6)')
    
    #return render_to_response('qianbao/zhangdan.html',locals())
    return render_to_response('aui/qianbao/zhangdan.html',locals())
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
    #登录返回问题
    if "/login/?done=" in backurl:
        arrbackurl=backurl.split("/login/?done=")
        backurl=arrbackurl[1]
        if "http://" not in backurl:
            backurl="http://m.zz91.com"+backurl
    paytype=request.GET.get("paytype")
    buyer_id=request.GET.get("buyer_id")
    if not buyer_id:
        buyer_id='0'
    if not paytype:
        ldbvalue=getldbphone(company_id)
        if ldbvalue:
            paytype='ldb'
    paymoney=300
    companycontact=zzq.getcompanycontact(company_id)
    mobile=companycontact['mobile']
    contact=companycontact['contact']
    if(paytype == "ldb"):
        moerylist = ["3600.00","5000.00"];
        maxprice = 3600
        paymoney= 3600
    else:
        moerylist = ["300.00","500.00","800.00","1000.00","2000.00","5000.00","8000.00"];
        maxprice=300
        paymoney=300
    if not paytype:
        paytype="qianbao"
    money=request.GET.get("money")
    if money:
        moerylist = '';
        maxprice=money
        paymoney=money
    #钱包充值广告词
    #ggc=dbc.fetchnumberdb('select txt from qianbao_gg where id=1')
    return render_to_response('aui/qianbao/chongzhi.html',locals())
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
    return HttpResponsePermanentRedirect("http://m.zz91.com/service/index.html")
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
        errflag='true'
    errtext='系统错误'
    blanceflag='1'
    if not company_id or str(company_id)=="0":
        errflag='true'
        errtext='未登录，请先登录！'
    jsonlist={'err':errflag,'errtext':errtext,'blanceflag':blanceflag,'login':'false'}
    if company_id:
        paytype=str(request.GET.get('paytype'))
        money=request.GET.get('money')
        proid=request.GET.get('proid')
        mobile=request.GET.get('mobile')
        baoming=request.GET.get('baoming')
        voucher_id=request.GET.get('voucher_id')
        datevalue=request.GET.get("datevalue")
        #voucher_id=request.REQUEST.getlist("voucher_id")
        jsonlist=qianbaopaysave(company_id=company_id,paytype=paytype,money=money,proid=proid,mobile=mobile,baoming=baoming,voucher_id=voucher_id,datevalue=datevalue,request=request)
    js=request.GET.get('js')
    if js:
        return HttpResponse("var ret="+simplejson.dumps(jsonlist, ensure_ascii=False))
    return HttpResponse(simplejson.dumps(jsonlist, ensure_ascii=False))
def qianbaopaysave(company_id="",paytype="",money="",proid="",mobile="",baoming="",voucher_id="",datevalue="",request=""):
    errflag='true'
    errtext='系统错误'
    blanceflag='1'
    jsonlist={'err':errflag,'errtext':errtext,'blanceflag':blanceflag,'login':'true'}
    if money:
        money=int('-'+str(money))
    #----手机钱包付费
    gmt_end=''
    gmt_created=datetime.datetime.now()
    gmt_date=datetime.date.today()
    #供求置顶
    if paytype=='9':
        type='10431004'
        keywords=None
        if request:
            keywords=request.GET.get("keywords")
        result=zzq.getpayfee(company_id=company_id,product_id=proid,ftype=paytype,fee=money)
        if result==1:
            if keywords:
                zzq.getprotop(company_id,datevalue,keywords,proid)
            else:
                company_account=getaccount(company_id)
                if proid:
                    sql='insert into products_keywords_rank(product_id,is_checked,gmt_created,gmt_modified,company_id,apply_account,type,bz) values(%s,%s,%s,%s,%s,%s,%s,%s)'
                    dbc.updatetodb(sql,[proid,0,gmt_created,gmt_created,company_id,company_account,type,mobile])
            errflag='false'
            errtext='恭喜您，您已经设置成功！'
            #使用代金券
            if voucher_id:
                sql="update shop_voucher set used_id=%s where id in ("+str(voucher_id)+")"
                dbc.updatetodb(sql,[1])
            #送企业秀代金券
            title="企业秀（微站）代金券"
            zzq.insert_voucher(title=title,company_id=company_id,qtype_id=39,fee=20)
        else:
            errflag='true'
            errtext='余额不足，请充值！'
            blanceflag='0'
    #微信优质信息推广
    elif paytype=='10':
#            result=1
        sql2='select id from shop_product_wxtg where company_id=%s and is_check=0'
        result2=dbc.fetchonedb(sql2,[company_id])
        if result2:
            errflag='true'
            errtext='该供求已经设置过置顶操作，请选择其他供求。'
        else:
            result=zzq.getpayfee(company_id=company_id,product_id=proid,ftype=paytype)
            if result==1:
                if baoming:
                    sql='insert into shop_product_wxtg(company_id,mobile,is_check,gmt_date,gmt_created,gmt_modified) values(%s,%s,%s,%s,%s,%s)'
                    dbc.updatetodb(sql,[company_id,mobile,'0',gmt_date,gmt_created,gmt_created])
                errflag='false'
                errtext='恭喜您，您已经设置成功！'
                #使用代金券
                if voucher_id:
                    sql="update shop_voucher set used_id=%s where id in ("+str(voucher_id)+")"
                    dbc.updatetodb(sql,[1])
            else:
                errflag='true'
                errtext='余额不足，请充值！'
                blanceflag='0'
            
    #显示联系方式
    elif paytype=='11':
        result=zzq.getpayfee(company_id=company_id,ftype=paytype,fee=money)
        if result==1:
            zzq.buyshowcontact(company_id,money,datevalue=datevalue)
            #使用代金券
            if voucher_id:
                sql="update shop_voucher set used_id=%s where id in ("+str(voucher_id)+")"
                dbc.updatetodb(sql,[1])
            #送自动刷新代金券
            title="供求自动刷新代金券"
            zzq.insert_voucher(title=title,company_id=company_id,qtype_id=42,fee=10)
            errflag='false'
            errtext='恭喜您，您已经成功开通显示联系方式的服务！'
        else:
            errflag='true'
            errtext='余额不足，请充值！'
            blanceflag='0'
    #定时刷新供求
    elif paytype=='42':
        fee=int(money)*100
        if (datevalue):
            fee=money
        else:
            datevalue=-int(money)
        result=zzq.getpayfee(company_id=company_id,ftype=paytype,fee=fee)
        if result==1:
            zzq.buyreflushtrade(company_id,-int(datevalue))
            #使用代金券
            if voucher_id:
                sql="update shop_voucher set used_id=%s where id in ("+str(voucher_id)+")"
                dbc.updatetodb(sql,[1])
            #送显示联系方式代金券
            title="显示联系方式代金券"
            zzq.insert_voucher(title=title,company_id=company_id,qtype_id=11,fee=10)
            errflag='false'
            errtext='恭喜您，您已经成功开通供求自动刷新的服务！'
        else:
            errflag='true'
            errtext='余额不足，请充值！'
            blanceflag='0'
    #企业秀
    elif paytype=='39':
        fee=money
        xiumovalue="h1"
        if request:
            xiumovalue=request.GET.get("xiumovalue")
        result=zzq.getpayfee(company_id=company_id,ftype=paytype,fee=fee)
        if result==1:
            zzq.buyqiyexiu(company_id,int(datevalue),xiumovalue=xiumovalue)
            #使用代金券
            if voucher_id:
                sql="update shop_voucher set used_id=%s where id in ("+str(voucher_id)+")"
                dbc.updatetodb(sql,[1])
            #送供求置顶代金券
            title="供求置顶代金券"
            zzq.insert_voucher(title=title,company_id=company_id,qtype_id=9,fee=20)
            errflag='false'
            errtext='恭喜您，您已经成功开通企业秀服务！'
        else:
            errflag='true'
            errtext='余额不足，请充值！'
            blanceflag='0'
    #购买显示联系方式+供求自动刷新 抢购服务
    elif paytype=='48':
        result=zzq.getpayfee(company_id=company_id,ftype=paytype,fee=money)
        if result==1:
            zzq.buyshowcontact(company_id,-300)
            zzq.buyreflushtrade(company_id,-1)
            errflag='false'
            errtext='恭喜您，您已经成功开通“显示联系方式的服务”和“供求自动刷新的服务”！'
        else:
            errflag='true'
            errtext='余额不足，请充值！'
            blanceflag='0'
    #供求置顶2个月+企业秀
    elif paytype=='52':
        result=zzq.getpayfee(company_id=company_id,ftype=paytype,fee=money)
        if result==1:
            errflag='false'
            errtext='恭喜您，您已经购买成功，我们会两个工作日内（节假日顺延）与你联系！'
        else:
            errflag='true'
            errtext='余额不足，请充值！'
            blanceflag='0'
    #购买商务大全
    elif paytype=='16':
        result=zzq.getpayfee(company_id=company_id,ftype=paytype)
        if str(result)=="1":
            sql='insert into shop_baoming(company_id,content,gmt_created,paytype) values(%s,%s,%s,%s)'
            dbc.updatetodb(sql,[company_id,baoming,gmt_created,paytype])
            errflag='false'
            errtext='恭喜您，您已经购买成功，我们会尽快和您联系！'
        elif result=="nomoney":
            errflag='true'
            errtext='余额不足，请充值！'
            blanceflag='0'
    #移动端列表页广告
    elif paytype=='17':
        fee=money
        result=zzq.getpayfee(company_id=company_id,ftype=paytype,fee=fee)
        if result==1:
            if baoming:
                sql='insert into shop_baoming(company_id,content,gmt_created,paytype) values(%s,%s,%s,%s)'
                dbc.updatetodb(sql,[company_id,baoming,gmt_created,paytype])
            errflag='false'
            errtext='恭喜您，您已经购买成功，我们会两个工作日内（节假日顺延）与你联系！'
            #送企业秀代金券
            title="企业秀（微站）代金券"
            zzq.insert_voucher(title=title,company_id=company_id,qtype_id=39,fee=20)
        elif result=="nomoney":
            errflag='true'
            errtext='余额不足，请充值！'
            blanceflag='0'
    #再生资源商务大全App抢购价
    elif paytype in ('20','40','41'):
        result=zzq.getpayfee(company_id=company_id,ftype=paytype)
        if str(result)=="1":
            if baoming:
                sql='insert into shop_baoming(company_id,content,gmt_created,paytype) values(%s,%s,%s,%s)'
                dbc.updatetodb(sql,[company_id,baoming,gmt_created,paytype])
            errflag='false'
            errtext='恭喜您，您已经购买成功，我们会尽快和您联系！'
        elif result=="nomoney":
            errflag='true'
            errtext='余额不足，请充值！'
            blanceflag='0'
        elif result=="havepay":
            errflag='true'
            errtext='你已经购买了该服务！'
    #留言速配服务
    elif paytype=="60":
        result=zzq.getpayfee(company_id=company_id,ftype=paytype)
        if str(result)=="1":
            content=request.GET.get("content")
            if content:
                sql='insert into shop_qunfa(company_id,content,gmt_created) values(%s,%s,%s)'
                dbc.updatetodb(sql,[company_id,content,gmt_created])
            errflag='false'
            errtext='恭喜您，您已经购买成功！'
        elif result=="nomoney":
            errflag='true'
            errtext='余额不足，请充值！'
            blanceflag='0'
        elif result=="havepay":
            errflag='true'
            errtext='你已经购买了该服务！'
    jsonlist={'err':errflag,'errtext':errtext,'blanceflag':blanceflag,'login':'true'}
    return jsonlist

def getqianbao(request):
    weixinid=request.GET.get('weixinid')
    gettype=request.GET.get('gettype')
    account=weixinbinding(weixinid)
    gmt_created=datetime.datetime.now()
    gmt_date=datetime.date.today()
    if account:
        request.session["username"]=account
        company_id=getcompanyid(account)
        request.session['company_id']=company_id
        if (gettype=="7day"):
            suctext="你已经获取了10元再生钱包！"
            sql="select id,qiandao_list from weixin_qiandao_count where qiandao_count=7 and account=%s and checked=0 order by id asc"
            result=dbc.fetchonedb(sql,[account])
            if result:
                zzq.getsendfee(company_id,"10","46",more=1)
                qid=result[0]
                qiandao_list=result[1]
                #return HttpResponse(qiandao_list)
                sql="update weixin_qiandao_count set checked=1 where id=%s"
                dbc.updatetodb(sql,[qid])
                sql="update weixin_qiandao set checked=%s where id in ("+str(qiandao_list)+")"
                dbc.updatetodb(sql,[1])
                suctext="恭喜您，已经获取10元再生钱包！"
        if (gettype=="21day"):
            suctext="您已经开通了供求自动刷新的服务！"
            sql="select id,qiandao_list,qiandao_count from weixin_qiandao_count where qiandao_count>=7 and account=%s and checked=0 order by id asc"
            resulta=dbc.fetchalldb(sql,[account])
            if resulta:
                qiandao_count=0
                qidlist=""
                qiandao_list=""
                for list in resulta:
                    qid=list[0]
                    qidlist+=str(qid)+","
                    qiandao_list+=list[1]+","
                    qiandao_count+=list[2]
                    if qiandao_count==21:
                        sql="update weixin_qiandao_count set checked=1 where id in (%s)"
                        dbc.updatetodb(sql,[str(qidlist)[0:len(qidlist)-1]])
                        sql="update weixin_qiandao set checked=%s where id in ("+str(qiandao_list)[0:len(qiandao_list)-1]+")"
                        dbc.updatetodb(sql,[1])
                        sql2='select id,UNIX_TIMESTAMP(gmt_end) from shop_reflush where company_id=%s and DATEDIFF(CURDATE(),gmt_end)<=0 order by id desc'
                        result=dbc.fetchonedb(sql2,[company_id])
                        if result:
                            errflag='true'
                            suctext='您已经开通了供求自动刷新的服务，请不必重复开通。'
                            reupdate=1
                            gmt_begin=result[1]
                        else:
                            reupdate=1
                            gmt_begin=int(time.time())
                        if reupdate==1:
                            gmt_end=gmt_begin+(3600*24*30)
                            gmt_begin=int_to_datetime(gmt_begin)
                            gmt_end=int_to_datetime(gmt_end)
                            sql='insert into shop_reflush(company_id,gmt_begin,gmt_end,gmt_created,gmt_date) values(%s,%s,%s,%s,%s)'
                            dbc.updatetodb(sql,[company_id,gmt_begin,gmt_end,gmt_created,gmt_date])
                            errflag='false'
                            suctext='恭喜您，您已经成功开通供求自动刷新的服务！'
                            wxc = Client(weixinconfig['zz91dingyue']['appid'], weixinconfig['zz91dingyue']['secret'])
                            token=wxc.send_text_message(weixinid,suctext+"开始时间："+str(gmt_begin)+";到期时间："+str(gmt_end))
                        suctext="恭喜您，您已成功获取 一个月“自动刷新供求服务”！"
        return render_to_response('qianbao/suc.html',locals())
    return HttpResponse("错误")
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
#签到
def qiandao(request):
    host=getnowurl(request)
    username=request.session.get("username",None)
    company_id=request.session.get("company_id",None)
    if username and (company_id==None or str(company_id)=="0"):
        company_id=getcompanyid(username)
        request.session['company_id']=company_id
    if not company_id:
        errlist={'login':'false'}
        return HttpResponse(simplejson.dumps(errlist, ensure_ascii=False))
    gmt_created=datetime.datetime.now()
    gmt_date=datetime.date.today()
    sql="select id from app_qiandao where company_id=%s and gmt_date=%s"
    result=dbc.fetchonedb(sql,[company_id,gmt_date])
    if result:
        messagedata={'err':'true','errkey':'已经签到'}
        return HttpResponse(simplejson.dumps(messagedata, ensure_ascii=False))
    else:
        sql="insert into app_qiandao(company_id,gmt_date,gmt_created) values(%s,%s,%s)"
        dbc.updatetodb(sql,[company_id,gmt_date,gmt_created])
        ftype="29"
        fee="0.5"
        more=1
        zzq.getsendfee(company_id,fee,ftype,more=more)
        messagedata={'err':'false','errkey':''}
        return HttpResponse(simplejson.dumps(messagedata, ensure_ascii=False))
#钱包余额
def qianbaobaoblance(request):
    host=getnowurl(request)
    username=request.session.get("username",None)
    company_id=request.session.get("company_id",None)
    if username and (company_id==None or str(company_id)=="0"):
        company_id=getcompanyid(username)
        request.session['company_id']=company_id
    if (username==None or (company_id==None or str(company_id)=="0")):
        return HttpResponseRedirect("/login/?done="+host)
    baoblance=0
    if company_id:
        baoblance=zzq.getqianbaoblance(company_id)
        showphone=zzq.getisbuyshowphone(company_id)
        if not showphone:
            showphone=zzq.getiszstcompany(company_id)
        jsonlist={'blance':baoblance,'showphone':showphone}
    return HttpResponse(simplejson.dumps(jsonlist, ensure_ascii=False))

def llb_index(request):
    return render_to_response('aui/service/llb.html',locals())
def llb_add(request):
    host=getnowurl(request)
    username=request.session.get("username",None)
    company_id=request.session.get("company_id",None)
    if username and (company_id==None or str(company_id)=="0"):
        company_id=getcompanyid(username)
        request.session['company_id']=company_id
    if (username==None or (company_id==None or str(company_id)=="0")):
        return HttpResponseRedirect("/login/?done="+host)
    res={'maxprice':5,'minblance':300}
    return render_to_response('aui/service/llb_add.html',locals())
def llb_selectpro(request):
    return render_to_response('aui/service/llb_selectpro.html',locals())
def llb_category(request):
    return render_to_response('aui/service/llb_category.html',locals())
#竞价最低价，充值最低
def jingjia_info(request):
    res={'maxprice':5,'minblance':300}
    return HttpResponse(simplejson.dumps(res, ensure_ascii=False))
#关键字竞价排名保存
def jingjia_keywords_save(request):
    host=getnowurl(request)
    username=request.session.get("username",None)
    company_id=request.session.get("company_id",None)
    if username and (company_id==None or str(company_id)=="0"):
        company_id=getcompanyid(username)
        request.session['company_id']=company_id
    if (username==None or (company_id==None or str(company_id)=="0")):
        return HttpResponseRedirect("/login/?done="+host)
    keywords=request.POST.get("keywords")
    price=request.POST.get("price")
    product_id=request.POST.get("product_id")
    if keywords:
        gmt_created=datetime.datetime.now()
        arrkeywords=keywords.split(",")
        for k in arrkeywords:
            if k:
                sql="select id from app_jingjia_keywords where keywords=%s and product_id=%s"
                result=dbc.fetchonedb(sql,[k,product_id])
                if not result:
                    sqld="insert into app_jingjia_keywords(company_id,keywords,price,product_id,gmt_created) values(%s,%s,%s,%s,%s)"
                    dbc.updatetodb(sqld,[company_id,k,price,product_id,gmt_created])
        resjson={'err':'false','errkey':'开通成功！'}
        #首次开通送88元
        #zzq.getsendfee(company_id,88,56)
        return HttpResponse(simplejson.dumps(resjson, ensure_ascii=False))
    else:
        resjson={'err':'true','errkey':'没有提交关键词'}
        return HttpResponse(simplejson.dumps(resjson, ensure_ascii=False))
#竞价点击计费
def jingjia_click_save(request):
    company_id=request.GET.get("company_id")
    usertoken=request.GET.get("usertoken")
    key_id=request.GET.get("key_id")
    search_id=request.GET.get("search_id")
    keywords=request.GET.get("keywords")
    area=request.GET.get("area")
    userid=clientid=request.GET.get("clientid")
    sql="select company_id,price from app_jingjia_keywords where id=%s"
    result=dbc.fetchonedb(sql,[key_id])
    if result:
        forcompany_id=result[0]
        price=result[1]
        sourcetype=1
        user_company_id=company_id
        if int(company_id)!=int(forcompany_id):
            gmt_created=datetime.datetime.now()
            sqlc="select id from app_jingjia_click where key_id=%s and search_id=%s"
            res=dbc.fetchonedb(sqlc,[key_id,search_id])
            if not res:
                clickcount=1
                sqld="insert into app_jingjia_click(key_id,search_id,price,clickcount,sourcetype,userid,user_company_id,company_id,area,gmt_created) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
                dbc.updatetodb(sqld,[key_id,search_id,price,clickcount,sourcetype,userid,user_company_id,forcompany_id,area,gmt_created])
                #扣款
                zzq.getpayfee(company_id=forcompany_id,forcompany_id=company_id,ftype=55,fee=-int(price))
            else:
                sqld="update app_jingjia_click set clickcount=clickcount+1 where id=%s"
                dbc.updatetodb(sqld,[res[0]])
    resjson={'err':'false','errkey':''}
    return HttpResponse(simplejson.dumps(resjson, ensure_ascii=False))
            
#我的竞价推广
def jingjia_index(request):
    host=getnowurl(request)
    username=request.session.get("username",None)
    company_id=request.session.get("company_id",None)
    if username and (company_id==None or str(company_id)=="0"):
        company_id=getcompanyid(username)
        request.session['company_id']=company_id
    if (username==None or (company_id==None or str(company_id)=="0")):
        return HttpResponseRedirect("/login/?done="+host)
    #展示量
    sql="select sum(showcount>0),sum(clickcount>0) from app_jingjia_search where company_id=%s"
    result=dbc.fetchonedb(sql,[company_id])
    showcount=0
    clickcount=0
    if result:
        showcount=result[0]
        if not showcount:
            showcount=0
    blance=zzq.getqianbaoblance(company_id,jingjia=1)
    #点击量
    sql="select sum(clickcount) from app_jingjia_click where company_id=%s"
    result=dbc.fetchonedb(sql,[company_id])
    if result:
        clickcount=result[0]
    else:
        clickcount=0
    #消费
    sqlk="select sum(fee) from pay_mobilewallet where company_id=%s and ftype=%s"
    result=dbc.fetchonedb(sqlk,[company_id,55])
    pricecount=0
    if result:
        pricecount=result[0]
    if not pricecount:
        pricecount=0
    #电话量
    phonecount=0
    sql="select count(0) from phone_telclick_log where forcompany_id=%s"
    result=dbc.fetchonedb(sql,[company_id])
    if result:
        phonecount=result[0]
        if not phonecount:
            phonecount=0
    
    tjlist={'showcount':showcount,'clickcount':clickcount,'pricecount':pricecount,'phonecount':phonecount}
    #
    keylist=[]
    sql="select id,keywords,price,checked from app_jingjia_keywords where company_id=%s"
    result=dbc.fetchalldb(sql,[company_id])
    for list in result:
        key_id=list[0]
        keywords=list[1]
        checked=list[3]
        if checked==1:
            checktext="已上线"
        else:
            checktext="<font color='#ff0000'>已下线</font>"
        key_showcount=0
        key_clickcount=0
        sqlk="select sum(showcount) from app_jingjia_search where company_id=%s and key_id=%s"
        resultc=dbc.fetchonedb(sqlk,[company_id,key_id])
        if resultc:
            key_showcount=resultc[0]
            if not key_showcount:
                key_showcount=0
            
        sqlk="select sum(clickcount) from app_jingjia_click where company_id=%s and key_id=%s"
        resultc=dbc.fetchonedb(sqlk,[company_id,key_id])
        if resultc:
            key_clickcount=resultc[0]
            if not key_clickcount:
                key_clickcount=0
                
        sqlk="select clickcount,price from app_jingjia_click where company_id=%s and key_id=%s"
        result=dbc.fetchalldb(sqlk,[company_id,key_id])
        key_pricecount=0
        if result:
            for lk in result:
                clickc=lk[0]
                price=lk[1]
                key_pricecount+=price
        if not key_pricecount:
            key_pricecount=0
        #流量宝帮助中心
        hlist=zzhelp.getarticallist(0,20,typeid=73)
        
        ll={'key_id':key_id,'keywords':keywords,'key_showcount':key_showcount,'key_clickcount':key_clickcount,'key_pricecount':key_pricecount,'checktext':checktext}
        keylist.append(ll)
    reslist={'tjlist':tjlist,'keylist':keylist}
    return render_to_response('aui/myrc/my-llb.html',locals())
#关键词信息
def jingjia_keywords_info(request):
    host=getnowurl(request)
    username=request.session.get("username",None)
    company_id=request.session.get("company_id",None)
    if username and (company_id==None or str(company_id)=="0"):
        company_id=getcompanyid(username)
        request.session['company_id']=company_id
    if (username==None or (company_id==None or str(company_id)=="0")):
        return HttpResponseRedirect("/login/?done="+host)
    key_id=request.GET.get("key_id")
    list=None
    if key_id:
        sql="select keywords,price,checked from app_jingjia_keywords where id=%s"
        result=dbc.fetchonedb(sql,[key_id])
        if result:
            keywords=result[0]
            price=result[1]
            checked=result[2]
            list={'keywords':keywords,'price':price,'checked':checked}
    return render_to_response('aui/myrc/my-llb-mod.html',locals())

#保存关键词，出价
def jingjia_keywords_onesave(request):
    username=request.session.get("username",None)
    company_id=request.session.get("company_id",None)
    if username and (company_id==None or str(company_id)=="0"):
        company_id=getcompanyid(username)
        request.session['company_id']=company_id
    if (username==None or (company_id==None or str(company_id)=="0")):
        return HttpResponseRedirect("/login/?done="+host)
    key_id=request.POST.get("key_id")
    keywords=request.POST.get("keywords")
    price=request.POST.get("price")
    sql="update app_jingjia_keywords set keywords=%s,price=%s where id=%s and company_id=%s"
    dbc.updatetodb(sql,[keywords,price,key_id,company_id])
    resjson={'err':'false','errkey':''}
    return HttpResponse(simplejson.dumps(resjson, ensure_ascii=False))
#关键词下线
def jingjia_keywords_offline(request):
    username=request.session.get("username",None)
    company_id=request.session.get("company_id",None)
    if username and (company_id==None or str(company_id)=="0"):
        company_id=getcompanyid(username)
        request.session['company_id']=company_id
    if (username==None or (company_id==None or str(company_id)=="0")):
        return HttpResponseRedirect("/login/?done="+host)
    key_id=request.POST.get("key_id")
    checked=request.POST.get("checked")
    if not checked:
        checked=0
    sql="update app_jingjia_keywords set checked=%s where id=%s and company_id=%s"
    dbc.updatetodb(sql,[checked,key_id,company_id])
    resjson={'err':'false','errkey':''}
    return HttpResponse(simplejson.dumps(resjson, ensure_ascii=False))
#我的关键词消费明细
def jingjia_keywords_paylist(request):
    host=getnowurl(request)
    username=request.session.get("username",None)
    company_id=request.session.get("company_id",None)
    if username and (company_id==None or str(company_id)=="0"):
        company_id=getcompanyid(username)
        request.session['company_id']=company_id
    if (username==None or (company_id==None or str(company_id)=="0")):
        return HttpResponseRedirect("/login/?done="+host)
    page=request.GET.get("page")
    if not page:
        page=1
    funpage=zz91page()
    limitNum=funpage.limitNum(20)
    nowpage=funpage.nowpage(int(page))
    frompageCount=funpage.frompageCount()
    after_range_num = funpage.after_range_num(3)
    before_range_num = funpage.before_range_num(6)
    key_id=request.GET.get("key_id")
    if not key_id:
        key_id=''
    
    datekey=request.GET.get("datekey")
    
    searchlist={}
    if datekey:
        searchlist['datekey']=datekey
    if key_id:
        searchlist['key_id']=key_id
    searchurl=urllib.urlencode(searchlist)
    
    messagelist=zzq.jingjia_keypaylist(frompageCount,limitNum,company_id=company_id,key_id=key_id,datekey=datekey)
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
    keylist=zzq.jingjia_keywords(company_id=company_id)
    return render_to_response('aui/myrc/my-llb-fee.html',locals())
#用户点击明细
def jingjia_keywords_clicklist(request):
    host=getnowurl(request)
    username=request.session.get("username",None)
    company_id=request.session.get("company_id",None)
    if username and (company_id==None or str(company_id)=="0"):
        company_id=getcompanyid(username)
        request.session['company_id']=company_id
    if (username==None or (company_id==None or str(company_id)=="0")):
        return HttpResponseRedirect("/login/?done="+host)
    page=request.GET.get("page")
    if not page:
        page=1
    funpage=zz91page()
    limitNum=funpage.limitNum(20)
    nowpage=funpage.nowpage(int(page))
    frompageCount=funpage.frompageCount()
    after_range_num = funpage.after_range_num(3)
    before_range_num = funpage.before_range_num(6)
    key_id=request.GET.get("key_id")
    messagelist=zzq.jingjia_keyclicklist(frompageCount,limitNum,company_id=company_id,key_id=key_id)
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
    keylist=zzq.jingjia_keywords(company_id=company_id)
    return render_to_response('aui/myrc/my-llb-click.html',locals())

#窗口充值
def minichongzhi(request):
    host=getnowurl(request)
    backurl=request.META.get('HTTP_REFERER','/')
    username=request.session.get("username",None)
    company_id=request.session.get("company_id",None)
    if username and (company_id==None or str(company_id)=="0"):
        company_id=getcompanyid(username)
        request.session['company_id']=company_id
    if (username==None or (company_id==None or str(company_id)=="0")):
        return HttpResponseRedirect("/login/?done="+host)
    paytype=request.GET.get("paytype")
    companycontact=zzq.getcompanycontact(company_id)
    mobile=companycontact['mobile']
    contact=companycontact['contact']
    if(paytype == "ldb"):
        moerylist = ["2500","3000","4000","5000"];
        maxprice = 2500
    else:
        moerylist = ["300.00","500.00","800.00","1000.00","2000.00","5000.00"];
        maxprice=300
    return render_to_response('aui/qianbao/minichongzhi.html',locals())
def myservice(request):
    host=getnowurl(request)
    zzm.weixinautologin(request,request.GET.get("weixinid"))
    username=request.session.get("username",None)
    company_id=request.session.get("company_id",None)
    if username and (company_id==None or str(company_id)=="0"):
        company_id=getcompanyid(username)
        request.session['company_id']=company_id
    if (username==None or (company_id==None or str(company_id)=="0")):
        return HttpResponseRedirect("/login/?done="+host)
    serverlist=zzms.getmyservice(company_id)
    return render_to_response('aui/service/myservice.html',locals())
#产品服务
def cp_index(request):
    
    return render_to_response('aui/service/index.html',locals())
def cp_youhui(request):
    youhuilist=zzms.listgoods(0,20,ptype="1")['list']
    return render_to_response('aui/service/youhui.html',locals())
def cp_autoreflush(request):
    host=getnowurl(request)
    zzm.weixinautologin(request,request.GET.get("weixinid"))
    username=request.session.get("username",None)
    company_id=request.session.get("company_id",None)
    if username and (company_id==None or str(company_id)=="0"):
        company_id=getcompanyid(username)
        request.session['company_id']=company_id
    if (username==None or (company_id==None or str(company_id)=="0")):
        return HttpResponseRedirect("/login/?done="+host)
    youhuilist=zzms.listgoods(0,5,ptype="1")['list']
    mydjq=zzms.mydaijinquan(company_id,42)
    return render_to_response('aui/service/cp_autoreflush.html',locals())
def cp_book_buy(request):
    host=getnowurl(request)
    zzm.weixinautologin(request,request.GET.get("weixinid"))
    username=request.session.get("username",None)
    company_id=request.session.get("company_id",None)
    if username and (company_id==None or str(company_id)=="0"):
        company_id=getcompanyid(username)
        request.session['company_id']=company_id
    if (username==None or (company_id==None or str(company_id)=="0")):
        return HttpResponseRedirect("/login/?done="+host)
    return render_to_response('aui/service/cp_book_buy.html',locals())

def cp_book(request):
    host=getnowurl(request)
    zzm.weixinautologin(request,request.GET.get("weixinid"))
    username=request.session.get("username",None)
    company_id=request.session.get("company_id",None)
    if username and (company_id==None or str(company_id)=="0"):
        company_id=getcompanyid(username)
        request.session['company_id']=company_id
    if (username==None or (company_id==None or str(company_id)=="0")):
        return HttpResponseRedirect("/login/?done="+host)
    return render_to_response('aui/service/cp_book.html',locals())
def cp_createwebsite(request):
    host=getnowurl(request)
    zzm.weixinautologin(request,request.GET.get("weixinid"))
    username=request.session.get("username",None)
    company_id=request.session.get("company_id",None)
    if username and (company_id==None or str(company_id)=="0"):
        company_id=getcompanyid(username)
        request.session['company_id']=company_id
    if (username==None or (company_id==None or str(company_id)=="0")):
        return HttpResponseRedirect("/login/?done="+host)
    return render_to_response('aui/service/cp_createwebsite.html',locals())
def cp_createwebsite_buy(request):
    return render_to_response('aui/service/cp_createwebsite_buy.html',locals())
def cp_ldb(request):
    host=getnowurl(request)
    zzm.weixinautologin(request,request.GET.get("weixinid"))
    username=request.session.get("username",None)
    company_id=request.session.get("company_id",None)
    if username and (company_id==None or str(company_id)=="0"):
        company_id=getcompanyid(username)
        request.session['company_id']=company_id
    if (username==None or (company_id==None or str(company_id)=="0")):
        return HttpResponseRedirect("/login/?done="+host)
    return render_to_response('aui/service/cp_ldb.html',locals())
def cp_listad(request):
    return render_to_response('aui/service/cp_listad.html',locals())
def cp_listad_buy(request):
    host=getnowurl(request)
    zzm.weixinautologin(request,request.GET.get("weixinid"))
    username=request.session.get("username",None)
    company_id=request.session.get("company_id",None)
    if username and (company_id==None or str(company_id)=="0"):
        company_id=getcompanyid(username)
        request.session['company_id']=company_id
    if (username==None or (company_id==None or str(company_id)=="0")):
        return HttpResponseRedirect("/login/?done="+host)
    youhuilist=zzms.listgoods(0,5,ptype="1")['list']
    mydjq=zzms.mydaijinquan(company_id,17)
    return render_to_response('aui/service/cp_listad_buy.html',locals())
def cp_indexad_buy(request):
    host=getnowurl(request)
    zzm.weixinautologin(request,request.GET.get("weixinid"))
    username=request.session.get("username",None)
    company_id=request.session.get("company_id",None)
    if username and (company_id==None or str(company_id)=="0"):
        company_id=getcompanyid(username)
        request.session['company_id']=company_id
    if (username==None or (company_id==None or str(company_id)=="0")):
        return HttpResponseRedirect("/login/?done="+host)
    youhuilist=zzms.listgoods(0,5,ptype="1")['list']
    mydjq=zzms.mydaijinquan(company_id,58)
    return render_to_response('aui/service/cp_indexad_buy.html',locals())
def cp_huangjinad_buy(request):
    host=getnowurl(request)
    zzm.weixinautologin(request,request.GET.get("weixinid"))
    username=request.session.get("username",None)
    company_id=request.session.get("company_id",None)
    if username and (company_id==None or str(company_id)=="0"):
        company_id=getcompanyid(username)
        request.session['company_id']=company_id
    if (username==None or (company_id==None or str(company_id)=="0")):
        return HttpResponseRedirect("/login/?done="+host)
    youhuilist=zzms.listgoods(0,5,ptype="1")['list']
    mydjq=zzms.mydaijinquan(company_id,59)
    return render_to_response('aui/service/cp_huangjinad_buy.html',locals())
def cp_lookcontact(request):
    host=getnowurl(request)
    zzm.weixinautologin(request,request.GET.get("weixinid"))
    username=request.session.get("username",None)
    company_id=request.session.get("company_id",None)
    if username and (company_id==None or str(company_id)=="0"):
        company_id=getcompanyid(username)
        request.session['company_id']=company_id
    if (username==None or (company_id==None or str(company_id)=="0")):
        return HttpResponseRedirect("/login/?done="+host)
    return render_to_response('aui/service/cp_lookcontact.html',locals())
def cp_producttop(request):
    return render_to_response('aui/service/cp_producttop.html',locals())
def cp_producttop_buy(request):
    host=getnowurl(request)
    zzm.weixinautologin(request,request.GET.get("weixinid"))
    username=request.session.get("username",None)
    company_id=request.session.get("company_id",None)
    if username and (company_id==None or str(company_id)=="0"):
        company_id=getcompanyid(username)
        request.session['company_id']=company_id
    if (username==None or (company_id==None or str(company_id)=="0")):
        return HttpResponseRedirect("/login/?done="+host)
    youhuilist=zzms.listgoods(0,5,ptype="1")['list']
    mydjq=zzms.mydaijinquan(company_id,9)
    return render_to_response('aui/service/cp_producttop_buy.html',locals())
def cp_producttop_select(request):
    return render_to_response('aui/service/cp_producttop_select.html',locals())
def cp_qyx(request):
    return render_to_response('aui/service/cp_qyx.html',locals())
def cp_qyx_buy(request):
    host=getnowurl(request)
    zzm.weixinautologin(request,request.GET.get("weixinid"))
    username=request.session.get("username",None)
    company_id=request.session.get("company_id",None)
    if username and (company_id==None or str(company_id)=="0"):
        company_id=getcompanyid(username)
        request.session['company_id']=company_id
    if (username==None or (company_id==None or str(company_id)=="0")):
        return HttpResponseRedirect("/login/?done="+host)
    youhuilist=zzms.listgoods(0,5,ptype="1")['list']
    mydjq=zzms.mydaijinquan(company_id,39)
    return render_to_response('aui/service/cp_qyx_buy.html',locals())
def cp_seo(request):
    host=getnowurl(request)
    host=host.replace("^and^","&")
    return render_to_response('aui/service/cp_seo.html',locals())
def cp_seo_buy(request):
    
    return render_to_response('aui/service/cp_seo_buy.html',locals())
def cp_showcontact(request):
    host=getnowurl(request)
    zzm.weixinautologin(request,request.GET.get("weixinid"))
    username=request.session.get("username",None)
    company_id=request.session.get("company_id",None)
    if username and (company_id==None or str(company_id)=="0"):
        company_id=getcompanyid(username)
        request.session['company_id']=company_id
    if (username==None or (company_id==None or str(company_id)=="0")):
        return HttpResponseRedirect("/login/?done="+host)
    youhuilist=zzms.listgoods(0,5,ptype="1")['list']
    mydjq=zzms.mydaijinquan(company_id,11)
    return render_to_response('aui/service/cp_showcontact.html',locals())
def cp_zst(request):
    host=getnowurl(request)
    zzm.weixinautologin(request,request.GET.get("weixinid"))
    username=request.session.get("username",None)
    company_id=request.session.get("company_id",None)
    if username and (company_id==None or str(company_id)=="0"):
        company_id=getcompanyid(username)
        request.session['company_id']=company_id
    if (username==None or (company_id==None or str(company_id)=="0")):
        return HttpResponseRedirect("/login/?done="+host)
    return render_to_response('aui/service/cp_zst.html',locals())
def cp_qunfa(request):
    host=getnowurl(request)
    zzm.weixinautologin(request,request.GET.get("weixinid"))
    username=request.session.get("username",None)
    company_id=request.session.get("company_id",None)
    if username and (company_id==None or str(company_id)=="0"):
        company_id=getcompanyid(username)
        request.session['company_id']=company_id
    if (username==None or (company_id==None or str(company_id)=="0")):
        return HttpResponseRedirect("/login/?done="+host)
    return render_to_response('aui/service/cp_qunfa.html',locals())
def fuwu(request):
    host=getnowurl(request)
    host=host.replace("^and^","&")
    return render_to_response('aui/service/fuwu.html',locals())

def fuwu_baidu(request):
    host=getnowurl(request)
    host=host.replace("^and^","&")
    return render_to_response('aui/service/fuwu_baidu.html',locals())

def fuwu_jpppt(request):
    return render_to_response('aui/service/fuwu_jpppt.html',locals())
def fuwu_ldb(request):
    host=getnowurl(request)
    host=host.replace("^and^","&")
    zzm.weixinautologin(request,request.GET.get("weixinid"))
    username=request.session.get("username",None)
    company_id=request.session.get("company_id",None)
    
    return render_to_response('aui/service/fuwu_ldb.html',locals())

def fuwu_ppai(request):
    host=getnowurl(request)
    host=host.replace("^and^","&")
    return render_to_response('aui/service/fuwu_ppai.html',locals())

def fuwu_zsppt(request):
    return render_to_response('aui/service/fuwu_zsppt.html',locals())

def fuwu_zst(request):
    host=getnowurl(request)
    host=host.replace("^and^","&")
    zzm.weixinautologin(request,request.GET.get("weixinid"))
    username=request.session.get("username",None)
    company_id=request.session.get("company_id",None)
    return render_to_response('aui/service/fuwu_zst.html',locals())

def fuwu_zstct(request):
    return render_to_response('aui/service/fuwu_zstct.html',locals())


