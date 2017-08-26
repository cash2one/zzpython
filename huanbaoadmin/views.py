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
reload(sys)
sys.setdefaultencoding('UTF-8')

nowpath=os.path.dirname(__file__)
execfile(nowpath+"/conn.py")
def changezw(strvalue):
	if(strvalue == None):
		tempstr=""
	else:
		tempstr=str(strvalue).encode('gbk','ignore').replace("'","")
	return tempstr
def changezhongwen(strvalue):
	if(strvalue == None):
		tempstr=""
	else:
		tempstr=strvalue.decode('GB18030','ignore').encode('utf-8')
		#tempstr=strvalue.decode('GB18030').encode('utf-8')
	return tempstr
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

def default(request):
	aa=""
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
	cursor_ep.execute(sql)
	returnlist=cursor_ep.fetchall()
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
	cursor_ep.execute(sql)
	newcode=cursor_ep.fetchone()
	if (newcode == None):
		sql="insert into tomcat_manager(title,start,stop,ip,tomcat_part,server_part,warname,appname,website) values(%s,%s,%s,%s,%s,%s,%s,%s,%s)"
		cursor_ep.execute(sql,value);
	else:
		sql="update tomcat_manager set title=%s,ip=%s,tomcat_part=%s,server_part=%s,warname=%s,appname=%s,website=%s where title=%s and ip=%s"
		cursor_ep.execute(sql,valueu);
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
		cursor_ep.execute(sql,value);
	if (action=="start"):
		start=1
		value=[start,id];
		sql="update tomcat_manager set start=%s where id=%s";
		cursor_ep.execute(sql,value);
	if (action=="del"):
		value=[id];
		sql="delete from tomcat_manager where id=%s";
		cursor_ep.execute(sql,value);
	response = HttpResponse()
	response.write("<script>window.location='/tomcatmanager/?ip="+str(sip)+"'</script>")
	return response
def test(request):
	port = 9312
	cl = SphinxClient()
	cl.SetServer ( '192.168.110.2', port )
	cl.SetMatchMode ( SPH_MATCH_BOOLEAN )
	#cl.SetSortMode( SPH_SORT_EXTENDED,"refresh_time desc" )
	listall=[]
	cl.SetLimits (0,50000,50000)
	res = cl.Query ('@(ptitle,tags,details_query,category_label1,category_label2,category_label3,category_label4,area_label1,area_label2,area_label3,area_label4,area_label5,parea_name) 供应类别','supplyPreTreeDay')
	if res:
		if res.has_key('matches'):
			tagslist=res['matches']
			
			for match in tagslist:
				id=match['id']
				list={'id':id}
				listall.append(list)
	
			listcount=res['total_found']
	return render_to_response('test.html',locals())
	closeconn()
def __unicode__(self):
	return self;
