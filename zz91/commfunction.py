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
		sql1="select pic_address from products_pic where product_id="+str(productlist[2])+" and check_status=1"
		cursort.execute(sql1)
		productspic = cursort.fetchone()
		if productspic:
			pdt_images=productspic[0]
		else:
			pdt_images=""
		if (pdt_images == '' or pdt_images == '0'):
			pdt_images='../cn/img/noimage.gif'
		else:
			pdt_images='http://images.zz91.com/images.php?picurl=http://img1.zz91.com/'+pdt_images+'&width=118&height=85'
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
		pdt_detail=stripTags(list1['pdt_detail'])
		pdt_detail=pdt_detail.replace('<br>','').replace('&nbsp;',' ')
		docs=[pdt_detail]
		list1['pdt_detail']=subString(pdt_detail,150)+'...'
		
		pdt_name=list1['pdt_name']
		#pdt_name=getlightkey(keywords,pdt_name)
		docs=[pdt_name]
		if (keywords!="" and keywords!=None):
			pdt_name=pdt_name.replace(keywords,"<font color=red>"+keywords+"</font>")
		#pdt_name=pdt_name.replace(keywords,'<font color=#F30/>'+keywords+'</font>')
		list1['pdt_name']=pdt_name		
	return list1
##过滤HTML中的标签
def stripTags(s):
	intag = [False]
	def chk(c):
		if intag[0]:
			intag[0] = (c != '>')
			return False
		elif c == '<':
			intag[0] = True
			return False
		return True
	return ''.join(c for c in s if chk(c))
def getnum_str(numstr,nowcode,num):
	if (str(numstr)=='None' or str(numstr)==''):
		return num
	else:
		nstr=numstr.split(',')
		for i in nstr:
			ii=i.split(':')
			if (len(ii)>=1):
				if (str(ii[0])==nowcode):
					num= int(ii[1])
	return num
#关键字加亮
def getlightkey(keywords,content):
	content=stripTags(content)
	p=""
	for a in keywords:
		#if (content.find(a)>0):
		#p=p+a.decode('utf-8')+content
		content=content.replace(str(a),"<font color=red>"+str(a)+"</font>")
	return content
#判断是否为HEX码
def gethextype(keywords):
	zwtype=0
	zwflag=0
	strvalue="abcdef0123456789"
	for a in keywords:
		if (a >= u'\u4e00' and a<=u'\u9fa5'):
			zwflag=zwflag+1
	if zwflag>0:
		zwtype=1
	zwflag=0
	if zwtype==0:
		for a in keywords:
			if (strvalue.find(a)==-1):
				zwflag=zwflag+1
		if zwflag>0:
			zwtype=1
	if zwtype==1:
		return False
	else:
		return True
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
def _key_to_file(key):
	path = str(int(int(key) / 1000))
	return '/usr/data/offerlist/'+path+'/'
def getproid(id):
	fname = _key_to_file(id)
	if not (os.path.exists(fname+str(id)+'.pkl')):
		return None
	else:
		pkl_file = open(fname+str(id)+'.pkl','rb')
		return pickle.load(pkl_file)
		pkl_file.close()

#加密
def getjiami(strword):
	return strword.encode('utf8','ignore').encode("hex")
def getjiemi(strword):
	return strword.decode("hex").decode('utf8','ignore')
def gettagsName(id):
	sql="select tags from tags where old_id=%s"
	cursor_tags.execute(sql,id)
	arrtags=cursor_tags.fetchone()
	if (arrtags):
		return arrtags[0].encode('utf-8')
	else:
		sql="select tags from tags where id=%s"
		cursor_tags.execute(sql,id)
		arrtags=cursor_tags.fetchone()
		if (arrtags):
			return arrtags[0].encode('utf-8')
#记录点击次数
def tagschickNum(keywords):
	sql="update tags set search_count=search_count+1 where tags=%s"
	cursor_tags.execute(sql,[keywords])
	

#广告
def getadlist(pkind,keywords):
	keystr="|1:"+keywords+"|"
	sql="select ad_content,ad_target_url,id from ad where position_id=%s and gmt_plan_end>='"+str(date.today()+timedelta(days=1))+"' and search_exact='"+str(keystr)+"' and review_status='Y' and online_status='Y' order by gmt_start asc,sequence asc"
	cursor_ads.execute(sql,pkind)
	alist = cursor_ads.fetchone()
	if alist:
		list={'url':'http://gg.zz91.com/hit?a='+str(alist[2]),'picaddress':alist[0]}
		return list
def newtagslist(kname,num):
	#-------------最新标签
	port = settings.SPHINXCONFIG['port']
	cl = SphinxClient()
	cl.SetServer ( settings.SPHINXCONFIG['serverid'], port )
	cl.SetMatchMode ( SPH_MATCH_BOOLEAN )
	cl.SetSortMode( SPH_SORT_EXTENDED,"search_count desc" )
	cl.SetLimits (0,num)
	if (kname):
		res = cl.Query ('@tname '+kname,'tagslist')
	else:
		res = cl.Query ('','tagslist')
	if res:
		if res.has_key('matches'):
			tagslist=res['matches']
			listall_tags=[]
			ii=1
			for match in tagslist:
				id=match['id']
				attrs=match['attrs']
				tags=attrs['tags']
				tags=tags.replace("/","")
				list1={'kname':tags,'id':id,'classid':ii,'kname_hex':tags.encode("hex")}
				listall_tags.append(list1)
				ii+=1
				if (ii>2):
					ii=1
			return listall_tags
def getpricelist(kname="",num=""):
	#------最新报价信息
	port = settings.SPHINXCONFIG['port']
	cl = SphinxClient()
	cl.SetServer ( settings.SPHINXCONFIG['serverid'], port )
	cl.SetMatchMode ( SPH_MATCH_BOOLEAN )
	cl.SetSortMode( SPH_SORT_EXTENDED,"gmt_order desc" )
	if num:
		limitnum=num
	else:
		limitnum=30
	cl.SetLimits (0,limitnum)
	if (kname==""):
		res = cl.Query ('@(title,tags) '+kname+'','price')
	else:
		res = cl.Query ('','price')
	if res:
		if res.has_key('matches'):
			tagslist=res['matches']
			listall_baojia=[]
			for match in tagslist:
				td_id=match['id']
				attrs=match['attrs']
				title=attrs['ptitle']
				gmt_time=attrs['gmt_time']
				list1={'td_title':title,'td_id':td_id,'td_time':gmt_time}
				listall_baojia.append(list1)
				havelist=listall_baojia
		listcount_baojia=res['total_found']
		if (listcount_baojia==0):
			havelist=None
			res = cl.Query ('','price')
			if res:
				if res.has_key('matches'):
					tagslist=res['matches']
					listall_baojia=[]
					for match in tagslist:
						td_id=match['id']
						attrs=match['attrs']
						title=attrs['ptitle']
						gmt_time=attrs['gmt_time']
						list1={'td_title':title,'td_id':td_id,'td_time':gmt_time}
						listall_baojia.append(list1)
				listcount_baojia=0
		return {'list':listall_baojia,'count':listcount_baojia,'havelist':havelist}
#企业报价
def getpricelist_company(kname="",num=""):
	#------最新报价信息
	port = settings.SPHINXCONFIG['port']
	cl = SphinxClient()
	cl.SetServer ( settings.SPHINXCONFIG['serverid'], port )
	cl.SetMatchMode ( SPH_MATCH_BOOLEAN )
	cl.SetSortMode( SPH_SORT_EXTENDED,"post_time desc" )
	if num:
		limitnum=num
	else:
		limitnum=30
	cl.SetLimits (0,limitnum)
	res = cl.Query ('@(title,label1,label2,label3,area1,area2,area3) '+kname+'','company_price')
	if res:
		if res.has_key('matches'):
			tagslist=res['matches']
			listall_baojia=[]
			for match in tagslist:
				td_id=match['id']
				attrs=match['attrs']
				title=attrs['ptitle']
				gmt_time=attrs['ppost_time']
				price_unit=attrs['price_unit']
				min_price=attrs['min_price']
				max_price=attrs['max_price']
				#if (price=="" or price=="none"):
				price=min_price+"-"+max_price+price_unit
				#td_time=gmt_time.strftime('%Y-%m-%d')
				list1={'td_title':title,'td_id':td_id,'td_time':gmt_time,'price':price,'url':'http://price.zz91.com/companyprice/priceDetails'+str(td_id)+'.htm'}
				listall_baojia.append(list1)
		listcount_baojia=res['total_found']
		return {'list':listall_baojia,'count':listcount_baojia}
def getbbslist(kname="",num=""):
	#最新互助信息
	port = settings.SPHINXCONFIG['port']
	cl = SphinxClient()
	cl.SetServer ( settings.SPHINXCONFIG['serverid'], port )
	cl.SetMatchMode ( SPH_MATCH_BOOLEAN )
	cl.SetSortMode( SPH_SORT_EXTENDED,"post_time desc" )
	if num:
		limitnum=num
	else:
		limitnum=30
	cl.SetLimits (0,limitnum)
	res = cl.Query ('@(title,tags) '+kname,'huzhu')
	if res:
		if res.has_key('matches'):
			tagslist=res['matches']
			listall_news=[]
			for match in tagslist:
				td_id=match['id']
				attrs=match['attrs']
				title=attrs['ptitle']
				gmt_time=attrs['ppost_time']
				list1={'td_title':subString(title,60),'td_title_f':title,'td_id':td_id,'td_time':gmt_time}
				listall_news.append(list1)
				havelist=listall_news
		listcount_news=res['total_found']
		if (listcount_news==0):
			res = cl.Query ('','huzhu')
			havelist=None
			if res:
				if res.has_key('matches'):
					tagslist=res['matches']
					listall_news=[]
					for match in tagslist:
						td_id=match['id']
						attrs=match['attrs']
						title=attrs['ptitle']
						gmt_time=attrs['ppost_time']
						list1={'td_title':subString(title,60),'td_title_f':title,'td_id':td_id,'td_time':gmt_time}
						listall_news.append(list1)
				listcount_news=0
		return {'list':listall_news,'count':listcount_news,'havelist':havelist}

def getofferlist(kname="",ckind="",num=""):
	#-----------供求信息
	port = settings.SPHINXCONFIG['port']
	cl = SphinxClient()
	cl.SetServer ( settings.SPHINXCONFIG['serverid'], port )
	cl.SetMatchMode ( SPH_MATCH_BOOLEAN )
	cl.SetFilter('check_status',[1])
	if ckind:
		cl.SetFilter('pdt_kind',[int(ckind)])
	cl.SetSortMode( SPH_SORT_EXTENDED,"company_id desc,refresh_time desc" )
	if num:
		limitnum=num
	else:
		limitnum=50
	cl.SetLimits (0,1000,1000)
	res = cl.Query ('@(title,label0,label1,label2,label3,label4,city,province,tags) '+kname,'offersearch_new,offersearch_new_vip')
	if res:
		if res.has_key('matches'):
			tagslist=res['matches']
			listall=[]
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
				
				#list1=getcompinfo(pdtid,cursor_my,kname)
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
		#列出供求信息列表
		listall=[]
		for match in listallvip[0:limitnum]:
			list1=getcompinfo(match[0],cursor_my,kname)
			listall.append(list1)
		listcount=res['total_found']
		return {'list':listall,'count':listcount}
	
def newcustmerprice(kname):
	#-------------最新产品企业报价
	port = settings.SPHINXCONFIG['port']
	cl = SphinxClient()
	cl.SetServer ( settings.SPHINXCONFIG['serverid'], port )
	cl.SetMatchMode ( SPH_MATCH_BOOLEAN )
	cl.SetSortMode( SPH_SORT_EXTENDED,"post_time desc" )
	cl.SetLimits (0,20,20)
	res = cl.Query ('@title '+kname,'company_price')
	if res:
		if res.has_key('matches'):
			tagslist=res['matches']
			listall_customerPrice=[]
			for match in tagslist:
				id=match['id']
				attrs=match['attrs']
				title=attrs['ptitle']
				title=subString(title,12)
				gmt_time=attrs['ppost_time']
				price=subString(attrs['price'],12)
				list1={'pdt_name':title,'id':id,'pdt_price':price}
				listall_customerPrice.append(list1)
			return listall_customerPrice
			
#类别列表
def getindexcategorylist(code,showflag):
	l=len(code)
	sql="select label,code from category_products where code like '"+str(code)+"____' order by sort asc"
	cursor.execute(sql)
	listall_cate=[]
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
		list={'label':a[0],'label_hex':getjiami(a[0]),'code':a[1],'catelist':listall_cate1}
		listall_cate.append(list)
		
	
	
	return listall_cate
#---标签库首页有图片的最新供求列表
def getindexofferlist_pic(kname,pdt_type,limitcount):
	port = settings.SPHINXCONFIG['port']
	cl = SphinxClient()
	cl.SetServer ( settings.SPHINXCONFIG['serverid'], port )
	cl.SetMatchMode ( SPH_MATCH_BOOLEAN )
	cl.SetSortMode( SPH_SORT_EXTENDED," company_id desc,refresh_time desc" )
	cl.SetLimits (0,limitcount,limitcount)
	if (pdt_type!=None and pdt_type!=""):
		cl.SetFilter('pdt_kind',[int(pdt_type)])
	cl.SetFilterRange('havepic',1,100)
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
				pdt_kind=attrs['pdt_kind']
				kindtxt=''
				if (pdt_kind=='1'):
					kindtxt="供应"
				if (pdt_kind=='2'):
					kindtxt="求购"
				title=subString(attrs['ptitle'],40)
				sql1="select pic_address from products_pic where product_id=%s and check_status=1 order by is_default desc,id desc"
				cursor.execute(sql1,[pid])
				productspic = cursor.fetchone()
				if productspic:
					pdt_images=productspic[0]
				else:
					pdt_images=""
				if (pdt_images == '' or pdt_images == '0'):
					pdt_images='http://img0.zz91.com/front/images/global/noimage.gif'
				else:
					pdt_images='http://images.zz91.com/images.php?picurl=http://img1.zz91.com/'+pdt_images+'&width=100&height=100'
				list={'id':pid,'title':title,'gmt_time':pdt_date,'kindtxt':kindtxt,'fulltitle':attrs['ptitle'],'pdt_images':pdt_images}
				listall_offerlist.append(list)
			return listall_offerlist
def getcompanyindexcomplist(kname,num):
	#-------------最新加入企业
	port = settings.SPHINXCONFIG['port']
	cl = SphinxClient()
	cl.SetServer ( settings.SPHINXCONFIG['serverid'], port )
	cl.SetMatchMode ( SPH_MATCH_BOOLEAN )
	cl.SetSortMode( SPH_SORT_EXTENDED," gmt_start desc" )
	cl.SetLimits (0,num,num)
	cl.SetFilter('apply_status',[1])

	nowdate=date.today()-timedelta(days=360)
	nextday=date.today()+timedelta(days=1)
	formatnowdate=time.mktime(nowdate.timetuple())
	formatnextday=time.mktime(nextday.timetuple())
	cl.SetFilterRange('gmt_start',int(formatnowdate),int(formatnextday))
	
	if (kname):
		res = cl.Query ('@(name,business,address,sale_details,buy_details,tags,area_name,area_province) '+kname,'company')
	else:
		res = cl.Query ('','company')
	if res:
		if res.has_key('matches'):
			itemlist=res['matches']
			listall_company=[]
			for match in itemlist:
				id=match['id']
				attrs=match['attrs']
				comname=attrs['compname']
				business=attrs['pbusiness']
				area_province=attrs['parea_province']
				domain_zz91=attrs['domain_zz91']
				list={'id':id,'comname':comname,'business':business,'area_province':area_province,'domain_zz91':domain_zz91}
				listall_company.append(list)
			return listall_company
def englishlist():
	pinyin=['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']
	return pinyin	
#-------------------------
def getdaohanglist(sid):
	sql="select id,label,pingyin,templates,ord,sid from daohang where sid="+str(sid)+" order by ord asc"
	cursor.execute(sql)
	listall=[]
	complist=cursor.fetchall()
	for a in complist:
		list={'id':a[0],'sid':a[5],'label':a[1],'pingyin':a[2],'templates':a[3],'ord':a[4]}
		listall.append(list)
	return listall
def getdaohanglist_child(sid):
	sql="select id,label,pingyin,templates,ord,sid,keywords2 from daohang where sid="+str(sid)+" order by ord asc"
	cursor.execute(sql)
	listall=[]
	complist=cursor.fetchall()
	for a in complist:
		childlist=getdaohanglist(a[0])
		keywords2=a[6]
		priceInfo=getpricelist_daohang(kname=keywords2,limitcount=10,titlelen=100)
		list={'id':a[0],'sid':a[5],'label':a[1],'pingyin':a[2],'templates':a[3],'ord':a[4],'childlist':childlist,'priceInfo':priceInfo,'keywords2':keywords2}
		listall.append(list)
	return listall
def gettagslist(kname,num):
	#-------------标签列表
	port = settings.SPHINXCONFIG['port']
	cl = SphinxClient()
	cl.SetServer ( settings.SPHINXCONFIG['serverid'], port )
	cl.SetMatchMode ( SPH_MATCH_BOOLEAN )
	cl.SetSortMode( SPH_SORT_EXTENDED," search_count desc" )
	cl.SetLimits (0,num)
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
				list={'id':id,'name':tname,'n':i}
				listall_tagslist.append(list)
				i+=1
				if (i>3):
					i=1
			return listall_tagslist
#标签总数
def gettagsallcout():
	port = settings.SPHINXCONFIG['port']
	cl = SphinxClient()
	cl.SetServer ( settings.SPHINXCONFIG['serverid'], port )
	cl.SetLimits (0,1)
	res = cl.Query ('','tagslist')
	if res:
		listcount=res['total_found']
	return listcount
#--获取资讯url
def get_newstype(id,cursor_news):
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
			list={'typename':result2[0],'url':result2[1],'typeid':typeid,'typeid2':typeid2,'url2':''}
			if typeid2!='0':
				sql3='select keywords from dede_arctype where id=%s'
				cursor_news.execute(sql3,[typeid2])
				result3=cursor_news.fetchone()
				if result3:
					list['url2']=result3[0]
			return list
#----资讯列表
def getnewslist(keywords="",frompageCount="",limitNum="",typeid="",allnum="",typeid2="",contentflag=""):
	cursor_news = conn_news.cursor()
	port = settings.SPHINXCONFIG['port']
	cl = SphinxClient()
	cl.SetServer ( settings.SPHINXCONFIG['serverid'], port )
	cl.SetMatchMode ( SPH_MATCH_EXTENDED )
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
		res = cl.Query ('@(title,description) '+keywords,'news')
	else:
		res = cl.Query ('','news')
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
				title=attrs['ptitle']
				title10=title.decode('utf-8')[:13]
				pubdate=attrs['pubdate']
				pubdate2=timestamp_datetime2(pubdate)
#				havepic=havepicflag(content)
				#littlecontent=subString(filter_tags(content),60)
				list1={'title':title,'title10':title10,'id':id,'pubdate':pubdate2,'newsurl':newsurl,'weburl':weburl}
				listall_news.append(list1)
			listcount_news=res['total_found']
	return {'list':listall_news,'count':listcount_news}

def timestamp_datetime2(value):
    format = '%Y-%m-%d'
    value = time.localtime(value)
    dt = time.strftime(format, value)
    return dt


#----供求地区详情
def getproducts_area(company_id):
	sql='select label from category where code=(select area_code from company where id=%s)'
	cursor.execute(sql,[company_id])
	result1=cursor.fetchone()
	if result1:
		list={'source':result1[0]}
		return list

#----供应详情2条
def getproducts_detail(product_id):
	sql='select quantity,quantity_unit,price,price_unit,refresh_time from products where id=%s'
	cursor.execute(sql,[product_id])
	result=cursor.fetchone()
	if result:
		price=result[2]
		if price=="" or price==" ":
			price=None
		if price=="0.0":
			price=None
		list={'quantity':result[0],'quantity_unit':result[1],'price':price,'price_unit':result[3],'refresh_time':result[4]}
		return list

def getpic_address(product_id):
	sql='select pic_address from products_pic where product_id=%s and check_status=1 order by is_default desc,id desc'
	cursor.execute(sql,[product_id])
	ldbresult=cursor.fetchone()
	if ldbresult:
		return ldbresult[0]

def getdaohangtype(pingyin):
	sql='select sid from daohang where pingyin=%s'
	cursor.execute(sql,[pingyin])
	ldbresult=cursor.fetchone()
	if ldbresult:
		return ldbresult[0]

def offerlist(kname="",pdt_type="",limitcount="",havepic="",fromlimit=""):
	#-------------供求列表
	port = settings.SPHINXCONFIG['port']
	cl = SphinxClient()
	cl.SetServer ( settings.SPHINXCONFIG['serverid'], port )
	cl.SetMatchMode ( SPH_MATCH_BOOLEAN )
	cl.SetSortMode( SPH_SORT_EXTENDED," refresh_time desc" )
	if (fromlimit):
		cl.SetLimits (fromlimit,limitcount+fromlimit,limitcount+fromlimit)
	else:
		cl.SetLimits (0,limitcount,limitcount)
	if (pdt_type!="" and pdt_type!=None):
		cl.SetFilter('pdt_kind',[int(str(pdt_type))])
	if (havepic):
		cl.SetFilterRange('havepic',1,100)
	if (kname=='' or kname==None):
		res = cl.Query ('','offersearch_new_vip')
	else:
		res = cl.Query ('@(title,label0,label1,label2,label3,label4,city,province,tags) '+kname,'offersearch_new,offersearch_new_vip')
	if res:
		if res.has_key('matches'):
			itemlist=res['matches']
			listall_offerlist=[]
			numb=0
			arg=''
			for match in itemlist:
				numb=numb+1
				if numb==1:
					arg='l'
				if numb==2:
					arg='r'
				pid=match['id']
				attrs=match['attrs']
				company_id=attrs['company_id']
				parea=getproducts_area(company_id)
				
				
				pdt_date=timestamp_datetime2(attrs['refresh_time'])
				short_time=pdt_date[5:]
				
				products_detail=getproducts_detail(pid)
				productspic=getpic_address(pid)
				if productspic:
					pdt_images=productspic
				else:
					pdt_images=""
				if (pdt_images == '' or pdt_images == '0'):
					pdt_images='http://img0.zz91.com/front/images/global/noimage.gif'
				else:
					pdt_images='http://images.zz91.com/images.php?picurl=http://img1.zz91.com/'+pdt_images+'&width=100&height=100'
				pic_address=pdt_images
				#pdt_date=pdt_date.strftime( '%-Y-%-m-%-d-%-H-%-M')
#				sql="select refresh_time from products where id="+str(pid)+""
#				cursor.execute(sql)
#				productlist = cursor.fetchone()
#				if productlist:
#					pdt_date=productlist[0].strftime( '%-Y-%-m-%-d')
				"""
				pfromdate=date.today()
				pfromdate_int=int(time.mktime(pfromdate.timetuple()))
				pdt_date=pfromdate_int-pdt_date
				
				pdtnum=date.today()-timedelta(seconds=3)
				
				pdt_date=(datetime.datetime.now()-datetime.timedelta(seconds=20)).strftime( '%-Y-%-m-%-d')
				"""
				title=subString(attrs['ptitle'],40)
				list={'id':pid,'title':title,'gmt_time':pdt_date,'short_time':short_time,'fulltitle':attrs['ptitle'],'pic_address':pic_address,'products_detail':products_detail,'arg':arg,'parea':parea}
				listall_offerlist.append(list)
			return listall_offerlist

def getpricelist_daohang(kname="",assist_type_id="",limitcount="",searchname="",titlelen="",hangqing=""):
	#------最新报价信息
	if (titlelen==""):
		titlelen=35
	port = settings.SPHINXCONFIG['port']
	cl = SphinxClient()
	cl.SetServer ( settings.SPHINXCONFIG['serverid'], port )
	cl.SetMatchMode ( SPH_MATCH_EXTENDED )
	cl.SetSortMode( SPH_SORT_EXTENDED,"gmt_order desc" )
	cl.SetLimits (0,limitcount,limitcount)
	if(assist_type_id!=None and assist_type_id!=""):
		if (hangqing=="1"):
			cl.SetFilter('type_id',[217,216,220])
		else:
			cl.SetFilter('assist_type_id',[assist_type_id])
	if (kname==None):
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
def getbbslist_daohang(kname,limitcount):
	#最新互助信息
	port = settings.SPHINXCONFIG['port']
	cl = SphinxClient()
	cl.SetServer ( settings.SPHINXCONFIG['serverid'], port )
	cl.SetMatchMode ( SPH_MATCH_EXTENDED )
	cl.SetSortMode( SPH_SORT_EXTENDED,"@weight desc,post_time desc" )
	cl.SetLimits (0,limitcount,limitcount)
	res = cl.Query ('@(title,tags) '+kname,'huzhu')
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
def getseolist():
	strseo="回收丝锥|http://wzjs.zz91.com/,"
	strseo=strseo+"回收废钨钢|http://feiwugang.zz91.com/,"
	strseo=strseo+"回收高速钢|http://mojugang.zz91.com/,"
	strseo=strseo+"回收废钛|http://feitai.zz91.com/,"
	strseo=strseo+"废电路板|http://lantianxianluban.zz91.net/,"
	strseo=strseo+"增强尼龙|http://wx-hengrun.zz91.com/,"
	strseo=strseo+"供应玻璃纤维|http://laoyc.zz91.com/,"
	strseo=strseo+"数控刀片回收|http://zygjs.zz91.com/,"
	strseo=strseo+"三边封袋|http://zhangxf.zz91.com/,"
	strseo=strseo+"四氧化锇|http://cj.zz91.com/,"
	strseo=strseo+"碎牛皮|http://kaiyuanpige.zz91.com/,"
	strseo=strseo+"爆竹生产厂家|http://lhbzc.zz91.com/,"
	strseo=strseo+"白色开花料|http://kaihualiao.zz91.com/"
	seolist=strseo.split(",")
	listall=[]
	for a in seolist:
		alist=a.split("|")
		label=alist[0]
		url=alist[1]
		list={'label':label,'url':url}
		listall.append(list)
	return listall
#微门户关键词
def getcplist():
	sql="select label,pingyin from daohang where type=1 and sid=3738"
	cursor.execute(sql)
	cplist=cursor.fetchall()
	listall=[]
	if cplist:
		for list in cplist:
			list={'label':list[0],'pingyin':list[1]}
			listall.append(list)
	return listall
def getHour():
	return str(datetime.datetime.now())[11:13] 
def getshowadflag():
	thour=getHour()
	if (int(thour)>=18 or int(thour)<7):
		showad=1
	else:
		showad=None
	return showad
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
	s=s.replace(" ","")
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
#加密
def getjiami(strword):
	return strword.encode('utf8','ignore').encode("hex")
def getjiemi(strword):
	return strword.decode("hex").decode('utf8','ignore')