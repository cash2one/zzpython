#-*- coding:utf-8 -*-
from django.shortcuts import render_to_response
from django.http import HttpResponse,HttpResponseRedirect
from zz91page import *
from zz91settings import SPHINXCONFIG,logpath
from zz91tools import formattime,getoptionlist,date_to_strall,date_to_str,filter_tags,int_to_strall
import os,datetime,time,re,urllib,md5,json,sys,random,hashlib
from django.core.cache import cache
from zz91db_ast import companydb
from zz91db_dacong import dacongdb
from zhuaqu.getnews2 import getonenews
from zhuaqu.getnews import get_img_url
from zhuaqu.simptools import imgpath
dcdb=dacongdb()
reload(sys)
sys.setdefaultencoding('UTF-8')
nowpath=os.path.dirname(__file__)
execfile(nowpath+"/func/dacong_function.py")
dcfunc=dacongfunc()
def dacongadd(request):
    typelist=dcfunc.gettypelist()
    username=request.session.get('username')
    if not username:
        return HttpResponseRedirect('login.html')
    weburl=request.GET.get("weburl")
    keywords=request.GET.get("keywords")
    request_url=request.META.get('HTTP_REFERER','/')
    listconf={}
    listconf['main_url']="http://mp.weixin.qq.com/"
    listconf['weixin']=1
    #listconf['list_url']="http://www.ys137.com/slys/xjys/list_31_1.html"
    #listconf['list_nextpage']=r'<li class="next-article">(.*?)</li></ul></nav>'
    
    listconf['re_title']=r'<title>(.*?)</title>'
    listconf['re_html']=r'<div class="msg_page" id="msg_page">(.*?)<div class="loading_wrapper loading" style="display: none;">'
    listconf['re_list']=r'<h4.*?msg_title.*? hrefs="([^"]+)".*?>([^"]+)</h4>'
    listconf['re_content']=r'<div class="rich_media_content " id="js_content">(.*?)<div class="rich_media_tool" id="js_toobar3">'
    #过滤内容
    #listconf['re_remove']=[r'<div class="article-sharedblock">(.*?)<ul class="article-list">',r'<div class="article-sharedblock">(.*?)</div>']
    listconf['re_encode']="utf8"
    #listconf['re_contentpage']=r'<div class="article_pager clearfix">(.*?)</ul>'
    listconf['re_contentpage']=None
    listconf['re_contentpagestr']=None
    listconf['re_contentpagenum']=None
    listconf['re_time']=r'<em id="post-date" class="rich_media_meta rich_media_meta_text">(.*?)</em>'
    
    #listconf['re_keywords']=r'<div class="tag_head">(.*?)</div>'
    listconf['keywords']='生活妙方'
    listconf['source']="微信"
    
    if weburl:
        listconf['keywords']=keywords
        typeid=request.GET.get("typeid")
        pic=request.GET.get("pic")
        cstyle=request.GET.get("cstyle")
        listconf['selectpic']=pic
        listconf['cstyle']=cstyle
        result=getonenews(typeid,1,weburl,listconf)
        if result:
            request_url=request.GET.get("request_url")
            return HttpResponseRedirect(request_url)
    return render_to_response('adminmobile/dacong_add.html',locals())
def dacong_view(request):
    id=request.GET.get("id")
    sql="select id,typeid,title,litpic,pubdate,keywords,flag,arcrank from dede_archives where id=%s"
    result=dcdb.fetchonedb(sql,[id])
    if result:
        typeid=result[1]
        title=result[2]
        litpic=result[3]
        pubdate=result[4]
        keywords=result[5]
        flag=result[6]
        arcrank=result[7]
    sql="select body from dede_addonarticle where aid=%s"
    result=dcdb.fetchonedb(sql,[id])
    if result:
        content=result[0]
    return render_to_response('adminmobile/dacong_view.html',locals())
def daconglist(request):
    username=request.session.get('username')
    if not username:
        return HttpResponseRedirect('login.html')
    page=request.GET.get('page')
    arcrank=request.GET.get('arcrank')
    ptype=request.GET.get('ptype')
    searchlist={}
    if arcrank:
        searchlist['arcrank']=arcrank
    if ptype:
        searchlist['ptype']=ptype
    searchurl=urllib.urlencode(searchlist)
    if not page:
        page=1
    funpage=zz91page()
    limitNum=funpage.limitNum(5)
    nowpage=funpage.nowpage(int(page))
    frompageCount=funpage.frompageCount()
    after_range_num = funpage.after_range_num(3)
    before_range_num = funpage.before_range_num(6)
    messagelist=dcfunc.getnewslist(frompageCount,limitNum,ptype=ptype,arcrank=arcrank)
    listcount=0
    listall=messagelist['list']
    listcount=messagelist['count']
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
    return render_to_response('adminmobile/dacong_list.html',locals())
def editcontent(request):
    username=request.session.get('username')
    if not username:
        return HttpResponseRedirect('login.html')
    id=request.GET.get("id")
    sql="select body from dede_addonarticle where aid=%s"
    result=dcdb.fetchonedb(sql,[id])
    if result:
        content=result[0]
    return render_to_response('adminmobile/dacong_content.html',locals())
def editnews(request):
    username=request.session.get('username')
    if not username:
        return HttpResponseRedirect('login.html')
    id=request.GET.get("id")
    request_url=request.META.get('HTTP_REFERER','/')
    sql="select id,typeid,title,litpic,pubdate,keywords,flag,arcrank from dede_archives where id=%s"
    result=dcdb.fetchonedb(sql,[id])
    if result:
        typeid=result[1]
        title=result[2]
        litpic=result[3]
        pubdate=result[4]
        keywords=result[5]
        flag=result[6]
        arcrank=str(result[7])
    
    sql="select cstyle from dede_addonarticle where aid=%s"
    result=dcdb.fetchonedb(sql,[id])
    if result:
        cstyle=result[0]
    typelist=dcfunc.gettypelist()
    return render_to_response('adminmobile/dacong_edit.html',locals())
def dacong_delnews(request):
    username=request.session.get('username')
    if not username:
        return HttpResponseRedirect('login.html')
    id=request.POST.get("id")
    tablevalue = request.POST.get("tablevalue")
    sql="delete from dede_archives where id=%s"
    dcdb.updatetodb(sql,[id])
    sql="delete from dede_addonarticle where aid=%s"
    dcdb.updatetodb(sql,[id])
    sql="select aid,url from dede_uploads where arcid=%s"
    result=dcdb.fetchalldb(sql,[id])
    for list in result:
        pid=list[0]
        purl=list[1]
        if purl:
            purl=purl.replace("http://img.daconglaile.com/","")
            localpic=imgpath+purl
            if os.path.exists(localpic):
                if os.path.isfile(localpic):
                    #return file_full_path
                    os.remove(localpic)
            #os.system("rm "+localpic+"")
            sql="delete from dede_uploads where aid=%s"
            dcdb.updatetodb(sql,[pid])
    result={'err':'false','errkey':''}
    return HttpResponse(json.dumps(result, ensure_ascii=False))
def savecontent(request):
    username=request.session.get('username')
    if not username:
        return HttpResponseRedirect('login.html')
    id=request.POST.get("id")
    content=request.POST.get("content")
    sql="update dede_addonarticle set body=%s where aid=%s"
    dcdb.updatetodb(sql,[content,id])
    result={'err':'false','errkey':''}
    return HttpResponse(json.dumps(result, ensure_ascii=False))

def savenews(request):
    username=request.session.get('username')
    if not username:
        return HttpResponseRedirect('login.html')
    username=request.session.get('username')
    gmt_created=datetime.datetime.now()
    fild = request.POST.get("fild")
    fildvalue = request.POST.get("fildvalue")
    tablevalue = request.POST.get("tablevalue")
    id=request.POST.get("id")
    #选择第几张图片
    if fild=="litpic" and fildvalue:
        sql="select body from dede_addonarticle where aid=%s"
        result=dcdb.fetchonedb(sql,[id])
        if result:
            content=result[0]
            img_url=get_img_url(content)#获得新闻图片
            if img_url:
                img_urlone=None
                if len(img_url)>=1:
                    img_urlone=img_url[int(fildvalue)]
                    fildvalue=img_urlone
                else:
                    fildvalue=''
    #样式过滤还是保留
    if fild=="cstyle":
        sql="update dede_addonarticle set cstyle=%s where aid=%s"
        dcdb.updatetodb(sql,[fildvalue,id])
    else:
        sql="update "+str(tablevalue)+" set "+str(fild)+"=%s where id=%s"
        dcdb.updatetodb(sql,[fildvalue,id])
    #标签
    if fild=="keywords":
        if fildvalue:
            fildvalue=fildvalue.replace("，",",")
            arrkey=fildvalue.split(",")
            for k in arrkey:
                sql="select id from dede_tagindex where tag=%s"
                result=dcdb.fetchonedb(sql,[k])
                if not result:
                    sql="insert into dede_tagindex(tag) values(%s)"
                    dcdb.updatetodb(sql,[k])
    #有图无图
    if fild=="flag" and fildvalue=='':
        sql="update "+str(tablevalue)+" set litpic='' where id=%s"
        dcdb.updatetodb(sql,[id])
    result={'err':'false','errkey':''}
    return HttpResponse(json.dumps(result, ensure_ascii=False))
