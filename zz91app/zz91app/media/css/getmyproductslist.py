def getmyproductslist(frompageCount="",limitNum="",company_id="",checkStatus=""):
	listcount=0
	if (checkStatus=="" or checkStatus==None):
		checkStatus=1
	sql="select count(0) from products where company_id=%s and check_status=%s and is_del=0"
	cursor.execute(sql,[company_id,checkStatus])
	alist=cursor.fetchone()
	if alist:
		listcount=alist[0]
	sql="select id,title,real_time,refresh_time from products where company_id=%s and check_status=%s and is_del=0 order by refresh_time desc limit "+str(frompageCount)+","+str(frompageCount+limitNum)+""
	cursor.execute(sql,[company_id,checkStatus])
	alist=cursor.fetchall()
	listall=[]
	if alist:
		for list in alist:
			rlist={'proid':list[0],'protitle':list[1],'real_time':formattime(list[2],0),'refresh_time':formattime(list[3],0)}
#			list=getcompinfo(proid,cursor,None)
			listall.append(rlist)
	return {'list':listall,'count':listcount}