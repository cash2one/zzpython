#-*- coding:utf-8 -*-
from django.utils.http import urlquote
from django.shortcuts import render_to_response
from django.http import HttpResponse,HttpResponseRedirect
#----首页
def default(request,path):
    return render_to_response(path,locals())
