def getcompinfo(pdtid,cursort,keywords):
	sql="SELECT c.id AS com_id, c.name AS com_name, p.id AS pdt_id, RIGHT( p.products_type_code, 1 ) AS pdt_kind, p.title AS pdt_name, p.details AS pdt_detail, DATE_FORMAT(p.refresh_time,'%Y/%m/%d'), c.domain_zz91 AS com_subname, p.price AS pdt_price,c.membership_code,e.label as city FROM products AS p LEFT OUTER JOIN company AS c ON p.company_id = c.id LEFT OUTER JOIN category as e ON c.area_code=e.code where p.id="+str(pdtid)+""
	cursort.execute(sql)
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
			arrviptype['vippic']='http://img.zz91.com/zz91images/recycle.gif'
			arrviptype['vipname']='再生通'
		if (viptype == '100510021000'):
			arrviptype['vippic']='http://img.zz91.com/zz91images/pptSilver.gif'
			arrviptype['vipname']='银牌品牌通'
		if (viptype == '100510021001'):
			arrviptype['vippic']='http://img.zz91.com/zz91images/pptGold.gif'
			arrviptype['vipname']='金牌品牌通'
		if (viptype == '100510021002'):
			arrviptype['vippic']='http://img.zz91.com/zz91images/pptDiamond.gif'
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
		sql1="select pic_address from products_pic where product_id="+str(productlist[2])+""
		cursort.execute(sql1)
		productspic = cursort.fetchone()
		if productspic:
			pdt_images=productspic[0]
		else:
			pdt_images=""
		if (pdt_images == '' or pdt_images == '0'):
			pdt_images='../cn/img/noimage.gif'
		else:
			pdt_images='http://image01.zz91.com/images.php?picurl=http://img1.zz91.com/'+pdt_images+'&width=220&height=300'
		list1={'com_id':productlist[0],'com_name':productlist[1],'pdt_id':productlist[2],'pdt_kind':arrpdt_kind
		,'pdt_name':productlist[4],'com_province':com_province,'pdt_detail':productlist[5]
		,'pdt_time_en':productlist[6],'com_subname':productlist[7],'vipflag':arrviptype
		,'pdt_images':pdt_images,'pdt_price':productlist[8]
		,'vippaibian':'','pdt_name1':productlist[4],'wordsrandom':1}
	else:
		list1=None
		
	#list1=getproid(pdtid)
	if (list1 == None):
		return None
	else:
		pdt_images=list1['pdt_images']
		if (pdt_images=='../cn/img/noimage.gif'):
			list1['pdt_images']='http://img0.zz91.com/front/images/global/noimage.gif'
		pdt_detail=list1['pdt_detail']
		pdt_detail=pdt_detail.replace('<br>','').replace('&nbsp;',' ')
		docs=[pdt_detail]
		list1['pdt_detail']=subString(pdt_detail,50)+'...'
		
		pdt_name=list1['pdt_name']
		docs=[pdt_name]
		#pdt_name=pdt_name.replace(keywords,'<font color=#F30/>'+keywords+'</font>')
		list1['pdt_name']=pdt_name		
	return list1
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