#-*- coding:utf-8 -*-
import MySQLdb   
import settings
import codecs
from django.utils.http import urlquote
from django.shortcuts import render_to_response
from django.http import HttpResponse,HttpResponseRedirect
from django.core.paginator import Paginator,InvalidPage,EmptyPage,PageNotAnInteger
import time
import sys
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


nowpath=os.path.dirname(__file__)
execfile(nowpath+"/conn.py")
execfile(nowpath+"/commfunction.py")

#滚动供求信息
def guijinshupricelist(request):
    price_guijinshu=getpricelist_daohang(kname='贵金属'.decode('utf-8'),limitcount=15,titlelen=100)
    return render_to_response('guijinshuprice.html',locals())
    closeconn()
def guijinshupricelist1(request):
    price_guijinshu=getpricelist_daohang(kname='国际贵金属'.decode('utf-8'),limitcount=15,titlelen=100)
    return render_to_response('guijinshuprice.html',locals())
    closeconn()
#标签首页改版
def newdefault(request):
    categorylist1=getindexcategorylist('1000',1)
    categorylist2=getindexcategorylist('1001',1)
    categorylist3=getindexcategorylist('1002',1)
    categorylist4=getindexcategorylist('1003',1)
    categorylist5=getindexcategorylist('1004',1)
    categorylist6=getindexcategorylist('1005',1)
    categorylist7=getindexcategorylist('1006',1)
    categorylist8=getindexcategorylist('1007',0)
    categorylist9=getindexcategorylist('1008',1)
    categorylist10=getindexcategorylist('1009',1)
    offerlist1=getindexofferlist_pic("金属",None,5)
    offerlist2=getindexofferlist_pic("塑料",None,5)
    offerlist3=getindexofferlist_pic("废纺织品",None,5)
    offerlist4=getindexofferlist_pic("废橡胶",None,5)
    offerlist5=getindexofferlist_pic("废纸",None,5)
    offerlist6=getindexofferlist_pic("废电子电器",None,5)
    offerlist7=getindexofferlist_pic("废玻璃",None,5)
    offerlist8=getindexofferlist_pic("废旧二手设备",None,5)
    offerlist9=getindexofferlist_pic("其他废料",None,5)
    offerlist10=getindexofferlist_pic("清关|物流",None,5)
    
    complist=getcompanyindexcomplist(None,40)
    tagslist=newtagslist(None,80)
    pricelist=getpricelist(kname=None,num=30)
    tagsallcount=gettagsallcout()
    pinyinlist=englishlist()
    
    return render_to_response('tags/index.html',locals())
    closeconn()
#----------------------------------------photo
def photoindex(request):
    navlist=[{'t':'废金属','t_hex':''},{'t':'废塑料','t_hex':''},{'t':'废电子电器','t_hex':''},{'t':'废橡胶','t_hex':''},{'t':'废旧二手设备','t_hex':''},{'t':'废纸','t_hex':''}]
    for list in navlist:
        t=list['t']
        list['t_hex']=getjiami(t)

    return render_to_response('photo/index.html',locals())
    closeconn()

def photolist(request,keywords):
    navlist=[{'t':'废金属','t_hex':''},{'t':'废塑料','t_hex':''},{'t':'废电子电器','t_hex':''},{'t':'废橡胶','t_hex':''},{'t':'废旧二手设备','t_hex':''},{'t':'废纸','t_hex':''}]
    for list in navlist:
        t=list['t']
        list['t_hex']=getjiami(t)

    return render_to_response('photo/list.html',locals())
    closeconn()
    
def netindex(request):
    categorylist1=getindexcategorylist('1000',1)
    categorylist2=getindexcategorylist('1001',1)
    categorylist3=getindexcategorylist('1002',1)
    categorylist4=getindexcategorylist('1003',1)
    categorylist5=getindexcategorylist('1004',1)
    categorylist6=getindexcategorylist('1005',1)
    categorylist7=getindexcategorylist('1006',1)
    categorylist8=getindexcategorylist('1007',0)
    categorylist9=getindexcategorylist('1008',1)
    categorylist10=getindexcategorylist('1009',1)
    
    #priceInfo_gang=getpricelist_daohang(kname='钢'.decode('utf-8'),limitcount=6,titlelen=50)
    #priceInfo_tong=getpricelist_daohang(kname='铜'.decode('utf-8'),limitcount=6,titlelen=50)
    #priceInfo_tie=getpricelist_daohang(kname='铁'.decode('utf-8'),limitcount=6,titlelen=50)
    #priceInfo_ysjs=getpricelist_daohang(kname='有色金属'.decode('utf-8'),limitcount=10,titlelen=50)
    #priceInfo_gjs=getpricelist_daohang(kname='贵金属'.decode('utf-8'),limitcount=6,titlelen=50)
    
    
    #priceInfo_slkl=getpricelist_daohang(kname='颗粒'.decode('utf-8'),limitcount=6,titlelen=50)
    #priceInfo_slscjg=getpricelist_daohang(kname='塑料 市场价格'.decode('utf-8'),limitcount=6,titlelen=50)
    
    priceInfo_feisl=getpricelist_daohang(kname='塑料'.decode('utf-8'),limitcount=8,titlelen=50)
    priceInfo_feijs=getpricelist_daohang(kname='金属'.decode('utf-8'),limitcount=8,titlelen=50)
    priceInfo_feizhi=getpricelist_daohang(kname='纸'.decode('utf-8'),limitcount=6,titlelen=50)
    priceInfo_feixj=getpricelist_daohang(kname='橡胶'.decode('utf-8'),limitcount=6,titlelen=50)
    priceInfo_feidz=getpricelist_daohang(kname='电子'.decode('utf-8'),limitcount=6,titlelen=50)
    
    priceInfo_jixshebei=getpricelist_daohang(kname='机械 设备'.decode('utf-8'),limitcount=6,titlelen=50)
    offerlist_boli=offerlist(kname='玻璃'.decode('utf-8'),limitcount=3)
    offerlist_fangzhi=offerlist(kname='纺织'.decode('utf-8'),limitcount=6)
    offerlist_qit=offerlist(kname='玻璃 木料'.decode('utf-8'),limitcount=6)
    offerlist_fuwu=offerlist(kname='报关 通关 清关'.decode('utf-8'),limitcount=3)
    return render_to_response('zz91.net/index.html',locals())
    closeconn()
def default(request):
    host = request.META['HTTP_HOST']
    if (host=="www.zz91.net" or host=="zz91.net"):
        return netindex(request)
    if (host=="tags.zz91.com"):
        return newdefault(request)
    if (host=="daohang.zz91.com"):
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
        return render_to_response('daohang_index.html',locals())
    return render_to_response('daohang_index.html',locals())

   
def daohangdetail(request , pingyin):
    host = request.META['HTTP_HOST']
    if (host=="tags.zz91.com"):
        response = HttpResponse()
        response.write("<script>window.location='http://tags.zz91.com/index.htm'</script>")
        return response
    if (pingyin=="kuaijie"):
        offerSalesinfo=offerlist(kname='',pdt_type=0,limitcount=7)
        offerBuyinfo=offerlist(kname='',pdt_type=1,limitcount=7)
        return render_to_response('kuaijie/index.html',locals())
        return False;
        closeconn()
    sql="select label,templates,keywords,keywords1,num_str,keywords2,keywords3,sid,id from daohang where pingyin=%s"
    cursor.execute(sql,pingyin)
    daohanglist=cursor.fetchone()
    if (daohanglist):
        label=daohanglist[0]
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
            #huzhuInfo_num=getnum_str(num_str,'huzhuInfo',25)
        
        priceInfo_new=getpricelist_daohang(kname=keywords,limitcount=priceInfo_new_num,titlelen=100)
        number_price=len(priceInfo_new)
        if number_price<priceInfo_new_num:
            num_company=priceInfo_new_num-number_price
            pricelist_company=getpricelist_company(kname=keywords,num=num_company)
        else:
            num_company=priceInfo_new_num
        
        
        #最新互助信息
        huzhuInfo_new_num=getnum_str(num_str,'huzhuInfo_new',25)
        huzhuInfo_new=getbbslist_daohang(keywords,huzhuInfo_new_num)
        #标签
        tagsinfo_num=getnum_str(num_str,'tagsinfo',20)
        tagsinfo=gettagslist(keywords,tagsinfo_num)
        
        #        offerSalesinfo_num2=getnum_str(num_str,'offerSalesinfo',2)
        offerSalesinfo2=offerlist(kname=keywords,pdt_type="0",limitcount=2,havepic=1,fromlimit=0)
        newslist=getnewslist(keywords=keywords2,frompageCount=0,limitNum=newsinfo_num,typeid="",allnum=newsinfo_num,typeid2="",contentflag="")
        
#        offerSalesinfo_num=getnum_str(num_str,'offerSalesinfo',25)
        offerSalesinfo=offerlist(kname=keywords,pdt_type="0",limitcount=offerSalesinfo_num,fromlimit=2)
        
#        offerBuyinfo_num=getnum_str(num_str,'offerBuyinfo',25)
        daohangtype=getdaohangtype(pingyin)
        feijinshu=[6,7,8,9,10,11]
        feisuliao=[12,13,14]
        if daohangtype in feijinshu:
            code_type=1
        elif daohangtype in feisuliao:
            code_type=2
        else:
            code_type=''
        
        offerBuyinfo=offerlist(kname=keywords,pdt_type="1",limitcount=offerBuyinfo_num)
        #江浙沪报价
        priceInfo_jzf_num=getnum_str(num_str,'priceInfo_jzf',25)
        priceInfo_jzf=getpricelist_daohang(kname=keywords,assist_type_id=53,limitcount=priceInfo_jzf_num)
        #广东地区
        priceInfo_gd_num=getnum_str(num_str,'priceInfo_gd',25)
        priceInfo_gd=getpricelist_daohang(kname=keywords+' 广东'.decode('utf-8'),limitcount=priceInfo_gd_num)
        #清远地区
        priceInfo_qy_num=getnum_str(num_str,'priceInfo_qy',25)
        priceInfo_qy=getpricelist_daohang(kname=keywords,assist_type_id=59,limitcount=priceInfo_qy_num)
        #天津地区
        priceInfo_tj_num=getnum_str(num_str,'priceInfo_tj',25)
        priceInfo_tj=getpricelist_daohang(kname=keywords,assist_type_id=57,limitcount=priceInfo_tj_num)
        #南海
        priceInfo_nanhai_num=getnum_str(num_str,'priceInfo_nanhai',25)
        priceInfo_nanhai=getpricelist_daohang(kname=keywords,assist_type_id=54,limitcount=priceInfo_nanhai_num)
        #上海地区
        priceInfo_sh_num=getnum_str(num_str,'priceInfo_sh',25)
        priceInfo_sh=getpricelist_daohang(kname=keywords+' 上海'.decode('utf-8'),limitcount=priceInfo_sh_num)
        #华通地区
        priceInfo_ht_num=getnum_str(num_str,'priceInfo_ht',25)
        priceInfo_ht=getpricelist_daohang(kname=keywords+' 华通'.decode('utf-8'),limitcount=priceInfo_ht_num)
        #北京地区
        priceInfo_bj_num=getnum_str(num_str,'priceInfo_bj',25)
        priceInfo_bj=getpricelist_daohang(kname=keywords+' 北京'.decode('utf-8'),limitcount=priceInfo_bj_num)
        #全国各地地区
        priceInfo_qggd_num=getnum_str(num_str,'priceInfo_qggd',25)
        priceInfo_qggd=getpricelist_daohang(kname=keywords+' 全国各地'.decode('utf-8'),limitcount=priceInfo_qggd_num)
        #汩罗
        priceInfo_miluo_num=getnum_str(num_str,'priceInfo_miluo',25)
        priceInfo_miluo=getpricelist_daohang(kname=keywords+' 汩罗'.decode('utf-8'),limitcount=priceInfo_miluo_num)
        #长葛
        priceInfo_changge_num=getnum_str(num_str,'priceInfo_changge',25)
        priceInfo_changge=getpricelist_daohang(kname=keywords+' 长葛'.decode('utf-8'),limitcount=priceInfo_changge_num)
        #临沂
        priceInfo_lingx_num=getnum_str(num_str,'priceInfo_lingx',25)
        priceInfo_lingx=getpricelist_daohang(kname=keywords+' 临沂'.decode('utf-8'),limitcount=priceInfo_lingx_num)
        #天津山东
        priceInfo_tianshang_num=getnum_str(num_str,'priceInfo_tianshang',25)
        priceInfo_tianshang=getpricelist_daohang(kname=keywords+' 天津 山东'.decode('utf-8'),limitcount=priceInfo_tianshang_num)
        
        
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
        #所有报价行情
        priceInfo_all_num=getnum_str(num_str,'priceInfo_all',30)
        priceInfo_all=getpricelist_daohang(kname=keywords,limitcount=priceInfo_all_num)
        #市场动态
        priceInfo_dongtai_num=getnum_str(num_str,'priceInfo_dongtai',25)
        priceInfo_dongtai=getpricelist_daohang(kname=keywords+' 市场动态'.decode('utf-8'),limitcount=priceInfo_dongtai_num)
        #热门话题
        huzhuInfo=getbbslist_daohang(keywords,huzhuInfo_num)
        seolist=getseolist()
        cplist=getcplist()
        #closeconn()
    #return render_to_response('daohang/2014new/template.html',locals())
    return render_to_response('daohang/'+str(daohangtemplate)+'',locals())
