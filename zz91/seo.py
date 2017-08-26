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
import urllib2
import datetime
from datetime import timedelta, date 
from django.views.decorators.cache import cache_control
import os
from django.core.cache import cache
import random
import shutil
import hashlib
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

def getcompanyinfo(pingyin):
	sqlc="select name,business,regtime,address,introduction,membership_code,id,tags from company where domain_zz91=%s"
	cursor.execute(sqlc,pingyin)
	company_id=0
	clist=cursor.fetchone()
	if clist:
		company_id=clist[6]
		compname=clist[0]
		business=clist[1]
		regtime=clist[2]
		address=clist[3]
		introduction=clist[4]
		viptype=clist[5]
		tags=clist[7]
		arrviptype={'vippic':'','vipname':'','vipcheck':''}
		if (viptype == '10051000'):
			arrviptype['vippic']=None
			arrviptype['vipname']='普通会员'
		if (viptype == '10051001'):
			arrviptype['vippic']='http://m.zz91.com/images/recycle.gif'
			arrviptype['vipname']='再生通'
		if (viptype == '100510021000'):
			arrviptype['vippic']='http://m.zz91.com/images/pptSilver.gif'
			arrviptype['vipname']='银牌品牌通'
		if (viptype == '100510021001'):
			arrviptype['vippic']='http://m.zz91.com/images/pptGold.gif'
			arrviptype['vipname']='金牌品牌通'
		if (viptype == '100510021002'):
			arrviptype['vippic']='http://m.zz91.com/images/pptDiamond.gif'
			arrviptype['vipname']='钻石品牌通'
		if (viptype == '10051000'):
			arrviptype['vipcheck']=None
		else:
			arrviptype['vipcheck']=1
	if (company_id>0):
		sqlc="select contact,tel_country_code,tel_area_code,tel,mobile,fax_country_code,fax_area_code,fax,email"
		sqlc=sqlc+",sex,position,qq "
		sqlc=sqlc+"from company_account where company_id=%s"
		cursor.execute(sqlc,company_id)
		alist=cursor.fetchone()
		if alist:
			contact=alist[0]
			tel_country_code=alist[1]
			if (str(tel_country_code)=='None'):
				tel_country_code=""
			tel_area_code=alist[2]
			if (str(tel_area_code)=='None'):
				tel_area_code=""
			tel=alist[3]
			mobile=alist[4]
			fax_country_code=alist[5]
			fax_area_code=alist[6]
			fax=alist[7]
			email=alist[8]
			sex=alist[9]
			position=alist[10]
			if (position==None):
				position=""
				position=position.strip()
			qq=alist[11]
	list={'company_id':company_id,'name':compname,'business':business,'regtime':regtime,'address':address,'introduction':introduction,'contact':contact,'tel_country_code':tel_country_code,'tel_area_code':tel_area_code,'tel':tel,'mobile':mobile,'fax_country_code':fax_country_code,'fax_area_code':fax_area_code,'fax':fax,'email':email,'sex':sex,'position':position,'qq':qq,'viptype':arrviptype,'tags':tags}
	return list
def getcompanynews(company_id):
	sql="select id,title,post_time from esite_news where company_id=%s order by id desc limit 0,10 "
	cursor.execute(sql,company_id)
	alist=cursor.fetchall()
	listall=[]
	if alist:
		for a in alist:
			id=a[0]
			title=a[1]
			post_time=a[2]
			list={'id':id,'title':title,'post_time':post_time}
			listall.append(list)
	return listall
def getpricelist(kname="",assist_type_id="",limitcount="",searchname="",titlelen="",hangqing=""):
	#------最新报价信息
	if (titlelen==""):
		titlelen=35
	port = 9315
	cl = SphinxClient()
	cl.SetServer ( '192.168.110.120', port )
	cl.SetMatchMode ( SPH_MATCH_BOOLEAN )
	cl.SetSortMode( SPH_SORT_EXTENDED,"gmt_order desc" )
	cl.SetLimits (0,limitcount,limitcount)
	if(assist_type_id!=None and assist_type_id!=""):
		if (hangqing=="1"):
			cl.SetFilter('type_id',[217,216,220])
		else:
			cl.SetFilter('assist_type_id',[assist_type_id])
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
				title=subString(attrs['ptitle'],titlelen)
				gmt_time=attrs['gmt_time']
				#td_time=gmt_time.strftime('%Y-%m-%d')
				list1={'title':title,'id':id,'gmt_time':gmt_time,'fulltitle':attrs['ptitle']}
				listall_baojia.append(list1)
			listcount_baojia=res['total_found']
			return listall_baojia
def gettagslist(kname,num):
	#-------------标签列表
	port = 9315
	cl = SphinxClient()
	cl.SetServer ( '192.168.110.120', port )
	cl.SetMatchMode ( SPH_MATCH_BOOLEAN )
	cl.SetSortMode( SPH_SORT_EXTENDED," search_count desc" )
	cl.SetLimits (0,num,num)
	if (kname=="" or kname==None):
		res = cl.Query ('','tagslist')
	else:
		res = cl.Query ('@tname '+kname,'tagslist')
	if res:
		if res.has_key('matches'):
			itemlist=res['matches']
			listall_tagslist=[]
			i=1
			for match in itemlist:
				attrs=match['attrs']
				id=attrs['tid']
				tname=str(attrs['tags'])
				list={'id':id,'name':tname,'name_hex':tname.encode("hex"),'n':i}
				listall_tagslist.append(list)
				i+=1
				if (i>3):
					i=1
			return listall_tagslist

def getproductslist(company_id,num):
	port = 9315
	cl = SphinxClient()
	cl.SetServer ( '192.168.110.120', port )
	cl.SetMatchMode ( SPH_MATCH_BOOLEAN )
	if (company_id):
		cl.SetFilter('company_id',[int(company_id)])
	cl.SetSortMode( SPH_SORT_EXTENDED,"refresh_time desc" )
	cl.SetLimits (0,num,num)
	res = cl.Query ('','offersearch_new,offersearch_new_vip')
	if res:
		if res.has_key('matches'):
			tagslist=res['matches']
			listall=[]
			for match in tagslist:
				id=match['id']
				list=getcompinfo(id,cursor,"")
				listall.append(list)
			listcount=res['total_found']
			return {'list':listall,'count':listcount}
#获得产品标签
def getproductstags(company_id):
	sql="select id,tags from products where company_id=%s order by refresh_time desc limit 0,20"
	cursor.execute(sql,company_id)
	alist=cursor.fetchall()
	listall=[]
	if alist:
		for a in alist:
			list={'id':a[0],'tags':a[1]}
			listall.append(list)
	return listall
def jsproducts(request):
	company_id=request.GET.get("company_id")
	pingyin=request.GET.get("pingyin")
	productslist=getproductslist(company_id,8)
	return render_to_response('seocompany/products.js',locals())
@cache_control(max_age=0)
def company(request,pingyin):
	complist=getcompanyinfo(pingyin)
	company_id=complist['company_id']
	productslist=getproductslist(company_id,8)
	tags=complist['tags']
	tags=tags.replace(",","|")
	tagslist=getproductstags(company_id)
	pricelist=getpricelist(kname=tags,limitcount=15)
	companynews=getcompanynews(company_id)
	return render_to_response('seocompany/'+str(pingyin)+'.html',locals())
	closeconn()
def companynew(request,pingyin):
	complist=getcompanyinfo(pingyin)
	company_id=complist['company_id']
	productslist=getproductslist(company_id,12)
	companynews=getcompanynews(company_id)
	return render_to_response('seocompany/c/'+str(pingyin)+'.html',locals())
	closeconn()