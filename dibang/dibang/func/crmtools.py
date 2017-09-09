# -*- coding:utf-8 -*-
import datetime
import time
#时间撮转化为日期
def timestamp_to_date(timestamp):
    ltime=time.localtime(timestamp)
    timeStr=time.strftime("%Y-%m-%d %H:%M:%S", ltime)
    return timeStr
#格式化字符串
def formattime(value,flag=''):
    if value:
        if (flag==1):
            return value.strftime('%Y-%m-%d')
        elif flag==3:
            return value.strftime('%Y-%m')
        #第几周
        elif flag==4:
            begind=str_to_date(value.strftime('%Y-%m')+"-1")
            beginw=begind.strftime('%W')
            #return beginw
            return int(value.strftime('%W'))-int(beginw)+1
        else:
            return value.strftime('%Y-%m-%d %H:%M:%S')
    else:
        return ''

#----所有时间转换函数
def str_to_date(stringDate):
    if not ':' in stringDate:
        stringDate=stringDate+' 00:00:00'
    return datetime.datetime.strptime(stringDate,"%Y-%m-%d %H:%M:%S").date()
def str_to_datetime(stringDate):
    if not ':' in stringDate:
        stringDate=stringDate+' 00:00:00'
    return datetime.datetime.fromtimestamp(time.mktime(time.strptime(stringDate,"%Y-%m-%d %H:%M:%S")))
def str_to_int(stringDate):
    if not ':' in stringDate:
        stringDate=stringDate+' 00:00:00'
    return int(time.mktime(time.strptime(stringDate,"%Y-%m-%d %H:%M:%S")))
def int_to_str(intDate):
    return time.strftime('%Y-%m-%d', time.localtime(intDate))
def int_to_str2(intDate):
    return time.strftime('%m-%d', time.localtime(intDate))
def int_to_strall(intDate):
    return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(intDate))
def int_to_date(intDate):
    return str_to_date(int_to_strall(intDate))
def int_to_datetime(intDate):
    return str_to_datetime(int_to_strall(intDate))
def date_to_str(dttime):
    return dttime.strftime('%Y-%m-%d')
def date_to_strall(dttime):
    return dttime.strftime('%Y-%m-%d %H:%M:%S')
def dateall_to_int(dttime):
    return str_to_int(date_to_strall(dttime))
def date_to_int(dttime):
    return str_to_int(date_to_str(dttime))
def get_str_time():
    return time.strftime('%Y-%m-%d',time.localtime(time.time()))
def get_str_timeall():
    return time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
#----获得某一天的明天
def getnextdate(stringDate,arg=''):
    datestrdate=str_to_date(stringDate)
    days=datetime.timedelta(days=1)
    rdates=datestrdate+days
    if arg==1:
        rdates=date_to_str(rdates)
    return rdates
#----获得过去几天函数
def getpastday(numb,arg=''):
    listnumb=range(1,numb+1)
    today=datetime.date.today()
    listall=[]
    for lnumb in listnumb:
        days=datetime.timedelta(days=lnumb)
        ddays=today-days
        if arg==1:
            ddays=ddays.strftime('%Y-%m-%d')
        elif arg==2:
            ddays=ddays.strftime('%m-%d')
        listall.append(ddays)
    return listall
#----第前几天
def getpastoneday(numb):
    today=datetime.date.today()
    days=datetime.timedelta(days=numb)
    nowday=today-days
    return nowday
#----获得过去相差一天时间列表字典
def getdatelist(numb):
    listnumb=range(1,numb+1)
    today=datetime.date.today()
    listall=[]
    for lnumb in listnumb[::-1]:
        days=datetime.timedelta(days=lnumb)
        gmt_begin=today-days
        gmt_end=gmt_begin+datetime.timedelta(days=1)
        list={'gmt_begin':gmt_begin,'gmt_end':gmt_end}
        listall.append(list)
    return listall
#----获得两段时间差的列表(返回时间字符串列表)
def gettimedifference(datebegin,dateend):
    if str(datebegin).isdigit()==False and type(datebegin)==str:
        datebegin=str_to_int(datebegin)
    if type(datebegin)==datetime.datetime:
        datebegin=date_to_int(datebegin)
    if str(dateend).isdigit()==False and type(dateend)==str:
        dateend=str_to_int(dateend)
    if type(dateend)==datetime.datetime:
        dateend=date_to_int(dateend)
    timelist2=[]
    timedifference=(dateend-datebegin)/(3600*24)
    datebegin2=datebegin
    timelist=range(1,timedifference+1)
    for tl in timelist:
        timelist2.append(int_to_str(datebegin2))
        datebegin2=datebegin2+3600*24
    timelist2.append(int_to_str(dateend))
    return timelist2

#时间戳转为格式化字符串
def timestamp_datetime(value,time):
    format = '%Y-%m-%d'
    value = time.localtime(value)
    dt = time.strftime(format, value)
    return dt
#----获得昨天datetime类型
def getYesterday():
    today=datetime.date.today()   
    oneday=datetime.timedelta(days=1)   
    yesterday=today-oneday    
    return yesterday
def getTomorrow():
    today=datetime.date.today()   
    oneday=datetime.timedelta(days=1)   
    yesterday=today+oneday    
    return yesterday
#----获得今天datetime类型
def getToday():
    return datetime.date.today()
#获取周几
def getweekday(timevalue):
    if timevalue:
        wk=timevalue.weekday()
        wkcn=['一','二','三','四','五','六','日']
        n=0
        for w in wkcn:
            if n==wk:
                return w
            n+=1

#----获得不带0的日期
def getsimptime(arg='%m月,%d日'):
    arglist=arg.split(',')
    arg1=arglist[0]
    arg2=arglist[1]
    timed1=time.strftime(arg1,time.localtime(time.time()))
    timed2=time.strftime(arg2,time.localtime(time.time()))
    if timed1[:1]=='0':
        timed1=timed1[1:]
    if timed2[:1]=='0':
        timed2=timed2[1:]
    simptime=timed1+timed2
    return simptime
#----秒数转化为00:00:00类型
def getnub_tostr(s):
    s1=s%60
    m=s/60
    h=m/60
    if h>0:
        m=m-(h*60)
    numb=str(h)+':'+str(m)+':'+str(s1)
    return numb
    
#搜索引擎数据更新
def updatesearchseek(keylist,values):
    #keylist  如: ['user_id','name']
    #values  如：{ 2:[123,1000000000], 4:[456,1234567890] }
    indexname="company"
    servername=searchconfig['servername']
    serverport=searchconfig['serverport']
    cl=SphinxClient()
    cl.SetServer(servername,serverport)
    res = cl.UpdateAttributes (indexname, keylist, values)
    indexname="delta_company"
    servername=searchconfig['servername']
    serverport=searchconfig['serverport']
    cl=SphinxClient()
    cl.SetServer(servername,serverport)
    res = cl.UpdateAttributes (indexname, keylist, values)
    return ''

def savekhlog(company_id,user_id,admin_user_id,details):
    gmt_created=datetime.datetime.now()
    sql="insert into kh_log (company_id,user_id,details,admin_user_id,gmt_created) values(%s,%s,%s,%s,%s)"
    db.updatetodb(sql,[company_id,user_id,details,admin_user_id,gmt_created])
    return 1
    
#更新当天数据
def updateseekoneday():
    os.system("/usr/local/coreseek/bin/indexer --config /mnt/pythoncode/zz91crm/coreseek/etc/company.conf delta_company --rotate")