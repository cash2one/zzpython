#-*- coding:utf-8 -*-

from django.shortcuts import render_to_response
from django.http import HttpResponse,HttpResponseRedirect,HttpResponsePermanentRedirect
import MySQLdb,sys,os,memcache,settings,urllib,re,time,datetime,requests,random,string,md5,hashlib,json,simplejson
from django.core.cache import cache
from sphinxapi import *
from zz91page import *
from settings import spconfig
from zz91settings import SPHINXCONFIG,weixinconfig
from commfunction import filter_tags,formattime,havepicflag,subString,getjiami,getIPFromDJangoRequest,validateEmail
from function import getnowurl,getbbslist
from zz91tools import int_to_str
from datetime import timedelta, date 
from zz91db_ast import companydb
from zz91db_2_news import newsdb
from zz91db_ads import adsdb
from zz91db_sms import smsdb
from zz91conn import database_mongodb
import operator
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

from zweixin.client import WeixinAPI,WeixinMpAPI
from zweixin.oauth2 import OAuth2AuthExchangeError

APP_ID = weixinconfig['zz91service']['appid']
APP_SECRET = weixinconfig['zz91service']['secret']
REDIRECT_URI = 'http://m.zz91.com/kanjia/redirect_uri.html'
api = WeixinMpAPI(appid=APP_ID,
                app_secret=APP_SECRET,
                redirect_uri=REDIRECT_URI)

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
    newslist=zzmain.getnewslist(limitNum=5,allnum=5)
    host=getnowurl(request)
    username=request.session.get("username",None)
    company_id=request.session.get("company_id",None)
    #供求总数
    zz91app_pcount=cache.get("zz91app_pcount")
    if not zz91app_pcount:
        sql="select count(0) from products"
        result=dbc.fetchonedb(sql)
        pcount='{:,}'.format(int(result[0]*4.65))
        cache.set("zz91app_pcount",pcount,60*24)
    else:
        pcount=zz91app_pcount
    if not company_id:
        appid=request.session.get("appid",None)
    else:
        appid=company_id
    mysearchkeylist=getkeywords(appid)
    abountkeywords=searchtis('')
    #广告
    adlist=zzmain.getadlistall(722)
    return render_to_response('aui/index.html',locals())
def yuanbaopu_help(request):
    return render_to_response('yuanbaopu/help.html',locals())
def yuanbaopu_about(request):
    return render_to_response('yuanbaopu/about.html',locals())
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
def loginstatus(request):
    company_id=request.session.get("company_id",None)
    if not company_id:
        return HttpResponse("var success='false';var companyId='0';")
    else:
        return HttpResponse("var success='true';var companyId='"+str(company_id)+"';")
    
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
    
#百度推广留下联系方式
def getcontactinfo(request):
    username=request.session.get("username",None)
    company_id=request.session.get("company_id",None)
    product_id=request.POST.get("product_id")
    if not username:
        s=zzcompany.regsave(request)
        company_id=s['company_id']
        username=s['userName']
        request.session['username']=username
        request.session['company_id']=company_id
        
        zzcompany.savemessages(request,s,paytype=0)
    #return HttpResponse("http://trade.zz91.com/productdetails"+str(product_id)+".htm")
    return HttpResponseRedirect("http://trade.zz91.com/productdetails"+str(product_id)+".htm")
def seoregister(request):
    s=zzcompany.regsave(request)
    errflag=s.get("errflag")
    errtext=s.get("errtext")
    regtime=datetime.datetime.now()
    if errflag==0:
        return HttpResponseRedirect("http://www.zz91.com/cp/reg.html?suc=1&"+str(regtime))
    else:
        return HttpResponseRedirect("http://www.zz91.com/cp/reg.html?err="+errtext+"&"+str(regtime))
#在线留言
def messages(request):
    merchant_url=request.META.get('HTTP_REFERER')
    pdt_id=0
    forcompany_id=0
    huzhu_id=request.GET.get("huzhu_id")
    username=request.session.get("username",None)
    company_id=request.session.get("company_id",None)
    companyname=request.GET.get("companyname")
    if merchant_url:
        if "/trade/detail" in merchant_url:
            re_detail=ur'/trade/detail(.*?).html'
            pdt_id=get_content(re_detail,merchant_url)
        if "/company/detail" in merchant_url:
            re_detail=ur'/company/detail(.*?).html'
            forcompany_id=get_content(re_detail,merchant_url)
        if not pdt_id:
            pdt_id=request.POST.get("pdt_id")
        if not forcompany_id:
            forcompany_id=request.POST.get("forcompany_id")
        if not huzhu_id:
            huzhu_id=request.POST.get("huzhu_id")
        if not forcompany_id:
            forcompany_id=request.GET.get("forcompany_id")
    return render_to_response("main/messages.html",locals())

def messages_save(request):
    merchant_url=request.POST.get("merchant_url")
    #如果有登录
    username=request.session.get("username",None)
    company_id=request.session.get("company_id",None)
    if not username:
        s=zzcompany.regsave(request)
    else:
        s={'userName':username,'company_id':company_id,'errflag1':'','errflag':'','errtext':'errtext'}
    
    messPhone = str(request.POST.get('messPhone'))
    messQQ = str(request.POST.get('messQQ'))
    messEmail = str(request.POST.get('messEmail'))
    messName = str(request.POST.get('messName'))
    messText=str(request.POST.get("messText"))
    pdt_id = request.POST.get('pdt_id')
    if str(pdt_id)=="0" or str(pdt_id)=="None":
        pdt_id=None
    forcompany_id = request.POST.get('forcompany_id')
    if str(forcompany_id)=="0"  or str(forcompany_id)=="None":
        forcompany_id=None
    huzhu_id = request.POST.get('huzhu_id')
    if str(huzhu_id)=="0"  or str(huzhu_id)=="None":
        huzhu_id=None
    errflag=None
    errflag1=s['errflag1']
    errtext=s['errtext']
    if (messText==""):
        errflag1=1
        errtext="请填写留言内容！"
    
    if not username:
        if (validateEmail(messEmail)==0):
            errtext="您输入邮箱格式有错误！"
            errflag1=1
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
        #未登录情况下
        if not pdt_id and not forcompany_id and not huzhu_id:
            zzcompany.savemessages(request,s)
        
        gmt_created=datetime.datetime.now()
        gmt_modified=datetime.datetime.now()
        
        #否则用刚注册的
        if not username:
            username=s['userName']
            company_id=s['company_id']
            #company_id=zzcompany.getcompanyid(username)
        sender_account=getcompanyaccount(company_id)
        title=""
        #写入留言表
        #对供求留言
        if pdt_id:
            be_inquired_type=0
            be_inquired_id=pdt_id
            sql="select company_id from products where id=%s"
            result=dbc.fetchonedb(sql,[pdt_id])
            if result:
                re_company_id=result[0]
                receiver_account=getcompanyaccount(re_company_id)
        #对公司留言
        if forcompany_id:
            be_inquired_type=1
            be_inquired_id=forcompany_id
            receiver_account=getcompanyaccount(forcompany_id)
        #互助留言
        if huzhu_id:
            be_inquired_type=4
            be_inquired_id=forcompany_id
            receiver_account=getcompanyaccount(forcompany_id)
        gmt_created=datetime.datetime.now()
        gmt_modified=datetime.datetime.now()
        #
        if pdt_id or forcompany_id:
            inquired_type=0
            send_time=datetime.datetime.now()
            content=messText
            value=[title,content,be_inquired_type,be_inquired_id,inquired_type,sender_account,receiver_account,send_time,gmt_created,gmt_modified]
            sql="insert into inquiry(title,content,be_inquired_type,be_inquired_id,inquired_type,sender_account,receiver_account,send_time,gmt_created,gmt_modified) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            dbc.updatetodb(sql,value);
        
        bbs_post_assist_id=107
        if huzhu_id:
            if (messText and messText!=""):
                bbs_post_id=huzhu_id
                content=messText
                value=[company_id,username,title,bbs_post_id,content,0,0,gmt_created,gmt_modified,1]
                sql="insert into bbs_post_reply(company_id,account,title,bbs_post_id,content,is_del,check_status,gmt_created,gmt_modified,postsource) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
                dbc.updatetodb(sql,value)
                sql="update bbs_post set reply_time=%s,reply_count=reply_count+1,gmt_modified=%s where id=%s"
                dbc.updatetodb(sql,[gmt_modified,gmt_modified,bbs_post_id])
        else:
            if (messText and messText!=""):
                bbs_user_profiler_id=zzcompany.getprofilerid(username)
                if (bbs_user_profiler_id==None):
                    bbs_user_profiler_id=1
                value=[company_id,bbs_user_profiler_id,username,106,title,messText,0,1,gmt_created,gmt_modified,gmt_modified,gmt_modified,1,bbs_post_assist_id]
                sql="insert into bbs_post(company_id,bbs_user_profiler_id,account,bbs_post_category_id,title,content,is_del,check_status,gmt_created,gmt_modified,post_time,reply_time,postsource,bbs_post_assist_id) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
                dbc.updatetodb(sql,value)
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
#2016台州塑交会抽奖
def taizhou2016(request):
    company_id=request.session.get("company_id",None)
    username=request.session.get("username",None)
    if not company_id:
        company_id=request.GET.get("mid")
    if not company_id:
        company_id=0
    return render_to_response("taizhou2016/index.html",locals())

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

#2016中秋祝福
def zhongqiu(request):
    appid=weixinconfig['zz91service']['appid']
    client = Client(weixinconfig['zz91service']['appid'], weixinconfig['zz91service']['secret'])
    host=getnowurl(request)
    host=host.replace("^and^","&")
    url="http://m.zz91.com"+host
    signlist=client.get_sign(url=url)
    timestamp=signlist['timestamp']
    nonceStr=signlist['nonceStr']
    signature=signlist['signature']
    jsapi_ticket=signlist['jsapi_ticket']
    s=request.GET.get("s")
    noweixin=request.GET.get("noweixin")
    if not noweixin:
        noweixin=0
    sql="select content,sharename from weixin_zhongqiushare where signature=%s"
    result=dbc.fetchonedb(sql,[s])
    if result:
        content=result[0]
        sharename=result[1]
        sharenametitle=sharename.replace("<br>","")
    return render_to_response("zhongqiu/index.html",locals())
def ybzhongqiu(request):
    appid=weixinconfig['zz91service']['appid']
    client = Client(weixinconfig['zz91service']['appid'], weixinconfig['zz91service']['secret'])
    host=getnowurl(request)
    host=host.replace("^and^","&")
    url="http://m.zz91.com"+host
    signlist=client.get_sign(url=url)
    timestamp=signlist['timestamp']
    nonceStr=signlist['nonceStr']
    signature=signlist['signature']
    jsapi_ticket=signlist['jsapi_ticket']
    s=request.GET.get("s")
    noweixin=request.GET.get("noweixin")
    if not noweixin:
        noweixin=0
    sql="select content,sharename from weixin_zhongqiushare where signature=%s"
    result=dbc.fetchonedb(sql,[s])
    if result:
        content=result[0]
        sharename=result[1]
        sharenametitle=sharename.replace("<br>","")
    return render_to_response("zhongqiu/ybindex.html",locals())

def zhongqiu_savecontent(request):
    gmt_created=datetime.datetime.now()
    signature = request.POST.get("signature")
    content = request.POST.get("content")
    sharename = request.POST.get("sharename")
    sql="select id from weixin_zhongqiushare where signature=%s"
    result=dbc.fetchonedb(sql,[signature])
    if result:
        sql="update weixin_zhongqiushare set content=%s,sharename=%s where id=%s"
        dbc.updatetodb(sql,[content,sharename,result[0]])
    else:
        sql="insert into weixin_zhongqiushare(signature,content,sharename,gmt_created) values(%s,%s,%s,%s)"
        dbc.updatetodb(sql,[signature,content,sharename,gmt_created])
    result={'err':'false','errkey':''}
    return HttpResponse(json.dumps(result, ensure_ascii=False))

#砍价首页
def kanjiaindex(request):
    gmt_created=gmt_modified=datetime.datetime.now()
    company_id=request.session.get("company_id",None)
    apploadflag=request.GET.get("apploadflag")
    if not company_id or apploadflag:
        company_id=request.GET.get("company_id")
        usertoken=request.GET.get("usertoken")
        if company_id:
            if apploadflag and usertoken:
                if getloginstatus(company_id,usertoken):
                    request.session['company_id']=company_id
    username=request.session.get("username",None)
    shuang11tourl=request.session.get("shuang11tourl",None)
    loadflag=request.GET.get("loadflag")
    
    d=request.GET.get("d")
    if d:
        if shuang11tourl and str(shuang11tourl)!="None":
            return HttpResponseRedirect(shuang11tourl)
    weixinid=request.GET.get("weixinid")
    kanjiaprolist=zzmain.getkanjialist(company_id=company_id)
    kanjiaprolist=sorted(kanjiaprolist, key=operator.itemgetter('havebaoming'),reverse=True)
    #是否已经报名
    baoming=None
    if company_id:
        if not apploadflag:
            if not weixinid or str(weixinid)=="None":
                account=getcompanyaccount(company_id)
                weixinid=weixinhavebind(account)
                if not weixinid:
                    weixinid=request.session.get("openid_dy",None)
                if not weixinid:
                    weixinid=request.session.get("openid_fw",None)
            if weixinid:
                sql="select id from weixin_live where weixinid=%s"
                result=dbc.fetchonedb(sql,[weixinid])
                if not result:
                    noweixin=1
                else:
                    noweixin=None
            else:
                noweixin=1
        sql="select pro_id from subject_kanjia_baoming where company_id=%s"
        result=dbc.fetchonedb(sql,[company_id])
        if result:
            baoming=1
    return render_to_response("subject/kanjia/index.html",locals())
def kanjiaappload(request):
    company_id=request.session.get("company_id",None)
    if not company_id:
        company_id=request.GET.get("company_id")
        usertoken=request.GET.get("usertoken")
        if not getloginstatus(company_id,usertoken):
            return HttpResponseRedirect("index.html?loadflag=0")
        else:
            if company_id:
                request.session['company_id']=company_id
                return HttpResponseRedirect("index.html?loadflag=0&company_id="+str(company_id))
            else:
                return HttpResponseRedirect("index.html?loadflag=0&company_id="+str(company_id))
    else:
        return HttpResponseRedirect("index.html?loadflag=0&company_id="+str(company_id))
    
    
#砍价-报名参加
def kanjiabaoming(request):
    appid=weixinconfig['zz91service']['appid']
    client = Client(weixinconfig['zz91service']['appid'], weixinconfig['zz91service']['secret'])
    host=getnowurl(request)
    host=host.replace("^and^","&")
    url="http://m.zz91.com"+host
    signlist=client.get_sign(url=url)
    timestamp=signlist['timestamp']
    nonceStr=signlist['nonceStr']
    signature=signlist['signature']
    jsapi_ticket=signlist['jsapi_ticket']
        
    host=getnowurl(request)
    gmt_created=gmt_modified=datetime.datetime.now()
    company_id=request.session.get("company_id",None)
    if not company_id:
        company_id=request.GET.get("company_id")
        usertoken=request.GET.get("usertoken")
        if usertoken and str(usertoken)!="None":
            if getloginstatus(company_id,usertoken):
                request.session['company_id']=company_id
    
    company_id=request.session.get("company_id",None)
    weixinid=request.GET.get("weixinid")
    username=request.session.get("username",None)
    if ((company_id==None or str(company_id)=="0")):
        return HttpResponseRedirect("/weixin/login.html?tourl="+host+"&weixinid="+str(weixinid))
    account=getcompanyaccount(company_id)
    weixinid=weixinhavebind(account)
    if not weixinid:
        weixinid=request.GET.get("weixinid")
    pro_id=request.GET.get("pro_id")
    kanjiaprolist=""
    #是否已经报名
    sql="select pro_id from subject_kanjia_baoming where company_id=%s"
    result=dbc.fetchonedb(sql,[company_id])
    if result:
        if str(result[0])==str(pro_id):
            a=1
            if not weixinid or str(weixinid)=="None":
                account=getcompanyaccount(company_id)
                weixinid=weixinhavebind(account)
            if weixinid:
                sql="select id from weixin_live where weixinid=%s"
                result=dbc.fetchonedb(sql,[weixinid])
                if not result:
                    noweixin=1
                else:
                    noweixin=None
            else:
                noweixin=1
            if noweixin:
                return HttpResponseRedirect("index.html?weixinid="+str(weixinid))
        else:
            return HttpResponseRedirect("index.html?weixinid="+str(weixinid))
    if pro_id:
        kanjiaprolist=zzmain.getkanjialist(proid=pro_id)[0]
        price=kanjiaprolist['price']
        cut_price=kanjiaprolist['cut_price']
        number=kanjiaprolist['number']
        lastprice=kanjiaprolist['lastprice']
        endtimeflag=kanjiaprolist['endtimeflag']
        if int(endtimeflag)>=0:
            endtimeflag=None
        else:
            endtimeflag=1
        #havenumber=kanjiaprolist['havenumber']
        #剩余0元数量
        havenumber=kanjiaprolist['bcount']
        
        companyname=getppccompanyinfo(company_id)['companyname']
        #报名
        sql="select price_now,payflag,id from subject_kanjia_baoming where company_id=%s and pro_id=%s"
        result=dbc.fetchonedb(sql,[company_id,pro_id])
        if result:
            price_now=result[0]
            payflag=result[1]
            #是否支付
            nopay=None
            if str(payflag)=="1":
                nopay=1
            baoming_id=result[2]
            #帮砍人数
            sql1="select sum(price_cut),count(0) from subject_kanjia_havecut where baoming_id=%s and pro_id=%s"
            result1=dbc.fetchonedb(sql1,[baoming_id,pro_id])
            if result1:
                price_now=int(price)-int(result1[0])
                #帮砍人数
                cutnumber=int(result1[1])
                if price_now<=0:
                    price_now=0
                #支付金额
                paymaney=price_now
                if havenumber<=0:
                    paymaney=price_now
                
                if int(price_now)<=int(lastprice) and havenumber<=0:
                    paymaney=lastprice
                    helpnum=None
                else:
                    helpnum=paymaney/5
                #砍价人员
                kanjiacutlist=zzmain.getkanjiacutlist(baoming_id=baoming_id)
            showsuc=None
        else:
            price_now=int(price)-int(cut_price)
            payflag=0
            #是否支付
            nopay=None
            sql="insert into subject_kanjia_baoming(company_id,price_now,payflag,pro_id,gmt_created) values(%s,%s,%s,%s,%s)"
            result=dbc.updatetodb(sql,[company_id,price_now,payflag,pro_id,gmt_created])
            if result:
                baoming_id=result[0]
                #自己先砍
                cutflag=zzmain.kanjiacutsave(baoming_id,weixinid,pro_id,cut_price)
            #帮砍人数
            cutnumber=1
            paymaney=price_now
            helpnum=paymaney/5
            #砍价人员
            kanjiacutlist=zzmain.getkanjiacutlist(baoming_id=baoming_id)
            showsuc=1
    else:
        return render_to_response("subject/kanjia/index.html",locals())
        
        
    return render_to_response("subject/kanjia/baoming.html",locals())
def redirect_uri(request):
    code=request.GET.get("code")
    gmt_created=gmt_modified=datetime.datetime.now()
    access_token = api.exchange_code_for_access_token(code=code)
    openid_fw=access_token['openid']
    request.session['openid_fw']=openid_fw
    shuang11tourl=request.session.get("shuang11tourl",None)
    return HttpResponseRedirect(shuang11tourl)
#用户砍价显示页
def kanjiacut(request,baoming_id):
    serviceopenid=request.session.get("openid_fw",None)
    shuang11tourl=getnowurl(request)
    request.session['shuang11tourl']=shuang11tourl
    if not serviceopenid:
        scope = ("snsapi_base", )
        authorize_url = api.get_authorize_url(scope=scope)
        openid_dy=request.GET.get("clientid")
        request.session['clientid']=openid_dy
        gmt_created=gmt_modified=datetime.datetime.now()
        if openid_dy:
            request.session['openid_dy']=openid_dy
        if shuang11tourl:
            request.session['shuang11tourl']=shuang11tourl
        return HttpResponseRedirect(authorize_url)
        
    
    gmt_created=gmt_modified=datetime.datetime.now()
    company_id=request.session.get("company_id",None)
    username=request.session.get("username",None)
    weixinid=request.GET.get("weixinid")
    if str(weixinid)=="None":
        weixinid=""
    if not weixinid:
        if company_id:
            account=getcompanyaccount(company_id)
            weixinid=weixinhavebind(account)
    suc=request.GET.get("suc")
    showsuc=None
    if suc:
        showsuc=1
    kanjiacutlist=None
    if baoming_id:
        #是否关注
        if not weixinid:
            weixinid=request.session.get("openid_dy",None)
        if not weixinid:
            weixinid=request.session.get("openid_fw",None)
        if weixinid:
            sql="select id from weixin_live where weixinid=%s"
            result=dbc.fetchonedb(sql,[weixinid])
            if not result:
                noweixin=1
            else:
                noweixin=None
        else:
            noweixin=1
        
        sql="select price_now,payflag,id,pro_id,company_id from subject_kanjia_baoming where id=%s"
        result=dbc.fetchonedb(sql,[baoming_id])
        if result:
            price_now=result[0]
            payflag=result[1]
            baoming_id=result[2]
            pro_id=result[3]
            company_id=result[4]
            companyname=zzcompany.getcompanyname(company_id)
            kanjiaprolist=zzmain.getkanjialist(proid=pro_id)[0]
            
            price=kanjiaprolist['price']
            lastprice=kanjiaprolist['lastprice']
            number=kanjiaprolist['number']
            endtimeflag=kanjiaprolist['endtimeflag']
            cut_price=kanjiaprolist['cut_price']
            if int(endtimeflag)>=0:
                endtimeflag=None
            else:
                endtimeflag=1
            #剩余0元数量
            havenumber=kanjiaprolist['bcount']
            #帮砍人数
            sql1="select sum(price_cut),count(0) from subject_kanjia_havecut where baoming_id=%s and pro_id=%s"
            result1=dbc.fetchonedb(sql1,[baoming_id,pro_id])
            if result1:
                price_now=int(price)-int(result1[0])
                #帮砍人数
                cutnumber=int(result1[1])
                if price_now<=0:
                    price_now=0
                #支付金额
                paymaney=price_now
                if havenumber<=0:
                    paymaney=price_now
                
                if int(price_now)<=int(lastprice) and havenumber<=0:
                    paymaney=lastprice
                    helpnum=None
                else:
                    helpnum=paymaney/5
                #砍价人员
                kanjiacutlist=zzmain.getkanjiacutlist(baoming_id=baoming_id)
            havekan=None
            sql="select id from subject_kanjia_havecut where baoming_id=%s and weixinid=%s"
            result=dbc.fetchonedb(sql,[baoming_id,weixinid])
            if result:
                havekan=1
                    
    return render_to_response("subject/kanjia/friend.html",locals())

#用户砍价保存
def kanjiacut_save(request):
    gmt_created=gmt_modified=datetime.datetime.now()
    company_id=request.session.get("company_id",None)
    username=request.session.get("username",None)
    weixinid=request.GET.get("weixinid")
    baoming_id=request.GET.get("baoming_id")
    noguanzhu=0
    if weixinid:
        
        sql="select id from weixin_live where weixinid=%s"
        result=dbc.fetchonedb(sql,[weixinid])
        if not result:
            noguanzhu=1
            #result={'err':'true','errkey':'您还未关注微信公众号，请关注后，点击“砍价”帮您朋友进行砍价吧！'}
    
        if baoming_id and noguanzhu==0:
            sql="select a.price_now,a.payflag,a.pro_id,b.cut_price,DATEDIFF(b.end_time,CURDATE()) from subject_kanjia_baoming as a left join subject_kanjia_pro as b on a.pro_id=b.id where a.id=%s"
            result=dbc.fetchonedb(sql,[baoming_id])
            if result:
                price_now=result[0]
                payflag=result[1]
                pro_id=result[2]
                cut_price=result[3]
                endtimeflag=result[4]
                if str(payflag)=="0" and int(endtimeflag)>=0:
                    cutflag=zzmain.kanjiacutsave(baoming_id,weixinid,pro_id,cut_price)
                    price_now=int(price_now)-int(cut_price)
                    return HttpResponseRedirect("cut"+str(baoming_id)+".html?suc=1&weixinid="+str(weixinid))
                
                
                    
    return HttpResponseRedirect("cut"+str(baoming_id)+".html")
#百度推广单页
def bdtuiguan(request):
    return render_to_response("subject/tuiguan/index.html",locals())
        
#2017元旦送祝福
def newyearindex(request):
    s=request.GET.get("s")
    if s:
        sql="select content from weixin_zhongqiushare where signature=%s"
        result=dbc.fetchonedb(sql,[s])
        if result:
            content=result[0]
    appid=weixinconfig['zz91service']['appid']
    client = Client(weixinconfig['zz91service']['appid'], weixinconfig['zz91service']['secret'])
    host=getnowurl(request)
    host=host.replace("^and^","&")
    url="http://m.zz91.com"+host
    signlist=client.get_sign(url=url)
    timestamp=signlist['timestamp']
    nonceStr=signlist['nonceStr']
    signature=signlist['signature']
    jsapi_ticket=signlist['jsapi_ticket']
    return render_to_response("subject/newyear/index.html",locals())
#2017元旦送祝福
def newyearybpindex(request):
    s=request.GET.get("s")
    if s:
        sql="select content from weixin_zhongqiushare where signature=%s"
        result=dbc.fetchonedb(sql,[s])
        if result:
            content=result[0]
    appid=weixinconfig['zz91service']['appid']
    client = Client(weixinconfig['zz91service']['appid'], weixinconfig['zz91service']['secret'])
    host=getnowurl(request)
    host=host.replace("^and^","&")
    url="http://m.zz91.com"+host
    signlist=client.get_sign(url=url)
    timestamp=signlist['timestamp']
    nonceStr=signlist['nonceStr']
    signature=signlist['signature']
    jsapi_ticket=signlist['jsapi_ticket']
    return render_to_response("subject/newyear/ybpindex.html",locals())

def feedbacksave(request):
    title = "手机问题反馈"
    content = request.POST.get('content')
    contact = request.POST.get('contact')
    company_id=request.session.get("company_id",None)
    username=request.session.get("username",None)
    if not contact:
        contact=""
    if not content:
        messagedata={'err':'true','errkey':'请填写问题描述','type':'leavewords'}
        return HttpResponse(simplejson.dumps(messagedata, ensure_ascii=False))
    gmt_created=datetime.datetime.now()
    paytype=47
    content=content+"<br/>电话："+contact
    sql='insert into shop_baoming(company_id,content,gmt_created,paytype) values(%s,%s,%s,%s)'
    dbc.updatetodb(sql,[company_id,content,gmt_created,paytype])
    #sql="insert into subject_baoming(title,contents,gmt_created) values(%s,%s,%s)"
    #dbc.updatetodb(sql,[title,content+"<br/>"+str(company_id)+"电话："+contact,gmt_created])
    messagedata={'err':'false','errkey':'提交成功,两个工作日内（节假日自动顺延）我们工作人员会联系您','type':'leavewords'}
    return HttpResponse(simplejson.dumps(messagedata, ensure_ascii=False))

#2017开春红包
def hongbao(request):
    host=getnowurl(request)
    company_id=request.session.get("company_id",None)
    username=request.session.get("username",None)
    datatype=request.GET.get("datatype")
    hongbaolist=[18,28,38,58]
    selecthongbao=random.choice(hongbaolist)
    if company_id:
        sql="select id,bnum,jiangpin from subject_choujiang where company_id=%s and btype='20111009'"
        result=dbc.fetchonedb(sql,[company_id])
        if result:
            checked=1
            jiangpin=result[2]
        else:
            checked=0
            btype='20111009'
            bnum=0
            jiangpin=selecthongbao
            gmt_created=gmt_modified=datetime.datetime.now()
            sql="insert into subject_choujiang(btype,gmt_created,bnum,company_id,jiangpin) values(%s,%s,%s,%s,%s)"
            dbc.updatetodb(sql,[btype,gmt_created,bnum,company_id,jiangpin])
        #jsonlist={'hongbao':jiangpin,'checked':checked,'err':'false'}
        #return HttpResponse(simplejson.dumps(jsonlist, ensure_ascii=False))
        return HttpResponse('var _suggest_result_={"hongbao":"'+str(jiangpin)+'","checked":'+str(checked)+',"err":"false"}')
        #return HttpResponseRedirect("/qianbao/chongzhi.html")
    else:
        return HttpResponse('var _suggest_result_={"err":"true"}')
        #return HttpResponseRedirect("/login/?done=http://app.zz91.com/app/html/ad/hongbao/index.html")
        #jsonlist={'err':'true','company_id':company_id}
        #return HttpResponse(simplejson.dumps(jsonlist, ensure_ascii=False))

#621专题
def subject_621(request):
    appid=weixinconfig['zz91service']['appid']
    client = Client(weixinconfig['zz91service']['appid'], weixinconfig['zz91service']['secret'])
    host=getnowurl(request)
    host=host.replace("^and^","&")
    url="http://m.zz91.com"+host
    signlist=client.get_sign(url=url)
    timestamp=signlist['timestamp']
    nonceStr=signlist['nonceStr']
    signature=signlist['signature']
    jsapi_ticket=signlist['jsapi_ticket']
    
    return render_to_response("subject/621/index.html",locals())

#康庄支付
def kangzhuang_zhifu(request):
    
    return render_to_response("main/kangzhuangzhifu.html",locals())
