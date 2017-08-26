#-*- coding:utf-8 -*-
from django.shortcuts import render_to_response,render
from django.http import HttpResponse,HttpResponseRedirect
import simplejson,sys,os,urllib,re,datetime,time,hashlib,random,calendar
from django.core.handlers.wsgi import WSGIRequest
import calendar as cal
from zz91db_ast import companydb
from zz91page import *
from zz91tools import formattime
from sphinxapi import *
db=companydb(dict=1)
reload(sys)
sys.setdefaultencoding('UTF-8')
nowpath=os.path.dirname(__file__)
execfile(nowpath+"/func/gd_function.py")
zzs=zzgd()
#所有工单
def gd_list(request):
    page=request.GET.get('page')
    if not page:
        page=1
    searchlist={}
    question_kind=request.GET.get("question_kind")
    if question_kind:
         searchlist['question_kind']=question_kind
    compelete=request.GET.get('compelete')
    if compelete:
         searchlist['compelete']=compelete
    index=request.GET.get('index')
    if index:
        searchlist['index']=index
    funpage=zz91page()
    limitNum=funpage.limitNum(10)
    nowpage=funpage.nowpage(int(page))
    frompageCount=funpage.frompageCount()
    after_range_num = funpage.after_range_num(3)
    before_range_num = funpage.before_range_num(6)
    userallr=zzs.getgdlist(frompageCount=frompageCount,limitNum=limitNum,searchlist=searchlist)
    listcount=userallr['count']
    listall=userallr['list']
    index=userallr['index']
    listcount = funpage.listcount(listcount)
    page_listcount=funpage.page_listcount()
    firstpage = funpage.firstpage()
    lastpage = funpage.lastpage()
    page_range  = funpage.page_range()
    nextpage = funpage.nextpage()
    prvpage = funpage.prvpage()
    return render_to_response('gd/gd_list.html',locals())


#工单详情
def gd_details(request):
    id=request.GET.get('id')
    if id:
        details=zzs.getgddetail(id=id)
    return render_to_response('gd/gd_details.html',locals())
#我要回复
def gd_reply(request):
    question_id=request.GET.get("question_id")
    return render_to_response('gd/gd_reply.html',locals())
#回复提交
def gd_replysave(request):
    company_id=0
    content=request.POST.get('content')
    question_kind='1'
    piclist=request.POST.get('piclist')
    question_id=request.POST.get('question_id')
    compelete=request.POST.get('compelete')
    if content:
        answer_time=datetime.datetime.now()
        #内容里插入图片
        if piclist:
            piclist=piclist.split(",")
            for p in piclist:
                if p:
                    pid=p
                    sql="select path from other_piclist where id=%s"
                    result=db.fetchonedb(sql,[pid])
                    if result:
                        picurl=result[0]
                        picurl="http://img3.zz91.com/300x15000/"+picurl
                        # 获取文件名后缀
                        filetype=picurl.split(".")[-1]
                        if (filetype.lower() in ["mp4","mov","avi","3gp","3gp2","wav","rm","mpg","asf","mid"]):
                            content+='<br /><img src="http://static.m.zz91.com/image/video.png" path="'+picurl+'" class="videoframe" style="width:100px"><br />'
                        else:
                            content+='<br /><img src="'+picurl+'"><br />'
        sql='insert into gd_answer(company_id,question_id,answer,answer_time) values(%s, %s, %s,%s)'
        result=db.updatetodb(sql,[company_id,question_id,content,answer_time])
        if result:
            postid=result['lastid']
            #保存图片
            if piclist:
                for p in piclist:
                    if p:
                        sql="update other_piclist set source_id=%s where id=%s"
                        db.updatetodb(sql,[postid,p])
        #更新问题状态
        sql="update gd_question set compelete=%s where id=%s"
        db.updatetodb(sql,[compelete,question_id])
        messagedata={'err':'false','errkey':'','type':'gdreply'}
        return HttpResponse(simplejson.dumps(messagedata, ensure_ascii=False))
    else:
        messagedata={'err':'true','errkey':'请填写回复内容！','type':'gdreply'}
        return HttpResponse(simplejson.dumps(messagedata, ensure_ascii=False))
#工单状态
def gd_station(request):
    id=request.GET.get('id')
    compelete=request.GET.get('compelete')
    if id:
        sqls='update gd_question set compelete=%s where id=%s'
        result=db.updatetodb(sqls,[compelete,id])
    return HttpResponseRedirect('list_com.html')
