#-*- coding:utf-8 -*-
from django.shortcuts import render_to_response
from django.http import HttpResponse,HttpResponseRedirect,HttpResponsePermanentRedirect
import MySQLdb,sys,os,memcache,settings,urllib,re,time,datetime,requests
from django.core.cache import cache
from sphinxapi import *
from zz91page import *

from settings import spconfig
from function import getnowurl
from zz91db_ast import companydb
from zz91db_sms import smsdb
from zz91db_2_news import newsdb
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
execfile(nowpath+"/commfunction.py")
execfile(nowpath+"/function.py")

zzcompany=zcompany()
zzqianbao=qianbao()
zztrade=ztrade()
ldb_weixin=ldbweixin()

def huzhu_wenda(request):
    return huzhu(request,category_id=1)
def huzhu_shequ(request):
    return huzhu(request,category_id=2)
def huzhu_xueyuan(request):
    return huzhu(request,category_id=3)
def huzhu_remen(request):
    return huzhu(request,htype="hot")
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

    keywords=request.GET.get("keywords")
    username=request.session.get("username",None)
    company_id=request.session.get("company_id",None)
    if not htype:
        htype=request.GET.get("htype")
    #判断是否已经填写了昵称
#    mynickname=getcompanynickname(company_id)
#    if not mynickname:
#        nickname=request.GET.get("nickname")
#        if nickname:
#            rpl1=re.findall('[0-9\ ]+',nickname)
#            for r1 in rpl1:
#                if len(r1)>10:
#                    nickname=nickname.replace(r1,r1[:-3]+'***')
#            addcompanynickname(nickname,company_id,username)
    #判断是否填写关注行业
    myguanzhu=gethuzhuguanzhu(company_id)
    if not myguanzhu or myguanzhu=="":
        myguanzhu=request.REQUEST.getlist("myguanzhu")
        if myguanzhu:
            addmyzhuzhuguanzhu(myguanzhu,company_id,username)
    category_id=str(category_id)
    if (keywords!=None):
        webtitle=keywords+"-互助列表"
    if (str(keywords)=='None'):    
        keywords=None
        webtitle="互助列表"
        datefirst=1
    if (str(category_id)=='None'):
        category_id=None
    if (category_id==None and keywords==None):
        #category_id=1
        webtitle="废料问答-互助列表"
    if (str(category_id)=='1'):
        labelstyle1="class=chk"
        labelstyle2=""
        labelstyle3=""
        webtitle="废料问答-互助列表"
    if (str(category_id)=='2'):
        labelstyle1=""
        labelstyle2="class=chk"
        labelstyle3=""
        webtitle="废料社区-互助列表"
    if (str(category_id)=='3'):
        labelstyle1=""
        labelstyle2=""
        labelstyle3="class=chk"
        webtitle="江湖学院-互助列表"
    #bbslistall=getbbslist(keywords,0,20,category_id)
#    return render_to_response('huzhu/huzhu2.html',locals())
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
    """
    #----每日每周每月
    serverida=spconfig['serverid']
    if keywords==None:
        bbslistall=getbbslist(keywords,0,20,category_id,datetype=datetype,htype=htype)
    else:
        bbslistall=getbbslist(keywords,0,20,category_id,datetype=datetype,htype=htype)
    
    
    bbslist=bbslistall['list']
    bbslistcount=bbslistall['count']
    if (bbslistcount==1):
        morebutton='style=display:none'
    else:
        morebutton=''

    return render_to_response('huzhu/huzhu2.html',locals())

    
def huzhumore(request):
    username=request.session.get("username",None)
    category_id=request.GET.get("category_id")
    datetype=request.GET.get("datetype")
    keywords=request.GET.get("keywords")
    htype=request.GET.get("htype")
    if (keywords!=None):
        webtitle=keywords+"互助列表"
    if (str(keywords)=='None'):    
        keywords=None
    page=request.GET.get("page")
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
    
    if keywords==None:
        bbslistall=getbbslist(keywords,(int(page)-1)*20+1,20,category_id,datetype=datetype,htype=htype)
    else:
        bbslistall=getbbslist(keywords,(int(page)-1)*20+1,20,category_id,datetype=datetype,htype=htype)
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
    #判断是否已经填写了昵称
    mynickname=getcompanynickname(mycompany_id)
    if not mynickname:
        nickname=request.GET.get("nickname")
        if nickname:
            rpl1=re.findall('[0-9\ ]+',nickname)
            for r1 in rpl1:
                if len(r1)>10:
                    nickname=nickname.replace(r1,r1[:-3]+'***')
            addcompanynickname(nickname,mycompany_id,username)
    #判断是否填写关注行业
    myguanzhu=gethuzhuguanzhu(mycompany_id)
    if not myguanzhu or myguanzhu=="":
        myguanzhu=request.REQUEST.getlist("myguanzhu")
        if myguanzhu:
            addmyzhuzhuguanzhu(myguanzhu,mycompany_id,username)
    
    if mycompany_id!=None:
        
        sql="update bbs_invite set is_viewed='1',answercheck=1,gmt_created=%s where company_id=%s and post_id=%s"
        dbc.updatetodb(sql,[gmt_created,mycompany_id,id])
        sqlp="select id from bbs_post_viewed where company_id=%s and bbs_post_id=%s"
        alist=dbc.fetchonedb(sqlp,[mycompany_id,id])
        if alist:
            sql="update bbs_post_viewed set is_viewed=1,gmt_created=%s where company_id=%s and bbs_post_id=%s"
            dbc.updatetodb(sql,[gmt_created,mycompany_id,id])
        else:
            sql="insert into bbs_post_viewed(gmt_created,company_id,bbs_post_id,is_viewed) values(%s,%s,%s,%s)"
            dbc.updatetodb(sql,[gmt_created,mycompany_id,id,1])
        
    mynickname=getusername(mycompany_id)
    replycount=0
    sql="select title,content,account,gmt_created,bbs_post_category_id,company_id from bbs_post where id=%s"
    alist=dbc.fetchonedb(sql,[str(id)])
    if alist:
        title=alist[0]
        huzhuclick_add(id)
        content=alist[1]
        if (title!=None):
            webtitle=title+"-互助列表"
        company_id=alist[5]
        nickname=getusername(company_id)
        sqlp="select file_path from bbs_post_upload_file where bbs_post_id=%s"
        presult=dbc.fetchalldb(sqlp,[id])
        picurllist=[]
        if presult:
            for ll in presult:
                plist={'file_path':ll[0]}
                picurllist.append(plist)
        gmt_created=alist[3].strftime( '%-Y-%-m-%-d %-H:%-M:%-S')
        bbs_post_category_id=alist[4]
        content=content.replace("http://huzhu.zz91.com/viewReply","http://m.zz91.com/huzhuview/viewReply")
        content=replacepic(content)
        content=replacetel(content)
        content=replaceurl(content)
        if content=="":
            content==None
        replycount=gethuzhureplaycout(id)

    listall_reply=replylist(id,0,10)
    if not replycount:
        replycount=0
    if (int(replycount)>10):
        moreflag=1
    else:
        moreflag=None
    
    return render_to_response('huzhu/huzhuview2.html',locals())
#---查看更多回复
def replymore(request):
    page=request.GET.get("page")
    type=request.GET.get("type")
    if page==None:
        page=1
    postid=request.GET.get("postid")
    replyid=request.GET.get("replyid")
    if type=="0":
        listall_reply=replylist(postid,(int(page)-1)*10+1,10)
        return render_to_response('huzhu/replymore.html',locals())
    if type=="1":
        listall_reply=replyreplylist(replyid,(int(page)-1)*10+1,10)
        return render_to_response('huzhu/replyreplymore.html',locals())
    
    return render_to_response('huzhu/replymore.html',locals())
#----保存发布帖子
def huzhupostsave(request):
    bbs_post_id = request.POST['category_id']
    picidlist = request.POST['picidlist']
    if (bbs_post_id==None or bbs_post_id==""):
        bbs_post_id=106
    content = request.POST['content']
    if content:
        rpl1=re.findall('[0-9\ ]+',content)
        for r1 in rpl1:
            if len(r1)>10:
                content=content.replace(r1,r1[:-3]+'***')
    title=""
    gmt_created=datetime.datetime.now()
    gmt_modified=datetime.datetime.now()
    username=request.session.get("username",None)
    company_id=request.session.get("company_id",None)
    if username and (company_id==None or str(company_id)=="0"):
        company_id=getcompanyid(username)
        request.session['company_id']=company_id
    bbs_post_assist_id=107
    if (username==None or (company_id==None or str(company_id)=="0")):
        return HttpResponseRedirect("/login/?done=/huzhupost/")
    if (content and content!=""):
        bbs_user_profiler_id=getprofilerid(username)
        if (bbs_user_profiler_id==None):
            bbs_user_profiler_id=1
        value=[company_id,bbs_user_profiler_id,username,1,title,content,0,1,gmt_created,gmt_modified,gmt_modified,gmt_modified,1,bbs_post_assist_id]
        sql="insert into bbs_post(company_id,bbs_user_profiler_id,account,bbs_post_category_id,title,content,is_del,check_status,gmt_created,gmt_modified,post_time,reply_time,postsource,bbs_post_assist_id) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        dbc.updatetodb(sql,value)
        if picidlist!="":
            sql_bbs_post='SELECT max(id) from bbs_post where title=%s'
            result=dbc.fetchonedb(sql_bbs_post,[title])
            if result:
                bbs_post_id=result[0]
                sql_pic='update bbs_post_upload_file set bbs_post_id=%s where id in (%s)'
                dbc.updatetodb(sql_pic,[bbs_post_id,picidlist])
        #return HttpResponseRedirect("/huzhu/?datetype=1")
        return HttpResponseRedirect("/huzhupost/?category_id="+str(bbs_post_id)+"&suc=1#hh")
    else:
        return HttpResponseRedirect("/huzhupost/?category_id="+str(bbs_post_id)+"&err=1#hh")
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
    return render_to_response('huzhu/huzhureply.html',locals())
#----发帖人回复
def reply_reply(request):
    host=getnowurl(request)
    replyid=request.POST.get('replyid')
    postid=request.POST.get('postid')
    replycontent=request.POST.get('replycontent')
    tocompany_id=request.POST.get('tocompany_id')
    nowlanmu="<a href='/huzhu/'>再生互助</a>"
    gmt_created=datetime.datetime.now()
    gmt_modified=datetime.datetime.now()
    title=""
    username=request.session.get("username",None)
    company_id=request.session.get("company_id",None)
    if username and (company_id==None or str(company_id)=="0"):
        company_id=getcompanyid(username)
        request.session['company_id']=company_id
    
    if (username==None or (company_id==None or str(company_id)=="0")):
        return HttpResponseRedirect("/login/")
    if replycontent:
        value=[company_id,username,title,postid,replycontent,0,0,gmt_created,gmt_modified,replyid,tocompany_id,1]
        sql="insert into bbs_post_reply(company_id,account,title,bbs_post_id,content,is_del,check_status,gmt_created,gmt_modified,bbs_post_reply_id,tocompany_id,postsource) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        dbc.updatetodb(sql,value)
        sql="update bbs_post set reply_time=%s,reply_count=reply_count+1,gmt_modified=%s where id=%s"
        dbc.updatetodb(sql,[gmt_modified,gmt_modified,postid])
        sql="select max(id) from bbs_post_reply where bbs_post_id=%s"
        alist=dbc.fetchonedb(sql,[postid])
        nickname=""
        replyid=0
        if alist:
            replyid=alist[0]
            nickname=getusername(company_id)
            tonickname=getusername(tocompany_id)
        posttime=formattime(gmt_created,0)
        updatepostviewed(tocompany_id,postid)
        #----更新弹窗
        updateopenfloat(tocompany_id,0)
        suc=1
        return HttpResponseRedirect("/huzhu/"+str(postid)+".html?suc=1")
    else:
        err=1
    return render_to_response('huzhu/huzhureply.html',locals())
    #return render_to_response('huzhu/replytext.html',locals())
    #return HttpResponse(simplejson.dumps("[{'replyid':'"+str(replyid)+"','nickname':'"+nickname+"'}]", ensure_ascii=False))

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
    return render_to_response('huzhupost.html',locals())
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
    timepath=time.strftime('%Y/%m/%d/',time.localtime(time.time()))
    gmt_created=datetime.datetime.now()
    nowtime=int(time.time())
    if request.FILES:
        file = request.FILES['file']
        #image = Image.open(reqfile)
        suportFormat = ['BMP', 'GIF', 'JPG','JPGE', 'PNG','JPEG']
        #image.thumbnail((128,128),Image.ANTIALIAS)
        tempim = StringIO.StringIO()
        mstream = StringIO.StringIO(file.read())
        im = Image.open(mstream)
        rheight=500
        rwidth=500
        
        pwidth=im.size[0]
        pheight=im.size[1]
        
        rate = int(pwidth/pheight)
        if rate==0:
            rate=1
        nwidth=200
        nheight=200
        if (pwidth>rwidth):
            nwidth=rwidth
            nheight=nwidth /rate
        else:
            nwidth=pwidth
            nheight=pheight
        
        if (pheight>rheight):
            nheight=rheight
            nwidth=rheight*rate
        else:
            nwidth=pwidth
            nheight=pheight
        
        #im.thumbnail((10,10),Image.ANTIALIAS)
        im.thumbnail((nwidth,nheight),Image.ANTIALIAS)
        tmp = random.randint(100, 999)
        
        newpath=pyuploadpath+timepath
        
        imgpath=newpath+str(nowtime)+str(tmp)+"."+im.format
        if not os.path.isdir(newpath):
            os.makedirs(newpath)
        im.save(imgpath,im.format,quality = 60)
        mstream.closed
        tempim.closed
        picurl=pyimgurl+timepath+str(nowtime)+str(tmp)+"."+im.format

        sql='insert into bbs_post_upload_file(company_id,bbs_post_id,file_path,gmt_created) values(%s,0,%s,%s)'
        dbc.updatetodb(sql,[company_id,picurl,gmt_created])
        sql1="select id from bbs_post_upload_file where file_path=%s"
        productspicresult=dbc.fetchonedb(sql1,[picurl])
        if productspicresult:
            productspicid=productspicresult[0]
            return HttpResponse("<script>parent.changepic('"+picurl+"','"+str(productspicid)+"')</script>")
    return HttpResponse("请选择一张图片.")