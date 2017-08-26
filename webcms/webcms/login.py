#-*- coding:utf-8 -*-
from django.shortcuts import render_to_response
from django.http import HttpResponse,HttpResponseRedirect
from zz91db_130 import pycmsdb
import re
dbp=pycmsdb()

def loginpage(request):
    backurl=request.GET.get('backurl')
    if not backurl:
        backurl=''
    return render_to_response('login/loginpage.html',locals())

def login(request):
    username1=request.POST['username1']
    password1=request.POST['password1']
    backurl=''
    if request.POST.has_key('backurl'):
        backurl=request.POST['backurl']
    error1=''
    error2=''
    if not username1:
        error1='请输入用户名'
    if not password1:
        error2='请输入密码'
    if error1 or error2:
        return render_to_response('login/loginpage.html',locals())
    #----客户登录入口
    sql='select id from py_user where username=%s and password=%s and sortrank=0'
    result=dbp.fetchonedb(sql,[username1,password1])
    if result:
        request.session['username']=username1
        request.session['user_id']=result[0]
        request.session['sortrank']='0'
        if backurl:
            return HttpResponseRedirect(backurl)
        else:
            return HttpResponseRedirect('/user/')
    #----管理员登录入口
    sql1='select id from py_user where username=%s and password=%s and sortrank=1'
    result1=dbp.fetchonedb(sql1,[username1,password1])
    if result1:
        request.session['username']=username1
        request.session['user_id']=result1[0]
        request.session['sortrank']='1'
        if backurl:
            return HttpResponseRedirect(backurl)
        else:
#            return HttpResponseRedirect('/admin/')
            return HttpResponseRedirect('/user/')
    return render_to_response('login/loginpage.html',locals())

def logout(request):
    request_url = request.META.get('HTTP_REFERER', '/')
    request.session.delete()
    return HttpResponseRedirect('loginpage.html')
