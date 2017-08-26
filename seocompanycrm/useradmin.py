#-*- coding:utf-8 -*-
from django.shortcuts import render_to_response
from django.http import HttpResponse,HttpResponseRedirect
from views import fetchonedb
import re

permissions=[
             {'zhanghao':'yunying','mima':'123456'},
             {'zhanghao':'seo','mima':'123'},
             {'zhanghao':'sales','mima':'123'}
             ]

def loginpage(request):
    return render_to_response('useradmin/loginpage.html',locals())

def login(request):
    username1=request.POST['username1']
    password1=request.POST['password1']
    error1=''
    error2=''
    if not username1:
        error1='请输入用户名'
    if not password1:
        error2='请输入密码'
    if error1 or error2:
        return render_to_response('useradmin/loginpage.html',locals())
    for pm in permissions:
        un=pm['zhanghao']
        pw=pm['mima']
        if username1==un and password1==pw:
            request.session['username']=un
            return HttpResponseRedirect('/')
    sql1='select id,name,type from seo_user where username=%s and password=%s'
    result1=fetchonedb(sql1,[username1,password1])
    if result1:
        type=result1[2]
        request.session['userid']=result1[0]
        request.session['username']=result1[1]
        if type==1:
            request.session['usertype']='seouser'
        elif type==2:
            request.session['usertype']='salesman'
        return HttpResponseRedirect('/')
    if username1==password1:
        sql='select id,mobile,name from seo_company where mobile=%s'
        result=fetchonedb(sql,[username1])
        if result:
            request.session['company_id']=result[0]
            request.session['username']=result[1]
            request.session['usertype']='company'
            return HttpResponseRedirect('/')
    error1='账号或密码不正确'
    return render_to_response('useradmin/loginpage.html',locals())

def logout(request):
    request_url = request.META.get('HTTP_REFERER', '/')
    request.session.delete()
    return HttpResponseRedirect('/')
