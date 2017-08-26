#-*- coding:utf-8 -*-
from django.shortcuts import render_to_response
import simplejson
from django.http import HttpResponse,HttpResponseRedirect,HttpResponsePermanentRedirect
import MySQLdb,sys,os,memcache,settings,urllib,re,time,requests,hashlib,StringIO,Image,ImageDraw,ImageFont,ImageFilter,random
from django.core.cache import cache
from zz91db_sex import newsdb
from zz91db_ast import companydb
from zz91tools import int_to_strall
from settings import spconfig,appurl,pyuploadpath,pyimgurl
spconfig=settings.SPHINXCONFIG
from sphinxapi import *
from zz91page import *

dbn=newsdb()
reload(sys)
sys.setdefaultencoding('UTF-8')
nowpath=os.path.dirname(__file__)
execfile(nowpath+"/func/public_function.py")
execfile(nowpath+"/func/sex_function.py")

zzn=zznews()

#----资讯首页(一期)
def newsindex(request):
    newscolumn=zzn.getnewscolumn()
    return render_to_response('sex/index.html',locals())
def navlist(request):
    column=zzn.getmyorderlist()
    return HttpResponse(simplejson.dumps(column, ensure_ascii=False))
    return render_to_response('sex/navlist.html',locals())
def mynavlist(request):
    mid=request.GET.get("mid")
    if not mid:
        mid=0
    deviceId=request.GET.get("deviceId")
    mycolumn=zzn.getnewscolumn(deviceId=deviceId)
    allcolumn=zzn.getmyorderlist()
    column={'mycolumn':mycolumn,'allcolumn':allcolumn}
    return HttpResponse(simplejson.dumps(column, ensure_ascii=False))
#----资讯搜索
def news_search(request,page=''):
    cursor_news = conn_news.cursor()
    keywords=request.GET.get("keywords")
#    page=request.GET.get("page")
    if (keywords!=None):
        keywords=keywords.replace("资讯","")
        keywords=keywords.replace("价格","")
        webtitle=keywords
    if (str(keywords)=='None'):    
        keywords=None
        webtitle="资讯中心"
    if (page=='' or page==0 or page==None):
        page=1
    nowlanmu="<a href='/news/'>资讯中心</a>"
    funpage=zz91page()
    limitNum=funpage.limitNum(10)
    nowpage=funpage.nowpage(int(page))
    frompageCount=funpage.frompageCount()
    after_range_num = funpage.after_range_num(5)
    before_range_num = funpage.before_range_num(4)
    newslist=zzn.getnewslist(keywords=keywords,frompageCount=frompageCount,limitNum=limitNum)
    listcount=0
    if (newslist):
        listall=newslist['list']
        listcount=newslist['count']
        if (int(listcount)>1000000):
            listcount=1000000-1
    listcount = funpage.listcount(listcount)
    page_listcount=funpage.page_listcount()
    firstpage = funpage.firstpage()
    lastpage = funpage.lastpage()
    page_range  = funpage.page_range()
    nextpage = funpage.nextpage()
    prvpage = funpage.prvpage()
    if (listcount==1):
        morebutton='style=display:none'
    else:
        morebutton=''
    cursor_news.close()
    return render_to_response('sex/list.html',locals())
#资讯列表页(一期)
def news_list(request):
    host=getnowurl(request)
    typeid=request.GET.get("typeid")
    page=request.GET.get("page")
    #columnid=getcolumnid(cursor_news)
    if typeid:
        typename=zzn.get_typename(typeid)
#    webtitle="资讯中心"
#    nowlanmu="<a href='newslist.html'>资讯中心</a>"
    keywords=request.GET.get("keywords")
    username=request.session.get("username",None)
    nowlanmu="<a href='/news/'>资讯中心</a>"
#    page=request.GET.get("page")
    if (keywords!=None):
        keywords=keywords.replace("资讯","")
        keywords=keywords.replace("价格","")
        webtitle=keywords
    if (str(keywords)=='None'):    
        keywords=None
        webtitle="资讯中心"
        
    if (page=='' or page==0 or page==None):
        page=1
    funpage=zz91page()
    limitNum=funpage.limitNum(20)
    nowpage=funpage.nowpage(int(page))
    frompageCount=funpage.frompageCount()
    after_range_num = funpage.after_range_num(5)
    before_range_num = funpage.before_range_num(4)
    if not typeid:
        typeidarr=None
    else:
        typeidarr=[int(typeid)]
    newslist=zzn.getnewslist(keywords=keywords,frompageCount=frompageCount,limitNum=limitNum,allnum='',typeid=typeidarr,typeid2="")
    listcount=0
    if (newslist):
        listall=newslist['list']
        listcount=newslist['count']
        if (int(listcount)>1000000):
            listcount=1000000-1
    listcount = funpage.listcount(listcount)
    page_listcount=funpage.page_listcount()
    firstpage = funpage.firstpage()
    lastpage = funpage.lastpage()
    page_range  = funpage.page_range()
    nextpage = funpage.nextpage()
    prvpage = funpage.prvpage()
#    newsnav=getnewsnav()
#    listall=listalla['list']
#    newslistcount=listalla['count']
    
    if (listcount==1):
        morebutton='style=display:none'
    else:
        morebutton=''
    #if page>1:
        #return render_to_response('sex/listmore.html',locals())
    pagetype=request.GET.get("pagetype")
    if pagetype:
        #return HttpResponse(listall)
        resultlist={"error_code":0,"reason":"","result":listall,"lastpage":page_listcount,'listcount':listcount,"queryString":{"typeid":typeid,"pagetype":pagetype}}
        response = HttpResponse(simplejson.dumps(resultlist, ensure_ascii=False))
        return response
    return render_to_response('sex/list.html',locals())

#----资讯最终页(一期)
def newsdetail(request,id=''):
    host=getnowurl(request)
    typeid=request.GET.get("typeid")
    mid=request.GET.get("mid")
    deviceId=request.GET.get("deviceId")
    webtitle="资讯中心"
    listall=[]
    zzn.newsclick_add(id)
    #记录最近浏览
    zzn.insert_viewhistory(mid,id,deviceId=deviceId)
    content=zzn.getnewscontent(id)
    content['content']=remove_content_value(content['content'])
#        content=content.replace('uploads/uploads','http://newsimg.zz91.com/uploads/uploads')
    webtitle=content['title']
    listall.append(content)
    #获得当前新闻栏目
    newstype=dbn.get_newstype(id)
    if newstype:
        typename=newstype['typename']
        typeid=newstype['typeid']
        typeid2=newstype['typeid2']
        #相关阅读
        typenews=zzn.get_typenews(typeid,typeid2)
        #上一篇文章
        #articalup=zzn.getarticalup(id,typeid)
        #下一篇文章
        #articalnx=zzn.getarticalnx(id,typeid)
        #listall['othernews']=typenews
        listall.append({'othernews':typenews})
    pagetype=request.GET.get("pagetype")
    if pagetype:
        resultlist={"error_code":0,"reason":"","result":listall,"lastpage":"",'listcount':"","queryString":{"typeid":typeid,"pagetype":pagetype}}
        response = HttpResponse(simplejson.dumps(resultlist, ensure_ascii=False))
        return response

def order(request):
    deviceId=request.GET.get("deviceId")
    tid=request.GET.get("tid")
    action=request.GET.get("action")
    zzn.saveorder(deviceId,tid,action)
    return HttpResponse(1)
#登录   
def login(request):
    userName = request.POST.get('username')
    passwd = request.POST.get('passwd')
    appid = request.POST.get('appid')
    if not userName:
        userName = request.GET.get('username')
        passwd = request.GET.get('passwd')
        appid = request.GET.get('appid')
    
    md5pwd=""
    if not userName or not passwd:
        error="用户名或密码错误"
        resultlist={"error_code":10,"reason":error,'result':'',"queryString":{}}
        return HttpResponse(simplejson.dumps(resultlist, ensure_ascii=False))
    if passwd:
        md5pwd = hashlib.md5(passwd)
        md5pwd = md5pwd.hexdigest()[8:-8]
    gmt_created=datetime.datetime.now()
    gmt_modified=datetime.datetime.now()
    token = hashlib.md5(passwd+userName+str(gmt_modified))
    token = token.hexdigest()[8:-8]
    sql="select mid from dede_member where userid=%s and pwd=%s"
    plist=dbn.fetchonedb(sql,[userName,md5pwd])
    error="suc"
    if plist:
        mid=plist[0]
        sql="select mid from member_appinfo where mid=%s"
        mlist=dbn.fetchonedb(sql,[mid])
        if mlist:
            sql="update member_appinfo set appid=%s,token=%s,gmt_modified=%s where mid=%s"
            dbn.updatetodb(sql,[appid,token,gmt_modified,mid])
        else:
            sql="insert into member_appinfo(mid,appid,token,gmt_modified) values(%s,%s,%s,%s)"
            dbn.updatetodb(sql,[mid,appid,token,gmt_modified])
        resultlist={"error_code":0,"reason":"","result":{"mid":mid,"token":token},"queryString":{}}
        return HttpResponse(simplejson.dumps(resultlist, ensure_ascii=False))
    else:
        error="用户名或密码错误"
        resultlist={"error_code":10,"reason":error,'result':'',"queryString":{}}
        return HttpResponse(simplejson.dumps(resultlist, ensure_ascii=False))
#注册
def reg(request):
    sql=""
    userid = request.POST.get('username')
    passwd = request.POST.get('passwd')
    if not userid or not passwd:
        error="错误，请填写注册信息"
        resultlist={"error_code":10,"reason":error,'result':'',"queryString":{}}
        return HttpResponse(simplejson.dumps(resultlist, ensure_ascii=False))
    if passwd:
        md5pwd = hashlib.md5(passwd)
        md5pwd = md5pwd.hexdigest()[8:-8]
    pwd=md5pwd
    gmt_created=datetime.datetime.now()
    gmt_modified=datetime.datetime.now()
    mtype="个人"
    uname="两性知识网友"
    jointime=int(time.time())
    joinip=request.META['REMOTE_ADDR']
    sql="select mid from dede_member where userid=%s"
    plist=dbn.fetchonedb(sql,[userid])
    error="suc"
    if not plist:
        sql="insert into dede_member(userid,pwd,mtype,uname,jointime,joinip) values(%s,%s,%s,%s,%s,%s)"
        dbn.updatetodb(sql,[userid,pwd,mtype,uname,jointime,joinip])
        resultlist={"error_code":0,"reason":"","result":"","queryString":{}}
        return HttpResponse(simplejson.dumps(resultlist, ensure_ascii=False))
    else:
        error="该用户名已经注册！请选择其他用户名"
        resultlist={"error_code":10,"reason":error,'result':'',"queryString":{}}
        return HttpResponse(simplejson.dumps(resultlist, ensure_ascii=False))
def modinfo(request):
    mid=request.POST.get("mid")
    userid=request.POST.get("userid")
    uname=request.POST.get("uname")
    sex=request.POST.get("sex")
    deviceId=request.POST.get("appid")
    sql="update dede_member set uname=%s,sex=%s where userid=%s"
    dbn.updatetodb(sql,[uname,sex,userid])
    resultlist={"error_code":0,"reason":uname,"result":"","queryString":{}}
    return HttpResponse(simplejson.dumps(resultlist, ensure_ascii=False))
    
#---收藏夹显示(根据mid获得)
def show_memebe_stom(request):
    mid=request.GET.get("mid")
    page=request.GET.get("page")
    deviceId=request.GET.get("deviceId")
    if (page=='' or page==0 or page==None):
        page=1
    funpage=zz91page()
    limitNum=funpage.limitNum(20)
    nowpage=funpage.nowpage(int(page))
    frompageCount=funpage.frompageCount()
    after_range_num = funpage.after_range_num(5)
    before_range_num = funpage.before_range_num(4)
    newslist=zzn.get_memebe_stom(mid=mid,frompageCount=frompageCount,limitNum=limitNum,allnum='',deviceId=deviceId)
    listcount=0
    if (newslist):
        listall=newslist['list']
        listcount=newslist['count']
        if (int(listcount)>1000000):
            listcount=1000000-1
    listcount = funpage.listcount(listcount)
    page_listcount=funpage.page_listcount()
    firstpage = funpage.firstpage()
    lastpage = funpage.lastpage()
    page_range  = funpage.page_range()
    nextpage = funpage.nextpage()
    prvpage = funpage.prvpage()
    
    resultlist={"error_code":0,"reason":"","result":listall,"lastpage":page_listcount,'listcount':listcount,"queryString":{"mid":mid}}
    return HttpResponse(simplejson.dumps(resultlist, ensure_ascii=False))

#---评论表显示(根据aid获得)
def show_feedback(request):
    aid=request.GET.get("aid")
    mid=request.GET.get("mid")
    page=request.GET.get("page")
    deviceId=request.GET.get("deviceId")
    if (page=='' or page==0 or page==None):
        page=1
    funpage=zz91page()
    limitNum=funpage.limitNum(20)
    nowpage=funpage.nowpage(int(page))
    frompageCount=funpage.frompageCount()
    after_range_num = funpage.after_range_num(5)
    before_range_num = funpage.before_range_num(4)
    newslist=zzn.get_feedback(aid=aid,mid=mid,frompageCount=frompageCount,limitNum=limitNum,allnum='',deviceId=deviceId)
    listcount=0
    if (newslist):
        listall=newslist['list']
        listcount=newslist['count']
        if (int(listcount)>1000000):
            listcount=1000000-1
    listcount = funpage.listcount(listcount)
    page_listcount=funpage.page_listcount()
    firstpage = funpage.firstpage()
    lastpage = funpage.lastpage()
    page_range  = funpage.page_range()
    nextpage = funpage.nextpage()
    prvpage = funpage.prvpage()
    
    resultlist={"error_code":0,"reason":"","result":listall,"lastpage":page_listcount,'listcount':listcount,"queryString":{"aid":aid}}
    return HttpResponse(simplejson.dumps(resultlist, ensure_ascii=False))
#---显示我的订阅(根据mid获得)
def show_myorder(request):
    mid=request.GET.get("mid")
    deviceId=request.GET.get("deviceId")
    list_myorder=zzn.get_myorder(deviceId)
    return HttpResponse(simplejson.dumps(list_myorder, ensure_ascii=False))

#---获取我的资料
def show_member(request):
    mid=request.GET.get("mid")
    info=zzn.getmemberinfo(mid)
    return HttpResponse(simplejson.dumps(info, ensure_ascii=False))

#---插入至留言板
def insert_member_guestbook(request):
    request_url=request.META.get('HTTP_REFERER','/')
    mid=request.POST.get("mid")
    if not mid:
        mid=0
    gid=request.POST.get("gid")
    if not gid:
        gid="0"
    title=request.POST.get("title")
    if not title:
        title="0"
    uname=request.POST.get("uname")
    if not uname:
        uname="0"
    email=request.POST.get("email")
    if not email:
        email="0"
    qq=request.POST.get("qq")
    if not qq:
        qq="0"
    tel=request.POST.get("tel")
    if not tel:
        tel="0"
    ip=request.META['REMOTE_ADDR']
    dtime=int(time.time())
    msg=request.POST.get("msg")
    if not msg:
        msg="null"
    zzn.insert_guestbook(mid,gid,title,uname,email,qq,tel,ip,dtime,msg)
    return HttpResponse(simplejson.dumps({"error_code":0,"reason":"","result":""}, ensure_ascii=False))
    #return HttpResponseRedirect(request_url)
#订阅
def insert_myorder(request):
    aid=request.POST.get("aid")
    if not aid:
        aid=request.GET.get("aid")
    mid=request.POST.get("mid")
    if not mid:
        mid=request.GET.get("mid")
    tid=request.POST.get("tid")
    if not tid:
        tid=request.GET.get("tid")
    fclose=request.POST.get("close")
    if not fclose:
        fclose=request.GET.get("close")
    deviceId=request.POST.get("deviceId")
    if not deviceId:
        deviceId=request.GET.get("deviceId")
    gmt_created=time.time()
    if str(fclose)=="1":
        sql="delete from myorder where deviceId=%s and tid=%s"
        dbn.updatetodb(sql,[deviceId,tid])
    else:
        sql="select id from myorder where deviceId=%s and tid=%s"
        result=dbn.fetchonedb(sql,[deviceId,tid])
        if not result:
            sql="insert into myorder (deviceId,tid,gmt_created) values(%s,%s,%s)"
            dbn.updatetodb(sql,[deviceId,tid,gmt_created])
    return HttpResponse(simplejson.dumps({"error_code":0,"reason":"","result":""}, ensure_ascii=False))
#收藏
def insert_dede_member_stow(request):
    aid=request.POST.get("aid")
    deviceId=request.POST.get("deviceId")
    arctitle="0"
    if not aid:
        aid=request.GET.get("aid")
    mid=request.POST.get("mid")
    if not mid:
        mid=request.GET.get("mid")
    if aid:
        arctitle=zzn.getnewstitle(aid)
        if arctitle:
            arctitle=arctitle['title']
    addtime=int(time.time())
    fclose=request.POST.get("close")
    if not fclose:
        fclose=request.GET.get("close")
    if not deviceId:
        deviceId=request.GET.get("deviceId")
    gmt_created=time.time()
    if fclose=="1":
        sql="delete from dede_member_stow where mid=%s and aid=%s"
        dbn.updatetodb(sql,[mid,aid])
    else:
        sql="select id from dede_member_stow where mid=%s and aid=%s"
        result=dbn.fetchonedb(sql,[mid,aid])
        if not result:
            sql="insert into dede_member_stow (mid,aid,title,addtime,deviceId) values(%s,%s,%s,%s,%s)"
            dbn.updatetodb(sql,[mid,aid,arctitle,addtime,deviceId])
    return HttpResponse(simplejson.dumps({"error_code":0,"reason":"","result":""}, ensure_ascii=False))
#写评论      
def insert_dede_feedback(request):
    aid=request.POST.get("aid")
    if not aid:
        aid=request.GET.get("aid")
    #arctitle=request.POST.get("arctitle")
    arctitle=""
    if aid:
        arctitle=zzn.getnewstitle(aid)
        if arctitle:
            arctitle=arctitle['title']
    if not aid:
        aid=0
    typeid=0
    
    ip=request.META['REMOTE_ADDR']
    ischeck=1
    dtime=int(time.time())
    mid=request.POST.get("mid")
    deviceId=request.POST.get("deviceId")
    if not deviceId:
        deviceId=request.GET.get("deviceId")
    if not mid:
        mid=request.GET.get("mid")
    msg=request.POST.get("msg")
    if not msg:
        msg=request.GET.get("msg")
    username=""
    if mid:
        username=zzn.getmemberinfo(mid)
        if username:
            username=username['uname']
    if str(username)=="null" or not username:
        username="网友"
        
    if not mid or mid=="null":
        mid=0
    sql="insert into dede_feedback(aid,username,ip,ischeck,dtime,mid,msg,arctitle,deviceId) values(%s,%s,%s,%s,%s,%s,%s,%s,%s)"
    dbn.updatetodb(sql,[aid,username,ip,ischeck,dtime,mid,msg,arctitle,deviceId])
    #sql="insert into dede_feedback(aid,username,ip) values(%s,%s,%s)"
    #dbn.updatetodb(sql,[aid,username,ip])
    return HttpResponse(simplejson.dumps({"error_code":0,"reason":username,"result":""}, ensure_ascii=False))
#---插入至最近浏览
def show_view_history(request):
    mid=request.GET.get("mid")
    page=request.GET.get("page")
    if (page=='' or page==0 or page==None):
        page=1
    funpage=zz91page()
    limitNum=funpage.limitNum(20)
    nowpage=funpage.nowpage(int(page))
    frompageCount=funpage.frompageCount()
    after_range_num = funpage.after_range_num(5)
    before_range_num = funpage.before_range_num(4)
    newslist=zzn.get_history(mid=mid,frompageCount=frompageCount,limitNum=limitNum,allnum='')
    listcount=0
    if (newslist):
        listall=newslist['list']
        listcount=newslist['count']
        if (int(listcount)>1000000):
            listcount=1000000-1
    listcount = funpage.listcount(listcount)
    page_listcount=funpage.page_listcount()
    firstpage = funpage.firstpage()
    lastpage = funpage.lastpage()
    page_range  = funpage.page_range()
    nextpage = funpage.nextpage()
    prvpage = funpage.prvpage()
    
    resultlist={"error_code":0,"reason":"","result":listall,"lastpage":page_listcount,'listcount':listcount,"queryString":{"mid":mid}}
    return HttpResponse(simplejson.dumps(resultlist, ensure_ascii=False))
    
#----图片上传
def upload(request):
    mid=request.POST.get("mid")
    timepath=time.strftime('%Y/%m/%d/',time.localtime(time.time()))
    gmt_created=datetime.datetime.now()
    nowtime=int(time.time())
    if request.FILES:
        file = request.FILES['file']
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
        im.thumbnail((nwidth,nheight),Image.ANTIALIAS)
        tmp = random.randint(100, 999)
        newpath=pyuploadpath+timepath
        imgpath=newpath+str(nowtime)+str(tmp)+"."+im.format
        if not os.path.isdir(newpath):
            os.makedirs(newpath)

#        im.save(imgpath,im.format,quality = 100)

        des_origin_f = open(imgpath,"w")
        for chunk in file.chunks():  
            des_origin_f.write(chunk)  
        des_origin_f.close()

        mstream.closed
        tempim.closed
        picurl=imgpath.replace(pyuploadpath,'')
        pic_url=pyimgurl+picurl
        sql="update dede_member set face=%s where mid=%s"
        dbn.updatetodb(sql,[pic_url,mid])
        resultlist={"error_code":0,"reason":"","result":pic_url,"queryString":{"mid":mid}}
        return HttpResponse(simplejson.dumps(resultlist, ensure_ascii=False))
    #return render_to_response('imgload.html',locals())
    return HttpResponse(simplejson.dumps({"error_code":10,"reason":""}, ensure_ascii=False))
def insert_feedback_goodbad(request):
    aid=request.POST.get("aid")
    tid=request.POST.get("tid")
    if str(tid)=="0":
        sql="update dede_feedback set bad=bad+1 where id=%s"
        dbn.updatetodb(sql,[aid])
    if str(tid)=="1":
        sql="update dede_feedback set good=good+1 where id=%s"
        dbn.updatetodb(sql,[aid])
    return HttpResponse(simplejson.dumps({}, ensure_ascii=False))
    


    