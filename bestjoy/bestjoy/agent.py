#-*- coding:utf-8 -*-
from django.shortcuts import render_to_response
from django.http import HttpResponse,HttpResponseRedirect
import simplejson,sys,os,urllib,re,datetime,time,md5,hashlib,random,calendar
import StringIO,qrcode
from conn import bestjoydb
from zz91page import *
db = bestjoydb()
reload(sys)
sys.setdefaultencoding('UTF-8')
nowpath=os.path.dirname(__file__)
execfile(nowpath+"/func/crmtools.py")
execfile(nowpath+"/func/order_function.py")
from zweixin.client import WeixinAPI,WeixinMpAPI
from zz91settings import weixinconfig
APP_ID = weixinconfig['bestjoyserver']['appid']
APP_SECRET = weixinconfig['bestjoyserver']['secret']
REDIRECT_URI = 'http://bestjoy.asto.com.cn/agent/redirect_uri.html'
api = WeixinMpAPI(appid=APP_ID,
                app_secret=APP_SECRET,
                redirect_uri=REDIRECT_URI)

orddb=orderfun()

#微信授权登陆
def auth_login(request):
    scope = ("snsapi_base", )
    authorize_url = api.get_authorize_url(scope=scope)
    randomstr=request.GET.get("randomstr")
    gmt_created=gmt_modified=datetime.datetime.now()
    request.session['best_randomstr']=randomstr
    request.session.set_expiry(6000*6000)
    
    return HttpResponseRedirect(authorize_url)
#授权跳转
def redirect_uri(request):
    code=request.GET.get("code")
    gmt_created=gmt_modified=datetime.datetime.now()
    access_token = api.exchange_code_for_access_token(code=code)
    weixinid=access_token['openid']
    request.session.set_expiry(6000*6000)
    randomstr=request.session.get("best_randomstr")
    request.session['best_weixinid']=weixinid
    sql="select id,agent_id from agent_contact where weixinid=%s"
    result=db.fetchonedb(sql,[weixinid])
    if result:
        return HttpResponseRedirect("bindsuc.html?havebind=1")
    
    sql="select id,agent_id from agent_contact where randomstr=%s and checked=0"
    result=db.fetchonedb(sql,[randomstr])
    havebind="0"
    if not result:
        havebind="1"
    else:
        agent_id=result['agent_id']
        id=result['id']
        sql="update agent_contact set checked=1,weixinid=%s where id=%s"
        db.updatetodb(sql,[weixinid,id])
        request.session['best_randomstr']=''
    
    return HttpResponseRedirect("bindsuc.html?havebind="+str(havebind))
        
#绑定成功
def bindsuc(request):
    havebind=request.GET.get("havebind")
    return render_to_response('mobile/bindsuc.html',locals())
#确认是否绑定
def binding(request):
    randomstr=request.GET.get("randomstr")
    sql="select id,agent_id from agent_contact where randomstr=%s and checked=0"
    result=db.fetchonedb(sql,[randomstr])
    havebind=None
    if not result:
        havebind=1
    else:
        agent_id=result['agent_id']
        sql="select aname,contactname from agentlist where id=%s"
        resulta=db.fetchonedb(sql,[agent_id])
        
    return render_to_response('mobile/binding.html',locals())

#我的订单
def agent_orderlist(request):
    best_weixinid=request.session.get("best_weixinid")
    if not best_weixinid:
        return HttpResponseRedirect("/err.html?errkey=登录过期，请重新从微信订单中进入。。")
    request_url=request.META.get('HTTP_REFERER','/')
    
    sql="select agent_id from agent_contact where weixinid=%s and checked=1"
    result=db.fetchonedb(sql,[best_weixinid])
    agentlist_id=''
    if not result:
        return HttpResponseRedirect("/err.html?errkey=你的微信还未绑定分单系统。")
    else:
        agentlist_id=result['agent_id']
    page=request.GET.get('page')
    status=request.GET.get('status')
    if not page:
        page=1
    if not status:
        status='1'
    orderno=request.GET.get("orderno")
    proname=request.GET.get("proname")
    if not proname:
        proname=''
    protype=request.GET.get("protype")
    if not protype:
        protype=''
    prosize1=request.GET.get("prosize1")
    prosize2=request.GET.get("prosize2")
    proprice2=request.GET.get("proprice2")
    proprice1=request.GET.get("proprice1")
    pronumber1=request.GET.get("pronumber1")
    pronumber2=request.GET.get("pronumber2")
    prodesc=request.GET.get("prodesc")
    iscomplete=request.GET.get("iscomplete")
    if not prodesc:
        prodesc=''
    area=request.GET.get("area")
    if not area:
        area=''
    address=request.GET.get("address")
    if not address:
        address=''
    postcode=request.GET.get("postcode")
    if not postcode:
        postcode=''
    contactname=request.GET.get("contactname")
    if not contactname:
        contactname=''
    phone=request.GET.get("phone")
    mobile=request.GET.get("mobile")
    searchlist={}
   
    if orderno:
        searchlist['orderno']=orderno
    if proname:
        searchlist['proname']=proname
    if protype:
        searchlist['protype']=protype
    if prosize1:
        searchlist['prosize1']=prosize1
    if prosize2:
        searchlist['prosize2']=prosize2
    if proprice1:
        searchlist['proprice1']=proprice1
    if proprice2:
        searchlist['proprice2']=proprice2
    if pronumber1:
        searchlist['pronumber1']=pronumber1
    if pronumber2:
        searchlist['pronumber2']=pronumber2
    if prodesc:
        searchlist['prodesc']=prodesc
    if area:
        searchlist['area']=area
    if address:
        searchlist['address']=address
    if postcode:
        searchlist['postcode']=postcode
    if contactname:
        searchlist['contactname']=contactname
    if mobile:
        searchlist['mobile']=mobile
    if phone:
        searchlist['phone']=phone
    if agentlist_id:
        searchlist['agentlist_id']=agentlist_id
    if iscomplete:
        searchlist['iscomplete']=iscomplete
    searchurl=urllib.urlencode(searchlist)
    
    funpage=zz91page()
    limitNum=funpage.limitNum(8)
    nowpage=funpage.nowpage(int(page))
    frompageCount=funpage.frompageCount()
    after_range_num = funpage.after_range_num(3)
    before_range_num = funpage.before_range_num(6)
    #获得客户
    allcustomer=orddb.orderlist(frompageCount=frompageCount,limitNum=limitNum,searchlist=searchlist,status=status)
    if allcustomer:
        listcount=allcustomer['count']
        listall=allcustomer['list']
        listcount = funpage.listcount(listcount)
        page_listcount=funpage.page_listcount()
        firstpage = funpage.firstpage()
        lastpage = funpage.lastpage()
        page_range  = funpage.page_range()
        if len(page_range)>7:
            page_range=page_range[:7]
        nextpage = funpage.nextpage()
        prvpage = funpage.prvpage()
    return render_to_response('mobile/agent_orderlist.html',locals())

def agent_ordershow(request):
    weixinid=request.GET.get("weixinid")
    best_weixinid=request.session.get("best_weixinid")
    if not weixinid:
        weixinid=best_weixinid
    sql="select agent_id from agent_contact where weixinid=%s and checked=1"
    result=db.fetchonedb(sql,[weixinid])
    agentlist_id=''
    if not result:
        return HttpResponseRedirect("/err.html?errkey=你的微信还未绑定分单系统。")
    else:
        request.session.set_expiry(6000*6000)
        request.session['best_weixinid']=weixinid
        
    request_url=request.META.get('HTTP_REFERER','/')
    if not request_url:
        request_url="/agent/agent_orderlist.html"
    order_id=request.GET.get("order_id")
    sql="select * from orderlist where id=%s"
    result=db.fetchonedb(sql,[order_id])
    area=result['area']
    arealabel2=''
    arealabel3=''
    arealabel4=''
    if len(area)>=12:
        arealabel2=orddb.getarea(area_code=area[0:12])
    if len(area)>=16:
        arealabel3=orddb.getarea(area_code=area[0:16])
    if len(area)>=20:
        arealabel4=orddb.getarea(area_code=area[0:20])
    result['arealabel']=arealabel2+"-"+arealabel3+"-"+arealabel4
    phone=result['phone']
    result['gmt_created']=formattime(result['gmt_created'])
    arrphone=phone.split("-")
    if len(arrphone)>=2:
        phone1=arrphone[0]
        phone2=arrphone[1]
        phone3=arrphone[2]
        result['phone1']=phone1
        result['phone2']=phone2
        result['phone3']=phone3
    return render_to_response('mobile/agent_ordershow.html',locals())
#确认收单
def completeorder(request):
    best_weixinid=request.session.get("best_weixinid")
    if not best_weixinid:
        return HttpResponseRedirect("/err.html?errkey=登录过期，请重新从微信订单中进入。。")
    request_url=request.META.get('HTTP_REFERER','/')
    order_id=request.GET.get("order_id")
    sql="update orderlist set iscomplete=1 where id=%s"
    result=db.updatetodb(sql,[order_id])
    return HttpResponseRedirect("/agent/agent_orderlist.html")

#错误跳转
def errfun(request):
    errkey=request.GET.get("errkey")
    return render_to_response('mobile/err.html',locals())
