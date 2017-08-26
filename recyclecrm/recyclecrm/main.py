# -*- coding:utf-8 -*-
from django.shortcuts import render,render_to_response
from django.http import HttpResponse,HttpResponseRedirect
import simplejson,sys,os,urllib,urllib2,re,datetime,time,md5,hashlib,random,calendar
import json
import random
import time
from django.core.handlers.wsgi import WSGIRequest
from zz91db_recyclecrm import recyclecrmdb
from zz91db_ast import companydb
from zz91page import *
from sphinxapi import *
from zz91settings import SPHINXCONFIG
from django.core.cache import cache


db=recyclecrmdb(1)
dbc=companydb(1)
reload(sys)
sys.setdefaultencoding('UTF-8')
nowpath=os.path.dirname(__file__)
execfile(nowpath+"/func/main_function.py")
execfile(nowpath+"/func/crmtools.py")
zzs=zzcompany()
#首页
def index(request):
    username=request.session.get('username',default=None)
    user_id=request.session.get('user_id',default=None)
    if not username or not user_id:
        return HttpResponseRedirect("/crm/login.html")
    return render_to_response('main/index.html',locals())
#首页
def login(request):
    username=request.session.get('username',default=None)
    user_id=request.session.get('user_id',default=None)
    done= request.GET.get("done")
    if not done:
        done= request.POST.get("done")
    if (done):
        done=done.replace("^and^","&")
        done=done.replace("^wenhao^","?")
        done=done.replace("%5Eand%5E","&")
        done=done.replace("^jing^","#")
    if not done:
        done=''
    #----登录页跳转到注册页后跳转
    if user_id and done:
        return HttpResponseRedirect(done)
    return render_to_response('main/login.html',locals())
def loginsave(request):
    gmt_modified=datetime.datetime.now()
    done = request.POST.get('done')
    username = request.POST.get('username')
    pwd = request.POST.get('pwd')
    error="用户名或密码错误！"
    if not pwd:
        error="用户名或密码错误！"
        return render_to_response('main/login.html',locals())
    md5pwd = hashlib.md5(pwd)
    md5pwd = md5pwd.hexdigest()[8:-8]
    if username:
        sql="select id,name from user where name=%s and password=%s"
        plist=db.fetchonedb(sql,[username,md5pwd]);
        if plist:
            request.session.set_expiry(6000*6000)
            username=plist["name"]
            request.session['username']=username
            request.session['user_id']=plist["id"]
            if not done:
                response=HttpResponseRedirect("/crm/index.html")
                return response
            else:
                response=HttpResponseRedirect(done)
                return response
        else:
            error="您的用户名或密码错误，请注意英文大小写！"
            return render_to_response('main/login.html',locals())
    return render_to_response('main/login.html',locals())
#注册第一步
def reg_one(request):
    return render_to_response('main/reg_one.html',locals())

#注册第二步
def reg_two(request):
    mobile=request.POST.get('mobile')
    password=request.POST.get('password')
    sql='select id from user where name=%s'
    result=db.fetchonedb(sql, [mobile])
    if not result:
        return render_to_response('main/reg_two.html',locals())
    else:
        return HttpResponseRedirect('reg_one.html',locals())
#保存注册信息
def reg_save(request):
    result=zzs.reg_save(request)
    return render_to_response('main/login.html',locals())
#主页面
def main(request):
    username=request.session.get('username',default=None)
    user_id=request.session.get('user_id',default=None)
    if not username or not user_id:
        return HttpResponseRedirect("/crm/login.html")
    arealist=['浙江','广东','江苏','福建','安徽','河南','河北','湖北','湖南','四川','江西','山东','海南','黑龙江','北京','上海','天津','青海','陕西','山西','贵州','辽宁','宁夏','吉林','内蒙古','广西','云南','西藏','重庆','甘肃','新疆','台湾','香港','澳门']
    return render_to_response('main/main.html',locals())
#公司资料
def company(request):
    username=request.session.get('username',default=None)
    user_id=request.session.get('user_id',default=None)
    if not username or not user_id:
        return HttpResponseRedirect("/crm/login.html")
    keywords=request.POST.get('keywords')
    area=request.GET.get('area')
    industry=request.GET.get('industry')
    jisd=request.GET.get('jisd')
    userall=zzs.getcompanylist(keywords,area,industry,jisd,1,10,20)
    listall=userall['list']
    return render_to_response('main/company.html',locals())
#公司详情
def details(request):
    username=request.session.get('username',default=None)
    user_id=request.session.get('user_id',default=None)
    if not username or not user_id:
        return HttpResponseRedirect("/crm/login.html")
    #userall=zzs.details(request)
    userall=zzs.yundetails(request)
    companyinfo=userall['companyinfo']
    companyuserlist=userall['companyuserlist']
    company_id=request.GET.get('company_id')
    return render_to_response('main/details.html',locals())
#修改公司资料
def company_modify(request):
    username=request.session.get('username',default=None)
    user_id=request.session.get('user_id',default=None)
    if not username or not user_id:
        return HttpResponseRedirect("/crm/login.html")
    result=zzs.company_modify(request)
    data = {"answer": "answer"}
    return HttpResponse(simplejson.dumps(data, ensure_ascii=False))
#我的联系人
def contact_list(request):
    username=request.session.get('username',default=None)
    user_id=request.session.get('user_id',default=None)
    if not username or not user_id:
        return HttpResponseRedirect("/crm/login.html")
    result=zzs.contact_list(request)
    listall=result['listall']
    return render_to_response('main/contact_list.html', locals())
    
#添加联系人
def contact_add(request):
    username=request.session.get('username',default=None)
    user_id=request.session.get('user_id',default=None)
    if not username or not user_id:
        return HttpResponseRedirect("/crm/login.html")
    result=zzs.contact_add(request)
    data = {"answer": "answer"}
    return HttpResponse(simplejson.dumps(data, ensure_ascii=False))
#修改联系人
def contact_mod(request):
    username=request.session.get('username',default=None)
    user_id=request.session.get('user_id',default=None)
    if not username or not user_id:
        return HttpResponseRedirect("/crm/login.html")
    result=zzs.contact_mod(request)
    data = {"answer": "answer"}
    return HttpResponse(simplejson.dumps(data, ensure_ascii=False))
#跟进记录
def history(request):
    username=request.session.get('username',default=None)
    user_id=request.session.get('user_id',default=None)
    if not username or not user_id:
        return HttpResponseRedirect("/crm/login.html")
    userall_history=zzs.history(request)
    listall=userall_history['listall']
    userall=zzs.details(request)
    companyinfo=userall['companyinfo']
    companyuserlist=userall['companyuserlist']
    company_id=request.GET.get('company_id')
    return render_to_response('main/history.html',locals())
#添加到我的客户库
def addto(request):
    username=request.session.get('username',default=None)
    user_id=request.session.get('user_id',default=None)
    if not username or not user_id:
        return HttpResponseRedirect("/crm/login.html")
    result=zzs.addto(request)
    data = {"answer": "answer"}
    return HttpResponse(simplejson.dumps(data, ensure_ascii=False))
#立即联系
def contact(request):
    username=request.session.get('username',default=None)
    user_id=request.session.get('user_id',default=None)
    if not username or not user_id:
        return HttpResponseRedirect("/crm/login.html")
    company_id=request.GET.get('company_id')
    value=request.POST.get('action')
    if request.method=="GET":
        return render_to_response('handle/contact.html',locals())
    else:
        if value=="打电话":
            listall=zzs.contact(request)['listall']
            return render_to_response('main/call.html',locals())
        elif value=="发短信":
            listall=zzs.contact(request)['listall']
            return render_to_response('main/text.html',locals())
        elif value=="约见面":
            listall=zzs.contact(request)['listall']
            return render_to_response('main/date.html',locals())
#立即行动
def action(request):
    username=request.session.get('username',default=None)
    user_id=request.session.get('user_id',default=None)
    if not username or not user_id:
        return HttpResponseRedirect("/crm/login.html")
    result=zzs.action(request)
    return render_to_response('main/details.html')
#客户小计
def bz(request):
    username=request.session.get('username',default=None)
    user_id=request.session.get('user_id',default=None)
    if not username or not user_id:
        return HttpResponseRedirect("/crm/login.html")
    result=zzs.bz(request)
    data = {"answer": "answer"}
    return HttpResponse(simplejson.dumps(data, ensure_ascii=False))
#操作记录
def remark(request):
    username=request.session.get('username',default=None)
    user_id=request.session.get('user_id',default=None)
    if not username or not user_id:
        return HttpResponseRedirect("/crm/login.html")
    result=zzs.remark(request)
    data = {"answer": "answer"}
    return HttpResponse(simplejson.dumps(data, ensure_ascii=False))
#获取行业类别
def categoryinfo(request):
    host=zzs.getnowurl(request)
    username=request.session.get("username",None)
    categorycode=request.GET.get("categorycode")
    categorycodelist=getindexcategorylist(categorycode,1)
    ctype=request.GET.get("ctype")
    if ctype=="company":
        return render_to_response('new/categorycode_key.html',locals())
    if ctype=="aui":
        return render_to_response('new/categorycode_aui.html',locals())
    return render_to_response('new/categorycode.html',locals())