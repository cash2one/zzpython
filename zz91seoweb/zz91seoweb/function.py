def getnowurl(request):
	host=request.path_info
	qstring=request.META.get('QUERY_STRING','/')
	qstring=qstring.replace("&","^and^")
	if qstring:
		return host+"?"+qstring
	else:
		return host
def tradeorderby(listall):
	listall = sorted(listall, key=itemgetter(1))
	changeflag="0"
	listallvip1=[]
	listallvip2=[]
	m=0
	for i in listall:
		m+=1
		if (changeflag==str(i[1])):
			list1=[i[0],i[1],i[2],i[3],i[4],i[5]]
			listallvip2.append(list1)
			if (len(listall)==m):
				listallvip1+=listallvip2
		else:
			listallvip2=sorted(listallvip2, key=itemgetter(4,2,5,3),reverse=True)
			listallvip1+=listallvip2
			listallvip2=[]
			list1=[i[0],i[1],i[2],i[3],i[4],i[5]]
			listallvip2.append(list1)
			if (len(listall)==m):
				listallvip1+=listallvip2
		changeflag=str(i[1])
	return listallvip1
#加密
def getjiami(strword):
	return strword.encode('utf8','ignore').encode("hex")
def getjiemi(strword):
	return strword.decode("hex").decode('utf8','ignore')
def gethostname(request):
	host = request.META['HTTP_HOST']
	subname=host.split(".")
	subname=subname[0]
	domain=host[len(subname)+1:len(host)]
	return {'subname':subname,'domain':domain}

#获得公司产品信息
def getcompinfo(pdtid,cursort,keywords):
	list1=cache.get("seoweb_compproinfo"+str(pdtid))
	if not list1:
		sql="SELECT c.id AS com_id, c.name AS com_name, p.id AS pdt_id, RIGHT( p.products_type_code, 1 ) AS pdt_kind, p.title AS pdt_name, p.details AS pdt_detail, DATE_FORMAT(p.refresh_time,'%%Y/%%m/%%d'), c.domain_zz91 AS com_subname, p.price AS pdt_price,c.membership_code,e.label as city,p.min_price,p.max_price,p.price_unit,p.quantity_unit,p.quantity FROM products AS p LEFT OUTER JOIN company AS c ON p.company_id = c.id LEFT OUTER JOIN category as e ON c.area_code=e.code where p.id=%s;"
		cursort.execute(sql,pdtid)
		productlist = cursort.fetchone()
		if productlist:
			arrpdt_kind={'kindtxt':'','kindclass':''}
			pdt_kind=productlist[3]
			viptype=str(productlist[9])
			if (str(pdt_kind) == '1'):
				arrpdt_kind['kindtxt']='求购'
				arrpdt_kind['kindclass']='buy'
			else:
				arrpdt_kind['kindtxt']='供应'
				arrpdt_kind['kindclass']='sell'
			arrviptype={'vippic':'','vipname':'','vipsubname':'','vipcheck':'','com_fqr':''}
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
			arrviptype['vipsubname'] = productlist[7]
			arrviptype['com_fqr']=''
			com_province=productlist[10]
			if (com_province==None):
				com_province=''
			pdt_images=""
			#价格范围判断
			allprice=""
			min_price=productlist[11]
			if not min_price:
				min_price=''
			else:
				min_price=str(min_price)
				if (min_price!='0.0'):
					allprice=allprice+min_price
			max_price=productlist[12]
			if (not max_price):
				max_price=''
			else:
				max_price=str(max_price)
				if (max_price!='0.0' and max_price!=min_price):
					if not min_price:
						allprice=allprice+max_price
					else:
						allprice=allprice+'-'+max_price
			price_unit=productlist[13]
			if (price_unit==None):
				price_unit=''
			else:
				if allprice:
					allprice=allprice+price_unit
			quantity_unit = productlist[14]
			if (quantity_unit==None):
				quantity_unit=''
			else:
				if (allprice):
					allprice=allprice+'/'+quantity_unit
			
			total_quantity=productlist[15]

			if (total_quantity=='' or total_quantity==' ' or total_quantity==None):
				total_quantity=None
			else:
				if quantity_unit not in total_quantity:
					total_quantity=total_quantity+quantity_unit
			if total_quantity==None:
				total_quantity=""

			#----
			sql1="select pic_address from products_pic where product_id=%s and check_status=1"
			cursort.execute(sql1,productlist[2])
			productspic = cursort.fetchone()
			if productspic:
				pdt_images=productspic[0]
			else:
				pdt_images=""
			pdt_images=pdt_images.replace("img1.zz91.com/", "")
			if (pdt_images == '' or pdt_images == '0'):
				pdt_images='../cn/img/noimage.gif'
			else:
				pdt_images='http://img3.zz91.com/150x150/'+pdt_images+''
			laidb=laidianbaofunction()
			yangflag=laidb.getyangflag(pdtid)
			company_id=productlist[0]
			if company_id:
				companymarket=getcompanymarket(company_id)		
			list1={'com_id':productlist[0],'com_name':productlist[1],'pdt_id':productlist[2],'pdt_kind':arrpdt_kind
			,'pdt_name':productlist[4],'com_province':com_province,'pdt_detail':productlist[5]
			,'pdt_detaillclear':subString(filter_tags(productlist[5]),350),'pdt_time_en':productlist[6],'com_subname':productlist[7],'vipflag':arrviptype
			,'pdt_images':pdt_images,'pdt_price':allprice,'total_quantity':total_quantity
			,'vippaibian':'','pdt_name1':productlist[4],'wordsrandom':1,'yangflag':yangflag,'companymarket':companymarket}
		else:
			list1=None
			
		#list1=getproid(pdtid)
		if (list1 == None):
			return None
		else:
			pdt_images=list1['pdt_images']
			if (pdt_images=='../cn/img/noimage.gif'):
				list1['pdt_images']='http://img0.zz91.com/front/images/global/noimage.gif'
			pdt_detail=list1['pdt_detaillclear']
			if pdt_detail:
				pdt_detail=pdt_detail.replace('<br>','').replace('&nbsp;',' ')
				docs=[pdt_detail]
				list1['pdt_detail']=subString(pdt_detail,50)+'...'
			
				pdt_name=list1['pdt_name']
				docs=[pdt_name]
				list1['pdt_name']=pdt_name
		
		cache.set("seoweb_compproinfo"+str(pdtid),list1,60*60*2)
		
	return list1

#获得公司产品信息 给tuijian 页面用
def getcompinfoForTuijian(pdtid,cursor,keywords):
	if keywords:
		keywords=keywords.replace('\\','')
		keywords=keywords.replace('/','')
		keywords=keywords.replace('/','')
		keywords=keywords.replace('(','')
		keywords=keywords.replace(')','')
		keywords=keywords.replace('+','')
		keywords=keywords.upper()
	sql="SELECT c.id AS com_id, c.name AS com_name, p.id AS pdt_id, RIGHT( p.products_type_code, 1 ) AS pdt_kind, p.title AS pdt_name, p.details AS pdt_detail, DATE_FORMAT(p.refresh_time,'%Y/%m/%d'), c.domain_zz91 AS com_subname, p.price AS pdt_price,c.membership_code,e.label as city,p.min_price,p.max_price,p.price_unit,p.total_quantity,DATE_FORMAT(p.expire_time,'%Y-%m-%d'),DATEDIFF(p.expire_time,CURDATE()) as yxtime,p.quantity_unit,f.label,c.address,DATE_FORMAT(c.regtime,'%Y-%m-%d'),c.area_code,p.check_status FROM products AS p LEFT OUTER JOIN company AS c ON p.company_id = c.id LEFT OUTER JOIN category as e ON c.area_code=e.code left outer join category_products as f on p.category_products_main_code=f.code where p.id="+str(pdtid)+""
	cursor.execute(sql)
	productlist = cursor.fetchone()
	if productlist:
		arrpdt_kind={'kindtxt':'','kindclass':''}
		pdt_kind=productlist[3]
		viptype=str(productlist[9])
		if (str(pdt_kind) == '1'):
			arrpdt_kind['kindtxt']='求购'
			arrpdt_kind['kindclass']='buy'
		else:
			arrpdt_kind['kindtxt']='供应'
			arrpdt_kind['kindclass']='sell'
		arrviptype={'vippic':'','vipname':'','vipclass':'','vipsubname':'','vipcheck':'','com_fqr':'','zstNum':'','ldb':''}
		if (viptype == '10051000'):
			arrviptype['vippic']=None
			arrviptype['vipname']='普通会员'
		if (viptype == '10051001'):
			arrviptype['vippic']='http://img.zz91.com/zz91images/recycle.gif'
			arrviptype['vipname']='再生通'
			arrviptype['vipclass']='zst_logo'
		if (viptype == '100510021000'):
			arrviptype['vippic']='http://img.zz91.com/zz91images/pptSilver.gif'
			arrviptype['vipname']='银牌品牌通'
			arrviptype['vipclass']='ypppt_logo'
		if (viptype == '100510021001'):
			arrviptype['vippic']='http://img.zz91.com/zz91images/pptGold.gif'
			arrviptype['vipname']='金牌品牌通'
			arrviptype['vipclass']='jpppt_logo'
		if (viptype == '100510021002'):
			arrviptype['vippic']='http://img.zz91.com/zz91images/pptDiamond.gif'
			arrviptype['vipname']='钻石品牌通'
			arrviptype['vipclass']='zsppt_logo'
		if (viptype == '10051003'):
			arrviptype['vippic']=''
			arrviptype['vipname']='来电宝客户'
			arrviptype['vipclass']='ldb_logo'
		if (viptype == '10051000'):
			arrviptype['vipcheck']=None
		else:
			arrviptype['vipcheck']=1
		#来电宝客户
		sqll="select id from crm_company_service where company_id="+str(productlist[0])+" and crm_service_code in ('1007','1008','1009','1010','1011') and apply_status=1"
		cursor.execute(sqll)
		ldbresult=cursor.fetchone()
		if ldbresult:
			sqlg="select front_tel from phone where company_id="+str(productlist[0])+" and expire_flag=0"
			cursor.execute(sqlg)
			phoneresult=cursor.fetchone()
			if phoneresult:
				ldbphone = phoneresult[0]
				if ldbphone:
					# 来电宝积分参数
					sqlg="select phone_rate,level from ldb_level where company_id="+str(productlist[0])+""
					cursor.execute(sqlg)
					scoreresult=cursor.fetchone()
					if scoreresult :
						if scoreresult[0] > 0:
							ldbrate =  str(int(scoreresult[0]))+"%"
						else :
							ldbrate = "--"
						ldblevel=scoreresult[1]
					else:
						ldbrate = "--"
						ldblevel=None
						
				else:
					ldbrate = "--"
				
				arrviptype['ldb']={'ldbphone':ldbphone,'ldbrate':ldbrate,'level':ldblevel}
			else:
				arrviptype['ldb']=None
				
		else:
			arrviptype['ldb']=None
		arrviptype['vipsubname'] = productlist[7]
		com_province=productlist[10]
		if (com_province==None):
			com_province=''
		pdt_images=""
		area_code=productlist[21]
		#地区信息
		if (area_code):
			sqld="select label from category where code='"+str(area_code[:-4])+"'"
			cursor.execute(sqld)
			arealabel = cursor.fetchone()
			if arealabel:
				if arealabel[0]:
					com_province=arealabel[0]+' '+com_province
		#公司信息
		if (arrviptype['vipcheck'] or arrviptype['ldb']):
			address=productlist[19]
			regtime=productlist[20]
			if (productlist[0]):
				sqlp="select count(0) from products where company_id="+str(productlist[0])+""
				cursor.execute(sqlp)
				pcopt = cursor.fetchone()
				if pcopt:
					offercount=pcopt[0]
				else:
					offercount=0
			
				sqlc="select tel_country_code,tel_area_code,tel,mobile,qq,contact from company_account where company_id="+str(productlist[0])+" "
				cursor.execute(sqlc)
				compinfolist = cursor.fetchone()
				if compinfolist:
					if (compinfolist[0]):
						tel_country_code=compinfolist[0]
					else:
						tel_country_code=''
					if (compinfolist[1]):
						tel_area_code=compinfolist[1]
					else:
						tel_area_code=''
					if (compinfolist[2]):
						tel=compinfolist[2]
					else:
						tel=''
					tel=tel_country_code+'-'+tel_area_code+'-'+tel
					mobile=compinfolist[3]
					qq=compinfolist[4]
					contact=compinfolist[5]
					if (qq):
						qq=qq.strip()
						if (qq==""):
							qq=None
					arrcompinfo={'tel':tel,'mobile':mobile,'address':address,'regtime':regtime,'offercount':offercount,'qq':qq,'contact':contact}
				else:
					arrcompinfo=None
			else:
				arrcompinfo=None
		else:
			arrcompinfo=None
		#价格范围判断
		allprice=""
		min_price=productlist[11]
		if not min_price:
			min_price=''
		else:
			min_price=str(min_price)
			if (min_price!='0.0'):
				allprice=allprice+min_price
		max_price=productlist[12]
		if not max_price:
			max_price=''
		else:
			max_price=str(max_price)
			if (max_price!='0.0' and max_price!=min_price):
				if not min_price:
					allprice=allprice+max_price
				else:
					allprice=allprice+'-'+max_price
		price_unit=productlist[13]
		total_quantity=productlist[14]
		quantity_unit=productlist[17]
		if (quantity_unit==None):
			quantity_unit=''
		if (total_quantity=='' or total_quantity==' ' or total_quantity==None):
			total_quantity=None
		else:
			total_quantity=total_quantity+quantity_unit
		expire_time=productlist[15]
		yxtime=productlist[16]
		procatetype=productlist[18]
		if (procatetype!=None):
			procatetype=procatetype.replace('|',' ')
			procatetype=procatetype.replace('\\',' ')
			procatetype=procatetype.replace('/',' ')
			procatetype=procatetype.replace('(',' ')
			procatetype=procatetype.replace(')',' ')

		if (str(expire_time)=='9999-12-31'):
			yxtimevalue='长期有效'
		else:
			if (yxtime<0):
				yxtimevalue='已经过期'
			else:
				yxtimevalue='截止：'+str(expire_time)
		#
		if (price_unit==None):
			price_unit=''
		else:
			if (allprice!=''):
				allprice=allprice+price_unit
		#----
		sql1="select pic_address from products_pic where product_id="+str(productlist[2])+" and check_status=1 order by is_default desc,id desc"
		cursor.execute(sql1)
		productspic = cursor.fetchone()
		if productspic:
			pdt_images=productspic[0]
		else:
			pdt_images=""
		if (pdt_images == '' or pdt_images == '0'):
			pdt_images='../cn/img/noimage.gif'
		else:
			pdt_images='http://img3.zz91.com/122x93/'+pdt_images+''
		company_id=productlist[0]
		
		
		
		
		
		list1={'com_id':productlist[0],'com_name':productlist[1],'pdt_id':productlist[2],'pdt_kind':arrpdt_kind
		,'pdt_name':productlist[4],'com_province':com_province,'pdt_detail':productlist[5],'pdt_detaillclear':filter_tags(productlist[5])[0:50]
		,'pdt_time_en':productlist[6],'com_subname':productlist[7],'vipflag':arrviptype,'check_status':productlist[22]
		,'pdt_images':pdt_images,'pdt_price':allprice
		,'vippaibian':'','pdt_name1':productlist[4],'wordsrandom':1,'total_quantity':total_quantity,'expire_time':expire_time,'yxtimevalue':yxtimevalue,'procatetype':procatetype,'arrcompinfo':arrcompinfo}
	else:
		list1=None
		
	#list1=getproid(pdtid)
	if (list1 == None):
		return None
	else:
		pdt_images=list1['pdt_images']
		if (pdt_images=='../cn/img/noimage.gif'):
			list1['pdt_images']='http://img0.zz91.com/front/images/global/noimage.gif'
		pdt_detail=filter_tags(list1['pdt_detail'])
		pdt_detail=pdt_detail.replace('<br>','').replace('&nbsp;',' ')
		docs=[pdt_detail]
		list1['pdt_detail']=subString(pdt_detail,50)+'...'
		
	return list1

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
#根据门市部获得companyid
def getdomaincompanyid(domain):
	company_id=cache.get("seoweb_domain"+domain)
	#company_id=None
	if (company_id==None):
		sql="select id from company where domain_zz91=%s"
		cursor.execute(sql,[domain])
		returnresult=cursor.fetchone()
		if returnresult:
			company_id=returnresult[0]
		else:
			company_id=0
		cache.set("seoweb_domain"+domain,company_id,60*600)
	return company_id
#用户名获得company_id
def getcompanyid(account):
	company_id=cache.get("seoweb_company_id"+account)
	if (company_id==None):
		sql="select company_id from company_account where account=%s"
		cursor.execute(sql,[account])
		returnresult=cursor.fetchone()
		if returnresult:
			company_id=returnresult[0]
		else:
			company_id=0
		cache.set("seoweb_company_id"+account,company_id,60*600)
	return company_id
def getOrderadlist(pkind,e):
	listdir=cache.get("seoweb_Orderadlist"+str(pkind)+str(e))
	listdir=None
	if not listdir:
		sql="select ad_content,ad_target_url,DATE_FORMAT(gmt_plan_end,'%Y') as ayear,DATE_FORMAT(gmt_plan_end,'%m') as amouth,DATE_FORMAT(gmt_plan_end,'%d') as aday,id,ad_title,ad_description from ad where position_id="+str(pkind)+" and gmt_plan_end>='"+str(date.today()+timedelta(days=0))+"' and review_status='Y' and sequence='"+str(e)+"' order by gmt_start asc limit 0,10"
		cursor_ad.execute(sql)
		alist = cursor_ad.fetchone()
		if alist:
			ad_description=alist[7]
			if (ad_description!="" or ad_description!=None):
				arrdescription=ad_description.split("|")
				if (len(arrdescription)>=3):
					ad_description={'title':arrdescription[0],'company':arrdescription[1],'price':arrdescription[2]}
				else:
					ad_description=None
			else:
				ad_description=None
				
			listdir={'id':alist[5],'picaddress':alist[0],'picurl':alist[1],'ayear':alist[2],'amouth':alist[3],'aday':alist[4],'ad_title':alist[5],'ad_description':ad_description,'num':''}
			cache.set("seoweb_Orderadlist"+str(pkind)+str(e),listdir,60*60)
			return listdir
		else:
			list={}
			return None
#获得广告位广告数
def getadpostionNum(akind):
	sql="select count(0) from ad where position_id="+str(akind)+" and gmt_plan_end>='"+str(date.today()+timedelta(days=0))+"' and review_status='Y'"
	cursor_ad.execute(sql)
	alist = cursor_ad.fetchone()
	if alist:
		return alist[0]
	else:
		return 1	
def subString(string,length):
	if not string:
		return ""
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
def formattime(value,flag=''):
	if value:
		if (flag==1):
			return value.strftime( '%-Y-%-m-%-d')
		else:
			return value.strftime( '%-Y-%-m-%-d %-H:%-M:%-S')
	else:
		return ''
#图片替换
def replacepic(htmlstr):
	nowhtml=htmlstr
	for n in range(1,20):
		head = nowhtml.find('<img')
		tail=len(nowhtml)
		if head != -1:
			cut = nowhtml[head:tail]
			src = cut.find('http')
			cut2 = cut[src:tail]
			quo = cut2.find('"')
			url = cut2[0:quo]
			nowhtml=cut2
			url=url.replace("http://","")
			url=url.replace("img1.zz91.com/","")
			newpicurl="http://img3.zz91.com/300x300/"+url+""
			htmlstr=htmlstr.replace(url,newpicurl)
	return htmlstr
#类别列表
def getindexcategorylist(code,showflag):
	listall=cache.get("seoweb_indexcategorylist"+str(code)+str(showflag))
	#listall=None
	if not listall:
		sql="select label,code from category_products where code like '"+str(code)+"____' order by sort asc"
		cursor.execute(sql)
		listall=[]
		catelist=cursor.fetchall()
		for a in catelist:
			if (showflag==1):
				sql1="select label from category_products where code like '"+str(a[1])+"____' order by sort asc"
				cursor.execute(sql1)
				listall_cate1=[]
				catelist1=cursor.fetchall()
				for b in catelist1:
					list1={'label':b[0],'label_hex':getjiami(b[0])}
					listall_cate1.append(list1)
			else:
				listall_cate1=None
			list={'label':a[0],'code':a[1],'label_hex':getjiami(a[0]),'catelist':listall_cate1}
			listall.append(list)
		if listall:
			cache.set("seoweb_indexcategorylist"+str(code)+str(showflag),listall,6)
	return listall

def getproducstcategorylist(code):
	listall=cache.get("seoweb_producstcategorylist"+str(code))
	if not listall:
		codelen=len(code)
		sql="select label,code from category_products where left(code,"+str(codelen)+")=%s and length(code)="+str(codelen+4)+" order by sort asc"
		cursor.execute(sql,code)
		catelist=cursor.fetchall()
		listall=[]
		for b in catelist:
			list={'code':b[1],'label':b[0],'sql':sql}
			listall.append(list)
		if listall:
			cache.set("seoweb_producstcategorylist"+str(code),listall,60*60)
	return listall
	
	
#相关供求类别
def getcategorylist(kname='',limitcount=''):
	kname_hex=''
	if kname:
		kname_hex=getjiami(kname)
	listall=cache.get("seoweb_categorylist"+kname_hex+str(limitcount))
	if not listall:
		port = settings.SPHINXCONFIG['port']
		cl = SphinxClient()
		cl.SetServer ( settings.SPHINXCONFIG['serverid'], port )
		cl.SetMatchMode ( SPH_MATCH_BOOLEAN )
		#cl.SetSortMode( SPH_SORT_EXTENDED,"sort desc" )
		if (limitcount!=''):
			cl.SetLimits (0,limitcount,limitcount)
		if (kname!=""):
			res = cl.Query ('@label '+str(kname),'category_products')
		else:
			res = cl.Query ('','category_products')
		if res:
			if res.has_key('matches'):
				tagslist=res['matches']
				listall=[]
				for match in tagslist:
					id=match['id']
					attrs=match['attrs']
					label=attrs['plabel']
					code=attrs['pcode']
					list1={'id':id,'code':code,'label':label}
					listall.append(list1)
				cache.set("seoweb_categorylist"+kname_hex+str(limitcount),listall,60*60)
				return listall

#------最新报价信息
def getindexpricelist(kname="",assist_type_id="",limitcount="",searchname="",titlelen=""):
	if (titlelen=="" or titlelen==None):
		titlelen=100
	price=settings.SPHINXCONFIG['name']['price']['name']
	serverid=settings.SPHINXCONFIG['name']['price']['serverid']
	port=settings.SPHINXCONFIG['name']['price']['port']
	cl = SphinxClient()
	cl.SetServer ( serverid, port )
	cl.SetMatchMode ( SPH_MATCH_BOOLEAN )
	cl.SetSortMode( SPH_SORT_EXTENDED,"gmt_order desc" )
	cl.SetLimits (0,limitcount,limitcount)
	if(assist_type_id!=None and assist_type_id!=""):
		cl.SetFilter('assist_type_id',[assist_type_id])
	if (kname):
		res = cl.Query ('@(title,tags) '+kname,'price')
	else:
		res = cl.Query ('','price')
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
				list1={'title':title,'id':id,'gmt_time':gmt_time,'fulltitle':attrs['ptitle'],'url':'http://price.zz91.com/priceDetails_'+str(id)+'.htm'}
				listall_baojia.append(list1)
			listcount_baojia=res['total_found']
			return listall_baojia
#------最新企业报价信息
def getcompanypricelist(kname="",limitcount="",titlelen=""):
	
	if (titlelen=="" or titlelen==None):
		titlelen=100
	port = settings.SPHINXCONFIG['port']
	cl = SphinxClient()
	cl.SetServer ( settings.SPHINXCONFIG['serverid'], port )
	cl.SetMatchMode ( SPH_MATCH_BOOLEAN )
	cl.SetSortMode( SPH_SORT_EXTENDED,"post_time desc" )
	cl.SetLimits (0,limitcount,limitcount)
	if (kname):
		res = cl.Query ('@title '+kname,'company_price')
	else:
		res = cl.Query ('','company_price')
	if res:
		if res.has_key('matches'):
			tagslist=res['matches']
			listall_baojia=[]
			for match in tagslist:
				id=match['id']
				attrs=match['attrs']
				title=subString(attrs['ptitle'],titlelen)
				title=title.replace("\\","-")
				gmt_time=attrs['ppost_time']
				list1={'title':title,'id':id,'gmt_time':gmt_time,'fulltitle':attrs['ptitle'],'url':'http://price.zz91.com/companyprice/priceDetails'+str(id)+'.htm'}
				listall_baojia.append(list1)
			listcount_baojia=res['total_found']
			return listall_baojia
#最新互助信息
def getindexbbslist(kname='',limitcount='',bbs_post_category_id=''):
	
	port = settings.SPHINXCONFIG['port']
	cl = SphinxClient()
	cl.SetServer ( settings.SPHINXCONFIG['serverid'], port )
	cl.SetMatchMode ( SPH_MATCH_BOOLEAN )
	cl.SetSortMode( SPH_SORT_EXTENDED,"post_time desc" )
	cl.SetLimits (0,limitcount,limitcount)
	if(bbs_post_category_id!=None and bbs_post_category_id!=""):
		cl.SetFilter('bbs_post_category_id',[bbs_post_category_id])
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
				title=attrs['ptitle']
				gmt_time=attrs['ppost_time']
				list1={'title':title,'id':id,'gmt_time':gmt_time}
				listall_news.append(list1)
			return listall_news
#最新互助信息 翻页
def getbbslist(kname,frompageCount,limitNum,category_id):
	port = settings.SPHINXCONFIG['port']
	cl = SphinxClient()
	cl.SetServer ( settings.SPHINXCONFIG['serverid'], port )
	cl.SetMatchMode ( SPH_MATCH_BOOLEAN )
	if (category_id):
		cl.SetFilter('bbs_post_category_id',[int(category_id)])
	cl.SetSortMode( SPH_SORT_EXTENDED,"post_time desc" )
	cl.SetLimits (frompageCount,limitNum,20000)
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
				sql="select content,account from bbs_post where id=%s"
				cursor.execute(sql,id)
				alist = cursor.fetchone()
				if alist:
					havepic=havepicflag(alist[0])
					content=filter_tags(alist[0][0:1000])[0:50]+'...'
					username=getusername(alist[1])
				attrs=match['attrs']
				title=attrs['ptitle']
				gmt_time=attrs['ppost_time']
				replycount=gethuzhureplaycout(id)
				list1={'title':title,'id':id,'gmt_time':gmt_time,'content':content,'nickname':username,'replycount':replycount,'havepic':havepic}
				listall_news.append(list1)
			listcount_news=res['total_found']
			return {'list':listall_news,'count':listcount_news}
#最新互助信息 翻页
def getbbsreplylist(kname,frompageCount,limitNum,bbs_post_id):
	port = settings.SPHINXCONFIG['port']
	cl = SphinxClient()
	cl.SetServer ( settings.SPHINXCONFIG['serverid'], port )
	cl.SetMatchMode ( SPH_MATCH_BOOLEAN )
	if (bbs_post_id):
		cl.SetFilter('bbs_post_id',[int(bbs_post_id)])
	cl.SetSortMode( SPH_SORT_EXTENDED,"post_time desc" )
	cl.SetLimits (frompageCount,limitNum,20000)
	if (kname):
		res = cl.Query ('@(title,tags) '+kname,'huzhureply')
	else:
		res = cl.Query ('','huzhureply')
	if res:
		if res.has_key('matches'):
			tagslist=res['matches']
			listall_news=[]
			lou=1
			for match in tagslist:
				id=match['id']
				sql="select content,account,gmt_created from bbs_post_reply where id=%s"
				cursor.execute(sql,id)
				alist = cursor.fetchone()
				if alist:
					content=filter_tags(alist[0][0:1000])[0:50]+'...'
					username=getusername(alist[1])
					gmt_time=alist[2].strftime( '%-Y-%-m-%-d %-H:%-M:%-S')
				attrs=match['attrs']
				title=attrs['ptitle']
				list1={'lou':lou,'title':title,'id':id,'gmt_time':gmt_time,'content':content,'nickname':username}
				lou=lou+1
				listall_news.append(list1)
			listcount_news=res['total_found']
			return {'list':listall_news,'count':listcount_news}
#报价列表 翻页
def getpricelist(kname,frompageCount,limitNum,category_id):
	port = settings.SPHINXCONFIG["port"]
	cl = SphinxClient()
	cl.SetServer ( settings.SPHINXCONFIG["serverid"], port )
	cl.SetMatchMode ( SPH_MATCH_BOOLEAN )
	if (category_id):
		cl.SetFilter('type_id',[int(category_id)])
	cl.SetSortMode( SPH_SORT_EXTENDED,"gmt_time desc" )
	cl.SetLimits (frompageCount,limitNum,20000)
	if (kname):
		res = cl.Query ('@(title,tags) '+kname,'price')
	else:
		res = cl.Query ('','price')
	if res:
		if res.has_key('matches'):
			tagslist=res['matches']
			listall_news=[]
			for match in tagslist:
				id=match['id']
				sql="select content,tags from price where id=%s and is_checked=1"
				cursor.execute(sql,id)
				alist = cursor.fetchone()
				if alist:
					content=filter_tags(alist[0][0:1000])[0:50]+'...'
					tags=alist[1]
				attrs=match['attrs']
				title=attrs['ptitle']
				gmt_time=attrs['gmt_time']
				list1={'title':title,'id':id,'gmt_time':gmt_time,'content':content,'tags':tags}
				listall_news.append(list1)
			listcount_news=res['total_found']
			return {'list':listall_news,'count':listcount_news}
# seo推荐页面使用 带趋势图 和厂家数 的报价
def getPriceListForTuijian(kname="",num=""):
	pricelist=settings.SPHINXCONFIG['name']['pricelist']['name']
	serverid=settings.SPHINXCONFIG['name']['pricelist']['serverid']
	port=settings.SPHINXCONFIG['name']['pricelist']['port']
	cl = SphinxClient()
	cl.SetServer ( serverid, port )
	cl.SetMatchMode ( SPH_MATCH_BOOLEAN )
	cl.SetSortMode( SPH_SORT_EXTENDED,"@weight DESC,postdate desc" )
	if num:
		limitnum=num
	else:
		limitnum=30
	cl.SetLimits (0,limitnum,limitnum)
	if (kname!="" and kname):
		res = cl.Query ('@(title,typename,label,label1,label2,spec,spec1,spec2,area,area1,area2) '+kname+'',pricelist)
	else:
		res = cl.Query ('',pricelist)
	listall=[]
	if res:
		if res.has_key('matches'):
			tagslist=res['matches']
			for match in tagslist:
				id=match['id']
				sql="select postdate,label,label1,label2,spec,spec1,spec2,area,area1,area2,price1,price2,price3,price4,price5,price6,unit,price,priceid,title from price_list where id=%s"
				cursor.execute(sql,[id])
				alist = cursor.fetchone()
				if alist:
					postdate=alist[0]
					label=alist[1]
					purl=None
					pcompcount=""
					if label:
						pcompcount=getpricelist_company_count(label)
						if pcompcount==0:
							purl=None
						else:
							purl="http://jiage.zz91.com/s/"+getjiami(label)+"-1/"
					if label==None:
						label=""
					label1=alist[2]
					if label1==None:
						label1=""
					label2=alist[3]
					if label2==None:
						label2=""
					spec=alist[4]
					if spec==None:
						spec=""
					spec1=alist[5]
					if spec1==None:
						spec1=""
					spec2=alist[6]
					if spec2==None:
						spec2=""
					area=alist[7]
					if area==None:
						area=""
					area1=alist[8]
					if area1==None:
						area1=""
					area2=alist[9]
					if area2==None:
						area2=""
					price1=alist[10]
					price2=alist[11]
					price3=alist[12]
					price4=alist[13]
					price5=alist[14]
					price6=alist[15]
					unit=alist[16]
					if unit==None:
						unit=""
					price=alist[17]
					if not price:
						price=""
					priceid=alist[18]
					title=alist[19]
					list={'id':id,'priceid':priceid,'title':title,'postdate':postdate,'label':label,'label1':label1,'label2':label2,'spec':spec,'spec1':spec1,'spec2':spec2,'area':area,'area1':area1,'area2':area2,'price':price,'price1':price1,'price2':price2,'price3':price3,'price4':price4,'price5':price5,'price6':price6,'unit':unit,'pcompcount':pcompcount,'purl':purl}
					listall.append(list)
					
	return listall
#企业报价条数
def getpricelist_company_count(kname):
	company_price=settings.SPHINXCONFIG['name']['company_price']['name']
	serverid=settings.SPHINXCONFIG['name']['company_price']['serverid']
	port=settings.SPHINXCONFIG['name']['company_price']['port']
	
	cl = SphinxClient()
	cl.SetServer ( serverid, port )
	cl.SetMatchMode ( SPH_MATCH_BOOLEAN )
	cl.SetSortMode( SPH_SORT_EXTENDED,"post_time desc" )
	cl.SetLimits (0,1,1)
	try:
		res = cl.Query ('@(title,label1,label2,label3,area1,area2,area3) '+kname+'',company_price)
		if res:
			return res['total_found']
		return 0
	except:
		return 0
#公司信息列表 翻页
def getcompanylist(kname,frompageCount,limitNum):
	port = settings.SPHINXCONFIG['port']
	cl = SphinxClient()
	cl.SetServer ( settings.SPHINXCONFIG['serverid'], port )
	cl.SetMatchMode ( SPH_MATCH_BOOLEAN )
	cl.SetSortMode( SPH_SORT_EXTENDED,"membership_code desc" )
	cl.SetLimits (frompageCount,limitNum,20000)
	if (kname):
		res = cl.Query ('@(name,business,address,sale_details,buy_details,tags,area_name,area_province) '+kname,'company')
	else:
		res = cl.Query ('','company')
	if res:
		if res.has_key('matches'):
			tagslist=res['matches']
			listall_comp=[]
			for match in tagslist:
				id=match['id']
				attrs=match['attrs']
				compname=attrs['compname']
				viptype=str(attrs['membership_code'])
				membership="普通会员"
				if (viptype == '10051000'):
					membership='普通会员'
				if (viptype == '10051001'):
					membership='再生通'
				if (viptype == '1725773192'):
					membership='银牌品牌通'
				if (viptype == '1725773193'):
					membership='金牌品牌通'
				if (viptype == '1725773194'):
					membership='钻石品牌通'
				pbusiness=filter_tags(attrs['pbusiness'][0:1000])[0:150]+'...'
				parea_province=attrs['parea_province']
				list1={'id':id,'compname':compname,'business':pbusiness,'area_province':parea_province,'membership':membership,'viptype':viptype}
				listall_comp.append(list1)
			listcount_comp=res['total_found']
			return {'list':listall_comp,'count':listcount_comp}
#发布者 回复者
def getusername(account):
	nickname=cache.get("seoweb_username"+str(account))
	if not nickname:
		sqlu="select nickname from bbs_user_profiler where account=%s"
		cursor.execute(sqlu,account)
		ulist = cursor.fetchone()
		if ulist:
			nickname= ulist[0]
			if (nickname==None):
				sqlu="select contact from company_account where account=%s"
				cursor.execute(sqlu,account)
				ulist = cursor.fetchone()
				if ulist:
					nickname=ulist[0]
			if nickname:
				cache.set("seoweb_username"+str(account),nickname,60*20)
	return nickname
#回复数
def gethuzhureplaycout(bbs_post_id):
	sqlr="select count(0) from bbs_post_reply where bbs_post_id=%s"
	cursor.execute(sqlr,str(bbs_post_id))
	rlist = cursor.fetchone()
	if rlist:
		return rlist[0]
#价格分类
def getcate(categoryId):
	catestr=cache.get("seoweb_cate"+str(categoryId))
	if not catestr:
		sql="select name,id from price_category where parent_id=%s"
		cursor.execute(sql,str(categoryId))
		alist = cursor.fetchall()
		catestr=""
		if alist:
			listall=[]
			catestr="<table class='cate-tb-inner'><tr>"
			i=0
			for a in alist:
				id=a[1]
				name=a[0]
				list={'id':id,'name':name}
				mm=i % 2
				catestr=catestr+"<td><a href='/priceindex/?id="+str(id)+"&pname="+str(name)+"'><div class='c6'>"+str(name)+"</div></a></td>"
				if (str(mm) == "1"):
					catestr=catestr+"</tr><tr>"
				i=i+1
			catestr=catestr+"</tr></table>"
		cache.set("seoweb_cate"+str(categoryId),catestr,60*60)
	return catestr
#获得帐号
def getcompanyaccount(company_id):
	sql="select account from  company_account where company_id=%s"
	cursor.execute(sql,[company_id])
	result=cursor.fetchone()
	if (result):
		return result[0]
#获得公司ID
def getcompany_id(cname,regtime):
	sql="select id from company where name=%s and gmt_created=%s"
	cursor.execute(sql,[str(cname),str(regtime)])
	newcode=cursor.fetchone()
	if (newcode == None):
		return '0'
	else:
		return newcode[0]
#获得公司名称
def getcompanyname(uname):
	listdir=cache.get("seoweb_companyname"+str(uname))
	if not listdir:
		sql="select company_id from company_account where account=%s"
		cursor.execute(sql,[uname])
		newcode=cursor.fetchone()
		if (newcode):
			company_id=newcode[0]
			sqlc="select name from company where id=%s"
			cursor.execute(sqlc,[company_id])
			clist=cursor.fetchone()
			if clist:
				listdir={'company_id':company_id,'companyname':clist[0]}
				cache.set("seoweb_companyname"+str(uname),listdir,60*60)
	return listdir

#公司供求信息 翻页
def getcompanyproductslist(kname="",frompageCount="",limitNum="",company_id="",pdt_type="",seriesid='',fcflag='',haveprice="",maxcount=20000,groupbyflag=""):
	if not seriesid:
		if fcflag:
			cl = SphinxClient()
			servername=settings.SPHINXCONFIG["serverid"]
			serverport=settings.SPHINXCONFIG["port"]
			cl.SetServer ( servername, serverport )
			cl.SetMatchMode ( SPH_MATCH_BOOLEAN )
			if (company_id):
				cl.SetFilter('company_id',[int(company_id)])
			if (pdt_type !='' and pdt_type!=None):
				cl.SetFilter('pdt_kind',[int(pdt_type)])
			if haveprice:
				cl.SetFilter('min_price',[0],True)
			if groupbyflag:
				cl.SetGroupBy('company_id',SPH_GROUPBY_ATTR)
			cl.SetSortMode( SPH_SORT_EXTENDED,"refresh_time desc" )
			cl.SetLimits (frompageCount,limitNum,maxcount)
			if (kname and str(kname)!=""):
				res = cl.Query ('@(title,label0,label1,label2,label3,label4,city,province,tags) '+kname,'offersearch_new,offersearch_new_vip')
			else:
				res = cl.Query ('','offersearch_new,offersearch_new_vip')
			listall=[]
			listcount=0
			if res:
				if res.has_key('matches'):
					tagslist=res['matches']
					for match in tagslist:
						id=match['id']
						list=getcompinfo(id,cursor,kname)
						if list :
							pdtimgs=list['pdt_images']
							#pdtimgs=pdtimgs.replace('width=150&height=150','width=100&height=75')
							list['pdt_images']=pdtimgs
							listall.append(list)
					listcount=res['total_found']
			return {'list':listall,'count':listcount}
		else:	
			listcount=0
			sql="select count(0) from products where company_id=%s and is_del=0 and is_pause=0 and check_status=1"
			cursor.execute(sql,[company_id])
			alist=cursor.fetchone()
			if alist:
				listcount=alist[0]
				
			sql="select id,source from products where company_id=%s and is_del=0  and is_pause=0 and check_status=1 limit %s,%s"
			cursor.execute(sql,[company_id,frompageCount,limitNum])
			alist=cursor.fetchall()
			listall=[]
			if alist:
				for list in alist:
					id=list[0]
					list=getcompinfo(id,cursor,kname)
					pdtimgs=list['pdt_images']
					#pdtimgs=pdtimgs.replace('width=150&height=150','width=100&height=75')
					list['pdt_images']=pdtimgs
					listall.append(list)
			return {'list':listall,'count':listcount}
		
	else:
		sql="select count(0) from products_series_contacts where products_series_id=%s"
		cursor.execute(sql,[seriesid])
		alist=cursor.fetchone()
		if alist:
			listcount=alist[0]
		sql="select products_id from products_series_contacts where products_series_id=%s"
		cursor.execute(sql,[seriesid])
		alistall=cursor.fetchall()
		listall=[]
		if alistall:
			for alist in alistall:
				list=getcompinfo(alist[0],cursor,kname)
				listall.append(list)
		return {'list':listall,'count':listcount}
def getcompanyprolist(frompageCount="",limitNum="",company_id=""):
	cl = SphinxClient()
	servername=settings.SPHINXCONFIG["serverid"]
	serverport=settings.SPHINXCONFIG["port"]
	cl.SetServer ( servername, serverport )
	cl.SetMatchMode ( SPH_MATCH_BOOLEAN )
	if (company_id):
		cl.SetFilter('company_id',[int(company_id)])
	cl.SetSortMode( SPH_SORT_EXTENDED,"refresh_time desc" )
	cl.SetLimits (frompageCount,limitNum,limitNum)
	res = cl.Query ('','offersearch_new,offersearch_new_vip')
	listall=[]
	listcount=0
	if res:
		if res.has_key('matches'):
			tagslist=res['matches']
			i=1
			for match in tagslist:
				id=match['id']
				list=getproductdetail(id)
				listall.append(list)
				list['n']=str(i)
				i=i+1
				if i>=3:
					i=1
			listcount=res['total_found']
	return {'list':listall,'count':listcount}
#ppc供求信息 翻页
def getPpcProductsList(keywords="",frompageCount="",limitNum="",pdt_type=""):
	cl = SphinxClient()
	servername=settings.SPHINXCONFIG["serverid"]
	serverport=settings.SPHINXCONFIG["port"]
	cl.SetServer ( servername, serverport )
	cl.SetMatchMode ( SPH_MATCH_BOOLEAN )
	if (pdt_type !='' and pdt_type!=None):
		cl.SetFilter('pdt_kind',[int(pdt_type)])
	cl.SetGroupBy("company_id",SPH_GROUPBY_ATTR)
	cl.SetSortMode( SPH_SORT_EXTENDED,"refresh_time desc" )
	cl.SetLimits (frompageCount,limitNum,20000)
	if (keywords):
		res = cl.Query ('@(title,label0,label1,label2,label3,label4,city,province,tags) '+keywords,'offersearch_ppc')
	else:
		res = cl.Query ('','offersearch_ppc')
	listall=[]
	listcount=0
	if res:
		if res.has_key('matches'):
			tagslist=res['matches']
			for match in tagslist:
				id=match['id']
				list=getcompinfo(id,cursor,keywords)
				pdtimgs=list['pdt_images']
				attrs=match['attrs']
				front_tel=attrs['front_tel']
				list['pdt_images']=pdtimgs
				list['ldbtel']=front_tel
				listall.append(list)
			listcount=res['total_found']
	return {'list':listall,'count':listcount}

#获得公司供求分类
def getproductsseries(company_id):
	listall=cache.get("seoweb_productsseries"+str(company_id))
	if not listall:
		sql="select id,name from products_series where company_id=%s"
		cursor.execute(sql,[company_id])
		alist=cursor.fetchall()
		listall=[]
		if alist:
			for list in alist:
				list={'id':list[0],'name':list[1]}
				listall.append(list)
			cache.set("seoweb_productsseries"+str(company_id),listall,60*60)
	return listall
#---供求列表
def getindexofferlist(kname,pdt_type="",limitcount=""):
	port = settings.SPHINXCONFIG["port"]
	cl = SphinxClient()
	cl.SetServer ( settings.SPHINXCONFIG["serverid"], port )
	cl.SetMatchMode ( SPH_MATCH_BOOLEAN )
	cl.SetSortMode( SPH_SORT_EXTENDED," refresh_time desc" )
	cl.SetLimits (0,limitcount,limitcount)
	if (pdt_type):
		cl.SetFilter('pdt_kind',[int(pdt_type)])
	if (kname==None):
		res = cl.Query ('','offersearch_new,offersearch_new_vip')
	else:
		res = cl.Query ('@(title,label0,label1,label2,label3,label4,city,province,tags) '+kname,'offersearch_new,offersearch_new_vip')
	if res:
		if res.has_key('matches'):
			itemlist=res['matches']
			listall_offerlist=[]
			for match in itemlist:
				pid=match['id']
				attrs=match['attrs']
				pdt_date=attrs['pdt_date']
				sql="select refresh_time from products where id="+str(pid)+""
				cursor.execute(sql)
				productlist = cursor.fetchone()
				if productlist:
					pdt_date=productlist[0].strftime( '%-Y-%-m-%-d')
				title=subString(attrs['ptitle'],40)
				list={'id':pid,'title':title,'gmt_time':pdt_date,'fulltitle':attrs['ptitle']}
				listall_offerlist.append(list)
			return listall_offerlist

#获得诚信认证文件
def getcertificatefile(company_id):
	listall=cache.get("seoweb_certificatefile"+str(company_id))
	if not listall:
		sql="select file_name,start_time,end_time,organization,pic_name from credit_file where company_id=%s and check_status=1"
		cursor.execute(sql,[company_id])
		alist=cursor.fetchone()
		listall=[]
		if alist:
			for list in alist:
				list={'file_name':alist[0],'start_time':alist[1],'end_time':alist[2],'organization':alist[3],'pic_name':alist[4]}
				listall.append(list)
			cache.set("seoweb_certificatefile"+str(company_id),listall,60*60)
	return listall
#过期证书
def getcertificatefile2(company_id):
	listdir=cache.get("seoweb_certificatefile2"+str(company_id))
	if not listdir:
		time2=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
		sql="select count(id) from credit_file where end_time<%s and company_id=%s"
		cursor.execute(sql,[time2,company_id])
		alist=cursor.fetchone()
		if alist:
			listdir=alist[0]
			cache.set("seoweb_certificatefile2"+str(company_id),listdir,60*60)
	return listdir
#获得诚信指数
def getcompanyintegral(company_id):
	sql="select sum(integral) from credit_integral_details where company_id=%s"
	cursor.execute(sql,[company_id])
	alist=cursor.fetchone()
	if alist:
		return alist[0]
#获得类别名称
def getcategoryname(code):
	sqld="select label from category where code=%s"
	cursor.execute(sqld,[code])
	returnlabel = cursor.fetchone()
	if returnlabel:
		return returnlabel[0]

#认证状态
def getcheck_status(company_id):
	sqlc="select check_status from company_attest where company_id=%s"
	cursor.execute(sqlc,[company_id])
	clist=cursor.fetchone()
	if clist:
		check_status=clist[0]
		return check_status
#是否通过认证
def getrenzheng(company_id):
	sql = "SELECT id FROM  company_attest where company_id = %s and check_status = '1' "
	cursor.execute(sql,[company_id])
	attestResult = cursor.fetchone()
	if attestResult:
		return 1
	else :
		sql="select id from credit_file where company_id=%s and check_status='1'"
		cursor.execute(sql,[company_id])
		attestResult = cursor.fetchone()
		if attestResult:
			return 1
		else:
			return None
# 诚信档案营业执照
def getcredit_file(company_id):
	sqlc="select file_name,pic_name from credit_file where company_id=%s and check_status='1' and category_code in ('10401000','10401001','10401002','10401003','10401005')"
	cursor.execute(sqlc,[company_id])
	clist=cursor.fetchall()
	listall=[]
	if clist:
		for c in clist:
			filename=c[0]
			if (not filename):
				filename=""
			filepath=c[1]
			if (not filepath):
				filepath=""
			filepath1='http://img3.zz91.com/150x150/'+filepath
			filepath2='http://img3.zz91.com/800x800/'+filepath
			list={'filename':filename,'filepath':filepath1,'filepath_big':filepath2}
			listall.append(list)
	sqlc="select pic_address,attest_type from company_attest where company_id=%s and check_status='1' and attest_type='1'"
	cursor.execute(sqlc,[company_id])
	clist=cursor.fetchall()
	if clist:
		for c in clist:
			filename="营业执照"
			if c[1]=="0":
				filename='身份证'
			if (not filename):
				filename=""
			filepath=c[0]
			if (not filepath):
				filepath=""
			if filepath:
				filepath2='http://img3.zz91.com/800x800/'+filepath
				filepath1='http://img3.zz91.com/150x150/'+filepath
				list={'filename':filename,'filepath':filepath1,'filepath_big':filepath2}
				listall.append(list)
	return listall
#----公司图片
def getcompanyimg(company_id,flag):
	if flag:
		sqlc="select filename,filepath from company_upload_file where company_id=%s"
		cursor.execute(sqlc,[company_id])
		clist=cursor.fetchall()
		listall=[]
		if clist:
			for c in clist:
				filename=c[0]
				if (filename==None or str(filename)=='null'):
					filename=""
				filepath=c[1]
				if (filepath==None or str(filepath)=='null'):
					filepath=""
				filepath1='http://img3.zz91.com/250x250/'+filepath+filename
				list={'filename':filename,'filepath':filepath1}
				listall.append(list)
		return listall
	else:
		return getcompanyimgone(company_id)
#----公司图片一张
def getcompanyimgone(company_id):
	listdir=cache.get("seoweb_companyimgone"+str(company_id))
	if not listdir:
		sqlc="select filename,filepath from company_upload_file where company_id=%s"
		cursor.execute(sqlc,[company_id])
		clist=cursor.fetchone()
		list=None
		if clist:
			filename=clist[0]
			if (filename==None or str(filename)=='null'):
				filename=""
			filepath=clist[1]
			if (filepath==None or str(filepath)=='null'):
				filepath=""
			filepath1='http://img3.zz91.com/250x250/'+filepath+filename
			listdir={'filename':filename,'filepath':filepath1}
			cache.set("seoweb_companyimgone"+str(company_id),listdir,60*60)
	return listdir
#----公司图片列表
def getcompanyimgall(frompageCount,limitNum,company_id):
	sqlc="select filename,filepath from company_upload_file where company_id=%s order by id desc limit "+str(frompageCount)+','+str(limitNum)
	cursor.execute(sqlc,[company_id])
	clistall=cursor.fetchall()
	listall=[]
	if clistall:
		for clist in clistall:
			filename=clist[0]
			if not filename:
				filename=""
			filepath=clist[1]
			if not filepath:
				filepath=""
			filepath1='http://img3.zz91.com/250x250/'+filepath+filename
			list={'filename':filename,'filepath':filepath1}
			listall.append(list)
	return listall

#公司详情
def getcompanydetail(company_id):
	listdir=cache.get("seoweb_companydetails"+str(company_id))
	if listdir:
		return listdir
	showcontact=None
	if not listdir:
		sqlc="select c.name,c.business,c.regtime,c.address,c.introduction,c.membership_code,e.label,c.area_code,c.address_zip,c.zst_year,c.sale_details,c.buy_details,c.website,c.industry_code,c.tags,c.domain_zz91,c.service_code,c.classified_code from company as c  LEFT OUTER JOIN category as e ON c.area_code=e.code where c.id=%s"
		cursor.execute(sqlc,company_id)
		clist=cursor.fetchone()
		if clist:
			compname=clist[0]
			business=clist[1]
			regtime=clist[2]
			address=clist[3]
			introduction=clist[4]
			introduction_s=subString(filter_tags_ppc(introduction),200)
			viptype=clist[5]
			province=clist[6]
			if not province:
				province=""
			area_code=clist[7]
			address_zip=clist[8]
			zst_year=clist[9]
			sale_details=clist[10]
			buy_details=clist[11]
			website=clist[12]
			industry_code=clist[13]
			ctags=clist[14]
			domain_zz91=clist[15]
			service_code=clist[16]
			classified_code=clist[17]
			servicename=getcategoryname(service_code)
			industry=getcategoryname(industry_code)
			classified=getcategoryname(classified_code)
			#地区信息
			if (area_code):
				sqld="select label from category where code='"+str(area_code[:-4])+"'"
				cursor.execute(sqld)
				arealabel = cursor.fetchone()
				if arealabel:
					if arealabel[0]:
						province=arealabel[0]+' '+province
			arrviptype={'vippic':'','vipname':'','vipcheck':''}
			if (viptype == '10051000'):
				arrviptype['vippic']=None
				arrviptype['vipname']='普通会员'
			if (viptype == '10051001'):
				arrviptype['vippic']='http://img0.zz91.com/zz91/tradelist/images/zst_logo.jpg'
				arrviptype['vipname']='再生通'
			if (viptype == '100510021000'):
				arrviptype['vippic']='http://img0.zz91.com/zz91/tradelist/images/ypppt_logo.jpg'
				arrviptype['vipname']='银牌品牌通'
			if (viptype == '100510021001'):
				arrviptype['vippic']='http://img0.zz91.com/zz91/tradelist/images/jpppt_logo.jpg'
				arrviptype['vipname']='金牌品牌通'
			if (viptype == '100510021002'):
				arrviptype['vippic']='http://img0.zz91.com/zz91/tradelist/images/zsppt_logo.jpg'
				arrviptype['vipname']='钻石品牌通'
			if (viptype == '10051003'):
				arrviptype['vippic']='http://img0.zz91.com/zz91/tradelist/images/ldb_logo.jpg'
				arrviptype['vipname']='来电宝'
			if (viptype == '10051000'):
				# 1.判断是否为 百度优化会员
				sql="select count(*) from crm_company_service where company_id=%s and crm_service_code='10001002' and apply_status='1' and gmt_end>now() and now()>=gmt_start"
				cursor.execute(sql,[company_id])
				baiduResult = cursor.fetchone()
				if baiduResult and baiduResult[0]>0:
					arrviptype['vipcheck']=1
				else:
					arrviptype['vipcheck']=None
				showcontact=None
			else:
				arrviptype['vipcheck']=1
				showcontact=1
				
			
			
			#获取公司logo
			#logo_pic=None
			#sqlc="select logo_pic from esite_config where company_id=%s"
			#cursor.execute(sqlc,[company_id])
			#alist=cursor.fetchone()
			#if alist:
				#logo_pic=json.loads(alist[0].decode('utf8','ignore'))
				#if logo_pic:
					#logo_pic=logo_pic['url']
			logo_pic='http://b.zz91.com/ppc/img/logo.png'
			sqlc="select contact,tel_country_code,tel_area_code,tel,mobile,fax_country_code,fax_area_code,fax,email"
			sqlc=sqlc+",sex,position,qq,is_use_back_email,back_email,account,weixin "
			sqlc=sqlc+"from company_account where company_id=%s"
			cursor.execute(sqlc,[company_id])
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
				mobile=alist[4][0:26]
				fax_country_code=alist[5]
				fax_area_code=alist[6]
				fax=alist[7]
				email=alist[8]
				sex=alist[9]
				if str(sex)=="0":
					sex="先生"
				if str(sex)=="1":
					sex="女士"
				if str(sex)=="男":
					sex="先生"
				if str(sex)=="女":
					sex="女士"
				if contact:
					if str(sex) in str(contact):
						sex=''
				if not sex:
					sex=''
				position=alist[10]
				if (position==None):
					position=""
				position=position.strip()
				qq=alist[11]
				is_use_back_email=alist[12]
				back_email=alist[13]
				account=alist[14]
				weixin = alist[15]
				if str(is_use_back_email)=="1":
					email=back_email
				
				#是否诚信认证，未认证的公司直接显示  个体经营（）
				isrenzheng=getrenzheng(company_id)
				if not isrenzheng:
					compname="个体经营("+str(contact)+")"
				ppcphone_zhuan=''
				sqlc="select front_tel,tel,photo_cover from phone where company_id=%s and expire_flag=0"
				cursor.execute(sqlc,[company_id])
				alist=cursor.fetchone()
				if alist:
					ppcphone=alist[0]
					photo_cover=alist[2]
					if '转分机' in ppcphone:
						ppcphonelist=ppcphone.split('转分机')
						ppcphone1=ppcphonelist[0]
						ppcphone_zhuan='转分机'+ppcphonelist[1]
						
					tel=alist[1]
					if (len(tel)>10):
						fjtel=tel[11:15]
					else:
						fjtel=None
					tel=tel[0:10]
					if not photo_cover:
						midpic="http://b.zz91.com/ppc/img/banner.png"
					else:
						midpic="http://img3.zz91.com/980x280/"+photo_cover
				else:
					ppcphone=None
					fjtel=None
					midpic=None
				#百度优化客户
				sql1="select id from crm_company_service where company_id=%s and crm_service_code='10001002' and apply_status=1 and gmt_end>='"+str(date.today())+"'"
				cursor.execute(sql1,[company_id])
				fqrflag = cursor.fetchone()
				if fqrflag:
					baidu=1
					showcontact=1
				else:
					baidu=None
				#微站客户
				sql1="select id from crm_company_service where company_id=%s and crm_service_code='10001007' and apply_status=1 and gmt_end>='"+str(date.today())+"'"
				cursor.execute(sql1,[company_id])
				fqrflag = cursor.fetchone()
				if fqrflag:
					weizhan=1
					showcontact=1
				else:
					weizhan=None
					
				
				if company_id:
					companymarket=getcompanymarket(company_id)
				
				# 来电宝积分等级
				sqlg="select level from ldb_level where company_id="+str(company_id)+""
				cursor.execute(sqlg)
				scoreresult=cursor.fetchone()
				if scoreresult :
					ldblevel = scoreresult[0]
				else:
					ldblevel = 1
				
				#多个联系人
				contactmore=[]
				if account:
					sqlc="select name,sex,tel,mobile,email,qq from company_account_contact where is_hidden=0 and account=%s"
					cursor.execute(sqlc,[account])
					result=cursor.fetchall()
					if result:
						for l in result:
							name1=l[0]
							sex1=l[1]
							if sex1=="0":
								sex1="先生"
							if sex1=="1":
								sex1="女士"
							tel1=l[2]
							if not tel1:
								tel1=None
							mobile1=l[3]
							if not mobile1:
								mobile1=None
							email1=l[4]
							if not email1:
								email1=None
							qq1=l[5]
							if not qq1:
								qq1=None
							clist={'name':name1,'sex':sex1,'tel':tel1,'mobile':mobile1,'email':email1,'qq':qq1}
						contactmore.append(clist)
				listdir={'name':compname,'businesstop':subString(business,200),'business':business,'ctags':ctags,'servicename':servicename,'classified':classified,'industry':industry,'regtime':regtime,'address':address,'address_zip':address_zip,'website':website,'zst_year':zst_year,'sale_details':sale_details,'buy_details':buy_details,'province':province,'introduction':introduction,'introduction_s':introduction_s,'contact':contact,'ppcphone':ppcphone,'ppcphone_zhuan':ppcphone_zhuan,'fjtel':fjtel,'tel_country_code':tel_country_code,'tel_area_code':tel_area_code,'tel':tel,'mobile':mobile,'fax_country_code':fax_country_code,'fax_area_code':fax_area_code,'fax':fax,'email':email,'sex':sex,'position':position,'qq':qq,'viptype':arrviptype,'domain_zz91':domain_zz91,'midpic':midpic,'companymarket':companymarket,'weizhan':weizhan,'showcontact':showcontact,'ldblevel':ldblevel,'contactmore':contactmore,'baidu':baidu,'logo_pic':logo_pic,'weixin':weixin}
		if listdir:
			cache.set("seoweb_companydetails"+str(company_id),listdir,60*10)
	return listdir
#--------------------------------------------------------------------------------------------------------
def getleavewords(qid):
	sql="select title,content,send_time,sender_account from inquiry where id=%s"
	cursor.execute(sql,qid)
	alist=cursor.fetchone()
	if alist:
		companyarray=getcompanyname(alist[3])
		list={'title':alist[0],'content':alist[1],'stime':formattime(alist[2],0),'companyarray':companyarray}
	return list
def getmoreproperty(listmore,text,value):
	if (value!="" and value!=None):
		value=value.strip()
		if value[0:4]=="1011":
			value=getcategorylabel(value)
		listmore.append({'property':text,'content':value})
	return listmore
#获得供求详细信息
def getproductdetail(id):
	listdir=cache.get("seoweb_prodetail"+str(id))
	if not listdir:
		sql="select company_id,title,details,location,provide_status,quantity,price_unit,quantity_unit,quantity,source"
		sql=sql+",specification,origin,impurity,color,useful,appearance,manufacture,min_price,max_price,tags,refresh_time,expire_time,products_type_code,ship_day"
		sql=sql+" from products where id=%s and is_del=0"
		cursor.execute(sql,str(id))
		plist=cursor.fetchone()
		if plist:
			company_id=plist[0]
			title=plist[1]
			details=plist[2]
			details=filter_tags(details)
			detailsfull=plist[2]
			details75=details[0:75]
			location=plist[3]
			if (location):
				if (location.strip()==''):
					location=None
			provide_status=plist[4]
			total_quantity=plist[5]
			
			quantity_unit=plist[7]
			
			if not quantity_unit:
				quantity_unit=''

			if (total_quantity=='' or total_quantity==' ' or total_quantity==None):
				total_quantity=None
			else:
				if quantity_unit not in total_quantity:
					total_quantity=total_quantity+quantity_unit
			if total_quantity==None:
				total_quantity=""
			
			quantity=plist[8]
			source=plist[9]
			if source:
				if (source.strip()==''):
					source=None
			specification=plist[10]
			origin=plist[11]
			impurity=plist[12]
			color=plist[13]
			useful=plist[14]
			appearance=plist[15]
			manufacture=plist[16]
			
			price_unit=plist[6]
			min_price=plist[17]
			max_price=plist[18]
			price=""
			if (min_price!=None and min_price!='' and str(min_price)!='0.0'):
				price=price+str(min_price)+'-'
			if (max_price!=None and max_price!='' and str(max_price)!='0.0'):
				price=price+str(max_price)
			if (price!="" and price_unit!=None and price_unit!=''):
				price=price+str(price_unit)
			if (price!="" and quantity_unit!=None and quantity_unit!=''):
				price=price+'/'+str(quantity_unit)
			if (price==''):
				price=None
			
			tags=plist[19]
			tagslist=None
			
			if tags:
				#tagslist=getdaohanglist(tags,num=15)
				tagslist=getcplist(tags,12)
				#tagsarray=tags.split(",")
				#tagslist=[]
				#for i in tagsarray:
					#l={'label':i,'label_hex':getjiami(i)}
					#tagslist.append(l)
			refresh_time=formattime(plist[20],0)
			expire_time=plist[21]
			if (str(expire_time)=='9999-12-31 23:59:59'):
				expire_time="长期有效"
			if (expire_time==None or expire_time==""):
				expire_time=None
			else:
				if (expire_time!="长期有效"):
					expire_time=formattime(expire_time,0)
			products_type_code=plist[22]
			ship_day = plist[23]
			if (str(products_type_code[-1])=="1"):
				products_type="求购"
			else:
				products_type="供应"
			sqlc="select name,business,regtime,address,introduction,membership_code,domain_zz91 from company where id=%s"
			cursor.execute(sqlc,company_id)
			clist=cursor.fetchone()
			if clist:
				compname=clist[0]
				business=clist[1]
				regtime=clist[2]
				address=clist[3]
				introduction=clist[4]
				viptype=clist[5]
				domain_zz91=clist[6]
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
				
			sqlc="select contact,tel_country_code,tel_area_code,tel,mobile,fax_country_code,fax_area_code,fax,email"
			sqlc=sqlc+",sex,position,qq,is_use_back_email,back_email,weixin "
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
				is_use_back_email=alist[12]
				back_email=alist[13]
				weixin=alist[14]
				if str(is_use_back_email)=="1":
					email=back_email
			sql1="select pic_address from products_pic where product_id=%s and check_status=1 order by is_default desc,id asc"
			cursor.execute(sql1,id)
			productspic = cursor.fetchone()
			if productspic:
				defaultimages=productspic[0]
			else:
				defaultimages=""
			if (defaultimages == '' or defaultimages == '0'):
				defaultimages='http://img0.zz91.com/front/images/global/noimage.gif'
			else:
				defaultimages='http://img3.zz91.com/300x300/'+defaultimages+''
				
			sql1="select pic_address from products_pic where product_id=%s and check_status=1"
			cursor.execute(sql1,id)
			productspic = cursor.fetchall()
			piclist=[]
			if productspic:
				im=1
				for p in productspic:
					pimages=p[0]
					if (pimages == '' or pimages == '0' or pimages==None):
						pdt_images='../cn/img/noimage.gif'
						pdt_images_big='../cn/img/noimage.gif'
					else:
						pdt_images="http://img3.zz91.com/300x180/"+pimages+""
						pdt_images_big="http://img3.zz91.com/350x350/"+pimages+""
					picurl={'im':str(im),'images':pdt_images,'images_big':pdt_images_big,'pdt_images_big':pdt_images_big}
					im=im+1
					piclist.append(picurl)
			sqlc="select front_tel from phone where company_id=%s and expire_flag=0"
			cursor.execute(sqlc,[company_id])
			alist=cursor.fetchone()
			if alist:
				ppcphone=alist[0]
			else:
				ppcphone=None
			#供求更多属性
			sqlm="select property,content from product_addproperties where pid=%s and is_del='0'"
			cursor.execute(sqlm,[id])
			resultmore=cursor.fetchall()
			listmore=[]
			if resultmore:
				for ll in resultmore:
					if (ll[1]!=None):
						contentp=ll[1].strip()
						if (contentp==""):
							contentp=None
					else:
						contentp=None
					list={'property':ll[0],'content':contentp}
					listmore.append(list)
					
			listmore=getmoreproperty(listmore,'货源地',source)
			listmore=getmoreproperty(listmore,'来源产品',origin)
			listmore=getmoreproperty(listmore,'产品规格',specification)
			listmore=getmoreproperty(listmore,'杂质含量',impurity)
			listmore=getmoreproperty(listmore,'颜色',color)
			listmore=getmoreproperty(listmore,'用途',useful)
			listmore=getmoreproperty(listmore,'外观',appearance)
			listmore=getmoreproperty(listmore,'加工说明',manufacture)
			
			listdir={'pdtid':id,'company_id':company_id,'title':title,'refresh_time':refresh_time,'expire_time':expire_time,'details':details,'detailsfull':detailsfull,'details75':details75,'location':location,'provide_status':provide_status,'total_quantity':total_quantity,'price':price,'price_unit':price_unit,'quantity_unit':quantity_unit,'quantity':quantity,'source':source,'specification':specification,'origin':origin,'impurity':impurity,'color':color,'useful':useful,'appearance':appearance,'manufacture':manufacture,'min_price':min_price,'max_price':max_price,'tags':tags,'compname':compname,'business':business,'regtime':regtime,'address':address,'introduction':introduction,'contact':contact,'ppcphone':ppcphone,'tel_country_code':tel_country_code,'tel_area_code':tel_area_code,'tel':tel,'mobile':mobile,'fax_country_code':fax_country_code,'fax_area_code':fax_area_code,'fax':fax,'email':email,'sex':sex,'position':position,'qq':qq,'piclist':piclist,'defaultimages':defaultimages,'viptype':arrviptype,'products_type_code':products_type_code,'products_type':products_type,'listmore':listmore,'tagslist':tagslist,'domain_zz91':domain_zz91,'weixin':weixin,'ship_day':ship_day}
			cache.set("seoweb_prodetail"+str(id),listdir,60*10)
	return listdir
#询盘留言列表 翻页
def getleavewordslist(frompageCount,limitNum,company_id):
	port = settings.SPHINXCONFIG["port"]
	cl = SphinxClient()
	cl.SetServer ( settings.SPHINXCONFIG["serverid"], port )
	cl.SetMatchMode ( SPH_MATCH_BOOLEAN )
	if (company_id):
		cl.SetFilter('rcomid',[int(company_id)])
	cl.SetSortMode( SPH_SORT_EXTENDED,"qid desc" )
	cl.SetLimits (frompageCount,limitNum,20000)
	res = cl.Query ('','question')
	if res:
		if res.has_key('matches'):
			tagslist=res['matches']
			listall=[]
			for match in tagslist:
				id=match['id']
				list=getleavewords(id)
				listall.append(list)
			listcount=res['total_found']
			return {'list':listall,'count':listcount}
			
#我的收藏夹
def getfavoritelist(frompageCount,limitNum,company_id):
	sql="select count(0) from myfavorite where company_id=%s"
	cursor.execute(sql,[company_id])
	alist=cursor.fetchone()
	if alist:
		listcount=alist[0]
	sql="select favorite_type_code,content_id,content_title from myfavorite where company_id=%s order by gmt_created desc limit "+str(frompageCount)+","+str(frompageCount+limitNum)+""
	cursor.execute(sql,[company_id])
	alist=cursor.fetchall()
	listall=[]
	if alist:
		for list in alist:
			favorite_type_code=list[0]
			content_id=list[1]
			content_title=list[2]
			if (favorite_type_code=="10091006" or favorite_type_code=="10091000" or favorite_type_code=="10091001" or favorite_type_code=="10091007"):
				favorite_type="供求信息"
				favorite_url="/detail/?id="+str(content_id)
				favorite_urls="/standard/productdetail/?pdtid="+str(content_id)
			if (favorite_type_code=="10091002" or favorite_type_code=="10091003"):
				favorite_type="公司信息"
				favorite_url="/companyinfo/?company_id="+str(content_id)
				favorite_urls="/standard/companyinfo/?company_id="+str(content_id)
			if (favorite_type_code=="10091004" or favorite_type_code=="10091003"):
				favorite_type="公司信息"
				favorite_url="/companyinfo/?company_id="+str(content_id)
				favorite_urls="/standard/companyinfo/?company_id="+str(content_id)
			if (favorite_type_code=="10091004"):
				favorite_type="报价信息"
				favorite_url="/priceviews/?id="+str(content_id)
				favorite_urls="/standard/priceviews/?id="+str(content_id)
			if (favorite_type_code=="10091005"):
				favorite_type="互助社区"
				favorite_url="/huzhuview/"+str(content_id)+".htm"
				favorite_urls="/standard/huzhuviews/"+str(content_id)+".htm"
			
			
			list={'favorite_type_code':favorite_type_code,'favorite_type':favorite_type,'favorite_url':favorite_url,'favorite_urls':favorite_urls,'content_id':content_id,'content_title':content_title}
			listall.append(list)
	return {'list':listall,'count':listcount}

#门市部公司动态  翻页
def getcompanynewslist(frompageCount,limitNum,company_id):
	sql="select count(0) from esite_news where company_id=%s"
	cursor.execute(sql,[company_id])
	alist=cursor.fetchone()
	if alist:
		listcount=alist[0]
	sql="select title,content,post_time,id from esite_news where company_id=%s order by gmt_created desc limit %s,%s"
	cursor.execute(sql,[company_id,frompageCount,limitNum])
	alist=cursor.fetchall()
	listall=[]
	if alist:
		for list1 in alist:
			title=list1[0]
			id=list1[3]
			content=subString(filter_tags(list1[1]),200)
			post_time=list1[2].strftime( '%-Y-%-m-%-d')
			list={'id':id,'title':title,'content':content,'post_time':post_time}
			listall.append(list)
	return {'list':listall,'count':listcount}
#门市部公司动态详细信息
def getcompanynewsdetails(company_id,id):
	listdir=cache.get("seoweb_companynewsdetails"+str(id))
	if not listdir:
		sql="select title,content,post_time from esite_news where company_id=%s and id=%s"
		cursor.execute(sql,[company_id,id])
		alist=cursor.fetchone()
		if alist:
			title=alist[0]
			content=alist[1]
			post_time=alist[2].strftime( '%-Y-%-m-%-d')
			listdir={'title':title,'content':content,'post_time':post_time}
			cache.set("seoweb_companynewsdetails"+str(id),listdir,60*60)
	return listdir
# 根据公司动态id获取详细信息
def getcompanynewsdetails2(nid):
	listdir=cache.get("seoweb_companynewsdetails2"+str(nid))
	if not listdir:
		sql="select title,content,post_time from esite_news where id=%s"
		cursor.execute(sql,[nid])
		alist=cursor.fetchone()
		if alist:
			title=alist[0]
			content=alist[1]
			post_time=alist[2].strftime( '%-Y-%-m-%-d')
			listdir={'title':title,'content':content,'post_time':post_time}
			cache.set("seoweb_companynewsdetails2"+str(nid),listdir,60*60)
	return listdir
#门市部公司动态详细页 上下资讯
def getcompanynewsnext(company_id,id):
	listall=cache.get("seoweb_companynewsnext"+str(company_id)+str(id))
	if not listall:
		listall={'news1':'','news2':''}
		sql="select title,post_time,id from esite_news where company_id=%s and id>%s order by id asc"
		cursor.execute(sql,[company_id,id])
		alist=cursor.fetchone()
		if alist:
			list={'title':alist[0],'post_time':alist[1],'id':alist[2]}
			listall['news1']=list
		sql="select title,post_time,id from esite_news where company_id=%s and id<%s order by id desc"
		cursor.execute(sql,[company_id,id])
		alist=cursor.fetchone()
		if alist:
			list={'title':alist[0],'post_time':alist[1],'id':alist[2]}
			listall['news2']=list
		cache.set("seoweb_companynewsnext"+str(company_id)+str(id),listall,60*60)
	return listall

#供求详细页报价信息
def gettradetags(tradeid):
	listdir=cache.get("seoweb_tradetags"+str(tradeid))
	if not listdir:
		sql="select category_products_main_code,tags from products where id=%s"
		cursor.execute(sql,tradeid)
		arrlist=cursor.fetchone()
		if arrlist:
			category_products_main_code=arrlist[0]
			tags=arrlist[1]
			if (tags!=None and tags!='' and tags!=' '):
				return tags
			else:
				sqlt="select label from category_products where code =%s"
				cursor.execute(sqlt,str(category_products_main_code))
				arrcatelist=cursor.fetchone()
				if arrcatelist:
					listdir=arrcatelist[0]
					cache.set("seoweb_tradetags"+str(tradeid),listdir,60*60)
	return listdir
def getfriend_link(company_id):
	listall=cache.get("seoweb_friend_link"+str(company_id))
	if not listall:
		sql="select link_name,link_address from esite_friend_link where company_id=%s "
		cursor.execute(sql,[company_id])
		alist=cursor.fetchall()
		listall=[]
		if alist:
			for list in alist:
				list={'link_name':list[0],'link_address':list[1]}
				listall.append(list)
			cache.set("seoweb_friend_link"+str(company_id),listall,60*60)
	return listall
#获得中文首拼音
def single_get_first(unicode1):
	str1 = unicode1.encode('gbk')
	try:		
		ord(str1)
		return str1
	except:
		asc = ord(str1[0]) * 256 + ord(str1[1]) - 65536
		if asc >= -20319 and asc <= -20284:
			return 'a'
		if asc >= -20283 and asc <= -19776:
			return 'b'
		if asc >= -19775 and asc <= -19219:
			return 'c'
		if asc >= -19218 and asc <= -18711:
			return 'd'
		if asc >= -18710 and asc <= -18527:
			return 'e'
		if asc >= -18526 and asc <= -18240:
			return 'f'
		if asc >= -18239 and asc <= -17923:
			return 'g'
		if asc >= -17922 and asc <= -17418:
			return 'h'
		if asc >= -17417 and asc <= -16475:
			return 'j'
		if asc >= -16474 and asc <= -16213:
			return 'k'
		if asc >= -16212 and asc <= -15641:
			return 'l'
		if asc >= -15640 and asc <= -15166:
			return 'm'
		if asc >= -15165 and asc <= -14923:
			return 'n'
		if asc >= -14922 and asc <= -14915:
			return 'o'
		if asc >= -14914 and asc <= -14631:
			return 'p'
		if asc >= -14630 and asc <= -14150:
			return 'q'
		if asc >= -14149 and asc <= -14091:
			return 'r'
		if asc >= -14090 and asc <= -13119:
			return 's'
		if asc >= -13118 and asc <= -12839:
			return 't'
		if asc >= -12838 and asc <= -12557:
			return 'w'
		if asc >= -12556 and asc <= -11848:
			return 'x'
		if asc >= -11847 and asc <= -11056:
			return 'y'
		if asc >= -11055 and asc <= -10247:
			return 'z'
		return ''
#根据供求获得公司ID
def getproductscompanyid(id):
	sql="select company_id from products where id=%s"
	cursor.execute(sql,[id])
	result=cursor.fetchone()
	if result:
		return result[0]
#根据公司动态获得公司ID
def getnewscompanyid(id):
	sql="select company_id from esite_news where id=%s"
	cursor.execute(sql,[id])
	result=cursor.fetchone()
	if result:
		return result[0]
#获得城市信息
def getnavareavalue(code):
	sql="select label,code from category where code='"+code+"'"
	cursor.execute(sql)
	result=cursor.fetchone()
	if result:
		area2=result[0]
		return result
#获得类别名称
def getcategorylabel(code):
	sql="select label from category where code='"+code+"'"
	cursor.execute(sql)
	result=cursor.fetchone()
	if result:
		return result[0]
		
def getnextareavalue(code):
	sql="select code,label from category where code like '"+str(code)+"____'"
	cursor.execute(sql)
	result=cursor.fetchone()
	if result:
		return 1
	else:
		return 0
def getproductscategoryname(id):
	sql="select label,code from category_products where id=%s"
	cursor.execute(sql,id)
	result=cursor.fetchone()
	if result:
		return result
def havepicflag(htmlstr):
	head = htmlstr.find('<img')
	tail=len(htmlstr)
	if head >0:
		return {'no':1}
	else:
		return None
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
	if htmlstr:
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
	else:
		return htmlstr
	
##过滤HTML中的标签
#将HTML中标签等信息去掉
#@param htmlstr HTML字符串.
import re
def filter_tags_ppc(htmlstr):
	#先过滤CDATA
	re_cdata=re.compile('//<!\[CDATA\[[^>]*//\]\]>',re.I) #匹配CDATA
	re_script=re.compile('<\s*script[^>]*>[^<]*<\s*/\s*script\s*>',re.I)#Script
	re_br=re.compile('<br\s*?/?>')#处理换行
	re_comment=re.compile('<!--[^>]*-->')#HTML注释
	if htmlstr:
		s=re_cdata.sub('',htmlstr)#去掉CDATA
		s=re_script.sub('',s) #去掉SCRIPT
		s=re_br.sub('\n',s)#将br转换为换行
		s=re.sub('<[^>]+>','',s) #去掉html代码
		s=re_comment.sub('',s)#去掉HTML注释
		#去掉多余的空行
		blank_line=re.compile('\n+')
		s=blank_line.sub('\n',s)
		s=replaceCharEntity(s)#替换实体
		return s
	else:
		return htmlstr

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

def getdatelist():
	nyear=getYear()
	nmonth=getMonth()
	yearlist=[]
	monthlist=[]
	for i in range(1,int(nmonth)+1):
		monthlist.append(i)
	for i in range(int(nyear),2004,-1):
		if (i!=int(nyear)):
			monthl=[1,2,3,4,5,6,7,8,9,10,11,12]
		else:
			monthl=monthlist
		list={'year':i,'month':monthl}
		yearlist.append(list)
	return yearlist
def getwebhtml(url):
	f = urllib.urlopen(url)
	html = f.read()
	return html

#来电宝客户
def getppccomplist(keywords='',fromNom='',limitNum='',havepic='',picsize='200x200'):
	port = settings.sphinxconfig['port']
	cl = SphinxClient()
	cl.SetServer ( settings.sphinxconfig['server'], port )
	cl.SetLimits (fromNom,limitNum,limitNum)
	if (havepic):
		cl.SetFilterRange('havepic',1,100)
	if (keywords):
		cl.SetMatchMode ( SPH_MATCH_BOOLEAN )
		cl.SetSortMode( SPH_SORT_EXTENDED," refresh_time desc" )
		cl.SetGroupBy("company_id",SPH_GROUPBY_ATTR)
		if '|' in keywords:
			keywd=keywords.split('|')
			query1=''
			for kwd in keywd:
				query1=query1+'@(title,label0,label1,label2,label3,label4,city,province,tags) "'+kwd+'"|'
			res = cl.Query (query1[:-1],'offersearch_ppc')
		else:
			res = cl.Query ('@(title,label0,label1,label2,label3,label4,city,province,tags) '+keywords,'offersearch_ppc')
	else:
		cl.SetMatchMode ( SPH_MATCH_BOOLEAN )
		cl.SetGroupBy("company_id",SPH_GROUPBY_ATTR)
		res = cl.Query ('','offersearch_ppc')
	listall=[]
	listcount=res['total_found']
	if (listcount==0):
		cl.SetMatchMode ( SPH_MATCH_ANY )
		cl.SetGroupBy("company_id",SPH_GROUPBY_ATTR)
		if '|' in keywords:
			keywd=keywords.split('|')
			query1=''
			for kwd in keywd:
				query1=query1+'@(title,label0,label1,label2,label3,label4,city,province,tags) "'+kwd+'"|'
			res = cl.Query (query1[:-1],'offersearch_ppc')
		else:
			res = cl.Query ('@(title,label0,label1,label2,label3,label4,city,province,tags) '+keywords,'offersearch_ppc')
#		res = cl.Query ('@(title,label0,label1,label2,label3,label4,city,province,tags) '+keywords,'offersearch_ppc')
	if res:
#		return res
		if res.has_key('matches'):
			tagslist=res['matches']
			
			for match in tagslist:
				id=match['id']
				attrs=match['attrs']
				company_id=attrs['company_id']
				ptitle=attrs['ptitle']
				ppckeywords1=attrs['ppckeywords']
				ppckeywords=subString(ppckeywords1,50)
				companyname=attrs['companyname']
				front_tel=attrs['front_tel']
				pdt_kind=attrs['pdt_kind']
				pdttxt=""
				if (str(pdt_kind)=="0"):
					pdttxt="供应"
				if (str(pdt_kind)=="1"):
					pdttxt="求购"
				sql1="select pic_address from products_pic where product_id=%s order by is_default desc,id desc"
				cursor.execute(sql1,id)
				productspic = cursor.fetchone()
				if productspic:
					pdt_images0=productspic[0]
					pdt_images='http://img3.zz91.com/'+picsize+'/'+pdt_images0+''
				else:
					pdt_images=None
				lis={'id':id,'ptitle':ptitle,'pdttxt':pdttxt,'pdt_images':pdt_images,'company_id':company_id,'ppckeywords':ppckeywords,'ppctel':front_tel,'companyname':companyname}
				listall.append(lis)
				if limitNum==1:
					return lis
	return listall

def getSuccessfulCase(frompageCount,limitNum):
	sql='select id,name,pic,url,content from website where wtype=5 order by sortrank,id desc limit '+str(frompageCount)+','+str(limitNum)
	cursor_other.execute(sql)
	result=cursor_other.fetchone()
	if result:
		list={'id':result[0],'name':result[1],'pic':result[2],'url':result[3],'content':result[4]}
		return list
	
#--判断手机端还是pc
def mobileuseragent(agent):
	data=["Nokia",#诺基亚，有山寨机也写这个的，总还算是手机，Mozilla/5.0 (Nokia5800 XpressMusic)UC AppleWebkit(like Gecko) Safari/530  
	"SAMSUNG",#三星手机 SAMSUNG-GT-B7722/1.0+SHP/VPP/R5+Dolfin/1.5+Nextreaming+SMM-MMS/1.2.0+profile/MIDP-2.1+configuration/CLDC-1.1  
	"MIDP-2",#j2me2.0，Mozilla/5.0 (SymbianOS/9.3; U; Series60/3.2 NokiaE75-1 /110.48.125 Profile/MIDP-2.1 Configuration/CLDC-1.1 ) AppleWebKit/413 (KHTML like Gecko) Safari/413  
	"CLDC1.1",#M600/MIDP2.0/CLDC1.1/Screen-240X320  
	"SymbianOS",#塞班系统的，  
	"MAUI",#MTK山寨机默认ua  
	"UNTRUSTED/1.0",#疑似山寨机的ua，基本可以确定还是手机  
	"Windows CE",#Windows CE，Mozilla/4.0 (compatible; MSIE 6.0; Windows CE; IEMobile 7.11)  
	"iPhone",#iPhone是否也转wap？不管它，先区分出来再说。Mozilla/5.0 (iPhone; U; CPU iPhone OS 4_1 like Mac OS X; zh-cn) AppleWebKit/532.9 (KHTML like Gecko) Mobile/8B117  
	"iPad",#iPad的ua，Mozilla/5.0 (iPad; U; CPU OS 3_2 like Mac OS X; zh-cn) AppleWebKit/531.21.10 (KHTML like Gecko) Version/4.0.4 Mobile/7B367 Safari/531.21.10  
	"Android",#Android是否也转wap？Mozilla/5.0 (Linux; U; Android 2.1-update1; zh-cn; XT800 Build/TITA_M2_16.22.7) AppleWebKit/530.17 (KHTML like Gecko) Version/4.0 Mobile Safari/530.17  
	"BlackBerry",#BlackBerry8310/2.7.0.106-4.5.0.182  
	"UCWEB",#ucweb是否只给wap页面？ Nokia5800 XpressMusic/UCWEB7.5.0.66/50/999  
	"ucweb",#小写的ucweb貌似是uc的代理服务器Mozilla/6.0 (compatible; MSIE 6.0;) Opera ucweb-squid  
	"BREW",#很奇怪的ua，例如：REW-Applet/0x20068888 (BREW/3.1.5.20; DeviceId: 40105; Lang: zhcn) ucweb-squid  
	"J2ME",#很奇怪的ua，只有J2ME四个字母  
	"YULONG",#宇龙手机，YULONG-CoolpadN68/10.14 IPANEL/2.0 CTC/1.0  
	"YuLong",#还是宇龙  
	"COOLPAD",#宇龙酷派YL-COOLPADS100/08.10.S100 POLARIS/2.9 CTC/1.0  
	"TIANYU",#天语手机TIANYU-KTOUCH/V209/MIDP2.0/CLDC1.1/Screen-240X320  
	"TY-",#天语，TY-F6229/701116_6215_V0230 JUPITOR/2.2 CTC/1.0  
	"K-Touch",#还是天语K-Touch_N2200_CMCC/TBG110022_1223_V0801 MTK/6223 Release/30.07.2008 Browser/WAP2.0  
	"Haier",#海尔手机，Haier-HG-M217_CMCC/3.0 Release/12.1.2007 Browser/WAP2.0  
	"DOPOD",#多普达手机  
	"Lenovo",# 联想手机，Lenovo-P650WG/S100 LMP/LML Release/2010.02.22 Profile/MIDP2.0 Configuration/CLDC1.1  
	"LENOVO",# 联想手机，比如：LENOVO-P780/176A  
	"HUAQIN",#华勤手机  
	"AIGO-",#爱国者居然也出过手机，AIGO-800C/2.04 TMSS-BROWSER/1.0.0 CTC/1.0  
	"CTC/1.0",#含义不明  
	"CTC/2.0",#含义不明  
	"CMCC",#移动定制手机，K-Touch_N2200_CMCC/TBG110022_1223_V0801 MTK/6223 Release/30.07.2008 Browser/WAP2.0  
	"DAXIAN",#大显手机DAXIAN X180 UP.Browser/6.2.3.2(GUI) MMP/2.0  
	"MOT-",#摩托罗拉，MOT-MOTOROKRE6/1.0 LinuxOS/2.4.20 Release/8.4.2006 Browser/Opera8.00 Profile/MIDP2.0 Configuration/CLDC1.1 Software/R533_G_11.10.54R  
	"SonyEricsson",# 索爱手机，SonyEricssonP990i/R100 Mozilla/4.0 (compatible; MSIE 6.0; Symbian OS; 405) Opera 8.65 [zh-CN]  
	"GIONEE",#金立手机  
	"HTC",#HTC手机  
	"ZTE",#中兴手机，ZTE-A211/P109A2V1.0.0/WAP2.0 Profile  
	"HUAWEI",#华为手机，  
	"webOS",#palm手机，Mozilla/5.0 (webOS/1.4.5; U; zh-CN) AppleWebKit/532.2 (KHTML like Gecko) Version/1.0 Safari/532.2 Pre/1.0  
	"GoBrowser",#3g GoBrowser.User-Agent=Nokia5230/GoBrowser/2.0.290 Safari  
	"IEMobile",#Windows CE手机自带浏览器，  
	"WAP2.0"]#支持wap 2.0的
	#agent=request.META['HTTP_USER_AGENT']
	for list in data:
		if list in agent:
			return 1

def getprotitle(id):
	sql='select title from products where id=%s'
	cursor.execute(sql,[id])
	result=cursor.fetchone()
	if result:
		return result[0]
	
#----读取来电宝推荐
def getppcrecom(data_index_code,fromNom,LimitNum,picsize='200x200'):
	sql='select id,title,products_id,company_id,products_type,refresh_time from products_index where data_index_code=%s order by id limit %s,%s'
	cursor.execute(sql,[data_index_code,fromNom,LimitNum])
	resultlist=cursor.fetchall()
	listall=[]
	if resultlist:
		for result in resultlist:
			id=result[0]
			products_id=result[2]
			title=getprotitle(products_id)
			company_id=result[3]
			products_type=result[4]
			refresh_time=formattime(result[5])
#			compinfo=getcompinfo(id)
			sql1="select pic_address from products_pic where product_id=%s order by is_default desc,id desc"
			cursor.execute(sql1,[products_id])
			productspic = cursor.fetchone()
			if productspic:
				pdt_images0=productspic[0]
				pdt_images='http://img3.zz91.com/'+picsize+'/'+pdt_images0+''
			else:
				pdt_images=''
			sql2="select front_tel from phone where company_id=%s and expire_flag=0"
			cursor.execute(sql2,[company_id])
			tel400 = cursor.fetchone()
			ppctel2=''
			if tel400:
				ppctel=tel400[0]
				if '转分机' in ppctel:
					ppctels=ppctel.split('转分机')
					ppctel=ppctels[0]
					ppctel2=ppctels[1]
			else:
				ppctel=''
			weburl='http://www.zz91.com/ppc/productdetail'+str(products_id)+'.htm'
			list={'id':id,'title':title,'products_id':products_id,'company_id':company_id,'products_type':products_type,'refresh_time':refresh_time,'pdt_images':pdt_images,'ppctel':ppctel,'ppctel2':ppctel2,'weburl':weburl}
			if LimitNum==1:
				return list
			listall.append(list)
	if len(listall)<LimitNum:
		numbnew=LimitNum-len(listall)
		xuwei={'id':'','title':'','products_id':'','company_id':'','products_type':'','refresh_time':'','pdt_images':'http://img1.zz91.com/bbs/2014/6/25/8b471aa4-ee53-45c3-91e2-1f8a1db370c5.jpg','ppctel':'','weburl':'http://www.zz91.com/ppc/'}
		for rg in range(0,numbnew):
			listall.append(xuwei)
	return listall
def getcategorylabel(code):
	if code:
		sql="select label from category where code='"+code+"'"
		cursor.execute(sql)
		result=cursor.fetchone()
		if result:
			return result[0]
#----来电宝
class laidianbaofunction():
	def __init__(self):
		self._account = None
		self._page=1
	#----判断是否样品
	def getyangflag(self,product_id):
		sql="select sample_id from sample_relate_product where product_id=%s"
		cursor.execute(sql,[product_id])
		productlist = cursor.fetchone()
		result = None
		if productlist:
			result = productlist[0]
		if result :
			sql1 = "select id from sample where id=%s and is_del=%s"
			cursor.execute(sql1,[result,'0'])
			sampleid = cursor.fetchone()
			if sampleid :
				return sampleid[0]
			else :
				return None
		else :
			return None
	def getyangprice(self,product_id):
		listdir=cache.get("seoweb_yangprice"+str(product_id))
		if not listdir:
			sql="select a.amount,a.weight,a.take_price,a.send_price,a.id,a.area_code,a.is_cashdelivery from sample as a left join sample_relate_product as b on a.id=b.sample_id where b.product_id=%s and a.is_del=0"
			cursor.execute(sql,[product_id])
			p = cursor.fetchone()
			list={}
			if p:
				amount=p[0]
				weight=p[1]
				take_price=p[2]
				send_price=p[3]
				id=p[4]
				area_code=p[5]
				is_cashdelivery=p[6]
				listdir={'id':id,'amount':amount,'weight':weight,'take_price':take_price,'send_price':send_price,'area_code':getcategorylabel(area_code),'is_cashdelivery':is_cashdelivery}
				cache.set("seoweb_yangprice"+str(product_id),listdir,60*60)
		return listdir
#----判断是否为再生通
def getiszstcompany(company_id):
	if company_id:
		sqll="select id from crm_company_service where company_id=%s and crm_service_code='1000' and apply_status=1 and DATEDIFF(CURDATE(),`gmt_end`)<=0"
		cursor.execute(sqll,company_id)
		zstresult=cursor.fetchone()
		if zstresult:
			return 1
#----获得公司二级域名
def getdomain_zz91(company_id):
	sql='select domain_zz91 from company where id=%s'
	cursor.execute(sql,company_id)
	result=cursor.fetchone()
	if result:
		domain_zz91=result[0]
		companyurl="http://"+domain_zz91+".zz91.com"
		return companyurl
#----再生通301跳转
def ppciszst301(company_id,arg=''):
	#iszst=getiszstcompany(company_id)
	#if iszst:
	domain_zz91=getdomain_zz91(company_id)+'/'+arg+'.htm'
	return HttpResponsePermanentRedirect(domain_zz91)
#----资讯列表
def getNewsList(keywords="",frompageCount="",limitNum="",typeid="",allnum="",typeid2="",contentflag=""):
	cursor_news = conn_news.cursor()
	news=settings.SPHINXCONFIG['name']['news']['name']
	serverid=settings.SPHINXCONFIG['name']['news']['serverid']
	port=settings.SPHINXCONFIG['name']['news']['port']
#	port = settings.SPHINXCONFIG['port']
	cl = SphinxClient()
	cl.SetServer ( serverid, port )
	cl.SetMatchMode ( SPH_MATCH_ANY )
	if (typeid):
		cl.SetFilter('typeid',typeid)
	if (typeid2):
		cl.SetFilter('typeid2',[typeid2])
	cl.SetSortMode( SPH_SORT_EXTENDED,'@weight DESC,@id desc' )
	if (allnum):
		cl.SetLimits (frompageCount,limitNum,allnum)
	else:
		cl.SetLimits (frompageCount,limitNum)
	if (keywords):
		res = cl.Query ('@(title,description) '+keywords,news)
	else:
		res = cl.Query ('',news)
	listall_news=[]
	listcount_news=0
	if res:
		if res.has_key('matches'):
			tagslist=res['matches']
			for match in tagslist:
				id=match['id']
				newsurl=get_newstype(id,cursor_news)
				weburl="http://news.zz91.com"
				if newsurl:
					if newsurl["url2"]:
						weburl+="/"+newsurl["url2"]
					weburl+="/"+newsurl["url"]+"/newsdetail1"+str(id)+".htm"
#				newsurl='news'
				attrs=match['attrs']
				fulltitle=attrs['ptitle']
				
				title=subString(fulltitle,100)
#				title=getlightkeywords(cl,[title],keywords,"news")
				
				pubdate=attrs['pubdate']
				pubdate2=timestamp_datetime2(pubdate)
#				havepic=havepicflag(content)
				#littlecontent=subString(filter_tags(content),60)
				list1={'title':title,'fulltitle':fulltitle,'id':id,'pubdate':pubdate2,'newsurl':newsurl,'weburl':weburl}
				listall_news.append(list1)
			listcount_news=res['total_found']
	return {'list':listall_news,'count':listcount_news}
#--获取资讯url
def get_newstype(id,cursor_news):
	listdir=cache.get("daohang_newstype"+str(id))
	if not listdir:
		sql='select typeid,typeid2 from dede_archives where id=%s'
		cursor_news.execute(sql,[id])
		result=cursor_news.fetchone()
		if result:
			typeid=result[0]
			typeid2=result[1]
			sql2='select typename,keywords from dede_arctype where id=%s'
			cursor_news.execute(sql2,[typeid])
			result2=cursor_news.fetchone()
			if result2:
				listdir={'typename':result2[0],'url':result2[1],'typeid':typeid,'typeid2':typeid2,'url2':''}
				if typeid2!='0':
					sql3='select keywords from dede_arctype where id=%s'
					cursor_news.execute(sql3,[typeid2])
					result3=cursor_news.fetchone()
					if result3:
						listdir['url2']=result3[0]
				cache.set("daohang_newstype"+str(id),listdir,60*60)
	return listdir
# 时间格式化
def timestamp_datetime2(value):
	format = '%Y-%m-%d'
	value = time.localtime(value)
	dt = time.strftime(format, value)
	return dt
# 获取供求信息
def getproductsinfo(pdtid,cursor,keywords):
	keywords=keywords.replace('\\','')
	keywords=keywords.replace('/','')
	keywords=keywords.replace('/','')
	keywords=keywords.replace('(','')
	keywords=keywords.replace(')','')
	keywords=keywords.replace('+','')
	sql="SELECT c.id AS com_id, c.name AS com_name, p.id AS pdt_id, RIGHT( p.products_type_code, 1 ) AS pdt_kind, p.title AS pdt_name, p.details AS pdt_detail, DATE_FORMAT(p.refresh_time,'%Y/%m/%d'), c.domain_zz91 AS com_subname, p.price AS pdt_price,c.membership_code,e.label as city,p.min_price,p.max_price,p.price_unit,p.quantity,DATE_FORMAT(p.expire_time,'%Y-%m-%d'),DATEDIFF(p.expire_time,CURDATE()) as yxtime,p.quantity_unit,f.label,c.address,DATE_FORMAT(c.regtime,'%Y-%m-%d'),c.area_code,p.check_status,p.tags,p.source,p.specification,p.impurity,p.color,p.useful,p.appearance,p.manufacture,p.origin,p.tags FROM products AS p LEFT OUTER JOIN company AS c ON p.company_id = c.id LEFT OUTER JOIN category as e ON c.area_code=e.code left outer join category_products as f on p.category_products_main_code=f.code where p.id="+str(pdtid)+""
	cursor.execute(sql)
	productlist = cursor.fetchone()
	if productlist:
		arrpdt_kind={'kindtxt':'','kindclass':''}
		pdt_kind=productlist[3]
		viptype=str(productlist[9])
		if (str(pdt_kind) == '1'):
			arrpdt_kind['kindtxt']='求购'
			arrpdt_kind['kindclass']='buy'
		else:
			arrpdt_kind['kindtxt']='供应'
			arrpdt_kind['kindclass']='sell'
		arrviptype={'vippic':'','vipname':'','vipclass':'','vipsubname':'','vipcheck':'','com_fqr':'','zstNum':'','ldb':''}
		if (viptype == '10051000'):
			arrviptype['vippic']=None
			arrviptype['vipname']='普通会员'
		if (viptype == '10051001'):
			arrviptype['vippic']='http://img.zz91.com/zz91images/recycle.gif'
			arrviptype['vipname']='再生通'
			arrviptype['vipclass']='zst_logo'
		if (viptype == '100510021000'):
			arrviptype['vippic']='http://img.zz91.com/zz91images/pptSilver.gif'
			arrviptype['vipname']='银牌品牌通'
			arrviptype['vipclass']='ypppt_logo'
		if (viptype == '100510021001'):
			arrviptype['vippic']='http://img.zz91.com/zz91images/pptGold.gif'
			arrviptype['vipname']='金牌品牌通'
			arrviptype['vipclass']='jpppt_logo'
		if (viptype == '100510021002'):
			arrviptype['vippic']='http://img.zz91.com/zz91images/pptDiamond.gif'
			arrviptype['vipname']='钻石品牌通'
			arrviptype['vipclass']='zsppt_logo'
		if (viptype == '10051003'):
			arrviptype['vippic']=''
			arrviptype['vipname']='来电宝客户'
			arrviptype['vipclass']='ldb_logo'
		if (viptype == '10051000'):
			arrviptype['vipcheck']=None
		else:
			arrviptype['vipcheck']=1
		#来电宝客户
		company_id=productlist[0]
		if company_id:
			sqll="select id from crm_company_service where company_id=%s and crm_service_code in('1007','1008','1009','1010','1011') and apply_status=1"
			cursor.execute(sqll,[company_id])
			ldbresult=cursor.fetchone()
			if ldbresult:
				sqlg="select front_tel from phone where company_id="+str(company_id)+" and expire_flag=0"
				cursor.execute(sqlg)
				phoneresult=cursor.fetchone()
				if phoneresult:
					arrviptype['ldb']={'ldbphone':phoneresult[0]}
				else:
					arrviptype['ldb']=None
			else:
				arrviptype['ldb']=None
		arrviptype['vipsubname'] = productlist[7]
		arrviptype['com_fqr']=''
		com_province=productlist[10]
		if (com_province==None):
			com_province=''
		pdt_images=""
		area_code=productlist[21]
		#地区信息
		if (area_code):
			sqld="select label from category where code='"+str(area_code[:-4])+"'"
			cursor.execute(sqld)
			arealabel = cursor.fetchone()
			if arealabel:
				if arealabel[0]:
					com_province=arealabel[0]+' '+com_province
					
		arrcompinfo=None
		bindweixin=None
		sqld="select qq,account from company_account where company_id=%s"
		cursor.execute(sqld,[productlist[0]])
		compqq = cursor.fetchone()
		if compqq:
			qq=compqq[0]
			if qq:
				qq=qq.strip()
			if (qq==""):
				qq=None
			if (qq):
				arrcompinfo={'qq':qq}
			account=compqq[1]
			bindweixin=isbindweixin(account)
		#价格范围判断
		allprice=""
		min_price=productlist[11]
		if (min_price==None):
			min_price=''
		else:
			min_price=str(min_price)
			if (min_price!='0.0'):
				allprice=allprice+min_price
		max_price=productlist[12]
		if (max_price==None):
			max_price=''
		else:
			max_price=str(max_price)
			if (max_price!='0.0' and max_price!=min_price):
				if not min_price:
					allprice=allprice+max_price
				else:
					allprice=allprice+'-'+max_price
		price_unit=productlist[13]
		#
		if (price_unit==None):
			price_unit=''
		else:
			if (allprice!=''):
				allprice=allprice+price_unit
				
		total_quantity=productlist[14]
		quantity_unit=productlist[17]
		if (quantity_unit==None):
			quantity_unit=''
		if (total_quantity=='' or total_quantity==' ' or total_quantity==None):
			total_quantity=None
		else:
			total_quantity=total_quantity+quantity_unit

		procatetype=productlist[18]
		if (procatetype!=None):
			procatetype=procatetype.replace('|',' ')
			procatetype=procatetype.replace('\\',' ')
			procatetype=procatetype.replace('/',' ')
			procatetype=procatetype.replace('(',' ')
			procatetype=procatetype.replace(')',' ')

		
		
		#----
		sql1="select pic_address from products_pic where product_id="+str(productlist[2])+" and check_status=1 order by is_default desc,id desc"
		cursor.execute(sql1)
		productspic = cursor.fetchone()
		if productspic:
			pdt_images=productspic[0]
		else:
			pdt_images=""
		if (pdt_images == '' or pdt_images == '0'):
			pdt_images='../cn/img/noimage.gif'
		else:
			pdt_images='http://img3.zz91.com/122x93/'+pdt_images+''
		#发起人标志
		zs=None
		cxcompany=None
		if (company_id!=None):
			sql1="select id from crm_company_service where company_id="+str(company_id)+" and crm_service_code='10001001' and apply_status=1 and gmt_end>='"+str(date.today())+"'"
			cursor.execute(sql1)
			fqrflag = cursor.fetchone()
			if fqrflag:
				fqr=1
			else:
				fqr=None
			
			#诚信会员
			sql1="select id from crm_company_service where company_id="+str(company_id)+" and crm_service_code='10001005' and apply_status=1 and gmt_end>='"+str(date.today())+"'"
			cursor.execute(sql1)
			cxflag = cursor.fetchone()
			if cxflag:
				cxcompany=1
			else:
				cxcompany=None

			#终生会员
			sql1="select id from crm_company_service where company_id="+str(company_id)+" and crm_service_code='10001003' and apply_status=1 and gmt_end>='"+str(date.today())+"'"
			cursor.execute(sql1)
			zsflag = cursor.fetchone()
			if zsflag:
				zs=1
			else:
				zs=None
			zst_year=0
			#年限
			sql2="select sum(zst_year) from crm_company_service where company_id="+str(company_id)+" and apply_status=1"
			cursor.execute(sql2)
			zstNumvalue = cursor.fetchone()
			if zstNumvalue:
				zst_year=zstNumvalue[0]
			arrviptype['zstNum']=zst_year
		else:
			fqr=None
		#供求更多属性
		sqlm="select property,content from product_addproperties where pid=%s and is_del='0'"
		cursor.execute(sqlm,[productlist[2]])
		resultmore=cursor.fetchall()
		listmore=[]
		if resultmore:
			for ll in resultmore:
				if (ll[1]!=None):
					contentp=ll[1].strip()
					if (contentp==""):
						contentp=None
				else:
					contentp=None
				list={'property':ll[0],'content':contentp}
				listmore.append(list)
		source=productlist[24]
		listmore=getmoreproperty(listmore,'货源地',source)
		origin=productlist[31]
		listmore=getmoreproperty(listmore,'来源产品',origin)
		specification=productlist[25]
		listmore=getmoreproperty(listmore,'产品规格',specification)
		impurity=productlist[26]
		listmore=getmoreproperty(listmore,'杂质含量',impurity)
		color=productlist[27]
		listmore=getmoreproperty(listmore,'颜色',color)
		useful=productlist[28]
		listmore=getmoreproperty(listmore,'用途',useful)
		appearance=productlist[29]
		listmore=getmoreproperty(listmore,'外观',appearance)
		manufacture=productlist[30]
		listmore=getmoreproperty(listmore,'加工说明',getcategorylabel(manufacture))
		
		#询盘量
		questioncount=None
		if company_id:
			questioncount=getquestioncount(company_id)
		tagslist=[]
		tags=productlist[32]
		if tags:
			tagsarray=tags.split(",")
			for i in tagsarray:
				l={'label':i,'label_hex':getjiami(i)}
				tagslist.append(l)
		yangflag=getyangflag(pdtid)
		#拿样价
		takeprice=''
		if yangflag:
			takeprice=gettakeprice(yangflag)
		
		
		
		pdt_name=productlist[4]
		list1={'com_id':productlist[0],'com_name':productlist[1],'pdt_id':productlist[2],'pdt_kind':arrpdt_kind
		,'pdt_name':productlist[4],'com_province':com_province,'pdt_detail':productlist[5],'pdt_detailfull':productlist[5]
		,'pdt_time_en':productlist[6],'com_subname':productlist[7],'vipflag':arrviptype,'check_status':productlist[22]
		,'pdt_images':pdt_images,'pdt_price':allprice
		,'vippaibian':'','pdt_name1':productlist[4],'wordsrandom':1,'fqr':fqr
		,'cxcompany':cxcompany,'total_quantity':total_quantity,'procatetype':procatetype
		,'zs':zs,'xianhuoid':'','questioncount':questioncount,'tagslist':tagslist
		,'arrcompinfo':arrcompinfo,'listmore':listmore,'bindweixin':bindweixin,'yangflag':yangflag,'takeprice':takeprice}
	else:
		list1=None
		
	#list1=getproid(pdtid)
	if (list1 == None):
		return None
	else:
		pdt_images=list1['pdt_images']
		if (pdt_images=='../cn/img/noimage.gif'):
			list1['pdt_images']='http://img0.zz91.com/front/images/global/noimage.gif'
		pdt_detail=filter_tags(list1['pdt_detail'])
		pdt_detail=pdt_detail.replace('<br>','').replace('&nbsp;',' ')
		docs=[pdt_detail]
		list1['pdt_detail']=subString(pdt_detail,30)+'...'
		"""
		sqlxx="select id from products_spot where product_id=%s"
		cursor.execute(sqlxx,[pdtid])
		result=cursor.fetchone()
		if result:
			list1['xianhuoid']=result[0]
		else:
			list1['xianhuoid']=None
		"""
		pdt_name=list1['pdt_name']
		docs=[pdt_name]
		pdt_name=pdt_name.replace(keywords,'<em>'+keywords+'</em>')
		#for k in keywords:
			#pdt_name=pdt_name.replace(k,'<em>'+k+'</em>')
		list1['pdt_name']=pdt_name	
	return list1

#----是否绑定微信
def isbindweixin(account):
	sql="select id from oauth_access where target_account=%s and open_type='weixin.qq.com'"
	cursor.execute(sql,[account]);
	plist=cursor.fetchone()
	if plist:
		return 1
	else:
		return None

#获得留言数
def getquestioncount(company_id):
	sqlg="select qcount from inquiry_count where company_id=%s"
	cursor.execute(sqlg,company_id)
	phoneresult=cursor.fetchone()
	if phoneresult:
		return phoneresult[0]
	else:
		return None
	
#----判断是否样品
def getyangflag(products_id):
	sql="select a.sample_id from sample_relate_product as a left join sample as b on a.sample_id=b.id where product_id=%s and b.is_del=0"
	cursor.execute(sql,[products_id])
	productlist = cursor.fetchone()
	if productlist:
		return productlist[0]
	
#----获得拿样价
def gettakeprice(sample_id):
	sql='select take_price from sample where id=%s'
	cursor.execute(sql,sample_id)
	result = cursor.fetchone()
	if result:
		return result[0]
def getdaohanglist(keywords,num=10):
	port = settings.SPHINXCONFIG['port']
	cl = SphinxClient()
	cl.SetServer ( settings.SPHINXCONFIG['serverid'], port )
	cl.SetMatchMode ( SPH_MATCH_ANY )
	cl.SetSortMode( SPH_SORT_EXTENDED,"@weight DESC,search_count desc" )
	cl.SetLimits (0,num,num)
	if keywords:
		keywords=keywords.replace(","," | ")
	res = cl.Query ("@(tname) "+keywords,'tagslist')
	listall=[]
	listcount=0
	if res:
		if res.has_key('matches'):
			itemlist=res['matches']
			for match in itemlist:
				attrs=match['attrs']
				id=attrs['tid']
				tname=str(attrs['tags'])
				main_code=attrs['main_code']
				pingyin=attrs['pingyin']
				list={'id':id,'name':tname,'pingyin':pingyin,'main_code':main_code}
				listall.append(list)
	return listall
#微门户关键词
def getcplist(keywords,limitcount):
	port = settings.SPHINXCONFIG['port']
	cl = SphinxClient()
	cl.SetServer ( settings.SPHINXCONFIG['serverid'], port )
	cl.SetMatchMode ( SPH_MATCH_ANY )
	cl.SetSortMode( SPH_SORT_EXTENDED,"@weight DESC,showcount desc" )
	cl.SetLimits (0,limitcount,limitcount)
	if keywords:
		keywords=keywords.replace(","," | ")
	if keywords:
		res = cl.Query ('@(label) '+keywords,'daohangkeywords')
	else:
		res = cl.Query ('','daohangkeywords')
	listall=[]
	if res:
		if res.has_key('matches'):
			tagslist=res['matches']
			listall_news=[]
			for match in tagslist:
				id=match['id']
				attrs=match['attrs']
				label=attrs['plabel']
				pingyin=attrs['ppinyin']
				if pingyin!="":
					list={'label':label,'label_hex':getjiami(label),'pingyin':pingyin}
					listall.append(list)
	if listall==[]:
		res = cl.Query ('','daohangkeywords')
		if res:
			if res.has_key('matches'):
				tagslist=res['matches']
				listall_news=[]
				for match in tagslist:
					id=match['id']
					attrs=match['attrs']
					label=attrs['plabel']
					pingyin=attrs['ppinyin']
					if pingyin!="":
						list={'label':label,'label_hex':getjiami(label),'pingyin':pingyin}
						listall.append(list)
	return listall
#公司对应产业带
def getcompanymarket(company_id):
	sql="select a.name,a.words from market as a left join market_company as b on a.id=b.market_id where b.company_id=%s and b.is_quit=0 and a.is_del=0"
	cursor.execute(sql,[company_id])
	mlist=cursor.fetchone()
	if mlist:
		if len(mlist)>1:
			if mlist[1] and mlist[0]:
				return {'url':'http://y.zz91.com/'+str(mlist[1])+'/','name':str(mlist[0]),'murl':'http://m.zz91.com/ye/ye_detail/'+str(mlist[1])+'.html'}
	return None


#-------以下为原料供求	
#-----获得原料供求列表页	
def getyuanliaolist(kname="",frompageCount="",limitNum="",company_id=""):
	sqlarg=''
	argument=[]
	argument.append(company_id)
	if kname:
		sqlarg+=' and title like %s'
		argument.append('%'+kname+'%')
	
	sql1='select count(0) from  yuanliao where company_id=%s'+sqlarg
	sql='select id,title,category_yuanliao_code,category_main_desc,category_assist_desc,yuanliao_type_code,trade_mark,type,price,min_price,max_price,price_unit,quantity,unit,description from yuanliao where company_id=%s'+sqlarg
	sql=sql+' order by id desc limit '+str(frompageCount)+','+str(limitNum)
	cursor.execute(sql1,argument)
	alist=cursor.fetchone()
	if alist:
		listcount=alist[0]
	cursor.execute(sql,argument)
	resultlist=cursor.fetchall()
	listall=[]
	typetxt=''
	jiagetxt=''
	factory=""
	if resultlist:
		for result in resultlist:
			id=result[0]
			title=result[1]
			category_yuanliao_code=result[2]
			category_main_desc=result[3]
			category_assist_desc=result[4]
			if (category_main_desc=="" or category_main_desc==None):
				factory=category_assist_desc
			else:
				factory=getfactory(category_main_desc)
			yuanliao_type_code=result[5]
			trade_mark=result[6]
			type=result[7]
			typetxt=getyualiaotype(type)
			price=result[8]
			min_price=result[9]
			max_price=result[10]
			if (price=="" or price==None):
				jiagetxt=str(min_price)+'-'+str(max_price)
			else:
				jiagetxt=price
			price_unit=result[11]
			quantity=result[12]
			unit=result[13]
			description=result[14]
			description=filter_tags(description)
			description75=description[0:75]
			#默认图片
			sql1="select pic_address from yuanliao_pic where yuanliao_id=%s and check_status=1 and is_del=0 and is_default=1"
			cursor.execute(sql1,id)
			productspic = cursor.fetchone()
			if productspic:
				defaultimages=productspic[0]
			else:
				defaultimages=""
			if (defaultimages == '' or defaultimages == '0'):
				defaultimages='http://img0.zz91.com/front/images/global/noimage.gif'
			else:
				defaultimages='http://img3.zz91.com/150x150/'+defaultimages+''
			
			list={'id':id,'title':title,'category_yuanliao_code':category_yuanliao_code,'factory':factory,'yuanliao_type_code':yuanliao_type_code,'trade_mark':trade_mark,'typetxt':typetxt,'jiagetxt':jiagetxt,'price_unit':price_unit,'quantity':quantity,'unit':unit,'description':description75,'defaultimages':defaultimages}	
			listall.append(list)
	return {'list':listall,'count':listcount}
#原料产品类型（正牌料，副牌料，协议料。。）
def getyualiaotype(typecode):
	sql='select label from category where code=%s'
	cursor.execute(sql,[typecode])
	result=cursor.fetchone()
	if result:
		return result[0]
	else:
		return ''
	
#原料详细页
#根据原料供求获得公司ID
def getyuanliaoproductscompanyid(id):
	sql="select company_id from yuanliao where id=%s"
	cursor.execute(sql,[id])
	result=cursor.fetchone()
	if result:
		return result[0]
#获得所在地	
def getlocation(code):
	sql='select label from category where code=%s'
	cursor.execute(sql,[code])
	result=cursor.fetchone()
	if result:
		return result[0]
	else:
		return ''
#获得厂家产地
def getfactory(code):
	sql='select label from category_yuanliao where code=%s'
	cursor.execute(sql,[code])
	result=cursor.fetchone()
	if result:
		return result[0]
	else:
		return ''
#原料属性
def getlevel(levelcode=''):
	sql='select label from category where code=%s'
	cursor.execute(sql,[levelcode])
	result=cursor.fetchone()
	if result:
		return result[0]
	else:
		return ''

#原料特性的字符串处理	
def deal_texing(levelcode=''):
	level_txt=''
	if ',' in levelcode:
		level_list=levelcode.split(',')
		for l in level_list:
			level_txt=getlevel(l)+','+level_txt
		level_txt=level_txt[:-1]
	else:
		level_txt=getlevel(levelcode)
	return level_txt

#获得原料供求详细信息
def getyuanliaoproductdetail(id):
#	 listdir=cache.get("seoweb_yuanliaoprodetail"+str(id))
#	 listdir=None
#	 if not listdir:
	sql="select company_id,title,tags,category_yuanliao_code,category_main_desc,category_assist_desc,yuanliao_type_code,price,min_price,max_price"
	sql=sql+",price_unit,quantity,unit,provide_status,trade_mark,type,location,send_time,refresh_time,description"
	sql=sql+",process_level,chara_level,useful_level,color,density,hardness,tensile,bending from yuanliao where id=%s"
	cursor.execute(sql,str(id))
	plist=cursor.fetchone()
	factory=""
	if plist:
		company_id=plist[0]  
		#标题
		title=plist[1]				
		#相关标签
		tags=plist[2]
		tagslist=None
		if tags:
			#tagslist=getdaohanglist(tags,num=15)
			tagslist=getcplist(tags,12)
		
		category_yuanliao_code=plist[3]#没用
		#厂家产地
		category_main_desc=plist[4]
# 		fectory=getfactory(category_main_desc)
		category_assist_desc=plist[5]#没用
		if (category_main_desc=="" or category_main_desc==None):
			factory=category_assist_desc
		else:
			factory=getfactory(category_main_desc)
		#供应还是求购
		yuanliao_type_code_txt=''
		yuanliao_type_code=plist[6]
		if yuanliao_type_code=="10331000":
			yuanliao_type_code_txt='供应'
		if yuanliao_type_code=="10331001":
			yuanliao_type_code_txt='求购'
		#价格或价格区间和单位
		pricetxt=''
		price=plist[7]
		min_price=plist[8]
		max_price=plist[9]
		price_unit=plist[10]
		if (price=="" or price==None):
			pricetxt=str(min_price)+'-'+str(max_price)
		else:
			pricetxt=price
		#质量与单位
		quantity=plist[11]
		unit=plist[12]
		#供货情况：长期供应or不定期供应
		provide_status=plist[13]
		provide_status_text=''
		if provide_status==0:
			provide_status_text='长期'
		if provide_status==1:
			provide_status_text='不定期'
		#牌号
		trade_mark=plist[14]
		#原料产品类型（正牌料，副牌料，协议料。。）
		typelei=plist[15]
		typetxt=getyualiaotype(typelei)
		#货物所在地
		location=plist[16]
		locationtxt=''
		locationtxt=getlocation(location)#####
		#几天内发货
		send_time=plist[17]
		#发布日期
		refresh_time=formattime(plist[18],1)
		#详细信息
		description=plist[19]
		#---以下为特性属性可以为空
		process_level=plist[20]
		chara_leval=plist[21]
		useful_leval=plist[22]
		process_txt=deal_texing(process_level)
		chara_txt=deal_texing(chara_leval)
		useful_txt=deal_texing(useful_leval)
		color=plist[23]
		density=plist[24]
		hardness=plist[25]
		tensile=plist[26]
		bending=plist[27]
		#默认图片
		sql1="select pic_address from yuanliao_pic where yuanliao_id=%s and check_status=1 and is_del=0 order by is_default desc"
		cursor.execute(sql1,id)
		productspic = cursor.fetchone()
		if productspic:
			defaultimages=productspic[0]
		else:
			defaultimages=""
		if (defaultimages == '' or defaultimages == '0'):
			defaultimages='http://img0.zz91.com/front/images/global/noimage.gif'
		else:
			defaultimages='http://img3.zz91.com/300x300/'+defaultimages+''
		#图片列表
		sql2="select pic_address from yuanliao_pic where yuanliao_id=%s and check_status=1 and is_del=0"
		cursor.execute(sql2,id)
		productspic = cursor.fetchall()
		piclist=[]
		if productspic:
			for p in productspic:
				pimages=p[0]
				if (pimages == '' or pimages == '0' or pimages==None):
					pdt_images='../cn/img/noimage.gif'
					pdt_images_big='../cn/img/noimage.gif'
				else:
					pdt_images="http://img3.zz91.com/135x135/"+pimages+""
					pdt_images_big="http://img3.zz91.com/300x300/"+pimages+""
				picurl={'images':pdt_images,'images_big':pdt_images_big}
				piclist.append(picurl)
		listdir={'pdtid':id,'company_id':company_id,'title':title,'tags':tags,'tagslist':tagslist,'factory':factory,'yuanliao_type_code_txt':yuanliao_type_code_txt,'pricetxt':pricetxt,'price_unit':price_unit,'quantity':quantity,'unit':unit,'provide_status_text':provide_status_text,'trade_mark':trade_mark,'typetxt':typetxt,'locationtxt':locationtxt,'send_time':send_time,'refresh_time':refresh_time,'description':description,'piclist':piclist,'defaultimages':defaultimages,'process_level_txt':process_txt,'chara_level_txt':chara_txt,'useful_leval_txt':useful_txt,'color':color,'density':density,'hardness':hardness,'tensile':tensile,'bending':bending}
	return listdir
#底部其他供求
def getyuanliaoproductslist(frompageCount="",limitNum="",company_id=""):
	sql="select id,title,yuanliao_type_code from yuanliao where company_id=%s and is_del=0  and is_pause=0 and check_status=1 limit %s,%s"
	cursor.execute(sql,[company_id,frompageCount,limitNum])
	resultlist=cursor.fetchall()
	listall=[]
	if resultlist:
		for result in resultlist:
			id=result[0]
			title=result[1]
			#求购还是供应
			yuanliao_type_code=result[2]
			if yuanliao_type_code=="10331000":
				yuanliao_type_code_txt='供应'
			if yuanliao_type_code=="10331001":
				yuanliao_type_code_txt='求购'
			#获得默认图片
			sql1='select pic_address from yuanliao_pic where yuanliao_id=%s and check_status=1 and is_del=0 and is_default=1'
			cursor.execute(sql1,id)
			buttom_pic=cursor.fetchone()
			if buttom_pic:
				buttomdefaultimages=buttom_pic[0]
			else:
				buttomdefaultimages=""
			if (buttomdefaultimages == '' or buttomdefaultimages == '0'):
				buttomdefaultimages='http://img0.zz91.com/front/images/global/noimage.gif'
			else:
				buttomdefaultimages='http://img3.zz91.com/150x150/'+buttomdefaultimages+''
			
			list={'id':id,'title':title,'yuanliao_type_code_txt':yuanliao_type_code_txt,'buttom_default_pic':buttomdefaultimages}
			listall.append(list)
	return listall
#获得明感字符
def getmingganword(s):
	sql="select id,updateflag,content from data_feifacontent where id=1"
	cursor.execute(sql)
	result=cursor.fetchone()
	if not result:
		r=requests.get("http://pyapp.zz91.com/feifa.html")
		content=r.text
		sql="insert into data_feifacontent(id,content,updateflag) values(%s,%s,%s)"
		cursor.execute(sql,[1,content,0])
		conn.commit()
	else:
		updateflag=result[1]
		if str(updateflag)=="1":
			r=requests.get("http://pyapp.zz91.com/feifa.html?a=0")
			content=r.text
			sql="update data_feifacontent set content=%s where id=1"
			cursor.execute(sql,[content])
			conn.commit()
		else:
			content=result[2]
	lines=eval(content)
	list=[]
	if lines:
		for line in lines:
			line=line['k']
			line=line.strip('\n').strip()
			if line in s:
				return line
				break
			list.append(line)
	if s in list:
		return 2
	if "激情" in s:
		return 2
	if "乱伦" in s:
		return 2
	return None



