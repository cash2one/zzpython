#-*- coding:utf-8 -*-

from django.shortcuts import render_to_response
from django.http import HttpResponse,HttpResponseRedirect,HttpResponsePermanentRedirect
import MySQLdb,sys,os,memcache,settings,urllib,re,time,datetime,requests,random,string,md5,hashlib
from django.core.cache import cache
from sphinxapi import *
from zz91page import *
from settings import spconfig
from zz91settings import SPHINXCONFIG
from commfunction import filter_tags,formattime,havepicflag,subString,getjiami,getIPFromDJangoRequest,validateEmail
from function import getnowurl,getbbslist
from zz91tools import int_to_str
from datetime import timedelta, date 
from zz91db_ast import companydb
from zz91db_2_news import newsdb
from zz91db_ads import adsdb
from zz91db_sms import smsdb
from zz91conn import database_mongodb
dbc=companydb()
dbn=newsdb()
dbads=adsdb()
dbsms=smsdb()
#连接loginfo集合（表）
dbmongo=database_mongodb()

reload(sys)
sys.setdefaultencoding('UTF-8')
nowpath=os.path.dirname(__file__)
execfile(nowpath+"/func/main_function.py")
execfile(nowpath+"/func/company_function.py")
execfile(nowpath+"/function.py")
#from SmsWap.SmsWap import MerchantAPI
#import SmsWap.Gl as Gl

from zzwx.client import Client
zzmain=zmain()
zzcompany=zcompany()

def closedb():
    a=1
    #dbc.closedb()
    #dbn.closedb()
    #dbads.closedb()
    #dbsms.closedb()

def index(request):
    endtime=int(time.time())
    fromtime=endtime-24*3600
    fromtime2=endtime-24*3600*7
    bbslist=zzmain.getbbslist(datetype=2,fromtime=fromtime,endtime=endtime)
    if not bbslist:
        bbslist=zzmain.getbbslist(datetype=2,fromtime=fromtime2,endtime=endtime)
    newslist=zzmain.getnewslist(limitNum=3,allnum=3)
    host=getnowurl(request)
    index=1
    webtitle="ZZ91手机站"
    username=request.session.get("username",None)
    company_id=request.session.get("company_id",None)
    categorycodelist=zzmain.getindexcategorylist('1000',1)
    if (str(username)=="None"):
        username=""
    #广告
    adlist=zzmain.getadlistall(722)
    closedb()
    return render_to_response('2016new/index/index.html',locals())

def guanggao(request):
    #----一个ip只弹一次广告type=1手机钱包送20活动广告
    if request.META.has_key('HTTP_X_FORWARDED_FOR'):
        ip =  request.META['HTTP_X_FORWARDED_FOR']
    else:
        ip = request.META['REMOTE_ADDR']
    sql='select id from mobile_ip_visit where ip=%s and type=1'
    result=dbc.fetchonedb(sql,[ip])
    if not result:
        gmt_date=datetime.date.today()
        gmt_created=datetime.datetime.now()
        sql2='insert into mobile_ip_visit(ip,type,gmt_date,gmt_created) values(%s,%s,%s,%s)'
        dbc.updatetodb(sql2,[ip,1,gmt_date,gmt_created])
        closedb()
        return HttpResponse('1')
    else:
        closedb()
        #return render_to_response('main/guanggao.html',locals())
        return HttpResponse('0')
def test(request):
    #return render_to_response('zz91weixin/test.html',locals())
    client = Client("wx2891ef70c5a770d6", "d3f9436cfc50cd9e4f62f96893a1ee0c")
    
    signlist=client.get_sign()
    timestamp=signlist['timestamp']
    nonceStr=signlist['nonceStr']
    signature=signlist['signature']
    jsapi_ticket=signlist['jsapi_ticket']
    return render_to_response('main/test3.html',locals())
def app(request):
    closedb()
    return render_to_response('app/appdownload.html',locals())
#查看邀请码
def invitesee(request,mcode=''):
    webtitle="分享邀请码"
    showpost="1"
    showgooglead=1
    nowlanmu="<a href='/invite/help.html'>分享邀请码</a>"
    code=str(random.randint(100000, 999999))
    sql='select id,code from app_invite where jiamicompanyid=%s'
    result=dbc.fetchonedb(sql,[mcode])
    if result:
        code=result[1]
    else:
        gmt_created=datetime.datetime.now()
        sql2='insert into app_invite(company_id,code,gmt_created,jiamicompanyid) values(%s,%s,%s,%s)'
        dbc.updatetodb(sql2,[company_id,code,gmt_created,mcode])
    title="使用我的ZZ91再生网邀请码“"+str(code)+"”,即可获得获取20元再生钱包。"
    closedb()
    return render_to_response('invite/invite.html',locals())
#分享邀请码
def invite(request,mcode=''):
    webtitle="分享邀请码"
    showpost="1"
    showgooglead=1
    nowlanmu="<a href='/invite/help.html'>分享邀请码</a>"
    company_id=request.session.get("company_id",None)
    
    username=request.session.get("username",None)
    if ((company_id==None or str(company_id)=="0")):
        return HttpResponseRedirect("/login/?done=/invite/invite.html")
    
    md5companyid = hashlib.md5(username+str(company_id))
    md5companyid = md5companyid.hexdigest()[8:-8]
    if (mcode==md5companyid):
        code=str(random.randint(100000, 999999))
        sql='select id,code from app_invite where company_id=%s'
        result=dbc.fetchonedb(sql,[company_id])
        if result:
            code=result[1]
            sql2="update app_invite set jiamicompanyid=%s where company_id=%s"
            dbc.updatetodb(sql2,[md5companyid,company_id])
        else:
            gmt_created=datetime.datetime.now()
            sql2='insert into app_invite(company_id,code,gmt_created,jiamicompanyid) values(%s,%s,%s,%s)'
            dbc.updatetodb(sql2,[company_id,code,gmt_created,mcode])
        title="使用我的ZZ91再生网邀请码“"+str(code)+"”,即可获得获取20元再生钱包。"
        closedb()
        return render_to_response('invite/invite.html',locals())
    else:
        closedb()
        return HttpResponse("error!")
#分享码查看帮助
def invitehelp(request,code=""):
    webtitle="邀请码"
    showpost="1"
    showgooglead=1
    nowlanmu="<a href='/invite/help.html'>邀请码</a>"
    company_id=request.session.get("company_id",None)
    username=request.session.get("username",None)
    if not code:
        code=request.GET.get("code")
    closedb()
    return render_to_response('invite/help.html',locals())
def pay(request):
    mer=MerchantAPI()
    transtime=int(time.time())
    od=str(random.randint(10, 100000))
    
    data=request.GET.get("data")
    #data="1"
    encryptkey=request.GET.get("encryptkey")
    #encryptkey="22"
    ll={'data':data,'encryptkey':encryptkey}
    #return HttpResponse(ll['data'])
    resualt=mer.result_decrypt1(ll)
    #url=mer.testwap_credit(Gl.merchantaccount,"zz91pay"+od,transtime,transtime,156,2,"1","再生钱包","","zz91account","192.168.5.251","ee",6,"","","","www.baidu.com","www.baidu.com","1|2")
    #url=mer.testwap_credit(merchantaccount=Gl.merchantaccount,orderid="zz91pay"+od,orderexpdate=transtime,transtime=transtime,currency=156,amount=2,productcatalog="7",userua="zz91account",productname="再生钱包",productdesc="",userip="192.168.5.251",identityid="4930024075993521"+od,identitytype=0,callbackurl="http://m.zz91.com",fcallbackurl="http://m.zz91.com",terminaltype=3,terminalid="05-16-DC-59-C2-34")
    #mer.testBindPaysignAsync(Gl.merchantaccount, "51804", "bangkazhifu"+od, transtime, 156, 2, "1", "商品", "", "172.0.0.1", "dd", 6, 0, "123", "www.baidu.com", "www.baidu.com")
    #mer.testvalidatecode(Gl.merchantaccount, "jiejikazhifu26622")
    #mer.testpayvalidatecode(Gl.merchantaccount, "jiejikazhifu26622","123123")
    #mer.testUnbindCardsign(Gl.merchantaccount,"940","ee",6)
    #mer.testQueryOrderSign(Gl.merchantaccount,"33hhkssseef3u"+od)
    #mer.testQueryPay(Gl.merchantaccount,"33hhkssseef3u17442","411308194795724586")
    #mer.testQueryRefund(Gl.merchantaccount,"tt9393232341025545687")
    #mer.testDirectRefund(Gl.merchantaccount,"tt9393232341025"+od,"411308194832127621",2,156,"退款")
    closedb()
    return HttpResponse(resualt)

#ppc浮动广告
def showppccomplist_float(request):
    company_id = request.GET.get("company_id")
    
    page = request.GET.get("page")
    keywords = request.GET.get("keywords")
    listall={'list':None,'count':200}
    if not keywords:
        keywords=""
        if str(company_id)!="0" and company_id:
            keywords=zzmain.getuserkeywords(company_id)
    if page:
        listall=zzmain.getcplist(keywords,frompageCount=(int(page)-1)*12,limitNum=12,allnum=2000)
    closedb()
    if not page:
        return render_to_response('script_showppccomplist_float.js',locals())
    else:
        return render_to_response('script_showppccomplist_float_next.js',locals())
#在线留言
def messages(request):
    merchant_url=request.META.get('HTTP_REFERER')
    closedb()
    return render_to_response("main/messages.html",locals())

def messages_save(request):
    merchant_url=request.POST.get("merchant_url")
    s=zzcompany.regsave(request)
    messPhone = str(request.POST.get('messPhone'))
    messQQ = str(request.POST.get('messQQ'))
    messEmail = str(request.POST.get('messEmail'))
    messName = str(request.POST.get('messName'))
    messText=str(request.POST.get("messText"))
    errflag=None
    errflag1=s['errflag1']
    errtext=s['errtext']
    if (validateEmail(messEmail)==0):
        errtext="您输入邮箱格式有错误！"
        errflag1=1
    if (messText==""):
        errflag1=1
        errtext="请填写留言内容！"
    if (messPhone=='' or messPhone.isdigit()==False):
        errtext="必须填写 手机号码"
        errflag1=1
    if (len(messPhone)<=10):
        errtext="填写手机号码必须大于11位"
        errflag1=1
    if str(merchant_url)=="None":
        merchant_url=None
    if errflag1==1:
        errflag=1
        return render_to_response("main/messages.html",locals())
    else:
        errtext=""
        zzcompany.savemessages(request)
        
        gmt_created=datetime.datetime.now()
        gmt_modified=datetime.datetime.now()
        #如果有登录
        username=request.session.get("username",None)
        company_id=request.session.get("company_id",None)
        #否则用刚注册的
        if not username:
            username=s['userName']
            company_id=zzcompany.getcompanyid(username)
        title=""
        bbs_post_assist_id=107
        if (messText and messText!=""):
            bbs_user_profiler_id=zzcompany.getprofilerid(username)
            if (bbs_user_profiler_id==None):
                bbs_user_profiler_id=1
            value=[company_id,bbs_user_profiler_id,username,106,title,messText,0,1,gmt_created,gmt_modified,gmt_modified,gmt_modified,1,bbs_post_assist_id]
            sql="insert into bbs_post(company_id,bbs_user_profiler_id,account,bbs_post_category_id,title,content,is_del,check_status,gmt_created,gmt_modified,post_time,reply_time,postsource,bbs_post_assist_id) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            dbc.updatetodb(sql,value)
    closedb()
    return render_to_response("main/messages_suc.html",locals())
#日志技术
def getloginfo(request):
    #return HttpResponse('document.write("'+str(request)+'")')
    return render_to_response("main/log.js",locals())
#全站日志统计
def saveloginfo(request):
    collection=dbmongo.zzlogall
    userid=request.GET.get("userid")
    title=request.GET.get("title")
    url=request.GET.get("url")
    mytime=formattime(datetime.datetime.now(),0)
    equip=request.GET.get("equip")
    ip=request.GET.get("ip")
    add=request.GET.get("add")
    preurl=request.GET.get("preurl")
    #preurl=request.META.get('HTTP_REFERER','/')
    ip=getIPFromDJangoRequest(request)
    
    collection.insert({"userid":userid,"title":title,"url":url,"mytime":mytime,"equip":equip,"ip":ip,"add":add,"preurl":preurl})
    closedb()
    return HttpResponse("1")
#帮你找
def need_put(request):
    return render_to_response("order/need_put.html",locals())
def need_category(request):
    ordercategorylist=getordercategorylistmain()
    return render_to_response("order/need_category.html",locals())
def need_province(request):
    arealist=['浙江','广东','江苏','福建','安徽','河南','河北','湖北','湖南','四川','江西','山东','海南','黑龙江','北京','上海','天津','青海','陕西','山西','贵州','辽宁','宁夏','吉林','内蒙古','广西','云南','西藏','重庆','甘肃','新疆','台湾','香港','澳门']
    return render_to_response("order/need_province.html",locals())

def choujiang(request):
    company_id=request.session.get("company_id",None)
    username=request.session.get("username",None)
    if not company_id:
        company_id=request.GET.get("mid")
    if not company_id:
        company_id=0
    return render_to_response("choujiang/index.html",locals())

#砸金蛋抽奖
def zadanplay(request):
    company_id=request.session.get("company_id",None)
    username=request.session.get("username",None)
    if not company_id:
        company_id=0
    return render_to_response("2016zadanplay/index.html",locals())

#刮刮乐
def guaguale_index(request):
    company_id=request.session.get("company_id",None)
    username=request.session.get("username",None)
    if not company_id:
        company_id=0
    return render_to_response("guaguale/index.html",locals())
def guaguale_play(request):
    company_id=request.session.get("company_id",None)
    username=request.session.get("username",None)
    if not company_id:
        company_id=0
    return render_to_response("guaguale/play.html",locals())

#购买优惠券获得
def youhui(request):
    company_id=request.session.get("company_id",None)
    username=request.session.get("username",None)
    if not company_id:
        company_id=0
    return render_to_response("youhui/index.html",locals())
