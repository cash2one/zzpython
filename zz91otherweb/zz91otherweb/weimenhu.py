#-*- coding:utf-8 -*-
from django.shortcuts import render_to_response
from django.http import HttpResponse,HttpResponseRedirect
from zz91page import *
from zz91conn import database_mongodb
from zz91db_ast import companydb
from zz91db_zzlog import zzlogdb
from zz91db_work import workdb
from zz91settings import SPHINXCONFIG,logpath
from zz91tools import formattime
import time,urllib,sys,os,datetime,xlwt,re
from time import strftime, localtime
from datetime import timedelta, date,datetime
dbc=companydb()
dblog=zzlogdb()
dbwork=workdb()
reload(sys)
sys.setdefaultencoding('UTF-8')
nowpath=os.path.dirname(__file__)
execfile(nowpath+"/func/weimenhu_function.py")
from pinyin import chinese_abstract
wmh=weimenhu()

#-----所有关键词
def key_list(request):
    username=request.session.get("username",None)
    if not username:
        return HttpResponseRedirect("/feiliao123/loginpage.html")
    page=request.GET.get('page')
    ptype=request.GET.get('ptype')
    keywords=request.GET.get('keywords')
    pinyin=request.GET.get('pinyin')
    searchlist={}
    if not ptype:
        ptype=0
    if ptype:
        searchlist['ptype']=ptype
    if keywords:
        searchlist['keywords']=keywords
    if pinyin:
        searchlist['pinyin']=pinyin
    searchurl=urllib.urlencode(searchlist)
    if not page:
        page=1
    funpage=zz91page()
    limitNum=funpage.limitNum(20)
    nowpage=funpage.nowpage(int(page))
    frompageCount=funpage.frompageCount()
    after_range_num = funpage.after_range_num(3)
    before_range_num = funpage.before_range_num(6)
    keywordslist= wmh.listallkeywords(frompageCount,limitNum,ptype=ptype,keywords=keywords,pinyin=pinyin)
    listcount=0
    listall=keywordslist['list']
    listcount=keywordslist['count']
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
    return render_to_response('weimenhu/key_list.html',locals())
#审核统计
def key_tongji(request):
    username=request.session.get("username",None)
    if not username:
        return HttpResponseRedirect("/feiliao123/loginpage.html")
    page=request.GET.get('page')
    gmt_begin=request.GET.get('gmt_begin')
    gmt_end=request.GET.get('gmt_end')
    searchlist={}
    if gmt_begin:
        searchlist['gmt_begin']=gmt_begin
    if gmt_end:
        searchlist['gmt_end']=gmt_end
    searchurl=urllib.urlencode(searchlist)
    if not page:
        page=1
    funpage=zz91page()
    limitNum=funpage.limitNum(20)
    nowpage=funpage.nowpage(int(page))
    frompageCount=funpage.frompageCount()
    after_range_num = funpage.after_range_num(3)
    before_range_num = funpage.before_range_num(6)
    tongjilist= wmh.gettongjiweimenhu(frompageCount,limitNum,gmt_begin,gmt_end)
    listcount=0
    listall=tongjilist['list']
    listcount=tongjilist['count']
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
    return render_to_response('weimenhu/key_tongji.html',locals())
#-----所有关键词
def key_list_del(request):
    page=request.GET.get('page')
    ptype=request.GET.get('ptype')
    keywords=request.GET.get('keywords')
    pinyin=request.GET.get('pinyin')
    searchlist={}
    if not ptype:
        ptype=0
    if ptype:
        searchlist['ptype']=ptype
    if keywords:
        searchlist['keywords']=keywords
    if pinyin:
        searchlist['pinyin']=pinyin
    searchurl=urllib.urlencode(searchlist)
    if not page:
        page=1
    funpage=zz91page()
    limitNum=funpage.limitNum(20)
    nowpage=funpage.nowpage(int(page))
    frompageCount=funpage.frompageCount()
    after_range_num = funpage.after_range_num(3)
    before_range_num = funpage.before_range_num(6)
    keywordslist= wmh.listallkeywords_del(frompageCount,limitNum,ptype=ptype,keywords=keywords,pinyin=pinyin)
    listcount=0
    listall=keywordslist['list']
    listcount=keywordslist['count']
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
    return render_to_response('weimenhu/key_list_del.html',locals())
#修改关键词
def key_mod(request):
    id=request.GET.get("id")
    if id:
        request_url=request.META.get('HTTP_REFERER','/')
        sql="select label,keywords from daohang where id=%s"
        result=dbc.fetchonedb(sql,[id])
        if result:
            label=result[0]
            keywords=result[1]
            if not keywords:
                keywords=''
        else:
            return HttpResponse('err')
    return render_to_response('weimenhu/key_mod.html',locals())
def key_save(request):
    id=request.GET.get("id")
    keywords=request.POST.get("keywords")
    label=request.POST.get("label")
    sql="select id from daohang where label=%s and id>%s and id<%s"
    result=dbc.fetchonedb(sql,[label,id,id])
    if not result:
        pinyin=chinese_abstract(label.decode('utf-8','ignore'))
        sql="update daohang set label=%s,keywords=%s,pingyin=%s where id=%s"
        dbc.updatetodb(sql,[label,keywords,pinyin,id])
    else:
        return HttpResponse('你修改的关键词已经存在！')
    request_url=request.POST.get("request_url")
    return HttpResponseRedirect(request_url)
#----微门户关键词导入
def key_daoru(request):
    return render_to_response('weimenhu/key_daoru.html',locals())
def key_listsave(request):
    keywordslist=request.POST.get('keywordslist')
    gmt_created=datetime.datetime.now()
    if keywordslist:
        arrkeywordslist=keywordslist.split(",")
        arrkeywordslist=keywordslist.split("\r\n")
        for list in arrkeywordslist:
            keywords=list
            if keywords:
                kw=keywords
                kw=kw.replace(" ","").strip()
                kw=kw.replace(",","")
                if kw and kw!="" and len(kw)<=12 and len(kw)>=2:
                    pinyin=chinese_abstract(kw.decode('utf-8','ignore'))
                    sqlc="select pingyin from daohang where pingyin=%s"
                    result=dbc.fetchonedb(sqlc,[pinyin])
                    if not result:
                        sqld="select pingyin from daohang_del where pingyin=%s"
                        resultd=dbc.fetchonedb(sqld,[pinyin])
                        if not resultd:
                            print pinyin
                            sqld="insert into daohang(type,sid,label,pingyin) values(%s,%s,%s,%s)"
                            dbc.updatetodb(sqld,[1,3738,kw,pinyin])
    return HttpResponseRedirect('key_list.html')
def huifu_ok_all(request):
    checkid=request.GET.getlist('checkid')
    for id in checkid:
        sql="insert into daohang select * from daohang_del where id=%s and not exists(select id from daohang where id=daohang_del.id)"
        dbc.updatetodb(sql,[id])
        sql="delete from daohang_del where id=%s"
        dbc.updatetodb(sql,[id])
    request_url=request.META.get('HTTP_REFERER','/')
    return HttpResponseRedirect(request_url)

def shenhe_ok(request):
    username=request.session.get("username",None)
    if not username:
        return HttpResponseRedirect("/feiliao123/loginpage.html")
    k_id=request.GET.get('id')
    wmh.shenheok(k_id=k_id,request=request)
    request_url=request.META.get('HTTP_REFERER','/')
    return HttpResponseRedirect(request_url)

def shenhe_no(request):
    username=request.session.get("username",None)
    if not username:
        return HttpResponseRedirect("/feiliao123/loginpage.html")
    k_id=request.GET.get('id')
    wmh.shenheno(k_id=k_id)
    request_url=request.META.get('HTTP_REFERER','/')
    return HttpResponseRedirect(request_url)

def delthis(request):
    username=request.session.get("username",None)
    if not username:
        return HttpResponseRedirect("/feiliao123/loginpage.html")
    request_url=request.META.get('HTTP_REFERER','/')
    k_id=request.GET.get('id')
    sql='delete from daohang where id=%s'
    dbc.updatetodb(sql,k_id)
    wmh.checkweimenhu(request,keyid=k_id,dotype=1)
    return HttpResponseRedirect(request_url)
#一键审核
def shenhe_ok_all(request):
    username=request.session.get("username",None)
    if not username:
        return HttpResponseRedirect("/feiliao123/loginpage.html")
    checkid=request.GET.getlist('checkid')
    wmh.shenheokall(checkid,request=request)
    request_url=request.META.get('HTTP_REFERER','/')
    return HttpResponseRedirect(request_url)
#一键删除1
def del_all1(request):
    username=request.session.get("username",None)
    if not username:
        return HttpResponseRedirect("/feiliao123/loginpage.html")
    checkid=request.GET.getlist('checkid')
    wmh.delall1(checkid,request=request)
    request_url=request.META.get('HTTP_REFERER','/')
    return HttpResponseRedirect(request_url)


#------未审核客户搜索关键字
def key_nocheck(request):
    page=request.GET.get('page')
    ptype=request.GET.get('ptype')
    keywords=request.GET.get('keywords')
    if not ptype:
        ptype=0
    searchlist={}
    if ptype:
        searchlist['ptype']=ptype
    if keywords:
        searchlist['keywords']=keywords
    searchurl=urllib.urlencode(searchlist)
    if not page:
        page=1
    funpage=zz91page()
    limitNum=funpage.limitNum(20)
    nowpage=funpage.nowpage(int(page))
    frompageCount=funpage.frompageCount()
    after_range_num = funpage.after_range_num(3)
    before_range_num = funpage.before_range_num(6)
    keywordslist= wmh.getnocheckedkeywords(frompageCount,limitNum,ptype=ptype,keywords=keywords)
    listcount=0
    listall=keywordslist['list']
    listcount=keywordslist['count']
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
    return render_to_response('weimenhu/key_nocheck.html',locals())
#状态已审
def status_ok(request):
    username=request.session.get("username",None)
    if not username:
        return HttpResponseRedirect("/feiliao123/loginpage.html")
    k_id=request.GET.get('id')
    wmh.statusok(k_id=k_id)
    request_url=request.META.get('HTTP_REFERER','/')
    return HttpResponseRedirect(request_url)
#状态未审
def status_no(request):
    username=request.session.get("username",None)
    if not username:
        return HttpResponseRedirect("/feiliao123/loginpage.html")
    k_id=request.GET.get('id')
    wmh.statusno(k_id=k_id)
    request_url=request.META.get('HTTP_REFERER','/')
    return HttpResponseRedirect(request_url)
#删除
def del_this(request):
    request_url=request.META.get('HTTP_REFERER','/')
    k_id=request.GET.get('id')
    sql='delete from analysis_trade_keywords where id=%s'
    dbc.updatetodb(sql,k_id)
    return HttpResponseRedirect(request_url)

###############################
#推送至所有关键词,执行推送时默认审核通过
def pushtype1(request):
    checkid=request.GET.getlist('checkid')
    suc=wmh.addbbs_post_invite(checkid)
    #return HttpResponse(checkid)
    request_url=request.META.get('HTTP_REFERER','/')
    return HttpResponseRedirect(request_url)

#一键审核2
def shenhe_ok_all2(request):
    checkid=request.GET.getlist('checkid')
    wmh.shenheokall2(checkid)
    request_url=request.META.get('HTTP_REFERER','/')
    return HttpResponseRedirect(request_url)
#一键删除2
def del_all2(request):
    checkid=request.GET.getlist('checkid')
    wmh.delall2(checkid)
    request_url=request.META.get('HTTP_REFERER','/')
    return HttpResponseRedirect(request_url)
#导出回收站数据(按时间)
def deleted_keywords_export(request):
    gmt_begin=request.GET.get('gmt_begin')
    gmt_end=request.GET.get('gmt_end')
    listall=''
    dpubdate=''
    dpubdate2=''
    if gmt_begin:
        dpubdate=datetime.datetime.strptime(gmt_begin+' 00:00:00',"%Y-%m-%d %H:%M:%S")
    if gmt_end:
        dpubdate2=datetime.datetime.strptime(gmt_end+' 00:00:00',"%Y-%m-%d %H:%M:%S")
    if dpubdate and dpubdate2:
        resultall=wmh.export_datalist(dpubdate,dpubdate2)
    if resultall:
        wb =xlwt.Workbook()
        ws = wb.add_sheet(u'Sheetname')
        style_k=xlwt.easyxf('align: wrap off')
        ws.col(0).width = 0x0d00 + 1000
        ws.col(1).width = 0x0d00 + 8000
        ws.col(2).width = 0x0d00 + 8000
        ws.col(3).width = 0x0d00 + 8000
        ws.col(4).width = 0x0d00 + 8000
        ws.col(5).width = 0x0d00 + 8000
        ws.col(6).width = 0x0d00 + 8000
        ws.col(7).width = 0x0d00 + 8000
        ws.col(8).width = 0x0d00 + 8000
        ws.col(9).width = 0x0d00 + 8000
        ws.col(10).width = 0x0d00 + 8000
        ws.col(11).width = 0x0d00 + 8000
        
        
        ws.write(0, 0, u'id')
        ws.write(0, 1, u'关键词')
        ws.write(0, 2, u'拼音')
        ws.write(0, 3, u'首页')
        ws.write(0, 4, u'价格页')
        ws.write(0, 5, u'价格更多页')
        ws.write(0, 6, u'公司页')
        ws.write(0, 7, u'公司更多页')
        ws.write(0, 8, u'采购页')
        ws.write(0, 9, u'供求页')
        ws.write(0, 10, u'日期')
        ws.write(0, 11, u'状态')
        
        js=0
        newsurl=''
        for result in resultall:
            id=str(result['id']).decode('UTF-8')
            label=str(result['label']).decode('UTF-8')
            pingyin=str(result['pingyin']).decode('UTF-8')
            url_index=str(result['url_index']).decode('UTF-8')
            url_price=str(result['url_price']).decode('UTF-8')
            url_pricemore=str(result['url_pricemore']).decode('UTF-8')
            url_company=str(result['url_company']).decode('UTF-8')
            url_companymore=str(result['url_companymore']).decode('UTF-8')
            url_caigou=str(result['url_caigou']).decode('UTF-8')
            url_gongqiu=str(result['url_gongqiu']).decode('UTF-8')
            gmt_created=str(result['gmt_created']).decode('UTF-8')
            checktxt=str(result['checktxt']).decode('UTF-8')
            js=js+1
            ws.write(js, 0, id)
            ws.write(js, 1, label)
            ws.write(js, 2, pingyin)
            ws.write(js, 3, url_index)
            ws.write(js, 4, url_price)
            ws.write(js, 5, url_pricemore)
            ws.write(js, 6, url_company)
            ws.write(js, 7, url_companymore)
            ws.write(js, 8, url_caigou)
            ws.write(js, 9, url_gongqiu)
            ws.write(js, 10, gmt_created)
            ws.write(js, 11, checktxt)
        export_time=time.strftime('%Y-%m-%d_%H:%M:%S')
        fname = export_time+'.xls'
        agent=request.META.get('HTTP_USER_AGENT') 
        if agent and re.search('MSIE',agent):
            response =HttpResponse(content_type="application/vnd.ms-excel") #解决ie不能下载的问题
            response['Content-Disposition'] ='attachment; filename=%s' % fname #解决文件名乱码/不显示的问题
        else:
            response =HttpResponse(content_type="application/vnd.ms-excel")#解决ie不能下载的问题
            response['Content-Disposition'] ='attachment; filename=%s' % fname #解决文件名乱码/不显示的问题
        wb.save(response)
        return response
    return HttpResponse('无数据')


def export_who_selected(request):
    checkid=request.GET.getlist('checkid')
    if checkid:
        resultall=wmh.getselectexport(checkid)
        if resultall:
            wb =xlwt.Workbook()
            ws = wb.add_sheet(u'Sheetname')
            style_k=xlwt.easyxf('align: wrap off')
            ws.col(0).width = 0x0d00 + 1000
            ws.col(1).width = 0x0d00 + 8000
            ws.col(2).width = 0x0d00 + 8000
            ws.col(3).width = 0x0d00 + 8000
            ws.col(4).width = 0x0d00 + 8000
            ws.col(5).width = 0x0d00 + 8000
            ws.col(6).width = 0x0d00 + 8000
            ws.col(7).width = 0x0d00 + 8000
            ws.col(8).width = 0x0d00 + 8000
            ws.col(9).width = 0x0d00 + 8000
            ws.col(10).width = 0x0d00 + 8000
            ws.col(11).width = 0x0d00 + 8000
            
            
            ws.write(0, 0, u'id')
            ws.write(0, 1, u'拼音')
            ws.write(0, 2, u'关键词')
            ws.write(0, 3, u'首页')
            ws.write(0, 4, u'价格页')
            ws.write(0, 5, u'价格更多页')
            ws.write(0, 6, u'公司页')
            ws.write(0, 7, u'公司更多页')
            ws.write(0, 8, u'采购页')
            ws.write(0, 9, u'供求页')
            ws.write(0, 10, u'日期')
            ws.write(0, 11, u'状态')
            
            js=0
            newsurl=''
            for result in resultall:
                id=str(result['id']).decode('UTF-8')
                label=str(result['label']).decode('UTF-8')
                pingyin=str(result['pingyin']).decode('UTF-8')
                url_index=str(result['url_index']).decode('UTF-8')
                url_price=str(result['url_price']).decode('UTF-8')
                url_pricemore=str(result['url_pricemore']).decode('UTF-8')
                url_company=str(result['url_company']).decode('UTF-8')
                url_companymore=str(result['url_companymore']).decode('UTF-8')
                url_caigou=str(result['url_caigou']).decode('UTF-8')
                url_gongqiu=str(result['url_gongqiu']).decode('UTF-8')
                gmt_created=str(result['gmt_created']).decode('UTF-8')
                checktxt=str(result['checktxt']).decode('UTF-8')
                js=js+1
                ws.write(js, 0, id)
                ws.write(js, 1, label)
                ws.write(js, 2, pingyin)
                ws.write(js, 3, url_index)
                ws.write(js, 4, url_price)
                ws.write(js, 5, url_pricemore)
                ws.write(js, 6, url_company)
                ws.write(js, 7, url_companymore)
                ws.write(js, 8, url_caigou)
                ws.write(js, 9, url_gongqiu)
                ws.write(js, 10, gmt_created)
                ws.write(js, 11, checktxt)
            export_time=time.strftime('%Y-%m-%d_%H:%M:%S')
            fname = export_time+'.xls'
            agent=request.META.get('HTTP_USER_AGENT') 
            if agent and re.search('MSIE',agent):
                response =HttpResponse(content_type="application/vnd.ms-excel") #解决ie不能下载的问题
                response['Content-Disposition'] ='attachment; filename=%s' % fname #解决文件名乱码/不显示的问题
            else:
                response =HttpResponse(content_type="application/vnd.ms-excel")#解决ie不能下载的问题
                response['Content-Disposition'] ='attachment; filename=%s' % fname #解决文件名乱码/不显示的问题
            wb.save(response)
            return response
    return HttpResponse('无数据hbfghaskiau ')


