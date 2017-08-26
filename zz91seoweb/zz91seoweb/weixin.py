#-*- coding:utf-8 -*- 
from django.shortcuts import render_to_response,RequestContext
from django.http import HttpResponse,HttpResponseRedirect


def default(request):
    return render_to_response('weixin/index.html',locals())