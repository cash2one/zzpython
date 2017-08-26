def openConfirm1(request):
	localhostIP=getlocalIP()
	com_id= request.GET.get("com_id")
	com_email=request.GET.get("com_email")
	userid=request.GET.get("userid")
	mbflag=request.GET.get("mbflag")
	

	if (com_id!="" and com_id!=None):
		sqla="select name from company where id=%s"
		cursor_server.execute(sqla,[com_id])
		newreturna=cursor_server.fetchone()
		if (newreturna):
			com_name=newreturna[0]
		sqla="select gmt_created,contact,mobile,num_login,email from company_account where company_id=%s"
		cursor_server.execute(sqla,[com_id])
		newreturna=cursor_server.fetchone()
		if (newreturna):
			com_contactperson=com_name+"("+newreturna[1]+")"
			com_mobile=newreturna[2]
			com_regtime=formattime(newreturna[0],0)
			com_logincount=newreturna[3]
			com_email=newreturna[4]
		personid = request.GET.get("personid")
		username= request.GET.get("username")
	
	service_type1=['再生通','品牌通','展会产品','广告','线下纸媒','短信报价','百度优化','国际站','移动生意管家','再生通发起人','终身服务','商铺服务','诚信会员','定金','来电宝','其他']
	service_type2=['再生通','品牌通','广告','黄页','展会广告','百度优化','简版再生通','移动生意管家','再生通发起人','终身服务','商铺服务','诚信会员','定金','来电宝','其他']
	service_type3=['再生通续费','再生通','品牌通续费','展会产品','百度优化','广告续费','简版续费','移动生意管家','再生通发起人','终身服务','商铺服务','诚信会员','定金','来电宝','其他']
	
	return render_to_response('openConfirm0.html',locals())
	closeconn()

def openConfirmsave1(request):
	response = HttpResponse()
	localhostIP=getlocalIP()
	company_id=com_id=request.POST["com_id"]
	personid = request.POST["personid"]
	#service_type = str(request.POST["service_type"])
	#service_type1 = str(request.POST["service_type1"])
	gmt_income=payTime = request.POST["payTime"]
	email=newemail = request.POST["newemail"]
	amount=payMoney = str(request.POST["payMoney"])+'00'
	sale_staff=saler = request.POST["saler"]
	adkeywords = request.POST["adkeywords"]
	adfromdate = request.POST["adfromdate"]
	adtodate = request.POST["adtodate"]
	adcontent = request.POST["adcontent"]
	remark = request.POST["remark"]
	gmt_created=datetime.datetime.now()
	gmt_modified=datetime.datetime.now()
	gmt_date=gmt_created.strftime('%Y-%m-%d')
	mbradio = request.POST["mbradio"]
	remark="广告关键字："+adkeywords+"|开始时间："+adfromdate+"|结束时间："+adtodate+"|广告内容："+adcontent+"|备注："+remark
	"""
	sql="select company_id from company_account where (account='"+email+"' or email='"+email+"')"
	cursor.execute(sql)
	newreturn=cursor.fetchone()
	if (newreturn==None):
		sqla="select email from company_account where company_id="+str(company_id)+""
		cursor.execute(sqla)
		newreturna=cursor.fetchone()
		if (newreturna==None):
			response.write("<script>alert('该开通的邮箱不存在');</script>")
			return response
		else:
			email=newreturna[0]
	else:
		company_id=newreturn[0]
	"""
	suc=""
	servicestr=request.REQUEST.getlist("service_type2")
	order_nostr=""
	i=0
	for t in servicestr:
		apply_groupstr=""
		apply_group=random.randrange(0,1000000000)
		apply_groupstr=apply_groupstr+str(apply_group)+"|"
		order_no=str(gmt_income)+email+str(mbradio)+str(t)+str(company_id)
		order_nostr=order_nostr+order_no+"|"
		#判断订单是否已经申请
		errflag=0
		service_type=t
		crm_service_code='1005'
		if (service_type=='再生通' or service_type=='再生通续费' or service_type=='品牌通' or service_type=='品牌通续费'):
			crm_service_code='1000'
		if (service_type=='品牌通'):
			crm_service_code='1000'
			remark1='开通品牌通'
		if (service_type=='广告' or service_type=='广告续费'):
			crm_service_code='1002'
		if (service_type=='黄页'):
			crm_service_code='1003'
		if (service_type=='展会产品' or service_type=='展会广告'):
			crm_service_code='1004'
		if (service_type=='简版再生通' or service_type=='简版续费'):
			crm_service_code='1006'
		if (service_type=='百度优化'):
			crm_service_code='10001002'
		if (service_type=='商铺服务'):
			crm_service_code='10001004'
		if (service_type=='移动生意管家'):
			crm_service_code='10001000'
		if (service_type=='终身服务'):
			crm_service_code='10001003'
		if (service_type=='再生通发起人'):
			crm_service_code='10001001'
		if (service_type=='诚信会员'):
			crm_service_code='10001005'
		if (service_type=='定金'):
			crm_service_code='10001006'
		if (service_type=='来电宝'):
			crm_service_code='1007'
		
		sql="select id from crm_service_apply where order_no='"+order_no+"'"
		cursor_server.execute(sql)
		newreturn=cursor_server.fetchone()
		if (newreturn!=None):
			errflag=1
		if (errflag!=1):
			value=[apply_group, order_no, gmt_income, email, amount,  sale_staff, remark,  gmt_created, gmt_modified]
			sql="insert into crm_service_apply(apply_group, order_no, gmt_income, email, amount,  sale_staff, remark,  gmt_created, gmt_modified) values(%s,%s,%s,%s,%s,%s,%s,%s,%s)"
			cursor_server.execute(sql,value);
			remark1=''
			apply_status='0'
			value=[company_id,crm_service_code,apply_group,remark1,gmt_created, gmt_modified,apply_status]
			sql="insert into crm_company_service(company_id,crm_service_code,apply_group,remark,gmt_created, gmt_modified,apply_status) values(%s,%s,%s,%s,%s,%s,%s)"
			cursor_server.execute(sql,value);
		
		#保存本地数据
		order_no = hashlib.md5(order_no)
		order_no = order_no.hexdigest()[8:-8]
		
		userid=request.POST["userid"]
		realname=request.POST["realname"]
		sales_date=request.POST["sales_date"]
		service_type=request.POST["service_type"]
		sales_type=request.POST["sales_type"]
		sales_price=request.POST["sales_price"]
		if (i!=0):
			sales_price=0
		sales_email=request.POST["sales_email"]
		sales_mobile=request.POST["sales_mobile"]
		sales_bz=request.POST["sales_bz"]
		com_contactperson=request.POST["com_contactperson"]
		com_mobile=request.POST["com_mobile"]
		com_ly1=request.POST["com_ly1"]
		
		com_ly1=request.POST["com_ly1"]
		com_ly2=request.POST["com_ly2"]
		com_zq=request.POST["com_zq"]
		com_fwq=request.POST["com_fwq"]
		com_khdq=request.POST["com_khdq"]
		com_pro=request.POST["com_pro"]
		com_cpjb=request.POST["com_cpjb"]
		com_cxfs=request.POST["com_cxfs"]
		com_regtime=request.POST["com_regtime"]
		com_hkfs=request.POST["com_hkfs"]
		com_logincount=request.POST["com_logincount"]
		com_gjd=request.POST["com_gjd"]
		com_servernum=request.POST["com_servernum"]
	
	
		svalues=(order_no,personid,userid,realname,sales_date,com_id,service_type,sales_type,
			sales_price,sales_email,sales_mobile,sales_bz,com_contactperson,com_mobile,
			com_ly1,com_ly2,com_zq,com_fwq,com_khdq,com_pro,com_cpjb,com_cxfs,com_regtime,
			com_hkfs,com_logincount,com_gjd,com_servernum)
			
		sql="select * from renshi_salesIncome where order_no=%s"
		cursor.execute(sql,(order_no))
		returna=cursor.fetchone()
		if (returna==None):
			sqlp="insert into renshi_salesIncome(order_no,personid,userid,realname,sales_date,com_id,service_type,sales_type,"
			sqlp=sqlp+"sales_price,sales_email,sales_mobile,sales_bz,com_contactperson,com_mobile,"
			sqlp=sqlp+"com_ly1,com_ly2,com_zq,com_fwq,com_khdq,com_pro,com_cpjb,com_cxfs,com_regtime,"
			sqlp=sqlp+"com_hkfs,com_logincount,com_gjd,com_servernum) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
			cursor.execute(sqlp,svalues)
			conn.commit()
		if (crm_service_code=='10001006'):
			noconfirm=1
		else:
			noconfirm=0
			
		i=i+1
		
	suc=suc+"服务器数据保存成功！"
	##
	if (noconfirm==0):
		
		
		order_no1 = hashlib.md5(order_nostr)
		order_no1 = order_no1.hexdigest()[8:-8]
		confirmID=order_no1
		
		payUserName=request.POST["payUserName"]
		customType=request.POST["customType"]
		salerID=request.POST["salerID"]
		mbradio=request.POST["mbradio"]
		if (mbradio=='1' or mbradio=='3'):
			assignflag=1
		else:
			assignflag=0
		
		
		
		sql="select * from crm_openConfirm where com_id=%s and confirmID=%s"
		cursor.execute(sql,(com_id,confirmID))
		returna=cursor.fetchone()
		cvalue=(com_id,confirmID,payTime,payUserName,payMoney,saler,newemail,remark,customType,salerID,assignflag)
		if (returna==None):
			sqlu="insert into crm_openConfirm(com_id,confirmID,payTime,payUserName,payMoney,saler,newemail,remark,customType,salerID,assignflag) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
			cursor.execute(sqlu,cvalue)
			conn.commit()
		suc=suc+"本地数据保存成功！"
	return render_to_response('openConfirm_suc.html',locals())
	#response.write("<script>parent.changeform('"+order_nostr+"',"+str(mbradio)+",'"+str(apply_groupstr)+"');</script>")
	#return response
	closeconn()
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