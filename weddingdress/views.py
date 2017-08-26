#-*- coding:utf-8 -*-
from django.shortcuts import render_to_response
from django.http import HttpResponse,HttpResponseRedirect
from zz91db_130 import otherdb
import os,datetime
nowpath=os.path.dirname(__file__)
execfile(nowpath+"/function.py")
zzother=otherdb()
hzj=hunzhiji()

def default(request,page=''):
    index=1
    return render_to_response('index.html',locals())

def weddingdress(request):
    index=3
    return render_to_response('weddingdress.html',locals())

def shop(request):
    index=4
    return render_to_response('shop.html',locals())

def wedingshow(request):
    index=5
    return render_to_response('wedingshow.html',locals())

def marrygettogether(request):
    index=6
    return render_to_response('marrygettogether.html',locals())

def help(request):
    typeid=request.GET.get('typeid')
    artid=request.GET.get('artid')
    if typeid=='2':
        artdetail=hzj.getartdetail(artid)
    else:
        artlist=hzj.getartlist(15,1)
        if artid:
            artdetail=hzj.getartdetail(artid)
    arttypelist=hzj.getartlist(7,2)
    if artid:
        artid=int(artid)
    return render_to_response('help.html',locals())

def callus(request):
    index=7
    return render_to_response('callus.html',locals())

def dressfree(request):
    return render_to_response('dressfree.html',locals())

def marryenjoy(request,page=''):
    index=2
    if page:
        return render_to_response('marryenjoy2.html',locals())
    return render_to_response('marryenjoy.html',locals())

def openqqwindow(request):
    return render_to_response('openqqwindow.html',locals())

def sendyuyue(request):
    request_url=request.META.get('HTTP_REFERER','/')
#    name=request.POST['name']
#    telphone=request.POST['telphone']
#    email=request.POST['email']
#    friend='' 
#    if request.POST.has_key('friend'):
#        friend=request.POST.getlist('friend')
#    remark=request.POST['remark']
    name=request.GET.get('name')
    telphone=request.GET.get('telphone')
    email=request.GET.get('email')
    remark=request.GET.get('remark')
    friend=request.GET.get('friend')
    if request.META.has_key('HTTP_X_FORWARDED_FOR'):
        ip =  request.META['HTTP_X_FORWARDED_FOR']
    else:
        ip = request.META['REMOTE_ADDR']
    phonedetail=zzother.getphonedetail(telphone)
    province=phonedetail['province']
    city=phonedetail['city']
    gmt_created=datetime.datetime.now()
    argument=[name,telphone,email,friend,remark,ip,province,city,gmt_created,gmt_created]
    sql='insert into hunsha_yuyue(name,phone,mail,friend,remark,ip,province,city,sendtime,gmt_created) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
    zzother.updatetodb(sql,argument)
    return HttpResponse('1')
#    return HttpResponseRedirect(request_url)
