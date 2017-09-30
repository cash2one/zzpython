#-*- coding:utf-8 -*-
from django.shortcuts import render_to_response
from django.http import HttpResponse,HttpResponseRedirect
from zz91page import *
from zz91db_dibang import dibangdb
from zz91settings import SPHINXCONFIG,logpath
from zz91tools import formattime,getoptionlist,date_to_strall,date_to_str,filter_tags
import time,urllib,sys,os,datetime
dbd=dibangdb(1)
reload(sys)
sys.setdefaultencoding('UTF-8')
nowpath=os.path.dirname(__file__)
execfile(nowpath+"/func/dibang_function.py")
execfile(nowpath+"/func/crmtools.py")
zzdibang=zzdibang()
#公司列表
def company_list(request):
    page=request.GET.get('page')
    name=request.GET.get('name')
    searchlist={}
    if name:
        searchlist['name']=name
    searchurl=urllib.urlencode(searchlist)
    if not page:
        page=1
    funpage=zz91page()
    limitNum=funpage.limitNum(20)
    nowpage=funpage.nowpage(int(page))
    frompageCount=funpage.frompageCount()
    after_range_num = funpage.after_range_num(3)
    before_range_num = funpage.before_range_num(6)
    company_list=zzdibang.company_list(frompageCount,limitNum,name=name)
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
    return render_to_response('dibang/company_list.html',locals())

def company_mod(request):
    id=request.GET.get('id')
    sql='select group_id,name,address,ctype from company where id=%s'
    result=dbd.fetchonedb(sql,[id])
    group_id=result['group_id']
    name=result['name']
    ctype=result['ctype']
    address=result['address']
    return render_to_response('dibang/company_mod.html',locals())
    
def company_add(request):
    group_id=request.GET.get('group_id')
    return render_to_response('dibang/company_add.html',locals())
    
def company_del(request):
    id=request.GET.get('id')
    if id:
        sql='delete from company where id=%s'
        result=dbd.updatetodb(sql,[id])
    check_box_list = request.REQUEST.getlist("check_box_list")
    if check_box_list:
        for id in check_box_list:
            sql='delete from company where id=%s'
            result=dbd.updatetodb(sql,[id])
    return HttpResponseRedirect('company_list.html',locals())
def company_save(request):
    result=zzdibang.company_save(request)
    return HttpResponseRedirect('company_list.html',locals())


#人员管理
def user_list(request):
    page=request.GET.get('page')
    name=request.GET.get('name')
    searchlist={}
    if name:
        searchlist['name']=name
    searchurl=urllib.urlencode(searchlist)
    if not page:
        page=1
    funpage=zz91page()
    limitNum=funpage.limitNum(20)
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
    return render_to_response('dibang/user_list.html',locals())

def user_mod(request):
    id=request.GET.get('id')
    sql='select group_id,company_id,clientid,utype,username,pwd,contact,sex,mobile,bz from users where id=%s'
    result=dbd.fetchonedb(sql,[id])
    group_id=result['group_id']
    company_id=result['company_id']
    clientid=result['clientid']
    utype=result['utype']
    username=result['username']
    pwd=result['pwd']
    contact=result['contact']
    sex=result['sex']
    mobile=result['mobile']
    bz=result['bz']
    return render_to_response('dibang/user_mod.html',locals())
    
def user_add(request):
    group_id=request.GET.get('group_id')
    company_id=request.GET.get('company_id')
    return render_to_response('dibang/user_add.html',locals())
    
def user_del(request):
    id=request.GET.get('id')
    if id:
        sql='delete from users where id=%s'
        result=dbd.updatetodb(sql,[id])
    check_box_list = request.REQUEST.getlist("check_box_list")
    if check_box_list:
        for id in check_box_list:
            sql='delete from users where id=%s'
            result=dbd.updatetodb(sql,[id])
    return HttpResponseRedirect('user_list.html',locals())

def user_save(request):
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
            return render_to_response('dibang/user_mod.html',locals())
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
            return render_to_response('dibang/user_add.html',locals())
    result=zzdibang.user_save(request)
    return HttpResponseRedirect('user_list.html',locals())


#入库单管理
def storage_list(request):
    page=request.GET.get('page')
    code=request.GET.get('code')
    searchlist={}
    if code:
        searchlist['code']=code
    searchurl=urllib.urlencode(searchlist)
    if not page:
        page=1
    funpage=zz91page()
    limitNum=funpage.limitNum(20)
    nowpage=funpage.nowpage(int(page))
    frompageCount=funpage.frompageCount()
    after_range_num = funpage.after_range_num(3)
    before_range_num = funpage.before_range_num(6)
    storage_list=zzdibang.storage_list(frompageCount,limitNum,code=code)
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
    return render_to_response('dibang/storage_list.html',locals())

def storage_add(request):
    product_list=zzdibang.getproductlist(request)
    supplier_list=zzdibang.getsupplierlist(request)
    user_list=zzdibang.getuserlist(request)
    group_id=request.GET.get('group_id')
    company_id=request.GET.get('company_id')
    return render_to_response('dibang/storage_add.html',locals())

def storage_mod(request):
    id=request.GET.get('id')
    sql='select selfid,group_id,company_id,code,products_selfid,suppliers_selfid,price,gw,nw,tare,total,status,price_users_selfid,price_time,ispay,scorecheck,pay_time,pay_users_selfid,gmt_created,gmt_modified from storage where id=%s'
    result=dbd.fetchonedb(sql,[id])
    selfid=result['selfid']
    group_id=result['group_id']
    company_id=result['company_id']
    code=result['code']
    products_selfid=result['products_selfid']
    suppliers_selfid=result['suppliers_selfid']
    price=result['price']
    gw=result['gw']
    nw=result['nw']
    tare=result['tare']
    total=result['total']
    status=result['status']
    price_users_selfid=result['price_users_selfid']
    out_time=result['price_time']
    out_time=formattime(out_time,flag=1)
    ispay=result['ispay']
    scorecheck=result['scorecheck']
    pay_time=result['pay_time']
    pay_time=formattime(pay_time,flag=1)
    pay_users_selfid=result['pay_users_selfid']
    gmt_created=result['gmt_created']
    gmt_created=formattime(gmt_created,flag=2)
    gmt_modified=result['gmt_modified']
    user_list=zzdibang.getuserlist(request)
    product_list=zzdibang.getproductlist(request)
    supplier_list=zzdibang.getsupplierlist(request)
    return render_to_response('dibang/storage_mod.html',locals())

def storage_del(request):
    id=request.GET.get('id')
    if id:
        sql='delete from storage where id=%s'
        result=dbd.updatetodb(sql,[id])
    check_box_list = request.REQUEST.getlist("check_box_list")
    if check_box_list:
        for id in check_box_list:
            sql='delete from storage where id=%s'
            result=dbd.updatetodb(sql,[id])
    return HttpResponseRedirect('storage_list.html',locals())

def storage_save(request):
    result=zzdibang.storage_save(request)
    return HttpResponseRedirect('storage_list.html',locals())


#集团管理
def group_list(request):
    page=request.GET.get('page')
    name=request.GET.get('name')
    searchlist={}
    if name:
        searchlist['name']=name
    searchurl=urllib.urlencode(searchlist)
    if not page:
        page=1
    funpage=zz91page()
    limitNum=funpage.limitNum(20)
    nowpage=funpage.nowpage(int(page))
    frompageCount=funpage.frompageCount()
    after_range_num = funpage.after_range_num(3)
    before_range_num = funpage.before_range_num(6)
    group_list=zzdibang.group_list(frompageCount,limitNum,name=name)
    listcount=0
    listall=group_list['list']
    listcount=group_list['count']
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
    return render_to_response('dibang/group_list.html',locals())

def group_add(request):
    return render_to_response('dibang/group_add.html',locals())

def group_mod(request):
    id=request.GET.get('id')
    sql='select name,address,ctype from grouplist where id=%s'
    result=dbd.fetchonedb(sql,[id])
    name=result['name']
    address=result['address']
    ctype=result['ctype']
    return render_to_response('dibang/group_mod.html',locals())

def group_del(request):
    id=request.GET.get('id')
    if id:
        sql='delete from grouplist where id=%s'
        result=dbd.updatetodb(sql,[id])
    check_box_list = request.REQUEST.getlist("check_box_list")
    if check_box_list:
        for id in check_box_list:
            sql='delete from grouplist where id=%s'
            result=dbd.updatetodb(sql,[id])
    return HttpResponseRedirect('group_list.html',locals())

def group_save(request):
    result=zzdibang.group_save(request)
    return HttpResponseRedirect('group_list.html',locals())


#供应商管理
def supplier_list(request):
    page=request.GET.get('page')
    name=request.GET.get('name')
    searchlist={}
    if name:
        searchlist['name']=name
    searchurl=urllib.urlencode(searchlist)
    if not page:
        page=1
    funpage=zz91page()
    limitNum=funpage.limitNum(20)
    nowpage=funpage.nowpage(int(page))
    frompageCount=funpage.frompageCount()
    after_range_num = funpage.after_range_num(3)
    before_range_num = funpage.before_range_num(6)
    supplier_list=zzdibang.supplier_list(frompageCount,limitNum,name=name)
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
    return render_to_response('dibang/supplier_list.html',locals())

def supplier_add(request):
    group_id=request.GET.get('group_id')
    company_id=request.GET.get('company_id')
    return render_to_response('dibang/supplier_add.html',locals())

def supplier_mod(request):
    id=request.GET.get('id')
    sql='select ctype,group_id,company_id,iccode,name,htype,contact,mobile,pwd,address,bz from suppliers where id=%s'
    result=dbd.fetchonedb(sql,[id])
    ctype=result['ctype']
    group_id=result['group_id']
    company_id=result['company_id']
    iccode=result['iccode']
    name=result['name']
    htype=result['htype']
    contact=result['contact']
    mobile=result['mobile']
    pwd=result['pwd']
    address=result['address']
    bz=result['bz']
    return render_to_response('dibang/supplier_mod.html',locals())

def supplier_del(request):
    id=request.GET.get('id')
    if id:
        sql='delete from suppliers where id=%s'
        result=dbd.updatetodb(sql,[id])
    check_box_list = request.REQUEST.getlist("check_box_list")
    if check_box_list:
        for id in check_box_list:
            sql='delete from suppliers where id=%s'
            result=dbd.updatetodb(sql,[id])
    return HttpResponseRedirect('supplier_list.html',locals())

def supplier_save(request):
    result=zzdibang.supplier_save(request)
    return HttpResponseRedirect('supplier_list.html',locals())


#产品信息管理
def product_list(request):
    page=request.GET.get('page')
    name=request.GET.get('name')
    searchlist={}
    if name:
        searchlist['name']=name
    searchurl=urllib.urlencode(searchlist)
    if not page:
        page=1
    funpage=zz91page()
    limitNum=funpage.limitNum(20)
    nowpage=funpage.nowpage(int(page))
    frompageCount=funpage.frompageCount()
    after_range_num = funpage.after_range_num(3)
    before_range_num = funpage.before_range_num(6)
    supplier_list=zzdibang.product_list(frompageCount,limitNum,name=name)
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
    return render_to_response('dibang/product_list.html',locals())

def product_add(request):
    company_id=request.GET.get('company_id')
    category_selfid=request.GET.get('category_selfid')
    category_list=zzdibang.getcategorylist(request)
    return render_to_response('dibang/product_add.html',locals())

def product_mod(request):
    id=request.GET.get('id')
    sql='select group_id,company_id,name,name_py,category_selfid,spec,unit,stock,bz from products where id=%s'
    result=dbd.fetchonedb(sql,[id])
    group_id=result['group_id']
    company_id=result['company_id']
    name=result['name']
    name_py=result['name_py']
    category_selfid=result['category_selfid']
    spec=result['spec']
    unit=result['unit']
    stock=result['stock']
    bz=result['bz']
    category_list=zzdibang.getcategorylist(request)
    return render_to_response('dibang/product_mod.html',locals())

def product_del(request):
    id=request.GET.get('id')
    if id:
        sql='delete from products where id=%s'
        result=dbd.updatetodb(sql,[id])
    check_box_list = request.REQUEST.getlist("check_box_list")
    if check_box_list:
        for id in check_box_list:
            sql='delete from products where id=%s'
            result=dbd.updatetodb(sql,[id])
    return HttpResponseRedirect('product_list.html',locals())

def product_save(request):
    result=zzdibang.product_save(request)
    return HttpResponseRedirect('product_list.html',locals())


#废品类别管理
def category_list(request):
    page=request.GET.get('page')
    name=request.GET.get('name')
    sub_selfid=request.GET.get("sub_selfid")
    searchlist={}
    if name:
        searchlist['name']=name
    if sub_selfid:
        searchlist['sub_selfid']=sub_selfid
    else:
        searchlist['sub_selfid']="0"
    searchurl=urllib.urlencode(searchlist)
    if not page:
        page=1
    funpage=zz91page()
    limitNum=funpage.limitNum(20)
    nowpage=funpage.nowpage(int(page))
    frompageCount=funpage.frompageCount()
    after_range_num = funpage.after_range_num(3)
    before_range_num = funpage.before_range_num(6)
    category_list=zzdibang.category_list(frompageCount,limitNum,searchlist=searchlist)
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
    return render_to_response('dibang/category_list.html',locals())

def category_add(request):
    sub_selfid=request.GET.get('sub_selfid')
    company_id=request.GET.get('company_id')
    group_id=request.GET.get('group_id')
    return render_to_response('dibang/category_add.html',locals())

def category_mod(request):
    id=request.GET.get('id')
    sql='select name from category_products where id=%s'
    result=dbd.fetchonedb(sql,[id])
    name=result['name']
    return render_to_response('dibang/category_mod.html',locals())

def category_del(request):
    id=request.GET.get('id')
    if id:
        sql='delete from category_products where id=%s'
        result=dbd.updatetodb(sql,[id])
    check_box_list = request.REQUEST.getlist("check_box_list")
    if check_box_list:
        for id in check_box_list:
            sql='delete from category_products where id=%s'
            result=dbd.updatetodb(sql,[id])
    return HttpResponseRedirect('category_list.html',locals())

def category_save(request):
    result=zzdibang.category_save(request)
    return HttpResponseRedirect('category_list.html',locals())