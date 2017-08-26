#-*- coding:utf-8 -*-
from django.shortcuts import render_to_response,render
from django.http import HttpResponse,HttpResponseRedirect
import simplejson,sys,os,urllib,re,datetime,time,hashlib,random,calendar,socket
from django.core.handlers.wsgi import WSGIRequest
import calendar as cal
from zz91db_ast import companydb
from zz91page import *
from sphinxapi import *
import Image,ImageDraw,ImageFont,ImageFilter
try:
    import cStringIO as StringIO
except ImportError:
    import StringIO
from trade import otherimgupload
db=companydb(dict=1)
dbc=companydb()
reload(sys)
sys.setdefaultencoding('UTF-8')
nowpath=os.path.dirname(__file__)
execfile(nowpath+"/func/public_function.py")
execfile(nowpath+"/func/gd_function.py")
zzs=zzgd()
#所有工单
def gd_list(request):
    company_id = request.GET.get('company_id')
    usertoken=request.GET.get("usertoken")
    if not getloginstatus(company_id,usertoken):
        errlist={'tokenerr':'true'}
        return HttpResponse(simplejson.dumps(errlist, ensure_ascii=False))
    if not company_id or str(company_id)=="0":
        return HttpResponse("err")
    page=request.GET.get('page')
    if not page:
        page=1
    searchlist={}
    question_kind=request.GET.get("question_kind")
    if question_kind:
         searchlist['question_kind']=question_kind
    isviewflag=request.GET.get("isviewflag")
    if str(isviewflag)=="0":
         searchlist['isviewflag']=isviewflag
    compelete=request.GET.get('compelete')
    if compelete:
         searchlist['compelete']=compelete
    index=request.GET.get('index')
    if index:
        searchlist['index']=index
    if company_id:
        searchlist['company_id']=company_id
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
    list={'list':listall,'listcout':listcount}
    return HttpResponse(simplejson.dumps(list, ensure_ascii=False))
#我要回复
def gd_reply(request):
    host=getnowurl(request)
    username=request.session.get("username",None)
    company_id=request.session.get("company_id",None)
    if username and (company_id==None or str(company_id)=="0"):
        company_id=getcompanyid(username)
        request.session['company_id']=company_id
    if (username==None or (company_id==None or str(company_id)=="0")):
        return HttpResponseRedirect("/login/?done="+host)
    question_id=request.GET.get("question_id")
    return render_to_response('aui/help/gd_reply.html',locals())
#工单提交
def gd_save(request):
    company_id = request.POST.get('company_id')
    usertoken=request.POST.get("usertoken")
    if not getloginstatus(company_id,usertoken):
        errlist={'tokenerr':'true'}
        return HttpResponse(simplejson.dumps(errlist, ensure_ascii=False))
    if not company_id or str(company_id)=="0":
        return HttpResponse("err")
    content = request.POST.get('content')
    piclist=otherimgupload(request)
    gmt_created=datetime.datetime.now()
    gmt_modified=datetime.datetime.now()
    question_kind='1'
    if company_id and content:
        question_time=datetime.datetime.now()
        #内容里插入图片
        if piclist:
            for p in piclist:
                if p:
                    picurl=p['path']
                    # 获取文件名后缀
                    filetype=picurl.split(".")[-1]
                    if (filetype.lower() in ["mp4","mov","avi","3gp","3gp2","wav","rm","mpg","asf","mid"]):
                        content+='<br /><img src="../../image/video.png" path="'+picurl+'" class="videoframe" style="width:100px"><br />'
                    else:
                        content+='<br /><img src="'+picurl+'"><br />'
        sql='insert into gd_question(question,question_kind,file,company_id,question_time) values(%s, %s, %s,%s, %s)'
        result=dbc.updatetodb(sql,[content,question_kind,'',company_id,question_time])
        if result:
            postid=result[0]
            #保存图片
            if piclist:
                for p in piclist:
                    sql="update other_piclist set source_id=%s where id=%s"
                    dbc.updatetodb(sql,[postid,p['id']])
        messagedata={'err':'false','errkey':'','type':'gdpost'}
        return HttpResponse(simplejson.dumps(messagedata, ensure_ascii=False))
    else:
        messagedata={'err':'true','errkey':'请填写提问内容！','type':'gdpost'}
        return HttpResponse(simplejson.dumps(messagedata, ensure_ascii=False))
#回复提交
def gd_replysave(request):
    company_id = request.POST.get('company_id')
    usertoken=request.POST.get("usertoken")
    if not getloginstatus(company_id,usertoken):
        errlist={'tokenerr':'true'}
        return HttpResponse(simplejson.dumps(errlist, ensure_ascii=False))
    if not company_id or str(company_id)=="0":
        return HttpResponse("err")
    content=request.POST.get('content')
    question_kind='1'
    piclist=otherimgupload(request)
    gmt_created=datetime.datetime.now()
    gmt_modified=datetime.datetime.now()
    
    question_id=request.POST.get('question_id')
    compelete=request.POST.get('compelete')
    if company_id and content:
        answer_time=datetime.datetime.now()
        #内容里插入图片
        if piclist:
            for p in piclist:
                if p:
                    picurl=p['path']
                    # 获取文件名后缀
                    filetype=picurl.split(".")[-1]
                    if (filetype.lower() in ["mp4","mov","avi","3gp","3gp2","wav","rm","mpg","asf","mid"]):
                        content+='<br /><img src="../../image/video.png" path="'+picurl+'" class="videoframe" style="width:100px"><br />'
                    else:
                        content+='<br /><img src="'+picurl+'"><br />'
        sql='insert into gd_answer(company_id,question_id,answer,answer_time) values(%s, %s, %s,%s)'
        result=dbc.updatetodb(sql,[company_id,question_id,content,answer_time])
        if result:
            postid=result[0]
            #保存图片
            if piclist:
                for p in piclist:
                    sql="update other_piclist set source_id=%s where id=%s"
                    dbc.updatetodb(sql,[postid,p['id']])
        #更新问题状态
        sql="update gd_question set compelete=%s where id=%s"
        dbc.updatetodb(sql,[compelete,question_id])
        messagedata={'err':'false','errkey':'','type':'gdreply'}
        return HttpResponse(simplejson.dumps(messagedata, ensure_ascii=False))
    else:
        messagedata={'err':'true','errkey':'请填写回复内容！','type':'gdreply'}
        return HttpResponse(simplejson.dumps(messagedata, ensure_ascii=False))
#工单详情
def gd_details(request):
    company_id = request.GET.get('company_id')
    usertoken=request.GET.get("usertoken")
    if not getloginstatus(company_id,usertoken):
        errlist={'tokenerr':'true'}
        return HttpResponse(simplejson.dumps(errlist, ensure_ascii=False))
    if not company_id or str(company_id)=="0":
        return HttpResponse("err")
    id=request.GET.get('id')
    details=zzs.getgddetail(id=id,mycompany_id=company_id)
    sql="update gd_answer set isview=1 where question_id=%s"
    dbc.updatetodb(sql,[id])
    return HttpResponse(simplejson.dumps(details, ensure_ascii=False))
#未查看工单
def gd_noview(request):
    company_id = request.GET.get('company_id')
    usertoken=request.GET.get("usertoken")
    if not getloginstatus(company_id,usertoken):
        errlist={'tokenerr':'true'}
        return HttpResponse(simplejson.dumps(errlist, ensure_ascii=False))
    list={'noviewcount':0}
    #未读工单
    if company_id:
        sql="select count(0) from gd_question as a left join gd_answer as b on a.id=b.question_id where b.isview=0 and a.company_id=%s"
        result=dbc.fetchonedb(sql,[company_id])
        noviewanwer=result[0]
        list['noviewcount']=noviewanwer
    return HttpResponse(simplejson.dumps(list, ensure_ascii=False))
