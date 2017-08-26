#-*- coding:utf-8 -*-
from django.shortcuts import render_to_response
from django.http import HttpResponse,HttpResponseRedirect,HttpResponsePermanentRedirect
import MySQLdb,sys,os,memcache,settings,urllib,re,time,datetime,requests,random
from django.core.cache import cache
from sphinxapi import *
from zz91page import *
import simplejson

from settings import spconfig
from function import getnowurl
from zz91db_ast import companydb
from zz91db_sms import smsdb
from zz91db_2_news import newsdb

from trade import otherimgupload
from qianbao import qianbaopaysave

dbc=companydb()
dbsms=smsdb()
dbn=newsdb()

reload(sys)
sys.setdefaultencoding('UTF-8')
nowpath=os.path.dirname(__file__)
execfile(nowpath+"/func/company_function.py")
execfile(nowpath+"/func/qianbao_function.py")
execfile(nowpath+"/func/trade_function.py")
execfile(nowpath+"/func/weixin_function.py")
execfile(nowpath+"/func/ldb_weixin_function.py")
execfile(nowpath+"/func/huzhu_function.py")
execfile(nowpath+"/commfunction.py")
execfile(nowpath+"/function.py")

zzcompany=zcompany()
zzqianbao=qianbao()
zztrade=ztrade()
ldb_weixin=ldbweixin()
zzh=zzhuzhu()

def huzhu_wenda(request):
    return huzhu(request,category_id=1)
def huzhu_shequ(request):
    return huzhu(request,category_id=2)
def huzhu_xueyuan(request):
    return huzhu(request,category_id=3)
def huzhu_remen(request):
    return huzhu(request,htype="hot")
def huzhu_shangquan(request):
    return huzhu(request,category_id=106)
def huzhu_zuixin(request):
    return huzhu(request,htype="new")
def huzhu301(request):
    tourl="/huzhu/"
    category_id=request.GET.get("category_id")
    if category_id:
        if str(category_id)=="1":
            tourl+="wenda.html"
        if str(category_id)=="2":
            tourl+="shequ.html"
        if str(category_id)=="3":
            tourl+="xueyuan.html"
    htype=request.GET.get("htype")
    if htype:
        if htype=="hot":
            tourl+="remen.html"
        if htype=="new":
            tourl+="zuixin.html"
    if not category_id and not htype:
        tourl+="zuixin.html"
    keywords=request.GET.get("keywords")
    tourl+="?"
    if keywords:
        tourl+="keywords="+keywords
    datetype=request.GET.get("datetype")
    if datetype:
        tourl+="datetype="+datetype
    return HttpResponsePermanentRedirect(tourl)
#互助列表
def huzhu(request,category_id="",htype=""):
    host=getnowurl(request)
    nowlanmu="<a href='/huzhu/'>再生互助</a>"
    showpost=1
    if not category_id:
        category_id=request.GET.get("category_id")
    datetype=request.GET.get("datetype")
    page=request.GET.get("page")
    if page==None or page=='':
        page=1
    
    keywords=request.GET.get("keywords")
    username=request.session.get("username",None)
    company_id=request.session.get("company_id",None)
    #最近搜索和相关搜索
    if not company_id:
        appid=request.session.get("appid",None)
    else:
        appid=company_id
    mysearchkeylist=getkeywords(appid)
    abountkeywords=searchtis(keywords)
    hhtype=request.GET.get("htype")
    if hhtype:
        htype=hhtype
        
    bbs_post_assist_id=request.GET.get("bbs_post_assist_id")
    navlist106=zzh.getbbs_post_categorys(106)
    navlist1=zzh.getbbs_post_categorys(1)
    navlist2=zzh.getbbs_post_categorys(2)
    navlist3=zzh.getbbs_post_categorys(3)
    navlist122=zzh.getbbs_post_categorys(122)
    
    if (keywords!=None):
        webtitle=keywords+"-互助列表"
        updatesearchKeywords(request,company_id,keywords,ktype="huzhu")
    if (str(keywords)=='None'):    
        keywords=None
        webtitle="互助列表"
        datefirst=1
    if (str(category_id)=='None'):
        category_id=None
    if (category_id==None and keywords==None):
        webtitle="废料问答-互助列表"
    if (str(category_id)=='1'):
        webtitle="废料问答-互助列表"
    if (str(category_id)=='2'):
        webtitle="废料社区-互助列表"
    if (str(category_id)=='3'):
        webtitle="江湖学院-互助列表"
    if (str(category_id)=='122'):
        webtitle="招聘-助列表"

    searchlist={}
    if keywords:
        searchlist['keywords']=keywords
    if category_id:
        searchlist['category_id']=category_id
    if htype:
        searchlist['htype']=htype
    if bbs_post_assist_id:
        searchlist['bbs_post_assist_id']=bbs_post_assist_id
    searchurl=urllib.urlencode(searchlist)
    funpage=zz91page()
    limitNum=funpage.limitNum(20)
    nowpage=funpage.nowpage(int(page))
    frompageCount=funpage.frompageCount()
    after_range_num = funpage.after_range_num(3)
    before_range_num = funpage.before_range_num(6)
    bbslistall=zzh.getbbslist(keywords,frompageCount,limitNum,category_id,datetype=datetype,htype=htype,bbs_post_assist_id=bbs_post_assist_id)
    listcount=0
    bbslist=bbslistall['list']
    listcount=bbslistall['count']
    if (int(listcount)>20000):
        listcount=20000-1
    listcount = funpage.listcount(listcount)
    page_listcount=funpage.page_listcount()
    firstpage = funpage.firstpage()
    lastpage = funpage.lastpage()
    page_range  = funpage.page_range()
    if len(page_range)>7:
        page_range=page_range[:7]
    nextpage = funpage.nextpage()
    prvpage = funpage.prvpage()
    return render_to_response('aui/huzhu/list.html',locals())
    #return render_to_response('huzhu/huzhu2.html',locals())

    
def huzhumore(request):
    username=request.session.get("username",None)
    category_id=request.GET.get("category_id")
    datetype=request.GET.get("datetype")
    keywords=request.GET.get("keywords")
    bbs_post_assist_id=request.GET.get("bbs_post_assist_id")
    htype=request.GET.get("htype")
    if (keywords!=None):
        webtitle=keywords+"互助列表"
    if (str(keywords)=='None'):    
        keywords=None
    page=request.GET.get("page")
    if str(keywords)=="None":
        keywords=None
    if str(htype)=="None":
        htype=None
    if page==None or page=='':
        page=1
    if (str(category_id)=='None'):
        category_id=None
        
    if datetype==None:
        datetype="1"
    """
    timenow201=int(time.time())
    if datetype=="1":
        timehw=int(time.time())-3600*24
    if datetype=="2":
        timehw=int(time.time())-3600*24*7
    if datetype=="3":
        timehw=int(time.time())-3600*24*30
    """
    
    bbslistall=zzh.getbbslist(keywords,(int(page)-1)*20,20,category_id,datetype=datetype,htype=htype,bbs_post_assist_id=bbs_post_assist_id)
    datatype=request.GET.get("datatype")
    if datatype=='json':
        return HttpResponse(simplejson.dumps(bbslistall, ensure_ascii=False))
    bbslist=bbslistall['list']
    return render_to_response('huzhu/huzhumore.html',locals())
def huzhuview301(request,id):
    tourl="/huzhu/"+str(id)+".html"
    return HttpResponsePermanentRedirect(tourl)
#查看帖子
def huzhuview(request,id):
    host=getnowurl(request)
    showpost=1
    nowlanmu="<a href='/huzhu/'>再生互助</a>"
    done = request.path
    suc=request.GET.get("suc")
    err=request.GET.get("err")
    username=request.session.get("username",None)
    mycompany_id=request.session.get("company_id",None)
    gmt_created=datetime.datetime.now()
    
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
        favoriteflag=0
        if mycompany_id:
            category_id=str(category_id)
            favoriteflag=isfavorite(id,'10091005',mycompany_id)
    else:
        return HttpResponse('数据错误！')
    webtitle=filter_tags(title)
    if not title:
        webtitle=filter_tags(content)
    sqlp="select file_path from bbs_post_upload_file where bbs_post_id=%s"
    presult=dbc.fetchalldb(sqlp,[id])
    picurllist=[]
    if presult:
        for ll in presult:
            file_path=ll[0]
            if file_path:
                ldotarr=file_path.split(".")
                ldot=ldotarr[len(ldotarr)-1]
                filekz=None
                if ldot in vodiolist:
                    filekz=ldot
                plist={'file_path':ll[0],'filekz':filekz}
            picurllist.append(plist)

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
    if not company_id:
        company_id=0
    jsonlist={'title':title,'content':content,'company_id':company_id,'nickname':nickname,'gmt_created':gmt_created,'replycount':replycount,'pagecount':page_listcount,'picurllist':picurllist,'listall_reply':listall_reply,'moreflag':moreflag,'category_id':category_id,'notice_count':notice_count,'recommend_count':recommend_count,'collect_count':collect_count,'visited_count':visited_count,'facepic':facepic,'piclist':piclist,'notice':notice,'recommend':recommend}

    return render_to_response('aui/huzhu/detail.html',locals())
    #return render_to_response('huzhu/huzhuview2.html',locals())
#---点赞/关注 添加
def recommend_add(request):
    username=request.session.get("username",None)
    company_id=request.session.get("company_id",None)
    if username and (company_id==None or str(company_id)=="0"):
        company_id=getcompanyid(username)
        request.session['company_id']=company_id
    bbs_post_assist_id=107
    if (username==None or (company_id==None or str(company_id)=="0")):
        errlist={'err':'login'}
        return HttpResponse(simplejson.dumps(errlist, ensure_ascii=False))
    
    type=request.GET.get("type")
    category=request.GET.get("category")
    content_id=request.GET.get("content_id")
    content_title=request.GET.get("content_title")
    if content_title:
        content_title=content_title.strip()
    gmt_created=gmt_modified=datetime.datetime.now()
    
    
    account=getcompanyaccount(company_id)
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
                    zzcompany.joinaddressbook(company_id,forcompany_id)
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
                    zzcompany.joinaddressbook(company_id,forcompany_id)
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
                    zzcompany.joinaddressbook(company_id,forcompany_id)
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
                    zzcompany.joinaddressbook(company_id,forcompany_id)
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
    username=request.session.get("username",None)
    company_id=request.session.get("company_id",None)
    if username and (company_id==None or str(company_id)=="0"):
        company_id=getcompanyid(username)
        request.session['company_id']=company_id
    bbs_post_assist_id=107
    if (username==None or (company_id==None or str(company_id)=="0")):
        errlist={'err':'login'}
        return HttpResponse(simplejson.dumps(errlist, ensure_ascii=False))
    
    bbs_post_id = request.POST.get('category_id')
    title = request.POST.get('title')
    if (bbs_post_id==None or bbs_post_id==""):
        bbs_post_id=106
    content = request.POST.get('content')
    piclist=request.POST.get('piclist')
    
    if content:
        rpl1=re.findall('[0-9\ ]+',content)
        for r1 in rpl1:
            if len(r1)>10:
                content=content.replace(r1,r1[:-3]+'***')
    gmt_created=datetime.datetime.now()
    gmt_modified=datetime.datetime.now()
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
            piclist=piclist.split(",")
            for p in piclist:
                if p:
                    pid=p
                    sql="select path from other_piclist where id=%s"
                    result=dbc.fetchonedb(sql,[pid])
                    if result:
                        picurl=result[0]
                        picurl="http://img3.zz91.com/300x15000/"+picurl
                        # 获取文件名后缀
                        filetype=picurl.split(".")[-1]
                        if (filetype.lower() in ["mp4","mov","avi","3gp","3gp2","wav","rm","mpg","asf","mid"]):
                            content+='<br /><img src="http://static.m.zz91.com/image/video.png" path="'+picurl+'" class="videoframe" style="width:100px"><br />'
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
            for p in piclist:
                if p:
                    sql="update other_piclist set source_id=%s where id=%s"
                    dbc.updatetodb(sql,[postid,p])
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
#----回复帖子
def huzhu_replay(request):
    showpost=1
    nowlanmu="<a href='/huzhu/'>再生互助</a>"
    bbs_post_id = request.POST['bbs_post_id']
    tocompany_id = request.POST['tocompany_id']
    title=request.POST['title']
    content = request.POST['content']
    picidlist=request.POST['picidlist']
    gmt_created=datetime.datetime.now()
    gmt_modified=datetime.datetime.now()
    username=request.session.get("username",None)
    company_id=request.session.get("company_id",None)
    if username and (company_id==None or str(company_id)=="0"):
        company_id=getcompanyid(username)
        request.session['company_id']=company_id

    if (username==None or (company_id==None or str(company_id)=="0")):
        return HttpResponseRedirect("/login/")
    if (content and content!=""):
        value=[company_id,username,title,bbs_post_id,content,0,0,gmt_created,gmt_modified,1]
        sql="insert into bbs_post_reply(company_id,account,title,bbs_post_id,content,is_del,check_status,gmt_created,gmt_modified,postsource) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        dbc.updatetodb(sql,value)
        sql="update bbs_post set reply_time=%s,reply_count=reply_count+1,gmt_modified=%s where id=%s"
        dbc.updatetodb(sql,[gmt_modified,gmt_modified,bbs_post_id])
        if picidlist!="":
            sql_bbs_post='SELECT max(id) from bbs_post_reply where bbs_post_id=%s'
            result=dbc.fetchonedb(sql_bbs_post,[bbs_post_id])
            if result:
                bbs_post_reply_id=result[0]
                sql_pic='update bbs_post_upload_file set bbs_post_reply_id=%s where id in (%s)'
                dbc.updatetodb(sql_pic,[bbs_post_reply_id,picidlist])
        updatepostviewed(tocompany_id,bbs_post_id)
        #----更新弹窗
        updateopenfloat(tocompany_id,0)
        return HttpResponseRedirect("/huzhu/"+str(bbs_post_id)+".html?suc=1#hh")
    else:
        return HttpResponseRedirect("/huzhu/"+str(bbs_post_id)+".html?err=1#hh")
def huzhu_replayshow(request):
    host=getnowurl(request)
    nowlanmu="<a href='/huzhu/'>再生互助</a>"
    replyid=request.GET.get('replyid')
    postid=request.GET.get('postid')
    tocompany_id=request.GET.get('tocompany_id')
    username=request.session.get("username",None)
    company_id=request.session.get("company_id",None)
    if username and (company_id==None or str(company_id)=="0"):
        company_id=getcompanyid(username)
        request.session['company_id']=company_id
    if (username==None or (company_id==None or str(company_id)=="0")):
        return HttpResponseRedirect("/login/?done="+host)
    sql="select title,content,account,gmt_created,bbs_post_category_id,company_id from bbs_post where id=%s"
    alist=dbc.fetchonedb(sql,[postid])
    if alist:
        title=alist[0]
        content=alist[1]
        category_id=alist[4]
    return render_to_response('aui/huzhu/reply.html',locals())
    #return render_to_response('huzhu/huzhureply.html',locals())

#----发帖人回复
def reply_reply(request):
    host=getnowurl(request)
    replyid=request.POST.get('replyid')
    postid=request.POST.get('postid')
    replycontent=request.POST.get('replycontent')
    tocompany_id=request.POST.get('tocompany_id')
    piclist=request.POST.get('piclist')
    gmt_created=datetime.datetime.now()
    gmt_modified=datetime.datetime.now()
    title=""
    username=request.session.get("username",None)
    company_id=request.session.get("company_id",None)
    if username and (company_id==None or str(company_id)=="0"):
        company_id=getcompanyid(username)
        request.session['company_id']=company_id
    
    if (username==None or (company_id==None or str(company_id)=="0")):
        errlist={'err':'login'}
        return HttpResponse(simplejson.dumps(errlist, ensure_ascii=False))
    if replycontent:
        #内容里插入图片
        if piclist:
            piclist=piclist.split(",")
            for p in piclist:
                if p:
                    pid=p
                    sql="select path from other_piclist where id=%s"
                    result=dbc.fetchonedb(sql,[pid])
                    if result:
                        picurl=result[0]
                        picurl="http://img3.zz91.com/300x15000/"+picurl
                        # 获取文件名后缀
                        filetype=picurl.split(".")[-1]
                        if (filetype.lower() in ["mp4","mov","avi","3gp","3gp2","wav","rm","mpg","asf","mid"]):
                            replycontent+='<br /><img src="http://static.m.zz91.com/image/video.png" path="'+picurl+'" class="videoframe" style="width:100px"><br />'
                        else:
                            replycontent+='<br /><img src="'+picurl+'"><br />'
        value=[company_id,username,title,postid,replycontent,0,1,gmt_created,gmt_modified,replyid,tocompany_id,1]
        sql="insert into bbs_post_reply(company_id,account,title,bbs_post_id,content,is_del,check_status,gmt_created,gmt_modified,bbs_post_reply_id,tocompany_id,postsource) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        result=dbc.updatetodb(sql,value)
        if result:
            sql="update bbs_post set reply_time=%s,reply_count=reply_count+1,gmt_modified=%s where id=%s"
            dbc.updatetodb(sql,[gmt_modified,gmt_modified,postid])
            replyid=result[0]
            nickname=getusername(company_id)
            tonickname=getusername(tocompany_id)
            posttime=formattime(gmt_created,0)
            updatepostviewed(tocompany_id,postid)
            #更新图片
            for p in piclist:
                if p:
                    sql="update other_piclist set source_id=%s where id=%s"
                    dbc.updatetodb(sql,[replyid,p])
        messagedata={'err':'false','errkey':'','type':'replyhuzhu'}
        return HttpResponse(simplejson.dumps(messagedata, ensure_ascii=False))
        #return HttpResponseRedirect("/huzhu/"+str(postid)+".html?suc=1")
    else:
        err=1
        messagedata={'err':'true','errkey':'没有回复内容','type':'replyhuzhu'}
        return HttpResponse(simplejson.dumps(messagedata, ensure_ascii=False))
    #return render_to_response('huzhu/huzhureply.html',locals())

def huzhu_imgload(request):
    return render_to_response('huzhu/imgload.html',locals())

def huzhupost(request):
    username=request.session.get("username",None)
    company_id=request.session.get("company_id",None)
    if username and (company_id==None or str(company_id)=="0"):
        company_id=getcompanyid(username)
        request.session['company_id']=company_id
    
    if (username==None or (company_id==None or str(company_id)=="0")):
        return HttpResponseRedirect("/login/?done=/huzhupost/")
    #判断是否已经填写了昵称
    mynickname=getcompanynickname(company_id)
    if not mynickname:
        nickname=request.GET.get("nickname")
        if nickname:
            rpl1=re.findall('[0-9\ ]+',nickname)
            for r1 in rpl1:
                if len(r1)>10:
                    nickname=nickname.replace(r1,r1[:-3]+'***')
            addcompanynickname(nickname,company_id,username)
    #判断是否填写关注行业
    myguanzhu=gethuzhuguanzhu(company_id)
    if not myguanzhu or myguanzhu=="":
        myguanzhu=request.REQUEST.getlist("myguanzhu")
        if myguanzhu:
            addmyzhuzhuguanzhu(myguanzhu,company_id,username)
            
            
    host=getnowurl(request)
    showpost=1
    nowlanmu="<a href='/huzhu/'>再生互助</a>"
    webtitle="互助发帖-互助列表"
    suc=request.GET.get("suc")
    err=request.GET.get("err")
    category_id=request.GET.get("category_id")
    return render_to_response('aui/huzhu/post.html',locals())
    #return render_to_response('huzhupost.html',locals())
def huzhucate(request):
    host=getnowurl(request)
    showpost=1
    webtitle="再生互助"
    nowlanmu="<a href='/huzhu/'>再生互助</a>"
    username=request.session.get("username",None)
    return render_to_response('huzhucate.html',locals())

#----图片上传
def huzhu_upload(request):
    username=request.session.get("username",None)
    company_id=request.session.get("company_id",None)
    if (username==None or (company_id==None or str(company_id)=="0")):
        errlist={'err':'login'}
        return HttpResponse(simplejson.dumps(errlist, ensure_ascii=False))
    piclist=otherimgupload(request)
    if piclist:
        jsonresult={'err':'false','piclist':piclist}
        return HttpResponse(simplejson.dumps(jsonresult, ensure_ascii=False))
    else:
        jsonresult={'err':'true','errkey':'请选择一张图片'}
        return HttpResponse(simplejson.dumps(jsonresult, ensure_ascii=False))
