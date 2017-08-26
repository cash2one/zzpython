import settings
import MySQLdb
from MySQLdb.cursors import DictCursor
from DBUtils.PooledDB import PooledDB
import os
from django.utils.http import urlquote
from django.shortcuts import render_to_response
from django.http import HttpResponse,HttpResponseRedirect

nowpath=os.path.dirname(__file__)
execfile(nowpath+"/conn.py")
execfile(nowpath+"/commfunction.py")

def default(request):
	sql="select aid,subject from bz_article order by posttime desc limit 0,9"
	helplist=fetchalldb(sql)
	listall=[]
	if helplist:
		for a in helplist:
			list={'aid':a[0],'subject':a[1]}
			listall.append(list)
	#conn.close()
	return render_to_response('company_homepage.html',locals())
def about(request):
	return render_to_response('about.html',locals())
def cluster(request):
	return render_to_response('cluster.html',locals())
def news(request,newsid):
	sql="select aid,subject,content,cat_id from bz_article where aid=%s"
	helpdetail=fetchonedb(sql,[newsid])
	if helpdetail:
		subject=helpdetail[1]
		details=helpdetail[2]
		details=details.replace('&lt;',"<")
		details=details.replace('&gt;',">")
		details=details.replace('&amp;',"&")
		details=details.replace('&quot;',"'")
		details=details.replace('&quot;',"'")
	return render_to_response('news.html',locals())
def astoer(request):
	return render_to_response('astoer.html',locals())
def opportunity_school(request):
	return render_to_response('opportunity_school.html',locals())
def public(request):
	return render_to_response('public.html',locals())
def footprint(request):
	return render_to_response('footprint.html',locals())
def b2c_cluster(request):
	return render_to_response('b2c_cluster.html',locals())
def contact(request):
	return render_to_response('contact.html',locals())
def focusing(request):
	return render_to_response('focusing.html',locals())
def honor(request):
	return render_to_response('honor.html',locals())
def knowledge(request):
	return render_to_response('knowledge.html',locals())
def knowledge1(request):
	return render_to_response('knowledge1.html',locals())
def knowledge2(request):
	return render_to_response('knowledge2.html',locals())
def opportunity(request):
	return render_to_response('opportunity.html',locals())
def stronghold(request):
	return render_to_response('stronghold.html',locals())
def culture(request):
	return render_to_response('culture.html',locals())
def ybpjob(request):
	return render_to_response('ybp-job.html',locals())
def mr_cluster(request):
	return render_to_response('mr_cluster.html',locals())