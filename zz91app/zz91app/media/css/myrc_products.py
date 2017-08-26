def myrc_products(request):
	
	webtitle="生意管家"
	nowlanmu="<a href='/myrc_index/'>生意管家</a>"
	weixinautologin(request,request.GET.get("weixinid"))
	username=request.session.get("username",None)
	company_id=request.session.get("company_id",None)
	if (username==None or company_id==None):
		return HttpResponseRedirect("/login/?done=/myrc_products/")
	page=request.GET.get("page")
	checkStatus=request.GET.get("checkStatus")
	if (checkStatus=="" or checkStatus==None):
		checkStatus=1
	if (page==None):
		page=1
	funpage = zz91page()
	limitNum=funpage.limitNum(5)
	nowpage=funpage.nowpage(int(page))
	frompageCount=funpage.frompageCount()
	after_range_num = funpage.after_range_num(2)
	before_range_num = funpage.before_range_num(9)
	qlistall=getmyproductslist(frompageCount=frompageCount,limitNum=limitNum,company_id=company_id,checkStatus=checkStatus)
	qlist=qlistall['list']
	qlistcount=qlistall['count']
	listcount=qlistcount
	if (int(listcount)>100000):
		listcount=100000
	listcount = funpage.listcount(listcount)
	page_listcount=funpage.page_listcount()
	firstpage = funpage.firstpage()
	lastpage = funpage.lastpage()
	page_range  = funpage.page_range()
	nextpage = funpage.nextpage()
	prvpage = funpage.prvpage()
	
	sql1="select count(0) from products where company_id=%s and check_status=1 and is_del=0 and refresh_time<expire_time"
	cursor.execute(sql1,[company_id])
	result1=cursor.fetchone()
	if result1:
		alist1=result1[0]
	sql0="select count(0) from products where company_id=%s and check_status=0 and is_del=0  and refresh_time<expire_time"
	cursor.execute(sql0,[company_id])
	result0=cursor.fetchone()
	if result0:
		alist0=result0[0]
	sql2="select count(0) from products where company_id=%s and check_status=2 and is_del=0  and refresh_time<expire_time"
	cursor.execute(sql2,[company_id])
	result2=cursor.fetchone()
	if result2:
		alist2=result2[0]
	isnotldb=1
	viptype=getviptype(company_id)
	if viptype=='10051003':
		isnotldb=None
	return render_to_response('myrc_products.html',locals())