#-*- coding:utf-8 -*-
import MySQLdb   
import pymssql
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
conn_rcu=pymssql.connect(host=r'192.168.110.112',trusted=False,user='astotest',password='zj88friend',database='rcu',charset=None)
cursor_rcu=conn_rcu.cursor()

connt = MySQLdb.connect(host='192.168.110.118', user='ast', passwd='astozz91jiubao',db='ast',charset='utf8')   
cursor_my = connt.cursor()
nowpath=os.path.dirname(__file__)
execfile(nowpath+"/commfunction.py")


def getcate_province(conn,id):
	sql="select top 1 meno from cate_province where code="+str(id)+""
	conn.execute(sql)
	arrkname=conn.fetchone()
	if (arrkname):
		return arrkname[0].decode('GB18030','ignore').encode('utf-8')
def getprovinceDetail(conn,provinceID):
	sql="select top 1 Introduce from Area_Introduce where code="+str(provinceID)+""
	conn.execute(sql)
	arrkname=conn.fetchone()
	if (arrkname):
		return arrkname[0].decode('GB18030','ignore').encode('utf-8')

def default(request):
	#-----------供求信息
	provinceID = request.GET.get("provinceID")
	city = request.GET.get("city")
	trade=request.GET.get("trade")
	keys=request.GET.get("keys")
	
	if (provinceID!=None and str(provinceID)!='0' and provinceID!=''):
		if (city!="" and str(city)!='None'):
			province=getcate_province(cursor_rcu,city)
			provinceDetail=getprovinceDetail(cursor_rcu,city)
		else:
			province=getcate_province(cursor_rcu,provinceID)
			provinceDetail=getprovinceDetail(cursor_rcu,provinceID)
		#provinceDetail=HttpResponse(provinceDetail)
	else:
		province=None
		provinceDetail=None
		provinceID=0
	page = request.GET.get("page")
	if (page==None):
		page=1
	funpage = zz91page()
	limitNum=funpage.limitNum(14)
	nowpage=funpage.nowpage(int(page))
	frompageCount=funpage.frompageCount()
	after_range_num = funpage.after_range_num(2)
	before_range_num = funpage.before_range_num(9)
	listcount=0
	port = 9315
	cl = SphinxClient()
	cl.SetServer ( '192.168.110.120', port )
	cl.SetMatchMode ( SPH_MATCH_BOOLEAN )
	cl.SetSortMode( SPH_SORT_EXTENDED,"refresh_time desc" )
	cl.SetLimits (frompageCount,limitNum,100000)
	searcher=''
	if (province!=None and province!=""):
		searcher+='@province '+province
	if (trade!=None and keys!=''):
		searcher+='&@(title,label0,label1,label2,label3,label4,city,province,tags) '+trade.encode('utf-8')
	if (keys!=None and keys!=''):
		searcher+=''
		searcher+='&@(title,label0,label1,label2,label3,label4,city,province,tags) '+keys.encode('utf-8')
	res = cl.Query (''+searcher+'','offersearch_new')
	if res:
		if res.has_key('matches'):
			tagslist=res['matches']
			listall=[]
			for match in tagslist:
				pdtid=match['id']
				list1=getcompinfo(pdtid,cursor_my,keys)
				if (list1!=None):
					pdt_detail=list1['pdt_detail']
					if (pdt_detail!=None):
						pdt_detail=pdt_detail.replace('<br>','').replace('&nbsp;',' ')
						pdt_detail=subString(pdt_detail,50)+'...'
					list1['pdt_detail']=pdt_detail
					pdt_kind=list1['pdt_kind']
					kindclass=pdt_kind['kindclass']
					vipflag=list1['vipflag']
					vippic=vipflag['vippic']
					if (vippic==None):
						list1['vipflag']['vipname']='普通会员'
					if (vippic=='http://img.zz91.com/zz91images/recycle.gif'):
						list1['vipflag']['vipname']='再生通'
					if (vippic=='http://img.zz91.com/zz91images/pptSilver.gif'):
						list1['vipflag']['vipname']='银牌品牌通'
					if (vippic=='http://img.zz91.com/zz91images/pptGold.gif'):
						list1['vipflag']['vipname']='金牌品牌通'
					if (vippic=='http://img.zz91.com/zz91images/pptDiamond.gif'):
						list1['vipflag']['vipname']='钻石品牌通'
					if (kindclass=='sell'):
						list1['pdt_kind']['kindtxt']='供应'
					if (kindclass=='buy'):
						list1['pdt_kind']['kindtxt']='求购'
				listall.append(list1)
		listcount=res['total_found']
	if (int(listcount)>100000):
		listcount=100000
	listcount = funpage.listcount(listcount)
	page_listcount=funpage.page_listcount()
	firstpage = funpage.firstpage()
	lastpage = funpage.lastpage()
	page_range  = funpage.page_range()
	nextpage = funpage.nextpage()
	prvpage = funpage.prvpage()
	province1=province
	if (str(province)=='None'):
		province="全国"
	listall_forum=getbbslist(province1,8)
	listall_price=getpricelist(province1,10,"")
	listall_sales=offerlist(province1,1,8)
	listall_buy=offerlist(province1,2,8)
	listall_news=getbbslist(province1,10)
	return render_to_response('default.html',locals())
	closeconn()

def getpricelist(kname,limitcount,titlelen):
	#------最新报价信息
	if (titlelen==""):
		titlelen=35
	port = 9315
	cl = SphinxClient()
	cl.SetServer ( '192.168.110.120', port )
	cl.SetMatchMode ( SPH_MATCH_BOOLEAN )
	cl.SetSortMode( SPH_SORT_EXTENDED,"gmt_order desc" )
	cl.SetLimits (0,limitcount)
	
	if (kname==None or kname==""):
		res = cl.Query ('','price')
	else:
		res = cl.Query ('@(title,tags) '+kname,'price')
	if res:
		if res.has_key('matches'):
			tagslist=res['matches']
			listall_baojia=[]
			for match in tagslist:
				id=match['id']
				attrs=match['attrs']
				title=subString(str(attrs['ptitle']),titlelen)
				gmt_time=attrs['gmt_time']
				#td_time=gmt_time.strftime('%Y-%m-%d')
				list1={'title':title,'id':id,'gmt_time':gmt_time,'fulltitle':attrs['ptitle']}
				listall_baojia.append(list1)
			listcount_baojia=res['total_found']
			return listall_baojia
def offerlist(kname,pdt_type,limitcount):
	#-----------供应信息
	#-------------供求列表
	port = 9315
	cl = SphinxClient()
	cl.SetServer ( '192.168.110.120', port )
	cl.SetMatchMode ( SPH_MATCH_BOOLEAN )
	cl.SetSortMode( SPH_SORT_EXTENDED," refresh_time desc" )
	cl.SetLimits (0,limitcount)
	if (pdt_type!=None):
		cl.SetFilter('pdt_kind',[int(pdt_type)])
	if (kname):
		res = cl.Query ('@(title,label0,label1,label2,label3,label4,city,province,tags) '+kname,'offersearch_new,offersearch_new_vip')
	else:
		res = cl.Query ('','offersearch_new,offersearch_new_vip')
	if res:
		if res.has_key('matches'):
			itemlist=res['matches']
			listall_offerlist=[]
			for match in itemlist:
				pid=match['id']
				attrs=match['attrs']
				pdt_date=attrs['pdt_date']
				#pdt_date=pdt_date.strftime( '%-Y-%-m-%-d-%-H-%-M')
				sql="select refresh_time from products where id="+str(pid)+""
				cursor_my.execute(sql)
				productlist = cursor_my.fetchone()
				if productlist:
					pdt_date=productlist[0].strftime( '%-Y-%-m-%-d')
				title=subString(str(attrs['ptitle']),50)
				list={'id':pid,'title':title,'gmt_time':pdt_date,'fulltitle':attrs['ptitle']}
				listall_offerlist.append(list)
			return listall_offerlist

def getbbslist(kname,limitcount):
	#最新互助信息
	port = 9315
	cl = SphinxClient()
	cl.SetServer ( '192.168.110.120', port )
	cl.SetMatchMode ( SPH_MATCH_BOOLEAN )
	cl.SetSortMode( SPH_SORT_EXTENDED,"post_time desc" )
	cl.SetLimits (0,limitcount)
	if (kname):
		res = cl.Query ('@(title,tags) '+kname,'huzhu')
	else:
		res = cl.Query ('','huzhu')
	if res:
		if res.has_key('matches'):
			tagslist=res['matches']
			listall_news=[]
			for match in tagslist:
				id=match['id']
				attrs=match['attrs']
				title=subString(attrs['ptitle'],40)
				gmt_time=attrs['ppost_time']
				list1={'title':title,'id':id,'gmt_time':gmt_time,'fulltitle':attrs['ptitle']}
				listall_news.append(list1)
			return listall_news


	

def closeconn():
	cursor.close()
	cursor_rcu.close
	cursor_my.close
