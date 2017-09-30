#-*- coding:utf-8 -*-
import MySQLdb,settings,codecs,os,sys,datetime,time,random,requests,hashlib,md5,simplejson,urllib
from django.shortcuts import render_to_response
from django.http import HttpResponse,HttpResponseRedirect,HttpResponseForbidden,HttpResponseNotFound,HttpResponsePermanentRedirect
from datetime import timedelta, date 
from dict2xml import dict2xml
from django.core.cache import cache
from zz91db_dibang import dibangdb
from zz91tools import formattime,int_to_strall
dbd=dibangdb(1)
from zz91page import *
reload(sys) 
sys.setdefaultencoding('utf-8') 
nowpath=os.path.dirname(__file__)
execfile(nowpath+"/func/dibang_function.py")
execfile(nowpath+"/func/crmtools.py")
zzdibang=zzdibang()

#登录
def login(request):
    username=request.session.get('username',default='')
    company_id=request.session.get('company_id',default=None)
    if username:
        return HttpResponseRedirect("index.html")
    if not username:
        username=''
        return render_to_response('mobile/login.html',locals())
    
#登录检查
def logincheck(request):
    username=request.POST.get('username')
    password=passwd=request.POST.get('password')
    if passwd:
        md5pwd = hashlib.md5(passwd)
        md5pwd = md5pwd.hexdigest()[8:-8]
    
    if username and password:
        openid_fw=request.session.get("openid_fw")
        sql='select id,group_id,selfid,company_id,utype from users where username=%s and pwd=%s and isdel=0'
        result=dbd.fetchonedb(sql,[username,md5pwd])
        if result:
            user_id=result['id']
            group_id=result['group_id']
            user_selfid=result['selfid']
            company_id=result['company_id']
            utype=result['utype']
            request.session.set_expiry(6000*60000)
            request.session['user_id']=user_id
            request.session['username']=username
            request.session['group_id']=group_id
            request.session['user_selfid']=user_selfid
            request.session['company_id']=company_id
            request.session['utype']=utype
            
            sql="update users set weixinid=%s where id=%s"
            dbd.updatetodb(sql,[openid_fw,user_id])
            return HttpResponseRedirect('index.html')
        else:
            errtext="用户名或密码错误"
            return render_to_response('mobile/login.html',locals())
    else:
        errtext="请输入用户名或密码"
        return render_to_response('mobile/login.html',locals())
#首页
def index(request):
    username=request.session.get('username',default=None)
    user_id=request.session.get('user_id',default=None)
    group_id=request.session.get('group_id',default=None)
    company_id=request.session.get('company_id',default=None)
    utype=request.session.get('utype',default=None)
    user_selfid=request.session.get('user_selfid',default=None)
    if not username:
        return HttpResponseRedirect('login.html')
    isadmin=zzdibang.isadmin(utype)
    sql='select count(0) as count from storage where company_id=%s and status not in (2,4)'
    count=dbd.fetchonedb(sql,[company_id])['count']
    return render_to_response('mobile/index.html',locals())
    
#登出
def logout(request):
    try:
        request.session.delete()
        del request.session['username']
        del request.session['user_id']
        del request.session['group_id']
        del request.session['user_selfid']
        del request.session['company_id']
        del request.session['utype']
        
    except KeyError:
        pass
    return HttpResponseRedirect("login.html")
#待定价榜单
def pricing(request):
    username=request.session.get('username',default=None)
    company_id=request.session.get('company_id',default=None)
    group_id=request.session.get('group_id',default=None)
    if not username:
        return HttpResponseRedirect("login.html")
    page=request.GET.get('page')
    code=request.POST.get('code')
    iccode=request.POST.get('iccode')
    pricing=request.GET.get('pricing')
    searchlist={}
    if code:
        searchlist['code']=code
    if iccode:
        searchlist['iccode']=iccode
    if pricing:
        searchlist['pricing']=pricing
    searchurl=urllib.urlencode(searchlist)
    if not page:
        page=1
    funpage=zz91page()
    limitNum=funpage.limitNum(10)
    nowpage=funpage.nowpage(int(page))
    frompageCount=funpage.frompageCount()
    after_range_num = funpage.after_range_num(3)
    before_range_num = funpage.before_range_num(6)
    storage_list=zzdibang.storage_list(frompageCount,limitNum,searchlist=searchlist,company_id=company_id,group_id=group_id)
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
    category_list=zzdibang.getcategorylist(company_id=company_id)
    #productslist=zzdibang.getproductlist(company_id=company_id)
    return render_to_response('mobile/pricing.html',locals())
#今日已定价
def pricing_today(request):
    username=request.session.get('username',default=None)
    company_id=request.session.get('company_id',default=None)
    group_id=request.session.get('group_id',default=None)
    if not username:
        return HttpResponseRedirect("login.html")
    page=request.GET.get('page')
    code=request.POST.get('code')
    iccode=request.POST.get('iccode')
    pricing_today=request.GET.get('pricing_today')
    jiesuan=request.GET.get('jiesuan')
    searchlist={}
    if code:
        searchlist['code']=code
    if iccode:
        searchlist['iccode']=iccode
    if pricing_today:
        searchlist['pricing_today']=pricing_today
    if jiesuan:
        searchlist['jiesuan']=jiesuan
    searchurl=urllib.urlencode(searchlist)
    if not page:
        page=1
    funpage=zz91page()
    limitNum=funpage.limitNum(10)
    nowpage=funpage.nowpage(int(page))
    frompageCount=funpage.frompageCount()
    after_range_num = funpage.after_range_num(3)
    before_range_num = funpage.before_range_num(6)
    storage_list=zzdibang.storage_list(frompageCount,limitNum,searchlist=searchlist,company_id=company_id,group_id=group_id)
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
    return render_to_response('mobile/pricing_today.html',locals())
#立即定价
def pricing_now_save(request):
    username=request.session.get('username',default=None)
    company_id=request.session.get('company_id',default=None)
    user_selfid=request.session.get('user_selfid',default=None)
    if not username:
        return HttpResponseRedirect("login.html")
    id=request.POST.get("id")
    category_selfid=request.POST.get("category_selfid")
    products_selfid=request.POST.get("products_selfid")
    price=request.POST.get("price")
    gmt_created=gmt_modified=datetime.datetime.now()
    if id:
        sql="update storage set products_selfid=%s,price=%s,price_users_selfid=%s,price_time=%s,gmt_modified=%s,status=2 where id=%s"
        dbd.updatetodb(sql,[products_selfid,price,user_selfid,gmt_created,gmt_modified,id])
    page=request.POST.get('page')
    return HttpResponseRedirect('pricing.html?pricing=1&t='+str(gmt_created))
#供应商列表
def supplier(request):
    username=request.session.get('username',default=None)
    company_id=request.session.get('company_id',default=None)
    group_id=request.session.get('group_id',default=None)
    if not username:
        return HttpResponseRedirect("login.html")
    page=request.GET.get('page')
    iccode=request.POST.get('iccode')
    searchlist={}
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
    supplier_list=zzdibang.supplier_list(frompageCount,limitNum,searchlist=searchlist,company_id=company_id)
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
    return render_to_response('mobile/supplier.html',locals())
#添加供货商
def supplier_add(request):
    request_url=request.META.get('HTTP_REFERER','/')
    username=request.session.get('username',default=None)
    company_id=request.session.get('company_id',default=None)
    if not username or not company_id:
        return HttpResponseRedirect("login.html")
    company_id=request.session.get('company_id',default=None)
    group_id=request.session.get('group_id',default=None)
    return render_to_response('mobile/supplier_add.html',locals())
#供货商修改
def supplier_mod(request):
    request_url=request.META.get('HTTP_REFERER','/')
    username=request.session.get('username',default=None)
    company_id=request.session.get('company_id',default=None)
    if not username:
        return HttpResponseRedirect("login.html")
    id=request.GET.get('id')
    sql='select iccode,contact,mobile,address,bz,name from suppliers where id=%s'
    result=dbd.fetchonedb(sql,[id])
    iccode=result['iccode']
    contact=result['contact']
    mobile=result['mobile']
    address=result['address']
    name=result['name']
    bz=result['bz']
    return render_to_response('mobile/supplier_mod.html',locals())
#供货商保存
def supplier_save(request):
    relist={'err':'false','errtext':''}
    username=request.session.get('username',default=None)
    if not username:
        return HttpResponseRedirect("login.html")
    id=request.POST.get('id')
    iccode=request.POST.get('iccode')
    mobile=request.POST.get('mobile')
    contact=request.POST.get('contact')
    address=request.POST.get('address')
    name=request.POST.get('name')
    bz=request.POST.get('bz')
    request_url=request.POST.get('request_url')
    if id:
        sql='select id from suppliers where iccode=%s and id!=%s'
        result=dbd.fetchonedb(sql,[iccode,id])
        if result:
            errtext="该供应商编号已被占用！"
            relist['err']='true'
            relist['errtext']=errtext
        sql="update suppliers set iccode=%s,name=%s,mobile=%s,address=%s,contact=%s,bz=%s where id=%s"
        dbd.updatetodb(sql,[iccode,name,mobile,address,contact,bz,id])
    elif not id:
        sql='select id from suppliers where iccode=%s'
        result=dbd.fetchonedb(sql,[iccode])
        if result:
            errtext="该供应商编号已被占用！"
            relist['err']='true'
            relist['errtext']=errtext
        zzdibang.supplier_save(request)
    return HttpResponse(simplejson.dumps(relist, ensure_ascii=False))
#数据汇总
def alldata(request):
    username=request.session.get('username',default=None)
    company_id=request.session.get('company_id',default=None)
    if not username:
        return HttpResponseRedirect("login.html")
    time_min=request.POST.get('time_min')
    time_max=request.POST.get('time_max')
    result=zzdibang.alldata(request,time_min=time_min,time_max=time_max,company_id=company_id)
    total_weight=result['total_weight']
    if not total_weight:
        total_weight=''
    total_price=result['total_price']
    if not total_price:
        total_price=''
    listall=result['listall']
    list={"total_weight":total_weight,"total_price":total_price,"listall":listall}
    return render_to_response('mobile/alldata.html',locals())
#入库明细
def storage(request):
    username=request.session.get('username',default=None)
    company_id=request.session.get('company_id',default=None)
    group_id=request.session.get('group_id',default=None)
    if not username:
        return HttpResponseRedirect("login.html")
    page=request.GET.get('page')
    searchtype=request.GET.get('searchtype')
    if not searchtype:
        searchtype='iccode'
    iccode=request.GET.get('iccode')
    ucompany_id=request.GET.get('ucompany_id')
    nw=request.GET.get('nw')
    suppliers_selfid=request.GET.get('suppliers_selfid')
    gw=request.GET.get('gw')
    gmt_created=request.GET.get('gmt_created')
    price=request.GET.get('price')
    searchlist={}
    if iccode:
        searchlist['iccode']=iccode
    if ucompany_id:
        searchlist['ucompany_id']=ucompany_id
    if nw:
        searchlist['nw']=nw
    if suppliers_selfid:
        searchlist['suppliers_selfid']=suppliers_selfid
    if gw:
        searchlist['gw']=gw
    if gmt_created:
        searchlist['gmt_created']=gmt_created
    if price:
        searchlist['price']=price
    if searchtype:
        searchlist['searchtype']=searchtype
    searchurl=urllib.urlencode(searchlist)
    if not page:
        page=1
    funpage=zz91page()
    limitNum=funpage.limitNum(10)
    nowpage=funpage.nowpage(int(page))
    frompageCount=funpage.frompageCount()
    after_range_num = funpage.after_range_num(3)
    before_range_num = funpage.before_range_num(6)
    storage_list=zzdibang.storage_list(frompageCount,limitNum,searchlist=searchlist,company_id=company_id,group_id=group_id)
    listcount=0
    listall=storage_list['list']
    listcount=storage_list['count']
    total_price=storage_list['total_price']
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
    
    supplier_list=zzdibang.getsupplierlist(company_id=company_id)
    company_list=zzdibang.getcompanylist(company_id=company_id)
    productslist=zzdibang.getproductlist(company_id=company_id)
    
    return render_to_response('mobile/storage.html',locals())
#分站管理
def company(request):
    username=request.session.get('username',default=None)
    group_id=request.session.get('group_id',default=None)
    utype=request.session.get('utype',default=None)
    company_id=request.session.get('company_id',default=None)
    if not username:
        return HttpResponseRedirect("login.html")
    if str(utype)=="1":
        a=1
    else:
        return HttpResponse("你没有权限操作")
    name=request.GET.get('name')
    page=request.GET.get('page')
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
    return render_to_response('mobile/company.html',locals())
#添加分站
def company_add(request):
    request_url=request.META.get('HTTP_REFERER','/')
    username=request.session.get('username',default=None)
    if not username:
        return HttpResponseRedirect("login.html")
    group_id=request.session.get('group_id',default=None)
    return render_to_response('mobile/company_add.html',locals())
#修改分站
def company_mod(request):
    request_url=request.META.get('HTTP_REFERER','/')
    username=request.session.get('username',default=None)
    if not username:
        return HttpResponseRedirect("login.html")
    id=request.GET.get('id')
    sql="select name,ctype,address from company where id=%s"
    result=dbd.fetchonedb(sql,[id])
    
    return render_to_response('mobile/company_mod.html',locals())
#保存分站
def company_save(request):
    username=request.session.get('username',default=None)
    company_id=request.session.get('company_id',default=None)
    group_id=request.session.get('group_id',default=None)
    if not username:
        return HttpResponseRedirect("login.html")
    gmt_created=gmt_modified=datetime.datetime.now()
    id=request.POST.get("id")
    name=request.POST.get("name")
    ctype=request.POST.get("ctype")
    address=request.POST.get("address")
    request_url=request.POST.get("request_url")
    if id:
        sql="update company set name=%s,ctype=%s,address=%s,gmt_modified=%s where id=%s"
        dbd.updatetodb(sql,[name,ctype,address,gmt_modified,id])
    else:
        sql='insert into company(group_id,name,ctype,address,gmt_created) values(%s,%s,%s,%s,%s)'
        dbd.updatetodb(sql,[group_id,name,ctype,address,gmt_created])
    return HttpResponseRedirect(request_url)
#产品类别
def category(request):
    username=request.session.get('username',default=None)
    company_id=request.session.get('company_id',default=None)
    group_id=request.session.get('group_id',default=None)
    if not username:
        return HttpResponseRedirect("login.html")
    name=request.POST.get('name')
    page=request.GET.get('page')
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
    return render_to_response('mobile/category.html',locals())
#添加类别
def category_add(request):
    request_url=request.META.get('HTTP_REFERER','/')
    username=request.session.get('username',default=None)
    if not username:
        return HttpResponseRedirect("login.html")
    company_id=request.session.get('company_id')
    return render_to_response('mobile/category_add.html')
#修改类别
def category_mod(request):
    request_url=request.META.get('HTTP_REFERER','/')
    username=request.session.get('username',default=None)
    if not username:
        return HttpResponseRedirect("login.html")
    id=request.POST.get('id')
    name=request.POST.get('name')
    return render_to_response('mobile/category_mod.html',locals())
def category_del(request):
    username=request.session.get('username',default=None)
    company_id=request.session.get('company_id',default=None)
    group_id=request.session.get('group_id',default=None)
    if not username:
        return HttpResponseRedirect("login.html")
    request_url=request.GET.get('request_url')
    id=request.GET.get('id')
    if not request_url:
        request_url="category.html"
    if id:
        sql="update category_products set isdel=1 where id=%s and company_id=%s"
        dbd.updatetodb(sql,[id,company_id])
    return HttpResponseRedirect(request_url)
    
#保存类别
def category_save(request):
    username=request.session.get('username',default=None)
    company_id=request.session.get('company_id',default=None)
    group_id=request.session.get('group_id',default=None)
    if not username:
        return HttpResponseRedirect("login.html")
    id=request.POST.get('id')
    sub_selfid=request.POST.get('sub_selfid')
    if not sub_selfid:
        sub_selfid=0
    request_url=request.POST.get('request_url')
    name=request.POST.get('name')
    gmt_created=datetime.datetime.now()
    gmt_modified=datetime.datetime.now()
    if id:
        sql='update category_products set name=%s,gmt_modified=%s where id=%s'
        result=dbd.updatetodb(sql,[name,gmt_modified,id])
    else:
        selfid=str(time.time())+str(company_id)+str(random.randint(100, 999))
        md5selfid = hashlib.md5(selfid)
        selfid = md5selfid.hexdigest()[8:-8]
        sql='insert into category_products(selfid,sub_selfid,company_id,name,gmt_created) values(%s,%s,%s,%s,%s)'
        result=dbd.updatetodb(sql,[selfid,sub_selfid,company_id,name,gmt_created])
    if not request_url:
        request_url="category.html"
    return HttpResponseRedirect(request_url)
#产品列表
def product(request):
    username=request.session.get('username',default=None)
    company_id=request.session.get('company_id',default=None)
    group_id=request.session.get('group_id',default=None)
    if not username:
        return HttpResponseRedirect("login.html")
    name=request.POST.get('name')
    page=request.GET.get('page')
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
    product_list=zzdibang.product_list(frompageCount,limitNum,name=name,category_selfid='',company_id=company_id,group_id=group_id)
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
    return render_to_response('mobile/product.html',locals())
#添加产品
def product_add(request):
    request_url=request.META.get('HTTP_REFERER','/')
    username=request.session.get('username',default=None)
    if not username:
        return HttpResponseRedirect("login.html")
    group_id=request.session.get('group_id',default=None)
    company_id=request.session.get('company_id',default=None)
    category_list=zzdibang.getcategorylist(company_id=company_id)
    return render_to_response('mobile/product_add.html',locals())
#修改产品
def product_mod(request):
    request_url=request.META.get('HTTP_REFERER','/')
    username=request.session.get('username',default=None)
    company_id=request.session.get('company_id',default=None)
    if not username:
        return HttpResponseRedirect("login.html")
    id=request.GET.get('id')
    if id:
        sql="select * from products where id=%s"
        result=dbd.fetchonedb(sql,[id])
    category_list=zzdibang.getcategorylist(company_id=company_id)
    return render_to_response('mobile/product_mod.html',locals())
    
#保存产品
def product_save(request):
    company_id=request.session.get('company_id',default=None)
    group_id=request.session.get('group_id',default=None)
    username=request.session.get('username',default=None)
    if not username:
        return HttpResponseRedirect("login.html")
    
    id=request.POST.get('id')
    request_url=request.POST.get("request_url")
    selfid=str(time.time())+str(company_id)+str(random.randint(100, 999))
    md5selfid = hashlib.md5(selfid)
    selfid = md5selfid.hexdigest()[8:-8]
    name=request.POST.get('name')
    name_py=request.POST.get('name_py')
    category_selfid=request.POST.get('category_selfid')
    spec=request.POST.get('spec')
    unit=request.POST.get('unit')
    stock=request.POST.get('stock')
    bz=request.POST.get('bz')
    gmt_created=datetime.datetime.now()
    gmt_modified=datetime.datetime.now()
    if not id:
        sql='insert into products(selfid,group_id,company_id,name,name_py,category_selfid,spec,unit,bz,gmt_created,gmt_modified) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
        result=dbd.updatetodb(sql,[selfid,group_id,company_id,name,name_py,category_selfid,spec,unit,bz,gmt_created,gmt_modified])
    else:
        sql="update products set name=%s,name_py=%s,category_selfid=%s,spec=%s,unit=%s,bz=%s,gmt_modified=%s where id=%s"
        dbd.updatetodb(sql,[name,name_py,category_selfid,spec,unit,bz,gmt_modified,id])
    if not request_url:
        request_url='product.html'
    return HttpResponseRedirect(request_url)
def product_del(request):
    username=request.session.get('username',default=None)
    company_id=request.session.get('company_id',default=None)
    group_id=request.session.get('group_id',default=None)
    if not username:
        return HttpResponseRedirect("login.html")
    request_url=request.GET.get('request_url')
    id=request.GET.get('id')
    if not request_url:
        request_url="product.html"
    if id:
        sql="update products set isdel=1 where id=%s and company_id=%s"
        dbd.updatetodb(sql,[id,company_id])
    return HttpResponseRedirect(request_url)
#人员列表
def user(request):
    username=request.session.get('username',default=None)
    company_id=request.session.get('company_id',default=None)
    group_id=request.session.get('group_id',default=None)
    if not username:
        return HttpResponseRedirect("login.html")
    contact=request.POST.get('contact')
    page=request.GET.get('page')
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
    user_list=zzdibang.user_list(frompageCount,limitNum,contact=contact,company_id=company_id,group_id=group_id)
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
    return render_to_response('mobile/user.html', locals())
#添加人员
def user_add(request):
    request_url=request.META.get('HTTP_REFERER','/')
    username=request.session.get('username',default=None)
    company_id=request.session.get('company_id',default=None)
    group_id=request.session.get('group_id',default=None)
    user_selfid=request.session.get('user_selfid',default=None)
    myutype=request.session.get('utype',default=None)
    if not username:
        return HttpResponseRedirect("login.html")
    if str(myutype)=="1":
        company_list=zzdibang.getcompanylist(group_id=group_id)
    else:
        company_list=zzdibang.getcompanylist(company_id=company_id)
    return render_to_response('mobile/user_add.html',locals())
#修改人员
def user_mod(request):
    request_url=request.META.get('HTTP_REFERER','/')
    username=request.session.get('username',default=None)
    company_id=request.session.get('company_id',default=None)
    group_id=request.session.get('group_id',default=None)
    user_selfid=request.session.get('user_selfid',default=None)
    myutype=request.session.get('utype',default=None)
    if not username:
        return HttpResponseRedirect("login.html")
    if str(myutype)=="1":
        company_list=zzdibang.getcompanylist(group_id=group_id)
    else:
        company_list=zzdibang.getcompanylist(company_id=company_id)
    id=request.GET.get('id')
    if id:
        sql='select * from users where id=%s'
        result=dbd.fetchonedb(sql,[id])
        utype=result['utype']
        ucompany_id=result['company_id']
        username=result['username']
        contact=result['contact']
        sex=result['sex']
        mobile=result['mobile']
        bz=result['bz']
    return render_to_response('mobile/user_mod.html',locals())
    
#保存人员
def user_save(request):
    username=request.session.get('username',default=None)
    company_id=request.session.get('company_id',default=None)
    group_id=request.session.get('group_id',default=None)
    user_selfid=request.session.get('user_selfid',default=None)
    if not username:
        return HttpResponseRedirect("login.html")
    id=request.POST.get('id')
    request_url=request.POST.get("request_url")
    selfid=str(time.time())+str(company_id)+str(random.randint(100, 999))
    md5selfid = hashlib.md5(selfid)
    selfid = md5selfid.hexdigest()[8:-8]
    utype=request.POST.get('utype')
    username=request.POST.get('username')
    if str(group_id)=="1":
        company_id=request.POST.get('company_id')
    mobile=request.POST.get('mobile')
    pwd=request.POST.get('pwd')
    if pwd:
        md5pwd = hashlib.md5(pwd)
        pwd = md5pwd.hexdigest()[8:-8]
    ischange_pwd=request.POST.get('ischange_pwd')
    contact=request.POST.get('contact')
    sex=request.POST.get('sex')
    bz=request.POST.get('bz')
    gmt_created=datetime.datetime.now()
    gmt_modified=datetime.datetime.now()
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
            return render_to_response('mobile/user_mod.html',locals())
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
            return render_to_response('mobile/user_add.html',locals())
    if not id:
        sql='insert into users(selfid,group_id,company_id,utype,username,pwd,contact,sex,mobile,bz,gmt_created,gmt_modified) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
        result=dbd.updatetodb(sql,[selfid,group_id,company_id,utype,username,pwd,contact,sex,mobile,bz,gmt_created,gmt_modified])
    else:
        argument=[company_id,utype,username,contact,sex,mobile,bz,gmt_modified]
        sql="update users set company_id=%s , utype=%s , username=%s , contact=%s , sex=%s , mobile=%s , bz=%s , gmt_modified=%s"
        if ischange_pwd:
            sql+=" , pwd=%s"
            argument.append(pwd)
        sql+=" where id=%s"
        argument.append(id)
        dbd.updatetodb(sql,argument)
            
        
    if not request_url:
        request_url="user.html"
    return HttpResponseRedirect(request_url)
def user_del(request):
    username=request.session.get('username',default=None)
    user_id=request.session.get('user_id',default=None)
    company_id=request.session.get('company_id',default=None)
    group_id=request.session.get('group_id',default=None)
    request_url=request.GET.get('request_url')
    if not username:
        return HttpResponseRedirect("login.html")
    id=request.GET.get('id')
    if str(group_id)=="1":
        sql="update users set isdel=1 where id=%s and group_id=%s"
        dbd.updatetodb(sql,[id,group_id])
    else:
        sql="update users set isdel=1 where id=%s and company_id=%s"
        dbd.updatetodb(sql,[id,company_id])
    if not request_url:
        request_url='user.html'
    return HttpResponseRedirect(request_url)
    
#个人信息
def myinfo(request):
    username=request.session.get('username',default=None)
    user_id=request.session.get('user_id',default=None)
    if not username:
        return HttpResponseRedirect("login.html")
    id=request.GET.get('id')
    sql='select pwd,contact,sex,mobile from users where id=%s'
    result=dbd.fetchonedb(sql,[user_id])
    pwd=result['pwd']
    contact=result['contact']
    sex=result['sex']
    mobile=result['mobile']
    return render_to_response('mobile/myinfo.html',locals())
#个人信息保存
def myinfo_save(request):
    username=request.session.get('username',default=None)
    company_id=request.session.get('company_id',default=None)
    user_id=request.session.get('user_id',default=None)
    group_id=request.session.get('group_id',default=None)
    user_selfid=request.session.get('user_selfid',default=None)
    if not username:
        return HttpResponseRedirect("login.html")
    request_url=request.POST.get("request_url")

    mobile=request.POST.get('mobile')
    pwd=request.POST.get('pwd')
    ischange_pwd=request.POST.get('ischange_pwd')
    if pwd and ischange_pwd:
        md5pwd = hashlib.md5(pwd)
        pwd = md5pwd.hexdigest()[8:-8]
    
    contact=request.POST.get('contact')
    sex=request.POST.get('sex')
    gmt_modified=datetime.datetime.now()
    sql='select id from users where mobile=%s and id!=%s'
    result=dbd.fetchonedb(sql,[mobile,user_id])
    if result:
        errtext="该手机号已被占用！"
        return render_to_response('mobile/myinfo.html',locals())
    
    argument=[contact,sex,mobile,gmt_modified]
    sql="update users set contact=%s, sex=%s , mobile=%s , gmt_modified=%s"
    if ischange_pwd:
        sql+=" , pwd=%s"
        argument.append(pwd)
    sql+=" where id=%s"
    argument.append(user_id)
    dbd.updatetodb(sql,argument)
    return HttpResponseRedirect("index.html")
#自动获取供应商编码
def get_iccode(request):
    iccode=time.strftime("%Y-%m-%d %X", time.localtime())
    iccode=iccode.replace('-','').replace(':','').replace(' ','')
    list={'iccode':iccode}
    return HttpResponse(simplejson.dumps(list, ensure_ascii=False))
