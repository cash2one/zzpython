#-*- coding:utf-8 -*-
import MySQLdb,settings,codecs,os,sys,datetime,time,random,requests,hashlib,urllib,md5,simplejson
from django.shortcuts import render_to_response
from django.http import HttpResponse,HttpResponseRedirect,HttpResponseForbidden,HttpResponseNotFound,HttpResponsePermanentRedirect
from datetime import timedelta, date 
from dict2xml import dict2xml
from django.core.cache import cache
from zz91db_dibang import dibangdb
from zz91tools import formattime,int_to_strall
import json
from xml.etree import ElementTree as ET
try:
    import cPickle as pickle
except ImportError:
    import pickle
from math import ceil

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
        
        sql="select * from users where username=%s and pwd=%s"
        result=db.fetchonedb(sql,[username,md5pwd])
        if result:
            result['gmt_created']=formattime(result['gmt_created'])
            result['gmt_modified']=formattime(result['gmt_modified'])
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
    group_id=request.GET.get("group_id")
    xmltype=request.GET.get("xmltype")
    list={'err':'true','list':''}
    if iccode:
        sql="select * from suppliers where iccode=%s and group_id=%s limit 0,20"
        result=db.fetchalldb(sql,[iccode,group_id])
        if result:
            for dic in result:
                dic['gmt_created']=formattime(dic['gmt_created'])
                dic['gmt_modified']=formattime(dic['gmt_modified'])
            list['err']='false'
            list['list']=result
    if pname:
        sql="select * from suppliers where name like %s  and group_id=%s limit 0,20"
        result=db.fetchalldb(sql,['%'+pname+'%',group_id])
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

#更新数据
def api_datatable_update(request):
    maxid=request.GET.get("maxid")
    datatable=request.GET.get("datatable")
    company_id=request.GET.get("company_id")
    xmltype=request.GET.get("xmltype")
    list={'err':'true','list':''}
    if datatable:
        if maxid=="0" or not maxid:
            maxdate='1970-1-1'
        else:
            maxdate=int_to_strall(int(maxid))
        if datatable=="category_products":
            tablename="category_products"
        if datatable=="products":
            tablename="products"
        if datatable=="suppliers":
            tablename="suppliers"
        if datatable=="users":
            tablename="users"
        if datatable=="storage":
            tablename="storage"
        
        
        if datatable=="company":
            tablename="company"
            sql="select * from "+tablename+" where id=%s"
            result=db.fetchalldb(sql,[company_id])
        elif datatable=="grouplist":
            tablename="grouplist"
            sql="select * from "+tablename+" where id=%s"
            result=db.fetchalldb(sql,[company_id])
        else:
            if datatable=="storage":
                sql="select * from storage where gmt_modified>%s and price>0 and company_id=%s order by gmt_modified asc"
            else:
                sql="select * from "+tablename+" where gmt_modified>%s and company_id=%s order by gmt_modified asc"
            result=db.fetchalldb(sql,[maxdate,company_id])
        if result:
            for dic in result:
                dic['gmt_created']=formattime(dic['gmt_created'])
                dic['gmt_modified']=formattime(dic['gmt_modified'])
                if datatable=="storage":
                    dic['price_time']=formattime(dic['price_time'])
                    dic['out_time']=formattime(dic['out_time'])
                    dic['pay_time']=formattime(dic['pay_time'])
            list['err']='false'
            list['list']=result
        #return HttpResponse(sql)
    if xmltype:
        xml=dict2xml(list,wrap='xml')
        return HttpResponse(xml)
    else:
        return HttpResponse(simplejson.dumps(list, ensure_ascii=False))

def api_getstoragedate(request):
    company_id=request.GET.get("company_id")
    sql="select max(gmt_modified) as gmt_modified from storage where company_id=%s"
    result=db.fetchonedb(sql,[company_id])
    if result:
        if result['gmt_modified']:
            return HttpResponse(formattime(result['gmt_modified']))
        else:
            return HttpResponse("0")
    else:
        return HttpResponse("0")
    #return HttpResponse(simplejson.dumps(list, ensure_ascii=False))
def api_getsuppliersdate(request):
    company_id=request.GET.get("company_id")
    sql="select max(gmt_modified) as gmt_modified from suppliers where company_id=%s"
    result=db.fetchonedb(sql,[company_id])
    if result:
        if result['gmt_modified']:
            return HttpResponse(formattime(result['gmt_modified']))
        else:
            return HttpResponse("0")
    else:
        return HttpResponse("0")
    
#----更新供应商
def api_updatesuppliers(request):
    supplierlist=request.POST.get("supplierlist")
    if not supplierlist:
        supplierlist=request.GET.get("supplierlist")
    if supplierlist:
        supparr1=supplierlist.split("$")
        for list in supparr1:
            a=list.split("|")
            if len(a)>12:
                selfid=a[0]
                ctype=a[1]
                iccode=a[2]
                group_id=a[3]
                company_id=a[4]
                name=a[5]
                htype=a[6]
                contact=a[7]
                mobile=a[8]
                pwd=a[9]
                address=a[10]
                bz=a[11]
                gmt_created=a[12]
                gmt_modified=a[13]
                sql="select id from suppliers where selfid=%s"
                result=db.fetchonedb(sql,[selfid])
                if not result:
                    sql="insert into suppliers(selfid,ctype,iccode,group_id,company_id,name,htype,contact,mobile,pwd,address,bz,gmt_created,gmt_modified) values"
                    sql+="(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
                    db.updatetodb(sql,[selfid,ctype,iccode,group_id,company_id,name,htype,contact,mobile,pwd,address,bz,gmt_created,gmt_modified])
                else:
                    sql="update suppliers set ctype=%s,iccode=%s,name=%s,htype=%s,contact=%s,mobile=%s,pwd=%s,address=%s,bz=%s,gmt_modified=%s where selfid=%s"
                    db.updatetodb(sql,[ctype,iccode,name,htype,contact,mobile,pwd,address,bz,gmt_modified,selfid])
    return HttpResponse("0")
#----更新库存信息
def api_updatestorage(request):
    storelist=request.POST.get("storelist")
    if not storelist:
        storelist=request.GET.get("storelist")
    #return HttpResponse(storelist)
    if storelist:
        storelistarr1=storelist.split("$")
        for list in storelistarr1:
            
            a=list.split("|")
            if len(a)>21:
                selfid=a[0]
                #return HttpResponse(a[1])
                group_id=a[1]
                company_id=a[2]
                code=a[3]
                products_selfid=a[4]
                suppliers_selfid=a[5]
                price=a[6]
                gw=a[7]
                nw=a[8]
                tare=a[9]
                tare_check=a[10]
                total=a[11]
                status=a[12]
                price_users_selfid=a[13]
                price_time=a[14]
                out_time=a[15]
                ispay=a[16]
                scorecheck=a[17]
                pay_time=a[18]
                pay_users_selfid=a[19]
                gmt_created=a[20]
                gmt_modified=a[21]
                sql="select id from storage where selfid=%s"
                result=db.fetchonedb(sql,[selfid])
                if not result:
                    sql="insert into storage(selfid,group_id,company_id,code,products_selfid,suppliers_selfid,price,gw,nw,tare,tare_check,total,status,price_users_selfid,price_time,out_time,ispay,scorecheck,pay_time,pay_users_selfid,gmt_created,gmt_modified) values"
                    sql+="(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
                    db.updatetodb(sql,[selfid,group_id,company_id,code,products_selfid,suppliers_selfid,price,gw,nw,tare,tare_check,total,status,price_users_selfid,price_time,out_time,ispay,scorecheck,pay_time,pay_users_selfid,gmt_created,gmt_modified])
                    
                else:
                    sql="update storage set products_selfid=%s,suppliers_selfid=%s,price=%s,gw=%s,nw=%s,tare=%s,tare_check=%s,total=%s,status=%s,price_users_selfid=%s,price_time=%s,out_time=%s,ispay=%s,scorecheck=%s,pay_time=%s,pay_users_selfid=%s,gmt_modified=%s where selfid=%s"
                    db.updatetodb(sql,[products_selfid,suppliers_selfid,price,gw,nw,tare,tare_check,total,status,price_users_selfid,price_time,out_time,ispay,scorecheck,pay_time,pay_users_selfid,gmt_modified,selfid])
    return HttpResponse("0")
#----入库微信提醒
    
#微信
def api_weixinget(request):
    #地磅微信
    token = "dibang123weixin"
    params = request.GET
    args = [token, params['timestamp'], params['nonce']]
    args.sort()
    if hashlib.sha1("".join(args)).hexdigest() == params['signature']:
        if params.has_key('echostr'):
            return HttpResponse(params['echostr'])
        else:
            if request.body:
                xml = ET.fromstring(request.body)
                fromUserName = xml.find("ToUserName").text
                toUserName = xml.find("FromUserName").text
                MsgType = xml.find("MsgType").text
                Event1=None
                content=None
                EventKey=""
                if (MsgType=="event"):
                    Event1 = xml.find("Event").text
                    EventKey = xml.find("EventKey").text
                if (MsgType=="text"):
                    content = xml.find("Content").text
                if (MsgType=="image"):
                    PicUrl = xml.find("PicUrl").text
                if EventKey==None:
                    keyw=Event1
                else:
                    keyw=EventKey
                #记录日志
                
                postTime = str(int(time.time()))
                
                if (Event1 == "subscribe" or Event1 == "scan"):
                    title="您好！感谢关注再生汇"
                    xml=backxml(xmltype=2,fromUserName=toUserName,toUserName=fromUserName,title=title)
                    return HttpResponse(xml)
                else:
                    title=content
                    
                if (content==None  and EventKey=='qiandao'):
                    tpurl="http://m.zz91.com/wechat/auth_login.html?tourl=/zsh/index.html?clientid="+str(toUserName)+""
                    titlelist=[{'title':'2017废纸产业发展论坛现场签到','Description':'点此签到','PicUrl':'http://m.zz91.com/zt/feizhiluntanH5/images/weixin_qiandao.jpg','Url':tpurl}]
                    ArticleCount=len(titlelist)
                    xml=backxml(xmltype=3,fromUserName=toUserName,toUserName=fromUserName,ArticleCount=ArticleCount,titlelist=titlelist)
                    return HttpResponse(xml)
                else:
                    return HttpResponse("Invalid Request")
    else:
        return HttpResponse("Invalid Request")
