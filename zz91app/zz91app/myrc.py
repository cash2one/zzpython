#-*- coding:utf-8 -*-
from django.shortcuts import render_to_response
import simplejson
from django.http import HttpResponse,HttpResponseRedirect,HttpResponsePermanentRedirect
import MySQLdb,sys,os,memcache,settings,urllib,re,datetime,time,random,hashlib
from django.core.cache import cache
from zz91db_ast import companydb
from zz91db_2_news import newsdb
from zz91conn import database_mongodb
from zz91tools import int_to_strall,formattime
from settings import spconfig,appurl
from datetime import timedelta,date
from sphinxapi import *
from zz91page import *
from trade import otherimgupload
dbc=companydb()
dbn=newsdb()
reload(sys)
sys.setdefaultencoding('UTF-8')
nowpath=os.path.dirname(__file__)
execfile(nowpath+"/func/public_function.py")
execfile(nowpath+"/func/qianbao_function.py")
execfile(nowpath+"/func/message_function.py")
execfile(nowpath+"/func/myrc_function.py")
execfile(nowpath+"/func/weixin_function.py")
execfile(nowpath+"/func/ldb_weixin_function.py")
execfile(nowpath+"/func/company_function.py")
execfile(nowpath+"/func/price_function.py")

zzm=zmyrc()
zzw=zzweixin()
zzq=zzqianbao()
zzms=zzmessage()
dbmongo=database_mongodb()
zzldb=ldbweixin()
zzc=zzcompany()
zzprice=zprice()
#生意管家---------------------------------------
def myrc_index(request):
    myrc=1
    webtitle="生意管家"
    company_id=request.GET.get("company_id")
    usertoken=request.GET.get("usertoken")
    appsystem=request.GET.get("appsystem")
    if not getloginstatus(company_id,usertoken):
        errlist={'tokenerr':'true'}
        return HttpResponse(simplejson.dumps(errlist, ensure_ascii=False))
    if not company_id or str(company_id)=="0":
        return HttpResponse("err")
    #判断是否拉黑
    sqlh="select id from company where id=%s and is_block=1"
    listh=dbc.fetchonedb(sqlh,[company_id]);
    if listh:
        error="该用户已经被禁止登录！"
        messagedata={'err':'true','errkey':error,'result':company_id,'token':''}
        return HttpResponse(simplejson.dumps(messagedata, ensure_ascii=False))
    completeflag={'text':'','showflag':0}
    faceurl=None
    sql="select picture_path from bbs_user_profiler where company_id=%s"
    piclist=dbc.fetchonedb(sql,[company_id])
    faceurl=None
    if piclist:
        if piclist[0]:
            faceurl="http://img3.zz91.com/100x100/"+piclist[0]
    if not faceurl:
       completeflag['text']="请上传您的头像！"
       completeflag['showflag']=1
    """
    account=zzm.getcompanyaccount(company_id)
    sql1="select count(0) from inquiry where receiver_account=%s and is_viewed=0"
    result1=dbc.fetchonedb(sql1,[account])
    leavewordscount=None
    if result1:
        leavewordscount=result1[0]
        if leavewordscount==0:
            leavewordscount=None
    """
    #是否来电宝
    ldbjtl=None
    ldbvalue=getldbphone(company_id)
    paymoney=10
    if not ldbvalue:
        #----余额
        blance=zzq.getqianbaoblance(company_id)
        #留言量
        qcount=zzms.getnoviewmessagecount(company_id,1)
    else:
        blancelist=zzldb.getldbbalance(company_id)
        if blancelist:
            blance=blancelist['lave']
        qcount=0
        #接听率
        ldbjtl=zzldb.getnowmonthstate(company_id)
        #看联系方式价格
        paymoney=zzldb.getldbonephonemoney(company_id)
    #是否企业秀
    isqiyexiu=zzq.getisqiyexiu(company_id)
    #是否签到
    gmt_date=datetime.date.today()
    qiandao=None
    if not ldbvalue:
        sql="select id from app_qiandao where company_id=%s and gmt_date=%s"
        result=dbc.fetchonedb(sql,[company_id,gmt_date])
        if result:
            qiandao=1
        else:
            qiandao=None
    sqlc="select industry_code,business,area_code,address,name from company where id=%s"
    result=dbc.fetchonedb(sqlc,[company_id])
    if result:
        industry_code=result[0]
        business=result[1]
        area_code=result[2]
        address=result[3]
        companyname=result[4]
        if not industry_code or not business or not area_code or not address:
            completeflag['text']="填写完善获得更优质服务！"
            completeflag['showflag']=1
    if company_id:
        sql="select company_id,account,contact,sex,mobile,qq from company_account where company_id=%s"
        listc=dbc.fetchonedb(sql,[company_id])
        if listc:
            company_id=listc[0]
            contact=listc[2]
            sex=listc[3]
            mobile=listc[4]
            qq=listc[5]
            if not qq:
               completeflag['text']="请QQ号码！"
               completeflag['showflag']=1
            if str(sex)=="0":
                if ("先生" not in contact):
                    contact+="先生"
            if str(sex)=="1":
                if ("女士" not in contact):
                    contact+="女士"
        else:
            list={'err':'true','errkey':'请重新登录！'}
            return HttpResponse(simplejson.dumps(list, ensure_ascii=False))
        zxinfo=zzc.getcxinfo(company_id)
        zxclose=None
        #销售助理信息
        cslist=''
        sql="select cs_account from crm_cs where company_id=%s"
        result=dbc.fetchonedb(sql,[company_id])
        if result:
            cs_account=result[0]
            if cs_account:
                sql="select value from param where types='cs_info' and param.key=%s"
                result1=dbc.fetchonedb(sql,[cs_account])
                if result1:
                    value=result1[0]
                    if value:
                        valuelist=value.split(",")
                        csname=valuelist[0]
                        cstel=valuelist[1]
                        cslist={'name':csname,'tel':cstel}
        list={'err':'false','errkey':'','contact':contact,'blance':blance,'qcount':qcount,'ldbvalue':ldbvalue,'paymoney':paymoney,'qiandao':qiandao,'faceurl':faceurl,'mobile':mobile,'ldbjtl':ldbjtl,'completeflag':completeflag,'zxinfo':zxinfo,'zxclose':zxclose,'isqiyexiu':isqiyexiu,'companyname':companyname,'cslist':cslist}
        #未读工单信息
        sql="select count(0) from gd_question as a left join gd_answer as b on a.id=b.question_id where b.isview=0 and a.company_id=%s"
        result=dbc.fetchonedb(sql,[company_id])
        noviewanwer=result[0]
        list['noviewcount']=noviewanwer
    else:
        list={'err':'true','errkey':'请重新登录！'}
    
    ##返回json数据
    return HttpResponse(simplejson.dumps(list, ensure_ascii=False))
#----我的社区
def myrc_mycommunity(request):
    webtitle="消息中心"
    nowlanmu="<a href='/myrc_index/'>生意管家</a>"
    company_id=request.GET.get("company_id")
    usertoken=request.GET.get("usertoken")
    appsystem=request.GET.get("appsystem")
    if not getloginstatus(company_id,usertoken):
        errlist={'tokenerr':'true'}
        return HttpResponse(simplejson.dumps(errlist, ensure_ascii=False))
    if not company_id or str(company_id)=="0":
        return HttpResponse("err")
    account=zzm.getcompanyaccount(company_id)
    """
    #----更新弹窗
    zzm.updateopenfloat(company_id,1);
    #判断是否已经填写了昵称
    mynickname=zzm.getcompanynickname(company_id)
    if not mynickname or mynickname=="":
        nickname=request.GET.get("nickname")
        if nickname:
            addcompanynickname(nickname,company_id,username)
    #判断是否填写关注行业
    myguanzhu=zzm.gethuzhuguanzhu(company_id)
    if not myguanzhu or myguanzhu=="":
        myguanzhu=request.REQUEST.getlist("myguanzhu")
        if myguanzhu:
            zzm.addmyzhuzhuguanzhu(myguanzhu,company_id,username)
    """
    invitelist=zzm.getbbs_invite(company_id)
    if invitelist:
        invitecount=len(invitelist)
    else:
        invitecount=0
        
    #huzhureply=zzm.getmessgelist(company_id,0,10)
    #if huzhureply:
        #listall=huzhureply['list']
        #replycount=int(huzhureply['count'])+invitecount
    
    page=request.GET.get("page")
    if (page==None):
        page=1
    funpage = zz91page()
    limitNum=funpage.limitNum(5)
    nowpage=funpage.nowpage(int(page))
    frompageCount=funpage.frompageCount()
    after_range_num = funpage.after_range_num(2)
    before_range_num = funpage.before_range_num(9)
    qlistall=zzm.getmessgelist(company_id,frompageCount,limitNum)
    listall=qlistall['list']
    listcount=qlistall['count']
    replycount=int(listcount)+invitecount
    if (int(listcount)>100000):
        listcount=100000
    listcount = funpage.listcount(listcount)
    page_listcount=funpage.page_listcount()
    firstpage = funpage.firstpage()
    lastpage = funpage.lastpage()
    page_range  = funpage.page_range()
    nextpage = funpage.nextpage()
    prvpage = funpage.prvpage()
    ##返回json数据
    datatype=request.GET.get("datatype")
    if datatype=="json":
        jsonlist={'qlistall':qlistall,'invitelist':invitelist,'pagecount':page_listcount}
        return HttpResponse(simplejson.dumps(jsonlist, ensure_ascii=False))
    return render_to_response('myrc/mycommunity.html',locals())
#
def myrc_mycommunitydel(request):
    pid=request.POST.get("pid")
    company_id=request.POST.get("company_id")
    usertoken=request.POST.get("usertoken")
    if not getloginstatus(company_id,usertoken):
        errlist={'tokenerr':'true'}
        return HttpResponse(simplejson.dumps(errlist, ensure_ascii=False))
    
    if not company_id or str(company_id)=="0":
        return HttpResponse("err")
    ptype=request.POST.get("ptype")
    post_id=request.POST.get("post_id")
    gmt_created=gmt_modified=datetime.datetime.now()
    messagedata=""
    if ptype=="invitedel":
        sql="select id from bbs_invite where id=%s"
        returnone=dbc.fetchonedb(sql,[pid])
        if returnone:
            sql="update bbs_invite set is_del=1 and answercheck=3 where id=%s"
            dbc.updatetodb(sql,[pid])
        else:
            sql="insert into bbs_invite(post_id,company_id,is_del,answercheck,gmt_created) values(%s,%s,%s,%s,%s)"
            dbc.updatetodb(sql,[post_id,company_id,1,3,gmt_created])
        messagedata={'err':'false','errkey':'','type':'mycommunitydel'}
    return HttpResponse(simplejson.dumps(messagedata, ensure_ascii=False))
def myrc_mypostsave(request):
    company_id=request.session.get("company_id",None)
    username=request.session.get("username",None)
    return HttpResponse("suc")

def myrc_myreplysave(request):
    pid=request.GET.get("pid")
    ptype=request.GET.get("ptype")
    company_id=request.GET.get("company_id")
    usertoken=request.GET.get("usertoken")
    if not getloginstatus(company_id,usertoken):
        errlist={'tokenerr':'true'}
        return HttpResponse(simplejson.dumps(errlist, ensure_ascii=False))
    if not company_id or str(company_id)=="0":
        return HttpResponse("err")
    username=request.session.get("username",None)
    if username and company_id==None:
        company_id=getcompanyid(username)
        request.session['company_id']=company_id
    if (username==None or company_id==None):
        return HttpResponseRedirect("/login/")
    
    tocompany_id=request.GET.get("tocompany_id")
    account=getcompanyaccount(company_id)
    bbs_post_id=request.GET.get("post_id")
    title="回复:"+getbbspost_title(bbs_post_id)
    content=request.GET.get("replycontent")
    check_status=1
    gmt_created=gmt_modified=datetime.datetime.now()
    if ptype=="invitereply":
        valu=[company_id,account,title,tocompany_id,bbs_post_id,content,check_status,gmt_created,gmt_modified,1]
        sql="insert into bbs_post_reply(company_id,account,title,tocompany_id,bbs_post_id,content,check_status,gmt_created,gmt_modified,postsource) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        cursor.execute(sql,valu)
    if ptype=="postreply":
        valu=[company_id,account,title,tocompany_id,bbs_post_id,content,check_status,gmt_created,gmt_modified,pid,1]
        sql="insert into bbs_post_reply(company_id,account,title,tocompany_id,bbs_post_id,content,check_status,gmt_created,gmt_modified,bbs_post_reply_id,postsource) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        cursor.execute(sql,valu)
    #加入通信录
    if tocompany_id:
        zzc.joinaddressbook(company_id,tocompany_id)
    updatepostviewed(tocompany_id,bbs_post_id)
    #----更新弹窗
    updateopenfloat(tocompany_id,0)
    sql="update bbs_post set reply_time=%s,reply_count=reply_count+1,gmt_modified=%s where id=%s"
    cursor.execute(sql,[gmt_modified,gmt_modified,bbs_post_id])
    return HttpResponse("suc")

#-我的提问
def myrc_mypost(request):
    webtitle="我的提问"
    nowlanmu="<a href='/myrc_index/'>生意管家</a>"
    company_id=request.GET.get("company_id")
    usertoken=request.GET.get("usertoken")
    appsystem=request.GET.get("appsystem")
    if not getloginstatus(company_id,usertoken):
        errlist={'tokenerr':'true'}
        return HttpResponse(simplejson.dumps(errlist, ensure_ascii=False))
    #account=zzm.getcompanyaccount(company_id)
    if not company_id or str(company_id)=="0":
        return HttpResponse("err")
    page=request.GET.get("page")
    if (page==None):
        page=1
    funpage = zz91page()
    limitNum=funpage.limitNum(5)
    nowpage=funpage.nowpage(int(page))
    frompageCount=funpage.frompageCount()
    after_range_num = funpage.after_range_num(2)
    before_range_num = funpage.before_range_num(9)
    qlistall=zzm.getmyquestion(company_id,frompageCount,limitNum)
    listall=qlistall['list']
    listcount=qlistall['count']

    if (int(listcount)>100000):
        listcount=100000
    listcount = funpage.listcount(listcount)
    page_listcount=funpage.page_listcount()
    firstpage = funpage.firstpage()
    lastpage = funpage.lastpage()
    page_range  = funpage.page_range()
    nextpage = funpage.nextpage()
    prvpage = funpage.prvpage()
    ##返回json数据
    datatype=request.GET.get("datatype")
    if datatype=="json":
        return HttpResponse(simplejson.dumps({'list':qlistall,'pagecount':page_listcount}, ensure_ascii=False))
    return render_to_response('myrc/mypost.html',locals())
#-我的关注
def myrc_myguanzhu(request):
    webtitle="我的提问"
    nowlanmu="<a href='/myrc_index/'>生意管家</a>"
    company_id=request.GET.get("company_id")
    usertoken=request.GET.get("usertoken")
    appsystem=request.GET.get("appsystem")
    if not getloginstatus(company_id,usertoken):
        errlist={'tokenerr':'true'}
        return HttpResponse(simplejson.dumps(errlist, ensure_ascii=False))
    #account=zzm.getcompanyaccount(company_id)
    if not company_id or str(company_id)=="0":
        return HttpResponse("err")
    page=request.GET.get("page")
    if (page==None):
        page=1
    funpage = zz91page()
    limitNum=funpage.limitNum(5)
    nowpage=funpage.nowpage(int(page))
    frompageCount=funpage.frompageCount()
    after_range_num = funpage.after_range_num(2)
    before_range_num = funpage.before_range_num(9)
    qlistall=zzm.getmygaunzhu(company_id,frompageCount,limitNum)
    listall=qlistall['list']
    listcount=qlistall['count']

    if (int(listcount)>100000):
        listcount=100000
    listcount = funpage.listcount(listcount)
    page_listcount=funpage.page_listcount()
    firstpage = funpage.firstpage()
    lastpage = funpage.lastpage()
    page_range  = funpage.page_range()
    nextpage = funpage.nextpage()
    prvpage = funpage.prvpage()
    ##返回json数据
    datatype=request.GET.get("datatype")
    if datatype=="json":
        return HttpResponse(simplejson.dumps({'list':qlistall,'pagecount':page_listcount}, ensure_ascii=False))
    return render_to_response('myrc/mypost.html',locals())
#我的回复
def myrc_myreply(request):
    webtitle="我的回复"
    nowlanmu="<a href='/myrc_index/'>生意管家</a>"
    company_id=request.GET.get("company_id")
    usertoken=request.GET.get("usertoken")
    appsystem=request.GET.get("appsystem")
    if not getloginstatus(company_id,usertoken):
        errlist={'tokenerr':'true'}
        return HttpResponse(simplejson.dumps(errlist, ensure_ascii=False))
    if not company_id or str(company_id)=="0":
        return HttpResponse("err")
    page=request.GET.get("page")
    if (page==None):
        page=1
    funpage = zz91page()
    limitNum=funpage.limitNum(5)
    nowpage=funpage.nowpage(int(page))
    frompageCount=funpage.frompageCount()
    after_range_num = funpage.after_range_num(2)
    before_range_num = funpage.before_range_num(9)
    qlistall=zzm.getmyreply(company_id,frompageCount,limitNum)
    listall=qlistall['list']
    listcount=qlistall['count']

    if (int(listcount)>100000):
        listcount=100000
    listcount = funpage.listcount(listcount)
    page_listcount=funpage.page_listcount()
    firstpage = funpage.firstpage()
    lastpage = funpage.lastpage()
    page_range  = funpage.page_range()
    nextpage = funpage.nextpage()
    prvpage = funpage.prvpage()
    ##返回json数据
    datatype=request.GET.get("datatype")
    if datatype=="json":
        return HttpResponse(simplejson.dumps({'list':qlistall,'pagecount':page_listcount}, ensure_ascii=False))
    return render_to_response('myrc/myreply.html',locals())

#---刷新供求
def products_refresh(request):
    gmt_created=datetime.datetime.now()
    proid=request.POST.get("proid")
        
    company_id=request.POST.get("company_id")
    usertoken=request.POST.get("usertoken")
    if not getloginstatus(company_id,usertoken):
        errlist={'tokenerr':'true'}
        return HttpResponse(simplejson.dumps(errlist, ensure_ascii=False))
    if not company_id or str(company_id)=="0":
        return HttpResponse("err")
    if proid=="0" or proid==None:
        messagedata={'err':'true','errkey':'请选择一条供求刷新'}
    else:
        messagedata={'err':'false','errkey':'','type':'proreflush'}
        sql="update products set refresh_time=%s,gmt_modified=%s where id in ("+str(proid)+") and company_id = %s"
        dbc.updatetodb(sql,[gmt_created,gmt_created,company_id])
        
    return HttpResponse(simplejson.dumps(messagedata, ensure_ascii=False))
#---刷新供求
def products_refreshall(request):
    gmt_created=datetime.datetime.now()
    company_id=request.POST.get("company_id")
    usertoken=request.POST.get("usertoken")
    if not getloginstatus(company_id,usertoken):
        errlist={'tokenerr':'true'}
        return HttpResponse(simplejson.dumps(errlist, ensure_ascii=False))
    if not company_id:
        company_id=request.POST.get("company_id")
    if company_id=="0" or company_id==None:
        messagedata={'err':'true','errkey':'系统错误'}
    else:
        messagedata={'err':'false','errkey':'','type':'proreflush'}
        sql="update products set refresh_time=%s,gmt_modified=%s where company_id = %s and check_status='1'"
        dbc.updatetodb(sql,[gmt_created,gmt_created,company_id])
    return HttpResponse(simplejson.dumps(messagedata, ensure_ascii=False))
#---暂不发布
def products_stop(request):
    gmt_created=datetime.datetime.now()
    proid=request.POST.get("proid")
    company_id=request.POST.get("company_id")
    usertoken=request.POST.get("usertoken")
    if not getloginstatus(company_id,usertoken):
        errlist={'tokenerr':'true'}
        return HttpResponse(simplejson.dumps(errlist, ensure_ascii=False))
    if not company_id or str(company_id)=="0":
        return HttpResponse("err")
    if proid=="0" or proid==None:
        messagedata={'err':'true','errkey':'请选择一条供求'}
    else:
        messagedata={'err':'false','errkey':'','type':'prostop'}
        sql="update products set is_pause=1,gmt_modified=%s where id in ("+str(proid)+") and company_id = %s"
        dbc.updatetodb(sql,[gmt_created,company_id])
        
    return HttpResponse(simplejson.dumps(messagedata, ensure_ascii=False))
#---重新发布
def products_start(request):
    gmt_created=datetime.datetime.now()
    proid=request.POST.get("proid")
    company_id=request.POST.get("company_id")
    usertoken=request.POST.get("usertoken")
    appsystem=request.POST.get("appsystem")
    if not getloginstatus(company_id,usertoken):
        errlist={'tokenerr':'true'}
        return HttpResponse(simplejson.dumps(errlist, ensure_ascii=False))
    if not company_id or str(company_id)=="0":
        return HttpResponse("err")
    if proid=="0" or proid==None:
        messagedata={'err':'true','errkey':'请选择一条供求信息后操作！'}
    else:
        messagedata={'err':'false','errkey':'','type':'prorestart'}
        sql="update products set is_pause=0,gmt_modified=%s where id in ("+str(proid)+") and company_id = %s"
        dbc.updatetodb(sql,[gmt_created,company_id])
        
    return HttpResponse(simplejson.dumps(messagedata, ensure_ascii=False))
#定制首页(一期)
def orderindex(request):
    host=getnowurl(request)
    company_id=request.GET.get("company_id")
    usertoken=request.GET.get("usertoken")
    appsystem=request.GET.get("appsystem")
    if not getloginstatus(company_id,usertoken) and appsystem=="Android":
        return HttpResponse("nologin")
    if not company_id or str(company_id)=="0":
        return HttpResponse("err")
    return render_to_response('order/index.html',locals())
#商机定制
def orderbusiness(request):
    host=getnowurl(request)
    ordercategorylist=zzm.getordercategorylistmain()
    company_id=request.GET.get("company_id")
    usertoken=request.GET.get("usertoken")
    appsystem=request.GET.get("appsystem")
    if not getloginstatus(company_id,usertoken):
        errlist={'tokenerr':'true'}
        return HttpResponse(simplejson.dumps(errlist, ensure_ascii=False))
    if not company_id or str(company_id)=="0":
        return HttpResponse("err")
    if company_id:
        mybusinesscollect=zzm.get_mybusinesscollectid(company_id)
        listall=[]
        for li in ordercategorylist:
            childlist=li['childlist']
            listall1=[]
            parentcheck=0
            for list in childlist:
                list1={'title':list['title'],'id':list['id']}
                id=list['id']
                if str(id) in mybusinesscollect:
                    list1['selected']=1
                    parentcheck=1
                listall1.append(list1)
            list2={'code':li['code'],'label':li['label'],'childlist':listall1}
            if parentcheck==1:
                list2['selected']=1
            listall.append(list2)
        ordercategorylist=listall
    #返回json数据
    datatype=request.GET.get("datatype")
    if datatype=="json":
        return HttpResponse(simplejson.dumps(ordercategorylist, ensure_ascii=False))
    return render_to_response('order/business.html',locals())
#新版app行情定制
def myorderprice(request):
    host=getnowurl(request)
    company_id=request.POST.get("company_id")
    usertoken=request.POST.get("usertoken")
    if not getloginstatus(company_id,usertoken):
        messagedata={'err':'false','errkey':'','type':'mycollect','listall':None}
        return HttpResponse(simplejson.dumps(messagedata, ensure_ascii=False))
    appsystem=request.POST.get("appsystem")
    datatype=request.POST.get("datatype")
    if company_id:
        mypriceorderlist=zzm.getmyorderprice(company_id)
        if datatype=="json":
            if mypriceorderlist==[]:
                myprice=None
            else:
                myprice=mypriceorderlist
            messagedata={'err':'false','errkey':'','type':'mycollect','listall':myprice}
            return HttpResponse(simplejson.dumps(messagedata, ensure_ascii=False))
#新版app行情定制保存
def myorderprice_save(request):
    company_id=request.POST.get("company_id")
    usertoken=request.POST.get("usertoken")
    if not getloginstatus(company_id,usertoken):
        errlist={'tokenerr':'true'}
        return HttpResponse(simplejson.dumps(errlist, ensure_ascii=False))
    appsystem=request.POST.get("appsystem")
    datatype=request.POST.get("datatype")
    label=request.POST.get("label")
    category_id=request.POST.get("category_id")
    assist_id=request.POST.get("assist_id")
    keywords=request.POST.get("keywords")
    if not company_id:
        company_id=request.GET.get("company_id")
        label=request.GET.get("label")
        category_id=request.GET.get("category_id")
        assist_id=request.GET.get("assist_id")
        keywords=request.GET.get("keywords")
    list={
          'label':label,
          'company_id':company_id,
          'category_id':category_id,
          'assist_id':assist_id,
          'keywords':keywords}
    result=zzm.savemyorderprice(list)
    if result:
        messagedata={'err':'false','errkey':'','type':'savecollect','orderid':result}
    else:
        messagedata={'err':'true','errkey':'已经添加','type':'savecollect'}
    return HttpResponse(simplejson.dumps(messagedata, ensure_ascii=False))
#新版 app 删除定制
def myorderprice_del(request):
    company_id=request.GET.get("company_id")
    usertoken=request.GET.get("usertoken")
    """
    if not getloginstatus(company_id,usertoken):
        errlist={'tokenerr':'true'}
        return HttpResponse(simplejson.dumps(errlist, ensure_ascii=False))
    """
    appsystem=request.GET.get("appsystem")
    datatype=request.GET.get("datatype")
    orderid=request.GET.get("orderid")
    sql="delete from app_order_price where id=%s and company_id=%s"
    result=dbc.updatetodb(sql,[orderid,company_id])
    if result:
        messagedata={'err':'false','errkey':'','type':'delcollect','orderid':result}
    else:
        messagedata={'err':'true','errkey':'已经添加','type':'delcollect'}
    return HttpResponse(simplejson.dumps(messagedata, ensure_ascii=False))
#新版app 我的供求定制
def myordertrade(request):
    company_id=request.GET.get("company_id")
    usertoken=request.GET.get("usertoken")
    if not getloginstatus(company_id,usertoken):
        errlist={'tokenerr':'true'}
        return HttpResponse(simplejson.dumps(errlist, ensure_ascii=False))
    appsystem=request.GET.get("appsystem")
    datatype=request.GET.get("datatype")
    result=zzm.getmyordertrade(company_id)
    messagedata={'err':'false','errkey':'','type':'mycollect','listall':result}
    return HttpResponse(simplejson.dumps(messagedata, ensure_ascii=False))
#新版app 供求定制
def myordertrade_save(request):
    company_id=request.POST.get("company_id")
    usertoken=request.POST.get("usertoken")
    if not getloginstatus(company_id,usertoken):
        errlist={'tokenerr':'true'}
        return HttpResponse(simplejson.dumps(errlist, ensure_ascii=False))
    appsystem=request.POST.get("appsystem")
    datatype=request.POST.get("datatype")
    otype=request.POST.get("otype")
    timelimit=request.POST.get("timelimit")
    keywordslist=request.POST.get("keywordslist")
    provincelist=request.POST.get("provincelist")
    list={
          'otype':otype,
          'company_id':company_id,
          'timelimit':timelimit,
          'keywordslist':keywordslist,
          'provincelist':provincelist}
    result=zzm.savemyordertrade(list)
    messagedata={'err':'false','errkey':'','type':'savecollect','orderid':result}
    return HttpResponse(simplejson.dumps(messagedata, ensure_ascii=False))

#行情定制
def orderprice(request):
    host=getnowurl(request)
    company_id=request.GET.get("company_id")
    usertoken=request.GET.get("usertoken")
    if not getloginstatus(company_id,usertoken):
        errlist={'tokenerr':'true'}
        return HttpResponse(simplejson.dumps(errlist, ensure_ascii=False))
    appsystem=request.GET.get("appsystem")
    datatype=request.GET.get("datatype")
    if not getloginstatus(company_id,usertoken) and appsystem=="Android":
        return HttpResponse("nologin")
    if not company_id or str(company_id)=="0":
        return HttpResponse("err")
    if company_id:
        mypricecollect=zzm.get_mypricecollectid(company_id)
        if datatype=="json":
            jsonlist={'listall':mypricecollect}
            return HttpResponse(simplejson.dumps(jsonlist, ensure_ascii=False))
        category1=[40,328,41,45,44,47,43,48,51,279,46,308,206,69,70,71,72,79,80,81,210,83,84,86,208,32,33,216]
        category2=[40,328,41,45,44,47,43,48,51,279,46,308,206,69,70,71,72]
        
        sql="select name,id from price_category where parent_id='1' and showflag=1"
        alist = dbc.fetchalldb(sql)
        if alist:
            listall=[]
            for a in alist:
                id=a[1]
                sql="select name,id from price_category where parent_id=%s and showflag=1"
                blist = dbc.fetchalldb(sql,[id])
                if blist:
                    listb=[]
                    parentcheck2=None
                    for bl in blist:
                        idb=bl[1]
                        sql="select name,id from price_category where parent_id=%s and showflag=1"
                        clist = dbc.fetchalldb(sql,[idb])
                        if clist:
                            listc=[]
                            parentcheck1=None
                            for cl in clist:
                                idc=cl[1]
                                namec=cl[0]
                                if str(idc) in mypricecollect:
                                    checkflag=1
                                    parentcheck1=1
                                    parentcheck2=1
                                else:
                                    checkflag=None
                                list_c={'id':idc,'name':namec,'checked':checkflag}
                                listc.append(list_c)
                        nameb=bl[0]
                        if clist:
                            list_b={'id':idb,'name':nameb,'checked':parentcheck1}
                            list_b['listc']=listc
                            listb.append(list_b)
                name=a[0]
                #childmemu=zzm.getcate(id)
                if listb:
                    list={'id':id,'name':name,'checked':parentcheck2}
                    list['listb']=listb
                    listall.append(list)
            #返回json数据
            
            if datatype=="json":
                jsonlist={'listall':listall,'alist':alist}
                return HttpResponse(simplejson.dumps(jsonlist, ensure_ascii=False))
    return render_to_response('order/price.html',locals())
#保存定制
def save_collect(request):
    host=getnowurl(request)
    #获取定制类型,1是商机,2是行情
    collect_type=request.POST.get('collect_type')
    company_id=request.POST.get("company_id")
    usertoken=request.POST.get("usertoken")
    if not getloginstatus(company_id,usertoken):
        errlist={'tokenerr':'true'}
        return HttpResponse(simplejson.dumps(errlist, ensure_ascii=False))
    if not company_id or str(company_id)=="0":
        return HttpResponse("err")
    #获取定制信息
    #customp=request.POST.getlist('ordervalue')
    ordervalue=request.POST.get('ordervalue')
    ordervaluelist=request.POST.get('ordervaluelist')
    llist=ordervalue
    #for l in ordervalue:
        #llist=llist+","+l
    #llist=llist[1:]
    gmt_created=datetime.datetime.now()
        #保存定制信息进入数据库
    if ordervaluelist or ordervalue:
        zzm.savecollect(company_id,llist,gmt_created,collect_type,keywordslist=ordervaluelist)
    else:
        zzm.savecollect(company_id,"",gmt_created,collect_type,keywordslist="")
    messagedata={'err':'false','errkey':'','type':'savecollect'}
    return HttpResponse(simplejson.dumps(messagedata, ensure_ascii=False))

#我的定制
def myrc_collect(request):
    
    webtitle="我的定制商机"
    company_id=request.GET.get("company_id")
    usertoken=request.GET.get("usertoken")
    if not getloginstatus(company_id,usertoken):
        errlist={'tokenerr':'true'}
        return HttpResponse(simplejson.dumps(errlist, ensure_ascii=False))
    appsystem=request.GET.get("appsystem")
    if not getloginstatus(company_id,usertoken) and appsystem=="Android":
        return HttpResponse("nologin")
    if not company_id or str(company_id)=="0":
        return HttpResponse("err")
    #获得商机定制信息
    mybusinesscollect=zzm.get_mybusinesscollect(company_id)
    mypricecollect=zzm.get_mypricecollect(company_id)
    #返回json数据
    datatype=request.GET.get("datatype")
    if datatype=="json":
        jsonlist={'mybusinesscollect':mybusinesscollect,'mypricecollect':mypricecollect}
        return HttpResponse(simplejson.dumps(jsonlist, ensure_ascii=False))
    return render_to_response('myrc/myrc_collect2.html',locals())
#我的定制
def myrc_collectprice(request):
    webtitle="我的行情定制"
    company_id=request.GET.get("company_id")
    usertoken=request.GET.get("usertoken")
    if not getloginstatus(company_id,usertoken):
        errlist={'tokenerr':'true'}
        return HttpResponse(simplejson.dumps(errlist, ensure_ascii=False))
    appsystem=request.GET.get("appsystem")
    if not getloginstatus(company_id,usertoken) and appsystem=="Android":
        return HttpResponse("nologin")
    if not company_id or str(company_id)=="0":
        return HttpResponse("err")
    #获得商机定制信息
    mypricecollect=zzm.get_mypricecollect(company_id)
    #返回json数据
    datatype=request.GET.get("datatype")
    if datatype=="json":
        return HttpResponse(simplejson.dumps(mypricecollect, ensure_ascii=False))
    return render_to_response('myrc/myrc_collect3.html',locals())
#我的定制
def myrc_collectmain(request):
    webtitle="我的定制商机"
    company_id=request.GET.get("company_id")
    usertoken=request.GET.get("usertoken")
    if not getloginstatus(company_id,usertoken):
        errlist={'tokenerr':'true'}
        return HttpResponse(simplejson.dumps(errlist, ensure_ascii=False))
    appsystem=request.GET.get("appsystem")
    if not getloginstatus(company_id,usertoken) and appsystem=="Android":
        return HttpResponse("nologin")
    if not company_id or str(company_id)=="0":
        return HttpResponse("err")
    weixinautologin(request,request.GET.get("weixinid"))
    if (company_id==None):
        return HttpResponseRedirect("/login/?done=/myrc_collectmain/")
    #获得商机定制信息
    #mybusinesscollect=get_mybusinesscollect(company_id)
    #mypricecollect=get_mypricecollect(company_id)
    return render_to_response('myrc/myrc_collectmain.html',locals())
#我的询盘
def myrc_leavewords(request):
    webtitle="生意管家"
    nowlanmu="<a href='/myrc_index/'>生意管家</a>"
    
    sendtype=request.GET.get("sendtype")
    if sendtype==None:
        sendtype="0"
    company_id=request.GET.get("company_id")
    usertoken=request.GET.get("usertoken")
    appsystem=request.GET.get("appsystem")
    if not getloginstatus(company_id,usertoken):
        errlist={'tokenerr':'true'}
        return HttpResponse(simplejson.dumps(errlist, ensure_ascii=False))
    if not company_id or str(company_id)=="0":
        return HttpResponse("err")
    #----更新已读
    zzms.updatemessagesall(company_id)
    page=request.GET.get("page")
    if (page==None):
        page=1
    funpage = zz91page()
    limitNum=funpage.limitNum(5)
    nowpage=funpage.nowpage(int(page))
    frompageCount=funpage.frompageCount()
    after_range_num = funpage.after_range_num(2)
    before_range_num = funpage.before_range_num(9)
    #qlistall=zzm.getleavewordslist(frompageCount,limitNum,company_id,str(sendtype))
    qlistall=zzm.getchatlist(frompageCount,limitNum,company_id,str(sendtype))
    qlist=qlistall['list']
    qlistcount=qlistall['count']
    listcount=qlistcount
    if (int(listcount)>100000):
        listcount=100000
    listcount = funpage.listcount(listcount)
    page_listcount=funpage.page_listcount()
    firstpage = funpage.firstpage()
    lastpage = funpage.lastpage()
    page_range  = funpage.page_range()
    nextpage = funpage.nextpage()
    prvpage = funpage.prvpage()
    #返回json数据
    datatype=request.GET.get("datatype")
    if datatype=="json":
        return HttpResponse(simplejson.dumps(qlistall, ensure_ascii=False))
    return render_to_response('myrc/leavewords.html',locals())

def myrc_backquestion(request):
    webtitle="留言回复"
    nowlanmu="<a href='/myrc_index/'>生意管家</a>"
    company_id=request.GET.get("company_id")
    usertoken=request.GET.get("usertoken")
    appsystem=request.GET.get("appsystem")
    if not getloginstatus(company_id,usertoken):
        errlist={'tokenerr':'true'}
        return HttpResponse(simplejson.dumps(errlist, ensure_ascii=False))
    if not company_id or str(company_id)=="0":
        return HttpResponse("err")
    account=zzm.getcompanyaccount(company_id)
    
    sendcompany_id=request.GET.get("sendcom_id")
    inquired_id=request.GET.get("inquired_id")

    sendflag=0
    if str(sendcompany_id)!=str(company_id):
        sendflag=1
    
    #getupdatelookquestion(inquired_id)
    qlist=zzm.getleavewords(inquired_id)
    #返回json数据
    datatype=request.GET.get("datatype")
    if datatype=="json":
        jsonlist={"sendflag":sendflag,'qlist':qlist}
        return HttpResponse(simplejson.dumps(jsonlist, ensure_ascii=False))
    return render_to_response('myrc/backquestion.html',locals())

def myrc_backquestionsave(request):
    webtitle="留言回复"
    nowlanmu="<a href='/myrc_index/'>生意管家</a>"
    company_id=request.POST.get("company_id")
    usertoken=request.POST.get("usertoken")
    if not getloginstatus(company_id,usertoken):
        errlist={'tokenerr':'true'}
        return HttpResponse(simplejson.dumps(errlist, ensure_ascii=False))
    if not company_id or str(company_id)=="0":
        return HttpResponse("err")
    account=zzm.getcompanyaccount(company_id)
    
    send_username=account
    send_company_id=company_id
    
    re_company_id = request.POST.get('sendcompany_id')
    
    title='我对贵公司的产品感兴趣！'
    content = request.POST.get('content')
    
    if content=="":
        messagedata={'err':'true','errkey':'请填写回复的内容！','type':'questionback'}
        return HttpResponse(simplejson.dumps(messagedata, ensure_ascii=False))
    
    be_inquired_type=2
    be_inquired_id=request.POST.get('be_inquired_id')
    inquired_type=0
    inquired_id=request.POST.get('inquired_id')
    sender_account=send_username
    receiver_account=zzm.getcompanyaccount(re_company_id)
    #return HttpResponse(receiver_account)
    #加入通信录
    if re_company_id:
        zzc.joinaddressbook(company_id,re_company_id)
    send_time=datetime.datetime.now()
    gmt_created=datetime.datetime.now()
    gmt_modified=datetime.datetime.now()
    value=[title,content,be_inquired_type,be_inquired_id,inquired_type,sender_account,receiver_account,send_time,gmt_created,gmt_modified,inquired_id]
    sql="insert into inquiry(title,content,be_inquired_type,be_inquired_id,inquired_type,sender_account,receiver_account,send_time,gmt_created,gmt_modified,inquired_id) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
    dbc.updatetodb(sql,value)
    #----更新弹窗
    #updateopenfloat(re_company_id,0)
    messagedata={'err':'false','errkey':'回复成功','type':'questionback'}
    return HttpResponse(simplejson.dumps(messagedata, ensure_ascii=False))
#我的企业报价
def myrc_companyprice(request):
    company_id=request.GET.get("company_id")
    usertoken=request.GET.get("usertoken")
    appsystem=request.GET.get("appsystem")
    if not getloginstatus(company_id,usertoken):
        errlist={'tokenerr':'true'}
        return HttpResponse(simplejson.dumps(errlist, ensure_ascii=False))
    #company_id=1310082
    if not company_id or str(company_id)=="0":
        return HttpResponse("err")
    is_checked=request.GET.get("is_checked")
    
    page=request.GET.get("page")
    if (page==None):
        page=1
    funpage = zz91page()
    limitNum=funpage.limitNum(20)
    nowpage=funpage.nowpage(int(page))
    frompageCount=funpage.frompageCount()
    after_range_num = funpage.after_range_num(2)
    before_range_num = funpage.before_range_num(9)
    qlistall=zzm.mycompanyprice(frompageCount=frompageCount,limitNum=limitNum,company_id=company_id,is_checked=is_checked)
    qlist=qlistall['list']
    qlistcount=qlistall['count']
    listcount=qlistcount
    if (int(listcount)>100000):
        listcount=100000
    listcount = funpage.listcount(listcount)
    page_listcount=funpage.page_listcount()
    firstpage = funpage.firstpage()
    lastpage = funpage.lastpage()
    page_range  = funpage.page_range()
    nextpage = funpage.nextpage()
    prvpage = funpage.prvpage()
    list={'list':qlist,'pagecount':page_listcount}
    return HttpResponse(simplejson.dumps(list, ensure_ascii=False))

#企业报价修改
def myrc_companyprice_edit(request):
    id=request.GET.get("id")
    detail=zzprice.getcompanyprice_detail(id)
    return HttpResponse(simplejson.dumps(detail, ensure_ascii=False))
def myrc_companyprice_save(request):
    company_id=request.POST.get("company_id")
    usertoken=request.POST.get("usertoken")
    if not getloginstatus(company_id,usertoken):
        errlist={'tokenerr':'true'}
        return HttpResponse(simplejson.dumps(errlist, ensure_ascii=False))
    id=request.POST.get("id")
    appsystem=request.POST.get("appsystem")
    category_company_price_code=request.POST.get("category_company_price_code")
    title=request.POST.get("title")
    min_price=request.POST.get("min_price")
    max_price=request.POST.get("max_price")
    price_unit=request.POST.get("price_unit")
    area_code=request.POST.get("area_code")
    details=request.POST.get("details")
    is_checked=0
    post_time=gmt_created=gmt_modified=datetime.datetime.now()
    qpic="http://img0.zz91.com/zz91/images/indexLogo.png"
    sql="update company_price set category_company_price_code=%s,title=%s,min_price=%s,max_price=%s,price_unit=%s,area_code=%s,details=%s,is_checked=%s,gmt_modified=%s where id=%s"
    result=dbc.updatetodb(sql,[category_company_price_code,title,min_price,max_price,price_unit,area_code,details,is_checked,gmt_modified,id])
    if result:
        messagedata={'err':'false','errkey':'','type':'pricesave'}
    else:
        messagedata={'err':'true','errkey':'系统错误，请重试'}
    return HttpResponse(simplejson.dumps(messagedata, ensure_ascii=False))
#我的收藏夹
def myrc_favorite(request):
    webtitle="生意管家"
    nowlanmu="<a href='/myrc_index/'>生意管家</a>"
    company_id=request.GET.get("company_id")
    usertoken=request.GET.get("usertoken")
    appsystem=request.GET.get("appsystem")
    if not getloginstatus(company_id,usertoken):
        errlist={'tokenerr':'true'}
        return HttpResponse(simplejson.dumps(errlist, ensure_ascii=False))
    #company_id=1310082
    if not company_id or str(company_id)=="0":
        return HttpResponse("err")
    checkStatus=request.GET.get("checkStatus")
    if (checkStatus=="" or checkStatus==None):
        checkStatus=1
    
    page=request.GET.get("page")
    if (page==None):
        page=1
    funpage = zz91page()
    limitNum=funpage.limitNum(20)
    nowpage=funpage.nowpage(int(page))
    frompageCount=funpage.frompageCount()
    after_range_num = funpage.after_range_num(2)
    before_range_num = funpage.before_range_num(9)
    qlistall=zzm.getfavoritelist(frompageCount=frompageCount,limitNum=limitNum,company_id=company_id,checkStatus=checkStatus)
    qlist=qlistall['list']
    qlistcount=qlistall['count']
    listcount=qlistcount
    if (int(listcount)>100000):
        listcount=100000
    listcount = funpage.listcount(listcount)
    page_listcount=funpage.page_listcount()
    firstpage = funpage.firstpage()
    lastpage = funpage.lastpage()
    page_range  = funpage.page_range()
    nextpage = funpage.nextpage()
    prvpage = funpage.prvpage()
    """
    #供求信息数量
    sql1="select count(0) from myfavorite where company_id=%s and (favorite_type_code=10091006 or favorite_type_code=10091000 or favorite_type_code=10091001 or favorite_type_code=10091007 )"                                            
    result1=dbc.fetchonedb(sql1,[company_id])
    if result1:
        alist1=result1[0]
    #公司信息数量    
    sql2="select count(0) from myfavorite where company_id=%s and (favorite_type_code=10091002 or favorite_type_code=10091003 or favorite_type_code=10091004) "
    result2=dbc.fetchonedb(sql2,[company_id])
    if result2:
        alist2=result2[0]
    #报价信息数量    
    sql3="select count(0) from myfavorite where company_id=%s and favorite_type_code=10091004 "
    result3=dbc.fetchonedb(sql3,[company_id])
    if result3:
        alist3=result3[0]
    #互助社区数量
    sql4="select count(0) from myfavorite where company_id=%s and favorite_type_code=10091005 "
    result4=dbc.fetchonedb(sql4,[company_id])
    if result4:
        alist4=result4[0]
    #资讯中心数量
    sql5="select count(0) from myfavorite where company_id=%s and favorite_type_code=10091012 "
    result5=dbc.fetchonedb(sql5,[company_id])
    if result5:
        alist5=result5[0]   
    """
    if page>1:
        #返回json数据
        datatype=request.GET.get("datatype")
        if datatype=="json":
            return HttpResponse(simplejson.dumps({'list':qlistall,'pagecount':page_listcount}, ensure_ascii=False))
        return render_to_response('myrc/favorite_more.html',locals())
    #返回json数据
    datatype=request.GET.get("datatype")
    if datatype=="json":
        return HttpResponse(simplejson.dumps(qlistall, ensure_ascii=False))
    return render_to_response('myrc/favorite.html',locals())

def del_favorite(request):
    company_id=request.POST.get("company_id")
    usertoken=request.POST.get("usertoken")
    if not getloginstatus(company_id,usertoken):
        errlist={'tokenerr':'true'}
        return HttpResponse(simplejson.dumps(errlist, ensure_ascii=False))
    id=request.POST.get("id")
    if not company_id:
        company_id=request.GET.get("company_id")
        id=request.GET.get("id")
    usertoken=request.GET.get("usertoken")
    appsystem=request.GET.get("appsystem")
    if not getloginstatus(company_id,usertoken):
        return HttpResponse("nologin")
    if not company_id or str(company_id)=="0":
        return HttpResponse("err")
    sql="delete from myfavorite where id=%s and company_id=%s"
    dbc.updatetodb(sql,[id,company_id])
    messagedata={'err':'false','errkey':'删除成功','type':'favorite'}
    return HttpResponse(simplejson.dumps(messagedata, ensure_ascii=False))

#---生意管家 我的供求信息
def myrc_products(request):
    webtitle="生意管家"
    nowlanmu="<a href='/myrc_index/'>生意管家</a>"
    company_id=request.GET.get("company_id")
    usertoken=request.GET.get("usertoken")
    if not getloginstatus(company_id,usertoken):
        errlist={'tokenerr':'true'}
        return HttpResponse(simplejson.dumps(errlist, ensure_ascii=False))
    appsystem=request.GET.get("appsystem")
    if not company_id or str(company_id)=="0":
        return HttpResponse("err")
    page=request.GET.get("page")
    checkStatus=request.GET.get("checkStatus")
    if (checkStatus=="" or checkStatus==None):
        checkStatus=1
    if (page==None):
        page=1
    funpage = zz91page()
    limitNum=funpage.limitNum(20)
    nowpage=funpage.nowpage(int(page))
    frompageCount=funpage.frompageCount()
    after_range_num = funpage.after_range_num(2)
    before_range_num = funpage.before_range_num(9)
    qlistall=zzm.getmyproductslist(frompageCount=frompageCount,limitNum=limitNum,company_id=company_id,checkStatus=checkStatus)
    qlist=qlistall['list']
    qlistcount=qlistall['count']
    listcount=qlistcount
    if (int(listcount)>100000):
        listcount=100000
    listcount = funpage.listcount(listcount)
    page_listcount=funpage.page_listcount()
    firstpage = funpage.firstpage()
    lastpage = funpage.lastpage()
    page_range  = funpage.page_range()
    nextpage = funpage.nextpage()
    prvpage = funpage.prvpage()
    
    sql1="select count(0) from products where company_id=%s and check_status=1 and is_del=0 and is_pause=0 "
    result1=dbc.fetchonedb(sql1,[company_id])
    if result1:
        alist1=result1[0]
    sql0="select count(0) from products where company_id=%s and check_status=0 and is_del=0 and is_pause=0 "
    result0=dbc.fetchonedb(sql0,[company_id])
    if result0:
        alist0=result0[0]
    sql2="select count(0) from products where company_id=%s and check_status=2 and is_del=0 and is_pause=0 "
    result2=dbc.fetchonedb(sql2,[company_id])
    if result2:
        alist2=result2[0]
    sql3="select count(0) from products where company_id=%s and is_pause=1 and is_del=0 "
    result3=dbc.fetchonedb(sql3,[company_id])
    if result3:
        alist3=result3[0]
    #返回json数据
    datatype=request.GET.get("datatype")
    if datatype=="json":
        jsonlist={'checkStatus':checkStatus,'qlistall':qlistall,'count':{'c0':alist0,'c1':alist1,'c2':alist2,'c3':alist3},'pagecount':page_listcount}
        return HttpResponse(simplejson.dumps(jsonlist, ensure_ascii=False))
    return render_to_response('myrc/products.html',locals())

#----修改供求
def products_update(request):
    saveform="products_updatesave"
    proid=request.GET.get("proid")
    randid = random.randint(10000, 99999)
    company_id=request.GET.get("company_id")
    usertoken=request.GET.get("usertoken")
    if not getloginstatus(company_id,usertoken):
        errlist={'tokenerr':'true'}
        return HttpResponse(simplejson.dumps(errlist, ensure_ascii=False))
    appsystem=request.GET.get("appsystem")
    #if not getloginstatus(company_id,usertoken):
    #    return HttpResponse("nologin")
    #if not company_id or str(company_id)=="0":
    #    return HttpResponse("err")

    myproductsbyid=zzm.getmyproductsbyid(proid)
    if myproductsbyid:
        categorycode=myproductsbyid['categorycode']
        category=categorycode
        title=myproductsbyid['title']
        quantity=myproductsbyid['quantity']
        ptype=products=myproductsbyid['products_type_code']
        quantity_unit=myproductsbyid['quantity_unit']
        price=myproductsbyid['price']
        validity=myproductsbyid['validity']
        if price:
            pricetype='1'
        else:
            pricetype='0'
        price_unit=myproductsbyid['price_unit']
        details=myproductsbyid['details']
    
    piclist=zzm.getmyproductspic(proid)
    #返回json数据
    datatype=request.GET.get("datatype")
    if datatype=="json":
        jsonlist={'piclist':piclist,'myproductsbyid':myproductsbyid}
        return HttpResponse(simplejson.dumps(jsonlist, ensure_ascii=False))
    return render_to_response('myrc/pro_edit.html',locals())
#---删除图片
def del_productpic(request):
    company_id=request.GET.get("company_id")
    usertoken=request.GET.get("usertoken")
    if not getloginstatus(company_id,usertoken):
        errlist={'tokenerr':'true'}
        return HttpResponse(simplejson.dumps(errlist, ensure_ascii=False))
    appsystem=request.GET.get("appsystem")
    picid=request.GET.get("picid")
    product_id=request.GET.get("product_id")
    sql="delete from products_pic where product_id=%s and id=%s"
    dbc.updatetodb(sql,[product_id,picid])
    messagedata={'err':'true','errkey':''}
    return HttpResponse(simplejson.dumps(messagedata, ensure_ascii=False))
#---我的通讯录
def my_addressbook(request):
    company_id=request.GET.get("company_id")
    usertoken=request.GET.get("usertoken")
    if not getloginstatus(company_id,usertoken):
        errlist={'tokenerr':'true'}
        return HttpResponse(simplejson.dumps(errlist, ensure_ascii=False))
    appsystem=request.GET.get("appsystem")
    if not getloginstatus(company_id,usertoken) and appsystem=="Android":
        return HttpResponse("nologin")
    if not company_id or str(company_id)=="0":
        return HttpResponse("err")
    page=request.GET.get("page")
    if (page==None):
        page=1
    funpage = zz91page()
    limitNum=funpage.limitNum(10)
    nowpage=funpage.nowpage(int(page))
    frompageCount=funpage.frompageCount()
    after_range_num = funpage.after_range_num(2)
    before_range_num = funpage.before_range_num(9)
    qlistall=zzm.getmyaddressbooklist(frompageCount=frompageCount,limitNum=limitNum,company_id=company_id)
    qlist=qlistall['list']
    qlistcount=qlistall['count']
    listcount=qlistcount
    if (int(listcount)>100000):
        listcount=100000
    listcount = funpage.listcount(listcount)
    page_listcount=funpage.page_listcount()
    firstpage = funpage.firstpage()
    lastpage = funpage.lastpage()
    page_range  = funpage.page_range()
    nextpage = funpage.nextpage()
    prvpage = funpage.prvpage()
    #返回json数据
    datatype=request.GET.get("datatype")
    if datatype=="json":
        jsonlist={'list':qlist,'listcount':listcount}
        return HttpResponse(simplejson.dumps(jsonlist, ensure_ascii=False))
#加入通信录
def join_addressbook(request):
    company_id=request.POST.get("company_id")
    usertoken=request.POST.get("usertoken")
    if not getloginstatus(company_id,usertoken):
        errlist={'tokenerr':'true'}
        return HttpResponse(simplejson.dumps(errlist, ensure_ascii=False))
    appsystem=request.POST.get("appsystem")
    forcompany_id=request.POST.get("forcompany_id")
    sql="select id from company_addressbook where company_id=%s and forcompany_id=%s"
    result=dbc.fetchonedb(sql,[company_id,forcompany_id])
    gmt_created=datetime.datetime.now()
    if not result:
        sqlc="insert into company_addressbook(company_id,forcompany_id,gmt_created) values(%s,%s,%s)"
        dbc.updatetodb(sqlc,[company_id,forcompany_id,gmt_created])
        messagedata={'err':'false','errkey':'加入成功！'}
    else:
        messagedata={'err':'true','errkey':'已经加入！'}
    return HttpResponse(simplejson.dumps(messagedata, ensure_ascii=False))
#---删除通信录
def del_addressbook(request):
    company_id=request.GET.get("company_id")
    usertoken=request.GET.get("usertoken")
    if not getloginstatus(company_id,usertoken):
        errlist={'tokenerr':'true'}
        return HttpResponse(simplejson.dumps(errlist, ensure_ascii=False))
    appsystem=request.GET.get("appsystem")
    forcompany_id=request.GET.get("forcompany_id")
    sql="delete from company_addressbook where company_id=%s and forcompany_id=%s"
    dbc.updatetodb(sql,[company_id,forcompany_id])
    messagedata={'err':'true','errkey':''}
    return HttpResponse(simplejson.dumps(messagedata, ensure_ascii=False))
#---诚信档案文件
def infocreditfile(request):
    company_id=request.GET.get("company_id")
    usertoken=request.GET.get("usertoken")
    if not getloginstatus(company_id,usertoken):
        errlist={'tokenerr':'true'}
        return HttpResponse(simplejson.dumps(errlist, ensure_ascii=False))
    sql="select check_status,file_name,pic_name,file_number,organization,id,category_code from credit_file where company_id=%s"
    result=dbc.fetchalldb(sql,[company_id])
    listall=[]
    if result:
        for list in result:
            picname=list[1]
            picurl=list[2]
            personcode=list[3]
            personname=list[4]
            check_status=list[0]
            id=list[5]
            category_code=list[6]
            l={'id':id,'check_status':check_status,'picname':picname,'picurl':picurl,'personcode':personcode,'personname':personname,'category_code':category_code}
            listall.append(l)
    messagedata={'list':listall}
    return HttpResponse(simplejson.dumps(messagedata, ensure_ascii=False))
#删除诚信档案
def delcreditfile(request):
    company_id=request.POST.get("company_id")
    usertoken=request.POST.get("usertoken")
    isperson=request.POST.get("isperson")
    if not getloginstatus(company_id,usertoken):
        errlist={'tokenerr':'true'}
        return HttpResponse(simplejson.dumps(errlist, ensure_ascii=False))
    pid=request.POST.get("pid")
    if pid:
        sql="delete from credit_file where id=%s and company_id=%s"
        dbc.updatetodb(sql,[pid,company_id])
    messagedata={'err':'false','errkey':''}
    return HttpResponse(simplejson.dumps(messagedata, ensure_ascii=False))
#---诚信档案保存
def savecreditfile(request):
    company_id=request.POST.get("company_id")
    usertoken=request.POST.get("usertoken")
    isperson=request.POST.get("isperson")
    if not getloginstatus(company_id,usertoken):
        errlist={'tokenerr':'true'}
        return HttpResponse(simplejson.dumps(errlist, ensure_ascii=False))
    piclist=otherimgupload(request)
    account=getaccount(company_id)
    
    if isperson=="0":
        file_name="营业执照"
        category_code="10401005"
    if isperson=="1":
        file_name="身份证"
        category_code="10401004"
    gmt_created=gmt_modified=datetime.datetime.now()
    
    organization=request.POST.get("personname")
    file_number=request.POST.get("personcode")
    
    if piclist:
        for p in piclist:
            pic_name=p['databasepath']
            sql="insert into credit_file(company_id,account,category_code,file_name,pic_name,gmt_created,gmt_modified,file_number,organization) values(%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            resl=dbc.updatetodb(sql,[company_id,account,category_code,file_name,pic_name,gmt_created,gmt_modified,file_number,organization])
            if resl:
                source_id=resl[0]
                sql="update other_piclist set source_id=%s where id=%s"
                dbc.updatetodb(sql,[source_id,p['id']])
        messagedata={'err':'false','errkey':'','type':'credit'}
        return HttpResponse(simplejson.dumps(messagedata, ensure_ascii=False))
    else:
        messagedata={'err':'true','errkey':'错误！','type':'credit'}
        return HttpResponse(simplejson.dumps(messagedata, ensure_ascii=False))

#我的名片
def mycard(request):
    company_id=request.GET.get("company_id")
    usertoken=request.GET.get("usertoken")
    appsystem=request.GET.get("appsystem")
    if not getloginstatus(company_id,usertoken):
        errlist={'tokenerr':'true'}
        return HttpResponse(simplejson.dumps(errlist, ensure_ascii=False))
    
    clist=zzc.getcompanydetail(company_id)
    #被查看者是高会直接显示联系方式
    #iszstflag=zzt.getiszstcompany(company_id)
    list=[]
    if clist:
        industry=clist['industry']
        province=clist['province']
        city=clist['city']
        business=clist['business']
        address=clist['address']
        contact=clist['contact']
        mobile=clist['mobile1']
        position=clist['position']
        faceurl=clist['faceurl']
        #是否已经查看过联系方式公开
        isseecompany=zzq.getisseecompany(company_id,company_id)
        list={'companyname':clist['name'],'faceurl':faceurl,'industry':industry,'province':province,'city':city,'business':business,'address':address,'contact':contact,'mobile':mobile,'position':position,'isseecompany':isseecompany}
            
    return HttpResponse(simplejson.dumps(list, ensure_ascii=False))
    
    
    
