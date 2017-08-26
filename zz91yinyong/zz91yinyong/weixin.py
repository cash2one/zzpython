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
	
from sphinxapi import *
from zz91page import *
from zz91db_ast import companydb
from zz91db_2_news import newsdb
from zz91db_ads import adsdb
from zz91db_ep import adshuanbao

#from jobjoke import luckcheck
dbc=companydb()
dbn=newsdb()
dbads=adsdb()
dbhuanbao=adshuanbao()

reload(sys)
sys.setdefaultencoding('UTF-8')
nowpath=os.path.dirname(__file__)
execfile(nowpath+"/commfunction.py")
execfile(nowpath+"/function.py")
execfile(nowpath+"/func/ldb_weixin_function.py")


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
#----微信端登录
def login(request):
	username=request.session.get("username",None)
	ldb_weixin=ldbweixin()
	weixinid=request.GET.get("weixinid")
	if (weixinid!=""):
		request.session['weixinid']=weixinid
	return render_to_response('new/login.html',locals())
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
						title="感谢关注ZZ91再生网来电宝,从今儿起，您可以在微信上查询“来电宝”话单详单，余额查询，在线充值等业务了啦!\n\n 请先 <a href='http://m.zz91.com/weixin/login.html?weixinid="+str(toUserName)+"'>点击绑定ZZ91再生网帐号</a>\n\n <a href='http://m.zz91.com/weixin/reg.html?weixinid="+str(toUserName)+"'>木有帐号？用3秒钟注册一个</a>"
					xml=backxml(xmltype=2,fromUserName=toUserName,toUserName=fromUserName,title=title)
					return HttpResponse(xml)
				
				if (Event1 == "subscribe" or Event1 == "scan"):
					title="感谢关注ZZ91再生网来电宝,从今儿起，您可以在微信上查询“来电宝”话单详单，余额查询，在线充值等业务了啦!\n\n 请先 <a href='http://m.zz91.com/weixin/login.html?weixinid="+str(toUserName)+"'>点击绑定ZZ91再生网帐号</a>\n\n <a href='http://m.zz91.com/weixin/reg.html?weixinid="+str(toUserName)+"'>木有帐号？用3秒钟注册一个</a>"
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
				request.session.set_expiry(60*60)
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
				useragent=str(request.META.get('HTTP_USER_AGENT',None)).encode('utf8','ignore').encode("hex")
				saveweixincount(request,toUserName,content,keyw,useragent)
				
				postTime = str(int(time.time()))
				
				if (Event1=="VIEW"):
					xml=backxml(xmltype=4,fromUserName=toUserName,toUserName=fromUserName,title=title,Url=EventKey)
					return HttpResponse(xml)
				if (content==None  and (EventKey=='contact' or EventKey=='lucky0')):
					title="服务电话\n\n0571-56611111\n\n0571-56612345\n\n公司地址：浙江省杭州市江干区九盛路9号东方电子商务园13栋\n\n邮编：310019 \n\n传真：0571-56637777\n"
					xml=backxml(xmltype=2,fromUserName=toUserName,toUserName=fromUserName,title=title)
					return HttpResponse(xml)
				if (content==None  and EventKey=='qiandao'):
					
					waccount=weixinbinding(toUserName)
					if waccount:
						gmt_created=datetime.datetime.now()
						morpic="http://img0.zz91.com/zz91/weixin/images/more.jpg"
						titlelist=[{'title':'现在是'+str(formattime(gmt_created,0))+'，点此签到送大礼！','Description':'','PicUrl':'http://img0.zz91.com/zz91/weixin/images/qiandao.gif','Url':'http://m.zz91.com/score/index.html?weixinid='+toUserName+'&qiandao=1'}]
						wcompany_id=getcompanyid(waccount)
						qcout=getleavewordscount(wcompany_id)
						hcount=getmyhuzhureplaycoutno(waccount)
						if (qcout>0):
							tlist={'title':'[询盘] 您有'+str(qcout)+'条新的留言','Description':'','PicUrl':'http://img0.zz91.com/zz91/weixin/images/2.gif','Url':'http://m.zz91.com/myrc_leavewords/?weixinid='+toUserName+''}
							titlelist.append(tlist)
						tlist={'title':'[供求] 查看我定制的供求商机','Description':'','PicUrl':'http://img0.zz91.com/zz91/weixin/images/3.gif','Url':'http://m.zz91.com/myrc_collect/?weixinid='+toUserName+''}
						titlelist.append(tlist)
						tlist={'title':'[行情] 查看那我定制的行情报价','Description':'','PicUrl':'http://img0.zz91.com/zz91/weixin/images/3.gif','Url':'http://m.zz91.com/myrc_collectprice/?weixinid='+toUserName+''}
						titlelist.append(tlist)
						if (hcount>0):
							tlist={'title':'[问答] 互助社区有'+str(hcount)+'人给您回复','Description':'','PicUrl':'http://img0.zz91.com/zz91/weixin/images/4.gif','Url':'http://m.zz91.com/myrc_mycommunity/?weixinid='+toUserName+''}
							titlelist.append(tlist)
						"""
						luckone=luckcheck(toUserName)
						if (luckone):
							id=luckone['id']
							flag=luckone['flag']
							type=luckone['type']
							titletype=""
							if type=="joke":
								titletype="[幽默笑话]"
							if type=="job":
								titletype="[职场]"
							if type=="news":
								titletype="[资讯]"
							title=titletype+luckone['title']
							PicUrl=""
							if (type=='news'):
								Url="http://m.zz91.com/news/newsdetail"+str(id)+".htm?type="+str(type)
							else:
								Url="http://m.zz91.com/otherdetail"+str(id)+".htm?type="+str(type)
							tlist={'title':title,'Description':'','PicUrl':morpic,'Url':Url}
							titlelist.append(tlist)
						"""
					else:
						titlelist=[{'title':'立即绑定帐号，签到送大礼！','Description':'您还未绑定您的ZZ91再生网帐号，绑定后即可立即签到，大礼等着您哦！点此立即绑定。','PicUrl':'http://m.zz91.com/images/gangtan1.jpg','Url':'http://m.zz91.com/weixin/login.html?weixinid='+str(toUserName)+''}]
					
					
					ArticleCount=len(titlelist)
					xml=backxml(xmltype=3,fromUserName=toUserName,toUserName=fromUserName,ArticleCount=ArticleCount,titlelist=titlelist)
					return HttpResponse(xml)
				"""
				if (content==None  and EventKey=='lucky'):
					try:
						luckone=luckcheck(toUserName)
						if (luckone):
							id=luckone['id']
							
							body=luckone['body']
							flag=luckone['flag']
							type=luckone['type']
							titletype=""
							if type=="joke":
								titletype="[幽默笑话]"
							if type=="job":
								titletype="[职场]"
							if type=="news":
								titletype="[资讯]"
							title=titletype+luckone['title']
							PicUrl=""
						
							re_py=r'<img.*?src="([^"]+)"'
							urls_pat=re.compile(re_py)
							img_url=re.findall(urls_pat,body)
							re_py2=r'<IMG.*?src="([^"]+)"'
							urls_pat2=re.compile(re_py2)
							img_url2=re.findall(urls_pat2,body)
							if (img_url):
								PicUrl=img_url
							else:
								if(img_url2):
									PicUrl=img_url2
								else:
									PicUrl=""
						
							pic=""
							Description=""
							Descriptiona=subString(filter_tags(body),200).strip()
							
							if (PicUrl=="" and ("/uploads/uploads/media/" in body)):
								#pic="http://pyapp.zz91.com/app/changepic.html?height=300&width=300&url=http://192.168.110.2:805/"+body
								pic=body
								Description=""
							else:
								if (PicUrl!="" and ("/uploads/uploads/media/" in body)):
									#pic="http://pyapp.zz91.com/app/changepic.html?height=300&width=300&url=http://192.168.110.2:805/"+PicUrl[0]
									pic=PicUrl[0]
									Description=Descriptiona
								else:
									Description=Descriptiona
							
							Description=Description
							if (type=='news'):
								Url="http://m.zz91.com/news/newsdetail"+str(id)+".htm?type="+str(type)
							else:
								Url="http://m.zz91.com/otherdetail"+str(id)+".htm?type="+str(type)
						
							titlelist=[{'title':title,'Description':str(Description),'PicUrl':pic,'Url':Url}]
							ArticleCount=len(titlelist)
						else:
							title="再点我试试！"
							xml=backxml(xmltype=2,fromUserName=toUserName,toUserName=fromUserName,title=title)
							return HttpResponse(xml)
						xml=backxml(xmltype=3,fromUserName=toUserName,toUserName=fromUserName,ArticleCount=ArticleCount,titlelist=titlelist)
						return HttpResponse(xml)
					
					except IOError as e:
						#title=e
						title="再点我试试！"
						xml=backxml(xmltype=2,fromUserName=toUserName,toUserName=fromUserName,title=title)
						return HttpResponse(xml)
				"""
				if (content==None  and EventKey=='pay'):
					title="支付方式\n\nZZ91支付宝帐号：zhifu@zz91.com\n\n开户银行：中国农业银行杭州朝晖支行\n收 款 人：杭州阿思拓信息科技有限公司\n帐　　号：19-0156 0104 0013 383\n\n公司地址：浙江省杭州市江干区九盛路9号东方电子商务园13栋\n\n邮编：310019 \n\n传真：0571-56637777\n"
					xml=backxml(xmltype=2,fromUserName=toUserName,toUserName=fromUserName,title=title)
					return HttpResponse(xml)
				if (content==None  and EventKey=='help'):
					title="使用帮助：\n"
					#title+="ZZ91微信号升级了!\n"
					title+="=================\n"
					title+="除了菜单外\n"
					title+="您还可以：\n"
					title+="查看报价：\n回复：地区+产品+报价 \n如：上海废铝报价、国内PP报价\n"
					title+="查看供求：\n回复：供求+产品名称 \n如：求购PP、供应废铁\n"
					#title+="查看“企业库”，\n回复：企业\n"
					title+="查看再生网“联系方式”，\n回复：联系\n"
					title+="查看再生网“支付方式”，\n回复：支付\n"
					title+="“AQSIQ咨询”，\n回复：aqsiq\n"
					xml=backxml(xmltype=2,fromUserName=toUserName,toUserName=fromUserName,title=title)
					return HttpResponse(xml)
				
				if (content==None  and EventKey=='aqsiq'):
					title="AQSIQ国内收货人证书申请、变更、延续；环保证办理；AQSIQ国外供货商证书申请、变更、延续等请咨询：\n"
					title+="北京市京元物环认证咨询有限公司北京总公司\n"
					title+="联系人：马宏燕 女士\n"
					title+="电话：010-5287 8591 \n 传真：010-5126 3773\n"
					title+="移动电话：18610344990\n"
					title+="E-mail:mhy@aqsiq.com\n"
					title+="QQ: 2851637211\n"
					title+="地址：北京市朝阳区广渠路36号首城国际5号楼B座612\n"
					title+="网址：www.aqsiq.com \n"
					xml=backxml(xmltype=2,fromUserName=toUserName,toUserName=fromUserName,title=title)
					return HttpResponse(xml)
				if (content==None  and EventKey=='forgetpasswd'):
					title="您正在取回密码\n\n<a href='http://m.zz91.com/weixin/forgetpasswd.html?weixinid="+str(toUserName)+"'>点此获得您的密码</a>\n\n或拨打服务电话\n\n0571-56611111\n0571-56612345\n"
					xml=backxml(xmltype=2,fromUserName=toUserName,toUserName=fromUserName,title=title)
					return HttpResponse(xml)
				
				if (content==None  and EventKey=='binding'):
					bd=weixinbinding(toUserName)
					if bd:
						title="您已经绑定了ZZ91再生网帐号，现在就可以进行下面的操作啦～\n\n1.<a href='http://m.zz91.com/myrc_leavewords/?weixinid="+str(toUserName)+"'>我的询价</a>\n\n2.<a href='http://m.zz91.com/myrc_favorite/?weixinid="+str(toUserName)+"'>我的收藏夹</a>\n\n3.<a href='http://m.zz91.com/weixin/tradesearch.html'>商机查询</a>\n" 
					else:
						title="感谢关注ZZ91再生网,从今儿起，ZZ91就可以在微信给亲提供行情和供求商机啦!\n\n 请先 <a href='http://m.zz91.com/weixin/login.html?weixinid="+str(toUserName)+"'>点击绑定ZZ91再生网帐号</a>\n\n <a href='http://m.zz91.com/weixin/reg.html?weixinid="+str(toUserName)+"'>木有帐号？用3秒钟注册一个</a>"
					xml=backxml(xmltype=2,fromUserName=toUserName,toUserName=fromUserName,title=title)
					return HttpResponse(xml)
				
				if (Event1 == "subscribe" or Event1 == "scan"):
					title="感谢关注ZZ91再生网,从今儿起，ZZ91就可以在微信给亲提供行情和供求商机啦!\n\n 请先 <a href='http://m.zz91.com/weixin/login.html?weixinid="+str(toUserName)+"'>点击绑定ZZ91再生网帐号</a>\n\n <a href='http://m.zz91.com/weixin/reg.html?weixinid="+str(toUserName)+"'>木有帐号？用3秒钟注册一个</a>"
					xml=backxml(xmltype=2,fromUserName=toUserName,toUserName=fromUserName,title=title)
					return HttpResponse(xml)
				else:
					title=content
					try:
						if (len(title)==1 and title=="1"):
							tmp = random.randint(100000, 999999)
							gmt_created=datetime.datetime.now()
							open_type="weixin.qq.com"
							target_account="0"
							value=[toUserName,open_type,target_account,tmp,gmt_created,gmt_created]
							sqlp="insert into oauth_access(open_id,open_type,target_account,code,gmt_created,gmt_modified) values(%s,%s,%s,%s,%s,%s)"
							dbc.updatetodb(sqlp,value)
							title="注册验证码："+str(tmp)+"\n十分钟内有效（此验证码在网页端微信验证时使用）"
							xml=backxml(xmltype=2,fromUserName=toUserName,toUserName=fromUserName,title=title)
							return HttpResponse(xml)
						if (title=="支付"):
							title="支付方式\n\nZZ91支付宝帐号：zhifu@zz91.com\n\n开户银行：中国农业银行杭州朝晖支行\n收 款 人：杭州阿思拓信息科技有限公司\n帐　　号：19-0156 0104 0013 383\n\n公司地址：浙江省杭州市江干区九盛路9号东方电子商务园13栋\n\n邮编：310019 \n\n传真：0571-56637777\n"
							xml=backxml(xmltype=2,fromUserName=toUserName,toUserName=fromUserName,title=title)
							return HttpResponse(xml)
						if (title=="联系"):
							title="服务电话\n\n0571-56611111\n\n0571-56612345\n\n公司地址：浙江省杭州市江干区九盛路9号东方电子商务园13栋\n\n邮编：310019 \n\n传真：0571-56637777\n"
							xml=backxml(xmltype=2,fromUserName=toUserName,toUserName=fromUserName,title=title)
							return HttpResponse(xml)
						if (title=="抽奖"):
							title="很遗憾，您没有中奖！"
							xml=backxml(xmltype=2,fromUserName=toUserName,toUserName=fromUserName,title=title)
							return HttpResponse(xml)
						if (("报价" in title) or ("价格" in title)):
							keywords=title.replace("报价","").replace("报价","")
							pricelistall=getpricelist(keywords=keywords,frompageCount=0,limitNum=10,allnum=10)
							if pricelistall:
								pricelist=pricelistall['list']
								if pricelist:
									listall=[]
									for list in pricelist:
										#Description=subString(filter_tags(list['content']),200)
										Description=""
										PicUrl=""
										Url="http://m.zz91.com/priceviews/?id="+str(list['id'])
										list1={'title':list['title'],'Description':Description,'PicUrl':PicUrl,'Url':Url}
										listall.append(list1)
									ArticleCount=str(len(listall))
									#listall=[{'title':"sdfsdf",'Description':'dfsdfs','PicUrl':'','Url':''}]
									xml=backxml(xmltype=3,fromUserName=toUserName,toUserName=fromUserName,ArticleCount=ArticleCount,titlelist=listall)
									return HttpResponse(xml)
								else:
									title="没有找到你搜索的报价，有问题可以咨询服务电话\n\n0571-56611111\n\n0571-56612345\n\n"
									xml=backxml(xmltype=2,fromUserName=toUserName,toUserName=fromUserName,title=title)
									return HttpResponse(xml)
							
							else:
								title="没有找到你搜索的报价，有问题可以咨询服务电话\n\n0571-56611111\n\n0571-56612345\n\n"
								xml=backxml(xmltype=2,fromUserName=toUserName,toUserName=fromUserName,title=title)
								return HttpResponse(xml)
						if title=="aqsiq":
							title="AQSIQ国内收货人证书申请、变更、延续；环保证办理；AQSIQ国外供货商证书申请、变更、延续等请咨询：\n"
							title+="北京市京元物环认证咨询有限公司北京总公司\n"
							title+="联系人：马宏燕 女士\n"
							title+="电话：010-5287 8591 \n 传真：010-5126 3773\n"
							title+="移动电话：18610344990\n"
							title+="E-mail:mhy@aqsiq.com\n"
							title+="QQ: 2851637211\n"
							title+="地址：北京市朝阳区广渠路36号首城国际5号楼B座612\n"
							title+="网址：www.aqsiq.com \n"
							xml=backxml(xmltype=2,fromUserName=toUserName,toUserName=fromUserName,title=title)
							return HttpResponse(xml)
				
						if (("供应" in title) or ("求购" in title)):
							pdt_type=None
							if ("供应" in title):
								pdt_type=1
							if ("求购" in title):
								pdt_type=2
							
							keywords=title.replace("求购","").replace("供应","")
							if keywords=="":
								keywords=None
							offerlistall=getindexofferlist_pic(keywords,pdt_type,10,havepic=None)
							
							if offerlistall:
								listall=[]
								for list in offerlistall:
									#Description=subString(filter_tags(list['content']),200)
									Description=""
									PicUrl=list['pdt_images']
									kindtxt=list['kindtxt']
									gmt_time=list['gmt_time']
									Url="http://m.zz91.com/detail/?id="+str(list['id'])
									list1={'title':kindtxt+list['title'],'Description':Description,'PicUrl':PicUrl,'Url':Url}
									listall.append(list1)
								ArticleCount=str(len(listall))
								#listall=[{'title':"sdfsdf",'Description':'dfsdfs','PicUrl':'','Url':''}]
								xml=backxml(xmltype=3,fromUserName=toUserName,toUserName=fromUserName,ArticleCount=ArticleCount,titlelist=listall)
								return HttpResponse(xml)
							else:
								title="没有找到你搜索的供求信息，有问题可以咨询服务电话\n\n0571-56611111\n\n0571-56612345\n\n"
								xml=backxml(xmltype=2,fromUserName=toUserName,toUserName=fromUserName,title=title)
								return HttpResponse(xml)
						else:
							title="使用帮助：\n"
							#title+="ZZ91微信号升级了!\n"
							title+="=================\n"
							title+="除了菜单外\n"
							title+="您还可以：\n"
							title+="查看报价：\n回复：地区+产品+报价 \n如：上海废铝报价、国内PP报价\n"
							title+="查看供求：\n回复：供求+产品名称 \n如：求购PP、供应废铁\n"
							#title+="查看“企业库”，\n回复：企业\n"
							title+="查看再生网“联系方式”，\n回复：联系\n"
							title+="查看再生网“支付方式”，\n回复：支付\n"
							title+="“AQSIQ咨询”，\n回复：aqsiq\n"
							xml=backxml(xmltype=2,fromUserName=toUserName,toUserName=fromUserName,title=title)
							return HttpResponse(xml)
					except:
						title="很抱歉，网络忙！，你可以点击其他菜单试试！"
						#title="您好，您已经超过了500名，很遗憾您没有获得话费，但是您获得了第二天抽奖资格，祝您好运，感谢您的参与。"
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
				request.session.set_expiry(60*60)
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
					#title="感谢关注ZZ91再生网,从今儿起，ZZ91就可以在微信给亲提供行情和供求商机啦!\n\n 请先 <a href='http://m.zz91.com/weixin/login.html?weixinid="+str(toUserName)+"'>点击绑定ZZ91再生网帐号</a>\n\n <a href='http://m.zz91.com/weixin/reg.html?weixinid="+str(toUserName)+"'>木有帐号？发3秒钟注册一个</a>"
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
#----ZZ91微信验证提示
def zz91weixin_yzfront(request):
	account= request.GET.get("account")
	flag=request.GET.get("flag")
	scriptvalue="document.write(\"<div class=tishi>您的账号还未进行微信验证，请<a href='javascript:onclick=openweixinyz()'>点此立即验证</a></div>\")"
	sql="select id from oauth_access where target_account=%s and open_type='weixin.qq.com'"
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
#----发手机短信
def postsms(mobile,username,userid):
	sqlp="select count(id) from auth_forgot_password where username=%s and DATEDIFF(CURDATE(),gmt_created)<1"
	plist=dbc.fetchonedb(sqlp,[username]);
	if (int(plist[0])<5):
		if (int(plist[0])<3):
			tmp = random.randint(10000, 99999)
			content="欢迎使用ZZ91再生网服务。验证码是："+str(tmp)+",输入验证码继续完成操作，该验证码12小时内输入有效。"
			url="http://mt.10690404.com/send.do?Account=hzasto&Password=123456&Mobile="+str(mobile)+"&Content="+content+"&Exno=0"
			f = urllib.urlopen(url)
			html = f.read()
			#html='{"message":"提交成功","code":"1003","reNum":0}'
			o = json.loads(html)
			gmt_created=datetime.datetime.now()
			sql="insert into auth_forgot_password(username,userid,auth_key,gmt_created) values(%s,%s,%s,%s)"
			dbc.updatetodb(sql,[username,userid,tmp,gmt_created]);
			if (o['message']=='提交成功'):
				return True
			else:
				return o['message']
		else:
			return True
	else:
		return "您已经超过了每天发生5条短信的限制！"
#-----忘记密码	
def forgetpasswd(request):
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
			dbc.updatetodb(sql,[md5pwd,mobile,account,gmt_modified]);
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
	userName = request.POST['userName']
	passwd = request.POST['passwd']
	weixinid = request.POST['weixinid']
	md5pwd = hashlib.md5(passwd)
	md5pwd = md5pwd.hexdigest()[8:-8]
	gmt_created=datetime.datetime.now()
	gmt_modified=datetime.datetime.now()
	sql="select id,username from auth_user where (username=%s or email=%s) and password=%s"
	plist=dbc.fetchonedb(sql,[userName,userName,md5pwd]);
	if plist:
		request.session.set_expiry(6000*6000)
		account=plist[1]
		
		
		sqlc="select company_id from company_account where account=%s"
		list=dbc.fetchonedb(sqlc,[account]);
		if list:
			request.session['username']=account
			request.session['company_id']=list[0]
			updatelogin(request,list[0])
			sqlc="select id from oauth_access where open_id=%s and target_account=%s"
			list=dbc.fetchonedb(sqlc,[str(weixinid),account])
			if list:
				aaa="b"
				return render_to_response('new/loginsuc.html',locals())
			else:
				sql="insert into oauth_access(open_id,open_type,target_account,gmt_created,gmt_modified) values(%s,%s,%s,%s,%s)"
				dbc.updatetodb(sql,[weixinid,'weixin.qq.com',account,gmt_created,gmt_modified])
				aaa="a"
		else:
			error="用户名或邮箱 还未在ZZ91注册！"
			return render_to_response('new/login.html',locals())
	else:
		sqlc="select account,company_id from company_account where mobile=%s order by id desc"
		list=dbc.fetchonedb(sqlc,[userName]);
		if list:
			account=list[0]
			company_id=list[1]
			sqlp="select id from auth_user where username=%s and password=%s"
			listp=dbc.fetchonedb(sqlp,[account,md5pwd]);
			if listp:
				request.session.set_expiry(6000*6000)
				request.session['username']=account
				request.session['company_id']=company_id
				updatelogin(request,company_id)
				sqlc="select id from oauth_access where open_id=%s and target_account=%s"
				listw=dbc.fetchonedb(sqlc,[weixinid,account]);
				if listw:
					return render_to_response('new/loginsuc.html',locals())
				else:
					sql="insert into oauth_access(open_id,open_type,target_account,gmt_created,gmt_modified) values(%s,%s,%s,%s,%s)"
					dbc.updatetodb(sql,[weixinid,'weixin.qq.com',account,gmt_created,gmt_modified])
			else:
				error="用户名或密码错误！"
				return render_to_response('new/login.html',locals())
		else:
			error="密码错误或你填写的手机/用户名还未注册"
			return render_to_response('new/login.html',locals())
	return render_to_response('new/loginsuc.html',locals())
#----注册保存
def regsave(request):
	userName = request.POST['userName']
	passwd = request.POST['passwd']
	qq = request.POST['qq']
	email = request.POST['email']
	contact = request.POST['contact']
	weixinid = request.POST['weixinid']
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
		
		value2=[contact, industry_code, business, service_code, area_code, foreign_city, category_garden_id, membership_code,domain, classified_code, regfrom_code,  regtime, gmt_created, gmt_modified,  address, address_zip, website, introduction]
		sql2="insert into company (name, industry_code, business, service_code, area_code, foreign_city, category_garden_id, membership_code,    domain, classified_code, regfrom_code,  regtime, gmt_created, gmt_modified,  address, address_zip, website, introduction)"
		sql2=sql2+" values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)";
		dbc.updatetodb(sql2,value2)
		
		company_id=getcompany_id(contact,gmt_created)
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
		return render_to_response('new/regsuc.html',locals())
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