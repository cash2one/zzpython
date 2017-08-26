#-*- coding:utf-8 -*-
from django.shortcuts import render_to_response
from django.http import HttpResponse,HttpResponseRedirect,HttpResponseNotFound,HttpResponsePermanentRedirect
from django.views.decorators.csrf import csrf_exempt
from django.core.cache import cache
from zz91settings import SPHINXCONFIG,weixinconfig
from zz91tools import filter_tags,getjiami,getjiemi,subString,formattime,getpastday,int_to_str,int_to_str2,str_to_int,str_to_date,date_to_int,date_to_str,getpastoneday,getnextdate,getTomorrow,mobileuseragent
from zz91db_ast import companydb
from zz91db_2_news import newsdb
from zz91page import *
from sphinxapi import *
import MySQLdb,os,datetime,time,sys,calendar,urllib,simplejson
from zzwx.client import Client
dbc=companydb()
dbn=newsdb()
reload(sys)
sys.setdefaultencoding('UTF-8')
nowpath=os.path.dirname(__file__)
execfile(nowpath+"/zhibo_func.py")
zzzhibo=zhibofun()
def zhibo(request):
    orderflag1=request.GET.get("orderflag")
    mobileflag=request.GET.get("mobileflag")
    orderflag=0
    if not orderflag1:
        orderflag1=""
    if not orderflag1:
        orderflag="1"
    if str(orderflag1)=="0":
        orderflag="1"
    if str(orderflag1)=="1":
        orderflag="0"
    zzzhibo.huzhuclick_add(680765)
    #zhibolist=zzzhibo.getzhibolist(0,10,orderflag=orderflag)['list']
    pinlunlist=zzzhibo.replylist(680765,0,10)
    if mobileflag:
        return render_to_response('zhibo/m-index.html',locals())
    return render_to_response('zhibo/index.html',locals())

def zhibo_pinlun_save(request):
    zzzhibo.huzhu_replay(request)
    rerult={'err':''}
    return HttpResponse(simplejson.dumps(rerult, ensure_ascii=False))
def zhibo_pinluncount(request):
    visited_count=0
    postid=680765
    sql="select visited_count from bbs_post where id=%s"
    result=dbc.fetchonedb(sql,[postid])
    if result:
        visited_count=result[0]
    rcount=0
    sql="select count(0) from bbs_post_reply where bbs_post_id=%s and is_del='0' and check_status in ('1','2') "
    result=dbc.fetchonedb(sql,[postid])
    if result:
        rcount=result[0]
    rerult={'visited_count':visited_count,'rcount':rcount}
    return HttpResponse(simplejson.dumps(rerult, ensure_ascii=False))
def zhibo_pinlun_more(request):
    page=request.GET.get("page")
    mobileflag=request.GET.get("mobileflag")
    if not page:
        page=1
    else:
        page=int(page)
    pinlunlist=zzzhibo.replylist(680765,(page-1)*10,10)
    if mobileflag:
        return render_to_response('zhibo/m-pinlun_more.html',locals())
    return render_to_response('zhibo/pinlun_more.html',locals())

def zhibo_more(request):
    page=request.GET.get("page")
    orderflag1=request.GET.get("orderflag")
    mobileflag=request.GET.get("mobileflag")
    orderflag=0
    if not orderflag1:
        orderflag1=""
    if not orderflag1:
        orderflag="1"
    if str(orderflag1)=="0":
        orderflag="1"
    if str(orderflag1)=="1":
        orderflag="0"
    if not page:
        page=1
    else:
        page=int(page)
    zhibolist=zzzhibo.getzhibolist((page-1)*10,10,orderflag=orderflag,bbs_post_id='680765')['list']
    if mobileflag:
        return render_to_response('zhibo/m-zhibo_more.html',locals())
    return render_to_response('zhibo/zhibo_more.html',locals())

#专题资讯公用
def comm_newslist(request):
    page=request.GET.get("page")
    num=request.GET.get("num")
    if not num:
        num=10
    if not page:
        page=1
    else:
        page=int(page)
    newstypeid=request.GET.get("newstypeid")
    newslist=zzzhibo.getnewslist(frompageCount=(page-1)*10,limitNum=int(num),typeid=185,typeid2=newstypeid)
    return HttpResponse(simplejson.dumps(newslist, ensure_ascii=False))

#公用直播
def comm_zhibolist(request):
    page=request.GET.get("page")
    if not page:
        page=1
    else:
        page=int(page)
    num=request.GET.get("num")
    if not num:
        num=10
    ztype=request.GET.get("ztype")
    zhibolist=zzzhibo.getzhibolist((page-1)*10,int(num),ztype=ztype,orderflag=1)
    return HttpResponse(simplejson.dumps(zhibolist, ensure_ascii=False))

#621 专题

def fh621_index(request):
    zhibolist=zzzhibo.getzhibolist(0,5,ztype='20170621')
    qiandaolist=zzzhibo.zsh_qiandaolist(0,100,ztype='20170621')
    list={'zhibolist':zhibolist,'qiandaolist':qiandaolist}
    return HttpResponse(simplejson.dumps(list, ensure_ascii=False))
#621资讯
def fh621_news(request):
    zhibolist=zzzhibo.getzhibolist(0,10,ztype='20170621')
    qiandaolist=zzzhibo.zsh_qiandaolist(0,100,ztype='20170621')
    newslist=zzzhibo.getnewslist(frompageCount=0,limitNum=30,typeid=185,typeid2=394)
    list={'newslist':newslist,'qiandaolist':qiandaolist,'zhibolist':zhibolist}
    return HttpResponse(simplejson.dumps(list, ensure_ascii=False))
#更多直播
def fh621_zhibo_more(request):
    page=request.GET.get("page")
    if not page:
        page=1
    else:
        page=int(page)
    zhibolist=zzzhibo.getzhibolist((page-1)*10,10,ztype='20170621')
    return HttpResponse(simplejson.dumps(zhibolist, ensure_ascii=False))

#抽奖用户列表
def fh621_luck(request):
    sql="select a.zheng_no,b.isluky from zsh_list as a LEFT OUTER JOIN zsh_choujian as b on a.zheng_no=b.zheng_no where (b.isluky is null or  b.isluky=0) and b.isqiandao=1"
    result=dbc.fetchalldb(sql)
    listall=[]
    if result:
        for list in result:
            zheng_no=list[0]
            listall.append(zheng_no)
    return HttpResponse(simplejson.dumps(listall, ensure_ascii=False))

#抽中
def fh621_luck_save(request):
    zheng_no=request.GET.get("zheng_no")
    delflag=request.GET.get("delflag")
    gmt_created=datetime.datetime.now()
    if delflag:
        sql="select id from zsh_choujian where zheng_no=%s"
        result=dbc.fetchonedb(sql,[zheng_no])
        if result:
            sql="select clientid from zsh_list where zheng_no=%s"
            result=dbc.fetchonedb(sql,[zheng_no])
            if result:
                weixinid=result[0]
                if weixinid:
                    suctext="因你未能在摇奖现场！很抱歉，我们已经将您的抽奖机会取消。"
                    wxc = Client(weixinconfig['zaishenghui']['appid'], weixinconfig['zaishenghui']['secret'])
                    token=wxc.send_text_message(weixinid,suctext)
        list={'err':'false','errkey':''}
    else:
        sql="select id from zsh_choujian where zheng_no=%s"
        result=dbc.fetchonedb(sql,[zheng_no])
        if result:
            sql="update zsh_choujian set isluky=1 where zheng_no=%s"
            dbc.updatetodb(sql,[zheng_no])
            sql="select clientid from zsh_list where zheng_no=%s"
            result=dbc.fetchonedb(sql,[zheng_no])
            if result:
                weixinid=result[0]
                if weixinid:
                    suctext="恭喜您已获砸金蛋机会，砸金蛋赢大奖活动等着您！"
                    wxc = Client(weixinconfig['zaishenghui']['appid'], weixinconfig['zaishenghui']['secret'])
                    token=wxc.send_text_message(weixinid,suctext)
            list={'err':'false','errkey':''}
        else:
            list={'err':'true','errkey':'此参展证没有签到'}
    return HttpResponse(simplejson.dumps(list, ensure_ascii=False))
def fh621_zajindanlist(request):
    clear=request.GET.get("clear")
    if clear:
        sql="delete from zsh_choujian_jiangpin where id>%s"
        dbc.updatetodb(sql,[0])
    sql="select num,jiangpin from zsh_choujian_jiangpin"
    result=dbc.fetchalldb(sql)
    listall=[]
    if result:
        for list in result:
            l={'num':list[0],'jiangpin':list[1]}
            listall.append(l)
    return HttpResponse(simplejson.dumps(listall, ensure_ascii=False))
#砸金蛋
def fh621_zajindan(request):
    ztype="20170621"
    num=request.GET.get("num")
    jiangpin=request.GET.get("jiangpin")
    sql="select id from zsh_choujian_jiangpin where num=%s"
    result=dbc.fetchonedb(sql,[num])
    if not result:
        sql="insert into zsh_choujian_jiangpin(num,jiangpin) values(%s,%s)"
        dbc.updatetodb(sql,[num,jiangpin])
    else:
        sql="update zsh_choujian_jiangpin set jiangpin=%s where num=%s"
        dbc.updatetodb(sql,[jiangpin,num])
    list={'err':'false','errkey':''}
    return HttpResponse(simplejson.dumps(list, ensure_ascii=False))
        
#参会企业
def chcompanylist(request):
    votename="2017823feizhi"
    votename=request.GET.get("votename")
    sql="select id,vtype from vote_pv where forno=%s"
    result=dbc.fetchonedb(sql,[votename])
    if result:
        vtype=result[1]
        countid=result[0]
    else:
        list={'err':'true','errkey':''}
        return HttpResponse(simplejson.dumps(list, ensure_ascii=False))
    sql="select id,company_name,orderid,votecount,company_id,business from vote_list where vtype=%s order by orderid asc"
    result=dbc.fetchalldb(sql,[vtype])
    listall=[]
    if result:
        n=1
        for list in result:
            id=list[0]
            company_name=list[1]
            orderid=list[2]
            company_id=list[4]
            sqlc="select count(0) from vote_log where forcompany_id=%s and vtype=%s"
            resultc=dbc.fetchonedb(sqlc,[company_id,vtype])
            votecount=resultc[0]
            business=list[5]
            ll={'id':id,'company_name':company_name,'orderid':orderid,'votecount':votecount,'business':business}
            listall.append(ll)
    return HttpResponse(simplejson.dumps(listall, ensure_ascii=False))
    