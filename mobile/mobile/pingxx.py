#-*- coding:utf-8 -*-
from django.shortcuts import render_to_response
from django.http import HttpResponse,HttpResponseRedirect,HttpResponsePermanentRedirect
import MySQLdb,sys,os,memcache,settings,urllib,re,time,datetime,requests,random,string,md5,hashlib
from django.core.cache import cache
from sphinxapi import *
from zz91page import *
from settings import spconfig
from zz91settings import SPHINXCONFIG
import simplejson,json
from commfunction import filter_tags,formattime,havepicflag,subString,getjiami
from function import getnowurl,getbbslist
from zz91tools import int_to_str
from datetime import timedelta, date 
from zz91db_ast import companydb
import pingpp
from wxpay import QRWXpay, JSWXpay

dbc=companydb()

reload(sys)
sys.setdefaultencoding('UTF-8')
nowpath=os.path.dirname(__file__)
js_wxpay = JSWXpay(appid='wx2891ef70c5a770d6',
                   mch_id='1230440002',
                   key='YWm2FhYr2BDbTZrPYWm2FhYr2BDbTZrP',
                   ip='120.26.66.166',
                   notify_url='http://m.zz91.com/zz91payverify_notify.html',
                   appsecret='d3f9436cfc50cd9e4f62f96893a1ee0c')
def wx_pay(request):
    out_trade_no = request.GET.get('out_trade_no')
    info_dict = {
        'redirect_uri': 'http://m.zz91.com/wxpay/wx_makepayment.html',
        'state': str(out_trade_no),
    }
    url = js_wxpay.generate_redirect_url(info_dict)
    sql="select subject from pay_order where out_trade_no=%s"
    result=dbc.fetchonedb(sql,[out_trade_no])
    if result:
        subject=result[0]
        sql="update pay_order set subject=%s where out_trade_no=%s"
        dbc.updatetodb(sql,[subject+'(在线-微信支付)',out_trade_no])
    
    return HttpResponseRedirect(url)

def payupdate(request):
    out_trade_no = request.GET.get('out_trade_no')
    sql="select subject from pay_order where out_trade_no=%s"
    result=dbc.fetchonedb(sql,[out_trade_no])
    if result:
        subject=result[0]
        sql="update pay_order set subject=%s where out_trade_no=%s"
        payfrom=request.GET.get('payfrom')
        dbc.updatetodb(sql,[subject+'('+str(payfrom)+')',out_trade_no])
    return HttpResponse("")

def wx_makepayment(request):
    code = request.GET.get('code')
    state = request.GET.get('state')
    out_trade_no = state
    openid = js_wxpay.generate_openid(code)
    #todate=datetime.datetime.now()
    #today=todate.strftime('%Y%m%d')
    #t=random.randrange(100000,999999)
    #out_trade_no=str(today)+str(t)
    payreturn_url=''
    sql="select total_fee,contact,mobile,payreturn_url from pay_order where out_trade_no=%s"
    result=dbc.fetchonedb(sql,[out_trade_no])
    if result:
        fee=result[0]
        contact=result[1]
        mobile=result[2]
        payreturn_url=result[3]
    product = {
        'attach': u'再生钱包充值',
        'body': str(contact)+str(mobile),
        'out_trade_no': out_trade_no,
        'total_fee': float(fee),
    }
    ret_dict = js_wxpay.generate_jsapi(product, openid)
    ret_str = """
    <html>
    <head></head>
    <body>
    <script type="text/javascript">
    function callpay(){
        if (typeof WeixinJSBridge == "undefined"){
            if( document.addEventListener ){
                document.addEventListener('WeixinJSBridgeReady', jsApiCall, false);
            }else if (document.attachEvent){
                document.attachEvent('WeixinJSBridgeReady', jsApiCall); 
                document.attachEvent('onWeixinJSBridgeReady', jsApiCall);
            }
        }else{
            jsApiCall();
        }
    }
    function jsApiCall(){
        WeixinJSBridge.invoke(
            'getBrandWCPayRequest',
            %s,
            function(res){
                //alert(JSON.stringify(res));
                if(res.err_msg == "get_brand_wcpay_request:ok" ) {  
                    window.location="%s";
                }else{
                    alert("支付失败")
                }
            }
        );
    }
    callpay();
    </script>
    </body>
    </html>
    """ % (json.dumps(ret_dict),payreturn_url)
    #ret_dict=json.dumps(ret_dict)
    #return render_to_response('pingxx/wxpay.html',locals())
    return HttpResponse(ret_str)

def pay(request):
    backurl=request.META.get('HTTP_REFERER','/')
    host=getnowurl(request)
    pagefrom=request.GET.get("pagefrom")
    if pagefrom=="None":
        pagefrom=None
    order_id=request.GET.get("order_id")
    identity_id=request.GET.get("identity_id")
    product_name=request.GET.get("product_name")
    product_desc=request.GET.get("product_desc")
    amount=request.GET.get("amount")
    amount_r='%.2f' % float(float(amount) / 100)
    merchant_url=request.GET.get("merchant_url")
    user_ip=request.GET.get("user_ip")
    user_ipa=user_ip.split(",")
    user_ip=user_ipa[0]
    payload={'order_id':order_id,'identity_id':identity_id,'product_name':product_name,'product_desc':product_desc,'amount':amount,'merchant_url':merchant_url,'user_ip':user_ip}
    yeeurl=urllib.urlencode(payload)
    return render_to_response('aui/qianbao/pay.html',locals())
    #return render_to_response('pingxx/pay.html',locals())

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
                app=dict(id='app_SqrzfLn5iDq5K0Om'),
                extra=dict(open_id='wx2891ef70c5a770d6'),
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
                extra=dict(
                product_category='7',
                identity_id=order_id,
                identity_type=0,
                terminal_type=3,
                terminal_id='05-16-DC-59-C2-34',
                result_url='http://m.zz91.com/pay/callback_get.html',
                user_ua='NokiaN70/3.0544.5.1 Series60/2.8 Profile/MIDP-2.0 Configuration/CLDC-1.1'
                ),
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
                extra=dict(success_url='http://m.zz91.com/zz91payreturn_url.html'),
                client_ip="115.236.188.99"
            )
        return HttpResponse(simplejson.dumps(ch, ensure_ascii=False))
    else:
        return HttpResponse("err")
