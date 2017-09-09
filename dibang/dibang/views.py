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
    user_selfid=request.session.get('user_selfid',default=None)
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
    name=request.GET.get('name')
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
    list={"code":0,"msg":"","count":listcount,"data":listall}
    return HttpResponse(simplejson.dumps(list, ensure_ascii=False))
#供货商添加
def supplier_add(request):
    username=request.session.get('username',default=None)
    group_id=request.session.get('group_id',default=None)
    user_selfid=request.session.get('user_selfid',default=None)
    if not username:
        return HttpResponseRedirect("login.html")
    company_id=request.GET.get('company_id')
    return render_to_response('supplier_add.html',locals())
#供货商修改
def supplier_mod(request):
    username=request.session.get('username',default=None)
    group_id=request.session.get('group_id',default=None)
    user_selfid=request.session.get('user_selfid',default=None)
    if not username:
        return HttpResponseRedirect("login.html")
    id=request.GET.get('id')
    sql='select ctype,group_id,company_id,name,htype,contact,mobile,pwd,address,bz from suppliers where id=%s'
    result=dbd.fetchonedb(sql,[id])
    return render_to_response('supplier_mod.html',locals())
#供货商保存
def supplier_save(request):
    username=request.session.get('username',default=None)
    group_id=request.session.get('group_id',default=None)
    user_selfid=request.session.get('user_selfid',default=None)
    if not username:
        return HttpResponseRedirect("login.html")
    zzdibang.supplier_save(request)
    return HttpResponseRedirect("supplier.html")

#供货商删除
def supplier_del(request):
    username=request.session.get('username',default=None)
    group_id=request.session.get('group_id',default=None)
    user_selfid=request.session.get('user_selfid',default=None)
    if not username:
        return HttpResponseRedirect("login.html")
    id=request.POST.get('id')
    sql='delete from supplier where id=%s'
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
    category_list=zzdibang.category_list(frompageCount,limitNum,name=name)
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
    if not username:
        return HttpResponseRedirect("login.html")
    company_id=request.GET.get('company_id')
    return render_to_response('category_add.html',locals())
#产品类别修改
def category_mod(request):
    username=request.session.get('username',default=None)
    group_id=request.session.get('group_id',default=None)
    user_selfid=request.session.get('user_selfid',default=None)
    if not username:
        return HttpResponseRedirect("login.html")
    id=request.GET.get('id')
    sql='select name from category_products where id=%s'
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


def viewer_404(request):
    t = get_template('404.html')
    html = t.render(Context())
    return HttpResponseNotFound(html)
def viewer_500(request):
    t = get_template('404.html')
    html = t.render(Context())
    return HttpResponseNotFound(html)