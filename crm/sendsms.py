#-*- coding:utf-8 -*-
import MySQLdb
import time,sys,os,codecs
import datetime,hashlib,urllib,httplib,random,shutil
from datetime import timedelta, date
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
import pymssql
conn=pymssql.connect(host=r'192.168.2.2',trusted=False,user='rcu_crm',password='fdf@$@#dfdf9780@#1.kdsfd',database='rcu_crm',charset=None)
cursor=conn.cursor()
def postsms_yunpian(mobile,content):
    #服务地址
    host = "yunpian.com"
    #端口号
    port = 80
    #版本号
    version = "v1"
    #查账户信息的URI
    user_get_uri = "/" + version + "/user/get.json"
    #通用短信接口的URI
    sms_send_uri = "/" + version + "/sms/send.json"
    #模板短信接口的URI
    sms_tpl_send_uri = "/" + version + "/sms/tpl_send.json"
    
    sms_pull_status ="/"+version+"/sms/pull_status.json"
    
    def get_user_info(apikey):
        """
        取账户信息
        """
        conns = httplib.HTTPConnection(host, port=port)
        conns.request('GET', user_get_uri + "?apikey=" + apikey)
        response = conns.getresponse()
        response_str = response.read()
        conns.close()
        return response_str
    
    def get_pull_status(apikey):
        """
        取获取状态报告
        """
        conns = httplib.HTTPConnection(host, port=port)
        conns.request('GET', sms_pull_status + "?apikey=" + apikey)
        response = conns.getresponse()
        response_str = response.read()
        conns.close()
        return response_str
    
    def send_sms(apikey, text, mobile):
        """
        能用接口发短信
        """
        params = urllib.urlencode({'apikey': apikey, 'text': text, 'mobile':mobile})
        headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain"}
        conns = httplib.HTTPConnection(host, port=port, timeout=30)
        conns.request("POST", sms_send_uri, params, headers)
        response = conns.getresponse()
        response_str = response.read()
        conns.close()
        return response_str
    
    def tpl_send_sms(apikey, tpl_id, tpl_value, mobile):
        """
        模板接口发短信
        """
        params = urllib.urlencode({'apikey': apikey, 'tpl_id':tpl_id, 'tpl_value': tpl_value, 'mobile':mobile})
        headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain"}
        conns = httplib.HTTPConnection(host, port=port, timeout=30)
        conns.request("POST", sms_tpl_send_uri, params, headers)
        response = conns.getresponse()
        response_str = response.read()
        conn.close()
        return response_str
    #apikey ="9eff414d0e38d926fc7f36a80282acbd "   #系统
    apikey ="b0e18bf55ea73c19e3a630c4f0184e90"    #群发
    text = content
    #查账户信息
    #return get_pull_status(apikey)
    #调用通用接口发短信
    
    send_sms(apikey, text, mobile)
    
    #调用模板接口发短信
    #tpl_id = 1 #对应的模板内容为：您的验证码是#code#【#company#】
    #tpl_value = '#username#=1234&#company#=云片网'
    #print(tpl_send_sms(apikey, tpl_id, tpl_value, mobile))
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
def getwebhtml(k,check_url,baidu_url,id):
    f = urllib.urlopen(baidu_url)
    html = f.read()
    return html
def closeconn():
    cursor.close()

def savesmssend(mobile):
    if len(mobile)<=12 and len(mobile)>9:
        print mobile
        sql="select id from temp_smssend where mobile='"+str(mobile)+"'"
        cursor.execute(sql)
        arrlist=cursor.fetchone()
        if arrlist==None:
            sqld="insert into temp_smssend(mobile) values('"+str(mobile)+"')"
            cursor.execute(sqld)
        conn.commit()
        
def getmobile():
    port = 9315
    cl = SphinxClient()
    cl.SetServer ('192.168.2.21', port)
    cl.SetMatchMode ( SPH_MATCH_BOOLEAN )
    cl.SetFilter('personid',[0])
    cl.SetFilter('zst',[0])
    cl.SetFilter('vap',[0])
    Regfromdate1=datediff('1970-1-1','2011-1-1')
    Regtodate1=datediff('1970-1-1',getToday().strftime( '%-Y-%-m-%-d'))
    #Regtodate1=datediff('1970-1-1','2010-12-31')
    cl.SetFilterRange('com_regtime1',int(Regfromdate1),int(Regtodate1))
    
    #Lfromdatef=datediff('1970-1-1','2011-1-1')
    #Lfromdatet=datediff('1970-1-1',getToday().strftime( '%-Y-%-m-%-d'))
    #cl.SetFilterRange('lastlogintime1',int(Lfromdatef),int(Lfromdatet))
    cl.SetLimits (0,100000,100000)
    
    #res = cl.Query ("@(com_productslist_en) 塑料|pet|pvc|pp|pc|pe|abs|pmma|pps|PPO|pom|pa|EVA|TPU|再生颗粒&@(com_province,com_add) 山东|河南|河北|广东|福建",'crminfo')
    res = cl.Query ("@(com_province,com_add) 山东|河南|河北|广东|福建",'crminfo')
    if res:
        listcount=res['total_found']
        print listcount
        if res.has_key('matches'):
            tagslist=res['matches']
            listall=[]
            for match in tagslist:
                com_id=match['id']
                sql="select com_tel,com_mobile,com_keywords FROM temp_salescomp where com_id="+str(match['id'])
                cursor.execute(sql)
                arrkname=cursor.fetchone()
                if (arrkname):
                    com_keywords=arrkname[2]
                    if com_keywords:
                        if "2" in com_keywords:
                            if (arrkname[1]):
                                com_mobile=arrkname[1].decode('GB18030','ignore').encode('utf-8')
                            else:
                                com_mobile=''
                            sqlc="select com_id from crm_assignvap where com_id="+str(com_id)
                            cursor.execute(sqlc)
                            arrlist=cursor.fetchone()
                            if arrlist==None:
                                savesmssend(com_mobile)
                            else:
                                sqlc="select com_id from crm_assign where com_id="+str(com_id)
                                cursor.execute(sqlc)
                                arrlist=cursor.fetchone()
                                if arrlist==None:
                                    savesmssend(com_mobile)
                    """
                    else:
                        if (arrkname[1]):
                            com_mobile=arrkname[1].decode('GB18030','ignore').encode('utf-8')
                        else:
                            com_mobile=''
                        sqlc="select com_id from crm_assignvap where com_id="+str(com_id)
                        cursor.execute(sqlc)
                        arrlist=cursor.fetchone()
                        if arrlist==None:
                            savesmssend(com_mobile)
                        else:
                            sqlc="select com_id from crm_assign where com_id="+str(com_id)
                            cursor.execute(sqlc)
                            arrlist=cursor.fetchone()
                            if arrlist==None:
                                savesmssend(com_mobile)
                    """   
                    #print com_mobile
def sendsms():
    content="14届塑交会倒计时21天！ZZ91再生网邀您参与！另有少量展位面向全国招商，热线：0571-56611688"
    #postsms_yunpian("13666651091",content)
    sql="select mobile,id from temp_smssend where flag=0"
    cursor.execute(sql)
    arrlist=cursor.fetchall()
    if arrlist:
        i=0
        arrmobile=""
        mobilelist=""
        for list in arrlist:
            mobile=list[0]
            id=list[1]
            if i<=98:
                if len(mobile)==11:
                    arrmobile+=mobile+","
                mobilelist=""
            else:
                mobilelist=arrmobile
                arrmobile=mobile+","
                i=0
            if i==0:
                if mobilelist!="":
                    mobilelist=mobilelist[0:len(mobilelist)-1]
                    postsms_yunpian(mobilelist,content)
                    print mobilelist
            i=i+1
            sqlc="update temp_smssend set flag=1 where id="+str(id)
            cursor.execute(sqlc)
            conn.commit()
            print i
            #time.sleep(1)
def havesendsms():
    print postsms_yunpian("","")         
sendsms()
#havesendsms()                
