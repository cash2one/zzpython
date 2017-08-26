import MySQLdb
from django.utils import simplejson
from django.http import HttpResponse
import time,datetime
from datetime import timedelta, date 
import pymssql
conn=pymssql.connect(host=r'192.168.2.2',trusted=False,user='rcu_crm',password='fdf@$@#dfdf9780@#1.kdsfd',database='rcu_crm',charset=None)
cursor=conn.cursor()
connmy = MySQLdb.connect(host='192.168.10.3', user='root', passwd='zj88friend',db='freeiris2',charset='utf8')     
cursormy = connmy.cursor()
def formattime(value,flag):
    if value:
        if (flag==1):
            return value.strftime( '%-Y-%-m-%-d')
        if (flag==2):
            return value.strftime( '%-m-%-d %-H:%-M')
        else:
            return value.strftime( '%-Y-%-m-%-d %-H:%-M:%-S')
    else:
        return ''
def changedate(datestring):
    if (datestring=="" or datestring==None):
        return ""
    else:
        nowsdatestr=datestring.strftime( '%Y-%m-%d %X')
        if (nowsdatestr=='1900-01-01 00:00:00'):
            nowsdatestr=""
        return nowsdatestr
def getrecord(request):
    caller=request.GET.get("caller")
    sqlser=""
    if caller and caller!="":
        sqlser=sqlser+" and src='"+caller+"'"
    sql="select id,calldate,src,dst,dcontext,duration,billsec,userfield from cdr where disposition='ANSWERED' and lastapp='Dial'  "+sqlser+" order by id desc limit 0,80"
    cursormy.execute(sql)
    results = cursormy.fetchall()
    recordlist=[]
    for a in results:
        uniqueid=a[0]
        startime=str(a[1])
        caller=a[2]
        answeredtime=a[6]
        called=a[3]
        dcontext=a[4]
        type=1
        userfield=a[7]
        if (dcontext=='from-exten-sip'):
            type=1
        else:
            type=2
        filename=""
        fid=userfield
        folder=""
        if (fid!=None and fid!=""):
            sqlr="select filename,folder from voicefiles where associate='"+str(fid)+"'"
            cursormy.execute(sqlr)
            flist=cursormy.fetchone()
            if (flist):
                folder=flist[1]
                filename=flist[0]
            else:
                folder=""
                filename=''
        monitorfile="http://192.168.2.2/admin1/crmlocal/file/download.asp?FileName=http://192.168.2.27/freeiris2/cpanel/record/"+str(folder)+"/"+filename+".WAV"
        listenfile="http://192.168.2.2/admin1/crmlocal/recordService/play.asp?mdname="+filename+".WAV&ml="+str(folder)+"/"
        list={'uniqueid':uniqueid,'startime':startime,'caller':caller,'answeredtime':answeredtime,'called':called,'type':type,'downloadfile':monitorfile,'listenfile':listenfile}
        recordlist.append(list)
    return HttpResponse(simplejson.dumps(recordlist, ensure_ascii=False))
def getrecord1(request):
    caller=request.GET.get("caller")
    sqlser=""
    if caller and caller!="":
        sqlser=sqlser+" and caller='"+caller+"'"
    sql="select top 200 uniqueid,startime,caller,accountcode,answeredtime,called,type,monitorfile from record_list where id>0 "+sqlser+" order by id desc"
    cursor.execute(sql)
    results = cursor.fetchall()
    recordlist=[]
    for a in results:
        uniqueid=a[0]
        startime=str(a[1])
        caller=a[2]
        accountcode=a[3]
        answeredtime=a[4]
        called=a[5]
        type=a[6]
        folder="1"
        monitorfile="http://192.168.2.2/admin1/crmlocal/file/download.asp?FileName=http://192.168.2.27/freeiris2/cpanel/record/"+str(folder)+"/"+a[7]+".WAV"
        listenfile="http://192.168.2.2/admin1/crmlocal/recordService/play.asp?mdname="+a[7]+".WAV&ml="+str(folder)+"/"
        list={'uniqueid':uniqueid,'startime':startime,'caller':caller,'answeredtime':answeredtime,'called':called,'type':type,'downloadfile':monitorfile,'listenfile':listenfile}
        recordlist.append(list)
    return HttpResponse(simplejson.dumps(recordlist, ensure_ascii=False))