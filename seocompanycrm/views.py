#-*- coding:utf-8 -*-
from django.shortcuts import render_to_response
from django.http import HttpResponse,HttpResponseRedirect
from zz91page import *
import datetime,time,urllib,urllib2,re,os,MySQLdb
nowpath=os.path.dirname(__file__)
execfile(nowpath+"/conn.py")
execfile(nowpath+"/function.py")
conn=database()
cursor = conn.cursor()

def uppassword(request):
	username=request.session.get('username')
	if not username:
		return HttpResponseRedirect('/loginpage/')
	usertype=request.session.get('usertype')
	if usertype in ['seouser','salesman']:
		seouser_id=str(request.session.get('userid'))
		seouser_name=getseoname(seouser_id)
		seo_password=getseo_password(seouser_id)
	seo_id=request.GET.get('seo_id')
	request_url = request.META.get('HTTP_REFERER', '/')
	return render_to_response('uppassword.html',locals())

#----首页
def default(request):
	username=request.session.get('username')
	if not username:
		return HttpResponseRedirect('/loginpage/')
	usertype=request.session.get('usertype')
	index='1'
	return render_to_response('index2.html',locals())
def contact(request):
	return render_to_response('contact.html',locals())
#----添加公司
def addcompany(request):
	username=request.session.get('username')
	usertype=request.session.get('usertype')
	addkeywords=request.GET.get('addkeywords')
	if usertype=='seouser':
		seouser_id=str(request.session.get('userid'))
		seouser_name=getseoname(seouser_id)
	list_company=get_company(0,5)
	seouser=get_seouser()
	begintime=time.strftime('%Y-%m-%d',time.localtime(time.time()))
	return render_to_response('addcompany2.html',locals())
#----修改公司
def updatecompany(request):
	username=request.session.get('username')
	request_url = request.META.get('HTTP_REFERER', '/')
	company_id=request.GET.get('company_id')
	company_detail=getcompany_detail(company_id)
	company_id=int(company_id)
	name=company_detail['name']
	mobile=company_detail['mobile']
	mail=company_detail['mail']
	contact=company_detail['contact']
	list_company=get_company(0,5)
	return render_to_response('company2.html',locals())

def returnpage(request):
	request_url=request.GET.get('request_url')
	return HttpResponseRedirect(request_url)

#----添加关键字
def addkeywords(request):
	username=request.session.get('username')
	usertype=request.session.get('usertype')
	addkeywords=request.GET.get('addkeywords')
	if usertype=='seouser':
		seouser_id=str(request.session.get('userid'))
		seouser_name=getseoname(seouser_id)
	company_id=request.GET.get('company_id')
	begintime=time.strftime('%Y-%m-%d',time.localtime(time.time()))
	list_company=get_company(0,5)
	seouser=get_seouser()
	return render_to_response('addkeywords2.html',locals())

#----公司列表
def company(request):
	username=request.session.get('username')
	if not username:
		return HttpResponse('页面超时,请刷新..')
	salesman_id=''
	seouser=get_seouser()
	usertype=request.session.get('usertype')
	seouser_id=request.GET.get('seo_id')
	if usertype=='seouser':
		seouser_id=str(request.session.get('userid'))
	if seouser_id:
		seouser_name=getseoname(seouser_id)
	if usertype=='salesman':
		salesman_id=str(request.session.get('userid'))
	company_name=request.GET.get('company_name')
	mobile=request.GET.get('mobile')
	if usertype=='company':
		mobile=username
	mail=request.GET.get('mail')
	contact=request.GET.get('contact')
	chargetype=request.GET.get('chargetype')
	company_type=request.GET.get('company_type')
	if not company_type:
		company_type='2'
	#翻页参数
	searchlist={}
	if chargetype:
		searchlist['chargetype']=chargetype
	if company_name:
		searchlist['company_name']=company_name.encode('utf8')
	if mail:
		searchlist['mail']=mail
	if mobile:
		searchlist['mobile']=mobile
	if company_type:
		searchlist['company_type']=company_type
	searchurl=urllib.urlencode(searchlist)
	
	page=request.GET.get('page')
	if (page==None or page==0):
		page=1
	funpage=zz91page()
	limitNum=funpage.limitNum(15)
	nowpage=funpage.nowpage(int(page))
	frompageCount=funpage.frompageCount()
	after_range_num = funpage.after_range_num(5)
	before_range_num = funpage.before_range_num(4)
	list_company=get_company(frompageCount,limitNum,chargetype,company_type,company_name,mobile,mail,contact,seouser_id,salesman_id)
	listcount=0
	if (list_company):
		listall=list_company['list']
		listcount=list_company['count']
		if (int(listcount)>1000000):
			listcount=1000000-1
	listcount = funpage.listcount(listcount)
	page_listcount=funpage.page_listcount()
	firstpage = funpage.firstpage()
	lastpage = funpage.lastpage()
	page_range  = funpage.page_range()
	nextpage = funpage.nextpage()
	prvpage = funpage.prvpage()
	return render_to_response('company2.html',locals())

#----关键词分配给seo
def assigntoseo(request):
	request_url = request.META.get('HTTP_REFERER', '/')
	seo_id=request.GET.get('seo_id')
	seo_name=getseoname(seo_id)
	klist=request.GET.getlist('checkAll')
	if seo_id and klist:
		for kl in klist:
			sql='update seo_keywords set seouser_id=%s where id=%s'
			inserintodb(sql,[seo_id,kl])
	return HttpResponseRedirect(request_url)
#----关键词分配给销售
def assigntosales(request):
	request_url = request.META.get('HTTP_REFERER', '/')
	seo_id=request.GET.get('seo_id')
	seo_name=getseoname(seo_id)
	klist=request.GET.getlist('checkAll')
	if seo_id and klist:
		for kl in klist:
			sql='update seo_keywords set salesman_id=%s where id=%s'
			inserintodb(sql,[seo_id,kl])
	return HttpResponseRedirect(request_url)

#----公司分配给seo
def assigntoseocomp(request):
	request_url = request.META.get('HTTP_REFERER', '/')
	seo_id=request.GET.get('seo_id')
	seo_name=getseoname(seo_id)
	klist=request.GET.getlist('checkAll')
	if seo_id and klist:
		for kl in klist:
			sql='update seo_keywords set seouser_id=%s where company_id=%s'
			inserintodb(sql,[seo_id,kl])
	return HttpResponseRedirect(request_url)
#----多选删除关键词
def choicedelete(request):
	request_url = request.META.get('HTTP_REFERER', '/')
	klist=request.GET.getlist('checkAll')
	if klist:
		for kl in klist:
			sql='update seo_keywords set isdelete=1 where id=%s'
			inserintodb(sql,[kl])
	return HttpResponseRedirect(request_url)
#----多选关键词丢单
def choicelost(request):
	request_url = request.META.get('HTTP_REFERER', '/')
	klist=request.GET.getlist('checkAll')
	if klist:
		for kl in klist:
			sql='update seo_keywords set islost=1 where id=%s'
			inserintodb(sql,[kl])
	return HttpResponseRedirect(request_url)
#----多选公司丢单
def choicelostcomp(request):
	request_url = request.META.get('HTTP_REFERER', '/')
	klist=request.GET.getlist('checkAll')
	if klist:
		for kl in klist:
			sql='update seo_company set islost=1 where id=%s'
			inserintodb(sql,[kl])
			sql='update seo_keywords set islost=1 where company_id=%s'
			inserintodb(sql,[kl])
	return HttpResponseRedirect(request_url)
#----多选还原关键词
def choicereduction(request):
	request_url = request.META.get('HTTP_REFERER', '/')
	klist=request.GET.getlist('checkAll')
	if klist:
		for kl in klist:
			sql='update seo_keywords set isdelete=0 where id=%s'
			inserintodb(sql,[kl])
	return HttpResponseRedirect(request_url)
#----多选还原关键词丢单
def choicereductionlost(request):
	request_url = request.META.get('HTTP_REFERER', '/')
	klist=request.GET.getlist('checkAll')
	if klist:
		for kl in klist:
			sql='update seo_keywords set islost=0 where id=%s'
			inserintodb(sql,[kl])
	return HttpResponseRedirect(request_url)
#----多选还原公司丢单
def choicereductioncomp(request):
	request_url = request.META.get('HTTP_REFERER', '/')
	klist=request.GET.getlist('checkAll')
	if klist:
		for kl in klist:
			sql='update seo_company set islost=0 where id=%s'
			inserintodb(sql,[kl])
			sql='update seo_keywords set islost=0 where company_id=%s'
			inserintodb(sql,[kl])
	return HttpResponseRedirect(request_url)

#----关键字列表
def keywords(request):
	username=request.session.get('username')
	if not username:
		return HttpResponse('页面超时,请刷新..')
	update=request.GET.get('update')
	sortrank=request.GET.get('sortrank')
	if not sortrank:
		sortrank='7'
	usertype=request.session.get('usertype')
	seouser_id=request.GET.get('seo_id')
	if usertype=='seouser':
		seouser_id=str(request.session.get('userid'))
	if seouser_id:
		seouser_name=getseoname(seouser_id)
	begintime=request.GET.get('begintime')
	begintime2=request.GET.get('begintime2')
	seouser=get_seouser()
	salesuser=get_salesuser()
	sales_id=request.GET.get('sales_id')
	if usertype=='salesman':
		sales_id=str(request.session.get('userid'))
	if sales_id:
		sales_name=getseoname(sales_id)
	chargetype=request.GET.get('chargetype')
	keywords_type=request.GET.get('keywords_type')
	if not keywords_type:
		keywords_type='8'
	keywords=request.GET.get('keywords')
	shopsaddress=request.GET.get('shopsaddress')
	mail=request.GET.get('mail')
	company_name=request.GET.get('company_name')
	mobile=request.GET.get('mobile')
	if usertype=='company':
		mobile=username
	#翻页参数
	searchlist={}
	if sortrank:
		searchlist['sortrank']=sortrank
	if chargetype:
		searchlist['chargetype']=chargetype
	if keywords:
		searchlist['keywords']=keywords.encode('utf8')
	if company_name:
		searchlist['company_name']=company_name.encode('utf8')
	if mail:
		searchlist['mail']=mail
	if mobile:
		searchlist['mobile']=mobile
	if shopsaddress:
		searchlist['shopsaddress']=shopsaddress
	if keywords_type:
		searchlist['keywords_type']=keywords_type
	if seouser_id:
		searchlist['seo_id']=seouser_id
	if sales_id:
		searchlist['sales_id']=sales_id
	if begintime:
		searchlist['begintime']=begintime
	if begintime2:
		searchlist['begintime2']=begintime2
	searchurl=urllib.urlencode(searchlist)
	
	page=request.GET.get('page')
	page_listcount=request.GET.get('page_listcount')
	if (page==None or page=='' or page=='0'):
		page=1
	elif page.isdigit()==False:
		page=1
	if page_listcount and int(page)>int(page_listcount):
		page=page_listcount
	funpage=zz91page()
	limitNum=funpage.limitNum(30)
	nowpage=funpage.nowpage(int(page))
	frompageCount=funpage.frompageCount()
	after_range_num = funpage.after_range_num(3)
	before_range_num = funpage.before_range_num(6)
	list_keywords=get_keywords(frompageCount,limitNum,chargetype,keywords_type,sortrank,keywords,seouser_id,shopsaddress,begintime,begintime2,company_name,mail,mobile,sales_id)
	listcount=0
	listcount1=0
	if (list_keywords):
		listall=list_keywords['list']
		listcount=list_keywords['count']
		listcount1=list_keywords['count1']
		if (int(listcount)>1000000):
			listcount=1000000-1
	listcount = funpage.listcount(listcount)
	page_listcount=funpage.page_listcount()
	firstpage = funpage.firstpage()
	lastpage = funpage.lastpage()
	page_range  = funpage.page_range()
	if len(page_range)>7:
		page_range=page_range[:7]
	nextpage = funpage.nextpage()
	prvpage = funpage.prvpage()
	if begintime==None:
		begintime=''
	if begintime2==None:
		begintime2=''
	if update and seouser_id:
		sql='select id from seo_keywords where seouser_id='+seouser_id
		resultlist=fetchalldb(sql)
		if resultlist:
			for result in resultlist:
				id=result[0]
				updaterankings(str(id))
	return render_to_response('keywords2.html',locals())

#----添加销售人员
def addsalesman(request):
	username=request.session.get('username')
	if not username:
		return HttpResponse('页面超时,请刷新..')
	salesuser=get_salesuser()
	salesadmins=2
	return render_to_response('useradmin/addsalesman.html',locals())
def addsalesmanok(request):
	username=request.session.get('username')
	salesuser=get_salesuser()
	salesadmins=2
	seouser_name=request.GET.get('seouser_name')
	seo_username=request.GET.get('seo_username')
	seo_password=request.GET.get('seo_password')
	error='不能为空'
	errors=''
	if not seouser_name:
		error1=error
		errors=1
	if seouser_name:
		seouser_name2=seouser_name.replace(' ','')
		sql='select id from seo_user where name="'+seouser_name2+'"'
		result=fetchnumberdb(sql)
		if result!=0:
			error1='此姓名已存在'
	if not seo_username:
		error2=error
		errors=1
	if seo_username:
		seo_username=seo_username.replace(' ','')
		sql='select id from seo_user where username="'+seo_username+'"'
		result=fetchnumberdb(sql)
		if result!=0:
			error2='此帐号已存在'
			errors=1
	if not seo_password:
		error3=error
		errors=1
	if errors:
		return render_to_response('useradmin/addsalesman.html',locals())
	seouser_name2=seouser_name.replace(' ','')
	sql='insert into seo_user(name,username,password,type) values(%s,%s,%s,2)'
	inserintodb(sql,[seouser_name2,seo_username,seo_password])
	return HttpResponseRedirect('/salesman/')
def updatesalesman(request):
	username=request.session.get('username')
	seo_id=request.GET.get('seouser_id')
	seo_detail=getseodetail(seo_id)
	seo_name=seo_detail['name']
	seo_uname=seo_detail['username']
	seo_pword=seo_detail['password']
	salesuser=get_salesuser()
	salesadmins=2
	updateseouser=2
	return render_to_response('useradmin/addsalesman.html',locals())
def updatesalesmanok(request):
	seo_id=request.GET.get('seo_id')
	seo_password=request.GET.get('seo_password')
	if seo_password=='':
		return HttpResponseRedirect('/addsalesman/')
	sql2='update seo_user set password=%s where id=%s'
	inserintodb(sql2,[seo_password,seo_id])
	return HttpResponseRedirect('/salesman/')
#----修改密码
def updatepassword(request):
	request_url = request.META.get('HTTP_REFERER', '/')
	request.session['request_url']=request_url
	seouser_id=str(request.session.get('userid'))
	usertype=request.session.get('usertype')
	if usertype=='seouser' or usertype=='salesman':
		return render_to_response('useradmin/updatepassword.html',locals())
	else:
		return HttpResponseRedirect(request_url)
#----完成修改密码
def updatepasswordok(request):
	request_url=request.session['request_url']
	originalpassword=request.GET.get('originalpassword')
	password=request.GET.get('password')
	repassword=request.GET.get('repassword')
	seouser_id=request.GET.get('seouser_id')
	errors=''
	error='不能为空'
	if password!=repassword:
		error1='两次输入密码不一致'
		error2=error1
	if not password:
		error1=error
		errors=1
	if not repassword:
		error2=error
		errors=1
	if originalpassword:
		sql='select id from seo_user where password=%s and id=%s'
		result=fetchonedb(sql,[originalpassword,seouser_id])
		if not result:
			error3='原密码不正确'
			errors=1
	else:
		error3=error
		errors=1
	if errors:
		return render_to_response('useradmin/updatepassword.html',locals())
	sql2='update seo_user set password=%s where id=%s'
	inserintodb(sql2,[password,seouser_id])
	return HttpResponseRedirect(request_url)

#----添加seo人员
def addseouser(request):
	username=request.session.get('username')
	if not username:
		return HttpResponse('页面超时,请刷新..')
	seouser=get_seouser()
	seoadmins=1
	return render_to_response('useradmin/addseouser2.html',locals())

def updateseouser(request):
	username=request.session.get('username')
	seo_id=request.GET.get('seouser_id')
	seo_detail=getseodetail(seo_id)
	seo_name=seo_detail['name']
	seo_uname=seo_detail['username']
	seo_pword=seo_detail['password']
	seoadmins=1
	updateseouser=1
	seouser=get_seouser()
	username=request.session.get('username')
	return render_to_response('useradmin/addseouser2.html',locals())

def updateseouserok(request):
	request_url=request.GET.get('request_url')
	seo_id=request.GET.get('seo_id')
	seo_password=request.GET.get('seo_password')
	if seo_password=='':
		return HttpResponseRedirect('/seouser/')
	sql2='update seo_user set password=%s where id=%s'
	inserintodb(sql2,[seo_password,seo_id])
	return HttpResponseRedirect(request_url)

def delseouser(request):
	seouser_id=request.GET.get('seouser_id')
	sql='delete from seo_user where id=%s'
	inserintodb(sql,[seouser_id])
	request_url = request.META.get('HTTP_REFERER', '/')
	return HttpResponseRedirect(request_url)

def addseouserok(request):
	username=request.session.get('username')
	seouser=get_seouser()
	seouser_name=request.GET.get('seouser_name')
	seo_username=request.GET.get('seo_username')
	seo_password=request.GET.get('seo_password')
	error='不能为空'
	errors=''
	if not seouser_name:
		error1=error
		errors=1
	if seouser_name:
		seouser_name2=seouser_name.replace(' ','')
		sql='select id from seo_user where name="'+seouser_name2+'"'
		result=fetchnumberdb(sql)
		if result!=0:
			error1='此姓名已存在'
	if not seo_username:
		error2=error
		errors=1
	if seo_username:
		seo_username=seo_username.replace(' ','')
		sql='select id from seo_user where username="'+seo_username+'"'
		result=fetchnumberdb(sql)
		if result!=0:
			error2='此帐号已存在'
			errors=1
	if not seo_password:
		error3=error
		errors=1
	if errors:
		return render_to_response('useradmin/addseouser.html',locals())
	seouser_name2=seouser_name.replace(' ','')
	sql='insert into seo_user(name,username,password,type) values(%s,%s,%s,1)'
	inserintodb(sql,[seouser_name2,seo_username,seo_password])
	return HttpResponseRedirect('/seouser/')

#----手点更新排名
def updateranking(request):
	request_url = request.META.get('HTTP_REFERER', '/')
	keywords_id=request.GET.get('keywords_id')
	baidu_ranking=updaterankings(keywords_id)
	return HttpResponse(str(baidu_ranking))
#----查看历史排名
def rankinghistory(request):
	keywords_id=request.GET.get('keywords_id')
	sql='select id,gmt_created,baidu_ranking,update_time from seo_rankinghistory where keywords_id='+keywords_id+' order by gmt_created desc'
	resultlist=fetchalldb(sql)
	list_ranking=[]
	if resultlist:
		for result in resultlist:
			gmt_created=result[1].strftime('%Y-%m-%d')
			update_time=formattime(result[3],0)
			list={'id':result[0],'gmt_created':gmt_created,'baidu_ranking':result[2],'update_time':update_time}
			list_ranking.append(list)
	return render_to_response('rankinghistory.html',locals())
#----关键词备注
def keywordsremarks(request):
	username=request.session.get('username')
	usertype=request.session.get('usertype')
	keywords_id=request.GET.get('keywords_id')
	remarks_list=getremarkslist(keywords_id)
	errors1=''
	errors2=''
	seouser=get_seouser()
	gmt_created=datetime.datetime.now()
	seouser_id=request.GET.get('seouser_id')
	if usertype=='seouser':
		seouser_id=str(request.session.get('userid'))
	seouser_name=getseoname(seouser_id)
	if not seouser_id:
		errors1='请选择优化人员 '
	company_id=getcompany_id(keywords_id)
	remarks=request.GET.get('remarks')
	if not remarks:
		errors2='请填写备注内容 '
	if errors1 or errors2:
		return render_to_response('keywordsremarks.html',locals())
	argument=[company_id,keywords_id,remarks,seouser_id,gmt_created]
	sql='insert into seo_remarks(company_id,keywords_id,remarks,seouser_id,gmt_created) values(%s,%s,%s,%s,%s)'
	inserintodb(sql,argument)
	return HttpResponseRedirect('/keywordsremarks/?keywords_id='+keywords_id)

#----修改备注
def updateremarks(request):
	remarks_id=request.GET.get('remarks_id')
	remarksdir=getremarks(remarks_id)
	remarks=remarksdir['remarks']
	keywords_id=remarksdir['keywords_id']
	return render_to_response('keywordsremarks.html',locals())
	
def updateremarksok(request):
	remarks_id=request.GET.get('remarks_id')
	keywords_id=request.GET.get('keywords_id')
	remarks=request.GET.get('remarks')
	argument=[remarks,remarks_id]
	sql='update seo_remarks set remarks=%s where id=%s'
	inserintodb(sql,argument)
	return HttpResponseRedirect('/keywordsremarks/?keywords_id='+keywords_id)
#----修改关键字
def updatekeywords(request):
	username=request.session.get('username')
	request_url = request.META.get('HTTP_REFERER', '/')
	seouser=get_seouser()
	keywords_id=request.GET.get('keywords_id')
	keywords_detail=getkeywords_detail(keywords_id)
	keywords=keywords_detail['keywords']
	begintime=keywords_detail['begintime']
	standardtime=keywords_detail['standardtime']
	isstandard=str(keywords_detail['isstandard'])
	if not standardtime:
		standardtime=''
	expire_time=keywords_detail['expire_time']
	if not expire_time:
		expire_time=''
	standarddemand=keywords_detail['standarddemand']
	shopsaddress=keywords_detail['shopsaddress']
	chargetype=keywords_detail['chargetype']
	price=keywords_detail['price']
	years=keywords_detail['years']
	unit_price=keywords_detail['unit_price']
	seouser_id=keywords_detail['seouser_id']
	seouser_name=getseoname(seouser_id)
	return render_to_response('updatekeywords2.html',locals())
#----删除关键字
def delkeywords(request):
	keywords_id=request.GET.get('keywords_id')
	sql='update seo_keywords set isdelete=1 where id=%s'
	inserintodb(sql,[keywords_id])
	request_url = request.META.get('HTTP_REFERER', '/')
	return HttpResponseRedirect(request_url)
#----删除公司
def delcompany(request):
	company_id=request.GET.get('company_id')
	sql='update seo_company set isdelete=1 where id=%s'
	inserintodb(sql,[company_id])
	sql='update seo_keywords set isdelete=1 where company_id=%s'
	inserintodb(sql,[company_id])
	request_url = request.META.get('HTTP_REFERER', '/')
	return HttpResponseRedirect(request_url)
#	return HttpResponseRedirect('/keywords/')
#----还原删除的关键字
def reductionkeywords(request):
	keywords_id=request.GET.get('keywords_id')
	sql='update seo_keywords set isdelete=0 where id=%s'
	inserintodb(sql,[keywords_id])
	request_url = request.META.get('HTTP_REFERER', '/')
	return HttpResponseRedirect(request_url)
#----还原删除的公司
def reductioncompany(request):
	company_id=request.GET.get('company_id')
	sql='update seo_company set isdelete=0 where id=%s'
	inserintodb(sql,[company_id])
	sql='update seo_keywords set isdelete=0 where company_id=%s'
	inserintodb(sql,[company_id])
	request_url = request.META.get('HTTP_REFERER', '/')
	return HttpResponseRedirect(request_url)

#----保存公司信息
def addcompanyok(request):
	request_url=request.GET.get('request_url')
	username=request.session.get('username')
	usertype=request.session.get('usertype')
	company_id=request.GET.get('company_id')
	list_company=get_company(0,5)
	name=request.GET.get('name')
	mobile=request.GET.get('mobile')
	mail=request.GET.get('mail')
	contact=request.GET.get('contact')
	keywords=request.GET.get('keywords')
	standarddemand=request.GET.get('standarddemand')
	begintime=request.GET.get('begintime')
	if not begintime:
		begintime=time.strftime('%Y-%m-%d',time.localtime(time.time()))
	shopsaddress=request.GET.get('shopsaddress')
	chargetype=request.GET.get('chargetype')
	price=request.GET.get('price')
	years=request.GET.get('years')
	days=request.GET.get('days')
	unit_price=request.GET.get('unit_price')
	seouser=get_seouser()
	seouser_id=request.GET.get('seouser_id')
	seouser_name=getseoname(seouser_id)
	
	error1=''
	error2=''
	error3=''
	error4=''
	error=u'不能为空'
	errors=''
	if company_id:
		if not name:
			error1=error
			errors=1
		if not mobile:
			error2=error
			errors=1
		if not mail:
			error3=error
			errors=1
		if not contact:
			error4=error
			errors=1
	else:
		if name:
			sql='select id from seo_company where name="'+name+'"'
			result=fetchnumberdb(sql)
			if result!=0:
				error1='此公司已存在'
				errors=1
		else:
			error1=error
			errors=1
		if mobile:
			if len(mobile)!=11 or mobile.isdigit()==False:
				error2=u'手机号码不正确'
				errors=1
			sql='select id from seo_company where mobile="'+mobile+'"'
			result=fetchnumberdb(sql)
			if result!=0:
				error2='此手机号已存在'
				errors=1
		else:
			error2=error
			errors=1
		if mail:
			if u'@' not in mail:
				error3=u'请输出正确的邮箱地址'
				errors=1
			else:
				sql='select id from seo_company where mail="'+mail+'"'
				result=fetchnumberdb(sql)
				if result!=0:
					error3='此邮箱已存在'
					errors=1
		else:
			error3=error
			errors=1
		if not contact:
			error4=error
			errors=1
		error10=''
		error11=''
		error12=''
		error13=''
		error14=''
		error15=''
		error16=''
		error17=''
		if not keywords:
			error17=error
			errors=1
		if not begintime:
			error10=error
			errors=1
		else:
			begintime=begintime.replace('.','-')
			if begintime[-1:]=='-' or begintime.replace('-','').isdigit()==False:
				error10='日期格式不对'
				errors=1
		if not standarddemand:
			error11=error
			errors=1
		if standarddemand and standarddemand.isdigit()==False:
			error11='请输入数字'
			errors=1
		if not shopsaddress:
			error12=error
			errors=1
		if not price:
			error13=error
			errors=1
		if price and price.isdigit()==False:
			error13='请输入数字'
			errors=1
		if chargetype=='1':
			balance=None
			if not years:
				error14=error
				errors=1
			if years and years.isdigit()==False:
				error14='请输入数字'
				errors=1
		if chargetype=='2':
			balance=price
			if not unit_price:
				error16=error
				errors=1
			if unit_price and unit_price.isdigit()==False:
				error16='请输入数字'
				errors=1
	if errors:
		return render_to_response('addcompany2.html',locals())
	gmt_created=datetime.datetime.now()
	argument=[name,mobile,mail,contact,gmt_created]
	if company_id:
		argument.append(company_id)
		sql='update seo_company set name=%s,mobile=%s,mail=%s,contact=%s,gmt_created=%s where id=%s'
		inserintodb(sql,argument)
		return HttpResponseRedirect(request_url)
	else:
		sql='insert into seo_company(name,mobile,mail,contact,gmt_created) values(%s,%s,%s,%s,%s)'
		inserintodb(sql,argument)
		keywords=keywords.replace(' ','')
		keywords_list=[]
		if u'|' in keywords:
			keywords_list=keywords.split('|')
		sql2='select id from seo_company where name="'+name+'"'
		company_id=fetchnumberdb(sql2)
		if company_id:
			if keywords_list:
				for keywords1 in keywords_list:
					argument2=[company_id,keywords1,gmt_created,begintime,standarddemand,shopsaddress,chargetype,price,years,unit_price,seouser_id,balance]
					sql='insert into seo_keywords(company_id,keywords,baidu_ranking,gmt_created,begintime,standarddemand,shopsaddress,chargetype,price,years,unit_price,seouser_id,balance) values(%s,%s,100,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
					inserintodb(sql,argument2)
			else:
				argument2=[company_id,keywords,gmt_created,begintime,standarddemand,shopsaddress,chargetype,price,years,unit_price,seouser_id,balance]
				sql='insert into seo_keywords(company_id,keywords,baidu_ranking,gmt_created,begintime,standarddemand,shopsaddress,chargetype,price,years,unit_price,seouser_id,balance) values(%s,%s,100,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
				inserintodb(sql,argument2)
		return HttpResponseRedirect('/company/')

#----保存关键字信息
def addkeywordsok(request):
	username=request.session.get('username')
	usertype=request.session.get('usertype')
	addkeywords=request.GET.get('addkeywords')
	seouser=get_seouser()
	list_company=get_company(0,5)
	gmt_created=datetime.datetime.now()
	request_url=request.GET.get('request_url')
	company_id=request.GET.get('company_id')
	keywords_id=request.GET.get('keywords_id')
	seouser_id=request.GET.get('seouser_id')
	keywords=request.GET.get('keywords')
	begintime=request.GET.get('begintime')
	standardtime=request.GET.get('standardtime')
	expire_time=request.GET.get('expire_time')
	isstandard=request.GET.get('isstandard')
	shopsaddress=request.GET.get('shopsaddress')
	chargetype=request.GET.get('chargetype')
	price=request.GET.get('price')
	years=request.GET.get('years')
	unit_price=request.GET.get('unit_price')
	if not seouser_id:
		seouser_id=request.GET.get('seouser')
	standarddemand=request.GET.get('standarddemand')
	seouser_name=getseoname(seouser_id)
	
	error1=''
	error2=''
	error3=''
	error4=''
	error5=''
	error6=''
	error7=''
	error8=''
	error=u'不能为空'
	errors=''
	if not keywords:
		error1=error
		errors=1
	if begintime:
		begintime=begintime.replace('.','-')
		if begintime[-1:]=='-' or begintime.replace('-','').isdigit()==False:
			error2='日期格式不对'
			errors=1
	else:
		error2=error
		errors=1
	if isstandard=='1' and chargetype=='1':
		if standardtime:
			standardtime=standardtime.replace('.','-')
			if standardtime[-1:]=='-' or standardtime.replace('-','').isdigit()==False:
				error11='日期格式不对'
				errors=1
#		else:
#			error11=error
#			errors=1
		if expire_time:
			expire_time=expire_time.replace('.','-')
			if expire_time[-1:]=='-' or expire_time.replace('-','').isdigit()==False:
				error10='日期格式不对'
				errors=1
#		else:
#			error10=error
#			errors=1
	if not shopsaddress:
		error4=error
		errors=1
	if not price:
		error5=error
		errors=1
	if price and price.isdigit()==False:
		error5=u'请输入数字'
		errors=1
	if not standarddemand:
		error8=error
		errors=1
	if standarddemand and standarddemand.isdigit()==False:
		error8=u'请输入数字'
		errors=1
	if chargetype=='1':
		balance=None
		if not years:
			error6=error
			errors=1
		if years and years.isdigit()==False:
			error6=u'请输入数字'
			errors=1
	if chargetype=='2':
		if keywords_id:
			sql9='select balance from seo_keywords where id=%s'
			result9=fetchonedb(sql9,[keywords_id])
			if result9:
				balance=result9[0]
			else:
				balance=price
		else:
			balance=price
		if not unit_price:
			error9=error
			errors=1
		if unit_price and price.isdigit()==False:
			error9=u'请输入数字'
			errors=1
	if errors:
		if keywords_id:
			return render_to_response('updatekeywords2.html',locals())
		else:
			return render_to_response('addkeywords2.html',locals())
	if keywords_id:
		argument=[keywords,begintime,standardtime,expire_time,standarddemand,shopsaddress,chargetype,price,years,unit_price,seouser_id,balance]
		sql='update seo_keywords set keywords=%s,begintime=%s,standardtime=%s,expire_time=%s,standarddemand=%s,shopsaddress=%s,chargetype=%s,price=%s,years=%s,unit_price=%s,seouser_id=%s,balance=%s where id='+keywords_id
		inserintodb(sql,argument)
		return HttpResponseRedirect(request_url)
	else:
		keywords_list=[]
		if u'|' in keywords:
			keywords_list=keywords.split('|')
		if keywords_list:
			for keywords1 in keywords_list:
				argument=[company_id,keywords1,gmt_created,begintime,standarddemand,shopsaddress,chargetype,price,years,unit_price,seouser_id,balance]
				sql='insert into seo_keywords(company_id,keywords,baidu_ranking,gmt_created,begintime,standarddemand,shopsaddress,chargetype,price,years,unit_price,seouser_id,balance) values(%s,%s,100,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
				inserintodb(sql,argument)
		else:
			argument=[company_id,keywords,gmt_created,begintime,standarddemand,shopsaddress,chargetype,price,years,unit_price,seouser_id,balance]
			sql='insert into seo_keywords(company_id,keywords,baidu_ranking,gmt_created,begintime,standarddemand,shopsaddress,chargetype,price,years,unit_price,seouser_id,balance) values(%s,%s,100,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
			inserintodb(sql,argument)
		return HttpResponseRedirect('/company/')