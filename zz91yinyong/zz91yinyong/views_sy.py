#-*- coding:utf-8 -*-
import MySQLdb   
import settings
from settings import pyuploadpath,pyimgurl,spconfig
import codecs
from django.utils.http import urlquote
from django.shortcuts import render_to_response
from django.http import HttpResponse,HttpResponseRedirect
from django.core.paginator import Paginator,InvalidPage,EmptyPage,PageNotAnInteger
import time
import sys
import datetime,md5,hashlib
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
#验证码
import memcache
import Image,ImageDraw,ImageFont,ImageFilter
try:
	import cStringIO as StringIO
except ImportError:
	import StringIO
import requests
	
from sphinxapi import *
from zz91page import *

from zz91db_ast import companydb
from zz91db_2_news import newsdb
from zz91db_ads import adsdb

dbc=companydb()
dbn=newsdb()
dbads=adsdb()

reload(sys)
sys.setdefaultencoding('UTF-8')
nowpath=os.path.dirname(__file__)
execfile(nowpath+"/commfunction.py")
execfile(nowpath+"/function.py")
def englishlist():
	pinyin=['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']
	return pinyin
	
def default(request):
	pinyinlist=englishlist()
	categorylist=getcategorylist(kname='',limitcount=10000)
	return render_to_response('sy/index.html',locals())
def plist_pinyin(request,pinyin,page):
	pinyinlist=englishlist()
	if (page==None):
		page=1
	funpage = zz91page()
	limitNum=funpage.limitNum(1000)
	nowpage=funpage.nowpage(int(page))
	frompageCount=funpage.frompageCount()
	after_range_num = funpage.after_range_num(500)
	before_range_num = funpage.before_range_num(500)
	
	listall=getsyproductslist(None,frompageCount,limitNum,pinyin,200000)
	
	productslist=listall['list']
	productslistcount=listall['count']
	listcount=productslistcount
	if (int(listcount)>1000000):
		listcount=1000000-1
	listcount = funpage.listcount(listcount)
	page_listcount=funpage.page_listcount()
	firstpage = funpage.firstpage()
	lastpage = funpage.lastpage()
	page_range  = funpage.page_range()
	nextpage = funpage.nextpage()
	prvpage = funpage.prvpage()
	return render_to_response('sy/plist_pinyin.html',locals())
	
def plist(request,id,page):
	pinyinlist=englishlist()
	if (int(id)>0):
		label=getproductscategoryname(id)
		if label:
			keywords=label[0]
		else:
			keywords=None
	else:
		keywords=None
	if (page==None):
		page=1
	funpage = zz91page()
	limitNum=funpage.limitNum(1000)
	nowpage=funpage.nowpage(int(page))
	frompageCount=funpage.frompageCount()
	after_range_num = funpage.after_range_num(500)
	before_range_num = funpage.before_range_num(500)
	
	listall=getsyproductslist(keywords,frompageCount,limitNum,None,allnum=200000)
	
	productslist=listall['list']
	productslistcount=listall['count']
	listcount=productslistcount
	if (int(listcount)>1000000):
		listcount=1000000-1
	listcount = funpage.listcount(listcount)
	page_listcount=funpage.page_listcount()
	firstpage = funpage.firstpage()
	lastpage = funpage.lastpage()
	page_range  = funpage.page_range()
	nextpage = funpage.nextpage()
	prvpage = funpage.prvpage()
	if (keywords==None):
		keywords="废料"
	return render_to_response('sy/plist.html',locals())
##索引公司列表页
def clist_pinyin(request,pinyin,page):
	pinyinlist=englishlist()
	if (page==None):
		page=1
	funpage = zz91page()
	limitNum=funpage.limitNum(1000)
	nowpage=funpage.nowpage(int(page))
	frompageCount=funpage.frompageCount()
	after_range_num = funpage.after_range_num(500)
	before_range_num = funpage.before_range_num(500)
	
	listall=getsycompanylist(None,frompageCount,limitNum,pinyin)
	
	companylist=listall['list']
	companylistcount=listall['count']
	listcount=companylistcount
	if (int(listcount)>1000000):
		listcount=1000000-1
	listcount = funpage.listcount(listcount)
	page_listcount=funpage.page_listcount()
	firstpage = funpage.firstpage()
	lastpage = funpage.lastpage()
	page_range  = funpage.page_range()
	nextpage = funpage.nextpage()
	prvpage = funpage.prvpage()
	return render_to_response('sy/clist_pinyin.html',locals())
def clist(request,id,page):
	pinyinlist=englishlist()
	if (int(id)>0):
		label=getproductscategoryname(id)
		keywords=label[0]
	else:
		keywords=None
	if (page==None):
		page=1
	funpage = zz91page()
	limitNum=funpage.limitNum(1000)
	nowpage=funpage.nowpage(int(page))
	frompageCount=funpage.frompageCount()
	after_range_num = funpage.after_range_num(500)
	before_range_num = funpage.before_range_num(500)
	
	listall=getsycompanylist(keywords,frompageCount,limitNum,None)
	
	companylist=listall['list']
	companylistcount=listall['count']
	listcount=companylistcount
	if (int(listcount)>1000000):
		listcount=1000000-1
	listcount = funpage.listcount(listcount)
	page_listcount=funpage.page_listcount()
	firstpage = funpage.firstpage()
	lastpage = funpage.lastpage()
	page_range  = funpage.page_range()
	nextpage = funpage.nextpage()
	prvpage = funpage.prvpage()
	if (keywords==None):
		keywords="废料"
	return render_to_response('sy/clist.html',locals())
#标签索引
def tagslist(request,page):
	pinyinlist=englishlist()
	if (page==None):
		page=1
	funpage = zz91page()
	limitNum=funpage.limitNum(1000)
	nowpage=funpage.nowpage(int(page))
	frompageCount=funpage.frompageCount()
	after_range_num = funpage.after_range_num(500)
	before_range_num = funpage.before_range_num(500)
	
	listall=gettagslist(frompageCount,limitNum,None)
	tagslist=listall['list']
	tagslistcount=listall['count']
	listcount=tagslistcount
	if (int(listcount)>1000000):
		listcount=1000000-1
		
	listcount = funpage.listcount(listcount)
	page_listcount=funpage.page_listcount()
	firstpage = funpage.firstpage()
	lastpage = funpage.lastpage()
	page_range  = funpage.page_range()
	nextpage = funpage.nextpage()
	prvpage = funpage.prvpage()

	
	return render_to_response('sy/tagslist.html',locals())
def tagslist_pinyin(request,pinyin,page):
	pinyinlist=englishlist()
	if (page==None):
		page=1
	funpage = zz91page()
	limitNum=funpage.limitNum(1000)
	nowpage=funpage.nowpage(int(page))
	frompageCount=funpage.frompageCount()
	after_range_num = funpage.after_range_num(500)
	before_range_num = funpage.before_range_num(500)
	
	listall=gettagslist(frompageCount,limitNum,pinyin)
	tagslist=listall['list']
	tagslistcount=listall['count']
	listcount=tagslistcount
	if (int(listcount)>1000000):
		listcount=1000000-1
		
	listcount = funpage.listcount(listcount)
	page_listcount=funpage.page_listcount()
	firstpage = funpage.firstpage()
	lastpage = funpage.lastpage()
	page_range  = funpage.page_range()
	nextpage = funpage.nextpage()
	prvpage = funpage.prvpage()

	
	return render_to_response('sy/tagslist_pinyin.html',locals())

def plist_date(request):
	pinyinlist=englishlist()
	yearlist=getdatelist()
	
	categorylist=getindexcategorylist('____',2)
	return render_to_response('sy/plist_date.html',locals())