#-*- coding:utf-8 -*-
from django.shortcuts import render_to_response
import simplejson
from django.http import HttpResponse,HttpResponseRedirect,HttpResponsePermanentRedirect
import MySQLdb,sys,os,json,memcache,settings,urllib,urllib2,cStringIO,re,time,requests,hashlib,StringIO,Image,ImageDraw,ImageFont,ImageFilter,random
from django.core.cache import cache
from urllib import quote
from zz91db_dacong import dacongdb
from zz91tools import int_to_strall
from settings import spconfig,appurl,pyuploadpath,pyimgurl
from xml.etree import ElementTree as ET
from dict2xml import dict2xml
spconfig=settings.SPHINXCONFIG
from sphinxapi import *
from zz91page import *
import top.api

dbn=dacongdb()
reload(sys)
sys.setdefaultencoding('UTF-8')
nowpath=os.path.dirname(__file__)
execfile(nowpath+"/func/public_function.py")
execfile(nowpath+"/func/dacong_function.py")

zzn=zznews()
def columnall(request):
    deviceId=request.GET.get("deviceId")
    userinfo=zzn.getuserinfo(deviceId=deviceId)
    listall=zzn.getcolumnall()
    listall['userinfo']=userinfo
    return HttpResponse(simplejson.dumps(listall, ensure_ascii=False))
def mycolumlist(request):
    deviceId=request.GET.get("deviceId")
    mid=request.GET.get("mid")
    listall=zzn.getcolumnall(mid=mid)
    return HttpResponse(simplejson.dumps(listall, ensure_ascii=False))
def navlist(request):
    reid=request.GET.get("reid")
    deviceId=request.GET.get("deviceId")
    type=request.GET.get("type")
    typeid=request.GET.get("typeid")
    mid=request.GET.get("mid")
    if (type=="tj"):
        column = [{
            "typename" : "热门",
            "url":"../list/list1.html",
            "pageParam":{'type':'hot'}
        }, {
            "typename" : "喜欢",
            "url":"../list/list1.html",
            "pageParam":{'type':'like'}
        }, {
            "typename" : "推荐",
            "url":"../list/list1.html",
            "pageParam":{'flag':'c'}
        }]
        return HttpResponse(simplejson.dumps(column, ensure_ascii=False))
    if (type=="gz"):
        column=zzn.getmyguanzhu(mid=mid)
        return HttpResponse(simplejson.dumps(column, ensure_ascii=False))
    column=zzn.getnewscolumn(reid=reid,typeid=typeid,deviceId=deviceId)
    if not column:
        column={'err':'true'}
    return HttpResponse(simplejson.dumps(column, ensure_ascii=False))
def mynavlist(request):
    mid=request.GET.get("mid")
    if not mid:
        mid=0
    reid=request.GET.get("reid")
    deviceId=request.GET.get("deviceId")
    mycolumn=zzn.getnewscolumn(deviceId=deviceId)
    allcolumn=zzn.getmyorderlist()
    column={'mycolumn':mycolumn,'allcolumn':allcolumn}
    return HttpResponse(simplejson.dumps(column, ensure_ascii=False))
#记录搜索
def savesearchkey(request):
    mid=request.GET.get("mid")
    if not mid:
        mid=0
    keywords=request.GET.get("keywords")
    sql="select aid from dede_search_keywords where keyword=%s and mid=%s"
    result=dbn.fetchonedb(sql,[keywords,mid])
    if not result:
        sql="insert into dede_search_keywords(spwords,keyword,mid) values(%s,%s,%s)"
        dbn.updatetodb(sql,[keywords,keywords,mid])
    list={'err':'false'}
    return HttpResponse(simplejson.dumps(list, ensure_ascii=False))
#搜索记录
def searchhistory(request):
    mid=request.GET.get("mid")
    if not mid:
        mid=0
    sql="select keyword from dede_search_keywords where mid=%s limit 0,20"
    result=dbn.fetchalldb(sql,[mid])
    listall=[]
    if result:
        for list in result:
            l={'keywords':list[0]}
            listall.append(l)
    return HttpResponse(simplejson.dumps(listall, ensure_ascii=False))
#----资讯搜索
def news_search(request,page=''):
    keywords=request.GET.get("keywords")
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
    return render_to_response('sex/list.html',locals())
#资讯列表页(一期)
def news_list(request):
    host=getnowurl(request)
    page=request.GET.get("page")
    typeid=request.GET.get("typeid")
    type=request.GET.get("type")
    flag=request.GET.get("flag")
    mid=request.GET.get("mid")
    keywords=request.GET.get("keywords")
    if mid and keywords:
        value=[mid]
        sql="select id from myguanzhu where mid=%s"
        if (typeid and str(typeid)!="0" and str(typeid)!=""):
            sql+=" and typeid in (%s)"
            value.append(typeid)
        sql+=" and tags=%s"
        value.append(keywords)
        result=dbn.fetchonedb(sql,value)
        if result:
            sql="update myguanzhu set maxnewstime=%s where id=%s"
            dbn.updatetodb(sql,[time.time(),result[0]])
    if typeid:
        typename=zzn.get_typename(typeid)
    
    username=request.session.get("username",None)
    nowlanmu="<a href='/news/'>资讯中心</a>"
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
    
    #if type=="new":
        #头部滚动图片
        #toppiclist=zzn.getnewspiclist(keywords=keywords,typeid=typeidarr,typeid2="",type=type,flag=flag)
    #else:
        #toppiclist=None
    toppiclist=None
    newslist=zzn.getnewslist(keywords=keywords,frompageCount=frompageCount,limitNum=limitNum,allnum='',typeid=typeidarr,typeid2="",type=type,flag=flag)
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
    datatype=request.GET.get("datatype")
    if datatype:
        resultlist={"error_code":0,"reason":"","result":listall,"pagecount":page_listcount,'listcount':listcount,'toppiclist':toppiclist,"queryString":{"typeid":typeid,"datatype":datatype}}
        response = HttpResponse(simplejson.dumps(resultlist, ensure_ascii=False))
        return response
    return render_to_response('sex/list.html',locals())
#获得资讯数和关注数
def newstitlecount(request):
    keywords=request.GET.get("keywords")
    mid=request.GET.get("mid")
    resultlist=zzn.getnewstitlecount(keywords,mid=mid)
    response = HttpResponse(simplejson.dumps(resultlist, ensure_ascii=False))
    return response
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
    content=zzn.getnewscontent(id,mid=mid)
    if content:
        cstyle=content.get("cstyle")
        detail=content['content'].lower()
        detail=remove_script(detail)
        title=filter_tags(content['title'])
        detail=qqvadio(detail)
        #detail=re.sub('<iframe.*?>','',detail)
        if str(cstyle)=="1":
            content['content']=remove_content_value(detail)
        else:
            content['content']=detail
        content['title']=title
        webtitle=content['title']
        listall.append(content)
        
    resultlist={"error_code":0,"reason":"","result":listall,"lastpage":"",'listcount':"","queryString":{"typeid":typeid}}
    response = HttpResponse(simplejson.dumps(resultlist, ensure_ascii=False))
    return response
#意见反馈
def feedback(request):
    mid=request.POST.get("mid")
    content=request.POST.get("content")
    usertoken=request.POST.get("usertoken")
    if not getloginstatus(mid,usertoken):
        errlist={'tokenerr':'true'}
        return HttpResponse(simplejson.dumps(errlist, ensure_ascii=False))
    gmt_created=datetime.datetime.now()
    sql="insert into feedback(mid,gmt_created,content) values(%s,%s,%s)"
    dbn.updatetodb(sql,[mid,gmt_created,content])
    resultlist={'err':'false','errkey':'提交成功，我们会尽快回复。'}
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
    mobile = request.POST.get('mobile')
    passwd = request.POST.get('passwd')
    appid = request.POST.get('deviceId')
    
    md5pwd=""
    if not mobile or not passwd:
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
    sql="select mid from dede_member where mobile=%s and pwd=%s"
    plist=dbn.fetchonedb(sql,[mobile,md5pwd])
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
    marry = request.POST.get('marry')
    sex = request.POST.get('sex')
    #userid = request.POST.get('username')
    #passwd = request.POST.get('passwd')
    deviceId=request.POST.get("deviceId")
    userid = "dacong"+str(random.randint(10000, 99999))
    passwd = str(random.randint(10000, 99999))
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
    uname="网友"
    jointime=int(time.time())
    joinip=request.META['HTTP_X_FORWARDED_FOR']
    sql="select mid from dede_member where deviceId=%s"
    plist=dbn.fetchonedb(sql,[deviceId])
    error="suc"
    if not plist:
        sql="insert into dede_member(userid,pwd,mtype,uname,jointime,joinip,sex,marry,deviceId) values(%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        result=dbn.updatetodb(sql,[userid,pwd,mtype,uname,jointime,joinip,sex,marry,deviceId])
        lastmid=result[0]
        if lastmid:
            sql="insert into "
        
        token = hashlib.md5(pwd+userid+str(gmt_modified))
        token = token.hexdigest()[8:-8]
        zzn.savetoken(lastmid,token,deviceId)
        resultlist={"error_code":0,"reason":"","result":"","queryString":{}}
        return HttpResponse(simplejson.dumps(resultlist, ensure_ascii=False))
    else:
        error="该用户名已经注册！请选择其他用户名"
        resultlist={"error_code":10,"reason":error,'result':'',"queryString":{}}
        return HttpResponse(simplejson.dumps(resultlist, ensure_ascii=False))
#绑定手机，验证码
def auth_yzmcode(request):
    usertoken=request.POST.get("usertoken")
    appsystem=request.POST.get("appsystem")
    mid = request.POST.get('mid')
    mobilemod = request.POST.get('mobile')
    deviceId=request.POST.get("deviceId")
    
    #修改密码
    sqlc="select mobile from dede_member where mid=%s"
    list=dbn.fetchonedb(sqlc,[mid]);
    if list:
        mobile=list[0]
        if not mobile or mobile=="":
            mobile=mobilemod
        if mobile:
            smsreresult=postsms(mobile,mid)
            if (smsreresult!=True):
                errkey=smsreresult
                err="true"
            else:
                errkey="发送成功"
                err="false"
        else:
            errkey="系统错误！"+company_id
            err="true"
    else:
        errkey="系统错误，账号不存在！"
        err="true"
    messagedata={'err':err,'errkey':errkey}
    return HttpResponse(simplejson.dumps(messagedata, ensure_ascii=False))
#注册
def regsuc(request):
    mid=request.POST.get("mid")
    mobile=request.POST.get("mobile")
    
    usertoken=request.POST.get("usertoken")
    if not getloginstatus(mid,usertoken):
        errlist={'tokenerr':'true'}
        return HttpResponse(simplejson.dumps(errlist, ensure_ascii=False))
    
    yzcode=request.POST.get("yzcode")
    newcold=request.POST.get("newcold")
    sedcold=request.POST.get("sedcold")
    err="true"
    errkey="用户有误！账号不存在或未录入验证码！"
    if mid and yzcode and newcold:
        md5pwd = hashlib.md5(newcold)
        md5pwd = md5pwd.hexdigest()[8:-8]
        sql="select code from mobile_code where mid=%s and TIMESTAMPDIFF(MINUTE,gmt_created,now())<=10"
        result=dbn.fetchonedb(sql,[mid])
        if not result:
            errkey="短信验证码过期，请重新获取！"
            err="true"
        else:
            code=result[0]
            if yzcode==code:
                sql="update dede_member set mobile=%s,pwd=%s where mid=%s"
                dbn.updatetodb(sql,[mobile,md5pwd,mid])
                errkey="注册成功！"
                err="false"
            else:
                errkey="短信验证码有误，请重新录入！"
                err="true"
    messagedata={'err':err,'errkey':errkey}
    return HttpResponse(simplejson.dumps(messagedata, ensure_ascii=False))
#获取token
def tokeninfo(request):
    token=request.POST.get("usertoken")
    mid=request.POST.get("mid")
    messagedata={'err':'true','errkey':'未获得TOKEN','result':''}
    if mid:
        #过期时间为2小时  MINUTE,HOUR
        sql="select token from member_appinfo where mid=%s and token=%s and TIMESTAMPDIFF(HOUR,gmt_modified,NOW())<=2"
        listd=dbn.fetchonedb(sql,[mid,token])
        if not listd:
            messagedata={'err':'true','errkey':'未获得TOKEN','result':token}
            return get_token(request)
        else:
            messagedata={'err':'false','errkey':'','result':token}
    return HttpResponse(simplejson.dumps(messagedata, ensure_ascii=False))
#获取新token
def get_token(request):
    token=request.POST.get("usertoken")
    mid=request.POST.get("mid")
    pwd_hash=request.POST.get("pwd_hash")
    deviceId=request.POST.get("deviceId")
    #md5pwd=pwd_hash[8:-8]
    md5pwd=pwd_hash
    gmt_created=datetime.datetime.now()
    gmt_modified=datetime.datetime.now()
    messagedata={'err':'true','errkey':'','result':''}
    sql="select userid from dede_member where mid=%s and pwd=%s and deviceId=%s"
    result=dbn.fetchonedb(sql,[mid,md5pwd,deviceId])
    if result:
        userid=result[0]
        token = hashlib.md5(str(md5pwd)+str(userid)+str(gmt_modified))
        token = token.hexdigest()[8:-8]
        messagedata={'err':'false','errkey':'','result':token}
        sql="select mid from member_appinfo where mid=%s"
        mlist=dbn.fetchonedb(sql,[mid])
        if mlist:
            sql="update member_appinfo set appid=%s,token=%s,gmt_modified=%s where mid=%s"
            dbn.updatetodb(sql,[deviceId,token,gmt_modified,mid])
        else:
            sql="insert into member_appinfo(mid,appid,token,gmt_modified) values(%s,%s,%s,%s)"
            dbn.updatetodb(sql,[mid,deviceId,token,gmt_modified])
    return HttpResponse(simplejson.dumps(messagedata, ensure_ascii=False))
#修改我的资料
def modinfo(request):
    mid=request.POST.get("mid")
    usertoken=request.POST.get("usertoken")
    if not getloginstatus(mid,usertoken):
        errlist={'tokenerr':'true'}
        return HttpResponse(simplejson.dumps(errlist, ensure_ascii=False))
    
    piclist=upload(request)
        
    userid=request.POST.get("userid")
    uname=request.POST.get("uname")
    sex=request.POST.get("sex")
    marry=request.POST.get("marry")
    mobile=request.POST.get("mobile")
    deviceId=request.POST.get("deviceId")
    
    sql="update dede_member set uname=%s,sex=%s,marry=%s,mobile=%s where mid=%s"
    dbn.updatetodb(sql,[uname,sex,marry,mobile,mid])
    messagedata={'err':'false','errkey':'保存成功！','result':''}
    return HttpResponse(simplejson.dumps(messagedata, ensure_ascii=False))
    
#---收藏夹显示(根据mid获得)
def show_memebe_stom(request):
    mid=request.GET.get("mid")
    usertoken=request.GET.get("usertoken")
    if not getloginstatus(mid,usertoken):
        errlist={'tokenerr':'true'}
        return HttpResponse(simplejson.dumps(errlist, ensure_ascii=False))
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
    newslist=zzn.get_memebe_stom(mid=mid,frompageCount=frompageCount,limitNum=limitNum,allnum='')
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
    
    resultlist={"error_code":0,"reason":"","result":listall,"page_listcount":page_listcount,'listcount':listcount,"queryString":{"mid":mid}}
    return HttpResponse(simplejson.dumps(resultlist, ensure_ascii=False))
#删除收藏夹
def del_memebe_stom(request):
    mid=request.GET.get("mid")
    usertoken=request.GET.get("usertoken")
    if not getloginstatus(mid,usertoken):
        errlist={'tokenerr':'true'}
        return HttpResponse(simplejson.dumps(errlist, ensure_ascii=False))
    id=request.GET.get("id")
    sql="delete from dede_member_stow where id=%s and mid=%s"
    dbn.updatetodb(sql,[id,mid])
    return HttpResponse(simplejson.dumps({'err':'false'}, ensure_ascii=False))

#---评论表显示(根据aid获得)
def show_feedback(request):
    aid=request.GET.get("aid")
    mid=request.GET.get("mid")
    usertoken=request.GET.get("usertoken")
    if not getloginstatus(mid,usertoken):
        errlist={'tokenerr':'true'}
        return HttpResponse(simplejson.dumps(errlist, ensure_ascii=False))
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
    newslist=zzn.get_feedback(aid=aid,frompageCount=frompageCount,limitNum=limitNum,allnum='',deviceId=deviceId)
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
    
    resultlist={"error_code":0,"reason":"","result":listall,"pagecount":page_listcount,'listcount':listcount,"queryString":{"aid":aid}}
    return HttpResponse(simplejson.dumps(resultlist, ensure_ascii=False))
#---显示我的订阅(根据mid获得)
def show_myorder(request):
    mid=request.GET.get("mid")
    usertoken=request.GET.get("usertoken")
    if not getloginstatus(mid,usertoken):
        errlist={'tokenerr':'true'}
        return HttpResponse(simplejson.dumps(errlist, ensure_ascii=False))
    deviceId=request.GET.get("deviceId")
    list_myorder=zzn.get_myorder(deviceId)
    return HttpResponse(simplejson.dumps(list_myorder, ensure_ascii=False))

#---获取我的资料
def show_member(request):
    mid=request.GET.get("mid")
    usertoken=request.GET.get("usertoken")
    if not getloginstatus(mid,usertoken):
        errlist={'tokenerr':'true'}
        return HttpResponse(simplejson.dumps(errlist, ensure_ascii=False))
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
    arctitle="0"
    mid=request.POST.get("mid")
    usertoken=request.POST.get("usertoken")
    if not getloginstatus(mid,usertoken):
        errlist={'tokenerr':'true'}
        return HttpResponse(simplejson.dumps(errlist, ensure_ascii=False))
    if aid:
        arctitle=zzn.getnewstitle(aid)
        if arctitle:
            arctitle=arctitle['title']
    addtime=int(time.time())
    fclose=request.POST.get("close")
    gmt_created=time.time()
    if fclose=="1":
        sql="delete from dede_member_stow where mid=%s and aid=%s"
        dbn.updatetodb(sql,[mid,aid])
    else:
        sql="select id from dede_member_stow where mid=%s and aid=%s"
        result=dbn.fetchonedb(sql,[mid,aid])
        if not result:
            sql="insert into dede_member_stow (mid,aid,title,addtime) values(%s,%s,%s,%s)"
            dbn.updatetodb(sql,[mid,aid,arctitle,addtime])
    return HttpResponse(simplejson.dumps({"error_code":0,"reason":"","result":''}, ensure_ascii=False))
#关注
def insert_myguanzhu(request):
    mid=request.POST.get("mid")
    usertoken=request.POST.get("usertoken")
    if not getloginstatus(mid,usertoken):
        errlist={'tokenerr':'true'}
        return HttpResponse(simplejson.dumps(errlist, ensure_ascii=False))
    tags=request.POST.get("tags")
    typeid=request.POST.get("typeid")
    fclose=request.POST.get("close")
    addtime=time.time()
    if str(fclose)=="1":
        sql="delete from myguanzhu where mid=%s and tags=%s"
        dbn.updatetodb(sql,[mid,tags])
        delflag=1
    else:
        sql="select id from myguanzhu where mid=%s and tags=%s"
        result=dbn.fetchonedb(sql,[mid,tags])
        if not result:
            sql="insert into myguanzhu (mid,tags,typeid,addtime) values(%s,%s,%s,%s)"
            dbn.updatetodb(sql,[mid,tags,typeid,addtime])
        delflag=0
    return HttpResponse(simplejson.dumps({"error_code":0,"reason":"","result":tags,'delflag':delflag}, ensure_ascii=False))
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
    sql="insert into dede_feedback(aid,username,ip,ischeck,dtime,mid,msg,arctitle) values(%s,%s,%s,%s,%s,%s,%s,%s)"
    dbn.updatetodb(sql,[aid,username,ip,ischeck,dtime,mid,msg,arctitle])
    #sql="insert into dede_feedback(aid,username,ip) values(%s,%s,%s)"
    #dbn.updatetodb(sql,[aid,username,ip])
    return HttpResponse(simplejson.dumps({"error_code":0,"reason":username,"result":""}, ensure_ascii=False))
#---最近浏览
def show_view_history(request):
    mid=request.GET.get("mid")
    usertoken=request.GET.get("usertoken")
    if not getloginstatus(mid,usertoken):
        errlist={'tokenerr':'true'}
        return HttpResponse(simplejson.dumps(errlist, ensure_ascii=False))
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
    
    resultlist={"error_code":0,"reason":"","result":listall,"pagecount":page_listcount,'listcount':listcount,"queryString":{"mid":mid}}
    return HttpResponse(simplejson.dumps(resultlist, ensure_ascii=False))
#---热门标签
def hot_tagslist(request):
    mid=request.GET.get("mid")
    usertoken=request.GET.get("usertoken")
    page=request.GET.get("page")
    if (page=='' or page==0 or page==None):
        page=1
    funpage=zz91page()
    limitNum=funpage.limitNum(20)
    nowpage=funpage.nowpage(int(page))
    frompageCount=funpage.frompageCount()
    after_range_num = funpage.after_range_num(5)
    before_range_num = funpage.before_range_num(4)
    newslist=zzn.get_tagslist(frompageCount=frompageCount,limitNum=limitNum,allnum='',mid=mid)
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
    
    resultlist={"error_code":0,"reason":"","result":listall,"pagecount":page_listcount,'listcount':listcount,"queryString":''}
    return HttpResponse(simplejson.dumps(resultlist, ensure_ascii=False))
#----图片上传
def upload(request):
    mid=request.POST.get("mid")
    usertoken=request.POST.get("usertoken")
    if not getloginstatus(mid,usertoken):
        errlist={'tokenerr':'true'}
        return HttpResponse(simplejson.dumps(errlist, ensure_ascii=False))
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
        newpath=pyuploadpath+"dachong/"+timepath
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
    
#app版本更新
def appversion(request):
    systemType=request.GET.get("systemType")
    appVersion=request.GET.get("appVersion")
    if not systemType:
        systemType="androd"
    if systemType.lower()=="ios":
        if appVersion:
            #判断ios当前版本号是否存在，如果不存在就去读取 id=2 的数据
            sql="select app_versionupdate.update,closed,version,versionDes,closeTip,updateTip,source from app_versionupdate where version=%s"
            alist = dbc.fetchonedb(sql,[appVersion])
            if alist:
                #如果存在且，更新状态为   1 那么是给IOS审核用的版本，直接返回审核版本
                #如果审核通过，将其状态更新为0
                if alist[1]==0:
                    sql="select app_versionupdate.update,closed,version,versionDes,closeTip,updateTip,source from app_versionupdate where id=2"
                    alist = dbc.fetchonedb(sql)
            else:
                sql="select app_versionupdate.update,closed,version,versionDes,closeTip,updateTip,source from app_versionupdate where id=2"
                alist = dbc.fetchonedb(sql)
        else:
            sql="select app_versionupdate.update,closed,version,versionDes,closeTip,updateTip,source from app_versionupdate where id=2"
            alist = dbc.fetchonedb(sql)
    else:
        sql="select app_versionupdate.update,closed,version,versionDes,closeTip,updateTip,source from app_versionupdate where id=1"
        alist = dbc.fetchonedb(sql)
    if alist:
        list={'update':alist[0],'closed':alist[1],'version':alist[2],'versionDes':alist[3],'closeTip':alist[4],'updateTip':alist[5],'source':alist[6]}
    else:
        list=None
    return HttpResponse(simplejson.dumps(list, ensure_ascii=False))

#发现首页
def find(request):
    sql="select count(0) from dede_tagindex"
    result=dbn.fetchonedb(sql)
    list={'tagscount':result[0]}
    return HttpResponse(simplejson.dumps(list, ensure_ascii=False))

def urlencode(request):
    city=request.GET.get("city")
    cityen=quote(city.encode('gb2312'))
    r=requests.get("http://php.weather.sina.com.cn/xml.php?city="+cityen+"&password=DJOYnieT8234jlsK&day=0")
    r.encoding="utf-8"
    xml=r.text
    re_city=r'<city>(.*?)</city>'
    re_status1=r'<status1>(.*?)</status1>'
    re_status2=r'<status2>(.*?)</status2>'
    re_figure1=r'<figure1>(.*?)</figure1>'
    re_figure2=r'<figure2>(.*?)</figure2>'
    re_tgd1=r'<tgd1>(.*?)</tgd1>'
    re_tgd2=r'<tgd2>(.*?)</tgd2>'
    city=get_content(re_city,xml)
    status1=get_content(re_status1,xml)
    status2=get_content(re_status2,xml)
    figure1=get_content(re_figure1,xml)
    figure2=get_content(re_figure2,xml)
    tgd1=get_content(re_tgd1,xml)
    tgd2=get_content(re_tgd2,xml)
    nowdint=int(time.strftime('%H',time.localtime(time.time())))
    
    list={'city':city,'status1':status1,'status2':status2,'figure1':figure1,'figure2':figure2,'tgd1':tgd1,'tgd2':tgd2,'nowdint':nowdint}
    return HttpResponse(simplejson.dumps(list, ensure_ascii=False))

    