#-*- coding:utf-8 -*-
import datetime,time
"""
def formattime(value,flag=''):
    if value:
        if (flag==1):
            return value.strftime('%Y-%m-%d')
        else:
            return value.strftime('%Y-%m-%d %H:%M:%S')
    else:
        return ''
def Caltime(date1,date2):
    date1=time.strptime(date1,"%Y-%m-%d %H:%M:%S")
    date2=time.strptime(date2,"%Y-%m-%d %H:%M:%S")
    date1=datetime.datetime(date1[0],date1[1],date1[2],date1[3],date1[4],date1[5])
    date2=datetime.datetime(date2[0],date2[1],date2[2],date2[3],date2[4],date2[5])
    return date2-date1

date1='2012-08-16 01:28:33'
date2='2012-08-18 06:26:54'
now_time=formattime(datetime.datetime.now(),0)
#print now_time
#print type(date1)
a=Caltime(date1,now_time)
print a
d=a.days
print a.days
s=a.seconds
print a.seconds
if d==0:
    differ_time=s/60
    if differ_time>=60:
        differ_time=differ_time/60
        print str(differ_time)+'小时'
    else:
        print str(differ_time)+'分钟'
else:
    differ_time=d
    print str(d)+'天'
    
"""
