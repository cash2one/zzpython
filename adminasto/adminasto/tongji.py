from sphinxapi import *
import os
import MySQLdb 
import datetime
nowpath=os.path.dirname(__file__)
execfile("conn.py")
#产品数量
def getproductnum(nowday):
	format="%Y-%m-%d";
	nowday=strtodatetime(nowday,format)
	oneday=datetime.timedelta(days=1)
	
	sql="select count(0) from products where gmt_created>'"+str(nowday)+"' and gmt_created<='"+str(nowday+oneday)+"'"
	cursor.execute(sql)
	offerlist=cursor.fetchone()
	if offerlist:
		return offerlist[0]
	else:
		return 0

#数据统计
def tongji(request):
	fromday="2013-8-1";
	format="%Y-%m-%d";
	fromday=strtodatetime(fromday,format)
	oneday=datetime.timedelta(days=1) 
	num=30
	listall=[] 
	for i in range(0,num):
		fromday=fromday-oneday
		postnum=0
		postnum=getproductnum(datetostr(fromday))
		leavewordsnum=0
		#leavewordsnum=getleavewordsnum(datetostr(fromday))

		list={'date':datetostr(fromday),'postnum':postnum,'leavewordsnum':leavewordsnum}
		
		listall.append(list)
	return render_to_response('tongji.html',locals())
	closeconn()