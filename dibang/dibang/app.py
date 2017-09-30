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

def logincheck(request):
    username = request.POST.get('username')
    passwd = request.POST.get('pwd')
    passwdjm = request.POST.get('passwdjm')
    clientid = request.POST.get('clientid')
    if passwd:
        md5pwd = hashlib.md5(passwd)
        md5pwd = md5pwd.hexdigest()[8:-8]
    else:
        if passwdjm:
            md5pwd=passwdjm[8:-8]
    if not username or not passwdjm:
        list={'err':'true','errtext':'用户名或密码错误','result':''}
    else:
        gmt_created=datetime.datetime.now()
        gmt_modified=datetime.datetime.now()
        token = hashlib.md5(str(passwd)+str(username)+str(gmt_modified))
        token = token.hexdigest()[8:-8]
        
        sql="select * from users where username=%s and pwd=%s and isdel=0"
        result=dbd.fetchonedb(sql,[username,md5pwd])
        if result:
            result['gmt_created']=formattime(result['gmt_created'])
            result['gmt_modified']=formattime(result['gmt_modified'])
            if not result["selfid"]:
                selfid=token
                sql="update users set selfid=%s where id=%s"
                dbd.updatetodb(sql,[selfid,result['id']])
            sql="update users set clientid=%s where id=%s"
            dbd.updatetodb(sql,[clientid,result['id']])
            company_id=result['company_id']
            group_id=result['group_id']
            list={'err':'false','token':token,'memberID':company_id,'md5pwd':md5pwd,'username':username,'group_id':group_id}
        else:
            list={'err':'true','errtext':'用户名或密码错误','result':''}
    return HttpResponse(simplejson.dumps(list, ensure_ascii=False))
#主界面气泡num
def get_num(request):
    company_id=request.POST.get('company_id')
    sql='select count(0) as count from storage where company_id=%s'
    count=dbd.fetchonedb(sql,[company_id])['count']
    list={'count':count}
    return HttpResponse(simplejson.dumps(list, ensure_ascii=False))
#待定价榜单
def pricing(request):
    page=request.POST.get('page')
    code=request.POST.get('code')
    iccode=request.POST.get('iccode')
    pricing=request.POST.get('pricing')
    pricing_today=request.POST.get('pricing_today')
    company_id=request.POST.get('company_id')
    group_id=request.POST.get('group_id')
    searchlist={}
    if code:
        searchlist['code']=code
    if iccode:
        searchlist['iccode']=iccode
    if pricing:
        searchlist['pricing']=pricing
    if not page:
        page=1
    funpage=zz91page()
    limitNum=funpage.limitNum(2)
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
    list={'listall':listall,'listcount':listcount,'page_listcount':page_listcount}
    return HttpResponse(simplejson.dumps(list, ensure_ascii=False))

#保存定价
def pricing_now_save(request):
    zzdibang.storage_save(request)
    list={"answer":"answer"}
    return HttpResponse(simplejson.dumps(list, ensure_ascii=False))

#供应商列表
def supplier(request):
    page=request.POST.get('page')
    iccode=request.POST.get('iccode')
    company_id=request.POST.get('company_id')
    searchlist={}
    if iccode:
        searchlist['iccode']=iccode
    if not page:
        page=1
    funpage=zz91page()
    limitNum=funpage.limitNum(2)
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
    list={'listall':listall,'listcount':listcount,'page_listcount':page_listcount}
    return HttpResponse(simplejson.dumps(list, ensure_ascii=False))
#供货商保存
def supplier_save(request):
    id=request.POST.get('id')
    iccode=request.POST.get('iccode')
    if id:
        sql='select id from suppliers where iccode=%s and id!=%s'
        result=dbd.fetchonedb(sql,[iccode,id])
        if result:
            list={'err':'true'}
            return HttpResponse(simplejson.dumps(list, ensure_ascii=False))
    elif not id:
        sql='select id from suppliers where iccode=%s'
        result=dbd.fetchonedb(sql,[iccode])
        if result:
            list={'err':'true'}
            return HttpResponse(simplejson.dumps(list, ensure_ascii=False))
    zzdibang.supplier_save(request)
    list={'err':'false'}
    return HttpResponse(simplejson.dumps(list, ensure_ascii=False))
#数据汇总
def alldata(request):
    time_min=request.POST.get('time_min')
    time_max=request.POST.get('time_max')
    company_id=request.POST.get('company_id')
    result=zzdibang.alldata(request,time_min=time_min,time_max=time_max,company_id=company_id)
    total_weight=result['total_weight']
    total_price=result['total_price']
    listall=result['listall']
    list={"total_weight":total_weight,"total_price":total_price,"listall":listall}
    return HttpResponse(simplejson.dumps(list, ensure_ascii=False))
#入库明细
def storage(request):
    page=request.POST.get('page')
    company_id=request.POST.get('company_id')
    group_id=request.POST.get('group_id')
    searchtype=request.POST.get('searchtype')
    searchinfo=request.POST.get('searchinfo')
    searchinfo_date=request.POST.get('searchinfo_date')
    searchlist={}
    if searchtype=='iccode':
        searchlist['iccode']=searchinfo
    if searchtype=='supplier':
        searchlist['supplier']=searchinfo
    if searchtype=='gw':
        searchlist['gw']=searchinfo
    if searchtype=='gmt_created':
        searchlist['gmt_created']=searchinfo_date
    if searchtype=='price':
        searchlist['price']=searchinfo
    searchurl=urllib.urlencode(searchlist)
    if not page:
        page=1
    funpage=zz91page()
    limitNum=funpage.limitNum(2)
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
    list={'listall':listall,'listcount':listcount,'total_price':total_price,'page_listcount':page_listcount}
    return HttpResponse(simplejson.dumps(list, ensure_ascii=False))
#分站管理
def company(request):
    name=request.POST.get('name')
    page=request.POST.get('page')
    company_id=request.POST.get('company_id')
    group_id=request.POST.get('group_id')
    if not page:
        page=1
    funpage=zz91page()
    limitNum=funpage.limitNum(2)
    nowpage=funpage.nowpage(int(page))
    frompageCount=funpage.frompageCount()
    after_range_num = funpage.after_range_num(3)
    before_range_num = funpage.before_range_num(6)
    company_list=zzdibang.company_list(frompageCount,limitNum,name=name,group_id=group_id,company_id=company_id)
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
    list={'listall':listall,'listcount':listcount,'page_listcount':page_listcount}
    return HttpResponse(simplejson.dumps(list, ensure_ascii=False))
#添加分站
def company_save(request):
    zzdibang.company_save(request)
    list={'answer':'answer'}
    return HttpResponse(simplejson.dumps(list, ensure_ascii=False))
#产品类别
def category(request):
    name=request.POST.get('name')
    page=request.POST.get('page')
    group_id=request.POST.get('group_id')
    company_id=request.POST.get('company_id')
    if not page:
        page=1
    funpage=zz91page()
    limitNum=funpage.limitNum(2)
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
    list={'listall':listall,'listcount':listcount,'page_listcount':page_listcount}
    return HttpResponse(simplejson.dumps(list, ensure_ascii=False))
#添加类别
def category_save(request):
    zzdibang.category_save(request)
    list={"answer":"answer"}
    return HttpResponse(simplejson.dumps(list, ensure_ascii=False))
#产品列表
def product(request):
    name=request.POST.get('name')
    page=request.POST.get('page')
    category_selfid=request.POST.get('category_selfid')
    company_id=request.POST.get('company_id')
    group_id=request.POST.get('group_id')
    if not page:
        page=1
    funpage=zz91page()
    limitNum=funpage.limitNum(2)
    nowpage=funpage.nowpage(int(page))
    frompageCount=funpage.frompageCount()
    after_range_num = funpage.after_range_num(3)
    before_range_num = funpage.before_range_num(6)
    product_list=zzdibang.product_list(frompageCount,limitNum,name=name,category_selfid=category_selfid,company_id=company_id,group_id=group_id)
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
    list={'listall':listall,'listcount':listcount,'page_listcount':page_listcount}
    return HttpResponse(simplejson.dumps(list, ensure_ascii=False))
#添加产品
def product_save(request):
    zzdibang.product_save(request)
    list={"answer":"answer"}
    return HttpResponse(simplejson.dumps(list, ensure_ascii=False))
#人员列表
def user(request):
    contact=request.POST.get('contact')
    page=request.POST.get('page')
    company_id=request.POST.get('company_id')
    group_id=request.POST.get('group_id')
    if not page:
        page=1
    funpage=zz91page()
    limitNum=funpage.limitNum(2)
    nowpage=funpage.nowpage(int(page))
    frompageCount=funpage.frompageCount()
    after_range_num = funpage.after_range_num(3)
    before_range_num = funpage.before_range_num(6)
    category_list=zzdibang.user_list(frompageCount,limitNum,contact=contact,company_id=company_id,group_id=group_id)
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
    list={'listall':listall,'listcount':listcount,'page_listcount':page_listcount}
    return HttpResponse(simplejson.dumps(list, ensure_ascii=False))
#添加人员
def user_save(request):
    zzdibang.user_save(request)
    list={"answer":"answer"}
    return HttpResponse(simplejson.dumps(list, ensure_ascii=False))
#个人信息
def myinfo(request):
    username=request.POST.get('username')
    sql='select id,sex,mobile,contact from users where username=%s'
    result=dbd.fetchonedb(sql,[username])
    sex=result['sex']
    mobile=result['mobile']
    id=result['id']
    contact=result['contact']
    list={'sex':sex,'username':username,'mobile':mobile,'id':id,'contact':contact}
    return HttpResponse(simplejson.dumps(list, ensure_ascii=False))
#个人信息保存
def myinfo_save(request):
    zzdibang.user_save(request)
    list={"err":"false"}
    return HttpResponse(simplejson.dumps(list, ensure_ascii=False))
#自动获取供应商编号
def get_iccode(request):
    iccode=time.strftime("%Y-%m-%d %X", time.localtime())
    iccode=iccode.replace('-','').replace(':','').replace(' ','')
    list={'iccode':iccode}
    return HttpResponse(simplejson.dumps(list, ensure_ascii=False))
#查询供应商
def searchsuppliers(request):
    iccode=request.GET.get("iccode")
    pname=request.GET.get("pname")
    group_id=request.GET.get("group_id")
    xmltype=request.GET.get("xmltype")
    list={'err':'true','list':''}
    if iccode:
        sql="select * from suppliers where iccode=%s and group_id=%s limit 0,20"
        result=db.fetchalldb(sql,[iccode,group_id])
        if result:
            for dic in result:
                dic['gmt_created']=formattime(dic['gmt_created'])
                dic['gmt_modified']=formattime(dic['gmt_modified'])
            list['err']='false'
            list['list']=result
    if pname:
        sql="select * from suppliers where name like %s  and group_id=%s limit 0,20"
        result=db.fetchalldb(sql,['%'+pname+'%',group_id])
        if result:
            for dic in result:
                dic['gmt_created']=formattime(dic['gmt_created'])
                dic['gmt_modified']=formattime(dic['gmt_modified'])
            list['err']='false'
            list['list']=result
    if xmltype:
        xml=dict2xml(list,wrap='xml')
        return HttpResponse(xml)
    else:
        return HttpResponse(simplejson.dumps(list, ensure_ascii=False))

#更新数据
def datatable_update(request):
    maxid=request.GET.get("maxid")
    datatable=request.GET.get("datatable")
    company_id=request.GET.get("company_id")
    xmltype=request.GET.get("xmltype")
    list={'err':'true','list':''}
    if datatable:
        if maxid=="0" or not maxid:
            maxdate='1970-1-1'
        else:
            maxdate=int_to_strall(int(maxid))
        if datatable=="category_products":
            tablename="category_products"
        if datatable=="products":
            tablename="products"
        if datatable=="suppliers":
            tablename="suppliers"
        if datatable=="users":
            tablename="users"
        if datatable=="company":
            tablename="company"
            sql="select * from "+tablename+" where id=%s"
            result=db.fetchalldb(sql,[company_id])
        elif datatable=="grouplist":
            tablename="grouplist"
            sql="select * from "+tablename+" where id=%s"
            result=db.fetchalldb(sql,[company_id])
        else:
            sql="select * from "+tablename+" where gmt_modified>%s and company_id=%s order by gmt_modified asc"
            result=db.fetchalldb(sql,[maxdate,company_id])
        if result:
            for dic in result:
                dic['gmt_created']=formattime(dic['gmt_created'])
                dic['gmt_modified']=formattime(dic['gmt_modified'])
            list['err']='false'
            list['list']=result
        #return HttpResponse(sql)
    if xmltype:
        xml=dict2xml(list,wrap='xml')
        return HttpResponse(xml)
    else:
        return HttpResponse(simplejson.dumps(list, ensure_ascii=False))
