#-*- coding:utf-8 -*-
from django.shortcuts import render_to_response
from django.http import HttpResponse,HttpResponseRedirect
import MySQLdb,simplejson,sys,os,urllib,re,datetime,time,md5,hashlib,random,calendar,json,xlwt
import StringIO,qrcode

from zweixin.client import WeixinAPI,WeixinMpAPI
from zweixin.oauth2 import OAuth2AuthExchangeError

from zzwx.client import Client
from zz91settings import weixinconfig
from zz91db_dibang import dibangdb

APP_ID = weixinconfig['dibang']['appid']
APP_SECRET = weixinconfig['dibang']['secret']

wxc = Client(APP_ID, APP_SECRET)

REDIRECT_URI = 'http://dibang.zz91.com/wechat/redirect_uri.html'
api = WeixinMpAPI(appid=APP_ID,
                app_secret=APP_SECRET,
                redirect_uri=REDIRECT_URI)

reload(sys)
sys.setdefaultencoding('UTF-8')
nowpath=os.path.dirname(__file__)
dbd=dibangdb(1)
#微信授权登陆
def auth_login(request):
    scope = ("snsapi_base", )
    authorize_url = api.get_authorize_url(scope=scope)
    tourl=request.GET.get("tourl")
    if tourl:
        request.session['tourl']=tourl
    return HttpResponseRedirect(authorize_url)
def redirect_uri(request):
    code=request.GET.get("code")
    gmt_created=gmt_modified=datetime.datetime.now()
    access_token = api.exchange_code_for_access_token(code=code)
    openid_fw=access_token['openid']
    request.session['openid_fw']=openid_fw
    tourl=request.session.get("tourl")
    #return HttpResponse(openid_fw)
    sql='select id,group_id,selfid,company_id,utype,username from users where weixinid=%s and isdel=0'
    result=dbd.fetchonedb(sql,[openid_fw])
    if result:
        user_id=result['id']
        group_id=result['group_id']
        user_selfid=result['selfid']
        company_id=result['company_id']
        username=result['username']
        utype=result['utype']
        request.session.set_expiry(6000*60000)
        request.session['user_id']=user_id
        request.session['username']=username
        request.session['group_id']=group_id
        request.session['user_selfid']=user_selfid
        request.session['company_id']=company_id
        request.session['utype']=utype
    if not tourl:
        tourl="http://dibang.zz91.com/mobile/index.html"
    return HttpResponseRedirect(tourl)
    
def weixintixin(storage_selfid=""):
    if storage_selfid:
        weixinid=''
        sql="select company_id from storage where selfid=%s"
        result=dbd.fetchonedb(sql,[storage_selfid])
        if result:
            company_id=result["company_id"]
            sql="select weixinid from users where company_id=%s"
            result=dbd.fetchonedb(sql,[company_id])
            if result:
                weixinid=result['weixinid']
        if weixinid:
            datava={
                "touser":weixinid,
                "template_id":"dobF8p5gug2Te4rgjNQeli5qJuAo776Q2HsA5u8twZ4",
                "url":"http://bestjoy.asto.com.cn/agent/agent_ordershow.html?order_id="+str(orderid)+"&weixinid="+str(weixinid),
                "topcolor":"#FF0000",
                "data":{
                    "first": {
                    "value":"有新的发货订单，敬请查收！",
                    "color":"#173177"
                    },
                    "keyword1":{
                    "value":str(order['orderno']),
                    "color":"#173177"
                    },
                    "keyword2":{
                    "value":order['proname'],
                    "color":"#173177"
                    },
                    "keyword3":{
                    "value":str(order['protype'])+"/"+str(order['prosize']),
                    "color":"#173177"
                    },
                    "keyword4":{
                    "value":str(order['proprice'])+"/"+str(order['pronumber']),
                    "color":"#173177"
                    },
                    "keyword5":{
                    "value":str(order['arealabel'])+str(order['address']),
                    "color":"#173177"
                    },
                    "remark":{
                    "value":"请尽快联系客户，预约时间，有问题请致电步多健全国电商服务热线：400-115-2022",
                    "color":"#173177"
                    },
                }
            }
            datava=json.dumps(datava,ensure_ascii=False,indent=2)
            token=wxc.send_template_message(datava)