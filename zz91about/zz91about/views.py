#-*- coding:utf-8 -*-
import settings
import MySQLdb 
import os,sys
from django.utils.http import urlquote
from django.shortcuts import render_to_response
from django.http import HttpResponse,HttpResponseRedirect
from django.core.context_processors import csrf
from django.views.decorators.csrf import csrf_exempt

import random,datetime
from zz91db import zz91other
from zz91conn import database_comp
conn_comp=database_comp()
cursorc=conn_comp.cursor()
reload(sys)
sys.setdefaultencoding('UTF-8')
from alipay import Alipay
import requests
zzother=zz91other()

nowpath=os.path.dirname(__file__)
execfile(nowpath+"/conn.py")
execfile(nowpath+"/commfunction.py")
def default(request):
	sql="select aid,subject from bz_article order by posttime desc limit 0,15"
	cursor.execute(sql)
	helplist=cursor.fetchall()
	listall=[]
	if helplist:
		for a in helplist:
			list={'aid':a[0],'subject':a[1]}
			listall.append(list)
	return render_to_response('index.html',locals())
def linkus(request):
	websitelist=zzother.getwebsitelist(0,100,typeid=74,recommend='',wtype=3,order='sortrank',desc='asc')
	websitelist2=zzother.getwebsitelist(0,100,typeid=76,recommend='',wtype=3,order='sortrank',desc='asc')
	return render_to_response('linkus.html',locals())
def about(request):
	return render_to_response('about.html',locals())
def team(request):
	return render_to_response('team.html',locals())
def jobs(request):
	return render_to_response('jobs.html',locals())
def honor(request):
	return render_to_response('honor.html',locals())
def events(request):
	return render_to_response('events.html',locals())
def cooperation(request):
	return render_to_response('cooperation.html',locals())
def contact(request):
	return render_to_response('contact.html',locals())
def yssm(request):
	return render_to_response('yssm.html',locals())
def public(request):
	return render_to_response('public.html',locals())
def qqcontact(request):
	return render_to_response('qq.html',locals())
def qqcontact1(request):
	return render_to_response('qq1.html',locals())
def qqcontact2(request):
	return render_to_response('qq2.html',locals())
def news(request,newsid):
	sql="select aid,subject,content,cat_id from bz_article where aid=%s"
	cursor.execute(sql,[newsid])
	helpdetail=cursor.fetchone()
	if helpdetail:
		subject=helpdetail[1]
		details=helpdetail[2]
		details=details.replace('&lt;',"<")
		details=details.replace('&gt;',">")
		details=details.replace('&amp;',"&")
		details=details.replace('&quot;',"'")
		details=details.replace('&quot;',"'")
	return render_to_response('news.html',locals())
#ali支付数据生成
def zz91payfirst(request):
	c={}
	c.update(csrf(request))
	paytype = request.GET.get("paytype")
	if (paytype=="8"):
		money = request.GET.get('money')
		name = request.GET.get("name")
	total_fee="0"
	subject="其他服务"
	if (paytype=="1"):
		total_fee="3600.00"
		subject="来电宝服务"
	if (paytype=="2"):
		total_fee="5800.00"
		subject="一年再生通"
	if (paytype=="5"):
		total_fee="9800.00"
		subject="一年金牌品牌通"
	if (paytype=="7"):
		total_fee="18880.00"
		subject="一年钻石品牌通"
	if (paytype=="8"):
		total_fee=None
		otherje="1"
		subject="其他服务"
	
	
	return render_to_response('pay/alipay.html',locals())
def pay11(request):
	c={}
	c.update(csrf(request))
	paytype = request.GET.get("paytype")
	if (paytype=="ad260"):
		total_fee="260.00"
		subject="热门推荐广告3个月"
	if (paytype=="ad508"):
		total_fee="508.00"
		subject="热门推荐广告6个月"
	if (paytype=="ad1000"):
		total_fee="1000.00"
		subject="热门推荐广告12个月"
	if (paytype=="huangye"):
		total_fee="88.00"
		subject="2014中国再生资源商务大全 秒杀价"
		huangye=1
	if (paytype=="trade318"):
		total_fee="318.00"
		subject="手机供求信息置顶3个月"
	if (paytype=="trade608"):
		total_fee="608.00"
		subject="手机供求信息置顶6个月"
	if (paytype=="trade1180"):
		total_fee="1180.00"
		subject="手机供求信息置顶12个月"
	if (paytype=="mobile"):
		total_fee="388.00"
		subject="手机微站"
	
	if (paytype=="ldb"):
		total_fee="1500.00"
		subject="来电宝"
	if (paytype=="zst1"):
		total_fee="3500.00"
		subject="再生通一年"
	if (paytype=="zst2"):
		total_fee="7000.00"
		subject="再生通两年"
	if (paytype=="jpt"):
		total_fee="5880.00"
		subject="金牌通"
	if (paytype=="huangzhan"):
		total_fee="6000.00"
		subject="黄展"
	return render_to_response('pay/pay11.html',locals())
#---支付跳转到ali支付页面
@csrf_exempt
def zz91pay(request):
	total_fee = request.POST.get('total_fee')
	subject = request.POST.get('subject')
	mobile=request.POST.get("mobile")
	contact=request.POST.get("contact")
	address=request.POST.get("address")
	todate=datetime.datetime.now()
	today=todate.strftime('%Y%m%d')
	t=random.randrange(100000,999999)
	out_trade_no=str(today)+str(t)
	gmt_created=datetime.datetime.now()
	
	title="在线支付"
	content="电话："+str(mobile)+"<br />联系人："+str(contact)
	if address:
		content=content+"<br />收货地址："+str(address)
	if subject:
		content=content+"<br />产品："+str(subject)
	
	sql="insert into subject_baoming(title,contents,gmt_created) values(%s,%s,%s)"
	cursorc.execute(sql,[title,content+"<br/>时间："+str(gmt_created),gmt_created])
	
	is_success="F"
	valu=[out_trade_no,subject,total_fee,contact,mobile,is_success]
	sql="insert into pay_order(out_trade_no,subject,total_fee,contact,mobile,is_success) values(%s,%s,%s,%s,%s,%s)"
	cursorc.execute(sql,valu)
	conn_comp.commit()
	#subject=urlquote(subject)
	url="https://shenghuo.alipay.com/send/payment/fill.htm?optEmail=zhifu%40asto-inc.com&payAmount="+str(total_fee)+"&title="+mobile+"&memo="+subject
	return render_to_response('pay/paybank.html',locals())
	return HttpResponseRedirect(url)
	return HttpResponseRedirect("http://www.zz91.com/hkfs/")
	alipay = Alipay(pid='2088511051388426', key='ovtvgwuew1zdfmbiydepr0k9m8b25exp', seller_email='zhifu@asto-inc.com')
	payurl=alipay.create_direct_pay_by_user_url(out_trade_no=out_trade_no, subject=subject, total_fee=total_fee, return_url='http://about.zz91.com/zz91payreturn_url.html', notify_url='http://about.zz91.com/zz91payverify_notify.html')
	return HttpResponseRedirect(payurl)
#---异步返回保持信息，和判断是否支付成功
@csrf_exempt
def zz91payverify_notify(request):
	tn = request.POST.get("out_trade_no")
	trade_status=request.POST.get("trade_status")
	if tn:
		sql="update pay_order set trade_status=%s,where out_trade_no=%s"
		cursorc.execute(sql,[trade_status,tn])
		conn_comp.commit()
	return HttpResponse("success")
	if request.method == POST:
		verify_result = alipay.verify_notify(request.POST) # 解码并验证数据是否有效 
        if verify_result: 
            tn = request.POST.get("out_trade_no")
            if request.POST.get("trade_status") in ("TRADE_FINISHED","TRADE_SUCCESS"): 
                trade_status=request.POST.get("trade_status")
                buyer_email=request.POST.get("buyer_email")
                sql="update pay_order set trade_status=%s,buyer_email=%s where out_trade_no=%s"
                cursorc.execute(sql,[trade_status,buyer_email,tn])
                conn_comp.commit()
                #remark = u"使用支付宝 %s 充值，交易号: %s % (request.POST.get(buyer_email), tn)" 
            	return HttpResponse("success") #有效数据需要返回 success 给 alipay
            else:
            	return HttpResponse("fail")
        else:
        	return HttpResponse("fail") # 无效数据返回 fail
#----支付成功返回页面	
def zz91payreturn_url(request):
	tn = request.GET.get("out_trade_no")
	trade_status=request.GET.get("trade_status")
	buyer_email=request.GET.get("buyer_email")
	is_success=request.GET.get("is_success")
	notify_id=request.GET.get("notify_id")
	notify_time=request.GET.get("notify_time")
	subject=request.GET.get("subject")
	trade_no=request.GET.get("trade_no")
	if is_success=="T":
		suc="您已经成功完成支付，我们将在1个工作日内容为您开通服务。"
		sql="update pay_order set trade_status=%s,buyer_email=%s,is_success=%s,notify_id=%s,notify_time=%s,subject=%s,trade_no=%s where out_trade_no=%s"
		cursorc.execute(sql,[trade_status,buyer_email,is_success,notify_id,notify_time,subject,trade_no,tn])
		conn_comp.commit()
	else:
		suc="可能因为网络的原因，没有支付,请重新下单再试。"
	#buyer_email=kangxianyue%40sina.com&buyer_id=2088002519567678&exterface=create_direct_pay_by_user&is_success=T&notify_id=RqPnCoPT3K9%252Fvwbh3InR9dBYXYo5QXwv2224BAsIzz%252Fl5Xzf%252BAtx1Xqg7vfJ1chSbAGT&notify_time=2014-07-10+11%3A58%3A58&notify_type=trade_status_sync&out_trade_no=2312434&payment_type=1&seller_email=zhifu%40asto-inc.com&seller_id=2088511051388426&subject=其他服务&total_fee=0.10&trade_no=2014071060972767&trade_status=TRADE_SUCCESS&sign=a70409e04bb6159a5f83ad70defb5bdd&sign_type=MD5
	return render_to_response('pay/suc.html',locals())

