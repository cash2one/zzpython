#-*- coding:utf-8 -*-
from django.shortcuts import render_to_response
from django.http import HttpResponse,HttpResponseRedirect,HttpResponseNotFound,HttpResponsePermanentRedirect
from django.views.decorators.csrf import csrf_exempt
from django.core.cache import cache
from zz91db import zz91news,getlightkeywords
from zz91settings import SPHINXCONFIG
from zz91tools import filter_tags,getjiami,getjiemi,subString,formattime,getpastday,int_to_str,int_to_str2,str_to_int,str_to_date,date_to_int,date_to_str,getpastoneday,getnextdate,getTomorrow,mobileuseragent
from zz91db_ast import companydb
from zz91page import *
from sphinxapi import *
import MySQLdb,os,datetime,time,sys,calendar,urllib,simplejson,requests
try:
    import cStringIO as StringIO
except ImportError:
    import StringIO
dbc=companydb()

reload(sys)
sys.setdefaultencoding('UTF-8')
nowpath=os.path.dirname(__file__)
execfile(nowpath+"/func/function.py")
zzcomp=zz91company()
#首页
def index(request):
    type=''
    #每日推荐
    pricelist=zzcomp.getpricedblist(frompageCount=0,limitNum=3,assist_type_id=362)
    if len(pricelist['list'])>=3:
        price1=pricelist['list'][0]
        price2=pricelist['list'][1]
        price3=pricelist['list'][2]
    #废金属
    pricelist=zzcomp.getpricedblist(frompageCount=0,limitNum=8,typeid="359,360")
    #右侧列表数据
    #行业报告
    price_hy_top=zzcomp.getpricedblist(frompageCount=0,limitNum=1,typeid=357)
    price_hy=zzcomp.getpricedblist(frompageCount=1,limitNum=5,typeid=357)
    #专家解读
    price_zj_top=zzcomp.getpricedblist(frompageCount=0,limitNum=1,typeid=358)
    price_zj=zzcomp.getpricedblist(frompageCount=1,limitNum=5,typeid=358)
    #废金属市场价格
    price_js=zzcomp.getpricedblist(frompageCount=0,limitNum=5,typeid=216)
    #废塑料市场价格
    price_sl=zzcomp.getpricedblist(frompageCount=0,limitNum=5,typeid=217)
    
    
    return render_to_response('study/index.html',locals())
def indexlistjson(request):
    typeid="359,360"
    page=request.GET.get("page")
    if not page:
        page=1
    funpage=zz91page()
    limitNum=funpage.limitNum(8)
    nowpage=funpage.nowpage(int(page))
    frompageCount=funpage.frompageCount()
    after_range_num = funpage.after_range_num(3)
    before_range_num = funpage.before_range_num(6)
    pricelist=zzcomp.getpricedblist(frompageCount=frompageCount,limitNum=limitNum,typeid=typeid)
    listcount=0
    plist=pricelist['list']
    listcount=pricelist['count']
    if (int(listcount)>1000000):
        listcount=1000000-1
    listcount = funpage.listcount(listcount)
    page_listcount=funpage.page_listcount()
    firstpage = funpage.firstpage()
    lastpage = funpage.lastpage()
    page_range  = funpage.page_range()
    if len(page_range)>7:
        page_range=page_range[:7]
    nextpage = funpage.nextpage()
    if nextpage>=page_listcount:
        nextpage=page_listcount
    prvpage = funpage.prvpage()
    if prvpage<=1:
        prvpage=1
    if int(page)>3:
        pricelist=None
    return HttpResponse(simplejson.dumps(plist, ensure_ascii=False))
#列表
def list(request,type='',type1='',assist='',page=''):
    category=zzcomp.getcategorydetail(type)
    typeid=category['id']
    if category:
        seotitle=category['name']
        if page:
            seotitle=seotitle+"_第"+str(page)+"页"
        seotitle=seotitle+"_再生资源行情研究院 -ZZ91再生网"
        seokeywords=category['name']
    
    if type1=="fsl":
        seotitle="废塑料行情研究院"
        if page:
            seotitle=seotitle+"_第"+str(page)+"页"
        seotitle=seotitle+" -ZZ91再生网"
        seokeywords="废塑料行情研究院"
    if type1=="fjs":
        seotitle="废金属行情研究院"
        if page:
            seotitle=seotitle+"_第"+str(page)+"页"
        seotitle=seotitle+" -ZZ91再生网"
        seokeywords="废金属行情研究院"
    categoryname1=''
    if category:
        categoryname1=category['name']
    if type1:
        category=zzcomp.getcategorydetail(type+"/"+type1)
        typeid=category['id']
    #导航条
    navlist=''
    if categoryname1:
        navlist+=" > <a href='/study/"+str(type)+"/'>"+categoryname1+"</a>"
    if type1:
        navlist+=" > <a href='/study/"+str(type)+"/"+str(type1)+"/'>"+category['name']+"</a>"
        
        
    else:
        if type=="djgd":
            typeid="359,360"
    #右侧列表数据
    #行业报告
    price_hy_top=zzcomp.getpricedblist(frompageCount=0,limitNum=1,typeid=357)
    price_hy=zzcomp.getpricedblist(frompageCount=1,limitNum=5,typeid=357)
    #专家解读
    price_zj_top=zzcomp.getpricedblist(frompageCount=0,limitNum=1,typeid=358)
    price_zj=zzcomp.getpricedblist(frompageCount=1,limitNum=5,typeid=358)
    #废金属市场价格
    price_js=zzcomp.getpricedblist(frompageCount=0,limitNum=5,typeid=216)
    #废塑料市场价格
    price_sl=zzcomp.getpricedblist(frompageCount=0,limitNum=5,typeid=217)
    
    if not page:
        page=1
    funpage=zz91page()
    limitNum=funpage.limitNum(8)
    nowpage=funpage.nowpage(int(page))
    frompageCount=funpage.frompageCount()
    after_range_num = funpage.after_range_num(3)
    before_range_num = funpage.before_range_num(6)
    pricelist=zzcomp.getpricedblist(frompageCount=frompageCount,limitNum=limitNum,typeid=typeid,assist_type_id=assist)
    listcount=0
    plist=pricelist['list']
    listcount=pricelist['count']
    if (int(listcount)>1000000):
        listcount=1000000-1
    listcount = funpage.listcount(listcount)
    page_listcount=funpage.page_listcount()
    firstpage = funpage.firstpage()
    lastpage = funpage.lastpage()
    page_range  = funpage.page_range()
    if len(page_range)>7:
        page_range=page_range[:7]
    nextpage = funpage.nextpage()
    if nextpage>=page_listcount:
        nextpage=page_listcount
    prvpage = funpage.prvpage()
    if prvpage<=1:
        prvpage=1
    
    return render_to_response('study/list.html',locals())

def detail(request,id='',type='',type1='',assist=''):
    category=zzcomp.getcategorydetail(type)
    typeid=category['id']
    categoryname1=''
    if category:
        categoryname1=category['name']
    if type1:
        category=zzcomp.getcategorydetail(type+"/"+type1)
        typeid=category['id']
    #导航条
    navlist=''
    if categoryname1:
        navlist+=" > <a href='/study/"+str(type)+"/'>"+categoryname1+"</a>"
    if type1:
        navlist+=" > <a href='/study/"+str(type)+"/"+str(type1)+"/'>"+category['name']+"</a>"
    #右侧列表数据
    #行业报告
    price_hy_top=zzcomp.getpricedblist(frompageCount=0,limitNum=1,typeid=357)
    price_hy=zzcomp.getpricedblist(frompageCount=1,limitNum=5,typeid=357)
    #专家解读
    price_zj_top=zzcomp.getpricedblist(frompageCount=0,limitNum=1,typeid=358)
    price_zj=zzcomp.getpricedblist(frompageCount=1,limitNum=5,typeid=358)
    #废金属市场价格
    price_js=zzcomp.getpricedblist(frompageCount=0,limitNum=5,typeid=216)
    #废塑料市场价格
    price_sl=zzcomp.getpricedblist(frompageCount=0,limitNum=5,typeid=217)
    
    if id:
        detail=zzcomp.getpricedetail(id)
    prenextlist=zzcomp.getpre_nextprice(id,typeid=typeid)
    return render_to_response('study/detail.html',locals())