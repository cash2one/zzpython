#-*- coding:utf-8 -*-
import MySQLdb   
import settings
import codecs,requests
from django.utils.http import urlquote
from django.shortcuts import render_to_response
from django.http import HttpResponse,HttpResponseRedirect
from django.views.decorators.csrf import csrf_protect
from django.core.paginator import Paginator,InvalidPage,EmptyPage,PageNotAnInteger
import time,json
import sys
import datetime,md5,hashlib
from datetime import timedelta, date 
import os
import urllib
import re

from django.core.cache import cache
import random
import shutil
try:
	import cPickle as pickle
except ImportError:
	import pickle
from math import ceil
#验证码
import memcache
try:
	import cStringIO as StringIO
except ImportError:
	import StringIO
	
from sphinxapi import *
from zz91page import *
#memcache
mc = memcache.Client(['cache.zz91server.com:11211'],debug=0)

reload(sys)
sys.setdefaultencoding('UTF-8')
nowpath=os.path.dirname(__file__)
execfile(nowpath+"/conn.py")
execfile(nowpath+"/function.py")

def htmlinclude(company_id):
	sql="select mobile_templates from crm_company_service where company_id=%s and crm_service_code='10001007' and apply_status=1 and DATEDIFF(CURDATE(),`gmt_end`)<=0"
	cursor.execute(sql,[company_id])
	mlist = cursor.fetchone()
	if mlist:
		mobile_templates=mlist[0]
		if (mobile_templates==None):
			mobile_templates="01"
		closeflag=0
	else:
		mobile_templates="01"
		closeflag=1
	csscode="/mobile/"+mobile_templates+"/"
	imgurl="/mobile/"+mobile_templates+"/"
	htmlcode="mobile/"+mobile_templates+""
	topinclude="html/"+htmlcode+"/top.html"
	buttominclude="html/"+htmlcode+"/bottom.html"
	leftinclude="html/"+htmlcode+"/leftcontact.html"
	#if closeflag==1:
		#htmlcode=""

	return {'buttominclude':buttominclude,'mobile_templates':mobile_templates,'topinclude':topinclude,'leftinclude':leftinclude,'html':htmlcode,'css':csscode,'img':imgurl}

def getlmselected(nid):
	list={'n1':'','n2':'','n3':'','n4':'','n5':'','n6':'','n7':'','n8':'','n9':'','n10':''}
	list[nid]='class=current'
	return list
def mobiledefault(request,company_id):
	htmlincludes=htmlinclude(company_id)
	if (htmlincludes['html']=="" or company_id==0):
		return render_to_response('html/404.html',locals())
	html=htmlincludes['html']
	csscode=htmlincludes['css']
	lmselected=getlmselected("n1")
	mobile_templates=htmlincludes['mobile_templates']
	integral=getcompanyintegral(company_id)
	#serieslist=getproductsseries(company_id)
	list=getcompanydetail(company_id)
	#companyimglist=getcompanyimgall(0,5,company_id)
	companyimg=getcompanyimg(company_id,1)
	#friendlist=getfriend_link(company_id)
	prolist=getcompanyproductslist(None,0,4,company_id,None,None,None)
	prolist1=getcompanyproductslist(None,4,4,company_id,None,None,None)
	#newslist=getcompanynewslist(0,5,company_id)
	return render_to_response('html/'+html+'/index.html',locals())

def mabout(request):
	domainlist=gethostname(request)
	subname=domainlist['subname']
	domain=domainlist['domain']
	company_id=getdomaincompanyid(subname)
	return about(request,company_id)
def about(request,company_id):
	htmlincludes=htmlinclude(company_id)
	if (htmlincludes['html']==""):
		return render_to_response('html/404.html',locals())
		
	html=htmlincludes['html']
	csscode=htmlincludes['css']
	lmselected=getlmselected("n2")
	mobile_templates=htmlincludes['mobile_templates']
	if (mobile_templates=='02' or mobile_templates=='03'):
		flag=None
	else:
		flag=1
	companyimg=getcompanyimg(company_id,flag)
	
	integral=getcompanyintegral(company_id)
	#serieslist=getproductsseries(company_id)
	list=getcompanydetail(company_id)
	return render_to_response('html/'+html+'/company.html',locals())

def mproductsmain(request):
	domainlist=gethostname(request)
	subname=domainlist['subname']
	domain=domainlist['domain']
	company_id=getdomaincompanyid(subname)
	return productsmain(request,company_id)
def productsmain(request,company_id):
	return products(request,company_id,0,1)


def products(request,company_id,seriesid,page):
	htmlincludes=htmlinclude(company_id)
	if (htmlincludes['html']==""):
		return render_to_response('html/404.html',locals())
	html=htmlincludes['html']
	csscode=htmlincludes['css']
	lmselected=getlmselected("n3")
	keywords=request.GET.get('keywords')
	if keywords==None:
		keywords=""
	integral=getcompanyintegral(company_id)
	list=getcompanydetail(company_id)
	#serieslist=getproductsseries(company_id)
	if (str(seriesid)=='0'):
		toseriesid=None
	else:
		toseriesid=seriesid
	
	if (page==None):
		page=1
	funpage = zz91page()
	limitNum=funpage.limitNum(10)
	nowpage=funpage.nowpage(int(page))
	frompageCount=funpage.frompageCount()
	after_range_num = funpage.after_range_num(5)
	before_range_num = funpage.before_range_num(9)
	
	listall=getcompanyproductslist(keywords,frompageCount,limitNum,company_id,None,toseriesid,keywords)
	
	prolist=listall['list']
	prolistcount=listall['count']
	listcount=prolistcount
	if (int(listcount)>1000000):
		listcount=1000000-1
	listcount = funpage.listcount(listcount)
	page_listcount=funpage.page_listcount()
	firstpage = funpage.firstpage()
	lastpage = funpage.lastpage()
	page_range  = funpage.page_range()
	nextpage = funpage.nextpage()
	prvpage = funpage.prvpage()
	
	return render_to_response('html/'+html+'/buy.html',locals())

def productslist(request,company_id,page):
	list=getcompanydetail(company_id)
	pdt_type=request.GET.get('pdt_type')
	if pdt_type=='1':
		gongying=1
	company_id=int(company_id)
	htmlincludes=htmlinclude(company_id)
	if (htmlincludes['html']==""):
		return render_to_response('html/404.html',locals())
	html=htmlincludes['html']
	csscode=htmlincludes['css']
	lmselected=getlmselected("n3")
	listall=getcompanyproductslist(None,0,5,company_id,pdt_type,None,None)
	prolist=listall['list']
	prolistcount=int(listall['count']/5)
	return render_to_response('html/'+html+'/buy.html',locals())
#下拉翻页 
def productsmore(request,company_id,page):
	htmlincludes=htmlinclude(company_id)
	html=htmlincludes['html']
	listall=getcompanyproductslist(None,int(page)*5,5,company_id,None,None,1)
	prolist=listall['list']
	prolistcount=listall['count']
	return render_to_response('html/'+html+'/productsmore.html',locals())
#公司简介
def company_profile(request,company_id):
	integral=getcompanyintegral(company_id)
	htmlincludes=htmlinclude(company_id)
	companyimg=getcompanyimg(company_id,1)
	html=htmlincludes['html']
	list=getcompanydetail(company_id)
	return render_to_response('html/'+html+'/company.html',locals())
#诚信档案
def credit(request,company_id):
	integral=getcompanyintegral(company_id)
	check_status=getcheck_status(company_id)
	if check_status==1:
		checks=1
	certificatefile=len(getcertificatefile(company_id))*2
	certificatefile2=getcertificatefile2(company_id)
	htmlincludes=htmlinclude(company_id)
	html=htmlincludes['html']
	list=getcompanydetail(company_id)
	zst_year=list['zst_year']
	if zst_year:
		zst_year_grade=zst_year*10
	return render_to_response('html/'+html+'/credit.html',locals())
def mcontact(request):
	domainlist=gethostname(request)
	subname=domainlist['subname']
	domain=domainlist['domain']
	company_id=getdomaincompanyid(subname)
	return contact(request,company_id)
#联系方式
def contact(request,company_id):
	htmlincludes=htmlinclude(company_id)
	if (htmlincludes['html']==""):
		return render_to_response('html/404.html',locals())
	html=htmlincludes['html']
	csscode=htmlincludes['css']
	lmselected=getlmselected("n4")
	
	integral=getcompanyintegral(company_id)
	#serieslist=getproductsseries(company_id)
	list=getcompanydetail(company_id)
	return render_to_response('html/'+html+'/contact.html',locals())

def productsdetail(request,id):
	company_id=getproductscompanyid(id)
	htmlincludes=htmlinclude(company_id)
	if (htmlincludes['html']==""):
		return render_to_response('html/404.html',locals())
	html=htmlincludes['html']
	csscode=htmlincludes['css']
	lmselected=getlmselected("n3")
	
	integral=getcompanyintegral(company_id)
	#serieslist=getproductsseries(company_id)
	list=getcompanydetail(company_id)
	
	productsdetail=getproductdetail(id)
	#otherprolist=getcompanyproductslist(None,0,12,company_id,None,None,None)
	
	return render_to_response('html/'+html+'/productsdetail.html',locals())

def newsmain(request,company_id):
	return news(request,company_id,1)
def news(request,company_id,page):
	
	htmlincludes=htmlinclude(company_id)
	if (htmlincludes['html']==""):
		return render_to_response('html/404.html',locals())
	html=htmlincludes['html']
	csscode=htmlincludes['css']
	lmselected=getlmselected("n4")
	
	if (page==None):
		page=1
	funpage = zz91page()
	limitNum=funpage.limitNum(10)
	nowpage=funpage.nowpage(int(page))
	frompageCount=funpage.frompageCount()
	after_range_num = funpage.after_range_num(2)
	before_range_num = funpage.before_range_num(9)
	
	
	listall=getcompanynewslist(frompageCount,limitNum,company_id)
	
	newslist=listall['list']
	newslistcount=listall['count']
	listcount=newslistcount
	if (int(listcount)>1000000):
		listcount=1000000-1
	listcount = funpage.listcount(listcount)
	page_listcount=funpage.page_listcount()
	firstpage = funpage.firstpage()
	lastpage = funpage.lastpage()
	page_range  = funpage.page_range()
	nextpage = funpage.nextpage()
	prvpage = funpage.prvpage()
	
	integral=getcompanyintegral(company_id)
	list=getcompanydetail(company_id)
	return render_to_response('html/'+html+'/news.html',locals())
	
def newsdetail(request,id):
	
	company_id=getnewscompanyid(id)
	htmlincludes=htmlinclude(company_id)
	if (htmlincludes['html']==""):
		return render_to_response('html/404.html',locals())
	html=htmlincludes['html']
	csscode=htmlincludes['css']
	
	lmselected=getlmselected("n4")
	newsdetail=getcompanynewsdetails(company_id,id)
	integral=getcompanyintegral(company_id)
	list=getcompanydetail(company_id)
	nextnews=getcompanynewsnext(company_id,id)
	otherlist=getcompanynewslist(0,10,company_id)
	
	return render_to_response('html/'+html+'/news_detail.html',locals())


