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
import urllib
import json
from xml.etree import ElementTree as ET
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
from dict2xml import dict2xml
from sphinxapi import *
from zz91page import *
from zz91db_ast import companydb
from zz91db_2_news import newsdb
from zz91db_ads import adsdb
from zz91db_ep import adshuanbao
from settings import spconfig,weixinconfig
from zz91tools import date_to_int,date_to_strall,str_to_int
from zzwx.client import Client
import top.api
#from jobjoke import luckcheck
dbc=companydb()
dbn=newsdb()
dbads=adsdb()
#dbhuanbao=adshuanbao()

reload(sys)
sys.setdefaultencoding('UTF-8')
nowpath=os.path.dirname(__file__)
execfile(nowpath+"/commfunction.py")
execfile(nowpath+"/function.py")
execfile(nowpath+"/func/ldb_weixin_function.py")
execfile(nowpath+"/func/qianbao_function.py")

zzq=qianbao()
#----微信端最新商机
def order(request):
	#host = request.META.get('HTTP_REFERER','..')
	username=request.session.get("username",None)
	#username=request.COOKIES.get("username",None)
	#company_id=request.COOKIES.get('company_id',None)
	companylist1=getindexcompanylist_pic(keywords="金属",num=4,allnum=4)
	companylist2=getindexcompanylist_pic(keywords="塑料",num=4,allnum=4)
	companylist3=getindexcompanylist_pic(keywords="纺织品|废纸|二手设备|电子电器|橡胶|轮胎|服务",num=4,allnum=4)
	return render_to_response('new/order.html',locals())
#----微信供求商机搜索
def tradesearch(request):
	username=request.session.get("username",None)
	#username=request.COOKIES.get("username",None)
	#company_id=request.COOKIES.get('company_id',None)
	ccountall=getsyproductslist(None,0,1,None,1)["count"]
	return render_to_response('new/tradesearch.html',locals())
#优质客户类别
def categoryindex(request):
	categorylist=getordercategorylistmain(code="1019")
	return render_to_response('zz91weixin/categoryindex.html',locals())
def categorylist(request,code):
	categoryname=getdata_index_categorylabel(code)
	categorylist=getordercategorylist(code)
	return render_to_response('zz91weixin/category.html',locals())
#----微信行情搜索
def pricesearch(request):
	username=request.session.get("username",None)
	#username=request.COOKIES.get("username",None)
	#company_id=request.COOKIES.get('company_id',None)
	ccountall=getpricelist(frompageCount=0,limitNum=1,allnum=1)["count"]
	return render_to_response('new/pricesearch.html',locals())
#----微信端注册
def reg(request):
	weixinid= request.GET.get("weixinid")
	if (weixinid!=""):
		request.session['weixinid']=weixinid
	return render_to_response('new/reg.html',locals())

#微信报名
def baoming(request):
	webtitle="2017年度再生塑料“金牌采购商”& “金牌供应商”评选报名"
	return render_to_response('new/baoming.html',locals())
#----微信端登录
def login(request):
	username=request.session.get("username",None)
	ldb_weixin=ldbweixin()
	weixinid=request.GET.get("weixinid")
	qrcode=request.GET.get("qrcode")
	tourl=request.GET.get("tourl")
	if (weixinid!=""):
		request.session['weixinid']=weixinid
	return render_to_response('new/login.html',locals())
#再生汇微信
def getzsh(request):
	token = "zaishenghui"
	params = request.GET
	args = [token, params['timestamp'], params['nonce']]
	args.sort()
	if hashlib.sha1("".join(args)).hexdigest() == params['signature']:
		if params.has_key('echostr'):
			return HttpResponse(params['echostr'])
		else:
			if request.body:
				xml = ET.fromstring(request.body)
				fromUserName = xml.find("ToUserName").text
				toUserName = xml.find("FromUserName").text
				MsgType = xml.find("MsgType").text
				Event1=None
				content=None
				EventKey=""
				#request.session.set_expiry(60*60)
				request.session['weixinid']=toUserName
				if (MsgType=="event"):
					Event1 = xml.find("Event").text
					EventKey = xml.find("EventKey").text
				if (MsgType=="text"):
					content = xml.find("Content").text
				if (MsgType=="image"):
					PicUrl = xml.find("PicUrl").text
				if EventKey==None:
					keyw=Event1
				else:
					keyw=EventKey
				#记录日志
				
				postTime = str(int(time.time()))
				
				if (Event1 == "subscribe" or Event1 == "scan"):
					title="您好！感谢关注再生汇"
					xml=backxml(xmltype=2,fromUserName=toUserName,toUserName=fromUserName,title=title)
					return HttpResponse(xml)
				else:
					title=content
					
				if (content==None  and EventKey=='qiandao'):
					tpurl="http://m.zz91.com/wechat/auth_login.html?tourl=/zsh/index.html?clientid="+str(toUserName)+""
					titlelist=[{'title':'2017废纸产业发展论坛现场签到','Description':'点此签到','PicUrl':'http://m.zz91.com/zt/feizhiluntanH5/images/weixin_qiandao.jpg','Url':tpurl}]
					ArticleCount=len(titlelist)
					xml=backxml(xmltype=3,fromUserName=toUserName,toUserName=fromUserName,ArticleCount=ArticleCount,titlelist=titlelist)
					return HttpResponse(xml)
				else:
					return HttpResponse("Invalid Request")
	else:
		return HttpResponse("Invalid Request")
#----zz91微信
def doget(request):
	try:
		return getweixin(request)
	except Exception as e:
		return HttpResponse(e)
#---来电宝微信
def ldbdoget(request):
	token = "ldbweixin"
	params = request.GET
	args = [token, params['timestamp'], params['nonce']]
	args.sort()
	if hashlib.sha1("".join(args)).hexdigest() == params['signature']:
		if params.has_key('echostr'):
			return HttpResponse(params['echostr'])
		else:
			if request.raw_post_data:
				xml = ET.fromstring(request.raw_post_data)
				fromUserName = xml.find("ToUserName").text
				toUserName = xml.find("FromUserName").text
				MsgType = xml.find("MsgType").text
				Event1=None
				content=None
				EventKey=""
				if (MsgType=="event"):
					Event1 = xml.find("Event").text
					EventKey = xml.find("EventKey").text
				if (MsgType=="text"):
					content = xml.find("Content").text
				if (MsgType=="image"):
					PicUrl = xml.find("PicUrl").text
				if EventKey==None:
					keyw=Event1
				else:
					keyw=EventKey
				#记录日志
				useragent=str(request.META.get('HTTP_USER_AGENT',None)).encode('utf8','ignore').encode("hex")
				saveweixincount(request,toUserName,content,keyw,useragent)
				
				postTime = str(int(time.time()))
				if (content==None  and EventKey=='binding'):
					bd=weixinbinding(toUserName)
					if bd:
						title="您已经绑定了ZZ91再生网来电宝！请选择菜单进行操作！" 
					else:
						title="感谢关注ZZ91再生网来电宝,从今儿起，您可以在微信上查询“来电宝”话单详单，余额查询，在线充值等业务了啦!\n\n 请先 <a href='http://m.zz91.com/weixin/login.html?weixinid="+str(toUserName)+"'>点击绑定ZZ91再生网帐号</a>\n\n <a href='http://m.zz91.com/register/?weixinid="+str(toUserName)+"'>木有帐号？用3秒钟注册一个</a>"
					xml=backxml(xmltype=2,fromUserName=toUserName,toUserName=fromUserName,title=title)
					return HttpResponse(xml)
				
				if (Event1 == "subscribe" or Event1 == "scan"):
					title="感谢关注ZZ91再生网来电宝,从今儿起，您可以在微信上查询“来电宝”话单详单，余额查询，在线充值等业务了啦!\n\n 请先 <a href='http://m.zz91.com/weixin/login.html?weixinid="+str(toUserName)+"'>点击绑定ZZ91再生网帐号</a>\n\n <a href='http://m.zz91.com/register/?weixinid="+str(toUserName)+"'>木有帐号？用3秒钟注册一个</a>"
					xml=backxml(xmltype=2,fromUserName=toUserName,toUserName=fromUserName,title=title)
					return HttpResponse(xml)
				else:
					title=content
					
				

				if (content==None  and EventKey=='fenxi'):
					bd=weixinbinding(toUserName)
					if not bd:
						title="您还未绑定来电宝帐号\n\n请先 <a href='http://m.zz91.com/weixin/login.html?weixinid="+str(toUserName)+"'>点击绑定来电宝帐号</a>\n\n"
					else:
						ldb_weixin=ldbweixin()
						company_id=getcompanyid(bd)
						phone400=ldb_weixin.getcompany400(company_id)
						if not phone400:
							title="您还未开通来电宝服务\n <a href='http://m.zz91.com/ldb_weixin/balance.html'>点此充值立即开通服务</a>"
						else:
							
							area_custom=ldb_weixin.getarea_custom2(company_id)
							time_custom=ldb_weixin.gettime_custom2(company_id)
							nowmonthstate=ldb_weixin.getnowmonthstate(company_id)
							fenxistr=area_custom+"的客户对您的产品最感兴趣\n"
							fenxistr+=time_custom+"时间为来电高峰\n"
							fenxistr+=nowmonthstate+"接听率"
							title=fenxistr
					xml=backxml(xmltype=2,fromUserName=toUserName,toUserName=fromUserName,title=title)
					return HttpResponse(xml)
				else:
					return HttpResponse("Invalid Request")
	else:
		return HttpResponse("Invalid Request")
def weixintest(request):
	fromUserName="aa"
	toUserName="oO7y2jvuaFhEq4ofNMEVDaAJNuK8"
	bd=weixinbinding(toUserName)
	if str(bd)=="None":
		title="您还未绑定来电宝帐号\n\n请先 <a href='http://m.zz91.com/weixin/login.html?weixinid="+str(toUserName)+"'>点击绑定来电宝帐号</a>\n\n"
	else:
		company_id=getcompanyid(bd)
		title=str(company_id)
	xml=backxml(xmltype=2,fromUserName=toUserName,toUserName=fromUserName,title=title)
	return HttpResponse(xml)
#记录日志
def saveweixincount(request,weixinid,keywords,keyw,useragent):
	gmt_created=datetime.datetime.now()
	localip=request.META.get('REMOTE_HOST',None)
	sql="insert into weixin_count(weixinid,keywords,keyw,useragent,ip,gmt_created) values(%s,%s,%s,%s,%s,%s)"
	dbc.updatetodb(sql,[weixinid,str(keywords),str(keyw),useragent,localip,gmt_created])
	sql="select id from weixin_live where weixinid=%s"
	result=dbc.fetchonedb(sql,[weixinid])
	if not result:
		sql="insert into weixin_live(weixinid,livetime) values(%s,%s)"
		dbc.updatetodb(sql,[weixinid,gmt_created])
	else:
		sql="update weixin_live set livetime=%s where id=%s"
		dbc.updatetodb(sql,[gmt_created,result[0]])
def getweixin(request):
	
	token = "zz91com"
	params = request.GET
	args = [token, params['timestamp'], params['nonce']]
	args.sort()
	if hashlib.sha1("".join(args)).hexdigest() == params['signature']:
		if params.has_key('echostr'):
			return HttpResponse(params['echostr'])
		else:
			if request.body:
				xml = ET.fromstring(request.body)
				fromUserName = xml.find("ToUserName").text
				toUserName = xml.find("FromUserName").text
				MsgType = xml.find("MsgType").text
				Event1=None
				content=None
				EventKey=""
				#request.session.set_expiry(60*60)
				request.session['weixinid']=toUserName
				if (MsgType=="event"):
					Event1 = xml.find("Event").text
					EventKey = xml.find("EventKey").text
				if (MsgType=="text"):
					content = xml.find("Content").text
				if (MsgType=="image"):
					PicUrl = xml.find("PicUrl").text
				if EventKey==None:
					keyw=Event1
				else:
					keyw=EventKey
				#记录日志
				directUrl="http://m.zz91.com/wechat/auth_login.html?clientid="+str(toUserName)
				useragent=str(request.META.get('HTTP_USER_AGENT',None)).encode('utf8','ignore').encode("hex")
				#useragent=str(request.META.get('HTTP_COOKIE'))
				saveweixincount(request,toUserName,content,keyw,EventKey)
				
				if (Event1 == "subscribe" or Event1 == "SCAN"):
					try:
						subscribewelcome(toUserName)
						tpurl="http://m.zz91.com/wechat/auth_login.html?clientid="+str(toUserName)+"&tourl=/vote/621/"
						titlelist=[{'title':'2017金牌供应商&采购商评选活动!','Description':'微信投票时间 2017.5.25-6.9','PicUrl':'http://img0.zz91.com/subject/621fenghuiH5/images/vote900x500.png','Url':tpurl}]
						ArticleCount=len(titlelist)
						xml=backxml(xmltype=3,fromUserName=toUserName,toUserName=fromUserName,ArticleCount=ArticleCount,titlelist=titlelist)
						#return HttpResponse(xml)
					except Exception , e:
						sql="insert into err_log (content) values(%s)"
						dbc.updatetodb(sql,[e])
						title="很抱歉，网络忙！你可以点击其他菜单试试！"
						title+='====================\r\n'
						title+='更多资源下载ZZ91再生网App客户端  <a href="http://m.zz91.com/app.html">点此下载</a>\r\n'
						xml=backxml(xmltype=2,fromUserName=toUserName,toUserName=fromUserName,title=title)
						return HttpResponse(xml)
				postTime = str(int(time.time()))
				
				
				if (content==None  and EventKey=='qiandao'):
					waccount=weixinbinding(toUserName)
					if waccount:
						gmt_created=datetime.datetime.now()
						wxqd=zzq.wxqiandao(waccount,toUserName)
						company_id=getcompanyid(waccount)
						dakacount=zzq.wxqiandaocount(waccount)
						qianbaoblance=zzq.getqianbaoblance(company_id)
						if (wxqd==0):
							#送1元再生钱包
							zzq.getsendfee(company_id,"1","45",more=1)
							if dakacount<7:
								title="恭喜您，打卡成功\r\n!您已获得1元再生钱包。继续打卡“"+str((7-dakacount))+"”天,您即可获得 10 元再生钱包,目前你的钱包余额为："+str(qianbaoblance)+"元"
							if dakacount==7:
								title="恭喜您，打卡成功\r\n!您已获得1元再生钱包。您已连续打卡 7 天，赠送给您10元钱包，<a href='http://m.zz91.com/weixin/getqianbao.html?weixinid="+str(toUserName)+"&gettype=7day'>点此领取</a>，领取签到数即清零，未领取将累加入连续打卡3周送“供求自动刷新”一个月服务，继续加油哦。"
							if dakacount>7:
								title="恭喜您，打卡成功\r\n!您已获得1元再生钱包。继续打卡“"+str((21-dakacount))+"”天,您即可获得 “供求自动刷新”一个月服务,目前你的钱包余额为："+str(qianbaoblance)+"元"
							if dakacount>=21:
								title="恭喜您，打卡成功\r\n!您已获得1元再生钱包。您已连续打卡 3周，赠送获得 “供求自动刷新”一个月服务。<a href='http://m.zz91.com/weixin/getqianbao.html?weixinid="+str(toUserName)+"&gettype=21day'>点此领取</a>，领取签到数即清零，继续打卡获取更多服务,目前你的钱包余额为："+str(qianbaoblance)+"元"
							xml=backxml(xmltype=2,fromUserName=toUserName,toUserName=fromUserName,title=title)
						if (wxqd==1):
							if dakacount<7:
								title="今天您已经打过卡了。继续打卡“"+str((7-dakacount))+"”天,您即可获得 10 元再生钱包,目前你的钱包余额为："+str(qianbaoblance)+"元"
							if dakacount==7:
								title="今天您已经打过卡了。您已连续打卡 7 天，赠送给您10元钱包，<a href='http://m.zz91.com/weixin/getqianbao.html?weixinid="+str(toUserName)+"&gettype=7day'>点此领取</a>，领取签到数即清零，未领取将累加入连续打卡3周送“供求自动刷新”一个月服务，继续加油哦。"
							if dakacount>7:
								title="今天您已经打过卡了。继续打卡“"+str((21-dakacount))+"”天,您即可获得 “供求自动刷新”一个月服务,目前你的钱包余额为："+str(qianbaoblance)+"元"
							if dakacount>=21:
								title="今天您已经打过卡了。您已连续打卡 3周，赠送获得 “供求自动刷新”一个月服务。<a href='http://m.zz91.com/weixin/getqianbao.html?weixinid="+str(toUserName)+"&gettype=21day'>点此领取</a>，领取签到数即清零，继续打卡获取更多服务,目前你的钱包余额为："+str(qianbaoblance)+"元"
							xml=backxml(xmltype=2,fromUserName=toUserName,toUserName=fromUserName,title=title)
					else:
						title="您还未绑定您的ZZ91再生网帐号，<a href='http://m.zz91.com/weixin/login.html?weixinid="+str(toUserName)+"'>点此立即绑定</a>\r\n。"
						title+="未注册,<a href='http://m.zz91.com/register/?weixinid='"+str(toUserName)+"'>3秒钟注册账号</a>"
						xml=backxml(xmltype=2,fromUserName=toUserName,toUserName=fromUserName,title=title)
					return HttpResponse(xml)
				if (content==None  and EventKey=='pay'):
					title="支付方式\n\nZZ91支付宝帐号：zhifu@zz91.com\n\n开户银行：中国农业银行杭州朝晖支行\n收 款 人：杭州阿思拓信息科技有限公司\n帐　　号：19-0156 0104 0013 383\n\n公司地址：浙江省杭州市江干区九盛路9号东方电子商务园13栋\n\n邮编：310019 \n\n传真：0571-56637777\n"
					xml=backxml(xmltype=2,fromUserName=toUserName,toUserName=fromUserName,title=title)
					return HttpResponse(xml)
				if (content==None  and EventKey=='help'):
					title="使用帮助：\n"
					#title+="ZZ91微信号升级了!\n"
					title+="===================\n"
					title+="除了菜单外\n"
					title+="您还可以：\n"
					title+="查看报价：\n回复：地区+产品+报价 \n如：上海废铝报价、国内PP报价\n"
					title+="查看供求：\n回复：供求+产品名称 \n如：求购PP、供应废铁\n"
					#title+="查看“企业库”，\n回复：企业\n"
					title+="查看再生网“联系方式”，\n回复：联系\n"
					title+="查看再生网“支付方式”，\n回复：支付\n"
					title+='====================\r\n'
					title+='更多资源下载ZZ91再生网App客户端  <a href="http://m.zz91.com/app.html">点此下载</a>\r\n'
					#title+="“AQSIQ咨询”，\n回复：aqsiq\n"
					xml=backxml(xmltype=2,fromUserName=toUserName,toUserName=fromUserName,title=title)
					return HttpResponse(xml)
				
				if (content==None  and EventKey=='forgetpasswd'):
					title="您正在取回密码\n\n<a href='http://m.zz91.com/weixin/forgetpasswd.html?weixinid="+str(toUserName)+"'>点此获得您的密码</a>\n\n或拨打服务电话\n\n0571-56611111\n0571-56612345\n"
					xml=backxml(xmltype=2,fromUserName=toUserName,toUserName=fromUserName,title=title)
					return HttpResponse(xml)
				if (content==None  and EventKey=='tpyzm'):
					randomnum = random.randint(100, 999)
					gmt_modified=datetime.datetime.now()
					weixinid=toUserName
					checked=0
					sqlw="select id,TIMESTAMPDIFF(SECOND,gmt_modified,NOW()) from vote_yzm where weixinid=%s"
					result=dbc.fetchonedb(sqlw,[weixinid])
					if not result:
						sqla="insert into vote_yzm(weixinid,randomnum,checked,gmt_modified) values(%s,%s,%s,%s)"
						dbc.updatetodb(sqla,[weixinid,randomnum,checked,gmt_modified])
					else:
						wid=result[0]
						sleanum=result[1]
						sqlb="update vote_yzm set gmt_modified=%s,randomnum=%s,checked=0 where id=%s"
						dbc.updatetodb(sqlb,[gmt_modified,randomnum,wid])
					title="投票验证码："+str(randomnum)+"，十分钟后过期。"
					xml=backxml(xmltype=2,fromUserName=toUserName,toUserName=fromUserName,title=title)
					return HttpResponse(xml)
					#sendweixinmsg(weixinid,"投票验证码："+str(randomnum)+"，十分钟后过期。")
				if (content==None  and EventKey=='toupiao'):
					tpurl="http://m.zz91.com/wechat/auth_login.html?clientid="+str(toUserName)+"&tourl=/vote/v2017823feizhi/list.html"
					titlelist=[{'title':'2017废纸产业发展论坛-废纸行业TOP10评选微信投票！','Description':'谁是真正的行业精英？你来决定！','PicUrl':'http://m.zz91.com/zt/feizhiluntanH5/images/weixin_feizhilogo.png','Url':tpurl}]
					ArticleCount=len(titlelist)
					xml=backxml(xmltype=3,fromUserName=toUserName,toUserName=fromUserName,ArticleCount=ArticleCount,titlelist=titlelist)
					return HttpResponse(xml)
				if (content==None  and EventKey=='binding'):
					waccount=weixinbinding(toUserName)
					if waccount:
						title="您已经绑定了账号（用户名："+waccount+"），是否为您的账号，如果不是，请<a href='http://m.zz91.com/weixin/login.html?weixinid="+str(toUserName)+"'>点击重新绑定ZZ91再生网帐号</a>"
						xml=backxml(xmltype=2,fromUserName=toUserName,toUserName=fromUserName,title=title)
						return HttpResponse(xml)
					
						gmt_created=datetime.datetime.now()
						morpic="http://img0.zz91.com/zz91/weixin/images/more.jpg"
						titlelist=[{'title':'第16届中国塑料交易会 10.12-15,台州,招商电话：0571-56612345','Description':'招商电话：0571-56612345 56611111','PicUrl':'http://img1.zz91.com/ads/1467302400000/f4e6faa4-1566-4cc6-b731-53e1ad6418ca.jpg','Url':'http://zhanhui.zz91.com/exhibitchannel/taizhou/index.htm'}]
						#titlelist=[]
						wcompany_id=getcompanyid(waccount)
						qcout=getleavewordscount(wcompany_id)
						hcount=getmyhuzhureplaycoutno(waccount)
						if not hcount:
							hcount="0"
						
						tlist={'title':'我的收藏','Description':'','PicUrl':'http://m.zz91.com/images/qianbao/sc.png','Url':'http://m.zz91.com/myrc_favorite/?weixinid='+toUserName+''}
						titlelist.append(tlist)
						tlist={'title':'发布供求','Description':'','PicUrl':'http://app.zz91.com/images/post.png','Url':'http://m.zz91.com/products_publish/?weixinid='+toUserName+''}
						titlelist.append(tlist)
						tlist={'title':'我的供求','Description':'','PicUrl':'http://m.zz91.com/images/qianbao/gq.png','Url':'http://m.zz91.com/myrc_products/?weixinid='+toUserName+''}
						titlelist.append(tlist)
						tlist={'title':'我的询盘('+str(qcout)+')','Description':'','PicUrl':'http://m.zz91.com/images/qianbao/xp.png','Url':'http://m.zz91.com/myrc_leavewords/?weixinid='+toUserName+''}
						titlelist.append(tlist)
						tlist={'title':'我的社区('+str(hcount)+')','Description':'','PicUrl':'http://m.zz91.com/images/qianbao/sq.png','Url':'http://m.zz91.com/myrc_mycommunity/?weixinid='+toUserName+''}
						titlelist.append(tlist)
						tlist={'title':'我的供求','Description':'','PicUrl':'http://m.zz91.com/images/qianbao/gq.png','Url':'http://m.zz91.com/myrc_products/?weixinid='+toUserName+''}
						titlelist.append(tlist)
						#tlist={'title':'定制的供求商机','Description':'','PicUrl':'http://m.zz91.com/images/qianbao/sj.png','Url':'http://m.zz91.com/myrc_collect/?weixinid='+toUserName+''}
						#titlelist.append(tlist)
						#tlist={'title':'定制的行情报价','Description':'','PicUrl':'http://m.zz91.com/images/qianbao/dz.png','Url':'http://m.zz91.com/myrc_collectprice/?weixinid='+toUserName+''}
						#titlelist.append(tlist)
						tlist={'title':'再生钱包','Description':'','PicUrl':'http://m.zz91.com/images/qianbao/zs.png','Url':'http://m.zz91.com/qianbao/?weixinid='+toUserName+''}
						titlelist.append(tlist)
						tlist={'title':'修改我的资料','Description':'','PicUrl':'http://m.zz91.com/images/qianbao/3.png','Url':'http://m.zz91.com/myrc/info.html?weixinid='+toUserName+''}
						titlelist.append(tlist)
						
						ArticleCount=len(titlelist)
						xml=backxml(xmltype=3,fromUserName=toUserName,toUserName=fromUserName,ArticleCount=ArticleCount,titlelist=titlelist)
						return HttpResponse(xml)
					else:
						title="您还未绑定您的ZZ91再生网帐号，<a href='http://m.zz91.com/weixin/login.html?weixinid="+str(toUserName)+"'>点击绑定ZZ91再生网帐号</a>\r\n。"
						title+="未注册,<a href='http://m.zz91.com/register/?weixinid='"+str(toUserName)+"'>3秒钟注册账号</a>"
						xml=backxml(xmltype=2,fromUserName=toUserName,toUserName=fromUserName,title=title)
						return HttpResponse(xml)
						titlelist=[{'title':'第16届中国塑料交易会 10.12-15,台州,招商电话：0571-56612345','Description':'招商电话：0571-56612345 56611111','PicUrl':'http://img1.zz91.com/ads/1467302400000/f4e6faa4-1566-4cc6-b731-53e1ad6418ca.jpg','Url':'http://zhanhui.zz91.com/exhibitchannel/taizhou/index.htm'}]
						tlist={'title':'绑定ZZ91再生网账号','Description':'','PicUrl':'','Url':'http://m.zz91.com/weixin/login.html?weixinid='+str(toUserName)}
						titlelist.append(tlist)
						tlist={'title':'3秒钟注册账号','Description':'','PicUrl':'','Url':'http://m.zz91.com/register/?weixinid='+str(toUserName)}
						titlelist.append(tlist)
						ArticleCount=len(titlelist)
						xml=backxml(xmltype=3,fromUserName=toUserName,toUserName=fromUserName,ArticleCount=ArticleCount,titlelist=titlelist)
						return HttpResponse(xml)
						
				if (content==None  and "shuang11" in EventKey):
					titlelist=[{'title':'双11，呼朋唤友来砍价，“零”元价格到','Description':'先到先得，活动名额有限！','PicUrl':'http://m.zz91.com/subject/kanjia/images/222.jpg','Url':'http://m.zz91.com/kanjia/index.html?weixinid='+str(toUserName)+'&d=1'}]
					ArticleCount=len(titlelist)
					xml=backxml(xmltype=3,fromUserName=toUserName,toUserName=fromUserName,ArticleCount=ArticleCount,titlelist=titlelist)
					return HttpResponse(xml)
				if (Event1 == "subscribe"):
					try:
						subscribewelcome(toUserName)
						if not EventKey:
							weixinorder(toUserName)
							title="随时随地为您提供最新商机！点击以上马上订阅吧！"
							xml=backxml(xmltype=2,fromUserName=toUserName,toUserName=fromUserName,title=title)
							return HttpResponse(xml)
					except Exception , e:
						sql="insert into err_log (content) values(%s)"
						dbc.updatetodb(sql,[e])
						title="很抱歉，网络忙！你可以点击其他菜单试试！"
						title+='====================\r\n'
						title+='更多资源下载ZZ91再生网App客户端  <a href="http://m.zz91.com/app.html">点此下载</a>\r\n'
						xml=backxml(xmltype=2,fromUserName=toUserName,toUserName=fromUserName,title=title)
						return HttpResponse(xml)
				if (content==None  and "orderprice" in EventKey):
					#提醒定制商机
					weixinorder(toUserName)
					#Url="http://m.zz91.com/wechat/auth_login.html?clientid="+str(toUserName)
					#title="商机订阅！\n <a href='"+Url+"&tourl=/order/price.html'>行情订阅。点此 </a>\n <a href='"+Url+"&tourl=/order/business.html'>供求订阅。点此</a>"
					title="随时随地为您提供最新商机！点击以上马上订阅吧！"
					xml=backxml(xmltype=2,fromUserName=toUserName,toUserName=fromUserName,title=title)
					return HttpResponse(xml)
				if (content==None  and "tradesee" in EventKey):
					#提醒定制商机
					weixinorder(toUserName)
					#Url="http://m.zz91.com/wechat/auth_login.html?clientid="+str(toUserName)
					#title="商机订阅！\n <a href='"+Url+"&tourl=/order/price.html'>行情订阅。点此 </a>\n <a href='"+Url+"&tourl=/order/business.html'>供求订阅。点此</a>"
					title="随时随地为您提供最新商机！点击以上马上订阅吧！"
					xml=backxml(xmltype=2,fromUserName=toUserName,toUserName=fromUserName,title=title)
					return HttpResponse(xml)
				
				if (Event1 == "subscribe" or Event1 == "SCAN"):
					#--微信扫描登录
					try:
						if EventKey:
							title=""
							EventKey=EventKey.lower().replace("qrscene_", "")
							if EventKey:
								#tmp = random.randint(1000000, 99999999)
								qrcode=EventKey
								gmt_created=datetime.datetime.now()
								open_type="weixin.qq.com"
								target_account="0"
								value=[toUserName,open_type,target_account,qrcode,gmt_created,gmt_created]
								sql="select id,target_account from oauth_access where open_id=%s and open_type=%s and closeflag=0"
								result=dbc.fetchonedb(sql,[toUserName,open_type])
								if not result:
									#判断是否在登录的情况下扫描关注
									sqlb="select id,account from weixin_pclogin where qrcode=%s and TIMESTAMPDIFF(MINUTE,gmt_created,now())<11 and loginflag=2"
									resultc=dbc.fetchonedb(sqlb,[str(qrcode)])
									if resultc:
										target_account=resultc[1]
										if target_account and  str(target_account)!="0":
											sql="update weixin_pclogin set openid=%s where id=%s"
											dbc.updatetodb(sql,[toUserName,resultc[0]])
											value=[toUserName,open_type,target_account,str(qrcode),gmt_created,gmt_created]
											sqlp="insert into oauth_access(open_id,open_type,target_account,code,gmt_created,gmt_modified) values(%s,%s,%s,%s,%s,%s)"
											dbc.updatetodb(sqlp,value)
											title="您已经绑定成功！"
									else:
										title="您还未绑定ZZ91再生网账号，请先 <a href='http://m.zz91.com/weixin/login.html?weixinid="+str(toUserName)+"&qrcode="+str(qrcode)+"'>点击绑定ZZ91再生网帐号</a>！绑定ZZ91账号，实时接收用户留言，第一时间获取最新行情和商机！"
								else:
									sqlp="update oauth_access set code=%s,gmt_modified=%s where id=%s"
									dbc.updatetodb(sqlp,[qrcode,gmt_created,result[0]])
									account=result[1]
									oid=result[0]
									if not account or str(account)=="0":
										#判断是否在登录的情况下扫描关注
										sqlb="select id,account from weixin_pclogin where qrcode=%s and TIMESTAMPDIFF(MINUTE,gmt_created,now())<11 and loginflag=2"
										resultc=dbc.fetchonedb(sqlb,[str(qrcode)])
										if resultc:
											sql="update weixin_pclogin set openid=%s where id=%s"
											dbc.updatetodb(sql,[toUserName,resultc[0]])
											target_account=resultc[1]
											if target_account and target_account!='None':
												sql="update oauth_access set target_account=%s,gmt_modified=%s where id=%s"
												dbc.updatetodb(sql,[target_account,gmt_created,oid])
											title="您已经绑定成功！"
										else:
											title="您还未绑定ZZ91再生网账号，请先 <a href='http://m.zz91.com/weixin/login.html?weixinid="+str(toUserName)+"&qrcode="+str(qrcode)+"'>点击绑定ZZ91再生网帐号</a>！绑定ZZ91账号，实时接收用户留言，第一时间获取最新行情和商机！"
									else:
										#判断是否在登录的情况下扫描关注
										sqlb="select id,loginflag,gmt_created from weixin_pclogin where qrcode=%s and TIMESTAMPDIFF(MINUTE,gmt_created,now())<11 and loginflag=2"
										resultc=dbc.fetchonedb(sqlb,[str(qrcode)])
										if resultc:
											gmttime=resultc[2]
											gmtnow=getNow()
											difmin=date_to_int(gmtnow)-date_to_int(gmttime)
											sql="update weixin_pclogin set openid=%s where id=%s"
											dbc.updatetodb(sql,[toUserName,resultc[0]])
											title='微信认证完毕，您已经绑定成功！'
										else:
											#pc端登录扫描
											sqlb="select id,loginflag,gmt_created from weixin_pclogin where qrcode=%s"
											resultc=dbc.fetchonedb(sqlb,[str(qrcode)])
											if resultc:
												loginflag=resultc[1]
												gmttime=resultc[2]
												gmtnow=getNow()
												difmin=date_to_int(gmtnow)-date_to_int(gmttime)
												if difmin>600:
													title='微信已过期，请刷新二维码，重新扫描！'
												else:
													if loginflag==0:
														sqlp="update weixin_pclogin set loginflag=1 where id=%s"
														dbc.updatetodb(sqlp,[resultc[0]])
														title='微信认证完毕，电脑端将自动登录，请点击PC端"点此进入生意管家"！'
													if loginflag==2:
														sql="update weixin_pclogin set openid=%s where id=%s"
														dbc.updatetodb(sql,[toUserName,resultc[0]])
														title='微信认证完毕，您已经绑定成功！'
											else:
												#pc端登录扫描
												#sqlp="insert into weixin_pclogin (openid,account,loginflag,gmt_created,qrcode) values(%s,%s,%s,%s,%s)"
												#dbc.updatetodb(sqlp,[toUserName,account,1,gmt_created,str(qrcode)])
												try:
													sql="insert into weixin_pclogin(openid,account,loginflag,qrcode,gmt_created) values(%s,%s,%s,%s,%s)"
													pcloginid=dbc.updatetodb(sql,[toUserName,account,1,str(qrcode),gmt_created])[0]
												except Exception , e:
													sql="insert into err_log (content) values(%s)"
													dbc.updatetodb(sql,[e])
												title='微信认证完毕，电脑端将自动登录，请点击PC端"点此进入生意管家"！'
								xml=backxml(xmltype=2,fromUserName=toUserName,toUserName=fromUserName,title=title)
								return HttpResponse(xml)
						else:
							title="感谢关注ZZ91再生网,从今儿起，ZZ91就可以在微信给亲提供行情和供求商机啦!\n\n\n\n 请先 <a href='http://m.zz91.com/weixin/login.html?weixinid="+str(toUserName)+"'>点击绑定ZZ91再生网帐号</a>！ <a href='http://m.zz91.com/register/?weixinid="+str(toUserName)+"'>木有帐号？用3秒钟注册一个</a>"
							xml=backxml(xmltype=2,fromUserName=toUserName,toUserName=fromUserName,title=title)
							return HttpResponse(xml)	
					except Exception , e:
						sql="insert into err_log (content) values(%s)"
						dbc.updatetodb(sql,[e])
						#title="很抱歉，网络忙！你可以点击其他菜单试试！"
						#title+='====================\r\n'
						title='更多资源下载ZZ91再生网App客户端  <a href="http://m.zz91.com/app.html">点此下载</a>\r\n'
						xml=backxml(xmltype=2,fromUserName=toUserName,toUserName=fromUserName,title=title)
						return HttpResponse(xml)
					"""
					#titlelist=[{'title':'6月16日，再生塑料订货峰会,招商电话：0571-56612345','Description':'招商电话：0571-56612345 56611111','PicUrl':'http://img1.zz91.com/ads/1462032000000/95457ab9-d33d-4098-a777-20b304676780.jpg','Url':'http://www.rabbitpre.com/m/V7rqeyN'}]
					titlelist=[{'title':'第16届中国塑料交易会 10.12-15,台州,招商电话：0571-56612345','Description':'招商电话：0571-56612345 56611111','PicUrl':'http://img1.zz91.com/ads/1467302400000/f4e6faa4-1566-4cc6-b731-53e1ad6418ca.jpg','Url':'http://zhanhui.zz91.com/exhibitchannel/taizhou/index.htm'}]
					tlist={'title':'点此登录ZZ91再生网','Description':'','PicUrl':'http://m.zz91.com/images/qianbao/5.png','Url':'http://m.zz91.com/weixin/login.html?weixinid='+str(toUserName)}
					titlelist.append(tlist)
					tlist={'title':'点此3秒钟注册账号','Description':'','PicUrl':'http://m.zz91.com/images/qianbao/5.png','Url':'http://m.zz91.com/register/?weixinid='+str(toUserName)}
					titlelist.append(tlist)
					tlist={'title':'免费发布','Description':'','PicUrl':'http://m.zz91.com/images/trust_logo.png','Url':'http://m.zz91.com/products_publish/?weixinid='+toUserName+''}
					titlelist.append(tlist)
					tlist={'title':'行情日报','Description':'','PicUrl':'http://m.zz91.com/images/qianbao/2.png','Url':'http://m.zz91.com/jiage/?weixinid='+toUserName+''}
					titlelist.append(tlist)
					tlist={'title':'商机查询','Description':'','PicUrl':'http://m.zz91.com/images/qianbao/7.png','Url':'http://m.zz91.com/trade/?weixinid='+toUserName+''}
					titlelist.append(tlist)
					ArticleCount=len(titlelist)
					xml=backxml(xmltype=3,fromUserName=toUserName,toUserName=fromUserName,ArticleCount=ArticleCount,titlelist=titlelist)
					#return HttpResponse(xml)
					#title="感谢关注ZZ91再生网,从今儿起，ZZ91就可以在微信给亲提供行情和供求商机啦!\n\n\n\n 请先 <a href='http://m.zz91.com/weixin/login.html?weixinid="+str(toUserName)+"'>点击绑定ZZ91再生网帐号</a>！ <a href='http://m.zz91.com/register/?weixinid="+str(toUserName)+"'>木有帐号？用3秒钟注册一个</a>"
					#xml=backxml(xmltype=2,fromUserName=toUserName,toUserName=fromUserName,title=title)
					#return HttpResponse(xml)
					"""
				else:
					title=content
					
					try:
						if not title:
							title="很抱歉，目前只支持文字的方式提交需求！你可以点击其他菜单试试！"
							title+='====================\r\n'
							title+='更多商机下载ZZ91再生网App客户端  <a href="http://m.zz91.com/app.html">点此下载</a>\r\n'
							xml=backxml(xmltype=2,fromUserName=toUserName,toUserName=fromUserName,title=title)
							return HttpResponse(xml)
						if (len(title)==1 and title=="1"):
							tmp = random.randint(1000000, 99999999)
							gmt_created=datetime.datetime.now()
							open_type="weixin.qq.com"
							target_account="0"
							value=[toUserName,open_type,target_account,tmp,gmt_created,gmt_created]
							sql="select id from oauth_access where open_id=%s and open_type=%s"
							result=dbc.fetchonedb(sql,[toUserName,open_type])
							if not result:
								sqlp="insert into oauth_access(open_id,open_type,target_account,code,gmt_created,gmt_modified) values(%s,%s,%s,%s,%s,%s)"
								dbc.updatetodb(sqlp,value)
							else:
								sql="update oauth_access set closeflag=1 where open_id=%s and open_type=%s"
								dbc.updatetodb(sql,[toUserName,open_type])
								sqlp="update oauth_access set code=%s,gmt_modified=%s,closeflag=0 where id=%s"
								dbc.updatetodb(sqlp,[tmp,gmt_created,result[0]])
							title="注册验证码："+str(tmp)+"\n十分钟内有效（此验证码在网页端微信验证时使用）"
							xml=backxml(xmltype=2,fromUserName=toUserName,toUserName=fromUserName,title=title)
							return HttpResponse(xml)
						if ("惊喜" in title):
							waccount=weixinbinding(toUserName)
							if waccount:
								taizhou2016(toUserName)
								title="恭喜你获得一次抽奖机会，马上登录抽奖，<a href='http://m.zz91.com/wechat/auth_login.html?tourl=http://m.zz91.com/taizhou2016/index.html&clientid="+str(toUserName)+"'>点此抽奖</a>"
								xml=backxml(xmltype=2,fromUserName=toUserName,toUserName=fromUserName,title=title)
								return HttpResponse(xml)
							else:
								title="您还未绑定您的ZZ91再生网帐号，<a href='http://m.zz91.com/weixin/login.html?weixinid="+str(toUserName)+"&tourl=http://m.zz91.com/taizhou2016/index.html'>点击绑定ZZ91再生网帐号</a>\r\n。"
								title+="未注册,<a href='http://m.zz91.com/register/?weixinid='"+str(toUserName)+"'>3秒钟注册账号</a>"
								xml=backxml(xmltype=2,fromUserName=toUserName,toUserName=fromUserName,title=title)
								return HttpResponse(xml)
						#投票
						if ("投票" in title):
							tpurl="http://m.zz91.com/wechat/auth_login.html?clientid="+str(toUserName)+"&tourl=/vote/v2017823feizhi/list.html"
							titlelist=[{'title':'废纸产业发展论坛-好评榜TOP10评选微信投票!','Description':'谁是真正的行业精英？你来决定！','PicUrl':'http://m.zz91.com/zt/feizhiluntanH5/images/feizhitoupiao.jpg','Url':tpurl}]
							ArticleCount=len(titlelist)
							
							xml=backxml(xmltype=3,fromUserName=toUserName,toUserName=fromUserName,ArticleCount=ArticleCount,titlelist=titlelist)
							return HttpResponse(xml)
						if ("砍价" in title):
							titlelist=[{'title':'双11，呼朋唤友来砍价，“零”元价格到','Description':'先到先得，活动名额有限！','PicUrl':'http://m.zz91.com/subject/kanjia/images/222.jpg','Url':'http://m.zz91.com/kanjia/index.html?weixinid='+str(toUserName)+''}]
							ArticleCount=len(titlelist)
							xml=backxml(xmltype=3,fromUserName=toUserName,toUserName=fromUserName,ArticleCount=ArticleCount,titlelist=titlelist)
							return HttpResponse(xml)
						if ("打卡" in title):
							waccount=weixinbinding(toUserName)
							if waccount:
								gmt_created=datetime.datetime.now()
								wxqd=zzq.wxqiandao(waccount,toUserName)
								company_id=getcompanyid(waccount)
								dakacount=zzq.wxqiandaocount(waccount)
								qianbaoblance=zzq.getqianbaoblance(company_id)
								if (wxqd==0):
									#送1元再生钱包
									zzq.getsendfee(company_id,"1","45",more=1)
									if dakacount<7:
										title="恭喜您，打卡成功\r\n!您已获得1元再生钱包。继续打卡“"+str((7-dakacount))+"”天,您即可获得 10 元再生钱包,目前你的钱包余额为："+str(qianbaoblance)+"元"
									if dakacount==7:
										title="恭喜您，打卡成功\r\n!您已获得1元再生钱包。您已连续打卡 7 天，赠送给您10元钱包，<a href='http://m.zz91.com/weixin/getqianbao.html?weixinid="+str(toUserName)+"&gettype=7day'>点此领取</a>，领取签到数即清零，未领取将累加入连续打卡3周送“供求自动刷新”一个月服务，继续加油哦。"
									if dakacount>7:
										title="恭喜您，打卡成功\r\n!您已获得1元再生钱包。继续打卡“"+str((21-dakacount))+"”天,您即可获得 “供求自动刷新”一个月服务,目前你的钱包余额为："+str(qianbaoblance)+"元"
									if dakacount>=21:
										title="恭喜您，打卡成功\r\n!您已获得1元再生钱包。您已连续打卡 3周，赠送获得 “供求自动刷新”一个月服务。<a href='http://m.zz91.com/weixin/getqianbao.html?weixinid="+str(toUserName)+"&gettype=21day'>点此领取</a>，领取签到数即清零，继续打卡获取更多服务,目前你的钱包余额为："+str(qianbaoblance)+"元"
									xml=backxml(xmltype=2,fromUserName=toUserName,toUserName=fromUserName,title=title)
								if (wxqd==1):
									if dakacount<7:
										title="今天您已经打过卡了。继续打卡“"+str((7-dakacount))+"”天,您即可获得 10 元再生钱包,目前你的钱包余额为："+str(qianbaoblance)+"元"
									if dakacount==7:
										title="今天您已经打过卡了。您已连续打卡 7 天，赠送给您10元钱包，<a href='http://m.zz91.com/weixin/getqianbao.html?weixinid="+str(toUserName)+"&gettype=7day'>点此领取</a>，领取签到数即清零，未领取将累加入连续打卡3周送“供求自动刷新”一个月服务，继续加油哦。"
									if dakacount>7:
										title="今天您已经打过卡了。继续打卡“"+str((21-dakacount))+"”天,您即可获得 “供求自动刷新”一个月服务,目前你的钱包余额为："+str(qianbaoblance)+"元"
									if dakacount>=21:
										title="今天您已经打过卡了。您已连续打卡 3周，赠送获得 “供求自动刷新”一个月服务。<a href='http://m.zz91.com/weixin/getqianbao.html?weixinid="+str(toUserName)+"&gettype=21day'>点此领取</a>，领取签到数即清零，继续打卡获取更多服务,目前你的钱包余额为："+str(qianbaoblance)+"元"
									xml=backxml(xmltype=2,fromUserName=toUserName,toUserName=fromUserName,title=title)
							else:
								tourl="/weixin/login.html?weixinid="+str(toUserName)
								if tourl:
									tourl=tourl.replace("&","^and^")
									tourl=tourl.replace("#","^jing^")
									tourl=tourl.replace("?","^wenhao^")
								Url="http://m.zz91.com/wechat/auth_login.html?tourl="+tourl+"&clientid="+str(toUserName)
								title="您还未绑定您的ZZ91再生网帐号，<a href='"+Url+"'>点此立即绑定</a>\r\n。"
								title+="未注册,<a href='http://m.zz91.com/register/?weixinid='"+str(toUserName)+"'>3秒钟注册账号</a>"
								title+='====================\r\n'
								title+='更多资源下载ZZ91再生网App客户端  <a href="http://m.zz91.com/app.html">点此下载</a>\r\n'
								xml=backxml(xmltype=2,fromUserName=toUserName,toUserName=fromUserName,title=title)
							return HttpResponse(xml)
						if ("支付" in title):
							title="支付方式\n\nZZ91支付宝帐号：zhifu@zz91.com\n\n开户银行：中国农业银行杭州朝晖支行\n收 款 人：杭州阿思拓信息科技有限公司\n帐　　号：19-0156 0104 0013 383\n\n公司地址：浙江省杭州市江干区九盛路9号东方电子商务园13栋\n\n邮编：310019 \n\n传真：0571-56637777\n"
							xml=backxml(xmltype=2,fromUserName=toUserName,toUserName=fromUserName,title=title)
							return HttpResponse(xml)
						if (title=="联系"):
							title="服务电话\n\n0571-56611111\n\n0571-56612345\n\n公司地址：浙江省杭州市江干区九盛路9号东方电子商务园13栋\n\n邮编：310019 \n\n传真：0571-56637777\n"
							xml=backxml(xmltype=2,fromUserName=toUserName,toUserName=fromUserName,title=title)
							return HttpResponse(xml)
						if (title=="抽奖1"):
							title="很遗憾，您没有中奖！"
							xml=backxml(xmltype=2,fromUserName=toUserName,toUserName=fromUserName,title=title)
							return HttpResponse(xml)
						if (("报价" in title) or ("价格" in title)):
							keywords=title.replace("报价","").replace("报价","")
							title="<a href='http://m.zz91.com/jiage/?keywords="+keywords+"'>点此查看‘"+keywords+"’报价</a>"
							xml=backxml(xmltype=2,fromUserName=toUserName,toUserName=fromUserName,title=title)
							return HttpResponse(xml)
						if (("供应" in title) or ("求购" in title)):
							pdt_type=''
							if ("供应" in title):
								pdt_type=1
							if ("求购" in title):
								pdt_type=2
							keywords=title.replace("求购","").replace("供应","")
							title="<a href='http://m.zz91.com/trade/?keywords="+keywords+"&ptype="+str(pdt_type)+"'>点此查看‘"+keywords+"’供求</a>"
							xml=backxml(xmltype=2,fromUserName=toUserName,toUserName=fromUserName,title=title)
							return HttpResponse(xml)
						
						else:
							weixinhelp(toUserName)
							title='更多下载ZZ91再生网App客户端  <a href="http://m.zz91.com/app.html">点此下载</a>\r\n'
							title=str(title)
							CreateTime=str(int(time.time()))
							post_dict={
								"ToUserName":"<![CDATA["+toUserName+"]]>",
								"FromUserName":"<![CDATA["+fromUserName+"]]>",
								"CreateTime":"<![CDATA["+CreateTime+"]]>",
								"MsgType":"<![CDATA[text]]>",
								"Content":"<![CDATA["+title+"]]>",
								"FuncFlag":"<![CDATA[0]]>"
							}
							xml = dict2xml(post_dict, wrap='xml')
							sql="insert into err_log (content) values(%s)"
							dbc.updatetodb(sql,[xml])
							#xml=backxml(xmltype=2,fromUserName=toUserName,toUserName=fromUserName,title=title)
							return HttpResponse(xml)
					except Exception , e:
						sql="insert into err_log (content) values(%s)"
						dbc.updatetodb(sql,[e])
						title="很抱歉，网络忙！你可以点击其他菜单试试！"
						title+='====================\r\n'
						title+='更多资源下载ZZ91再生网App客户端  <a href="http://m.zz91.com/app.html">点此下载</a>\r\n'
						xml=backxml(xmltype=2,fromUserName=toUserName,toUserName=fromUserName,title=title)
						return HttpResponse(xml)
					#title=title.replace('求购','').replace('供应','').replace('报价','')
					#xml=backxml(xmltype=1,fromUserName=toUserName,toUserName=fromUserName,title=title)
					#return HttpResponse(xml)
			else:
				return HttpResponse("Invalid Request")
	else:
		return HttpResponse("Invalid Request")
	return render_to_response('new/doget.html',locals())
#金牌供应商投票
def votecom(orderid,toUserName,fromUserName):
	title="投票已经结束！截至时间：2016-6-12 23:59:59"
	xml=backxml(xmltype=2,fromUserName=toUserName,toUserName=fromUserName,title=title)
	return HttpResponse(xml)
	vtype=1
	clientid_dy=toUserName
	company_id=None
	if orderid:
		sql="select company_id,company_name from vote_list where orderid=%s and vtype=%s"
		result=dbc.fetchonedb(sql,[orderid,vtype])
		if result:
			company_id=result[0]
			company_name=result[1]
	if not company_id:
		title="很抱歉，您输入的投票序号不存在，请输入其他序号进行投票！"
		xml=backxml(xmltype=2,fromUserName=toUserName,toUserName=fromUserName,title=title)
		return HttpResponse(xml)
	if company_id:
		gmt_created=gmt_modified=datetime.datetime.now()
		gmt_date=formattime(gmt_created,1)
		#投票
		sql="select count(0) from vote_log where clientid=%s and gmt_date=%s and vtype=%s"
		result=dbc.fetchonedb(sql,[clientid_dy,gmt_date,vtype])
		if result:
			vcount=result[0]
			if vcount>=3:
				title="很抱歉，您今天投票已经超过3次，明天继续加油哦！"
				xml=backxml(xmltype=2,fromUserName=toUserName,toUserName=fromUserName,title=title)
				return HttpResponse(xml)
			else:
				if company_id:
					sql="insert into vote_log(forcompany_id,clientid,gmt_date,gmt_created,vtype) values(%s,%s,%s,%s,%s)"
					dbc.updatetodb(sql,[company_id,clientid_dy,gmt_date,gmt_created,vtype])
					sql="select count(0) from vote_log where forcompany_id=%s and vtype=%s"
					result=dbc.fetchonedb(sql,[company_id,vtype])
					if result:
						vcount=result[0]
						sql="update vote_list set votecount=%s where company_id=%s and vtype=%s"
						dbc.updatetodb(sql,[vcount,company_id,vtype])
						tpurl="http://m.zz91.com/wechat/auth_login.html?clientid="+str(toUserName)+"&tourl=/vote/jsindex.html"
						title="恭喜您，您已投票成功，您投的公司是："+company_name+"，目前票数："+str(vcount)+",<a href='"+tpurl+"'>点此查看详情</a>"
						xml=backxml(xmltype=2,fromUserName=toUserName,toUserName=fromUserName,title=title)
						return HttpResponse(xml)
	title="系统错误，请重试！"
	xml=backxml(xmltype=2,fromUserName=toUserName,toUserName=fromUserName,title=title)
	return HttpResponse(xml)
#----环保微信
def huanbaowxget(request):
	token = "huanbao"
	params = request.GET
	args = [token, params['timestamp'], params['nonce']]
	args.sort()
	if hashlib.sha1("".join(args)).hexdigest() == params['signature']:
		if params.has_key('echostr'):
			return HttpResponse(params['echostr'])
		else:
			if request.body:
				xml = ET.fromstring(request.body)
				fromUserName = xml.find("ToUserName").text
				toUserName = xml.find("FromUserName").text
				MsgType = xml.find("MsgType").text
				Event1=None
				content=None
				EventKey=""
				#request.session.set_expiry(60*60)
				request.session['weixinid']=toUserName
				if (MsgType=="event"):
					Event1 = xml.find("Event").text
					EventKey = xml.find("EventKey").text
				if (MsgType=="text"):
					content = xml.find("Content").text
				if (MsgType=="image"):
					PicUrl = xml.find("PicUrl").text
					
				postTime = str(int(time.time()))
				
				if (content==None  and EventKey=='binding'):
					title="您好！欢迎您加入中国环保网（www.huanbao.com）公众平台！\n\n 回复1：注册验证 \n\n 回复产品名：了解最新供求商机！\n\n感谢您的关注"
					xml=backxml(xmltype=2,fromUserName=toUserName,toUserName=fromUserName,title=title)
					return HttpResponse(xml)
				if (Event1 == "subscribe" or Event1 == "scan"):
					title="您好！欢迎您加入中国环保网（www.huanbao.com）公众平台！\n\n 回复1：注册验证 \n\n 回复产品名：了解最新供求商机！\n\n感谢您的关注"
					#title="感谢关注ZZ91再生网,从今儿起，ZZ91就可以在微信给亲提供行情和供求商机啦!\n\n 请先 <a href='http://m.zz91.com/weixin/login.html?weixinid="+str(toUserName)+"'>点击绑定ZZ91再生网帐号</a>\n\n <a href='http://m.zz91.com/register/?weixinid="+str(toUserName)+"'>木有帐号？发3秒钟注册一个</a>"
					xml=backxml(xmltype=2,fromUserName=toUserName,toUserName=fromUserName,title=title)
					return HttpResponse(xml)
				else:
					title=content
					try:
						if (len(title)==1 and title=="1"):
							tmp = random.randint(100000, 999999)
							gmt_created=datetime.datetime.now()
							sql="insert into user_validate(weixinid,code,gmt_greated) values(%s,%s,%s)"
							dbhuanbao.updatetodb(sql,[str(toUserName),tmp,gmt_created]);
							title="注册验证码："+str(tmp)+"\n五分钟内有效（此验证码在网页端微信验证时使用）"
							xml=backxml(xmltype=2,fromUserName=toUserName,toUserName=fromUserName,title=title)
							return HttpResponse(xml)
					except:
						title="在点我试试！"
						xml=backxml(xmltype=2,fromUserName=toUserName,toUserName=fromUserName,title=title)
						return HttpResponse(xml)
			else:
				return HttpResponse("Invalid Request")
	else:
		return HttpResponse("Invalid Request")
	return render_to_response('new/doget.html',locals())

#----元宝铺微信
def yuanbaopuwxget(request):
	#sql="insert into err_log (content) values(%s)"
	#dbc.updatetodb(sql,[request])
	token = "yuanbaopu"
	params = request.GET
	args = [token, params['timestamp'], params['nonce']]
	args.sort()
	
	if hashlib.sha1("".join(args)).hexdigest() == params['signature']:
		if params.has_key('echostr'):
			return HttpResponse(params['echostr'])
		else:
			if request.body:
				xml = ET.fromstring(request.body)
				fromUserName = xml.find("ToUserName").text
				toUserName = xml.find("FromUserName").text
				MsgType = xml.find("MsgType").text
				Event1=None
				content=None
				EventKey=""
				if (MsgType=="event"):
					Event1 = xml.find("Event").text
					EventKey = xml.find("EventKey").text
				if (MsgType=="text"):
					content = xml.find("Content").text
				if (MsgType=="image"):
					PicUrl = xml.find("PicUrl").text
				gmt_created=gmt_modified=datetime.datetime.now()
				postTime = str(int(time.time()))
				sql="select id from weixin_gzlist where openid=%s"
				result=dbc.fetchonedb(sql,[toUserName])
				if not result:
					sql="insert into weixin_gzlist(openid,wxname,gmt_created) values(%s,%s,%s)"
					dbc.updatetodb(sql,[toUserName,'ybpdyh',gmt_created])
				if (content==None  and EventKey=='binding'):
					title="感谢您关注元宝铺！\n元宝铺--数据贷动未来！\n为电商卖家提供无抵押、低利息、高额度信用贷款！\n为您大促备货、活动保证金、运营推广提供资金！\n您可以通过自助菜单来了解我们。\n更欢迎您的来电！\n 4007-117-000"
					xml=backxml(xmltype=2,fromUserName=toUserName,toUserName=fromUserName,title=title)
					return HttpResponse(xml)
				if (content==None  and EventKey=='zx'):
					title="您好，感谢您使用在线咨询服务，现在您可以反馈您的问题，我们将尽快回复。\n 我们的电话：4007-117-000"
					xml=backxml(xmltype=2,fromUserName=toUserName,toUserName=fromUserName,title=title)
					return HttpResponse(xml)
				#调查问卷
				if (content==None  and EventKey=='dc'):
					titlelist=[{'title':'元宝铺客户满意度调查表!','Description':'填写完毕即可领取惊喜福利！','PicUrl':'http://m.zz91.com/vote/images/vote_top.jpg','Url':'http://m.zz91.com/vote/ybp_redirect.html?clientid='+toUserName+''}]
					ArticleCount=len(titlelist)
					xml=backxml(xmltype=3,fromUserName=toUserName,toUserName=fromUserName,ArticleCount=ArticleCount,titlelist=titlelist)
					return HttpResponse(xml)
				#调查问卷
				if (content==None  and EventKey=='xjjl'):
					titlelist=[{'title':'分享二维码，马上返现金！','Description':'恭喜您成为元宝铺带盐人！分享您的专属二维码邀请好友成为元宝铺用户，若好友成功办理信贷产品，您将获得300元的现金奖励。可叠加，无上限，每单都奖300元。','PicUrl':'http://img0.zz91.com/yuanbaopu/weixin/20160831.png','Url':'https://act.yuanbaopu.com/brand/login.htm?flag=share&openid='+toUserName+''}]
					ArticleCount=len(titlelist)
					xml=backxml(xmltype=3,fromUserName=toUserName,toUserName=fromUserName,ArticleCount=ArticleCount,titlelist=titlelist)
					return HttpResponse(xml)
				if (Event1 == "subscribe" or Event1 == "scan"):
					
					wxc = Client(weixinconfig['yuanbaopu']['appid'], weixinconfig['yuanbaopu']['secret'])
					token=wxc.send_text_message(toUserName,"感谢您关注元宝铺！\n元宝铺--数据贷动未来！\n为电商卖家提供无抵押、低利息、高额度信用贷款！\n为您大促备货、活动保证金、运营推广提供资金！\n您可以通过自助菜单来了解我们。\n更欢迎您的来电！\n 4007-117-000")
					
					#titlelist=[{'title':'元宝铺客户满意度调查表!','Description':'填写完毕即可领取惊喜福利！','PicUrl':'http://m.zz91.com/vote/images/vote_top.jpg','Url':'http://m.zz91.com/vote/ybp_redirect.html?clientid='+toUserName+''}]
					titlelist=[{'title':'分享二维码，马上返现金！','Description':'恭喜您成为元宝铺带盐人！分享您的专属二维码邀请好友成为元宝铺用户，若好友成功办理信贷产品，您将获得300元的现金奖励。可叠加，无上限，每单都奖300元。','PicUrl':'http://img0.zz91.com/yuanbaopu/weixin/20160831.png','Url':'https://act.yuanbaopu.com/brand/login.htm?flag=share&openid='+toUserName+''}]
					ArticleCount=len(titlelist)
					xml=backxml(xmltype=3,fromUserName=toUserName,toUserName=fromUserName,ArticleCount=ArticleCount,titlelist=titlelist)
					return HttpResponse(xml)
					#title="感谢您关注元宝铺！\n元宝铺--数据贷动未来！\n为电商卖家提供无抵押、低利息、高额度信用贷款！\n为您大促备货、活动保证金、运营推广提供资金！\n您可以通过自助菜单来了解我们。\n更欢迎您的来电！\n 4007-117-000"
					#xml=backxml(xmltype=2,fromUserName=toUserName,toUserName=fromUserName,title=title)
					#return HttpResponse(xml)
					
				
				else:
					title=content
					if "调查" in title:
						titlelist=[{'title':'元宝铺客户满意度调查表!','Description':'填写完毕即可领取惊喜福利！','PicUrl':'http://m.zz91.com/vote/images/vote_top.jpg','Url':'http://m.zz91.com/vote/ybp_redirect.html?clientid='+toUserName+''}]
						ArticleCount=len(titlelist)
						xml=backxml(xmltype=3,fromUserName=toUserName,toUserName=fromUserName,ArticleCount=ArticleCount,titlelist=titlelist)
						return HttpResponse(xml)
					title="您好，感谢您使用在线咨询服务，您反馈您的问题，我们将尽快回复。\n 我们的电话：4007-117-000"
					xml=backxml(xmltype=2,fromUserName=toUserName,toUserName=fromUserName,title=title)
					return HttpResponse(xml)
			else:
				return HttpResponse("Invalid Request")
	else:
		return HttpResponse("Invalid Request")
	return render_to_response('new/doget.html',locals())

#----ZZ91微信验证提示
def zz91weixin_yzfront(request):
	account= request.GET.get("account")
	flag=request.GET.get("flag")
	scriptvalue="document.write(\"<div class=tishi>您的账号还未进行微信验证，请<a href='javascript:onclick=openweixinyz()'>点此立即验证</a></div>\")"
	sql="select id from oauth_access where target_account=%s and open_type='weixin.qq.com' and closeflag=0"
	plist=dbc.fetchonedb(sql,[account]);
	if plist:
		if (flag=='1'):
			return HttpResponse("var _suggest_result_={'result':'1'}")
		else:
			return HttpResponse("")
	else:
		if (flag=='1'):
			return HttpResponse("var _suggest_result_={'result':'0'}")
		else:
			return HttpResponse(scriptvalue)
#----ZZ91微信验证
def zz91weixin_yz(request):
	account= request.GET.get("account")

	step1=1
	return render_to_response('zz91weixin/yz.html',locals())
def zz91weixin_yzsave(request):
	account = request.POST['account']
	yzm = request.POST['yzm']
	if (yzm and yzm!=""):
		sql="select id from oauth_access where code=%s and TIMESTAMPDIFF(MINUTE,gmt_created,now())<10"
		plist=dbc.fetchonedb(sql,[yzm]);
		if plist:
			sqlp="update oauth_access set target_account=%s where id=%s"
			dbc.updatetodb(sqlp,[account,plist[0]]);
			step2=1
		else:
			err="您输入的验证码错误或已过期！"
			step1=1
	return render_to_response('zz91weixin/yz.html',locals())
#----环保微信验证提示
def huanbaoweixin_yzfront(request):
	account= request.GET.get("account")
	flag=request.GET.get("flag")
	scriptvalue="document.write(\"<dl class='info-wrap'><dt>微信验证：</dt><dd class=tishi>您的账号还未进行微信验证，请<a href='javascript:onclick=openweixinyz()'>点此立即验证</a></dd></dl>\")"
	sql="select id from user_validate where account=%s"
	plist=dbhuanbao.fetchonedb(sql,[account]);
	if plist:
		if (flag=='1'):
			return HttpResponse("var _suggest_result_={'result':'1'}")
		else:
			return HttpResponse("")
	else:
		if (flag=='1'):
			return HttpResponse("var _suggest_result_={'result':'0'}")
		else:
			return HttpResponse(scriptvalue)
#----环保微信验证
def huanbaoweixin_yz(request):
	account= request.GET.get("account")
	step1=1
	return render_to_response('huanbaoweixin/yz.html',locals())
def huanbaoweixin_yzsave(request):
	account = request.POST['account']
	yzm = request.POST['yzm']
	sql="select id from user_validate where code=%s and TIMESTAMPDIFF(MINUTE,gmt_greated,now())<20"
	plist=dbhuanbao.fetchonedb(sql,[yzm]);
	if plist:
		sqlp="update user_validate set account=%s,codecheck=1 where id=%s"
		dbhuanbao.updatetodb(sqlp,[account,plist[0]]);
		step2=1
	else:
		err="您输入的验证码错误或已过期！"
		step1=1
	return render_to_response('huanbaoweixin/yz.html',locals())
#阿里大于短信系统
def postsms_dayu(mobile,sms_template_code,sms_free_sign_name,sms_param):
    req = top.api.AlibabaAliqinFcSmsNumSendRequest()
    req.set_app_info(top.appinfo("23410861", "72b4d7f51b757714b946d82ff9376a55"))
    req.sms_type = "normal"
    req.rec_num = mobile
    req.sms_template_code=sms_template_code
    req.sms_free_sign_name=sms_free_sign_name
    req.sms_param = json.dumps(sms_param,ensure_ascii=False,indent=2)
    try:
        resp= req.getResponse()
        if resp.get('alibaba_aliqin_fc_sms_num_send_response').get('result').get('success')==True:
            return True
        else:
            return False
    except Exception,e:
        return False
#----发手机短信
def postsms(mobile,username,userid):
	sqlp="select TIMESTAMPDIFF(SECOND,gmt_created,now()) as ltime from auth_forgot_password_log where company_id=%s and DATEDIFF(CURDATE(),gmt_created)<1 order by gmt_created desc"
	plist=dbc.fetchalldb(sqlp,[userid])
	pcount=len(plist)
	if (pcount<10):
		if plist:
			ltime=plist[0][0]
			if ltime<=60:
				return '验证码已经发送，一分钟内请不要重复提交！'
		tmp = random.randint(10000, 99999)
		#content="欢迎使用ZZ91再生网服务。验证码是："+str(tmp)+",输入验证码继续完成操作，该验证码10分钟内输入有效。"
		#url="http://mt.10690404.com/send.do?Account=astokf&Password=C@4k@33lsbe2lw^6&Mobile="+str(mobile)+"&Content="+content+"&Exno=0"
		#f = urllib.urlopen(url)
		#html = f.read()
		#o = json.loads(html)
		
		sms_template_code="SMS_12520535"
		sms_free_sign_name="ZZ91再生网"
		smscontent=r'验证是：(.*?)，请勿泄露'
		code=tmp
		sms_param={"code": str(code), "product": "ZZ91再生网"}
		returnsms=postsms_dayu(mobile[0:11],sms_template_code,sms_free_sign_name,sms_param)
		
		gmt_created=datetime.datetime.now()
		sql="insert into auth_forgot_password_log(company_id,type,gmt_created,gmt_modified) values(%s,%s,%s,%s)"
		dbc.updatetodb(sql,[userid,1,gmt_created,gmt_created]);
		sqlp="select id from auth_forgot_password where username=%s and userid=%s order by id desc"
		plist=dbc.fetchonedb(sqlp,[username,userid]);
		if not plist:
			sql="insert into auth_forgot_password(username,userid,auth_key,gmt_created) values(%s,%s,%s,%s)"
			dbc.updatetodb(sql,[username,userid,tmp,gmt_created]);
		else:
			sql="update auth_forgot_password set auth_key=%s,gmt_created=%s where id=%s"
			dbc.updatetodb(sql,[tmp,gmt_created,plist[0]]);
		return True
	else:
		return "您已经超过了每天发生10条短信的限制！"
#-----忘记密码	
def forgetpassword(request):
	return HttpResponseRedirect("/myrc/forgetpassword.html")
	step= request.GET.get("step")
	username=request.session.get("username",None)
	if username==None:
		username=''
	#username=request.COOKIES.get("username",None)
	#company_id=request.COOKIES.get('company_id',None)
	gmt_modified=datetime.datetime.now()
	if (step=="4"):
		step="4"
	else:
		pw=weixinautologin(request,request.GET.get("weixinid"))
		if pw:
			step="3"
	if (step==None or step==""):
		step0=1
		weixinid=request.GET.get("weixinid")
	if (step=="1"):
		step1=1
		step0=None
		username = request.POST['username']
		weixinid = request.POST['weixinid']
		
		if (username==""):
			step1=None
			step0=1
			error="请输入手机 或 用户名 或 邮箱"
		else:
			sql="select id,username from auth_user where (username=%s or email=%s or mobile=%s)"
			plist=dbc.fetchonedb(sql,[username,username,username]);
			if plist:
				account=plist[1]
				sqlc="select company_id,mobile from company_account where account=%s"
				list=dbc.fetchonedb(sqlc,[account]);
				if list:
					company_id=list[0]
					mobile=list[1]
					smsreresult=postsms(mobile,account,company_id)
					if (smsreresult!=True):
						step1=None
						step0=1
						error=smsreresult	
				else:
					step1=None
					step0=1
					error="未知的错误！"
			else:
				sqlc="select company_id,mobile,account from company_account where mobile=%s"
				list=dbc.fetchonedb(sqlc,[username]);
				if list:
					company_id=list[0]
					mobile=list[1]
					account=list[2]
					smsreresult=postsms(mobile,account,company_id)
					if (smsreresult!=True):
						step1=None
						step0=1
						error=smsreresult	
				else:
					step1=None
					step0=1
					error="手机或用户名或邮箱不存在！"
			#return HttpResponse(step0)
	if (step=="2"):
		step2=1
		mobile=request.POST["mobile"]
		account = request.POST['account']
		yzcode = request.POST['yzcode']
		weixinid = request.POST['weixinid']
		sql="select id from auth_forgot_password where username=%s and auth_key=%s and DATEDIFF(CURDATE(),gmt_created)<1"
		plist=dbc.fetchonedb(sql,[account,yzcode]);
		if (plist==None):
			step1=1
			step2=None
			error="你输入的验证码错误！"
			
	if (step=="3"):
		step3=1
		weixinid=request.GET.get("weixinid")
		
	if (step=="4"):
		mobile=request.POST["mobile"]
		account = request.POST['account']
		weixinid = request.POST['weixinid']
		passwd1=request.POST["passwd1"]
		passwd2=request.POST["passwd2"]
		error=""
		if (passwd1==""):
			step2=1
			error="密码不能为空！"
		if (passwd1!=passwd2):
			step2=1
			error="两次输入的密码不一致！"
		if (error==""):
			md5pwd = hashlib.md5(passwd1)
			md5pwd = md5pwd.hexdigest()[8:-8]
			sql="update auth_user set password=%s,mobile=%s,gmt_modified=%s where username=%s "
			dbc.updatetodb(sql,[md5pwd,mobile,gmt_modified,account]);
			sql="update company_account set password=%s,gmt_modified=%s where account=%s"
			dbc.updatetodb(sql,[passwd1,gmt_modified,account]);
			
			step4=1
	if (step=="5"):
		weixinid = request.POST['weixinid']
		passwd1=request.POST["passwd1"]
		passwd2=request.POST["passwd2"]
		error=""
		if (passwd1==""):
			step3=1
			error="密码不能为空！"
		if (passwd1!=passwd2):
			step3=1
			error="两次输入的密码不一致！"
		if (error==""):
			account=weixinbinding(weixinid)
			if account:
				md5pwd = hashlib.md5(passwd1)
				md5pwd = md5pwd.hexdigest()[8:-8]
				sql="update auth_user set password=%s,gmt_modified=%s where username=%s "
				dbc.updatetodb(sql,[md5pwd,gmt_modified,account]);
				sql="update company_account set password=%s,gmt_modified=%s where account=%s"
				dbc.updatetodb(sql,[passwd1,gmt_modified,account]);
				step4=1
			
	return render_to_response('new/forgetpasswd.html',locals())
#----登录保存
def loginsave(request):
	userName = request.POST.get('userName')
	passwd = request.POST.get('passwd')
	tourl = request.POST.get('tourl')
	weixinid = request.POST.get('weixinid')
	qrcode = request.POST.get('qrcode')
	md5pwd = hashlib.md5(passwd)
	md5pwd = md5pwd.hexdigest()[8:-8]
	gmt_created=datetime.datetime.now()
	gmt_modified=datetime.datetime.now()
	sql="select id,username from auth_user where (username=%s or email=%s or mobile=%s) and password=%s"
	plist=dbc.fetchonedb(sql,[userName,userName,userName,md5pwd]);
	if plist:
		request.session.set_expiry(6000*6000)
		account=plist[1]
		sqlc="select company_id from company_account where account=%s"
		list=dbc.fetchonedb(sqlc,[account]);
		if list:
			company_id=list[0]
			#判断是否拉黑
			sqlh="select id from company where id=%s and is_block=1"
			listh=dbc.fetchonedb(sqlh,[company_id]);
			if listh:
				error="该用户已经被禁止登录！"
				return render_to_response('new/login.html',locals())
			request.session['username']=account
			request.session['company_id']=list[0]
			
			updatelogin(request,list[0])
			sqlc="select id from oauth_access where open_id=%s and target_account=%s"
			list=dbc.fetchonedb(sqlc,[str(weixinid),account])
			if list:
				sql="update oauth_access set closeflag=1 where open_id=%s and open_type=%s"
				dbc.updatetodb(sql,[weixinid,'weixin.qq.com'])
				#设置当前为默认登陆账号
				sql="update oauth_access set closeflag=0 where id=%s"
				dbc.updatetodb(sql,[list[0]])
				
				if tourl and str(tourl)!="None":
					tourl=getlogintourl(tourl)
					return HttpResponseRedirect(tourl)
				return render_to_response('new/loginsuc.html',locals())
			else:
				sql="update oauth_access set closeflag=1 where open_id=%s and open_type=%s"
				dbc.updatetodb(sql,[weixinid,'weixin.qq.com'])
				#设置当前为默认登陆账号
				sql="insert into oauth_access(open_id,open_type,target_account,gmt_created,gmt_modified,closeflag) values(%s,%s,%s,%s,%s,%s)"
				dbc.updatetodb(sql,[weixinid,'weixin.qq.com',account,gmt_created,gmt_modified,0])
				#提醒定制商机
				weixinorder(weixinid)
				#首次微信绑定获得1次抽奖机会
				choujiang(company_id=company_id,weixinid=weixinid)
			
		else:
			error="用户名或邮箱 还未在ZZ91注册！"
			return render_to_response('new/login.html',locals())
	else:
		sqlc="select account,company_id from company_account where mobile=%s order by id desc"
		list=dbc.fetchonedb(sqlc,[userName]);
		if list:
			account=list[0]
			company_id=list[1]
			#判断是否拉黑
			sqlh="select id from company where id=%s and is_block=1"
			listh=dbc.fetchonedb(sqlh,[company_id]);
			if listh:
				error="该用户已经被禁止登录！"
				return render_to_response('new/login.html',locals())
			sqlp="select id from auth_user where username=%s and password=%s"
			listp=dbc.fetchonedb(sqlp,[account,md5pwd]);
			#return HttpResponse(account)
			if listp:
				request.session.set_expiry(6000*6000)
				request.session['username']=account
				request.session['company_id']=company_id
				updatelogin(request,company_id)
				sqlc="select id from oauth_access where open_id=%s and target_account=%s"
				listw=dbc.fetchonedb(sqlc,[weixinid,account]);
				if listw:
					sql="update oauth_access set closeflag=1 where open_id=%s and open_type=%s"
					dbc.updatetodb(sql,[weixinid,'weixin.qq.com'])
					#设置当前为默认登陆账号
					sql="update oauth_access set closeflag=0 where id=%s"
					dbc.updatetodb(sql,[listw[0]])
					if tourl and str(tourl)!="None":
						tourl=getlogintourl(tourl)
						return HttpResponseRedirect(tourl)
					return render_to_response('new/loginsuc.html',locals())
				else:
					sql="update oauth_access set closeflag=1 where open_id=%s and open_type=%s"
					dbc.updatetodb(sql,[weixinid,'weixin.qq.com'])
					#设置当前为默认登陆账号
					sql="insert into oauth_access(open_id,open_type,target_account,gmt_created,gmt_modified,closeflag) values(%s,%s,%s,%s,%s,%s)"
					dbc.updatetodb(sql,[weixinid,'weixin.qq.com',account,gmt_created,gmt_modified,0])
					#提醒定制商机
					weixinorder(weixinid)
					#微信绑定获得1次抽奖机会
					choujiang(company_id=company_id,weixinid=weixinid)
					
				#更新pc端登录状态
				if qrcode and str(qrcode)!='None':
					sqlb="select id from weixin_pclogin where openid=%s and account=%s and qrcode=%s"
					resultc=dbc.fetchonedb(sqlb,[weixinid,account,qrcode])
					if resultc:
						sqlp="update weixin_pclogin set loginflag=1,gmt_created=%s where id=%s"
						dbc.updatetodb(sqlp,[gmt_created,resultc[0]])
					else:
						sqlp="insert into weixin_pclogin (openid,account,loginflag,gmt_created,qrcode) values(%s,%s,%s,%s,%s)"
						dbc.updatetodb(sqlp,[weixinid,account,1,gmt_created,str(qrcode)])
					#微信登录成功提醒
					loginsuctishi(weixinid)
			else:
				error="用户名或密码错误！"
				return render_to_response('new/login.html',locals())
		else:
			error="密码错误或你填写的手机/用户名还未注册"
			return render_to_response('new/login.html',locals())
	#return HttpResponse(tourl)
	if tourl and str(tourl)!="None":
		tourl=getlogintourl(tourl)
		return HttpResponseRedirect(tourl)
	return render_to_response('new/loginsuc.html',locals())
#----注册保存
def regsave(request):
	userName = request.POST['userName']
	passwd = request.POST['passwd']
	qq = request.POST['qq']
	email = request.POST['email']
	contact = request.POST['contact']
	weixinid = request.POST['weixinid']
	qrcode = request.POST.get('qrcode')
	mobile=userName
	regtime=gmt_created=datetime.datetime.now()
	gmt_modified=datetime.datetime.now()
	errflag=0
	if (userName=='' or userName.isdigit()==False):
		errtext1="必须填写 手机号码"
		errflag=1
	if (passwd==''):
		errtext2="必须填写 密码"
		errflag=1
	if (email==''):
		errtext5="请输入您的邮箱"
		errflag=1
	if (contact==''):
		errtext4="必须填写 联系人"
		errflag=1
	if (errflag==0):
		#''判断邮箱帐号是否存在
		sql="select id  from auth_user where username=%s"
		accountlist=dbc.fetchonedb(sql,str(userName))
		if (accountlist):
			errflag=1
			errtext1="您填写的手机号码已经注册！点此<a href='/weixin/forgetpasswd.html'>忘记密码?</a>"
			
		sql="select id  from company_account where mobile=%s"
		accountlist=dbc.fetchonedb(sql,str(userName))
		if (accountlist):
			errflag=1
			errtext1="您填写的手机号码已经注册！点此<a href='/weixin/forgetpasswd.html'>忘记密码?</a>"
			
		sql="select id  from auth_user where email=%s"
		accountlist=dbc.fetchonedb(sql,str(email))
		if (accountlist):
			errflag=1
			errtext3="您填写邮箱已经注册！请修改后重新提交！"
	if (errflag==0):
		#帐号添加
		md5pwd = hashlib.md5(passwd)
		md5pwd = md5pwd.hexdigest()[8:-8]
		value1=[userName,md5pwd,email,gmt_created,gmt_modified]
		sql1="insert into auth_user (username,password,email,gmt_created,gmt_modified) values(%s,%s,%s,%s,%s)"
		dbc.updatetodb(sql1,value1)
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
		company_id=0
		
		value2=[contact, industry_code, business, service_code, area_code, foreign_city, category_garden_id, membership_code,domain, classified_code, regfrom_code,  regtime, gmt_created, gmt_modified,  address, address_zip, website, introduction]
		sql2="insert into company (name, industry_code, business, service_code, area_code, foreign_city, category_garden_id, membership_code,	in, classified_code, regfrom_code,  regtime, gmt_created, gmt_modified,  address, address_zip, website, introduction)"
		sql2=sql2+" values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)";
		result=dbc.updatetodb(sql2,value2)
		if result:
			company_id=result[0]
			#company_id=getcompany_id(contact,gmt_created)
			is_admin='1'
			tel_country_code=''
			tel_area_code=''
			tel=mobile
	
			fax_country_code=''
			fax_area_code=''
			fax=''
			sex=''
			#'添加联系方式
			value3=[userName, company_id, contact, is_admin, tel_country_code, tel_area_code, tel, mobile, fax_country_code, fax_area_code, fax, email, sex, passwd, gmt_modified, gmt_created]
			sql3="insert into company_account (account, company_id, contact, is_admin, tel_country_code, tel_area_code, tel, mobile, fax_country_code, fax_area_code, fax, email, sex, password, gmt_modified, gmt_created)"
			sql3=sql3+" values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)";
			dbc.updatetodb(sql3,value3);
			#-互助用户表
			sqlh="select id from bbs_user_profiler where company_id=%s"
			userlist=dbc.fetchonedb(sqlh,[company_id])
			if (userlist==None):
				value=[company_id,userName,userName,email,tel,mobile,qq,userName,gmt_modified,gmt_created]
				sqlu="insert into bbs_user_profiler(company_id,account,nickname,email,tel,mobile,qq,real_name,gmt_modified,gmt_created) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
				dbc.updatetodb(sqlu,value);
			#-微信绑定
			sql="select id from oauth_access where open_id=%s and target_account=%s"
			accountlist=dbc.fetchonedb(sql,[weixinid,userName]);
			if (accountlist==None):
				sqlp="insert into oauth_access(open_id,open_type,target_account,gmt_created,gmt_modified) values(%s,%s,%s,%s,%s)"
				dbc.updatetodb(sqlp,[weixinid,'weixin.qq.com',userName, gmt_created,gmt_modified]);
				#提醒定制商机
				weixinorder(weixinid)
				#微信绑定获得1次抽奖机会
				choujiang(company_id=company_id,weixinid=weixinid)
			request.session.set_expiry(6000*6000)
			request.session['username']=userName
			request.session['company_id']=company_id
			updatelogin(request,company_id)
			#更新pc端登录状态
			if qrcode and str(qrcode)!='None':
				sqlb="select id from weixin_pclogin where openid=%s and account=%s and qrcode=%s"
				resultc=dbc.fetchonedb(sqlb,[weixinid,account,str(qrcode)])
				if resultc:
					sqlp="update weixin_pclogin set loginflag=1,gmt_created=%s where id=%s"
					dbc.updatetodb(sqlp,[gmt_created,resultc[0]])
				else:
					sqlp="insert into weixin_pclogin (openid,account,loginflag,gmt_created,qrcode) values(%s,%s,%s,%s,%s)"
					dbc.updatetodb(sqlp,[weixinid,account,1,gmt_created,str(qrcode)])
				#微信登录成功提醒
				loginsuctishi(weixinid)
			return render_to_response('new/regsuc.html',locals())
		else:
			errflag=1
	if (errflag==1):
		return render_to_response('new/reg.html',locals())
	
def qqlogin(request):
	return render_to_response('new/qqlogin.html',locals())
#----微信每日商情
def priceday(request):
	#useragent=hashlib.md5(str(request.META.get('HTTP_USER_AGENT',None)))
	return HttpResponseRedirect("/priceindex/")
	nowlanmu="<a href='/priceindex/'>行情报价</a>"
	tt=request.GET.get("t")
	p=request.GET.get("p")
	pricenav=getpricenav()
	tp=request.GET.get("tp")
	if (tp==None):
		tp=1
	ll=[]
	if (p):
		sqlt="select id from price_category where parent_id=%s"
		tlist=dbc.fetchalldb(sqlt,[p])
		for l in tlist:
			ll.append(l[0])
	a=request.GET.get("a")
	t=None
	if a:
		a=int(a)
	if tt:
		t=[int(tt)]
	if ll:
		t=ll
	
	keywords=request.GET.get("keywords")
	if (keywords!=None):
		keywords=keywords.replace("报价","")
		keywords=keywords.replace("价格","")
		webtitle=keywords
	if (str(keywords)=='None'):	
		keywords=None
		webtitle="行情日报"


	pricelistall=getpricelist(keywords=keywords,frompageCount=0,limitNum=20,category_id=t,allnum=20,assist_type_id=a)
	pricelist=pricelistall['list']
	pricelistcount=pricelistall['count']
	if (pricelistcount==1):
		morebutton='style=display:none'
	else:
		morebutton=''
	return render_to_response('price-day.html',locals())
#创建二维码ticket
def getqrcode(request):
	wxc = Client(weixinconfig['zz91service']['appid'], weixinconfig['zz91service']['secret'])
	#return HttpResponse(weixinconfig['zz91service']['appid'])
	data={"action_name": "QR_LIMIT_STR_SCENE", "action_info": {"scene": {"scene_str": "tradesee"}}}
	token=wxc.create_qrcode(data)
	img=wxc.show_qrcode(token['ticket'])
	return HttpResponse("<img src='"+img+"' />")
	#return HttpResponse(img,'image/gif')
	return HttpResponse(json.dumps(token, ensure_ascii=False))
#微信登录二维码
def getloginqrcode(request):
	loginqrcode=request.session.get("loginqrcode",None)
	loginticket=request.session.get("loginticket",None)
	logintime=request.session.get("logintime",None)
	gmt_created=datetime.datetime.now()
	#logintime=None
	if not loginqrcode or not loginticket or not logintime:
		loginqrcode = random.randint(1000000, 99999999)
		#request.session.set_expiry(60*10)
		request.session['loginqrcode']=loginqrcode
	
		wxc = Client(weixinconfig['zz91service']['appid'], weixinconfig['zz91service']['secret'])
		data={"expire_seconds": 700, "action_name": "QR_SCENE", "action_info": {"scene": {"scene_id": loginqrcode}}}
		token=wxc.create_qrcode(data)
		loginticket=token['ticket']
		difmin=0
		request.session['loginticket']=loginticket
		request.session['logintime']=date_to_strall(gmt_created)
		logintime=date_to_strall(gmt_created)
	else:
		gmtnow=getNow()
		'''判断是否是一个有效的日期字符串'''
		try:
			time.strptime(logintime, "%Y-%m-%d")
			logintime=date_to_int(logintime)
		except:
			logintime=str_to_int(logintime)
		difmin=date_to_int(gmtnow)-logintime
		if difmin>600:
			loginqrcode = random.randint(1000000, 99999999)
			request.session['loginqrcode']=loginqrcode
			wxc = Client(weixinconfig['zz91service']['appid'], weixinconfig['zz91service']['secret'])
			data={"expire_seconds": 700, "action_name": "QR_SCENE", "action_info": {"scene": {"scene_id": loginqrcode}}}
			token=wxc.create_qrcode(data)
			loginticket=token['ticket']
			request.session['loginticket']=loginticket
			request.session['logintime']=date_to_strall(gmt_created)
		else:
			loginticket=request.session.get("loginticket",None)
	img="https://mp.weixin.qq.com/cgi-bin/showqrcode?ticket="+loginticket
	list={'img':img,'qrcode':loginqrcode,'createdtime':logintime,'difftime':difmin}
	data=json.dumps(list, ensure_ascii=False)
	return HttpResponse('success_jsonpCallback(' + data + ');')   
	return HttpResponse(json.dumps(list, ensure_ascii=False))
	#return HttpResponse("<img src='"+img+"' code='"+str(loginqrcode)+"' />")
def weixinshare(request):
	host=getnowurl(request)
	nowlanmu="<a href='/huzhu/'>再生互助</a>"
	return render_to_response('zz91weixin/share.html',locals())
