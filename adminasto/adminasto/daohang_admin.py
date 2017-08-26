#-*- coding:utf-8 -*-
import MySQLdb   
import settings
import codecs
from django.utils.http import urlquote
from django.shortcuts import render_to_response
from django.http import HttpResponse,HttpResponseRedirect
from django import http
from adminasto.settings import MEDIA_ROOT
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
reload(sys)
sys.setdefaultencoding('UTF-8')

nowpath=os.path.dirname(__file__)
execfile(nowpath+"/conn.py")
def getsubsid(sid):
    sql="select sid from daohang where id="+sid+""
    cursor.execute(sql)
    slist=cursor.fetchone()
    if (slist!=None):
        return slist[0]
def daohangadd(request):
    listall=[]
    sid = request.GET.get("sid")
    type = request.GET.get("type")
    if type=="None":
        type=""
    if type==None:
        type=""
    
    label_s = request.GET.get("label_s")
    if label_s==None:
        label_s=""
    pingyin_s = request.GET.get("pingyin_s")
    if pingyin_s==None:
        pingyin_s=""
    page = request.GET.get("page")
    if (page==None):
        page=1
    funpage = zz91page()
    limitNum=funpage.limitNum(30)
    nowpage=funpage.nowpage(int(page))
    frompageCount=funpage.frompageCount()
    after_range_num = funpage.after_range_num(2)
    before_range_num = funpage.before_range_num(9)
    searchmore="a=1"
    sqlmore=""    
    if (label_s!=None and label_s!=''):
        sqlmore+=" and label like '%"+str(label_s)+"%'"
        searchmore+="&label_s="+str(label_s)
    else:
        if (sid!=None):
            sqlmore+=" and sid="+str(sid)+""
        else:
            sid="0"
            sqlmore+=" and sid=0"
        searchmore+="&sid="+str(sid)
    searchmore+="&type="+str(type)
    searchmore+="&pingyin_s="+str(pingyin_s)
    
    sqlc="select count(0) from daohang where  id>0 "+sqlmore+""
    cursor.execute(sqlc)
    listcount=cursor.fetchone()[0]
    sql="select id,label,pingyin,templates,ord,sid,keywords,keywords1,num_str,keywords2,keywords3,type from daohang where id>0 "+sqlmore+" order by ord asc limit "+str(frompageCount)+","+str(limitNum)
    cursor.execute(sql)
    complist=cursor.fetchall()
    for a in complist:
        sqld="select count(0) from daohang where sid="+str(a[0])+""
        cursor.execute(sqld)
        dcount=cursor.fetchone()
        keywords1=str(a[7])
        keywords2=str(a[9])
        keywords3=str(a[10])
        type1=str(a[11])
        if (keywords1=='None'):
            keywords1=''
        if (keywords2=='None'):
            keywords2=''
        if (keywords3=='None'):
            keywords3=''
        list={'id':a[0],'sid':a[5],'label':a[1],'pingyin':a[2],'templates':a[3],'ord':a[4],'dcount':dcount[0],'keywords':str(a[6]),'keywords1':keywords1,'num_str':str(a[8]),'keywords2':keywords2,'keywords3':keywords3,'type':type1}
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
    
    if (sid==None):
        sid="0"
    subid=getsubsid(sid)
    if (subid==None):
        subid=0
    sql="select id,label from daohang where sid="+str(subid)+" order by ord asc"
    cursor.execute(sql)
    listcb=[]
    complist=cursor.fetchall()
    for a in complist:
        list={'id':a[0],'label':a[1]}
        listcb.append(list)
    return render_to_response('daohang_add.html',locals())
    closeconn()
def daohangsave(request):
    localhostIP=getlocalIP()
    id=request.POST["id"]
    sid=request.POST["sid"]
    type=request.POST["type"]
    label=request.POST["label"]
    pingyin = request.POST["pingyin"]
    templates1 = request.POST["templates"]
    ord= request.POST["ord"]
    keywords= request.POST["keywords"]
    keywords1= request.POST["keywords1"]
    keywords2= request.POST["keywords2"]
    keywords3= request.POST["keywords3"]
    num_str=request.POST["num_str"]
    num_str=num_str.replace(' ','')
    value=[label,sid,pingyin,templates1,ord,keywords,keywords1,keywords2,keywords3,num_str,type]
    valueu=[label,sid,pingyin,templates1,ord,keywords,keywords1,keywords2,keywords3,num_str,type,id]
    if (id=='0'):
        sql="select id from daohang where pingyin='"+str(pingyin)+"' and pingyin<>'' and type="+str(type)+""
        cursor.execute(sql)
        newcode=cursor.fetchone()
        if (newcode != None):
            response = HttpResponse()
            response.write("<script>alert('改拼音已经存在，请重新填写');window.location='/daohangadd/'</script>")
            return response
    sql="select id from daohang where id='"+str(id)+"'"
    cursor.execute(sql)
    newcode=cursor.fetchone()
    if (newcode == None):
        sql="insert into daohang(label,sid,pingyin,templates,ord,keywords,keywords1,keywords2,keywords3,num_str,type) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        cursor.execute(sql,value);
        conn.commit()
    else:
        sql="update daohang set label=%s,sid=%s,pingyin=%s,templates=%s,ord=%s,keywords=%s,keywords1=%s,keywords2=%s,keywords3=%s,num_str=%s,type=%s where id=%s"
        cursor.execute(sql,valueu);
        conn.commit()
    response = HttpResponse()
    if (id==0):
        response.write("<script>window.location='/daohangadd/?sid="+sid+"'</script>")
    else:
        response.write(label+"保存成功")
    return response
    closeconn()
def daohangdel(request):
    id = request.GET.get("id")
    value=[id]
    sql="delete from daohang where id=%s"
    cursor.execute(sql,value);
    response = HttpResponse()
    response.write("<script>window.location='/daohangadd/'</script>")
    return response
    closeconn()
def cscomp(request):
    com_id = request.GET.get("com_id")
    cs_account=request.GET.get("cs_account")
    sql="select id from crm_cs where company_id="+str(com_id)+" and cs_account='"+str(cs_account)+"'"
    cursor.execute(sql)
    newcode=cursor.fetchone()
    if (newcode != None):
        comtext="存在"
    else:
        comtext="不存在"
    return render_to_response('cscomp.html',locals())
    closeconn()
def directupload(request):
    template= 'fileupload.html'
    if request.method == 'POST':
        if 'file' in request.FILES:
            file = request.FILES['file']
            filename = file['filename']
            fd = open('%s/%s' % (MEDIA_ROOT, filename.encode('utf-8')), 'wb')
            fd.write(file['content'])
            fd.close()
            return http.HttpResponseRedirect('../upload_success')
    return render_to_response(template, locals())

#首页模块    
def indexdatamain(request):
    delflag = request.GET.get("del")
    code = request.GET.get("code")
    id=request.GET.get("id")
    if not code:
        code=""
    procode=code[0:len(code)-4]
    if (code==None):
        code='100010191001'
    if delflag:
        sql="delete from data_index_category where id=%s"
        cursor.execute(sql,[id])
        response = HttpResponse()
        response.write("<script>window.location='/indexdatamain/?code="+procode+"'</script>")
        return response
    
    
    sql="select id,code,label from data_index_category where code like '"+code+"____'"
    cursor.execute(sql)
    datalist=cursor.fetchall()
    listall=[]
    for a in datalist:
        list={'id':a[0],'code':a[1],'label':a[2]}
        listall.append(list)
    return render_to_response('index_datamain.html',locals())
    closeconn()
    
    
def indexdata(request):
    id=request.GET.get("id")
    delflag = request.GET.get("del")
    category_code = request.GET.get("category_code")
    if delflag:
        sql="delete from data_index where id=%s"
        cursor.execute(sql,[id])
        response = HttpResponse()
        response.write("<script>window.location='/indexdata/?category_code="+category_code+"'</script>")
        return response
    sql="select id,category_code,title,link,is_checked,sort from data_index where category_code='"+category_code+"' order by sort asc"
    cursor.execute(sql)
    datalist=cursor.fetchall()
    listall=[]
    for a in datalist:
        list={'id':a[0],'category_code':a[1],'title':a[2],'link':a[3],'is_checked':a[4],'sort':a[5]}
        listall.append(list)
    return render_to_response('index_data.html',locals())
    closeconn()
    
    
def indexdataadd(request):
    code=request.POST["code"]
    sqlm="select right(code,4) from data_index_category where code like '"+code+"____' order by right(code,4) desc limit 0,1"
    cursor.execute(sqlm)
    datalist=cursor.fetchone()
    if datalist:
        maxcode=datalist[0]
        nowcode=str(code)+str(int(maxcode)+1)
    else:
        maxcode="1000"
        nowcode=str(code)+str(int(maxcode)+1)
    label=request.POST["label"]
    value=[nowcode,label]
    sql="insert into data_index_category (code,label) values(%s,%s)"
    cursor.execute(sql,value)
    conn.commit()
    
    response = HttpResponse()
    response.write("<script>window.location='/indexdatamain/?code="+code+"'</script>")
    return response
def indexdatamoreadd(request):
    category_code=request.POST["category_code"]
    title=request.POST["title"]
    linkurl1=request.POST["linkurl1"]
    sort=request.POST["sort"]
    arrtitle=title.split(' ')
    for p in arrtitle:
        title=p
        value=[category_code,title,linkurl1,sort]
        sql="insert into data_index (category_code,title,link,sort) values(%s,%s,%s,%s)"
        cursor.execute(sql,value)
        conn.commit()
    response = HttpResponse()
    response.write("<script>window.location='/indexdata/?category_code="+category_code+"'</script>")
    return response
    
#----报价类别管理

def pricecategorymain(request):
    delflag = request.GET.get("del")
    id=request.GET.get("id")
    parent_id=request.GET.get("parent_id")
    if (parent_id==None):
        parent_id=0
    if delflag:
        sql="delete from price_category where id=%s"
        cursor.execute(sql,[id])
        response = HttpResponse()
        response.write("<script>window.location='/pricecategorymain/?parent_id="+str(parent_id)+"'</script>")
        return response
    
    
    sql="select id,parent_id,name,showflag from price_category where parent_id=%s"
    cursor.execute(sql,[parent_id])
    datalist=cursor.fetchall()
    listall=[]
    for a in datalist:
        list={'id':a[0],'parent_id':a[1],'name':a[2],'showflag':a[3]}
        listall.append(list)
    return render_to_response('price/pricecategorymain.html',locals())
def pricecategorysave(request):
    name=request.POST["pname"]
    id=request.POST["id"]
    showflag=request.POST["showflag"]
    sql="update price_category set name=%s,showflag=%s where id=%s"
    cursor.execute(sql,[name,showflag,id])
    conn.commit()
    return HttpResponse("suc")
    