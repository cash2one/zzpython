import os,urllib,httplib,json,time,sys,random,shutil,codecs,datetime,md5,hashlib,requests
import json
import MySQLdb
from datetime import timedelta, date 
try:
    import cPickle as pickle
except ImportError:
    import pickle
from math import ceil
#验证码
import memcache,qrcode,six
import Image,ImageDraw,ImageFont,ImageFilter
try:
    import cStringIO as StringIO
except ImportError:
    import StringIO
from sphinxapi import *
reload(sys)
sys.setdefaultencoding('UTF-8')
nowpath=os.getcwd()
execfile(nowpath+"/commfunction.py")
execfile(nowpath+"/function.py")
cache = memcache.Client([memcacheconfig],debug=0)
def getuserlist():
    # and DATEDIFF(CURDATE(),gmt_created)<=50
    sql="select distinct weixinid from weixin_count where left(weixinid,4)='okX-'"
    cursor.execute(sql)
    alist = cursor.fetchall()
    lall=[]
    for list in alist:
        l={"weixinid":list[0]}
        lall.append(l)
    return lall
def getmessagelist(touser):
    listalla=getnewslist(keywords="",frompageCount=0,limitNum=5,allnum=5)
    listall=listalla['list']
    mlist=[]
    newstopimg=get_newsimgsone()
    mlist.append(newstopimg)
    for list in listall:
        alist={"title":list['title'],"url":list['mobileweburl'],"picurl":"http://img0.zz91.com/zz91/weixin/images/more.jpg"}
        #get_newsimgsone()
        mlist.append(alist)
    mlist=json.dumps(mlist, ensure_ascii=False)
    list='''
    {
        "touser":"'''+touser+'''",
        "msgtype":"news",
        "news":{
            "articles": 
    '''
    list=list+str(mlist)
    list=list+'''
        }
    }
    '''
    return list
#params="{\"touser\":\"okX-XjuUbYgdwBAY9_L6gE1nX9vg\",\"msgtype\":\"text\",\"text\":{\"content\":\""+"欢迎您关注ZZ91再生网"+"\"}}"   
def send_text_message():
    ACCESS_TOKEN=get_access_token()
    
    userlist=getuserlist()
    for list in userlist:
        #touser="okX-XjuUbYgdwBAY9_L6gE1nX9vg"
        #okX-Xjs1ONPsOH3Ew3m56UtyMNo0
        touser=list["weixinid"]
        sqld="select id from weixin_sendlog where weixinid=%s and TIMESTAMPDIFF(MINUTE,gmt_created,now())<180"
        cursor.execute(sqld,[touser])
        alist = cursor.fetchone()
        if alist:
            print "have sended!"
        else:
            params=getmessagelist(touser)
            #print params
            headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain"}
            httpClient = httplib.HTTPConnection("api.weixin.qq.com", 80, timeout=30)
            httpClient.request("POST", "/cgi-bin/message/custom/send?access_token="+ACCESS_TOKEN, params, headers)
            response = httpClient.getresponse()
            #print response.status
            #print response.reason
            msglist=response.read()
            #msglist={"errcode":0,"errmsg":"ok"}
            #msglist=json.dumps(msglist, ensure_ascii=False)
            print msglist
            gmt_created=datetime.datetime.now()
            sqla="insert into weixin_sendlog(weixinid,gmt_created) values(%s,%s)"
            cursor.execute(sqla,[touser,gmt_created])
            conn.commit()
            
        
        #print response.getheaders() #获取头信息
def send_text_messageone():
    ACCESS_TOKEN=get_access_token()
    touser="okX-Xjs1ONPsOH3Ew3m56UtyMNo0"
    params=getmessagelist(touser)
    print params
    headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain"}
    httpClient = httplib.HTTPConnection("api.weixin.qq.com", 80, timeout=30)
    httpClient.request("POST", "/cgi-bin/message/custom/send?access_token="+ACCESS_TOKEN, params, headers)
    response = httpClient.getresponse()
    #print response.status
    #print response.reason
    msglist=json.dumps(response.read())
    print msglist
    #print response.getheaders() #获取头信息
send_text_message()

