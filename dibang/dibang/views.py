#-*- coding:utf-8 -*-
import MySQLdb,settings,codecs,os,sys,datetime,time,random,requests,hashlib,md5,simplejson,urllib
from django.shortcuts import render_to_response
from django.template.loader import get_template
from django.template import Context
from django.http import HttpResponse,HttpResponseRedirect,HttpResponseForbidden,HttpResponseNotFound,HttpResponsePermanentRedirect
from datetime import timedelta, date 
from dict2xml import dict2xml
from django.core.cache import cache
from zz91db_dibang import dibangdb
dbd=dibangdb(1)
from zz91page import *
reload(sys) 
sys.setdefaultencoding('utf-8') 
nowpath=os.path.dirname(__file__)
execfile(nowpath+"/func/dibang_function.py")
execfile(nowpath+"/func/crmtools.py")
zzdibang=zzdibang()
#主框架
def main(request):
    username=request.session.get('username',default=None)
    group_id=request.session.get('group_id',default=None)
    utype=request.session.get('utype',default=None)
    user_selfid=request.session.get('user_selfid',default=None)
    isadmin=zzdibang.isadmin(utype)
    if not username:
        return HttpResponseRedirect("login.html")
    return render_to_response('main.html',locals())
def index(request):
    username=request.session.get('username',default=None)
    group_id=request.session.get('group_id',default=None)
    user_selfid=request.session.get('user_selfid',default=None)
    if not username:
        return HttpResponseRedirect("login.html")
    return render_to_response('index.html',locals())
#分站（打包站）列表
def company(request):
    username=request.session.get('username',default=None)
    group_id=request.session.get('group_id',default=None)
    user_selfid=request.session.get('user_selfid',default=None)
    if not username:
        return HttpResponseRedirect("login.html")
    return render_to_response('company.html',locals())
#分站（打包站）列表数据
def company_data(request):
    page=request.GET.get('page')
    name=request.GET.get('name')
    username=request.session.get('username',default=None)
    group_id=request.session.get('group_id',default=None)
    user_selfid=request.session.get('user_selfid',default=None)
    searchlist={}
    if name:
        searchlist['name']=name
    searchurl=urllib.urlencode(searchlist)
    if not page:
        page=1
    funpage=zz91page()
    limitNum=funpage.limitNum(10)
    nowpage=funpage.nowpage(int(page))
    frompageCount=funpage.frompageCount()
    after_range_num = funpage.after_range_num(3)
    before_range_num = funpage.before_range_num(6)
    company_list=zzdibang.company_list(frompageCount,limitNum,name=name,group_id=group_id)
    listcount=0
    listall=company_list['list']
    listcount=company_list['count']
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
    list={"code":0,"msg":"","count":listcount,"data":listall}
    return HttpResponse(simplejson.dumps(list, ensure_ascii=False))
#分站添加
def company_add(request):
    username=request.session.get('username',default=None)
    group_id=request.session.get('group_id',default=None)
    user_selfid=request.session.get('user_selfid',default=None)
    if not username:
        return HttpResponseRedirect("login.html")
    return render_to_response('company_add.html',locals())
#分站修改
def company_mod(request):
    username=request.session.get('username',default=None)
    group_id=request.session.get('group_id',default=None)
    user_selfid=request.session.get('user_selfid',default=None)
    if not username:
        return HttpResponseRedirect("login.html")
    id=request.GET.get('id')
    sql='select name,ctype,address from company where id=%s'
    result=dbd.fetchonedb(sql,[id])
    if result:
        if not result['address']:
            result['address']=''
    return render_to_response('company_mod.html',locals())
#分站保存
def company_save(request):
    username=request.session.get('username',default=None)
    group_id=request.session.get('group_id',default=None)
    user_selfid=request.session.get('user_selfid',default=None)
    if not username:
        return HttpResponseRedirect("login.html")
    zzdibang.company_save(request)
    return HttpResponseRedirect("company.html")

#分站删除
def company_del(request):
    username=request.session.get('username',default=None)
    group_id=request.session.get('group_id',default=None)
    user_selfid=request.session.get('user_selfid',default=None)
    if not username:
        return HttpResponseRedirect("login.html")
    id=request.POST.get('id')
    sql='delete from company where id=%s'
    dbd.updatetodb(sql,[id])
    data={'answer':'answer'}
    return HttpResponse(simplejson.dumps(data, ensure_ascii=False))


#供货商列表
def supplier(request):
    username=request.session.get('username',default=None)
    group_id=request.session.get('group_id',default=None)
    user_selfid=request.session.get('user_selfid',default=None)
    if not username:
        return HttpResponseRedirect("login.html")
    return render_to_response('supplier.html',locals())
#供货商列表数据
def supplier_data(request):
    page=request.GET.get('page')
    iccode=request.GET.get('iccode')
    name=request.GET.get('name')
    username=request.session.get('username',default=None)
    group_id=request.session.get('group_id',default=None)
    company_id=request.session.get('company_id',default=None)
    searchlist={}
    if name:
        searchlist['name']=name
    if iccode:
        searchlist['iccode']=iccode
    searchurl=urllib.urlencode(searchlist)
    if not page:
        page=1
    funpage=zz91page()
    limitNum=funpage.limitNum(10)
    nowpage=funpage.nowpage(int(page))
    frompageCount=funpage.frompageCount()
    after_range_num = funpage.after_range_num(3)
    before_range_num = funpage.before_range_num(6)
    supplier_list=zzdibang.supplier_list(frompageCount,limitNum,searchlist=searchlist,group_id=group_id,company_id=company_id)
    listcount=0
    listall=supplier_list['list']
    listcount=supplier_list['count']
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
    list={"code":0,"msg":"","count":listcount,"data":listall}
    return HttpResponse(simplejson.dumps(list, ensure_ascii=False))
#供货商添加
def supplier_add(request):
    username=request.session.get('username',default=None)
    group_id=request.session.get('group_id',default=None)
    user_selfid=request.session.get('user_selfid',default=None)
    utype=request.session.get('utype',default=None)
    iccode=formattime(datetime.datetime.now(),5)[2:]+str(random.randint(1, 20))
    if not username:
        return HttpResponseRedirect("login.html")
    company_id=request.session.get('company_id')
    if not username:
        return HttpResponseRedirect("login.html")
    if str(utype)=="1":
        company_list=zzdibang.getcompanylist(group_id=group_id)
    else:
        company_list=zzdibang.getcompanylist(company_id=company_id)
    return render_to_response('supplier_add.html',locals())
#供货商修改
def supplier_mod(request):
    username=request.session.get('username',default=None)
    group_id=request.session.get('group_id',default=None)
    user_selfid=request.session.get('user_selfid',default=None)
    company_id=request.session.get('company_id',default=None)
    if not username:
        return HttpResponseRedirect("login.html")
    id=request.GET.get('id')
    utype=request.session.get('utype',default=None)
    if not username:
        return HttpResponseRedirect("login.html")
    if str(utype)=="1":
        company_list=zzdibang.getcompanylist(group_id=group_id)
    else:
        company_list=zzdibang.getcompanylist(company_id=company_id)
        
    sql='select iccode,ctype,group_id,company_id,name,htype,contact,mobile,pwd,address,bz from suppliers where id=%s'
    result=dbd.fetchonedb(sql,[id])
    return render_to_response('supplier_mod.html',locals())
#供货商保存
def supplier_save(request):
    username=request.session.get('username',default=None)
    group_id=request.session.get('group_id',default=None)
    user_selfid=request.session.get('user_selfid',default=None)
    if not username:
        return HttpResponseRedirect("login.html")
    result=zzdibang.supplier_save(request)
    return HttpResponse(simplejson.dumps(result, ensure_ascii=False))
    #return HttpResponseRedirect("supplier.html")

#供货商删除
def supplier_del(request):
    username=request.session.get('username',default=None)
    group_id=request.session.get('group_id',default=None)
    user_selfid=request.session.get('user_selfid',default=None)
    if not username:
        return HttpResponseRedirect("login.html")
    id=request.POST.get('id')
    sql='delete from suppliers where id=%s'
    dbd.updatetodb(sql,[id])
    data={'answer':'answer'}
    return HttpResponse(simplejson.dumps(data, ensure_ascii=False))


#产品类别列表
def category(request):
    username=request.session.get('username',default=None)
    group_id=request.session.get('group_id',default=None)
    user_selfid=request.session.get('user_selfid',default=None)
    if not username:
        return HttpResponseRedirect("login.html")
    return render_to_response('category.html',locals())
#产品类别数据
def category_data(request):
    page=request.GET.get('page')
    name=request.GET.get('name')
    username=request.session.get('username',default=None)
    group_id=request.session.get('group_id',default=None)
    company_id=request.session.get('company_id',default=None)
    searchlist={}
    if name:
        searchlist['name']=name
    searchurl=urllib.urlencode(searchlist)
    if not page:
        page=1
    funpage=zz91page()
    limitNum=funpage.limitNum(10)
    nowpage=funpage.nowpage(int(page))
    frompageCount=funpage.frompageCount()
    after_range_num = funpage.after_range_num(3)
    before_range_num = funpage.before_range_num(6)
    category_list=zzdibang.category_list(frompageCount,limitNum,name=name,company_id=company_id)
    listcount=0
    listall=category_list['list']
    listcount=category_list['count']
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
    list={"code":0,"msg":"","count":listcount,"data":listall}
    return HttpResponse(simplejson.dumps(list, ensure_ascii=False))
#产品类别添加
def category_add(request):
    username=request.session.get('username',default=None)
    group_id=request.session.get('group_id',default=None)
    user_selfid=request.session.get('user_selfid',default=None)
    utype=request.session.get('utype',default=None)
    if not username:
        return HttpResponseRedirect("login.html")
    sub_selfid=request.GET.get('sub_selfid')
    company_id=request.session.get('company_id')
    if str(utype)=="1":
        company_list=zzdibang.getcompanylist(group_id=group_id)
    else:
        company_list=zzdibang.getcompanylist(company_id=company_id)
    return render_to_response('category_add.html',locals())
#产品类别修改
def category_mod(request):
    username=request.session.get('username',default=None)
    group_id=request.session.get('group_id',default=None)
    user_selfid=request.session.get('user_selfid',default=None)
    utype=request.session.get('utype',default=None)
    if not username:
        return HttpResponseRedirect("login.html")
    id=request.GET.get('id')
    company_id=request.session.get('company_id')
    if str(utype)=="1":
        company_list=zzdibang.getcompanylist(group_id=group_id)
    else:
        company_list=zzdibang.getcompanylist(company_id=company_id)
    sql='select sub_selfid,name from category_products where id=%s'
    result=dbd.fetchonedb(sql,[id])
    return render_to_response('category_mod.html',locals())
#产品类别保存
def category_save(request):
    username=request.session.get('username',default=None)
    group_id=request.session.get('group_id',default=None)
    user_selfid=request.session.get('user_selfid',default=None)
    if not username:
        return HttpResponseRedirect("login.html")
    zzdibang.category_save(request)
    return HttpResponseRedirect("category.html")

#产品类别删除
def category_del(request):
    username=request.session.get('username',default=None)
    group_id=request.session.get('group_id',default=None)
    user_selfid=request.session.get('user_selfid',default=None)
    if not username:
        return HttpResponseRedirect("login.html")
    id=request.POST.get('id')
    sql='delete from category_products where id=%s'
    dbd.updatetodb(sql,[id])
    data={'answer':'answer'}
    return HttpResponse(simplejson.dumps(data, ensure_ascii=False))


#产品列表
def product(request):
    username=request.session.get('username',default=None)
    group_id=request.session.get('group_id',default=None)
    user_selfid=request.session.get('user_selfid',default=None)
    if not username:
        return HttpResponseRedirect("login.html")
    return render_to_response('product.html',locals())
#产品数据
def product_data(request):
    page=request.GET.get('page')
    name=request.GET.get('name')
    username=request.session.get('username',default=None)
    group_id=request.session.get('group_id',default=None)
    company_id=request.session.get('company_id',default=None)
    searchlist={}
    if name:
        searchlist['name']=name
    searchurl=urllib.urlencode(searchlist)
    if not page:
        page=1
    funpage=zz91page()
    limitNum=funpage.limitNum(10)
    nowpage=funpage.nowpage(int(page))
    frompageCount=funpage.frompageCount()
    after_range_num = funpage.after_range_num(3)
    before_range_num = funpage.before_range_num(6)
    product_list=zzdibang.product_list(frompageCount,limitNum,name=name,company_id=company_id,group_id=group_id)
    listcount=0
    listall=product_list['list']
    listcount=product_list['count']
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
    list={"code":0,"msg":"","count":listcount,"data":listall}
    return HttpResponse(simplejson.dumps(list, ensure_ascii=False))
#产品添加
def product_add(request):
    username=request.session.get('username',default=None)
    group_id=request.session.get('group_id',default=None)
    user_selfid=request.session.get('user_selfid',default=None)
    
    if not username:
        return HttpResponseRedirect("login.html")
    company_id=request.session.get('company_id')
    categorylist=zzdibang.getcategorylist(company_id=company_id)
    return render_to_response('product_add.html',locals())
#产品修改
def product_mod(request):
    username=request.session.get('username',default=None)
    group_id=request.session.get('group_id',default=None)
    user_selfid=request.session.get('user_selfid',default=None)
    if not username:
        return HttpResponseRedirect("login.html")
    id=request.GET.get('id')
    company_id=request.session.get('company_id')
    categorylist=zzdibang.getcategorylist(company_id=company_id)
    sql='select name,name_py,category_selfid,spec,unit,stock,bz from products where id=%s'
    result=dbd.fetchonedb(sql,[id])
    return render_to_response('product_mod.html',locals())
#产品保存
def product_save(request):
    username=request.session.get('username',default=None)
    group_id=request.session.get('group_id',default=None)
    user_selfid=request.session.get('user_selfid',default=None)
    if not username:
        return HttpResponseRedirect("login.html")
    zzdibang.product_save(request)
    return HttpResponseRedirect("product.html")

#产品删除
def product_del(request):
    username=request.session.get('username',default=None)
    group_id=request.session.get('group_id',default=None)
    user_selfid=request.session.get('user_selfid',default=None)
    if not username:
        return HttpResponseRedirect("login.html")
    id=request.POST.get('id')
    sql='delete from products where id=%s'
    dbd.updatetodb(sql,[id])
    data={'answer':'answer'}
    return HttpResponse(simplejson.dumps(data, ensure_ascii=False))


#入库单列表
def storage(request):
    username=request.session.get('username',default=None)
    group_id=request.session.get('group_id',default=None)
    user_selfid=request.session.get('user_selfid',default=None)
    company_id=request.session.get('company_id',default=None)
    if not username:
        return HttpResponseRedirect("login.html")
    sql='select count(id) as storage_count from storage where company_id=%s and status=4'
    storage_count=dbd.fetchonedb(sql,[company_id])['storage_count']
    sql='select sum(nw) as storage_weight from storage where company_id=%s and status=4'
    storage_weight=dbd.fetchonedb(sql,[company_id])['storage_weight']
    sql='select sum(total) as total_amount from storage where company_id=%s and ispay>=1'
    total_amount=dbd.fetchonedb(sql,[company_id])['total_amount']
    supplier_list=zzdibang.getsupplierlist(company_id=company_id)
    company_list=zzdibang.getcompanylist(company_id=company_id)
    #category_list=zzdibang.getcategorylist(company_id=company_id)
    productslist=zzdibang.getproductlist(company_id=company_id)
    return render_to_response('storage.html',locals())
#产品数据
def storage_data(request):
    username=request.session.get('username',default=None)
    group_id=request.session.get('group_id',default=None)
    company_id=request.session.get('company_id',default=None)
    page=request.GET.get('page')
    code=request.GET.get('code')
    products_selfid=request.GET.get('products_selfid')
    suppliers_selfid=request.GET.get('suppliers_selfid')
    time_min=request.GET.get('time_min')
    time_max=request.GET.get('time_max')
    proname=request.GET.get('proname')
    searchlist={}
    if code:
        searchlist['code']=code
    if products_selfid:
        searchlist['products_selfid']=products_selfid
    if suppliers_selfid:
        searchlist['suppliers_selfid']=suppliers_selfid
    if time_min:
        searchlist['time_min']=time_min
    if time_max:
        searchlist['time_max']=time_max
    if proname:
        searchlist['proname']=proname
    searchurl=urllib.urlencode(searchlist)
    if not page:
        page=1
    funpage=zz91page()
    limitNum=funpage.limitNum(10)
    nowpage=funpage.nowpage(int(page))
    frompageCount=funpage.frompageCount()
    after_range_num = funpage.after_range_num(3)
    before_range_num = funpage.before_range_num(6)
    storage_list=zzdibang.storage_list(frompageCount,limitNum,searchlist=searchlist,group_id=group_id,company_id=company_id)
    listcount=0
    listall=storage_list['list']
    listcount=storage_list['count']
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
    list={"code":0,"msg":"","count":listcount,"data":listall}
    return HttpResponse(simplejson.dumps(list, ensure_ascii=False))
#入库单添加
def storage_add(request):
    username=request.session.get('username',default=None)
    group_id=request.session.get('group_id',default=None)
    user_selfid=request.session.get('user_selfid',default=None)
    if not username:
        return HttpResponseRedirect("login.html")
    company_id=request.session.get('company_id')
    group_id=request.session.get('group_id')
    product_list=zzdibang.getproductlist()
    supplier_list=zzdibang.getsupplierlist()
    user_list=zzdibang.getuserlist()
    return render_to_response('storage_add.html',locals())
#入库单修改
def storage_mod(request):
    username=request.session.get('username',default=None)
    group_id=request.session.get('group_id',default=None)
    user_selfid=request.session.get('user_selfid',default=None)
    if not username:
        return HttpResponseRedirect("login.html")
    id=request.GET.get('id')
    sql='select company_id,code,price,gw,nw,tare,total,status,price_users_selfid,price_time,ispay,scorecheck,pay_time,pay_users_selfid from storage where id=%s'
    result=dbd.fetchonedb(sql,[id])
    result['price_time']=formattime(result['price_time'],flag=1)
    result['pay_time']=formattime(result['pay_time'],flag=1)
    user_list=zzdibang.getuserlist()
    return render_to_response('storage_mod.html',locals())
#入库单保存
def storage_save(request):
    username=request.session.get('username',default=None)
    group_id=request.session.get('group_id',default=None)
    user_selfid=request.session.get('user_selfid',default=None)
    if not username:
        return HttpResponseRedirect("login.html")
    zzdibang.storage_save(request)
    return HttpResponseRedirect("storage.html")

#入库单删除
def storage_del(request):
    username=request.session.get('username',default=None)
    group_id=request.session.get('group_id',default=None)
    user_selfid=request.session.get('user_selfid',default=None)
    if not username:
        return HttpResponseRedirect("login.html")
    id=request.POST.get('id')
    sql='delete from storage where id=%s'
    dbd.updatetodb(sql,[id])
    data={'answer':'answer'}
    return HttpResponse(simplejson.dumps(data, ensure_ascii=False))


#人员列表
def user(request):
    username=request.session.get('username',default=None)
    group_id=request.session.get('group_id',default=None)
    user_selfid=request.session.get('user_selfid',default=None)
    if not username:
        return HttpResponseRedirect("login.html")
    return render_to_response('user.html',locals())
#人员数据
def user_data(request):
    page=request.GET.get('page')
    contact=request.GET.get('contact')
    username=request.session.get('username',default=None)
    group_id=request.session.get('group_id',default=None)
    company_id=request.session.get('company_id',default=None)
    utype=request.session.get('utype',default=None)
    searchlist={}
    if contact:
        searchlist['contact']=contact
    searchurl=urllib.urlencode(searchlist)
    if not page:
        page=1
    funpage=zz91page()
    limitNum=funpage.limitNum(10)
    nowpage=funpage.nowpage(int(page))
    frompageCount=funpage.frompageCount()
    after_range_num = funpage.after_range_num(3)
    before_range_num = funpage.before_range_num(6)
    user_list=zzdibang.user_list(frompageCount,limitNum,contact=contact,company_id=company_id,group_id=group_id,utype=utype)
    listcount=0
    listall=user_list['list']
    listcount=user_list['count']
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
    list={"code":0,"msg":"","count":listcount,"data":listall}
    return HttpResponse(simplejson.dumps(list, ensure_ascii=False))
#人员添加
def user_add(request):
    username=request.session.get('username',default=None)
    group_id=request.session.get('group_id',default=None)
    company_id=request.session.get('company_id',default=None)
    user_selfid=request.session.get('user_selfid',default=None)
    utype=request.session.get('utype',default=None)
    if not username:
        return HttpResponseRedirect("login.html")
    if str(utype)=="1":
        company_list=zzdibang.getcompanylist(group_id=group_id)
    else:
        company_list=zzdibang.getcompanylist(company_id=company_id)
    return render_to_response('user_add.html',locals())
#人员修改
def user_mod(request):
    username=request.session.get('username',default=None)
    group_id=request.session.get('group_id',default=None)
    company_id=request.session.get('company_id',default=None)
    user_selfid=request.session.get('user_selfid',default=None)
    utype=request.session.get('utype',default=None)
    if not username:
        return HttpResponseRedirect("login.html")
    if str(utype)=="1":
        company_list=zzdibang.getcompanylist(group_id=group_id)
    else:
        company_list=zzdibang.getcompanylist(company_id=company_id)
    id=request.GET.get('id')
    sql='select * from users where id=%s'
    result=dbd.fetchonedb(sql,[id])
    if result:
        utype=result['utype']
        username=result['username']
        contact=result['contact']
        sex=result['sex']
        mobile=result['mobile']
        bz=result['bz']
        ucompany_id=result['company_id']
    return render_to_response('user_mod.html',locals())
#人员保存
def user_save(request):
    username=request.session.get('username',default=None)
    group_id=request.session.get('group_id',default=None)
    user_selfid=request.session.get('user_selfid',default=None)
    if not username:
        return HttpResponseRedirect("login.html")
    id=request.POST.get('id')
    utype=request.POST.get('utype')
    username=request.POST.get('username')
    mobile=request.POST.get('mobile')
    pwd=request.POST.get('pwd')
    contact=request.POST.get('contact')
    sex=request.POST.get('sex')
    bz=request.POST.get('bz')
    if id:
        sql1='select id from users where username=%s and id!=%s'
        result1=dbd.fetchonedb(sql1,[username,id])
        sql2='select id from users where mobile=%s and id!=%s'
        result2=dbd.fetchonedb(sql2,[mobile,id])
        if result1 or result2:
            if result1:
                errtext1="该用户名已被占用！"
            if result2:
                errtext2="该手机号已被占用！"
            return render_to_response('user_mod.html',locals())
    else:
        sql3='select id from users where username=%s'
        result3=dbd.fetchonedb(sql3,[username])
        sql4='select id from users where mobile=%s'
        result4=dbd.fetchonedb(sql4,[mobile])
        if result3 or result4:
            if result3:
                errtext1="该用户名已被占用！"
            if result4:
                errtext2="该手机号已被占用！"
            return render_to_response('user_add.html',locals())
    zzdibang.user_save(request)
    return HttpResponseRedirect("user.html")

#人员删除
def user_del(request):
    username=request.session.get('username',default=None)
    group_id=request.session.get('group_id',default=None)
    user_selfid=request.session.get('user_selfid',default=None)
    if not username:
        return HttpResponseRedirect("login.html")
    id=request.POST.get('id')
    sql='delete from users where id=%s'
    dbd.updatetodb(sql,[id])
    data={'answer':'answer'}
    return HttpResponse(simplejson.dumps(data, ensure_ascii=False))


#财务列表
def finance(request):
    username=request.session.get('username',default=None)
    group_id=request.session.get('group_id',default=None)
    user_selfid=request.session.get('user_selfid',default=None)
    company_id=request.session.get('company_id',default=None)
    if not username:
        return HttpResponseRedirect("login.html")
    supplier_list=zzdibang.getsupplierlist(company_id=company_id)
    company_list=zzdibang.getcompanylist(company_id=company_id)
    sql='select sum(total) as total_amount from storage where company_id=%s and ispay>=1'
    total_amount=dbd.fetchonedb(sql,[company_id])['total_amount']
    #category_list=zzdibang.getcategorylist(company_id=company_id)
    #productslist=zzdibang.getproductlist(company_id=company_id)
    return render_to_response('finance.html',locals())
#财务数据
def finance_data(request):
    username=request.session.get('username',default=None)
    group_id=request.session.get('group_id',default=None)
    company_id=request.session.get('company_id',default=None)
    page=request.GET.get('page')
    code=request.GET.get('code')
    products_selfid=request.GET.get('products_selfid')
    suppliers_selfid=request.GET.get('suppliers_selfid')
    time_min=request.GET.get('time_min')
    time_max=request.GET.get('time_max')
    proname=request.GET.get('proname')
    searchlist={}
    if code:
        searchlist['code']=code
    if products_selfid:
        searchlist['products_selfid']=products_selfid
    if suppliers_selfid:
        searchlist['suppliers_selfid']=suppliers_selfid
    if time_min:
        searchlist['time_min']=time_min
    if time_max:
        searchlist['time_max']=time_max
    if proname:
        searchlist['proname']=proname
    searchlist['ispay']=1
    searchurl=urllib.urlencode(searchlist)
    if not page:
        page=1
    funpage=zz91page()
    limitNum=funpage.limitNum(10)
    nowpage=funpage.nowpage(int(page))
    frompageCount=funpage.frompageCount()
    after_range_num = funpage.after_range_num(3)
    before_range_num = funpage.before_range_num(6)
    storage_list=zzdibang.storage_list(frompageCount,limitNum,searchlist=searchlist,group_id=group_id,company_id=company_id)
    listcount=0
    listall=storage_list['list']
    listcount=storage_list['count']
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
    list={"code":0,"msg":"","count":listcount,"data":listall}
    return HttpResponse(simplejson.dumps(list, ensure_ascii=False))


#每日账目清单列表
def finance_everyday(request):
    username=request.session.get('username',default=None)
    group_id=request.session.get('group_id',default=None)
    user_selfid=request.session.get('user_selfid',default=None)
    company_id=request.session.get('company_id',default=None)
    if not username:
        return HttpResponseRedirect("login.html")
    prolist=zzdibang.getproductlist(company_id=company_id)
    return render_to_response('finance_everyday.html',locals())
#每日账目清单数据
def finance_everyday_data(request):
    page=request.GET.get('page')
    company_id=request.GET.get('company_id')
    suppliers_selfid=request.GET.get('suppliers_selfid')
    time_min=request.GET.get('time_min')
    time_max=request.GET.get('time_max')
    searchlist={}
    if name:
        searchlist['name']=name
    searchurl=urllib.urlencode(searchlist)
    if not page:
        page=1
    funpage=zz91page()
    limitNum=funpage.limitNum(10)
    nowpage=funpage.nowpage(int(page))
    frompageCount=funpage.frompageCount()
    after_range_num = funpage.after_range_num(3)
    before_range_num = funpage.before_range_num(6)
    user_list=zzdibang.user_list(frompageCount,limitNum,name=name)
    listcount=0
    listall=user_list['list']
    listcount=user_list['count']
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
    list={"code":0,"msg":"","count":listcount,"data":listall}
    return HttpResponse(simplejson.dumps(list, ensure_ascii=False))
#----产品每日出账统计
def finance_productstotal_data(request):
    username=request.session.get('username',default=None)
    group_id=request.session.get('group_id',default=None)
    user_selfid=request.session.get('user_selfid',default=None)
    company_id=request.session.get('company_id',default=None)
    time_min=request.GET.get('time_min')
    time_max=request.GET.get('time_max')
    if not time_min or not time_max:
        datelist=getpastday(7)
    else:
        datelist=getDays(time_min,time_max)
    listcount=len(datelist)
    listall=[]
    prolist=zzdibang.getproductlist(company_id=company_id)
    for list in datelist:
        l={'datevalue':formattime(list,1)}
        for p in prolist:
            l['_'+p['selfid']]=zzdibang.getproducts_storage(p['selfid'],ndate=formattime(list,1))['total']
        listall.append(l)
    list={"code":0,"msg":"","count":listcount,"data":listall}
    return HttpResponse(simplejson.dumps(list, ensure_ascii=False))

def viewer_404(request):
    t = get_template('404.html')
    html = t.render(Context())
    return HttpResponseNotFound(html)
def viewer_500(request):
    t = get_template('404.html')
    html = t.render(Context())
    return HttpResponseNotFound(html)