#-*- coding:utf-8 -*-
import MySQLdb,settings,codecs,os,sys,datetime,time,random,requests,hashlib,md5,simplejson
from django.shortcuts import render_to_response
from django.http import HttpResponse,HttpResponseRedirect,HttpResponseForbidden,HttpResponseNotFound,HttpResponsePermanentRedirect
from datetime import timedelta, date 
from dict2xml import dict2xml
from django.core.cache import cache
from zz91db_dibang import dibangdb
from zz91tools import formattime
db=dibangdb(1)
from zz91page import *
reload(sys) 
sys.setdefaultencoding('utf-8') 
nowpath=os.path.dirname(__file__)

#登录
def api_loginsave(request):
    username = request.GET.get('username')
    passwd = request.GET.get('pwd')
    passwdjm = request.GET.get('passwdjm')
    clientid = request.GET.get('clientid')
    xmltype = request.GET.get('xmltype')
    if passwd:
        md5pwd = hashlib.md5(passwd)
        md5pwd = md5pwd.hexdigest()[8:-8]
    else:
        if passwdjm:
            md5pwd=passwdjm[8:-8]
    if not username or not passwd:
        list={'err':'true','errtext':'用户名或密码错误','result':''}
    else:
        gmt_created=datetime.datetime.now()
        gmt_modified=datetime.datetime.now()
        token = hashlib.md5(str(passwd)+str(username)+str(gmt_modified))
        token = token.hexdigest()[8:-8]
        
        sql="select id,group_id,company_id,selfid from users where username=%s and pwd=%s"
        result=db.fetchonedb(sql,[username,md5pwd])
        if result:
            list={'err':'false','errtext':'','result':result}
            if not result["selfid"]:
                selfid=token
                sql="update users set selfid=%s where id=%s"
                db.updatetodb(sql,[selfid,result['id']])
            sql="update users set clientid=%s where id=%s"
            db.updatetodb(sql,[clientid,result['id']])
        else:
            list={'err':'true','errtext':'用户名或密码错误','result':''}
    if xmltype:
        xml=dict2xml(list,wrap='xml')
        return HttpResponse(xml)
    else:
        return HttpResponse(simplejson.dumps(list, ensure_ascii=False))
#查询供应商
def api_searchsuppliers(request):
    iccode=request.GET.get("iccode")
    pname=request.GET.get("pname")
    xmltype=request.GET.get("xmltype")
    list={'err':'true','list':''}
    if iccode:
        sql="select * from suppliers where iccode=%s limit 0,20"
        result=db.fetchalldb(sql,[iccode])
        if result:
            for dic in result:
                dic['gmt_created']=formattime(dic['gmt_created'])
                dic['gmt_modified']=formattime(dic['gmt_modified'])
            list['err']='false'
            list['list']=result
    if pname:
        sql="select * from suppliers where name like %s  limit 0,20"
        result=db.fetchalldb(sql,['%'+pname+'%'])
        if result:
            for dic in result:
                dic['gmt_created']=formattime(dic['gmt_created'])
                dic['gmt_modified']=formattime(dic['gmt_modified'])
            list['err']='false'
            list['list']=result
    if xmltype:
        xml=dict2xml(list,wrap='xml')
        return HttpResponse(xml)
    else:
        return HttpResponse(simplejson.dumps(list, ensure_ascii=False))
