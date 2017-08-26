##过滤HTML中的标签
#将HTML中标签等信息去掉
#@param htmlstr HTML字符串.
def filter_tags(htmlstr):
	#先过滤CDATA
	re_cdata=re.compile('//<!\[CDATA\[[^>]*//\]\]>',re.I) #匹配CDATA
	re_script=re.compile('<\s*script[^>]*>[^<]*<\s*/\s*script\s*>',re.I)#Script
	re_style=re.compile('<\s*style[^>]*>[^<]*<\s*/\s*style\s*>',re.I)#style
	re_br=re.compile('<br\s*?/?>')#处理换行
	re_h=re.compile('</?\w+[^>]*>')#HTML标签
	re_comment=re.compile('<!--[^>]*-->')#HTML注释
	s=re_cdata.sub('',htmlstr)#去掉CDATA
	s=re_script.sub('',s) #去掉SCRIPT
	s=re_style.sub('',s)#去掉style
	s=re_br.sub('\n',s)#将br转换为换行
	s=re_h.sub('',s) #去掉HTML 标签
	s=re_comment.sub('',s)#去掉HTML注释
	#去掉多余的空行
	blank_line=re.compile('\n+')
	s=blank_line.sub('\n',s)
	s=replaceCharEntity(s)#替换实体
	return s

##替换常用HTML字符实体.
#使用正常的字符替换HTML中特殊的字符实体.
#你可以添加新的实体字符到CHAR_ENTITIES中,处理更多HTML字符实体.
#@param htmlstr HTML字符串.
def replaceCharEntity(htmlstr):
	CHAR_ENTITIES={'nbsp':' ','160':' ',
				'lt':'<','60':'<',
				'gt':'>','62':'>',
				'amp':'&','38':'&',
				'quot':'"','34':'"',}
   
	re_charEntity=re.compile(r'&#?(?P<name>\w+);')
	sz=re_charEntity.search(htmlstr)
	while sz:
		entity=sz.group()#entity全称，如&gt;
		key=sz.group('name')#去除&;后entity,如&gt;为gt
		try:
			htmlstr=re_charEntity.sub(CHAR_ENTITIES[key],htmlstr,1)
			sz=re_charEntity.search(htmlstr)
		except KeyError:
			#以空串代替
			htmlstr=re_charEntity.sub('',htmlstr,1)
			sz=re_charEntity.search(htmlstr)
	return htmlstr
#昨天
def getYesterday():   
	today=datetime.date.today()   
	oneday=datetime.timedelta(days=1)   
	yesterday=today-oneday    
	return yesterday  

#今天     
def getToday():   
	return datetime.date.today()     
 
#获取给定参数的前几天的日期，返回一个list   
def getDaysByNum(num):   
	today=datetime.date.today()   
	oneday=datetime.timedelta(days=1)       
	li=[]        
	for i in range(0,num):   
		#今天减一天，一天一天减   
		today=today-oneday   
		#把日期转换成字符串   
		#result=datetostr(today)   
		li.append(datetostr(today))   
	return li   
 
#将字符串转换成datetime类型  
def strtodatetime(datestr,format):       
	return datetime.datetime.strptime(datestr,format)   
 
#时间转换成字符串,格式为2008-08-02   
def datetostr(date):     
	return   str(date)[0:10]   
 
#两个日期相隔多少天，例：2008-10-03和2008-10-01是相隔两天  
def datediff(beginDate,endDate):   
	format="%Y-%m-%d";
	bd=strtodatetime(beginDate,format)   
	ed=strtodatetime(endDate,format)       
	oneday=datetime.timedelta(days=1)   
	count=0 
	while bd!=ed:   
		ed=ed-oneday   
		count+=1 
	return count   
 
#获取两个时间段的所有时间,返回list  
def getDays(beginDate,endDate):   
	format="%Y-%m-%d";   
	bd=strtodatetime(beginDate,format)   
	ed=strtodatetime(endDate,format)   
	oneday=datetime.timedelta(days=1)    
	num=datediff(beginDate,endDate)+1    
	li=[]   
	for i in range(0,num):    
		li.append(datetostr(ed))   
		ed=ed-oneday   
	return li   
 
#获取当前年份 是一个字符串  
def getYear():   
	return str(datetime.date.today())[0:4]    
 
#获取当前月份 是一个字符串  
def getMonth():   
	return str(datetime.date.today())[5:7]   
 
#获取当前天 是一个字符串  
def getDay():
	return str(datetime.date.today())[8:10]      
def getNow():   
	return datetime.datetime.now()
def changeuft8(stringvalue):
	if (stringvalue=="" or stringvalue==None):
		return ""
	else:
		return stringvalue.decode('GB18030','ignore').encode('utf-8')
def changedate(datestring):
	if (datestring=="" or datestring==None):
		return ""
	else:
		nowsdatestr=datestring.strftime( '%Y-%m-%d %X')
		if (nowsdatestr=='1900-01-01 00:00:00'):
			nowsdatestr=""
		return nowsdatestr
def changezw(strvalue):
	if(strvalue == None):
		tempstr=""
	else:
		tempstr=str(strvalue).encode('gbk','ignore').replace("'","")
	return tempstr
def changezhongwen(strvalue):
	if(strvalue == None):
		tempstr=""
	else:
		tempstr=strvalue.decode('GB18030','ignore').encode('utf-8')
		#tempstr=strvalue.decode('GB18030').encode('utf-8')
	return tempstr
def subString(string,length):   
	if length >= len(string):   
		return string   
	result = ''  
	i = 0  
	p = 0  
	while True:   
		ch = ord(string[i])   
		#1111110x   
		if ch >= 252:   
			p = p + 6  
		#111110xx   
		elif ch >= 248:   
			p = p + 5  
		#11110xxx   
		elif ch >= 240:   
			p = p + 4  
		#1110xxxx   
		elif ch >= 224:   
			p = p + 3  
		#110xxxxx   
		elif ch >= 192:
			p = p + 2  
		else:   
			p = p + 1	   
		if p >= length:   
			break;
		else:   
			i = p   
	return string[0:i]
	pass
def formattime(value,flag):
	if value:
		if (flag==1):
			return value.strftime( '%-Y-%-m-%-d')
		else:
			return value.strftime( '%-Y-%-m-%-d %-H:%-M:%-S')
	else:
		return ''
def getindustry_code(ckid):
	sql11="select code from category where code like '10001%' and old_id="+str(ckid)+""
	cursor.execute(sql11)
	areacode = cursor.fetchone()
	if (areacode == None):
		areacode1='0'
	else:
		areacode1=areacode[0]
	return areacode1
def getindustry_codeold(code):
	sql11="select old_id from category where code=%s"
	cursor.execute(sql11,[code])
	areacode = cursor.fetchone()
	if (areacode == None):
		areacode1='0'
	else:
		areacode1=areacode[0]
	return areacode1

def getservice_code(ckid):
	sql11="select code from category where code like '10201%' and old_code="+str(ckid)+""
	cursor.execute(sql11)
	areacode = cursor.fetchone()
	if (areacode == None):
		return '0'
	else:
		return areacode[0]
def getservice_name(code):
	sql11="select label from category where code=%s"
	cursor.execute(sql11,[code])
	areacode = cursor.fetchone()
	if (areacode == None):
		return '0'
	else:
		return areacode[0]
def getservicecategorylist(code):
	sql11="select code,label from category where code like '"+str(code)+"____' "
	cursor.execute(sql11)
	alist = cursor.fetchall()
	listall=[]
	for l in alist:
		list={'code':l[0],'label':l[1]}
		listall.append(list)
	return listall
#地区编号
def getprovincecode(strvalue):
	
	if (strvalue == None):
		areaname=""
	else:
		areaname=strvalue
	areaname=areaname.replace(',','').replace('|',',')
	arrarea=[]
	arrarea=areaname.split(',')
	if (len(arrarea)>1):
		area1=arrarea[1]
		if (area1 == ''):
			area1=arrarea[0]
	else:
		area1=arrarea[0]
	
	area1=area1.replace("'","")
	area1=area1.replace(changezhongwen('省'),'')
	area1=area1.replace(changezhongwen('市'),'')
	
	
	sql11="select code from category where label like '%"+area1+"%'"
	
	cursor.execute(sql11)
	areacode = cursor.fetchone()
	if (areacode == None):
		areacode1=''
	else:
		areacode1=areacode[0]
	
	return areacode1
def getgardid(cid):
	sql="select id from category_garden where old_code='"+str(cid)+"'"
	cursor.execute(sql)
	newcode=cursor.fetchone()
	if (newcode == None):
		return '0'
	else:
		return newcode[0]
def getcompany_id(cname,regtime):
	sql="select id from company where gmt_created=%s order by id desc limit 0,1"
	cursor.execute(sql,[regtime])
	newcode=cursor.fetchone()
	if (newcode == None):
		return 0
	else:
		return newcode[0]
#客户参加活动列表
def getactive():
	sql="select label,code from category where parent_code='2003'"
	cursor.execute(sql)
	aclist=cursor.fetchall()
	listall=[]
	for a in aclist:
		list={'label':a[0],'code':a[1]}
		listall.append(list)
	return listall
#产品数量
def getproductnum(nowday):
	format="%Y-%m-%d";
	nowday=strtodatetime(nowday,format)
	oneday=datetime.timedelta(days=1)
	
	sql="select sum(num) from analysis_product where gmt_created>'"+str(nowday)+"' and gmt_created<='"+str(nowday+oneday)+"'"
	cursor.execute(sql)
	offerlist=cursor.fetchone()
	if offerlist:
		return offerlist[0]
	else:
		return 0
#留言数量
def getleavewordsnum(nowday):
	format="%Y-%m-%d";
	nowday=strtodatetime(nowday,format)
	oneday=datetime.timedelta(days=1)
	
	sql="select sum(num) from analysis_inquiry where gmt_created>'"+str(nowday)+"' and gmt_created<='"+str(nowday+oneday)+"'"
	cursor.execute(sql)
	offerlist=cursor.fetchone()
	if offerlist:
		return offerlist[0]
	else:
		return 0
#留言数量
def getregnum(nowday):
	format="%Y-%m-%d";
	nowday=strtodatetime(nowday,format)
	oneday=datetime.timedelta(days=1)
	
	sql="select sum(num) from analysis_register where gmt_created>'"+str(nowday)+"' and gmt_created<='"+str(nowday+oneday)+"'"
	cursor.execute(sql)
	offerlist=cursor.fetchone()
	if offerlist:
		return offerlist[0]
	else:
		return 0
#联系方式
def getacount(companyid):
	sql="select account,contact,mobile from company_account where company_id="+str(companyid)+""
	cursor.execute(sql)
	returnresalt=cursor.fetchone()
	if returnresalt:
		return {'account':returnresalt[0],'contact':returnresalt[1],'mobile':returnresalt[2]}
		
#获得来电宝余额
def getppcpay(tel,company_id):
	sql="select sum(call_fee) from phone_log where tel=%s"
	cursor.execute(sql,[tel])
	returnresalt=cursor.fetchone()
	allcall_fee=0
	if returnresalt:
		allcall_fee=returnresalt[0]
	
	checkprice=1
	sql="select count(0) from phone_click_log where company_id=%s"
	cursor.execute(sql,[company_id])
	returnresalt=cursor.fetchone()
	allcheck_fee=0
	if returnresalt:
		allcheck_fee=returnresalt[0]
	if allcheck_fee==None:
		allcheck_fee=0
	if allcall_fee==None:
		allcall_fee=0
	return allcall_fee+allcheck_fee*checkprice
#获得总消费值
def getallppcpay():
	sql="select sum(call_fee) from phone_log"
	cursor.execute(sql)
	returnresalt=cursor.fetchone()
	allcall_fee=0
	if returnresalt:
		allcall_fee=returnresalt[0]
	
	checkprice=1
	sql="select count(0) from phone_click_log"
	cursor.execute(sql)
	returnresalt=cursor.fetchone()
	allcheck_fee=0
	if returnresalt:
		allcheck_fee=returnresalt[0]
	if allcheck_fee==None:
		allcheck_fee=0
	if allcall_fee==None:
		allcall_fee=0
	return allcall_fee+allcheck_fee*checkprice
#销售金额
def getallincome():
	sql="select sum(amount) from phone"
	cursor.execute(sql)
	returnresalt=cursor.fetchone()
	if returnresalt:
		return returnresalt[0]
#公司详情
def getcompanydetail(company_id):
	sqlc="select name,business,regtime,address,introduction,membership_code,domain_zz91,service_code from company where id=%s"
	cursor.execute(sqlc,company_id)
	clist=cursor.fetchone()
	if clist:
		compname=clist[0]
		business=clist[1]
		regtime=formattime(clist[2],0)
		address=clist[3]
		introduction=clist[4]
		viptype=clist[5]
		domain_zz91=clist[6]
		service_code=clist[7]
		arrviptype={'vippic':'','vipname':'','vipcheck':'','ldb':''}
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
		if (viptype == '10051003'):
			arrviptype['vippic']=''
			arrviptype['vipname']='来电宝客户'
		if (viptype == '10051000'):
			arrviptype['vipcheck']=None
		else:
			arrviptype['vipcheck']=1
		
	sqlc="select contact,tel_country_code,tel_area_code,tel,mobile,fax_country_code,fax_area_code,fax,email"
	sqlc=sqlc+",sex,position,qq,account "
	sqlc=sqlc+"from company_account where company_id=%s"
	cursor.execute(sqlc,company_id)
	alist=cursor.fetchone()
	list=[]
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
		account=alist[12]
		list={'company_id':company_id,'name':compname,'business':business,'domain_zz91':domain_zz91,'regtime':regtime,'address':address,'introduction':introduction,'contact':contact,'tel_country_code':tel_country_code,'tel_area_code':tel_area_code,'tel':tel,'mobile':mobile,'fax_country_code':fax_country_code,'fax_area_code':fax_area_code,'fax':fax,'email':email,'sex':sex,'position':position,'qq':qq,'viptype':arrviptype,'service_code':service_code,'account':account}
	return list
#----发手机短信
def postsms(mobile,content):
	gmt_created=datetime.datetime.now()
	gmt_modified=datetime.datetime.now()
	sqlc="select id from sms_log where receiver=%s and template_code='weixin'"
	cursor_sms.execute(sqlc,[mobile])
	alist=cursor_sms.fetchone()
	if alist==None:
		valu=['weixin',mobile,gmt_created,'yuexin',1,gmt_created,gmt_created,content]
		sqls="insert into sms_log (template_code,receiver,gmt_send,gateway_code,priority,gmt_created,gmt_modified,content) values(%s,%s,%s,%s,%s,%s,%s,%s)"
		cursor_sms.execute(sqls,valu)
		conn_sms.commit()
		return "insert"
	else:
		return "sended"
def getmobileaccount(company_id):
	sqlc="select account from company_account where company_id=%s"
	cursor.execute(sqlc,[company_id])
	alist=cursor.fetchone()
	if alist:
		sql="select id from oauth_access where open_type='weixin.qq.com' and target_account=%s"
		cursor.execute(sql,[alist[0]])
		aalist=cursor.fetchone()
		if aalist:
			return aalist[0]
def postsmsflag(mobile):
	sqlc="select id from sms_log where receiver=%s and template_code='weixin'"
	cursor_sms.execute(sqlc,[mobile])
	alist=cursor_sms.fetchone()
	if alist==None:
		return "1"
	else:
		return "0"
		
		
		
		