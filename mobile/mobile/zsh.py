#-*- coding:utf-8 -*-
from django.shortcuts import render_to_response
from django.http import HttpResponse,HttpResponseRedirect,HttpResponsePermanentRedirect
import MySQLdb,sys,os,memcache,settings,urllib,re,time,datetime,requests,random,string,md5,hashlib,simplejson
from django.core.cache import cache
from sphinxapi import *
from zz91page import *
from settings import spconfig
from zz91settings import SPHINXCONFIG,weixinconfig
from commfunction import filter_tags,formattime,havepicflag,subString,getjiami,getIPFromDJangoRequest,validateEmail
from zz91tools import int_to_str,str_to_int
from datetime import timedelta, date 
from zz91db_ast import companydb
from zz91db_sms import smsdb
dbc=companydb()
dbsms=smsdb()
reload(sys)
sys.setdefaultencoding('UTF-8')
nowpath=os.path.dirname(__file__)
execfile(nowpath+"/func/main_function.py")
execfile(nowpath+"/func/company_function.py")
execfile(nowpath+"/function.py")
#from zzwx.client import Client
zzc=zcompany()
def index(request):
    clientid_fw=request.session.get("openid_fw",None)
    clientid_dy=request.session.get("openid_dy",None)
    zshclientid=request.GET.get("clientid")
    if zshclientid:
        request.session['zshclientid']=zshclientid
    if not clientid_fw:
        return HttpResponseRedirect("/wechat/auth_login.html?tourl=/zsh/index.html")
    if clientid_fw:
        ztype="20170823"
        sql="select id,clientid from zsh_list where weixinid=%s and ztype=%s and isqiandao=1"
        result=dbc.fetchonedb(sql,[clientid_fw,ztype])
        if result:
            id=result[0]
            clientid=result[1]
            if not clientid:
                sql="update zsh_list set clientid=%s where id=%s"
                dbc.updatetodb(sql,[zshclientid,id])
            return HttpResponseRedirect("qiandao_suc.html?id="+str(id))
    return render_to_response("aui/zsh/qiandao.html",locals())
#签到
def qiandao_save(request):
    clientid_fw=request.session.get("openid_fw",None)
    zshclientid=request.session.get("zshclientid",None)
    if not clientid_fw:
        return HttpResponseRedirect("/zsh/")
    mobile=request.GET.get("mobile")
    gmt_created=gmt_modified=datetime.datetime.now()
    gmt_date=formattime(gmt_created,1)
    vfromdate="2017-8-23"
    if str_to_int(gmt_date)<str_to_int(vfromdate):
        res={'err':'true','errkey':'请在2017-8-23日当天签到。','type':'nostart'}
        res=simplejson.dumps(res,ensure_ascii=False)
        #return HttpResponse(res)
    if len(mobile)<11 and len(mobile)>12:
        res={'err':'true','errkey':'手机号码有误。','type':''}
        res=simplejson.dumps(res,ensure_ascii=False)
        return HttpResponse(res)
    if clientid_fw:
        ztype="20170823"
        sql="select id from zsh_list where weixinid=%s and ztype=%s and isqiandao=1"
        result=dbc.fetchonedb(sql,[clientid_fw,ztype])
        if result:
            id=result[0]
            res={'err':'true','errkey':'您的微信号已经签到，无需重复签到！','type':'havereg'}
            res=simplejson.dumps(res,ensure_ascii=False)
            return HttpResponse(res)
    ztype="20170823"
    sql="select id,isqiandao,weixinid from zsh_list where mobile=%s and ztype=%s"
    result=dbc.fetchonedb(sql,[mobile,ztype])
    if not result:
        res={'err':'true','errkey':'错误','type':'noreg'}
    else:
        isqiandao=result[1]
        id=result[0]
        weixinid=result[2]
        if not weixinid:
            if str(isqiandao)=="0":
                qiandaotime=gmt_modified=datetime.datetime.now()
                sqlu="update zsh_list set isqiandao=1,qiandaotime=%s,weixinid=%s,gmt_modified=%s,clientid=%s where id=%s"
                dbc.updatetodb(sqlu,[qiandaotime,clientid_fw,gmt_modified,zshclientid,id])
            res={'err':'false','errkey':'','id':id}
        else:
            if weixinid!=clientid_fw:
                res={'err':'true','errkey':'已经签到，无需重复签到！','type':'havereg'}
    res=simplejson.dumps(res,ensure_ascii=False)
    return HttpResponse(res)
#签到成功
def qiandao_suc(request):
    id=request.GET.get("id")
    clientid_fw=request.session.get("openid_fw",None)
    paysuc=request.GET.get("paysuc")
    if not clientid_fw:
        return HttpResponseRedirect("/zsh/")
    
    paymoney="500"
    sql="select id,isqiandao,companyname,mobile,contact,business,ispay,mobile,company_id,weixinid,zheng_no from zsh_list where id=%s"
    result=dbc.fetchonedb(sql,[id])
    if result:
        isqiandao=result[1]
        id=result[0]
        companyname=result[2]
        business=result[5]
        contact=result[4]
        ispay=str(result[6])
        mobile=result[7]
        company_id=result[8]
        weixinid=result[9]
        zheng_no=result[10]
        if weixinid!=clientid_fw:
            return HttpResponseRedirect("/zsh/")
        if company_id and str(company_id)!="0":
            iszst=getiszstcompany(company_id)
            if iszst:
                paymoney="500"
    else:
        return HttpResponseRedirect("/zsh/")
    backurl="http://m.zz91.com/zsh/qiandao_suc.html?paysuc=1&id="+str(id)
    return render_to_response("aui/zsh/qiandao_suc.html",locals())

#未登记签到（现场签到）
def qiandao_noreg(request):
    mobile=request.GET.get("mobile")
    clientid_fw=request.session.get("openid_fw",None)
    if not clientid_fw:
        return HttpResponseRedirect("/zsh/")
    sql="select a.id,a.name,a.business,b.contact from company as a left join company_account as b on a.id=b.company_id where b.mobile=%s"
    result=dbc.fetchonedb(sql,[mobile])
    companyname=''
    business=''
    contact=''
    paymoney="500"
    company_id=0
    if result:
        company_id=result[0]
        companyname=result[1]
        business=result[2]
        contact=result[3]
        if business:
            business=business[0:100]
        
    return render_to_response("aui/zsh/qiandao_noreg.html",locals())
#未登记签到
def qiandao_noreg_save(request):
    clientid_fw=request.session.get("openid_fw",None)
    zshclientid=request.session.get("zshclientid",None)
    if not clientid_fw:
        return HttpResponseRedirect("/zsh/")
    if clientid_fw:
        ztype="20170823"
        sql="select id from zsh_list where weixinid=%s and ztype=%s and isqiandao=1"
        result=dbc.fetchonedb(sql,[clientid_fw,ztype])
        if result:
            id=result[0]
            res={'err':'true','errkey':'您的微信号已经签到，无需重复签到！','type':'havereg'}
            res=simplejson.dumps(res,ensure_ascii=False)
            return HttpResponse(res)
    ztype="20170823"
    companyname=request.GET.get("companyname")
    if companyname:
        companyname=companyname[0:300]
    contact=request.GET.get("contact")
    mobile=request.GET.get("mobile")
    business=request.GET.get("business")
    if business:
        business=business[0:1000]
    company_id=request.GET.get("company_id")
    fee=0
    personnum=1
    paytype=''
    isqiandao=1
    isnowin=1
    paytime=datetime.datetime.now()
    qiandaotime=gmt_modified=datetime.datetime.now()
    zheng_no=1000
    sql="select max(zheng_no)+1 as zheng_no from zsh_list"
    result=dbc.fetchonedb(sql)
    if result:
        zheng_no=result[0]
    sql="insert into zsh_list(zheng_no,ztype,weixinid,clientid,companyname,contact,mobile,business,fee,personnum,paytype,paytime,qiandaotime,isqiandao,isnowin,company_id,gmt_modified) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
    result=dbc.updatetodb(sql,[zheng_no,ztype,clientid_fw,zshclientid,companyname,contact,mobile,business,fee,personnum,paytype,paytime,qiandaotime,isqiandao,isnowin,company_id,gmt_modified])
    id=result[0]
    res={'err':'false','errkey':'','id':id}
    res=simplejson.dumps(res,ensure_ascii=False)
    return HttpResponse(res)

#抽奖签到
def choujiangqiandao(request):
    clientid_fw=request.session.get("openid_fw",None)
    clientid_dy=request.session.get("openid_dy",None)
    if not clientid_fw:
        return HttpResponseRedirect("/wechat/auth_login.html?tourl=/zsh/choujiangqiandao.html")
    if clientid_fw:
        gmt_created=datetime.datetime.now()
        gmt_date=formattime(gmt_created,0)
        vfromdate="2017-8-23 18:00:00"
        if str_to_int(gmt_date)<str_to_int(vfromdate):
            errtext="晚宴签到时间18：00开始"
        else:
            ztype="20170823"
            sql="select id,isqiandao,companyname,mobile,contact,business,ispay,mobile,company_id,weixinid,zheng_no from zsh_list where weixinid=%s and ztype=%s and isqiandao=1 and ispay=1"
            result=dbc.fetchonedb(sql,[clientid_fw,ztype])
            if result:
                cqiandaoflag=1
                isqiandao=result[1]
                id=result[0]
                companyname=result[2]
                business=result[5]
                contact=result[4]
                ispay=str(result[6])
                mobile=result[7]
                company_id=result[8]
                weixinid=result[9]
                zheng_no=result[10]
                sql="select id from zsh_choujian where zheng_no=%s"
                result1=dbc.fetchonedb(sql,[zheng_no])
                if not result1:
                    sql="insert into zsh_choujian(zheng_no,isqiandao,isluky,gmt_created) values(%s,%s,%s,%s)"
                    dbc.updatetodb(sql,[zheng_no,1,0,gmt_created])
                else:
                    sql="update zsh_choujian set isqiandao=1 where zheng_no=%s"
                    dbc.updatetodb(sql,[zheng_no])
            else:
                errtext="您还未签到或付款，请联系展会工作人员。"
                cqiandaoflag=None
        
    return render_to_response("aui/zsh/choujiangqiandao.html",locals())
    
#团购首页
def groupbuy_index(request):
    joinstatus5=None
    joinstatus10=None
    #我是否已经参团
    company_id=request.session.get("company_id",None)
    if company_id:
        sql="select id,ispay from subject_groupbuy_join where company_id=%s and grouptype=5 and ispay=1"
        result=dbc.fetchonedb(sql,[company_id])
        if result:
            joinstatus5=1
        sql="select id,ispay from subject_groupbuy_join where company_id=%s and grouptype=10 and ispay=1"
        result=dbc.fetchonedb(sql,[company_id])
        if result:
            joinstatus10=1
    return render_to_response("subject/tuangou/groupbuy.html",locals())
#团购详情
def groupbuy_detail(request):
    backurl=request.META.get('HTTP_REFERER','/')
    host=getnowurl(request)
    username=request.session.get("username",None)
    company_id=request.session.get("company_id",None)
    if username and (company_id==None or str(company_id)=="0"):
        company_id=getcompanyid(username)
        request.session['company_id']=company_id
    if (username==None or (company_id==None or str(company_id)=="0")):
        return HttpResponseRedirect("/login/?done="+host)
    grouptype=request.GET.get("grouptype")
    #是否已经组团
    sql="select id from subject_groupbuy where company_id=%s and grouptype=%s"
    result=dbc.fetchonedb(sql,[company_id,grouptype])
    if result:
        return HttpResponseRedirect("success"+str(result[0])+".html")
    if grouptype=="5":
        price=400
        gimg="http://static.m.zz91.com/subject/tuangou/images/tuang-img1.png"
    if grouptype=="10":
        price=350
        gimg="http://static.m.zz91.com/subject/tuangou/images/tuang-img8.png"
    return render_to_response("subject/tuangou/groupbuy_detail.html",locals())
def groupbuy_success(request,gid=""):
    if gid:
        sql="select id,personnum,grouptype,gmt_created,price from subject_groupbuy where id=%s"
        result=dbc.fetchonedb(sql,[gid])
        if result:
            personnum=result[1]
            grouptype=str(result[2])
            creategrouptime=formattime(result[3],0)
            price=result[4]
            if not price:
                price=0
            if grouptype=="5":
                gimg="http://static.m.zz91.com/subject/tuangou/images/tuang-img2.png"
            if grouptype=="10":
                gimg="http://static.m.zz91.com/subject/tuangou/images/tuang-img9.png"
            
            sqlg="select count(0) from subject_groupbuy_join where groupbuy_id=%s and ispay=1"
            resultg=dbc.fetchonedb(sqlg,[gid])
            joincount=resultg[0]
            #还差多少人
            havecount=int(personnum)-joincount
            #参团人员
            sql="select a.company_id,b.contact from subject_groupbuy_join as a left join company_account as b on a.company_id=b.company_id where a.groupbuy_id=%s and a.ispay=1"
            resultlist=dbc.fetchalldb(sql,[gid])
            listall=[]
            for list in resultlist:
                facepic=zzc.getfacepic(list[0])
                list={'company_id':list[0],'contact':list[1],'facepic':facepic}
                listall.append(list)
            nojoinlist=range(0,havecount)
            
            joinstatus=0
            #我是否已经参团
            company_id=request.session.get("company_id",None)
            if company_id:
                sql="select id,ispay from subject_groupbuy_join where groupbuy_id=%s and company_id=%s and ispay=1"
                result=dbc.fetchonedb(sql,[gid,company_id])
                if result:
                    ispay=result[1]
                    joinstatus=1
            #组团成功
            if havecount==0:
                joinstatus=2
            
            #组团失败过期
            gmt_created=datetime.datetime.now()
            gmt_date=formattime(gmt_created,0)
            vfromdate="2017-8-10"
            leprice=500-int(price)
            if str_to_int(gmt_date)>str_to_int(vfromdate):
                joinstatus=3
            
    return render_to_response("subject/tuangou/groupbuy_success.html",locals())
#保存组团购
def groupbuy_detail_save(request):
    backurl=request.META.get('HTTP_REFERER','/')
    host=getnowurl(request)
    username=request.session.get("username",None)
    company_id=request.session.get("company_id",None)
    if username and (company_id==None or str(company_id)=="0"):
        company_id=getcompanyid(username)
        request.session['company_id']=company_id
    if (username==None or (company_id==None or str(company_id)=="0")):
        return HttpResponseRedirect("/login/?done="+host)
    grouptype=request.GET.get("grouptype")
    gmt_created=datetime.datetime.now()
    isgroup=0
    price=500
    if grouptype=="5":
        price=400
    if grouptype=="10":
        price=350
    personnum=grouptype
    #组团
    sql="select id from subject_groupbuy where company_id=%s and grouptype=%s"
    result=dbc.fetchonedb(sql,[company_id,grouptype])
    if not result:
        sql="insert into subject_groupbuy(company_id,grouptype,price,isgroup,gmt_created,personnum) values(%s,%s,%s,%s,%s,%s)"
        resultg=dbc.updatetodb(sql,[company_id,grouptype,price,isgroup,gmt_created,personnum])
        groupbuy_id=''
        if resultg:
            groupbuy_id=resultg[0]
    else:
        groupbuy_id=result[0]
    if groupbuy_id:
        #写入参团表
        sql="select id,ispay from subject_groupbuy_join where company_id=%s and groupbuy_id=%s"
        result=dbc.fetchonedb(sql,[company_id,groupbuy_id])
        if not result:
            sql="insert into subject_groupbuy_join(company_id,groupbuy_id,grouptype,price,gmt_created) values(%s,%s,%s,%s,%s)"
            resultg=dbc.updatetodb(sql,[company_id,groupbuy_id,grouptype,price,gmt_created])
            buyer_id=0
            ispay=0
            if resultg:
                buyer_id=resultg[0]
        else:
            ispay=result[1]
            buyer_id=result[0]
        if str(ispay)=="0":
            return HttpResponseRedirect("/qianbao/chongzhi.html?money="+str(price)+"&paytype=groupbuy&buyer_id="+str(buyer_id))
        else:
            return HttpResponseRedirect("success"+str(groupbuy_id)+".html")
    
    
    