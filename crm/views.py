#-*- coding:utf-8 -*-
import MySQLdb   
import settings
import codecs
from django.utils.http import urlquote
from django.shortcuts import render_to_response
from django.http import HttpResponse,HttpResponseRedirect
from django.core.paginator import Paginator,InvalidPage,EmptyPage,PageNotAnInteger
import time
import sys
import datetime,md5,hashlib
from datetime import timedelta, date 
import os
import urllib,urllib2,re
from django.core.cache import cache
from django.utils import simplejson
#from django.db.models import Q
#from django.db import connection
import random
import shutil
try:
    import cPickle as pickle
except ImportError:
    import pickle

from math import ceil
from sphinxapi import *
from zz91page import *

import socket

nowpath=os.path.dirname(__file__)
execfile(nowpath+"/conn.py")
execfile(nowpath+"/admin.py")
reload(sys)
sys.setdefaultencoding('UTF-8')
def changezhongwen(strvalue):
    if(strvalue == None):
        tempstr=""
    else:
        tempstr=strvalue.decode('GB18030','ignore').encode('utf-8')
    return tempstr
#昨天
def getYesterday():   
    today=datetime.date.today()   
    oneday=datetime.timedelta(days=1)   
    yesterday=today-oneday    
    return yesterday  

#今天     
def getToday():   
    return datetime.date.today()     
 
#获取给定参数的前几天的日期，返回一个list   
def getDaysByNum(num):   
    today=datetime.date.today()   
    oneday=datetime.timedelta(days=1)       
    li=[]        
    for i in range(0,num):   
        #今天减一天，一天一天减   
        today=today-oneday   
        #把日期转换成字符串   
        #result=datetostr(today)   
        li.append(datetostr(today))   
    return li   
 
#将字符串转换成datetime类型  
def strtodatetime(datestr,format):       
    return datetime.datetime.strptime(datestr,format)   
 
#时间转换成字符串,格式为2008-08-02   
def datetostr(date):     
    return   str(date)[0:10]   
 
#两个日期相隔多少天，例：2008-10-03和2008-10-01是相隔两天  
def datediff(beginDate,endDate):   
    format="%Y-%m-%d";
    bd=strtodatetime(str(beginDate)[0:10],format)   
    ed=strtodatetime(str(endDate)[0:10],format)       
    oneday=datetime.timedelta(days=1)   
    count=0 
    while bd!=ed:   
        ed=ed-oneday   
        count+=1 
    return count   
 
#获取两个时间段的所有时间,返回list  
def getDays(beginDate,endDate):   
    format="%Y-%m-%d";   
    bd=strtodatetime(beginDate,format)   
    ed=strtodatetime(endDate,format)   
    oneday=datetime.timedelta(days=1)    
    num=datediff(beginDate,endDate)+1    
    li=[]   
    for i in range(0,num):    
        li.append(datetostr(ed))   
        ed=ed-oneday   
    return li 
 
#获取当前年份 是一个字符串  
def getYear():   
    return str(datetime.date.today())[0:4]    
 
#获取当前月份 是一个字符串  
def getMonth():   
    return str(datetime.date.today())[5:7]   
 
#获取当前天 是一个字符串  
def getDay():
    return str(datetime.date.today())[8:10]      
def getNow():   
    return datetime.datetime.now()
def changeuft8(stringvalue):
    if (stringvalue=="" or stringvalue==None):
        return ""
    else:
        return stringvalue.decode('GB18030','ignore').encode('utf-8')
def changedate(datestring):
    if (datestring=="" or datestring==None):
        return ""
    else:
        nowsdatestr=datestring.strftime( '%Y-%m-%d %X')
        if (nowsdatestr=='1900-01-01 00:00:00'):
            nowsdatestr=""
        return nowsdatestr
def subString(string,length):   
    if length >= len(string):   
        return string   
    result = ''  
    i = 0  
    p = 0  
    while True:   
        ch = ord(string[i])   
        #1111110x   
        if ch >= 252:   
            p = p + 6  
        #111110xx   
        elif ch >= 248:   
            p = p + 5  
        #11110xxx   
        elif ch >= 240:   
            p = p + 4  
        #1110xxxx   
        elif ch >= 224:   
            p = p + 3  
        #110xxxxx   
        elif ch >= 192:
            p = p + 2  
        else:   
            p = p + 1       
        if p >= length:   
            break;
        else:   
            i = p   
    return string[0:i]
    pass
def formattime(value,flag):
    if value:
        if (flag==1):
            return value.strftime( '%-Y-%-m-%-d')
        else:
            return value.strftime( '%-Y-%-m-%-d %-H:%-M:%-S')
    else:
        return ''
def getwebhtml(baidu_url):
    f = urllib.urlopen(baidu_url)
    html = f.read()
    return html
def getsid(kid):
    sqls="select sid from seo_keywordslist where id="+str(kid)+""
    cursor.execute(sqls)
    result=cursor.fetchone()
    if result:
        return result[0]
def getbaidulist(html):
    html=html.split('<div id="content_left">')
    if len(html1)>1:
        html1=html[1]
        html2=html1.split('<div style="clear:both;height:0;"></div>')
        html3=html2[0]
    else:
        html3=""
    return html3

def get_url_content2(url):#突破网站防爬
    i_headers = {"User-Agent": "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9.1) Gecko/20090624 Firefox/3.5",\
                 "Referer": 'http://www.baidu.com'}
    req = urllib2.Request(url, headers=i_headers)
    html=urllib2.urlopen(req).geturl()
    return html
def get_url_content(url):#突破网站防爬
    i_headers = {"User-Agent": "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9.1) Gecko/20090624 Firefox/3.5",\
                 "Referer": 'http://www.baidu.com'}
    req = urllib2.Request(url, headers=i_headers)
    html=urllib2.urlopen(req).read()
    return html

def get_content(re_py,html):
    urls_pat=re.compile(re_py,re.DOTALL)
    content=re.findall(urls_pat,html)
    return content

#seo抓取数据
def zqweb(request):
    k=request.GET.get("k")
    id=request.GET.get("id")
    check_url=request.GET.get("check_url")
    if len(check_url)>16:
        check_url=check_url[:16]
    check_url=check_url.encode('utf-8')
    
    html=""
    weblist=[0,10,20,30,40,50,60,70,80,90]
        
    
    def saveh(html,id,check_url):    
        re_py=r'http://www.baidu.com/link\?url=.*?"'
        re_hy='<div class="result c-container ".*?</div>'
        html=html.split('<h3 class="t">')
        i=0
        c=0
        for list in html:
            #list=list.replace("<b>","")
            #list=list.replace("</b>","")
            if i>0:
                if (list.find(check_url)>0):
                    c=1
                    savedb(id,c,i)
                    return i
                    break
            i=i+1
            """
            kthml=get_content(re_py,list)
            if kthml:
                try:
                    kt=get_url_content2(kthml[0][:-1])
                except:
                    break
                print kt
                if check_url in kt:
                    c=1
                    savedb(id,c,i)
                    return i
                    break
            """
            
    def savedb(id,c,i):
        if (c==0):
            i=100
        if (i<=10):
            dbtype=1
        else:
            dbtype=0
        sql="update seo_keywordslist set baidu_ranking="+str(i)+",dbtype="+str(dbtype)+" where id="+str(id)
        cursor.execute(sql)
        #conn.commit()
        sqls="select sid from seo_keywordslist where id="+str(id)
        cursor.execute(sqls)
        result=cursor.fetchone()
        if (result):
            gxdb(result[0])
        #-----更新历史记录
        sqlk="select * from seo_keywords_history where kid="+str(id)+" and kdate='"+str(getToday())+"' and baidu_ranking="+str(i)+" and ktype='check_pai'"
        cursor.execute(sqlk)
        result=cursor.fetchone()
        if (result==None):
            sqlp="insert into seo_keywords_history(sid,kid,ktype,baidu_ranking,kdate) values("+str(getsid(id))+","+str(id)+",'check_pai',"+str(i)+",'"+str(getToday())+"')"
            cursor.execute(sqlp)
        conn.commit()
    baiduranking=100
    #return HttpResponse(check_url)
    for l in weblist:
        baidu_url="http://www.baidu.com/s?q1="+k.encode('utf-8')+"&pn="+str(l)
        nhtml=getwebhtml(baidu_url)
        html=html+nhtml
        if (nhtml.find(check_url)>0):
            break
    
    rehtml=saveh(html,id,check_url)
    if rehtml:
        baiduranking=rehtml
    #return HttpResponse(html)
    if baiduranking==100:
        savedb(id,0,100)
    html='var _suggest_result_={"baiduranking":'+str(baiduranking)+'}'
    return render_to_response('zqweb.html',locals())
def gxdb(id):
    sql="select id from seo_list where id="+str(id)
    cursor.execute(sql)
    result=cursor.fetchall()
    if (result):
        for list in result:
            sid=list[0]
            sqld="select id from seo_keywordslist where dbtype=0 and sid="+str(sid)+""
            cursor.execute(sqld)
            resultd=cursor.fetchone()
            if resultd==None:
                sqlp="update seo_list set dbflag=1 where id="+str(sid)+""
                cursor.execute(sqlp)
                conn.commit()
            else:
                sqlp="update seo_list set dbflag=0 where id="+str(sid)+""
                cursor.execute(sqlp)
                conn.commit()
#ICD公海分配
def icdassign(request):
    id=request.GET.get("id")
    assign=str(request.GET.get("assign"))
    sql="select lastcontacttime1,lastcontacttime2,lastlogintime1,lastlogintime2,regtime1,regtime2,province,togonghaitime1,togonghaitime2,telcount1,notelcount1,telcount2,notelcount2,comrank,trade,star5,star4,logincount1,logincount2,adminreg,assign_time,telpersoncount1,telpersoncount2,id,assigncount from icd_gonghai_assign where assignflag=0 and id="+str(id)+""
    cursor.execute(sql)
    results = cursor.fetchall()
    listcount=0
    if results:
        for a in results:
            lastcontacttime1=a[0]
            lastcontacttime2=a[1]
            lastlogintime1=a[2]
            lastlogintime2=a[3]
            regtime1=a[4]
            regtime2=a[5]
            province=changezhongwen(a[6])
            togonghaitime1=a[7]
            togonghaitime2=a[8]
            telcount1=a[9]
            telnocount1=a[10]
            telcount2=a[11]
            telnocount2=a[12]
            comrank=a[13]
            trade=changezhongwen(a[14])
            star5=a[15]
            star4=a[16]
            logincount1=a[17]
            logincount2=a[18]
            adminreg=a[19]
            assign_time=a[20]
            telpersoncount1=a[21]
            telpersoncount2=a[22]
            id=a[23]
            assigncount=a[24]

            #销售数
            sqlu="select count(id) from users where userid like  '13__' and closeflag=1 and assigngonghai=1 and chatflag=1 and chatclose=1"
            cursor.execute(sqlu)
            reusers=cursor.fetchone()
            if reusers:
                usercount=reusers[0]
            if (usercount>0):
                port = 9315
                
                cl = SphinxClient()
                cl.SetServer ('192.168.2.21', port)
                cl.SetMatchMode ( SPH_MATCH_BOOLEAN )
                cl.SetFilter('personid',[0])
                cl.SetFilter('zst',[0])
                cl.SetFilter('vap',[0])
                
                query=""
                
                #最后联系时间
                if (lastcontacttime1):
                    fromlasttelf=datediff('1970-1-1',lastcontacttime1)
                else:
                    fromlasttelf=0

                if (lastcontacttime2):
                    fromlasttelt=datediff('1970-1-1',lastcontacttime2)
                else:
                    fromlasttelt=datediff('1970-1-1',getToday().strftime( '%-Y-%-m-%-d'))

                
                if (lastcontacttime1):
                    cl.SetFilterRange('teldate1',int(fromlasttelf),int(fromlasttelt))
                    
                #最后登录时间
                if (lastlogintime1):
                    Lfromdatef=datediff('1970-1-1',lastlogintime1)
                else:
                    Lfromdatef=0

                if (lastlogintime2):
                    Lfromdatet=datediff('1970-1-1',lastlogintime2)
                else:
                    Lfromdatet=datediff('1970-1-1',getToday().strftime( '%-Y-%-m-%-d'))

                if (lastlogintime1):
                    cl.SetFilterRange('lastlogintime1',int(Lfromdatef),int(Lfromdatet))
                #注册时间
                if (regtime1):
                    Regfromdate1=datediff('1970-1-1',regtime1)
                else:
                    Regfromdate1=0

                if (regtime2):
                    Regtodate1=datediff('1970-1-1',regtime2)
                else:
                    Regtodate1=datediff('1970-1-1',getToday().strftime( '%-Y-%-m-%-d'))

                if (regtime1):
                    cl.SetFilterRange('com_regtime1',int(Regfromdate1),int(Regtodate1))
                #省份
                if (province and province!='' and province!='请选择...'):
                    query+='@(com_province,com_add) '+province

                #丢公海时间
                if (togonghaitime1):
                    togonghaitime1=datediff('1970-1-1',togonghaitime1)
                else:
                    togonghaitime1=0
                if (togonghaitime2):
                    togonghaitime2=datediff('1970-1-1',togonghaitime2)
                else:
                    togonghaitime2=datediff('1970-1-1',getToday().strftime( '%-Y-%-m-%-d'))
                if (togonghaitime1):
                    cl.SetFilterRange('outtime',int(togonghaitime1),int(togonghaitime2))
                    
                #联系次数
                if (telcount1 and telcount2):
                    cl.SetFilterRange('telcount',int(telcount1),int(telcount2))
                #无效联系次数
                if (telnocount1 and telnocount2):
                    cl.SetFilterRange('telnocount',int(telnocount1),int(telnocount2))
                
                #联系人数
                if (telpersoncount1 and telpersoncount2):
                    cl.SetFilterRange('telpersoncount',int(telpersoncount1),int(telpersoncount2))
                #客户等级
                if (comrank and comrank!=""):
                    frank=float(comrank)-0.01
                    trank=float(comrank)
                    cl.SetFilterFloatRange('com_rank',frank,trank)
                #主营业务
                if (trade and trade!='' and trade!=' '):
                    query+='@com_productslist_en '+trade
        
                #登录次数
                if (logincount1 and logincount2):
                    cl.SetFilterRange('logincount',int(logincount1),int(logincount2))
                    
                #是否录入
                if(adminreg=="1"):
                    cl.SetFilterRange('addcompany',1,10000000)
                #曾4、5星
                if (star4):
                    cl.SetFilter('have4star',[1])
                if (star5):
                    cl.SetFilter('have5star',[1])

                cl.SetSortMode( SPH_SORT_EXTENDED,"com_regtime2 desc")
                cl.SetLimits (0,10000,10000)
                res = cl.Query (query,'crminfo')
                
                personid=0
                n=0
                m=0
                html=""

                if (res):
                    listcount=res['total_found']
                    if (assign=="1"):
                        listcount_all=listcount
                        if res.has_key('matches'):
                            tagslist=res['matches']
                            listall=[]
                            for match in tagslist:
                                com_id=match['id']
                                #是否已经存在公海分配库里
                                sqlp="select com_id from crm_assign_gonghai where com_id="+str(com_id)+""
                                cursor.execute(sqlp)
                                assingflag_gonghai=cursor.fetchone()
                                
                                sqlp="select com_id from crm_assign where com_id="+str(com_id)+""
                                cursor.execute(sqlp)
                                assingflag=cursor.fetchone()
                                if (assingflag==None and personid!=None and assingflag_gonghai==None and m<=int(assigncount)):
                                    sqlt="select min(id) from users where userid like  '13__' and closeflag=1 and assigngonghai=1 and chatflag=1 and chatclose=1 and id>"+str(personid)+""
                                    cursor.execute(sqlt)
                                    puser=cursor.fetchone()
                                    if puser:
                                        personid=puser[0]
                                    n=n+1
                                    if (personid!=None):
                                        m=m+1
                                        
                                        sqli="insert into crm_assign_gonghai (com_id,personid,pid) values(%s,%s,%s)"
                                        cursor.execute(sqli,(com_id,personid,id))
                                        conn.commit()
                                        
                                        
                                        sqli="insert into crm_assign (com_id,personid) values(%s,%s)"
                                        cursor.execute(sqli,(com_id,personid))
                                        conn.commit()
                                        sqlo="insert into crm_assignHistory(com_id,personid,SDetail,mypersonid) values("+str(com_id)+",0,'gonghai system assign',"+str(personid)+")"
                                        cursor.execute(sqlo)
                                        conn.commit()
                                        
                                        html=html+"分配"+str(com_id)+"成功！"+str(m)+"<br />"
                                        if (n>=usercount):
                                            personid=0
                                            n=0    
                                        
            if (assign!="1"):
                sqlh="update icd_gonghai_assign set compcount="+str(listcount)+" where id="+str(id)
                cursor.execute(sqlh)
                conn.commit()
                html='var _suggest_result_={"compcount":'+str(listcount)+'}'

    return render_to_response('icdassign.html',locals())
    closeconn()
#商务大全录入
def huangyeadd(request):
    localIP="192.168.2.2"
    return render_to_response('huangyeadd.html',locals())
    closeconn()
def huangye(request):
    port = 9315
    cl = SphinxClient()
    province = request.GET.get("province")
    productlist = request.GET.get("productlist")
    if (province==None):
        province=''
    if (productlist==None):
        productlist=''
    ss=request.GET.get("ss")
    if (ss==None):
        ss="2"
    listall=[]
    if (ss=="1"):
        nindex="huangyeinfo2"
        nindextext="私海"
    if (ss=="2"):
        nindex="huangyeinfo1"
        nindextext="公海"
    if (ss=="3"):
        nindex="huangyeinfo3"
        nindextext="2011-1-1后联系私海"
    if (ss=="4"):
        nindex="huangyeinfo4"
        nindextext="2011-1-1后联系公海"
    button = request.GET.get("button")
    if (button and (productlist!="" or province!="")):
        cl.SetServer ('192.168.2.21', port)
        cl.SetMatchMode ( SPH_MATCH_BOOLEAN )
        cl.SetLimits (0,10000,10000)
        searchstr=""
        exip=0
        if (province!=None and province!=''):
            searchstr=searchstr+"(@com_province "+province+" | @com_add "+province+") "
            exip=1
        if (productlist!=None and productlist!='' and exip==1):
            searchstr=searchstr+"&@(com_productslist_en,com_name) "+productlist
        if (productlist!=None and productlist!='' and exip==0):
            searchstr=searchstr+"@(com_productslist_en,com_name) "+productlist
        res = cl.Query (searchstr,nindex)
        if res:
            if res.has_key('matches'):
                tagslist=res['matches']
                comidlist=""
                i=0
                for match in tagslist:
                    sql="select com_name,com_tel,com_mobile,com_contactperson,com_desi,com_add,com_productslist_en,com_intro FROM temp_salescomp where com_id="+str(match['id'])
                    cursor.execute(sql)
                    arrkname=cursor.fetchone()
                    i=i+1
                    if (arrkname):
                        com_id=str(match['id'])
                        if arrkname[0]:
                            com_name=arrkname[0].decode('GB18030','ignore').encode('utf-8')
                        else:
                            com_name=''
                        if arrkname[1]:
                            com_tel=arrkname[1].decode('GB18030','ignore').encode('utf-8')
                        else:
                            com_tel=''
                        if (arrkname[2]):
                            com_mobile=arrkname[2].decode('GB18030','ignore').encode('utf-8')
                        else:
                            com_mobile=''
                        if (arrkname[3]):
                            com_contactperson=arrkname[3].decode('GB18030','ignore').encode('utf-8')
                        else:
                            com_contactperson=''
                        if (arrkname[4]):
                            com_desi=arrkname[4].decode('GB18030','ignore').encode('utf-8')
                        else:
                            com_desi=''
                        if (arrkname[5]):
                            com_add=arrkname[5].decode('GB18030','ignore').encode('utf-8')
                        else:
                            com_add=''
                        if (arrkname[6]):
                            com_productslist=arrkname[6].decode('GB18030','ignore').encode('utf-8')
                        else:
                            com_productslist=''
                        if (arrkname[7]):
                            com_intro=arrkname[7].decode('GB18030','ignore').encode('utf-8')
                        else:
                            com_intro=''
                        list={'id':i,'com_id':com_id,'com_name':com_name,'com_tel':com_tel,'com_mobile':com_mobile,'com_contactperson':com_contactperson+com_desi,'com_add':com_add,'com_productslist':com_productslist,'com_intro':subString(com_intro,500)}
                        listall.append(list)
                        comidlist=comidlist+str(com_id)+":"
            listcount=res['total_found']
            """
            sql="select id from huanye_search where searchname='"+searchname+"'"
            cursor.execute(sql)
            arrresalt=cursor.fetchone()
            if (!arrresalt):
                sql="insert into huanye_search (searchname,arrcom_id) values('"+productlist+"','"+comidlist+"')"
            """
                

    return render_to_response('huangye.html',locals())
    closeconn()

#2013黄页导出
def huangye2013(request):
    port = 9315
    cl = SphinxClient()
    cl.SetServer ('192.168.2.21', port)
    cl.SetMatchMode ( SPH_MATCH_BOOLEAN )
    cl.SetLimits (0,10000,10000)
    membertype1=request.GET.get("membertype1")
    if membertype1:
        cl.SetFilter('membertype',[int(membertype1)])
    comkeywords1=request.GET.get("comkeywords1")
    if comkeywords1:
        cl.SetFilter('comkeywords',[int(comkeywords1)])
    searchstr=""
    cproductslist1=request.GET.get("cproductslist1")
    slselect=request.GET.get("slselect")
    jsselect=request.GET.get("jsselect")
    if (slselect==None):
        slselect=""
    if (jsselect==None):
        jsselect=""
    cadd1=request.GET.get("cadd1")
    if (cadd1==None):
        cadd1=""

    if (slselect=="0"):
        searchstr=searchstr+"@cproductslist (otherlist !PET !pp !PE !ABS !PVC !PS !PA !PC !PVB !PMMA !EVA)"
    if (slselect!="0" and slselect!=""):
        searchstr=searchstr+"@cproductslist "+slselect+""
    #if (jsselect=="0"):
        #searchstr=searchstr+"@cproductslist (otherlist !铜 & !铁 & !铝 & !镍 & !锌 & !锡 & !电缆 & !电线 & !合金 & !工具钢)"
    if (jsselect!="0" and jsselect!=""):
        searchstr=searchstr+"@cproductslist "+jsselect+""
                
    if (cadd1!=""):
        searchstr=searchstr+"&@(cadd,province) "+cadd1+""
        
    if (searchstr!="" or membertype1!="" or comkeywords1!=""):
        res = cl.Query (searchstr,"huangyeinfo_2013")
        if res:
            if res.has_key('matches'):
                list=res['matches']
                listall=[]
                for match in list:
                    id=match['id']
                    sql="select id,com_email,membertype,com_id,cname,comkeywords,province,cproductslist,ccontactp,ctel,cmobile,cadd from huangye_list where id=%s"
                    cursor.execute(sql,id)
                    result=cursor.fetchone()
                    if result:
                        com_email=result[1].decode('GB18030','ignore').encode('utf-8')
                        membertype=result[2]
                        com_id=result[3]
                        cname=result[4].decode('GB18030','ignore').encode('utf-8')
                        comkeywords=result[5]
                        province=result[6].decode('GB18030','ignore').encode('utf-8')
                        cproductslist=result[7].decode('GB18030','ignore').encode('utf-8')
                        cproductslist=cproductslist.replace("，",",")
                        slist=""
                        for s in range(len(cproductslist)):
                            slist=slist+cproductslist[s]
                            mm=s % 10
                            if (str(mm)=="1"):
                                slist=slist+"<br>"
                        #cproductslist=slist
                        ccontactp=result[8].decode('GB18030','ignore').encode('utf-8')
                        ctel=result[9].decode('GB18030','ignore').encode('utf-8')
                        cmobile=result[10].decode('GB18030','ignore').encode('utf-8')
                        cadd=result[11].decode('GB18030','ignore').encode('utf-8')
                        if (ctel=="" or ctel==" "):
                            ctel=None
                        list={'id':id,'com_email':com_email,'membertype':membertype,'com_id':com_id,'cname':cname,'comkeywords':comkeywords,'province':province,'cproductslist':cproductslist,'ccontactp':ccontactp,'ctel':ctel,'cmobile':cmobile,'cadd':cadd}
                        listall.append(list)
                listcount=res['total_found']
    return render_to_response('huangye2013.html',locals())
    closeconn()
#2014黄页导出
def huangye2014(request):
    port = 9315
    cl = SphinxClient()
    cl.SetServer ('192.168.2.21', port)
    cl.SetMatchMode ( SPH_MATCH_BOOLEAN )
    cl.SetLimits (0,10000,10000)
    membertype1=request.GET.get("membertype1")
    if membertype1:
        cl.SetFilter('membertype',[int(membertype1)])
    comkeywords1=request.GET.get("comkeywords1")
    if comkeywords1:
        cl.SetFilter('comkeywords',[int(comkeywords1)])
    searchstr=""
    cproductslist1=request.GET.get("cproductslist1")
    slselect=request.GET.get("slselect")
    jsselect=request.GET.get("jsselect")
    slselect1=1
    jsselect1=1
    if (slselect==None or slselect==""):
        slselect=""
        slselect1=None
        
    if (jsselect==None or jsselect==""):
        jsselect=""
        jsselect1=None
        
    cadd1=request.GET.get("cadd1")
    if (cadd1==None):
        cadd1=""
    
    if (comkeywords1=="1" and jsselect!="0" and jsselect!=""):
        searchstr=searchstr+"@(js1,js2) "+jsselect+""
    if (comkeywords1=="2" and slselect!="0" and slselect!=""):
        searchstr=searchstr+"@(sl1) "+slselect+""
                
    if (cadd1!=""):
        searchstr=searchstr+"&@(province) "+cadd1+""
        
    if (searchstr!="" or membertype1!="" or comkeywords1!=""):
        res = cl.Query (searchstr,"huangyeinfo_2014")
        if res:
            if res.has_key('matches'):
                list=res['matches']
                listall=[]
                for match in list:
                    id=match['id']
                    sql="select id,com_email,membertype,com_id,cname,comkeywords,province,cproductslist,ccontactp,ctel,cmobile,cadd,newemail from huangye_list where id=%s"
                    cursor.execute(sql,id)
                    result=cursor.fetchone()
                    if result:
                        com_email=result[1]
                        membertype=result[2]
                        com_id=result[3]
                        cname=result[4].decode('GB18030','ignore').encode('utf-8')
                        comkeywords=result[5]
                        province=result[6].decode('GB18030','ignore').encode('utf-8')
                        cproductslist=result[7].decode('GB18030','ignore').encode('utf-8')
                        cproductslist=cproductslist.replace("，",",")
                        slist=""
                        for s in range(len(cproductslist)):
                            slist=slist+cproductslist[s]
                            mm=s % 10
                            if (str(mm)=="1"):
                                slist=slist+"<br>"
                        #cproductslist=slist
                        ccontactp=result[8].decode('GB18030','ignore').encode('utf-8')
                        ctel=result[9]
                        if ctel:
                            ctel=ctel.decode('GB18030','ignore').encode('utf-8')
                        else:
                            ctel=""
                        cmobile=result[10].decode('GB18030','ignore').encode('utf-8')
                        cadd=result[11].decode('GB18030','ignore').encode('utf-8')
                        newemail=result[12]
                        #newemail=str(newemail)+str(com_email)
                        if newemail:
                            newemail=newemail.strip()
                           
                        if (newemail==None or newemail==""):
                            if (com_email):
                                newemail=com_email.strip()
                            else:
                                newemail=None
                        else:
                            newemail=newemail
                        if newemail:
                            if ("zz91.com" in newemail):
                                newemail=None
                        
                        if (ctel=="" or ctel==" "):
                            ctel=None
                        list={'id':id,'com_email':newemail,'membertype':membertype,'com_id':com_id,'cname':cname,'comkeywords':comkeywords,'province':province,'cproductslist':cproductslist,'ccontactp':ccontactp,'ctel':ctel,'cmobile':cmobile,'cadd':cadd}
                        listall.append(list)
                listcount=res['total_found']
    return render_to_response('huangye2014.html',locals())
    closeconn()
def gethuanye2015(comkeywords1,jsselect="",slselect="",otselect="",cadd1=""):
    port = 9315
    cl = SphinxClient()
    cl.SetServer ('192.168.2.21', port)
    cl.SetMatchMode ( SPH_MATCH_BOOLEAN )
    cl.SetLimits (0,10000,10000)
    searchstr=""
    if (cadd1==None):
        cadd1=""
    if (comkeywords1=="1"):
        searchstr=searchstr+"@(js1,js2) "+jsselect
    if (comkeywords1=="2"):
        searchstr=searchstr+"@(sl1,sl2) "+slselect+""
    if (comkeywords1=="3"):
        searchstr=searchstr+"@(qt1,qt2) "+otselect+""
    #if (cadd1!=""):
        #searchstr=searchstr+"&@(province) "+cadd1+""
    #return searchstr
    if (searchstr!=""):
        res = cl.Query ("@(js1,js2) 贵金属","huangyeinfo_2015")
        if res:
            if res.has_key('matches'):
                list=res['matches']
                listall=[]
                for match in list:
                    id=match['id']
                    sql="select id,com_email,membertype,com_id,cname,comkeywords,province,cproductslist,ccontactp,ctel,cmobile,cadd,newemail from huangye_list where id=%s"
                    cursor.execute(sql,id)
                    result=cursor.fetchone()
                    if result:
                        com_email=result[1]
                        membertype=result[2]
                        com_id=result[3]
                        cname=result[4].decode('GB18030','ignore').encode('utf-8')
                        comkeywords=result[5]
                        province=result[6].decode('GB18030','ignore').encode('utf-8')
                        cproductslist=result[7].decode('GB18030','ignore').encode('utf-8')
                        cproductslist=cproductslist.replace("，",",")
                        slist=""
                        for s in range(len(cproductslist)):
                            slist=slist+cproductslist[s]
                            mm=s % 10
                            if (str(mm)=="1"):
                                slist=slist+"<br>"
                        #cproductslist=slist
                        ccontactp=result[8].decode('GB18030','ignore').encode('utf-8')
                        ctel=result[9]
                        if ctel:
                            ctel=ctel.decode('GB18030','ignore').encode('utf-8')
                        else:
                            ctel=""
                        cmobile=result[10].decode('GB18030','ignore').encode('utf-8')
                        cadd=result[11].decode('GB18030','ignore').encode('utf-8')
                        newemail=result[12]
                        #newemail=str(newemail)+str(com_email)
                        if newemail:
                            newemail=newemail.strip()
                           
                        if (newemail==None or newemail==""):
                            if (com_email):
                                newemail=com_email.strip()
                            else:
                                newemail=None
                        else:
                            newemail=newemail
                        if newemail:
                            if ("zz91.com" in newemail):
                                newemail=None
                        
                        if (ctel=="" or ctel==" "):
                            ctel=None
                        list={'id':id,'com_email':newemail,'membertype':membertype,'com_id':com_id,'cname':cname,'comkeywords':comkeywords,'province':province,'cproductslist':cproductslist,'ccontactp':ccontactp,'ctel':ctel,'cmobile':cmobile,'cadd':cadd}
                        listall.append(list)
def huangye2015000(request):
    #port = 9315
    #cl = SphinxClient()
    #cl.SetServer ('192.168.2.21', port)
    #cl.SetMatchMode ( SPH_MATCH_BOOLEAN )
    #cl.SetLimits (0,10000,10000)
    
    js="贵金属|稀有金属|有色金属|钢铁|其他类"
    sl="PP|PET|PE|ABS|PVC|PS|PA|PC|PVB|PMMA|EVA|PU|其他类"
    ot="橡胶|纺织|废纸|废电子电器|服务行业|其他"
    
    dq="浙江|江苏|上海-广东|福建-山东|河南|河北-湖南|湖北-(otherprovince !浙江 !江苏 !上海 !广东 !福建 !河北 !山东 !河南 !湖南 !湖北)"
    
    listall=[]
    jslist=js.split("|")
    dqlist=dq.split("-")
    for l in jslist:
        for ll in dqlist:
            list=gethuanye2015("1",jsselect=l,cadd1=ll)
            listall.append({'dl':"废金属",'lb1':l,'lb2':ll,'list':list})
            
    
    
    
    return render_to_response('huangye2015.html',locals())
#2015黄页导出
def huangye2015(request):
    port = 9315
    cl = SphinxClient()
    cl.SetServer ('192.168.2.21', port)
    cl.SetMatchMode ( SPH_MATCH_BOOLEAN )
    cl.SetLimits (0,10000,10000)
    membertype1=request.GET.get("membertype1")
    if membertype1:
        cl.SetFilter('membertype',[int(membertype1)])
    comkeywords1=request.GET.get("comkeywords1")
    if comkeywords1:
        cl.SetFilter('comkeywords',[int(comkeywords1)])
    searchstr=""
    cproductslist1=request.GET.get("cproductslist1")
    slselect=request.GET.get("slselect")
    jsselect=request.GET.get("jsselect")
    otselect=request.GET.get("otselect")
    slselect1=1
    jsselect1=1
    otselect1=1
    if (slselect==None or slselect==""):
        slselect=""
        slselect1=None
        
    if (jsselect==None or jsselect==""):
        jsselect=""
        jsselect1=None
    if (otselect1==None or otselect==""):
        otselect=""
        otselect1=None
        
    cadd1=request.GET.get("cadd1")
    if (cadd1==None):
        cadd1=""
    ss2=""
    if (comkeywords1=="1" and jsselect!="0" and jsselect!=""):
        searchstr=searchstr+"@(js1,js2) "+jsselect+""
        ss2=1
    if (comkeywords1=="2" and slselect!="0" and slselect!=""):
        searchstr=searchstr+"@(sl1,sl2) "+slselect+""
        ss2=1
    if (comkeywords1=="3" and otselect!="0" and otselect!=""):
        searchstr=searchstr+"@(qt1,qt2) "+otselect+""
        ss2=1
                
    if (cadd1!=""):
        searchstr=searchstr+"&@(province) "+cadd1+""
    #searchstr="@(js1,js2) 贵金属"
    #cache.set('listid'+comkeywords1, [], 15*600)
    #idlists=cache.get('listid')
    s = hashlib.md5(searchstr)
    s = s.hexdigest()[8:-8]
    """
    idlist=cache.get('listid'+searchstr)
    idlist=[]
    
    if (searchstr!="" and cadd1!="" and ss2==1):
        res = cl.Query (searchstr,"huangyeinfo_2015")
        if res:
            if res.has_key('matches'):
                list=res['matches']
                
                for match in list:
                    id=match['id']

                    
                    sqlc="select id from temp_huangye where searchtext='"+s+"' and com_id="+str(id)+""
                    cursor.execute(sqlc)
                    result=cursor.fetchone()
                    if not result:
                        sqlp="insert into temp_huangye(searchtext,com_id,scount) values('"+s+"',"+str(id)+",1)"
                        cursor.execute(sqlp)
                        conn.commit()
                    
                        
                    
                    idlist.append(id) 
                        
    """           
                
    listall=[]
    sqlh="select com_id from v_huangye where searchtext='"+s+"'"
    cursor.execute(sqlh)
    results=cursor.fetchall()
    if results:
        for l in results:
            sql="select id,com_email,membertype,com_id,cname,comkeywords,province,cproductslist,ccontactp,ctel,cmobile,cadd,newemail from huangye_list where id=%s"
            cursor.execute(sql,l[0])
            result=cursor.fetchone()
            if result:
                com_email=result[1]
                membertype=result[2]
                com_id=result[3]
                cname=result[4].decode('GB18030','ignore').encode('utf-8')
                comkeywords=result[5]
                province=result[6].decode('GB18030','ignore').encode('utf-8')
                cproductslist=result[7].decode('GB18030','ignore').encode('utf-8')
                cproductslist=cproductslist.replace("，",",")
                slist=""
                for s in range(len(cproductslist)):
                    slist=slist+cproductslist[s]
                    mm=s % 10
                    if (str(mm)=="1"):
                        slist=slist+"<br>"
                #cproductslist=slist
                ccontactp=result[8].decode('GB18030','ignore').encode('utf-8')
                ctel=result[9]
                if ctel:
                    ctel=ctel.decode('GB18030','ignore').encode('utf-8')
                else:
                    ctel=""
                cmobile=result[10].decode('GB18030','ignore').encode('utf-8')
                cadd=result[11].decode('GB18030','ignore').encode('utf-8')
                newemail=result[12]
                #newemail=str(newemail)+str(com_email)
                if newemail:
                    newemail=newemail.strip()
                   
                if (newemail==None or newemail==""):
                    if (com_email):
                        newemail=com_email.strip()
                    else:
                        newemail=None
                else:
                    newemail=newemail
                if newemail:
                    if ("zz91.com" in newemail):
                        newemail=None
                
                if (ctel=="" or ctel==" "):
                    ctel=None
                list={'id':l,'com_email':newemail,'membertype':membertype,'com_id':com_id,'cname':cname,'comkeywords':comkeywords,'province':province,'cproductslist':cproductslist,'ccontactp':ccontactp,'ctel':ctel,'cmobile':cmobile,'cadd':cadd}
                listall.append(list)
    listcount=len(listall)
    return render_to_response('huangye2015.html',locals())
    closeconn()
#2016黄页导出
def huangye2016(request):
    port = 9315
    cl = SphinxClient()
    cl.SetServer ('192.168.2.21', port)
    cl.SetMatchMode ( SPH_MATCH_BOOLEAN )
    cl.SetLimits (0,10000,10000)
    membertype1=request.GET.get("membertype1")
    if membertype1:
        cl.SetFilter('membertype',[int(membertype1)])
    comkeywords1=request.GET.get("comkeywords1")
    if comkeywords1:
        cl.SetFilter('comkeywords',[int(comkeywords1)])
    searchstr=""
    cproductslist1=request.GET.get("cproductslist1")
    slselect=request.GET.get("slselect")
    jsselect=request.GET.get("jsselect")
    otselect=request.GET.get("otselect")
    slselect1=1
    jsselect1=1
    otselect1=1
    if (slselect==None or slselect==""):
        slselect=""
        slselect1=None
        
    if (jsselect==None or jsselect==""):
        jsselect=""
        jsselect1=None
    if (otselect1==None or otselect==""):
        otselect=""
        otselect1=None
        
    cadd1=request.GET.get("cadd1")
    if (cadd1==None):
        cadd1=""
    ss2=""
    if (comkeywords1=="1" and jsselect!="0" and jsselect!=""):
        searchstr=searchstr+"@(js1,js2) "+jsselect+""
        ss2=1
    if (comkeywords1=="2" and slselect!="0" and slselect!=""):
        searchstr=searchstr+"@(sl1,sl2) "+slselect+""
        ss2=1
    if (comkeywords1=="3" and otselect!="0" and otselect!=""):
        searchstr=searchstr+"@(qt1,qt2) "+otselect+""
        ss2=1
                
    if (cadd1!=""):
        searchstr=searchstr+"&@(province) "+cadd1+""

    s = hashlib.md5(searchstr)
    s = s.hexdigest()[8:-8]
    
    """
    if (searchstr!="" and cadd1!="" and ss2==1):
        res = cl.Query (searchstr,"huangyeinfo_2016")
        if res:
            if res.has_key('matches'):
                list=res['matches']
                
                for match in list:
                    id=match['id']
                    
                    sqlc="select id from temp_huangye2016 where searchtext='"+s+"' and com_id="+str(id)+""
                    cursor.execute(sqlc)
                    result=cursor.fetchone()
                    if not result:
                        sqlp="insert into temp_huangye2016(searchtext,com_id,scount) values('"+s+"',"+str(id)+",1)"
                        cursor.execute(sqlp)
                        conn.commit()
    #return render_to_response('huangye2016.html',locals())
    """
                
    listall=[]
    sqlh="select com_id from v_huangye2016 where searchtext='"+s+"'"
    cursor.execute(sqlh)
    results=cursor.fetchall()
    if results:
        for l in results:
            sql="select id,com_email,membertype,com_id,cname,comkeywords,province,cproductslist,ccontactp,ctel,cmobile,cadd,newemail from huangye_list where id=%s"
            cursor.execute(sql,l[0])
            result=cursor.fetchone()
            if result:
                com_email=result[1]
                membertype=result[2]
                com_id=result[3]
                cname=result[4].decode('GB18030','ignore').encode('utf-8')
                comkeywords=result[5]
                province=result[6].decode('GB18030','ignore').encode('utf-8')
                cproductslist=result[7].decode('GB18030','ignore').encode('utf-8')
                cproductslist=cproductslist.replace("，",",")
                slist=""
                for s in range(len(cproductslist)):
                    slist=slist+cproductslist[s]
                    mm=s % 10
                    if (str(mm)=="1"):
                        slist=slist+"<br>"
                #cproductslist=slist
                ccontactp=result[8].decode('GB18030','ignore').encode('utf-8')
                ctel=result[9]
                if ctel:
                    ctel=ctel.decode('GB18030','ignore').encode('utf-8')
                else:
                    ctel=""
                cmobile=result[10].decode('GB18030','ignore').encode('utf-8')
                cadd=result[11].decode('GB18030','ignore').encode('utf-8')
                newemail=result[12]
                #newemail=str(newemail)+str(com_email)
                if newemail:
                    newemail=newemail.strip()
                   
                if (newemail==None or newemail==""):
                    if (com_email):
                        newemail=com_email.strip()
                    else:
                        newemail=None
                else:
                    newemail=newemail
                if newemail:
                    if ("zz91.com" in newemail):
                        newemail=None
                
                if (ctel=="" or ctel==" "):
                    ctel=None
                list={'id':l,'com_email':newemail,'membertype':membertype,'com_id':com_id,'cname':cname,'comkeywords':comkeywords,'province':province,'cproductslist':cproductslist,'ccontactp':ccontactp,'ctel':ctel,'cmobile':cmobile,'cadd':cadd}
                listall.append(list)
    listcount=len(listall)
    return render_to_response('huangye2016.html',locals())
#2016黄页导出
def huangye2017(request):
    port = 9315
    cl = SphinxClient()
    cl.SetServer ('192.168.2.21', port)
    cl.SetMatchMode ( SPH_MATCH_BOOLEAN )
    cl.SetLimits (0,10000,10000)
    membertype1=request.GET.get("membertype1")
    if membertype1:
        cl.SetFilter('membertype',[int(membertype1)])
    comkeywords1=request.GET.get("comkeywords1")
    if comkeywords1:
        cl.SetFilter('comkeywords',[int(comkeywords1)])
    searchstr=""
    cproductslist1=request.GET.get("cproductslist1")
    slselect=request.GET.get("slselect")
    jsselect=request.GET.get("jsselect")
    otselect=request.GET.get("otselect")
    slselect1=1
    jsselect1=1
    otselect1=1
    if (slselect==None or slselect==""):
        slselect=""
        slselect1=None
        
    if (jsselect==None or jsselect==""):
        jsselect=""
        jsselect1=None
    if (otselect1==None or otselect==""):
        otselect=""
        otselect1=None
        
    cadd1=request.GET.get("cadd1")
    if (cadd1==None):
        cadd1=""
    ss2=""
    if (comkeywords1=="1" and jsselect!="0" and jsselect!=""):
        searchstr=searchstr+"@(js1,js2) "+jsselect+""
        ss2=1
    if (comkeywords1=="2" and slselect!="0" and slselect!=""):
        searchstr=searchstr+"@(sl1,sl2) "+slselect+""
        ss2=1
    if (comkeywords1=="3" and otselect!="0" and otselect!=""):
        searchstr=searchstr+"@(qt1,qt2) "+otselect+""
        ss2=1
                
    if (cadd1!=""):
        searchstr=searchstr+"&@(province) "+cadd1+""

    s = hashlib.md5(searchstr)
    s = s.hexdigest()[8:-8]
    
    """
    if (searchstr!="" and cadd1!="" and ss2==1):
        res = cl.Query (searchstr,"huangyeinfo_2017")
        if res:
            if res.has_key('matches'):
                list=res['matches']
                
                for match in list:
                    id=match['id']
                    
                    sqlc="select id from temp_huangye2017 where searchtext='"+s+"' and com_id="+str(id)+""
                    cursor.execute(sqlc)
                    result=cursor.fetchone()
                    if not result:
                        sqlp="insert into temp_huangye2017(searchtext,com_id,scount) values('"+s+"',"+str(id)+",1)"
                        cursor.execute(sqlp)
                        conn.commit()
    #return render_to_response('huangye2017.html',locals())
    """
    
                
    listall=[]
    sqlh="select com_id from v_huangye2017 where searchtext='"+s+"'"
    cursor.execute(sqlh)
    results=cursor.fetchall()
    if results:
        for l in results:
            sql="select id,com_email,membertype,com_id,cname,comkeywords,province,cproductslist,ccontactp,ctel,cmobile,cadd,newemail,weixin from huangye_list where id=%s"
            mycursor.execute(sql,l[0])
            result=mycursor.fetchone()
            if result:
                id=result[0]
                com_email=result[1]
                membertype=result[2]
                com_id=result[3]
                cname=result[4]
                comkeywords=result[5]
                province=result[6]
                cproductslist=result[7]
                #cproductslist=cproductslist.replace("，",",")
                #slist=""
                #for s in range(len(cproductslist)):
                #    slist=slist+cproductslist[s]
                #    mm=s % 10
                #    if (str(mm)=="1"):
                #        slist=slist+"<br>"
                #cproductslist=slist
                ccontactp=result[8]
                ctel=result[9]
                if ctel:
                    ctel=ctel
                else:
                    ctel=""
                cmobile=result[10]
                cadd=result[11]
                newemail=result[12]
                weixin=result[13]
                if weixin:
                    weixin=weixin.replace(" ","")
                if not weixin:
                    weixin=None
                #newemail=str(newemail)+str(com_email)
                if newemail:
                    newemail=newemail.strip()
                   
                if (newemail==None or newemail==""):
                    if (com_email):
                        newemail=com_email.strip()
                    else:
                        newemail=None
                else:
                    newemail=newemail
                if newemail:
                    if ("zz91.com" in newemail):
                        newemail=None
                
                if (ctel=="" or ctel==" "):
                    ctel=None
                list={'id':id,'com_email':newemail,'membertype':membertype,'com_id':com_id,'cname':cname,'comkeywords':comkeywords,'province':province,'cproductslist':cproductslist,'ccontactp':ccontactp,'ctel':ctel,'cmobile':cmobile,'cadd':cadd,'weixin':weixin}
                listall.append(list)
    listcount=len(listall)
    return render_to_response('huangye2017.html',locals())
#公海客户
def gonghaicomlist(request):
    dotype = request.GET.get("dotype")
    if not dotype:
        dotype="allall"
    localIP="192.168.2.2"#翻页
    nowdint=int(time.strftime('%H%M',time.localtime(time.time())))
    showtxt="所有客户"
    """
    if (dotype=="gonghai_all"):
        showtxt="全部公海"
        aa=1
        if nowdint>=1200 and nowdint<=1330:
            aa=0
        else:
            if nowdint>1730:
                aa=0
            if nowdint<830:
                aa=0
            if aa!=0:
                return render_to_response('nothing.html',locals())
    """
    #翻页
    page=request.GET.get("page")
    if (page==None):
        page=1
    funpage = zz91page()
    limitNum=funpage.limitNum(15)
    nowpage=funpage.nowpage(int(page))
    frompageCount=funpage.frompageCount()
    after_range_num = funpage.after_range_num(2)
    before_range_num = funpage.before_range_num(9)
    #-----------------
    #搜索条件
    query=""
    personid = request.GET.get("personid")
    sear=""
    if personid:
        sear+="&personid="+personid
    com_name1=request.GET.get("com_name")
    com_contactperson1=request.GET.get("com_contactperson")
    if (com_name1 and com_name1!='' and com_name1!='None'):
        query+='@com_name '+com_name1
        sear+='&com_name='+com_name1
    else:
        com_name1=''
    if (com_contactperson1 and com_contactperson1!='' and com_contactperson1!='None'):
        query+='@com_contactperson '+com_contactperson1
        sear+='&com_contactperson='+com_contactperson1
    else:
        com_contactperson1=''
    com_tel1=request.GET.get("com_tel")
    if (com_tel1 and com_tel1!=''):
        query+='@(com_tel,com_mobile) '+com_tel1
        sear+='&com_tel='+com_tel1
    com_email1=request.GET.get("com_email")
    if (com_email1 and com_email1!=''):
        query+='@com_email '+com_email1
        sear+='&com_email='+com_email1
    com_add1=request.GET.get("com_add")
    if (com_add1 and com_add1!=''):
        query+='@com_add '+com_add1
        sear+='&com_add='+com_add1
    zyyw1=request.GET.get("zyyw")
    if (zyyw1 and zyyw1!=''):
        query+='@com_productslist_en '+zyyw1
        sear+='&zyyw='+zyyw1
    
    keywords1=request.GET.get("keywords")
    if (keywords1 and keywords1!=''):
        query+='@(com_productslist_en,com_name) '+keywords1
        sear+='&keywords='+keywords1
    
    selectdiqu1=request.GET.get("selectdiqu")
    
    if (selectdiqu1 and selectdiqu1!=''):
        query+='@(com_province,com_add) '+selectdiqu1
        sear+='&selectdiqu='+selectdiqu1
    
    
    province1=request.GET.get("province")
    province2=request.GET.get("province1")
    city2=request.GET.get("city1")
    if (province1 and province1!=''):
        query+='@(com_province,com_add) '+province1
        sear+='&province='+province1
    city1=request.GET.get("city")
    if (city1 and city1!='' and city1!='请选择...'):
        query+='@(com_province,com_add) '+city1
        sear+='&city='+city1
        
        
    
    port = 9315
    cl = SphinxClient()
    
    cl.SetServer ('192.168.2.21', port)
    cl.SetMatchMode ( SPH_MATCH_BOOLEAN )
    #搜索条件
    com_rank1=request.GET.get("com_rank")
    if (com_rank1 and com_rank1!=""):
        frank=float(com_rank1)-0.01
        trank=float(com_rank1)
        cl.SetFilterFloatRange('com_rank',frank,trank)
        sear+='&com_rank='+com_rank1
    
    fromdate1=request.GET.get("fromdate")
    todate1=request.GET.get("todate")
    if (fromdate1):
        fromlasttelf=datediff('1970-1-1',fromdate1[0:10])
    else:
        fromlasttelf=0
    
    if (todate1):
        fromlasttelt=datediff('1970-1-1',todate1[0:10])
    else:
        fromlasttelt=datediff('1970-1-1',getToday().strftime( '%-Y-%-m-%-d'))
    if (fromdate1):
        cl.SetFilterRange('teldate1',int(fromlasttelf),int(fromlasttelt))
        sear+='&fromdate='+fromdate1
        sear+='&todate='+todate1
    
    Lfromdate=request.GET.get("Lfromdate")
    Ltodate=request.GET.get("Ltodate")
    if (Lfromdate):
        Lfromdatef=datediff('1970-1-1',Lfromdate[0:10])
    if (Ltodate):
        Lfromdatet=datediff('1970-1-1',Ltodate[0:10])
        sear+='&Ltodate='+Ltodate
    else:
        Lfromdatet=datediff('1970-1-1',getToday().strftime( '%-Y-%-m-%-d'))
    if (Lfromdate):
        cl.SetFilterRange('lastlogintime1',int(Lfromdatef),int(Lfromdatet))
        sear+='&Lfromdate='+Lfromdate
    Regfromdate=request.GET.get("Regfromdate")
    Regtodate=request.GET.get("Regtodate")
    if (Regfromdate):
        Regfromdate1=datediff('1970-1-1',Regfromdate[0:10])
    else:
        Regfromdate1=0
    if (Regtodate):
        Regtodate1=datediff('1970-1-1',Regtodate[0:10])
    else:
        Regtodate1=datediff('1970-1-1',getToday().strftime( '%-Y-%-m-%-d'))
    if (Regfromdate):
        cl.SetFilterRange('com_regtime1',int(Regfromdate1),int(Regtodate1))
        sear+='&Regfromdate='+Regfromdate
        sear+='&Regtodate='+Regtodate
    contactcount=request.GET.get("contactcount")
    if (contactcount!=None and contactcount!=""):
        arrcontactcount=contactcount.split("-")
        if (len(arrcontactcount)>=2):
            cl.SetFilterRange('telcount',int(arrcontactcount[0]),int(arrcontactcount[1]))
            sear+='&contactcount='+str(contactcount)
            
    nocontactcount=request.GET.get("nocontactcount")
    if (nocontactcount!=None and nocontactcount!=""):
        arrnocontactcount=nocontactcount.split("-")
        if (len(arrnocontactcount)>=2):
            cl.SetFilterRange('telnocount',int(arrnocontactcount[0]),int(arrnocontactcount[1]))
            sear+='&nocontactcount='+str(nocontactcount)
    logincounts=request.GET.get("logincounts")
    if (logincounts!=None and logincounts!=""):
        arrlogincount=logincounts.split("-")
        if (len(arrlogincount)>=2):
            cl.SetFilterRange('logincount',int(arrlogincount[0]),int(arrlogincount[1]))
            sear+='&logincounts='+str(logincounts)
    contactpersoncount=request.GET.get("contactpersoncount")
    if (contactpersoncount!=None and contactpersoncount!=""):
        arrcontactpersoncount=contactpersoncount.split("-")
        if (len(arrcontactpersoncount)>=2):
            cl.SetFilterRange('telpersoncount',int(arrcontactpersoncount[0]),int(arrcontactpersoncount[1]))
            sear+='&contactpersoncount='+str(contactpersoncount)
    zstflag=request.GET.get("zstflag")
    if (dotype=="gonghai_all"):
        cl.SetFilter('personid',[0])
        sear+='&dotype=gonghai_all'
        if (zstflag=="1"):
            cl.SetFilterRange('zst',1,90000000)
            zstflagselect="checked"
            sear+='&zstflag='+str(zstflag)
        else:
            cl.SetFilter('zst',[0])
            cl.SetFilter('vap',[0])
    else:
        if (zstflag=="1"):
            cl.SetFilterRange('zst',1,90000000)
            zstflagselect="checked"
            sear+='&zstflag='+str(zstflag)
        
    
    addcompany=request.GET.get("addcompany")
    addcompanyselect=""
    if (addcompany=='1'):
        cl.SetFilterRange('addcompany',1,10000000)
        sear+='&addcompany='+str(addcompany)
        addcompanyselect="checked"
    #----------------
    comporder=request.GET.get("comporder")
    ascdesc=request.GET.get("ascdesc")
    if (comporder and comporder!=''):
        orderbystr=comporder+" "+ascdesc
        cl.SetSortMode( SPH_SORT_EXTENDED,""+str(orderbystr)+"" )
        sear+='&comporder='+comporder+'&ascdesc='+ascdesc
        
    else:
        cl.SetSortMode( SPH_SORT_EXTENDED,"com_regtime2 desc" )
    
    
    
    cl.SetLimits (frompageCount,limitNum,100000)
    res = cl.Query (query,'crminfo')
    listcount=0
    if res:
        listcount=res['total_found']
        listcount_all=listcount
        if res.has_key('matches'):

            tagslist=res['matches']
            listall=[]
            for match in tagslist:
                sql="select com_id,com_email,com_name,com_tel,com_province,com_mobile,vipflag,com_rank,com_regtime,lastlogintime,teldate,contacttype,com_ctr_id,com_zip,com_contactperson,com_desi,fdate,logincount,personid,vpersonid,vip_datefrom,vip_dateto FROM v_salescomp where com_id="+str(match['id'])
                cursor.execute(sql)
                arrkname=cursor.fetchone()
                if (arrkname):
                    com_id=arrkname[0]
                    com_email=changeuft8(arrkname[1])
                    com_name=changeuft8(arrkname[2])
                    com_tel=changeuft8(arrkname[3])
                    com_province=changeuft8(arrkname[4])
                    com_mobile=changeuft8(arrkname[5])
                    com_rank=arrkname[7]
                    if (com_rank==None):
                        com_rank=''
                    com_regtime=changedate(arrkname[8])
                    
                    datediffvalue=datediff(com_regtime[0:10],getToday().strftime( '%-Y-%-m-%-d'))
                    trcolor=""
                    if (datediffvalue==1):
                        trcolor="bgcolor='#CCFFCC'"
                    
                    lastlogintime=changedate(arrkname[9])
                    if (lastlogintime!=''):
                        datediffvalue_l=datediff(lastlogintime[0:10],getToday().strftime( '%-Y-%-m-%-d'))
                        if (datediffvalue_l<=3):
                            trcolor="bgcolor='#FFDFD0'"
                    teldate=changedate(arrkname[10])
                    com_contactperson=changeuft8(arrkname[14])
                    com_desi=changeuft8(arrkname[15])
                    fdate=changedate(arrkname[16])
                    logincount=arrkname[17]
                    attrs=match['attrs']
                    lastlogintime2=attrs['lastlogintime2']
                    vap=attrs['vap']
                    zst=attrs['zst']
                    if (zst==0):
                        zst=None
                    realnametxt=''
                    havevip=gethavevip(com_id)
                    personid=arrkname[18]
                    vpersonid=arrkname[19]
                    vip_date=changedate(arrkname[20])
                    vip_dateto=changedate(arrkname[21])
                    if (str(personid)!='' and personid!=None):
                        trcolor="bgcolor='#cccccc'"
                    if arrkname[18]:
                        sql="select realname from users where id="+str(arrkname[18])
                        cursor.execute(sql)
                        realname=cursor.fetchone()
                        if realname:
                            realnametxt=changeuft8(realname[0])
                    realnametxtvap=""
                    if vpersonid:
                        sql="select realname from users where id="+str(vpersonid)
                        cursor.execute(sql)
                        realname=cursor.fetchone()
                        if realname:
                            realnametxtvap=changeuft8(realname[0])
                    list={'vap':vap,'trcolor':trcolor,'lastlogintime2':lastlogintime2,'com_id':com_id,'com_rank':com_rank,'com_name':com_name,'com_province':com_province,'com_email':com_email,'com_tel':com_tel,'com_mobile':com_mobile,'com_regtime':com_regtime,'lastlogintime':lastlogintime,'logincount':logincount,'teldate':teldate,'fdate':fdate,'com_contactperson':com_contactperson,'com_desi':com_desi,'realname':realnametxt,'realnametxtvap':realnametxtvap,'zst':zst,'havevip':havevip,'vip_date':vip_date,'vip_dateto':vip_dateto}
                    listall.append(list)
        if (int(listcount)>100000):
            listcount=100000
    listcount = funpage.listcount(listcount)
    page_listcount=funpage.page_listcount()-1
    firstpage = funpage.firstpage()
    lastpage = funpage.lastpage()
    page_range  = funpage.page_range()
    nextpage = funpage.nextpage()
    prvpage = funpage.prvpage()
    personid = request.GET.get("personid")
    if personid and str(personid)!="None":
        sqluser="select ywadminid from users where id=%s"
        cursor.execute(sqluser,(personid))
        result=cursor.fetchone()
        if result:
            ywadminid=result[0]
            if ywadminid:
                fpuserlist=getuserlist(ywadminid)
    
    return render_to_response('complist.html',locals())
    closeconn()
#获得用户权限
def getuserlist(userid):
    sql="select code,meno from cate_adminuser where code in("+userid+")"
    cursor.execute(sql)
    result=cursor.fetchall()
    listall=[]
    if result:
        for list in result:
            l={'code':list[0],'meno':changeuft8(list[1]),'userlist':''}
            sqlu="select realname,id from users where closeflag=1 and userid=%s"
            cursor.execute(sqlu,(list[0]))
            resultu=cursor.fetchall()
            lu=[]
            if resultu:
                for li in resultu:
                    ll={'realname':changeuft8(li[0]),'personid':li[1]}
                    lu.append(ll)
            l['userlist']=lu
            listall.append(l)
    return listall
def gethavevip(com_id):
    sql="select id from crm_category_info where property_value='10040004' and property_id=%s"
    cursor.execute(sql,(com_id))
    arrkname=cursor.fetchone()
    if arrkname:
        return 1
    else:
        return None
    
def searchcomlist(request):
    port = 9315
    cl = SphinxClient()
    lastlogintime = request.GET.get("lastlogintime")
    lastlogintime1=lastlogintime
    lastteldate = request.GET.get("lastteldate")
    shihai = request.GET.get("shihai")
    zst = request.GET.get("zst")
    if (lastlogintime):
        formatnowdate=datediff('1970-1-1',lastlogintime)
    else:
        formatnowdate=datediff('1970-1-1','2012-4-24')
    formatnextday=datediff('1970-1-1','2012-4-24')
    if (shihai):
        cl.SetFilterRange('personid',0,1000)
    cl.SetServer ('192.168.2.21', port)
    if (lastlogintime):
        cl.SetFilterRange('lastlogintime1',int(formatnowdate),int(formatnextday))
    
    if (lastteldate):
        fromlasttelf=datediff('1970-1-1',lastteldate)
    else:
        fromlasttelf=datediff('1970-1-1','2012-4-24')
    fromlasttelt=datediff('1970-1-1','2012-4-24')
    if (lastteldate):
        cl.SetFilterRange('teldate1',int(fromlasttelf),int(fromlasttelt))
    cl.SetSortMode( SPH_SORT_EXTENDED,"teldate1 desc" )
    cl.SetMatchMode ( SPH_MATCH_BOOLEAN )
    cl.SetLimits (0,2000,20000)
    res = cl.Query ('','crminfo')
    if res:
        if res.has_key('matches'):
            tagslist=res['matches']
            listall=[]
            i=1
            for match in tagslist:
                sql="select com_tel,com_mobile,lastlogintime,teldate FROM v_salescomp where com_id="+str(match['id'])
                cursor.execute(sql)
                arrkname=cursor.fetchone()
                if (arrkname):
                    
                    if arrkname[0]:
                        com_tel=arrkname[0].decode('GB18030','ignore').encode('utf-8')
                    else:
                        com_tel=''
                    if (arrkname[1]):
                        com_mobile=arrkname[1].decode('GB18030','ignore').encode('utf-8')
                    else:
                        com_mobile=''
                    if arrkname[2]:
                        lastlogintime=arrkname[2].strftime( '%-Y-%-m-%-d %-H:%-M:%-S')
                    else:
                        lastlogintime=''
                    if arrkname[3]:
                        teldate=arrkname[3].strftime( '%-Y-%-m-%-d %-H:%-M:%-S')
                    else:
                        teldate=''
                    list={'i':i,'com_tel':com_tel,'com_mobile':com_mobile,'lastlogintime':lastlogintime,'teldate':teldate}
                    i+=1
                    listall.append(list)
            listcount=res['total_found']
    return render_to_response('searchout.html',locals())
    closeconn()
#获得销售名字
def getusername(request):
    com_id = request.GET.get("com_id")
    sql="select b.realname from crm_assign as a left join users as b on a.personid=b.id where a.com_id="+str(com_id)
    cursor.execute(sql)
    arrkname=cursor.fetchone()
    if (arrkname):
        uname2=arrkname[0].decode('GB18030','ignore').encode('utf-8')
    else:
        uname2=None
    sql="select b.realname from crm_assignvap as a left join users as b on a.personid=b.id where a.com_id="+str(com_id)
    cursor.execute(sql)
    arrkname=cursor.fetchone()
    if (arrkname):
        uname1=arrkname[0].decode('GB18030','ignore').encode('utf-8')
    else:
        uname1=None
    namev=""
    if uname1:
        namev+="vap:"+uname1
    if uname2:
        namev+="icd:"+uname2
    
    list={'name':namev}
    return HttpResponse(simplejson.dumps(list, ensure_ascii=False))
    #return render_to_response('getusername.html',locals())
def complist(request):
    port = 9315
    cl = SphinxClient()
    com_tel1 = request.GET.get("com_tel")
    dotype = request.GET.get("dotype")
    com_mobile1 = request.GET.get("com_mobile")
    com_name1 = request.GET.get("com_name")
    cl.SetServer ('192.168.2.21', port)
    cl.SetMatchMode ( SPH_MATCH_BOOLEAN )
    #cl.SetSortMode( SPH_SORT_EXTENDED,"com_id desc" )
    cl.SetLimits (0,20)
    res = cl.Query ('@com_tel '+com_tel1+' | @com_mobile '+com_mobile1,'crminfo')
    if res:
        if res.has_key('matches'):
            tagslist=res['matches']
            listall=[]
            for match in tagslist:
                sql="select com_id,com_email,com_name,com_tel,com_province,com_mobile,vipflag,com_rank,com_regtime,lastlogintime,teldate,contacttype,com_ctr_id,com_zip,com_contactperson,com_desi,fdate,logincount,personid FROM v_salescomp where com_id="+str(match['id'])
                cursor.execute(sql)
                arrkname=cursor.fetchone()
                if (arrkname):
                    com_id=arrkname[0]
                    com_name=arrkname[2].decode('GB18030','ignore').encode('utf-8')
                    com_email=arrkname[1].decode('GB18030','ignore').encode('utf-8')
                    if arrkname[3]:
                        com_tel=arrkname[3].decode('GB18030','ignore').encode('utf-8')
                    else:
                        com_tel=''
                    if (arrkname[5]):
                        com_mobile=arrkname[5].decode('GB18030','ignore').encode('utf-8')
                    else:
                        com_mobile=''
                    if arrkname[9]:
                        lastlogintime=arrkname[9].strftime( '%-Y-%-m-%-d %-H:%-M:%-S')
                    else:
                        lastlogintime=''
                    if arrkname[10]:
                        teldate=arrkname[10].strftime( '%-Y-%-m-%-d %-H:%-M:%-S')
                    else:
                        teldate=''
                    if arrkname[16]:
                        fdate=arrkname[16].strftime( '%-Y-%-m-%-d %-H:%-M:%-S')
                    else:
                        fdate=''
                    realnametxt=''
                    if arrkname[18]:
                        sql="select realname from users where id="+str(arrkname[18])
                        cursor.execute(sql)
                        realname=cursor.fetchone()
                        if realname:
                            realnametxt=realname[0].decode('GB18030','ignore').encode('utf-8')
                    list={'com_id':com_id,'com_name':com_name,'com_email':com_email,'com_tel':com_tel,'com_mobile':com_mobile,'lastlogintime':lastlogintime,'teldate':teldate,'fdate':fdate,'realname':realnametxt}
                    listall.append(list)
    return render_to_response('default.html',locals())
    closeconn()
def zhuandan(request):
    port = 9315
    cl = SphinxClient()
    com_tel1 = request.GET.get("com_tel")
    dotype = request.GET.get("dotype")
    com_mobile1 = request.GET.get("com_mobile")
    com_name1 = request.GET.get("com_name")
    requesttype = request.GET.get("requesttype")
    cl.SetServer ('192.168.2.21', port)
    cl.SetMatchMode ( SPH_MATCH_BOOLEAN )
    #cl.SetSortMode( SPH_SORT_EXTENDED,"com_id desc" )
    cl.SetLimits (0,100)
    if (requesttype=='a'):
        res = cl.Query ('@(com_tel,com_mobile) '+com_tel1+' | @(com_tel,com_mobile) '+com_mobile1,'crminfo')
    else:
        res = cl.Query ('@com_name '+com_name1,'crminfo')
    if res:
        if res.has_key('matches'):
            tagslist=res['matches']
            listall=[]
            for match in tagslist:
                com_id=str(match['id'])
                list={'com_id':com_id}
                listall.append(list)
        listcount=res['total_found']
    return render_to_response('zhuandan.html',locals())
    closeconn()
def getwebconnect(request):
    webstatusip=socket.gethostbyname("adminasto.zz91.com")
    
    if (webstatusip=="120.26.66.166" or webstatusip=="221.12.127.195"):
        listcount=1
    else:
        listcount=0
    return render_to_response('count.html',locals())
def getCompcountlist(request):
    return HttpResponse("1")
    webstatusip=socket.gethostbyname("adminasto.zz91.com")
    if (webstatusip=="120.26.66.166" or webstatusip=="221.12.127.195"):
        port = 9315
        cl = SphinxClient()
        com_id = int(request.GET.get("com_id"))
        cl.SetServer ('120.26.66.166', port)
        cl.SetMatchMode ( SPH_MATCH_BOOLEAN )
        #cl.SetLimits (0,100000,100000)
        #cl.SetFilter('pdt_kind',[1])
        cl.SetFilter('company_id',[com_id],False)
        res = cl.Query ('','offersearch_new_vip,offersearch_new')
        if res:
            offercount=res['total_found']
        
        sendcount=''
        c2 = SphinxClient()
        c2.SetServer ('120.26.66.166', port)
        c2.SetMatchMode ( SPH_MATCH_BOOLEAN )
        c2.SetFilter('scomid',[com_id],False)
        res = c2.Query ('','question')
        if res:
            sendcount=res['total_found']
        
        resivecount=''
        c3 = SphinxClient()
        c3.SetServer ('120.26.66.166', port)
        c3.SetMatchMode ( SPH_MATCH_BOOLEAN )
        c3.SetFilter('rcomid',[com_id],False)
        res = c3.Query ('','question')
        if res:
            resivecount=res['total_found']
        listcount=str(offercount)+'|'+str(sendcount)+'|'+str(resivecount)
    return render_to_response('count.html',locals())
    closeconn()
def Sphinxstaus(request):
    #port = 9315
    #cl = SphinxClient()
    #cl.SetServer ('211.155.229.180', port)
    #listcount=cl.Status
    listcount=socket.gethostbyname("china.zz91.com")
    """
    cl.SetFilter('company_id',[824985],False)
    res = cl.Query ('','offersearch_new_vip,offersearch_new')
    if res:
        listcount=res['total_found']
    """
    return render_to_response('count.html',locals())
    closeconn()
#聊天版论坛信息
def bbslist(request):
    personid=request.GET.get("personid")
    conn = MySQLdb.connect(host='192.168.2.21', user='root', passwd='zj88friend',db='phpwind',charset='utf8')   
    cursor = conn.cursor()
    sql="select a.authorid,a.subject,FROM_UNIXTIME(a.lastpost,'%Y-%m-%d %H:%i:%S'),a.lastposter,a.replies,b.honor,a.tid from pw_threads as a left join pw_members as b on a.authorid=b.uid  order by a.lastpost desc limit 0,10 "
    cursor.execute(sql)
    arrbbslist=cursor.fetchall()
    listall=[]
    for list in arrbbslist:
        uid=list[0]
        subject=list[1]
        lastpost=list[2]
        lastposter=list[3]
        
        replies=list[4]
        authname=list[5]
        replyname=authname[0:10]
        tid=list[6]
        if (lastposter!="" and lastposter!=None):
            sqlu="select uid,honor from pw_members where username='"+lastposter+"'"
            cursor.execute(sqlu)
            arrulist=cursor.fetchone()
            if arrulist:
                replyname=arrulist[1][0:10]
                uid=arrulist[0]
        
        list={'tid':tid,'uid':uid,'subject':subject,'lastpost':lastpost,'authname':authname,'replyname':replyname,'replies':replies}
        listall.append(list)
    return render_to_response('bbslist.html',locals())
    closeconn()
def closeconn():
    cursor.close()
