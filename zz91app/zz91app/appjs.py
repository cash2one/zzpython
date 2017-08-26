#-*- coding:utf-8 -*-
from django.shortcuts import render_to_response
from django.http import HttpResponse,HttpResponseRedirect,HttpResponsePermanentRedirect
import MySQLdb,sys,os,memcache,settings,urllib,re,time,datetime,md5,hashlib,random
from django.core.cache import cache
import simplejson
#from commfunction import subString,filter_tags,replacepic,formattime
#from function import getnowurl
from zz91page import *
from zz91db_ast import companydb
from zz91db_2_news import newsdb
from zz91db_zzlog import zzlogdb
from zz91conn import database_mongodb
from sphinxapi import *
from settings import spconfig,appurl
from zz91settings import SPHINXCONFIG,weixinconfig
from zz91tools import formattime,subString,filter_tags,int_to_str,str_to_int
from appwxpay.wxpay import Wxpay

dbc=companydb()
dbn=newsdb()
dbzzlog=zzlogdb()
#连接loginfo集合（表）
dbmongo=database_mongodb()
 


reload(sys)
sys.setdefaultencoding('UTF-8')
nowpath=os.path.dirname(__file__)
execfile(nowpath+"/func/public_function.py")
execfile(nowpath+"/func/news_function.py")
execfile(nowpath+"/func/inquiry_function.py")
execfile(nowpath+"/func/huzhu_function.py")
execfile(nowpath+"/func/qianbao_function.py")
execfile(nowpath+"/func/message_function.py")
execfile(nowpath+"/func/order_function.py")
execfile(nowpath+"/func/price_function.py")
execfile(nowpath+"/func/myrc_function.py")
execfile(nowpath+"/func/company_function.py")

zzn=zznews()
zzi=zzinquiry()
zzh=zzhuzhu()
zzq=zzqianbao()
zzm=zzmessage()
zzo=zzorder()
zzmyrc=zmyrc()
zzprice=zprice()


def pricelist(request):
    company_id=request.GET.get("company_id")
    clientid=request.GET.get('clientid')
    mypricecollect=zzmyrc.get_mypricecollectid(company_id)
    mybusi=zzmyrc.get_mybusinesscollect(company_id)
    l=[99990]
    for a in mypricecollect:
        l.append(int(a))
    if not l or l==[99990]:
        pricelist=None
        pricelist=zzprice.getpricelist(frompageCount=0,limitNum=5,allnum=5)
    else:
        ll=getallpricecategroy(l)
        pricelist=zzprice.getpricelist(frompageCount=0,limitNum=5,allnum=5,category_id=ll)
    return HttpResponse(simplejson.dumps(pricelist, ensure_ascii=False))
#城市联动
def provincejson(request):
    list=provincejs()
    #return HttpResponse(list)
    return HttpResponse(simplejson.dumps(list, ensure_ascii=False))
#app版本更新
def appversion(request):
    systemType=request.GET.get("systemType")
    appVersion=request.GET.get("appVersion")
    if not systemType:
        systemType="androd"
    if systemType.lower()=="ios":
        if appVersion:
            #判断ios当前版本号是否存在，如果不存在就去读取 id=2 的数据
            sql="select app_versionupdate.update,closed,version,versionDes,closeTip,updateTip,source from app_versionupdate where version=%s"
            alist = dbc.fetchonedb(sql,[appVersion])
            if alist:
                #如果存在且，更新状态为   1 那么是给IOS审核用的版本，直接返回审核版本
                #如果审核通过，将其状态更新为0
                a=0
                if alist[1]==0:
                    sql="select app_versionupdate.update,closed,version,versionDes,closeTip,updateTip,source from app_versionupdate where id=2"
                    alist = dbc.fetchonedb(sql)
            else:
                sql="select app_versionupdate.update,closed,version,versionDes,closeTip,updateTip,source from app_versionupdate where id=2"
                alist = dbc.fetchonedb(sql)
        else:
            sql="select app_versionupdate.update,closed,version,versionDes,closeTip,updateTip,source from app_versionupdate where id=2"
            alist = dbc.fetchonedb(sql)
    else:
        sql="select app_versionupdate.update,closed,version,versionDes,closeTip,updateTip,source from app_versionupdate where id=1"
        alist = dbc.fetchonedb(sql)
    if alist:
        list={'update':alist[0],'closed':alist[1],'version':alist[2],'versionDes':alist[3],'closeTip':alist[4],'updateTip':alist[5],'source':alist[6]}
    else:
        list=None
    return HttpResponse(simplejson.dumps(list, ensure_ascii=False))
    
def wxpay(request):
    out_trade_no=request.POST.get("out_trade_no")
    total_fee=request.POST.get("total_fee")
    qr_wxpay = Wxpay(appid='wx6bb99d2f0581b5b0',
                   mch_id='1340905101',
                   key='OR3g3vtcNAdvm25ycHKfH5KWrLY9kAvd')
    args = {
        'body': u'再生钱包充值',
        'out_trade_no': out_trade_no,
        'total_fee': total_fee,
        'spbill_create_ip':'120.26.66.166',
        'notify_url':'http://m.zz91.com/zz91payverify_notify.html'
    }
    ret_xml=qr_wxpay.generate_prepay_order(args=args)
    #{"trade_type": "APP", "prepay_id": "wx20160706161342696a983ddb0086129855", "nonce_str": "OqoQTS6lpaSG8Bzi", "device_info": "WEB", "return_msg": "OK", "return_code": "SUCCESS", "mch_id": "1340905101", "appid": "wx6bb99d2f0581b5b0", "sign": "73DD26B5B86773E9A060010AE874BB49", "result_code": "SUCCESS"}
    wxd=qr_wxpay.generate_call_app_data(ret_xml['prepay_id'])
    wxdata={
        'apiKey': wxd['appid'],
        'orderId': ret_xml['prepay_id'],
        'mchId': ret_xml['mch_id'],
        'nonceStr': wxd['noncestr'],
        'timeStamp': wxd['timestamp'],
        'package': 'Sign=WXPay',
        'sign': wxd['sign']
    }
    return HttpResponse(simplejson.dumps(wxdata, ensure_ascii=False))
    #return HttpResponse(ret_xml)
#保存搜索关键字
def savekeywords(request):
    clientid=request.GET.get("clientid")
    appsystem=request.GET.get("appsystem")
    company_id=request.GET.get('company_id')
    keywords=request.GET.get('keywords')
    ktype=request.GET.get('ktype')
    if not company_id:
        company_id=0
    updatesearchKeywords(clientid,company_id,keywords,ktype="trade")
    return HttpResponse(simplejson.dumps({'err':''}, ensure_ascii=False))
#获得用户搜索历史
def getkeywords(request):
    clientid=request.GET.get("clientid")
    appsystem=request.GET.get("appsystem")
    company_id=request.GET.get('company_id')
    listall=[]
    if clientid:
        sql="select ktype,keywords from app_user_keywords where appid=%s order by id desc limit 0,20 "
        result=dbc.fetchalldb(sql,[clientid])
        if result:
            for list in result:
                l={'ktype':list[0],'keywords':list[1]}
                listall.append(l)
    return HttpResponse(simplejson.dumps(listall, ensure_ascii=False))
#智能搜索提示
def searchtis(request):
    #-------------智能搜索提示
    keywords = request.GET.get("keywords")
    listall=[]
    if keywords:
        port = spconfig['port']
        cl = SphinxClient()
        cl.SetServer ( spconfig['serverid'], port )
        cl.SetMatchMode ( SPH_MATCH_BOOLEAN )
        cl.SetSortMode( SPH_SORT_EXTENDED,"showcount desc" )
        cl.SetLimits (0,10,10)
        res = cl.Query ('@(label,pingyin) '+keywords,'daohangkeywords')
        if res:
            if res.has_key('matches'):
                keylist=res['matches']
                listall_keywordsearch=[]
                for match in keylist:
                    id=match['id']
                    attrs=match['attrs']
                    tags=attrs['plabel']
                    list1={'keywords':tags}
                    listall_keywordsearch.append(list1)
                listall=listall_keywordsearch
    return HttpResponse(simplejson.dumps(listall, ensure_ascii=False))

#广告是否打开
def ggopen(request):
    ggtype=request.GET.get("ggtype")
    company_id=request.GET.get("company_id")
    clientid=request.GET.get("clientid")
    if ggtype=="hongbao":
        if company_id and company_id!=0:
            sql="select id,bnum,jiangpin from subject_choujiang where company_id=%s and btype='20111009'"
            result=dbc.fetchonedb(sql,[company_id])
            if result:
                jsonlist={'openflag':1,'err':'false'}
            else:
                jsonlist={'openflag':0,'err':'false'}
            return HttpResponse(simplejson.dumps(jsonlist, ensure_ascii=False))
        else:
            jsonlist={'openflag':0,'err':'false'}
            return HttpResponse(simplejson.dumps(jsonlist, ensure_ascii=False))
    else:
        jsonlist={'openflag':1,'err':'false'}
        return HttpResponse(simplejson.dumps(jsonlist, ensure_ascii=False))
    
    