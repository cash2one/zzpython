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
reload(sys) 
sys.setdefaultencoding('utf-8') 

nowpath=os.path.dirname(__file__)
execfile(nowpath+"/conn.py")
execfile(nowpath+"/commfunction.py")

def keywordsearch(request):
    #-------------智能搜索提示
    keywords = request.GET.get("keywords")
    port = settings.SPHINXCONFIG['port']
    cl = SphinxClient()
    cl.SetServer ( settings.SPHINXCONFIG['serverid'], port )
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
    kname=keywords
    tagschickNum(kname)
    keywords_hex=getjiami(kname)
    kname_bg=urlquote(keywords)
    tags_keywords=keywords.replace("+","")
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
    if (gethextype(keywords)==False):
        kname=keywords.encode('utf8','ignore')
        keywords_hex=keywords.encode('utf8','ignore').encode("hex")
    else:
        kname=keywords.decode("hex")
        keywords_hex=keywords
    kname_bg=keywords
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
    
    port = settings.SPHINXCONFIG['port']
    cl = SphinxClient()
    cl.SetServer ( settings.SPHINXCONFIG['serverid'], port )
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
                list1=getcompinfo(pdtid,cursor_my,kname)
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
    
    port = settings.SPHINXCONFIG['port']
    cl = SphinxClient()
    cl.SetServer ( settings.SPHINXCONFIG['serverid'], port )
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
                list1=getcompinfo(pdtid,cursor_my,kname)
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
    kname_bg=urlquote(keywords)
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
    
    port = settings.SPHINXCONFIG['port']
    cl = SphinxClient()
    cl.SetServer ( settings.SPHINXCONFIG['serverid'], port )
    cl.SetMatchMode ( SPH_MATCH_BOOLEAN )
    cl.SetSortMode( SPH_SORT_EXTENDED,"gmt_order desc" )
    
    cl.SetLimits (frompageCount,limitNum,100000)
    listcount=0
    res = cl.Query ('@(title,tags) '+kname,'price')
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
    kname=keywords.decode("hex")
    adkeywords=urlquote(kname.replace("+",""))
    keywords_hex=keywords
    nowurl="http://www.zz91.com"
    if (kname==None):
        return HttpResponseRedirect(nowurl)
    #-----------报价信息
    funpage = zz91page()
    limitNum=funpage.limitNum(50)
    nowpage=funpage.nowpage(int(page))
    frompageCount=funpage.frompageCount()
    after_range_num = funpage.after_range_num(2)
    before_range_num = funpage.before_range_num(9)
    
    port = settings.SPHINXCONFIG['port']
    cl = SphinxClient()
    cl.SetServer ( settings.SPHINXCONFIG['serverid'], port )
    cl.SetMatchMode ( SPH_MATCH_BOOLEAN )
    cl.SetSortMode( SPH_SORT_EXTENDED,"gmt_order desc" )
    
    cl.SetLimits (frompageCount,limitNum,100000)
    listcount=0
    res = cl.Query ('@(title,tags) '+kname,'price')
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
    
    port = settings.SPHINXCONFIG['port']
    cl = SphinxClient()
    cl.SetServer ( settings.SPHINXCONFIG['serverid'], port )
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
    
    port = settings.SPHINXCONFIG['port']
    cl = SphinxClient()
    cl.SetServer ( settings.SPHINXCONFIG['serverid'], port )
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
    
    port = settings.SPHINXCONFIG['port']
    listcount=0
    cl = SphinxClient()
    cl.SetServer ( settings.SPHINXCONFIG['serverid'], port )
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
                list1=getcompinfo(pdtid,cursor_my,kname)
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
    showad=getshowadflag()
    if (gethextype(keywords)==False):
        kname=keywords.encode('utf8','ignore').strip()
        keywords_hex=keywords.encode('utf8','ignore').encode("hex")
    else:
        kname=keywords.decode("hex").strip()
        keywords_hex=keywords
    
    tags_keywords=kname.replace("+","")
    adkeywords=urlquote(kname.replace("+",""))
    nowurl="http://www.zz91.com"
    
    listall_tags=newtagslist(kname,50)
    
    
    if (kname==None):
        return HttpResponseRedirect(nowurl)
    #seo 客户链接
    seolist=getseolist()
    cplist=getcplist()
    tagschickNum(kname)
    #广告
    adlist=getadlist(373,kname)
    #-----------供应信息
    listcount0=0
    listall_offerlist=getofferlist(kname=kname,ckind='0',num=15)
    if (listall_offerlist):
        listall=listall_offerlist['list']
        listcount0=listall_offerlist['count']
    #-----------求购信息
    listcount1=0
    try:
        listall_offerlist1=getofferlist(kname=kname,ckind='1',num=15)
        #listall_offerlist1=None
        if (listall_offerlist1):
            listall1=listall_offerlist1['list']
            listcount1=listall_offerlist1['count']
        listcount=listcount0+listcount1
    except:
        
        listall_offerlist1 =None
    #-----------报价信息
    listcount_baojia_all=0
    listall_pricelist=getpricelist(kname=kname,num=10)
    if (listall_pricelist):
        listall_baojia=listall_pricelist['list']
        listcount_baojia=listall_pricelist['count']
        havelist_price=listall_pricelist['havelist']
        listcount_baojia_all=listcount_baojia_all+listcount_baojia
    #----企业报价
    listall_pricelist_company=getpricelist_company(kname=kname,num=10)
    if (listall_pricelist_company):
        listall_baojia_company=listall_pricelist_company['list']
        listcount_baojia_company=listall_pricelist_company['count']
        listcount_baojia_all=listcount_baojia_all+listcount_baojia_company
    
    #-----------资讯信息
    listall_bbslist=getbbslist(kname=kname,num=20)
    if (listall_bbslist):
        listall_news=listall_bbslist['list']
        listcount_news=listall_bbslist['count']
        havelist_bbs=listall_bbslist['havelist']

    
    

    return render_to_response('tags/mainlist.html',locals())
    closeconn()

#标签列表
def tagsTradeList(request, kind, keywords, page):
    showad=getshowadflag()
    if (gethextype(keywords)==False):
        kname=keywords.encode('utf8','ignore')
        keywords_hex=keywords.encode('utf8','ignore').encode("hex")
    else:
        kname=keywords.decode("hex")
        keywords_hex=keywords
    tags_keywords=kname.replace("+","")
    adkeywords=urlquote(kname.replace("+",""))
    #广告
    
    listall_tags=newtagslist(kname,50)
    nowurl="http://www.zz91.com"
    if (kname==None or listall_tags==None or listall_tags==[]):
        return HttpResponseRedirect(nowurl)
    adlist=getadlist(373,kname)
    #-----------供求信息
    funpage = zz91page()
    limitNum=funpage.limitNum(50)
    nowpage=funpage.nowpage(int(page))
    frompageCount=funpage.frompageCount()
    after_range_num = funpage.after_range_num(2)
    before_range_num = funpage.before_range_num(9)
    
    port = settings.SPHINXCONFIG['port']
    cl = SphinxClient()
    cl.SetServer ( settings.SPHINXCONFIG['serverid'], port )
    cl.SetMatchMode ( SPH_MATCH_BOOLEAN )
    cl.SetFilter('check_status',[1])
    if kind:
        cl.SetFilter('pdt_kind',[int(kind)])
    kindclass1=""
    kindclass2=""
    if (kind=='0'):
        kindclass1="on"
        kindclass2=""
        kindtext="供求信息"
        seo_t=kname+"_"+kname+"供应_"+kname+"出售_第"+str(page)+"页"
        seo_d=""+kname+"供应标签频道为你提供最新最全的"+kname+"供应信息,"+kname+"出售信息，让你及时掌握最新"+kname+"价格行情资讯，让你生意翻倍。"
        seo_k=kname+"供应"
    if (kind=='1'):
        kindclass1=""
        kindclass2="on"
        kindtext="求购信息"
        seo_t=""+kname+"_"+kname+"求购_"+kname+"回收_第"+str(page)+"页"
        seo_d=""+kname+"求购标签频道为你提供最新最全的"+kname+"求购信息,"+kname+"回收信息，让你及时掌握最新"+kname+"价格行情资讯，让你生意翻倍。"
        seo_k=""+kname+"求购, "+kname+"回收"
        
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
                list1=getcompinfo(pdtid,cursor_my,kname)
                
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
    
    
    return render_to_response('tags/tradelist.html',locals())
    closeconn()
def tagsPriceList(request, keywords, page):
    showad=getshowadflag()
    if (gethextype(keywords)==False):
        kname=keywords.encode('utf8','ignore')
        keywords_hex=keywords.encode('utf8','ignore').encode("hex")
    else:
        kname=keywords.decode("hex")
        keywords_hex=keywords
    tags_keywords=kname
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
    
    port = settings.SPHINXCONFIG['port']
    cl = SphinxClient()
    cl.SetServer ( settings.SPHINXCONFIG['serverid'], port )
    cl.SetMatchMode ( SPH_MATCH_BOOLEAN )
    cl.SetSortMode( SPH_SORT_EXTENDED,"gmt_order desc" )
    
    cl.SetLimits (frompageCount,limitNum,100000)

    res = cl.Query ('@(title,tags) '+kname,'price')
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
    
    return render_to_response('tags/pricelist.html',locals())
    closeconn()
def tagsPriceCompanyList(request, keywords, page):
    if (gethextype(keywords)==False):
        kname=keywords.encode('utf8','ignore')
        keywords_hex=keywords.encode('utf8','ignore').encode("hex")
    else:
        kname=keywords.decode("hex")
        keywords_hex=keywords
    tags_keywords=kname
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
    
    port = settings.SPHINXCONFIG['port']
    cl = SphinxClient()
    cl.SetServer ( settings.SPHINXCONFIG['serverid'], port )
    cl.SetMatchMode ( SPH_MATCH_BOOLEAN )
    cl.SetSortMode( SPH_SORT_EXTENDED,"post_time desc" )
    
    cl.SetLimits (frompageCount,limitNum,100000)
    listcount=0
    res = cl.Query ('@(title,label1,label2,label3,area1,area2,area3) '+kname,'company_price')
    if res:
        if res.has_key('matches'):
            tagslist=res['matches']
            listall=[]
            for match in tagslist:
                id=match['id']
                attrs=match['attrs']
                title=attrs['ptitle']
                gmt_time=attrs['ppost_time']
                price=attrs['price']
                price_unit=attrs['price_unit']
                min_price=attrs['min_price']
                max_price=attrs['max_price']
                #if (price=="" or price=="none"):
                price=min_price+"-"+max_price+price_unit
                list1={'title':title,'id':id,'gmt_time':gmt_time,'price':price}
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
    
    return render_to_response('tags/pricecompanylist.html',locals())
    closeconn()
def tagsnewsList(request, keywords, page):
    if (gethextype(keywords)==False):
        kname=keywords.encode('utf8','ignore')
        keywords_hex=keywords.encode('utf8','ignore').encode("hex")
    else:
        kname=keywords.decode("hex")
        keywords_hex=keywords
    tags_keywords=kname
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
    
    return render_to_response('tags/newslist.html',locals())    
def tagsHuzhuList(request, keywords, page):
    if (gethextype(keywords)==False):
        kname=keywords.encode('utf8','ignore')
        keywords_hex=keywords.encode('utf8','ignore').encode("hex")
    else:
        kname=keywords.decode("hex")
        keywords_hex=keywords
    tags_keywords=kname
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
    
    port = settings.SPHINXCONFIG['port']
    cl = SphinxClient()
    cl.SetServer ( settings.SPHINXCONFIG['serverid'], port )
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
                gmt_time=attrs['ppost_time']
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
    
    return render_to_response('tags/bbslist.html',locals())

def searckkeyword_hex(request):
    keywords=request.GET.get("tagName")
    keywords=getjiami(keywords)
    nowurl="/s/"+keywords+"/"
    #return render_to_response('tags/search.htm',locals())
    return HttpResponseRedirect(nowurl)

