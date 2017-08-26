#-*- coding:utf-8 -*- 
from getnews import get_img_url,getsimilarity
import random,time,jieba,re,os,sys,datetime
from simptools import time1,time2,time3,filter_tags,newspath,imgpath,getsimplecontent,str_to_int,date_to_int
from zz91db_dacong import dacongdb
dcdb=dacongdb()
reload(sys)
sys.setdefaultencoding('utf8')

def iszhuaqu(a_url):
    sql="select id from zhuaqu_url where url=%s"
    resultlist=dcdb.fetchonedb(sql,[a_url])
    if resultlist:
        return 1
    else:
        sql="insert into zhuaqu_url(url) values(%s)"
        dcdb.updatetodb(sql,[a_url])
        return None
def get_new(title):
    sql='select id from dede_archives where title=%s'
    resultlist=dcdb.fetchonedb(sql,[title])
    if resultlist:
        return resultlist
    
def savedbdacong(typeid,typeid2,main_url,url_a,title,content,keywords="",re_keywords="",listconf="",domain="",re_time=""):
    sortrankl=random.randint(0,3600*3)
    nkeywords=re_keywords
    if not nkeywords:
        nkeywords=keywords
    if not nkeywords:
        nkeywords=keywords
    pubdate=time1-sortrankl
    pubdate=int(pubdate)
    if re_time:
        pubdate=str_to_int(re_time)
    sortrank=random.randint(000000000,999999999)
    if title:
        sql='insert into dede_arctiny(typeid,typeid2,mid,senddate,sortrank) values(%s,%s,1,%s,%s)'
        dcdb.updatetodb(sql,[typeid,typeid2,time1,sortrank])
        sql='select id from dede_arctiny where typeid=%s and typeid2=%s and sortrank=%s'
        resultlist=dcdb.fetchonedb(sql,[typeid,typeid2,sortrank])
        if resultlist:
            id=resultlist[0]
            description=''
            if content:
                description=filter_tags(content)
            
            if description and len(description)>30:
                source=listconf['source']
                gmt_created=datetime.datetime.now()
                pubdate=date_to_int(gmt_created)
                senddate=pubdate
                cstyle=listconf.get("cstyle")
                if not cstyle:
                    cstyle=1
                sql='insert into dede_archives(id,ismake,title,typeid,typeid2,pubdate,senddate,sortrank,voteid,keywords,description,source,arcrank) values(%s,-1,%s,%s,%s,%s,%s,%s,0,%s,%s,%s,%s)'
                dcdb.updatetodb(sql,[id,title,typeid,typeid2,pubdate,senddate,pubdate,nkeywords,description,source,-1])
                simplecontent=getsimplecontent(content,main_url)
                sql='insert into dede_addonarticle(aid,typeid,body,cstyle) values(%s,%s,%s,%s)'
                dcdb.updatetodb(sql,[id,typeid,simplecontent,cstyle])
                img_url=get_img_url(content)#获得新闻图片
                if img_url:
                    img_urlone=None
                    for p in img_url:
                        if domain in p:
                           img_urlone=p
                           break
                    if listconf.has_key("weixin"):
                        if len(img_url)>1:
                            img_urlone=img_url[1]
                        if listconf.has_key("selectpic"):
                            selectpic=listconf['selectpic']
                            img_urlone=img_url[int(selectpic)]
                    #保存所有图片地址
                    if img_url:
                        for p in img_url:
                            picurl=p
                            sql="select aid from dede_uploads where url=%s"
                            result=dcdb.fetchonedb(sql,picurl)
                            if not result:
                                sql="insert into dede_uploads(arcid,url,uptime) values(%s,%s,%s)"
                                dcdb.updatetodb(sql,[id,picurl,pubdate])
                    if img_urlone:
                        sql="update dede_archives set flag='p',ismake=-1,litpic=%s where id=%s"
                        dcdb.updatetodb(sql,[img_urlone,id])
                    
                sql="update zhuaqu_url set aid=%s where url=%s"
                dcdb.updatetodb(sql,[id,url_a])
                return '抓取成功'
