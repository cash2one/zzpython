#-*- coding:utf-8 -*-
from django.shortcuts import render_to_response
from django.http import HttpResponse,HttpResponseRedirect,HttpResponsePermanentRedirect
import MySQLdb,sys,os,memcache,settings,urllib,re,time,datetime,requests,simplejson
from settings import pyuploadpath,pyimgurl,spconfig
from django.core.cache import cache
from django.utils.http import urlquote
from operator import itemgetter, attrgetter
from datetime import timedelta,date
from sphinxapi import *
from zz91page import *
import chardet
from zz91db_ast import companydb
dbc=companydb()
reload(sys)
sys.setdefaultencoding('UTF-8')
nowpath=os.path.dirname(__file__)
execfile(nowpath+"/func/ye_function.py")
execfile(nowpath+"/func/public_function.py")
execfile(nowpath+"/func/company_function.py")
zzc=zzcompany()
zzy=zye()
#url对应market表字段
code_map={
              "1000":"废金属",
              "10001000":"废钢铁",
              "10001001":"有色金属",
              "10001010":"稀贵金属",
              "10001011":"混合金属",
              "10001100":"再生金属",
              "10001101":"废金属处理设备",
              "1001":"废塑料",
              "10011000":"再生颗粒",
              "10011001":"塑料助剂",
              "10011010":"废塑料加工设备",
              "1002":"二手设备",
              "100210000":"交通工具",
              "100210001":"机床设备",
              "100210010":"工程设备",
              "100210011":"化工设备",
              "100211000":"制冷设备",
              "100211001":"纺织设备",
              "100211010":"电子设备",
              "100211011":"电力设备",
              "100211100":"矿业设备",
              "100211101":"塑料设备",
              "100211110":"印刷设备",
              };
industry_code_map={
                   '废塑料':"10001000",
                   '废金属':"10001001",
                   '二手设备':"10001007",
                   };
industry_code_map_reverse={
                    "10001000":'废塑料',
                    "10001001":'废金属',
                    "10001007":'二手设备' ,   
                   };
#产业带列表页
def ye_list(request,big_category='',small_category=''):
    page = request.GET.get("page")
    keywords=request.GET.get("keywords")
    province = request.GET.get("province")
    #arealist=['浙江','广东','江苏','福建','安徽','河南','河北','湖北','湖南','四川','江西','山东','海南','黑龙江','北京','上海','天津','青海','陕西','山西','贵州','辽宁','宁夏','吉林','内蒙古','广西','云南','西藏','重庆','甘肃','新疆','台湾','香港','澳门']
    #province=''
    #根据url获得产业带类型和行业类别
    industry=code_map[str(big_category)]
    category=None
    if small_category:
        category=code_map[str(small_category)]
    if not page:
        page=1
    funpage=zz91page()
    limitNum=funpage.limitNum(10)
    nowpage=funpage.nowpage(int(page))
    frompageCount=funpage.frompageCount()
    after_range_num = funpage.after_range_num(8)
    before_range_num = funpage.before_range_num(9)
    marketlistall=zzy.getmarketlist(frompageCount=frompageCount,limitNum=limitNum,industry=industry,category=category,province=province)
    marketlist=marketlistall['list']
    listcount=marketlistall['count']
    if (int(listcount)>1000000):
        listcount=1000000-1
    listcount = funpage.listcount(listcount)
    page_listcount=funpage.page_listcount()
    firstpage = funpage.firstpage()
    lastpage = funpage.lastpage()
    page_range  = funpage.page_range()
    nextpage = funpage.nextpage()
    prvpage = funpage.prvpage()
    datatype=request.GET.get("datatype")
    if datatype=="json":
        return HttpResponse(simplejson.dumps(marketlistall, ensure_ascii=False))

def ye_prolist(request,id):
    page=request.GET.get("page")
    if (page==None):
        page=1
    funpage = zz91page()
    limitNum=funpage.limitNum(10)
    nowpage=funpage.nowpage(int(page))
    frompageCount=funpage.frompageCount()
    after_range_num = funpage.after_range_num(5)
    before_range_num = funpage.before_range_num(4)
    productListall=zzy.getyeproductslist(frompageCount,limitNum,market_id=id)
    productList=productListall['list']
    productListcount=productListall['count']
    listcount=productListcount
    if (int(listcount)>100000):
        listcount=100000
    listcount = funpage.listcount(listcount)
    page_listcount=funpage.page_listcount()
    firstpage = funpage.firstpage()
    lastpage = funpage.lastpage()
    page_range  = funpage.page_range()
    nextpage = funpage.nextpage()
    prvpage = funpage.prvpage()
    datatype=request.GET.get("datatype")
    if datatype=="json":
        return HttpResponse(simplejson.dumps(productList, ensure_ascii=False))
def ye_complist(request,id):
    page=request.GET.get("page")
    if (page==None):
        page=1
    funpage = zz91page()
    limitNum=funpage.limitNum(10)
    nowpage=funpage.nowpage(int(page))
    frompageCount=funpage.frompageCount()
    after_range_num = funpage.after_range_num(5)
    before_range_num = funpage.before_range_num(4)
    companylistall=zzy.getcompanylist(frompageCount,limitNum,market_id=id)
    companylist=companylistall['list']
    companylistcount=companylistall['count']
    listcount=companylistcount
    if (int(listcount)>100000):
        listcount=100000
    listcount = funpage.listcount(listcount)
    page_listcount=funpage.page_listcount()
    firstpage = funpage.firstpage()
    lastpage = funpage.lastpage()
    page_range  = funpage.page_range()
    nextpage = funpage.nextpage()
    prvpage = funpage.prvpage()
    datatype=request.GET.get("datatype")
    if datatype=="json":
        return HttpResponse(simplejson.dumps(companylist, ensure_ascii=False))
#详细
def ye_detail(request,ye_pinyin):
    host=getnowurl(request)
    company_id=request.GET.get("company_id",None)
    ye_detailalllist=zzy.getmarketdetail(ye_pinyin=ye_pinyin)
    ye_detaillist=ye_detailalllist['list']
    ye_imglist=ye_detailalllist['pic_img']
    #判断当前登录用户是否已经加入该产业带来改变加入或退出的显示
    is_quit=0
    if company_id:
        is_quit=zzy.is_in_market(market_id=ye_detaillist['id'],company_id=company_id)
    #计算图片个数放入slide
    p_list=ye_imglist['pic_address']
    
    #市场id
    market_id=ye_detaillist['id']
    
    #-----
    #底部标签显示供求
    #productList=zzy.getyeproductslist(0,10,market_id=market_id)
    #if productList:
        #productList=productList['list']
    #底部显示公司黄页
    #companylistall=zzy.getcompanylist(0,10,market_id=market_id)
    #companylist=companylistall['list']
    #companylistcount=companylistall['count']
    jsonlist={'piclist':p_list,'detail':ye_detaillist,'is_quit':is_quit,'ye_pinyin':ye_pinyin}
    datatype=request.GET.get("datatype")
    if datatype=="json":
        return HttpResponse(simplejson.dumps(jsonlist, ensure_ascii=False))


#加入市场
def join_ye(request):
    host=getnowurl(request)
    datatype=request.GET.get("datatype")
    company_id=request.GET.get("company_id",None)
    """
    usertoken=request.GET.get("usertoken")
    if not getloginstatus(company_id,usertoken):
        errlist={'tokenerr':'true'}
        return HttpResponse(simplejson.dumps(errlist, ensure_ascii=False))
    """
    if ((company_id==None or str(company_id)=="0")):
        jsonlist={'err':'true','result':'系统错误'}
        return HttpResponse(simplejson.dumps(jsonlist, ensure_ascii=False))
    
    industry=request.GET.get("industry")
    industry=str(industry)
    areatxt=request.GET.get("area")
    market_id=request.GET.get("id")
    user_info=zzy.get_user_info(company_id)
    industry_code=user_info['industry_code']
    area_code=user_info['area_code']
    #如果用户信息填写到市则可加入
    if len(area_code)>=16:
        if len(area_code)==20:
            area_code=area_code[:4]
        if (industry_code_map[str(industry)]==str(industry_code) and zzy.isequal_area(area_code,areatxt)):
            zzy.join_market(company_id=company_id,market_id=market_id)
            jsonlist={'err':'false','result':'加入成功！'}
        else:
            jsonlist={'err':'true','result':'对不起,您的公司主营行业或公司地址不符合该市场入驻条件，您将无法入驻该市场如果您的公司经营地址有误，请修改公司地址后重新入驻！'}
    else:
        jsonlist={'err':'true','result':'对不起,您的公司主营行业或公司地址不符合该市场入驻条件，您将无法入驻该市场如果您的公司经营地址有误，请修改公司地址后重新入驻！'}
    return HttpResponse(simplejson.dumps(jsonlist, ensure_ascii=False))
#退出市场
def quit_ye(request):
    #自定义用户
    market_id=request.GET.get("id")
    zzy.quit_market(company_id,market_id)
    return HttpResponse('ok，已退出') 
    