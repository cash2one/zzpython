#-*- coding:utf-8 -*-
from django.shortcuts import render_to_response
from django.http import HttpResponse,HttpResponseRedirect,HttpResponsePermanentRedirect
import MySQLdb,sys,os,memcache,settings,urllib,re,time,datetime,requests,random,string,md5,hashlib
from django.core.cache import cache
from zz91db_ast import companydb
dbc=companydb()
reload(sys)
sys.setdefaultencoding('UTF-8')

from zweixin.client import WeixinAPI,WeixinMpAPI
from zweixin.oauth2 import OAuth2AuthExchangeError

APP_ID = 'wx2891ef70c5a770d6'
APP_SECRET = 'd3f9436cfc50cd9e4f62f96893a1ee0c'
REDIRECT_URI = 'http://m.zz91.com/wechat/redirect_uri.html'
api = WeixinMpAPI(appid=APP_ID,
                app_secret=APP_SECRET,
                redirect_uri=REDIRECT_URI)
#微信授权登陆
def auth_login(request):
    scope = ("snsapi_base", )
    authorize_url = api.get_authorize_url(scope=scope)
    clientid=clientid_dy=request.GET.get("clientid")
    gmt_created=gmt_modified=datetime.datetime.now()
    if clientid:
        request.session['clientid_dy']=clientid
    
    if clientid:
        sql="select id from vote_visit_log where clientid_dy=%s"
        result=dbc.fetchonedb(sql,clientid)
        if not result:
            clientid_fw=""
            sql="insert into vote_visit_log(clientid_dy,clientid_fw,gmt_created) values(%s,%s,%s)"
            dbc.updatetodb(sql,[clientid_dy,clientid_fw,gmt_created])
    
    return HttpResponseRedirect(authorize_url)
def redirect_uri(request):
    code=request.GET.get("code")
    access_token = api.exchange_code_for_access_token(code=code)
    openid=access_token['openid']
    request.session['clientid_fw']=openid
    clientid_dy=request.session.get("clientid_dy",None)
    sql="select id from vote_visit_log where clientid_dy=%s"
    result=dbc.fetchonedb(sql,clientid_dy)
    if result:
        clientid_fw=openid
        sql="update vote_visit_log set clientid_fw=%s where clientid_dy=%s"
        dbc.updatetodb(sql,[clientid_fw,clientid_dy])
    #return HttpResponse("suc")
    return HttpResponseRedirect("/vote/index.html")
    #return render_to_response("vote/vote.html",locals())
    #return HttpResponse('var _suggest_result_={"openid":"'+access_token['openid']+'"}')
    #return HttpResponse(access_token['openid'])
    