#-*- coding:utf-8 -*-
import MySQLdb
import settings
from settings import pyuploadpath,pyimgurl,spconfig
from zz91settings import SPHINXCONFIG
import codecs,json
from django.utils.http import urlquote

import simplejson
from django.shortcuts import render_to_response
from django.template.loader import get_template
from django.template import Context
from django.http import HttpResponse,HttpResponseRedirect,HttpResponseNotFound,HttpResponsePermanentRedirect
from django.core.paginator import Paginator,InvalidPage,EmptyPage,PageNotAnInteger
from zz91tools import subString,filter_tags,formattime,int_to_datetime,date_to_int
import time
import sys
import datetime,md5,hashlib
from datetime import timedelta,date 
import os
import urllib
from urllib import unquote
from operator import itemgetter, attrgetter
from dict2xml import dict2xml


from django.core.cache import cache
import random
import shutil
import chardet
try:
    import cPickle as pickle
except ImportError:
    import pickle
from math import ceil
#验证码
import memcache
import qrcode,six
import Image,ImageDraw,ImageFont,ImageFilter
try:
    import cStringIO as StringIO
except ImportError:
    import StringIO
from xml.etree import ElementTree as ET


from sphinxapi import *
from zz91page import *
from alipay import Alipay
from zz91db_ads import adsdb
from zz91db_ast import companydb
from zz91db_taozaisheng import taozaishengdb
from zz91db_2_news import newsdb
import requests
#--易宝支付
from SmsWap.SmsWap import MerchantAPI
import SmsWap.Gl as Gl
import pingpp
dbc=companydb()
dbn=newsdb()
dbads=adsdb()
dbtzs=taozaishengdb()

reload(sys)
sys.setdefaultencoding('UTF-8')
nowpath=os.path.dirname(__file__)
execfile(nowpath+"/commfunction.py")
execfile(nowpath+"/function.py")
execfile(nowpath+"/func/weixin_function.py")
execfile(nowpath+"/func/qianbao_function.py")
execfile(nowpath+"/func/ldb_weixin_function.py")
execfile(nowpath+"/func/myrc_function.py")
zzq=qianbao()
zzm=zmyrc()
execfile(nowpath+"/yzm.py")
execfile(nowpath+"/views_app.py")


def price301(request,typeid='',page='',page1='',id="",assist_id="",typeid1='',typeid2='',typeid3=''):
    jumpurl='http://m.zz91.com/'
    #if 'a' in typeid:
        #assist_id=typeid
        #typeid=''
    if typeid!="":
        #typeid=re.findall('[\d]+',typeid)[0]
        jumpurl+="priceindex/"+typeid+".html"
    else:
        if (id!=""):
            jumpurl+="priceviews/?id="+str(id)
        if (assist_id):
            #assist_id=re.findall('[\d]+',assist_id)[0]
            jumpurl+="priceindex/p"+assist_id+".html"
    """
    if typeid:
        pinyin=zzprice.getpricecategorypinyin(typeid)
        pinyin=pinyin.replace('-','_')
        pinyin=pinyin.replace('/','_')
        jumpurl+=pinyin+'/'
    """
    return HttpResponsePermanentRedirect(jumpurl)
def offerlist301(request):
    jumpurl='http://m.zz91.com/'
    ustring=request.META.get('QUERY_STRING','/')
    
    return HttpResponsePermanentRedirect(jumpurl+"trade/?"+ustring)

def goback(request):
    backurl=request.GET.get('backurl')
    return HttpResponseRedirect(backurl)

def addrecordeddata(request):
    company_id=request.session.get("company_id",None)
    gmt_created=datetime.datetime.now()
    weburl=request.GET.get('weburl')
    recordeddata(company_id,gmt_created,weburl)
    return HttpResponse("suc")
def wtext(request):
    return render_to_response('zz91weixin/test.html',locals())

def province(request):
    return render_to_response('aui/comm/province.html',locals())
def ajaxTopbbs(request):
    tp = request.GET.get("tp")
    bbslistvalue=getindexbbslist(kname=None,limitcount=5,bbs_post_category_id=int(tp))
    moreurl="/huzhu/"
    morename="更多"
    listvalue=[]
    for list in bbslistvalue:
        list1={"url":"/huzhuview/"+str(list['id'])+".htm","txt":str(list['title'])}
        listvalue.append(list1)
    return render_to_response('json.html',locals())

def ajaxTopprice(request):
    pricelist=getindexpricelist(kname=None,limitcount=5,titlelen=100)
    moreurl="/price/"
    morename="更多报价"
    listvalue=[]
    for list in pricelist:
        list1={"url":"/priceviews/?id="+str(list['id']),"txt":str(list['title'])}
        listvalue.append(list1)
    return render_to_response('json.html',locals())

def newdefault(request):
    username=request.session.get("username",None)
    categorylist=getindexcategorylist('____',2)
    bbslist=getindexbbslist(kname=None,limitcount=5,bbs_post_category_id=1)
    bbslist4=getindexbbslist(kname=None,limitcount=5,bbs_post_category_id=4)
    pricelist=getindexpricelist(kname=None,limitcount=5,titlelen=100)
    return render_to_response('default.html',locals())

def default(request):
    webtitle="ZZ91手机站"
    username=request.session.get("username",None)
    company_id=request.session.get("company_id",None)
    if (str(username)=="None"):
        username=""
    #ccount1=getsyproductslist("废金属",0,1,None)["count"]
    #ccount2=getsyproductslist("废塑料",0,1,None)["count"]
    #ccountall=getsyproductslist(None,0,1,None)["count"]
    #ccount3=ccountall-ccount1-ccount2
    bbslist=getindexbbslist(kname=None,limitcount=5,bbs_post_category_id=3)
    pricelist=getindexpricelist(kname=None,limitcount=5,titlelen=100)
    return render_to_response('new/index.html',locals())

#----首页(一期)
def default2(request):
    host=getnowurl(request)
    index=1
    webtitle="ZZ91手机站"
    username=request.session.get("username",None)
    company_id=request.session.get("company_id",None)
    if (str(username)=="None"):
        username=""
    categorycodelist=getindexcategorylist('1000',1)
    return render_to_response('new/index2.html',locals())


#----微站列表
def smallsite(request,page=''):
    webtitle="微站"
    nowlanmu="<a href='/laidianbao/'>微站客户</a>"
    host=getnowurl(request)
    username=request.session.get("username",None)
    if (page=='' or page==0):
        page=1
    funpage=zz91page()
    limitNum=funpage.limitNum(8)
    nowpage=funpage.nowpage(int(page))
    frompageCount=funpage.frompageCount()
    after_range_num = funpage.after_range_num(5)
    before_range_num = funpage.before_range_num(4)
    newslist=getcompanysmallsite(frompageCount,limitNum)
    listcount=0
    if (newslist):
        listall=newslist['list']
        listcount=newslist['count']
        if (int(listcount)>1000000):
            listcount=1000000-1
    listcount = funpage.listcount(listcount)
    page_listcount=funpage.page_listcount()
    firstpage = funpage.firstpage()
    lastpage = funpage.lastpage()
    page_range  = funpage.page_range()
    nextpage = funpage.nextpage()
    prvpage = funpage.prvpage()
    return render_to_response('new/smallsite.html',locals())

#----来电宝列表
def laidianbao(request,page=''):
    webtitle="来电宝"
    nowlanmu="<a href='/laidianbao/'>来电宝客户</a>"
    host=getnowurl(request)
    username=request.session.get("username",None)
    if (page=='' or page==0):
        page=1
    funpage=zz91page()
    limitNum=funpage.limitNum(8)
    nowpage=funpage.nowpage(int(page))
    frompageCount=funpage.frompageCount()
    after_range_num = funpage.after_range_num(5)
    before_range_num = funpage.before_range_num(4)
    newslist=getlaidianbao(frompageCount,limitNum)
    listcount=0
    if (newslist):
        listall=newslist['list']
        listcount=newslist['count']
        if (int(listcount)>1000000):
            listcount=1000000-1
    listcount = funpage.listcount(listcount)
    page_listcount=funpage.page_listcount()
    firstpage = funpage.firstpage()
    lastpage = funpage.lastpage()
    page_range  = funpage.page_range()
    nextpage = funpage.nextpage()
    prvpage = funpage.prvpage()
    return render_to_response('new/laidianbao.html',locals())

def category(request):
    host=getnowurl(request)
    webtitle="供求类别"
    showpost=1
    nowlanmu="<a href='/category/'>供求分类</a>"
    code = request.GET.get("code")
    datatype = request.GET.get("datatype")
    username=request.session.get("username",None)
    if (code==None):
        code='____'
        categorylist=getindexcategorylist(code,2)
        if datatype=="json":
            return HttpResponse(simplejson.dumps(categorylist, ensure_ascii=False))
        return HttpResponsePermanentRedirect("/trade/")
        return render_to_response('trade/index.html',locals())
    else:
#        code=str(code)+'____'
        categorylist=getindexcategorylist(code,1)
        if datatype=="json":
            return HttpResponse(simplejson.dumps(categorylist, ensure_ascii=False))
        return HttpResponsePermanentRedirect("/trade/")
        return render_to_response('trade/categorymore.html',locals())
#    return render_to_response('category.html',locals())

def category2(request):
    host=getnowurl(request)
    webtitle="供求类别"
    nowlanmu="<a href='/category/'>供求分类</a>"
    code = request.GET.get("code")
    username=request.session.get("username",None)
    if (code==None):
        code='____'
    else:
        code=str(code)+'____'
    categorylist=getindexcategorylist(code,2)
    return render_to_response('category2.html',locals())

def service(request):
    host=getnowurl(request)
    webtitle="ZZ91服务"
    nowlanmu="<a href='/huzhu/'>再生互助</a>"
    username=request.session.get("username",None)
    return render_to_response('new/service.html',locals())
#----供求列表(排序最复杂)
def offerlist(request):
    #shoprolist=getshoprolist()
    showpost=1
    arealist=['浙江','广东','江苏','福建','安徽','河南','河北','湖北','湖南','四川','江西','山东','海南','黑龙江','北京','上海','天津','青海','陕西','山西','贵州','辽宁','宁夏','吉林','内蒙古','广西','云南','西藏','重庆','甘肃','新疆','台湾','香港','澳门']
    host=getnowurl(request)
    #alijsload="1"
    nowlanmu="<a href='/category/'>供求类别</a>"
    page = request.GET.get("page")
    if (page == None or page=='' or page=="None"):
        page = 1
    nowsearcher="offersearch_new"
    keywords = request.GET.get("keywords")#搜索
    if (keywords):
        keywords=keywords.replace("+","")
        keywords=keywords.replace("\\","")
        keywords=keywords.replace("#","")
        keywords=keywords.replace(")","")
        keywords=keywords.replace("(","")
    keywords_real = keywords#搜索
    keywords111=str(host)
    arrkey=keywords111.split("keywords=")
    if len(arrkey)>1:
        keywords111=arrkey[1]
        arrkey=keywords111.split("^and^")
        keywords111=arrkey[0]
    #keywords111="ppr%D4%D9%C9%FA%BF%C5%C1%A3"
    charttype=chardet.detect(urllib.unquote(str(keywords111)))['encoding']
    #keywords111=charttype
    if charttype:
        if ("utf" not in charttype):
            keywords=urllib.unquote(str(keywords111)).decode('gb2312','ignore').encode('utf-8')
    if not keywords:
        keywords=keywords_real
    if keywords:
        adlist=getadlistkeywords("736",keywords)
    if keywords:
        webtitle=keywords+"_供求列表"
    if keywords=='None' or keywords=='':
        webtitle="供求列表"
        keywords=''
    company_id=request.session.get("company_id",None)
    if company_id:
        #----判断是否为来电宝用户,获取来电宝余额
        isldb=None
        viptype=getviptype(company_id)
        if viptype=='10051003':
            isldb=1
            ldbblance=getldblaveall(company_id,"")
            qianbaoblance=ldbblance
        else:
            qianbaoblance=getqianbaoblance2(company_id,"")
    username=request.session.get("username",None)
    searchname = urlquote(request.GET.get("searchname"))
    pdt_kind = request.GET.get("ptype")
    province = request.GET.get("province")
    provincecode = request.GET.get("provincecode")
    posttime = request.GET.get("posttime")
    pdtidlist = request.GET.get("pdtidlist")
    priceflag = str(request.GET.get("priceflag"))
    nopiclist = request.GET.get("nopiclist")
    tfromdate = request.GET.get("fromdate")
    ttodate = request.GET.get("todate")
    jmsearchname = request.GET.get("jmsearchname")
    fromsort = request.GET.get("fromsort")
    
    for ltt0 in ['供应','出售','卖']:
        if ltt0 in keywords:
            keywords=keywords.replace(ltt0,'')
            pdt_kind='1'
    for ltt1 in ['求购','回收','买','收购']:
        if ltt1 in keywords:
            keywords=keywords.replace(ltt1,'')
            pdt_kind='2'
    
    forcompany_id = request.GET.get("company_id")
    havepic = request.GET.get("havepic")
    haveprice = request.GET.get("haveprice")
    isding=1
    if havepic or haveprice:
        isding=''
    pdt_kindname=''
    if pdt_kind=='1':
        pdt_kindname='供应'
    if pdt_kind=='2':
        pdt_kindname='求购'
    nowlanmu2=pdt_kindname
    if haveprice:
        nowlanmu2+='－ 价格'
    if havepic:
        nowlanmu2+='－ 图片'
    #----时间筛选
    timearg = request.GET.get("timearg")
    if timearg:
        gmt_end=int(time.time())
        if timearg=='1':
            gmt_begin=gmt_end-24*3600
        elif timearg=='2':
            gmt_begin=gmt_end-24*3600*3
        elif timearg=='3':
            gmt_begin=gmt_end-24*3600*7
        elif timearg=='4':
            gmt_begin=gmt_end-24*3600*30
        elif timearg=='5':
            gmt_begin=gmt_end-24*3600*60
    else:
        timearg=''

    if (str(page)=='1' or page=='' or str(page)=='None'):
        pdtidlist=keywordsTop(keywords)
    else:
        pdtidlist=""

    #‘’‘’‘’‘’‘’‘’‘’‘
    if (nopiclist=='' or nopiclist==None or nopiclist=='None'):
        nopiclist=None
        offerFilterListPicInfo_class="offerFilterListPicInfo"
    else:
        offerFilterListPicInfo_class="offerFilterListPicInfo_long"
    #获得相关类别
    categorylist=getcategorylist(kname=keywords,limitcount=20)
    if (pdtidlist!=None and pdtidlist!=''):
        #arrpdtidlist=pdtidlist.split(',')
        arrpdtidlist=pdtidlist
        listall=[]
        n=1
        for p in arrpdtidlist:
            if (p!=''):
                list1=getcompinfo(p[0],"",keywords,company_id)
                m=1
                if (n<=1):
                    m=1
                elif(n>1 and n<=3):
                    m=2
                elif (n>3 and n<=7):
                    m=3
                if (list1!=None):
                    list1['vippaibian']=str(m)
                    n+=1
                    listall.append(list1)
        productListtop=listall
    
    #--------------------------------------------
    if (province=='' or province == None):
        province=''
        
    if (pdt_kind == '' or pdt_kind == None or pdt_kind=="0"):
        pdt_type=''
        pdt_kind='0'
        stab1="offerselect"
        stab2=""
        stab3=""
    if (pdt_kind =='1'):
        pdt_type='0'
        stab1=""
        stab2="offerselect"
        stab3=""
    if (pdt_kind=='2'):
        pdt_type='1'
        stab1=""
        stab2=""
        stab3="offerselect"
    
    
    nowpage=int(page)
    page=20*(int(page)-1)
    keywords2=keywords.replace('|','')
    keywords2=keywords2.replace(' ','')
    
    keywords1=urlquote(keywords2)
    ttype = request.GET.get("ttype")
    keywords=keywords.replace('|',' ')
    keywords=keywords.replace('\\',' ')
    keywords=keywords.replace('/',' ')
    keywords=keywords.replace('/',' ')
    keywords=keywords.replace('(',' ')
    keywords=keywords.replace(')',' ')
    seo_keywords=keywords
    if (ttype==None):
        ttype=''
    if (posttime==None):
        posttime=''
    if (priceflag==None or str(priceflag)=='None'):
        priceflag=''
    if (nopiclist==None or str(nopiclist)=='None'):
        nopiclist=''
    if (havepic==None or str(havepic)=='None'):
        havepic=''
    #action = '&keywords='+searchname+'&ptype='+pdt_kind+'&province='+urlquote(province)+'&posttime='+str(posttime)+'&ttype='+str(ttype)+'&priceflag='+str(priceflag)+'&nopiclist='+str(nopiclist)+'&jmsearchname='+str(jmsearchname)+'&havepic='+str(havepic)+'&fromsort='+str(fromsort)
    #a(\d*)--b(\d*)--c(\d*)--d(\d*)--e(\d*)--f(\d*)
    action='a'+str(pdt_kind)+'--b'+str(provincecode)+'--c'+str(posttime)+'--d'+str(priceflag)+'--e'+str(nopiclist)+'--f'+str(havepic)+''
    searchname=str(keywords1)
    searchname=searchname.replace('%28','astokhl')
    searchname=searchname.replace('%29','astokhr')
    searchname=searchname.replace('%5C','asto5c')
    searchname=searchname.replace('/','astoxg')
    searchname=searchname.replace('-','astohg')
    after_range_num = 8
    before_range_num = 9
    port = spconfig['port']

    #----------------------------
    cl = SphinxClient()
    cl = SphinxClient()
    list = SphinxClient()
    
    cl.SetServer ( spconfig['serverid'], port )
    list.SetServer ( spconfig['serverid'], port )
    cl.SetMatchMode ( SPH_MATCH_BOOLEAN )
    list.SetMatchMode ( SPH_MATCH_BOOLEAN )
    
    #取得总数
    nowdate=date.today()-timedelta(days=2)
    nextday=date.today()+timedelta(days=2)
    formatnowdate=time.mktime(nowdate.timetuple())
    formatnextday=time.mktime(nextday.timetuple())
    searstr=''
    
    if (pdt_kind !='0'):
        searstr+=";filter=pdt_kind,"+pdt_type
        cl.SetFilter('pdt_kind',[int(pdt_type)])
        list.SetFilter('pdt_kind',[int(pdt_type)])
        
    if(havepic=='1'):
        cl.SetFilterRange('havepic',1,100)
        list.SetFilterRange('havepic',1,100)
    #list.SetFilter('viptype',[0],True)
    #cl.SetFilter('offerstaus',[0])
    #list.SetFilter('offerstaus',[0])
    if (ttype == '1'):    
        cl.SetFilterRange('pdt_date',int(formatnowdate),int(formatnextday))
        list.SetFilterRange('pdt_date',int(formatnowdate),int(formatnextday))
        #searstr+=' ;range=refresh_time,'+str(formatnowdate)+','+str(formatnextday)+''
        
    if (posttime =='' or posttime==None or posttime=='None'):
        searstr +=''
    else:
        pfromdate=date.today()-timedelta(days=int(posttime)+1)
        #test=str(time.mktime(pfromdate.timetuple()))
        ptodate=date.today()+timedelta(days=3)
        
        pfromdate_int=int(time.mktime(pfromdate.timetuple()))
        ptodate_int=int(time.mktime(ptodate.timetuple()))
        if (pfromdate!=None):
            cl.SetFilterRange('pdt_date',int(pfromdate_int),int(ptodate_int))
            list.SetFilterRange('pdt_date',int(pfromdate_int),int(ptodate_int))
        #searstr += ';refresh_time,'+str(pfromdate_int)+','+str(ptodate_int)+''
    if timearg:
        cl.SetFilterRange('pdt_date',gmt_begin,gmt_end)
        list.SetFilterRange('pdt_date',gmt_begin,gmt_end)
    if haveprice:
        cl.SetFilterRange('length_price',4,10000)
        list.SetFilterRange('length_price',4,10000)
        cl.SetFilter('haveprice',[1],True)
        list.SetFilter('haveprice',[1],True)
    if forcompany_id:
        forcompany_id=int(forcompany_id)
        cl.SetFilter('company_id',[forcompany_id])
        list.SetFilter('company_id',[forcompany_id])
        forcompany_name=getppccompanyinfo(forcompany_id)
        if forcompany_name:
            forcompany_name=forcompany_name['companyname']
        seo_keywords=forcompany_name
    
    if (province ==None or province ==''):
        provincestr=''
    else:
        provincestr='&@(province,city) '+province

    if (priceflag == '1'):
        cl.SetFilter('length_price',[0],True)
        list.SetFilter('length_price',[0],True)
        list.SetSortMode( SPH_SORT_EXTENDED,"length_price desc,refresh_time desc" )
    elif (priceflag == '2'):
        list.SetFilter('length_price',[0],True)
        list.SetSortMode( SPH_SORT_EXTENDED,"length_price asc,refresh_time desc" )
    else:
        list.SetSortMode( SPH_SORT_EXTENDED,"refresh_time desc" )
    if keywords=='':
        res = list.Query ('',nowsearcher)
    else:
        res = list.Query ( '@(title,label0,label1,label2,label3,label4,city,province,tags) '+keywords+provincestr+'',nowsearcher)
    if not res:
        listcount=0
    else:
        listcount=res['total_found']
    
    cl.SetFilterRange('viptype',1,5)
    #cl.SetFilterRange('Prodatediff',0,3)
    
    #获得3天内再生通数据优先排序
    #listallvip=cache.get('list'+action)
    
    cl.SetSortMode( SPH_SORT_EXTENDED,"company_id desc,refresh_time desc" )
    cl.SetLimits (0,100000,100000)
    if keywords=='':
        rescount = cl.Query ('','offersearch_new_vip')
    else:
        rescount = cl.Query ( '@(title,label0,label1,label2,label3,label4,city,province,tags) '+keywords+provincestr+'','offersearch_new_vip')
    pcount=0
    listall=[]
    if rescount:
        if rescount.has_key('matches'):
            tagslist=rescount['matches']
            testcom_id=0
            pcount=100000
            for match in tagslist:
                id=match['id']
                com_id=match['attrs']['company_id']
                viptype=match['attrs']['viptype_ldb']
                phone_rate=int(match['attrs']['phone_rate'])
                phone_num=int(match['attrs']['phone_num'])
                phone_fee=float(match['attrs']['phone_cost'])
                refresh_time=float(match['attrs']['refresh_time'])
                pdt_date=float(match['attrs']['pdt_date'])
                phone_level=float(match['attrs']['phone_level'])
                if (testcom_id==com_id):
                    pcount-=1
                else:
                    pcount=100000
                phone_sort=100
                if str(viptype)=="6":
                    if int(phone_rate)>=75:
                        phone_sort=100
                    else:
                        phone_sort=2
                
                #if phone_num==10000:
                    #phone_sort=10000;
                #else:
                    #phone_sort=phone_rate*0.05+phone_num*0.85+phone_fee*0.1
                list1=(id,pcount,viptype,refresh_time,pdt_date,phone_sort,phone_level)
                listall.append(list1)
                testcom_id=com_id
    listallvip=sorted(listall, key=itemgetter(1,4,5,2,6,3),reverse=True)
    #listallvip=tradeorderby(listall)
    
    #cache.set('list'+action, listallvip, 15*60)
    #优先排序数
    viplen=len(listallvip)
    
    #供求总数
    listcount+=int(viplen)
    #最后一页的供求数
    lastpNum=int(viplen-ceil(viplen / 20)*20)
    #开始供求数位置
    beginpage=page
    #优先排序页码
    pageNum=0
    if (lastpNum==0):
        pageNum=int(ceil(viplen / 20))
    else:
        pageNum=int(ceil(viplen / 20)+1)
    
    #结束供求数位置
    if (int(nowpage)==int(pageNum) and lastpNum!=0):
        endpage=int(page+lastpNum)
    elif(int(nowpage)==int(pageNum) and lastpNum==0 and int(nowpage)==1):
        endpage=20
    elif(int(nowpage)==int(pageNum) and lastpNum==0):
        endpage=int(page)
    else:
        endpage=page+20
    #列出供求信息列表
    listall=[]
    for match in listallvip[beginpage:endpage]:
        list1=getcompinfo(match[0],"",keywords2,company_id)
        listall.append(list1)
    productList=listall
    
    #普通供求开始数
    offsetNum=0
    limitNum=20
    if (nowpage==pageNum and lastpNum!=0):
        offsetNum=0
        limitNum=20-lastpNum
        notvip=1
    elif (nowpage==pageNum and lastpNum==0 and viplen>0):
        offsetNum=0
        limitNum=20-lastpNum
        notvip=0
    elif (nowpage==pageNum and lastpNum==0 and viplen==0):
        offsetNum=0
        limitNum=20
        notvip=1
    elif (nowpage>pageNum and lastpNum==0):
        offsetNum=(nowpage-pageNum-1)*20
        limitNum=20-lastpNum
        notvip=1
    elif(nowpage>pageNum and lastpNum>0):
        offsetNum=((int(nowpage)-int(pageNum)-1)*20)+(20-int(lastpNum))
        limitNum=20
        notvip=1
    elif (viplen<1):
        offsetNum=(nowpage-1)*20
        limitNum=20
        notvip=1
    else:
        notvip=0
    #优先排序供求结束页的
    #test=str(lastpNum)+'|'+str(pageNum)+'|'+str(offsetNum)+'|'+str(limitNum)
    
    if (nowpage==pageNum and lastpNum!=0):
        listall=productList
    else:
        listall=[]
    if (notvip==1):
        list.SetLimits (offsetNum,limitNum,100000)
        if keywords=='':
            res = list.Query ('',nowsearcher)
        else:
            res = list.Query ('@(title,label0,label1,label2,label3,label4,city,province,tags) '+keywords+provincestr+'',nowsearcher)

        if res:
            if res.has_key('matches'):
                prodlist=res['matches']
                for list in prodlist:
                    id=list['id']
                    list1=getcompinfo(id,"",keywords2,company_id)
                    listall.append(list1)
                productList=listall

    #cache.set('productList', productList, 300)
    #底部页码
    #connt.close()
    try:
        page = int(request.GET.get('page',1))
        if page < 1:
            page = 1
    except ValueError:
            page = 1
    page_listcount=int(ceil(listcount / 20))+1
    page_rangep=[]
    i=1
    while (i<=page_listcount):
        pages={'number':'','nowpage':''}
        pages['number']=i
        if (i==page):
            pages['nowpage']='1'
        else:
            pages['nowpage']=None
            
        page_rangep.append(pages)
        i+=1
    if (page_listcount>1 and page>1):
        firstpage=1
    else:
        firstpage=None
    if (page<page_listcount and page_listcount>1):
        lastpage=1
    else:
        lastpage=None
    if page >= after_range_num:
        page_range = page_rangep[page-after_range_num:page + before_range_num]
    else:
        page_range = page_rangep[0:int(page) + before_range_num]
    nextpage=page+1
    prvpage=page-1
    #大于500页提示

    if(page_listcount>500 and page>=500):
        arrtishi="提示：为了提供最相关的搜索结果，ZZ91再生网只显示500页信息，建议您重新搜索！"
    else:
        arrtishi=None
    return render_to_response('trade/list.html',locals())

def reginfo(request):
    return render_to_response('aui/myrc/reginfo.html',locals())
#注册页面
def register(request):
    backurl=request.META.get('HTTP_REFERER','/')
    host=getnowurl(request)
    t=random.randrange(0,1000000)
    username=request.session.get("username",None)
    weixinid=request.GET.get("weixinid")
    regfrom=request.GET.get("regfrom")
    if not regfrom:
        regfrom=''
    if not weixinid:
        weixinid=""
    return render_to_response('aui/user/reg.html',locals())
    #return render_to_response('reg.html',locals())
def regsecond(request):
    backurl = request.GET.get('backurl')
    webtitle="ZZ91会员注册"
    if not backurl or backurl=="None" or backurl=="/":
        backurl="/myrc_index/"
    nowlanmu="<a href='/register/'>会员注册</a>"
    username=request.session.get("username",None)
    company_id=request.session.get("company_id",None)
    
    areaCode="10011000"
    return render_to_response('aui/user/regsecond.html',locals())
def regsuccess(request):
    backurl = request.GET.get('backurl')
    webtitle="ZZ91会员注册"
    if not backurl or backurl=="None" or backurl=="/":
        backurl="/myrc_index/"
    username=request.session.get("username",None)
    company_id=request.session.get("company_id",None)
    return render_to_response('aui/user/regsuccess.html',locals())
    #return render_to_response('reg_second.html',locals())
def regsecond_save(request):
    backurl = request.POST.get('backurl')
    if not backurl or backurl=="None" or backurl=="/":
        backurl="/myrc_index/"
    username=request.session.get("username",None)
    company_id=request.session.get("company_id",None)
    if (username==None or (company_id==None or str(company_id)=="0")):
        errlist={'err':'login'}
        return HttpResponse(simplejson.dumps(errlist, ensure_ascii=False))
    qq = request.POST.get('qq')
    email = request.POST.get('email')
    serviceCode = request.POST.get('serviceCode')
    provincecode = request.POST.get('provincecode')
    companyname = request.POST.get('companyname')
    if not provincecode:
        provincecode="10011000"
    address = request.POST.get('address')
    addresszip = request.POST.get('addresszip')
    #business = request.POST.get('business')
    if company_id:
        value=[companyname,serviceCode,provincecode,address,addresszip,company_id]
        sql="update company set name=%s,service_code=%s,area_code=%s,address=%s,address_zip=%s where id=%s"
        dbc.updatetodb(sql,value);
        if not email:
            email=''
        value1=[email,qq,company_id]
        sql1="update company_account set email=%s,qq=%s where company_id=%s"
        dbc.updatetodb(sql1,value1);
        messagedata={'err':'false','errkey':'','type':'reg'}
        return HttpResponse(simplejson.dumps(messagedata, ensure_ascii=False))
        
    #return render_to_response('reg/regsuc2.html',locals())
    #return HttpResponseRedirect(backurl)
#会员注册保存
def registerSave(request):
    backurl = request.POST.get('backurl')
    userName = request.POST.get('userName')
    passwd = request.POST.get('passwd')
    contact = request.POST.get('contact')
    sex = request.POST.get('sex')
    business = request.POST.get('business')
    weixinid=request.POST.get("weixinid")
    products_type_code=request.POST.get("products_type_code")
    regfrom=request.POST.get("regfrom")
    industry_code=request.POST.get("industry_code")
    mobile=userName
    email=mobile+"@139.com"
    regtime=gmt_created=datetime.datetime.now()
    gmt_modified=datetime.datetime.now()
    errflag=0
    errtext1=''
    if userName:
        if (userName=='' or userName.isdigit()==False):
            errtext1="必须填写 手机号码"
            errflag=1
    else:
        errtext1="必须填写 手机号码"
        errflag=1
    if (len(userName)<=10):
        errtext1="填写手机号码必须大于11位"
        errflag=1
    if (passwd==''):
        errtext1="必须填写 密码"
        errflag=1
    if (not contact):
        errtext1="必须填写 联系人"
        errflag=1
    if (business=='' or products_type_code==''):
        errtext1="必须填写主营产品和供求类型"
        errflag=1
    if (errflag==0):
        #''判断邮箱帐号是否存在
        sql="select id  from auth_user where username=%s"
        accountlist=dbc.fetchonedb(sql,[userName])
        if (accountlist):
            errflag=1
            errtext1="您填写的手机号码已经注册！点此<a href='/weixin/forgetpasswd.html'>找回密码?</a>"
        #''判断邮箱帐号是否存在
        sql="select id  from auth_user where mobile=%s"
        accountlist=dbc.fetchonedb(sql,[userName])
        if (accountlist):
            errflag=1
            errtext1="您填写的手机号码已经注册！点此<a href='/weixin/forgetpasswd.html'>找回密码?</a>"
            
        sql="select id  from company_account where mobile=%s"
        accountlist=dbc.fetchonedb(sql,str(userName))
        if (accountlist):
            errflag=1
            errtext1="您填写的手机号码已经注册！点此<a href='/weixin/forgetpasswd.html'>找回密码?</a>"
        
    if (errflag==0):
        #添加公司信息
        if not industry_code:
            industry_code=''
        #business=''
        compname="("+contact+")"
        service_code=''
        area_code=''
        foreign_city=''
        category_garden_id='0'
        membership_code='10051000'
        classified_code='10101002'
        regfrom_code='10031024'
        if regfrom=="tuiguang":
            regfrom_code="10031043"
        domain=''
        address=''
        address_zip=''
        website=''
        introduction=''
        company_id=0
        value2=[compname, industry_code, products_type_code+business, service_code, area_code, foreign_city, category_garden_id, membership_code,domain, classified_code, regfrom_code,  regtime, gmt_created, gmt_modified,  address, address_zip, website, introduction]
        sql2="insert into company (name, industry_code, business, service_code, area_code, foreign_city, category_garden_id, membership_code,    domain, classified_code, regfrom_code,  regtime, gmt_created, gmt_modified,  address, address_zip, website, introduction)"
        sql2=sql2+" values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)";
        result=dbc.updatetodb(sql2,value2)
        if result:
            company_id=result[0]
        
        if company_id==0:
            errtext1="系统错误，请重新提交信息！"
            errflag=1
        else:
            errtext1=''
            #帐号添加
            md5pwd = hashlib.md5(passwd)
            md5pwd = md5pwd.hexdigest()[8:-8]
            value1=[userName,md5pwd,gmt_created,gmt_modified]
            sql1="insert into auth_user (username,password,gmt_created,gmt_modified) values(%s,%s,%s,%s)"
            dbc.updatetodb(sql1,value1)
            #
            
            is_admin='1'
            tel_country_code=''
            tel_area_code=''
            tel=mobile
    
            fax_country_code=''
            fax_area_code=''
            fax=''
    #        sex=''
            qq=''
            real_name=contact
            nickname=contact
            #'添加联系方式
            value3=[userName, company_id, contact, is_admin, tel_country_code, tel_area_code, tel, mobile, fax_country_code, fax_area_code, fax, email, sex, passwd, gmt_modified, gmt_created]
            sql3="insert into company_account (account, company_id, contact, is_admin, tel_country_code, tel_area_code, tel, mobile, fax_country_code, fax_area_code, fax, email, sex, password, gmt_modified, gmt_created)"
            sql3=sql3+" values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)";
            dbc.updatetodb(sql3,value3);
            #return HttpResponse(company_id)
            #-互助用户表
            sqlh="select id from bbs_user_profiler where company_id=%s"
            userlist=dbc.fetchonedbmain(sqlh,[company_id])
            if (userlist==None):
                value=[company_id,userName,nickname,email,tel,mobile,qq,real_name,gmt_modified,gmt_created]
                sqlu="insert into bbs_user_profiler(company_id,account,nickname,email,tel,mobile,qq,real_name,gmt_modified,gmt_created) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
                dbc.updatetodb(sqlu,value);
            request.session['company_id']=company_id
            request.session['username']=userName
            #自动发布一条供求信息
            category_products_main_code=""
            username=userName
            
            title=products_type_code+business
            details=products_type_code+business
            
            products_type_codea="10331001"
            if products_type_code=="供应":
                products_type_codea="10331000"
            if products_type_code=="求购":
                products_type_codea="10331001"
            products_type_code=products_type_codea
            quantity=""
            quantity_unit=""
            price=""
            price_unit=""
            validitytime='9999-12-31 23:59:59'
            
            sql="insert into products(category_products_main_code,company_id,account,products_type_code,title,quantity,quantity_unit,price,price_unit,details,gmt_created,gmt_modified,real_time,refresh_time,expire_time,source_type_code,location,provide_status,total_quantity,is_show_in_price,source,specification,origin,min_price,max_price,goods_type_code,tags,tags_admin,impurity,color,useful,appearance,remark,old_id) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,'mobile_myrc','','N','',0,'','','',0,0,'','','','','','','','',0)"
            dbc.updatetodb(sql,[category_products_main_code,company_id,username,products_type_code,title,quantity,quantity_unit,price,price_unit,details,gmt_created,gmt_created,gmt_created,gmt_created,validitytime])
            #-微信绑定
            if weixinid:
                sql="select id from oauth_access where open_id=%s and target_account=%s"
                accountlist=dbc.fetchonedb(sql,[weixinid,userName]);
                if (accountlist==None):
                    sql="update oauth_access set closeflag=1 where open_id=%s and open_type=%s"
                    dbc.updatetodb(sql,[weixinid,'weixin.qq.com'])
                    
                    sqlp="insert into oauth_access(open_id,open_type,target_account,gmt_created,gmt_modified) values(%s,%s,%s,%s,%s)"
                    dbc.updatetodb(sqlp,[weixinid,'weixin.qq.com',userName, gmt_created,gmt_modified]);
            messagedata={'err':'false','errkey':errtext1,'type':'reg'}
            return HttpResponse(simplejson.dumps(messagedata, ensure_ascii=False))
            #return HttpResponseRedirect("/user/regsecond.html?backurl="+backurl)
    if (errflag==1):
         messagedata={'err':'true','errkey':errtext1,'type':'reg'}
         return HttpResponse(simplejson.dumps(messagedata, ensure_ascii=False))
    #return render_to_response('reg.html',locals())

def registerSave1(request):
    nowlanmu="<a href='/huzhu/'>再生互助</a>"
    userName = request.POST['userName']
    password1 = request.POST['password1']
    password2 = request.POST['password2']
    email = request.POST['email']
    mobile = request.POST['mobile']
    tel = request.POST['tel']
    company = request.POST['company']
    contact = request.POST['contact']
    productslist = request.POST['productslist']
    t = request.POST['t']
    valcode1 = request.POST['valcode1']
    regtime=gmt_created=datetime.datetime.now()
    gmt_modified=datetime.datetime.now()
    sessonyzm=cache.get("yzm"+str(t))
    
    errflag=0
    if (str(sessonyzm).lower()!=str(valcode1).lower()):
        errtext8="验证码错误"
        errflag=1
    if (userName==''):
        errtext1="必须填写 会员名"
        errflag=1
    if (password1==''):
        errtext2="必须填写 密码"
        errflag=1
    if (password2==''):
        errtext3="必须填写 密码验证"
        errflag=1
    if (email==''):
        errtext4="必须填写 邮箱"
        errflag=1
    if (mobile==''):
        errtext5="必须填写 手机号"
        errflag=1
    if (tel==''):
        errtext6="必须填写 电话"
        errflag=1
    if (company==''):
        errtext7="必须填写 公司名称"
        errflag=1
    if (valcode1==''):
        errtext8="必须填写 验证码"
        errflag=1
    if (contact==''):
        errtext9="必须填写 联系人"
        errflag=1
    if (errflag==0):
        #''判断邮箱帐号是否存在
        sql="select id  from auth_user where username=%s"
        accountlist=dbc.fetchonedb(sql,str(userName))
        if (accountlist):
            errflag=1
            errtext1="您填写的用户名已经存在！请修改用户名后重新提交！"
        sql="select id  from auth_user where email=%s"
        accountlist=dbc.fetchonedb(sql,str(email))
        if (accountlist):
            errflag=1
            errtext4="您填写的邮箱已经注册！请修改邮箱后重新提交！"
        if (password1!=password2):
            errflag=1
            errtext2="两次填写的密码不一致，请重新确认！"
    if (errflag==0):
        #''帐号添加
        md5pwd = hashlib.md5(password1)
        md5pwd = md5pwd.hexdigest()[8:-8]
        value=[userName,md5pwd,email,gmt_created,gmt_modified]
        sql="insert into auth_user (username,password,email,gmt_created,gmt_modified) values(%s,%s,%s,%s,%s)"
        dbc.updatetodb(sql,value)
        #添加公司信息
        industry_code=''
        business=''
        service_code=''
        area_code=''
        foreign_city=''
        category_garden_id='0'
        membership_code='10051000'
        classified_code='10101002'
        regfrom_code='10031024'
        domain=''
        address=''
        address_zip=''
        website=''
        introduction=''
        
        value=[company, industry_code, business, service_code, area_code, foreign_city, category_garden_id, membership_code,domain, classified_code, regfrom_code,  regtime, gmt_created, gmt_modified,  address, address_zip, website, introduction]
        sql="insert into company (name, industry_code, business, service_code, area_code, foreign_city, category_garden_id, membership_code,    domain, classified_code, regfrom_code,  regtime, gmt_created, gmt_modified,  address, address_zip, website, introduction)"
        sql=sql+" values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)";
        dbc.updatetodb(sql,value);
        
        company_id=getcompany_id(company,gmt_created)
        is_admin='1'
        tel_country_code=''
        tel_area_code=''

        fax_country_code=''
        fax_area_code=''
        fax=''
        sex=''
        #'添加联系方式
        if company_id!=0:
            value=[userName, company_id, contact, is_admin, tel_country_code, tel_area_code, tel, mobile, fax_country_code, fax_area_code, fax, email, sex, password1, gmt_modified, gmt_created]
            sql="insert into company_account (account, company_id, contact, is_admin, tel_country_code, tel_area_code, tel, mobile, fax_country_code, fax_area_code, fax, email, sex, password, gmt_modified, gmt_created)"
            sql=sql+" values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)";
            dbc.updatetodb(sql,value);
            return render_to_response('regsuc.html',locals())
        else:
            company_id=1
    if (errflag==1):
        return render_to_response('reg.html',locals())
# 会员登录    
def login(request):
    username=request.session.get("username",None)
    webtitle="登录"
    weixinautologin(request,request.GET.get("weixinid"))
    done= request.GET.get("done")
    if not done:
        done= request.POST.get("done")
    tourlstr=None
    if (done!=None):
        done=done.replace("^and^","&")
        done=done.replace("^wenhao^","?")
        done=done.replace("%5Eand%5E","&")
        done=done.replace("^jing^","#")
        tourlstr="您需要登录后才能操作！"
        if "myrc_index" in done:
            tourlstr="您需要登录后进入生意管家！"
        if "products_publish" in done:
            tourlstr="您需要登录后才能发布信息！"
        if "huzhu" in done:
            tourlstr="您需要登录后才能发布/回复帖子！"
        if "huzhupost" in done:
            tourlstr="您需要登录后才能发布/回复帖子！"
        if "huzhuview" in done:
            tourlstr="您需要登录后才能发布/回复帖子！"
        if "detail" in done:
            tourlstr="您需要登录后才能查看联系方式！"
        if "favorite" in done:
            tourlstr="您需要登录后收藏信息！"
        if "choujiang" in done:
            tourlstr="您需要登录后才可抽奖！"
        if "guaguale" in done:
            tourlstr="您需要登录后才可刮奖！"
    username=request.session.get("username",None)
    company_id=request.session.get("company_id",None)
    if (str(username)=="None"):
        username=""
    #----登录页跳转到注册页后跳转
    if company_id and done:
        return HttpResponseRedirect(done)
    return render_to_response('aui/myrc/login.html',locals())
    #return render_to_response('login.html',locals())
# 会员登录    
def loginredirect(request):
    username=request.session.get("username",None)
    webtitle="登录"
    weixinautologin(request,request.GET.get("weixinid"))
    nowlanmu="<a href='/myrc_index/'>生意管家</a>"
    done= request.GET.get("done")
    if (done!=None):
        done=done.replace("^and^","&")
    username=request.session.get("username",None)
    company_id=request.session.get("company_id",None)
    #username=request.COOKIES.get("username",None)
    #company_id=request.COOKIES.get('company_id',None)
    if (str(username)=="None"):
        username=""
    if (str(username)!=""):
        return HttpResponseRedirect(done)
    return render_to_response('aui/myrc/login.html',locals())
    #return render_to_response('login.html',locals())
#----注销,退出登陆
def loginout(request):
    request.session.delete()
    backurl=request.META.get('HTTP_REFERER','/')
    response=HttpResponseRedirect(backurl)
#    response=HttpResponseRedirect("/")
    #response.set_cookie('username','',max_age=0)
    #response.set_cookie('company_id','',max_age=0)
    return response
def loginof(request):
    gmt_modified=datetime.datetime.now()
    nowlanmu="<a href='/huzhu/'>再生互助</a>"
    done = request.POST.get('done')
    username = request.POST.get('username')
    pwd = request.POST.get('pwd')
    if not pwd:
        error="用户名或密码错误！"
        return render_to_response('aui/myrc/login.html',locals())
    md5pwd = hashlib.md5(pwd)
    md5pwd = md5pwd.hexdigest()[8:-8]
    if username:
        sql="select id,username from auth_user where (username=%s or email=%s or mobile=%s or account=%s) and password=%s"
        plist=dbc.fetchonedb(sql,[username,username,username,username,md5pwd]);
        if plist:
            request.session.set_expiry(6000*6000)
            username=plist[1]
            
            account=plist[1]
            sqlc="select company_id from company_account where account=%s"
            list=dbc.fetchonedb(sqlc,[account]);
            if list:
                company_id=list[0]
                #判断是否拉黑
                sqlh="select id from company where id=%s and is_block=1"
                listh=dbc.fetchonedb(sqlh,[company_id]);
                if listh:
                    error="该用户已经被禁止登录！"
                    return render_to_response('aui/myrc/login.html',locals())
                
                if str(company_id)!="0":
                    request.session['username']=username
                    request.session['company_id']=company_id
                    updatelogin(request,company_id)
            else:
                error="用户名或邮箱 还未注册！"
                return render_to_response('login.html',locals())
            if (done=="" or done=="None"):
                response=HttpResponseRedirect("/myrc/")
                return response
            else:
                response=HttpResponseRedirect(done)
                return response
        else:
            sqlc="select account,company_id from company_account where mobile=%s order by id desc"
            list=dbc.fetchonedb(sqlc,[username]);
            if list:
                account=list[0]
                company_id=list[1]
                #判断是否拉黑
                sqlh="select id from company where id=%s and is_block=1"
                listh=dbc.fetchonedb(sqlh,[company_id]);
                if listh:
                    error="该用户已经被禁止登录！"
                    return render_to_response('aui/myrc/login.html',locals())
                sqlp="select id from auth_user where username=%s and password=%s"
                listp=dbc.fetchonedb(sqlp,[account,md5pwd]);
                if listp:
                    if str(company_id)!="0":
                        request.session.set_expiry(6000*6000)
                        request.session['username']=account
                        request.session['company_id']=company_id
                        updatelogin(request,company_id)
                        if (done=="" or done=="None"):
                            response=HttpResponseRedirect("/myrc/index.html")
                            return response
                        else:
                            response=HttpResponseRedirect(done)
                            return response
                else:
                    error="用户名或密码错误！"
                    return render_to_response('aui/myrc/login.html',locals())
                    #return render_to_response('login.html',locals())
            else:
                error="您的用户名或密码错误，请注意英文大小写！"
                return render_to_response('aui/myrc/login.html',locals())
                #return render_to_response('login.html',locals())
    return render_to_response('aui/myrc/login.html',locals())
    #return render_to_response('login.html',locals())

#用户资料完善,将原有信息填入表单
def dataalter(request):
    saveform="dataalter_ok"
    #nowlanmu="<a href='/dataalter/'>用户资料修改</a>"
    #company_id=request.GET.get("company_id")
    #username=request.session.get("username",None)
    company_id="6713"
    contactinfolist=get_contactinfo(company_id)
    companyinfolist=get_companyinfo(company_id)
    industry_label=getindustrylabel(companyinfolist['industry_code'])
    service_label=getservicelabel(companyinfolist['service_code'])
    
    return render_to_response('main/dataalter.html',locals())
#用户资料完善提交
def dataalter_ok(request):
    """
    company_id=request.session.get("company_id",None)
    username=request.session.get("username",None)
    if (username==None or (company_id==None or str(company_id)=="0")):
        return HttpResponseRedirect("/login/?done=/products_update/")
       """
    company_id=request.POST.get("company_id")
    
    contact = request.POST.get("contact")
    sex = request.POST.get("sex")
    tel_country_code = request.POST.get("tel_country_code")
    tel_area_code= request.POST.get("tel_area_code")
    tel= request.POST.get("tel")
    mobile=request.POST.get("mobile")
    fax_country_code=request.POST.get("fax_country_code")
    fax_area_code=request.POST.get("fax_area_code")
    fax=request.POST.get("fax")
    back_email=request.POST.get("back_email")
    website=request.POST.get("website")
    name=request.POST.get("company_name")
    industrycode=request.POST.get("industrcode")
    servicecode=request.POST.get("servicecode")
    areacode=''
    #地区未写
    #集删地未写
    address=request.POST.get("address")
    address_zip=request.POST.get("address_zip")
    qq=request.POST.get("qq")
    weixin=request.POST.get("weixin")
    msn=request.POST.get("msn")
    introduction=request.POST.get("introduction")
    business=request.POST.get("business")
    
    sql='update company_account set contact=%s,sex=%s,tel_country_code=%s,tel_area_code=%s,tel=%s,fax_country_code=%s,fax_area_code=%s,fax=%s,mobile=%s,back_email=%s,qq=%s,weixin=%s,msn=%s where company_id=%s'
    dbc.updatetodb(sql,[contact,sex,tel_country_code,tel_area_code,tel,fax_country_code,fax_area_code,fax,mobile,back_email,qq,weixin,msn,company_id])
    sql1='update company set name=%s,service_code=%s,industry_code=%s,area_code=%s,address=%s,address_zip=%s,introduction=%s,business=%s,website=%s where id=%s'
    dbc.updatetodb(sql1,[name,servicecode,industrycode,areacode,address,address_zip,introduction,business,website,company_id])
    return render_to_response('main/dataalter_ok.html',locals())



def serviceterms(request):
    host=getnowurl(request)
    webtitle="ZZ91服务"
    username=request.session.get("username",None)
    return render_to_response('serviceterms.html',locals())
#搜索分类
def searchfirst(request):
    host=getnowurl(request)
    searchType = request.GET.get("searchtype")
    keywords=request.GET.get("keywords")
    if (searchType=="price"):
        return HttpResponsePermanentRedirect("/price/?keywords="+str(keywords)+"")
    if (searchType=="selloffer"):
        return HttpResponsePermanentRedirect("/offerlist/?keywords="+str(keywords)+"")
    if (searchType=="company"):
        return HttpResponsePermanentRedirect("/company/?keywords="+str(keywords)+"")
    return render_to_response('kong.html',locals())

def detail(request):
    host=getnowurl(request)
    alijsload="1"
    nowlanmu="<a href='/huzhu/'>返回</a>"
    id=request.GET.get("id")
    done = request.path
    username=request.session.get("username",None)
    company_id=request.session.get("company_id",None)
    iszstflag=getiszstcompany(company_id)
    list=getproductdetail(id)
    if list:
        compzstflag=list['viptype']['vipcheck']
        weixinviewcontactflag=None
        if username:
            scoreopt=weixinscore()
            weixinviewflag=scoreopt.getviewcontact(username)
            if weixinviewflag and compzstflag==None:
                weixinviewcontactflag=1
                scoreopt.saveviewcontact(username,company_id=list['company_id'])
                
        if iszstflag==1 or compzstflag==1 or weixinviewcontactflag==1:
            viewflag=1
        else:
            viewflag=None
        webtitle=list['title']
        products_type_code=list['products_type_code']
        backurl=request.META.get('HTTP_REFERER','/')
    return render_to_response('detail.html',locals())

#留言
def leavewords(request):
    done = request.path
    backurl=request.GET.get("backurl")
    webtitle="客户留言"
    username=request.session.get("username",None)
    company_id=request.GET.get("company_id")
    pdtid=request.GET.get("pdtid")
    
    if (not pdtid):
        pdtid="0"
        be_inquired_id=company_id
        be_inquired_type=1
    else:
        be_inquired_id=pdtid
        be_inquired_type=0
    if not be_inquired_id:
        be_inquired_id=0
    if (not username):
        return HttpResponseRedirect("/login/?done=/leavewords/?backurl="+str(backurl)+"^and^company_id="+str(company_id)+"^and^pdtid="+str(pdtid))
    return render_to_response('aui/trade/question.html',locals())
    #return render_to_response('leavewords.html',locals())

def leavewords_save(request):
    webtitle="客户留言"
    nowlanmu="<a href='/category/'>交易中心</a>"
    send_username=request.session.get("username",None)
    send_company_id=request.session.get("company_id",None)
    username=request.session.get("username",None)
    company_id=request.session.get("company_id",None)
    if (username==None or (company_id==None or str(company_id)=="0")):
        errlist={'err':'login'}
        return HttpResponse(simplejson.dumps(errlist, ensure_ascii=False))
    if send_username and send_company_id==None:
        send_company_id=getcompanyid(send_username)
        request.session['company_id']=send_company_id
    re_company_id = request.POST.get('forcompany_id')
    backurl=request.POST.get('backurl')
    title='我对贵公司的产品感兴趣！'
    content = request.POST.get('content')
    errflag=None
    if (content=="" or content==None):
        errflag=1
        
    if (errflag==None):
        be_inquired_type=request.POST.get('be_inquired_type')
        be_inquired_id=request.POST.get('be_inquired_id')
        inquired_type=0
        sender_account=send_username
        receiver_account=getcompanyaccount(re_company_id)
        send_time=datetime.datetime.now()
        gmt_created=datetime.datetime.now()
        gmt_modified=datetime.datetime.now()
        value=[title,content,be_inquired_type,be_inquired_id,inquired_type,sender_account,receiver_account,send_time,gmt_created,gmt_modified]
        sql="insert into inquiry(title,content,be_inquired_type,be_inquired_id,inquired_type,sender_account,receiver_account,send_time,gmt_created,gmt_modified) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        dbc.updatetodb(sql,value);
        #----更新弹窗
        updateopenfloat(re_company_id,0)
        messagedata={'err':'false','errkey':'','type':'tradesave'}
        return HttpResponse(simplejson.dumps(messagedata, ensure_ascii=False))
    messagedata={'err':'true','errkey':'请填写留言内容！'}
    return HttpResponse(simplejson.dumps(messagedata, ensure_ascii=False))
    #return render_to_response('leavewords.html',locals())
#收藏
def favorite(request):
    webtitle="我的收藏"
    nowlanmu="<a href='/myrc_index/'>生意管家</a>"
    backurl=request.GET.get("backurl")
    if (backurl==None):
        backurl=request.META.get('HTTP_REFERER','/')
        backurl=backurl.replace("&","^and^")
    else:
        backurl=backurl.replace("^and^","&")
    
    username=request.session.get("username",None)
    cid=request.GET.get("company_id")
    pdtid=request.GET.get("pdtid")
    products_type_code=request.GET.get("products_type_code")
    if (username==None):
        return HttpResponseRedirect("/login/?done=/favorite/?company_id="+str(cid)+"^and^pdtid="+str(pdtid)+"^and^products_type_code="+str(products_type_code)+"^and^title="+request.GET.get("title"))
        
    if (pdtid==None or pdtid=='None'):
        favorite_type_code="10091002"
        content_id=cid
    else:
        if (products_type_code=="10331000"):
            favorite_type_code="10091006"
        if (products_type_code=="10331001"):
            favorite_type_code="10091006"
        content_id=pdtid
    content_title=request.GET.get("title")
    gmt_created=datetime.datetime.now()
    gmt_modified=datetime.datetime.now()
    company_id=request.session.get("company_id",None)
    account=request.session.get("username",None)
    value=[favorite_type_code,content_id,content_title,gmt_created,gmt_modified,company_id,account]
    sql="select id from myfavorite where favorite_type_code=%s and content_id=%s and company_id=%s"
    clist=dbc.fetchonedb(sql,[favorite_type_code,content_id,company_id])
    if (clist):
        sucflag=None
    else:
        sql="insert into myfavorite(favorite_type_code,content_id,content_title,gmt_created,gmt_modified,company_id,account) values(%s,%s,%s,%s,%s,%s,%s)"
        dbc.updatetodb(sql,value);
        sucflag=1
    return render_to_response('favorite.html',locals())
#----弹窗收藏
def openfavorite(request):
    webtitle="我的收藏"
    nowlanmu="<a href='/myrc_index/'>生意管家</a>"
    
    username=request.session.get("username",None)
    cid=request.GET.get("company_id")
    pdtid=request.GET.get("pdtid")
    products_type_code=request.GET.get("products_type_code")
    favorite_type_code=request.GET.get("favorite_type_code")
    if (username==None):
        return HttpResponseRedirect("/login/?done=/favorite/?company_id="+str(cid)+"^and^pdtid="+str(pdtid)+"^and^products_type_code="+str(products_type_code)+"^and^title="+request.GET.get("title"))
        
    if (pdtid==None or pdtid=='None'):
        favorite_type_code="10091002"
        content_id=cid
    else:
        if (products_type_code=="10331000"):
            favorite_type_code="10091006"
        if (products_type_code=="10331001"):
            favorite_type_code="10091006"
        content_id=pdtid
    content_title=request.GET.get("title")
    gmt_created=datetime.datetime.now()
    gmt_modified=datetime.datetime.now()
    company_id=request.session.get("company_id",None)
    account=request.session.get("username",None)
    value=[favorite_type_code,content_id,content_title,gmt_created,gmt_modified,company_id,account]
    sql="select id from myfavorite where favorite_type_code=%s and content_id=%s and company_id=%s"
    clist=dbc.fetchonedb(sql,[favorite_type_code,content_id,company_id])
    if (clist):
        sucflag=None
    else:
        sql="insert into myfavorite(favorite_type_code,content_id,content_title,gmt_created,gmt_modified,company_id,account) values(%s,%s,%s,%s,%s,%s,%s)"
        dbc.updatetodb(sql,value);
        sucflag=1
    return render_to_response('favorite.html',locals())



#下拉翻页 
def productsmore(request,company_id,page):
    htmlincludes=htmlinclude(company_id)
    html=htmlincludes['html']
    listall=getcompanyproductslist(None,int(page)*5+1,5,company_id,None,None,1)
    prolist=listall['list']
    prolistcount=listall['count']
    return render_to_response('html/'+html+'/productsmore.html',locals())

def order(request):
    host=getnowurl(request)
    nowlanmu="<a href='/huzhu/'>再生互助</a>"
    username=request.session.get("username",None)
    return render_to_response('order.html',locals())
    
def feedback(request):
    host=getnowurl(request)
    webtitle="问题反馈"
    nowlanmu="<a href='/huzhu/'>问题反馈</a>"
    username=request.session.get("username",None)
    return render_to_response('feedback.html',locals())
def feedbacksave(request):
    title = request.POST['title']
    content = request.POST['content']
    contact = request.POST['contact']
    company_id=request.session.get("company_id",None)
    if not company_id:
        company_id=0
    gmt_created=datetime.datetime.now()
    paytype=47
    content=content+"<br/>电话："+contact
    sql='insert into shop_baoming(company_id,content,gmt_created,paytype) values(%s,%s,%s,%s)'
    dbc.updatetodb(sql,[company_id,content,gmt_created,paytype])
    #sql="insert into subject_baoming(title,contents,gmt_created) values(%s,%s,%s)"
    #dbc.updatetodb(sql,[title,content+"<br/>电话："+contact,gmt_created])
    suc="您的问题已经提交成功，感谢您的反馈！"
    return render_to_response('feedback.html',locals())

def about(request):
    host=getnowurl(request)
    webtitle="关于我们"
    nowlanmu="<a href='/huzhu/'>再生互助</a>"
    username=request.session.get("username",None)
    return render_to_response('new/about.html',locals())


#----我的社区
def myrc_mycommunity(request):
    webtitle="消息中心"
    nowlanmu="<a href='/myrc_index/'>生意管家</a>"
    company_id=request.session.get("company_id",None)
    username=request.session.get("username",None)
    if username and (company_id==None or str(company_id)=="0"):
        company_id=getcompanyid(username)
        request.session['company_id']=company_id
    if (username==None or (company_id==None or str(company_id)=="0")):
        return HttpResponseRedirect("/login/")
    #----更新弹窗
    updateopenfloat(company_id,1)
    
    #判断是否已经填写了昵称
    mynickname=getcompanynickname(company_id)
    if not mynickname or mynickname=="":
        nickname=request.GET.get("nickname")
        if nickname:
            rpl1=re.findall('[0-9\ ]+',nickname)
            for r1 in rpl1:
                if len(r1)>10:
                    nickname=nickname.replace(r1,r1[:-3]+'***')
            addcompanynickname(nickname,company_id,username)
    #判断是否填写关注行业
    myguanzhu=gethuzhuguanzhu(company_id)
    if not myguanzhu or myguanzhu=="":
        myguanzhu=request.REQUEST.getlist("myguanzhu")
        if myguanzhu:
            addmyzhuzhuguanzhu(myguanzhu,company_id,username)
    
    invitelist=getbbs_invite(company_id)
    if invitelist:
        invitecount=len(invitelist)
    else:
        invitecount=0
        
    page=request.GET.get("page")
    if (page==None):
        page=1
    funpage = zz91page()
    limitNum=funpage.limitNum(5)
    nowpage=funpage.nowpage(int(page))
    frompageCount=funpage.frompageCount()
    after_range_num = funpage.after_range_num(2)
    before_range_num = funpage.before_range_num(9)
    huzhureply=getmessgelist(company_id,frompageCount,limitNum)
    if huzhureply:
        listall=huzhureply['list']
        count=huzhureply['count']
    listcount=huzhureply['count']
    if (int(listcount)>100000):
        listcount=100000
    listcount = funpage.listcount(listcount)
    page_listcount=funpage.page_listcount()
    firstpage = funpage.firstpage()
    lastpage = funpage.lastpage()
    page_range  = funpage.page_range()
    nextpage = funpage.nextpage()
    prvpage = funpage.prvpage()
    myrc_type="myrccommunity"
    #return render_to_response('myrc/myrc_mycommunity.html',locals())
    return render_to_response('aui/myrc/mycommunity.html',locals())
def myrc_mycommunitydel(request):
    pid=request.GET.get("pid")
    company_id=request.session.get("company_id",None)
    username=request.session.get("username",None)
    if username and (company_id==None or str(company_id)=="0"):
        company_id=getcompanyid(username)
        request.session['company_id']=company_id
    if (username==None or (company_id==None or str(company_id)=="0")):
        return HttpResponseRedirect("/login/")
    ptype=request.GET.get("ptype")
    post_id=request.GET.get("post_id")
    gmt_created=gmt_modified=datetime.datetime.now()
    if ptype=="invitedel":
        sql="select id from bbs_invite where id=%s"
        returnone=dbc.fetchonedb(sql,[pid])
        if returnone:
            sql="update bbs_invite set is_del=1 and answercheck=3 where id=%s"
            dbc.updatetodb(sql,[pid])
        else:
            sql="insert into bbs_invite(post_id,company_id,is_del,answercheck,gmt_created) values(%s,%s,%s,%s,%s)"
            dbc.updatetodb(sql,[post_id,company_id,1,3,gmt_created])
    return HttpResponse("suc")
def myrc_mypostsave(request):
    company_id=request.session.get("company_id",None)
    username=request.session.get("username",None)
    return HttpResponse("suc")
def myrc_myreplysave(request):
    pid=request.GET.get("pid")
    ptype=request.GET.get("ptype")
    company_id=request.session.get("company_id",None)
    username=request.session.get("username",None)
    if username and (company_id==None or str(company_id)=="0"):
        company_id=getcompanyid(username)
        request.session['company_id']=company_id
    if (username==None or (company_id==None or str(company_id)=="0")):
        return HttpResponseRedirect("/login/")
    
    tocompany_id=request.GET.get("tocompany_id")
    account=getcompanyaccount(company_id)
    bbs_post_id=request.GET.get("post_id")
    title="回复:"+getbbspost_title(bbs_post_id)
    content=request.GET.get("replycontent")
    check_status=1
    gmt_created=gmt_modified=datetime.datetime.now()
    if ptype=="invitereply":
        valu=[company_id,account,title,tocompany_id,bbs_post_id,content,check_status,gmt_created,gmt_modified,1]
        sql="insert into bbs_post_reply(company_id,account,title,tocompany_id,bbs_post_id,content,check_status,gmt_created,gmt_modified,postsource) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        dbc.updatetodb(sql,valu)
    if ptype=="postreply":
        valu=[company_id,account,title,tocompany_id,bbs_post_id,content,check_status,gmt_created,gmt_modified,pid,1]
        sql="insert into bbs_post_reply(company_id,account,title,tocompany_id,bbs_post_id,content,check_status,gmt_created,gmt_modified,bbs_post_reply_id,postsource) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        dbc.updatetodb(sql,valu)
    updatepostviewed(tocompany_id,bbs_post_id)
    #----更新弹窗
    updateopenfloat(tocompany_id,0)
    sql="update bbs_post set reply_time=%s,reply_count=reply_count+1,gmt_modified=%s where id=%s"
    dbc.updatetodb(sql,[gmt_modified,gmt_modified,bbs_post_id])
    return HttpResponse("suc")


#定制首页(一期)
def orderindex(request):
    host=getnowurl(request)
    company_id=request.session.get("company_id",None)
    username=request.session.get("username",None)
    if ((company_id==None or str(company_id)=="0")):
        return HttpResponseRedirect("/login/?done=/order/")
    return render_to_response('aui/myrc/order.html',locals())
#商机定制
def orderbusiness(request):
    host=getnowurl(request)
    ordercategorylist=getordercategorylistmain()
    company_id=request.session.get("company_id",None)
    username=request.session.get("username",None)
    if ((company_id==None or str(company_id)=="0")):
        return HttpResponseRedirect("/login/?done=/order/business.html")
    result=zzm.getmyordertrade(company_id)
    return render_to_response('2016new/order/business.html',locals())

#行情定制
def orderprice(request):
    host=getnowurl(request)
    company_id=request.session.get("company_id",None)
    username=request.session.get("username",None)
    if ((company_id==None or str(company_id)=="0")):
        return HttpResponseRedirect("/login/?done=/order/price.html")
    if company_id:
       mypriceorderlist=zzm.getmyorderprice(company_id)
    return render_to_response('2016new/order/price.html',locals())
    
#新 行情定制
def myorderprice_save(request):
    company_id=request.session.get("company_id",None)
    if ((company_id==None or str(company_id)=="0")):
        return HttpResponseRedirect("/login/?done=/order/price.html")
    label=request.POST.get("label")
    category_id=request.POST.get("category_id")
    assist_id=request.POST.get("assist_id")
    keywords=request.POST.get("keywords")
    if not label:
        label=request.GET.get("label")
        category_id=request.GET.get("category_id")
        assist_id=request.GET.get("assist_id")
        keywords=request.GET.get("keywords")
    list={
          'label':label,
          'company_id':company_id,
          'category_id':category_id,
          'assist_id':assist_id,
          'keywords':keywords}
    if label:
       result=zzm.savemyorderprice(list)
    if result:
        messagedata={'err':'false','errkey':'','type':'savecollect','orderid':result}
    else:
        messagedata={'err':'true','errkey':'已经添加','type':'savecollect'}
    return HttpResponse(simplejson.dumps(messagedata, ensure_ascii=False))
#新版 app 删除定制
def myorderprice_del(request):
    company_id=request.session.get("company_id",None)
    if ((company_id==None or str(company_id)=="0")):
        return HttpResponseRedirect("/login/?done=/order/price.html")
    orderid=request.GET.get("orderid")
    messagedata={'err':'true','errkey':'错误',}
    if orderid:
	    sql="delete from app_order_price where id=%s and company_id=%s"
	    result=dbc.updatetodb(sql,[orderid,company_id])
	    if result:
	        messagedata={'err':'false','errkey':'','type':'delcollect','orderid':result}
	    else:
	        messagedata={'err':'true','errkey':'已经删除','type':'delcollect'}
    return HttpResponse(simplejson.dumps(messagedata, ensure_ascii=False))
#新版app 供求定制
def myordertrade_save(request):
    company_id=request.session.get("company_id",None)
    if ((company_id==None or str(company_id)=="0")):
        return HttpResponseRedirect("/login/?done=/order/price.html")
    datatype=request.POST.get("datatype")
    otype=request.POST.get("otype")
    timelimit=request.POST.get("timelimit")
    keywordslist=request.POST.get("keywordslist")
    provincelist=request.POST.get("provincelist")
    list={
          'otype':otype,
          'company_id':company_id,
          'timelimit':timelimit,
          'keywordslist':keywordslist,
          'provincelist':provincelist}
    result=zzm.savemyordertrade(list)
    messagedata={'err':'false','errkey':'','type':'savecollect','orderid':result}
    return HttpResponse(simplejson.dumps(messagedata, ensure_ascii=False))


#----发布供求
def products_publish(request):
    saveform="products_save"
    company_id=request.session.get("company_id",None)
    username=request.session.get("username",None)
    if (username==None or (company_id==None or str(company_id)=="0")):
        return HttpResponseRedirect("/login/?done=/products_publish/")
    return render_to_response('aui/trade/post.html',locals())
    #return render_to_response('products_publish.html',locals())
#----发布保存供求
def products_save(request):
    saveform="products_save"
    username=request.session.get("username",None)
    company_id=request.session.get("company_id",None)
    if (username==None):
        return HttpResponseRedirect("/login/?done=/products_save/")
    gmt_created=datetime.datetime.now()
    if request.POST:
        error1=''
        error2=''
        error3=''
        error4=''
        error5=''
        error6=''
        error7=''
        error8=''
        errors='此处不能为空'
        products=request.POST['products']
        if not products:
            error6=errors
        category=request.POST['category']
        if not category:
            error1=errors
        title=request.POST['title']
        if not title:
            error2=errors
        quantity=request.POST['quantity']
        if not quantity:
            error3=errors
        if (quantity.isdigit()!=True):
            error3="请输入数字"
        quantity_unit=request.POST['quantity_unit']
        pricetype=request.POST['pricetype']
        if not pricetype:
            error7=errors
        price=request.POST['price']
        if (price.isdigit()!=True and pricetype=='1' and products=='10331000'):
            error4="请输入数字"
        if products=='10331000' and pricetype=='1' and not price:
            error4=errors
        price_unit=request.POST['price_unit']
        if products=='10331001':
            price=''
            price_unit=''
        details=request.POST['details']
        if not details:
            error5=errors
            
        validity=request.POST['validity']
        if not validity:
            error8=errors
        if validity:
            if validity=='-1':
                validitytime='9999-12-31 23:59:59'
            else:
                validitytime=gmt_created + datetime.timedelta(days = int(validity))
#        expire_time=gmt_created+validitytime
        
        if error1 or error2 or error3 or error4 or error5 or error6 or error7 or error8:
            return render_to_response('products_publish.html',locals())
        else:
            sql="insert into products(category_products_main_code,company_id,account,products_type_code,title,quantity,quantity_unit,price,price_unit,details,gmt_created,gmt_modified,real_time,refresh_time,expire_time,source_type_code,location,provide_status,total_quantity,is_show_in_price,source,specification,origin,min_price,max_price,goods_type_code,tags,tags_admin,impurity,color,useful,appearance,remark,old_id) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,'mobile_myrc','','N','',0,'','','',0,0,'','','','','','','','',0)"
            dbc.updatetodb(sql,[category,company_id,username,products,title,quantity,quantity_unit,price,price_unit,details,gmt_created,gmt_created,gmt_created,gmt_created,validitytime])
            sql1="select id from products where company_id=%s order by id desc limit 0,1"
            result=dbc.fetchonedb(sql1,[company_id])
            if result:
                product_id=result[0]
                picidlist=request.POST['picidlist']
                suckwd='发布'
                if picidlist:
                    sql2="update products_pic set product_id=%s where id=%s"
                    dbc.updatetodb(sql2,[product_id,picidlist])
                    suckwd='修改'
#                return HttpResponseRedirect('/myrc_products/?checkStatus=0')
                return render_to_response('trade/publishsuc.html',locals())
#----修改供求
def products_update(request):
    saveform="products_updatesave"
    proid=request.GET.get("proid")
    username=request.session.get("username",None)
    company_id=request.session.get("company_id",None)
    if (username==None or (company_id==None or str(company_id)=="0")):
        return HttpResponseRedirect("/login/?done=/products_update/")
    myproductsbyid=getmyproductsbyid(proid)
    categorycode=myproductsbyid['categorycode']
    category=categorycode
    title=myproductsbyid['title']
    quantity=myproductsbyid['quantity']
    products=myproductsbyid['products_type_code']
    quantity_unit=myproductsbyid['quantity_unit']
    price=myproductsbyid['price']
    if price:
        pricetype='1'
    else:
        pricetype='0'
    price_unit=myproductsbyid['price_unit']
    details=myproductsbyid['details']
    return render_to_response('products_publish.html',locals())

#----修改保存供求
def products_updatesave(request):
    saveform="products_updatesave"
    company_id=request.session.get("company_id",None)
    username=request.session.get("username",None)
    if (username==None or (company_id==None or str(company_id)=="0")):
        return HttpResponseRedirect("/login/?done=/products_update/")
    gmt_created=datetime.datetime.now()
    if request.POST:
        proid=request.POST['proid']
        error1=''
        error2=''
        error3=''
        error4=''
        error5=''
        error6=''
        error7=''
        error8=''
        errors='此处不能为空'
        products=request.POST['products']
        if not products:
            error6=errors
        category=request.POST['category']
        category_products=category
        if not category:
            error1=errors
        title=request.POST['title']
        if not title:
            error2=errors
        quantity=request.POST['quantity']
        if (quantity.isdigit()!=True):
            error3="请输入数字"
        if not quantity:
            error3=errors
        quantity_unit=request.POST['quantity_unit']
        pricetype=request.POST['pricetype']
        if not pricetype:
            error7=errors
        price=request.POST['price']
        if (price.isdigit()!=True and pricetype=='1' and products=='10331000'):
            error4="请输入数字"
        if products=='10331000' and pricetype=='1' and not price:
            error4=errors
        price_unit=request.POST['price_unit']
        if products=='10331001':
            price=''
            price_unit=''
        details=request.POST['details']
        if not details:
            error5=errors
            
        validity=request.POST['validity']
        if not validity:
            error8=errors
        if validity:
            if validity=='-1':
                validitytime='9999-12-31 23:59:59'
            else:
                validitytime=gmt_created + datetime.timedelta(days = int(validity))
        if error1 or error2 or error3 or error4 or  error5 or error6 or error7 or error8:
            return render_to_response('products_publish.html',locals())
        else:
            sql="update products set category_products_main_code=%s,products_type_code=%s,source_type_code=%s,title=%s,quantity=%s,quantity_unit=%s,price=%s,price_unit=%s,details=%s,refresh_time=%s,expire_time=%s,check_status=0 where id=%s"
            dbc.updatetodb(sql,[category,products,'mobile_myrc',title,quantity,quantity_unit,price,price_unit,details,gmt_created,validitytime,proid])
            suckwd='修改'
            return render_to_response('trade/publishsuc.html',locals())
    return HttpResponseRedirect('/myrc_products/?checkStatus=0')

#----微信签到
def weixin_qiandao(request):
    host=getnowurl(request)
    username=request.session.get("username",None)
    company_id=request.session.get("company_id",None)
    weixinid=request.GET.get("weixinid")
    weixinautologin(request,request.GET.get("weixinid"))
    qiandao=request.GET.get("qiandao")
    if (username==None or (company_id==None or str(company_id)=="0")):
        return HttpResponseRedirect("/login/?done=/score/index.html?weixinid="+str(weixinid)+"^and^qiandao=1")
    wdate=str(getToday())
    gmt_created=datetime.datetime.now()
    format="%Y-%m-%d";
    nowday=strtodatetime(wdate,format)
    oneday=datetime.timedelta(days=1)
    validity=datetime.timedelta(days=180)
    
    
    scoreopt=weixinscore()
    scorecount=scoreopt.getscorecount(username)
    scorelist=scoreopt.getscorelist(username)
    if weixinid:
        sql="select id from weixin_qiandao where account=%s and gmt_created>'"+str(nowday)+"' and gmt_created<='"+str(nowday+oneday)+"'"
        result=dbc.fetchonedb(sql,[username])
        if result:
            rerr=1
            rtext="你今天已经签到成功！，一天只能签到一次！"
        else:
            rerr=0
            sqla="insert into weixin_qiandao(weixinid,account,gmt_created) values(%s,%s,%s)"
            dbc.updatetodb(sqla,[weixinid,username,gmt_created])
            rtext="恭喜您今天签到成功！你已经获得3个积分"
            sqlb="insert into weixin_score(account,rules_code,score,gmt_created,validity) values(%s,%s,%s,%s,%s)"
            dbc.updatetodb(sqlb,[username,"qiaodao",3,gmt_created,str(nowday+validity)])
    return render_to_response('score/index.html',locals())
#----微信积分列表
def weixin_scorelist(request):
    host=getnowurl(request)
    username=request.session.get("username",None)
    company_id=request.session.get("company_id",None)
    if (username==None or (company_id==None or str(company_id)=="0")):
        return HttpResponseRedirect("/login/?done=/score/scorelist.html")
    mobile=getcompanymobile(username)
    scoreopt=weixinscore()
    scorecount=scoreopt.getscorecount(username)
    scorelist=scoreopt.getscorelist(username)
    limitoutscore=scoreopt.getlimitoutscore(username)
    return render_to_response('score/scorelist.html',locals())
def weixin_scorelistmore(request):
    host=getnowurl(request)
    username=request.session.get("username",None)
    page=request.GET.get("page")
    if (username!=None):
        scoreopt=weixinscore()
        scorecount=scoreopt.getscorecount(username)
        scorelist=scoreopt.getscorelist(username,page=page)
    return render_to_response('score/scorelistmore.html',locals())
#----奖品列表
def weixin_prizelist(request):
    host=getnowurl(request)
    username=request.session.get("username",None)
    company_id=request.session.get("company_id",None)
    if (username==None or (company_id==None or str(company_id)=="0")):
        return HttpResponseRedirect("/login/?done=/score/prizelist.html")
    mobile=getcompanymobile(username)
    scoreopt=weixinscore()
    scorecount=scoreopt.getscorecount(username)
    prizelist=scoreopt.getprizelist(username)
    limitoutscore=scoreopt.getlimitoutscore(username)
    
    return render_to_response('score/prizelist.html',locals())
#---兑奖记录
def weixin_prizelog(request):
    host=getnowurl(request)
    username=request.session.get("username",None)
    company_id=request.session.get("company_id",None)
    if (username==None or (company_id==None or str(company_id)=="0")):
        return HttpResponseRedirect("/login/?done=/score/prizelog.html")
    mobile=getcompanymobile(username)
    scoreopt=weixinscore()
    scorecount=scoreopt.getscorecount(username)
    prizelog=scoreopt.getprizelog(username)
    limitoutscore=scoreopt.getlimitoutscore(username)
    
    return render_to_response('score/prizelog.html',locals())

def weixin_helptxt(request):
    host=getnowurl(request)
    return render_to_response('score/helptxt.html',locals())
#----保存手机
def weixin_savemoble(request):
    username=request.session.get("username",None)
    company_id=request.session.get("company_id",None)
    mobile=request.POST['mobile']
    if username:
        sql="select id from weixin_account where account=%s"
        returnlist=dbc.fetchonedb(sql,[username])
        if returnlist:
            sqlp="update weixin_account set mobile=%s where account=%s"
            dbc.updatetodb(sqlp,[mobile,username])
        else:
            sqlp="insert into weixin_account(mobile,account) values(%s,%s)"
            dbc.updatetodb(sqlp,[mobile,username])
    
    return HttpResponse(mobile)
#----开始兑奖
def weixin_saveprize(request):
    username=request.session.get("username",None)
    company_id=request.session.get("company_id",None)
    id=request.POST['id']
    sqls="select score from weixin_prize where id=%s"
    returnlist=dbc.fetchonedb(sqls,[id])
    if returnlist:
        score=int(returnlist[0])
    else:
        score=0
    gmt_created=datetime.datetime.now()
    scoreopt=weixinscore()
    scorecount=scoreopt.getscorecount(username)
    if scorecount>=score:
        if username:
            sqlp="insert into weixin_prizelog(account,prizeid,score,gmt_created,type) values(%s,%s,%s,%s,%s)"
            dbc.updatetodb(sqlp,[username,id,score,gmt_created,1])
    else:
        return HttpResponse('0')
    
    return HttpResponse(id)
        
#----图片上传
def upload(request):
    username=request.session.get("username",None)
    timepath=time.strftime('%Y/%m/%d/',time.localtime(time.time()))
    gmt_created=datetime.datetime.now()
    nowtime=int(time.time())
    if request.FILES:
        file = request.FILES['file']
        #image = Image.open(reqfile)
        suportFormat = ['BMP', 'GIF', 'JPG','JPGE', 'PNG','JPEG']
        #image.thumbnail((128,128),Image.ANTIALIAS)
        tempim = StringIO.StringIO()
        mstream = StringIO.StringIO(file.read())
        im = Image.open(mstream)
        rheight=500
        rwidth=500
        
        pwidth=im.size[0]
        pheight=im.size[1]
        
        rate = int(pwidth/pheight)
        if rate==0:
            rate=1
        nwidth=200
        nheight=200
        if (pwidth>rwidth):
            nwidth=rwidth
            nheight=nwidth /rate
        else:
            nwidth=pwidth
            nheight=pheight
        
        if (pheight>rheight):
            nheight=rheight
            nwidth=rheight*rate
        else:
            nwidth=pwidth
            nheight=pheight
        
        #im.thumbnail((10,10),Image.ANTIALIAS)
        im.thumbnail((nwidth,nheight),Image.ANTIALIAS)
        tmp = random.randint(100, 999)
        
        newpath="/mnt/data/resources/products/"+timepath
        
        imgpath=newpath+str(nowtime)+str(tmp)+"."+im.format
        if not os.path.isdir(newpath):
            os.makedirs(newpath)
        im.save(imgpath,im.format,quality = 60)
        mstream.closed
        tempim.closed
        picurl="http://img1.zz91.com/products/"+timepath+str(nowtime)+str(tmp)+"."+im.format
        
        sql="insert into products_pic(product_id,pic_address,gmt_created) values(0,%s,%s)"
        dbc.updatetodb(sql,[imgpath,gmt_created])
        sql1="select id from products_pic where pic_address=%s"
        productspicresult=dbc.fetchonedb(sql1,[imgpath])
        if productspicresult:
            productspicid=productspicresult[0]
            #del request.session["productspicid"]
            #request.session['productspicid']=productspicid
            return HttpResponse("<script>parent.changepic('"+picurl+"','"+str(productspicid)+"')</script>")
    return HttpResponse("请选择一张图片.")


#----消息提醒
def openmessages(request):
    return HttpResponse("")
    company_id=request.session.get("company_id",None)
    username=request.session.get("username",None)
    if (company_id==None or str(company_id)=="0"):
        return HttpResponse("")
    openfloat=getopenfloat(company_id)
    if openfloat:
        invitecount=getbbs_invitecount(company_id)
        
        replycount=getmessgecount(company_id)
        
        mcount=getopenquestioncount(username)
        if mcount:
            url="/myrc_leavewords/"
        else:
            url="/myrc_mycommunity/"
            mcount=replycount+invitecount
        if mcount==0:
            return HttpResponse("")
        return render_to_response('myrc/openmessages.html',locals())
    else:
        return HttpResponse("")

def categoryinfo(request):
    host=getnowurl(request)
    username=request.session.get("username",None)
    categorycode=request.GET.get("categorycode")
    categorycodelist=getindexcategorylist(categorycode,1)
    ctype=request.GET.get("ctype")
    if ctype=="company":
        return render_to_response('new/categorycode_key.html',locals())
    if ctype=="aui":
        return render_to_response('new/categorycode_aui.html',locals())
    return render_to_response('new/categorycode.html',locals())

#---变更图片大小
def changepic(request):
    username=request.session.get("username",None)
    rheight=int(request.GET.get("height"))
    rwidth=int(request.GET.get("width"))
    url=request.GET.get("url")
    #url = 'http://img1.zz91.com/ads/1377964800000/f53cb9e8-8fc5-4bf1-ae3b-468f5f814da0.gif'
    file = urllib.urlopen(url)
    suportFormat = ['BMP', 'GIF', 'JPG','JPGE', 'PNG','JPEG']
    tempim = StringIO.StringIO()
    mstream = StringIO.StringIO(file.read())
    im = Image.open(mstream)
    pwidth=im.size[0]
    pheight=im.size[1]
    
    rate = int(pwidth/pheight)
    if rate==0:
        rate=1
    nwidth=200
    nheight=200
    if (pwidth>rwidth):
        nwidth=rwidth
        nheight=nwidth /rate
    else:
        nwidth=pwidth
        nheight=pheight
    
    if (pheight>rheight):
        nheight=rheight
        nwidth=rheight*rate
    else:
        nwidth=pwidth
        nheight=pheight
    
    #im.thumbnail((10,10),Image.ANTIALIAS)
    im.thumbnail((nwidth,nheight),Image.ANTIALIAS)
    im.save(tempim,im.format, quality = 60)
    mstream.closed
    tempim.closed
    if im.format in suportFormat:
        a=1
        #return HttpResponse(nwidth)
        return HttpResponse(tempim.getvalue(),'image/'+im.format)
    else:
        return HttpResponse(im.format)
    #isize={'width':im.size[0],'height':im.size[1]}
    
#---变更图片大小
def showimg1(request,path):
    return HttpResponse(path)
def showimg(request,width,height,path):
    username=request.session.get("username",None)
    rheight=int(height)
    rwidth=int(width)
    
    url=path
    
    #url=url.replace("__","/")
    #url=url.replace("_",".")
    #return HttpResponse(url)
    #http://pyapp.zz91.com/img/100x300/img1.zz91.com/products/2014/3/28/ef9df0fa-007e-452c-b064-732def680758.jpg
    #url = 'http://img1.zz91.com/ads/1377964800000/f53cb9e8-8fc5-4bf1-ae3b-468f5f814da0.gif'
    if not url:
        return HttpResponse('err')
    try:
        file = urllib.urlopen("http://"+url)
        suportFormat = ['BMP', 'GIF', 'JPG','JPGE', 'PNG','JPEG']
        tempim = StringIO.StringIO()
        mstream = StringIO.StringIO(file.read())
        im = Image.open(mstream)
        pwidth=im.size[0]
        pheight=im.size[1]
        
        rate = round(float(pwidth) / float(pheight),2)
        
        nwidth=200
        nheight=200
        
        nwidth=rwidth
        nheight=int (float(nwidth) /rate)
        
        if (nheight>rheight):
            nheight=rheight
            nwidth=int(rheight*rate)
        
        if (nwidth>rwidth):
            nwidth=rwidth
            nheight=int(float(nwidth) / rate)
        
        #return HttpResponse(str(nwidth)+" "+str(nheight)+" |"+str(rate)+ "|"+ str(pwidth)+" "+str(pheight))
        
        """    
        if (pheight>rheight):
            nheight=rheight
            nwidth=rheight*rate
        else:
            nwidth=pwidth
            nheight=pheight
        """
        
        #im.thumbnail((10,10),Image.ANTIALIAS)
        im.thumbnail((nwidth,nheight),Image.ANTIALIAS)
        im.tostring()
        
        im.save(tempim,im.format, quality = 80)
        
        
        mstream.closed
        tempim.closed
        if im.format in suportFormat:
            a=1
            #return HttpResponse(nwidth)
            #self.set_header('Content-Type','image/'+im.format)
            return HttpResponse(tempim.getvalue(),mimetype='image/'+im.format)
        else:
            return HttpResponse(im.format)
    except IndexError:
        return HttpResponse('err')
    #isize={'width':im.size[0],'height':im.size[1]}
    
def useragent(request):
    data=["Nokia",#诺基亚，有山寨机也写这个的，总还算是手机，Mozilla/5.0 (Nokia5800 XpressMusic)UC AppleWebkit(like Gecko) Safari/530  
    "SAMSUNG",#三星手机 SAMSUNG-GT-B7722/1.0+SHP/VPP/R5+Dolfin/1.5+Nextreaming+SMM-MMS/1.2.0+profile/MIDP-2.1+configuration/CLDC-1.1  
    "MIDP-2",#j2me2.0，Mozilla/5.0 (SymbianOS/9.3; U; Series60/3.2 NokiaE75-1 /110.48.125 Profile/MIDP-2.1 Configuration/CLDC-1.1 ) AppleWebKit/413 (KHTML like Gecko) Safari/413  
    "CLDC1.1",#M600/MIDP2.0/CLDC1.1/Screen-240X320  
    "SymbianOS",#塞班系统的，  
    "MAUI",#MTK山寨机默认ua  
    "UNTRUSTED/1.0",#疑似山寨机的ua，基本可以确定还是手机  
    "Windows CE",#Windows CE，Mozilla/4.0 (compatible; MSIE 6.0; Windows CE; IEMobile 7.11)  
    "iPhone",#iPhone是否也转wap？不管它，先区分出来再说。Mozilla/5.0 (iPhone; U; CPU iPhone OS 4_1 like Mac OS X; zh-cn) AppleWebKit/532.9 (KHTML like Gecko) Mobile/8B117  
    "iPad",#iPad的ua，Mozilla/5.0 (iPad; U; CPU OS 3_2 like Mac OS X; zh-cn) AppleWebKit/531.21.10 (KHTML like Gecko) Version/4.0.4 Mobile/7B367 Safari/531.21.10  
    "Android",#Android是否也转wap？Mozilla/5.0 (Linux; U; Android 2.1-update1; zh-cn; XT800 Build/TITA_M2_16.22.7) AppleWebKit/530.17 (KHTML like Gecko) Version/4.0 Mobile Safari/530.17  
    "BlackBerry",#BlackBerry8310/2.7.0.106-4.5.0.182  
    "UCWEB",#ucweb是否只给wap页面？ Nokia5800 XpressMusic/UCWEB7.5.0.66/50/999  
    "ucweb",#小写的ucweb貌似是uc的代理服务器Mozilla/6.0 (compatible; MSIE 6.0;) Opera ucweb-squid  
    "BREW",#很奇怪的ua，例如：REW-Applet/0x20068888 (BREW/3.1.5.20; DeviceId: 40105; Lang: zhcn) ucweb-squid  
    "J2ME",#很奇怪的ua，只有J2ME四个字母  
    "YULONG",#宇龙手机，YULONG-CoolpadN68/10.14 IPANEL/2.0 CTC/1.0  
    "YuLong",#还是宇龙  
    "COOLPAD",#宇龙酷派YL-COOLPADS100/08.10.S100 POLARIS/2.9 CTC/1.0  
    "TIANYU",#天语手机TIANYU-KTOUCH/V209/MIDP2.0/CLDC1.1/Screen-240X320  
    "TY-",#天语，TY-F6229/701116_6215_V0230 JUPITOR/2.2 CTC/1.0  
    "K-Touch",#还是天语K-Touch_N2200_CMCC/TBG110022_1223_V0801 MTK/6223 Release/30.07.2008 Browser/WAP2.0  
    "Haier",#海尔手机，Haier-HG-M217_CMCC/3.0 Release/12.1.2007 Browser/WAP2.0  
    "DOPOD",#多普达手机  
    "Lenovo",# 联想手机，Lenovo-P650WG/S100 LMP/LML Release/2010.02.22 Profile/MIDP2.0 Configuration/CLDC1.1  
    "LENOVO",# 联想手机，比如：LENOVO-P780/176A  
    "HUAQIN",#华勤手机  
    "AIGO-",#爱国者居然也出过手机，AIGO-800C/2.04 TMSS-BROWSER/1.0.0 CTC/1.0  
    "CTC/1.0",#含义不明  
    "CTC/2.0",#含义不明  
    "CMCC",#移动定制手机，K-Touch_N2200_CMCC/TBG110022_1223_V0801 MTK/6223 Release/30.07.2008 Browser/WAP2.0  
    "DAXIAN",#大显手机DAXIAN X180 UP.Browser/6.2.3.2(GUI) MMP/2.0  
    "MOT-",#摩托罗拉，MOT-MOTOROKRE6/1.0 LinuxOS/2.4.20 Release/8.4.2006 Browser/Opera8.00 Profile/MIDP2.0 Configuration/CLDC1.1 Software/R533_G_11.10.54R  
    "SonyEricsson",# 索爱手机，SonyEricssonP990i/R100 Mozilla/4.0 (compatible; MSIE 6.0; Symbian OS; 405) Opera 8.65 [zh-CN]  
    "GIONEE",#金立手机  
    "HTC",#HTC手机  
    "ZTE",#中兴手机，ZTE-A211/P109A2V1.0.0/WAP2.0 Profile  
    "HUAWEI",#华为手机，  
    "webOS",#palm手机，Mozilla/5.0 (webOS/1.4.5; U; zh-CN) AppleWebKit/532.2 (KHTML like Gecko) Version/1.0 Safari/532.2 Pre/1.0  
    "GoBrowser",#3g GoBrowser.User-Agent=Nokia5230/GoBrowser/2.0.290 Safari  
    "IEMobile",#Windows CE手机自带浏览器，  
    "WAP2.0"]#支持wap 2.0的
    agent=request.META['HTTP_USER_AGENT']
    for list in data:
        if list in agent:
            return HttpResponse(list)
    return HttpResponse(data)
def closefloatapp(request):
    closeapp=request.GET.get("close")
    if closeapp:
        request.session['closeapp']="close"
        #request.session.set_expiry(60)
    closeapps=request.session.get("closeapp",None)
    restr="0"
    if closeapps:
        restr="1"
    return HttpResponse(restr)
def viewer_404(request):
    nowlanmu="<a href='/category/'>交易中心</a>"
    t = get_template('404.html')
    html = t.render(Context({'nowlanmu':nowlanmu}))
    return HttpResponseNotFound(html)
def viewer_500(request):
    t = get_template('404.html')
    nowlanmu="<a href='/category/'>首页</a>"
    html = t.render(Context({'nowlanmu':nowlanmu}))
    return HttpResponseNotFound(html)

