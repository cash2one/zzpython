#-*- coding:utf-8 -*-
from django.shortcuts import render_to_response
from django.http import HttpResponse,HttpResponseRedirect
from zz91page import *
from settings import pyuploadpath,pyimgurl
import os,datetime,time,urllib
from django.views.decorators.csrf import csrf_exempt
nowpath=os.path.dirname(__file__)
execfile(nowpath+"/admin_function.py")

adm=hzjadmin()

def returnpage(request):
    request_url=request.GET.get('request_url')
    return HttpResponseRedirect(request_url)

def admin(request):
    username=request.session.get('username')
    if not username:
        return HttpResponseRedirect('loginpage.html')
    return render_to_response('admin/admin.html',locals())

def changehand(request):
    is_ok=request.GET.get('is_ok')
    auto_id=request.GET.get('auto_id')
    if is_ok=='1':
        is_ok='0'
    else:
        is_ok='1'
    sql='update hunsha_yuyue set is_handle=%s where id=%s'
    adm.db.updatetodb(sql,[is_ok,auto_id])
    return HttpResponse('1')

def yuyue(request):
    username=request.session.get('username')
    if not username:
        return HttpResponseRedirect('weddingdress/loginpage.html')
    is_hand=request.GET.get('is_hand')
    if is_hand:
        if is_hand=='1':
            handname='已处理'
        else:
            handname='未处理'
    searchlist={}
    if is_hand:
        searchlist['is_hand']=is_hand
    searchurl=urllib.urlencode(searchlist)
    page=request.GET.get('page')
    if not page:
        page=1
    funpage=zz91page()
    limitNum=funpage.limitNum(15)
    nowpage=funpage.nowpage(int(page))
    frompageCount=funpage.frompageCount()
    after_range_num = funpage.after_range_num(3)
    before_range_num = funpage.before_range_num(6)
    hunshayuyue=adm.gethunshayuyue(frompageCount,limitNum,is_hand)
    listcount=0
    listall=hunshayuyue['list']
    listcount=hunshayuyue['count']
    if int(listcount)>1000000:
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
    return render_to_response('admin/yuyue.html',locals())

def arttype(request):
    typelist=adm.gettypelist()
    return render_to_response('admin/arttype.html',locals())

def artical(request):
    page=request.GET.get('page')
    is_del=request.GET.get('is_del')
#    typeid=request.GET.get('typeid')
#    if typeid:
#        typename=gettypename(typeid)
    searchlist={}
    if is_del:
        searchlist['is_del']=is_del
    searchurl=urllib.urlencode(searchlist)
    if not page:
        page=1
    funpage=zz91page()
    limitNum=funpage.limitNum(15)
    nowpage=funpage.nowpage(int(page))
    frompageCount=funpage.frompageCount()
    after_range_num = funpage.after_range_num(3)
    before_range_num = funpage.before_range_num(6)
    compdynamiclist=adm.getarticallist(frompageCount,limitNum,is_del)
    listcount=0
    listall=compdynamiclist['list']
    listcount=compdynamiclist['count']
    if int(listcount)>1000000:
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
    return render_to_response('admin/artical.html',locals())

def addartical(request):
    typelist=adm.gettypelist()
    request_url=request.META.get('HTTP_REFERER','/')
    gmt_created=time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
    return render_to_response('admin/addartical.html',locals())
def updateartical(request):
    typelist=adm.gettypelist()
    request_url=request.META.get('HTTP_REFERER','/')
    artid=request.GET.get('artid')
    artdetail=adm.getartdetail(artid)
    if artdetail:
        typeid=artdetail['typeid']
        typename=artdetail['typename']
        title=artdetail['title']
        litpic=artdetail['litpic']
        content=artdetail['content']
        sortrank=artdetail['sortrank']
        gmt_created=artdetail['gmt_created']
    return render_to_response('admin/addartical.html',locals())
def deldynamic(request):
    request_url=request.META.get('HTTP_REFERER','/')
    dynamicid=request.GET.get('dynamicid')
    is_del=request.GET.get('is_del')
    sql='update dynamic set is_del=%s where id=%s'
    adm.db.updatetodb(sql,[is_del,dynamicid])
    return HttpResponseRedirect(request_url)
@csrf_exempt
def addarticalok(request):
    request_url=request.POST['request_url']
    content=''
    artid=''
    error=0
    sortrank=request.POST['sortrank']
    typeid=request.POST['typeid']
    if typeid:
        typename=adm.gettypename(typeid)
    gmt_created=request.POST['gmt_created']
    litpic=request.POST['litpic']
    title=request.POST['title']
    if request.POST.has_key('myEditor'):
        content=request.POST['myEditor']
    if request.POST.has_key('artid'):
        artid=request.POST['artid']
    if not title:
        error=1
    if not content:
        error=1
    if error==1:
        return render_to_response('admin/addartical.html',locals())
    gmt_modified=datetime.datetime.now()
    if artid:
        sql='update hunsha_artical set title=%s,typeid=%s,content=%s,gmt_modified=%s,litpic=%s,sortrank=%s where id=%s'
        argument=[title,typeid,content,gmt_modified,litpic,sortrank,artid]
    else:
        sql='insert into hunsha_artical(title,typeid,content,gmt_created,gmt_modified,litpic,sortrank) values(%s,%s,%s,%s,%s,%s,%s)'
        argument=[title,typeid,content,gmt_created,gmt_created,litpic,sortrank]
    adm.db.updatetodb(sql,argument)
    return HttpResponseRedirect(request_url)

def mailimg(request):
    return render_to_response('admin/mailimg.html',locals())

#----上传文件通用
@csrf_exempt
def mailloadimg(request):
    username=request.session.get("username",None)
    timepath=time.strftime('%Y/%m/%d/',time.localtime(time.time()))
    gmt_created=datetime.datetime.now()
    nowtime=int(time.time())
    if request.FILES:
        file = request.FILES['file']
#        tmp = random.randint(100, 999)
        newpath=pyuploadpath+timepath
        filename=file.name
        imgpath=newpath+filename
        if not os.path.isdir(newpath):
            os.makedirs(newpath)
        des_origin_f = open(imgpath,"w")
        for chunk in file.chunks():
            des_origin_f.write(chunk)
        des_origin_f.close()
        
        suportFormat = ['BMP', 'GIF', 'JPG','JPGE', 'PNG','JPEG']
        officeFormat = ['DOC','DOCX', 'DOCM', 'DOTX','DOTM','XLS','XLSX','XLSM','XLTX','XLTM','XLSB','XLAM','PDF','TXT','ET']
        
        filetype=filename.split('.')[-1]
        filetype=filetype.upper()
        if filetype in suportFormat:
            imagetype=1
        elif filetype in officeFormat:
            officetype=1
        else:
            return HttpResponse("请选择一个正确的office文件格式.")
        picurl=imgpath.replace(pyuploadpath,'')
        pic_url=pyimgurl+picurl
        return render_to_response('admin/loadimg.html',locals())
    return HttpResponse("请选择一个文件.")
