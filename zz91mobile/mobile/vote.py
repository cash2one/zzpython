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
execfile(nowpath+"/func/vote_function.py")
execfile(nowpath+"/function.py")

from zzwx.client import Client
zzmain=zmain()
zzcompany=zcompany()
zzv=zvote()

def index(request):
    clientid_fw=request.session.get("clientid_fw",None)
    clientid_dy=request.session.get("clientid_dy",None)
    keywords=request.GET.get("keywords")
    qianbao_gglist=zzv.votelist(0,100,keywords=keywords)
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

def vote(request):
    #clientid_fw=request.GET.get("openid")
    clientid_fw=request.session.get("clientid_fw",None)
    clientid_dy=request.session.get("clientid_dy",None)
    company_id=request.GET.get("company_id")
    gmt_created=gmt_modified=datetime.datetime.now()
    gmt_date=formattime(gmt_created,1)
    return HttpResponse('var _suggest_result_={"err":"true","errtext":"投票已经结束！","gz":0}')
    if clientid_dy:
        sql="select id,clientid_fw from vote_visit_log where clientid_dy=%s"
        result=dbc.fetchonedb(sql,clientid_dy)
        if not result:
            sql="insert into vote_visit_log(clientid_dy,clientid_fw,gmt_created) values(%s,%s,%s)"
            dbc.updatetodb(sql,[clientid_dy,clientid_fw,gmt_created])
        else:
            myclientid_fw=result[1]
            if clientid_fw!=myclientid_fw:
                return HttpResponse('var _suggest_result_={"err":"true","errtext":"您还未关注微信公众号，请关注后，点击“我要投票”进行投票！","gz":1}')
            
        #投票
        sql="select count(0) from vote_log where clientid=%s and gmt_date=%s"
        result=dbc.fetchonedb(sql,[clientid_dy,gmt_date])
        if result:
            vcount=result[0]
            if vcount>=3:
                return HttpResponse('var _suggest_result_={"err":"true","errtext":"您今天投票已经超过3次，请明天再投！","gz":0}')
            else:
                if company_id:
                    sql="insert into vote_log(forcompany_id,clientid,gmt_date,gmt_created) values(%s,%s,%s,%s)"
                    dbc.updatetodb(sql,[company_id,clientid_dy,gmt_date,gmt_created])
                    sql="select count(0) from vote_log where forcompany_id=%s"
                    result=dbc.fetchonedb(sql,[company_id])
                    if result:
                        vcount=result[0]
                        sql="update vote_list set votecount=%s where company_id=%s"
                        dbc.updatetodb(sql,[vcount,company_id])
                        return HttpResponse('var _suggest_result_={"err":"false","vcount":"'+str(vcount)+'"}')
                return HttpResponse('var _suggest_result_={"err":"true","errtext":"系统错误！请重试！","gz":0}')
    else:
        return HttpResponse('var _suggest_result_={"err":"true","errtext":"还未关注微信公众号，请关注后，点击“我要投票”进行投票！","gz":1}')

def voteranking(request):
    gmt_created=gmt_modified=datetime.datetime.now()
    gmt_date=formattime(gmt_created,0)
    sql="select id,company_name,orderid,votecount,company_id from vote_list order by votecount desc"
    result=dbc.fetchalldb(sql)
    listall=[]
    if result:
        n=1
        for list in result:
            company_name=list[1]
            orderid=list[2]
            votecount=zzv.votecount(list[4])
            sqlc="update vote_list set votecount=%s where id=%s"
            dbc.updatetodb(sqlc,[votecount,list[0]])
            ll={'n':n,'company_name':company_name,'orderid':orderid,'votecount':votecount}
            listall.append(ll)
            n=n+1
    return render_to_response("vote/ranking.html",locals())
