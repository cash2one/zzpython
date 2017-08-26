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
import datetime
from datetime import timedelta, date 
import os
from django.core.cache import cache
import random
import shutil
try:
    import cPickle as pickle
except ImportError:
    import pickle

from math import ceil

from sphinxapi import *
from zz91page import *

nowpath=os.path.dirname(__file__)
execfile(nowpath+"/conn.py")
execfile(nowpath+"/commfunction.py")
#加密
def getjiami(strword):
    return strword.encode("gbk").encode("hex")
def getjiemi(strword):
    return strword.decode("hex").decode('GB18030','ignore')
#类别列表
def getcategorylist(pid,showflag):
    sql="select cid,cat_name from bz_category where pid="+str(pid)+" order by listorder asc"
    cursor.execute(sql)
    listall_cate=[]
    catelist=cursor.fetchall()
    for a in catelist:
        if (showflag==1):
            sql1="select cid,cat_name from bz_category where pid="+str(a[0])+" order by listorder asc"
            cursor.execute(sql1)
            listall_cate1=[]
            catelist1=cursor.fetchall()
            for b in catelist1:
                list1={'cid':b[0],'cat_name':b[1]}
                listall_cate1.append(list1)
        else:
            listall_cate1=None
        list={'cid':a[0],'cat_name':a[1],'catelist':listall_cate1}
        listall_cate.append(list)
    return listall_cate
#获得类别名称
def getcategoryname(cat_id):
    if (cat_id):
        sql="select cat_name,pid from bz_category where cid="+str(cat_id)+""
        cursor.execute(sql)
        cateone=cursor.fetchone()
        return cateone
#导航
def getnavlist(cat_id):
    nav1=getcategoryname(cat_id)
    if (nav1[1]!=0):
        nav2=getcategoryname(nav1[1])
        return "<a href='/list-"+str(nav1[1])+"/'>" + nav2[0]+"</a> > <a href='/list-"+str(cat_id)+"/'>" + nav1[0] +"</a>"
    else:
        return "<a href='/list-"+str(cat_id)+"/'>" + nav1[0] + "</a>"
#最新帮助
def gethelptoplist(cat_id="",limitnum="",commend=""):
    sqls=""
    if (cat_id!="" and cat_id!=None):
        sqls=sqls+" and cat_id="+str(cat_id)+""
    if (commend!="" and commend!=None):
        sqls=sqls+" and commend="+str(commend)+""
    sql="select aid,subject from bz_article where aid>0 "+sqls+" limit 0,"+str(limitnum)+""
    cursor.execute(sql)
    listall=[]
    helplist=cursor.fetchall()
    for a in helplist:
        list={'aid':a[0],'subject':a[1]}
        listall.append(list)
    return listall
#帮助列表
def gethelplist(cat_id="",subcat_id="",page="",ord="",keywords=""):
    funpage = zz91page()
    if (page==""):
        page=1
    if (cat_id==None or cat_id==""):
        cat_id=0
    if (ord==None or ord==""):
        ord='aid'
    limitNum=funpage.limitNum(20)
    nowpage=funpage.nowpage(int(page))
    frompageCount=funpage.frompageCount()
    after_range_num = funpage.after_range_num(2)
    before_range_num = funpage.before_range_num(9)
    
    sqlsear=""
    if (subcat_id==0):
        sqlsear=sqlsear+" and b.pid="+str(cat_id)+""
    else:
        if (cat_id!=0):
            sqlsear=sqlsear+" and a.cat_id="+str(cat_id)+""
    if (keywords!=None and keywords!=""):
        sqlsear=sqlsear+" and a.subject like '%"+getjiemi(keywords)+"%'"
    sql="select a.aid,a.cat_id,a.subject,a.description,a.color,a.keyword,a.posttime from bz_article as a left outer join bz_category as b on a.cat_id=b.cid where a.aid>0 "+sqlsear+" order by a."+str(ord)+" desc limit "+str(frompageCount)+","+str(int(frompageCount)+int(limitNum))+" "
    cursor.execute(sql)
    helplist=cursor.fetchall()
    
    sqlc="select count(0) from bz_article as a left outer join bz_category as b on a.cat_id=b.cid where a.aid>0 "+sqlsear+""
    cursor.execute(sqlc)
    helplistcount=cursor.fetchone()[0]
    listcount=0
    listall=[]
    if helplist:
        for a in helplist:
            list={'aid':a[0],'cat_id':a[1],'subject':a[2],'description':a[3],'color':a[4],'keyword':a[5],'posttime':a[6]}
            listall.append(list)
    listcount = funpage.listcount(helplistcount)
    page_listcount=funpage.page_listcount()    
    firstpage = funpage.firstpage()
    lastpage = funpage.lastpage()
    page_range  = funpage.page_range()
    nextpage = funpage.nextpage()
    prvpage = funpage.prvpage()
    
    pagelist={'firstpage':firstpage,'lastpage':lastpage,'page_range':page_range,'nextpage':nextpage,'prvpage':prvpage}
    return {'listall':listall,'pagelist':pagelist}
#
#首页
def default(request):
    #jj=getjiemi('e4b88de99488e992a2e6898be5b7a5e4ba95e5ad97e79b98')
    #jj='e4b88de99488e992a2e6898be5b7a5e4ba95e5ad97e79b98'.decode("hex")
    #jj=getjiami('广州实木美容床生产商')
    #jj='不锈钢'.encode("hex")
    indexcategory=getcategorylist(0,1)
    cjwtlist=gethelptoplist(limitnum=18)
    closeconn()
    return render_to_response('index.html',locals())
    #closeconn()
def question(request):
    indexcategory=getcategorylist(0,1)
    cjwtlist=gethelptoplist(limitnum=20,commend=1)
    return render_to_response('question.html',locals())
    closeconn()
def contact(request):
    cjwtlist=gethelptoplist(limitnum=20,commend=1)
    return render_to_response('contact.html',locals())
    closeconn()
def list(request,cat_id):
    indexcategory=getcategorylist(0,0)
    navcategory=getcategoryname(cat_id)
    navcategoryname=navcategory[0]
    navcategoryid=navcategory[1]
    navnamelist=getnavlist(cat_id)
    helplist=gethelplist(cat_id=cat_id,subcat_id=navcategoryid,page=1)
    if (str(cat_id)=='9'):
        zsttab2="class=lm_on"
        zsttab1="class=lm_off"
    else:
        zsttab2="class=lm_off"
        zsttab1="class=lm_on"
    return render_to_response('list.html',locals())
    closeconn()
def listmore(request,cat_id,page):
    indexcategory=getcategorylist(0,0)
    navcategory=getcategoryname(cat_id)
    navcategoryname=navcategory[0]
    navcategoryid=navcategory[1]
    navnamelist=getnavlist(cat_id)
    helplist=gethelplist(cat_id=cat_id,subcat_id=navcategoryid,page=page)
    if (str(cat_id)=='9'):
        zsttab2="class=lm_on"
        zsttab1="class=lm_off"
    else:
        zsttab2="class=lm_off"
        zsttab1="class=lm_on"
    return render_to_response('list.html',locals())
    closeconn()
def searchfirst(request):
    keywords=getjiami(request.GET.get("keywords"))
    return render_to_response('searchfirst.html',locals())
    closeconn()

def search(request,keywords):
    indexcategory=getcategorylist(0,0)
    
    navnamelist=getjiemi(keywords)
    navcategoryname=navnamelist
    helplist=gethelplist(page=1,keywords=keywords)
    
    zsttab2="class=lm_off"
    zsttab1="class=lm_on"
    return render_to_response('searchlist.html',locals())
    closeconn()
def detail(request,aid):
    indexcategory=getcategorylist(0,0)
    sql="select aid,subject,content,cat_id from bz_article where aid="+str(aid)+""
    cursor.execute(sql)
    helpdetail=cursor.fetchone()
    if helpdetail:
        subject=helpdetail[1]
        details=helpdetail[2]
        details=details.replace('&lt;',"<")
        details=details.replace('&gt;',">")
        details=details.replace('&amp;',"&")
        details=details.replace('&quot;',"'")
        details=details.replace('&quot;',"'")
        
        
        #re_noscript = re.compile('<(/?)script',re.IGNORECASE)
        navnamelist=getnavlist(helpdetail[3])
        cjwtlist=gethelptoplist(cat_id=helpdetail[3],limitnum=10)
    return render_to_response('detail.html',locals())
    closeconn()
def beginner(request):
    
    return render_to_response('beginner.html',locals())
    closeconn()
    
if __name__ == '__main__' : 
    cursor=autoReconnect()
    
