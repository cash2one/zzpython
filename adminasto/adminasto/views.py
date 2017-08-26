#-*- coding:utf-8 -*-
import MySQLdb    
import settings
import codecs
from django.utils.http import urlquote
from django.shortcuts import render_to_response
from django.http import HttpResponse,HttpResponseRedirect
from django.core.paginator import Paginator,InvalidPage,EmptyPage,PageNotAnInteger
import time,md5,hashlib,simplejson
import sys,json
import datetime
from datetime import timedelta, date 
from time import ctime, sleep
import os
from django.core.cache import cache
import random
import shutil
import urllib
import xlwt

try:
    import cPickle as pickle
except ImportError:
    import pickle
from math import ceil
from sphinxapi import *
from zz91page import *
reload(sys)
sys.setdefaultencoding('UTF-8')

nowpath=os.path.dirname(__file__)
execfile(nowpath+"/conn.py")
execfile(nowpath+"/function.py")

def default(request):
    return render_to_response('daohang_index.html',locals())
    closeconn()
def sendsmsflag(request):
    mobile=request.GET.get("mobile")
    flag=postsmsflag(mobile)
    return HttpResponse("var _suggest_result_={'result':'"+flag+"'}")
def sendsms(request):
    mobile=request.GET.get("mobile")
    company_id=request.GET.get("company_id")
    if len(mobile)==11 and getmobileaccount(company_id)==None:
        content="您好!欢迎关注ZZ91再生网，在微信中搜索zz91weixin关注我们，更多详情点击http://zz91.com/m-"
        result=postsms(mobile,content)
        return HttpResponse(result)
    else:
        return HttpResponse('err')
#开通申请单
def openConfirm(request):
    localhostIP=getlocalIP()
    personid = request.GET.get("personid")
    com_id= request.GET.get("com_id")
    username= request.GET.get("userName")
    com_name=request.GET.get("com_name")
    com_email=request.GET.get("com_email")
    return render_to_response('openConfirm.html',locals())
    closeconn()
def openConfirm1(request):
    localhostIP=getlocalIP()
    com_id= request.GET.get("com_id")
    #com_email=request.GET.get("com_email").strip()
    userid=request.GET.get("userid")
    mbflag=request.GET.get("mbflag")
    if (com_id!="" and com_id!=None):
        sqla="select name from company where id="+str(com_id)+""
        cursor.execute(sqla)
        newreturna=cursor.fetchone()
        com_name=""
        if (newreturna):
            com_name=newreturna[0].replace(" ","")
        sqla="select gmt_created,contact,mobile,num_login,email,account from company_account where company_id=%s"
        cursor.execute(sqla,[com_id])
        newreturna=cursor.fetchone()
        com_email=None
        if (newreturna):
            com_contactperson=str(com_name)+"("+newreturna[1]+")".replace(" ","")
            com_mobile=newreturna[2].replace(" ","")
            com_regtime=formattime(newreturna[0],0)
            com_logincount=newreturna[3]
            if newreturna[4]:
                com_email=newreturna[4].strip()
            else:
                com_email=""
            account=newreturna[5]
        else:
            return HttpResponse("该客户在外网不存在，选用其他账号！")
        if com_email==None:
            com_email=str(com_mobile)+"139.com"
        personid = request.GET.get("personid")
        username= request.GET.get("username")
    
    service_type1=['再生通','品牌通','短信报价','简版再生通','展会产品','广告','线下纸媒','百度优化','国际站','移动生意管家','再生通发起人','终身服务','商铺服务','诚信会员','定金','微站','来电宝(1或2.8)元','来电宝五元','来电宝按通','来电宝免月租','其他','首页直达广告','企业秀']
    service_type2=['再生通','品牌通','展会产品','广告','黄页','展会广告','百度优化','简版再生通','移动生意管家','再生通发起人','终身服务','商铺服务','诚信会员','定金','微站','来电宝(1或2.8)元','来电宝五元','来电宝按通','来电宝免月租','其他','首页直达广告','企业秀']
    service_type3=['再生通续费','再生通','品牌通续费','展会产品','百度优化','广告续费','简版续费','移动生意管家','再生通发起人','终身服务','商铺服务','诚信会员','定金','微站','来电宝(1或2.8)元','来电宝五元','来电宝按通','来电宝免月租','其他','首页直达广告','企业秀']
    
    return render_to_response('openConfirm0.html',locals())
    closeconn()

#开通单保存
def openConfirmsave(request):
    response = HttpResponse()
    
    localhostIP=getlocalIP()
    company_id=com_id=request.POST["com_id"]
    personid = request.POST["personid"]
    service_type = str(request.POST["service_type"])
    gmt_income=payTime = request.POST["payTime"]
    email=newemail = request.POST["newemail"]
    amount=payMoney = str(request.POST["payMoney"])+'00'
    sale_staff=saler = request.POST["saler"]
    adkeywords = request.POST["adkeywords"]
    adfromdate = request.POST["adfromdate"]
    adtodate = request.POST["adtodate"]
    adcontent = request.POST["adcontent"]
    remark = request.POST["remark"]
    gmt_created=datetime.datetime.now()
    gmt_modified=datetime.datetime.now()
    gmt_date=gmt_created.strftime('%Y-%m-%d')

    remark="广告关键字："+adkeywords+"|开始时间："+adfromdate+"|结束时间："+adtodate+"|广告内容："+adcontent+"|备注："+remark
    apply_group=random.randrange(0,1000000000000000)
    sql="select company_id from company_account where (account='"+email+"' or email='"+email+"')"
    cursor.execute(sql)
    newreturn=cursor.fetchone()
    if (newreturn==None):
        sqla="select email from company_account where company_id="+str(company_id)+""
        cursor.execute(sqla)
        newreturna=cursor.fetchone()
        if (newreturna==None):
            response.write("<script>alert('该开通的邮箱不存在');</script>")
            return response
        else:
            email=newreturna[0]
    else:
        company_id=newreturn[0]
    #判断订单是否已经申请
    errflag=0
    sql="select id from crm_service_apply where order_no='"+order_no+"'"
    cursor.execute(sql)
    newreturn=cursor.fetchone()
    if (newreturn!=None):
        response.write("<script>alert('该开通单已经申请，请不要重复申请！');</script>")
        errflag=1
        return response
    if (errflag!=1):
        value=[apply_group, order_no, gmt_income, email, amount,  sale_staff, remark,  gmt_created, gmt_modified]
        sql="insert into crm_service_apply(apply_group, order_no, gmt_income, email, amount,  sale_staff, remark,  gmt_created, gmt_modified) values(%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        cursor.execute(sql,value);
        conn.commit()
        remark1=''
        crm_service_code='1000'
        if (service_type=='1301'):
            crm_service_code='1000'
        if (service_type=='1302'):
            crm_service_code='1000'
            remark1='开通品牌通'
        if (service_type=='1303'):
            crm_service_code='1002'
        if (service_type=='1304'):
            crm_service_code='1005'
        if (service_type=='1305'):
            crm_service_code='1003'
        if (service_type=='1306'):
            crm_service_code='1004'
        if (service_type=='1307'):
            crm_service_code='10001002'
        if (service_type=='1308'):
            crm_service_code='1306'
        apply_status='0'
        value=[company_id,crm_service_code,apply_group,remark1,gmt_created, gmt_modified,apply_status]
        sql="insert into crm_company_service(company_id,crm_service_code,apply_group,remark,gmt_created, gmt_modified,apply_status) values(%s,%s,%s,%s,%s,%s,%s)"
        cursor.execute(sql,value);
        conn.commit()
    response.write("<script>parent.changeform();</script>")
    return response
    closeconn()
def openConfirmsave1(request):
    response = HttpResponse()
    localhostIP=getlocalIP()
    company_id=com_id=request.POST["com_id"]
    personid = request.POST["personid"]
    mtemplates = request.POST["templates"]
    #service_type = str(request.POST["service_type"])
    service_type1 = str(request.POST.get("service_type1"))
    gmt_income=payTime = request.POST["payTime"]
    email=newemail = request.POST["newemail"]
    account=request.POST.get("account")
    amount=payMoney = str(request.POST["payMoney"])+'00'
    sale_staff=saler = request.POST["saler"]
    adkeywords = request.POST["adkeywords"]
    adfromdate = request.POST["adfromdate"]
    adtodate = request.POST["adtodate"]
    adcontent = request.POST["adcontent"]
    remark = request.POST["remark"]
    gmt_created=datetime.datetime.now()
    gmt_modified=datetime.datetime.now()
    gmt_date=gmt_created.strftime('%Y-%m-%d')
    mbradio = request.POST["mbradio"]
    qiyexiu = request.POST["qiyexiu"]
    remark="广告关键字："+adkeywords+"|开始时间："+adfromdate+"|结束时间："+adtodate+"|广告内容："+adcontent+"|备注："+remark
    """
    sql="select company_id from company_account where (account='"+email+"' or email='"+email+"')"
    cursor.execute(sql)
    newreturn=cursor.fetchone()
    if (newreturn==None):
        sqla="select email from company_account where company_id="+str(company_id)+""
        cursor.execute(sqla)
        newreturna=cursor.fetchone()
        if (newreturna==None):
            response.write("<script>alert('该开通的邮箱不存在');</script>")
            return response
        else:
            email=newreturna[0]
    else:
        company_id=newreturn[0]
    """
    
    servicestr=request.REQUEST.getlist("service_type2")
    order_nostr=""
    for t in servicestr:
        apply_groupstr=""
        apply_group=random.randrange(0,1000000000)
        apply_groupstr=apply_groupstr+str(apply_group)+"|"
        order_no=str(gmt_income)+email+str(mbradio)+str(t)+str(company_id)+str(account)
        order_nostr=order_nostr+order_no+"|"
        #判断订单是否已经申请
        errflag=0
        service_type=t
        crm_service_code='1005'
        if (service_type=='再生通' or service_type=='再生通续费' or service_type=='品牌通' or service_type=='品牌通续费'):
            crm_service_code='1000'
        if (service_type=='品牌通'):
            crm_service_code='1000'
            remark1='开通品牌通'
        if (service_type=='广告' or service_type=='广告续费'):
            crm_service_code='1002'
        if (service_type=='黄页'):
            crm_service_code='1003'
        if (service_type=='展会产品' or service_type=='展会广告'):
            crm_service_code='1004'
        if (service_type=='简版再生通' or service_type=='简版续费'):
            crm_service_code='1006'
        if (service_type=='百度优化'):
            crm_service_code='10001002'
        if (service_type=='商铺服务'):
            crm_service_code='10001004'
        if (service_type=='移动生意管家'):
            crm_service_code='10001000'
        if (service_type=='终身服务'):
            crm_service_code='10001003'
        if (service_type=='再生通发起人'):
            crm_service_code='10001001'
        if (service_type=='诚信会员'):
            crm_service_code='10001005'
        if (service_type=='定金'):
            crm_service_code='10001006'
        if (service_type=='微站'):
            crm_service_code='10001007'
        if (service_type=='来电宝(1或2.8)元'):
            crm_service_code='1007'
        if (service_type=='来电宝五元'):
            crm_service_code='1008'
        if (service_type=='首页直达广告'):
            crm_service_code='10001008'
        if (service_type=='来电宝免月租'):
            crm_service_code='1010'
        if (service_type=='来电宝按通'):
            crm_service_code='1011'
        if (service_type=='企业秀'):
            crm_service_code='10001009'
        if service_type==service_type1:
            amount=amount
        else:
            amount=0
        sql="select id from crm_service_apply where order_no='"+order_no+"'"
        cursor.execute(sql)
        newreturn=cursor.fetchone()
        if not newreturn:
            value=[apply_group, order_no, gmt_income, email, amount,  sale_staff, remark,  gmt_created, gmt_modified]
            sql="insert into crm_service_apply(apply_group, order_no, gmt_income, email, amount,  sale_staff, remark,  gmt_created, gmt_modified) values(%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            cursor.execute(sql,value);
            conn.commit()
            remark1=''
            apply_status='0'
            value=[company_id,crm_service_code,apply_group,remark1,gmt_created, gmt_modified,apply_status,mtemplates]
            sql="insert into crm_company_service(company_id,crm_service_code,apply_group,remark,gmt_created, gmt_modified,apply_status,mobile_templates) values(%s,%s,%s,%s,%s,%s,%s,%s)"
            cursor.execute(sql,value);
            conn.commit()
        if crm_service_code=='10001009':
            sql="select id from crm_service_qiyexiu where company_id=%s"
            cursor.execute(sql,[company_id])
            result=cursor.fetchone()
            if not result:
                sql="insert into crm_service_qiyexiu(company_id,css,html) values(%s,%s,%s)"
                cursor.execute(sql,[company_id,qiyexiu,qiyexiu]);
                conn.commit()
    
    response.write("<script>parent.changeform('"+order_nostr+"',"+str(mbradio)+",'"+str(apply_groupstr)+"');</script>")
    return response
    closeconn()
#临时SEO合作客户添加
def saveseocompany(request):
    response = HttpResponse()
    comlist=request.GET.get("comlist")
    urllist=request.GET.get("url")
    urllist=urllist.replace("~amp~","&")
    apply_group=random.randrange(0,1000000000)
    gmt_created=datetime.datetime.now()
    gmt_modified=datetime.datetime.now()
    gmt_income=gmt_created.strftime('%Y-%m-%d')
    company_id=request.GET.get("comlist")
    amount=0
    sale_staff=''
    remark=''

    errflag=0
    order_no=str(gmt_income)+"10001002"+str(company_id)
    sqla="select email from company_account where company_id="+str(company_id)+""
    cursor.execute(sqla)
    newreturna=cursor.fetchone()
    if (newreturna==None):
        errflag=1
    else:
        email=newreturna[0]
    sql="select id from crm_service_apply where order_no='"+order_no+"'"
    cursor.execute(sql)
    newreturn=cursor.fetchone()
    if (newreturn!=None):
        errflag=1
    if (errflag!=1):
        value=[apply_group, order_no, gmt_income, email, amount,  sale_staff, remark,  gmt_created, gmt_modified]
        sql="insert into crm_service_apply(apply_group, order_no, gmt_income, email, amount,  sale_staff, remark,  gmt_created, gmt_modified) values(%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        cursor.execute(sql,value);
        conn.commit()
        remark1=''
        apply_status='0'
        value=[company_id,'10001002',apply_group,remark1,gmt_created, gmt_modified,apply_status]
        sql="insert into crm_company_service(company_id,crm_service_code,apply_group,remark,gmt_created, gmt_modified,apply_status) values(%s,%s,%s,%s,%s,%s,%s)"
        cursor.execute(sql,value);
        conn.commit()
    
    response.write("<script>document.write('正在放入中。。。');window.location='"+urllist+"';</script>")
    return response
    closeconn()
#会员服务历史
def serverhistory(request):
    localhostIP=getlocalIP()
    company_id=request.GET.get("company_id")
    email=request.GET.get("email")
    if (email=='' or email==None):
        email='000'
    domain_zz91=''
    sqld="select domain_zz91 from company where id="+str(company_id)+""
    cursor.execute(sqld)
    returnzlt=cursor.fetchone()
    if returnzlt:
        if (returnzlt[0]!=None and returnzlt[0]!=''):
            domain_zz91=returnzlt[0]
    sql="select a.name,c.gmt_signed,c.gmt_start,c.gmt_end,c.zst_year,b.amount,b.sale_staff,b.remark,c.crm_service_code,c.apply_status from crm_company_service as c left join crm_service as a on a.code=c.crm_service_code left OUTER join crm_service_apply as b on b.apply_group=c.apply_group where c.company_id="+str(company_id)+"  order by c.gmt_start asc"
    cursor.execute(sql)
    complist=cursor.fetchall()
    listall=[]
    for a in complist:
        amount=a[5]
        crm_service_code=a[8]
        fee=None
        lave=None
        isldb=None
        if crm_service_code in ['1007','1008','1009','1010','1011']:
            sqld="select sum(fee),sum(lave) from phone_cost_service where company_id=%s"
            cursor.execute(sqld,[company_id])
            returnzlt=cursor.fetchone()
            if returnzlt:
                if (returnzlt[0]):
                    fee='%.2f'%returnzlt[0]
                    lave='%.2f'%returnzlt[1]
                else:
                    fee="0"
                    lave="0"
            isldb=1    
        if amount:
            amount=amount/100
        apply_status=a[9]
        apply_statustext=""
        if str(apply_status)=="0":
            apply_statustext="待开通"
        if str(apply_status)=="1":
            apply_statustext="已开通"
        if str(apply_status)=="2":
            apply_statustext="<font color=#ff0>拒绝开通</font>"
        list={'company_id':company_id,'servername':a[0],'gmt_signed':formattime(a[1],1),'gmt_start':formattime(a[2],1),'gmt_end':formattime(a[3],1),'zst_year':a[4],'amount':amount,'sale_staff':a[6],'remark':a[7],'domain_zz91':domain_zz91,'fee':fee,'lave':lave,'apply_statustext':apply_statustext,'isldb':isldb}
        listall.append(list)
    #会员广告服务历史
    #sql="select b.name,a.online_status,a.gmt_start,a.gmt_plan_end,a.review_status,a.search_exact from ad as a,ad_position as b where a.position_id=b.id and a.ad_description='"+str(email)+"'"
    #cursor_ads.execute(sql)
    #adslist=cursor_ads.fetchall()
    #if (adslist==None):
    sql="select b.name,a.online_status,a.gmt_start,a.gmt_plan_end,a.review_status,a.search_exact from ad as a,ad_position as b,advertiser as c where a.position_id=b.id and a.advertiser_id=c.id and c.email='"+str(email)+"'"
    cursor_ads.execute(sql)
    adslist=cursor_ads.fetchall()
    listall_ads=[]
    for a in adslist:
        review_status=a[4]
        online_status=a[1]
        if (review_status=='Y'):
            checkstat="审核"
        else:
            checkstat="未审核"
        if (online_status=='Y'):
            online_status="在线"
        else:
            online_status="下线"
        list={'position_name':a[0],'online_status':a[1],'gmt_start':formattime(a[2],1),'gmt_plan_end':formattime(a[3],1),'review_status':online_status+"|"+checkstat,'search_exact':a[5]}
        listall_ads.append(list)
    #标王
    listall_ads1=[]
    sql="select '标王',a.is_checked,a.start_time,a.end_time,a.name from products_keywords_rank as a where a.company_id="+str(company_id)+""
    cursor.execute(sql)
    adslist=cursor.fetchall()
    for a in adslist:
        is_checked=a[1]
        if (str(is_checked)=='1'):
            is_checked="审核"
        else:
            is_checked="未审核"
        list={'position_name':a[0],'online_status':a[1],'gmt_start':formattime(a[2],1),'gmt_plan_end':formattime(a[3],1),'review_status':is_checked,'search_exact':a[4]}
        listall_ads1.append(list)
    
    return render_to_response('serverhistory.html',locals())
    closeconn()
#主要服务
def servicemain(request):
    company_id=request.GET.get("company_id")
    if company_id:
        domain_zz91=''
        sqld="select domain_zz91 from company where id="+str(company_id)+""
        cursor.execute(sqld)
        returnzlt=cursor.fetchone()
        if returnzlt:
            if (returnzlt[0]!=None and returnzlt[0]!=''):
                domain_zz91=returnzlt[0]
        sql="select a.name,c.gmt_signed,c.gmt_start,c.gmt_end,c.zst_year,b.amount,b.sale_staff,b.remark,c.crm_service_code,c.apply_status from crm_company_service as c left join crm_service as a on a.code=c.crm_service_code left OUTER join crm_service_apply as b on b.apply_group=c.apply_group where c.company_id=%s  order by c.gmt_start desc"
        cursor.execute(sql,[company_id])
        complist=cursor.fetchall()
        listall=[]
        for a in complist:
            amount=a[5]
            crm_service_code=a[8]
            fee=None
            lave=None
            isldb=None
            if crm_service_code in ['1007','1008','1009','1010','1011']:
                sqld="select sum(fee),sum(lave) from phone_cost_service where company_id=%s"
                cursor.execute(sqld,[company_id])
                returnzlt=cursor.fetchone()
                if returnzlt:
                    if (returnzlt[0]):
                        fee='%.2f'%returnzlt[0]
                        lave='%.2f'%returnzlt[1]
                    else:
                        fee="0"
                        lave="0"
                isldb=1    
            if amount:
                amount=amount/100
            apply_status=a[9]
            apply_statustext=""
            if str(apply_status)=="0":
                apply_statustext="待开通"
            if str(apply_status)=="1":
                apply_statustext="已开通"
            if str(apply_status)=="2":
                apply_statustext="<font color=#ff0>拒绝开通</font>"
            list={'company_id':company_id,'servername':a[0],'gmt_signed':formattime(a[1],1),'gmt_start':formattime(a[2],1),'gmt_end':formattime(a[3],1),'zst_year':a[4],'amount':amount,'sale_staff':a[6],'remark':a[7],'domain_zz91':domain_zz91,'fee':fee,'lave':lave,'apply_statustext':apply_statustext,'isldb':isldb}
            listall.append(list)
    rjson=request.GET.get("json")
    if str(rjson)=="1":
        #return HttpResponse(simplejson.dumps(listall,ensure_ascii=False))
        return HttpResponse("var _suggest_result_={'result':"+str(simplejson.dumps(listall,ensure_ascii=False))+"}")
    return render_to_response('service_main.html',locals())

#广告服务
def servicead(request):
    email=request.GET.get("email")
    if email:
        sql="select b.name,a.online_status,a.gmt_start,a.gmt_plan_end,a.review_status,a.search_exact from ad as a left outer join ad_position as b on a.position_id=b.id left outer join advertiser as c on a.advertiser_id=c.id where  c.email='"+str(email)+"'"
        cursor_ads.execute(sql)
        adslist=cursor_ads.fetchall()
        listall_ads=[]
        for a in adslist:
            review_status=a[4]
            online_status=a[1]
            if (review_status=='Y'):
                checkstat="审核"
            else:
                checkstat="未审核"
            if (online_status=='Y'):
                online_status="在线"
            else:
                online_status="下线"
            list={'position_name':a[0],'online_status':a[1],'gmt_start':formattime(a[2],1),'gmt_plan_end':formattime(a[3],1),'review_status':online_status+"|"+checkstat,'search_exact':a[5]}
            listall_ads.append(list)
    return render_to_response('service_ad.html',locals())
#其他小产品服务
def serviceother(request):
    company_id=request.GET.get("company_id")
    if company_id:
        #标王
        listall_ads1=[]
        sql="select '标王',a.is_checked,a.start_time,a.end_time,a.name from products_keywords_rank as a where a.company_id="+str(company_id)+" order by id desc"
        cursor.execute(sql)
        adslist=cursor.fetchall()
        for a in adslist:
            is_checked=a[1]
            if (str(is_checked)=='1'):
                is_checked="审核"
            else:
                is_checked="未审核"
            list={'position_name':a[0],'online_status':a[1],'gmt_start':formattime(a[2],1),'gmt_plan_end':formattime(a[3],1),'review_status':is_checked,'search_exact':a[4]}
            listall_ads1.append(list)
        sql="select '供求自动刷新',gmt_begin,gmt_end from shop_reflush where company_id=%s"
        cursor.execute(sql,[company_id])
        adslist=cursor.fetchall()
        for a in adslist:
            is_checked="审核"
            list={'position_name':a[0],'online_status':a[1],'gmt_start':formattime(a[1],1),'gmt_plan_end':formattime(a[2],1),'review_status':'','search_exact':''}
            listall_ads1.append(list)
            
        sql="select '显示联系方式',gmt_begin,gmt_end from shop_showphone where company_id=%s"
        cursor.execute(sql,[company_id])
        adslist=cursor.fetchall()
        for a in adslist:
            is_checked="审核"
            list={'position_name':a[0],'online_status':a[1],'gmt_start':formattime(a[1],1),'gmt_plan_end':formattime(a[2],1),'review_status':'','search_exact':''}
            listall_ads1.append(list)
    return render_to_response('service_other.html',locals())
#客户添加
def companyadd(request):
    localhostIP=getlocalIP()
    personid = request.GET.get("personid")
    addtype= request.GET.get("addtype")
    sid = request.GET.get("sid")
    com_mobile = request.GET.get("com_mobile")
    com_contactperson = request.GET.get("com_contactperson")
    activelist=getactive()
    if (com_mobile==None):
        com_mobile=""
    if (com_contactperson==None):
        com_contactperson=""
    if (addtype=="zst"):
        zstflag=1
    return render_to_response('compadd.html',locals())
    closeconn()
#客户预申请
def companysq(request):
    localhostIP=getlocalIP()
    personid = request.GET.get("personid")
    com_id = request.GET.get("com_id")
    addtype= request.GET.get("addtype")
    sid= request.GET.get("sid")
    activelist=getactive()
    #------------------帐号信息
    sql="select account,contact,tel_country_code,tel_area_code,tel,mobile,fax_country_code,fax_area_code,fax,email,sex  from company_account where company_id="+str(com_id)+""
    cursor.execute(sql)
    accountlist=cursor.fetchone()
    if (accountlist):
        account=accountlist[0]
        ccontactp=contact=accountlist[1]
        tel_country_code=accountlist[2]
        tel_area_code=accountlist[3]
        tel=accountlist[4]
        if (tel_country_code==None):
            tel_country_code=''
        if (tel_area_code==None):
            tel_area_code=''
        ctel=str(tel_country_code)+'-'+str(tel_area_code)+'-'+str(tel)
        cmobile=mobile=accountlist[5]
        fax_country_code=accountlist[6]
        fax_area_code=accountlist[7]
        fax=accountlist[8]
        if (fax_country_code==None):
            fax_country_code=''
        if (fax_area_code==None):
            fax_area_code=''
        cfax=str(fax_country_code)+'-'+str(fax_area_code)+'-'+str(fax)
        cemail=email=accountlist[9]
        if not cemail:
            cemail=account
        sex=accountlist[10]
        if (sex=='0'):
            sex='先生'
        if (sex=='1'):
            sex='女士'
        
    sql="select name,business,area_code,domain,regtime,address,address_zip,introduction,industry_code from company where id="+str(com_id)+""
    cursor.execute(sql)
    accountlist=cursor.fetchone()
    if (accountlist):
        cname=accountlist[0]
        cproductslist_en=accountlist[1]
        area_code=accountlist[2]
        cweb=accountlist[3]
        if (cweb==None):
            cweb=''
        regtime=accountlist[4]
        cadd=accountlist[5]
        czip=accountlist[6]
        cintroduce=accountlist[7]
        industry_code=accountlist[8]
        ckeywords=getindustry_codeold(industry_code)
        
    if (addtype=="zhanhui"):
        return render_to_response('company_sq_zh.html',locals())
    return render_to_response('company_sq.html',locals())
    closeconn()
#客户搜索
def searchcomplist(request):
    localhostIP=getlocalIP()
    personid = request.POST.get("personid")
    listall=[]
    searsql=" c.id>0 "
    newcrm = request.POST.get("newcrm")
    hosturl= request.POST.get("hosturl")
    com_tel = request.POST.get("com_tel")
    if (com_tel!=None and com_tel!=""):
        searsql=searsql+" and c.tel like '%"+com_tel+"%'"
    com_mobile = request.POST.get("com_mobile")
    if (com_mobile!=None and com_mobile!=""):
        searsql=searsql+" and c.mobile like '%"+com_mobile+"%'"
    com_name = request.POST.get("com_name")
    #com_name=com_name.encode("utf-8").decode('GB18030','ignore')
    
    if (com_name!=None and com_name!=""):
        searsql=searsql+" and exists(select id from company where name like '%"+com_name+"%' and id=c.company_id)"
    com_email = request.POST.get("com_email")
    if (com_email!=None and com_email!=''):
        searsql=searsql+" and c.email like '%"+com_email+"%'"
    account=request.POST.get("account")
    if account:
        searsql=searsql+" and c.account='"+str(account)+"'"
    sql="select c.tel_country_code, c.tel_area_code, c.tel,c.mobile,c.email,c.company_id,c.account from company_account as c where "+searsql+" order by c.id desc limit 0,10"
    cursor.execute(sql)
    complist=cursor.fetchall()
    for a in complist:
        account=a[6]
        sql1="select a.id, a.name, a.regtime  from company as a where a.id="+str(a[5])
        cursor.execute(sql1)
        accountlist=cursor.fetchone()
        if (accountlist):
            tel=str(a[0])+'-'+str(a[1])+'-'+str(a[2])
            list={'id':accountlist[0],'name':accountlist[1],'tel':tel,'mobile':a[3][0:3]+'***'+a[3][-3:],'email':a[4],'regtime':str(accountlist[2]),'account':account}
            listall.append(list)
    return render_to_response('searchcomp.html',locals())
    closeconn()
#短信报名客户添加  搜索
def sms_searchcomp(request):
    localhostIP=getlocalIP()
    sid = request.GET.get("sid")
    com_mobile = request.GET.get("com_mobile")
    com_contactperson = request.GET.get("com_contactperson")
    personid = request.GET.get("personid")
    addtype = request.GET.get("addtype")
    listall=[]
    searsql=" c.id>0 "
    if (com_mobile!=None):
        searsql=searsql+" and c.mobile like '%"+com_mobile+"%'"
    #com_name=com_name.encode("utf-8").decode('GB18030','ignore')

    sql="select    order by a.id desc limit 0,20"
    sql="select c.tel_country_code, c.tel_area_code, c.tel,c.mobile,c.email,c.company_id from company_account as c where "+searsql+" order by c.id desc limit 0,10"
    cursor.execute(sql)
    complist=cursor.fetchall()
    for a in complist:
        sql="select a.id, a.name, a.regtime  from company as a where a.id="+str(a[5])
        cursor.execute(sql)
        accountlist=cursor.fetchone()
        if (accountlist):
            tel=str(a[0])+'-'+str(a[1])+'-'+str(a[2])
            list={'id':accountlist[0],'name':accountlist[1],'tel':tel,'mobile':a[3][0:3]+'***'+a[3][-3:],'email':a[4],'regtime':str(accountlist[2])}
            listall.append(list)
    return render_to_response('sms_searchcomp.html',locals())
    closeconn()
#客户保存
def companysave(request):
    localhostIP=getlocalIP()
    addtype=request.POST["addtype"]
    name=cname = request.POST["cname"]
    contact=ccontactp = request.POST["ccontactp"]
    cdesi = request.POST["cdesi"]
    ckeywords = request.POST["ckeywords"]
    ckind = request.POST["ckind1"]
    province = request.POST["province"]
    city = request.POST["city"]
    sid = request.POST["sid"]
    active_flag = request.POST["active_flag"]
    Garden = request.POST["Garden1"]
    address=cadd = request.POST["cadd"]
    address_zip=czip = request.POST["czip"][0:6]
    ctel = request.POST["ctel"]
    mobile=cmobile = request.POST["cmobile"]
    cfax = request.POST["cfax"]
    account = request.POST["account"]
    cemail = request.POST["cemail"]
    website=domain=cweb = request.POST["cweb"]
    introduction=cintroduce = request.POST["cintroduce"]
    business = cproductslist_en = request.POST["cproductslist_en"]
    personid = request.POST["personid"]
    countryselect = request.POST["countryselect"]
    account=account.replace(' ','')
    cemail=cemail.replace(' ','')
    
    regtime=gmt_created=datetime.datetime.now()
    gmt_modified=datetime.datetime.now()
    password=sjs=random.randrange(0,100000000)
    md5pwd = hashlib.md5(str(password))
    md5pwd = md5pwd.hexdigest()[8:-8]
    #''判断邮箱帐号是否存在
    sql="select id  from auth_user where username='"+str(account)+"' or email='"+str(cemail)+"'"
    cursor.execute(sql)
    accountlist=cursor.fetchone()
    if (accountlist):
        response = HttpResponse()
        response.write("<script>alert('该用户名或邮箱已经存在！');window.history.back(1)</script>")
        return response
    
    #''帐号添加
    value=[account,md5pwd,cemail,gmt_created,gmt_modified];
    sql="insert into auth_user (username,password,email,gmt_created,gmt_modified) values(%s,%s,%s,%s,%s)";
    cursor.execute(sql,value);
    conn.commit()
    
    #添加公司信息
    industry_code=getindustry_code(ckeywords)
    service_code=getservice_code(ckind)
    area_code=getprovincecode(province+'|'+city)
    foreign_city=''
    category_garden_id=getgardid(Garden)
    membership_code='10051000'
    classified_code='10101002'
    regfrom_code='10031023'
    
    value=[name, industry_code, business, service_code, area_code, foreign_city, category_garden_id, membership_code,    domain, classified_code, regfrom_code,  regtime, gmt_created, gmt_modified,  address, address_zip, website, introduction,active_flag]
    sql="insert into company (name, industry_code, business, service_code, area_code, foreign_city, category_garden_id, membership_code,    domain, classified_code, regfrom_code,  regtime, gmt_created, gmt_modified,  address, address_zip, website, introduction,active_flag)"
    sql=sql+" values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)";
    cursor.execute(sql,value);
    conn.commit()
    
    company_id=getcompany_id(name,gmt_created)
    is_admin='1'
    tel_country_code=''
    tel_area_code=''
    tel=ctel
    fax_country_code=''
    fax_area_code=''
    fax=cfax
    email=cemail
    sex=cdesi
    #'添加联系方式
    value=[account, company_id, contact, is_admin, tel_country_code, tel_area_code, tel, mobile, fax_country_code, fax_area_code, fax, email, sex, password, gmt_modified, gmt_created]
    sql="insert into company_account (account, company_id, contact, is_admin, tel_country_code, tel_area_code, tel, mobile, fax_country_code, fax_area_code, fax, email, sex, password, gmt_modified, gmt_created)"
    sql=sql+" values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)";
    cursor.execute(sql,value);
    conn.commit()
    return render_to_response('company_save.html',locals())
    closeconn()
#获取客服人员信息
def getCsuserName(request):
    com_id = request.GET.get("com_id")
    sql="select cs_account,gmt_next_visit_phone from crm_cs where company_id='"+str(com_id)+"'"
    cursor.execute(sql)
    newcode=cursor.fetchone()
    if (newcode == None):
        comtext=""
    else:
        sql="select name from staff where account='"+str(newcode[0])+"'"
        cursor_work.execute(sql)
        arrname=cursor_work.fetchone()
        if arrname:
            comtext=arrname[0]
        if (newcode[1]!=None):
            gmt_next_visit_phone=formattime(newcode[1],0)
    return render_to_response('cscomp.html',locals())
    closeconn();
#门市部流量
def getesitecount(request):
    com_id = request.GET.get("com_id")
    sql="select real_visit_count from analysis_esite_visit where company_id='"+str(com_id)+"'"
    cursor.execute(sql)
    newcode=cursor.fetchone()
    if (newcode):
        comtext=newcode[0]
    else:
        comtext='0'
    return render_to_response('cscomp.html',locals())
#----报名管理2
def subjectbaoming2(request):
    page=request.GET.get("page")
    title=request.GET.get("title")
    if (page==None):
        page=1
    if (title==None):
        title=''
    funpage = zz91page()
    limitNum=funpage.limitNum(10)
    nowpage=funpage.nowpage(int(page))
    frompageCount=funpage.frompageCount()
    after_range_num = funpage.after_range_num(2)
    before_range_num = funpage.before_range_num(9)
    sqlm=""
    if (title!=None and title!=""):
        sqlm=sqlm+" and title like '%"+str(title)+"%'"
    sqlm=sqlm+" and title like '%来电宝%'"
    sqlc="select count(0) from subject_baoming where  id>0 "+sqlm+""
    cursor.execute(sqlc)
    listcount=cursor.fetchone()[0]
    
    sql="select title,contents,gmt_created from subject_baoming where id>0 "+sqlm+" order by gmt_created desc limit "+str(frompageCount)+","+str(limitNum)+" "
    cursor.execute(sql)
    baominglist=cursor.fetchall()
    listall=[]
    if baominglist:
        for a in baominglist:
            contents = a[1]
            
            list={'title':a[0],'contents':contents,'gmt_created':formattime(a[2],0)}
            listall.append(list)
    
    if (int(listcount)>100000):
        listcount=100000
    listcount = funpage.listcount(listcount)
    page_listcount=funpage.page_listcount()
    firstpage = funpage.firstpage()
    lastpage = funpage.lastpage()
    page_range  = funpage.page_range()
    nextpage = funpage.nextpage()
    prvpage = funpage.prvpage()
    
    return render_to_response('subjectbaoming.html',locals())
    closeconn();

#----报名管理
def subjectbaoming(request):
    page=request.GET.get("page")
    title=request.GET.get("title")
    pt=request.GET.get("pt")
    if pt=="1":
        title="手机问题反馈"
    if pt=="2":
        title="申请再生通"
    if pt=="3":
        title="在线支付"
    if (page==None):
        page=1
    if (title==None):
        title=''
    funpage = zz91page()
    limitNum=funpage.limitNum(10)
    nowpage=funpage.nowpage(int(page))
    frompageCount=funpage.frompageCount()
    after_range_num = funpage.after_range_num(2)
    before_range_num = funpage.before_range_num(9)
    sqlm=""
    if (title!=None and title!=""):
        sqlm=sqlm+" and title like '%"+str(title)+"%'"
    sqlm=sqlm+" and title not like '%来电宝%'"
    sqlc="select count(0) from subject_baoming where  id>0 "+sqlm+""
    cursor.execute(sqlc)
    listcount=cursor.fetchone()[0]
    
    sql="select title,contents,gmt_created from subject_baoming where id>0 "+sqlm+" order by gmt_created desc limit "+str(frompageCount)+","+str(limitNum)+" "
    cursor.execute(sql)
    baominglist=cursor.fetchall()
    listall=[]
    if baominglist:
        for a in baominglist:
            contents = a[1]
            
            list={'title':a[0],'contents':contents,'gmt_created':formattime(a[2],0)}
            listall.append(list)
    
    if (int(listcount)>100000):
        listcount=100000
    listcount = funpage.listcount(listcount)
    page_listcount=funpage.page_listcount()
    firstpage = funpage.firstpage()
    lastpage = funpage.lastpage()
    page_range  = funpage.page_range()
    nextpage = funpage.nextpage()
    prvpage = funpage.prvpage()
    
    return render_to_response('subjectbaoming.html',locals())
    closeconn();
#tomcat管理
def tomcatmanager(request):
    listall=[]
    if request.META.has_key('HTTP_X_FORWARDED_FOR'):
        ip =  request.META['HTTP_X_FORWARDED_FOR']
    else:
        ip = request.META['REMOTE_ADDR']
    ip = request.META['HTTP_HOST']
    sip = request.GET.get("ip");
    title=request.GET.get("title");
    searsql=""
    if sip:
        searsql+=" and ip='"+str(sip)+"'"
    if title:
        searsql+=" and title like '%"+str(title)+"%'"
    sql="select title, start, stop, gmt_created, gmt_modified, filename,id,start_test,stop_test,ip,tomcat_part,server_part,warname,appname,website from tomcat_manager where 1=1 "+str(searsql)+" order by ip desc,tomcat_part asc,server_part asc"
    cursor_work.execute(sql)
    returnlist=cursor_work.fetchall()
    for a in returnlist:
        warname=a[12]
        appname=a[13]
        website=a[14]
        if (website==None):
            website=''
        list={'title':a[0],'start':a[1],'stop':a[2],'gmt_created':a[3],'gmt_modified':a[4],'filename':a[5],'id':a[6],'start_test':a[7],'stop_test':a[8],'ip':a[9],'tomcat_part':a[10],'server_part':a[11],'warname':warname,'appname':appname,'website':website}
        listall.append(list)
    return render_to_response('tomcatmanager.html',locals())
    closeconn()
def tomcatadd(request):
    title=request.POST["title"]
    ip=request.POST["ip"]
    tomcat_part=request.POST["tomcat_part"]
    server_part=request.POST["server_part"]
    start='0'
    stop='0'
    warname=request.POST["warname"]
    appname=request.POST["appname"]
    website=request.POST["website"]
    value=[title,start,stop,ip,tomcat_part,server_part,warname,appname,website]
    valueu=[title,ip,tomcat_part,server_part,warname,appname,website,title,ip]
    sql="select id from tomcat_manager where title='"+str(title)+"' and ip='"+str(ip)+"'"
    cursor_work.execute(sql)
    newcode=cursor_work.fetchone()
    if (newcode == None):
        sql="insert into tomcat_manager(title,start,stop,ip,tomcat_part,server_part,warname,appname,website) values(%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        cursor_work.execute(sql,value);
        conn_work.commit()
    else:
        sql="update tomcat_manager set title=%s,ip=%s,tomcat_part=%s,server_part=%s,warname=%s,appname=%s,website=%s where title=%s and ip=%s"
        cursor_work.execute(sql,valueu);
        conn_work.commit()
    response = HttpResponse()
    response.write("<script>window.location='/tomcatmanager/?ip="+str(ip)+"'</script>")
    return response
def tomcatsave(request):
    id = request.GET.get("id");
    action=request.GET.get("action");
    sip=request.GET.get("ip");
    if (action=="start_test"):
        start=1
        value=[start,id];
        sql="update tomcat_manager set start_test=%s where id=%s";
        cursor_work.execute(sql,value);
        conn_work.commit()
    if (action=="start"):
        start=1
        value=[start,id];
        sql="update tomcat_manager set start=%s where id=%s";
        cursor_work.execute(sql,value);
        conn_work.commit()
    if (action=="del"):
        value=[id];
        sql="delete from tomcat_manager where id=%s";
        cursor_work.execute(sql,value);
        conn_work.commit()
    response = HttpResponse()
    response.write("<script>window.location='/tomcatmanager/?ip="+str(sip)+"'</script>")
    return response
#本地crm供求及留言查看
def crm_offerlist(request):
    companyId=request.GET.get("companyId");
    page=request.GET.get("page")
    if (page==None):
        page=1
    funpage = zz91page()
    limitNum=funpage.limitNum(10)
    nowpage=funpage.nowpage(int(page))
    frompageCount=funpage.frompageCount()
    after_range_num = funpage.after_range_num(2)
    before_range_num = funpage.before_range_num(9)
    sqlm=""
    if (companyId!=None and companyId!=""):
        sqlm=sqlm+" and company_id ="+str(companyId)+""
    sql="select products_type_code,title,details,check_status,refresh_time,expire_time,tags from products where id>0 "+sqlm+" order by id desc limit "+str(frompageCount)+","+str(int(frompageCount)+int(limitNum))+" "
    cursor.execute(sql)
    offerlist=cursor.fetchall()
    listcount=0
    listall=[]
    if offerlist:
        for a in offerlist:
            products_type_code = a[0]
            if (str(products_type_code)=='10331000'):
                products_type='供应'
            else:
                products_type='求购'
            title=a[1]
            details=a[2][0:50]+'...'
            check_status=a[3]
            if (str(check_status)=='0'):
                status='未审核'
            if (str(check_status)=='1'):
                status='已审核'
            if (str(check_status)=='2'):
                status='审核未通过退回'
            if (str(check_status)=='3'):
                status='暂不发布'
            refresh_time=a[4]
            expire_time=a[5]
            tags=a[6]
            list={'products_type':products_type,'title':title,'details':details,'status':status,'refresh_time':formattime(refresh_time,0),'expire_time':formattime(expire_time,0),'tags':tags}
            listall.append(list)
            listcount=listcount+1
    
    if (int(listcount)>100000):
        listcount=100000
    listcount = funpage.listcount(listcount)
    page_listcount=funpage.page_listcount()
    firstpage = funpage.firstpage()
    lastpage = funpage.lastpage()
    page_range  = funpage.page_range()
    nextpage = funpage.nextpage()
    prvpage = funpage.prvpage()
    return render_to_response('crm_offerlist.html',locals())
    closeconn()
def crm_receivequestionlist(request):
    return render_to_response('crm_receivequestionlist.html',locals())
    closeconn()
def crm_sendquestionlist(request):
    return render_to_response('crm_sendquestionlist.html',locals())
    closeconn()
def crm_servicequestionlist(request):
    return render_to_response('crm_servicequestionlist.html',locals())
    closeconn()
def getcompanyinfo(company_id):
    sql="select c.name,a.contact from company as c left join company_account as a on a.company_id=c.id where c.id=%s"
    cursor.execute(sql,[company_id])
    returnresult=cursor.fetchone()
    if returnresult:
        return {'name':returnresult[0],'contact':returnresult[1]}

def getservicetime(company_id,mcode):
    sql="select a.name,c.gmt_signed,c.gmt_start,c.gmt_end,c.zst_year,b.amount,b.sale_staff,b.remark from crm_company_service as c left join crm_service as a on a.code=c.crm_service_code left OUTER join crm_service_apply as b on b.apply_group=c.apply_group where c.company_id="+str(company_id)+" and c.apply_status=1 and a.code in ("+mcode+") order by c.gmt_start asc"
    cursor.execute(sql)
    a=cursor.fetchone()
    if a:
        amount=a[5]
        if amount:
            amount=amount/100
        list={'servername':a[0],'gmt_signed':formattime(a[1],1),'gmt_start':formattime(a[2],1),'gmt_end':formattime(a[3],1),'zst_year':a[4],'amount':amount,'sale_staff':a[6],'remark':a[7]}
        return list
def getchick():
    a=p
#来电宝推广
def ppcindex(request):
    page=request.GET.get("page")
    email=request.GET.get("email")
    mobile=request.GET.get("mobile")
    tel=request.GET.get("tel")
    funpage = zz91page()
    if (page=="" or page==None):
        page=1
    sear=""
    limitNum=funpage.limitNum(15)
    nowpage=funpage.nowpage(int(page))
    frompageCount=funpage.frompageCount()
    after_range_num = funpage.after_range_num(2)
    before_range_num = funpage.before_range_num(9)
    sqlsear=""
    if ((email!="" and email!=None) or (mobile!="" and mobile!=None)):
        sqlsear=sqlsear+" and exists(select company_id from company_account where company_id=phone.company_id"
        if (email!="" and email!=None):
            sqlsear=sqlsear+" and email='"+str(email)+"'"
        if (mobile!="" and mobile!=None):
            sqlsear=sqlsear+" and mobile='"+str(mobile)+"'"
        sqlsear=sqlsear+")"    
        sear=sear+"&mobile="+mobile+"&email="+email
    if (tel!="" and tel!=None):
        sqlsear=sqlsear+" and tel like '%"+str(tel)+"%'"
        sear=sear+"&tel="+tel
        
    sql="select company_id,account,tel,front_tel,keywords,amount,balance,gmt_open from phone where id>0 "+sqlsear+" order by id desc limit "+str(frompageCount)+","+str(limitNum)+""
    cursor.execute(sql)
    ppclist=cursor.fetchall()
    
    sqlc="select count(0) from phone"
    cursor.execute(sqlc)
    ppclistcount=cursor.fetchone()[0]
    listcount=0
    listall=[]
    if ppclist:
        for a in ppclist:
            companyinfo=getcompanyinfo(a[0])
            servicelist=getservicetime(a[0],'1007,1008,1009,1010,1011')
            acountlist=getacount(a[0])
            amount=a[5]
            if amount==None:
                amount=""
            balance=a[6]
            balance=getppcpay(a[2],a[0])
            if balance==None:
                balance=""
            list={'company_id':a[0],'mobile':acountlist['mobile'],'contact':acountlist['contact'],'account':a[1],'tel':a[2],'front_tel':a[3],'keywords':a[4],'amount':amount,'balance':balance,'gmt_open':a[7],'companyinfo':companyinfo,'servicelist':servicelist}
            listall.append(list)
    
    
    listcount = funpage.listcount(ppclistcount)
    page_listcount=funpage.page_listcount()    
    firstpage = funpage.firstpage()
    lastpage = funpage.lastpage()
    page_range  = funpage.page_range()
    nextpage = funpage.nextpage()
    prvpage = funpage.prvpage()
    allfee=getallppcpay()
    allincome=getallincome()
    return render_to_response('ppc/index.html',locals())
    closeconn()
#PPC供求列表
def ppcproducts(request):
    company_id=request.GET.get("company_id")
    refresh=request.GET.get("refresh")
    
    if (refresh=="1"):
        refresh_time=datetime.datetime.now()
        id=request.GET.get("id")
        if id!=None:
            sqla="update products set refresh_time=%s where id=%s"
            cursor.execute(sqla,[refresh_time,id]);
            conn.commit()
        else:
            sqla="update products set refresh_time=%s where company_id=%s"
            cursor.execute(sqla,[refresh_time,company_id]);
            conn.commit()
        response = HttpResponse()
        response.write("<script>window.location='/ppc/plist/?company_id="+str(company_id)+"'</script>")
        return response

    
    page=request.GET.get("page")
    funpage = zz91page()
    if (page=="" or page==None):
        page=1
    sear="&company_id="+str(company_id)
    limitNum=funpage.limitNum(20)
    nowpage=funpage.nowpage(int(page))
    frompageCount=funpage.frompageCount()
    after_range_num = funpage.after_range_num(2)
    before_range_num = funpage.before_range_num(9)
    sqlsear=""
    sql="select id,title,refresh_time,products_type_code from products where company_id="+str(company_id)+" order by refresh_time desc limit "+str(frompageCount)+","+str(int(limitNum))+" "
    cursor.execute(sql)
    ppclist=cursor.fetchall()
    
    sqlc="select count(0) from products where company_id="+str(company_id)+""
    cursor.execute(sqlc)
    ppclistcount=cursor.fetchone()[0]
    listcount=0
    listall=[]
    if ppclist:
        for a in ppclist:
            products_type_code=a[3]
            if (products_type_code=="10331001"):
                products_type="求购"
            if (products_type_code=="10331000"):
                products_type="供应"
            list={'id':a[0],'title':a[1],'products_type':products_type,'refresh_time':formattime(a[2],0)}
            listall.append(list)
    
    
    listcount = funpage.listcount(ppclistcount)
    page_listcount=funpage.page_listcount()    
    firstpage = funpage.firstpage()
    lastpage = funpage.lastpage()
    page_range  = funpage.page_range()
    nextpage = funpage.nextpage()
    prvpage = funpage.prvpage()
    
    return render_to_response('ppc/plist.html',locals())
    closeconn()
#群发邮件
def sendlist(request):
    company_id=request.GET.get("company_id")
    delaction=request.GET.get("del")
    if (delaction=="1"):
        id=request.GET.get("id")
        if (id):
            sqld="delete from phone_keywords where id=%s"
            cursor.execute(sqld,[id])
            conn.commit()
            response = HttpResponse()
            response.write("<script>window.location='/ppc/sendlist/?company_id="+str(company_id)+"'</script>")
            return response
    sqlc="select id,company_id,type,keywords,sendtitle,sendcontent from phone_keywords where company_id="+str(company_id)+""
    cursor.execute(sqlc)
    resaultlist=cursor.fetchall()
    listall=[]
    for a in resaultlist:
        list={'id':a[0],'company_id':a[1],'type':a[2],'keywords':a[3],'sendtitle':a[4],'sendcontent':a[5]}
        listall.append(list)
    return render_to_response('ppc/sendlist.html',locals())
    closeconn()
def getproinfo(company_id,pdtid):
    list={'pdt_name':'','mobile':'','email':'','refresh_time':'','pdt_kind':'','company_id':company_id}
    sql="select title,refresh_time,RIGHT( products_type_code, 1 ) AS pdt_kind from products where id="+str(pdtid)+""
    cursor.execute(sql)
    resaultlist=cursor.fetchone()
    if resaultlist:
        list['pdt_name']=resaultlist[0]
        list['refresh_time']=formattime(resaultlist[1],0)
        pdt_kind=resaultlist[2]
        if (str(pdt_kind) == '1'):
            list['pdt_kind']="求购"
        else:
            list['pdt_kind']="供应"
    sql="select mobile,email from company_account where company_id="+str(company_id)+""
    cursor.execute(sql)
    resaultlist=cursor.fetchone()
    if resaultlist:
        list['mobile']=resaultlist[0]
        list['email']=resaultlist[1]
    return list
    
def senddetail(request):
    company_id=request.GET.get("company_id")
    sid=request.GET.get("sid")
    stitle=request.GET.get("stitle")
    s_type=request.GET.get("stype")
    if (s_type==None):
        s_type='email'
    type=request.GET.get("type")
    sear=""
    sear=sear+"&company_id="+str(company_id)
    sear=sear+"&stitle="+str(stitle)
    sear=sear+"&type="+str(type)
    sear=sear+"&sid="+str(sid)
    sql="select type,keywords,sendtitle,sendcontent from phone_keywords where id=%s"
    cursor.execute(sql,[sid])
    resaultlist=cursor.fetchone()
    if resaultlist:
        stype=resaultlist[0]
        keywords=resaultlist[1]
        sendtitle=resaultlist[2]
        sendcontent=resaultlist[3]
        if (str(stype)=="1"):
            std1=""
            std2="checked"
        else:
            std1="checked"
            std2=""
    if (stitle and stitle!=""):
        #-----------------------
        page=request.GET.get("page")
        funpage = zz91page()
        if (page=="" or page==None):
            page=1
        limitNum=funpage.limitNum(5000)
        nowpage=funpage.nowpage(int(page))
        frompageCount=funpage.frompageCount()
        after_range_num = funpage.after_range_num(2)
        before_range_num = funpage.before_range_num(9)
        
        port = settings.SPHINXCONFIG['port']
        cl = SphinxClient()
        cl.SetServer ( settings.SPHINXCONFIG['serverid'], port )
        cl.SetMatchMode ( SPH_MATCH_BOOLEAN )
        if type:
            cl.SetFilter('pdt_kind',[int(type)])
        
        cl.SetSortMode( SPH_SORT_EXTENDED,"refresh_time desc" )
        cl.SetLimits (frompageCount,limitNum,5000)
        res = cl.Query ('@(title,label0,label1,label2,label3,label4,city,province,tags) '+stitle,'offersearch_new,offersearch_new_vip')
        if res:
            if res.has_key('matches'):
                tagslist=res['matches']
                listall=[]
                for match in tagslist:
                    id=match['id']
                    com_id=match['attrs']['company_id']
                    list=[]
                    list=getproinfo(com_id,id)
                    listall.append(list)
                listcount=res['total_found']
                
        listcount = funpage.listcount(listcount)
        page_listcount=funpage.page_listcount()    
        firstpage = funpage.firstpage()
        lastpage = funpage.lastpage()
        page_range  = funpage.page_range()
        nextpage = funpage.nextpage()
        prvpage = funpage.prvpage()
        
        for list in listall:
            sql="select id from phone_sendlist where s_id=%s and s_email=%s and s_type=%s"
            cursor.execute(sql,[sid,list['email'],s_type])
            resaultlist=cursor.fetchone()
            if resaultlist==None:
                sqlp="insert into phone_sendlist(company_id,tocompany_id,s_id,s_email,s_mobile,s_type,s_stats) values(%s,%s,%s,%s,%s,%s,%s)"
                cursor.execute(sqlp,[company_id,list['company_id'],sid,list['email'],list['mobile'],s_type,0])
                conn.commit()
                
        
    return render_to_response('ppc/senddetail.html',locals())
    closeconn()
def sendadd(request):
    company_id=request.GET.get("company_id")
    return render_to_response('ppc/sendadd.html',locals())
    closeconn()
def sendsave(request):
    company_id=com_id=request.POST["company_id"]
    type = request.POST["type"]
    keywords = request.POST["keywords"]
    sendtitle = request.POST["sendtitle"]
    sendcontent = request.POST["sendcontent"]
    
    sql="insert into phone_keywords (company_id,type,keywords,sendtitle,sendcontent) values(%s,%s,%s,%s,%s)"
    cursor.execute(sql,[company_id,type,keywords,sendtitle,sendcontent])
    conn.commit()
    response = HttpResponse()
    response.write("<script>window.location='/ppc/sendlist/?company_id="+company_id+"'</script>")
    return response
def shuliaozst(request):
    sql="select a.name,a.business,c.mobile from crm_company_service as b left join company as a on a.id=b.company_id left join company_account as c on c.company_id=b.company_id where a.industry_code='10001000' and b.gmt_end>'2013-7-24' and b.apply_status=1"
    cursor.execute(sql)
    resaultlist=cursor.fetchall()
    i=0
    listall=[]
    for list in resaultlist:
        list={'name':list[0],'business':list[1],'mobile':list[2]}
        listall.append(list)
        i=i+1
    return render_to_response('shuliaozst.html',locals())
    closeconn()
#数据统计
def tongji(request):
    fromday=request.GET.get("fromday")
    daysnum=request.GET.get("daysnum")
    if (fromday==None):
        fromday="2013-8-1"
    if (daysnum==None):
        daysnum=30
    return render_to_response('tongji.html',locals())
    closeconn()
#数据统计曲线图
def tongji_chart(request):
    fromday=request.GET.get("fromday")
    daysnum=request.GET.get("daysnum")
    if (fromday==None):
        fromday="2014-4-1"
    format="%Y-%m-%d";
    fromday=strtodatetime(fromday,format)
    oneday=datetime.timedelta(days=1)
    if (str(daysnum)=='None'):
        daysnum=90
    listall=[] 
    for i in range(0,int(daysnum)):
        fromday=fromday+oneday
        postnum=0
        postnum=getproductnum(datetostr(fromday))
        leavewordsnum=0
        leavewordsnum=getleavewordsnum(datetostr(fromday))
        regnum=0
        regnum=getregnum(datetostr(fromday))
        if (postnum!=None):
            list={'date':datetostr(fromday),'postnum':postnum,'leavewordsnum':leavewordsnum,'regnum':regnum}
            listall.append(list)
    return render_to_response('tongji_chart.html',locals())
    closeconn()
def getmobilelist(id):
    sql="select a.name,a.business,c.mobile from company as a left join company_account as c on c.company_id=a.id where a.id="+str(id)+""
    cursor.execute(sql)
    resaultlist=cursor.fetchone()
    if (resaultlist):
        return {'name':resaultlist[0],'business':resaultlist[1],'mobile':resaultlist[2]}
def getmobile(id):
    sql="select mobile from company_account where company_id=%s"
    cursor.execute(sql,[id])
    resaultlist=cursor.fetchone()
    if resaultlist:
        if resaultlist[0]:
            return resaultlist[0]
def outmobilelist(request):
    stitle=request.GET.get("stitle")
    province=request.GET.get("province")
    hangye=request.GET.get("hangye")
    gmt_modified=gmt_created=gmt_send=datetime.datetime.now()
    content=request.GET.get("content")
    hycode=request.GET.get("hycode")
    sendflag=request.GET.get("sendflag")
    catelist=getservicecategorylist("1000")
    if (province or hangye):
        port = settings.SPHINXCONFIG['port']
        cl = SphinxClient()
        cl.SetServer ( settings.SPHINXCONFIG['serverid'], port )
        cl.SetMatchMode ( SPH_MATCH_BOOLEAN )
        cl.SetLimits (0,100000,100000)
        if hycode:
            cl.SetFilter('industry_code',[int(hycode)])
        query=""
        if province:
            query=query+"@(area_name,area_province,address) "+province
        if hangye:
            query=query+"@(name,business,sale_details,buy_details,tags) "+hangye
        res = cl.Query (query,'company')
        if res:
            if res.has_key('matches'):
                tagslist=res['matches']
                listall=[]
                i=0
                wb =xlwt.Workbook()
                ws = wb.add_sheet(u'Sheetname')
                style_k=xlwt.easyxf('align: wrap off')
                ws.col(0).width = 0x0d00 + 1000
                ws.write(0, 0, u'手机')
                
                for match in tagslist:
                    id=match['id']
                    attrs=match['attrs']
                    compname=attrs['compname']
                    pbusiness=attrs['pbusiness']
                    acountlist=getmobile(id)
                    i=i+1
                    if acountlist and acountlist!="":
                        mobilev=acountlist.strip()
                        if mobilev:
                            list={'id':id,'mobile':mobilev}
                            listall.append(list)
                            ws.write(i, 0, acountlist)
                    if acountlist and acountlist!="":
                        mobile=receiver=acountlist.strip()
                    #mobile=receiver="13666651091"
                    send_status=0
                    """
                    priority=1
                    if (str(sendflag)=="1" and content!="" and content!=None and len(mobile)>=11):
                        if (mobile!="" and mobile!=None):
                            sqla="select id from sms_log where receiver=%s and template_code='sms_zhanhui'"
                            cursor_sms.execute(sqla,[mobile])
                            resaultlist=cursor_sms.fetchone()
                            value=['sms_zhanhui',receiver,send_status,gmt_send,priority,gmt_created,gmt_modified,content]
                            if (resaultlist==None):
                                sqlp="insert into sms_log(template_code,receiver,send_status,gmt_send,priority,gmt_created,gmt_modified,content) values(%s,%s,%s,%s,%s,%s,%s,%s)"
                                cursor_sms.execute(sqlp,value)
                    """
                    
                fname = 'mobile.xls'
                agent=request.META.get('HTTP_USER_AGENT') 
                if agent and re.search('MSIE',agent):
                    response =HttpResponse(content_type="application/vnd.ms-excel") #解决ie不能下载的问题
                    response['Content-Disposition'] ='attachment; filename=%s' % fname #解决文件名乱码/不显示的问题
                else:
                    response =HttpResponse(content_type="application/vnd.ms-excel")#解决ie不能下载的问题
                    response['Content-Disposition'] ='attachment; filename=%s' % fname #解决文件名乱码/不显示的问题
                wb.save(response)
                return response
            listcount=res['total_found']
    else:
        province=""
        hangye=""
    return render_to_response('outmobilelist.html',locals())
#seo客户商铺模板管理
def seotempmanager(request):
    page=request.GET.get("page")
    domain=request.GET.get("domain")
    funpage = zz91page()
    if (page=="" or page==None):
        page=1

    limitNum=funpage.limitNum(20)
    nowpage=funpage.nowpage(int(page))
    frompageCount=funpage.frompageCount()
    after_range_num = funpage.after_range_num(2)
    before_range_num = funpage.before_range_num(9)
    sqlsear=""
    if (domain and domain!=None):
        sqlsear=sqlsear+" and a.domain_zz91 like '%"+domain+"%'"
    sqlc="select count(0) from company as a left join crm_company_service as b  on a.id=b.company_id where b.apply_status=1 and b.crm_service_code='10001002' "+sqlsear
    cursor.execute(sqlc)
    seolistcount=cursor.fetchone()[0]
    
    
    sql="select a.id,a.name,a.domain_zz91 from company as a left join crm_company_service as b  on a.id=b.company_id where b.apply_status=1 and b.crm_service_code='10001002' "+sqlsear+" limit "+str(frompageCount)+","+str(int(limitNum))+""
    cursor.execute(sql)
    resaultlist=cursor.fetchall()
    listall=[]
    if (resaultlist):
        for list in resaultlist:
            sqlp="select css,html from seo_templates where company_id=%s"
            cursor.execute(sqlp,[list[0]])
            resault=cursor.fetchone()
            if resault:
                csscode=resault[0]
                htmlcode=resault[1]
            else:
                csscode=""
                htmlcode=""
            list={'company_id':list[0],'name':list[1],'domain_zz91':list[2],'css':csscode,'html':htmlcode}
            listall.append(list)
    listcount = funpage.listcount(seolistcount)
    page_listcount=funpage.page_listcount()    
    firstpage = funpage.firstpage()
    lastpage = funpage.lastpage()
    page_range  = funpage.page_range()
    nextpage = funpage.nextpage()
    prvpage = funpage.prvpage()
    return render_to_response('seo/seotempmanager.html',locals())
    closeconn()
def templatesave(request):
    company_id=request.POST["company_id"]
    css=request.POST["css"]
    html=request.POST["html"]
    sql="select * from seo_templates where company_id=%s"
    cursor.execute(sql,[company_id])
    resault=cursor.fetchone()
    if resault:
        if (str(css)=="" and str(html)==""):
            sqla="delete from seo_templates where company_id=%s"
            cursor.execute(sqla,[company_id])
            conn.commit()
        else:
            sqla="update seo_templates set css=%s,html=%s where company_id=%s"
            cursor.execute(sqla,[css,html,company_id])
            conn.commit()
    else:
        sqla="insert into seo_templates(css,html,company_id) value(%s,%s,%s)"
        cursor.execute(sqla,[css,html,company_id])
        conn.commit()
    response = HttpResponse()
    response.write("<script>window.location='/seo/seotempmanager/'</script>")
    return response
#再生通数据导出
def companylist(request):
    kname=request.GET.get("kname")
    page=request.GET.get("page")
    service_code=request.GET.get("service_code")
    industry_code=request.GET.get("industry_code")
    servicecategorylist=getservicecategorylist("1020")
    industry_codelist=getservicecategorylist("1000")
    
    regtimefrom=request.GET.get("regtimefrom")
    regtimeto=request.GET.get("regtimeto")
    format="%Y-%m-%d";
    if regtimefrom:
        
        timeArray = time.strptime(regtimefrom, "%Y-%m-%d %H:%M:%S")
        timeStamp = int(time.mktime(timeArray))
        fd=timeStamp
        #fromday=strtodatetime(regtimefrom[0:10],format)
        #fd=datediff("1970-1-1",str(regtimefrom[0:10]))
    if regtimeto:
        
        timeArray = time.strptime(regtimeto, "%Y-%m-%d %H:%M:%S")
        timeStamp = int(time.mktime(timeArray))
        td=timeStamp
        #today=strtodatetime(regtimeto[0:10],format)
        #td=datediff("1970-1-1",str(regtimeto[0:10]))
    funpage = zz91page()
    if (page=="" or page==None):
        page=1

    limitNum=funpage.limitNum(20)
    nowpage=funpage.nowpage(int(page))
    frompageCount=funpage.frompageCount()
    after_range_num = funpage.after_range_num(2)
    before_range_num = funpage.before_range_num(9)
    sqlsear=""
    searvalue=""
    port = settings.SPHINXCONFIG['port']
    cl = SphinxClient()
    cl.SetServer ( settings.SPHINXCONFIG['serverid'], port )
    cl.SetMatchMode ( SPH_MATCH_BOOLEAN )
    cl.SetSortMode( SPH_SORT_EXTENDED,"membership_code desc,gmt_start desc" )
    if service_code:
        cl.SetFilter('service_code',[int(service_code)])
        searvalue+="&service_code="+str(service_code)
    if industry_code:
        cl.SetFilter('industry_code',[int(industry_code)])
        searvalue+="&industry_code="+str(industry_code)
    if regtimefrom and regtimeto:
        cl.SetFilterRange("regtime",int(fd),int(td))
        searvalue+="&regtimefrom="+str(regtimefrom)
        searvalue+="&regtimeto="+str(regtimeto)
    
    cl.SetLimits (frompageCount,limitNum,2000000)
    if (kname):
        res = cl.Query ('@(name,business,address,sale_details,buy_details,tags,area_name,area_province) '+kname,'company')
    else:
        res = cl.Query ('','company')
    if res:
        if res.has_key('matches'):
            tagslist=res['matches']
            listall_comp=[]
            for match in tagslist:
                id=match['id']
                attrs=match['attrs']
                regtime=attrs['regtime']
                list=getcompanydetail(id)
                if list:
                    servicename=getservice_name(list['service_code'])
                    if servicename:
                        list['servicename']=servicename
                listall_comp.append(list)
            listcount_comp=res['total_found']
    listcount = funpage.listcount(listcount_comp)
    page_listcount=funpage.page_listcount()    
    firstpage = funpage.firstpage()
    lastpage = funpage.lastpage()
    page_range  = funpage.page_range()
    nextpage = funpage.nextpage()
    prvpage = funpage.prvpage()
    return render_to_response('company_list.html',locals())
    closeconn()

def outzstcomplist(request):
    kname=request.GET.get("kname")
    port = settings.SPHINXCONFIG['port']
    cl = SphinxClient()
    cl.SetServer ( settings.SPHINXCONFIG['serverid'], port )
    cl.SetMatchMode ( SPH_MATCH_BOOLEAN )
    cl.SetSortMode( SPH_SORT_EXTENDED,"membership_code desc,gmt_start desc" )
    cl.SetFilter('apply_status',[1])
    cl.SetLimits (0,1000,20000)
    if (kname):
        res = cl.Query ('@(name,business,address,sale_details,buy_details,tags,area_name,area_province) '+kname,'company')
    else:
        res = cl.Query ('','company')
    if res:
        if res.has_key('matches'):
            tagslist=res['matches']
            listall_comp=[]
            for match in tagslist:
                id=match['id']
                #年限
                sql2="select sum(zst_year) from crm_company_service where company_id=%s and apply_status=1"
                cursor.execute(sql2,[id])
                zstNumvalue = cursor.fetchone()
                if zstNumvalue:
                    zst_year=zstNumvalue[0]
                attrs=match['attrs']
                compname=attrs['compname']
                viptype=str(attrs['membership_code'])
                membership="普通会员"
                if (viptype == '10051000'):
                    membership='普通会员'
                if (viptype == '10051001'):
                    membership='再生通'
                if (viptype == '1725773192'):
                    membership='银牌品牌通'
                if (viptype == '1725773193'):
                    membership='金牌品牌通'
                if (viptype == '1725773194'):
                    membership='钻石品牌通'
                pbusiness=attrs['pbusiness']
                parea_province=attrs['parea_province']
                industry_code=attrs['industry_code']
                list1={'id':id,'viptype':viptype,'zst_year':zst_year,'compname':compname,'business':pbusiness,'area_province':parea_province,'membership':membership,'industry_code':industry_code}
                listall_comp.append(list1)
            listcount_comp=res['total_found']
    return render_to_response('outzstcomplist.html',locals())
    closeconn()
#----微信点击统计
def weixintongji(request):
    wdate=request.GET.get("wdate")
    if wdate==None:
        wdate=str(getToday())
    format="%Y-%m-%d";
    nowday=strtodatetime(wdate,format)
    oneday=datetime.timedelta(days=1)
    
    
    def tongji(keyw,wdate):
        sql="select count(0) from weixin_count where keyw=%s and gmt_created>'"+str(nowday)+"' and gmt_created<='"+str(nowday+oneday)+"'"
        cursor.execute(sql,[keyw])
        wcount = cursor.fetchone()[0]
        return wcount
    #cshouqi=tongji("lucky",wdate)
    guanzhu=tongji("subscribe",wdate)
    unguanzhu=tongji("unsubscribe",wdate)
    newscount=tongji("http://m.zz91.com/news/",wdate)
    aqsiqcount=tongji("aqsiq",wdate)
    bindingcount=tongji("binding",wdate)
    shengyiguanjia=tongji("http://m.zz91.com/myrc_index/",wdate)
    jiaoyizhongx=tongji("http://m.zz91.com/category/",wdate)
    hangqiribao=tongji("http://m.zz91.com/weixin/priceday.html",wdate)
    #shangjidingzhi=tongji("http://m.zz91.com/order/",wdate)
    #myshangjidingzhi=tongji("http://m.zz91.com/myrc_collectmain/",wdate)
    huzhucount=tongji("http://m.zz91.com/huzhu/",wdate)
    weizhananli=tongji("http://m.zz91.com/smallsite/",wdate)
    qianbao=tongji("http://m.zz91.com/qianbao/",wdate)
    qiandao=tongji("qiandao",wdate)
    
    androdown=tongji("http://m.zz91.com/app.html",wdate)
    iosdown=tongji("https://itunes.apple.com/us/app/zz91zai-sheng-wang/id944851616?l=zh&ls=1&mt=8",wdate)
    
    fabu=tongji("http://m.zz91.com/products_publish/",wdate)
    
    
    return render_to_response('weixin/weixincount.html',locals())
    closeconn()
def saveactive_flag(request):
    active_flag=request.GET.get("active_flag")
    if active_flag!="" and active_flag:
        company_id=request.GET.get("com_id")
        gmt_created=gmt_modified=datetime.datetime.now()
        sql="select id from company_active where company_id=%s and active_flag=%s"
        cursor.execute(sql,[company_id,active_flag])
        wlist = cursor.fetchone()
        if wlist:
            x=1
        else:
          sqlu="insert into company_active(company_id,active_flag,gmt_created,gmt_modified) values(%s,%s,%s,%s)"
          cursor.execute(sqlu,[company_id,active_flag,gmt_created,gmt_modified])
          conn.commit()
    return HttpResponse("suc")
    
def __unicode__(self):
    return self
def aa():
	adfs
