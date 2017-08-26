def getnowurl(request):
	host=request.path_info
	qstring=request.META.get('QUERY_STRING','/')
	qstring=qstring.replace("&","^and^")
	if qstring:
		return host+"?"+qstring
	else:
		return host
def getwebhtml(url):
	f = urllib.urlopen(url)
	html = f.read()
	return html	
def getzwpic(request):
	host = request.META['HTTP_REFERER']
	zposition=host.find("zz91.com")
	if (zposition>0):
		"""
		ic = ImageChar(fontColor=(0,0,0))
		chars=ic.randChinese(2).encode('utf-8')
		mstream = StringIO.StringIO()
		pic=ic.returnimg()
		img=pic.save(mstream, "GIF")
		mstream.closed
		#host = request.META['HTTP_REFERER']
		#zposition=host.find("zz91.com")
		#if (zposition>0):
		t = request.GET.get("t")
		cache.set("yzm"+str(t),chars,60*10)
		"""
		mstream = StringIO.StringIO()
		validate_code = create_validate_code()
		img = validate_code[0]
		img.save(mstream, "GIF")
		mstream.closed
		t = request.GET.get("t")
		code=validate_code[1]
		cache.set("yzm"+str(t),code,60*60)
		return HttpResponse(mstream.getvalue(),'image/gif')

def verifycode(request):
	host = request.META['HTTP_REFERER']
	zposition=host.find("zz91.com")
	if (zposition>0):
		mstream = StringIO.StringIO()
		validate_code = create_validate_code()
		img = validate_code[0]
		img.save(mstream, "GIF")
		mstream.closed
		t = request.GET.get("t")
		#tt = random.randrange(0,1000000000)
		code=validate_code[1]
		#cache.set("yzmrandom"+t,str(tt),60*60)
		#cache.set("yzm"+str(tt),code,60*60)
		cache.set("yzm"+str(t),code,60*60)
		#request.session['yzm']=validate_code[1]
		#浏览器关闭时失效
		#request.session.set_expiry(0)
		
		return HttpResponse(mstream.getvalue(),'image/gif')
def getcompany_area(company_id):
	sql='select area_code from company where id=%s'
	result=dbc.fetchonedb(sql,[company_id])
	if result:
		area_code=result[0]
		sql2='select label from category where code=%s'
		result2=dbc.fetchonedb(sql2,[area_code])
		if result2:
			area=result2[0]
			return area
def getviptype(company_id):
	sql='select membership_code from company where id=%s'
	result=dbc.fetchonedb(sql,[company_id])
	if result:
		return result[0]

#---需要改成搜索引擎,供求信息置顶
def getshop_productlist(company_id,paytype):
	gmt_created=datetime.datetime.now()
	topproductslist=cache.get("mobile_getshop_productlist"+str(company_id)+str(paytype))
	if getshop_productlist:
		return getshop_productlist
	sql='select pro_id from shop_product where company_id=%s and paytype=%s and gmt_end>%s'
	resultall=dbc.fetchalldb(sql,[company_id,paytype,gmt_created])
	listall=[]
	if resultall:
		for list in resultall:
			proid=result[0]
			
			sql1="select pic_address from products_pic where product_id=%s and check_status=1"
			productspic=dbc.fetchonedb(sql1,proid)
			if productspic:
				pdt_images=productspic[0]
			else:
				pdt_images=""
			if (pdt_images == '' or pdt_images == '0'):
				pdt_images='../cn/img/noimage.gif'
			else:
				pdt_images='http://img3.zz91.com/135x135/'+pdt_images+''
			
			sql2='select products_type_code,title,refresh_time,price,price_unit,source from products where id=%s'
			result2=dbc.fetchonedb(sql2,proid)
			if result2:
				products_type_code=result2[0]
				kindtxt=''
				if products_type_code=='10331000':
					kindtxt='供应'
				elif products_type_code=='10331001':
					kindtxt='求购'
				title=result2[1]
				refresh_time=result2[2]
				price=result2[3]
				if price:
					price_unit=result2[4]
					pdt_price=price+price_unit
				else:
					pdt_price='电议或面议'
				area=result2[5]
				if not area:
					area=getcompany_area(company_id)
			list={'pdt_id':proid,'pdt_images':pdt_images,'kindtxt':kindtxt,'pdt_name':title,'pdt_time_en':refresh_time,'pdt_price':pdt_price,'area':area}
			listall.append(list)
	cache.set("mobile_getshop_productlist"+str(company_id)+str(paytype),listall,60*5)
	return listall
#类别列表
def getindexcategorylist(code,showflag):
	catelist=cache.get("mobile_catec"+str(code))
	if (catelist==None):
		if (showflag==2):
			sql="select label,code,pinyin from category_products where code like %s order by sort asc"
		else:
			sql="select label,code,pinyin from category_products where code like %s"'"____"'" order by sort asc"
		#cursor.execute(sql,[str(code)])
		listall_cate=[]
		#catelist=cursor.fetchall()
		catelist=dbc.fetchalldb(sql,[str(code)])
		numb=0
		for a in catelist:
			numb=numb+1
			if (showflag==1):
				sql1="select label,pinyin from category_products where code like '"+str(a[1])+"____' order by sort asc"
				#cursor.execute(sql1)
				listall_cate1=[]
				#catelist1=cursor.fetchall()
				catelist1=dbc.fetchalldb(sql1)
				for b in catelist1:
					list1={'label':b[0],'pinyin':b[1].lower()}
					listall_cate1.append(list1)
			else:
				listall_cate1=None
			list={'label':a[0],'code':a[1],'catelist':listall_cate1,'numb':numb,'pinyin':a[2].lower()}
			listall_cate.append(list)
		cache.set("mobile_catec"+str(code),listall_cate,60*6)
	else:
		listall_cate=catelist
	
	return listall_cate

def getmyquestion(company_id,frompageCount,limitNum):
	sql1='select count(0) from bbs_post where company_id=%s '
	#cursor.execute(sql1,[company_id])
	#result1=cursor.fetchone()
	result1=dbc.fetchonedb(sql1,[company_id])
	if result1:
		count=result1
	else:
		count=0
	sql='select id,title,post_time,reply_count from bbs_post where company_id=%s  order by id desc limit %s,%s'
	#cursor.execute(sql,[company_id,frompageCount,limitNum])
	#resultlist=cursor.fetchall()
	resultlist=dbc.fetchalldb(sql,[company_id,frompageCount,limitNum])
	listall=[]
	if resultlist:
		for result in resultlist:
			list={'id':result[0],'title':result[1],'post_time':formattime(result[2],2),'reply_count':result[3]}
			listall.append(list)
	return {'list':listall,'count':count}
#----回复回复
def replyreplylist(replyid,frompageCount,limitNum):
	sql="select account,title,content,gmt_created,company_id,id,tocompany_id from bbs_post_reply where bbs_post_reply_id=%s and is_del='0' and check_status in ('1','2') order by gmt_created desc limit %s,%s"
	#cursor.execute(sql,[str(replyid),frompageCount,limitNum])
	#alist = cursor.fetchall()
	alist=dbc.fetchalldb(sql,[str(replyid),frompageCount,limitNum])
	listall={'list':'','count':''}
	listall_reply=[]
	i=0
	if alist:
		for list in alist:
			reply_id=list[5]
			accountr=list[0]
			company_id=list[4]
			tocompany_id=list[6]
			nicknamer=getusername(company_id)
			tonickname=getusername(tocompany_id)
			titler=list[1]
			contentr=list[2]
			contentr=replacetel(contentr)
			contentr=replaceurl(contentr)
			gmt_createdr=formattime(list[3],0)
			i+=1
			list={'reply_id':reply_id,'title':titler,'nickname':nicknamer,'content':contentr,'posttime':gmt_createdr,'company_id':company_id,'tonickname':tonickname,'tocompany_id':tocompany_id,'i':i}
			listall_reply.append(list)
	listall['list']=listall_reply
	if i>10:
		listall['count']=1
	else:
		listall['count']=None
	return listall
#---回复列表
def replylist(postid,frompageCount,limitNum):
	sql="select account,title,content,gmt_created,company_id,id from bbs_post_reply where bbs_post_id=%s and is_del='0' and check_status in ('1','2') and bbs_post_reply_id=0 order by gmt_created desc limit %s,%s"
	#cursor.execute(sql,[postid,frompageCount,limitNum])
	#alist = cursor.fetchall()
	alist=dbc.fetchalldb(sql,[postid,frompageCount,limitNum])
	listall_reply=[]
	if alist:
		
		i=0
		for list in alist:
			reply_id=list[5]
			accountr=list[0]
			company_id=list[4]
			nicknamer=getusername(company_id)
			titler=list[1]
			contentr=list[2]
			contentr=replacetel(contentr)
			contentr=replaceurl(contentr)
			gmt_createdr=formattime(list[3],0)
			relist=replyreplylist(reply_id,0,10)
			i+=1
			list={'reply_id':reply_id,'title':titler,'nickname':nicknamer,'content':contentr,'posttime':gmt_createdr,'replylist':relist,'i':frompageCount+i,'post_id':postid,'company_id':company_id}
			listall_reply.append(list)
	return listall_reply
#---获得未读互助
def getmessgecount(company_id):
	sql1='select count(0) from bbs_post as a right outer join bbs_post_reply as b on a.id=b.bbs_post_id where (a.company_id=%s or b.tocompany_id=%s) and  not exists(select bbs_post_id from bbs_post_viewed where is_viewed=1 and company_id=%s and bbs_post_id=a.id)'
	#cursor.execute(sql1,[company_id,company_id,company_id])
	#result1=cursor.fetchone()
	result1=dbc.fetchonedb(sql1,[company_id,company_id,company_id])
	if result1:
		count=result1
	else:
		count=0
	return count
#----更新互助为未读状态
def updatepostviewed(company_id,bbs_post_id):
	if company_id:
		sql="update bbs_post_viewed set is_viewed=0 where company_id=%s and bbs_post_id=%s"
		#cursor.execute(sql,[company_id,bbs_post_id])
		#conn.commit()
		dbc.updatetodb(sql,[company_id,bbs_post_id])
		
def getpostviewed(company_id,bbs_post_id):
	if company_id:
		sql="select id from bbs_post_viewed where company_id=%s and bbs_post_id=%s and is_viewed=1"
		#cursor.execute(sql,[company_id,bbs_post_id])
		#resultlist=cursor.fetchone()
		resultlist=dbc.fetchonedb(sql,[company_id,bbs_post_id])
		if resultlist:
			return None
		else:
			return "1"
#----是否要弹窗
def getopenfloat(company_id):
	if company_id:
		invitecount=0
		sql="select guanzhu from bbs_user_profiler where company_id=%s"
		#cursor.execute(sql,[company_id])
		#returnlist=cursor.fetchone()
		returnlist=dbc.fetchonedb(sql,[company_id])
		if returnlist:
			guanzhu=returnlist[0]
			if (guanzhu):
				if (guanzhu!=""):
					sql="select count(0) from bbs_post_invite where guanzhu_id in (%s) and not exists(select bbs_post_id from bbs_post_viewed where bbs_post_id=bbs_post_invite.bbs_post_id and company_id=%s and is_viewed=1)"
					#cursor.execute(sql,[guanzhu,company_id])
					#returnlist=cursor.fetchone()
					returnlist=dbc.fetchonedb(sql,[guanzhu,company_id])
					if returnlist:
						invitecount=returnlist
		if (invitecount>0):
			return '1'
		sql="select id from bbs_post_viewed where company_id=%s and bbs_post_id=0 and is_viewed=0 and TIMESTAMPDIFF(MINUTE,gmt_created,now())<5"
		#cursor.execute(sql,[company_id])
		#resultlist=cursor.fetchone()
		resultlist=dbc.fetchonedb(sql,[company_id])
		if resultlist:
			return '1'
		else:
			return None
#----更新弹窗
def updateopenfloat(company_id,viewed):
	sql="select id from bbs_post_viewed where company_id=%s and bbs_post_id=0"
	#cursor.execute(sql,[company_id])
	#resultlist=cursor.fetchone()
	resultlist=dbc.fetchonedb(sql,[company_id])
	gmt_created=datetime.datetime.now()
	if resultlist:
		sqlu="update bbs_post_viewed set is_viewed=%s,gmt_created=%s where company_id=%s and bbs_post_id=0"
		#cursor.execute(sqlu,[viewed,gmt_created,company_id])
		#conn.commit()
		dbc.updatetodb(sqlu,[viewed,gmt_created,company_id])
	else:
		sqlu="insert into bbs_post_viewed(company_id,bbs_post_id,is_viewed,gmt_created) values(%s,%s,%s,%s)"
		#cursor.execute(sqlu,[company_id,0,viewed,gmt_created])
		#conn.commit()
		dbc.updatetodb(sqlu,[company_id,0,viewed,gmt_created])
#互助消息中心
def getmessgelist(company_id,frompageCount,limitNum):
	mycompany_id=company_id
	sql1='select count(0) from bbs_post as a right outer join bbs_post_reply as b on a.id=b.bbs_post_id where (a.company_id=%s or b.tocompany_id=%s)'
	#cursor.execute(sql1,[company_id,company_id])
	#result1=cursor.fetchone()
	result1=dbc.fetchnumberdb(sql1,[company_id,company_id])
	if result1:
		count=result1
	else:
		count=0
	sql='select b.id,b.content,b.gmt_created,b.company_id,a.title,a.id,b.tocompany_id,a.reply_time from bbs_post as a right outer join bbs_post_reply as b on a.id=b.bbs_post_id where (a.company_id=%s or b.tocompany_id=%s) order by a.reply_time desc limit %s,%s'
	#cursor.execute(sql,[company_id,company_id,frompageCount,limitNum])
	#resultlist=cursor.fetchall()
	resultlist=dbc.fetchalldb(sql,[company_id,company_id,frompageCount,limitNum])
	listall=[]
	if resultlist:
		for result in resultlist:
			company_id=result[3]
			post_id=result[5]
			reply_time=result[7]
			nickname=getusername(company_id)
			postviewed=getpostviewed(mycompany_id,post_id)
			list={'id':result[0],'title':result[1],'gmt_created':formattime(result[2],2),'nickname':nickname,'post_title':result[4],'company_id':company_id,'post_id':post_id,'postviewed':postviewed,'reply_time':reply_time}
			listall.append(list)
	return {'list':listall,'count':count}
#我的回复
def getmyreply(company_id,frompageCount,limitNum):
	sql1='select count(0) from bbs_post as a right outer join bbs_post_reply as b on a.id=b.bbs_post_id where (b.company_id=%s)'
	#cursor.execute(sql1,[company_id])
	#result1=cursor.fetchone()
	result1=dbc.fetchnumberdb(sql1,[company_id])
	if result1:
		count=result1
	else:
		count=0
	sql='select b.id,b.content,b.gmt_created,a.company_id,a.title,a.reply_count,a.id from bbs_post as a right outer join bbs_post_reply as b on a.id=b.bbs_post_id where (b.company_id=%s) order by b.gmt_created desc limit %s,%s'
	#cursor.execute(sql,[company_id,frompageCount,limitNum])
	#resultlist=cursor.fetchall()
	resultlist=dbc.fetchalldb(sql,[company_id,frompageCount,limitNum])
	listall=[]
	if resultlist:
		for result in resultlist:
			company_id=result[3]
			nickname=getusername(company_id)
			if nickname==None:
				nickname="ZZ91管理员"
			reply_count=0
			if result[5]:
				reply_count=result[5]
			list={'id':result[0],'post_id':result[6],'content':result[1],'gmt_created':formattime(result[2],2),'nickname':nickname,'post_title':result[4],'reply_count':reply_count}
			listall.append(list)
	return {'list':listall,'count':count}
#----获得互助帖子标题
def getbbspost_title(post_id):
	sql="select title from bbs_post where id=%s"
	#cursor.execute(sql,[post_id])
	#returnlist=cursor.fetchone()
	returnlist=dbc.fetchonedb(sql,[post_id])
	if returnlist:
		return returnlist[0]
#---邀请问答数量
def getbbs_invitecount(company_id):
	sql="select guanzhu from bbs_user_profiler where company_id=%s"
	#cursor.execute(sql,[company_id])
	#returnlist=cursor.fetchone()
	returnlist=dbc.fetchonedb(sql,[company_id])
	if returnlist:
		guanzhu=returnlist[0]
	if (guanzhu and guanzhu!=""):
		sql="select count(0) from bbs_post_invite where guanzhu_id in (%s) and not exists(select post_id from bbs_invite where post_id=bbs_post_invite.bbs_post_id and company_id=%s and answercheck in (1,2,3))"
		#cursor.execute(sql,[guanzhu,company_id])
		#returnlist=cursor.fetchone()
		returnlist=dbc.fetchnumberdb(sql,[guanzhu,company_id])
		if returnlist:
			return returnlist

#邀请问答
def getbbs_invite(company_id):
	bbsinvite=cache.get("database_mail"+str(company_id))
	if bbsinvite:
		return bbsinvite
	sql="select guanzhu from bbs_user_profiler where company_id=%s"
	#cursor.execute(sql,[company_id])
	#returnlist=cursor.fetchone()
	returnlist=dbc.fetchonedb(sql,[company_id])
	if returnlist:
		guanzhu=returnlist[0]
	else:
		guanzhu=None
	if (guanzhu and guanzhu!=""):
		sql="select bbs_post_id,gmt_created from bbs_post_invite where guanzhu_id in (%s) and not exists(select post_id from bbs_invite where post_id=bbs_post_invite.bbs_post_id and company_id=%s and answercheck in (1,2,3))"
		#sql="select a.id,a.title,a.company_id,a.content,b.gmt_created from bbs_post as a left join bbs_post_invite as b on a.id=b.bbs_post_id where b.guanzhu_id in (%s) and  not exists(select post_id from bbs_invite where post_id=a.id and company_id=%s and answercheck=1 and is_del=1)"
		sql=sql+"  limit 0,10 "
		#cursor.execute(sql,[guanzhu,company_id])
		#returnlist=cursor.fetchall()
		returnlist=dbc.fetchalldb(sql,[guanzhu,company_id])
		listall=[]
		for list in returnlist:
			bbs_post_id=list[0]
			sqlb="select company_id,title,content from bbs_post where id=%s"
			#cursor.execute(sqlb,[bbs_post_id])
			#returnone=cursor.fetchone()
			returnone=dbc.fetchonedb(sqlb,[bbs_post_id])
			if returnone:
				ccompany_id=returnone[0]
				title=returnone[1]
				nickname=getusername(ccompany_id)
				if nickname==None:
					nickname="匿名"
				gmt_created=list[1]

				is_viewed=None
				sqlb="select is_viewed,answercheck,id from bbs_invite where company_id=%s and post_id=%s and answercheck in (0,1)"
				#cursor.execute(sqlb,[company_id,bbs_post_id])
				#returnone=cursor.fetchone()
				returnone=dbc.fetchonedb(sqlb,[company_id,bbs_post_id])
				if returnone:
					is_viewed=returnone[0]
					answercheck=returnone[1]
					pid=returnone[2]
					if answercheck==2:
						is_viewed=2
				else:
					pid=0
				
				is_viewed=getpostviewed(company_id,bbs_post_id)
	
				if is_viewed=="0":
					is_viewed=None
				
				
				ll={'id':pid,'post_id':bbs_post_id,'title':title,'company_id':company_id,'nickname':nickname,'gmt_created':formattime(gmt_created,2),'is_viewed':is_viewed}
				listall.append(ll)
		cache.set("database_mail"+str(company_id),listall,60)
		return listall
def getproducstcategorylist(code):
	codelen=len(code)
	productscalist=cache.get("getproducstcategorylist"+str(code))
	if productscalist:
		return productscalist
	sql="select label,code from category_products where left(code,"+str(codelen)+")=%s and length(code)="+str(codelen+4)+" order by sort asc"
	#cursor.execute(sql,code)
	#catelist=cursor.fetchall()
	catelist=dbc.fetchalldb(sql,code)
	listall=[]
	for b in catelist:
		list={'code':b[1],'label':b[0],'sql':sql}
		listall.append(list)
	cache.set("getproducstcategorylist"+str(code),listall,60)
	return listall
#相关供求类别
def getcategorylist(kname='',limitcount=''):
	port = spconfig['port']
	cl = SphinxClient()
	cl.SetServer ( spconfig['serverid'], port )
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
#关键字排名
def keywordsTop(keywords):
	keytop=cache.get("mobile_keywordstop"+getjiami(keywords))
	if keytop:
		return keytop
	if keywords:
		sql="select product_id from products_keywords_rank where name=%s and start_time<'"+str(date.today()+timedelta(days=1))+"' and end_time>'"+str(date.today())+"' and is_checked=1 and type in ('10431004','手机站关键字排名') and not exists(select id from products where id=products_keywords_rank.product_id and is_pause=1) order by start_time asc"
		results=dbc.fetchalldb(sql,[keywords])
		cache.set("mobile_keywordstop"+getjiami(keywords),results,60*60)
		return results
	else:
		return None
def keywords_fix(keywords):
	keyfix=cache.get("mobile_keywordsfix"+getjiami(keywords))
	if keyfix:
		return keyfix
	sql="select product_id from products_keywords_fix where keywords=%s and start_time<'"+str(date.today()+timedelta(days=1))+"' and end_time>'"+str(date.today())+"' and is_checked=1"
	#cursor.execute(sql,keywords)
	#results = cursor.fetchall()
	results=dbc.fetchalldb(sql,keywords)
	cache.set("mobile_keywordsfix"+str(keywords),results,60*60)
	return results

#------最新报价信息
def getindexpricelist(kname="",assist_type_id="",limitcount="",searchname="",titlelen=""):
	if (titlelen=="" or titlelen==None):
		titlelen=100
	price=spconfig['name']['price']['name']
	serverid=spconfig['name']['price']['serverid']
	port=spconfig['name']['price']['port']
	cl = SphinxClient()
	cl.SetServer ( serverid, port )
	cl.SetMatchMode ( SPH_MATCH_BOOLEAN )
	cl.SetSortMode( SPH_SORT_EXTENDED,"gmt_order desc" )
	cl.SetLimits (0,limitcount,limitcount)
	if(assist_type_id!=None and assist_type_id!=""):
		cl.SetFilter('assist_type_id',[assist_type_id])
	if (kname):
		res = cl.Query ('@(title,tags) '+kname,price)
	else:
		res = cl.Query ('',price)
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
	company_price=spconfig['name']['company_price']['name']
	serverid=spconfig['name']['company_price']['serverid']
	port=spconfig['name']['company_price']['port']
	cl = SphinxClient()
	cl.SetServer ( serverid, port )
	cl.SetMatchMode ( SPH_MATCH_BOOLEAN )
	cl.SetSortMode( SPH_SORT_EXTENDED,"refresh_time desc" )
	cl.SetLimits (0,limitcount,limitcount)
	if (kname):
		res = cl.Query ('@(title,label1,label2,label3,area1,area2,area3) '+kname,company_price)
	else:
		res = cl.Query ('',company_price)
	if res:
		if res.has_key('matches'):
			tagslist=res['matches']
			listall_baojia=[]
			for match in tagslist:
				id=match['id']
				attrs=match['attrs']
				title=subString(attrs['ptitle'],titlelen)
				title=title.replace("\\","-")
				gmt_time=attrs['prefresh_time']
				min_price=attrs['min_price']
				max_price=attrs['max_price']
				price_unit=attrs['price_unit']
				list1={'title':title,'id':id,'gmt_time':gmt_time,'min_price':min_price,'max_price':max_price,'price_unit':price_unit,'fulltitle':attrs['ptitle'],'url':'http://jiage.zz91.com/cdetail/'+str(id)+'.html'}
				listall_baojia.append(list1)
			listcount_baojia=res['total_found']
			return listall_baojia
#最新互助信息
def getindexbbslist(kname='',limitcount='',bbs_post_category_id=''):
	port = spconfig['port']
	cl = SphinxClient()
	cl.SetServer ( spconfig['serverid'], port )
	cl.SetMatchMode ( SPH_MATCH_BOOLEAN )
	cl.SetSortMode( SPH_SORT_EXTENDED,"reply_time desc" )
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
def getbbslist(kname,frompageCount,limitNum,category_id='',fromtime='',endtime='',datetype='',htype='',bbs_post_assist_id=''):
	port = spconfig['port']
	cl = SphinxClient()
	cl.SetServer ( spconfig['serverid'], port )
	cl.SetMatchMode ( SPH_MATCH_BOOLEAN )
	cl.SetFilter('is_del',[0])
	cl.SetFilter('check_status',[1,2],False)
	if (category_id):
		cl.SetFilter('bbs_post_category_id',[int(category_id)])
	if bbs_post_assist_id:
		cl.SetFilter('bbs_post_assist_id',[int(bbs_post_assist_id)])
	#if fromtime and endtime:
		#cl.SetFilterRange('reply_time',fromtime,endtime)
	#if (datetype==1):
		#cl.SetSortMode( SPH_SORT_EXTENDED,"post_time desc,reply_time desc" )
	#if (datetype in (2,3)):
		#cl.SetSortMode( SPH_SORT_EXTENDED,"reply_count desc" )
	
	
	if htype:
		if (htype=="hot"):
			cl.SetSortMode( SPH_SORT_EXTENDED,"reply_count desc,reply_time desc" )
		if (htype=="new"):
			cl.SetSortMode( SPH_SORT_EXTENDED,"post_time desc" )
	else:
		cl.SetSortMode( SPH_SORT_EXTENDED,"reply_time desc,post_time desc" )
	
	cl.SetLimits (frompageCount,limitNum,20000)
	if (kname):
		res = cl.Query ('@(title,tags) '+kname,'huzhu')
	else:
		res = cl.Query ('','huzhu')
	if res:
#		return res
		if res.has_key('matches'):
			tagslist=res['matches']
			listall_news=[]
			for match in tagslist:
				id=match['id']
				bbscontent=cache.get("bbscontent"+str(id))
				bbscontent=None
				if (bbscontent==None):
					sql="select content,account,company_id,reply_time from bbs_post where id=%s"
					#cursor.execute(sql,id)
					#alist = cursor.fetchone()
					alist=dbc.fetchonedb(sql,id)
					if alist:
						havepic=havepicflag(alist[0])
						content=subString(filter_tags(alist[0]),50)
						
						username=getusername(alist[2])
						if alist[3]:
							reply_time=formattime(alist[3],0)
						else:
							reply_time=""
					else:
						content=""
						havepic=0
						username=""
						reply_time=""
					attrs=match['attrs']
					title=attrs['ptitle']
					if (content!=""):
						title=content
					gmt_time=attrs['ppost_time']
					
					replycount=gethuzhureplaycout(id)
					bbscontent={'title':title,'id':id,'gmt_time':gmt_time,'content':content,'nickname':username,'replycount':replycount,'havepic':havepic,'reply_time':reply_time}
					cache.set("bbscontent"+str(id),bbscontent,60)
				
				listall_news.append(bbscontent)
			listcount_news=res['total_found']
			return {'list':listall_news,'count':listcount_news}
#最新互助信息 翻页
def getbbsreplylist(kname,frompageCount,limitNum,bbs_post_id):
	port = spconfig['port']
	cl = SphinxClient()
	cl.SetServer ( spconfig['serverid'], port )
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
				sql="select content,account,gmt_created,company_id from bbs_post_reply where id=%s"
				#cursor.execute(sql,id)
				#alist = cursor.fetchone()
				alist=dbc.fetchone(sql,id)
				if alist:
					content=subString(filter_tags(alist[0]),50)
					username=getusername(alist[3])
					gmt_time=alist[2].strftime( '%-Y-%-m-%-d %-H:%-M:%-S')
				attrs=match['attrs']
				title=attrs['ptitle']
				list1={'lou':lou,'title':title,'id':id,'gmt_time':gmt_time,'content':content,'nickname':username}
				lou=lou+1
				listall_news.append(list1)
			listcount_news=res['total_found']
			return {'list':listall_news,'count':listcount_news}
#报价列表 翻页
def getpricelist(keywords="",frompageCount="",limitNum="",category_id="",allnum="",assist_type_id=""):
	price=spconfig['name']['price']['name']
	serverid=spconfig['name']['price']['serverid']
	port=spconfig['name']['price']['port']
	cl = SphinxClient()
	cl.SetServer ( serverid, port )
	cl.SetMatchMode ( SPH_MATCH_BOOLEAN )
	if (category_id):
		cl.SetFilter('type_id',category_id)
	if (assist_type_id):
		cl.SetFilter('assist_type_id',[assist_type_id])
	cl.SetSortMode( SPH_SORT_EXTENDED,"gmt_time desc" )
	cl.SetLimits (frompageCount,limitNum,allnum)
	if (keywords):
		res = cl.Query ('@(title,tags) '+keywords,price)
	else:
		res = cl.Query ('',price)
	if res:
		if res.has_key('matches'):
			tagslist=res['matches']
			listall_news=[]
			icout=0
			for match in tagslist:
				id=match['id']
				icout+=1
				pricecontent=cache.get("pricecontent"+str(id))
				if (pricecontent==None):
					sql="select content,tags from price where id=%s and is_checked=1"
					#cursor.execute(sql,id)
					#alist = cursor.fetchone()
					alist=dbc.fetchonedb(sql,id)
					content=""
					tags=""
					if alist:
						content=subString(filter_tags(alist[0]),50)
						tags=alist[1]
					attrs=match['attrs']
					title=attrs['ptitle']
					gmt_time=attrs['gmt_time']
					list1={'title':title,'id':id,'gmt_time':gmt_time,'content':content,'tags':tags}
					pricecontent=list1
					cache.set("pricecontent"+str(id),pricecontent,60*60)
				
				listall_news.append(pricecontent)
			listcount_news=res['total_found']
			return {'list':listall_news,'count':listcount_news}

#获取新闻栏目名称(一期)
def get_typename(id):
	sql='select typename from dede_arctype where id=%s'
	#cursor_news.execute(sql,[id])
	#result=cursor_news.fetchone()
	result=dbn.fetchonedb(sql,[id])
	if result:
		return result[0]
#获得新闻栏目id列表
def getcolumnid():
	sql='select id,typename,keywords from dede_arctype where reid=184 order by sortrank limit 0,8'
	#cursor_news.execute(sql)
	#resultlist=cursor_news.fetchall()
	resultlist=dbn.fetchalldb(sql)
	if resultlist:
		listall=[]
		for result in resultlist:
			listall.append(result[0])
		return listall
#获取新闻栏目(一期)
def getnewscolumn():
	sql='select id,typename,keywords from dede_arctype where reid=184 and ishidden=0 order by sortrank limit 0,8'
	#cursor_news.execute(sql)
	#resultlist=cursor_news.fetchall()
	resultlist=dbn.fetchalldb(sql)
	if resultlist:
		listall=[]
		numb=0
		for result in resultlist:
			numb=numb+1
			id=result[0]
			typename=result[1]
			url=result[2]
			list={'typeid':id,'typename':typename,'url':url,'numb':numb}
			listall.append(list)
		return listall
def getnewscolumnid(pinyin):
	if pinyin:
		sql="select id from dede_arctype where keywords=%s"
		resultlist=dbn.fetchonedb(sql,[pinyin])
		if resultlist:
			return resultlist[0]
def getnewscolumnpinyin(id):
	if id:
		sql="select keywords from dede_arctype where id=%s"
		resultlist=dbn.fetchonedb(sql,[id])
		if resultlist:
			return resultlist[0]
#日期格式转换(一期)
def timestamp_datetime2(value):
    format = '%m-%d'
    value = time.localtime(value)
    dt = time.strftime(format, value)
    return dt

#----新闻列表 翻页
def getnewslist(keywords="",frompageCount="",limitNum="",typeid="",allnum="",typeid2="",contentflag="",cursornews=""):
	port = spconfig['port']
	cl = SphinxClient()
	
	news=spconfig['name']['news']['name']
	serverid=spconfig['name']['news']['serverid']
	port=spconfig['name']['news']['port']
	cl.SetServer ( serverid, port )
	cl.SetMatchMode ( SPH_MATCH_BOOLEAN )
	if (typeid and typeid!=[0]):
		cl.SetFilter('typeid',typeid)
	if (typeid2):
		cl.SetFilter('typeid2',[typeid2])
	cl.SetSortMode( SPH_SORT_EXTENDED,"id desc" )
	if (allnum):
		cl.SetLimits (frompageCount,limitNum,allnum)
	else:
		cl.SetLimits (frompageCount,limitNum)
	if (keywords):
		if "p" == keywords:
			res = cl.Query ('@(flag) '+keywords,'news')
		else:
			res = cl.Query ('@(title,keywords) '+keywords,'news')
	else:
		res = cl.Query ('','news')
	listall_news=[]
	listcount_news=0
	if res:
		if res.has_key('matches'):
			tagslist=res['matches']
			for match in tagslist:
				id=match['id']
				newsurl=get_newstype(id)
				attrs=match['attrs']
				weburl="http://news.zz91.com"
				if newsurl:
					if newsurl["url2"]:
						weburl+="/"+newsurl["url2"]
					weburl+="/"+newsurl["url"]+"/newsdetail1"+str(id)+".htm"
				mobileweburl="http://m.zz91.com/news/newsdetail"+str(id)+".htm?type=news"
				title=filter_tags(attrs['ptitle'])
				title10=subString(title.decode('utf-8'),80)
				pubdate=attrs['pubdate']
				pubdate2=timestamp_datetime2(pubdate)
				if (contentflag==None):
					content=getnewscontent(id)['content']
				else:
					content=""
				havepic=havepicflag(content)
				littlecontent=subString(filter_tags(content),60)
				littlecontent=littlecontent.replace('\n','').replace('\r','')
				littlecontent=littlecontent.replace('　','').rstrip()
				list1={'title':title,'title10':title10,'id':id,'pubdate':pubdate2,'littlecontent':littlecontent,'content':content,'havepic':havepic,'newsurl':newsurl,'weburl':weburl,'mobileweburl':mobileweburl}
				listall_news.append(list1)
			listcount_news=res['total_found']
	return {'list':listall_news,'count':listcount_news}
#最新图片新闻
def get_newsimgsone():
	#cursor_news = conn_news.cursor()
	sql="select id,title,pubdate from dede_archives where flag='p' order by pubdate desc limit 0,9"
	#cursor_news.execute(sql)
	#alist = cursor_news.fetchone()
	alist=dbn.fetchonedb(sql)
	list=None
	if alist:
		id=alist[0]
		title=alist[1]
		contentlist=getnewscontent(id)
		if contentlist:
			content=contentlist['content']
			result=get_img_url(content)
			mobileweburl="http://m.zz91.com/news/newsdetail"+str(id)+".htm?type=news"
			if result:
				imglll=result[0]
				if "uploads/media/img_news" in imglll:
					img_url="http://news.zz91.com"+imglll
				else:
					img_url=imglll
			else:
				img_url=""
			list={'id':id,'title':title,'picurl':img_url,'url':mobileweburl}
	return list

#新闻内容
def getnewscontent(id):
	newscontent=cache.get("mobile_newscontent"+str(id))
	newscontent=None
	if (newscontent==None):
		sqlt="select title,pubdate,click from dede_archives where id=%s"
		#cursor_news.execute(sqlt,[id])
		#alist = cursor_news.fetchone()
		alist=dbn.fetchonedb(sqlt,[id])
		title=""
		pubdate=""
		click=""
		if alist:
			title=alist[0]
			pubdate=timestamp_datetime(alist[1])
			click=alist[2]
		sql="select body from dede_addonarticle where aid=%s"
		#cursor_news.execute(sql,[id])
		#alist = cursor_news.fetchone()
		alist=dbn.fetchonedb(sql,[id])
		content=""
		if alist:
			content=alist[0]
			#content=getreplacepic(content)
			content=replacepic(content)
			
		
		newscontent={'title':title,'pubdate':pubdate,'content':content,'click':click}
		cache.set("mobile_newscontent"+str(id),newscontent,60*60)
	return newscontent
#----新闻加点击数
def newsclick_add(id):
    sql="update dede_archives set click=click+1 where id=%s"
    #cursor_news.execute(sql,[id])
    #conn_news.commit()
    dbn.updatetodb(sql,[id])
#----互助加点击数
def huzhuclick_add(id):
    sql="update bbs_post set visited_count=visited_count+1 where id=%s"
    dbc.updatetodb(sql,[id])
#----获取最终页当前新闻栏目(一期)
def get_newstype(id):
	sql='select typeid,typeid2 from dede_archives where id=%s'
	#cursor_news.execute(sql,[id])
	#result=cursor_news.fetchone()
	result=dbn.fetchonedb(sql,[id])
	if result:
		typeid=result[0]
		typeid2=result[1]
		sql2='select typename,keywords from dede_arctype where id=%s'
		#cursor_news.execute(sql2,[typeid])
		#result2=cursor_news.fetchone()
		result2=dbn.fetchonedb(sql2,[typeid])
		if result2:
			list={'typename':result2[0],'url':result2[1],'typeid':typeid,'typeid2':typeid2,'url2':''}
			if typeid2!='0':
				sql3='select keywords from dede_arctype where id=%s'
				#cursor_news.execute(sql3,[typeid2])
				#result3=cursor_news.fetchone()
				result3=dbn.fetchonedb(sql3,[typeid2])
				if result3:
					list['url2']=result3[0]
			return list
#----最终页相关阅读(4大类别)(一期)
def get_typenews(typeid,typeid2,cursor_news):
	sql="select id,title,click,description from dede_archives where typeid=%s and typeid2=%s order by pubdate desc limit 0,5"
	resultlist=dbn.fetchalldb(sql,[typeid,typeid2])
	listall=[]
	if resultlist:
		for result in resultlist:
			description=subString(filter_tags(result[3]),260)
			list={'id':result[0],'title':result[1],'click':result[2],'description':description}
			listall.append(list)
	return listall

#----新闻最终页上一篇下一篇(一期)
def getarticalup(id,typeid):
	sqlt="select id,title from dede_archives where typeid=%s and id>%s order by id limit 0,1"
	#cursor_news.execute(sqlt,[typeid,id])
	#resultu = cursor_news.fetchone()
	resultu=dbn.fetchonedb(sqlt,[typeid,id])
	if resultu:
		list={'id':resultu[0],'title':resultu[1]}
		return list
def getarticalnx(id,typeid):
	sqlt="select id,title from dede_archives where typeid=%s and id<%s order by id desc limit 0,1"
	#cursor_news.execute(sqlt,[typeid,id])
	#resultn = cursor_news.fetchone()
	resultn=dbn.fetchonedb(sqlt,[typeid,id])
	if resultn:
		list={'id':resultn[0],'title':resultn[1]}
		return list

#----新闻列表
def getindexnewslist(keywords="",limitNum="",typeid="",typeid2=""):
	cursor_news = conn_news.cursor()
	news=SPHINXCONFIG['name']['news']['name']
	serverid=SPHINXCONFIG['name']['news']['serverid']
	port=SPHINXCONFIG['name']['news']['port']
	cl = SphinxClient()
	cl.SetServer (serverid, port )
	cl.SetMatchMode ( SPH_MATCH_BOOLEAN )
	if (typeid):
		cl.SetFilter('typeid',[typeid])
	if (typeid2):
		cl.SetFilter('typeid2',[typeid2])
	cl.SetSortMode( SPH_SORT_EXTENDED,"pubdate desc" )
	cl.SetLimits (0,limitNum,limitNum)
	if (keywords):
		res = cl.Query ('@(title) '+keywords,news)
	else:
		res = cl.Query ('',news)
	listall_news=[]
	if res:
		if res.has_key('matches'):
			tagslist=res['matches']
			for match in tagslist:
				id=match['id']
				attrs=match['attrs']
				title=attrs['ptitle']
				pubdate=attrs['pubdate']
				littlecontent=subString(filter_tags(getnewscontent(id)['content']),60)##去掉了cursor_news
				list1={'title':title,'id':id,'pubdate':pubdate,'littlecontent':littlecontent}
				listall_news.append(list1)
	cursor_news.close()
	return listall_news

#----公司信息列表 翻页
def getcompanylist(kname,frompageCount,limitNum,ldb=''):
	port = spconfig['port']
	cl = SphinxClient()
	cl.SetServer ( spconfig['serverid'], port )
	cl.SetMatchMode ( SPH_MATCH_BOOLEAN )
	if ldb!='' and ldb:
		cl.SetFilter('apply_status',[1])
	cl.SetSortMode( SPH_SORT_EXTENDED,"mobile_order desc,gmt_start desc" )
	cl.SetLimits (frompageCount,limitNum,200000)
	if (kname):
		res = cl.Query ('@(name,business,address,sale_details,buy_details,tags,area_name,area_province) '+kname,'company')
	else:
		res = cl.Query ('','company')
	listcount_comp=0
	listall_comp=[]
	if res:
		if res.has_key('matches'):
			tagslist=res['matches']
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
				pbusiness=subString(filter_tags(attrs['pbusiness']),150)
				parea_province=attrs['parea_province']
				ldbphone=getldbphone(id)
				list1={'id':id,'compname':compname,'business':pbusiness,'area_province':parea_province,'membership':membership,'viptype':viptype,'ldbphone':ldbphone}
				listall_comp.append(list1)
			listcount_comp=res['total_found']
	return {'list':listall_comp,'count':listcount_comp}
#--发布者 回复者
def getusername(company_id):
	nickname=None
	sqlu="select nickname,account from bbs_user_profiler where company_id=%s"
	#cursor.execute(sqlu,[company_id])
	#ulist = cursor.fetchone()
	ulist=dbc.fetchonedb(sqlu,[company_id])
	if ulist:
		nickname= ulist[0]
		account=ulist[1]
		if (nickname==None or nickname==account):
			sqlu="select contact from company_account where company_id=%s"
			#cursor.execute(sqlu,[company_id])
			#ulist = cursor.fetchone()
			ulist=dbc.fetchonedb(sqlu,[company_id])
			if ulist:
				nickname=ulist[0]
	else:
		sqlu="select contact from company_account where company_id=%s"
		#cursor.execute(sqlu,[company_id])
		#ulist = cursor.fetchone()
		ulist=dbc.fetchonedb(sqlu,[company_id])
		if ulist:
			nickname=ulist[0]
	return nickname
#--回复数
def gethuzhureplaycout(bbs_post_id):
	sqlr="select count(0) from bbs_post_reply where bbs_post_id=%s and is_del='0' and check_status in ('1','2')"
	#cursor.execute(sqlr,str(bbs_post_id))
	#rlist = cursor.fetchone()
	rlist=dbc.fetchnumberdb(sqlr,str(bbs_post_id))
	if rlist:
		return rlist
#--我的回复数
def getmyhuzhureplaycout(account):
	sqlr="select count(0) from bbs_post_reply where account=%s and check_status in ('1','2')"
	#cursor.execute(sqlr,str(account))
	#rlist = cursor.fetchone()
	rlist=dbc.fetchnumberdb(sqlr,str(account))
	if rlist:
		return rlist
#--我的未读回复数
def getmyhuzhureplaycoutno(account):
	sqlr="select count(0) from bbs_post_reply where account=%s and check_status=0"
	#cursor.execute(sqlr,str(account))
	#rlist = cursor.fetchone()
	rlist=dbc.fetchnumberdb(sqlr,str(account))
	if rlist:
		return rlist

#--价格分类
def getpricecatename(id):
	sql="select name from price_category where id=%s"
	#cursor.execute(sql,[id])
	#alist = cursor.fetchone()
	alist=dbc.fetchonedb(sql,[id])
	if alist:
		return alist[0]
def getcate(categoryId):
	sql="select name,id from price_category where parent_id=%s and showflag=1"
	#cursor.execute(sql,str(categoryId))
	#alist = cursor.fetchall()
	alist=dbc.fetchalldb(sql,str(categoryId))
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
	return catestr
#--获得帐号
def getcompanyaccount(company_id):
	sql="select account from  company_account where company_id=%s"
	#cursor.execute(sql,[company_id])
	#result=cursor.fetchone()
	result=dbc.fetchonedb(sql,[company_id])
	if (result):
		return result[0]

#--获得公司id
def getcompanyid(account):
	sql="select company_id from  company_account where account=%s"
	#cursor.execute(sql,[account])
	#result=cursor.fetchone()
	result=dbc.fetchonedb(sql,[account])
	if result:
		return result[0]
#----获得手机号码
def getcompanymobile(account):
	sql="select mobile from  weixin_account where account=%s"
	#cursor.execute(sql,[account])
	#result=cursor.fetchone()
	result=dbc.fetchonedb(sql,[account])
	if (result):
		return result[0]
	sql="select mobile from  company_account where account=%s"
	#cursor.execute(sql,[account])
	#result=cursor.fetchone()
	result=dbc.fetchonedb(sql,[account])
	if (result):
		return result[0]
#---------------------------------
#--获得互助关注行业
def gethuzhuguanzhu(company_id):
	sql='select guanzhu from bbs_user_profiler where company_id=%s'
	#cursor.execute(sql,[company_id])
	#result=cursor.fetchone()
	result=dbc.fetchonedb(sql,[company_id])
	if result:
		return result[0]
	else:
		return ""
def addmyzhuzhuguanzhu(myguanzhu,company_id,account):
	sqla="select id from bbs_user_profiler where company_id=%s"
	#cursor.execute(sqla,[company_id])
	#result=cursor.fetchone()
	result=dbc.fetchonedb(sqla,[company_id])
	tt=""
	if myguanzhu:
		for t in myguanzhu:
			tt=tt+t+","
		myguanzhu=tt[:-1]
	else:
		myguanzhu=""
	gmt_created=gmt_modified=datetime.datetime.now()
	if result:
		sql='update bbs_user_profiler set guanzhu=%s,gmt_modified=%s where company_id=%s'
		#cursor.execute(sql,[str(myguanzhu),gmt_modified,company_id])
		#conn.commit()
		dbc.updatetodb(sql,[str(myguanzhu),gmt_modified,company_id])
	else:
		value=[company_id,account,str(myguanzhu),gmt_created,gmt_modified]
		sql='insert into bbs_user_profiler (company_id,account,guanzhu,gmt_created,gmt_modified) values(%s,%s,%s,%s,%s)'
		#cursor.execute(sql,value)
		#conn.commit()
		dbc.updatetodb(sql,value)
#----获得昵称
def getcompanynickname(company_id):
	sql='select nickname from bbs_user_profiler where company_id=%s'
	#cursor.execute(sql,[company_id])
	#result=cursor.fetchone()
	result=dbc.fetchonedb(sql,[company_id])
	if result:
		return result[0]
#----添加昵称
def addcompanynickname(nickname,company_id,account):
	sqla="select id from bbs_user_profiler where company_id=%s"
	#cursor.execute(sqla,[company_id])
	#result=cursor.fetchone()
	result=dbc.fetchonedb(sqla,[company_id])
	gmt_created=gmt_modified=datetime.datetime.now()
	if result:
		sql='update bbs_user_profiler set nickname=%s,gmt_modified=%s where company_id=%s'
		#cursor.execute(sql,[nickname,gmt_modified,company_id])
		#conn.commit()
		dbc.updatetodb(sql,[nickname,gmt_modified,company_id])
	else:
		value=[company_id,account,nickname,gmt_created,gmt_modified]
		sql='insert into bbs_user_profiler (company_id,account,nickname,gmt_created,gmt_modified) values(%s,%s,%s,%s,%s)'
		#cursor.execute(sql,value)
		#conn.commit()
		dbc.updatetodb(sql,value)
		

#---微信
def parse_msg():
	recvmsg = request.raw_post_data
	root = ET.fromstring(recvmsg)
	msg = {}
	for child in root:
		msg[child.tag] = child.text
	return msg
#验证微信是否绑定
def weixinbinding(weixinid):
	sql="select target_account from oauth_access where open_id=%s and target_account<>'0'"
	#cursor.execute(sql,[weixinid]);
	#list=cursor.fetchone()
	list=dbc.fetchonedb(sql,[weixinid])
	if list:
		return list[0]
	else:
		return None
#绑定的客户自动登录
def weixinautologin(request,weixinid):
	if (weixinid and weixinid!=""):
		account=weixinbinding(weixinid)
		if account:
			company_id=getcompanyid(account)
			updatelogin(request,company_id)
			
			request.session.set_expiry(60*60*60)
			request.session['username']=account
			request.session['company_id']=company_id
			return 1
		else:
			return None
	else:
		return None
#更新登录数据
def updatelogin(request,company_id):
	gmt_modified=datetime.datetime.now()
	sqll="update company_account set gmt_last_login=%s where company_id=%s"
	#cursor.execute(sqll,[gmt_modified,company_id]);
	#conn.commit()
	#conn.commit()
	dbc.updatetodb(sqll,[gmt_modified,company_id])
	ip=getIPFromDJangoRequest(request)
	gmt_modifiedto=str(int(time.mktime(gmt_modified.timetuple())))+"000"
	try:
		payload={'appCode':'zz91','operator':company_id,'operation':'login','ip':ip,'time':gmt_modifiedto,'data':''}
		r= requests.post("http://apps1.zz91.com/zz91-log/log",data=payload)
		return r.content
	except:
		return None
#-----微信自动回复
def backxml(xmltype="",fromUserName="",toUserName="",title="",Description="",PicUrl="",Url="",ArticleCount="",titlelist=""):
	#图文回复(搜索)
	CreateTime=str(int(time.time()))
	reply_news = """<xml>
	<ToUserName><![CDATA["""+fromUserName+"""]]></ToUserName>
	<FromUserName><![CDATA["""+toUserName+"""]]></FromUserName>
	<CreateTime>"""+CreateTime+"""</CreateTime>
	<MsgType><![CDATA[news]]></MsgType>
	<ArticleCount>3</ArticleCount>
	<Articles>	
	<item>
	<Title><![CDATA[ZZ91手机网]]></Title> 
	<Description><![CDATA['']]></Description>
	<PicUrl><![CDATA[http://img1.zz91.com/ads/1364745600000/0ba7bf8d-8bb2-4add-a475-aa26e3103105.jpg]]></PicUrl>
	<Url><![CDATA[http://m.zz91.com]]></Url>
	</item>
	<item>
	<Title><![CDATA[点此查看相关"""+title+"""的行情报价]]></Title> 
	<Description><![CDATA['']]></Description>
	<PicUrl><![CDATA[picurl]]></PicUrl>
	<Url><![CDATA[http://m.zz91.com/price/?keywords="""+title+"""]]></Url>
	</item>
	<item>
	<Title><![CDATA[点此查看相关"""+title+"""的供求商机]]></Title> 
	<Description><![CDATA['']]></Description>
	<PicUrl><![CDATA[picurl]]></PicUrl>
	<Url><![CDATA[http://m.zz91.com/offerlist/?keywords="""+title+"""]]></Url>
	</item>
	
	</Articles>
	</xml>"""
	reply_tw = """<xml>
	<ToUserName><![CDATA["""+fromUserName+"""]]></ToUserName>
	<FromUserName><![CDATA["""+toUserName+"""]]></FromUserName>
	<CreateTime>"""+CreateTime+"""</CreateTime>
	<MsgType><![CDATA[news]]></MsgType>
	<ArticleCount>"""+str(ArticleCount)+"""</ArticleCount>
	<Articles>"""
	for list in titlelist:
		title=list['title']
		reply_tw=reply_tw+"""
		<item>
		<Title><![CDATA["""+list['title']+"""]]></Title> 
		<Description><![CDATA['"""+list['Description']+"""']]></Description>
		<PicUrl><![CDATA["""+list['PicUrl']+"""]]></PicUrl>
		<Url><![CDATA["""+list['Url']+"""]]></Url>
		</item>"""
	reply_tw=reply_tw+"""
	</Articles>
	</xml>"""
	#图文（生意管家）
	reply_myrc = """<xml>
	<ToUserName><![CDATA["""+fromUserName+"""]]></ToUserName>
	<FromUserName><![CDATA["""+toUserName+"""]]></FromUserName>
	<CreateTime>"""+CreateTime+"""</CreateTime>
	<MsgType><![CDATA[news]]></MsgType>
	<ArticleCount>3</ArticleCount>
	<Articles>	
	<item>
	<Title><![CDATA[ZZ91手机网]]></Title> 
	<Description><![CDATA['']]></Description>
	<PicUrl><![CDATA[http://img1.zz91.com/ads/1364745600000/0ba7bf8d-8bb2-4add-a475-aa26e3103105.jpg]]></PicUrl>
	<Url><![CDATA[http://m.zz91.com]]></Url>
	</item>
	<item>
	<Title><![CDATA[点此查看相关"""+title+"""的行情报价]]></Title> 
	<Description><![CDATA['']]></Description>
	<PicUrl><![CDATA[picurl]]></PicUrl>
	<Url><![CDATA[http://m.zz91.com/price/?keywords="""+title+"""]]></Url>
	</item>
	<item>
	<Title><![CDATA[点此查看相关"""+title+"""的供求商机]]></Title> 
	<Description><![CDATA['']]></Description>
	<PicUrl><![CDATA[picurl]]></PicUrl>
	<Url><![CDATA[http://m.zz91.com/offerlist/?keywords="""+title+"""]]></Url>
	</item>
	
	</Articles>
	</xml>"""
	
	#文本回复
	reply_text = """<xml>
	<ToUserName><![CDATA["""+fromUserName+"""]]></ToUserName>
	<FromUserName><![CDATA["""+toUserName+"""]]></FromUserName>
	<CreateTime>"""+CreateTime+"""</CreateTime>
	<MsgType><![CDATA[text]]></MsgType>
	<Content><![CDATA["""+title+"""]]></Content>
	<FuncFlag>0</FuncFlag>
	</xml>"""
	#链接跳转
	reply_link = """<xml>
	<ToUserName><![CDATA["""+fromUserName+"""]]></ToUserName>
	<FromUserName><![CDATA["""+toUserName+"""]]></FromUserName>
	<CreateTime>"""+CreateTime+"""</CreateTime>
	<MsgType><![CDATA[event]]></MsgType>
	<Event><![CDATA[VIEW]]></Event>
	<EventKey><![CDATA["""+Url+"""?weixinid="""+fromUserName+"""]]></EventKey>
	</xml>"""
	if (xmltype==1):
		return reply_news
	if (xmltype==3):
		return reply_tw
	if (xmltype==4):
		return reply_link
	else:
		return reply_text
#--------------------------------------------------end
#获得公司ID
def getcompany_id(cname,regtime):
	sql="select max(id) from company"
	#newcode=dbc.fetchonedb(sql,[str(cname)])
	newcode=dbc.fetchonedbmain(sql)
	if (newcode == None):
		return 0
	else:
		return newcode[0]
def getprofilerid(company_id):
	sql="select id from bbs_user_profiler where account=%s"
	#cursor.execute(sql,[company_id])
	#newcode=cursor.fetchone()
	newcode=dbc.fetchonedb(sql,[company_id])
	if (newcode == None):
		return '0'
	else:
		return newcode[0]

#获得公司名称
def getcompanyname(uname):
	sql="select company_id from company_account where account=%s"
	#cursor.execute(sql,[uname])
	#newcode=cursor.fetchone()
	newcode=dbc.fetchonedb(sql,[uname])
	if (newcode):
		company_id=newcode[0]
		sqlc="select name from company where id=%s"
		#cursor.execute(sqlc,[company_id])
		#clist=cursor.fetchone()
		clist=dbc.fetchonedb(sqlc,[company_id])
		if clist:
			return {'company_id':company_id,'companyname':clist[0]}

#公司供求信息 翻页
def getcompanyproductslist(kname,frompageCount,limitNum,company_id,pdt_type):
	port = spconfig['port']
	cl = SphinxClient()
	cl.SetServer ( spconfig['serverid'], port )
	cl.SetMatchMode ( SPH_MATCH_BOOLEAN )
	if (company_id):
		cl.SetFilter('company_id',[int(company_id)])
	if (pdt_type !='' and pdt_type!=None):
		cl.SetFilter('pdt_kind',[int(pdt_type)])
	cl.SetSortMode( SPH_SORT_EXTENDED,"refresh_time desc" )
	cl.SetLimits (frompageCount,limitNum,20000)
	if (kname):
		res = cl.Query ('@(title,label0,label1,label2,label3,label4,city,province,tags) '+kname,'offersearch_new,offersearch_new_vip')
	else:
		res = cl.Query ('','offersearch_new,offersearch_new_vip')
	listcount=0
	listcount=[]
	if res:
		if res.has_key('matches'):
			tagslist=res['matches']
			listall=[]
			for match in tagslist:
				id=match['id']
				list=getcompinfo(id,"",kname)
				listall.append(list)
			listcount=res['total_found']
	return {'list':listall,'count':listcount}
#索引供求列表页
def getsyproductslist(kname,frompageCount,limitNum,pinyin,allnum):
	listcount=0
	listall=[]
	port = spconfig['port']
	cl = SphinxClient()
	cl.SetServer ( spconfig['serverid'], port )
	cl.SetMatchMode ( SPH_MATCH_BOOLEAN )
	cl.SetSortMode( SPH_SORT_EXTENDED,"id desc" )
	cl.SetLimits (frompageCount,limitNum,allnum)
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
#索引公司列表页
def getsycompanylist(kname,frompageCount,limitNum,pinyin):
	port = spconfig['port']
	cl = SphinxClient()
	cl.SetServer ( spconfig['serverid'], port )
	cl.SetMatchMode ( SPH_MATCH_BOOLEAN )
	cl.SetSortMode( SPH_SORT_EXTENDED,"id desc" )
	cl.SetLimits (frompageCount,limitNum,200000)
	if (kname and kname!=""):
		res = cl.Query ('@(name,business,address,sale_details,buy_details,tags,area_name,area_province) '+kname,'company')
	else:
		if (pinyin):
			res = cl.Query ('@pinyin '+str(pinyin),'company')
		else:
			res = cl.Query ('','company')
	listall=[]
	listcount=0
	if res:
		if res.has_key('matches'):
			tagslist=res['matches']
			listall=[]
			for match in tagslist:
				id=match['id']
				attrs=match['attrs']
				compname=attrs['compname']
				list={'id':id,'compname':compname}
				listall.append(list)
			listcount=res['total_found']
	return {'list':listall,'count':listcount}
#索引标签库列表
def gettagslist(frompageCount,limitNum,pinyin):
	port = spconfig['port']
	cl = SphinxClient()
	cl.SetServer ( spconfig['serverid'], port )
	cl.SetMatchMode ( SPH_MATCH_BOOLEAN )
	cl.SetSortMode( SPH_SORT_EXTENDED,"id desc" )
	cl.SetLimits (frompageCount,limitNum,200000)
	if (pinyin):
		res = cl.Query ('@pinyin '+str(pinyin),'tagslist')
	else:
		res = cl.Query ('','tagslist')
	listall=[]
	listcount=0
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
	port = spconfig['port']
	cl = SphinxClient()
	cl.SetServer ( spconfig['serverid'], port )
	cl.SetMatchMode ( SPH_MATCH_BOOLEAN )
	cl.SetSortMode( SPH_SORT_EXTENDED," refresh_time desc" )
	cl.SetLimits (0,limitcount,limitcount)
	if (pdt_type!=None):
		cl.SetFilter('pdt_kind',[int(pdt_type)])
	if (kname==None):
		res = cl.Query ('','offersearch_new,offersearch_new_vip')
	else:
		res = cl.Query ('@(title,label0,label1,label2,label3,label4,city,province,tags) '+kname,'offersearch_new,offersearch_new_vip')
	listall_offerlist=[]
	if res:
		if res.has_key('matches'):
			itemlist=res['matches']
			for match in itemlist:
				pid=match['id']
				attrs=match['attrs']
				pdt_date=attrs['pdt_date']
				sql="select refresh_time from products where id="+str(pid)+""
				productlist=dbc.fetchonedb(sql)
				if productlist:
					pdt_date=productlist[0].strftime( '%-Y-%-m-%-d')
				title=subString(attrs['ptitle'],40)
				list={'id':pid,'title':title,'gmt_time':pdt_date,'fulltitle':attrs['ptitle']}
				listall_offerlist.append(list)
	return listall_offerlist
#获得供求信息
def getproductdetail(id):
	productsdetai=cache.get("mobile_productsdetail"+str(id))
	if productsdetai:
		return productsdetai
	sql="select company_id,title,details,location,provide_status,total_quantity,price_unit,quantity_unit,quantity,source"
	sql=sql+",specification,origin,impurity,color,useful,appearance,manufacture,min_price,max_price,tags,refresh_time,expire_time,products_type_code"
	sql=sql+" from products where id=%s"
	#cursor.execute(sql,str(id))
	#plist=cursor.fetchone()
	plist=dbc.fetchonedb(sql,str(id))
	if plist:
		company_id=plist[0]
		title=plist[1]
		details=plist[2]
		details=filter_tags(details)
		location=plist[3]
		if (location):
			if (location.strip()==''):
				location=None
		provide_status=plist[4]
		total_quantity=plist[5]
		
		quantity_unit=plist[7]
		quantity=plist[8]
		if plist[9]:
			source=plist[9].strip()
		else:
			source=""
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
		if (price==''):
			price=None
			
		tags=plist[19]
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
		sqlc="select name,business,regtime,address,introduction,membership_code from company where id=%s"
		#cursor.execute(sqlc,company_id)
		#clist=cursor.fetchone()
		clist=dbc.fetchonedb(sqlc,company_id)
		if clist:
			compname=clist[0]
			business=clist[1]
			regtime=clist[2]
			address=clist[3]
			introduction=clist[4]
			viptype=clist[5]
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
			#来电宝客户
			sqll="select id from crm_company_service where company_id="+str(company_id)+" and crm_service_code in(1007,1008,1009,1010) and apply_status=1 and DATEDIFF(CURDATE(),`gmt_end`)<=0"
			#cursor.execute(sqll)
			#ldbresult=cursor.fetchone()
			ldbresult=dbc.fetchonedb(sqll)
			if ldbresult:
				sqlg="select front_tel,tel from phone where company_id="+str(company_id)+" and expire_flag=0"
				#cursor.execute(sqlg)
				#phoneresult=cursor.fetchone()
				phoneresult=dbc.fetchonedb(sqlg)
				if phoneresult:
					arrviptype['ldb']={'ldbphone':phoneresult[0],'ldbtel':phoneresult[1]}
				else:
					arrviptype['ldb']=None
			else:
				arrviptype['ldb']=None
		sqlc="select contact,tel_country_code,tel_area_code,tel,mobile,fax_country_code,fax_area_code,fax,email"
		sqlc=sqlc+",sex,position,qq "
		sqlc=sqlc+"from company_account where company_id=%s"
		#cursor.execute(sqlc,company_id)
		#alist=cursor.fetchone()
		alist=dbc.fetchonedb(sqlc,company_id)
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
			if (mobile):
				mobile1=mobile[0:11]
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
		sql1="select pic_address from products_pic where product_id=%s and check_status=1"
		#cursor.execute(sql1,id)
		#productspic = cursor.fetchall()
		productspic=dbc.fetchalldb(sql1,id)
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
		list={'pdtid':id,'company_id':company_id,'title':title,'refresh_time':refresh_time,'expire_time':expire_time,'details':details,'location':location,'provide_status':provide_status,'total_quantity':total_quantity,'price':price,'price_unit':price_unit,'quantity_unit':quantity_unit,'quantity':quantity,'source':source,'specification':specification,'origin':origin,'impurity':impurity,'color':color,'useful':useful,'appearance':appearance,'manufacture':manufacture,'min_price':min_price,'max_price':max_price,'tags':tags,'compname':compname,'business':business,'regtime':regtime,'address':address,'introduction':introduction,'contact':contact,'tel_country_code':tel_country_code,'tel_area_code':tel_area_code,'tel':tel,'mobile':mobile,'mobile1':mobile1,'fax_country_code':fax_country_code,'fax_area_code':fax_area_code,'fax':fax,'email':email,'sex':sex,'position':position,'qq':qq,'piclist':piclist,'viptype':arrviptype,'products_type_code':products_type_code}
		cache.set("mobile_productsdetail"+str(id),list,60*10)
		return list
#公司名称和主营业务
def getppccompanyinfo(company_id):
	sqlc="select name,business from company where id=%s"
	#cursor.execute(sqlc,company_id)
	#clist=cursor.fetchone()
	clist=dbc.fetchonedb(sqlc,company_id)
	if clist:
		list={'companyname':clist[0],'business':clist[1]}
	return list
#----判断是否为再生通
def getiszstcompany(company_id):
	if company_id:
		sqll="select id from crm_company_service where company_id=%s and crm_service_code='1000' and apply_status=1 and DATEDIFF(CURDATE(),`gmt_end`)<=0"
		#cursor.execute(sqll,[company_id])
		#zstresult=cursor.fetchone()
		zstresult=dbc.fetchonedb(sqll,[company_id])
		if zstresult:
			return 1
		else:
			return None
	else:
		return None
#----公司详情
def getcompanydetail(company_id):
	companydetail=cache.get("mobile_companydetail"+str(company_id))
	if companydetail:
		return companydetail
	sqlc="select name,business,regtime,address,introduction,membership_code,domain_zz91 from company where id=%s"
	#cursor.execute(sqlc,company_id)
	#clist=cursor.fetchone()
	clist=dbc.fetchonedb(sqlc,company_id)
	if clist:
		compname=clist[0]
		business=clist[1]
		regtime=clist[2]
		address=clist[3]
		introduction=clist[4]
		viptype=clist[5]
		domain_zz91=clist[6]
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
		#来电宝客户
		sqll="select id from crm_company_service where company_id="+str(company_id)+" and crm_service_code in(1007,1008,1009,1010) and apply_status=1 and DATEDIFF(CURDATE(),`gmt_end`)<=0"
		#cursor.execute(sqll)
		#ldbresult=cursor.fetchone()
		ldbresult=dbc.fetchonedb(sqll)
		if ldbresult:
			sqlg="select front_tel,tel from phone where company_id="+str(company_id)+" and expire_flag=0"
			#cursor.execute(sqlg)
			#phoneresult=cursor.fetchone()
			phoneresult=dbc.fetchonedb(sqlg)
			if phoneresult:
				ldbtel=phoneresult[1]
				ldbtel=ldbtel.replace("-",",")
				arrviptype['ldb']={'ldbphone':phoneresult[0],'ldbtel':ldbtel}
			else:
				arrviptype['ldb']=None
		else:
			arrviptype['ldb']=None
	sqlc="select contact,tel_country_code,tel_area_code,tel,mobile,fax_country_code,fax_area_code,fax,email"
	sqlc=sqlc+",sex,position,qq "
	sqlc=sqlc+"from company_account where company_id=%s"
	#cursor.execute(sqlc,company_id)
	#alist=cursor.fetchone()
	alist=dbc.fetchonedb(sqlc,company_id)
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
		if (mobile):
			mobile1=mobile[0:11]
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
	list={'company_id':company_id,'name':compname,'business':business,'domain_zz91':domain_zz91,'regtime':regtime,'address':address,'introduction':introduction,'contact':contact,'tel_country_code':tel_country_code,'tel_area_code':tel_area_code,'tel':tel,'mobile':mobile,'mobile1':mobile1,'fax_country_code':fax_country_code,'fax_area_code':fax_area_code,'fax':fax,'email':email,'sex':sex,'position':position,'qq':qq,'viptype':arrviptype}
	cache.set("mobile_companydetail"+str(company_id),list,60*10)
	return list
#--------------------------------------------------------------------------------------------------------
def getleavewords(qid):
	sql="select title,content,send_time,sender_account,id,is_viewed from inquiry where id=%s"
	#cursor.execute(sql,qid)
	#alist=cursor.fetchone()
	alist=dbc.fetchonedb(sql,qid)
	list=None
	if alist:
		companyarray=getcompanyname(alist[3])
		list={'id':alist[4],'title':alist[0],'content':alist[1],'is_viewed':alist[5],'stime':formattime(alist[2],0),'companyarray':companyarray}
	return list
#----查看留言
def getupdatelookquestion(qid):
	sql="update inquiry set is_viewed=1 where id=%s"
	#cursor.execute(sql,[qid])
	#conn.commit()
	dbc.updatetodb(sql,[qid])
	
#----弹出留言提醒
def getopenquestioncount(account):
	sql="select count(0) from inquiry where receiver_account=%s and is_viewed=0"
	#cursor.execute(sql,[account])
	#alist=cursor.fetchone()
	alist=dbc.fetchnumberdb(sql,[account])
	if alist:
		return alist
#询盘留言列表 翻页
def getleavewordslist(frompageCount,limitNum,company_id,sendtype):
	port = spconfig['port']
	cl = SphinxClient()
	cl.SetServer ( spconfig['serverid'], port )
	cl.SetMatchMode ( SPH_MATCH_BOOLEAN )
	listall=[]
	listcount=0
	if (company_id):
		if sendtype=="1":
			cl.SetFilter('scomid',[int(company_id)])
		else:
			cl.SetFilter('rcomid',[int(company_id)])
		cl.SetSortMode( SPH_SORT_EXTENDED,"qid desc" )
		cl.SetLimits (frompageCount,limitNum,20000)
		res = cl.Query ('','question')
		if res:
			if res.has_key('matches'):
				tagslist=res['matches']
				
				for match in tagslist:
					id=match['id']
					list=getleavewords(id)
					listall.append(list)
				listcount=res['total_found']
	return {'list':listall,'count':listcount}
#询盘留言列表 翻页
def getleavewordscount(company_id):
	port = spconfig['port']
	cl = SphinxClient()
	cl.SetServer ( spconfig['serverid'], port )
	cl.SetMatchMode ( SPH_MATCH_BOOLEAN )
	if (company_id):
		cl.SetFilter('rcomid',[int(company_id)])
		cl.SetFilter('is_viewed',[0])
		cl.SetLimits (0,1,1)
		res = cl.Query ('','question')
		if res:
			listcount=res['total_found']
			return listcount
		
#我的收藏夹
def getfavoritelist(frompageCount,limitNum,company_id,checkStatus):
	listcount=0
	sqlarg=""
	if (checkStatus=="" or checkStatus==None):
		checkStatus=1
	print "checkStatus:",checkStatus
	if  checkStatus==1 or checkStatus=='1' :
		sqlarg=' (favorite_type_code=10091006 or favorite_type_code=10091000 or favorite_type_code=10091001 or favorite_type_code=10091007 ) '
	if  checkStatus=='2':
		sqlarg=" (favorite_type_code=10091002 or favorite_type_code=10091003) "
	if   checkStatus=='3':
		sqlarg=" favorite_type_code=10091004"
	if  checkStatus=='4':
		sqlarg=" favorite_type_code=10091005"
	if  checkStatus=='5':
		sqlarg=" favorite_type_code=10091012"
	
	sql="select count(0) from myfavorite where company_id=%s  and "+sqlarg
	#cursor.execute(sql,[company_id])
	#alist=cursor.fetchone()
	alist=dbc.fetchnumberdb(sql,[company_id])
	if alist:
		listcount=alist
	print "sqlarg:",sqlarg
	sql2="select id,favorite_type_code,content_id,content_title from myfavorite where company_id="+str(company_id)+" and "+sqlarg+" order by gmt_created desc limit "+str(frompageCount)+","+str(limitNum)
	print sql2
	#cursor.execute(sql2)
	#aalist=cursor.fetchall()
	aalist=dbc.fetchalldb(sql2)
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

#----生意管家 供求管理
def getmyproductslist(frompageCount="",limitNum="",company_id="",checkStatus=""):
	listcount=0
	if (checkStatus=="" or checkStatus==None):
		checkStatus=1
	sql="select count(0) from products where company_id=%s and check_status=%s and is_del=0"
	#cursor.execute(sql,[company_id,checkStatus])
	#alist=cursor.fetchone()
	alist=dbc.fetchnumberdb(sql,[company_id,checkStatus])
	if alist:
		listcount=alist
	sql="select id,title,real_time,refresh_time from products where company_id=%s and check_status=%s and is_del=0 order by refresh_time desc limit "+str(frompageCount)+","+str(frompageCount+limitNum)+""
	#cursor.execute(sql,[company_id,checkStatus])
	#alist=cursor.fetchall()
	alist=dbc.fetchalldb(sql,[company_id,checkStatus])
	listall=[]
	if alist:
		for list in alist:
			rlist={'proid':list[0],'protitle':list[1],'real_time':formattime(list[2],0),'refresh_time':formattime(list[3],0)}
#			list=getcompinfo(proid,cursor,None)
			listall.append(rlist)
	return {'list':listall,'count':listcount}

#----根据id查询1条供求
def getmyproductsbyid(id):
	sql="select id,title,quantity,quantity_unit,price,price_unit,details,category_products_main_code,products_type_code from products where id=%s"
	#cursor.execute(sql,[id])
	#list=cursor.fetchone()
	list=dbc.fetchonedb(sql,[id])
	if list:
		alist={'id':list[0],'title':list[1],'quantity':list[2],'quantity_unit':list[3],'price':list[4],'price_unit':list[5],'details':list[6],'categorycode':list[7],'products_type_code':list[8]}
		return alist
	
#----根据code查询供求类别
def getcategory_products(code):
	sql="select code,label from category_products where code=%s"
	#cursor.execute(sql,[code])
	#list=cursor.fetchone()
	list=dbc.fetchonedb(sql,[code])
	if list:
		alist={'code':list[0],'label':list[1]}
		return alist

#保存定制
def savecollect(company_id,keywords,gmt_created,collect_type):
	sql='select company_id from app_order where company_id=%s'
	#cursor.execute(sql,[company_id])
	#alist=cursor.fetchone()
	alist=dbc.fetchonedb(sql,[company_id])
	if alist:
		if collect_type=='1':
			sql='update app_order set businesskeywords=%s,gmt_created=%s where company_id=%s'
		elif collect_type=='2':
			sql='update app_order set pricekeywords=%s,gmt_created=%s where company_id=%s'
		#cursor.execute(sql,[keywords,gmt_created,company_id])
		#conn.commit()
		dbc.updatetodb(sql,[keywords,gmt_created,company_id])
	else:
		if collect_type=='1':
			sql='insert into app_order(businesskeywords,gmt_created,company_id) values(%s,%s,%s)'
		elif collect_type=='2':
			sql='insert into app_order(pricekeywords,gmt_created,company_id) values(%s,%s,%s)'
		#cursor.execute(sql,[keywords,gmt_created,company_id])
		#conn.commit()
		dbc.updatetodb(sql,[keywords,gmt_created,company_id])

#----商机定制主类
def getcompanykeyword(id):
	sql="select title from data_index where id=%s"
	#cursor.execute(sql,[id])
	#datalist=cursor.fetchone()
	datalist=dbc.fetchonedb(sql,[id])
	if datalist:
		return datalist[0]

#获得我的商机定制
def get_mybusinesscollect(company_id):
	sql='select businesskeywords from app_order where company_id=%s'
	#cursor.execute(sql,[company_id])
	#alist = cursor.fetchone()
	alist=dbc.fetchonedb(sql,[company_id])
	listall=[]
	if alist:
		keywords=alist[0]
		keyword_list=keywords.split(',')
		for id in keyword_list:
			keywd=getcompanykeyword(id)
			listall.append(keywd)
	return listall
#获得我的商机定制
def get_mybusinesscollectid(company_id):
	sql='select businesskeywords from app_order where company_id=%s'
	#cursor.execute(sql,[company_id])
	#alist = cursor.fetchone()
	alist=dbc.fetchonedb(sql,[company_id])
	listall=[]
	if alist:
		keywords=alist[0]
		if keywords:
			keyword_list=keywords.split(',')
			for id in keyword_list:
				listall.append(id)
	return listall
#获得我的商机定制
def get_mypricecollectid(company_id):
	sql='select pricekeywords from app_order where company_id=%s'
	#cursor.execute(sql,[company_id])
	#alist = cursor.fetchone()
	alist=dbc.fetchonedb(sql,[company_id])
	listall=[]
	if alist:
		keywords=alist[0]
		if keywords:
			keyword_list=keywords.split(',')
			for id in keyword_list:
				listall.append(id)
	return listall

#获得我的行情定制
def get_mypricecollect(company_id):
	sql='select pricekeywords from app_order where company_id=%s'
	#cursor.execute(sql,[company_id])
	#alist = cursor.fetchone()
	alist=dbc.fetchonedb(sql,[company_id])
	listall=[]
	if alist:
		keywords=alist[0]
		if keywords:
			keyword_list=keywords.split(',')
			for id in keyword_list:
				keywd=getpricecatename(id)
				list={'label':keywd,'id':id}
				listall.append(list)
	return listall

#广告脚本
def getadnum(code):
	max_ad=None
	sqlp="select max_ad from ad_position where id=%s"
	alist=dbads.fetchonedb(sqlp,[code])
	if alist:
		max_ad=alist[0]
	return max_ad

def getadshowtype(id):
	js_function=None
	sqlp="select js_function from delivery_style where id=%s"
	alist=dbads.fetchonedb(sqlp,[id])
	if alist:
		js_function=alist[0]
	return js_function
def getadlist(pkind,p):
	width=None
	height=None
	max_ad=None
	sqlp="select width,height,max_ad,delivery_style_id from ad_position where id=%s"
	alist=dbads.fetchonedb(sqlp,[pkind])
	if alist:
		width=alist[0]
		height=alist[1]
		max_ad=alist[2]
		delivery_style_id=alist[3]
		js_function=getadshowtype(delivery_style_id)
		
	sql="select ad_content,ad_target_url,id,ad_title from ad where position_id=%s and gmt_plan_end>='"+str(date.today()+timedelta(days=1))+"' and review_status='Y' and sequence=%s and online_status='Y' order by gmt_start asc,sequence asc"
	alist=dbads.fetchonedb(sql,[pkind,p])
	list=[]
	if alist:
		if (width=="0"):
			width=""
		if (height=="0"):
			height=""
		js_function=js_function.replace("{1}",alist[0])
		js_function=js_function.replace("|","")
		js_function=js_function.replace("\"","'")
		js_function=js_function.replace("{2}",alist[3])
		js_function=js_function.replace("{3}",'http://gg.zz91.com/hit?a='+str(alist[2]))
		js_function=js_function.replace("{4}",'width='+str(width))
		js_function=js_function.replace("{5}",'height='+str(height))
		list={'url':'http://gg.zz91.com/hit?a='+str(alist[2]),'picaddress':alist[0],'height':height,'width':width,'max_ad':max_ad,'js_function':js_function,'ad_title':alist[3]}
	return list
def getadlistnew(pkind):
	width=None
	height=None
	max_ad=None
	sqlp="select width,height,max_ad,delivery_style_id from ad_position where id=%s"
	alist=dbads.fetchonedb(sqlp,[pkind])
	if alist:
		width=alist[0]
		height=alist[1]
		max_ad=alist[2]
		delivery_style_id=alist[3]
		js_function=getadshowtype(delivery_style_id)
		
	sql="select ad_content,ad_target_url,id,ad_title from ad where position_id=%s and gmt_plan_end>='"+str(date.today()+timedelta(days=1))+"' and review_status='Y' and online_status='Y' order by gmt_start asc,sequence asc"
	alist=dbads.fetchalldb(sql,[pkind])
	listvalue=[]
	if alist:
		for list in alist:
			if (width=="0"):
				width=""
			if (height=="0"):
				height=""
			js_function1=js_function.replace("{1}",list[0])
			js_function1=js_function1.replace("|","")
			js_function1=js_function1.replace("\"","'")
			js_function1=js_function1.replace("{2}",list[3])
			js_function1=js_function1.replace("{3}",'http://gg.zz91.com/hit?a='+str(list[2]))
			js_function1=js_function1.replace("{4}",'width='+str(width))
			js_function1=js_function1.replace("{5}",'height='+str(height))
			list1={'url':'http://gg.zz91.com/hit?a='+str(list[2]),'picaddress':list[0],'height':height,'width':width,'max_ad':max_ad,'js_function':js_function1,'ad_title':list[3]}
			listvalue.append(list1)
	return listvalue
def getadlistkeywords(pkind,keywords):
	adid="0"
	adidlist="0"
	sqlp="select ad_id from ad_exact_type where ad_position_id=%s and anchor_point=%s"
	alist=dbads.fetchalldb(sqlp,[pkind,keywords])
	if alist:
		for aid in alist:
			ad_id=aid[0]
			adidlist+=","+str(ad_id)
			#adidlist.append(ad_id)
	#if adidlist:
		#adid=adidlist[0]
	#return adidlist	
	sql="select ad_content,ad_target_url,id,ad_title from ad where position_id=%s and gmt_plan_end>='"+str(date.today()+timedelta(days=1))+"' and id in ("+str(adidlist)+") and review_status='Y' and online_status='Y' order by gmt_start asc,sequence asc"
	alist=dbads.fetchalldb(sql,[pkind])
	listvalue=[]
	if alist:
		for list in alist:
			list1={'url':'http://gg.zz91.com/hit?a='+str(list[2]),'picaddress':list[0],'ad_title':list[3]}
			listvalue.append(list1)
	return listvalue

	
#供求详细页报价信息
def gettradetags(tradeid):
	sql="select category_products_main_code,tags from products where id=%s"
	#cursor.execute(sql,tradeid)
	#arrlist=cursor.fetchone()
	arrlist=dbc.fetchonedb(sql,tradeid)
	if arrlist:
		category_products_main_code=arrlist[0]
		tags=arrlist[1]
		if (tags!=None and tags!='' and tags!=' '):
			return tags
		else:
			sqlt="select label from category_products where code =%s"
			#cursor.execute(sqlt,str(category_products_main_code))
			#arrcatelist=cursor.fetchone()
			arrcatelist=dbc.fetchonedb(sqlt,str(category_products_main_code))
			if arrcatelist:
				return arrcatelist[0]
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
#获得城市信息
def getnavareavalue(code):
	if code:
		sql="select label,code from category where code=%s"
		result=dbc.fetchonedb(sql,[code])
		if result:
			area2=result[0]
			return result
	else:
		return None
		
def getnextareavalue(code):
	sql="select code,label from category where code like '"+str(code)+"____'"
	#cursor.execute(sql)
	#result=cursor.fetchone()
	result=dbc.fetchonedb(sql)
	if result:
		return 1
	else:
		return 0
def getproductscategoryname(id):
	sql="select label,code from category_products where id=%s"
	#cursor.execute(sql,id)
	#result=cursor.fetchone()
	result=dbc.fetchonedb(sql,id)
	if result:
		return result
def getareavalue(code):
	codelen=len(code)
	provincevalue=cache.get("provincevalue"+str(code))
	if provincevalue:
		listall1=provincevalue
	else:
		sql="select code,label from category where left(code,"+str(codelen)+")=%s and length(code)="+str(codelen+4)+""
		#cursor.execute(sql,code)
		#result=cursor.fetchall()
		result=dbc.fetchalldb(sql,code)
		listall=[]
		if (result):
			for list in result:
				list2={'code':list[0],'label':list[1],'firstpinyin':single_get_first(list[1])}
				list1=[list[0],list[1],single_get_first(list[1])]
				listall.append(list1)
		listall0=sorted(listall, key=lambda d:d[2])
		
		listall1=[]
		for i in listall0:
			nextarea=getnextareavalue(i[0])
			list={'code':i[0],'label':i[1],'firstpinyin':i[2],'nextarea':nextarea}
			listall1.append(list)
		cache.set("provincevalue"+str(code),listall1,60*60*60)
	return listall1
	
#---公司库首页有图片的最新供求列表
def getindexofferlist_pic(kname,pdt_type,limitcount,havepic=""):
	port = spconfig['port']
	cl = SphinxClient()
	cl.SetServer ( spconfig['serverid'], port )
	cl.SetMatchMode ( SPH_MATCH_BOOLEAN )
	cl.SetSortMode( SPH_SORT_EXTENDED," refresh_time desc,havepic desc" )
	cl.SetLimits (0,limitcount,limitcount)
	if (pdt_type!=None and pdt_type!=""):
		cl.SetFilter('pdt_kind',[int(pdt_type)])
	if (havepic):
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
				if (str(pdt_kind)=='1'):
					kindtxt="供应"
				if (str(pdt_kind)=='2'):
					kindtxt="求购"
				title=subString(attrs['ptitle'],40)
				sql1="select pic_address from products_pic where product_id=%s and check_status=1 order by is_default desc,id desc"
				#cursor.execute(sql1,[pid])
				#productspic = cursor.fetchone()
				productspic=dbc.fetchonedb(sql1,[pid])
				if productspic:
					pdt_images=productspic[0]
				else:
					pdt_images=""
				if (pdt_images == '' or pdt_images == '0'):
					pdt_images='http://img0.zz91.com/front/images/global/noimage.gif'
				else:
					pdt_images='http://img3.zz91.com/125x100/'+pdt_images+''
				list={'id':pid,'title':title,'gmt_time':pdt_date,'kindtxt':kindtxt,'fulltitle':attrs['ptitle'],'pdt_images':pdt_images}
				listall_offerlist.append(list)
			return listall_offerlist
#-------------供求列表
def getcompanyindexcomplist(kname,num):
	
	port = spconfig['port']
	cl = SphinxClient()
	cl.SetServer ( spconfig['serverid'], port )
	cl.SetMatchMode ( SPH_MATCH_BOOLEAN )
	cl.SetSortMode( SPH_SORT_EXTENDED," gmt_start desc" )
	cl.SetLimits (0,num,num)
	cl.SetFilter('apply_status',[1])

	nowdate=date.today()-timedelta(days=90)
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
#获得公司主营业务
def getcompanybusiness(company_id):
	sql="select business from company where id=%s"
	#cursor.execute(sql,[company_id])
	#comp = cursor.fetchone()
	comp=dbc.fetchonedb(sql,[company_id])
	if comp:
		return comp[0]
#----是否来电宝客户
def isldb(company_id):
	sqlg="select front_tel from phone where company_id=%s and expire_flag=0 and exists(select company_id from crm_company_service where crm_service_code in ('1007','1008','1009','1010') and apply_status=1 and company_id=phone.company_id)"
	#cursor.execute(sqlg,company_id)
	#phoneresult=cursor.fetchone()
	phoneresult=dbc.fetchonedb(sqlg,company_id)
	if phoneresult:
		return 1
	else:
		return None
#---获得来电宝电话
def getldbphone(company_id):
	if company_id:
		sqlg="select front_tel,tel from phone where company_id=%s and expire_flag=0 and exists(select company_id from crm_company_service where crm_service_code in ('1007','1008','1009','1010') and apply_status=1 and company_id=phone.company_id)"
		phoneresult=dbc.fetchonedb(sqlg,[company_id])
		if phoneresult:
			tel=phoneresult[1]
			tel=tel.replace("-",",,,")
			return {'front_tel':phoneresult[0],'tel':tel}
		else:
			return None
	else:
		return None
#----最新加入高会(含供求图片)			
def getindexcompanylist_pic(keywords="",num="",frompageCount="",limitNum="",allnum=""):
	#-------------供求列表
	port = spconfig['port']
	cl = SphinxClient()
	cl.SetServer ( spconfig['serverid'], port )
	cl.SetMatchMode ( SPH_MATCH_BOOLEAN )
	cl.SetSortMode( SPH_SORT_EXTENDED," id desc" )
	cl.SetGroupBy("company_id",SPH_GROUPBY_ATTR)
	cl.SetFilterRange('havepic',1,100)
	#cl.SetFilterRange('viptype',1,100)
	if (num):
		cl.SetLimits (0,num,num)
	else:
		cl.SetLimits (frompageCount,limitNum,allnum)
		
	if (keywords):
		res = cl.Query ('@(title,label0,label1,label2,label3,label4,city,province,tags) '+keywords,'offersearch_new,offersearch_new_vip')
	else:
		res = cl.Query ('','offersearch_new,offersearch_new_vip')
	listall_company=[]
	listcount=0
	if res:
		if res.has_key('matches'):
			itemlist=res['matches']
			
			for match in itemlist:
				id=match['id']
				attrs=match['attrs']
				company_id=attrs['company_id']
				business=getcompanybusiness(company_id)
				list=getcompinfo(id,cursor,keywords)
				list['business']=business
				pdt_images=list['pdt_images']
				list['pdt_images']=pdt_images
				ldbflag=isldb(company_id)
				list['ldbflag']=ldbflag
				listall_company.append(list)
			listcount=res['total_found']
	return {'list':listall_company,'listcount':listcount}
#报价固定导航
def getpricenav():
	navlist1=[]
	nav1={'label':'废铜','url':'priceday.html?t=40'}
	navlist1.append(nav1)
	nav1={'label':'废铁','url':'priceday.html?t=42'}
	navlist1.append(nav1)
	nav1={'label':'废钢','url':'priceday.html?t=45'}
	navlist1.append(nav1)
	nav1={'label':'废铝','url':'priceday.html?t=41'}
	navlist1.append(nav1)
	nav1={'label':'废镍','url':'priceday.html?t=47'}
	navlist1.append(nav1)
	nav1={'label':'废不锈钢','url':'priceday.html?t=44'}
	navlist1.append(nav1)
	nav1={'label':'废钼钛','url':'priceday.html?t=49'}
	navlist1.append(nav1)
	nav1={'label':'国外废金属','url':'priceday.html?t=46'}
	navlist1.append(nav1)
	nav1={'label':'江浙沪','url':'priceday.html?a=53'}
	navlist1.append(nav1)
	nav1={'label':'山东','url':'priceday.html?a=314'}
	navlist1.append(nav1)
	nav1={'label':'广东','url':'priceday.html?a=180'}
	navlist1.append(nav1)
	nav1={'label':'临沂','url':'priceday.html?a=55'}
	navlist1.append(nav1)
	nav1={'label':'清远','url':'priceday.html?a=59'}
	navlist1.append(nav1)
	
	navlist2=[]
	nav1={'label':'PP','url':'priceday.html?a=291'}
	navlist2.append(nav1)
	nav1={'label':'PVC','url':'priceday.html?a=297'}
	navlist2.append(nav1)
	nav1={'label':'PMMA','url':'priceday.html?a=299'}
	navlist2.append(nav1)
	nav1={'label':'EVA','url':'priceday.html?a=302'}
	navlist2.append(nav1)
	nav1={'label':'HDPE','url':'priceday.html?a=295'}
	navlist2.append(nav1)
	nav1={'label':'LDPE','url':'priceday.html?a=292'}
	navlist2.append(nav1)
	nav1={'label':'POM','url':'priceday.html?a=289'}
	navlist2.append(nav1)
	nav1={'label':'PET','url':'priceday.html?a=290'}
	navlist2.append(nav1)
	nav1={'label':'ABS','url':'priceday.html?a=296'}
	navlist2.append(nav1)
	nav1={'label':'PC','url':'priceday.html?a=293'}
	navlist2.append(nav1)
	nav1={'label':'GPPS','url':'priceday.html?a=306'}
	navlist2.append(nav1)
	nav1={'label':'余姚','url':'priceday.html?t=110'}
	navlist2.append(nav1)
	nav1={'label':'再生料','url':'priceday.html?t=98'}
	navlist2.append(nav1)
	nav1={'label':'新料出厂','url':'priceday.html?t=61'}
	navlist2.append(nav1)
	nav1={'label':'新料市场','url':'priceday.html?p=60'}
	navlist2.append(nav1)
	
	navlist3=[]
	nav1={'label':'油价快报','url':'priceday.html?t=190'}
	navlist3.append(nav1)
	nav1={'label':'废纸价格','url':'priceday.html?p=13'}
	navlist3.append(nav1)
	nav1={'label':'废橡胶价格','url':'priceday.html?t=30'}
	navlist3.append(nav1)
	nav1={'label':'综合废料','url':'priceday.html?t=220'}
	navlist3.append(nav1)
	
	return {'navlist1':navlist1,'navlist2':navlist2,'navlist3':navlist3}
#报价固定导航
def getnewsnav():
	navlist1=[]
	nav1={'label':'废铜','url':'priceday.html?t=40'}
	navlist1.append(nav1)
	nav1={'label':'废铁','url':'priceday.html?t=42'}
	navlist1.append(nav1)
	nav1={'label':'废钢','url':'priceday.html?t=45'}
	navlist1.append(nav1)
	nav1={'label':'废铝','url':'priceday.html?t=41'}
	navlist1.append(nav1)
	nav1={'label':'废镍','url':'priceday.html?t=47'}
	navlist1.append(nav1)
	nav1={'label':'废不锈钢','url':'priceday.html?t=44'}
	navlist1.append(nav1)
	nav1={'label':'废钼钛','url':'priceday.html?t=49'}
	navlist1.append(nav1)
	nav1={'label':'国外废金属','url':'priceday.html?t=46'}
	navlist1.append(nav1)
	nav1={'label':'江浙沪','url':'priceday.html?a=53'}
	navlist1.append(nav1)
	nav1={'label':'山东','url':'priceday.html?a=314'}
	navlist1.append(nav1)
	nav1={'label':'广东','url':'priceday.html?a=180'}
	navlist1.append(nav1)
	nav1={'label':'临沂','url':'priceday.html?a=55'}
	navlist1.append(nav1)
	nav1={'label':'清远','url':'priceday.html?a=59'}
	navlist1.append(nav1)
	
	navlist2=[]
	nav1={'label':'PP','url':'priceday.html?a=291'}
	navlist2.append(nav1)
	nav1={'label':'PVC','url':'priceday.html?a=297'}
	navlist2.append(nav1)
	nav1={'label':'PMMA','url':'priceday.html?a=299'}
	navlist2.append(nav1)
	nav1={'label':'EVA','url':'priceday.html?a=302'}
	navlist2.append(nav1)
	nav1={'label':'HDPE','url':'priceday.html?a=295'}
	navlist2.append(nav1)
	nav1={'label':'LDPE','url':'priceday.html?a=292'}
	navlist2.append(nav1)
	nav1={'label':'POM','url':'priceday.html?a=289'}
	navlist2.append(nav1)
	nav1={'label':'PET','url':'priceday.html?a=290'}
	navlist2.append(nav1)
	nav1={'label':'ABS','url':'priceday.html?a=296'}
	navlist2.append(nav1)
	nav1={'label':'PC','url':'priceday.html?a=293'}
	navlist2.append(nav1)
	nav1={'label':'GPPS','url':'priceday.html?a=306'}
	navlist2.append(nav1)
	nav1={'label':'余姚','url':'priceday.html?t=110'}
	navlist2.append(nav1)
	nav1={'label':'再生料','url':'priceday.html?t=98'}
	navlist2.append(nav1)
	nav1={'label':'新料出厂','url':'priceday.html?t=61'}
	navlist2.append(nav1)
	nav1={'label':'新料市场','url':'priceday.html?p=60'}
	navlist2.append(nav1)
	
	navlist3=[]
	nav1={'label':'油价快报','url':'priceday.html?t=190'}
	navlist3.append(nav1)
	nav1={'label':'废纸价格','url':'priceday.html?p=13'}
	navlist3.append(nav1)
	nav1={'label':'废橡胶价格','url':'priceday.html?t=30'}
	navlist3.append(nav1)
	nav1={'label':'综合废料','url':'priceday.html?t=220'}
	navlist3.append(nav1)
	
	return {'navlist1':navlist1,'navlist2':navlist2,'navlist3':navlist3}
#----商机定制主类
def getordercategorylistmain(code=""):
	if not code:
		code="10161001____"
	else:
		code=code+"____"
	sql="select label,code from data_index_category where code like '"+code+"'"
	#cursor.execute(sql)
	#datalist=cursor.fetchall()
	datalist=dbc.fetchalldb(sql)
	listall=[]
	for list in datalist:
		code=list[1]
		label=list[0]
		childlist=getordercategorylist(code)
		list1={'code':code,'label':label,'childlist':childlist}
		listall.append(list1)
	return listall
def getdata_index_categorylabel(code):
	sql="select label from data_index_category where code=%s"
	#cursor.execute(sql,[code])
	#datalist=cursor.fetchone()
	datalist=dbc.fetchonedb(sql,[code])
	if datalist:
		return datalist[0]

#----定制商机子类别
def getordercategorylist(code):
	sql="select title,id from data_index where category_code=%s order by sort asc"
	#cursor.execute(sql,[code])
	#datalist=cursor.fetchall()
	datalist=dbc.fetchalldb(sql,[code])
	listall=[]
	for list in datalist:
		title=list[0]
		id=list[1]
		list1={'title':title,'id':id}
		listall.append(list1)
	return listall

#----获取当前year
def getYear(datestr):   
    return str(datestr)[0:4]
#----获取当前month
def getMonth(datestr):
    return str(datestr)[5:7]
#----获取当前day
def getDay(datestr=""):
    if datestr:
        return str(datestr)[8:10]
    else:
        return str(datetime.date.today())[8:10]
#----读取企业新闻
def getcompanynews(fromcount,limitcount):
    sql="select count(0) from esite_news"
    #cursor.execute(sql)
    #listcount=cursor.fetchone()[0]
    listcount=dbc.fetchnumberdb(sql)
    sql="select a.id,a.company_id,a.title,a.post_time,b.domain_zz91 from esite_news as a left join company as b on a.company_id=b.id order by id desc limit "+str(fromcount)+","+str(limitcount)+""
    #cursor.execute(sql)
    #result=cursor.fetchall()
    result=dbc.fetchalldb(sql)
    listall=[]
    if result:
        for list in result:
            id=list[0]
            company_id=list[1]
            title=list[2]
            title10=subString(title,80)
            post_time=list[3]
            short_time=getMonth(post_time)+"-"+getDay(post_time)
            domain_zz91=list[4]
            list={'id':id,'title':title,'domain_zz91':domain_zz91,'pubdate':getMonth(post_time)+"-"+getDay(post_time),'short_time':short_time,'title10':title10}
            listall.append(list)
    return {'list':listall,'count':listcount}

#----读企业新闻内容
def getshowcompanynews(id):
	sql="select title,content from esite_news where id=%s"
	#cursor.execute(sql,[id])
	#result=cursor.fetchone()
	result=dbc.fetchonedb(sql,[id])
	if result:
		list={'title':result[0],'content':result[1]}
		return list

#企业新闻最终页上一篇下一篇(一期)
def getcompanyup(id):
	sqlt="select id,title from esite_news where id>%s order by id limit 0,1"
	#cursor.execute(sqlt,[id])
	#resultu = cursor.fetchone()
	resultu=dbc.fetchonedb(sqlt,[id])
	if resultu:
		list={'id':resultu[0],'title':resultu[1]}
		return list
def getcompanynx(id):
	sqlt="select id,title from esite_news where id<%s order by id desc limit 0,1"
	#cursor.execute(sqlt,[id])
	#resultn = cursor.fetchone()
	resultn=dbc.fetchonedb(sqlt,[id])
	if resultn:
		list={'id':resultn[0],'title':resultn[1]}
		return list
# 获得企业微站信息
def getcompanysmallsite(frompageCount,limitNum):
	sqlt="select count(0) from crm_company_service where crm_service_code='10001007' and apply_status='1' and gmt_end>gmt_start"
	#cursor.execute(sqlt)
	#listcount=cursor.fetchone()[0]
	listcount=dbc.fetchnumberdb(sqlt)
	sql="select company_id from crm_company_service where crm_service_code='10001007' and apply_status='1' and gmt_end>gmt_start order by id desc limit %s,%s"
	#cursor.execute(sql,[frompageCount,limitNum])
	#resultlist = cursor.fetchall()
	resultlist=dbc.fetchalldb(sql,[frompageCount,limitNum])
	if resultlist:
		listall=[]
		for result in resultlist:
			company_id=result[0]
			companydetail=getcompanydetail(company_id)
			listall.append(companydetail)
		return {'list':listall,'count':listcount}
# 获得来电宝信息
def getlaidianbao(frompageCount,limitNum):
	sqlt="select count(0) from crm_company_service where exists(select crm_service_code from crm_service_group where crm_service_code=crm_company_service.crm_service_code and code='ldb') and apply_status='1' and gmt_end>gmt_start"
	#cursor.execute(sqlt)
	#listcount=cursor.fetchone()[0]
	listcount=dbc.fetchnumberdb(sqlt)
	sql="select company_id from crm_company_service where exists(select crm_service_code from crm_service_group where crm_service_code=crm_company_service.crm_service_code and code='ldb') and apply_status='1' and gmt_end>gmt_start order by id desc limit %s,%s"
	#cursor.execute(sql,[frompageCount,limitNum])
	#resultlist = cursor.fetchall()
	resultlist=dbc.fetchalldb(sql,[frompageCount,limitNum])
	if resultlist:
		listall=[]
		for result in resultlist:
			company_id=result[0]
			companydetail=getcompanydetail(company_id)
			listall.append(companydetail)
		return {'list':listall,'count':listcount}

#----记录用户访问页面
def recordeddata(company_id,gmt_created,visiturl):
	return None
	sql="insert into userwriter(company_id,gmt_created,visiturl) values(%s,%s,%s)"
	#cursor_other.execute(sql,[company_id,gmt_created,visiturl])
	#conn.commit()
	dbc.updatetodb(sql,[company_id,gmt_created,visiturl])
	

#----统计展示数
def saveshowppc(company_id,adposition,adtype=''):
	gmt_created=datetime.datetime.now()
	phour=gmt_created.strftime("%-H")
	pdate=formattime(gmt_created,1)
	if adtype=="":
		adtype="1"
	showcount=1
	checkcount=0
	if adposition==None:
		adposition="sy"
	sql="select id from analysis_ppc_adlog where company_id=%s and  pdate=%s and phour=%s and adposition=%s"
	#cursor.execute(sql,[company_id,pdate,phour,adposition])
	#ppclog = cursor.fetchone()
	ppclog=dbc.fetchonedb(sql,[company_id,pdate,phour,adposition])
	if ppclog:
		id=ppclog[0]
		if adtype=="1":
			sqld="update analysis_ppc_adlog set showcount=showcount+1 where id=%s"
			#cursor.execute(sqld,[id])
			#conn.commit()
			dbc.updatetodb(sqld,[id])
		else:
			sqld="update analysis_ppc_adlog set checkcount=checkcount+1 where id=%s"
			#cursor.execute(sqld,[id])
			#conn.commit()
			dbc.updatetodb(sqld,[id])
	else:
		
		value=[company_id,showcount,checkcount,phour,pdate,gmt_created,adposition]
		sql="insert into analysis_ppc_adlog(company_id,showcount,checkcount,phour,pdate,gmt_created,adposition) values(%s,%s,%s,%s,%s,%s,%s)"
		#cursor.execute(sql,value)
		#conn.commit()
		dbc.updatetodb(sql,value)


#-----以下为用户信息修改与完善
#获得当前用户的主营行业编号
def getindustrycode(company_id):
	sql='select industry_code from company where id=%s'
	result=dbc.fetchonedb(sql,[company_id])
	if result:
		return result[0]
#根据主营行业的编号获得主营行业的label
def getindustrylabel(industrycode):
	sql='select label from category where code=%s'
	result=dbc.fetchonedb(sql,[industrycode])
	if result:
		return result[0]
#根据service_code获得公司类型label
def getservicelabel(service_code):
	sql='select label from category where code=%s'
	result=dbc.fetchonedb(sql,[service_code])
	if result:
		return result[0]
#---获得联系信息
def get_contactinfo(company_id):
	sql="select contact,sex,tel_country_code,tel_area_code,tel,fax_country_code,fax_area_code,fax,mobile,email,back_email,qq,weixin,msn from company_account where company_id=%s"
	result=dbc.fetchonedb(sql,[company_id])
	if result:
		contact=result[0]
		sex=result[1]
		tel_country_code=result[2]
		tel_area_code=result[3]
		tel=result[4]
		fax_country_code=result[5]
		fax_area_code=result[6]
		fax=result[7]
		mobile=result[8]
		email=result[9]
		back_email=result[10]
		qq=result[11]
		weixin=result[12]
		msn=result[13]
		list={"contact":contact,"sex":sex,"tel_country_code":tel_country_code,"tel_area_code":tel_area_code,"tel":tel,"fax_country_code":fax_country_code,"fax_area_code":fax_area_code,"fax":fax,"mobile":mobile,"email":email,"back_email":back_email,"qq":qq,"weixin":weixin,"msn":msn}
		return list

#---获得公司信息
def get_companyinfo(company_id):
	sql="select name,service_code,industry_code,area_code,address,address_zip,introduction,business,website from company where id=%s"
	result=dbc.fetchonedb(sql,[company_id])
	if result:
		name=result[0]
		service_code=result[1]
		industry_code=result[2]
		area_code=result[3]
		address=result[4]
		address_zip=result[5]
		introduction=result[6]
		business=result[7]
		website=result[8]
		#获得园区集散地
		sql1="select name,shorter_name,industry_code,garden_type_code from category_garden where area_code=%s"
		res_garden=dbc.fetchonedb(sql1,[area_code])
		if res_garden:
			garden_name=res_garden[0]
			shorter_name=res_garden[1]
			industry_code=res_garden[2]
			garden_type_code=res_garden[3]
			list={"name":name,"service_code":service_code,"industry_code":industry_code,"area_code":area_code,"address":address,"address_zip":address_zip,"introduction":introduction,"business":business,"garden_name":garden_name,"shorter_name":shorter_name,"industry_code":industry_code,"garden_type_code":garden_type_code,"website":website}
		else:
			list={"name":name,"service_code":service_code,"industry_code":industry_code,"area_code":area_code,"address":address,"address_zip":address_zip,"introduction":introduction,"business":business,"website":website}	
		return list	

				
		