#-*- coding:utf-8 -*-
from django.shortcuts import render_to_response
import simplejson
from django.http import HttpResponse,HttpResponseRedirect,HttpResponsePermanentRedirect
import MySQLdb,sys,os,memcache,settings,urllib,re,time,datetime,random,hashlib,requests
from django.core.cache import cache
import memcache
from zz91tools import subString,filter_tags,formattime,int_to_datetime,date_to_int,date_to_strall,date_to_str
from zz91page import *
from zz91db_ast import companydb
from sphinxapi import *
from settings import spconfig,appurl
from zz91tools import getYesterday,getpastoneday

dbc=companydb()

reload(sys)
sys.setdefaultencoding('UTF-8')
nowpath=os.path.dirname(__file__)
execfile(nowpath+"/func/public_function.py")
execfile(nowpath+"/func/trade_function.py")
execfile(nowpath+"/func/qianbao_function.py")
execfile(nowpath+"/func/myrc_function.py")
execfile(nowpath+"/func/ldb_weixin_function.py")

zzq=zzqianbao()
zzms=mshop()
zzt=zztrade()
zzm=zmyrc()

#----首页
def index(request):
    host=getnowurl(request)
    company_id=request.GET.get("company_id")
    usertoken=request.GET.get("usertoken")
    appsystem=request.GET.get("appsystem")
    if not getloginstatus(company_id,usertoken):
        errlist={'tokenerr':'true'}
        return HttpResponse(simplejson.dumps(errlist, ensure_ascii=False))
    if not company_id or str(company_id)=="0":
        return HttpResponse("err")
    #----判断是否为来电宝,跳转到来电宝钱包
#    viptype=zzq.getviptype(company_id)
#    if viptype=='10051003':
#        isldb=1
#        return HttpResponseRedirect('/ldb_weixin/index.html')

    #----第一次登录钱包送20
#    getfee20=zzq.getsendfee(company_id,20,6)
    
    #outfeeall2=zzq.getoutfeeall(company_id)
    outfeeall2=0
    #----余额
    blance=zzq.getqianbaoblance(company_id)
    #----累计充值
    #infeeyd=zzq.getinfeegmt(company_id,ftype='(5)')
    infeeyd=0
    #----总进账
    #infeeall=zzq.getinfeegmt(company_id,notftype="(5)")
    infeeall=0
    #----昨日消费
    #outfeeyd=zzq.getoutfeeyd(company_id)
    outfeeyd=0
    #----总消费
    #outfeeall=zzq.getoutfeeall(company_id)
    outfeeall=0
    
    paymoney=300
    ##返回json数据
    datatype=request.GET.get("datatype")
    jsonlist={'blance':blance,'infeeyd':infeeyd,'infeeyd':infeeyd,'infeeall':infeeall,'outfeeyd':outfeeyd,'outfeeall':outfeeall}
    return HttpResponse(simplejson.dumps(jsonlist, ensure_ascii=False))
    return render_to_response('qianbao/index.html',locals())
#进账接口
def sendfee(request):
    company_id=request.GET.get("company_id")
    usertoken=request.GET.get("usertoken")
    if not getloginstatus(company_id,usertoken):
        errlist={'tokenerr':'true'}
        return HttpResponse(simplejson.dumps(errlist, ensure_ascii=False))
    if not company_id or str(company_id)=="0":
        return HttpResponse("err")
    ftype=request.GET.get('ftype')
    fee=request.GET.get('fee')
    more=request.GET.get('more')
    zzq.getsendfee(company_id,fee,ftype,more=more)
    return HttpResponse(company_id)
#出账扣费
def payfee(request):
    company_id=request.GET.get("company_id")
    usertoken=request.GET.get("usertoken")
    if not getloginstatus(company_id,usertoken):
        errlist={'tokenerr':'true'}
        return HttpResponse(simplejson.dumps(errlist, ensure_ascii=False))
    if not company_id or str(company_id)=="0":
        return HttpResponse("err")
    ftype=request.GET.get('ftype')
    fee=request.GET.get('fee')
    more=request.GET.get('more')
    result=zzq.getpayfee(company_id=company_id,ftype=ftype,more=more)
    return HttpResponse(result)
#充值卡使用
def voucherused(request):
    company_id=request.GET.get("company_id")
    usertoken=request.GET.get("usertoken")
    if not getloginstatus(company_id,usertoken):
        errlist={'tokenerr':'true'}
        return HttpResponse(simplejson.dumps(errlist, ensure_ascii=False))
    if not company_id or str(company_id)=="0":
        return HttpResponse("err")
    
    vid=request.GET.get('vid')
    jsonlist={'err':'true'}
    sql="select fee from shop_voucher where id=%s and used_id=0 and DATEDIFF(end_time,CURDATE())>=0"
    result=dbc.fetchonedb(sql,[vid])
    if result:
        fee=result[0]
        ftype=8
        more="1"
        zzq.getsendfee(company_id,fee,ftype,more=more)
        sql="update shop_voucher set used_id=1 where id=%s"
        dbc.updatetodb(sql,[vid])
        jsonlist={'err':'false'}
    return HttpResponse(simplejson.dumps(jsonlist, ensure_ascii=False))

def zhangdannore(request):
    
    timarg=request.GET.get('timarg')
    page=request.GET.get('page')
    if page:
        page=int(page)
    else:
        page=1
    company_id=request.GET.get("company_id")
    usertoken=request.GET.get("usertoken")
    appsystem=request.GET.get("appsystem")
    if not getloginstatus(company_id,usertoken):
        errlist={'tokenerr':'true'}
        return HttpResponse(simplejson.dumps(errlist, ensure_ascii=False))
    if not company_id or str(company_id)=="0":
        return HttpResponse("err")
    payfeelist=zzq.getpayfeelist(company_id,(page-1)*10,10,timarg)
    listall=payfeelist['list']
    #返回json数据
    datatype=request.GET.get("datatype")
    if datatype=="json":
        return HttpResponse(simplejson.dumps(payfeelist, ensure_ascii=False))
    return render_to_response('qianbao/zhangdannore.html',locals())

#----账单
def zhangdan(request):
    #host=getnowurl(request)
    #backurl=request.META.get('HTTP_REFERER','/')
    company_id=request.GET.get("company_id")
    usertoken=request.GET.get("usertoken")
    appsystem=request.GET.get("appsystem")
    if not getloginstatus(company_id,usertoken):
        errlist={'tokenerr':'true'}
        return HttpResponse(simplejson.dumps(errlist, ensure_ascii=False))
    if not company_id or str(company_id)=="0":
        return HttpResponse("err")
    timarg=request.GET.get('timarg')
    page=request.GET.get('page')
    if page:
        page=int(page)
    else:
        page=1
    payfeelist=zzq.getpayfeelist(company_id,(page-1)*20,20,timarg)
    listall=payfeelist['list']
    count=payfeelist['count']
    gmtdate=time.strftime('%Y-%m-01 00:00:',time.localtime(time.time()))
    #----本月进账
    infeegmtnowmonth=zzq.getinfeegmt(company_id,notftype="(5)")
    #----本月消费
    outfeegmtnowmonth=zzq.getoutfeegmt(company_id)
    #----本月充值
    outfee5gmtnowmonth=zzq.getinfeegmt(company_id,ftype='(5)')
    
    #返回json数据
    datatype=request.GET.get("datatype")
    if datatype=="json":
        jsonlist={'infeegmtnowmonth':infeegmtnowmonth,'outfeegmtnowmonth':outfeegmtnowmonth,'outfee5gmtnowmonth':outfee5gmtnowmonth,'payfeelist':payfeelist}
        return HttpResponse(simplejson.dumps(jsonlist, ensure_ascii=False))
    return render_to_response('qianbao/zhangdan.html',locals())
#----充值
def chongzhi(request):
    #backurl=request.META.get('HTTP_REFERER','/')
    #host=getnowurl(request)
    company_id=request.GET.get("company_id")
    usertoken=request.GET.get("usertoken")
    appsystem=request.GET.get("appsystem")
    if not getloginstatus(company_id,usertoken):
        errlist={'tokenerr':'true'}
        return HttpResponse(simplejson.dumps(errlist, ensure_ascii=False))
    if not company_id or str(company_id)=="0":
        return HttpResponse("err")
    appsystem=request.GET.get("appsystem")
    paytype=request.GET.get("paytype")
    userimei=request.GET.get("userimei")
    isios=None
    if (appsystem=="iOS"):
        isios=1
    backurl="http://app.zz91.com/qianbao/chongzhisuc.html"
    companycontact=zzq.getcompanycontact(company_id)
    mobile=companycontact['mobile']
    contact=companycontact['contact']
    #4-1号调价
    paymoney=300
    #返回json数据
    datatype=request.GET.get("datatype")
    if datatype=="json":
        jsonlist={'paytype':paytype,'companycontact':companycontact,'backurl':backurl,'company_id':company_id}
        return HttpResponse(simplejson.dumps(jsonlist, ensure_ascii=False))
    return render_to_response('qianbao/chongzhi.html',locals())
#新版app充值
def chongzhi_new(request):
    company_id=request.GET.get("company_id")
    usertoken=request.GET.get("usertoken")
    if not getloginstatus(company_id,usertoken):
        errlist={'tokenerr':'true'}
        return HttpResponse(simplejson.dumps(errlist, ensure_ascii=False))
    appsystem=request.GET.get("appsystem")
    paytype=request.GET.get("paytype")
    userimei=request.GET.get("userimei")
    backurl="http://app.zz91.com/qianbao/chongzhisuc.html"
    companycontact=zzq.getcompanycontact(company_id)
    mobile=companycontact['mobile']
    contact=companycontact['contact']
    #4-1号调价
    paymoney=300
    #返回json数据
    datatype=request.GET.get("datatype")
    if datatype=="json":
        jsonlist={'paytype':paytype,'mobile':mobile,'contact':contact,'backurl':backurl,'company_id':company_id}
        return HttpResponse(simplejson.dumps(jsonlist, ensure_ascii=False))
    return render_to_response('qianbao/chongzhi_new.html',locals())
def chongzhisuc(request):
    return render_to_response('qianbao/chongzhisuc.html',locals())
#----进账说明
def intxt(request):
    backurl=request.META.get('HTTP_REFERER','/')
    listall=zzq.getftypelist("23")
    return render_to_response('qianbao/intxt.html',locals())
#----消费说明
def outtxt(request):
    backurl=request.META.get('HTTP_REFERER','/')
    return render_to_response('qianbao/outtxt.html',locals())
#----商城
def shop(request):
    company_id=request.GET.get("company_id")
    usertoken=request.GET.get("usertoken")
    appsystem=request.GET.get("appsystem")
    if not getloginstatus(company_id,usertoken):
        errlist={'tokenerr':'true'}
        return HttpResponse(simplejson.dumps(errlist, ensure_ascii=False))
    if not company_id or str(company_id)=="0":
        return HttpResponse("err")
    backurl=request.META.get('HTTP_REFERER','/')
    host=getnowurl(request)
    #listall=zzm.getmyproductslist(frompageCount=0,limitNum=1,company_id=company_id)
    #offerlist=listall['list']
    #if offerlist:
    #    offid1=offerlist[0]['proid']
    #----获取用户余额
    qianbaoblance=zzq.getqianbaoblance2(company_id)
    #----判断是否在微信推广中
    gmt_created=datetime.datetime.now()
#    is_wxtg=zzms.getis_wxtg(company_id,gmt_created,paytype=10)
    is_wxtg=''
    return render_to_response('qianbao/shop.html',locals())
#----商城简介
def simptxt(request):
    backurl=request.META.get('HTTP_REFERER','/')
    host=getnowurl(request)
    company_id=request.GET.get("company_id")
    return render_to_response('qianbao/simptxt.html',locals())
def oflist(request):
    host=getnowurl(request)
    company_id=request.GET.get("company_id")
    usertoken=request.GET.get("usertoken")
    if not getloginstatus(company_id,usertoken):
        errlist={'tokenerr':'true'}
        return HttpResponse(simplejson.dumps(errlist, ensure_ascii=False))
    if not company_id or str(company_id)=="0":
        return HttpResponse("err")
    limitNum=7
    listall=zzm.getmyproductslist(frompageCount=0,limitNum=limitNum,company_id=company_id)
    count=listall['count']
    offerlist=listall['list']
#    if offerlist:
#        offid1=offerlist[0]['id']
    #返回json数据
    datatype=request.GET.get("datatype")
    if datatype=="json":
        return HttpResponse(simplejson.dumps(listall, ensure_ascii=False))
    return render_to_response('qianbao/oflist.html',locals())
def offmore(request):
    company_id=request.GET.get("company_id")
    usertoken=request.GET.get("usertoken")
    if not getloginstatus(company_id,usertoken):
        errlist={'tokenerr':'true'}
        return HttpResponse(simplejson.dumps(errlist, ensure_ascii=False))
    if not company_id or str(company_id)=="0":
        return HttpResponse("err")
    if company_id:
        page=request.GET.get('page')
        if page:
            page=int(page)
        else:
            page=1
        limitNum=7
        listall=zzm.getmyproductslist(frompageCount=(page-1)*limitNum,limitNum=limitNum,company_id=company_id)
        offerlist=listall['list']
        #返回json数据
        datatype=request.GET.get("datatype")
        if datatype=="json":
            return HttpResponse(simplejson.dumps(offerlist, ensure_ascii=False))
        return render_to_response('qianbao/offmore.html',locals())
#支付宝支付
def zz91pay(request):
    company_id=request.GET.get("company_id")
    usertoken=request.GET.get("usertoken")
    if not getloginstatus(company_id,usertoken):
        errlist={'tokenerr':'true'}
        return HttpResponse(simplejson.dumps(errlist, ensure_ascii=False))
    appsystem=request.GET.get("appsystem")
    #if not getloginstatus(company_id,usertoken):
    #    return HttpResponse("nologin")
    companycontact=zzq.getcompanycontact(company_id)
    mobile=companycontact['mobile']
    contact=companycontact['contact']
    
    user_ip=getIPFromDJangoRequest(request)
    if not user_ip:
        user_ip="0.0.0.0"
    if user_ip:
        user_ipa=user_ip.split(",")
        user_ip=user_ipa[0]
    #user_ip="127.0.0.1"
    total_fee = request.GET.get('total_fee')
    paytype=request.GET.get("paytype")
    subject = request.GET.get('subject')
    payflag=request.GET.get("payflag")
    if payflag:
        subject=subject+"("+str(payflag)+")"
    relfee=total_fee
    #relfee=float(total_fee)/100
    total_fee=float(total_fee)*100
    todate=datetime.datetime.now()
    today=todate.strftime('%Y%m%d')
    t=random.randrange(100000,999999)
    out_trade_no=str(today)+str(t)
    is_success="F"
    payreturn_url="http://app.zz91.com/qianbao/chongzhisuc.html"
    #中断返回
    merchant_url="http://app.zz91.com/qianbao/chongzhi_new.html"
    #total_fee=0.1
    gmt_created=datetime.datetime.now()
    
    valu=[out_trade_no,subject,relfee,contact,mobile,is_success,payreturn_url,paytype,company_id,gmt_created]
    sql="insert into pay_order(out_trade_no,subject,total_fee,contact,mobile,is_success,payreturn_url,paytype,company_id,gmt_created) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
    dbc.updatetodb(sql,valu)
    
    
    #payload={'out_trade_no':out_trade_no,'subject':subject,'total_fee':total_fee,'merchant_url':merchant_url}
    #r= requests.post("http://www.zz91.com/zzpay/alipay/alipayapi.jsp",data=payload)
    #r= requests.post("http://phppay.zz91.com/alipay/alipayapi.php",data=payload)
    #return HttpResponse(r.content)

    payload={'order_id':out_trade_no,'identity_id':out_trade_no,'product_name':subject,'product_desc':'','amount':total_fee,'merchant_url':merchant_url,'user_ip':user_ip,'relfee':relfee}
    #yeeurl=urllib.urlencode(payload)
    #payload['yeeurl']=yeeurl
    #返回json数据
    datatype=request.GET.get("datatype")
    if datatype=="json":
        return HttpResponse(simplejson.dumps(payload, ensure_ascii=False))
def zz91paysubmit(request):
    out_trade_no=request.GET.get("out_trade_no")
    total_fee=request.GET.get("total_fee")
    subject=request.GET.get("subject")
    #subject="手机钱包充值"
    merchant_url="http://m.zz91.com/qianbao/"
    
    payload={'out_trade_no':out_trade_no,'subject':subject,'total_fee':total_fee,'merchant_url':merchant_url}
    #payload=simplejson.dumps(payload, ensure_ascii=False)
    #return HttpResponse(payload)
    r= requests.post("http://www.zz91.com/pay/alipayapi.jsp",data=payload)
    return HttpResponse(r.content)
def zz91payrequery(request):
    requestlist='seller_id="zhifu@asto-inc.com"&partner="2088511051388426"&out_trade_no="20141018140245"&subject="DCloud项目捐赠"&body="DCloud致力于打造HTML5最好的移动开发工具，包括终端的Runtime、云端的服务和IDE，同时提供各项配套的开发者服务。"&total_fee="10"&_input_charset="UTF-8"&service="mobile.securitypay.pay"&payment_type="1"&quantity="1"&it_b_pay="1d"&show_url="http://demo.dcloud.net.cn/helloh5/payment/"&return_url="http://demo.dcloud.net.cn/helloh5/payment/"&notify_url="http://demo.dcloud.net.cn/helloh5/payment/"&sign="Cw3mklTi9ZJVsVDdcPvm4TtOEcBFM0fiTAvt%2FJgo58QfWpa8eNqWCElE18TT3OivwLd%2BRL%2FrL9IW1VSF3WnlOc2vzUX4fhQg0rPBya8Bgu4%2BeEsSWU1oFOzz%2BBnmSAkcqLBv4i%2Fi2E4qajFkTMXS0jouN05GchOXkVGL%2FMnz8gw%3D"&sign_type="RSA"'
    return HttpResponse(requestlist)

#服务开通
def openservice(request):
    company_id=request.GET.get("company_id")
    usertoken=request.GET.get("usertoken")
    opentype=request.GET.get("opentype")
    if not getloginstatus(company_id,usertoken):
        errlist={'tokenerr':'true'}
        return HttpResponse(simplejson.dumps(errlist, ensure_ascii=False))
    #开通显示联系方式
    if opentype=="showcontact":
        datevalue=request.GET.get("datevalue")
        zzq.buyshowcontact(company_id,None,datevalue=datevalue)
    #开通供求自动刷新
    if opentype=="proreflush":
        datevalue=request.GET.get("datevalue")
        zzq.buyreflushtrade(company_id,-int(datevalue))
    jsonlist={'err':'false'}
    return HttpResponse(simplejson.dumps(jsonlist, ensure_ascii=False))
#在线商城
def qianbaopay(request):
    company_id=request.GET.get("company_id")
    usertoken=request.GET.get("usertoken")
    if not getloginstatus(company_id,usertoken):
        errlist={'tokenerr':'true'}
        return HttpResponse(simplejson.dumps(errlist, ensure_ascii=False))
    errflag='true'
    errtext='系统错误'
    blanceflag='1'
    if not company_id or str(company_id)=="0":
        errflag='true'
        errtext='未登录，请重新登录！'
    jsonlist={'err':errflag,'errtext':errtext,'blanceflag':blanceflag}
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
    
    return HttpResponse(simplejson.dumps(jsonlist, ensure_ascii=False))

def qianbaopaysave(company_id="",paytype="",money="",proid="",mobile="",baoming="",voucher_id="",datevalue="",request=""):
    errflag='true'
    errtext='系统错误'
    blanceflag='1'
    jsonlist={'err':errflag,'errtext':errtext,'blanceflag':blanceflag}
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
    elif paytype in ('20','40','41','62'):
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
    jsonlist={'err':errflag,'errtext':errtext,'blanceflag':blanceflag}
    return jsonlist
#钱包余额
def qianbaobaoblance(request):
    company_id=request.GET.get("company_id")
    usertoken=request.GET.get("usertoken")
    if not getloginstatus(company_id,usertoken):
        errlist={'tokenerr':'true'}
        return HttpResponse(simplejson.dumps(errlist, ensure_ascii=False))
    baoblance=0
    if company_id:
        baoblance=zzq.getqianbaoblance(company_id)
        showphone=zzq.getisbuyshowphone(company_id)
        if not showphone:
            showphone=zzq.getiszstcompany(company_id)
        jsonlist={'blance':baoblance,'showphone':showphone}
    return HttpResponse(simplejson.dumps(jsonlist, ensure_ascii=False))

#抢购页面
def qg(request):
    gid=request.GET.get("gid")
    company_id=request.GET.get("company_id")
    usertoken=request.GET.get("usertoken")
    appsystem=request.GET.get("appsystem")
    if not getloginstatus(company_id,usertoken) and appsystem=="Android":
        return HttpResponse("nologin")
    if not company_id or str(company_id)=="0":
        return HttpResponse("err")
    list=zzq.getadgoods(gid=gid)
    if list:
        paytype=list['billing_Class_ID']
        paymoney=zzq.getpay_wallettypefee(list['billing_Class_ID'])
    qianbaoblance=zzq.getqianbaoblance(company_id)
    #返回json数据
    datatype=request.GET.get("datatype")
    if datatype=="json":
        jsonlist={'list':list,'paytype':paytype,'paymoney':paymoney,'qianbaoblance':qianbaoblance}
        return HttpResponse(simplejson.dumps(jsonlist, ensure_ascii=False))
    return render_to_response('qianbao/qg.html',locals())
def qg_tourl(request):
    gid=request.GET.get("gid")
    if gid[0:1]=="p":
        return HttpResponseRedirect("/detail/?id="+str(gid[1:len(gid)]))
    list=zzq.getadgoods(gid=gid)
    tourl=list['tourl']
    return HttpResponseRedirect(tourl)
#签到
def qiandao(request):
    company_id=request.GET.get("company_id")
    usertoken=request.GET.get("usertoken")
    if not getloginstatus(company_id,usertoken):
        errlist={'tokenerr':'true'}
        return HttpResponse(simplejson.dumps(errlist, ensure_ascii=False))
    """
    usertoken=request.GET.get("usertoken")
    appsystem=request.GET.get("appsystem")
    if not getloginstatus(company_id,usertoken):
        return HttpResponse("nologin")
    if not company_id or str(company_id)=="0":
        return HttpResponse("err")
    """
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
#我 的服务
def myservice(request):
    company_id=request.GET.get("company_id")
    usertoken=request.GET.get("usertoken")
    if not getloginstatus(company_id,usertoken):
        errlist={'tokenerr':'true'}
        return HttpResponse(simplejson.dumps(errlist, ensure_ascii=False))
    appsystem=request.GET.get("appsystem")
    #if not getloginstatus(company_id,usertoken):
        #return HttpResponse("nologin")
    sql="select a.name,c.gmt_signed,c.gmt_start,c.gmt_end,c.zst_year,b.amount,b.sale_staff,b.remark,c.crm_service_code,c.apply_status,DATEDIFF(c.gmt_end,CURDATE()) from crm_company_service as c left join crm_service as a on a.code=c.crm_service_code left OUTER join crm_service_apply as b on b.apply_group=c.apply_group where c.company_id=%s and c.apply_status!='2' and c.gmt_start is not null  order by c.gmt_start desc"
    complist=dbc.fetchalldb(sql,[company_id])
    listall=[]
    for a in complist:
        amount=a[5]
        crm_service_code=a[8]
        apply_status=a[9]
        gmt_diff=a[10]
        apply_statustext=""
        if str(apply_status)=="0":
            apply_statustext="<font color=blue>待开通</font>"
        if str(apply_status)=="1":
            apply_statustext="<font color=gree>已开通</font>"
        if str(apply_status)=="2":
            apply_statustext="<font color=#ff0>拒绝开通</font>"
        if gmt_diff<0:
            apply_statustext="已过期"
        list={'servername':a[0],'status':apply_statustext,'gmt_begin':formattime(a[2],1),'gmt_end':formattime(a[3],1),'type':'zst'}
        listall.append(list)
    
    #标王
    sql="select '标王',a.is_checked,a.start_time,a.end_time,a.name,DATEDIFF(a.end_time,CURDATE())  from products_keywords_rank as a where a.company_id=%s and a.end_time is not null"
    adslist=dbc.fetchalldb(sql,[company_id])
    for a in adslist:
        is_checked=a[1]
        if (str(is_checked)=='1'):
            is_checked="<font color=gree>已开通</font>"
        else:
            is_checked="<font color=blue>未审核</font>"
        gmt_diff=a[5]
        if gmt_diff<0:
            is_checked="已过期"
        list={'servername':'标王','status':is_checked,'gmt_begin':formattime(a[2],1),'gmt_end':formattime(a[3],1),'keywords':a[4],'type':'keytop'}
        listall.append(list)
    
    #显示联系方式    
    sql="select gmt_begin,gmt_end,DATEDIFF(gmt_end,CURDATE()) from shop_showphone where company_id=%s"
    alist=dbc.fetchalldb(sql,[company_id])
    for a in alist:
        status='<font color=gree>已开通</font>'
        gmt_diff=a[2]
        if gmt_diff<0:
            status="已过期"
        list={'servername':'显示联系方式','status':status,'gmt_begin':formattime(a[0],1),'gmt_end':formattime(a[1],1),'type':'showphone'}
        listall.append(list)
    #定时自动刷新    
    sql="select gmt_begin,gmt_end,DATEDIFF(gmt_end,CURDATE()) from shop_reflush where company_id=%s and gmt_end is not null"
    alist=dbc.fetchalldb(sql,[company_id])
    for a in alist:
        status='<font color=gree>已开通</font>'
        gmt_diff=a[2]
        if gmt_diff<0:
            status="已过期"
        list={'servername':'供求自动刷新','status':status,'gmt_begin':formattime(a[0],1),'gmt_end':formattime(a[1],1),'type':'autoreflush'}
        listall.append(list)
    #竞价排名，流量宝    
    sql="select id,gmt_created,checked from app_jingjia_keywords where company_id=%s"
    alist=dbc.fetchonedb(sql,[company_id])
    if alist:
        status='<font color=gree>已开通</font>'
        gmt_created=formattime(alist[1],1)
        list={'servername':'流量宝','status':status,'gmt_begin':gmt_created,'gmt_end':'','type':'llb','surl':'/qianbao/jingjia_index.html'}
        listall.append(list)
    return HttpResponse(simplejson.dumps(listall, ensure_ascii=False))
#优惠活动
def youhuilist(request):
    page=request.GET.get('page')
    ptype=request.GET.get('ptype')
    goodsNmae=request.GET.get('goodsNmae')
    ad_type=request.GET.get('ad_type')
    searchlist={}
    if ptype:
        searchlist['ptype']=ptype
    if goodsNmae:
        searchlist['goodsNmae']=goodsNmae
    if ad_type:
        searchlist['ad_type']=ad_type
    searchurl=urllib.urlencode(searchlist)
    if not page:
        page=1
    funpage=zz91page()
    limitNum=funpage.limitNum(20)
    nowpage=funpage.nowpage(int(page))
    frompageCount=funpage.frompageCount()
    after_range_num = funpage.after_range_num(3)
    before_range_num = funpage.before_range_num(6)
    messagelist=zzq.listgoods(frompageCount,limitNum,ptype=ptype,goodsNmae=goodsNmae,ad_type=ad_type)
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
    return HttpResponse(simplejson.dumps({'list':listall,'pagecount':page_listcount}, ensure_ascii=False))
#我的代金券
def mydaijinquan(request):
    company_id=request.GET.get("company_id")
    usertoken=request.GET.get("usertoken")
    qtype_id=request.GET.get("qtype_id")
    if not getloginstatus(company_id,usertoken):
        errlist={'tokenerr':'true'}
        return HttpResponse(simplejson.dumps(errlist, ensure_ascii=False))
    appsystem=request.GET.get("appsystem")
    if company_id:
        sql="select title,qcode,id,fee,used_id,begin_time,end_time,qtype_id from shop_voucher where company_id=%s and qtype_id=%s and used_id=0 and DATEDIFF(end_time,CURDATE())>=0 limit 0,10"
        result=dbc.fetchalldb(sql,[company_id,qtype_id])
        listall=[]
        if result:
            for list in result:
                if list[4]==1:
                    usedtext="已使用"
                else:
                    usedtext="未使用"
                l={'title':list[0],'qcode':list[1],'id':list[2],'fee':list[3],'used_id':list[4],'usedtext':usedtext,'qtype_id':list[7],'begin_time':formattime(list[5],1),'end_time':formattime(list[6],1)}
                listall.append(l)
    return HttpResponse(simplejson.dumps(listall, ensure_ascii=False))
#我的代金券
def mydaijinquanlist(request):
    company_id=request.GET.get("company_id")
    usertoken=request.GET.get("usertoken")
    if not getloginstatus(company_id,usertoken):
        errlist={'tokenerr':'true'}
        return HttpResponse(simplejson.dumps(errlist, ensure_ascii=False))
    appsystem=request.GET.get("appsystem")
    if company_id:
        sql="select title,qcode,id,fee,used_id,begin_time,end_time,qtype_id from shop_voucher where company_id=%s"
        sql+=" limit 0,50"
        result=dbc.fetchalldb(sql,[company_id])
        listall=[]
        if result:
            for list in result:
                if list[4]==1:
                    usedtext="已使用"
                else:
                    usedtext="未使用"
                l={'title':list[0],'qcode':list[1],'id':list[2],'fee':list[3],'used_id':list[4],'usedtext':usedtext,'qtype_id':list[7],'begin_time':formattime(list[5],1),'end_time':formattime(list[6],1)}
                listall.append(l)
    return HttpResponse(simplejson.dumps(listall, ensure_ascii=False))
#竞价最低价，充值最低
def jingjia_info(request):
    res={'maxprice':5,'minblance':300}
    return HttpResponse(simplejson.dumps(res, ensure_ascii=False))
#关键字竞价排名保存
def jingjia_keywords_save(request):
    company_id=request.POST.get("company_id")
    usertoken=request.POST.get("usertoken")
    if not getloginstatus(company_id,usertoken):
        errlist={'tokenerr':'true'}
        return HttpResponse(simplejson.dumps(errlist, ensure_ascii=False))
    appsystem=request.POST.get("appsystem")
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
    sql="select company_id,price,product_id from app_jingjia_keywords where id=%s"
    result=dbc.fetchonedb(sql,[key_id])
    if result:
        forcompany_id=result[0]
        price=result[1]
        product_id=result[2]
        sourcetype=1
        user_company_id=company_id
        #供求未审核不计费
        sqlp="select check_status from products where id=%s"
        resultp=dbc.fetchonedb(sqlp,[product_id])
        if resultp:
            check_status=resultp[0]
        if str(check_status)!="2":
            if int(company_id)!=int(forcompany_id):
                gmt_created=datetime.datetime.now()
                sqlc="select id from app_jingjia_click where key_id=%s and userid=%s"
                res=dbc.fetchonedb(sqlc,[key_id,userid])
                if not res:
                    clickcount=1
                    sqld="insert into app_jingjia_click(key_id,search_id,price,clickcount,sourcetype,userid,user_company_id,company_id,area,gmt_created) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
                    dbc.updatetodb(sqld,[key_id,search_id,price,clickcount,sourcetype,userid,user_company_id,forcompany_id,area,gmt_created])
                    #扣款
                    zzq.getpayfee(company_id=forcompany_id,forcompany_id=company_id,product_id=search_id,ftype=55,fee=-int(price))
                else:
                    sqld="update app_jingjia_click set clickcount=clickcount+1 where id=%s"
                    dbc.updatetodb(sqld,[res[0]])
    resjson={'err':'false','errkey':''}
    return HttpResponse(simplejson.dumps(resjson, ensure_ascii=False))
            
#我的竞价推广
def jingjia_index(request):
    company_id=request.POST.get("company_id")
    usertoken=request.POST.get("usertoken")
    if not getloginstatus(company_id,usertoken):
        errlist={'tokenerr':'true'}
        return HttpResponse(simplejson.dumps(errlist, ensure_ascii=False))
    sql="select sum(showcount>0),sum(clickcount>0) from app_jingjia_search where company_id=%s"
    result=dbc.fetchonedb(sql,[company_id])
    showcount=0
    clickcount=0
    if result:
        showcount=result[0]
        if not showcount:
            showcount=0
    
    sql="select sum(clickcount) from app_jingjia_click where company_id=%s"
    result=dbc.fetchonedb(sql,[company_id])
    if result:
        clickcount=result[0]
    else:
        clickcount=0
    if not clickcount:
        clickcount=0
        
    sqlk="select sum(fee) from pay_mobilewallet where company_id=%s and ftype=%s"
    result=dbc.fetchonedb(sqlk,[company_id,55])
    pricecount=0
    if result:
        pricecount=result[0]
    if not pricecount:
        pricecount=0
        
    phonecount=0
    sql="select count(0) from phone_telclick_log where forcompany_id=%s"
    result=dbc.fetchonedb(sql,[company_id])
    if result:
        phonecount=result[0]
        if not phonecount:
            phonecount=0
    #钱包余额
    blance=zzq.getqianbaoblance(company_id,jingjia=1)
    
    tjlist={'showcount':showcount,'clickcount':clickcount,'pricecount':pricecount,'phonecount':phonecount}
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
        
        
        ll={'key_id':key_id,'keywords':keywords,'key_showcount':key_showcount,'key_clickcount':key_clickcount,'key_pricecount':key_pricecount,'checktext':checktext}
        keylist.append(ll)
    reslist={'tjlist':tjlist,'keylist':keylist,'blance':blance}
    return HttpResponse(simplejson.dumps(reslist, ensure_ascii=False))
#关键词信息
def jingjia_keywords_info(request):
    company_id=request.POST.get("company_id")
    usertoken=request.POST.get("usertoken")
    if not getloginstatus(company_id,usertoken):
        errlist={'tokenerr':'true'}
        return HttpResponse(simplejson.dumps(errlist, ensure_ascii=False))
    key_id=request.POST.get("key_id")
    list=None
    if key_id:
        sql="select keywords,price,checked from app_jingjia_keywords where id=%s"
        result=dbc.fetchonedb(sql,[key_id])
        if result:
            keywords=result[0]
            price=result[1]
            checked=result[2]
            list={'keywords':keywords,'price':price,'checked':checked}
    return HttpResponse(simplejson.dumps(list, ensure_ascii=False))

#保存关键词，出价
def jingjia_keywords_onesave(request):
    company_id=request.POST.get("company_id")
    usertoken=request.POST.get("usertoken")
    if not getloginstatus(company_id,usertoken):
        errlist={'tokenerr':'true'}
        return HttpResponse(simplejson.dumps(errlist, ensure_ascii=False))
    key_id=request.POST.get("key_id")
    keywords=request.POST.get("keywords")
    price=request.POST.get("price")
    sql="update app_jingjia_keywords set keywords=%s,price=%s where id=%s"
    dbc.updatetodb(sql,[keywords,price,key_id])
    resjson={'err':'false','errkey':''}
    return HttpResponse(simplejson.dumps(resjson, ensure_ascii=False))
#关键词下线
def jingjia_keywords_offline(request):
    company_id=request.POST.get("company_id")
    usertoken=request.POST.get("usertoken")
    if not getloginstatus(company_id,usertoken):
        errlist={'tokenerr':'true'}
        return HttpResponse(simplejson.dumps(errlist, ensure_ascii=False))
    key_id=request.POST.get("key_id")
    checked=request.POST.get("checked")
    if not checked:
        checked=0
    sql="update app_jingjia_keywords set checked=%s where id=%s"
    dbc.updatetodb(sql,[checked,key_id])
    resjson={'err':'false','errkey':''}
    return HttpResponse(simplejson.dumps(resjson, ensure_ascii=False))
#我的关键词消费明细
def jingjia_keywords_paylist(request):
    page=request.GET.get('page')
    company_id=request.GET.get("company_id")
    usertoken=request.GET.get("usertoken")
    if not getloginstatus(company_id,usertoken):
        errlist={'tokenerr':'true'}
        return HttpResponse(simplejson.dumps(errlist, ensure_ascii=False))
    if not page:
        page=1
    funpage=zz91page()
    limitNum=funpage.limitNum(20)
    nowpage=funpage.nowpage(int(page))
    frompageCount=funpage.frompageCount()
    after_range_num = funpage.after_range_num(3)
    before_range_num = funpage.before_range_num(6)
    key_id=request.GET.get("key_id")
    datekey=request.GET.get("datekey")
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
    return HttpResponse(simplejson.dumps({'list':listall,'pagecount':page_listcount,'keylist':keylist,'sql':messagelist['sql']}, ensure_ascii=False))
#用户点击明细
def jingjia_keywords_clicklist(request):
    page=request.GET.get('page')
    company_id=request.GET.get("company_id")
    usertoken=request.GET.get("usertoken")
    if not getloginstatus(company_id,usertoken):
        errlist={'tokenerr':'true'}
        return HttpResponse(simplejson.dumps(errlist, ensure_ascii=False))
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
    return HttpResponse(simplejson.dumps({'list':listall,'pagecount':page_listcount,'keylist':keylist}, ensure_ascii=False))