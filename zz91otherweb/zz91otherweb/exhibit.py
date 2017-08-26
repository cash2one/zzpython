#-*- coding:utf-8 -*-
from django.shortcuts import render_to_response
from django.http import HttpResponse,HttpResponseRedirect
from zz91page import *
import os,datetime,time,re,urllib,simplejson,sys
from zz91tools import int_to_str,get_str_timeall,str_to_int,formattime,filter_tags
from zz91db_ast import companydb

from views import otherimgupload
dbc=companydb()
nowpath=os.path.dirname(__file__)
reload(sys)
sys.setdefaultencoding('UTF-8')
execfile(nowpath+"/func/exhibit_function.py")
zzzh=zzexhibit()

def list(request):
    bklist=zzzh.getcategorylist("1037")
    hylist=zzzh.getcategorylist("1038")
    #辅助类别
    hzlist=zzzh.getcategorylist("2012")
    page=request.GET.get('page')
    name=request.GET.get('name')
    area=request.GET.get('area')
    plate_category_code=request.GET.get('plate_category_code')
    if not plate_category_code:
        plate_category_code=''
    exhibit_category_code=request.GET.get('exhibit_category_code')
    if not exhibit_category_code:
        exhibit_category_code=''
    if not page:
        page=1
    searchlist={}
    if area:
        searchlist['area']=area
    if name:
        searchlist['name']=name
        
    if plate_category_code:
        searchlist['plate_category_code']=plate_category_code
    if exhibit_category_code:
        searchlist['exhibit_category_code']=exhibit_category_code
    
        
    searchurl=urllib.urlencode(searchlist)
    funpage=zz91page()
    limitNum=funpage.limitNum(10)
    nowpage=funpage.nowpage(int(page))
    frompageCount=funpage.frompageCount()
    after_range_num = funpage.after_range_num(3)
    before_range_num = funpage.before_range_num(6)
    qianbao_gglist=zzzh.zhlist(frompageCount,limitNum,searchlist=searchlist)
    listcount=0
    listall=qianbao_gglist['list']
    listcount=qianbao_gglist['count']
    if (int(listcount)>1000000):
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
    return render_to_response('exhibit/list.html',locals())

def add(request):
    exhibit_id=''
    bklist=zzzh.getcategorylist("1037")
    hylist=zzzh.getcategorylist("1038")
    #辅助类别
    hzlist=zzzh.getcategorylist("2012")
    return render_to_response('exhibit/add.html',locals())
def del_zh(request):
    request_url=request.META.get('HTTP_REFERER','/')
    eid=request.GET.get('eid')
    sql='delete from exhibit where id=%s'
    dbc.updatetodb(sql,[eid])
    return HttpResponseRedirect(request_url)
def zhedit(request):
    bklist=zzzh.getcategorylist("1037")
    hylist=zzzh.getcategorylist("1038")
    #辅助类别
    hzlist=zzzh.getcategorylist("2012")
    exhibit_id=request.GET.get("eid")
    sql="select name,area,start_time,end_time,plate_category_code,exhibit_category_code,content,tags,photo_cover,allzhuban,hz_categorylist,gmt_created,gmt_modified,redircturl from exhibit where id=%s"
    result=dbc.fetchonedb(sql,[exhibit_id])
    if result:
        name=result[0]
        area=result[1]
        if not area:
            area=''
        start_time=formattime(result[2])
        end_time=formattime(result[3])
        plate_category_code=result[4]
        exhibit_category_code=result[5]
        content=result[6]
        tags=result[7]
        if not tags:
            tags=''
        litpic=result[8]
        if not litpic:
            litpic=''
        allzhuban=result[9]
        if not allzhuban:
            allzhuban=''
        hz_categorylist=result[10]
        redircturl=result[13]
        if not redircturl:
            redircturl=''
        if not hz_categorylist:
            hz_categorylist=''
    return render_to_response('exhibit/add.html',locals())

def add_save(request):
    exhibit_id=request.POST.get("exhibit_id")
    zname=request.POST.get("zname")
    area=request.POST.get("area")
    start_time=request.POST.get("start_time")
    end_time=request.POST.get("end_time")
    plate_category_code=request.POST.get("plate_category_code")
    exhibit_category_code=request.POST.get("exhibit_category_code")
    content=request.POST.get("myEditor")
    tags=request.POST.get("tags")
    photo_cover=request.POST.get("litpic")
    allzhuban=request.POST.get("allzhuban")
    hz_categorylist=request.POST.getlist("hz_categorylist")
    redircturl=request.POST.get("redircturl")
    hzlist=''
    if hz_categorylist:
        for hz in hz_categorylist:
            hzlist+=hz+","
        hzlist=hzlist[0:len(hzlist)-1]
    gmt_created=gmt_modified=datetime.datetime.now()
    
    if exhibit_id:
        value=[zname,area,start_time,end_time,plate_category_code,exhibit_category_code,content,tags,photo_cover,allzhuban,str(hzlist),gmt_modified,redircturl,exhibit_id]
        sql="update exhibit set name=%s,area=%s,start_time=%s,end_time=%s,plate_category_code=%s,exhibit_category_code=%s,content=%s,tags=%s,photo_cover=%s,allzhuban=%s,hz_categorylist=%s,gmt_modified=%s,redircturl=%s where id=%s"
        dbc.updatetodb(sql,value)
    else:
        value=[zname,area,start_time,end_time,plate_category_code,exhibit_category_code,content,tags,photo_cover,allzhuban,str(hzlist),gmt_created,gmt_modified,redircturl]
        sql="insert into exhibit(name,area,start_time,end_time,plate_category_code,exhibit_category_code,content,tags,photo_cover,allzhuban,hz_categorylist,gmt_created,gmt_modified,redircturl) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        dbc.updatetodb(sql,value)
    return HttpResponseRedirect("/feiliao123/zh/list.html")
    
def zhupload(request):
    #piclist=otherimgupload(request)
    piclist=None
    if piclist:
        jsonresult={'err':'false','piclist':piclist}
        return HttpResponse(simplejson.dumps(jsonresult, ensure_ascii=False))
    else:
        jsonresult={'err':'true','errkey':'请选择一张图片'}
        return HttpResponse(simplejson.dumps(jsonresult, ensure_ascii=False))
    