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
#from django.db.models import Q
#from django.db import connection
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
def getcomplist(industryCode):
	#-------------供求列表
	port = 9315
	cl = SphinxClient()
	cl.SetServer ( '192.168.110.120', port )
	cl.SetMatchMode ( SPH_MATCH_BOOLEAN )
	cl.SetSortMode( SPH_SORT_EXTENDED," gmt_start desc" )
	cl.SetLimits (0,300)
	cl.SetFilter('apply_status',[1])
	if (industryCode==10001001 or industryCode==10001000):
		cl.SetFilter('industry_code',[industryCode])
	else:
		cl.SetFilter('industry_code',[10001001],True)
		cl.SetFilter('industry_code',[10001000],True)
	nowdate=date.today()-timedelta(days=90)
	nextday=date.today()+timedelta(days=1)
	formatnowdate=time.mktime(nowdate.timetuple())
	formatnextday=time.mktime(nextday.timetuple())
	cl.SetFilterRange('gmt_start',int(formatnowdate),int(formatnextday))
	
	res = cl.Query ('','company')
	if res:
		if res.has_key('matches'):
			itemlist=res['matches']
			listall_company=[]
			for match in itemlist:
				id=match['id']
				attrs=match['attrs']
				comname=attrs['compname']
				business=attrs['pbusiness']
				area_province=attrs['parea_province']
				domain_zz91=attrs['domain_zz91']
				list={'id':id,'comname':comname,'business':business,'area_province':area_province,'domain_zz91':domain_zz91}
				listall_company.append(list)
			return listall_company
def default(request,subjectname):
	return subject(request , subjectname,"default")
def subject(request , subjectname,pagename):
	compinfo1=getcomplist(10001001);
	compinfo2=getcomplist(10001000);
	compinfo3=getcomplist(10001003);
	return render_to_response('html/'+subjectname+'/'+pagename+'.html',locals())
	closeconn()

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
	cursor_work.execute(sql)
	returnlist=cursor_work.fetchall()
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
	cursor_work.execute(sql)
	newcode=cursor_work.fetchone()
	if (newcode == None):
		sql="insert into tomcat_manager(title,start,stop,ip,tomcat_part,server_part,warname,appname,website) values(%s,%s,%s,%s,%s,%s,%s,%s,%s)"
		cursor_work.execute(sql,value);
        conn_work.commit()
	else:
		sql="update tomcat_manager set title=%s,ip=%s,tomcat_part=%s,server_part=%s,warname=%s,appname=%s,website=%s where title=%s and ip=%s"
		cursor_work.execute(sql,valueu);
        conn_work.commit()
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
		cursor_work.execute(sql,value);
        conn_work.commit()
	if (action=="start"):
		start=1
		value=[start,id];
		sql="update tomcat_manager set start=%s where id=%s";
		cursor_work.execute(sql,value);
        conn_work.commit()
	if (action=="del"):
		value=[id];
		sql="delete from tomcat_manager where id=%s";
		cursor_work.execute(sql,value);
        conn_work.commit()
	response = HttpResponse()
	response.write("<script>window.location='/tomcatmanager/?ip="+str(sip)+"'</script>")
	return response
