#-*- coding:utf-8 -*-
import MySQLdb   
import settings
import codecs
from settings import pyuploadpath,pyimgurl,spconfig
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
execfile(nowpath+"/conn.py")
execfile(nowpath+"/commfunction.py")
execfile(nowpath+"/function.py")
execfile(nowpath+"/yzm.py")

def default(request):
	username=request.session.get("username",None)
	company_id=request.session.get("company_id",None)
	categorylist=getindexcategorylist('____',2)
	pricelist=getindexpricelist(kname=None,limitcount=5,titlelen=100)
	bbslist=getindexbbslist(kname=None,limitcount=5,bbs_post_category_id=None)
	offerlist=getindexofferlist(None,None,10)
	return render_to_response('standard/default.html',locals())
#注册
def reg(request):
	t=random.randrange(0,1000000)
	username=request.session.get("username",None)
	return render_to_response('standard/reg.html',locals())
def reg_save(request):
	userName = request.POST['userName']
	password1 = request.POST['password1']
	password2 = request.POST['password2']
	email = request.POST['email']
	mobile = request.POST['mobile']
	tel = request.POST['tel']
	company = request.POST['company']
	contact = request.POST['contact']
	productslist = request.POST['productslist']
	t = request.POST['t']
	valcode1 = request.POST['valcode1']
	regtime=gmt_created=datetime.datetime.now()
	gmt_modified=datetime.datetime.now()
	sessonyzm=cache.get("yzm"+str(t))
	
	errflag=0
	if (str(sessonyzm).lower()!=str(valcode1).lower()):
		errtext8="验证码错误"
		errflag=1
	if (userName==''):
		errtext1="必须填写 会员名"
		errflag=1
	if (password1==''):
		errtext2="必须填写 密码"
		errflag=1
	if (password2==''):
		errtext3="必须填写 密码验证"
		errflag=1
	if (email==''):
		errtext4="必须填写 邮箱"
		errflag=1
	if (mobile==''):
		errtext5="必须填写 手机号"
		errflag=1
	if (tel==''):
		errtext6="必须填写 电话"
		errflag=1
	if (company==''):
		errtext7="必须填写 公司名称"
		errflag=1
	if (valcode1==''):
		errtext8="必须填写 验证码"
		errflag=1
	if (contact==''):
		errtext9="必须填写 联系人"
		errflag=1
	if (errflag==0):
		#''判断邮箱帐号是否存在
		sql="select id  from auth_user where username=%s"
		cursor.execute(sql,str(userName))
		accountlist=cursor.fetchone()
		if (accountlist):
			errflag=1
			errtext1="您填写的用户名已经存在！请修改用户名后重新提交！"
		sql="select id  from auth_user where email=%s"
		cursor.execute(sql,str(email))
		accountlist=cursor.fetchone()
		if (accountlist):
			errflag=1
			errtext4="您填写的邮箱已经注册！请修改邮箱后重新提交！"
		if (password1!=password2):
			errflag=1
			errtext2="两次填写的密码不一致，请重新确认！"
	if (errflag==0):
		#''帐号添加
		md5pwd = hashlib.md5(password1)
		md5pwd = md5pwd.hexdigest()[8:-8]
		value=[userName,md5pwd,email,gmt_created,gmt_modified]
		sql="insert into auth_user (username,password,email,gmt_created,gmt_modified) values(%s,%s,%s,%s,%s)"
		cursor.execute(sql,value)
		conn.commit()
		#添加公司信息
		industry_code=''
		business=''
		service_code=''
		area_code=''
		foreign_city=''
		category_garden_id='0'
		membership_code='10051000'
		classified_code='10101002'
		regfrom_code='10031024'
		domain=''
		address=''
		address_zip=''
		website=''
		introduction=''
		
		value=[company, industry_code, business, service_code, area_code, foreign_city, category_garden_id, membership_code,domain, classified_code, regfrom_code,  regtime, gmt_created, gmt_modified,  address, address_zip, website, introduction]
		sql="insert into company (name, industry_code, business, service_code, area_code, foreign_city, category_garden_id, membership_code,    domain, classified_code, regfrom_code,  regtime, gmt_created, gmt_modified,  address, address_zip, website, introduction)"
		sql=sql+" values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)";
		cursor.execute(sql,value);
		conn.commit()
		
		company_id=getcompany_id(company,gmt_created)
		is_admin='1'
		tel_country_code=''
		tel_area_code=''

		fax_country_code=''
		fax_area_code=''
		fax=''
		sex=''
		#'添加联系方式
		value=[userName, company_id, contact, is_admin, tel_country_code, tel_area_code, tel, mobile, fax_country_code, fax_area_code, fax, email, sex, password1, gmt_modified, gmt_created]
		sql="insert into company_account (account, company_id, contact, is_admin, tel_country_code, tel_area_code, tel, mobile, fax_country_code, fax_area_code, fax, email, sex, password, gmt_modified, gmt_created)"
		sql=sql+" values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)";
		cursor.execute(sql,value);
		conn.commit()
		return render_to_response('standard/regsuc.html',locals())
	if (errflag==1):
		return render_to_response('standard/reg.html',locals())
#登录
def login(request):
	done= request.GET.get("done")
	if (done!=None):
		done=done.replace("^and^","&")
	username=request.session.get("username",None)
	company_id=request.session.get("company_id",None)
	if (str(username)=="None"):
		username=""
	if (str(username)!=""):
		return HttpResponseRedirect("/standard/myrc_index/")
	return render_to_response('standard/login.html',locals())
def loginout(request):
	request.session.delete()
	return HttpResponseRedirect("/standard/")
def loginof(request):
	done = request.POST['done']
	username = request.POST['username']
	pwd = request.POST['pwd']
	md5pwd = hashlib.md5(pwd)
	md5pwd = md5pwd.hexdigest()[8:-8]
	sql="select * from auth_user where (username=%s or email=%s) and password=%s"
	cursor.execute(sql,[username,username,md5pwd]);
	plist=cursor.fetchone()
	if plist:
		request.session.set_expiry(60*60)
		request.session['username']=username
		sqlc="select company_id from company_account where account=%s"
		cursor.execute(sqlc,[username]);
		list=cursor.fetchone()
		if list:
			request.session['company_id']=list[0]
			membercheck=getcompanytype(list[0])
			request.session['membercheck']=membercheck
		if (done=="" or done=="None"):
			return HttpResponseRedirect("/standard/myrc_index/")
		else:
			return HttpResponseRedirect(done)
	else:
		error="用户名或密码错误！"
		return render_to_response('standard/login.html',locals())
#生意管家---------------------------------------
def myrc_index(request):
	username=request.session.get("username",None)
	if (username==None):
		return HttpResponseRedirect("/standard/login/")
	return render_to_response('standard/myrc_index.html',locals())
def myrc_leavewords(request):
	username=request.session.get("username",None)
	company_id=request.session.get("company_id",None)
	if (username==None):
		return HttpResponseRedirect("/standard/login/")
	page=request.GET.get("page")
	if (page==None):
		page=1
	funpage = zz91page()
	limitNum=funpage.limitNum(20)
	nowpage=funpage.nowpage(int(page))
	frompageCount=funpage.frompageCount()
	after_range_num = funpage.after_range_num(2)
	before_range_num = funpage.before_range_num(9)
	qlistall=getleavewordslist(frompageCount,limitNum,company_id,"1")
	listcount=0
	if (qlistall):
		qlist=qlistall['list']
		qlistcount=qlistall['count']
		listcount=qlistcount
		if (int(listcount)>100000):
			listcount=100000
	listcount = funpage.listcount(listcount)
	page_listcount=funpage.page_listcount()
	firstpage = funpage.firstpage()
	lastpage = funpage.lastpage()
	page_range  = funpage.page_range()
	nextpage = funpage.nextpage()
	prvpage = funpage.prvpage()
	
	return render_to_response('standard/myrc_leavewords.html',locals())
def myrc_favorite(request):
	username=request.session.get("username",None)
	company_id=request.session.get("company_id",None)
	if (username==None):
		return HttpResponseRedirect("/standard/login/")
	page=request.GET.get("page")
	if (page==None):
		page=1
	funpage = zz91page()
	limitNum=funpage.limitNum(20)
	nowpage=funpage.nowpage(int(page))
	frompageCount=funpage.frompageCount()
	after_range_num = funpage.after_range_num(2)
	before_range_num = funpage.before_range_num(9)
	qlistall=getfavoritelist(frompageCount,limitNum,company_id)
	qlist=qlistall['list']
	qlistcount=qlistall['count']
	listcount=qlistcount
	if (int(listcount)>100000):
		listcount=100000
	listcount = funpage.listcount(listcount)
	page_listcount=funpage.page_listcount()
	firstpage = funpage.firstpage()
	lastpage = funpage.lastpage()
	page_range  = funpage.page_range()
	nextpage = funpage.nextpage()
	prvpage = funpage.prvpage()
	
	return render_to_response('standard/myrc_favorite.html',locals())

#------------------------------------------------
def priceviews(request):
	id=request.GET.get("id")
	username=request.session.get("username",None)
	sql="select title,content,gmt_created,tags from price where id=%s and is_checked=1"
	cursor.execute(sql,str(id))
	alist = cursor.fetchone()
	listall=[]
	if alist:
		title=alist[0]
		content=alist[1]
		content=content.replace("http://price.zz91.com/priceDetails_","http://m.zz91.com/standard/priceviews/")
		gmt_created=alist[2].strftime( '%-Y-%-m-%-d %-H:%-M:%-S')
		tags=alist[3]
		if tags:
			otherpricelist=getindexpricelist(kname=tags.replace(","," "),limitcount=5)
			arrtags=tags.split(",")
		list={'title':title,'content':content,'gmt_created':gmt_created,'tags':tags}
		listall.append(list)
	return render_to_response('standard/priceviews.html',locals())
def priceviews1(request,id):
	done = request.path
	suc=request.GET.get("suc")
	err=request.GET.get("err")
	username=request.session.get("username",None)
	sql="select title,content,gmt_created,tags from price where id=%s and is_checked=1"
	cursor.execute(sql,str(id))
	alist = cursor.fetchone()
	listall=[]
	if alist:
		title=alist[0]
		content=alist[1]
		content=content.replace("http://price.zz91.com/priceDetails_","http://m.zz91.com/standard/priceviews/")
		gmt_created=alist[2].strftime( '%-Y-%-m-%-d %-H:%-M:%-S')
		tags=alist[3]
		if tags:
			otherpricelist=getindexpricelist(kname=tags.replace(","," "),limitcount=5)
			arrtags=tags.split(",")
		list={'title':title,'content':content,'gmt_created':gmt_created,'tags':tags}
		listall.append(list)
	return render_to_response('standard/priceviews.html',locals())
	
def huzhuviews(request,id):
	#id=request.GET.get("id")
	done = request.path
	suc=request.GET.get("suc")
	err=request.GET.get("err")
	username=request.session.get("username",None)
	sql="select title,content,account,gmt_created,bbs_post_category_id,company_id from bbs_post where id=%s"
	cursor.execute(sql,str(id))
	alist = cursor.fetchone()
	if alist:
		title=alist[0]
		content=alist[1]
		company_id=alist[5]
		nickname=getusername(company_id)
		gmt_created=alist[3].strftime( '%-Y-%-m-%-d %-H:%-M:%-S')
		bbs_post_category_id=alist[4]
		content=content.replace("http://huzhu.zz91.com/viewReply","http://m.zz91.com/standard/huzhuviews/viewReply")
		content=replacepic(content)
	page=request.GET.get("page")
	if (page==None):
		page=1
	funpage = zz91page()
	limitNum=funpage.limitNum(20)
	nowpage=funpage.nowpage(int(page))
	frompageCount=funpage.frompageCount()
	after_range_num = funpage.after_range_num(2)
	before_range_num = funpage.before_range_num(9)
	
	pricelistall=getbbsreplylist(None,frompageCount,limitNum,id)
	listall_reply=pricelistall['list']
	pricelistcount=pricelistall['count']
	listcount=pricelistcount
	if (int(listcount)>100000):
		listcount=100000
	listcount = funpage.listcount(listcount)
	page_listcount=funpage.page_listcount()
	firstpage = funpage.firstpage()
	lastpage = funpage.lastpage()
	page_range  = funpage.page_range()
	nextpage = funpage.nextpage()
	prvpage = funpage.prvpage()
	
	replycount=pricelistcount
	
	bbslist=getindexbbslist(kname=None,limitcount=5,bbs_post_category_id=bbs_post_category_id)
	
	return render_to_response('standard/huzhuviews.html',locals())
#回复帖子
def huzhu_replay(request):
	bbs_post_id = request.POST['bbs_post_id']
	content = request.POST['content']
	gmt_created=datetime.datetime.now()
	gmt_modified=datetime.datetime.now()
	username=request.session.get("username",None)
	company_id=request.session.get("company_id",None)
	if (username==None):
		return HttpResponseRedirect("/login/")
	if (content and content!=""):
		value=[company_id,username,bbs_post_id,content,0,0,gmt_created,gmt_modified]
		sql="insert into bbs_post_reply(company_id,account,bbs_post_id,content,is_del,check_status,gmt_created,gmt_modified) values(%s,%s,%s,%s,%s,%s,%s,%s)"
		cursor.execute(sql,value)
		conn.commit()
		return HttpResponseRedirect("/standard/huzhuviews/"+str(bbs_post_id)+".htm?suc=1#hh")
	else:
		return HttpResponseRedirect("/standard/huzhuviews/"+str(bbs_post_id)+".htm?err=1#hh")
#收藏
def favorite(request):
	backurl=request.GET.get("backurl")
	if (backurl==None):
		backurl=request.META.get('HTTP_REFERER','/')
		backurl=backurl.replace("&","^and^")
	else:
		backurl=backurl.replace("^and^","&")
	
	username=request.session.get("username",None)
	cid=request.GET.get("company_id")
	pdtid=request.GET.get("pdtid")
	products_type_code=request.GET.get("products_type_code")
	if (username==None):
		return HttpResponseRedirect("/standard/login/?done=/favorite/?company_id="+str(cid)+"^and^pdtid="+str(pdtid)+"^and^products_type_code="+str(products_type_code)+"^and^title="+request.GET.get("title"))
		
	if (pdtid==None):
		favorite_type_code="10091002"
		content_id=cid
	else:
		if (products_type_code=="10331000"):
			favorite_type_code="10091006"
		if (products_type_code=="10331001"):
			favorite_type_code="10091006"
		content_id=pdtid
	content_title=request.GET.get("title")
	gmt_created=datetime.datetime.now()
	gmt_modified=datetime.datetime.now()
	company_id=request.session.get("company_id",None)
	account=request.session.get("username",None)
	value=[favorite_type_code,content_id,content_title,gmt_created,gmt_modified,company_id,account]
	sql="select id from myfavorite where favorite_type_code=%s and content_id=%s and company_id=%s"
	cursor.execute(sql,[favorite_type_code,content_id,company_id])
	clist=cursor.fetchone()
	if (clist):
		sucflag=None
	else:
		sql="insert into myfavorite(favorite_type_code,content_id,content_title,gmt_created,gmt_modified,company_id,account) values(%s,%s,%s,%s,%s,%s,%s)"
		cursor.execute(sql,value);
		conn.commit()
		sucflag=1
	return render_to_response('standard/favorite.html',locals())

def priceindex(request):
	username=request.session.get("username",None)
	sid=request.GET.get("id")
	pname=request.GET.get("pname")
	if (sid=="" or sid==None):
		sid=1
	sql="select name,id from price_category where parent_id=%s"
	cursor.execute(sql,str(sid))
	alist = cursor.fetchall()
	if alist:
		listall=[]
		for a in alist:
			id=a[1]
			name=a[0]
			childmemu=getcate(id)
			list={'id':id,'name':name,'childmemu':childmemu}
			listall.append(list)
	else:
		return HttpResponseRedirect("/standard/price/?category_id="+str(sid)+"")
	return render_to_response('standard/priceindex.html',locals())
#价格列表
def price(request):
	username=request.session.get("username",None)
	category_id=request.GET.get("category_id")
	keywords=request.GET.get("keywords")
	if (str(keywords)=='None'):	
		keywords=None
	if (str(category_id)=='None'):
		category_id=None
	if (category_id):
		category_id=[int(category_id)]
		
	page=request.GET.get("page")
	if (page==None):
		page=1
	funpage = zz91page()
	limitNum=funpage.limitNum(20)
	nowpage=funpage.nowpage(int(page))
	frompageCount=funpage.frompageCount()
	after_range_num = funpage.after_range_num(2)
	before_range_num = funpage.before_range_num(9)
	
	pricelistall=getpricelist(keywords=keywords,frompageCount=frompageCount,limitNum=limitNum,category_id=category_id,allnum=100000)
	pricelist=pricelistall['list']
	pricelistcount=pricelistall['count']
	listcount=pricelistcount
	if (int(listcount)>100000):
		listcount=100000
	listcount = funpage.listcount(listcount)
	page_listcount=funpage.page_listcount()
	firstpage = funpage.firstpage()
	lastpage = funpage.lastpage()
	page_range  = funpage.page_range()
	nextpage = funpage.nextpage()
	prvpage = funpage.prvpage()
	return render_to_response('standard/price.html',locals())
def huzhu(request):
	username=request.session.get("username",None)
	company_id=request.session.get("company_id",None)
	category_id=request.GET.get("category_id")
	keywords=request.GET.get("keywords")
	if (str(keywords)=='None'):	
		keywords=None
	if (str(category_id)=='None'):
		category_id=None
	page=request.GET.get("page")
	if (page==None):
		page=1
	funpage = zz91page()
	limitNum=funpage.limitNum(20)
	nowpage=funpage.nowpage(int(page))
	frompageCount=funpage.frompageCount()
	after_range_num = funpage.after_range_num(2)
	before_range_num = funpage.before_range_num(9)
	
	bbslistall=getbbslist(keywords,frompageCount,limitNum,category_id)
	bbslist=bbslistall['list']
	bbslistcount=bbslistall['count']
	listcount=bbslistcount
	if (int(listcount)>100000):
		listcount=100000
	listcount = funpage.listcount(listcount)
	page_listcount=funpage.page_listcount()
	firstpage = funpage.firstpage()
	lastpage = funpage.lastpage()
	page_range  = funpage.page_range()
	nextpage = funpage.nextpage()
	prvpage = funpage.prvpage()
	return render_to_response('standard/huzhu.html',locals())

def productslist(request):
	username=request.session.get("username",None)
	page = request.GET.get("page")
	if (page == None or page=='' or page=="None"):
		page = 1
	nowsearcher="offersearch_new"
	keywords = request.GET.get("keywords")#搜索
	if (keywords==None):
		keywords=""
	searchname = urlquote(request.GET.get("searchname"))
	pdt_kind = request.GET.get("ptype")
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
	havepic = request.GET.get("havepic")
	
	
	
	#--------------------------------------------
	if (province=='' or province == None):
		province=''
		
	if (pdt_kind == '' or pdt_kind == None or pdt_kind=="0"):
		pdt_type=''
		pdt_kind='0'
		stab1="offerselect"
		stab2=""
		stab3=""
	if (pdt_kind =='1'):
		pdt_type='0'
		stab1=""
		stab2="offerselect"
		stab3=""
	if (pdt_kind=='2'):
		pdt_type='1'
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
	after_range_num = 2
	before_range_num = 9
	
	port = SPHINXCONFIG['port']
	cl = SphinxClient()
	cl.SetServer ( SPHINXCONFIG['serverid'], port )
	#----------------------------
	list = SphinxClient()
	list.SetServer ( SPHINXCONFIG['serverid'], port )
	
	cl.SetMatchMode ( SPH_MATCH_BOOLEAN )
	list.SetMatchMode ( SPH_MATCH_BOOLEAN )
	
	#取得总数
	nowdate=date.today()-timedelta(days=2)
	nextday=date.today()+timedelta(days=2)
	formatnowdate=time.mktime(nowdate.timetuple())
	formatnextday=time.mktime(nextday.timetuple())
	searstr=''
	
	if (pdt_kind !='0'):
		searstr+=";filter=pdt_kind,"+pdt_type
		cl.SetFilter('pdt_kind',[int(pdt_type)])
		list.SetFilter('pdt_kind',[int(pdt_type)])
		
	if(havepic=='1'):
		cl.SetFilterRange('havepic',1,100)
		list.SetFilterRange('havepic',1,100)
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
	rescount = cl.Query ( '@(title,label0,label1,label2,label3,label4,city,province,tags) '+keywords+provincestr+'','offersearch_new_vip')
	pcount=0
	listall=[]
	if rescount:
		if rescount.has_key('matches'):
			tagslist=rescount['matches']
			testcom_id=0
			pcount=0
			for match in tagslist:
				id=match['id']
				com_id=match['attrs']['company_id']
				viptype=match['attrs']['viptype']
				refresh_time=float(match['attrs']['refresh_time'])
				pdt_date=float(match['attrs']['pdt_date'])
				if (testcom_id==com_id):
					pcount+=1
				else:
					pcount=0
				list1=[id,pcount,viptype,refresh_time,pdt_date]
				#list1=list1+[viptype]
				#list1=list1+[refresh_time]
				listall.append(list1)
				testcom_id=com_id
	#根据轮回排序
	listallvip=sorted(listall, key=lambda d:d[1])
	
	#根据日期排序
	changeflag=0
	listallvip1=[]
	listallvip2=[]
	m=0
	for i in listallvip:
		m+=1
		if (changeflag==int(i[1])):
			list1=[i[0],i[1],i[2],i[3],i[4]]
			listallvip2.append(list1)
			if (len(listallvip)==m):
				listallvip1+=listallvip2
		else:
			listallvip2=sorted(listallvip2, key=lambda a:a[4],reverse=True)
			listallvip1+=listallvip2
			listallvip2=[]
			list1=[i[0],i[1],i[2],i[3],i[4]]
			listallvip2.append(list1)
			if (len(listallvip)==m):
				listallvip1+=listallvip2
		changeflag=int(i[1])
	listallvip=listallvip1
	
	#根据会员类型排序
	changeflag=0
	changeflag1=0
	listallvip1=[]
	listallvip2=[]
	m=0
	strchangeflag=''
	for i in listallvip:
		m+=1
		if ((changeflag==int(i[4]) and changeflag1==int(i[1])) or changeflag==0):
			list1=[i[0],i[1],i[2],i[3],i[4]]
			listallvip2.append(list1)
			#strchangeflag+='|'+str(changeflag)+'*'+str(int(i[4]))
			if (len(listallvip)==m):
				listallvip1+=listallvip2
		else:
			listallvip2=sorted(listallvip2, key=lambda a:a[2],reverse=True)
			listallvip1+=listallvip2
			listallvip2=[]
			list1=[i[0],i[1],i[2],i[3],i[4]]
			listallvip2.append(list1)
			if (len(listallvip)==m):
				listallvip1+=listallvip2
		changeflag=int(i[4])
		changeflag1=int(i[1])
	listallvip=listallvip1
	
	#根据发布时间排序
	changeflag=0
	changeflag1=0
	changeflag2=0
	listallvip1=[]
	listallvip2=[]
	m=0
	for i in listallvip:
		m+=1
		if ((changeflag==int(i[2]) and changeflag1==int(i[1]) and changeflag2==int(i[4])) or changeflag==0):
			list1=[i[0],i[1],i[2],i[3],i[4]]
			listallvip2.append(list1)
			if (len(listallvip)==m):
				listallvip1+=listallvip2
		else:
			listallvip2=sorted(listallvip2, key=lambda d:d[3],reverse=True)
			listallvip1+=listallvip2
			listallvip2=[]
			list1=[i[0],i[1],i[2],i[3],i[4]]
			listallvip2.append(list1)
			if (len(listallvip)==m):
				listallvip1+=listallvip2
		changeflag=int(i[2])
		changeflag1=int(i[1])
		changeflag2=int(i[4])
	listallvip=listallvip1
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
		list1=getcompinfo(match[0],cursor,keywords2)
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
	
	if (nowpage==pageNum and lastpNum!=0):
		listall=productList
	else:
		listall=[]
	if (notvip==1):
		list.SetLimits (offsetNum,limitNum,100000)
		res = list.Query ( '@(title,label0,label1,label2,label3,label4,city,province,tags) '+keywords+provincestr+'',nowsearcher)

		if res:
			if res.has_key('matches'):
				prodlist=res['matches']
				for list in prodlist:
					id=list['id']
					list1=getcompinfo(id,cursor,keywords2)
					listall.append(list1)
				productList=listall
				
	try:
		page = int(request.GET.get('page',1))
		if page < 1:
			page = 1
	except ValueError:
			page = 1
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
	
	if(page_listcount>500 and page>=500):
		arrtishi="提示：为了提供最相关的搜索结果，ZZ91再生网只显示500页信息，建议您重新搜索！"
	else:
		arrtishi=None
	return render_to_response('standard/productslist.html',locals())

#供求类别
def productscategory(request):
	username=request.session.get("username",None)
	cid=request.GET.get("cid")
	label=request.GET.get("label")
	if (cid==None):
		cid=''
	pclist=getproducstcategorylist(cid)
	if pclist:
		return render_to_response('standard/productscategory.html',locals())
	else:
		return HttpResponseRedirect("/standard/productslist/?keywords="+str(label)+"")
def provincecategory(request):
	username=request.session.get("username",None)
	keywords=request.GET.get("keywords")
	pstr="广东 | 浙江 | 江苏 | 山东 | 河北 | 河南 | 福建 | 辽宁 | 安徽 | 广西 | 山西 | 海南 | 内蒙古 | 吉林 | 黑龙江 | 湖北 | 湖南 | 江西 | 宁夏 | 新疆 | 青海 | 陕西 | 甘肃 | 四川 | 云南 | 贵州 | 西藏 | 台湾 | 香港 | 澳门 "
	pvalue=[]
	arrpstr=pstr.split("|")
	for a in arrpstr:
		l={'name':a.strip()}
		pvalue.append(l)
	
	pstr="深圳 | 广州 | 宁波 | 温州 | 苏州 | 佛山 | 杭州 | 中山 | 青岛 | 台州 | 无锡 | 厦门 | 郑州 | 汕头 | 成都 | 济南 | 南京 | 武汉 | 石家庄 | 福州 | 长沙 | 沈阳 | 西安 | 合肥 | 昆明 | 南宁 | 洛阳 | 乌鲁木齐 "
	pvalue1=[]
	arrpstr=pstr.split("|")
	for a in arrpstr:
		l={'name':a.strip()}
		pvalue1.append(l)
	
	return render_to_response('standard/provincecategory.html',locals())
#公司列表
def companylist(request):
	username=request.session.get("username",None)
	company_id=request.session.get("company_id",None)
	keywords=request.GET.get("keywords")
	province=request.GET.get("province")
	if (province==None or province==''):
		province=''
	if (keywords==None):
		keywords=''
	page=request.GET.get("page")
	if (page==None or page=='' or page==0):
		page=1
	funpage = zz91page()
	limitNum=funpage.limitNum(20)
	nowpage=funpage.nowpage(int(page))
	frompageCount=funpage.frompageCount()
	after_range_num = funpage.after_range_num(2)
	before_range_num = funpage.before_range_num(9)
	
	if (str(keywords)=='None'):	
		keywords=None
	companylistall=getcompanylist(keywords+' '+province,frompageCount,limitNum)
	if companylistall:
		companylist=companylistall['list']
		companylistcount=companylistall['count']
		listcount=companylistcount
		if (int(listcount)>100000):
			listcount=100000
		listcount = funpage.listcount(listcount)
		page_listcount=funpage.page_listcount()
		firstpage = funpage.firstpage()
		lastpage = funpage.lastpage()
		page_range  = funpage.page_range()
		nextpage = funpage.nextpage()
		prvpage = funpage.prvpage()
		
		if (companylistcount==1):
			morebutton='style=display:none'
		else:
			morebutton=''
	return render_to_response('standard/companylist.html',locals())

#公司供求列表
def companyproducts(request):
	keywords=request.GET.get("keywords")
	company_id=request.GET.get("company_id")
	page=request.GET.get("page")
	pdt_kind = request.GET.get("ptype")
	if (page==None):
		page=1
	funpage = zz91page()
	limitNum=funpage.limitNum(20)
	nowpage=funpage.nowpage(int(page))
	frompageCount=funpage.frompageCount()
	after_range_num = funpage.after_range_num(2)
	before_range_num = funpage.before_range_num(9)
	
	if (pdt_kind == '' or pdt_kind == None or pdt_kind=="0"):
		pdt_type=''
		pdt_kind='0'
		stab1="offerselect"
		stab2=""
		stab3=""
	if (pdt_kind =='1'):
		pdt_type='0'
		stab1=""
		stab2="offerselect"
		stab3=""
	if (pdt_kind=='2'):
		pdt_type='1'
		stab1=""
		stab2=""
		stab3="offerselect"
	
	if (str(keywords)=='None'):	
		keywords=None
	listall=getcompanyproductslist(keywords,frompageCount,limitNum,company_id,pdt_type)
	productslist=listall['list']
	productslistcount=listall['count']
	listcount=productslistcount
	if (int(listcount)>100000):
		listcount=100000
	listcount = funpage.listcount(listcount)
	page_listcount=funpage.page_listcount()
	firstpage = funpage.firstpage()
	lastpage = funpage.lastpage()
	page_range  = funpage.page_range()
	nextpage = funpage.nextpage()
	prvpage = funpage.prvpage()
	
	if (productslistcount==1):
		morebutton='style=display:none'
	else:
		morebutton=''
	return render_to_response('standard/companyofferlist.html',locals())
#供求和公司搜索
def searchindex(request):
	offer=request.GET.get("offer")
	company=request.GET.get("company")
	keywords=request.GET.get("keywords")
	if offer:
		return HttpResponseRedirect("/standard/productslist/?keywords="+str(keywords)+"")
	if company:
		return HttpResponseRedirect("/standard/companylist/?keywords="+str(keywords)+"")
	
#供求详细页
def productdetail(request):
	username=request.session.get("username",None)
	membercheck=request.session.get("membercheck",None)
	pdtid=request.GET.get("pdtid")
	list=getproductdetail(pdtid)
	products_type_code=list['products_type_code']
	urlimages=list['piclist']
	if urlimages:
		urlimages=urlimages[0]['images']
	backurl=request.META.get('HTTP_REFERER','/')
	return render_to_response('standard/productdetail.html',locals())
def companyinfo(request):
	username=request.session.get("username",None)
	company_id=request.GET.get("company_id")
	membercheck=request.session.get("membercheck",None)
	pdtid=request.GET.get("pdtid")
	list=getcompanydetail(company_id)
	backurl=request.META.get('HTTP_REFERER','/')
	return render_to_response('standard/companyinfo.html',locals())
#公司详细页
def companydetail(request):
	username=request.session.get("username",None)
	company_id=request.GET.get("company_id")
	membercheck=request.session.get("membercheck",None)
	pdtid=request.GET.get("pdtid")
	#list=getproductdetail(pdtid)
	list=getcompanydetail(company_id)
	backurl=request.META.get('HTTP_REFERER','/')
	return render_to_response('standard/companydetail.html',locals())
