#-*- coding:utf-8 -*-
from django.shortcuts import render_to_response
from django.http import HttpResponse,HttpResponseRedirect,HttpResponsePermanentRedirect
import MySQLdb,sys,os,memcache,settings,urllib,re,time,datetime,requests,random,string,md5,hashlib
from django.core.cache import cache
import simplejson
from sphinxapi import *
from zz91page import *
from settings import spconfig
from zz91settings import SPHINXCONFIG,weixinconfig
from commfunction import filter_tags,formattime,havepicflag,subString,getjiami,getIPFromDJangoRequest,validateEmail
from function import getnowurl,getbbslist
from zz91tools import int_to_str,str_to_int,date_to_int
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
execfile(nowpath+"/func/vote_function.py")
execfile(nowpath+"/function.py")

from zzwx.client import Client
zzmain=zmain()
zzcompany=zcompany()
zzv=zvote()
#元宝铺调查问卷跳转
def ybp_redirect(request):
    clientid=clientid_dy=request.GET.get("clientid")
    gmt_created=gmt_modified=datetime.datetime.now()
    if clientid:
        request.session['openid_dy']=clientid
    return HttpResponseRedirect("/vote/ybp_index.html")

#元宝铺调查问卷
def ybp_index(request):
    openid=request.session.get("openid_dy",None)
    votelist=zzv.votecontent(forno='yuanbaopu')
    gmt_created=gmt_modified=datetime.datetime.now()
    sql="update vote_pv set vcount=vcount+1 where forno=%s"
    dbc.updatetodb(sql,['yuanbaopu'])
    sql="select vcount from vote_pv where forno='yuanbaopu'"
    result=dbc.fetchonedb(sql)
    if result:
        vcount=result[0]
    showgz=1
    havevote=0
    if openid:
        sql="select id from weixin_gzlist where openid=%s"
        result=dbc.fetchonedb(sql,[openid])
        if result:
            showgz=0
        sqlc="select id from vote_content_contact where openid=%s"
        resultc=dbc.fetchonedb(sqlc,[openid])
        if resultc:
            havevote=1
    return render_to_response("vote/ybp_index.html",locals())
#问卷调查保存
def ybp_vote_save(request):
    openid=request.session.get("openid_dy",None)
    if not openid:
        return HttpResponse('var _suggest_result_={"err":"true","errtext":"","gz":1}')
    vote_cidlist=request.GET.get("vote_cidlist")
    vote_cidtext=request.GET.get("vote_cidtext")
    vote_cidtextid=request.GET.get("vote_cidtextid")
    pname=request.GET.get("pname")
    pcontact=request.GET.get("pcontact")
    
    if not vote_cidlist or not pname or not pcontact:
        return HttpResponse('var _suggest_result_={"err":"true","errtext":"请填写完整调查表!","gz":3}')
    vote_cidlist=vote_cidlist.split(",")
    vote_cidtext=vote_cidtext.split("|")
    vote_cidtextid=vote_cidtextid.split("|")
    gmt_created=gmt_modified=datetime.datetime.now()
    sql="select id from vote_content_select where openid=%s"
    result=dbc.fetchonedb(sql,[openid])
    if not result:
        for list in vote_cidlist:
            sql="insert into vote_content_select(openid,vote_cid,vote_ctext,gmt_created) values(%s,%s,%s,%s)"
            dbc.updatetodb(sql,[openid,list,'',gmt_created])
        n=0
        for list in vote_cidtext:
            vote_cid=vote_cidtextid[n]
            n=n+1
            sql="select id from vote_content_select where openid=%s and vote_cid=%s"
            result=dbc.fetchonedb(sql,[openid,vote_cid])
            if result:
                id=result[0]
                sql="update vote_content_select set vote_ctext=%s where id=%s"
                dbc.updatetodb(sql,[list,id])
            else:
                sql="insert into vote_content_select(openid,vote_cid,vote_ctext,gmt_created) values(%s,%s,%s,%s)"
                dbc.updatetodb(sql,[openid,vote_cid,list,gmt_created])
        sqlc="select id from vote_content_contact where openid=%s"
        resultc=dbc.fetchonedb(sqlc,[openid])
        if not resultc:
            sqlc="insert into vote_content_contact(openid,pname,pcontact,gmt_created) values(%s,%s,%s,%s)"
            dbc.updatetodb(sqlc,[openid,pname,pcontact,gmt_created])
            wxc = Client(weixinconfig['yuanbaopu']['appid'], weixinconfig['yuanbaopu']['secret'])
            token=wxc.send_text_message(openid,"谢谢您，"+str(pname)+"，凭此截图，向您的客服领取专属福利！我们电话是\n 4007-117-000")
        return HttpResponse('var _suggest_result_={"err":"false","errtext":"凭此截图，向您的客服领取专属福利！","gz":0}')
    return HttpResponse('var _suggest_result_={"err":"true","errtext":"您已经填写调查问卷","gz":2}')
    
def index(request):
    clientid_fw=request.session.get("openid_fw",None)
    clientid_dy=request.session.get("openid_dy",None)
    keywords=request.GET.get("keywords")
    qianbao_gglist=zzv.votelist(0,100,keywords=keywords,vtype="0")
    listall=qianbao_gglist['list']
    count=qianbao_gglist['count']
    openid=request.GET.get("openid")
    sql="update vote_pv set vcount=vcount+1 where id=%s"
    dbc.updatetodb(sql,[1])
    vcount=998
    sql="select vcount from vote_pv where id=1"
    result=dbc.fetchonedb(sql)
    if result:
        vcount=result[0]
    return render_to_response("vote/index.html",locals())
#2016 12.21金属金牌采购商
def jsindex(request):
    clientid_fw=request.session.get("openid_fw",None)
    clientid_dy=request.session.get("openid_dy",None)
    if not clientid_fw:
        return HttpResponseRedirect("/wechat/auth_login.html?tourl=/vote/jsindex.html")
    keywords=request.GET.get("keywords")
    qianbao_gglist=zzv.votelist(0,100,keywords=keywords,vtype="1")
    listall=qianbao_gglist['list']
    count=qianbao_gglist['count']
    openid=request.GET.get("openid")
    sql="update vote_pv set vcount=vcount+1 where id=%s"
    dbc.updatetodb(sql,[3])
    vcount=998
    sql="select vcount from vote_pv where id=3"
    result=dbc.fetchonedb(sql)
    if result:
        vcount=result[0]
    return render_to_response("vote/jsindex.html",locals())

#2017 621峰会
def v621_index(request):
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
    clientid_fw=request.session.get("openid_fw",None)
    clientid_dy=request.session.get("openid_dy",None)
    #入围企业
    ccount=0
    sql="select count(0) from vote_list where vtype in (2,3)"
    result=dbc.fetchonedb(sql)
    if result:
        ccount=result[0]
    #访问量
    vcount=0
    sql="select sum(vcount) from vote_pv where id in (4,5)"
    result=dbc.fetchonedb(sql)
    if result:
        vcount=result[0]
    #投票量
    tcount=0
    sql="select count(0) from vote_log where vtype in (2,3)"
    result=dbc.fetchonedb(sql)
    if result:
        tcount=result[0]
    votecontent=zzv.getvote(id=4)
    sql="update vote_pv set vcount=vcount+1 where id=%s"
    dbc.updatetodb(sql,[4])
    return render_to_response("vote/621/index.html",locals())
def v621_gys(request):
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
    
    clientid_fw=request.session.get("openid_fw",None)
    clientid_dy=request.session.get("openid_dy",None)
    vtype="2"
    countid=4
    vcount=998
    if not clientid_fw:
        return HttpResponseRedirect("/wechat/auth_login.html?tourl=/vote/621/gys.html")
    keywords=request.GET.get("keywords")
    vlist=zzv.votelist(0,100,keywords=keywords,vtype=vtype)
    listall=vlist['list']
    count=vlist['count']
    openid=request.GET.get("openid")
    
    sql="update vote_pv set vcount=vcount+1 where id=%s"
    dbc.updatetodb(sql,[countid])
    votecontent=zzv.getvote(id=countid)
    vcount=votecontent['vcount']
        
    return render_to_response("vote/621/gys.html",locals())
def v621_gys_zxpm(request):
    gmt_created=gmt_modified=datetime.datetime.now()
    gmt_date=formattime(gmt_created,0)
    vtype=2
    votecontent=zzv.getvote(id=4)
    if vtype:
        sql="select id,company_name,orderid,votecount,company_id from vote_list where vtype=%s order by votecount desc"
        result=dbc.fetchalldb(sql,[vtype])
        listall=[]
        if result:
            n=1
            for list in result:
                id=list[0]
                company_name=list[1]
                orderid=list[2]
                votecount=zzv.getvotecount(list[4],vtype)
                sqlc="update vote_list set votecount=%s where id=%s"
                dbc.updatetodb(sqlc,[votecount,list[0]])
                ll={'id':id,'n':n,'company_name':company_name,'orderid':orderid,'votecount':votecount}
                listall.append(ll)
                n=n+1
    sql="update vote_pv set vcount=vcount+1 where id=%s"
    dbc.updatetodb(sql,[5])
    return render_to_response("vote/621/gys-zxpm.html",locals())
def v621_gys_view(request,vid):
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
    vtype=2
    id=vid
    
    clientid_fw=request.session.get("openid_fw",None)
    clientid_dy=request.session.get("openid_dy",None)
    if not clientid_fw:
        return HttpResponseRedirect("/wechat/auth_login.html?tourl=/vote/621/gys-view"+str(id)+".html")
    detail=zzv.getvotedetail(id)
    #入围企业
    ccount=0
    sql="select count(0) from vote_list where vtype in (2,3)"
    result=dbc.fetchonedb(sql)
    if result:
        ccount=result[0]
    #访问量
    vcount=0
    sql="select sum(vcount) from vote_pv where id in (4,5)"
    result=dbc.fetchonedb(sql)
    if result:
        vcount=result[0]
    #投票量
    tcount=0
    sql="select count(0) from vote_log where vtype in (2,3)"
    result=dbc.fetchonedb(sql)
    if result:
        tcount=result[0]
    votecontent=zzv.getvote(id=4)
    pcount=zzv.getvotecount(detail['company_id'],vtype)
    sql="update vote_pv set vcount=vcount+1 where id=%s"
    dbc.updatetodb(sql,[4])
    return render_to_response("vote/621/gys-view.html",locals())

def v621_cgs(request):
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
    
    clientid_fw=request.session.get("openid_fw",None)
    clientid_dy=request.session.get("openid_dy",None)
    vtype="3"
    countid=5
    vcount=1998
    if not clientid_fw:
        return HttpResponseRedirect("/wechat/auth_login.html?tourl=/vote/621/cgs.html")
    keywords=request.GET.get("keywords")
    qianbao_gglist=zzv.votelist(0,100,keywords=keywords,vtype=vtype)
    listall=qianbao_gglist['list']
    count=qianbao_gglist['count']
    openid=request.GET.get("openid")
    
    sql="update vote_pv set vcount=vcount+1 where id=%s"
    dbc.updatetodb(sql,[countid])
    
    votecontent=zzv.getvote(id=countid)
    vcount=votecontent['vcount']
        
    return render_to_response("vote/621/cgs.html",locals())
def v621_cgs_zxpm(request):
    gmt_created=gmt_modified=datetime.datetime.now()
    gmt_date=formattime(gmt_created,0)
    vtype=3
    votecontent=zzv.getvote(id=4)
    if vtype:
        sql="select id,company_name,orderid,votecount,company_id from vote_list where vtype=%s order by votecount desc"
        result=dbc.fetchalldb(sql,[vtype])
        listall=[]
        if result:
            n=1
            for list in result:
                id=list[0]
                company_name=list[1]
                orderid=list[2]
                votecount=zzv.getvotecount(list[4],vtype)
                sqlc="update vote_list set votecount=%s where id=%s"
                dbc.updatetodb(sqlc,[votecount,list[0]])
                ll={'id':id,'n':n,'company_name':company_name,'orderid':orderid,'votecount':votecount}
                listall.append(ll)
                n=n+1
    sql="update vote_pv set vcount=vcount+1 where id=%s"
    dbc.updatetodb(sql,[5])
    return render_to_response("vote/621/cgs-zxpm.html",locals())
def v621_cgs_view(request,vid):
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
    
    vtype=3
    id=vid
    clientid_fw=request.session.get("openid_fw",None)
    clientid_dy=request.session.get("openid_dy",None)
    if not clientid_fw:
        return HttpResponseRedirect("/wechat/auth_login.html?tourl=/vote/621/gys-view"+str(id)+".html")
    detail=zzv.getvotedetail(id)
    #入围企业
    ccount=0
    sql="select count(0) from vote_list where vtype in (2,3)"
    result=dbc.fetchonedb(sql)
    if result:
        ccount=result[0]
    #访问量
    vcount=0
    sql="select sum(vcount) from vote_pv where id in (4,5)"
    result=dbc.fetchonedb(sql)
    if result:
        vcount=result[0]
    #投票量
    tcount=0
    sql="select count(0) from vote_log where vtype in (2,3)"
    result=dbc.fetchonedb(sql)
    if result:
        tcount=result[0]
    votecontent=zzv.getvote(id=5)
    sql="update vote_pv set vcount=vcount+1 where id=%s"
    dbc.updatetodb(sql,[5])
    pcount=zzv.getvotecount(detail['company_id'],vtype)
    return render_to_response("vote/621/cgs-view.html",locals())

def vote_check(request):
    weixinid=request.GET.get("weixinid")
    randomnum=request.GET.get("randomnum")
    if weixinid and randomnum:
        sqlw="select id from vote_yzm where weixinid=%s and randomnum=%s and TIMESTAMPDIFF(SECOND,gmt_modified,NOW())<60"
        result=dbc.fetchonedb(sqlw,[weixinid,randomnum])
        if result:
            sqlb="update vote_yzm set checked=1 where weixinid=%s"
            dbc.updatetodb(sqlb,[weixinid])
            messagedata={'err':'false','errkey':''}
            return HttpResponse(simplejson.dumps(messagedata, ensure_ascii=False))
        else:
            messagedata={'err':'true','errkey':'验证码错误或已经过期，请在微信里重新点击“我要投票”'}
            return HttpResponse(simplejson.dumps(messagedata, ensure_ascii=False))
def vote(request):
    #clientid_fw=request.GET.get("openid")
    clientid_fw=request.session.get("openid_fw",None)
    clientid_dy=request.session.get("openid_dy",None)
    vtype=request.GET.get("vtype")
    company_id=request.GET.get("company_id")
    gmt_created=gmt_modified=datetime.datetime.now()
    gmt_date=formattime(gmt_created,1)
    
    sql="select vtodate,vfromdate from vote_pv where vtype=%s"
    result=dbc.fetchonedb(sql,[vtype])
    if result:
        todate=result[0]
        todate=formattime(todate,1)
        vfromdate=result[1]
        vfromdate=formattime(vfromdate,1)
        
    if str_to_int(gmt_date)<str_to_int(vfromdate):
        return HttpResponse('var _suggest_result_={"err":"true","errtext":"投票将在“'+str(vfromdate)+'”开始！","gz":0}')
    if str_to_int(gmt_date)>str_to_int(todate):
        return HttpResponse('var _suggest_result_={"err":"true","errtext":"投票已经结束！","gz":0}')
    if not vtype or str(vtype)=="0":
        return HttpResponse('var _suggest_result_={"err":"true","errtext":"投票已经结束！","gz":0}')
    
    if clientid_fw:
        sql="select openid_dy from weixin_bind where openid_fw=%s"
        result=dbc.fetchonedb(sql,[clientid_fw])
        if result:
            clientid_dy=openid_dy=result[0]
            if not openid_dy:
                return HttpResponse('var _suggest_result_={"err":"true","errtext":"长按二维码，识别二维码并关注后，点击菜单“我要投票”进行投票！","gz":1}')
        else:
            return HttpResponse('var _suggest_result_={"err":"true","errtext":"长按二维码，识别二维码并关注后，点击菜单“我要投票”进行投票！","gz":1}')
        
        sqlw="select id from vote_yzm where weixinid=%s and TIMESTAMPDIFF(SECOND,gmt_modified,NOW())<600 and checked=1"
        result=dbc.fetchonedb(sqlw,[request.session.get("openid_dy",None)])
        if not result:
            return HttpResponse('var _suggest_result_={"err":"true","errtext":"请输入投票验证码！'+str(request.session.get("openid_dy",None))+'","gz":2}')
        #投票
        sql="select count(0) from vote_log where clientid=%s and vtype=%s and gmt_date=%s"
        result=dbc.fetchonedb(sql,[clientid_dy,vtype,gmt_date])
        if result:
            vcount=result[0]
            if vcount>=3:
                return HttpResponse('var _suggest_result_={"err":"true","errtext":"您今天投票已经超过3次，请明天再投！","gz":0}')
            else:
                if company_id:
                    sql="insert into vote_log(forcompany_id,clientid,gmt_date,gmt_created,vtype) values(%s,%s,%s,%s,%s)"
                    dbc.updatetodb(sql,[company_id,clientid_dy,gmt_date,gmt_created,vtype])
                    sql="select count(0) from vote_log where forcompany_id=%s and vtype=%s"
                    result=dbc.fetchonedb(sql,[company_id,vtype])
                    if result:
                        vcount=result[0]
                        sql="update vote_list set votecount=%s where company_id=%s and vtype=%s"
                        dbc.updatetodb(sql,[vcount,company_id,vtype])
                        return HttpResponse('var _suggest_result_={"err":"false","vcount":"'+str(vcount)+'"}')
                return HttpResponse('var _suggest_result_={"err":"true","errtext":"系统错误！请重试！","gz":0}')
    else:
        return HttpResponse('var _suggest_result_={"err":"true","errtext":"长按二维码，请关注后，点击菜单“我要投票”进行投票！","gz":1}')
#投票排名
def voteranking(request):
    gmt_created=gmt_modified=datetime.datetime.now()
    gmt_date=formattime(gmt_created,0)
    vtype=request.GET.get("vtype")
    if vtype:
        sql="select id,company_name,orderid,votecount,company_id from vote_list where vtype=%s order by votecount desc"
        result=dbc.fetchalldb(sql,[vtype])
        listall=[]
        if result:
            n=1
            for list in result:
                company_name=list[1]
                orderid=list[2]
                votecount=zzv.getvotecount(list[4])
                sqlc="update vote_list set votecount=%s where id=%s"
                dbc.updatetodb(sqlc,[votecount,list[0]])
                ll={'n':n,'company_name':company_name,'orderid':orderid,'votecount':votecount}
                listall.append(ll)
                n=n+1
    return render_to_response("vote/ranking.html",locals())

#投票排名
def jsvoteranking(request):
    gmt_created=gmt_modified=datetime.datetime.now()
    gmt_date=formattime(gmt_created,0)
    vtype=request.GET.get("vtype")
    if vtype:
        sql="select id,company_name,orderid,votecount,company_id from vote_list where vtype=%s order by votecount desc"
        result=dbc.fetchalldb(sql,[vtype])
        listall=[]
        if result:
            n=1
            for list in result:
                company_name=list[1]
                orderid=list[2]
                votecount=zzv.getvotecount(list[4],1)
                sqlc="update vote_list set votecount=%s where id=%s"
                dbc.updatetodb(sqlc,[votecount,list[0]])
                ll={'n':n,'company_name':company_name,'orderid':orderid,'votecount':votecount}
                listall.append(ll)
                n=n+1
    return render_to_response("vote/jsranking.html",locals())

#投票公共模式
def vote_comm_list(request,votename=''):
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
    
    clientid_fw=request.session.get("openid_fw",None)
    clientid_dy=request.session.get("openid_dy",None)
    
    sql="select id,vtype from vote_pv where forno=%s"
    result=dbc.fetchonedb(sql,[votename])
    if result:
        vtype=result[1]
        countid=result[0]
        vcount=998
    else:
        return HttpResponse("错误")
    
    if not clientid_fw:
        return HttpResponseRedirect("/wechat/auth_login.html?tourl=/vote/v"+votename+"/list.html")
    keywords=request.GET.get("keywords")
    
    #入围企业
    ccount=0
    sql="select count(0) from vote_list where vtype=%s"
    result=dbc.fetchonedb(sql,[vtype])
    if result:
        ccount=result[0]
    #访问量
    vcount=0
    sql="select sum(vcount) from vote_pv where id =%s"
    result=dbc.fetchonedb(sql,[countid])
    if result:
        vcount=result[0]
    #投票量
    tcount=0
    sql="select count(0) from vote_log where vtype=%s"
    result=dbc.fetchonedb(sql,[vtype])
    if result:
        tcount=result[0]
    
    vlist=zzv.votelist(0,100,keywords=keywords,vtype=vtype)
    listall=vlist['list']
    count=vlist['count']
    openid=request.GET.get("openid")
    
    sql="update vote_pv set vcount=vcount+1 where id=%s"
    dbc.updatetodb(sql,[countid])
    votecontent=zzv.getvote(id=countid)
    vcount=votecontent['vcount']
        
    return render_to_response("vote/"+votename+"/list.html",locals())
#投票排名
def vote_comm_sort(request,votename=''):
    sql="select id,vtype from vote_pv where forno=%s"
    result=dbc.fetchonedb(sql,[votename])
    if result:
        vtype=result[1]
        countid=result[0]
        vcount=998
    else:
        return HttpResponse("错误")
    
    #入围企业
    ccount=0
    sql="select count(0) from vote_list where vtype=%s"
    result=dbc.fetchonedb(sql,[vtype])
    if result:
        ccount=result[0]
    """
    #访问量
    vcount=0
    sql="select sum(vcount) from vote_pv where id =%s"
    result=dbc.fetchonedb(sql,[countid])
    if result:
        vcount=result[0]
    #投票量
    tcount=0
    sql="select count(0) from vote_log where vtype=%s"
    result=dbc.fetchonedb(sql,[vtype])
    if result:
        tcount=result[0]
    """
    gmt_created=gmt_modified=datetime.datetime.now()
    gmt_date=formattime(gmt_created,0)
    votecontent=zzv.getvote(id=countid)
    if vtype:
        sql="select id,company_name,orderid,votecount,company_id from vote_list where vtype=%s order by votecount desc"
        result=dbc.fetchalldb(sql,[vtype])
        listall=[]
        if result:
            n=1
            for list in result:
                id=list[0]
                company_name=list[1]
                orderid=list[2]
                votecount=zzv.getvotecount(list[4],vtype)
                sqlc="update vote_list set votecount=%s where id=%s"
                dbc.updatetodb(sqlc,[votecount,list[0]])
                ll={'id':id,'n':n,'company_name':company_name,'orderid':orderid,'votecount':votecount}
                listall.append(ll)
                n=n+1
    sql="update vote_pv set vcount=vcount+1 where id=%s"
    dbc.updatetodb(sql,[countid])
    return render_to_response("vote/"+str(votename)+"/sort.html",locals())
#投票公司详情
def vote_comm_view(request,vid,votename=''):
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
    
    sql="select id,vtype from vote_pv where forno=%s"
    result=dbc.fetchonedb(sql,[votename])
    if result:
        vtype=result[1]
        countid=result[0]
    else:
        return HttpResponse("错误")
    
    id=vid
    
    clientid_fw=request.session.get("openid_fw",None)
    clientid_dy=request.session.get("openid_dy",None)
    if not clientid_fw:
        return HttpResponseRedirect("/wechat/auth_login.html?tourl=/vote/v"+str(votename)+"/view"+str(id)+".html")
    detail=zzv.getvotedetail(id)
    #入围企业
    ccount=0
    sql="select count(0) from vote_list where vtype=%s"
    result=dbc.fetchonedb(sql,[vtype])
    if result:
        ccount=result[0]
    #访问量
    vcount=0
    sql="select sum(vcount) from vote_pv where id =%s"
    result=dbc.fetchonedb(sql,[countid])
    if result:
        vcount=result[0]
    #投票量
    tcount=0
    sql="select count(0) from vote_log where vtype=%s"
    result=dbc.fetchonedb(sql,[vtype])
    if result:
        tcount=result[0]
    votecontent=zzv.getvote(id=countid)
    pcount=zzv.getvotecount(detail['company_id'],vtype)
    sql="update vote_pv set vcount=vcount+1 where id=%s"
    dbc.updatetodb(sql,[countid])
    return render_to_response("vote/"+str(votename)+"/view.html",locals())
