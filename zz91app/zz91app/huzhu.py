#-*- coding:utf-8 -*-
from django.shortcuts import render_to_response
import simplejson
from django.http import HttpResponse,HttpResponseRedirect,HttpResponsePermanentRedirect
import MySQLdb,sys,os,memcache,settings,urllib,re,datetime,time
from django.core.cache import cache
from zz91db_ast import companydb
from zz91db_2_news import newsdb
from settings import spconfig,appurl
from zz91tools import subString,filter_tags,formattime
from sphinxapi import *
from zz91page import *
import Image,ImageDraw,ImageFont,ImageFilter
try:
    import cStringIO as StringIO
except ImportError:
    import StringIO
    
from trade import otherimgupload
from qianbao import qianbaopaysave
     
     
dbc=companydb()
dbn=newsdb()
reload(sys)
sys.setdefaultencoding('UTF-8')
nowpath=os.path.dirname(__file__)
execfile(nowpath+"/func/public_function.py")
execfile(nowpath+"/func/huzhu_function.py")
execfile(nowpath+"/func/company_function.py")

zzh=zzhuzhu()
zzc=zzcompany()

#互助列表
def huzhu(request):
    host=getnowurl(request)
    nowlanmu="<a href='/huzhu/'>再生互助</a>"
    showpost=1
    category_id=request.GET.get("category_id")
    datetype=request.GET.get("datetype")
    htype=request.GET.get("htype")
    bbs_post_assist_id=request.GET.get("bbs_post_assist_id")
    keywords=request.GET.get("keywords")
    username=request.session.get("username",None)
    company_id=request.session.get("company_id",None)
    page=request.GET.get("page")
    if page==None or page=='':
        page=1
    if (keywords!=None):
        webtitle=keywords+"-互助列表"
    if (str(keywords)=='None'):    
        keywords=None
        webtitle="互助列表"
        datefirst=1
    
    """
    if datetype==None:
        datetype="1"
    timenow201=int(time.time())
    if datetype=="1":
        timehw=int(time.time())-3600*24
    if datetype=="2":
        timehw=int(time.time())-3600*24*7
    if datetype=="3":
        timehw=int(time.time())-3600*24*30
    #----每日每周每月
    """
    serverida=spconfig['serverid']
    #置顶
    topcode=None
    if category_id=="1":
        topcode="10041010"
    if category_id=="2":
        topcode="10041011"
    if category_id=="3":
        topcode="10041012"
    if category_id=="6":
        topcode="10041012"
    navlist=[]
    if str(page)=="1":
        navlist=zzh.getbbs_post_categorys(category_id)
        if (category_id=="106" or category_id=="1"):
            navlist=[{'name':'最新商机','category_id':category_id,'htype':'new','bbs_post_assist_id':''},{'name':'热门关注','category_id':category_id,'htype':'guanzhu','bbs_post_assist_id':''},{'name':'热门回复','category_id':category_id,'htype':'hot','bbs_post_assist_id':''}]
        
    
    
    bbstop=zzh.gettopbbslist(topcode)
    bbslistall=zzh.getbbslist(keywords,(int(page)-1)*20,20,category_id,datetype=datetype,htype=htype,bbs_post_assist_id=bbs_post_assist_id)
    bbslistall['bbstop']=bbstop
    bbslistall['navlist']=navlist
    return HttpResponse(simplejson.dumps(bbslistall, ensure_ascii=False))
def huzhu_imgload(request):
    return render_to_response('huzhu/imgload.html',locals())

def huzhupost(request):
    company_id=request.GET.get("company_id")
    usertoken=request.GET.get("usertoken")
    appsystem=request.GET.get("appsystem")
    if not getloginstatus(company_id,usertoken):
        errlist={'tokenerr':'true'}
        return HttpResponse(simplejson.dumps(errlist, ensure_ascii=False))
    #判断是否已经填写了昵称
    if not company_id or str(company_id)=="0":
        return HttpResponse("err")
    mynickname=zzh.getcompanynickname(company_id)
    if not mynickname or mynickname=="":
        nickname=request.GET.get("nickname")
        if nickname:
            zzh.addcompanynickname(nickname,company_id,username)
    #判断是否填写关注行业
    myguanzhu=zzh.gethuzhuguanzhu(company_id)
    if not myguanzhu or myguanzhu=="":
        myguanzhu=request.REQUEST.getlist("myguanzhu")
        if myguanzhu:
            zzh.addmyzhuzhuguanzhu(myguanzhu,company_id,username)

    category_id=18
    return render_to_response('huzhu/huzhupost2.html',locals())
    
def huzhumore(request):
    username=request.session.get("username",None)
    category_id=request.GET.get("category_id")
    datetype=request.GET.get("datetype")
    keywords=request.GET.get("keywords")
    htype=request.GET.get("htype")
    bbs_post_assist_id=request.GET.get("bbs_post_assist_id")
    if (str(keywords)=='None'):    
        keywords=None
    page=request.GET.get("page")
    if page==None or page=='':
        page=1
    if (str(category_id)=='None'):
        category_id=None
    if (str(htype)=='None'):
        htype=None
    if (str(bbs_post_assist_id)=='None'):
        bbs_post_assist_id=None 
    """
    timenow201=int(time.time())
    if datetype=="1":
        timehw=int(time.time())-3600*24
    if datetype=="2":
        timehw=int(time.time())-3600*24*7
    if datetype=="3":
        timehw=int(time.time())-3600*24*30
    """
    bbslistall=zzh.getbbslist(keywords,(int(page)-1)*20+1,20,category_id,htype=htype,bbs_post_assist_id=bbs_post_assist_id)
    bbslist=bbslistall['list']
    return render_to_response('huzhu/huzhumore.html',locals())

#查看帖子
def huzhuview(request,id):
    host=getnowurl(request)
    done = request.path
    gmt_created=datetime.datetime.now()
    replycount=0
    mycompany_id=request.GET.get("company_id")
    usertoken=request.GET.get("usertoken")
    appsystem=request.GET.get("appsystem")
    detail=zzh.getbbscontent(id,showcontent=1)
    if detail:
        zzh.huzhuclick_add(id)
        content=detail['contentall']
        content=zzh.replacetel(content)
        category_id=detail['bbs_post_category_id']
        title=detail['title']
        company_id=detail['company_id']
        nickname=detail['nickname']
        gmt_created=detail['gmt_time']
        replycount=detail['replycount']
        notice_count=detail['notice_count']
        recommend_count=detail['recommend_count']
        collect_count=detail['collect_count']
        visited_count=detail['visited_count']
        facepic=detail['facepic']
        piclist=detail['piclist']
        notice=zzh.isnotice(id,mycompany_id,1)
        recommend=zzh.isnotice(id,mycompany_id,0)
    else:
        errlist={'tokenerr':'true'}
        return HttpResponse(simplejson.dumps(errlist, ensure_ascii=False))
    sqlp="select file_path from bbs_post_upload_file where bbs_post_id=%s"
    presult=dbc.fetchalldb(sqlp,[id])
    picurllist=[]
    if presult:
        for ll in presult:
            plist={'file_path':ll[0]}
            picurllist.append(plist)
    #if not picurllist:
    #    picurllist=[{'file_path':''}]

    listall_reply=zzh.replylist(id,0,10)
    funpage=zz91page()
    limitNum=funpage.limitNum(10)
    listcount=replycount
    if (int(listcount)>1000000):
        listcount=1000000-1
    listcount = funpage.listcount(listcount)
    page_listcount=funpage.page_listcount()
    if (int(replycount)>10):
        moreflag=1
    else:
        moreflag=None
    jsonlist={'title':title,'content':content,'company_id':company_id,'nickname':nickname,'gmt_created':gmt_created,'replycount':replycount,'pagecount':page_listcount,'picurllist':picurllist,'listall_reply':listall_reply,'moreflag':moreflag,'category_id':category_id,'notice_count':notice_count,'recommend_count':recommend_count,'collect_count':collect_count,'visited_count':visited_count,'facepic':facepic,'piclist':piclist,'notice':notice,'recommend':recommend}
    return HttpResponse(simplejson.dumps(jsonlist, ensure_ascii=False))
#---点赞/关注 添加
def recommend_add(request):
    type=request.GET.get("type")
    category=request.GET.get("category")
    content_id=request.GET.get("content_id")
    content_title=request.GET.get("content_title")
    company_id=request.GET.get("company_id")
    if content_title:
        content_title=content_title.strip()
    gmt_created=gmt_modified=datetime.datetime.now()
    usertoken=request.GET.get("usertoken")
    appsystem=request.GET.get("appsystem")
    if not getloginstatus(company_id,usertoken):
        errlist={'tokenerr':'true'}
        return HttpResponse(simplejson.dumps(errlist, ensure_ascii=False))
    account=getaccount(company_id)
    sql="select id,state from bbs_post_notice_recommend where content_id=%s and company_id=%s and type=%s"
    result=dbc.fetchonedb(sql,[content_id,company_id,type])
    if result:
        state=result[1]
        if state==0:
            state=1
        else:
            state=0
        #点赞或推荐
        if type=="0":
            sqlc="select recommend_count,company_id from bbs_post where id=%s"
            resultc=dbc.fetchonedb(sqlc,[content_id])
            if resultc:
                forcompany_id=resultc[1]
                if resultc[0]:
                    if state==0:
                        sql="update bbs_post set recommend_count=recommend_count+1,gmt_modified=%s where id=%s"
                        dbc.updatetodb(sql,[gmt_modified,content_id])
                    else:
                        sql="update bbs_post set recommend_count=recommend_count-1,gmt_modified=%s where id=%s"
                        dbc.updatetodb(sql,[gmt_modified,content_id])
                else:
                    sql="update bbs_post set recommend_count=1,gmt_modified=%s where id=%s"
                    dbc.updatetodb(sql,[gmt_modified,content_id])
                #加入通信录
                if forcompany_id:
                    zzc.joinaddressbook(company_id,forcompany_id)
        #关注
        if type=="1":
            sqlc="select notice_count,company_id from bbs_post where id=%s"
            resultc=dbc.fetchonedb(sqlc,[content_id])
            if resultc:
                forcompany_id=resultc[1]
                if resultc[0]:
                    if state==0:
                        sql="update bbs_post set notice_count=notice_count+1 where id=%s"
                        dbc.updatetodb(sql,[content_id])
                    else:
                        sql="update bbs_post set notice_count=notice_count-1 where id=%s"
                        dbc.updatetodb(sql,[content_id])
                else:
                    sql="update bbs_post set notice_count=1,gmt_modified=%s where id=%s"
                    dbc.updatetodb(sql,[gmt_modified,content_id])
                #加入通信录
                if forcompany_id:
                    zzc.joinaddressbook(company_id,forcompany_id)
        sqla="update bbs_post_notice_recommend set state=%s where id=%s"
        dbc.updatetodb(sqla,[state,result[0]])
    else:
        state=0
        #点赞或推荐
        if str(type)=="0":
            sqlc="select recommend_count,company_id from bbs_post where id=%s"
            resultc=dbc.fetchonedb(sqlc,[content_id])
            if resultc:
                forcompany_id=resultc[1]
                if resultc[0]:
                    sql="update bbs_post set recommend_count=recommend_count+1,gmt_modified=%s where id=%s"
                    dbc.updatetodb(sql,[gmt_modified,content_id])
                else:
                    sql="update bbs_post set recommend_count=1,gmt_modified=%s where id=%s"
                    dbc.updatetodb(sql,[gmt_modified,content_id])
                #加入通信录
                if forcompany_id:
                    zzc.joinaddressbook(company_id,forcompany_id)
        #关注
        if str(type)=="1":
            sqlc="select notice_count,company_id from bbs_post where id=%s"
            resultc=dbc.fetchonedb(sqlc,[content_id])
            if resultc:
                forcompany_id=resultc[1]
                if resultc[0]:
                    sql="update bbs_post set notice_count=notice_count+1 where id=%s"
                    dbc.updatetodb(sql,[content_id])
                else:
                    sql="update bbs_post set notice_count=1,gmt_modified=%s where id=%s"
                    dbc.updatetodb(sql,[gmt_modified,content_id])
                #加入通信录
                if forcompany_id:
                    zzc.joinaddressbook(company_id,forcompany_id)
        sqla="insert into bbs_post_notice_recommend(type,category,state,content_id,content_title,company_id,account,gmt_created,gmt_modified) values(%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        dbc.updatetodb(sqla,[type,category,state,content_id,content_title,company_id,account,gmt_created,gmt_modified])
    jsonresult={'err':'false','state':state}
    return HttpResponse(simplejson.dumps(jsonresult, ensure_ascii=False))
    
#---查看更多回复
def replymore(request):
    page=request.GET.get("page")
    type=request.GET.get("type")
    if page==None:
        page=1
    postid=request.GET.get("postid")
    replyid=request.GET.get("replyid")
    if type=="0":
        listall_reply=zzh.replylist(postid,(int(page)-1)*10,10)
        datatype=request.GET.get("datatype")
        if datatype=="json":
            return HttpResponse(simplejson.dumps(listall_reply, ensure_ascii=False))
        return render_to_response('huzhu/replymore.html',locals())
    if type=="1":
        listall_reply=zzh.replyreplylist(replyid,(int(page)-1)*10,10)
        datatype=request.GET.get("datatype")
        if datatype=="json":
            return HttpResponse(simplejson.dumps(listall_reply, ensure_ascii=False))
        return render_to_response('huzhu/replyreplymore.html',locals())
    
    return render_to_response('huzhu/replymore.html',locals())
#----保存发布帖子
def huzhupostsave(request):
    bbs_post_id = request.POST.get('category_id')
    title = request.POST.get('title')
    company_id = request.POST.get('company_id')
    usertoken=request.POST.get("usertoken")
    if not getloginstatus(company_id,usertoken):
        errlist={'tokenerr':'true'}
        return HttpResponse(simplejson.dumps(errlist, ensure_ascii=False))
    if not company_id or str(company_id)=="0":
        return HttpResponse("err")
    if (bbs_post_id==None or bbs_post_id==""):
        bbs_post_id=106
    content = request.POST.get('content')
    piclist=otherimgupload(request)
    
    if content:
        rpl1=re.findall('[0-9\ ]+',content)
        for r1 in rpl1:
            if len(r1)>10:
                content=content.replace(r1,r1[:-3]+'***')
    gmt_created=datetime.datetime.now()
    gmt_modified=datetime.datetime.now()
    company_id=request.POST.get("company_id")
    username=getaccount(company_id)
    if not title:
        #title=subString(filter_tags(content),30)
        title=""
    
    if bbs_post_id==106:
        bbs_post_assist_id=107
    else:
        bbs_post_assist_id=24
    if (content and content!=""):
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
        bbs_user_profiler_id=zzh.getprofilerid(username)
        if (bbs_user_profiler_id==None):
            bbs_user_profiler_id=1
        #购买显示联系方式
        contactflag=request.POST.get('contactflag')
        if (contactflag=="1"):
            showcontactnum=request.POST.get('showcontactnum')
            if showcontactnum:
                qianbaopaysave(company_id=company_id,paytype="11",money=showcontactnum)
        value=[company_id,bbs_user_profiler_id,username,bbs_post_id,title,content,0,1,gmt_created,gmt_modified,gmt_modified,gmt_modified,4,bbs_post_assist_id]
        sql="insert into bbs_post(company_id,bbs_user_profiler_id,account,bbs_post_category_id,title,content,is_del,check_status,gmt_created,gmt_modified,post_time,reply_time,postsource,bbs_post_assist_id) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        result=dbc.updatetodb(sql,value)
        qpic=''
        if result:
            postid=result[0]
            #保存图片
            i=0
            if piclist:
                for p in piclist:
                    if (i==0):
                        qpic=p['path']
                    sql="update other_piclist set source_id=%s where id=%s"
                    dbc.updatetodb(sql,[postid,p['id']])
                    i+=1
            #写入朋友圈
            qtitle="发布一条互助信息"
            qcontent=title
            #qpic=""
            qtype="post_huzhu"
            qurl="http://m.zz91.com/huzhu/"+str(postid)+".html"
            #insert_appquan(company_id,qtitle,qcontent,qpic,qurl,qtype,gmt_created)
        messagedata={'err':'false','errkey':'','type':'posthuzhu'}
        return HttpResponse(simplejson.dumps(messagedata, ensure_ascii=False))
    else:
        messagedata={'err':'true','errkey':'请填写提问内容！','type':'posthuzhu'}
        return HttpResponse(simplejson.dumps(messagedata, ensure_ascii=False))
def sharetoquan(request):
    #写入朋友圈
    qtitle=request.POST.get('qtitle')
    qcompany_id=request.POST.get('company_id')
    qcontent=request.POST.get('qcontent')
    qpic=request.POST.get('qpic')
    qtype=request.POST.get('qtype')
    qurl=request.POST.get('qurl')
    gmt_created=datetime.datetime.now()
    qtitle=''
    insert_appquan(qcompany_id,qtitle,qcontent,qpic,qurl,qtype,gmt_created)
    messagedata={'err':'false','errkey':'','type':'sharequan'}
    return HttpResponse(simplejson.dumps(messagedata, ensure_ascii=False))
#我的商圈
def app_quan(request):
    company_id=request.GET.get("company_id")
    qtype=request.GET.get("qtype")
    page=request.GET.get("page")
    if not page:
        page=1
    list=zzh.getquanlist(company_id,(int(page)-1)*20,20,qtype=qtype)
    messagedata={'err':'false','errkey':'','list':list}
    return HttpResponse(simplejson.dumps(messagedata, ensure_ascii=False))
    
def newspinlun(request):
    news_id = request.GET.get('news_id')
    price_id = request.GET.get('price_id')
    listall_reply=None
    bbs_post_id=0
    if news_id:
        sql="select bbs_post_id from bbs_post_news where news_id=%s"
        result=dbc.fetchonedb(sql,[news_id])
    if price_id:
        sql="select bbs_post_id from bbs_post_news where price_id=%s"
        result=dbc.fetchonedb(sql,[price_id])
    if result:
        bbs_post_id=result[0]
        listall_reply=zzh.replylist(bbs_post_id,0,10)
    messagedata={'list':listall_reply,'bbs_post_id':bbs_post_id}
    return HttpResponse(simplejson.dumps(messagedata, ensure_ascii=False))
#资讯评论保存
def newspinlunsave(request):
    bbs_post_category_id = 2
    title = request.POST.get('title')
    news_id=request.POST.get('news_id')
    price_id=request.POST.get('price_id')
    company_id = request.POST.get('company_id')
    usertoken=request.POST.get("usertoken")
    if not getloginstatus(company_id,usertoken):
        errlist={'tokenerr':'true'}
        return HttpResponse(simplejson.dumps(errlist, ensure_ascii=False))
    if not company_id or str(company_id)=="0":
        return HttpResponse("err")
    
    content = request.POST.get('content')
    
    recontent=request.POST.get('recontent')
    if recontent:
        rpl1=re.findall('[0-9\ ]+',recontent)
        for r1 in rpl1:
            if len(r1)>10:
                recontent=recontent.replace(r1,r1[:-3]+'***')
    gmt_created=datetime.datetime.now()
    gmt_modified=datetime.datetime.now()
    username=account=getaccount(company_id)
    if not title:
        title=""
    
    if bbs_post_category_id==106:
        bbs_post_assist_id=107
    else:
        bbs_post_assist_id=24
    bbs_user_profiler_id=1
    if (recontent and recontent!=""):
        bbs_user_profiler_id=zzh.getprofilerid(username)
        if (bbs_user_profiler_id==None):
            bbs_user_profiler_id=1
        reply_count=1
        #资讯评论
        result=None
        if news_id:
            sql="select id,bbs_post_id from bbs_post_news where news_id=%s"
            result=dbc.fetchonedb(sql,[news_id])
            if title:
                title=title.strip()
                content="读资讯评论<div style='background-color: #ebebeb;padding: 10px;line-height: 22px;' class='newspinlun' id='"+str(news_id)+"'><img src='../../image/link.png' width='50' />"+title+"</div>"
                title=""
        #价格评论
        if price_id:
            sql="select id,bbs_post_id from bbs_post_news where price_id=%s"
            result=dbc.fetchonedb(sql,[price_id])
            if title:
                title=title.strip()
                content="读行情评论<div style='background-color: #ebebeb;padding: 10px;line-height: 22px;' class='pricepinlun' id='"+str(price_id)+"'><img src='../../image/link.png' width='50' />"+title+"</div>"
                title=""
        if result:
            bbs_post_id=result[1]
            #写入回复表
            title=""
            tocompany_id=0
            bbs_post_reply_id=0
            value=[company_id,account,title,bbs_post_id,recontent,0,1,gmt_created,gmt_modified,4,bbs_post_reply_id,tocompany_id]
            sql="insert into bbs_post_reply(company_id,account,title,bbs_post_id,content,is_del,check_status,gmt_created,gmt_modified,postsource,bbs_post_reply_id,tocompany_id) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            dbc.updatetodb(sql,value)
        else:
            value=[company_id,bbs_user_profiler_id,username,bbs_post_category_id,title,content,0,1,gmt_created,gmt_modified,gmt_modified,gmt_modified,4,bbs_post_assist_id,reply_count]
            sql="insert into bbs_post(company_id,bbs_user_profiler_id,account,bbs_post_category_id,title,content,is_del,check_status,gmt_created,gmt_modified,post_time,reply_time,postsource,bbs_post_assist_id,reply_count) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            result=dbc.updatetodb(sql,value)
            if result:
                bbs_post_id=result[0]
                if not news_id:
                    news_id=0
                if not price_id:
                    price_id=0
                sql="insert into bbs_post_news(bbs_post_id,news_id,price_id,gmt_created) values(%s,%s,%s,%s)"
                dbc.updatetodb(sql,[bbs_post_id,news_id,price_id,gmt_created])
                title=""
                tocompany_id=0
                bbs_post_reply_id=0
                value=[company_id,account,title,bbs_post_id,recontent,0,1,gmt_created,gmt_modified,4,bbs_post_reply_id,tocompany_id]
                sql="insert into bbs_post_reply(company_id,account,title,bbs_post_id,content,is_del,check_status,gmt_created,gmt_modified,postsource,bbs_post_reply_id,tocompany_id) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
                dbc.updatetodb(sql,value)
        messagedata={'err':'false','errkey':'','type':'posthuzhu'}
        return HttpResponse(simplejson.dumps(messagedata, ensure_ascii=False))
    else:
        messagedata={'err':'true','errkey':'请填写提问内容！','type':'posthuzhu'}
        return HttpResponse(simplejson.dumps(messagedata, ensure_ascii=False))
#----回复帖子
def huzhu_replay(request):
    showpost=1
    nowlanmu="<a href='/huzhu/'>再生互助</a>"
    company_id=request.POST.get("company_id")
    usertoken=request.POST.get("usertoken")
    if not getloginstatus(company_id,usertoken):
        errlist={'tokenerr':'true'}
        return HttpResponse(simplejson.dumps(errlist, ensure_ascii=False))
    if not company_id or str(company_id)=="0":
        return HttpResponse("err")
    bbs_post_id = request.POST.get('bbs_post_id')
    tocompany_id = request.POST.get('tocompany_id')
    bbs_post_reply_id=request.POST.get('bbs_post_reply_id')
    title=request.POST.get('title')
    if not title:
        title=""
    content = request.POST.get('content')
    gmt_created=datetime.datetime.now()
    gmt_modified=datetime.datetime.now()
    account=getaccount(company_id)
    piclist=otherimgupload(request)

    if (content and content!="" and company_id):
        #内容里插入图片
        if piclist:
            for p in piclist:
                if p:
                    picurl=p['path']
                    content+='<br /><img src="'+picurl+'"><br />'
        #加入通信录
        if tocompany_id:
            zzc.joinaddressbook(company_id,tocompany_id)
        value=[company_id,account,title,bbs_post_id,content,0,1,gmt_created,gmt_modified,1,bbs_post_reply_id,tocompany_id]
        sql="insert into bbs_post_reply(company_id,account,title,bbs_post_id,content,is_del,check_status,gmt_created,gmt_modified,postsource,bbs_post_reply_id,tocompany_id) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        dbc.updatetodb(sql,value)
        sql="update bbs_post set reply_time=%s,reply_count=reply_count+1,gmt_modified=%s where id=%s"
        result=dbc.updatetodb(sql,[gmt_modified,gmt_modified,bbs_post_id])
        if result:
            postid=result[0]
            #保存图片
            if piclist:
                for p in piclist:
                    sql="update other_piclist set source_id=%s where id=%s"
                    dbc.updatetodb(sql,[postid,p['id']])
        """
        if picidlist!="" and picidlist:
            sql_bbs_post='SELECT max(id) from bbs_post_reply where bbs_post_id=%s'
            result=dbc.fetchonedb(sql_bbs_post,[bbs_post_id])
            if result:
                bbs_post_reply_id=result[0]
                sql_pic='update bbs_post_upload_file set bbs_post_reply_id=%s where id in (%s)'
                dbc.updatetodb(sql_pic,[bbs_post_reply_id,picidlist])
        """
        #updatepostviewed(tocompany_id,bbs_post_id)
        #----更新弹窗
        #updateopenfloat(tocompany_id,0)
        messagedata={'err':'false','errkey':'','type':'huzhu'}
        return HttpResponse(simplejson.dumps(messagedata, ensure_ascii=False))
    else:
        messagedata={'err':'true','errkey':'系统错误，请重试','type':'huzhu'}
        return HttpResponse(simplejson.dumps(messagedata, ensure_ascii=False))

