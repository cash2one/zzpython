#-*- coding:utf-8 -*-
from django.shortcuts import render_to_response
from django.http import HttpResponse,HttpResponseRedirect
import os,datetime,time,re,urllib,md5,json,sys,random,hashlib
from zz91db_work import workdb
dbw=workdb()
permissions=[
             {'zhanghao':'yunying','mima':'123'},
             ]

def loginpage(request):
    return render_to_response('useradmin/loginpage.html',locals())

def login(request):
    username1=request.POST.get('username1')
    password1=passwd=request.POST.get('password1')
    if not username1:
        HttpResponseRedirect("loginpage.html")
    error1=''
    error2=''
    if not username1:
        error1='请输入用户名'
    if not password1:
        error2='请输入密码'
    if error1 or error2:
        return render_to_response('useradmin/loginpage.html',locals())
    if passwd:
        md5pwd = hashlib.md5(passwd)
        md5pwd = md5pwd.hexdigest()[8:-8]
    sql="select id,username from auth_user where username=%s and password=%s"
    plist=dbw.fetchonedb(sql,[username1,md5pwd]);
    if plist:
        userid=plist[0]
        username=plist[1]
        request.session.set_expiry(6000*6000)
        request.session['username']=username
        request.session['userid']=userid
        return HttpResponseRedirect('admin.html')
    else:
        error1="用户或密码错误"
    
    return render_to_response('useradmin/loginpage.html',locals())

def logout(request):
    request_url = request.META.get('HTTP_REFERER', '/')
    request.session.delete()
    return HttpResponseRedirect('loginpage.html')
