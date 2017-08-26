#-*- coding:utf-8 -*-
from django.shortcuts import render_to_response
from django.http import HttpResponse,HttpResponseRedirect,HttpResponsePermanentRedirect
import MySQLdb,sys,os,memcache,settings,urllib,re,time,datetime,requests,random,string,md5,hashlib
from django.core.cache import cache
from zz91settings import SPHINXCONFIG,weixinconfig
from zz91db_ast import companydb
from zz91db_sms import smsdb
from zz91db_2_news import newsdb

reload(sys)
sys.setdefaultencoding('UTF-8')

from zweixin.client import WeixinAPI,WeixinMpAPI
from zweixin.oauth2 import OAuth2AuthExchangeError

dbc=companydb()
dbn=newsdb()

nowpath=os.path.dirname(__file__)
execfile(nowpath+"/commfunction.py")
execfile(nowpath+"/function.py")
execfile(nowpath+"/func/myrc_function.py")

zzm=zmyrc()

APP_ID = weixinconfig['zz91service']['appid']
APP_SECRET = weixinconfig['zz91service']['secret']
REDIRECT_URI = 'http://m.zz91.com/wechat/redirect_uri.html'
api = WeixinMpAPI(appid=APP_ID,
                app_secret=APP_SECRET,
                redirect_uri=REDIRECT_URI)
from zzwx.client import Client
#微信授权登陆
def auth_login(request):
    scope = ("snsapi_base", )
    authorize_url = api.get_authorize_url(scope=scope)
    openid_dy=request.GET.get("clientid")
    request.session['clientid']=openid_dy
    tourl=request.GET.get("tourl")
    gmt_created=gmt_modified=datetime.datetime.now()
    if openid_dy:
        request.session['openid_dy']=openid_dy
    if tourl:
        request.session['tourl']=tourl
    """
    if openid_dy:
        sql="select id from weixin_bind where openid_dy=%s"
        result=dbc.fetchonedb(sql,openid_dy)
        if not result:
            openid_fw=""
            sql="insert into weixin_bind(openid_dy,openid_fw,gmt_created) values(%s,%s,%s)"
            dbc.updatetodb(sql,[openid_dy,openid_fw,gmt_created])
    """
    return HttpResponseRedirect(authorize_url)
def redirect_uri(request):
    code=request.GET.get("code")
    gmt_created=gmt_modified=datetime.datetime.now()
    access_token = api.exchange_code_for_access_token(code=code)
    openid_fw=access_token['openid']
    request.session['openid_fw']=openid_fw
    openid_dy=request.session.get("openid_dy")
    tourl=request.session.get("tourl")
    if openid_fw:
        sql="select id,company_id,openid_dy from weixin_bind where openid_fw=%s"
        result=dbc.fetchonedb(sql,openid_fw)
        if not result:
            #服务号未绑定
            if not request.session.get("openid_dy"):
                openid_dy=""
            else:
                openid_dy=request.session.get("openid_dy")
            sql="insert into weixin_bind(openid_dy,openid_fw,gmt_created) values(%s,%s,%s)"
            resultid=dbc.updatetodb(sql,[openid_dy,openid_fw,gmt_created])
            result=zzm.weixinautologin(request,openid_fw)
            #投票系统
            if "/vote/" in tourl:
                return HttpResponseRedirect(tourl)
            #621再生汇
            if "/zsh/" in tourl:
                return HttpResponseRedirect(tourl)
            if not result:
                if tourl:
                    tourl=tourl.replace("&","^and^")
                    tourl=tourl.replace("#","^jing^")
                    tourl=tourl.replace("?","^wenhao^")
                else:
                    tourl=""
                    
                if tourl in ['/trade/','/weixin/priceday.html','/trust/','/ye/','/huzhu/','/news/','/vote/jsindex.html']:
                    return HttpResponseRedirect(tourl)
                return HttpResponseRedirect("/weixin/login.html?weixinid="+openid_fw+"&tourl="+tourl)
            else:
                id=resultid[0]
                company_id=request.session.get("company_id")
                sql="update weixin_bind set company_id=%s where id=%s"
                dbc.updatetodb(sql,[company_id,id])
                
        else:
            company_id=result[1]
            id=result[0]
            nopenid_dy=result[2]
            if not nopenid_dy:
                if not request.session.get("openid_dy"):
                    openid_dy=""
                else:
                    openid_dy=request.session.get("openid_dy")
                sql="update weixin_bind set openid_dy=%s where id=%s"
                dbc.updatetodb(sql,[openid_dy,id])
            #已经绑定，设置登录
            #根据oauth_access来判断微信登陆账号
            #未设置，看之前是否绑定过，为绑定需要去绑定采能登录
            result=zzm.weixinautologin(request,openid_fw)
            if "/vote/" in tourl:
                return HttpResponseRedirect(tourl)
            if "/zsh/" in tourl:
                return HttpResponseRedirect(tourl)
            if not result:
                if tourl:
                    tourl=tourl.replace("&","^and^")
                    tourl=tourl.replace("#","^jing^")
                    tourl=tourl.replace("?","^wenhao^")
                else:
                    tourl=""
                if tourl in ['/trade/','/weixin/priceday.html','/trust/','/ye/','/huzhu/','/news/','/vote/jsindex.html','/vote/','/zsh/']:
                    return HttpResponseRedirect(tourl)
                return HttpResponseRedirect("/weixin/login.html?weixinid="+openid_fw+"&tourl="+tourl)
            else:
                company_id=request.session.get("company_id")
                sql="update weixin_bind set company_id=%s where id=%s"
                dbc.updatetodb(sql,[company_id,id])
    if not tourl:
        return HttpResponseRedirect("/")
    else:
        tourl=getlogintourl(tourl)
        return HttpResponseRedirect(tourl)
            
#统一微信分享js
def weixinsharejs(request):
    appid=weixinconfig['zz91service']['appid']
    client = Client(weixinconfig['zz91service']['appid'], weixinconfig['zz91service']['secret'])
    url=request.GET.get("wurl")
    pic=request.GET.get("pic")
    desc=request.GET.get("desc")
    #url="http://m.zz91.com"+host
    signlist=client.get_sign(url=url)
    timestamp=signlist['timestamp']
    nonceStr=signlist['nonceStr']
    signature=signlist['signature']
    jsapi_ticket=signlist['jsapi_ticket']
    
    return render_to_response("aui/wxshare.js",locals())
    