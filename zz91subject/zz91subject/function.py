#----类别列表
def getindexcategorylist(code,showflag):
	catelist=getstaticValue('cate',code)
	if (catelist==None):
		sql="select label,code from category_products where code like %s order by sort asc"
		cursor.execute(sql,[str(code)])
		listall_cate=[]
		catelist=cursor.fetchall()
		for a in catelist:
			if (showflag==1):
				sql1="select label from category_products where code like '%s____' order by sort asc"
				cursor.execute(sql1,str(a[1]))
				listall_cate1=[]
				catelist1=cursor.fetchall()
				for b in catelist1:
					list1={'label':b[0]}
					listall_cate1.append(list1)
			else:
				listall_cate1=None
			list={'label':a[0],'code':a[1],'catelist':listall_cate1}
			listall_cate.append(list)
		updatetaticValue('cate',code,listall_cate)
	else:
		listall_cate=catelist
	
	return listall_cate
#----获得所有地区
def getarealist(code):
	sql="select label,code from category where code like %s"
	cursor.execute(sql,[code+"____"])
	catelist=cursor.fetchall()
	listall=[]
	for b in catelist:
		list={'code':b[1],'label':b[0],'label_hex':b[0].encode("hex")}
		listall.append(list)
	return listall
def getproducstcategorylist(code):
	codelen=len(code)
	sql="select label,code from category_products where left(code,"+str(codelen)+")=%s and length(code)="+str(codelen+4)+" order by sort asc"
	cursor.execute(sql,code)
	catelist=cursor.fetchall()
	listall=[]
	for b in catelist:
		list={'code':b[1],'label':b[0],'sql':sql}
		listall.append(list)
	return listall
#----相关供求类别
def getcategorylist(kname='',limitcount=''):
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
			return listall

	return results
#------最新报价信息
def getindexpricelist(kname="",assist_type_id="",limitcount="",searchname="",titlelen=""):
	if (titlelen=="" or titlelen==None):
		titlelen=100
	port = settings.SPHINXCONFIG['port']
	cl = SphinxClient()
	cl.SetServer ( settings.SPHINXCONFIG['serverid'], port )
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
def getcompanypricelist(kname="",limitcount="",titlelen="",company=""):
	
	if (titlelen=="" or titlelen==None):
		titlelen=100
	port = settings.SPHINXCONFIG['port']
	cl = SphinxClient()
	cl.SetServer ( settings.SPHINXCONFIG['serverid'], port )
	cl.SetMatchMode ( SPH_MATCH_BOOLEAN )
	cl.SetSortMode( SPH_SORT_EXTENDED,"post_time desc" )
	cl.SetLimits (0,limitcount,limitcount)
	if (kname):
		res = cl.Query ('@(title,label1,label2,label3,area1,area2,area3) '+kname,'company_price')
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
				company_id=attrs['company_id']
				gmt_time=attrs['ppost_time']
				min_price=attrs['min_price']
				max_price=attrs['max_price']
				if max_price=="":
					max_price=None
				price_unit=attrs['price_unit']
				country=attrs['country']
				province=attrs['province']
				city=attrs['city']
				companyname=None
				if company:
					sqlc="select name from company where id=%s"
					cursor.execute(sqlc,[company_id])
					alist = cursor.fetchone()
					if alist:
						companyname=alist[0]
						
				list1={'title':title,'id':id,'gmt_time':gmt_time,'min_price':min_price,'max_price':max_price,'price_unit':price_unit,'area':province+city,'company_id':company_id,'companyname':companyname,'fulltitle':attrs['ptitle'],'url':'http://price.zz91.com/companyprice/priceDetails'+str(id)+'.htm'}
				listall_baojia.append(list1)
			listcount_baojia=res['total_found']
			return listall_baojia
#------企业报价 翻页
def getcompanypricelistmore(kname="",frompageCount="",limitNum="",titlelen="",company="",province=""):
	if (titlelen=="" or titlelen==None):
		titlelen=100
	port = settings.SPHINXCONFIG['port']
	cl = SphinxClient()
	cl.SetServer ( settings.SPHINXCONFIG['serverid'], port )
	cl.SetMatchMode ( SPH_MATCH_BOOLEAN )
	cl.SetSortMode( SPH_SORT_EXTENDED,"post_time desc" )
	cl.SetLimits (frompageCount,limitNum,20000)
	if (kname):
		if (province and province!=""):
			k=kname+" "+province
		else:
			k=kname
		res = cl.Query ('@(title,label1,label2,label3,area1,area2,area3) '+k,'company_price')
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
				company_id=attrs['company_id']
				gmt_time=attrs['ppost_time']
				min_price=attrs['min_price']
				max_price=attrs['max_price']
				if max_price=="":
					max_price=None
				price_unit=attrs['price_unit']
				country=attrs['country']
				province=attrs['province']
				city=attrs['city']
				companyname=None
				if company:
					sqlc="select name from company where id=%s"
					cursor.execute(sqlc,[company_id])
					alist = cursor.fetchone()
					if alist:
						companyname=alist[0]
						
				list1={'title':title,'id':id,'gmt_time':gmt_time,'min_price':min_price,'max_price':max_price,'price_unit':price_unit,'area':province+city,'company_id':company_id,'companyname':companyname,'fulltitle':attrs['ptitle'],'url':'http://price.zz91.com/companyprice/priceDetails'+str(id)+'.htm','k':k}
				listall_baojia.append(list1)
			listcount_baojia=res['total_found']
			return {'list':listall_baojia,'count':listcount_baojia}
#----最新互助信息
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
#----最新互助信息 翻页
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
			i=1
			for match in tagslist:
				id=match['id']
				yy=i % 6
				if yy==1:
					yyhtml=1
				else:
					yyhtml=None
				if (i % 6==0):
					yyhtml_end=1
				else:
					yyhtml_end=None
				sql="select content from bbs_post where id=%s"
				cursor.execute(sql,id)
				alist = cursor.fetchone()
				if alist:
					havepic=havepicflag(alist[0])
				attrs=match['attrs']
				title=attrs['ptitle']
				gmt_time=attrs['ppost_time']
				list1={'title':title,'id':id,'gmt_time':gmt_time,'yyhtml':yyhtml,'yyhtml_end':yyhtml_end,'havepic':havepic}
				listall_news.append(list1)
				if i>=6:
					i=1
				else:
					i=i+1
			listcount_news=res['total_found']
			return {'list':listall_news,'count':listcount_news}
#----最新互助信息 翻页
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
					content=subString(filter_tags(alist[0]),50)
					username=getusername(alist[1])
					gmt_time=alist[2].strftime( '%-Y-%-m-%-d %-H:%-M:%-S')
				attrs=match['attrs']
				title=attrs['ptitle']
				list1={'lou':lou,'title':title,'id':id,'gmt_time':gmt_time,'content':content,'nickname':username}
				lou=lou+1
				listall_news.append(list1)
			listcount_news=res['total_found']
			return {'list':listall_news,'count':listcount_news}
#----报价列表 翻页
def getpricelist(kname,frompageCount,limitNum,category_id):
	port = settings.SPHINXCONFIG['port']
	cl = SphinxClient()
	cl.SetServer ( settings.SPHINXCONFIG['serverid'], port )
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
					content=subString(filter_tags(alist[0]),50)
					tags=alist[1]
				attrs=match['attrs']
				title=attrs['ptitle']
				gmt_time=attrs['gmt_time']
				list1={'title':title,'id':id,'gmt_time':gmt_time,'content':content,'tags':tags}
				listall_news.append(list1)
			listcount_news=res['total_found']
			return {'list':listall_news,'count':listcount_news}
#----公司信息列表 翻页
def getcompanylist(kname,frompageCount,limitNum,allnum):
	port = settings.SPHINXCONFIG['port']
	cl = SphinxClient()
	cl.SetServer ( settings.SPHINXCONFIG['serverid'], port )
	cl.SetMatchMode ( SPH_MATCH_BOOLEAN )
	cl.SetSortMode( SPH_SORT_EXTENDED,"membership_code desc,gmt_start desc" )
	cl.SetLimits (frompageCount,limitNum,allnum)
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
				domain_zz91=attrs['domain_zz91']
				address=attrs['paddress']
				membership="普通会员"
				if (viptype == '10051000'):
					membership='普通会员'
					vipflag=None
				if (viptype == '10051001'):
					membership='再生通'
					vipflag=1
				if (viptype == '1725773192'):
					membership='银牌品牌通'
					vipflag=1
				if (viptype == '1725773193'):
					membership='金牌品牌通'
					vipflag=1
				if (viptype == '1725773194'):
					membership='钻石品牌通'
					vipflag=1
				pbusiness=attrs['pbusiness']
				if pbusiness:
					pbusiness=subString(filter_tags(pbusiness),100)
				parea_province=attrs['parea_province']
				list1={'id':id,'compname':compname,'business':pbusiness,'area_province':parea_province,'address':address,'membership':membership,'viptype':viptype,'vipflag':vipflag,'domain_zz91':domain_zz91}
				listall_comp.append(list1)
			listcount_comp=res['total_found']
			return {'list':listall_comp,'count':listcount_comp}

#----获得帐号
def getcompanyaccount(company_id):
	sql="select account from  company_account where company_id=%s"
	cursor.execute(sql,[company_id])
	result=cursor.fetchone()
	if (result):
		return result[0]
#----获得公司ID
def getcompany_id(cname,regtime):
	sql="select id from company where name=%s and gmt_created=%s"
	cursor.execute(sql,[str(cname),str(regtime)])
	newcode=cursor.fetchone()
	if (newcode == None):
		return '0'
	else:
		return newcode[0]
#----获得公司名称
def getcompanyname(uname):
	sql="select company_id from company_account where account=%s"
	cursor.execute(sql,[uname])
	newcode=cursor.fetchone()
	if (newcode):
		company_id=newcode[0]
		sqlc="select name from company where id=%s"
		cursor.execute(sqlc,[company_id])
		clist=cursor.fetchone()
		if clist:
			return {'company_id':company_id,'companyname':clist[0]}

#----公司供求信息 翻页
def getcompanyproductslist(kname,frompageCount,limitNum,company_id,pdt_type):
	port = settings.SPHINXCONFIG['port']
	cl = SphinxClient()
	cl.SetServer ( settings.SPHINXCONFIG['serverid'], port )
	cl.SetMatchMode ( SPH_MATCH_BOOLEAN )
	if (company_id):
		cl.SetFilter('company_id',[int(company_id)])
	if (pdt_type !='' and pdt_type!=None):
		cl.SetFilter('pdt_kind',[int(pdt_type)])
	cl.SetSortMode( SPH_SORT_EXTENDED,"refresh_time desc" )
	cl.SetLimits (frompageCount,limitNum,200000)
	if (kname):
		res = cl.Query ('@(title,label0,label1,label2,label3,label4,city,province,tags) '+kname,'offersearch_new,offersearch_new_vip')
	else:
		res = cl.Query ('','offersearch_new,offersearch_new_vip')
	if res:
		if res.has_key('matches'):
			tagslist=res['matches']
			listall=[]
			for match in tagslist:
				id=match['id']
				list=getproductsinfo(id,cursor,kname)
				listall.append(list)
			listcount=res['total_found']
			return {'list':listall,'count':listcount}
#----供求列表页
def getsyproductslist(kname,frompageCount,limitNum,pinyin):
	port = settings.SPHINXCONFIG['port']
	cl = SphinxClient()
	cl.SetServer ( settings.SPHINXCONFIG['serverid'], port )
	cl.SetMatchMode ( SPH_MATCH_BOOLEAN )
	cl.SetSortMode( SPH_SORT_EXTENDED,"id desc" )
	cl.SetLimits (frompageCount,limitNum,1000000)
	if (kname and kname!=""):
		res = cl.Query ('@(title,label0,label1,label2,label3,label4,city,province,tags) '+kname,'offersearch_new,offersearch_new_vip')
	else:
		if (pinyin):
			res = cl.Query ('@pinyin '+str(pinyin),'offersearch_new,offersearch_new_vip')
		else:
			res = cl.Query ('','offersearch_new,offersearch_new_vip')
	if res:
		if res.has_key('matches'):
			tagslist=res['matches']
			listall=[]
			for match in tagslist:
				id=match['id']
				attrs=match['attrs']
				pdt_name=attrs['ptitle']
				list={'id':id,'pdt_name':pdt_name}
				listall.append(list)
			listcount=res['total_found']
			return {'list':listall,'count':listcount}
#----供求列表页 翻页
def getproductslist(kname="",frompageCount="",limitNum="",ptype="",havepic=""):
	port = settings.SPHINXCONFIG['port']
	cl = SphinxClient()
	cl.SetServer ( settings.SPHINXCONFIG['serverid'], port )
	cl.SetMatchMode ( SPH_MATCH_BOOLEAN )
	cl.SetSortMode( SPH_SORT_EXTENDED,"refresh_time desc" )
	cl.SetLimits (frompageCount,limitNum,1000000)
	if (ptype=='None'):
		ptype=""
	if (ptype and ptype!=""):
		cl.SetFilter('pdt_kind',[int(ptype)])
	if (havepic and havepic!=""):
		cl.SetFilterRange('havepic',1,100)
	if (kname and kname!=""):
		res = cl.Query ('@(title,label0,label1,label2,label3,label4,city,province,tags) '+kname,'offersearch_new,offersearch_new_vip')
	else:
		res = cl.Query ('','offersearch_new,offersearch_new_vip')
	if res:
		if res.has_key('matches'):
			tagslist=res['matches']
			listall=[]
			for match in tagslist:
				id=match['id']
				attrs=match['attrs']
				pdt_name=attrs['ptitle']
				list=getproductsinfo(id,cursor,kname)
				listall.append(list)
			listcount=res['total_found']
			return {'list':listall,'count':listcount}
#----索引公司列表页
def getsycompanylist(kname,frompageCount,limitNum,pinyin,maxcount):
	port = settings.SPHINXCONFIG['port']
	cl = SphinxClient()
	cl.SetServer ( settings.SPHINXCONFIG['serverid'], port )
	cl.SetMatchMode ( SPH_MATCH_BOOLEAN )
	cl.SetSortMode( SPH_SORT_EXTENDED,"id desc" )
	cl.SetLimits (frompageCount,limitNum,maxcount)
	if (kname and kname!=""):
		res = cl.Query ('@(name,business,address,sale_details,buy_details,tags,area_name,area_province) '+kname,'company')
	else:
		if (pinyin):
			res = cl.Query ('@pinyin '+str(pinyin),'company')
		else:
			res = cl.Query ('','company')
	if res:
		if res.has_key('matches'):
			tagslist=res['matches']
			listall=[]
			for match in tagslist:
				id=match['id']
				attrs=match['attrs']
				compname=attrs['compname']
				pbusiness=filter_tags(attrs['pbusiness'][0:1000])[0:150]+'...'
				list={'id':id,'compname':compname,'business':pbusiness}
				listall.append(list)
			listcount=res['total_found']
			return {'list':listall,'count':listcount}
#-------------最新标签
def newtagslist(kname,num):
	port = settings.SPHINXCONFIG['port']
	cl = SphinxClient()
	cl.SetServer ( settings.SPHINXCONFIG['serverid'], port )
	cl.SetMatchMode ( SPH_MATCH_BOOLEAN )
	cl.SetSortMode( SPH_SORT_EXTENDED,"search_count desc" )
	cl.SetLimits (0,num,num)
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
#----索引标签库列表
def gettagslist(frompageCount,limitNum,pinyin,maxcount):
	port = settings.SPHINXCONFIG['port']
	cl = SphinxClient()
	cl.SetServer ( settings.SPHINXCONFIG['serverid'], port )
	cl.SetMatchMode ( SPH_MATCH_BOOLEAN )
	cl.SetSortMode( SPH_SORT_EXTENDED,"id desc" )
	cl.SetLimits (frompageCount,limitNum,maxcount)
	if (pinyin):
		res = cl.Query ('@pinyin '+str(pinyin),'tagslist')
	else:
		res = cl.Query ('','tagslist')
	if res:
		if res.has_key('matches'):
			tagslist=res['matches']
			listall=[]
			for match in tagslist:
				id=match['id']
				attrs=match['attrs']
				tags=attrs['tags']
				list={'id':id,'tags':tags,'tags_hex':tags.encode("hex")}
				listall.append(list)
			listcount=res['total_found']
			return {'list':listall,'count':listcount}
#---供求列表
def getindexofferlist(kname,pdt_type,limitcount):
	port = settings.SPHINXCONFIG['port']
	cl = SphinxClient()
	cl.SetServer ( settings.SPHINXCONFIG['serverid'], port )
	cl.SetMatchMode ( SPH_MATCH_BOOLEAN )
	cl.SetSortMode( SPH_SORT_EXTENDED," refresh_time desc" )
	cl.SetLimits (0,limitcount,limitcount)
	if (pdt_type!=None):
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
					pdt_datem=productlist[0].strftime( '%-m/%-d')
				title=subString(attrs['ptitle'],40)
				list={'id':pid,'title':title,'gmt_time':pdt_date,'gmt_time_m':pdt_datem,'fulltitle':attrs['ptitle']}
				listall_offerlist.append(list)
			return listall_offerlist

#----产品报价信息
def getofferprice(id):
	sql="select p.min_price,p.max_price,p.price_unit from products as p where p.id=%s"
	cursor.execute(sql,[id])
	plist = cursor.fetchone()
	if plist:
		#价格范围判断
		allprice=""
		min_price=plist[0]
		if (min_price==None):
			min_price=''
		else:
			min_price=str(min_price)
			if (min_price!='0.0'):
				allprice=allprice+min_price
		max_price=plist[1]
		if (max_price==None):
			max_price=''
		else:
			max_price=str(max_price)
			if (max_price!='0.0' and max_price!=min_price):
				allprice=allprice+'-'+max_price
		price_unit=plist[2]
		#
		if (price_unit==None):
			price_unit=''
		else:
			if (allprice!=''):
				allprice=allprice+price_unit
		if (allprice==""):
			allprice="电议或面议"
		return allprice
	
#----公司库首页有图片的最新供求列表
def getindexofferlist_pic(kname="",pdt_type="",limitcount="",membertype=""):
	port = settings.SPHINXCONFIG['port']
	cl = SphinxClient()
	cl.SetServer ( settings.SPHINXCONFIG['serverid'], port )
	cl.SetMatchMode ( SPH_MATCH_BOOLEAN )
	cl.SetSortMode( SPH_SORT_EXTENDED," refresh_time desc" )
	cl.SetGroupBy("company_id",SPH_GROUPBY_ATTR)
	
	cl.SetLimits (0,limitcount,limitcount)
	if (pdt_type!=None and pdt_type!=""):
		cl.SetFilter('pdt_kind',[int(pdt_type)])
	cl.SetFilterRange('havepic',1,100)
	cl.SetFilterRange('haveprice',2,1000)
	if membertype:
		searchindex="offersearch_new_vip"
		cl.SetFilterRange('length_price',1,100000)
	else:
		searchindex="offersearch_new,offersearch_new_vip"
	if (kname==None):
		res = cl.Query ('',searchindex)
	else:
		res = cl.Query ('@(title,label0,label1,label2,label3,label4,city,province,tags) '+kname,searchindex)
	if res:
		if res.has_key('matches'):
			itemlist=res['matches']
			listall_offerlist=[]
			for match in itemlist:
				pid=match['id']
				price=getofferprice(pid)
				attrs=match['attrs']
				pdt_date=attrs['pdt_date']
				pdt_kind=attrs['pdt_kind']
				kindtxt=''
				if (pdt_kind=='1'):
					kindtxt="供应"
				else:
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
					pdt_images='http://img3.zz91.com/125x125/'+pdt_images+''
				list={'id':pid,'title':title,'gmt_time':pdt_date,'kindtxt':kindtxt,'fulltitle':attrs['ptitle'],'pdt_images':pdt_images,'price':price}
				listall_offerlist.append(list)
			return listall_offerlist

#----最新加入高会			
def getcompanyindexcomplist(kname,num):
	#-------------供求列表
	port = settings.SPHINXCONFIG['port']
	cl = SphinxClient()
	cl.SetServer ( settings.SPHINXCONFIG['serverid'], port )
	cl.SetMatchMode ( SPH_MATCH_BOOLEAN )
	cl.SetSortMode( SPH_SORT_EXTENDED," gmt_start desc" )
	cl.SetLimits (0,num,num)
	cl.SetFilter('apply_status',[1])

	nowdate=date.today()-timedelta(days=900)
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
				business=filter_tags(attrs['pbusiness'])
				
				area_province=attrs['parea_province']
				domain_zz91=attrs['domain_zz91']
				list={'id':id,'comname':comname,'business':business,'area_province':area_province,'domain_zz91':domain_zz91}
				listall_company.append(list)
			return listall_company

def getvipcompanycount():
	port = settings.SPHINXCONFIG['port']
	cl = SphinxClient()
	cl.SetServer ( settings.SPHINXCONFIG['serverid'], port )
	cl.SetMatchMode ( SPH_MATCH_BOOLEAN )
	cl.SetSortMode( SPH_SORT_EXTENDED," gmt_start desc" )
	cl.SetLimits (0,1)
	cl.SetFilter('apply_status',[1])
	res = cl.Query ('','company')
	if res:
		listcount=res['total_found']
	return listcount

#----诚信客户列表
def getchenxincompany(num=""):
	sql="select company_id,company_name from company_attest where check_status=1 order by gmt_created desc limit 0,"+str(num)+""
	cursor.execute(sql)
	complist = cursor.fetchall()
	listall=[]
	for list in complist:
		company_id=list[0]
		company_name=list[1]
		company_pic=getoneproductscompany(company_id)['pdt_images']
		company_pic=company_pic.replace('width=200&height=169','width=278&height=216')
		companymore=getcompanybusiness(company_id)
		company_business=subString(companymore['business'],40)
		domain_zz91=companymore['domain_zz91']
		integral=getcompanyintegral(company_id)
		if(domain_zz91==""):
			domain_zz91=None
		list={'company_id':company_id,'company_name':company_name,'company_pic':company_pic,'company_business':company_business,'domain_zz91':domain_zz91,'integral':integral}
		listall.append(list)
	return listall
#----获得诚信指数
def getcompanyintegral(company_id):
	sql="select sum(integral) from credit_integral_details where company_id=%s"
	cursor.execute(sql,[company_id])
	alist=cursor.fetchone()
	if alist:
		return alist[0]
#----获得公司的一张供求图片信息
def getoneproductscompany(company_id):	
	sql="select a.pic_address,b.title from products_pic as a left join products as b on a.product_id=b.id where b.company_id=%s and a.check_status=1 order by a.is_default desc limit 0,1"
	cursor.execute(sql,[company_id])
	productspic = cursor.fetchone()
	pdt_title=""
	if productspic:
		pdt_images=productspic[0]
		pdt_title=productspic[1]
	else:
		pdt_images=""
	if (pdt_images == '' or pdt_images == '0'):
		pdt_images='http://img0.zz91.com/front/images/global/noimage.gif'
	else:
		pdt_images='http://img3.zz91.com/200x169/'+pdt_images+''
	return {'pdt_images':pdt_images,'pdt_title':pdt_title}
#获得公司主营业务
def getcompanybusiness(company_id):
	sql="select business,domain_zz91 from company where id=%s"
	cursor.execute(sql,[company_id])
	comp = cursor.fetchone()
	if comp:
		return {'business':comp[0],'domain_zz91':comp[1]}
#是否来电宝客户
def isldb(company_id):
	sqlg="select front_tel from phone where company_id=%s"
	cursor.execute(sqlg,company_id)
	phoneresult=cursor.fetchone()
	if phoneresult:
		return 1
	else:
		return None
#最新加入高会(含供求图片)			
def getindexcompanylist_pic(keywords="",num="",frompageCount="",limitNum=""):
	#-------------供求列表
	port = settings.SPHINXCONFIG['port']
	cl = SphinxClient()
	cl.SetServer ( settings.SPHINXCONFIG['serverid'], port )
	cl.SetMatchMode ( SPH_MATCH_BOOLEAN )
	cl.SetSortMode( SPH_SORT_EXTENDED," refresh_time desc" )
	cl.SetGroupBy("company_id",SPH_GROUPBY_ATTR)
	cl.SetFilterRange('havepic',1,100)
	cl.SetFilterRange('viptype',1,100)
	if (num):
		cl.SetLimits (0,num)
	else:
		cl.SetLimits (frompageCount,limitNum,20000)
		
	if (keywords):
		res = cl.Query ('@(title,label0,label1,label2,label3,label4,city,province,tags) '+keywords,'offersearch_new_vip')
	else:
		res = cl.Query ('','offersearch_new,offersearch_new_vip')
	if res:
		if res.has_key('matches'):
			itemlist=res['matches']
			listall_company=[]
			for match in itemlist:
				id=match['id']
				attrs=match['attrs']
				company_id=attrs['company_id']
				business=getcompanybusiness(company_id)['business']
				list=getproductsinfo(id,cursor,keywords)
				list['business']=business
				pdt_images=list['pdt_images']
				pdt_images=pdt_images.replace('122x93','194x166')
				list['pdt_images']=pdt_images
				ldbflag=isldb(company_id)
				list['ldbflag']=ldbflag
				listall_company.append(list)
			listcount=res['total_found']
			return {'list':listall_company,'listcount':listcount}
#最新加入普会
def getcommoncompanylist(keywords="",num="",frompageCount="",limitNum="",pic="",companyflag="",ptype=""):
	#-------------供求列表
	port = settings.SPHINXCONFIG['port']
	cl = SphinxClient()
	cl.SetServer ( settings.SPHINXCONFIG['serverid'], port )
	cl.SetMatchMode ( SPH_MATCH_BOOLEAN )
	cl.SetSortMode( SPH_SORT_EXTENDED," refresh_time desc" )
	#判断是否公司分组
	if (companyflag):
		cl.SetGroupBy("company_id",SPH_GROUPBY_ATTR)
	if pic:
		cl.SetFilterRange('havepic',1,100)
	if (ptype and ptype!=""):
		cl.SetFilter('pdt_kind',[int(ptype)])
	cl.SetFilter('viptype',[0])
	if (num):
		cl.SetLimits (0,num)
	else:
		cl.SetLimits (frompageCount,limitNum,20000)
		
	if (keywords):
		res = cl.Query ('@(title,label0,label1,label2,label3,label4,city,province,tags) '+keywords,'offersearch_new')
	else:
		res = cl.Query ('','offersearch_new')
	if res:
		if res.has_key('matches'):
			itemlist=res['matches']
			listall_company=[]
			for match in itemlist:
				id=match['id']
				attrs=match['attrs']
				company_id=attrs['company_id']
				business=getcompanybusiness(company_id)['business']
				list=getproductsinfo(id,cursor,keywords)
				list['business']=business
				pdt_images=list['pdt_images']
				pdt_images=pdt_images.replace('122x93','180x169')
				list['pdt_images']=pdt_images
				ldbflag=isldb(company_id)
				list['ldbflag']=ldbflag
				listall_company.append(list)
			listcount=res['total_found']
			return {'list':listall_company,'listcount':listcount}
#微信绑定客户
def getweixincomplist(frompageCount="",limitNum=""):
	sqlc="select count(0) from oauth_access as c where c.open_type='weixin.qq.com' and exists(select a.company_id from company_account as a left join products as b on a.company_id=b.company_id where b.check_status=1 and c.target_account=a.account)"
	cursor.execute(sqlc)
	listcount = cursor.fetchone()[0]
	
	sql="select c.target_account from oauth_access as c where c.open_type='weixin.qq.com' and exists(select a.company_id from company_account as a left join products as b on a.company_id=b.company_id where b.check_status=1 and c.target_account=a.account) order by c.gmt_created desc limit %s,%s"
	cursor.execute(sql,[frompageCount,limitNum])
	alist=cursor.fetchall()
	listall=[]
	if alist:
		for list in alist:
			sqlc="select company_id from company_account where account=%s"
			cursor.execute(sqlc,[list[0]])
			clist = cursor.fetchone()
			if clist:
				company_id=clist[0]
				sqlp="select id,company_id from products where company_id=%s and check_status=1 order by refresh_time desc limit 0,1"
				cursor.execute(sqlp,[company_id])
				aalist = cursor.fetchone()
				if aalist:
					id=aalist[0]
					company_id=aalist[1]
					business=getcompanybusiness(company_id)['business']
					keywords=None
					list=getproductsinfo(id,cursor,keywords)
					list['business']=business
					list['businessmini']=subString(business,10)
					pdt_images=list['pdt_images']
					pdt_images=pdt_images.replace('122x93','210x205')
					list['pdt_images']=pdt_images
					ldbflag=isldb(company_id)
					list['ldbflag']=ldbflag
					listall.append(list)
					
	return {'list':listall,'listcount':listcount}			
#根据拼音获得导航属性
def getpingyinattribute(pingyin):
	sql="select label,templates,keywords,keywords1,num_str,keywords2,keywords3,sid,id from daohang where pingyin=%s and type=1"
	cursor.execute(sql,[pingyin])
	daohanglist=cursor.fetchone()
	list=None
	if (daohanglist):
		label=daohanglist[0]
		keywords=daohanglist[2]
		keywords1=daohanglist[3]
		keywords2=daohanglist[5]
		keywords3=daohanglist[6]
		num_str=daohanglist[4]
		sid=daohanglist[7]
		id=daohanglist[8]
		label=label.replace("价格","")
		if (keywords=='' or keywords==None):
			keywords=label
		if (keywords1=='' or keywords1==None):
			keywords1=label
		if (keywords2=='' or keywords2==None):
			keywords2=label
		if (keywords3=='' or keywords3==None):
			keywords3=label
		keywords=keywords.replace("价格","")
		keywords1=keywords1.replace("价格","")
		keywords2=keywords2.replace("价格","")
		keywords3=keywords3.replace("价格","")
		adkeywords=urlquote(keywords)
		
		list={'id':id,'label':label,'keywords':keywords,'keywords1':keywords1,'keywords2':keywords2,'keywords3':keywords3}
	return list
def getcategoryname(code):
	sql="select label from category where code=%s"
	cursor.execute(sql,[code])
	resultlist=cursor.fetchone()
	if resultlist:
		return resultlist[0]
#老站相关
def getoldnewslist(kname=""):
	sql="select title,content,tags,post_time,visited_count,old_news_id from news_list order by post_time desc limit 0,10"
	cursor.execute(sql)
	oldlist = cursor.fetchall()
	if oldlist:
		listall=[]
		for nlist in oldlist:
			list={'title':nlist[0],'content':nlist[1],'tags':nlist[2],'post_time':nlist[3].strftime( '%-Y-%-m-%-d %-H:%-M:%-S'),'visited_count':nlist[4],'old_news_id':nlist[5]}
			listall.append(list)
		return listall

#老站资讯详细内容
def getnewsdetail(newsid="",newszd=""):
	tags=None
	list=None
	sql="select title,content,tags,post_time,visited_count from news_list where "+newszd+"=%s"
	cursor.execute(sql,[newsid])
	nlist = cursor.fetchone()
	if nlist:
		tags=nlist[2]
		if (tags and tags!=""):
			tags=tags.replace(",","|")
		content=nlist[1]
		content=replacepic(content)
		list={'title':nlist[0],'content':content,'tags':nlist[2],'post_time':nlist[3].strftime( '%-Y-%-m-%-d %-H:%-M:%-S'),'visited_count':nlist[4]}
		
	else:
		sql="select title,content,tags,post_time,visited_count from bbs_post where "+newszd+"=%s"
		cursor.execute(sql,[newsid])
		nlist = cursor.fetchone()
		if nlist:
			tags=nlist[2]
			content=nlist[1]
			content=replacepic(content)
			if (tags and tags!=""):
				tags=tags.replace(",","|")
			list={'title':nlist[0],'content':content,'tags':nlist[2],'post_time':nlist[3].strftime( '%-Y-%-m-%-d %-H:%-M:%-S'),'visited_count':nlist[4]}
		else:
			sql="select title,content,tags,post_time,visited_count from bbs_post where id=%s"
			cursor.execute(sql,[newsid])
			nlist = cursor.fetchone()
			if nlist:
				content=nlist[1]
				content=replacepic(content)
				list={'title':nlist[0],'content':content,'tags':nlist[2],'post_time':nlist[3].strftime( '%-Y-%-m-%-d %-H:%-M:%-S'),'visited_count':nlist[4]}
				tags=nlist[2]
				if (tags and tags!=""):
					tags=tags.replace(",","|")
					
	return {'list':list,'tags':tags}
#新闻栏目
def getlbhex():
	lb="国内资讯,国外资讯,市场动态,商务交流,焦点关注,行情综述,废料百科,热门评论,再生技术"
	lb_hex="国内,国外,市场动态,商务|交流,焦点关注,行情综述,百科,评论,再生技术"
	alllist=[]
	lbarr=lb.split(",")
	lbarr_hex=lb_hex.split(",")
	i=0
	for a in lbarr:
		list={'name_hex':getjiami(lbarr_hex[i]),'name':a}
		alllist.append(list)
		i=i+1
	return alllist
#优质客户推荐栏目			
def gettjhex1():
	lb="钢铁,稀有金属,贵金属,有色金属,金属混合\复合料,废金属处理设备,金属助剂"
	lb_hex="钢铁,稀有金属,贵金属,有色金属,金属混合|复合料,废金属处理设备,金属助剂"
	alllist=[]
	lbarr=lb.split(",")
	lbarr_hex=lb_hex.split(",")
	i=0
	for a in lbarr:
		list={'name_hex':getjiami(lbarr_hex[i]),'name':a}
		alllist.append(list)
		i=i+1
	return alllist
def gettjhex2():
	lb="通用废塑料,工程废塑料,塑料颗粒,特种废塑料,塑料混合/复合料,废塑料处理设备,塑料助剂"
	lb_hex="通用废塑料,工程废塑料,塑料颗粒,特种废塑料,塑料混合|复合料,废塑料处理设备,塑料助剂"
	alllist=[]
	lbarr=lb.split(",")
	lbarr_hex=lb_hex.split(",")
	i=0
	for a in lbarr:
		list={'name_hex':getjiami(lbarr_hex[i]),'name':a}
		alllist.append(list)
		i=i+1
	return alllist
def gettjhex3():
	lb="废纺织品,废纸,二手设备,废电子电器,废橡胶,废轮胎,服务"
	lb_hex="纺织品,废纸,设备,电子电器,橡胶,轮胎,服务"
	alllist=[]
	lbarr=lb.split(",")
	lbarr_hex=lb_hex.split(",")
	i=0
	for a in lbarr:
		list={'name_hex':getjiami(lbarr_hex[i]),'name':a}
		alllist.append(list)
		i=i+1
	return alllist
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
def getcomplist(industryCode):
	#-------------供求列表
	port = settings.SPHINXCONFIG['port']
	cl = SphinxClient()
	cl.SetServer ( settings.SPHINXCONFIG['serverid'], port )
	cl.SetMatchMode ( SPH_MATCH_BOOLEAN )
	cl.SetSortMode( SPH_SORT_EXTENDED," gmt_start desc" )
	cl.SetLimits (0,300)
	cl.SetFilter('apply_status',[1])
	if (industryCode==10001001 or industryCode==10001000):
		cl.SetFilter('industry_code',[industryCode])
	else:
		cl.SetFilter('industry_code',[10001001],True)
		cl.SetFilter('industry_code',[10001000],True)
	nowdate=date.today()-timedelta(days=90)
	nextday=date.today()+timedelta(days=1)
	formatnowdate=time.mktime(nowdate.timetuple())
	formatnextday=time.mktime(nextday.timetuple())
	cl.SetFilterRange('gmt_start',int(formatnowdate),int(formatnextday))
	
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
def getwarmwinter(pkind):
	sql="select ad_content,ad_target_url,DATE_FORMAT(gmt_plan_end,'%Y') as ayear,DATE_FORMAT(gmt_plan_end,'%m') as amouth,DATE_FORMAT(gmt_plan_end,'%d') as aday,id from ad where position_id=%s and gmt_plan_end>='"+str(date.today()+timedelta(days=1))+"' and review_status='Y' order by sequence asc"
	cursor_ad.execute(sql,[pkind])
	adlist = cursor_ad.fetchall()
	adlist_main=[]
	if adlist:
		adlist_all=[]
		adcount=0
		for alist in adlist:
			list={'id':alist[5],'picaddress':alist[0],'picurl':alist[1],'ayear':alist[2],'amouth':alist[3],'aday':alist[4]}
			adlist_all.append(list)
			adcount=adcount+1
		adlist_main.append(adlist_all)
		adlist_main.append(adcount)
		return adlist_main
def getOrderadlist(pkind,e):
	sql="select ad_content,ad_target_url,DATE_FORMAT(gmt_plan_end,'%Y') as ayear,DATE_FORMAT(gmt_plan_end,'%m') as amouth,DATE_FORMAT(gmt_plan_end,'%d') as aday,id,ad_title,ad_description from ad where position_id=%s and gmt_plan_end>='"+str(date.today()+timedelta(days=0))+"' and review_status='Y' and sequence=%s order by gmt_start asc"
	cursor_ad.execute(sql,[pkind,e])
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
			
		list={'id':alist[5],'picaddress':alist[0],'picurl':alist[1],'ayear':alist[2],'amouth':alist[3],'aday':alist[4],'ad_title':alist[5],'ad_description':ad_description}
		return list
	else:
		return None
#获得广告位广告数
def getadpostionNum(akind):
	sql="select max_ad from ad_position where id=%s"
	cursor_ad.execute(sql,[akind])
	alist = cursor_ad.fetchone()
	if alist:
		return alist[0]
	else:
		return 1
def getHour(): 
	#return str(datetime.datetime.now())
	return str(time.strftime('%H', time.localtime()))
def getRange():
	return str(time.strftime('%d', time.localtime()))+str(time.strftime('%T', time.localtime())).replace(":","")
	#return str(datetime.datetime.now())

#----获得专题栏目
def getwebtypelist(frompageCount,limitNum,wtype='',recommend=''):
    sql1='select count(0) from webtype'
    sql1=sql1+' where wtype='+str(wtype)
    count=fetchnumberdb(sql1,cursor_other)
    listall=[]
    sql='select id,typename,sortrank from webtype'
    sql=sql+' where wtype='+str(wtype)
    sql=sql+' order by sortrank,id limit '+str(frompageCount)+','+str(limitNum)
    resultlist=fetchalldb(sql,cursor_other)
    js=0
    if resultlist:
        for result in resultlist:
            id=result[0]
            js=js+1
            websitelist=getwebsitelist(0,4,id,recommend)
            listweb=[]
            list={'id':id,'typename':result[1],'sortrank':result[2],'listweb':'','js':js}
            if websitelist:
                listweb=websitelist['list']
            	list['listweb']=listweb
            listall.append(list)
    return {'list':listall,'count':count}
def gettypedetail(id):
    sql='select id,typename,sortrank from webtype where id=%s'
    result=fetchonedb(sql,cursor_other,[id])
    list=[]
    if result:
        list={'id':result[0],'typename':result[1],'sortrank':result[2]}
    return list
  
def getwebsitelist(frompageCount,limitNum,typeid='',recommend='',wtype='',order=''):
    sql1='select count(0) from website where isdelete=0'
    if typeid:
        sql1=sql1+' and typeid='+str(typeid)
    if wtype:
        sql1=sql1+' and wtype='+str(wtype)
    if recommend:
        sql1=sql1+' and recommend='+str(recommend)
    count=fetchnumberdb(sql1,cursor_other)
    listall=[]
    sql='select id,typeid,name,url,pic,gmt_created,sortrank,recommend from website where isdelete=0'
    if typeid:
        sql=sql+' and typeid='+str(typeid)
    if wtype:
        sql=sql+' and wtype='+str(wtype)
    if recommend:
        sql=sql+' and recommend='+str(recommend)
    if order:
    	sql=sql+' order by '+order+' desc'
    else:
    	sql=sql+' order by sortrank,updatetime desc,gmt_created desc'
    sql=sql+' limit '+str(frompageCount)+','+str(limitNum)
    resultlist=fetchalldb(sql,cursor_other)
    js=1
    if resultlist:
        for result in resultlist:
            typeid1=result[1]
            js=js+1
            typename=gettypedetail(typeid1)['typename']
            list={'id':result[0],'typeid':typeid1,'typename':typename,'name':result[2],'url':result[3],'pic':result[4],'gmt_created':formattime(result[5],1),'sortrank':result[6],'recommend':result[7],'js':js}
            listall.append(list)
    return {'list':listall,'count':count}

#----新闻列表
def getindexnewslist(keywords="",limitNum="",typeid="",typeid2=""):
	port = settings.SPHINXCONFIG['port']
	cl = SphinxClient()
	cl.SetServer ( settings.SPHINXCONFIG['serverid'], port )
	cl.SetMatchMode ( SPH_MATCH_BOOLEAN )
	if (typeid):
		cl.SetFilter('typeid',[typeid])
	if (typeid2):
		cl.SetFilter('typeid2',[typeid2])
	cl.SetSortMode( SPH_SORT_EXTENDED,"pubdate desc,click desc" )
	cl.SetLimits (0,limitNum,limitNum)
	if (keywords):
		res = cl.Query ('@(title) '+keywords,'news')
	else:
		res = cl.Query ('','news')
	listall_news=[]
	if res:
		if res.has_key('matches'):
			tagslist=res['matches']
			for match in tagslist:
				id=match['id']
				attrs=match['attrs']
				title=attrs['ptitle']
				short_title=title.decode('utf8')[:13]
				pubdate=attrs['pubdate']
				list1={'title':title,'short_title':short_title,'id':id,'pubdate':timestamp_datetime(pubdate,time)}
				listall_news.append(list1)
	return listall_news

#----资讯列表
def getnewslist(keywords="",frompageCount="",limitNum="",typeid="",allnum="",typeid2="",contentflag=""):
	cursor_news = conn_news.cursor()
	port = settings.SPHINXCONFIG['port']
	cl = SphinxClient()
	cl.SetServer ( settings.SPHINXCONFIG['serverid'], port )
	cl.SetMatchMode ( SPH_MATCH_BOOLEAN )
	if (typeid):
		cl.SetFilter('typeid',typeid)
	if (typeid2):
		cl.SetFilter('typeid2',[typeid2])
	cl.SetSortMode( SPH_SORT_EXTENDED,'"pubdate desc,click desc"' )
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
				attrs=match['attrs']
				title=attrs['ptitle']
				short_title=title.decode('utf8')[:13]
				pubdate=attrs['pubdate']
				pubdate2=timestamp_datetime(pubdate,time)
				list1={'title':title,'short_title':short_title,'id':id,'pubdate':pubdate2,'newsurl':newsurl,'weburl':weburl}
				listall_news.append(list1)
			listcount_news=res['total_found']
	return {'list':listall_news,'count':listcount_news}
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
				pdt_date=timestamp_datetime(attrs['refresh_time'],time)
				short_time=pdt_date[5:]
				title=subString(attrs['ptitle'],40)
				list={'id':pid,'title':title,'gmt_time':pdt_date,'short_time':short_time,'fulltitle':attrs['ptitle'],'arg':arg}
				listall_offerlist.append(list)
			return listall_offerlist
		
#15届中国塑料交易会会后报道客户名单
def zsshowcomp():
	sql="select 公司名,联系人,手机,地区,主营业务 from zt_zhanhui_1"
	cursor.execute(sql)
	catelist=cursor.fetchall()
	listall=[]
	for b in catelist:
		list={'name':b[0],'contact':b[1],'mobile':b[2],'area':b[3],'zhuyin':b[4]}
		listall.append(list)
	return listall