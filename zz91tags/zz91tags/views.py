#-*- coding:utf-8 -*-
import MySQLdb
import settings
import codecs,requests
from django.utils.http import urlquote
from django.shortcuts import render_to_response
from django.http import HttpResponse,HttpResponsePermanentRedirect,HttpResponseRedirect,HttpResponseNotFound
from django.core.paginator import Paginator,InvalidPage,EmptyPage,PageNotAnInteger
import time
import sys
import datetime
from datetime import timedelta, date 
import os
from django.core.cache import cache
import random
import shutil
try:
    import cPickle as pickle
except ImportError:
    import pickle

from math import ceil
from sphinxapi import *
from zz91page import *
from zz91settings import SPHINXCONFIG,limitpath
reload(sys) 
sys.setdefaultencoding('utf-8') 

nowpath=os.path.dirname(__file__)
execfile(nowpath+"/conn.py")
execfile(nowpath+"/commfunction.py")

#----标签首页改版
def default(request):
    mobileurl=getnowurl(request)
    categorylist=getindexcategorylist('',None)
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
    
    complist=getcompanyindexcomplist(None,20)
    tagslist=newtagslist(None,80)
    pricelist=getpricelist(kname="废",num=30)
    tagsallcount=gettagsallcout()
    pinyinlist=englishlist()
    #agent=request.META['HTTP_USER_AGENT']
    #agentflag=mobileuseragent(agent)
    #if agentflag:
    mobileflag=request.GET.get("mobileflag")
    if mobileflag:
        return render_to_response('mobile/index.html',locals())
    return render_to_response('tags/index.html',locals())
    closeconn()
def tagscategory(request,code):
    categorylist=getindexcategorylist(code,1)
    categoryname=getcategoryname(code)
    keywords_hex=getjiami(categoryname)
    return render_to_response('mobile/tagscategory.html',locals())
    closeconn()
def keywordsearch(request):
    #-------------智能搜索提示
    keywords = request.GET.get("keywords")
    
    serverid=SPHINXCONFIG['serverid']
    port=SPHINXCONFIG['port']
    
    cl = SphinxClient()
    cl.SetServer ( serverid, port )
    cl.SetMatchMode ( SPH_MATCH_ANY )
    #cl.SetSortMode( SPH_SORT_EXTENDED,"pdt_time_en desc" )
    cl.SetLimits (0,10,10)
    res = cl.Query ('@tname '+keywords,'tagslist')
    if res:
        if res.has_key('matches'):
            keylist=res['matches']
            listall_keywordsearch=[]
            for match in keylist:
                id=match['id']
                attrs=match['attrs']
                tags=attrs['tags']
                list1={'keyword':tags}
                listall_keywordsearch.append(list1)
            listall=listall_keywordsearch
    return render_to_response('keywordsearch.html',locals())
    closeconn()
#@cache_control(max_age=1800)
def tagssearchName(request , keywords):
    #keywords = request.GET.get("keywords")#搜索
    tagsexits=gettagsexists(keywords)
    if tagsexits:
        rightpricelistnav=getrightpricenav(tagsexits['tags_code'][0:4])
    else:
        return HttpResponseNotFound("<h1>Page not found</h1>")
    kname=keywords
    mingang=getmingganword(kname)
    if mingang:
        return HttpResponseNotFound(keywords+"<h1>FORBIDDEN4</h1>")
    tagschickNum(kname)
    keywords_hex=getjiami(kname)
    kname_bg=urlquote(keywords)
    tags_keywords=keywords.replace("+","")
    
    mobileflag=request.GET.get("mobileflag")
    if mobileflag:
        return HttpResponsePermanentRedirect("http://m.zz91.com/offerlist/?keywords="+tags_keywords)
    
    adkeywords=urlquote(kname.replace("+",""))
    nowurl="http://www.zz91.com"
    if (kname==None):
        return HttpResponseRedirect(nowurl)
    
    #listall_keycomp=newkeywordstop(kname_bg,2)
    #-----------供求信息
    listall=getofferlist(kname=kname)['list']
    listcount=getofferlist(kname=kname)['count']
    #-----------报价信息
    listall_baojia=getpricelist(kname=kname)['list']
    listcount_baojia=getpricelist(kname=kname)['count']
    #-----------资讯信息
    listall_news=getbbslist(kname=kname)['list']
    listcount_news=getbbslist(kname=kname)['count']
    
    listall_customerPrice=newcustmerprice(kname)
    listall_tags=newtagslist(kname,50)
    listall_forum=getbbslist(kname=kname)['list']
    
    return render_to_response('tags/tagsInfoList.html',locals())
    closeconn()
def tagssearchName_hex(request , keywords):
    if (gethextype(keywords)==False):
        kname=keywords.encode('utf8','ignore')
        keywords_hex=keywords.encode('utf8','ignore').encode("hex")
    else:
        kname=keywords.decode("hex")
        keywords_hex=keywords
    kname1=kname
    mingang=getmingganword(kname)
    if mingang:
        return HttpResponseNotFound(keywords+"<h1>FORBIDDEN4</h1>")

    kname=kname.replace("/"," ")
    mobileflag=request.GET.get("mobileflag")
    if mobileflag:
        return HttpResponsePermanentRedirect("http://m.zz91.com/offerlist/?keywords="+kname)
    tagsexits=gettagsexists(kname1)
    if tagsexits:
        rightpricelistnav=getrightpricenav(tagsexits['tags_code'][0:4])
    else:
        return HttpResponseNotFound("<h1>Page not found</h1>")
    tagschickNum(kname)
    tags_keywords=kname.replace("+","")
    adkeywords=urlquote(kname.replace("+",""))
    nowurl="http://www.zz91.com"
    if (kname==None):
        return HttpResponseRedirect(nowurl)
    
    #listall_keycomp=newkeywordstop(kname_bg,2)
    #-----------供求信息
    listall_offerlist=getofferlist(kname=kname)
    if (listall_offerlist):
        listall=listall_offerlist['list']
        listcount=listall_offerlist['count']
    #-----------报价信息
    listall_pricelist=getpricelist(kname=kname)
    if (listall_pricelist):
        listall_baojia=listall_pricelist['list']
        listcount_baojia=listall_pricelist['count']
    #-----------资讯信息
    listall_bbslist=getbbslist(kname=kname)
    if (listall_bbslist):
        listall_news=listall_bbslist['list']
        listcount_news=listall_bbslist['count']

    
    listall_customerPrice=newcustmerprice(kname)
    listall_tags=newtagslist(kname,50)

    return render_to_response('tags/tagsInfoList_hex.html',locals())
    closeconn()
def tagssearchList_hex(request , keywords , page):
    mobileurl=getnowurl(request)
    if (gethextype(keywords)==False):
        kname=keywords.encode('utf8','ignore')
        keywords_hex=keywords.encode('utf8','ignore').encode("hex")
    else:
        kname=keywords.decode("hex")
        keywords_hex=keywords
    kname_bg=keywords
    kname1=kname
    mingang=getmingganword(kname)
    if mingang:
        return HttpResponseNotFound(keywords+"<h1>FORBIDDEN4</h1>")

    kname=kname.replace("/"," ")
    mobileflag=request.GET.get("mobileflag")
    if mobileflag:
        return HttpResponsePermanentRedirect("http://m.zz91.com/offerlist/?keywords="+kname)
    tagsexits=gettagsexists(kname1)
    if tagsexits:
        rightpricelistnav=getrightpricenav(tagsexits['tags_code'][0:4])
    else:
        return HttpResponseNotFound("<h1>Page not found</h1>")
    tags_keywords=kname
    adkeywords=urlquote(kname.replace("+",""))
    nowurl="http://www.zz91.com"
    if (kname==None):
        return HttpResponseRedirect(nowurl)
    #listall_keycomp=newkeywordstop(kname,1)
    #-----------供求信息
    funpage = zz91page()
    limitNum=funpage.limitNum(50)
    nowpage=funpage.nowpage(int(page))
    frompageCount=funpage.frompageCount()
    after_range_num = funpage.after_range_num(2)
    before_range_num = funpage.before_range_num(9)
    
    serverid=SPHINXCONFIG['serverid']
    port=SPHINXCONFIG['port']
    
    cl = SphinxClient()
    cl.SetServer ( serverid, port )
    cl.SetMatchMode ( SPH_MATCH_BOOLEAN )
    cl.SetSortMode( SPH_SORT_EXTENDED,"refresh_time desc" )
    cl.SetLimits (frompageCount,limitNum,100000)
    listcount=0
    res = cl.Query ('@(title,label0,label1,label2,label3,label4,city,province,tags) '+kname,'offersearch_new,offersearch_new_vip')
    if res:
        if res.has_key('matches'):
            tagslist=res['matches']
            listall=[]
            for match in tagslist:
                pdtid=match['id']
                list1=getcompinfo(pdtid,cursor,kname)
                pdt_detail=list1['pdt_detail']
                pdt_detail=pdt_detail.replace('<br>','').replace('&nbsp;',' ')
                pdt_detail=subString(pdt_detail,50)+'...'
                
                list1['pdt_detail']=pdt_detail
                pdt_kind=list1['pdt_kind']
                kindclass=pdt_kind['kindclass']
                vipflag=list1['vipflag']
                vippic=vipflag['vippic']
                if (vippic==None):
                    list1['vipflag']['vipname']='普通会员'
                if (vippic=='http://img.zz91.com/zz91images/recycle.gif'):
                    list1['vipflag']['vipname']='再生通'
                if (vippic=='http://img.zz91.com/zz91images/pptSilver.gif'):
                    list1['vipflag']['vipname']='银牌品牌通'
                if (vippic=='http://img.zz91.com/zz91images/pptGold.gif'):
                    list1['vipflag']['vipname']='金牌品牌通'
                if (vippic=='http://img.zz91.com/zz91images/pptDiamond.gif'):
                    list1['vipflag']['vipname']='钻石品牌通'
                if (kindclass=='sell'):
                    list1['pdt_kind']['kindtxt']='供应'
                if (kindclass=='buy'):
                    list1['pdt_kind']['kindtxt']='求购'
                listall.append(list1)
        listcount=res['total_found']
    if (int(listcount)>100000):
        listcount=100000
    listcount = funpage.listcount(listcount)
    page_listcount=funpage.page_listcount()
    firstpage = funpage.firstpage()
    lastpage = funpage.lastpage()
    page_range  = funpage.page_range()
    nextpage = funpage.nextpage()
    prvpage = funpage.prvpage()
    
    listall_customerPrice=newcustmerprice(kname)
    listall_tags=newtagslist(kname,50)
    listall_bbslist=getbbslist(kname=kname)
    if (listall_bbslist):
        listall_forum=listall_bbslist['list']
    return render_to_response('tags/tagsSearchList_hex.html',locals())
    closeconn()
#@cache_control(max_age=1800)
def tagsInfoList(request , tags_id):
    showad=getshowadflag()
    kname=gettagsName(tags_id)
    
    mingang=getmingganword(kname)
    if mingang:
        return HttpResponseNotFound(keywords+"<h1>FORBIDDEN4</h1>")
    mobileflag=request.GET.get("mobileflag")
    if mobileflag:
        return HttpResponsePermanentRedirect("http://m.zz91.com/offerlist/?keywords="+kname)
    tagsexits=gettagsexists(kname)
    if tagsexits:
        rightpricelistnav=getrightpricenav(tagsexits['tags_code'][0:4])
    else:
        return HttpResponseNotFound("<h1>Page not found</h1>")
    tagschickNum(kname)
    
    #testkname=kname.encode("hex")
    kname=kname.replace("；","")
    kname=kname.replace("（","")
    kname=kname.replace("）","")
    kname=kname.replace("+"," ")
    kname=kname.replace("、"," ")
    kname=kname.replace("/"," ")
    
    
    keywords_hex=kname.encode("hex")
    kname_bg=kname
    adkeywords=urlquote(kname.replace("+",""))
    
    tags_keywords=urlquote(kname)
    #nowurl=request.META.get('HTTP_REFERER','/')
    nowurl="http://www.zz91.com"
    if (kname==None or kname=='None' or kname==''):
        return HttpResponseRedirect(nowurl)
    #listall_keycomp=newkeywordstop(kname_bg,2)
    #-----------供求信息
    if kname:
        listall=getofferlist(kname=str(kname))['list']
        listcount=getofferlist(kname=kname)['count']
        #-----------报价信息
        listall_baojia=getpricelist(kname=kname)['list']
        listcount_baojia=getpricelist(kname=kname)['count']
        #-----------资讯信息
        listall_news=getbbslist(kname=kname)['list']
        listcount_news=getbbslist(kname=kname)['count']
        
        listall_customerPrice=newcustmerprice(kname)
        listall_tags=newtagslist(kname,50)
        listall_forum=getbbslist(kname=kname)['list']
    return render_to_response('tags/tagsInfoList.html',locals())
    closeconn()
#@cache_control(max_age=1800)
def tagsInfoListMore(request , tags_id , page):
    #keywords = request.GET.get("keywords")#搜索
    kname=gettagsName(tags_id)
    mingang=getmingganword(kname)
    if mingang:
        return HttpResponseNotFound(keywords+"<h1>FORBIDDEN4</h1>")
    mobileflag=request.GET.get("mobileflag")
    if mobileflag:
        return HttpResponsePermanentRedirect("http://m.zz91.com/offerlist/?keywords="+kname)
    tagsexits=gettagsexists(kname)
    if tagsexits:
        rightpricelistnav=getrightpricenav(tagsexits['tags_code'][0:4])
    else:
        return HttpResponseNotFound("<h1>Page not found</h1>")
    kname_bg=kname
    keywords_hex=kname.encode("hex")
    tags_keywords=urlquote(kname)
    adkeywords=urlquote(kname.replace("+",""))
    
    nowurl="http://www.zz91.com"
    if (kname==None):
        return HttpResponseRedirect(nowurl)
    #listall_keycomp=newkeywordstop(kname_bg,2)
    #-----------供求信息
    funpage = zz91page()
    limitNum=funpage.limitNum(50)
    nowpage=funpage.nowpage(int(page))
    frompageCount=funpage.frompageCount()
    after_range_num = funpage.after_range_num(2)
    before_range_num = funpage.before_range_num(9)
    
    serverid=SPHINXCONFIG['serverid']
    port=SPHINXCONFIG['port']
    
    cl = SphinxClient()
    cl.SetServer ( serverid, port )
    cl.SetMatchMode ( SPH_MATCH_BOOLEAN )
    cl.SetSortMode( SPH_SORT_EXTENDED,"refresh_time desc" )
    
    cl.SetLimits (frompageCount,limitNum,100000)
    listcount=0
    res = cl.Query ('@(title,label0,label1,label2,label3,label4,city,province,tags) '+kname,'offersearch_new,offersearch_new_vip')
    if res:
        if res.has_key('matches'):
            tagslist=res['matches']
            listall=[]
            for match in tagslist:
                pdtid=match['id']
                list1=getcompinfo(pdtid,cursor,kname)
                pdt_detail=list1['pdt_detail']
                pdt_detail=pdt_detail.replace('<br>','').replace('&nbsp;',' ')
                pdt_detail=subString(pdt_detail,50)+'...'
                list1['pdt_detail']=pdt_detail
                pdt_kind=list1['pdt_kind']
                kindclass=pdt_kind['kindclass']
                vipflag=list1['vipflag']
                vippic=vipflag['vippic']
                if (vippic==None):
                    list1['vipflag']['vipname']='普通会员'
                if (vippic=='http://img.zz91.com/zz91images/recycle.gif'):
                    list1['vipflag']['vipname']='再生通'
                if (vippic=='http://img.zz91.com/zz91images/pptSilver.gif'):
                    list1['vipflag']['vipname']='银牌品牌通'
                if (vippic=='http://img.zz91.com/zz91images/pptGold.gif'):
                    list1['vipflag']['vipname']='金牌品牌通'
                if (vippic=='http://img.zz91.com/zz91images/pptDiamond.gif'):
                    list1['vipflag']['vipname']='钻石品牌通'
                if (kindclass=='sell'):
                    list1['pdt_kind']['kindtxt']='供应'
                if (kindclass=='buy'):
                    list1['pdt_kind']['kindtxt']='求购'
                listall.append(list1)
        listcount=res['total_found']
    if (int(listcount)>100000):
        listcount=100000
    listcount = funpage.listcount(listcount)
    page_listcount=funpage.page_listcount()
    firstpage = funpage.firstpage()
    lastpage = funpage.lastpage()
    page_range  = funpage.page_range()
    nextpage = funpage.nextpage()
    prvpage = funpage.prvpage()
    
    
    listall_customerPrice=newcustmerprice(kname)
    listall_tags=newtagslist(kname,50)
    listall_forum=getbbslist(kname=kname)['list']
    return render_to_response('tags/tagsSearchList.html',locals())
    closeconn()
#@cache_control(max_age=1800)
def tagspricelistMore(request , keywords , page):
    #keywords = request.GET.get("keywords")#搜索
    kname=keywords
    mingang=getmingganword(kname)
    if mingang:
        return HttpResponseNotFound(keywords+"<h1>FORBIDDEN4</h1>")
    kname_bg=urlquote(keywords)
    mobileflag=request.GET.get("mobileflag")
    if mobileflag:
        return HttpResponsePermanentRedirect("http://m.zz91.com/offerlist/?keywords="+kname)
        
    tagsexits=gettagsexists(kname)
    if tagsexits:
        rightpricelistnav=getrightpricenav(tagsexits['tags_code'][0:4])
    else:
        return HttpResponseNotFound("<h1>Page not found</h1>")
    keywords_hex=getjiami(kname)
    tags_keywords=keywords
    adkeywords=urlquote(kname.replace("+",""))
    nowurl="http://www.zz91.com"
    if (kname==None):
        return HttpResponseRedirect(nowurl)
    #listall_keycomp=newkeywordstop(kname_bg,2)
    #-----------报价信息
    funpage = zz91page()
    limitNum=funpage.limitNum(50)
    nowpage=funpage.nowpage(int(page))
    frompageCount=funpage.frompageCount()
    after_range_num = funpage.after_range_num(2)
    before_range_num = funpage.before_range_num(9)
    
    price=SPHINXCONFIG['name']['price']['name']
    serverid=SPHINXCONFIG['name']['price']['serverid']
    port=SPHINXCONFIG['name']['price']['port']
    
    cl = SphinxClient()
    cl.SetServer ( serverid, port )
    cl.SetMatchMode ( SPH_MATCH_BOOLEAN )
    cl.SetSortMode( SPH_SORT_EXTENDED,"gmt_order desc" )
    
    cl.SetLimits (frompageCount,limitNum,100000)
    listcount=0
    res = cl.Query ('@(title,tags) '+kname,price)
    if res:
        if res.has_key('matches'):
            tagslist=res['matches']
            listall=[]
            for match in tagslist:
                id=match['id']
                attrs=match['attrs']
                title=attrs['ptitle']
                gmt_time=attrs['gmt_time']
                list1={'title':title,'id':id,'gmt_time':gmt_time}
                listall.append(list1)
        listcount=res['total_found']
    if (int(listcount)>100000):
        listcount=100000
    listcount = funpage.listcount(listcount)
    page_listcount=funpage.page_listcount()
    firstpage = funpage.firstpage()
    lastpage = funpage.lastpage()
    page_range  = funpage.page_range()
    nextpage = funpage.nextpage()
    prvpage = funpage.prvpage()

    listall_customerPrice=newcustmerprice(kname)
    listall_tags=newtagslist(kname,50)
    listall_forum=getbbslist(kname=kname)['list']
    return render_to_response('tags/tagspriceList.html',locals())
    closeconn()
def tagspricelistMore_hex(request , keywords , page):
    #keywords = request.GET.get("keywords")#搜索
    navnum="2"
    kname=keywords.decode("hex")
    mingang=getmingganword(kname)
    if mingang:
        return HttpResponseNotFound(keywords+"<h1>FORBIDDEN4</h1>")
    mobileflag=request.GET.get("mobileflag")
    if mobileflag:
        return HttpResponsePermanentRedirect("http://m.zz91.com/offerlist/?keywords="+kname)
    adkeywords=urlquote(kname.replace("+",""))
    keywords_hex=keywords
    nowurl="http://www.zz91.com"
    kname1=kname
    kname=kname.replace("；","")
    kname=kname.replace("（","")
    kname=kname.replace("）","")
    kname=kname.replace("+"," ")
    kname=kname.replace("、"," ")
    kname=kname.replace("/"," ")
    tagsexits=gettagsexists(kname1)
    if tagsexits:
        rightpricelistnav=getrightpricenav(tagsexits['tags_code'][0:4])
    else:
        return HttpResponseNotFound("<h1>Page not found</h1>")
    if (kname==None):
        return HttpResponseRedirect(nowurl)
    #-----------报价信息
    funpage = zz91page()
    limitNum=funpage.limitNum(50)
    nowpage=funpage.nowpage(int(page))
    frompageCount=funpage.frompageCount()
    after_range_num = funpage.after_range_num(2)
    before_range_num = funpage.before_range_num(9)
    
    price=SPHINXCONFIG['name']['price']['name']
    serverid=SPHINXCONFIG['name']['price']['serverid']
    port=SPHINXCONFIG['name']['price']['port']
    
    cl = SphinxClient()
    cl.SetServer ( serverid, port )
    cl.SetMatchMode ( SPH_MATCH_BOOLEAN )
    cl.SetSortMode( SPH_SORT_EXTENDED,"gmt_order desc" )
    
    cl.SetLimits (frompageCount,limitNum,100000)
    listcount=0
    res = cl.Query ('@(title,tags) '+kname,price)
    if res:
        if res.has_key('matches'):
            tagslist=res['matches']
            listall=[]
            for match in tagslist:
                id=match['id']
                attrs=match['attrs']
                title=attrs['ptitle']
                gmt_time=attrs['gmt_time']
                list1={'title':title,'id':id,'gmt_time':gmt_time}
                listall.append(list1)
        listcount=res['total_found']
    if (int(listcount)>100000):
        listcount=100000
    listcount = funpage.listcount(listcount)
    page_listcount=funpage.page_listcount()
    firstpage = funpage.firstpage()
    lastpage = funpage.lastpage()
    page_range  = funpage.page_range()
    nextpage = funpage.nextpage()
    prvpage = funpage.prvpage()

    listall_customerPrice=newcustmerprice(kname)
    listall_tags=newtagslist(kname,50)
    listall_forum=getbbslist(kname=kname)['list']
    return render_to_response('tags/tagspriceList_hex.html',locals())
    closeconn()
#@cache_control(max_age=1800)
def tagsbbslistMore_hex(request , keywords , page):
    #keywords = request.GET.get("keywords")#搜索
    kname=keywords.decode("hex")
    mingang=getmingganword(kname)
    if mingang:
        return HttpResponseNotFound(keywords+"<h1>FORBIDDEN4</h1>")
    mobileflag=request.GET.get("mobileflag")
    if mobileflag:
        return HttpResponsePermanentRedirect("http://m.zz91.com/offerlist/?keywords="+kname)
        
    kname1=kname
    kname=kname.replace("；","")
    kname=kname.replace("（","")
    kname=kname.replace("）","")
    kname=kname.replace("+"," ")
    kname=kname.replace("、"," ")
    kname=kname.replace("/"," ")
    tagsexits=gettagsexists(kname1)
    if tagsexits:
        rightpricelistnav=getrightpricenav(tagsexits['tags_code'][0:4])
    else:
        return HttpResponseNotFound("<h1>Page not found</h1>")
    keywords_hex=keywords
    adkeywords=urlquote(kname.replace("+",""))
    nowurl="http://www.zz91.com"
    if (kname==None):
        return HttpResponseRedirect(nowurl)
    #listall_keycomp=newkeywordstop(kname_bg,2)
    #-----------资讯信息
    funpage = zz91page()
    limitNum=funpage.limitNum(50)
    nowpage=funpage.nowpage(int(page))
    frompageCount=funpage.frompageCount()
    after_range_num = funpage.after_range_num(2)
    before_range_num = funpage.before_range_num(9)
    
    serverid=SPHINXCONFIG['serverid']
    port=SPHINXCONFIG['port']
    
    cl = SphinxClient()
    cl.SetServer ( serverid, port )
    cl.SetMatchMode ( SPH_MATCH_BOOLEAN )
    cl.SetSortMode( SPH_SORT_EXTENDED,"post_time desc" )
    
    cl.SetLimits (frompageCount,limitNum,100000)
    listcount=0
    res = cl.Query ('@(title,tags) '+kname,'huzhu')
    if res:
        if res.has_key('matches'):
            tagslist=res['matches']
            listall=[]
            for match in tagslist:
                id=match['id']
                attrs=match['attrs']
                title=attrs['ptitle']
                ppost_time=attrs['ppost_time']
                list1={'title':title,'id':id,'gmt_time':ppost_time}
                listall.append(list1)
        listcount=res['total_found']
    if (int(listcount)>100000):
        listcount=100000
    listcount = funpage.listcount(listcount)
    page_listcount=funpage.page_listcount()
    firstpage = funpage.firstpage()
    lastpage = funpage.lastpage()
    page_range  = funpage.page_range()
    nextpage = funpage.nextpage()
    prvpage = funpage.prvpage()

    listall_customerPrice=newcustmerprice(kname)
    listall_tags=newtagslist(kname,50)
    listall_forum=getbbslist(kname=kname)['list']
    return render_to_response('tags/tagsbbsList_hex.html',locals())
    closeconn()
def tagsbbslistMore(request , keywords , page):
    #keywords = request.GET.get("keywords")#搜索
    kname=keywords
    kname1=kname
    mobileflag=request.GET.get("mobileflag")
    if mobileflag:
        return HttpResponsePermanentRedirect("http://m.zz91.com/offerlist/?keywords="+kname)
    mingang=getmingganword(kname)
    if mingang:
        return HttpResponseNotFound(keywords+"<h1>FORBIDDEN4</h1>")
    kname=kname.replace("；","")
    kname=kname.replace("（","")
    kname=kname.replace("）","")
    kname=kname.replace("+"," ")
    kname=kname.replace("、"," ")
    kname=kname.replace("/"," ")
    tagsexits=gettagsexists(kname1)
    if tagsexits:
        rightpricelistnav=getrightpricenav(tagsexits['tags_code'][0:4])
    else:
        return HttpResponseNotFound("<h1>Page not found</h1>")
    kname_bg=urlquote(keywords)
    keywords_hex=getjiami(kname)
    tags_keywords=keywords
    adkeywords=urlquote(kname.replace("+",""))
    nowurl="http://www.zz91.com"
    if (kname==None):
        return HttpResponseRedirect(nowurl)
    #listall_keycomp=newkeywordstop(kname_bg,2)
    #-----------资讯信息
    funpage = zz91page()
    limitNum=funpage.limitNum(50)
    nowpage=funpage.nowpage(int(page))
    frompageCount=funpage.frompageCount()
    after_range_num = funpage.after_range_num(2)
    before_range_num = funpage.before_range_num(9)
    
    serverid=SPHINXCONFIG['serverid']
    port=SPHINXCONFIG['port']
    
    cl = SphinxClient()
    cl.SetServer ( serverid, port )
    cl.SetMatchMode ( SPH_MATCH_BOOLEAN )
    cl.SetSortMode( SPH_SORT_EXTENDED,"post_time desc" )
    
    cl.SetLimits (frompageCount,limitNum,100000)
    listcount=0
    res = cl.Query ('@(title,tags) '+kname,'huzhu')
    if res:
        if res.has_key('matches'):
            tagslist=res['matches']
            listall=[]
            for match in tagslist:
                id=match['id']
                attrs=match['attrs']
                title=attrs['ptitle']
                ppost_time=attrs['ppost_time']
                list1={'title':title,'id':id,'gmt_time':ppost_time}
                listall.append(list1)
        listcount=res['total_found']
    if (int(listcount)>100000):
        listcount=100000
    listcount = funpage.listcount(listcount)
    page_listcount=funpage.page_listcount()
    firstpage = funpage.firstpage()
    lastpage = funpage.lastpage()
    page_range  = funpage.page_range()
    nextpage = funpage.nextpage()
    prvpage = funpage.prvpage()

    listall_customerPrice=newcustmerprice(kname)
    listall_tags=newtagslist(kname,50)
    listall_forum=getbbslist(kname=kname)['list']
    return render_to_response('tags/tagsbbsList.html',locals())
    closeconn()
#@cache_control(max_age=1800)    
def tagssearchList(request , keywords , page):
    #keywords = request.GET.get("keywords")#搜索
    kname=keywords
    kname1=kname
    mingang=getmingganword(kname)
    if mingang:
        return HttpResponseNotFound(keywords+"<h1>FORBIDDEN4</h1>")
    mobileflag=request.GET.get("mobileflag")
    if mobileflag:
        return HttpResponsePermanentRedirect("http://m.zz91.com/offerlist/?keywords="+kname)
    
    kname=kname.replace("；","")
    kname=kname.replace("（","")
    kname=kname.replace("）","")
    kname=kname.replace("+"," ")
    kname=kname.replace("、"," ")
    kname=kname.replace("/"," ")
    tagsexits=gettagsexists(kname1)
    if tagsexits:
        rightpricelistnav=getrightpricenav(tagsexits['tags_code'][0:4])
    else:
        return HttpResponseNotFound("<h1>Page not found</h1>")
    kname_bg=urlquote(keywords)
    keywords_hex=getjiami(kname)
    tags_keywords=keywords
    adkeywords=urlquote(kname.replace("+",""))
    nowurl="http://www.zz91.com"
    if (kname==None):
        return HttpResponseRedirect(nowurl)
    #listall_keycomp=newkeywordstop(kname,1)
    #-----------供求信息
    funpage = zz91page()
    limitNum=funpage.limitNum(50)
    nowpage=funpage.nowpage(int(page))
    frompageCount=funpage.frompageCount()
    after_range_num = funpage.after_range_num(2)
    before_range_num = funpage.before_range_num(9)
    
    serverid=SPHINXCONFIG['serverid']
    port=SPHINXCONFIG['port']
    listcount=0
    cl = SphinxClient()
    cl.SetServer ( serverid, port )
    cl.SetMatchMode ( SPH_MATCH_BOOLEAN )
    cl.SetSortMode( SPH_SORT_EXTENDED,"refresh_time desc" )
    cl.SetLimits (frompageCount,limitNum,100000)
    res = cl.Query ('@(title,label0,label1,label2,label3,label4,city,province,tags) '+kname,'offersearch_new,offersearch_new_vip')
    if res:
        if res.has_key('matches'):
            tagslist=res['matches']
            listall=[]
            for match in tagslist:
                pdtid=match['id']
                list1=getcompinfo(pdtid,cursor,kname)
                pdt_detail=list1['pdt_detail']
                pdt_detail=pdt_detail.replace('<br>','').replace('&nbsp;',' ')
                pdt_detail=subString(pdt_detail,50)+'...'
                list1['pdt_detail']=pdt_detail
                pdt_kind=list1['pdt_kind']
                kindclass=pdt_kind['kindclass']
                vipflag=list1['vipflag']
                vippic=vipflag['vippic']
                if (vippic==None):
                    list1['vipflag']['vipname']='普通会员'
                if (vippic=='http://img.zz91.com/zz91images/recycle.gif'):
                    list1['vipflag']['vipname']='再生通'
                if (vippic=='http://img.zz91.com/zz91images/pptSilver.gif'):
                    list1['vipflag']['vipname']='银牌品牌通'
                if (vippic=='http://img.zz91.com/zz91images/pptGold.gif'):
                    list1['vipflag']['vipname']='金牌品牌通'
                if (vippic=='http://img.zz91.com/zz91images/pptDiamond.gif'):
                    list1['vipflag']['vipname']='钻石品牌通'
                if (kindclass=='sell'):
                    list1['pdt_kind']['kindtxt']='供应'
                if (kindclass=='buy'):
                    list1['pdt_kind']['kindtxt']='求购'
                listall.append(list1)
        listcount=res['total_found']
    if (int(listcount)>100000):
        listcount=100000
    listcount = funpage.listcount(listcount)
    page_listcount=funpage.page_listcount()
    firstpage = funpage.firstpage()
    lastpage = funpage.lastpage()
    page_range  = funpage.page_range()
    nextpage = funpage.nextpage()
    prvpage = funpage.prvpage()
    
    listall_customerPrice=newcustmerprice(kname)
    listall_tags=newtagslist(kname,50)
    listall_forum=getbbslist(kname=kname)['list']
    return render_to_response('tags/tagsSearchList.html',locals())
    closeconn()
    




#新版2013-1-21
def tagsmain(request,keywords):
    mobileurl=getnowurl(request)
    navnum="1"
    showad=getshowadflag()
    if (gethextype(keywords)==False):
        kname=keywords.encode('utf8','ignore').strip()
        keywords_hex=keywords.encode('utf8','ignore').encode("hex")
    else:
        kname=keywords.decode("hex").strip()
        keywords_hex=keywords
    mingang=getmingganword(kname)
    if mingang:
        return HttpResponseNotFound(keywords+"<h1>FORBIDDEN4</h1>")
    kname=kname.upper()
    kname1=kname
    kname=kname.replace("；","")
    kname=kname.replace("（","")
    kname=kname.replace("）","")
    kname=kname.replace("+"," ")
    kname=kname.replace("、"," ")
    kname=kname.replace("/"," ")

    tagsexits=gettagsexists(kname1)
    if tagsexits:
        rightpricelistnav=getrightpricenav(tagsexits['tags_code'][0:4])
    else:
        return HttpResponseNotFound("<h1>Page not found</h1>")
    tags_keywords=kname.replace("+","")
    adkeywords=urlquote(kname.replace("+",""))
    nowurl="http://www.zz91.com"
    
    listall_tags=newtagslist(kname,100)
    
    
    
    if (kname==None):
        return HttpResponseRedirect(nowurl)
    #seo 客户链接
    #seolist=getseolist()
    cplist=getcplist(kname,50)
    tagschickNum(kname)
    #广告
    #adlist=getadlist(373,kname)
    kname1=kname.replace("价格","")
    kname1=kname1.replace("行情","")
    #-----------供应信息
    listcount0=0
    listall_offerlist=getofferlist(kname=kname1,ckind='0',num=15)
    if (listall_offerlist):
        listall=listall_offerlist['list']
        listcount0=listall_offerlist['count']
    #-----------求购信息
    listcount1=0
    try:
        listall_offerlist1=getofferlist(kname=kname1,ckind='1',num=15)
        #listall_offerlist1=None
        if (listall_offerlist1):
            listall1=listall_offerlist1['list']
            listcount1=listall_offerlist1['count']
        listcount=listcount0+listcount1
    except:
        
        listall_offerlist1 =None
    #-----------报价信息
    listcount_baojia_all=0
    listall_pricelist=getpricelist(kname=kname1,num=10)
    if (listall_pricelist):
        listall_baojia=listall_pricelist['list']
        listcount_baojia=listall_pricelist['count']
        havelist_price=listall_pricelist['havelist']
        listcount_baojia_all=listcount_baojia_all+listcount_baojia
    #----企业报价
    listall_pricelist_company=getpricelist_company(kname=kname1,num=10)
    if (listall_pricelist_company):
        listall_baojia_company=listall_pricelist_company['list']
        listcount_baojia_company=listall_pricelist_company['count']
        listcount_baojia_all=listcount_baojia_all+listcount_baojia_company
    
    #-----------互助信息
    listall_bbslist=getbbslist(kname=kname1,num=20)
    if (listall_bbslist):
        listall_huzhu=listall_bbslist['list']
        listcount_huzhu=listall_bbslist['count']
        havelist_bbs=listall_bbslist['havelist']
    #-----------互助信息
    listall_newslist=getnewslist(keywords=kname1,frompageCount=0,limitNum=20,allnum=20)
    if (listall_bbslist):
        listall_news=listall_newslist['list']
        listcount_news=listall_newslist['count']

    
    #agent=request.META['HTTP_USER_AGENT']
    #agentflag=mobileuseragent(agent)
    #if agentflag:
    mobileflag=request.GET.get("mobileflag")
    if mobileflag:
        return render_to_response('mobile/tagsmain.html',locals())

    return render_to_response('tags/mainlist.html',locals())
    closeconn()

#标签列表
def tagsTradeList(request, kind="", keywords="", page=""):
    showad=getshowadflag()
    mobileurl=getnowurl(request)
    if (gethextype(keywords)==False):
        kname=keywords.encode('utf8','ignore')
        keywords_hex=keywords.encode('utf8','ignore').encode("hex")
    else:
        kname=keywords.decode("hex")
        keywords_hex=keywords
    kname=kname.upper()
    mingang=getmingganword(kname)
    if mingang:
        return HttpResponseNotFound(keywords+"<h1>FORBIDDEN4</h1>")
        
    kname2=kname
    kname=kname.replace("；","")
    kname=kname.replace("（","")
    kname=kname.replace("）","")
    kname=kname.replace("+"," ")
    kname=kname.replace("、"," ")
    kname=kname.replace("/"," ")
    kname1=kname.replace("价格","")
    kname1=kname1.replace("行情","")
    tagsexits=gettagsexists(kname2)
    if tagsexits:
        rightpricelistnav=getrightpricenav(tagsexits['tags_code'][0:4])
    else:
        return HttpResponseNotFound("<h1>Page not found</h1>")
    tags_keywords=kname.replace("+","")
    adkeywords=urlquote(kname.replace("+",""))
    #广告
    
    listall_tags=newtagslist(kname,50)
    nowurl="http://www.zz91.com"
    if (kname==None):
        return HttpResponseRedirect(nowurl)
    adlist=getadlist(373,kname)
    #-----------供求信息
    funpage = zz91page()
    limitNum=funpage.limitNum(50)
    nowpage=funpage.nowpage(int(page))
    frompageCount=funpage.frompageCount()
    after_range_num = funpage.after_range_num(2)
    before_range_num = funpage.before_range_num(9)
    

    serverid=SPHINXCONFIG['serverid']
    port=SPHINXCONFIG['port']
    
    cl = SphinxClient()
    cl.SetServer ( serverid, port )
    cl.SetMatchMode ( SPH_MATCH_BOOLEAN )
    cl.SetFilter('check_status',[1])
    if kind:
        cl.SetFilter('pdt_kind',[int(kind)])
    kindclass1=""
    kindclass2=""
    navnum="3"
    kindtext="供求信息"
    seo_t=""+kname+"_第"+str(page)+"页"
    seo_d=""+kname+"标签频道为你提供最新最全的"+kname+"供应信息,"+kname+"出售信息，让你及时掌握最新"+kname+"价格行情资讯，让你生意翻倍。"
    seo_k=""+kname
    if (kind=='0'):
        kindclass1="on"
        kindclass2=""
        navnum="3"
        kindtext="供求信息"
        seo_t="供应"+kname+"_"+kname+"出售_第"+str(page)+"页"
        seo_d="供应"+kname+"标签频道为你提供最新最全的"+kname+"供应信息,"+kname+"出售信息，让你及时掌握最新"+kname+"价格行情资讯，让你生意翻倍。"
        seo_k="供应"+kname
    if (kind=='1'):
        kindclass1=""
        navnum="3"
        kindclass2="on"
        kindtext="求购信息"
        seo_t="求购"+kname+"_"+kname+"回收_第"+str(page)+"页"
        seo_d="求购"+kname+"标签频道为你提供最新最全的"+kname+"求购信息,"+kname+"回收信息，让你及时掌握最新"+kname+"价格行情资讯，让你生意翻倍。"
        seo_k="求购"+kname+", "+kname+"回收"
    if not kind:
        kind=None
        
    cl.SetSortMode( SPH_SORT_EXTENDED,"refresh_time desc" )
    cl.SetLimits (frompageCount,limitNum,100000)
    listcount=0
    res = cl.Query ('@(title,label0,label1,label2,label3,label4,city,province,tags) '+kname1,'offersearch_new,offersearch_new_vip')
    if res:
        if res.has_key('matches'):
            tagslist=res['matches']
            listall=[]
            for match in tagslist:
                pdtid=match['id']
                list1=getcompinfo(pdtid,cursor,kname)
                pdt_name=list1['pdt_name']
            
                list1['fulltitle']=list1["pdt_kind"]["kindtxt"]+pdt_name
                
                #pdt_name=getlightkeywords(cl,[pdt_name],kname,"offersearch_new")
                
                list1['pdt_name']=pdt_name
                
                listall.append(list1)
        listcount=res['total_found']
    if (int(listcount)>100000):
        listcount=100000
    listcount = funpage.listcount(listcount)
    page_listcount=funpage.page_listcount()
    firstpage = funpage.firstpage()
    lastpage = funpage.lastpage()
    page_range  = funpage.page_range()
    nextpage = funpage.nextpage()
    prvpage = funpage.prvpage()
    #agent=request.META['HTTP_USER_AGENT']
    #agentflag=mobileuseragent(agent)
    #if agentflag:
    mobileflag=request.GET.get("mobileflag")
    if mobileflag:
        return render_to_response('mobile/tags_trade.html',locals())
    
    return render_to_response('tags/tradelist.html',locals())
    closeconn()
def tagsPriceList(request, keywords, page):
    mobileurl=getnowurl(request)
    navnum="2"
    showad=getshowadflag()
    if (gethextype(keywords)==False):
        kname=keywords.encode('utf8','ignore')
        keywords_hex=keywords.encode('utf8','ignore').encode("hex")
    else:
        kname=keywords.decode("hex")
        keywords_hex=keywords
    kname=kname.upper()
    mingang=getmingganword(kname)
    if mingang:
        return HttpResponseNotFound(keywords+"<h1>FORBIDDEN4</h1>")
        
    kname1=kname
    kname=kname.replace("；","")
    kname=kname.replace("（","")
    kname=kname.replace("）","")
    kname=kname.replace("+"," ")
    kname=kname.replace("、"," ")
    kname=kname.replace("/"," ")
    kname1=kname.replace("今日","")
    kname1=kname1.replace("价格","")
    kname1=kname1.replace("行情","")
    tagsexits=gettagsexists(kname1)
    if tagsexits:
        rightpricelistnav=getrightpricenav(tagsexits['tags_code'][0:4])
    else:
        return HttpResponseNotFound("<h1>Page not found</h1>")
    tags_keywords=kname
    adkeywords=urlquote(kname.replace("+",""))
    #广告
    adlist=getadlist(373,kname)
    nowurl="http://www.zz91.com"
    if (kname==None):
        return HttpResponseRedirect(nowurl)
    
    #----企业报价
    listall_pricelist_company=getpricelist_company(kname=kname1,num=10)
    if (listall_pricelist_company):
        listall_baojia_company=listall_pricelist_company['list']
        listcount_baojia_company=listall_pricelist_company['count']
        
    #-----------报价信息
    funpage = zz91page()
    limitNum=funpage.limitNum(80)
    nowpage=funpage.nowpage(int(page))
    frompageCount=funpage.frompageCount()
    after_range_num = funpage.after_range_num(2)
    before_range_num = funpage.before_range_num(9)
    
    price=SPHINXCONFIG['name']['price']['name']
    serverid=SPHINXCONFIG['name']['price']['serverid']
    port=SPHINXCONFIG['name']['price']['port']
    
    cl = SphinxClient()
    cl.SetServer ( serverid, port )
    cl.SetMatchMode ( SPH_MATCH_BOOLEAN )
    cl.SetSortMode( SPH_SORT_EXTENDED,"gmt_order desc" )
    
    cl.SetLimits (frompageCount,limitNum,100000)

    res = cl.Query ('@(title,tags) '+kname1,price)
    listcount=0
    if res:
        if res.has_key('matches'):
            tagslist=res['matches']
            listall=[]
            for match in tagslist:
                id=match['id']
                attrs=match['attrs']
                title=attrs['ptitle']
                gmt_time=attrs['gmt_time']
                list1={'title':title,'id':id,'gmt_time':gmt_time}
                listall.append(list1)
        listcount=res['total_found']
    if (int(listcount)>100000):
        listcount=100000
    listcount = funpage.listcount(listcount)
    page_listcount=funpage.page_listcount()
    firstpage = funpage.firstpage()
    lastpage = funpage.lastpage()
    page_range  = funpage.page_range()
    nextpage = funpage.nextpage()
    prvpage = funpage.prvpage()

    listall_tags=newtagslist(kname,50)
    #agent=request.META['HTTP_USER_AGENT']
    #agentflag=mobileuseragent(agent)
    #if agentflag:
    mobileflag=request.GET.get("mobileflag")
    if mobileflag:
        return render_to_response('mobile/tags_price.html',locals())
    return render_to_response('tags/pricelist.html',locals())
    closeconn()
def tagsPriceCompanyList(request, keywords, page):
    mobileurl=getnowurl(request)
    navnum="2"
    if (gethextype(keywords)==False):
        kname=keywords.encode('utf8','ignore')
        keywords_hex=keywords.encode('utf8','ignore').encode("hex")
    else:
        kname=keywords.decode("hex")
        keywords_hex=keywords
    kname=kname.upper()
    mingang=getmingganword(kname)
    if mingang:
        return HttpResponseNotFound(keywords+"<h1>FORBIDDEN4</h1>")
        
    kname2=kname
    kname=kname.replace("；","")
    kname=kname.replace("（","")
    kname=kname.replace("）","")
    kname=kname.replace("+"," ")
    kname=kname.replace("、"," ")
    kname=kname.replace("/"," ")
    kname1=kname.replace("今日","")
    kname1=kname1.replace("价格","")
    kname1=kname1.replace("行情","")
    tags_keywords=kname
    tagsexits=gettagsexists(kname2)
    if tagsexits:
        rightpricelistnav=getrightpricenav(tagsexits['tags_code'][0:4])
    else:
        return HttpResponseNotFound("<h1>Page not found</h1>")
    adkeywords=urlquote(kname.replace("+",""))
    nowurl="http://www.zz91.com"
    #广告
    adlist=getadlist(373,kname)
    if (kname==None):
        return HttpResponseRedirect(nowurl)
    #-----------报价信息
    funpage = zz91page()
    limitNum=funpage.limitNum(80)
    nowpage=funpage.nowpage(int(page))
    frompageCount=funpage.frompageCount()
    after_range_num = funpage.after_range_num(2)
    before_range_num = funpage.before_range_num(9)
    
    company_price=SPHINXCONFIG['name']['company_price']['name']
    serverid=SPHINXCONFIG['name']['company_price']['serverid']
    port=SPHINXCONFIG['name']['company_price']['port']
    
    cl = SphinxClient()
    cl.SetServer ( serverid, port )
    cl.SetMatchMode ( SPH_MATCH_ANY )
    cl.SetSortMode( SPH_SORT_EXTENDED,"post_time desc" )
    
    cl.SetLimits (frompageCount,limitNum,100000)
    listcount=0
    res = cl.Query ('@(title,label1,label2,label3,area1,area2,area3) '+kname1,company_price)
    if res:
        if res.has_key('matches'):
            tagslist=res['matches']
            listall=[]
            for match in tagslist:
                id=match['id']
                
                
                attrs=match['attrs']
                title=attrs['ptitle']
                company_id=attrs["company_id"]
                companyvalue=getcompanyname(company_id)
                if companyvalue:
                    companyname=companyvalue['name']
                    domain_zz91=companyvalue['domain_zz91']
                else:
                    companyname=""
                    domain_zz91=""
                if domain_zz91=="" or domain_zz91==None:
                    companyurl="http://company.zz91.com/compinfo"+str(company_id)+".htm"
                else:
                    companyurl="http://"+domain_zz91+".zz91.com"
                gmt_time=attrs['ppost_time']
                price=attrs['price']
                price_unit=attrs['price_unit']
                min_price=attrs['min_price']
                max_price=attrs['max_price']
                #if (price=="" or price=="none"):
                price=min_price+"-"+max_price+price_unit
                list1={'title':title,'id':id,'gmt_time':gmt_time,'price':price,'companyname':companyname,'companyurl':companyurl}
                listall.append(list1)
        listcount=res['total_found']
    if (int(listcount)>100000):
        listcount=100000
    listcount = funpage.listcount(listcount)
    page_listcount=funpage.page_listcount()
    firstpage = funpage.firstpage()
    lastpage = funpage.lastpage()
    page_range  = funpage.page_range()
    nextpage = funpage.nextpage()
    prvpage = funpage.prvpage()

    listall_tags=newtagslist(kname,50)
    #agent=request.META['HTTP_USER_AGENT']
    #agentflag=mobileuseragent(agent)
    #if agentflag:
    mobileflag=request.GET.get("mobileflag")
    if mobileflag:
        return render_to_response('mobile/tags_price_company.html',locals())
    return render_to_response('tags/pricecompanylist.html',locals())
    closeconn()
def tagsnewsList(request, keywords, page):
    mobileurl=getnowurl(request)
    navnum="6"
    if (gethextype(keywords)==False):
        kname=keywords.encode('utf8','ignore')
        keywords_hex=keywords.encode('utf8','ignore').encode("hex")
    else:
        kname=keywords.decode("hex")
        keywords_hex=keywords
    kname=kname.upper()
    mingang=getmingganword(kname)
    if mingang:
        return HttpResponseNotFound(keywords+"<h1>FORBIDDEN4</h1>")
        
    tags_keywords=kname
    kname1=kname
    kname=kname.replace("；","")
    kname=kname.replace("（","")
    kname=kname.replace("）","")
    kname=kname.replace("+"," ")
    kname=kname.replace("、"," ")
    kname=kname.replace("/"," ")
    tagsexits=gettagsexists(kname1)
    if tagsexits:
        rightpricelistnav=getrightpricenav(tagsexits['tags_code'][0:4])
    else:
        return HttpResponseNotFound("<h1>Page not found</h1>")
    adkeywords=urlquote(kname.replace("+",""))
    #广告
    adlist=getadlist(373,kname)
    nowurl="http://www.zz91.com"
    if (kname==None):
        return HttpResponseRedirect(nowurl)
    #-----------报价信息
    funpage = zz91page()
    limitNum=funpage.limitNum(80)
    nowpage=funpage.nowpage(int(page))
    frompageCount=funpage.frompageCount()
    after_range_num = funpage.after_range_num(2)
    before_range_num = funpage.before_range_num(9)
    
    newslist=getnewslist(keywords=kname,frompageCount=frompageCount,limitNum=limitNum)
    
    listall=newslist['list']
    listcount = funpage.listcount(newslist['count'])
    page_listcount=funpage.page_listcount()
    firstpage = funpage.firstpage()
    lastpage = funpage.lastpage()
    page_range  = funpage.page_range()
    nextpage = funpage.nextpage()
    prvpage = funpage.prvpage()

    listall_tags=newtagslist(kname,50)
    #agent=request.META['HTTP_USER_AGENT']
    #agentflag=mobileuseragent(agent)
    #if agentflag:
    mobileflag=request.GET.get("mobileflag")
    if mobileflag:
        return render_to_response('mobile/tags_news.html',locals())
    return render_to_response('tags/newslist.html',locals())    
def tagsHuzhuList(request, keywords, page):
    mobileurl=getnowurl(request)
    navnum="7"
    if (gethextype(keywords)==False):
        kname=keywords.encode('utf8','ignore')
        keywords_hex=keywords.encode('utf8','ignore').encode("hex")
    else:
        kname=keywords.decode("hex")
        keywords_hex=keywords
    kname=kname.upper()
    mingang=getmingganword(kname)
    if mingang:
        return HttpResponseNotFound(keywords+"<h1>FORBIDDEN4</h1>")
        
    tags_keywords=kname
    kname1=kname
    kname=kname.replace("；","")
    kname=kname.replace("（","")
    kname=kname.replace("）","")
    kname=kname.replace("+"," ")
    kname=kname.replace("、"," ")
    kname=kname.replace("/"," ")
    tagsexits=gettagsexists(kname1)
    if tagsexits:
        rightpricelistnav=getrightpricenav(tagsexits['tags_code'][0:4])
    else:
        return HttpResponseNotFound("<h1>Page not found</h1>")
    adkeywords=urlquote(kname.replace("+",""))
    #广告
    adlist=getadlist(373,kname)
    nowurl="http://www.zz91.com"
    if (kname==None):
        return HttpResponseRedirect(nowurl)
    #-----------报价信息
    funpage = zz91page()
    limitNum=funpage.limitNum(80)
    nowpage=funpage.nowpage(int(page))
    frompageCount=funpage.frompageCount()
    after_range_num = funpage.after_range_num(2)
    before_range_num = funpage.before_range_num(9)
    

    serverid=SPHINXCONFIG['serverid']
    port=SPHINXCONFIG['port']

    cl = SphinxClient()
    cl.SetServer ( serverid, port )
    cl.SetMatchMode ( SPH_MATCH_ANY )
    cl.SetSortMode( SPH_SORT_EXTENDED,"@weight DESC,post_time desc" )
    
    cl.SetLimits (frompageCount,limitNum,100000)
    listcount=0
    res = cl.Query ('@(title,tags) '+kname,'huzhu')
    if res:
        if res.has_key('matches'):
            tagslist=res['matches']
            listall=[]
            for match in tagslist:
                id=match['id']
                attrs=match['attrs']
                title=attrs['ptitle']
                gmt_time=attrs['ppost_time']
                pid=attrs['pid']
                #return HttpResponse(id)
                if id:
                    try:
                        sql="select content,account,company_id,reply_time from bbs_post where id="+str(pid)
                        #return HttpResponse(sql)
                        cursor.execute(sql)
                        alist = cursor.fetchone()
                        if alist:
                            havepic=havepicflag(alist[0])
                            content=subString(filter_tags(alist[0]),50)
                            username=getusername(alist[2])
                            reply_time=formattime(alist[3],0)
                        else:
                            content=""
                            havepic=0
                            username=""
                            reply_time=''
                    except Exception, e:
                        content=""
                        havepic=0
                        username=""
                        reply_time=''
                    
                    list1={'title':title,'id':id,'gmt_time':gmt_time,'content':content,'havepic':havepic,'username':username,'reply_time':reply_time}
                    listall.append(list1)
        listcount=res['total_found']
    if (int(listcount)>100000):
        listcount=100000
    listcount = funpage.listcount(listcount)
    page_listcount=funpage.page_listcount()
    firstpage = funpage.firstpage()
    lastpage = funpage.lastpage()
    page_range  = funpage.page_range()
    nextpage = funpage.nextpage()
    prvpage = funpage.prvpage()

    listall_tags=newtagslist(kname,50)
    listall_tags=newtagslist(kname,50)
    #agent=request.META['HTTP_USER_AGENT']
    #agentflag=mobileuseragent(agent)
    #if agentflag:
    mobileflag=request.GET.get("mobileflag")
    if mobileflag:
        return render_to_response('mobile/tags_huzhu.html',locals())
    return render_to_response('tags/bbslist.html',locals())
def tagscompanyList(request , keywords , page):
    navnum="4"
    if (gethextype(keywords)==False):
        kname=keywords.encode('utf8','ignore')
        keywords_hex=keywords.encode('utf8','ignore').encode("hex")
    else:
        kname=keywords.decode("hex")
        keywords_hex=keywords
    if keywords_hex=="e68a80e69cafe8aebee5a487e8bdace8aea9":
        return HttpResponseNotFound("<h1>Page not found</h1>")
    mobileflag=request.GET.get("mobileflag")
    if mobileflag:
        return HttpResponsePermanentRedirect("http://m.zz91.com/offerlist/?keywords="+kname)
    kname1=kname
    kname=kname.upper()
    mingang=getmingganword(kname)
    if mingang:
        return HttpResponseNotFound(keywords+"<h1>FORBIDDEN4</h1>")
    tagsexits=gettagsexists(kname1)
    if tagsexits:
        rightpricelistnav=getrightpricenav(tagsexits['tags_code'][0:4])
    else:
        return HttpResponseNotFound("<h1>Page not found</h1>")
        
    tags_keywords=kname
    kname1=kname
    kname=kname.replace("；","")
    kname=kname.replace("（","")
    kname=kname.replace("）","")
    kname=kname.replace("+"," ")
    kname=kname.replace("、"," ")
    kname=kname.replace("/"," ")
    adkeywords=urlquote(kname.replace("+",""))
    nowurl="http://www.zz91.com"
    if (kname==None):
        return HttpResponseRedirect(nowurl)
    #-----------供求信息
    funpage = zz91page()
    limitNum=funpage.limitNum(50)
    nowpage=funpage.nowpage(int(page))
    frompageCount=funpage.frompageCount()
    after_range_num = funpage.after_range_num(2)
    before_range_num = funpage.before_range_num(9)
    
    companylist=getcompanylist(kname,frompageCount,limitNum,100000)
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

    listall_tags=newtagslist(kname,50)
    listall_forum=getbbslist(kname=kname)['list']
    return render_to_response('tags/companylist.html',locals())
    closeconn()
def searckkeyword_hex(request):
    keywords=request.GET.get("tagName")
    keywords=getjiami(keywords)
    mingang=getmingganword(kname)
    if mingang:
        return HttpResponseNotFound(keywords+"<h1>FORBIDDEN4</h1>")
    nowurl="/s/"+keywords+"/"
    #return render_to_response('tags/search.htm',locals())
    return HttpResponseRedirect(nowurl)

