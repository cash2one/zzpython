#-*- coding:utf-8 -*-
import MySQLdb,settings,codecs,os,sys,datetime,time,random,requests
from django.utils.http import urlquote
from django.shortcuts import render_to_response
from django.template.loader import get_template
from django.template import Context
from django.http import HttpResponse,HttpResponseRedirect,HttpResponseForbidden,HttpResponseNotFound,HttpResponsePermanentRedirect
from django.core.paginator import Paginator,InvalidPage,EmptyPage,PageNotAnInteger
from zz91settings import SPHINXCONFIG,limitpath
from zz91tools import mobileuseragent,timestamp_datetime
from datetime import timedelta, date 
from django.core.cache import cache
from zz91conn import database_mongodb
from zz91db_ast import companydb
from zz91db_ads import adsdb
from zz91db_2_news import newsdb
dbc=companydb()
dbads=adsdb()
dbn=newsdb()
import shutil
try:
    import cPickle as pickle
except ImportError:
    import pickle

from math import ceil
from sphinxapi import *
from zz91page import *
reload(sys) 
sys.setdefaultencoding('utf-8') 
spconfig=SPHINXCONFIG
nowpath=os.path.dirname(__file__)
execfile(nowpath+"/conn.py")
execfile(nowpath+"/commfunction.py")
execfile(nowpath+"/function.py")

wmh=weimenhu()

def default(request):
    host = request.META['HTTP_HOST']
    hidfloat=1
    #最新微门户和热门搜索
    messagelist=wmh.getnewandhot()
    listnewest=messagelist['newest']
    listhot=messagelist['hot']
    companylist=wmh.getcomplist()
    #废金属价格
    priceInfo_feijs=wmh.getpricelist_daohang(kname='金属'.decode('utf-8'),limitcount=8,titlelen=50)
    lef_rig=wmh.leftandright(priceInfo_feijs)
    priceInfo_feijs_left=lef_rig['left']
    priceInfo_feijs_right=lef_rig['right']
   
    #废塑料价格
    priceInfo_feisl=wmh.getpricelist_daohang(kname='塑料'.decode('utf-8'),limitcount=8,titlelen=50)
    lef_rig=wmh.leftandright(priceInfo_feisl)
    priceInfo_feisl_left=lef_rig['left']
    priceInfo_feisl_right=lef_rig['right']

    #废纸价格       
    priceInfo_feizhi=wmh.getpricelist_daohang(kname='纸'.decode('utf-8'),limitcount=8,titlelen=50)
    lef_rig=wmh.leftandright(priceInfo_feizhi)
    priceInfo_feizhi_left=lef_rig['left']
    priceInfo_feizhi_right=lef_rig['right']
    
    #废橡胶价格
    priceInfo_feixj=wmh.getpricelist_daohang(kname='橡胶'.decode('utf-8'),limitcount=8,titlelen=50)
    lef_rig=wmh.leftandright(priceInfo_feixj)
    priceInfo_feixj_left=lef_rig['left']
    priceInfo_feixj_right=lef_rig['right']

    #废二手设备
    priceInfo_jixshebei=wmh.getpricelist_daohang(kname='机械 设备'.decode('utf-8'),limitcount=8,titlelen=50)
    lef_rig=wmh.leftandright(priceInfo_jixshebei)
    priceInfo_jixshebei_left=lef_rig['left']
    priceInfo_jixshebei_right=lef_rig['right']

    #废电器
    priceInfo_feidz=wmh.getpricelist_daohang(kname='电子'.decode('utf-8'),limitcount=8,titlelen=50)
    lef_rig=wmh.leftandright(priceInfo_feidz)
    priceInfo_feidz_left=lef_rig['left']
    priceInfo_feidz_right=lef_rig['right']
    #类别列表
    #--废金属
    #-----钢铁最终类
    gangtie=wmh.getlastcategory(category_code='10001019100110001000')
    #-----稀有金属贵金属最终类
    xiyou=wmh.getlastcategory(category_code='10001019100110001004')
    #-----有色金属 最终类
    youse=wmh.getlastcategory(category_code='10001019100110001002')
    #-----金属混合/复合料  硅 最终类
    hunhe=wmh.getlastcategory(category_code='10001019100110001003')
    
    #--废塑料
    #-----通用废塑料 类
    tysl=wmh.getlastcategory(category_code='10001019100110011001')
    #-----工程废塑料  类
    gcsl=wmh.getlastcategory(category_code='10001019100110011002')
    #-----塑料颗粒  类
    slkl=wmh.getlastcategory(category_code='10001019100110011003')
    #-----特种废塑料  塑料混合/复合料  类
    tzsl=wmh.getlastcategory(category_code='10001019100110011004')
    
    #--废纺织品
    #-----化纤类
    huaqian=wmh.getlastcategory(category_code='10001019100110021001')
    #-----皮革类
    pige=wmh.getlastcategory(category_code='10001019100110021002')
    #-----丝 牛仔布  家纺废料  类
    si=wmh.getlastcategory(category_code='10001019100110021003')
    #-----废玻璃废木  化工废料  服务 类
    fbl=wmh.getlastcategory(category_code='10001019100110021004')
    
    #--包装废纸   工业废纸
    #-----包装废纸  工业废纸 类
    bzfz=wmh.getlastcategory(category_code='10001019100110031001')
    #-----印刷废纸  办公废纸 类
    ysfz=wmh.getlastcategory(category_code='10001019100110031002')
    #-----生活废纸  特种废纸  废纸制品 类
    shfz=wmh.getlastcategory(category_code='10001019100110031003')
    #-----美废  欧废  日废  纸浆  卡纸  纸边 类
    meifei=wmh.getlastcategory(category_code='10001019100110031004')
    
    #-- 二手设备
    #-----工程设备  类
    gcsb=wmh.getlastcategory(category_code='10001019100110041001')
    #-----化工设备 类
    hgsb=wmh.getlastcategory(category_code='10001019100110041002')
    #-----制冷设备  冶炼设备  类
    zlsb=wmh.getlastcategory(category_code='10001019100110041003')
    #-----交通工具  二手商品  类
    jtgj=wmh.getlastcategory(category_code='10001019100110041004')
    
    #-- 废电子电器   废橡胶   废轮胎
    #-----废电子  办公设备  类
    fdz=wmh.getlastcategory(category_code='10001019100110051001')
    #-----废电器 类
    fdq=wmh.getlastcategory(category_code='10001019100110051002')
    #-----废橡胶  合成橡胶   类
    fxj=wmh.getlastcategory(category_code='10001019100110051003')
    #-----再生胶  废轮胎  废橡胶处理设备  类
    zsj=wmh.getlastcategory(category_code='10001019100110051004')
    
    cp_link=wmh.getdaohanglist(10221000)
    
    return render_to_response('index2.html',locals())
#注册
def reg(request):
    suc=request.GET.get("suc")
    err=request.GET.get("err")
    return render_to_response('reg/index.html',locals())
def cp(request , pingyin):
    newflag=request.GET.get("newflag")
    mobileflag=request.GET.get("mobileflag")
    host = request.META.get("HTTP_HOST")
    moaddr=request.META.get("REMOTE_ADDR")
    if moaddr=="115.29.35.147":
        return HttpResponseNotFound(request.META.get("REMOTE_PORT"))
    if (pingyin=="carveout"):
        return carveout(request)
    pingyinlist=getpingyinattribute(pingyin)
    cpchickNum(pingyin)
    keywords=""
    if pingyinlist:
        pingyinname=pingyinlist['label']
        keywords=pingyinlist['keywords']
        if not keywords:
            return HttpResponseNotFound("<h1>FORBIDDEN1</h1>")
        if keywords:
            keywords=keywords.replace(" ","")
        keylabel=pingyinlist['label']
    else:
        return HttpResponseNotFound("<h1>FORBIDDEN2</h1>")
    if pingyin=="jiqingluanlunxiaoshuo":
        return HttpResponseNotFound("<h1>FORBIDDEN3</h1>")
    mingang=getmingganword(pingyinname)
    if mingang:
        return HttpResponseNotFound(keywords+"敏感词："+mingang+"<h1>FORBIDDEN4</h1>")
    
    plist1=getindexofferlist(keywords,0,4)
    plist2=getindexofferlist(keywords,1,4)
    if not mobileflag:
        companypricelist=getcompanypricelist(kname=keywords,limitcount=15,titlelen=20,searchmode=2)
    pricelist=getindexpricelist(kname=keywords,limitcount=15,searchmode=2)
    bbslist=getindexbbslist(kname=keywords,limitcount=15,searchmode=2)
    if not mobileflag:
        plist_pic=getindexofferlist_pic(kname=keywords,limitcount=8)
        if plist_pic:
            picone=plist_pic[0]['pdt_images']
        pcompanylist=getcompanyindexcomplist(keywords,8)
        newjoincomplist=getsycompanylist(keywords,0,20,None,10)
    
    #tagslist=newtagslist(keywords,40)
    cplist=getcplist(keywords,50)
    
    #----进入手机模版
    #agent=request.META['HTTP_USER_AGENT']
    #agentflag=mobileuseragent(agent)
    #if agentflag:
    
    hidfloat=1
    if mobileflag:
        adlist=getadlistkeywords("789",pingyinname)
        jingjialist=getjingjialist(keywords=keywords,limitcount=10,mycompany_id='')
        return render_to_response('mobile/mindex.html',locals())
    return render_to_response('new/index.html',locals())

def price(request,pingyin):
    newflag=request.GET.get("newflag")
    mobileflag=request.GET.get("mobileflag")
    cpchickNum(pingyin)
    pingyinlist=getpingyinattribute(pingyin)
    if not pingyinlist:
        return HttpResponseNotFound("<h1>FORBIDDEN</h1>")
    pingyinname=pingyinlist['label']
    keywords=pingyinlist['keywords']
    mingang=getmingganword(keywords)
    if mingang:
        return HttpResponseNotFound("<h1>FORBIDDEN</h1>")
    if not mobileflag:
        plist_pic=getindexofferlist_pic(kname=keywords,pdt_type=None,limitcount=4)
        salesproducts=getindexofferlist(keywords,0,9)
        buyproducts=getindexofferlist(keywords,1,9)
        newjoincomplist=getsycompanylist(keywords,0,20,None,10)
    arealist=getarealist("10011000")
    compnaypricelist=getcompanypricelist(kname=keywords,limitcount=30,company=1,searchmode=2)
    pricelist=getindexpricelist(kname=keywords,limitcount=15,searchmode=2)
    cplist=getcplist(keywords,50)
    hidfloat=1
    #----进入手机模版
    if mobileflag:
        adlist=getadlistkeywords("793",pingyinname)
        return render_to_response('mobile/mprice.html',locals())
    return render_to_response('new/price.html',locals())
def pricemore(request,pingyin,page):
    mobileflag=request.GET.get("mobileflag")
    pingyinlist=getpingyinattribute(pingyin)
    if not pingyinlist:
        return HttpResponseNotFound("<h1>FORBIDDEN</h1>")
    pingyinname=pingyinlist['label']
    keywords=pingyinlist['keywords']
    cplist=getcplist(keywords,50)
    province = request.GET.get("province")
    if (province=='None' or province==None):
        province=""
    pricelist=getindexpricelist(kname=keywords,limitcount=15,searchmode=2)
    arealist=getarealist("10011000")
    if (page==None or page==0):
        page=1
    funpage = zz91page()
    limitNum=funpage.limitNum(50)
    nowpage=funpage.nowpage(int(page))
    frompageCount=funpage.frompageCount()
    after_range_num = funpage.after_range_num(5)
    before_range_num = funpage.before_range_num(9)
    
    compnaypricelist=getcompanypricelistmore(kname=keywords,frompageCount=frompageCount,limitNum=limitNum,titlelen=50,company=1,province=province,searchmode=2)
    listcount=0
    if (compnaypricelist):
        listall=compnaypricelist['list']
        listcount=compnaypricelist['count']
        if (int(listcount)>1000000):
            listcount=1000000-1
    listcount = funpage.listcount(listcount)
    page_listcount=funpage.page_listcount()
    firstpage = funpage.firstpage()
    lastpage = funpage.lastpage()
    page_range  = funpage.page_range()
    nextpage = funpage.nextpage()
    prvpage = funpage.prvpage()
    hidfloat=1
    if not mobileflag:
        newjoincomplist=getsycompanylist(keywords,0,20,None,10)
    if mobileflag:
        return render_to_response('mobile/mpricemore.html',locals())
    return render_to_response('new/pricemore.html',locals())
def trade(request,pingyin,page=''):
    mobileflag=request.GET.get("mobileflag")
    cpchickNum(pingyin)
    pingyinlist=getpingyinattribute(pingyin)
    if not pingyinlist:
        return HttpResponseNotFound("<h1>FORBIDDEN</h1>")
    pingyinname=pingyinlist['label']
    keywords=pingyinlist['keywords']
    mingang=getmingganword(keywords)
    if mingang:
        return HttpResponseNotFound("<h1>FORBIDDEN</h1>")
    if not mobileflag:
        companypricelist=getcompanypricelist(keywords,16,20,searchmode=2)
        pcompanylist=getcompanyindexcomplist(keywords,4)
        bbslist=getindexbbslist(kname=keywords,limitcount=7)
        salesproducts=getindexofferlist(keywords,0,15)
        buyproducts=getindexofferlist(keywords,1,15)
    ptype=request.GET.get("ptype")
    if (ptype==None):
        ptype=""
    ptab1="mainLeft-contentTop1 fl"#"ms-title-left"
    ptab2="mainLeft-contentTop2 fl"#"ms-title-right"
    ptab3="mainLeft-contentTop2 fl"#"ms-title-right"
    if (ptype=="1"):
         ptab1="mainLeft-contentTop2 fl"#"ms-title-left"
         ptab2="mainLeft-contentTop1 fl"#"ms-title-right"
         ptab3="mainLeft-contentTop2 fl"#"ms-title-right"
    if (ptype=="0"):
         ptab1="mainLeft-contentTop2 fl"#"ms-title-left"
         ptab2="mainLeft-contentTop2 fl"#"ms-title-right"
         ptab3="mainLeft-contentTop1 fl"#"ms-title-right"
    
    cplist=getcplist(keywords,50)
    
    if not page:
        page=1
    funpage = zz91page()
    limitNum=funpage.limitNum(20)
    nowpage=funpage.nowpage(int(page))
    frompageCount=funpage.frompageCount()
    after_range_num = funpage.after_range_num(5)
    before_range_num = funpage.before_range_num(9)
    
    prolist=getproductslist(kname=keywords,frompageCount=frompageCount,limitNum=limitNum,ptype=ptype)
    
    listcount=0
    if (prolist):
        listall=prolist['list']
        listcount=prolist['count']
        if (int(listcount)>1000000):
            listcount=1000000-1
    listcount = funpage.listcount(listcount)
    page_listcount=funpage.page_listcount()
    firstpage = funpage.firstpage()
    lastpage = funpage.lastpage()
    page_range  = funpage.page_range()
    nextpage = funpage.nextpage()
    prvpage = funpage.prvpage()
    
    hidfloat=1
    if mobileflag:
        jingjialist=getjingjialist(keywords=keywords,limitcount=10,mycompany_id='')
        adlist=getadlistkeywords("792",pingyinname)
        return render_to_response('mobile/mtrade.html',locals())
    return render_to_response('new/trade.html',locals())
def trademore(request,pingyin,page):
    mobileflag=request.GET.get("mobileflag")
    ptype=request.GET.get("ptype")
    if (ptype==None):
        ptype=""
    ptab1="mainLeft-contentTop1 fl"#"ms-title-left"
    ptab2="mainLeft-contentTop2 fl"#"ms-title-right"
    ptab3="mainLeft-contentTop2 fl"#"ms-title-right"
    if (ptype=="1"):
         ptab1="mainLeft-contentTop2 fl"#"ms-title-left"
         ptab2="mainLeft-contentTop1 fl"#"ms-title-right"
         ptab3="mainLeft-contentTop2 fl"#"ms-title-right"
    if (ptype=="0"):
         ptab1="mainLeft-contentTop2 fl"#"ms-title-left"
         ptab2="mainLeft-contentTop2 fl"#"ms-title-right"
         ptab3="mainLeft-contentTop1 fl"#"ms-title-right"
    pingyinlist=getpingyinattribute(pingyin)
    keywords=pingyinlist['keywords']
    if not mobileflag:
        salesproducts=getindexofferlist(keywords,0,15)
        buyproducts=getindexofferlist(keywords,1,15)
        companypricelist=getcompanypricelist(keywords,16,20,searchmode=2)
        bbslist=getindexbbslist(kname=keywords,limitcount=7)
    if not pingyinlist:
        return HttpResponseNotFound("<h1>FORBIDDEN</h1>")
    pingyinname=pingyinlist['label']
    cplist=getcplist(keywords,50)
    if (page==None or page==0):
        page=1
    funpage = zz91page()
    limitNum=funpage.limitNum(20)
    nowpage=funpage.nowpage(int(page))
    frompageCount=funpage.frompageCount()
    after_range_num = funpage.after_range_num(5)
    before_range_num = funpage.before_range_num(9)
    prolist=getproductslist(kname=keywords,frompageCount=frompageCount,limitNum=limitNum,ptype=ptype)
    
    listcount=0
    if (prolist):
        listall=prolist['list']
        listcount=prolist['count']
        if (int(listcount)>1000000):
            listcount=1000000-1
    listcount = funpage.listcount(listcount)
    page_listcount=funpage.page_listcount()
    firstpage = funpage.firstpage()
    lastpage = funpage.lastpage()
    page_range  = funpage.page_range()
    nextpage = funpage.nextpage()
    prvpage = funpage.prvpage()
    hidfloat=1
    
    if mobileflag:
        return render_to_response('mobile/mtrademore.html',locals())
    return render_to_response('new/trademore.html',locals())
def company(request,pingyin):
    mobileflag=request.GET.get("mobileflag")
    cpchickNum(pingyin)
    pingyinlist=getpingyinattribute(pingyin)
    if not pingyinlist:
        return HttpResponseNotFound("<h1>FORBIDDEN</h1>")
    pingyinname=pingyinlist['label']
    keywords=pingyinlist['keywords']
    mingang=getmingganword(keywords)
    if mingang:
        return HttpResponseNotFound("<h1>FORBIDDEN</h1>")
    cplist=getcplist(keywords,50)
    if not mobileflag:
        salesproducts=getindexofferlist(keywords,0,15)
        buyproducts=getindexofferlist(keywords,1,15)
        pcompanylist=getcompanyindexcomplist(keywords,4)
    companylist=getcompanylist(keywords,0,15,15)['list']
    hidfloat=1
    if mobileflag:
        adlist=getadlistkeywords("791",pingyinname)
        return render_to_response('mobile/mcompany.html',locals())
    return render_to_response('new/company.html',locals())
def companymore(request,pingyin,page):
    mobileflag=request.GET.get("mobileflag")
    pingyinlist=getpingyinattribute(pingyin)
    if not pingyinlist:
        return HttpResponseNotFound("<h1>FORBIDDEN</h1>")
    pingyinname=pingyinlist['label']
    keywords=pingyinlist['keywords']
    cplist=getcplist(keywords,50)
    if not mobileflag:
        salesproducts=getindexofferlist(keywords,0,15)
        buyproducts=getindexofferlist(keywords,1,15)
    if (page==None or page==0):
        page=1
    funpage = zz91page()
    limitNum=funpage.limitNum(10)
    nowpage=funpage.nowpage(int(page))
    frompageCount=funpage.frompageCount()
    after_range_num = funpage.after_range_num(5)
    before_range_num = funpage.before_range_num(9)
    
    companylist=getcompanylist(keywords,frompageCount,limitNum,20000)
    listcount=0
    if (companylist):
        listall=companylist['list']
        listcount=companylist['count']
        if (int(listcount)>1000000):
            listcount=1000000-1
    listcount = funpage.listcount(listcount)
    page_listcount=funpage.page_listcount()
    firstpage = funpage.firstpage()
    lastpage = funpage.lastpage()
    page_range  = funpage.page_range()
    nextpage = funpage.nextpage()
    prvpage = funpage.prvpage()
    hidfloat=1
    if mobileflag:
        return render_to_response('mobile/mcompanymore.html',locals())
    return render_to_response('new/companymore.html',locals())
def picture(request,pingyin):
    mobileflag=request.GET.get("mobileflag")
    cpchickNum(pingyin)
    pingyinlist=getpingyinattribute(pingyin)
    if not pingyinlist:
        return HttpResponseNotFound("<h1>FORBIDDEN</h1>")
    pingyinname=pingyinlist['label']
    keywords=pingyinlist['keywords']
    mingang=getmingganword(keywords)
    if mingang:
        return HttpResponseNotFound("<h1>FORBIDDEN</h1>")
    cplist=getcplist(keywords,50)
    if not mobileflag:
        salesproducts=getindexofferlist(keywords,0,9)
        buyproducts=getindexofferlist(keywords,1,9)
        newjoincomplist=getsycompanylist(keywords,0,6,None,6)
    piclist=getproductslist(kname=keywords,frompageCount=0,limitNum=48,havepic=1)
    
    hidfloat=1
    if mobileflag:
        adlist=getadlistkeywords("790",pingyinname)
        return render_to_response('mobile/mpicture.html',locals())
    return render_to_response('new/picture.html',locals())
def picturemore(request,pingyin,page):
    mobileflag=request.GET.get("mobileflag")
    pingyinlist=getpingyinattribute(pingyin)
    if not pingyinlist:
        return HttpResponseNotFound("<h1>FORBIDDEN</h1>")
    pingyinname=pingyinlist['label']
    keywords=pingyinlist['keywords']
    cplist=getcplist(keywords,50)
    if not mobileflag:
        salesproducts=getindexofferlist(keywords,0,9)
        buyproducts=getindexofferlist(keywords,1,9)
        newjoincomplist=getsycompanylist(keywords,0,10,None,10)
    if (page==None or page==0):
        page=1
    funpage = zz91page()
    limitNum=funpage.limitNum(48)
    nowpage=funpage.nowpage(int(page))
    frompageCount=funpage.frompageCount()
    after_range_num = funpage.after_range_num(5)
    before_range_num = funpage.before_range_num(9)
    piclist=getproductslist(kname=keywords,frompageCount=frompageCount,limitNum=limitNum,havepic=1)
    listcount=0
    if (piclist):
        listall=piclist['list']
        listcount=piclist['count']
        if (int(listcount)>1000000):
            listcount=1000000-1
    listcount = funpage.listcount(listcount)
    page_listcount=funpage.page_listcount()
    firstpage = funpage.firstpage()
    lastpage = funpage.lastpage()
    page_range  = funpage.page_range()
    nextpage = funpage.nextpage()
    prvpage = funpage.prvpage()
    hidfloat=1
    
    if mobileflag:
        return render_to_response('mobile/mpicturemore.html',locals())
    return render_to_response('new/picturemore.html',locals())
    
def huzhu(request,pingyin):
    mobileflag=request.GET.get("mobileflag")
    cpchickNum(pingyin)
    pingyinlist=getpingyinattribute(pingyin)
    if not pingyinlist:
        return HttpResponseNotFound("<h1>FORBIDDEN</h1>")
    pingyinname=pingyinlist['label']
    keywords=pingyinlist['keywords']
    mingang=getmingganword(keywords)
    if mingang:
        return HttpResponseNotFound("<h1>FORBIDDEN</h1>")
    if not mobileflag:
        salesproducts=getindexofferlist(keywords,0,9)
        buyproducts=getindexofferlist(keywords,1,9)
    bbslist=getindexbbslist(kname=keywords,limitcount=20,bbs_post_category_id="",searchmode=2)
    cplist=getcplist(keywords,50)
    hidfloat=1
    
    if mobileflag:
        adlist=getadlistkeywords("793",pingyinname)
        return render_to_response('mobile/mhuzhu.html',locals())
    return render_to_response('new/huzhu.html',locals())

def huzhumore(request,pingyin,page):
    mobileflag=request.GET.get("mobileflag")
    pingyinlist=getpingyinattribute(pingyin)
    if not pingyinlist:
        return HttpResponseNotFound("<h1>FORBIDDEN</h1>")
    pingyinname=pingyinlist['label']
    keywords=pingyinlist['keywords']
    cplist=getcplist(keywords,50)
    province = request.GET.get("province")
    if (province=='None' or province==None):
        province=""
    if not mobileflag:
        salesproducts=getindexofferlist(keywords,0,9)
        buyproducts=getindexofferlist(keywords,1,9)
    if (page==None or page==0):
        page=1
    funpage = zz91page()
    limitNum=funpage.limitNum(35)
    nowpage=funpage.nowpage(int(page))
    frompageCount=funpage.frompageCount()
    after_range_num = funpage.after_range_num(5)
    before_range_num = funpage.before_range_num(9)
    bbslist=getbbslist(kname=keywords,frompageCount=frompageCount,limitNum=limitNum,category_id="",searchmode=2)
    listall=bbslist['list']
    listcount=0
    if (bbslist):
        listall=bbslist['list']
        listcount=bbslist['count']
        if (int(listcount)>1000000):
            listcount=1000000-1
    listcount = funpage.listcount(listcount)
    page_listcount=funpage.page_listcount()
    firstpage = funpage.firstpage()
    lastpage = funpage.lastpage()
    page_range  = funpage.page_range()
    nextpage = funpage.nextpage()
    prvpage = funpage.prvpage()
    hidfloat=1
    
    if mobileflag:
        return render_to_response('mobile/mhuzhumore.html',locals())
    return render_to_response('new/huzhumore.html',locals())

def news(request,pingyin,page):
    mobileflag=request.GET.get("mobileflag")
    pingyinlist=getpingyinattribute(pingyin)
    if not pingyinlist:
        return HttpResponseNotFound("<h1>FORBIDDEN</h1>")
    pingyinname=pingyinlist['label']
    keywords=pingyinlist['keywords']
    cplist=getcplist(keywords,50)
    province = request.GET.get("province")
    if (province=='None' or province==None):
        province=""
    if not mobileflag:
        salesproducts=getindexofferlist(keywords,0,9)
        buyproducts=getindexofferlist(keywords,1,9)
        companypricelist=getcompanypricelist(keywords,16,20,searchmode=2)
    bbslist=getindexbbslist(kname=keywords,limitcount=7)
    if (page==None or page==0):
        page=1
    funpage = zz91page()
    limitNum=funpage.limitNum(35)
    nowpage=funpage.nowpage(int(page))
    frompageCount=funpage.frompageCount()
    after_range_num = funpage.after_range_num(5)
    before_range_num = funpage.before_range_num(9)
    newslist=getnewslist(keywords=keywords,frompageCount=frompageCount,limitNum=limitNum,searchmode=2)
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
    
    hidfloat=1
    if mobileflag:
        return render_to_response('mobile/mnews.html',locals())
    return render_to_response('new/news.html',locals())

#优质客户推荐
def carveout(request):
    lb1=gettjhex1()
    lb2=gettjhex2()
    lb3=gettjhex3()
    companycount=getvipcompanycount()
    companylist1=getindexcompanylist_pic(keywords="金属",num=8)
    companylist2=getindexcompanylist_pic(keywords="塑料",num=8)
    companylist3=getindexcompanylist_pic(keywords="纺织品|废纸|二手设备|电子电器|橡胶|轮胎|服务",num=8)
    return render_to_response('carveout/index.html',locals())
#SEO推广页面搜索
def prosearch(request):
    keywords = request.GET.get("keywords")
    if keywords:
        keywords=keywords.replace("利乐","无菌")
        keywords=keywords.replace("利乐包","无菌包")
        keywords_hex=getjiami(keywords)
        nowurl="/cp/pro-"+keywords_hex+".html"
        return HttpResponsePermanentRedirect(nowurl)
    else:
        return HttpResponse("搜索错误！")
#SEO推广客户
def prolist(request,keywords,page=""):
    keywords_hex=keywords
    keywords=getjiami(keywords)
    province = request.GET.get("province")
    
    if keywords:
        xgcategorylist1=getcategorylist(kname=keywords,limitcount=12)
        xgcategorylist2=getcategorylist(kname=keywords,limitcount=30,frompageCount=12)
        
        newslist=getindexbbslist(kname=keywords,limitcount=6)
        pricelist=getindexpricelist(kname=keywords,limitcount=6)
    if province:
        keywords=keywords+" "+province
    pdt_kind = request.GET.get("pdt_kind")
    if not page:
        page=1
    funpage = zz91page()
    limitNum=funpage.limitNum(18)
    nowpage=funpage.nowpage(int(page))
    frompageCount=funpage.frompageCount()
    after_range_num = funpage.after_range_num(2)
    before_range_num = funpage.before_range_num(3)
    companylist=getindexcompanylist_pic(keywords=keywords,num=None,frompageCount=frompageCount,limitNum=limitNum,pdt_kind=pdt_kind,nopic=1)
    listcount=0
    if (companylist):
        listall=companylist['list']
        listcount=companylist['listcount']
        if (int(listcount)>1000000):
            listcount=1000000-1
    listcount = funpage.listcount(listcount)
    page_listcount=funpage.page_listcount()
    firstpage = funpage.firstpage()
    lastpage = funpage.lastpage()
    page_range  = funpage.page_range()
    nextpage = funpage.nextpage()
    prvpage = funpage.prvpage()
    if not listall:
        keywords='暂无'
    return render_to_response('prolist/list.html',locals())

#关键词页面公司
def firm(request,keywords,page=""):
    keywords_hex=keywords
    #keywords=getjiami(keywords)
    province = request.GET.get("province")
    business_mod=request.GET.get("business_mod")
    industry=request.GET.get("industry")
    
    
    if keywords:
        xgcategorylist1=getcategorylist(kname=keywords,limitcount=12)
        xgcategorylist2=getcategorylist(kname=keywords,limitcount=30,frompageCount=12)
        
        newslist=getindexbbslist(kname=keywords_hex,limitcount=6)
        pricelist=getindexpricelist(kname=keywords_hex,limitcount=6)
    if province:
        keywords_hex=keywords_hex+" "+province
    else:
        province=''
    if business_mod:
        keywords_hex=keywords_hex+" "+business_mod
    else:
        business_mod=''
    if industry:
        keywords_hex=keywords_hex+" "+industry
    else:
        industry=''
    pdt_kind = request.GET.get("pdt_kind")
    if (not page):
        page=1
    funpage = zz91page()
    limitNum=funpage.limitNum(4)
    nowpage=funpage.nowpage(int(page))
    frompageCount=funpage.frompageCount()
    after_range_num = funpage.after_range_num(2)
    before_range_num = funpage.before_range_num(3)
    companylist=getcompanylist_firm(kname=keywords_hex,frompageCount=frompageCount,limitNum=limitNum,allnum=1000)
    listcount=0
    if (companylist):
        listall=companylist['list']
        listcount=companylist['count']
        if (int(listcount)>1000000):
            listcount=1000000-1
    listcount = funpage.listcount(listcount)
    page_listcount=funpage.page_listcount()
    firstpage = funpage.firstpage()
    lastpage = funpage.lastpage()
    page_range  = funpage.page_range()
    nextpage = funpage.nextpage()
    prvpage = funpage.prvpage()
    if not listall:
        keywords='暂无'
    business_mod=getbusiness_mod(1020)
    industry_label=getindustry_label(1000)
    arealist=getarealist("10011000")
    return render_to_response('prolist/firm.html',locals())
    
#关键词页面价格

def pro_price(request,keywords,page=""):
    newflag=request.GET.get("newflag")
    mobileflag=request.GET.get("mobileflag")
    province = request.GET.get("province")
    keyword=keywords
    if keywords:
        newslist=getindexbbslist(kname=keywords,limitcount=6)
        pricelist=getindexpricelist(kname=keywords,limitcount=6)
    if province:
        keywords=keywords+" "+province
    else:
        province=''
    mingang=getmingganword(keywords)
    if mingang:
        return HttpResponseNotFound("<h1>FORBIDDEN</h1>")
    if not mobileflag:
        plist_pic=getindexofferlist_pic(kname=keywords,pdt_type=None,limitcount=4)
        salesproducts=getindexofferlist(keywords,0,9)
        buyproducts=getindexofferlist(keywords,1,9)
        newjoincomplist=getsycompanylist(keywords,0,20,None,10)
    arealist=getarealist("10011000")
    if (not page):
        page=1
    funpage = zz91page()
    limitNum=funpage.limitNum(10)
    nowpage=funpage.nowpage(int(page))
    frompageCount=funpage.frompageCount()
    after_range_num = funpage.after_range_num(2)
    before_range_num = funpage.before_range_num(3)
    compnaypricelist=getcompanypricelistmore(kname=keywords,frompageCount=frompageCount,limitNum=limitNum)
    listcount=0
    if (compnaypricelist):
        listall=compnaypricelist['list']
        listcount=compnaypricelist['count']
        if (int(listcount)>1000000):
            listcount=1000000-1
    listcount = funpage.listcount(listcount)
    page_listcount=funpage.page_listcount()
    firstpage = funpage.firstpage()
    lastpage = funpage.lastpage()
    page_range  = funpage.page_range()
    nextpage = funpage.nextpage()
    prvpage = funpage.prvpage()
    pricelist=getindexpricelist(kname=keywords,limitcount=15,searchmode=2)
    cplist=getcplist(keywords,50)
    hidfloat=1
    #----进入手机模版
    if mobileflag:
        adlist=getadlistkeywords("793",pingyinname)
        return render_to_response('mobile/mprice.html',locals())
    arealist=getarealist("10011000")
    return render_to_response('prolist/price.html',locals())

def carveoutmore(request,keywords,page):
    lb1=gettjhex1()
    lb2=gettjhex2()
    lb3=gettjhex3()
    companycount=getvipcompanycount()
    t=request.GET.get("t")
    keywords_hex=keywords
    if (keywords=="c"):
        keywords="废 !金属 & !塑料"
    else:
        keywords=getjiemi(keywords)
    if (page==None):
        page=1
    
    funpage = zz91page()
    limitNum=funpage.limitNum(16)
    nowpage=funpage.nowpage(int(page))
    frompageCount=funpage.frompageCount()
    after_range_num = funpage.after_range_num(5)
    before_range_num = funpage.before_range_num(9)
    companylist=getindexcompanylist_pic(keywords=keywords,num=None,frompageCount=frompageCount,limitNum=16)
    listcount=0
    if (companylist):
        listall=companylist['list']
        listcount=companylist['listcount']
        if (int(listcount)>1000000):
            listcount=1000000-1
    listcount = funpage.listcount(listcount)
    page_listcount=funpage.page_listcount()
    firstpage = funpage.firstpage()
    lastpage = funpage.lastpage()
    page_range  = funpage.page_range()
    nextpage = funpage.nextpage()
    prvpage = funpage.prvpage()
    
    return render_to_response('carveout/list.html',locals())
    
#普通客户推荐
def commoncustomer(request):
    lb1=gettjhex1()
    lb2=gettjhex2()
    lb3=gettjhex3()
    
    companycount=getvipcompanycount()
    companylist1=getcommoncompanylist(keywords="金属",num=8)
    companylist2=getcommoncompanylist(keywords="塑料",num=8)
    companylist3=getcommoncompanylist(keywords="纺织品|废纸|二手设备|电子电器|橡胶|轮胎|服务",num=8)
    return render_to_response('carveout/common.html',locals())

def commoncustomermore(request,keywords,page):
    lb1=gettjhex1()
    lb2=gettjhex2()
    lb3=gettjhex3()
    companycount=getvipcompanycount()
    t=request.GET.get("t")
    keywords_hex=keywords
    if (keywords=="c"):
        keywords="废 !金属 & !塑料"
    else:
        keywords=getjiemi(keywords)
    if (page==None):
        page=1
    
    funpage = zz91page()
    limitNum=funpage.limitNum(16)
    nowpage=funpage.nowpage(int(page))
    frompageCount=funpage.frompageCount()
    after_range_num = funpage.after_range_num(4)
    before_range_num = funpage.before_range_num(4)
    companylist=getcommoncompanylist(keywords=keywords,num=None,frompageCount=frompageCount,limitNum=16,pic=None,companyflag="1")
    company6=getcommoncompanylist(keywords=keywords,num=None,frompageCount=0,limitNum=6,pic=None,companyflag=1)
    listcount=0
    if (companylist):
        listall=companylist['list']
        listcount=companylist['listcount']
        if (int(listcount)>1000000):
            listcount=1000000-1
    listcount = funpage.listcount(listcount)
    page_listcount=funpage.page_listcount()
    firstpage = funpage.firstpage()
    lastpage = funpage.lastpage()
    page_range  = funpage.page_range()
    nextpage = funpage.nextpage()
    prvpage = funpage.prvpage()
    
    return render_to_response('carveout/commonlist.html',locals())

#微信2014开春专题
def weixin2014(request):
    page=request.GET.get("page")
    if (page==None):
        page=1
    funpage = zz91page()
    limitNum=funpage.limitNum(16)
    nowpage=funpage.nowpage(int(page))
    frompageCount=funpage.frompageCount()
    after_range_num = funpage.after_range_num(5)
    before_range_num = funpage.before_range_num(9)
    companylist=getweixincomplist(frompageCount=frompageCount,limitNum=limitNum)
    listcount=0
    if (companylist):
        listall=companylist['list']
        listcount=companylist['listcount']
        if (int(listcount)>1000000):
            listcount=1000000-1
    listcount = funpage.listcount(listcount)
    page_listcount=funpage.page_listcount()
    firstpage = funpage.firstpage()
    lastpage = funpage.lastpage()
    page_range  = funpage.page_range()
    nextpage = funpage.nextpage()
    prvpage = funpage.prvpage()
    return render_to_response('weixin2014/index.html',locals())
    

def viewer_404(request):
    t = get_template('404.html')
    html = t.render(Context())
    return HttpResponseNotFound(html)
def viewer_500(request):
    t = get_template('404.html')
    html = t.render(Context())
    return HttpResponseNotFound(html)

        