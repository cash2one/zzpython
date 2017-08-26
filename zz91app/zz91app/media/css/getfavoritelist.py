def getfavoritelist(frompageCount,limitNum,company_id):
	sql="select count(0) from myfavorite where company_id=%s"
	cursor.execute(sql,[company_id])
	listall=None
	listcount=0
	alist=cursor.fetchone()
	if alist:
		listcount=alist[0]
		
	sql="select id,favorite_type_code,content_id,content_title from myfavorite where company_id=%s order by gmt_created desc limit "+str(frompageCount)+","+str(frompageCount+limitNum)+""
	cursor.execute(sql,[company_id])
	aalist=cursor.fetchall()
	listall=[]
	if alist:
		for list in aalist:
			favid=list[0]
			favorite_type_code=list[1]
			content_id=list[2]
			content_title=list[3]
			favorite_url=None
			favorite_urls=None
			favorite_type=None
			if (favorite_type_code):
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
				if (favorite_type_code=="10091012"):
					favorite_type="资讯中心"
					favorite_url="/news/newsdetail"+str(content_id)+".htm"
					favorite_urls=""
			
			
			lista={'favid':favid,'favorite_type_code':favorite_type_code,'favorite_type':favorite_type,'favorite_url':favorite_url,'favorite_urls':favorite_urls,'content_id':content_id,'content_title':content_title}
			listall.append(lista)
	return {'list':listall,'count':listcount}