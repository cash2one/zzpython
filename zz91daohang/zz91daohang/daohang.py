#-*- coding:utf-8 -*-
import MySQLdb   
import settings
import codecs
from django.utils.http import urlquote
from django.shortcuts import render_to_response
from django.http import HttpResponse,HttpResponseRedirect,HttpResponseForbidden,HttpResponsePermanentRedirect
from django.core.paginator import Paginator,InvalidPage,EmptyPage,PageNotAnInteger
import time
import sys,requests
import urllib2
import datetime
from datetime import timedelta, date 
from django.views.decorators.cache import cache_control
import os
from django.core.cache import cache
import random
import shutil
import hashlib
try:
    import cPickle as pickle
except ImportError:
    import pickle

from math import ceil

from sphinxapi import *
from zz91page import *
from zz91settings import SPHINXCONFIG,limitpath
from zz91tools import mobileuseragent

from zz91db_ast import companydb
dbc=companydb()
from zz91db_tags import zztagsdb
dbt=zztagsdb()
from zz91db_ads import adsdb
dba=adsdb()
from zz91db_2_news import newsdb
dbn=newsdb()

nowpath=os.path.dirname(__file__)
execfile(nowpath+"/conn.py")
execfile(nowpath+"/commfunction.py")

def index(request,tags_id="",code=""):
    mobileflag=request.GET.get("mobileflag")
    if mobileflag:
        return HttpResponsePermanentRedirect("http://m.zz91.com/category/")
    bignavlist=getindexcategorylist("",0)
    listall=[]
    for nav in bignavlist:
        code=nav['code']
        toplist=None
        if code=="1000":
            toplist=getdaohanglist1("6,7,8,9,10,11",10)
        if code=="1001":
            toplist=getdaohanglist1("12,13,14",10)
        if code=="1002":
            toplist=getdaohanglist1("16",10)
        if code=="1003":
            toplist=getdaohanglist1("19",10)
        if code=="1004":
            toplist=getdaohanglist1("15",10)
        if code=="1005":
            toplist=getdaohanglist1("17",10)
        if code=="1007":
            toplist=getdaohanglist1("18",10)
        if code=="1008" or code=="1006":
            toplist=getdaohanglist1("20",10)
        if code=="1009":
            toplist=getdaohanglist1("21",10)
        if code=="1010":
            toplist=getdaohanglist1("16",10)
        if code=="1011":
            toplist=getdaohanglist1("16",10)
        nav['navchild']=gettagstypelist(code,0,40,40)['list']
        nav['toplist']=toplist
        listall.append(nav)
    return render_to_response('default.html',locals())
def tagslist(request,code="",page=""):
    if code:
        navlabel=getcategory_productsname(code)
    if not page:
        page=1
    funpage = zz91page()
    limitNum=funpage.limitNum(200)
    nowpage=funpage.nowpage(int(page))
    frompageCount=funpage.frompageCount()
    after_range_num = funpage.after_range_num(5)
    before_range_num = funpage.before_range_num(9)
    navlist=gettagstypelist(code,frompageCount,limitNum,100000)
    
    listall=navlist['list']
    listcount=navlist['count']
    if (int(listcount)>1000000):
        listcount=1000000-1
    listcount = funpage.listcount(listcount)
    page_listcount=funpage.page_listcount()
    firstpage = funpage.firstpage()
    lastpage = funpage.lastpage()
    page_range  = funpage.page_range()
    nextpage = funpage.nextpage()
    prvpage = funpage.prvpage()
    mobileflag=request.GET.get("mobileflag")
    if mobileflag:
        return render_to_response('mobile/mcategory.html',locals())
    return render_to_response('tagslist.html',locals())

def detail(request,code="",tags_id=""):
    mobileflag=request.GET.get("mobileflag")
    keywords=gettagslabel(tags_id)
    label=keywords
    if "毛片" in label:
        return HttpResponseRedirect("http://www.zjfriend.com")
    mingang=getmingganword(keywords)
    if mingang:
        return HttpResponseForbidden("<h1>FORBIDDEN</h1>")
    if mobileflag:
        return HttpResponsePermanentRedirect("http://m.zz91.com/offerlist/?keywords="+str(keywords))
    toplabel=keywords
    #dadlist=getadlist(751,keywords)
    seolist=getseolist()
    cplist=getcplist(keywords,50)
    tagslist=newtagslist(keywords,20)
    searchlist=getcategorylist(keywords,20)
    rightpricelistnav=getrightpricenav(code)
    newslist=getnewslist(keywords=keywords,frompageCount=0,limitNum=12,allnum=12)
    offerlist=getofferlist(kname=keywords,num=4)
    companyprice=getpricelist_company(keywords,7)
    huzhulist=getbbslist(keywords,20)
    companylist=getcompanyindexcomplist(keywords,6)
    companycount=getcompanyallcout()
    procount=getproallcout()
    companycountvip=getcompanyallcout(vip=1)
    pricelist=getpricealllist(keywords,7)
    navlist=getnav(tags_id)
    
    priceurl="http://jiage.zz91.com/s/"+getjiami(label)+"-0/"
    newsurl="http://news.zz91.com/column_list/tags-"+getjiami(label)+".html"
    companyurl="http://company.zz91.com/index-p-"+label+".htm"
    return render_to_response('detail.html',locals())

def default(request,daohangid=''):
    
    listall1=getdaohanglist(8)
    listall2=getdaohanglist(7)
    listall3=getdaohanglist(6)
    listall4=getdaohanglist(9)
    listall5=getdaohanglist(10)
    listall6=getdaohanglist(11)
    listall7=getdaohanglist(12)
    listall8=getdaohanglist(13)
    listall9=getdaohanglist(14)
    listall10=getdaohanglist(15)
    listall11=getdaohanglist(16)
    listall12=getdaohanglist(17)
    listall13=getdaohanglist(18)
    listall14=getdaohanglist(19)
    listall15=getdaohanglist(20)
    listall16=getdaohanglist(21)
    listall17=getdaohanglist(955)
    priceInfo_gang=getpricelist_daohang(kname='钢'.decode('utf-8'),limitcount=6,titlelen=50)
    priceInfo_tong=getpricelist_daohang(kname='铜'.decode('utf-8'),limitcount=6,titlelen=50)
    priceInfo_tie=getpricelist_daohang(kname='铁'.decode('utf-8'),limitcount=6,titlelen=50)
    priceInfo_ysjs=getpricelist_daohang(kname='有色金属'.decode('utf-8'),limitcount=10,titlelen=50)
    priceInfo_gjs=getpricelist_daohang(kname='贵金属'.decode('utf-8'),limitcount=6,titlelen=50)
    priceInfo_feijs=getpricelist_daohang(kname='金属'.decode('utf-8'),limitcount=6,titlelen=50)
    priceInfo_feisl=getpricelist_daohang(kname='塑料'.decode('utf-8'),limitcount=6,titlelen=50)
    priceInfo_slkl=getpricelist_daohang(kname='颗粒'.decode('utf-8'),limitcount=6,titlelen=50)
    priceInfo_slscjg=getpricelist_daohang(kname='塑料 市场价格'.decode('utf-8'),limitcount=6,titlelen=50)
    priceInfo_feizhi=getpricelist_daohang(kname='纸'.decode('utf-8'),limitcount=6,titlelen=50)
    priceInfo_feixj=getpricelist_daohang(kname='橡胶'.decode('utf-8'),limitcount=6,titlelen=50)
    priceInfo_feidz=getpricelist_daohang(kname='电子'.decode('utf-8'),limitcount=6,titlelen=50)
    priceInfo_jixshebei=getpricelist_daohang(kname='机械 设备'.decode('utf-8'),limitcount=6,titlelen=50)
    offerlist_fangzhi=offerlist(kname='纺织'.decode('utf-8'),limitcount=6)
    offerlist_qit=offerlist(kname='玻璃 木料'.decode('utf-8'),limitcount=6)
    offerlist_fuwu=offerlist(kname='报关 通关 清关'.decode('utf-8'),limitcount=6)
    
    #----进入手机模版
    agent=request.META['HTTP_USER_AGENT']
    agentflag=mobileuseragent(agent)
    if daohangid:
        if agentflag:
            categorylist=getdaohanglist(daohangid)
            return render_to_response('mobile/mindexdetail.html',locals())
        else:
            return HttpResponsePermanentRedirect('/')
    else:
        if agentflag:
            categorylist=getmdaohanglist()
            return render_to_response('mobile/mindex.html',locals())
    return render_to_response('daohang_index.html',locals())
def daohangdetail_o(request , pingyin,path):
    done="http://www2.zz91.com/specialsubject/"+pingyin+"/"+path
    return HttpResponseRedirect(done)
def daohangdetail(request , pingyin):
    host = request.META['HTTP_HOST']
    if (pingyin=="kuaijie"):
        offerSalesinfo=offerlist(kname='',pdt_type=0,limitcount=7)
        offerBuyinfo=offerlist(kname='',pdt_type=1,limitcount=7)
        return render_to_response('kuaijie/index.html',locals())
        return False;
        closeconn()
    sql="select label,templates,keywords,keywords1,num_str,keywords2,keywords3,sid,id from daohang where pingyin=%s"
    #cursor.execute(sql,pingyin)
    #daohanglist=cursor.fetchone()
    daohanglist=dbc.fetchonedb(sql,pingyin)
    if (daohanglist):
        label=daohanglist[0]
        mingang=getmingganword(label)
        if mingang:
            return HttpResponseForbidden("<h1>FORBIDDEN</h1>")
        keywords=daohanglist[2]
        keywords1=daohanglist[3]
        keywords2=daohanglist[5]
        keywords3=daohanglist[6]
        num_str=daohanglist[4]
        sid=daohanglist[7]
        id=daohanglist[8]
        daohanglist_child=getdaohanglist_child(id)
        daohangtoplist=getdaohanglist(id)
        if (keywords=='' or keywords==None):
            keywords=label
        if (keywords1=='' or keywords1==None):
            keywords1=label
        if (keywords2=='' or keywords2==None):
            keywords2=label
        if (keywords3=='' or keywords3==None):
            keywords3=label
        daohangtemplate=daohanglist[1]
        adkeywords=urlquote(keywords)
        label_hex=getjiami(label)
        keywords_hex=getjiami(keywords)
        keywords2_hex=getjiami(keywords2)

        #最新报价行情信息
        if (pingyin in ["hdpe","HDPE","feitong","buxiugangjiage","steel","feitie","shenghuofeizhi","feisuliaowang","feilvjiage"]):
            priceInfo_new_num=15
            if pingyin in ["feitong","buxiugangjiage","steel","feitie","feilvjiage","feisuliaowang"]:
                priceInfo_new_num=15
            if pingyin in ["shenghuofeizhi"]:
                priceInfo_new_num=16
            if pingyin in ["hdpe","HDPE"]:
                priceInfo_new_num=15
            
            offerSalesinfo_num=12
            offerBuyinfo_num=17
            huzhuInfo_num=18
            newsinfo_num=17
        else:
            offerSalesinfo_num=12
#            offerSalesinfo_num=getnum_str(num_str,'offerSalesinfo',9)
            #offerBuyinfo_num=getnum_str(num_str,'offerBuyinfo',15)
            offerBuyinfo_num=17
            newsinfo_num=17
            #priceInfo_new_num=getnum_str(num_str,'priceInfo_new',25)
            priceInfo_new_num=15
            huzhuInfo_num=18
        if pingyin in ["petpingpian"]:
            keywords2="pet"
        else:
            keywords2=keywords
            #huzhuInfo_num=getnum_str(num_str,'huzhuInfo',25)
        
        priceInfo_new=getpricelist_daohang(kname=keywords2,limitcount=priceInfo_new_num,titlelen=100)
        number_price=len(priceInfo_new)
        if number_price<priceInfo_new_num:
            num_company=priceInfo_new_num-number_price
            pricelist_company=getpricelist_company(kname=keywords,num=num_company)
        else:
            num_company=priceInfo_new_num
        
        
        #最新互助信息
        #huzhuInfo_new_num=getnum_str(num_str,'huzhuInfo_new',25)
        #huzhuInfo_new=getbbslist_daohang(keywords,huzhuInfo_new_num)
        #标签
        #tagsinfo_num=getnum_str(num_str,'tagsinfo',20)
        #tagsinfo=gettagslist(keywords,tagsinfo_num)
        
        #        offerSalesinfo_num2=getnum_str(num_str,'offerSalesinfo',2)
        offerSalesinfo2=offerlist(kname=keywords,pdt_type="0",limitcount=2,havepic=1,fromlimit=0)
        newslist=getnewslist(keywords=keywords2,frompageCount=0,limitNum=newsinfo_num,typeid="",allnum=newsinfo_num,typeid2="",contentflag="")
        
#        offerSalesinfo_num=getnum_str(num_str,'offerSalesinfo',25)
        offerSalesinfo=offerlist(kname=keywords,pdt_type="0",limitcount=offerSalesinfo_num,fromlimit=2)

        daohangtype=getdaohangtype(pingyin)
        feijinshu=[6,7,8,9,10,11]
        feisuliao=[12,13,14]
        if daohangtype in feijinshu:
            code_type=1
        elif daohangtype in feisuliao:
            code_type=2
        else:
            code_type=''

#        offerBuyinfo_num=getnum_str(num_str,'offerBuyinfo',25)
        offerBuyinfo=offerlist(kname=keywords,pdt_type="1",limitcount=offerBuyinfo_num)
        #江浙沪报价
        #priceInfo_jzf_num=getnum_str(num_str,'priceInfo_jzf',25)
        #priceInfo_jzf=getpricelist_daohang(kname=keywords,assist_type_id=53,limitcount=priceInfo_jzf_num)
        #广东地区
        #priceInfo_gd_num=getnum_str(num_str,'priceInfo_gd',25)
        #priceInfo_gd=getpricelist_daohang(kname=keywords+' 广东'.decode('utf-8'),limitcount=priceInfo_gd_num)
        #清远地区
        #priceInfo_qy_num=getnum_str(num_str,'priceInfo_qy',25)
        #priceInfo_qy=getpricelist_daohang(kname=keywords,assist_type_id=59,limitcount=priceInfo_qy_num)
        #天津地区
        #priceInfo_tj_num=getnum_str(num_str,'priceInfo_tj',25)
        #priceInfo_tj=getpricelist_daohang(kname=keywords,assist_type_id=57,limitcount=priceInfo_tj_num)
        #南海
        #priceInfo_nanhai_num=getnum_str(num_str,'priceInfo_nanhai',25)
        #priceInfo_nanhai=getpricelist_daohang(kname=keywords,assist_type_id=54,limitcount=priceInfo_nanhai_num)
        #上海地区
        #priceInfo_sh_num=getnum_str(num_str,'priceInfo_sh',25)
        #priceInfo_sh=getpricelist_daohang(kname=keywords+' 上海'.decode('utf-8'),limitcount=priceInfo_sh_num)
        #华通地区
        #priceInfo_ht_num=getnum_str(num_str,'priceInfo_ht',25)
        #priceInfo_ht=getpricelist_daohang(kname=keywords+' 华通'.decode('utf-8'),limitcount=priceInfo_ht_num)
        #北京地区
        #priceInfo_bj_num=getnum_str(num_str,'priceInfo_bj',25)
        #priceInfo_bj=getpricelist_daohang(kname=keywords+' 北京'.decode('utf-8'),limitcount=priceInfo_bj_num)
        #全国各地地区
        #priceInfo_qggd_num=getnum_str(num_str,'priceInfo_qggd',25)
        #priceInfo_qggd=getpricelist_daohang(kname=keywords+' 全国各地'.decode('utf-8'),limitcount=priceInfo_qggd_num)
        #汩罗
        #priceInfo_miluo_num=getnum_str(num_str,'priceInfo_miluo',25)
        #priceInfo_miluo=getpricelist_daohang(kname=keywords+' 汩罗'.decode('utf-8'),limitcount=priceInfo_miluo_num)
        #长葛
        #priceInfo_changge_num=getnum_str(num_str,'priceInfo_changge',25)
        #priceInfo_changge=getpricelist_daohang(kname=keywords+' 长葛'.decode('utf-8'),limitcount=priceInfo_changge_num)
        #临沂
        #priceInfo_lingx_num=getnum_str(num_str,'priceInfo_lingx',25)
        #priceInfo_lingx=getpricelist_daohang(kname=keywords+' 临沂'.decode('utf-8'),limitcount=priceInfo_lingx_num)
        #天津山东
        #priceInfo_tianshang_num=getnum_str(num_str,'priceInfo_tianshang',25)
        #priceInfo_tianshang=getpricelist_daohang(kname=keywords+' 天津 山东'.decode('utf-8'),limitcount=priceInfo_tianshang_num)
        
        """
        #行情动态
        priceInfo_hangqing_num=getnum_str(num_str,'priceInfo_hangqing',30)
        port = settings.SPHINXCONFIG['port']
        cl = SphinxClient()
        cl.SetServer ( settings.SPHINXCONFIG['serverid'], port )
        cl.SetMatchMode ( SPH_MATCH_BOOLEAN )
        cl.SetSortMode( SPH_SORT_EXTENDED,"gmt_order desc" )
        cl.SetLimits (0,priceInfo_hangqing_num,priceInfo_hangqing_num)
        cl.SetFilter('type_id',[217,216,220])
        res = cl.Query ('@(title,tags) '+keywords,'price')
        if res:
            if res.has_key('matches'):
                tagslista=res['matches']
                listall_baojia=[]
                for match in tagslista:
                    id=match['id']
                    attrs=match['attrs']
                    title=subString(attrs['ptitle'],35)
                    gmt_time=attrs['gmt_time']
                    #td_time=gmt_time.strftime('%Y-%m-%d')
                    list1={'title':title,'id':id,'gmt_time':gmt_time}
                    listall_baojia.append(list1)
                priceInfo_hangqing=listall_baojia
        """
        #所有报价行情
        #priceInfo_all_num=getnum_str(num_str,'priceInfo_all',30)
        #priceInfo_all=getpricelist_daohang(kname=keywords,limitcount=priceInfo_all_num)
        #市场动态
        #priceInfo_dongtai_num=getnum_str(num_str,'priceInfo_dongtai',25)
        #priceInfo_dongtai=getpricelist_daohang(kname=keywords+' 市场动态'.decode('utf-8'),limitcount=priceInfo_dongtai_num)
        #热门话题
        huzhuInfo=getbbslist_daohang(keywords,huzhuInfo_num)
        seolist=getseolist()
        cplist=getcplist(keywords,50)
    else:
        done="http://www2.zz91.com/specialsubject/"+pingyin+"/"
        return HttpResponseRedirect(done)
        #closeconn()
    #agent=request.META['HTTP_USER_AGENT']
    #agentflag=mobileuseragent(agent)
    #if agentflag:
    mobileflag=request.GET.get("mobileflag")
    if mobileflag:
        return render_to_response('mobile/mdetail.html',locals())
    return render_to_response('daohang/'+str(daohangtemplate)+'',locals())
        