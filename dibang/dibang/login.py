#-*- coding:utf-8 -*-
from django.shortcuts import render_to_response
from django.http import HttpResponse,HttpResponseRedirect
import simplejson,sys,os,urllib,re,hashlib,md5,random,datetime
from dict2xml import dict2xml
from zz91db_dibang import dibangdb
db=dibangdb(1)
from zz91page import *
reload(sys)
sys.setdefaultencoding('UTF-8')

def login(request):
    username=request.session.get('username',default=None)
    if username:
        return HttpResponseRedirect('main.html')
    if not username:
        username=''
    return render_to_response('login.html',locals())
def logincheck(request):
    username=request.POST.get('username')
    password=passwd=request.POST.get('password')
    if passwd:
        md5pwd = hashlib.md5(passwd)
        md5pwd = md5pwd.hexdigest()[8:-8]
    
    if username and password:
        sql='select id,group_id,selfid,company_id,utype from users where username=%s and pwd=%s and isdel=0'
        result=db.fetchonedb(sql,[username,md5pwd])
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
            return HttpResponseRedirect('main.html')
        else:
            errtext="用户名或密码错误"
            return render_to_response('login.html',locals())
    else:
        errtext="请输入用户名或密码"
        return render_to_response('login.html',locals())

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
