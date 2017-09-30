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
execfile(nowpath+"/func/crmtools.py")

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

#----单品报价数据
def price_table_list(request):
    pricecategorylist=zzprice.getpricecategorylist(parent_id="1")
    pricecategorylist1=zzprice.getpricecategorylist(parent_id="2")
    type_id=request.GET.get('type_id')
    priceid=request.GET.get('priceid')
    assist_type_id=request.GET.get('assist_type_id')
    searchlist={}
    if type_id:
        searchlist['type_id']=type_id
        price_category_label=zzprice.getpricecategorylabel(type_id)
    if assist_type_id:
        searchlist['assist_type_id']=assist_type_id
        assist_type_label=zzprice.getpricecategorylabel(assist_type_id)
    postdate_min=request.GET.get('postdate_min')
    postdate_max=request.GET.get('postdate_max')
    gmt_modified_min=request.GET.get('gmt_modified_min')
    gmt_modified_max=request.GET.get('gmt_modified_max')
    if postdate_min:
        searchlist['postdate_min']=postdate_min
    else:
        postdate_min=''
    if postdate_max:
        searchlist['postdate_max']=postdate_max
    else:
        postdate_max=''
    if gmt_modified_min:
        searchlist['gmt_modified_min']=gmt_modified_min
    else:
        gmt_modified_min=''
    if gmt_modified_max:
        searchlist['gmt_modified_max']=gmt_modified_max
    else:
        gmt_modified_max=''
    if priceid:
        searchlist['priceid']=priceid
    searchurl=urllib.urlencode(searchlist)
    page=request.GET.get('page')
    if not page:
        page=1
    funpage=zz91page()
    limitNum=funpage.limitNum(20)
    nowpage=funpage.nowpage(int(page))
    frompageCount=funpage.frompageCount()
    after_range_num = funpage.after_range_num(3)
    before_range_num = funpage.before_range_num(6)
    pricetablelist=zzprice.getpricetablelist(frompageCount,limitNum,searchlist=searchlist)
    listall=pricetablelist['list']
    listcount=pricetablelist['count']
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
    return render_to_response('price/price_table_list.html',locals())
def add_price_list(request):
    pricecategorylist=zzprice.getpricecategorylist(parent_id="1")
    pricecategorylist1=zzprice.getpricecategorylist(parent_id="2")
    return render_to_response('price/add_price_list.html',locals())
def update_price_list(request):
    pricecategorylist=zzprice.getpricecategorylist(parent_id="1")
    pricecategorylist1=zzprice.getpricecategorylist(parent_id="2")
    id=request.GET.get('id')
    sql='select id,priceid,typename,title,type_id,assist_type_id,label,label1,label2,spec,spec1,spec2,price,area,area1,area2,price1,price2,price3,price4,price5,price6,unit,qushi,qushi1,postdate,othertext,othertext1,num from price_list where id=%s'
    result=zzprice.dbc.fetchonedb(sql,[id])
    priceid=result[1]
    if priceid is None:
        priceid=''
    typename=result[2]
    if typename is None:
        typename=''
    title=result[3]
    if title is None:
        title=''
    type_id=result[4]
    if type_id is None:
        type_id=''
    assist_type_id=result[5]
    if assist_type_id is None:
        assist_type_id=''
    label=result[6]
    if label is None:
        label=''
    label1=result[7]
    if label1 is None:
        label1=''
    label2=result[8]
    if label2 is None:
        label2=''
    spec=result[9]
    if spec is None:
        spec=''
    spec1=result[10]
    if spec1 is None:
        spec1=''
    spec2=result[11]
    if spec2 is None:
        spec2=''
    price=result[12]
    if price is None:
        price=''
    area=result[13]
    if area is None:
        area=''
    area1=result[14]
    if area1 is None:
        area1=''
    area2=result[15]
    if area2 is None:
        area2=''
    price1=result[16]
    if price1 is None:
        price1=''
    price2=result[17]
    if price2 is None:
        price2=''
    price3=result[18]
    if price3 is None:
        price3=''
    price4=result[19]
    if price4 is None:
        price4=''
    price5=result[20]
    if price5 is None:
        price5=''
    price6=result[21]
    if price6 is None:
        price6=''
    unit=result[22]
    if unit is None:
        unit=''
    qushi=result[23]
    if qushi is None:
        qushi=''
    qushi1=result[24]
    if qushi1 is None:
        qushi1=''
    postdate=result[25]
    if postdate is None:
        postdate=''
    else:
        postdate=formattime(postdate,flag=1)
    othertext=result[26]
    if othertext is None:
        othertext=''
    othertext1=result[27]
    if othertext1 is None:
        othertext1=''
    num=result[28]
    if num is None:
        num=''
    return render_to_response('price/update_price_list.html',locals())
def save_price_list(request):
    id=request.POST.get('id')
    priceid=request.POST.get('priceid')
    typename=request.POST.get('typename')
    title=request.POST.get('title')
    type_id=request.POST.get('type_id')
    assist_type_id=request.POST.get('assist_type_id')
    label=request.POST.get('label')
    label1=request.POST.get('label1')
    label2=request.POST.get('label2')
    spec=request.POST.get('spec')
    spec1=request.POST.get('spec1')
    spec2=request.POST.get('spec2')
    price=request.POST.get('price')
    area=request.POST.get('area')
    area1=request.POST.get('area1')
    area2=request.POST.get('area2')
    price1=request.POST.get('price1')
    price2=request.POST.get('price2')
    price3=request.POST.get('price3')
    price4=request.POST.get('price4')
    price5=request.POST.get('price5')
    price6=request.POST.get('price6')
    unit=request.POST.get('unit')
    qushi=request.POST.get('qushi')
    qushi1=request.POST.get('qushi1')
    postdate=request.POST.get('postdate')
    othertext=request.POST.get('othertext')
    othertext1=request.POST.get('othertext1')
    num=request.POST.get('num')
    gmt_modified=datetime.datetime.now()
    if id:
        sql='update price_list set typename=%s,title=%s,type_id=%s,assist_type_id=%s,label=%s,label1=%s,label2=%s,spec=%s,spec1=%s,spec2=%s,price=%s,area=%s,area1=%s,area2=%s,price1=%s,price2=%s,price3=%s,price4=%s,price5=%s,price6=%s,unit=%s,qushi=%s,qushi1=%s,postdate=%s,othertext=%s,othertext1=%s,num=%s where id=%s'
        zzprice.dbc.updatetodb(sql,[typename,title,type_id,assist_type_id,label,label1,label2,spec,spec1,spec2,price,area,area1,area2,price1,price2,price3,price4,price5,price6,unit,qushi,qushi1,postdate,othertext,othertext1,num,id])
    elif not id:
        sql='insert into price_list(priceid,typename,title,type_id,assist_type_id,label,label1,label2,spec,spec1,spec2,price,area,area1,area2,price1,price2,price3,price4,price5,price6,unit,qushi,qushi1,postdate,othertext,othertext1,num,gmt_modified) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
        zzprice.dbc.updatetodb(sql,[priceid,typename,title,type_id,assist_type_id,label,label1,label2,spec,spec1,spec2,price,area,area1,area2,price1,price2,price3,price4,price5,price6,unit,qushi,qushi1,postdate,othertext,othertext1,num,gmt_modified])
    return HttpResponseRedirect('price_table_list.html')
def del_price_list(request):
    id=request.POST.get('id')
    sql='delete from price_list where id=%s'
    zzprice.dbc.updatetodb(sql,[id])
    return HttpResponseRedirect('price_table_list.html')
    
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