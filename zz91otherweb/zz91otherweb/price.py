#-*- coding:utf-8 -*-
from django.shortcuts import render_to_response
from django.http import HttpResponse,HttpResponseRedirect
from django.core.cache import cache
from zz91tools import getToday,getYesterday,date_to_str
from zz91page import *
import os,datetime,time,sys,calendar,urllib
reload(sys)
sys.setdefaultencoding('UTF-8')
nowpath=os.path.dirname(__file__)
execfile(nowpath+"/func/price_function.py")

zzprice=zz91price()

def price_category(request):
    parent_id=request.GET.get('parent_id')
    if not parent_id:
        parent_id=0
    listall=zzprice.getpricenextcategory(parent_id)
    return render_to_response('price/price_category.html',locals())

def getc_label(request):
    c_pinyin=''
    c_label=request.GET.get('c_label')
    if c_label:
        c_pinyin=zzprice.getpriceattrpinyin(c_label)
    return HttpResponse(c_pinyin)

def returnpage(request):
    request_url=request.GET.get('request_url')
    return HttpResponseRedirect(request_url)

#----报价类别字段
def price_category_field(request):
    pricecategorylist=zzprice.getpricecategorylist(parent_id="1")
    pricecategorylist1=zzprice.getpricecategorylist(parent_id="2")
    page=request.GET.get('page')
    price_category_id=request.GET.get('price_category_id')
    assist_type_id=request.GET.get('assist_type_id')
    searchlist={}
    if price_category_id:
        searchlist['price_category_id']=price_category_id
        price_category_label=zzprice.getpricecategorylabel(price_category_id)
    if assist_type_id:
        searchlist['assist_type_id']=assist_type_id
        assist_type_label=zzprice.getpricecategorylabel(assist_type_id)
    searchurl=urllib.urlencode(searchlist)
    if not page:
        page=1
    funpage=zz91page()
    limitNum=funpage.limitNum(20)
    nowpage=funpage.nowpage(int(page))
    frompageCount=funpage.frompageCount()
    after_range_num = funpage.after_range_num(3)
    before_range_num = funpage.before_range_num(6)
    pricectattrlist=zzprice.getpricectfieldlist(frompageCount,limitNum,price_category_id=price_category_id,assist_type_id="")
    listall=pricectattrlist['list']
    listcount=pricectattrlist['count']
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
    prvpage = funpage.prvpage()
    return render_to_response('price/price_category_field.html',locals())

def add_pricefield(request):
    listfields=listfield
    request_url=request.META.get('HTTP_REFERER','/')
#    pricectattrlist2=zzprice.getpricectattrlist2()
    pricecategorylist=zzprice.getpricecategorylist(parent_id="1")
    pricecategorylist1=zzprice.getpricecategorylist(parent_id="2")
    return render_to_response('price/add_pricefield.html',locals())
def update_pricefield(request):
    listfields=listfield
    request_url=request.META.get('HTTP_REFERER','/')
    pricecategorylist=zzprice.getpricecategorylist(parent_id="1")
    pricecategorylist1=zzprice.getpricecategorylist(parent_id="2")
    priceattrid=request.GET.get('priceattrid')
    pricefielddetail=zzprice.getpricefielddetail(priceattrid)
    price_category_id=pricefielddetail['price_category_id']
    price_category_label=pricefielddetail['price_category_label']
    assist_type_id=pricefielddetail['assist_type_id']
    assist_type_label=pricefielddetail['assist_type_label']
    name=pricefielddetail['name']
    field=pricefielddetail['field']
    sortrank=pricefielddetail['sortrank']
    return render_to_response('price/add_pricefield.html',locals())
def del_pricefield(request):
    request_url=request.META.get('HTTP_REFERER','/')
    priceattrid=request.GET.get('priceattrid')
    sql='delete from price_category_field where id=%s'
    zzprice.dbc.updatetodb(sql,[priceattrid])
    return HttpResponseRedirect(request_url)
def add_pricefieldok(request):
    request_url=request.GET.get('request_url')
    name=request.GET.get('name')
    field=request.GET.get('field')
    sortrank=request.GET.get('sortrank')
    priceattrid=request.GET.get('priceattrid')
    if sortrank.isdigit()==True:
        sortrank=int(sortrank)
    else:
        sortrank=50
    price_category_id=request.GET.get('price_category_id')
    if price_category_id:
        price_category_label=zzprice.getpricecategorylabel(price_category_id)
    assist_type_id=request.GET.get('assist_type_id')
    if assist_type_id:
        assist_type_label=zzprice.getpricecategorylabel(assist_type_id)
    error='此处不能为空'
    errors=''
    if not name:
        error1=error
        errors=1
    if not field:
        error2=error
        errors=1
    if not price_category_id:
        price_category_id=0
#        error3='请选择报价类别'
#        errors=1
    if errors:
        pricecategorylist=zzprice.getpricecategorylist(parent_id="1")
        pricecategorylist1=zzprice.getpricecategorylist(parent_id="2")
        return render_to_response('price/add_pricefield.html',locals())
    if priceattrid:
        sql='update price_category_field set price_category_id=%s,assist_type_id=%s,name=%s,field=%s,sortrank=%s where id=%s'
        zzprice.dbc.updatetodb(sql,[price_category_id,assist_type_id,name,field,sortrank,priceattrid])
    else:
        sql='insert into price_category_field(price_category_id,assist_type_id,name,field,sortrank) values(%s,%s,%s,%s,%s)'
        zzprice.dbc.updatetodb(sql,[price_category_id,assist_type_id,name,field,sortrank])
    return HttpResponseRedirect(request_url)

#----报价类别地区
def price_category_attr(request):
#    pricectattrlist2=zzprice.getpricectattrlist2()
#    pricecategorylist=zzprice.getpricecategorylist()
    jinshulist1=zzprice.getpricenextcategory2(9)
    suliaolist=zzprice.getpricenextcategory2(4)
    feizhilist=zzprice.getpricenextcategory2(7)
    jinshuarealist=zzprice.getpricenextcategory(3)
    suliaolist1=zzprice.getpricenextcategory2(11)
    suliaoarealist=zzprice.getpricenextcategory(22)
    shichanglist=zzprice.getpricenextcategory(60)
    parent_id=request.GET.get('parent_id')
    page=request.GET.get('page')
    price_category_id=request.GET.get('price_category_id')
    if not price_category_id:
        price_category_id=request.GET.get('price_category_id1')
    if not price_category_id:
        price_category_id=request.GET.get('price_category_id2')
    if not price_category_id:
        price_category_id=request.GET.get('price_category_id3')
    if not price_category_id:
        price_category_id=request.GET.get('price_category_id4')
    if not price_category_id:
        price_category_id=request.GET.get('price_category_id5')
    searchlist={}
    if price_category_id:
        searchlist['price_category_id']=price_category_id
        price_category_label=zzprice.getpricecategorylabel(price_category_id)
    searchurl=urllib.urlencode(searchlist)
    if not page:
        page=1
    funpage=zz91page()
    limitNum=funpage.limitNum(20)
    nowpage=funpage.nowpage(int(page))
    frompageCount=funpage.frompageCount()
    after_range_num = funpage.after_range_num(3)
    before_range_num = funpage.before_range_num(6)
    pricectattrlist=zzprice.getpricectattrlist(frompageCount,limitNum,price_category_id,parent_id)
    listall=pricectattrlist['list']
    listcount=pricectattrlist['count']
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
    prvpage = funpage.prvpage()
    return render_to_response('price/price_category_attr.html',locals())
def add_priceattr(request):
    request_url=request.META.get('HTTP_REFERER','/')
    pricectattrlist2=zzprice.getpricectattrlist2()
#    pricecategorylist=zzprice.getpricecategorylist()
    jinshulist1=zzprice.getpricenextcategory2(9)
    suliaolist=zzprice.getpricenextcategory2(4)
    feizhilist=zzprice.getpricenextcategory2(7)
    jinshuarealist=zzprice.getpricenextcategory(3)
    suliaolist1=zzprice.getpricenextcategory2(11)
    suliaoarealist=zzprice.getpricenextcategory(22)
    shichanglist=zzprice.getpricenextcategory(60)
    return render_to_response('price/add_priceattr.html',locals())
def update_priceattr(request):
    request_url=request.META.get('HTTP_REFERER','/')
    pricectattrlist2=zzprice.getpricectattrlist2()
    jinshulist1=zzprice.getpricenextcategory2(9)
    suliaolist=zzprice.getpricenextcategory2(4)
    feizhilist=zzprice.getpricenextcategory2(7)
    jinshuarealist=zzprice.getpricenextcategory(3)
    suliaolist1=zzprice.getpricenextcategory2(11)
    suliaoarealist=zzprice.getpricenextcategory(22)
    shichanglist=zzprice.getpricenextcategory(60)
#    pricecategorylist=zzprice.getpricecategorylist()
    priceattrid=request.GET.get('priceattrid')
    priceattrdetail=zzprice.getpriceattrdetail(priceattrid)
    parent_id=priceattrdetail['parent_id']
    parent_label=priceattrdetail['parent_label']
    price_category_id=priceattrdetail['price_category_id']
    price_category_label=priceattrdetail['price_category_label']
    label=priceattrdetail['label']
    pinyin=priceattrdetail['pinyin']
    sortrank=priceattrdetail['sortrank']
    page_type=priceattrdetail["page_type"]
    return render_to_response('price/add_priceattr.html',locals())
def del_priceattr(request):
    request_url=request.META.get('HTTP_REFERER','/')
    priceattrid=request.GET.get('priceattrid')
    sql='delete from price_category_attr where id=%s'
    zzprice.dbc.updatetodb(sql,[priceattrid])
    return HttpResponseRedirect(request_url)
def add_priceattrok(request):
    request_url=request.GET.get('request_url')
    label=request.GET.get('label')
    pinyin=request.GET.get('pinyin')
    sortrank=request.GET.get('sortrank')
    page_type=request.GET.get('page_type')
    priceattrid=request.GET.get('priceattrid')
    if sortrank.isdigit()==True:
        sortrank=int(sortrank)
    else:
        sortrank=50
    parent_id=request.GET.get('parent_id')
    if parent_id:
        parent_label=zzprice.getpriceattrlabel(parent_id)
    price_category_id=request.GET.get('price_category_id')
    if price_category_id:
        price_category_label=zzprice.getpricecategorylabel(price_category_id)
    error='此处不能为空'
    errors=''
    if not label:
        error1=error
        errors=1
    if not pinyin:
        error2=error
        errors=1
    if not parent_id:
        parent_id=0
    if not price_category_id:
        price_category_id=0
    if not priceattrid:
        sql2='select id from price_category_attr where parent_id=%s and price_category_id=%s and label=%s'
        result=zzprice.dbc.fetchonedb(sql2,[parent_id,price_category_id,label])
        if result:
            error3='此类别已经存在'
            errors=1
    if errors:
        pricectattrlist2=zzprice.getpricectattrlist2()
        pricecategorylist=zzprice.getpricecategorylist()
        return render_to_response('price/add_priceattr.html',locals())
    if priceattrid:
        sql='update price_category_attr set parent_id=%s,price_category_id=%s,label=%s,pinyin=%s,sortrank=%s,page_type=%s where id=%s'
        zzprice.dbc.updatetodb(sql,[parent_id,price_category_id,label,pinyin,sortrank,page_type,priceattrid])
    else:
        sql='insert into price_category_attr(parent_id,price_category_id,label,pinyin,sortrank,page_type) values(%s,%s,%s,%s,%s,%s)'
        zzprice.dbc.updatetodb(sql,[parent_id,price_category_id,label,pinyin,sortrank,page_type])
    return HttpResponseRedirect(request_url)