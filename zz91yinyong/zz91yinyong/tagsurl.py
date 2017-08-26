#-*- coding:utf-8 -*-
import sys
from django.http import HttpResponse,HttpResponseRedirect
reload(sys) 
sys.setdefaultencoding('utf-8') 
#加密
def getjiami(strword):
    return strword.encode('utf8','ignore').encode("hex")
def getjiemi(strword):
    return strword.decode("hex").decode('utf8','ignore')
#判断是否为HEX码
def gethextype(keywords):
    zwtype=0
    zwflag=0
    strvalue="abcdef0123456789"
    for a in keywords:
        if (a >= u'\u4e00' and a<=u'\u9fa5'):
            zwflag=zwflag+1
    if zwflag>0:
        zwtype=1
    zwflag=0
    if zwtype==0:
        for a in keywords:
            if (strvalue.find(a)==-1):
                zwflag=zwflag+1
        if zwflag>0:
            zwtype=1
    if zwtype==1:
        return False
    else:
        return True

def tagsPriceList(request,keywords,page):
    if (gethextype(keywords)==False):
        kname=keywords.encode('utf8','ignore')
        keywords_hex=keywords.encode('utf8','ignore').encode("hex")
    else:
        kname=keywords.decode("hex")
        keywords_hex=keywords
    nowurl="http://m.zz91.com/price/?keywords="+kname
    return HttpResponseRedirect(nowurl)
def tagsHuzhuList(request,keywords,page):
    if (gethextype(keywords)==False):
        kname=keywords.encode('utf8','ignore')
        keywords_hex=keywords.encode('utf8','ignore').encode("hex")
    else:
        kname=keywords.decode("hex")
        keywords_hex=keywords
    nowurl="http://m.zz91.com/huzhu/?keywords="+kname
    return HttpResponseRedirect(nowurl)
def tagsnewsList(request,keywords,page):
    if (gethextype(keywords)==False):
        kname=keywords.encode('utf8','ignore')
        keywords_hex=keywords.encode('utf8','ignore').encode("hex")
    else:
        kname=keywords.decode("hex")
        keywords_hex=keywords
    nowurl="http://m.zz91.com/news/search.html?keywords="+kname
    return HttpResponseRedirect(nowurl)
def tagsPriceCompanyList(request,keywords,page):
    if (gethextype(keywords)==False):
        kname=keywords.encode('utf8','ignore')
        keywords_hex=keywords.encode('utf8','ignore').encode("hex")
    else:
        kname=keywords.decode("hex")
        keywords_hex=keywords
    nowurl="http://m.zz91.com/price/?keywords="+kname
    return HttpResponseRedirect(nowurl)
def tagssearchList_hex(request,keywords,page):
    if (gethextype(keywords)==False):
        kname=keywords.encode('utf8','ignore')
        keywords_hex=keywords.encode('utf8','ignore').encode("hex")
    else:
        kname=keywords.decode("hex")
        keywords_hex=keywords
    nowurl="http://m.zz91.com/offerlist/?keywords="+kname
    return HttpResponseRedirect(nowurl)
def tagsTradeList(request,keywords,kind,page):
    if (gethextype(keywords)==False):
        kname=keywords.encode('utf8','ignore')
        keywords_hex=keywords.encode('utf8','ignore').encode("hex")
    else:
        kname=keywords.decode("hex")
        keywords_hex=keywords
    nowurl="http://m.zz91.com/offerlist/?keywords="+kname+"&ptype="+str(kind)+"&page="+str(page)
    return HttpResponseRedirect(nowurl)
def tagsmain(request,keywords):
    if (gethextype(keywords)==False):
        kname=keywords.encode('utf8','ignore')
        keywords_hex=keywords.encode('utf8','ignore').encode("hex")
    else:
        kname=keywords.decode("hex")
        keywords_hex=keywords
    nowurl="http://m.zz91.com/offerlist/?keywords="+kname
    return HttpResponseRedirect(nowurl)
