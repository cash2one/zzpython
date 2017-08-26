from django.shortcuts import render_to_response
from django.http import HttpResponse,HttpResponseRedirect,HttpResponsePermanentRedirect
import MySQLdb,sys,os,memcache,settings,urllib,re,time,datetime,requests,random,string,md5,hashlib
from django.core.cache import cache
from sphinxapi import *
from zz91page import *
from settings import spconfig
from zz91settings import SPHINXCONFIG
import simplejson
from commfunction import filter_tags,formattime,havepicflag,subString,getjiami
from function import getnowurl,getbbslist
from zz91tools import int_to_str
from datetime import timedelta, date 
from zz91db_ast import companydb
import pingpp

dbc=companydb()

reload(sys)
sys.setdefaultencoding('UTF-8')
nowpath=os.path.dirname(__file__)


def pay(request):
    backurl=request.META.get('HTTP_REFERER','/')
    host=getnowurl(request)
    """
    username=request.session.get("username",None)
    company_id=request.session.get("company_id",None)
    if username and company_id==None:
        company_id=getcompanyid(username)
        request.session['company_id']=company_id
    if (username==None or company_id==None):
        return HttpResponseRedirect("/login/?done="+host)
    
    companycontact=zzq.getcompanycontact(company_id)
    mobile=companycontact['mobile']
    contact=companycontact['contact']
    """
    order_id=request.GET.get("order_id")
    identity_id=request.GET.get("identity_id")
    product_name=request.GET.get("product_name")
    product_desc=request.GET.get("product_desc")
    amount=request.GET.get("amount")
    amount_r='%.2f' % int(float(amount) / 100)
    merchant_url=request.GET.get("merchant_url")
    user_ip=request.GET.get("user_ip")
    payload={'order_id':order_id,'identity_id':identity_id,'product_name':product_name,'product_desc':product_desc,'amount':amount,'merchant_url':merchant_url,'user_ip':user_ip}
    yeeurl=urllib.urlencode(payload)
    return render_to_response('pingxx/pay.html',locals())

def pay_save(request):
    pingpp.api_key = 'sk_live_dHUzL3M5N8EblzOkPlO2kJHs'
    amount=request.GET.get("amount")
    if amount:
        order_id=request.GET.get("order_id")
        product_name=request.GET.get("product_name")
        client_ip=request.GET.get("user_ip")
        channel=request.GET.get("channel")
        if channel=="wx_pub":
            ch = pingpp.Charge.create(
                order_no=order_id,
                channel=channel,
                amount=int(float(amount)),
                subject=product_name,
                body=product_name,
                currency='cny',
                app=dict(open_id='wx2891ef70c5a770d6'),
                extra=dict(success_url='http://pyapp.zz91.com/zz91payreturn_url.html'),
                client_ip="115.236.188.99"
            )
        elif channel=="yeepay_wap":
            ch = pingpp.Charge.create(
                order_no=order_id,
                channel=channel,
                amount=int(float(amount)),
                subject=product_name,
                body=product_name,
                currency='cny',
                app=dict(id='app_SqrzfLn5iDq5K0Om'),
                result_url='http://m.zz91.com/pay/callback_get.html',
                product_category='7',
                identity_id=order_id,
                identity_type=0,
                terminal_type=3,
                terminal_id='05-16-DC-59-C2-34',
                user_ua='NokiaN70/3.0544.5.1 Series60/2.8 Profile/MIDP-2.0 Configuration/CLDC-1.1',
                client_ip="115.236.188.99"
            )
        else:
            ch = pingpp.Charge.create(
                order_no=order_id,
                channel=channel,
                amount=int(float(amount)),
                subject=product_name,
                body=product_name,
                currency='cny',
                app=dict(id='app_SqrzfLn5iDq5K0Om'),
                extra=dict(success_url='http://pyapp.zz91.com/zz91payreturn_url.html'),
                client_ip="115.236.188.99"
            )
        return HttpResponse(simplejson.dumps(ch, ensure_ascii=False))
    else:
        return HttpResponse("err")
