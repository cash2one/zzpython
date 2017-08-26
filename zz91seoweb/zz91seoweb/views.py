#-*- coding:utf-8 -*-
import MySQLdb   
import settings
import codecs,requests
from django.utils.http import urlquote
from django.shortcuts import render_to_response
from django.template.loader import get_template
from django.template import Context
from django.http import HttpResponse,HttpResponseRedirect,HttpResponseNotFound
from django.views.decorators.csrf import csrf_protect
from django.core.paginator import Paginator,InvalidPage,EmptyPage,PageNotAnInteger
import time,json
import sys
import datetime,md5,hashlib
from datetime import timedelta, date 
import os
import urllib
import re
from views_mobile import mobiledefault
from operator import itemgetter, attrgetter

from django.core.cache import cache
import random
import shutil
try:
	import cPickle as pickle
except ImportError:
	import pickle
from math import ceil
#验证码
try:
	import cStringIO as StringIO
except ImportError:
	import StringIO
	
from sphinxapi import *
from zz91page import *

reload(sys)
sys.setdefaultencoding('UTF-8')
nowpath=os.path.dirname(__file__)


execfile(nowpath+"/conn.py")
execfile(nowpath+"/function.py")


def htmlinclude(company_id):
	sqlp="select staticurl,htmurl from esite_templates where company_id=%s"
	cursor.execute(sqlp,[company_id])
	resault=cursor.fetchone()
	if resault:
		csscode=str(resault[0])
		htmlcode=resault[1]
	else:
		sqlp="select css,html from seo_templates where company_id=%s"
		cursor.execute(sqlp,[company_id])
		resault=cursor.fetchone()
		if resault:
			csscode=str(resault[0])
			if not csscode:
				csscode=""
			htmlcode=str(resault[1])
			if not htmlcode:
				htmlcode=""
		else:
			csscode=""
			htmlcode=""
	imgurl="/"+csscode+"/"
	topinclude="html/"+htmlcode+"/top.html"
	buttominclude="html/"+htmlcode+"/bottom.html"
	leftinclude="html/"+htmlcode+"/leftcontact.html"
	return {'buttominclude':buttominclude,'topinclude':topinclude,'leftinclude':leftinclude,'html':htmlcode,'css':csscode,'img':imgurl}
#企业秀模板
def getcompanyqiyexiu(company_id):
	sqlp="select css,html from crm_service_qiyexiu where company_id=%s"
	cursor.execute(sqlp,[company_id])
	resault=cursor.fetchone()
	if resault:
		csscode=str(resault[0])
		if not csscode:
			csscode=""
		htmlcode=str(resault[1])
		if not htmlcode:
			htmlcode=""
	else:
		csscode=""
		htmlcode=""
	imgurl="/"+csscode+"/"
	return {'html':htmlcode,'css':csscode,'img':imgurl}
def getlmselected(nid):
	list={'n1':'','n2':'','n3':'','n4':'','n5':'','n6':'','n7':'','n8':'','n9':'','n10':''}
	list[nid]='class=current'
	return list

def netindex(request):
    categorylist1=getindexcategorylist('1000',1)
    categorylist2=getindexcategorylist('1001',1)
    categorylist3=getindexcategorylist('1002',1)
    categorylist4=getindexcategorylist('1003',1)
    categorylist5=getindexcategorylist('1004',1)
    categorylist6=getindexcategorylist('1005',1)
    categorylist7=getindexcategorylist('1006',1)
    categorylist8=getindexcategorylist('1007',0)
    categorylist9=getindexcategorylist('1008',1)
    categorylist10=getindexcategorylist('1009',1)
    
    priceInfo_feisl=getindexpricelist(kname='塑料'.decode('utf-8'),limitcount=8,titlelen=50)
    priceInfo_feijs=getindexpricelist(kname='金属'.decode('utf-8'),limitcount=8,titlelen=50)
    priceInfo_feizhi=getindexpricelist(kname='纸'.decode('utf-8'),limitcount=6,titlelen=50)
    priceInfo_feixj=getindexpricelist(kname='橡胶'.decode('utf-8'),limitcount=6,titlelen=50)
    priceInfo_feidz=getindexpricelist(kname='电子'.decode('utf-8'),limitcount=6,titlelen=50)
    
    priceInfo_jixshebei=getindexpricelist(kname='机械 设备'.decode('utf-8'),limitcount=6,titlelen=50)
    offerlist_boli=getindexofferlist(kname='玻璃'.decode('utf-8'),limitcount=3)
    offerlist_fangzhi=getindexofferlist(kname='纺织'.decode('utf-8'),limitcount=6)
    offerlist_qit=getindexofferlist(kname='玻璃 木料'.decode('utf-8'),limitcount=6)
    offerlist_fuwu=getindexofferlist(kname='报关 通关 清关'.decode('utf-8'),limitcount=3)
    return render_to_response('zz91.net/index.html',locals())
# 企业秀
def mobileqiyexiu(request,company_id):
	#企业秀服务是否开通
	sql="select id from crm_company_service where company_id=%s and crm_service_code='10001009' and apply_status=1 and DATEDIFF(CURDATE(),`gmt_end`)<=0"
	cursor.execute(sql,[company_id])
	mlist = cursor.fetchone()
	if not mlist:
		return render_to_response('html/404.html',locals())
	
	htmlincludes=getcompanyqiyexiu(company_id)
	if (htmlincludes['html']==""):
		return render_to_response('html/404.html',locals())
	html=htmlincludes['html']
	
	list=getcompanydetail(company_id)
	companyimglist=getcompanyimgall(0,5,company_id)
	productslist=getcompanyprolist(frompageCount=0,limitNum=5,company_id=company_id)
	
	return render_to_response('html/'+html+'/index.html',locals())
def default(request):
	domainlist=gethostname(request)
	subname=domainlist['subname']
	domain=domainlist['domain']
	company_id=getdomaincompanyid(subname)
	if (domain=="m.zz91.com"):
		return mobiledefault(request,company_id)
	host = request.META['HTTP_HOST']
	if (host=="www.zz91.net" or host=="zz91.net"):
		return netindex(request)
	if (host=="h5.zz91.com"):
		return mobileqiyexiu(request,company_id)
	htmlincludes=htmlinclude(company_id)
	if (htmlincludes['html']==""):
		return render_to_response('html/404.html',locals())
	html=htmlincludes['html']
	csscode=htmlincludes['css']
	lmselected=getlmselected("n1")
	
	integral=getcompanyintegral(company_id)
	serieslist=getproductsseries(company_id)
	list=getcompanydetail(company_id)
	companyimg=getcompanyimgone(company_id)
	if not companyimg:
		companyimg={'filename':'nopic','filepath':'http://b.zz91.com/comm/images/nopic.png'}
	if list:
		if not list['midpic']:
			list['midpic']='http://b.zz91.com/esite/banner/m1.jpg'
	friendlist=getfriend_link(company_id)
	
	prolist=getcompanyproductslist(None,0,8,company_id,None,None,None)
	newslist=getcompanynewslist(0,5,company_id)
	return render_to_response('html/'+html+'/default.html',locals())
def about(request):
	subname=gethostname(request)['subname']
	company_id=getdomaincompanyid(subname)
	htmlincludes=htmlinclude(company_id)
	if (htmlincludes['html']==""):
		return render_to_response('html/404.html',locals())
		
	html=htmlincludes['html']
	csscode=htmlincludes['css']
	lmselected=getlmselected("n2")
	
	
	integral=getcompanyintegral(company_id)
	serieslist=getproductsseries(company_id)
	list=getcompanydetail(company_id)
	return render_to_response('html/'+html+'/about.html',locals())

def products(request,seriesid,page):
	subname=gethostname(request)['subname']
	company_id=getdomaincompanyid(subname)
	htmlincludes=htmlinclude(company_id)
	if (htmlincludes['html']==""):
		return render_to_response('html/404.html',locals())
	html=htmlincludes['html']
	csscode=htmlincludes['css']
	lmselected=getlmselected("n3")
	
	integral=getcompanyintegral(company_id)
	list=getcompanydetail(company_id)
	serieslist=getproductsseries(company_id)
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
	
	listall=getcompanyproductslist(None,frompageCount,limitNum,company_id,None,toseriesid,None)
	
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
	
	return render_to_response('html/'+html+'/products.html',locals())
def productsdetail(request,id):
	subname=gethostname(request)['subname']
	company_id=getdomaincompanyid(subname)
	htmlincludes=htmlinclude(company_id)
	if (htmlincludes['html']==""):
		return render_to_response('html/404.html',locals())
	html=htmlincludes['html']
	csscode=htmlincludes['css']
	lmselected=getlmselected("n3")
	
	integral=getcompanyintegral(company_id)
	serieslist=getproductsseries(company_id)
	list=getcompanydetail(company_id)
	
	productsdetail=getproductdetail(id)
	otherprolist=getcompanyproductslist(None,0,12,company_id,None,None,None)
	
	return render_to_response('html/'+html+'/pdetail.html',locals())
def news(request,page):
	subname=gethostname(request)['subname']
	company_id=getdomaincompanyid(subname)
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
	
	subname=gethostname(request)['subname']
	company_id=getdomaincompanyid(subname)
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
def contact(request):
	subname=gethostname(request)['subname']
	company_id=getdomaincompanyid(subname)
	htmlincludes=htmlinclude(company_id)
	if (htmlincludes['html']==""):
		return render_to_response('html/404.html',locals())
	html=htmlincludes['html']
	csscode=htmlincludes['css']
	lmselected=getlmselected("n7")
	
	integral=getcompanyintegral(company_id)
	serieslist=getproductsseries(company_id)
	list=getcompanydetail(company_id)
	return render_to_response('html/'+html+'/contact.html',locals())
	
def certificate(request):
	subname=gethostname(request)['subname']
	company_id=getdomaincompanyid(subname)
	htmlincludes=htmlinclude(company_id)
	if (htmlincludes['html']==""):
		return render_to_response('html/404.html',locals())
	html=htmlincludes['html']
	csscode=htmlincludes['css']
	lmselected=getlmselected("n5")
	
	integral=getcompanyintegral(company_id)
	serieslist=getproductsseries(company_id)
	list=getcompanydetail(company_id)
	
	certificatelist=getcertificatefile(company_id)
	
	return render_to_response('html/'+html+'/certificate.html',locals())
@csrf_protect
def leavewords(request):

	subname=gethostname(request)['subname']
	company_id=getdomaincompanyid(subname)
	htmlincludes=htmlinclude(company_id)
	if (htmlincludes['html']==""):
		return render_to_response('html/404.html',locals())
	html=htmlincludes['html']
	csscode=htmlincludes['css']
	lmselected=getlmselected("n6")
	
	integral=getcompanyintegral(company_id)
	serieslist=getproductsseries(company_id)
	list=getcompanydetail(company_id)

	
	return render_to_response('html/'+html+'/leavewords.html',locals())
@csrf_protect
def leavewords_save(request):
	subname=gethostname(request)['subname']
	company_id=getdomaincompanyid(subname)
	htmlincludes=htmlinclude(company_id)
	if (htmlincludes['html']==""):
		return render_to_response('html/404.html',locals())
	html=htmlincludes['html']
	csscode=htmlincludes['css']
	lmselected=getlmselected("n6")
	
	integral=getcompanyintegral(company_id)
	serieslist=getproductsseries(company_id)
	list=getcompanydetail(company_id)
	
	send_username="admin"
	send_company_id="0"
	re_company_id = "0"
	
	title=request.POST['title']
	content = request.POST['content']+"<br>姓名:"+request.POST['name']+"<br>电话:"+request.POST['mobile']+"<br>邮箱:"+request.POST['email']+"<br>QQ:"+request.POST['qq']
	
	be_inquired_type=1
	be_inquired_id=company_id
	inquired_type=0
	sender_account=send_username
	receiver_account=getcompanyaccount(company_id)
	send_time=datetime.datetime.now()
	gmt_created=datetime.datetime.now()
	gmt_modified=datetime.datetime.now()
	value=[title,content,be_inquired_type,be_inquired_id,inquired_type,sender_account,receiver_account,send_time,gmt_created,gmt_modified]
	sql="insert into inquiry(title,content,be_inquired_type,be_inquired_id,inquired_type,sender_account,receiver_account,send_time,gmt_created,gmt_modified) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
	cursor.execute(sql,value);
	conn.commit()
	sucflag="1"
	return render_to_response('html/'+html+'/leavewords.html',locals()) 
def robots(request):
	subname=gethostname(request)['subname']
	company_id=getdomaincompanyid(subname)
	htmlincludes=htmlinclude(company_id)
	if (htmlincludes['html']==""):
		return render_to_response('html/404.html',locals())
	html=htmlincludes['html']
	return render_to_response('html/'+html+'/robots.html',locals())

def viewer_404(request):
	t = get_template('404.html')
	html = t.render(Context())
	return HttpResponseNotFound(html)
def viewer_500(request):
	t = get_template('404.html')
	html = t.render(Context())
	return HttpResponseNotFound(html)

def page404(request):
	
	return render_to_response('page404.html', locals())