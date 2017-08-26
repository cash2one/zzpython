#-*- coding:utf-8 -*-
from django.shortcuts import render_to_response
from django.http import HttpResponse,HttpResponseRedirect
from django.core.context_processors import csrf
from django.views.decorators.csrf import csrf_exempt
import re

permissions=[
             {'zhanghao':'hunsha','mima':'hunzhiji123'},
             ]

def loginpage(request):
    return render_to_response('useradmin/loginpage.html',locals())
@csrf_exempt
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
            return HttpResponseRedirect('admin.html')
    return render_to_response('useradmin/loginpage.html',locals())

def logout(request):
    request_url = request.META.get('HTTP_REFERER', '/')
    request.session.delete()
    return HttpResponseRedirect('loginpage.html')
