  # -*- coding:utf-8 -*-
# from symbol import if_stmt
import MySQLdb   
import settings
import codecs,requests
from django.utils.http import urlquote
from django.shortcuts import render_to_response
from django.template.loader import get_template
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, HttpResponsePermanentRedirect,HttpResponseNotFound
from django.views.decorators.csrf import csrf_protect
from django.core.paginator import Paginator, InvalidPage, EmptyPage, PageNotAnInteger
import time
import sys
from datetime import timedelta, date 
import os,json
import urllib
import re
from settings import spconfig
from operator import itemgetter, attrgetter

from django.core.cache import cache
import random
import shutil
try:
	import cPickle as pickle
except ImportError:
	import pickle
from math import ceil
# 验证码
try:
	import cStringIO as StringIO
except ImportError:
	import StringIO
	
from sphinxapi import *
from zz91page import *
from zz91settings import SPHINXCONFIG,limitpath


reload(sys)
sys.setdefaultencoding('UTF-8')
nowpath = os.path.dirname(__file__)
execfile(nowpath + "/conn.py")
execfile(nowpath + "/function.py")


def tongji(request):
	referrer = request.META.get('HTTP_REFERER')
	return HttpResponse(referrer)
	
#来电宝介绍首页
def index(request):
	showhead = 1
	ppcnumb = 1
	successfulCase = getSuccessfulCase(0, 1)
	successfulCase2 = getSuccessfulCase(1, 1)
	adpostionnum = getadpostionNum(621) + 1
	adlist = []
	for i in range(1, adpostionnum):
		list = getOrderadlist(621, i)
		if list:
			list['num'] = i
			adlist.append(list)
	return render_to_response('html/ppc/ppc2014/index.html', locals())
#来电宝交易区
def ppctrade(request):
	showhead = 1
	ppcnumb = 2
	steel = getppcrecom(10191000, 0, 1)
	steel2 = getppcrecom(10191000, 1, 5, '134x138')
	plastic = getppcrecom(10191001, 0, 1)
	plastic2 = getppcrecom(10191001, 1, 5, picsize='134x138')
	textiles = getppcrecom(10191002, 0, 1)
	textiles2 = getppcrecom(10191002, 1, 5, picsize='134x138')
	paper = getppcrecom(10191003, 0, 1)
	paper2 = getppcrecom(10191003, 1, 5, picsize='134x138')
	secondhand = getppcrecom(10191004, 0, 1)
	secondhand2 = getppcrecom(10191004, 1, 5, picsize='134x138')
	comprehensive = getppcrecom(10191005, 0, 1)
	comprehensive2 = getppcrecom(10191005, 1, 5, picsize='134x138')
	'''
	steel=getppccomplist('废金属',0,1,1)
	steel2=getppccomplist('废金属',1,5,1,picsize='134x138')
	plastic=getppccomplist('废塑料',0,1,1)
	plastic2=getppccomplist('废塑料',1,5,1,picsize='134x138')
	textiles=getppccomplist('废纺织品',0,1,1)
	textiles2=getppccomplist('废纺织品',1,5,1,picsize='134x138')
	paper=getppccomplist('废纸',0,1,1)
	paper2=getppccomplist('废纸',1,5,1,picsize='134x138')
	secondhand=getppccomplist('二手设备',0,1,1)
	secondhand2=getppccomplist('二手设备',1,5,1,picsize='134x138')
	comprehensive=getppccomplist('废电子电器 | 废橡胶 | 废轮胎',0,1,1)
	comprehensive2=getppccomplist('废电子电器 | 废橡胶 | 废轮胎',1,5,1,picsize='134x138')
	'''
	return render_to_response('html/ppc/ppc2014/trade.html', locals())

def ppcexperience(request):
	ppcnumb = 3
	showhead = 1
	return render_to_response('html/ppc/ppc2014/experience.html', locals())
def ppcexperience2(request):
	ppcnumb = 3
	return render_to_response('html/ppc/ppc2014/experience2.html', locals())
def ppcexperience3(request):
	ppcnumb = 3
	return render_to_response('html/ppc/ppc2014/experience3.html', locals())
def ppcexperience4(request):
	ppcnumb = 3
	return render_to_response('html/ppc/ppc2014/experience4.html', locals())
def ppcexperience5(request):
	ppcnumb = 3
	return render_to_response('html/ppc/ppc2014/experience5.html', locals())
def ppcexperience6(request):
	ppcnumb = 3
	return render_to_response('html/ppc/ppc2014/experience6.html', locals())
def ppcexperience7(request):
	ppcnumb = 3
	showhead = 1
	return render_to_response('html/ppc/ppc2014/experience7.html', locals())

#html模板
def htmlinclude(company_id):
	csscode="http://img0.zz91.com/zz91/ppc/"
	htmlcode="ldb/mo1"
	topinclude = "html/" + htmlcode + "/top.html"
	buttominclude = "html/" + htmlcode + "/bottom.html"
	leftinclude = "html/" + htmlcode + "/leftcontact.html"
	return {'buttominclude':buttominclude, 'topinclude':topinclude, 'leftinclude':leftinclude, 'html':htmlcode, 'css':csscode}
def oldhtmlinclude(company_id):
	csscode = "http://img0.zz91.com/zz91/ppc/"
	htmlcode = "ppc"
	topinclude = "html/" + htmlcode + "/top.html"
	buttominclude = "html/" + htmlcode + "/bottom.html"
	leftinclude = "html/" + htmlcode + "/leftcontact.html"
	return {'buttominclude':buttominclude, 'topinclude':topinclude, 'leftinclude':leftinclude, 'html':htmlcode, 'css':csscode}
def getlmselected(nid):
	list = {'n1':'', 'n2':'', 'n3':'', 'n4':'', 'n5':'', 'n6':'', 'n7':'', 'n8':'', 'n9':'', 'n10':''}
	list[nid] = 'class=a1'
	return list
#首页
def default(request, company_id):
	
	#----再生通301跳转
	iszst = getiszstcompany(company_id)
	if iszst:
		return ppciszst301(company_id)
	
	mobileurl="/company/shop"+str(company_id)+".html"
	htmlincludes = htmlinclude(company_id)
	if (htmlincludes['html'] == ""):
		return render_to_response('404.html', locals())
	
	html = htmlincludes['html']
	csscode = htmlincludes['css']
	lmselected = getlmselected("n1")
	
	#integral = getcompanyintegral(company_id)
	#serieslist = getproductsseries(company_id)
	list = getcompanydetail(company_id)
	if list:
		#不是会员
		if not list.get("viptype").get("vipcheck"):
			nohtml = render(request, '404.html', locals())
			return HttpResponseNotFound(nohtml)
		
		#做百度优化，但是不是会员
		if list.get("baidu") and not list.get("viptype").get("vipcheck"):
			nohtml = render(request, '404.html', locals())
			return HttpResponseNotFound(nohtml)
	# 非来电宝用户跳转到公司首页
	if not list:
		return HttpResponsePermanentRedirect('http://company.zz91.com/compinfo' + str(company_id) + '.htm')

	companypic = getcompanyimgone(company_id)
	friendlist = getfriend_link(company_id)
	
	prolist = getcompanyproductslist(frompageCount=0, limitNum=15, company_id=company_id)
	newslist = getcompanynewslist(0, 5, company_id)
	return render_to_response("html/" + str(html) + "/default.html", locals())
	#return render_to_response("html/ldb/mo1/default.html", locals())
#企业介绍
def about(request, company_id):
	#----再生通301跳转
	iszst = getiszstcompany(company_id)
	if iszst:
		return ppciszst301(company_id, 'gsjs')
	#---判断移动端设备
	agent = request.META['HTTP_USER_AGENT']
	agentflag = mobileuseragent(agent)
	if agentflag:
		return HttpResponseRedirect("http://m.zz91.com/companydetail/?company_id=" + str(company_id))
	
	htmlincludes = htmlinclude(company_id)
	if (htmlincludes['html'] == ""):
		return render_to_response('404.html', locals())
		
	html = htmlincludes['html']
	csscode = htmlincludes['css']
	lmselected = getlmselected("n2")
	
	#integral = getcompanyintegral(company_id)
	#产品系列，产品分类
	#serieslist = getproductsseries(company_id)
	#公司详情
	list = getcompanydetail(company_id)
	#认证信息
	#credit_file=getcredit_file(company_id)
	#非来电宝客户404
	if list:
		if list.get("viptype").get("vipcheck")==None or list.get("baidu"):
			html = render(request, '404.html', locals())
			return HttpResponseNotFound(html)
	# 非来电宝用户跳转到公司首页
	if not list:
		return HttpResponsePermanentRedirect('http://company.zz91.com/compinfo' + str(company_id) + '.htm')
	#公司图片
	companypiclist = getcompanyimgall(0, 5, company_id)
	#if not companypiclist:
	#	propiclist = getcompanyproductslist(frompageCount=0, limitNum=3, company_id=company_id)
	#prolist2 = getcompanyproductslist(frompageCount=0, limitNum=2, company_id=company_id)
	#compic=getcompanyimgall(0,4,company_id)
	return render_to_response('html/' + html + '/about.html', locals())
	#return render_to_response('html/ldb/mo1/about.html', locals())
def productsmain(request, company_id):
	#----再生通301跳转
	iszst = getiszstcompany(company_id)
	if iszst:
		return ppciszst301(company_id, 'zxgq')
	#---判断移动端设备
	agent = request.META['HTTP_USER_AGENT']
	agentflag = mobileuseragent(agent)
	if agentflag:
		return HttpResponseRedirect("http://m.zz91.com/companyproducts/?company_id=" + str(company_id))
	return products(request, company_id, 0, 1)
#供求列表
def products(request, company_id, seriesid, page):
	checkStatus=request.GET.get("checkStatus")#选择标签状态页（0为废料供求信息，1为原料供求信息）
	if (checkStatus=="" or checkStatus==None):
		checkStatus=0
	keywords = request.GET.get("keywords")
	htmlincludes = htmlinclude(company_id)
	if (htmlincludes['html'] == ""):
		return render_to_response('404.html', locals())
	html = htmlincludes['html']
	csscode = htmlincludes['css']
	lmselected = getlmselected("n3")
	
	#integral = getcompanyintegral(company_id)
	list = getcompanydetail(company_id)
	#非来电宝客户404
	if list:
		if list.get("viptype").get("vipcheck")==None or list.get("baidu"):
			html = render(request, '404.html', locals())
			return HttpResponseNotFound(html)
	# 非来电宝用户跳转到公司首页
	if not list:
		return HttpResponsePermanentRedirect('http://company.zz91.com/compinfo' + str(company_id) + '.htm')

	serieslist = getproductsseries(company_id)
	if seriesid:
		if seriesid == '0':
			toseriesid = ''
		else:
			toseriesid = seriesid
	else:
		toseriesid = ''
	if not page:
		page = 1
	funpage = zz91page()
	limitNum = funpage.limitNum(10)
	nowpage = funpage.nowpage(int(page))
	frompageCount = funpage.frompageCount()
	after_range_num = funpage.after_range_num(5)
	before_range_num = funpage.before_range_num(9)
	#废料翻页类
	funpage1 = zz91page()
	limitNum1 = funpage1.limitNum(10)
	nowpage1 = funpage1.nowpage(int(page))
	frompageCount1 = funpage1.frompageCount()
	#废料翻页类
	if not checkStatus:#废料料翻页
		nowpage1=funpage1.nowpage(1)
	if checkStatus:
		nowpage=funpage.nowpage(1)
	
	if (keywords):
		fcflag = 1
	else:
		fcflag = None
	
	listall = getcompanyproductslist(kname=keywords, frompageCount=frompageCount, limitNum=limitNum, company_id=company_id, seriesid=toseriesid, fcflag=fcflag)
	
	prolist = listall['list']
	prolistcount = listall['count']
	listcount = prolistcount
	if (int(listcount) > 1000000):
		listcount = 1000000 - 1
	listcount = funpage.listcount(listcount)
	page_listcount = funpage.page_listcount()
	firstpage = funpage.firstpage()
	lastpage = funpage.lastpage()
	page_range = funpage.page_range()
	nextpage = funpage.nextpage()
	prvpage = funpage.prvpage()
	
	#prolist2 = getcompanyproductslist(frompageCount=0, limitNum=2, company_id=company_id)
	"""
	#以下为原料供求
	#获得该公司的所有原料供求
	listall_yuanliao=getyuanliaolist(kname=keywords,frompageCount=frompageCount1,limitNum=limitNum1,company_id=company_id)
	yuanliaolist=listall_yuanliao['list']
	yuanliaolistcount=listall_yuanliao['count']
	listcount1 = yuanliaolistcount
	if (int(listcount1) > 1000000):
		listcount1 = 1000000 - 1
	listcount1 = funpage1.listcount(listcount1)
	page_listcount1 = funpage1.page_listcount()
	firstpage1 = funpage1.firstpage()
	lastpage1 = funpage1.lastpage()
	page_range1 = funpage1.page_range()
	nextpage1 = funpage1.nextpage()
	prvpage1 = funpage1.prvpage()
	"""
	return render_to_response('html/' + html + '/products.html', locals())
	#return render_to_response('html/ldb/mo1/products.html', locals())
#普通产品详细页
def productsdetail(request, id):
	company_id = getproductscompanyid(id)
	#----再生通301跳转
	iszst = getiszstcompany(company_id)
	if iszst:
		return ppciszst301(company_id, 'products' + str(id))
	#---判断移动端设备
	mobileurl="/detail/?id=" + str(id)
	productsdetail = getproductdetail(id)
	if productsdetail:
		mingang=getmingganword(productsdetail['title'])
		if mingang:
			return HttpResponseNotFound("<h1>FORBIDDEN</h1>")
		ppc_list = enumerate(productsdetail['piclist'])
	htmlincludes = htmlinclude(company_id)
	if (htmlincludes['html'] == "" or productsdetail == None):
		return render_to_response('404.html', locals())
	html = htmlincludes['html']
	csscode = htmlincludes['css']
	lmselected = getlmselected("n3")

	#integral = getcompanyintegral(company_id)
	#serieslist = getproductsseries(company_id)
	list = getcompanydetail(company_id)
	#非来电宝客户404
	if list:
		if list.get("viptype").get("vipcheck")==None or list.get("baidu"):
			html = render(request, '404.html', locals())
			return HttpResponseNotFound(html)
	# 非来电宝用户跳转到普通供求最终页
	if not list:
		return HttpResponsePermanentRedirect('http://trade.zz91.com/productdetails' + str(id) + '.htm')
	
	#laidb = laidianbaofunction()
	#laidbflag = laidb.getyangflag(id)
	#laidblist = laidb.getyangprice(id)
	

	
	otherprolist = getcompanyproductslist(frompageCount=0, limitNum=12, company_id=company_id)
	
	#prolist2 = getcompanyproductslist(frompageCount=0, limitNum=2, company_id=company_id)
	return render_to_response('html/' + html + '/products_detail.html', locals())
	#return render_to_response('html/ldb/mo1/products_detail.html', locals())
#原料产品详细页
def yuanliaodetail(request, id):
	company_id = getyuanliaoproductscompanyid(id)
	iszst = getiszstcompany(company_id)
	if iszst:
		return ppciszst301(company_id, 'products' + str(id))
	#---判断移动端设备
	agent = request.META['HTTP_USER_AGENT']
	agentflag = mobileuseragent(agent)
	if agentflag:
		return HttpResponseRedirect("http://m.zz91.com/detail/?id=" + str(id))
	productsdetail = getyuanliaoproductdetail(id)
	if productsdetail:
		mingang=getmingganword(productsdetail['title'])
		if mingang:
			return HttpResponseNotFound("<h1>FORBIDDEN</h1>")
	htmlincludes = htmlinclude(company_id)
	if (htmlincludes['html'] == "" or productsdetail == None):
		return render_to_response('404.html', locals())
	html = htmlincludes['html']
	csscode = htmlincludes['css']
	lmselected = getlmselected("n3")
	
	#integral = getcompanyintegral(company_id)
	serieslist = getproductsseries(company_id)
	list = getcompanydetail(company_id)
	#非来电宝客户404
	if list:
		if list.get("viptype").get("vipcheck")==None or list.get("baidu"):
			html = render(request, '404.html', locals())
			return HttpResponseNotFound(html)
	# 非来电宝用户跳转到普通供求最终页
	if not list:
		return HttpResponsePermanentRedirect('http://trade.zz91.com/productdetails' + str(id) + '.htm')
	
	laidb = laidianbaofunction()
	laidbflag = laidb.getyangflag(id)
	laidblist = laidb.getyangprice(id)
	
	otherprolist = getyuanliaoproductslist(frompageCount=0, limitNum=12, company_id=company_id)
	
	prolist2 = getcompanyproductslist(frompageCount=0, limitNum=2, company_id=company_id)
	return render_to_response('html/' + html + '/pdetail_yuanliao.html', locals())

# 公司相册
def companypic(request, company_id):
	#----再生通301跳转
	return compic(request, company_id, 1)
def compic(request, company_id, page):
	htmlincludes = htmlinclude(company_id)
	if (htmlincludes['html'] == ""):
		return render_to_response('404.html', locals())
	html = htmlincludes['html']
	csscode = htmlincludes['css']
	lmselected = getlmselected("n3")
	
	list = getcompanydetail(company_id)
	#非来电宝客户404
	if list:
		if list.get("viptype").get("vipcheck")==None or list.get("baidu"):
			html = render(request, '404.html', locals())
			return HttpResponseNotFound(html)
	# 非来电宝用户跳转到公司首页
	if not list:
		return HttpResponsePermanentRedirect('http://company.zz91.com/compinfo' + str(company_id) + '.htm')

	companypiclist = getcompanyimgall(0, 12, company_id)
	if not companypiclist:
		propiclist = getcompanyproductslist(frompageCount=0, limitNum=16, company_id=company_id)
	
	prolist2 = getcompanyproductslist(frompageCount=0, limitNum=2, company_id=company_id)
	return render_to_response('html/' + html + '/pic.html', locals())

def newsmain(request, company_id):
	#----再生通301跳转
	iszst = getiszstcompany(company_id)
	if iszst:
		return ppciszst301(company_id, 'gsjs')
	return news(request, company_id, 1)
#资讯列表
def news(request, company_id, page):
	#----再生通301跳转
	iszst = getiszstcompany(company_id)
	if iszst:
		return ppciszst301(company_id)
	htmlincludes = htmlinclude(company_id)
	if (htmlincludes['html'] == ""):
		return render_to_response('404.html', locals())
	html = htmlincludes['html']
	csscode = htmlincludes['css']
	lmselected = getlmselected("n4")
	
	if (page == None):
		page = 1
	funpage = zz91page()
	limitNum = funpage.limitNum(10)
	nowpage = funpage.nowpage(int(page))
	frompageCount = funpage.frompageCount()
	after_range_num = funpage.after_range_num(6)
	before_range_num = funpage.before_range_num(9)
	
	listall = getcompanynewslist(frompageCount, limitNum, company_id)
	
	newslist = listall['list']
	newslistcount = listall['count']
	listcount = newslistcount
	if (int(listcount) > 1000000):
		listcount = 1000000 - 1
	listcount = funpage.listcount(listcount)
	page_listcount = funpage.page_listcount()
	firstpage = funpage.firstpage()
	lastpage = funpage.lastpage()
	page_range = funpage.page_range()
	nextpage = funpage.nextpage()
	prvpage = funpage.prvpage()
	
	#integral = getcompanyintegral(company_id)
	list = getcompanydetail(company_id)
	#非来电宝客户404
	if list:
		if list.get("viptype").get("vipcheck")==None or list.get("baidu"):
			html = render(request, '404.html', locals())
			return HttpResponseNotFound(html)
	# 非来电宝用户跳转到公司首页
	if not list:
		return HttpResponsePermanentRedirect('http://company.zz91.com/compinfo' + str(company_id) + '.htm')

	return render_to_response('html/' + html + '/news.html', locals())
	#return render_to_response('html/' + html +'/news.html', locals())
#资讯详情
def newsdetail(request, id):
	
	company_id = getnewscompanyid(id)
	#----再生通301跳转
	iszst = getiszstcompany(company_id)
	if iszst:
		return ppciszst301(company_id)
		
	htmlincludes = htmlinclude(company_id)
	if (htmlincludes['html'] == ""):
		return render_to_response('404.html', locals())
	html = htmlincludes['html']
	csscode = htmlincludes['css']
	
	lmselected = getlmselected("n4")
	newsdetail = getcompanynewsdetails(company_id, id)
	#integral = getcompanyintegral(company_id)
	list = getcompanydetail(company_id)
	#非来电宝客户404
	if list:
		if list.get("viptype").get("vipcheck")==None or list.get("baidu"):
			html = render(request, '404.html', locals())
			return HttpResponseNotFound(html)
	#nextnews = getcompanynewsnext(company_id, id)
	#otherlist = getcompanynewslist(0, 10, company_id)
	
	return render_to_response('html/' + html + '/news_detail.html', locals())
#联系我们
def contact(request, company_id):
	#----再生通301跳转
	iszst = getiszstcompany(company_id)
	if iszst:
		return ppciszst301(company_id, 'lxfs')
	
	htmlincludes = htmlinclude(company_id)
	if (htmlincludes['html'] == ""):
		return render_to_response('404.html', locals())
	html = htmlincludes['html']
	csscode = htmlincludes['css']
	lmselected = getlmselected("n5")
	
	#integral = getcompanyintegral(company_id)
	#serieslist = getproductsseries(company_id)
	list = getcompanydetail(company_id)
	#非来电宝客户404
	if list:
		if list.get("viptype").get("vipcheck")==None or list.get("baidu"):
			html = render(request, '404.html', locals())
			return HttpResponseNotFound(html)
	# 非来电宝用户跳转到公司首页
	if not list:
		return HttpResponsePermanentRedirect('http://company.zz91.com/compinfo' + str(company_id) + '.htm')

	prolist2 = getcompanyproductslist(frompageCount=0, limitNum=2, company_id=company_id)
	return render_to_response('html/' + html + '/contact.html', locals())
	#return render_to_response('html/ldb/mo1/contact.html', locals())

# 搜索文字转码
def searchfirst(request):
	keywords = request.GET.get("keywords")
	keywords_hex=getjiami(keywords)
	nowurl="/ppc/s-"+keywords_hex
	return HttpResponsePermanentRedirect(nowurl)
#ppc推广页面
def tuijian(request, pinyin='', page='', pdt_type='',keyword=''):
	host=getnowurl(request)
	ishowad = True
	# 关键字拼音 获取中文
	keywords = ""
	if pinyin != None and pinyin !='' :
		pinyin = pinyin.lower()
		sql = "select title,id from phone_seo_keywords where pinyin=%s"
		cursor.execute(sql, [pinyin])
		result = cursor.fetchone()
		if result:
			keywords = result[0]
			id = result[1]
			sql = "update phone_seo_keywords set gmt_modified=now(),click_count=click_count + 1 where id=%s"
			cursor.execute(sql, [id])
			conn.commit()
		
		return HttpResponsePermanentRedirect("/ppc/s-"+getjiami(keywords))
	else :
		pinyin = "s-"+keyword
		keywords = keyword
		keywords_hex=keywords
		keywords=keywords.decode("hex").decode('utf8','ignore')
		keywords=keywords.replace("astojh","#")
		keywords=keywords.replace("astoxg","/")
		keywords=keywords.replace("astoxf","%")
		keywords=keywords.replace("astoxl","\\")
		keywords=keywords.replace("astohg","-")
		keywords=keywords.replace("astokhl","(")
		keywords=keywords.replace("astokhr",")")
	
	if "办证" in keywords or "办假" in keywords:
		return HttpResponseNotFound(keywords+"<h1>FORBIDDEN4</h1>")
	mingang=getmingganword(keywords)
	if mingang:
		return HttpResponseNotFound(keywords+"<h1>FORBIDDEN4</h1>")
	keywords_hex = getjiami(keywords)	
	# 判断页面是title keywords description
	if pdt_type == '0' :
		pdtName = '供应'
	elif pdt_type == '1':
		pdtName = '求购'
		
		#shoprolist=getshoprolist()
	
	mobileflag=request.GET.get("mobileflag")
	if mobileflag:
		return HttpResponsePermanentRedirect("http://m.zz91.com/offerlist/?keywords="+keywords)
	arealist=['浙江','广东','江苏','福建','安徽','河南','河北','湖北','湖南','山东','海南','哈尔滨','北京','上海','广州','天津','青海','陕西','山西','贵州','辽宁','宁夏','吉林','内蒙古','广西','云南','西藏','重庆','甘肃','新疆','台湾','香港','澳门']
	#alijsload="1"
	nowlanmu="<a href='/category/'>供求类别</a>"
	if (page == None or page=='' or page=="None"):
		page = 1
	nowsearcher="offersearch_new"
	company_id=request.session.get("company_id",None)
	username=request.session.get("username",None)
	searchname = urlquote(request.GET.get("searchname"))
	pdt_kind = pdt_type
	province = request.GET.get("province")
	provincecode = request.GET.get("provincecode")
	posttime = request.GET.get("posttime")
	pdtidlist = request.GET.get("pdtidlist")
	priceflag = str(request.GET.get("priceflag"))
	nopiclist = request.GET.get("nopiclist")
	tfromdate = request.GET.get("fromdate")
	ttodate = request.GET.get("todate")
	jmsearchname = request.GET.get("jmsearchname")
	fromsort = request.GET.get("fromsort")
	
	for ltt0 in ['供应','出售','卖']:
		if ltt0 in keywords:
			keywords=keywords.replace(ltt0,'')
			pdt_kind='1'
	for ltt1 in ['求购','回收','买','收购']:
		if ltt1 in keywords:
			keywords=keywords.replace(ltt1,'')
			pdt_kind='2'
	
	forcompany_id = request.GET.get("company_id")
	havepic = request.GET.get("havepic")
	haveprice = request.GET.get("haveprice")
	isding=1
	if havepic or haveprice:
		isding=''
	pdt_kindname=''
	if pdt_kind=='1':
		pdt_kindname='供应'
	if pdt_kind=='2':
		pdt_kindname='求购'
	nowlanmu2=pdt_kindname
	if haveprice:
		nowlanmu2+='－ 价格'
	if havepic:
		nowlanmu2+='－ 图片'
	#----时间筛选
	timearg = request.GET.get("timearg")
	if timearg:
		gmt_end=int(time.time())
		if timearg=='1':
			gmt_begin=gmt_end-24*3600
		elif timearg=='2':
			gmt_begin=gmt_end-24*3600*3
		elif timearg=='3':
			gmt_begin=gmt_end-24*3600*7
		elif timearg=='4':
			gmt_begin=gmt_end-24*3600*30
		elif timearg=='5':
			gmt_begin=gmt_end-24*3600*60
	else:
		timearg=''

	if (str(page)=='1' or page=='' or str(page)=='None'):
		pdtidlist=""
	else:
		pdtidlist=""
	#--------------------------------------------
	if (province=='' or province == None):
		provinceUrl=''
	else:
		provinceUrl="?province="+province
		
	if (pdt_kind == '' or pdt_kind == None or pdt_kind=="0"):
#		pdt_type=''
		pdt_kind='0'
		stab1="offerselect"
		stab2=""
		stab3=""
	if (pdt_kind =='1'):
#		pdt_type='0'
		stab1=""
		stab2="offerselect"
		stab3=""
	if (pdt_kind=='2'):
#		pdt_type='1'
		stab1=""
		stab2=""
		stab3="offerselect"
	
	
	nowpage=int(page)
	page=20*(int(page)-1)
	keywords2=keywords.replace('|','')
	keywords2=keywords2.replace(' ','')
	
	keywords1=urlquote(keywords2)
	ttype = request.GET.get("ttype")
	keywords=keywords.replace('|',' ')
	keywords=keywords.replace('\\',' ')
	keywords=keywords.replace('/',' ')
	keywords=keywords.replace('/',' ')
	keywords=keywords.replace('(',' ')
	keywords=keywords.replace(')',' ')
	if (ttype==None):
		ttype=''
	if (posttime==None):
		posttime=''
	if (priceflag==None or str(priceflag)=='None'):
		priceflag=''
	if (nopiclist==None or str(nopiclist)=='None'):
		nopiclist=''
	if (havepic==None or str(havepic)=='None'):
		havepic=''
	#action = '&keywords='+searchname+'&ptype='+pdt_kind+'&province='+urlquote(province)+'&posttime='+str(posttime)+'&ttype='+str(ttype)+'&priceflag='+str(priceflag)+'&nopiclist='+str(nopiclist)+'&jmsearchname='+str(jmsearchname)+'&havepic='+str(havepic)+'&fromsort='+str(fromsort)
	#a(\d*)--b(\d*)--c(\d*)--d(\d*)--e(\d*)--f(\d*)
	action='a'+str(pdt_kind)+'--b'+str(provincecode)+'--c'+str(posttime)+'--d'+str(priceflag)+'--e'+str(nopiclist)+'--f'+str(havepic)+''
	searchname=str(keywords1)
	searchname=searchname.replace('%28','astokhl')
	searchname=searchname.replace('%29','astokhr')
	searchname=searchname.replace('%5C','asto5c')
	searchname=searchname.replace('/','astoxg')
	searchname=searchname.replace('-','astohg')
	after_range_num = 8
	before_range_num = 9
	port = spconfig['port']

	#----------------------------
	cl = SphinxClient()
	cl = SphinxClient()
	list = SphinxClient()
	
	cl.SetServer ( spconfig['serverid'], port )
	list.SetServer ( spconfig['serverid'], port )
	cl.SetMatchMode ( SPH_MATCH_BOOLEAN )
	list.SetMatchMode ( SPH_MATCH_BOOLEAN )
	
	#取得总数
	nowdate=date.today()-timedelta(days=2)
	nextday=date.today()+timedelta(days=2)
	formatnowdate=time.mktime(nowdate.timetuple())
	formatnextday=time.mktime(nextday.timetuple())
	searstr=''
	
	if (pdt_kind !='0' and pdt_type):
		searstr+=";filter=pdt_kind,"+pdt_type
		cl.SetFilter('pdt_kind',[int(pdt_type)])
		list.SetFilter('pdt_kind',[int(pdt_type)])
		
	if(havepic=='1'):
		cl.SetFilterRange('havepic',1,100)
		list.SetFilterRange('havepic',1,100)
	#list.SetFilter('viptype',[0],True)
	#cl.SetFilter('offerstaus',[0])
	#list.SetFilter('offerstaus',[0])
	if (ttype == '1'):	
		cl.SetFilterRange('pdt_date',int(formatnowdate),int(formatnextday))
		list.SetFilterRange('pdt_date',int(formatnowdate),int(formatnextday))
		#searstr+=' ;range=refresh_time,'+str(formatnowdate)+','+str(formatnextday)+''
		
	if (posttime =='' or posttime==None or posttime=='None'):
		searstr +=''
	else:
		pfromdate=date.today()-timedelta(days=int(posttime)+1)
		#test=str(time.mktime(pfromdate.timetuple()))
		ptodate=date.today()+timedelta(days=3)
		
		pfromdate_int=int(time.mktime(pfromdate.timetuple()))
		ptodate_int=int(time.mktime(ptodate.timetuple()))
		if (pfromdate!=None):
			cl.SetFilterRange('pdt_date',int(pfromdate_int),int(ptodate_int))
			list.SetFilterRange('pdt_date',int(pfromdate_int),int(ptodate_int))
		#searstr += ';refresh_time,'+str(pfromdate_int)+','+str(ptodate_int)+''
	if timearg:
		cl.SetFilterRange('pdt_date',gmt_begin,gmt_end)
		list.SetFilterRange('pdt_date',gmt_begin,gmt_end)
	if haveprice:
		cl.SetFilterRange('length_price',4,10000)
		list.SetFilterRange('length_price',4,10000)
		cl.SetFilter('haveprice',[1],True)
		list.SetFilter('haveprice',[1],True)
	if forcompany_id:
		forcompany_id=int(forcompany_id)
		cl.SetFilter('company_id',[forcompany_id])
		list.SetFilter('company_id',[forcompany_id])
	
	if (province ==None or province ==''):
		provincestr=''
	else:
		provincestr='&@(province,city) '+province

	if (priceflag == '1'):
		cl.SetFilter('length_price',[0],True)
		list.SetFilter('length_price',[0],True)
		list.SetSortMode( SPH_SORT_EXTENDED,"length_price desc,refresh_time desc" )
	elif (priceflag == '2'):
		list.SetFilter('length_price',[0],True)
		list.SetSortMode( SPH_SORT_EXTENDED,"length_price asc,refresh_time desc" )
	else:
		list.SetSortMode( SPH_SORT_EXTENDED,"refresh_time desc" )
	if keywords=='':
		res = list.Query ('',nowsearcher)
	else:
		res = list.Query ( '@(title,label0,label1,label2,label3,label4,city,province,tags) '+keywords+provincestr+'',nowsearcher)
	if not res:
		listcount=0
	else:
		listcount=res['total_found']
	
	cl.SetFilterRange('viptype',1,5)
	#cl.SetFilterRange('Prodatediff',0,3)
	
	#获得3天内再生通数据优先排序
	#listallvip=cache.get('list'+action)
	
	cl.SetSortMode( SPH_SORT_EXTENDED,"company_id desc,refresh_time desc" )
	cl.SetLimits (0,100000,100000)
	if keywords=='':
		rescount = cl.Query ('','offersearch_new_vip')
	else:
		rescount = cl.Query ( '@(title,label0,label1,label2,label3,label4,city,province,tags) '+keywords+provincestr+'','offersearch_new_vip')
	pcount=0
	listall=[]
	if rescount:
		if rescount.has_key('matches'):
			tagslist=rescount['matches']
			testcom_id=0
			pcount=100000
			for match in tagslist:
				id=match['id']
				com_id=match['attrs']['company_id']
				viptype=match['attrs']['viptype_ldb']
				phone_rate=int(match['attrs']['phone_rate'])
				phone_num=int(match['attrs']['phone_num'])
				phone_fee=float(match['attrs']['phone_cost'])
				refresh_time=float(match['attrs']['refresh_time'])
				pdt_date=float(match['attrs']['pdt_date'])
				phone_level=float(match['attrs']['phone_level'])
				if (testcom_id==com_id):
					pcount-=1
				else:
					pcount=100000
				if phone_num==10000:
					phone_sort=10000;
				else:
					phone_sort=phone_rate*0.05+phone_num*0.85+phone_fee*0.1
				list1=(id,pcount,viptype,refresh_time,pdt_date,phone_sort,phone_level)
				listall.append(list1)
				testcom_id=com_id
	#listallvip=tradeorderby(listall)
	listallvip=sorted(listall, key=itemgetter(1,4,2,5,6,3),reverse=True)
	#cache.set('list'+action, listallvip, 15*60)
	#test=listallvip	
	#优先排序数
	viplen=len(listallvip)
	
	#供求总数
	listcount+=int(viplen)
	#最后一页的供求数
	lastpNum=int(viplen-ceil(viplen / 20)*20)
	#开始供求数位置
	beginpage=page
	#优先排序页码
	pageNum=0
	if (lastpNum==0):
		pageNum=int(ceil(viplen / 20))
	else:
		pageNum=int(ceil(viplen / 20)+1)
	
	#结束供求数位置
	if (int(nowpage)==int(pageNum) and lastpNum!=0):
		endpage=int(page+lastpNum)
	elif(int(nowpage)==int(pageNum) and lastpNum==0 and int(nowpage)==1):
		endpage=20
	elif(int(nowpage)==int(pageNum) and lastpNum==0):
		endpage=int(page)
	else:
		endpage=page+20
	#列出供求信息列表
	listall=[]
	for match in listallvip[beginpage:endpage]:
		list1=getcompinfoForTuijian(match[0],cursor,keywords2)
		listall.append(list1)
	productList=listall
	
	#普通供求开始数
	offsetNum=0
	limitNum=20
	if (nowpage==pageNum and lastpNum!=0):
		offsetNum=0
		limitNum=20-lastpNum
		notvip=1
	elif (nowpage==pageNum and lastpNum==0 and viplen>0):
		offsetNum=0
		limitNum=20-lastpNum
		notvip=0
	elif (nowpage==pageNum and lastpNum==0 and viplen==0):
		offsetNum=0
		limitNum=20
		notvip=1
	elif (nowpage>pageNum and lastpNum==0):
		offsetNum=(nowpage-pageNum-1)*20
		limitNum=20-lastpNum
		notvip=1
	elif(nowpage>pageNum and lastpNum>0):
		offsetNum=((int(nowpage)-int(pageNum)-1)*20)+(20-int(lastpNum))
		limitNum=20
		notvip=1
	elif (viplen<1):
		offsetNum=(nowpage-1)*20
		limitNum=20
		notvip=1
	else:
		notvip=0
	#优先排序供求结束页的
	#test=str(lastpNum)+'|'+str(pageNum)+'|'+str(offsetNum)+'|'+str(limitNum)
	
	if (nowpage==pageNum and lastpNum!=0):
		listall=productList
	else:
		listall=[]
	if (notvip==1):
		list.SetLimits (offsetNum,limitNum,100000)
		if keywords=='':
			res = list.Query ('',nowsearcher)
		else:
			res = list.Query ('@(title,label0,label1,label2,label3,label4,city,province,tags) '+keywords+provincestr+'',nowsearcher)

		if res:
			if res.has_key('matches'):
				prodlist=res['matches']
				for list in prodlist:
					id=list['id']
					list1=getcompinfoForTuijian(id,cursor,keywords2)
					listall.append(list1)
				productList=listall

	#cache.set('productList', productList, 300)
	#底部页码
	#connt.close()
	page_listcount=int(ceil(listcount / 20))+1
	page_rangep=[]
	i=1
	while (i<=page_listcount):
		pages={'number':'','nowpage':''}
		pages['number']=i
		if (i==page):
			pages['nowpage']='1'
		else:
			pages['nowpage']=None
			
		page_rangep.append(pages)
		i+=1
	if (page_listcount>1 and page>1):
		firstpage=1
	else:
		firstpage=None
	if (page<page_listcount and page_listcount>1):
		lastpage=1
	else:
		lastpage=None
	if page >= after_range_num:
		page_range = page_rangep[page-after_range_num:page + before_range_num]
	else:
		page_range = page_rangep[0:int(page) + before_range_num]
	nextpage=page+1
	prvpage=page-1
	#大于500页提示
	
	funpage = zz91page()
	limitNum=funpage.limitNum(20)
	nowpage=funpage.nowpage(int(page)/20+1)
	frompageCount=funpage.frompageCount()
	after_range_num = funpage.after_range_num(5)
	before_range_num = funpage.before_range_num(5)
	
	listcount = funpage.listcount(listcount)
	page_listcount=funpage.page_listcount()
	firstpage = funpage.firstpage()
	lastpage = funpage.lastpage()
	page_range  = funpage.page_range()
	nextpage = funpage.nextpage()
	prvpage = funpage.prvpage()

	if(page_listcount>500 and page>=500):
		arrtishi="提示：为了提供最相关的搜索结果，ZZ91再生网只显示500页信息，建议您重新搜索！"
	else:
		arrtishi=None
	
	if not productList:
		keywords='暂无'

	# 今日报价
	# priceList = getPriceListForTuijian(keywords,10)
	# 相关报价
	productsList = getcompanyproductslist(kname=keywords, frompageCount=0, limitNum=10, maxcount=10, fcflag=1, haveprice=1, groupbyflag=1)
	if productsList:
		productsList=productsList['list']
	
	# 热搜词
	sql = 'select id,pinyin,title,click_count from phone_seo_keywords order by click_count desc limit 8'
	cursor.execute(sql)
	keywordResult = cursor.fetchall()
	keywordList = []
	i = 1
	for obj in keywordResult:
		dict = {'id':obj[0], 'pinyin':obj[1], 'title':obj[2], 'clickCount':obj[3], 'numb':i}
		keywordList.append(dict)
		i = i + 1
	
	# 相关文章
	newsList = getNewsList(keywords=keywords, frompageCount=0, limitNum=12, allnum=12)
	
	return render_to_response('html/ppc/tuijian.html', locals())

def renzheng(request,company_id):
	#----再生通301跳转
	iszst = getiszstcompany(company_id)
	if iszst:
		return ppciszst301(company_id, 'gsjs')
	
	htmlincludes = htmlinclude(company_id)
	if (htmlincludes['html'] == ""):
		return render_to_response('404.html', locals())
		
	html = htmlincludes['html']
	csscode = htmlincludes['css']
	lmselected = getlmselected("n2")
	
	#integral = getcompanyintegral(company_id)
	#serieslist = getproductsseries(company_id)
	list = getcompanydetail(company_id)
	credit_file=getcredit_file(company_id)
	#非来电宝客户404
	if list:
		if list.get("viptype").get("vipcheck")==None or list.get("baidu"):
			html = render(request, '404.html', locals())
			return HttpResponseNotFound(html)
	# 非来电宝用户跳转到公司首页
	if not list:
		return HttpResponsePermanentRedirect('http://company.zz91.com/compinfo' + str(company_id) + '.htm')
	#companypiclist = getcompanyimgall(0, 3, company_id)
	#if not companypiclist:
	#	propiclist = getcompanyproductslist(frompageCount=0, limitNum=3, company_id=company_id)
	#prolist2 = getcompanyproductslist(frompageCount=0, limitNum=2, company_id=company_id)
	#compic=getcompanyimgall(0,4,company_id)
	return render_to_response('html/' + html + '/renzheng.html', locals())
	#return render_to_response('html/ldb/mo1/renzheng.html', locals())