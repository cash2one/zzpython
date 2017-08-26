#-*- coding:utf-8 -*-
from django.shortcuts import render_to_response
from django.http import HttpResponse,HttpResponseRedirect
import hashlib,datetime,md5,sys,os,json,urllib,shutil,re,random,time,requests
import simplejson
from django.core.cache import cache
from math import ceil
from zz91db_ast import companydb
from zz91tools import date_to_int
from settings import spconfig,appurl
import Image,ImageDraw,ImageFont,ImageFilter
try:
    import cStringIO as StringIO
except ImportError:
    import StringIO
    
from trade import otherimgupload

dbc=companydb()
reload(sys)
sys.setdefaultencoding('UTF-8')
nowpath=os.path.dirname(__file__)
execfile(nowpath+"/func/public_function.py")
execfile(nowpath+"/func/company_function.py")
execfile(nowpath+"/func/qianbao_function.py")
zzc=zzcompany()
zzq=zzqianbao()
def blank(request):
    return HttpResponse('<input type="hidden" id="appnavname" value="广告" />')
def reg(request):
    clientid=request.GET.get("clientid")
    return render_to_response('main/reg.html',locals())
def regsave(request):
    backurl = request.POST.get('backurl')
    userName = request.POST.get('userName')
    passwd = request.POST.get('passwd')
    qq = request.POST.get('qq')
    email = request.POST.get('email')
    if not email:
        email=""
    contact = request.POST.get('contact')
    sex = request.POST.get('sex')
    companyname = request.POST.get('companyname')
    if not companyname:
        companyname="("+contact+")"
    clientid = request.POST.get('clientid')
    qqopenid = request.POST.get('qqopenid')
    datatype = request.POST.get('datatype')
    industry_code=request.POST.get('industry_code')
    business = request.POST.get('business')
    #messagedata={'err':'false','errkey':'','type':'regsuc'}
    #return HttpResponse(simplejson.dumps(messagedata, ensure_ascii=False))
    isemail=1
    mobile=userName
    regtime=gmt_created=datetime.datetime.now()
    gmt_modified=datetime.datetime.now()
    errflag=0
    errtext=userName
    errname="userName"
    if (not userName and errflag==0):
        errtext="必须填写 手机号码 "
        errflag=1
        errname="userName"
    else:
        if (userName.isdigit()==False):
            errtext="必须填写 手机号码 "
            errname="userName"
            errflag=1
    if (not passwd and errflag==0):
        errtext="必须填写 密码"
        errflag=2
        errname="passwd"
    """
    if (not email and errflag==0):
        errtext="请输入您的邮箱 "
        errflag=6
        errname="email"
    else:
        if (validateEmail(email)==0 and errflag==0):
            errtext="您输入邮箱格式有错误! "
            errflag=6
            errname="email"
        else:
            isemail=1
    
    if not qq and errflag==0:
        errtext="请输入您的QQ号码"
        errflag=3
        errname="qq"
    if qq and errflag==0:
        if (qq.isdigit()==False):
            errtext="请输入QQ号码必须是数字！ "
            errflag=3
            errname="qq"
    """
    if (contact=='' and errflag==0):
        errtext="必须填写 联系人 "
        errflag=4
        errname="contact"
    """
    if (companyname=='' and errflag==0):
        errtext="必须填写 公司名称 ! "
        errflag=5
        errname="companyname"
    """
    if (errflag==0):
        #''判断邮箱帐号是否存在
        sql="select id  from auth_user where (username=%s or mobile=%s)"
        accountlist=dbc.fetchonedb(sql,[userName,userName])
        if (accountlist):
            errflag=1
            errname="userName"
            errtext="您填写的手机号码已经注册！点此<a href='/weixin/forgetpasswd.html'>忘记密码?</a>"
        
        sql="select id  from company_account where mobile=%s"
        accountlist=dbc.fetchonedb(sql,[userName])
        if (accountlist):
            errflag=1
            errname="userName"
            errtext="您填写的手机号码已经注册！点此<a href='/weixin/forgetpasswd.html'>忘记密码?</a>"
        #messagedata={'err':'true','errkey':errtext,'type':'regerr'}
        #return HttpResponse(simplejson.dumps(messagedata, ensure_ascii=False))
        if email:
            sql="select id  from auth_user where email=%s"
            accountlist=dbc.fetchonedb(sql,[email])
            if (accountlist):
                errflag=6
                errname="email"
                #errtext="<br><font size=3>"+userName+"</font><br>该手机号码已经注册！<br><br><a href='/weixin/forgetpasswd.html' class=\"mui-btn mui-btn-danger\">忘记密码?</a> <a href='#' class=\"mui-btn mui-btn-green\" onclick=closeoverlay()>重新修改</a>"
                errtext="您填写的邮箱已经注册！点此<a href='/weixin/sendemail.html'>获得密码?</a>或请修改后重新提交！"
            if (email!="" and isemail==0):
                sql="select id from company_account where email=%s"
                accountlist=dbc.fetchonedb(sql,[email])
                if (accountlist):
                    errflag=6
                    errname="email"
                    errtext="2您填写的邮箱已经注册！点此<a href='/weixin/sendemail.html'>获得密码?</a>或请修改后重新提交！"
        
    if (errflag==0):
        #帐号添加
        md5pwd = hashlib.md5(passwd)
        md5pwd = md5pwd.hexdigest()[8:-8]
        value1=[userName,md5pwd,email,gmt_created,gmt_modified]
        sql1="insert into auth_user (username,password,email,gmt_created,gmt_modified) values(%s,%s,%s,%s,%s)"
        
        #添加公司信息
        if not industry_code:
            industry_code=''
        if not business:
            business=''
        service_code=''
        area_code=''
        foreign_city=''
        category_garden_id='0'
        membership_code='10051000'
        classified_code='10101002'
        regfrom_code='10031038'
        domain=''
        address=''
        address_zip=''
        website=''
        introduction=''
        value2=[companyname, industry_code, business, service_code, area_code, foreign_city, category_garden_id, membership_code,domain, classified_code, regfrom_code,  regtime, gmt_created, gmt_modified,  address, address_zip, website, introduction]
        sql2="insert into company (name, industry_code, business, service_code, area_code, foreign_city, category_garden_id, membership_code,    domain, classified_code, regfrom_code,  regtime, gmt_created, gmt_modified,  address, address_zip, website, introduction)"
        sql2=sql2+" values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)";
        dbc.updatetodb(sql2,value2)
        
        company_id=getcompany_id(companyname,gmt_created)
        is_admin='1'
        tel_country_code=''
        tel_area_code=''
        tel=mobile
        fax_country_code=''
        fax_area_code=''
        fax=''
        if not sex:
            sex=''
        if not qq:
            qq=''
        real_name=contact
        nickname=contact
        
        #messagedata={'err':'true','errkey':company_id,'type':'regerr'}
        #return HttpResponse(simplejson.dumps(messagedata, ensure_ascii=False))
        #'添加联系方式
        dbc.updatetodb(sql1,value1)
        
        value3=[userName, company_id, contact, is_admin, tel_country_code, tel_area_code, tel, mobile, fax_country_code, fax_area_code, fax, email, sex, passwd, gmt_modified, gmt_created]
        sql3="insert into company_account (account, company_id, contact, is_admin, tel_country_code, tel_area_code, tel, mobile, fax_country_code, fax_area_code, fax, email, sex, password, gmt_modified, gmt_created)"
        sql3=sql3+" values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)";
        dbc.updatetodb(sql3,value3);
        
        #messagedata={'err':'false','errkey':'','type':'regsuc','company_id':company_id}
        #return HttpResponse(simplejson.dumps(messagedata, ensure_ascii=False))
        #-互助用户表
        sqlh="select id from bbs_user_profiler where company_id=%s"
        userlist=dbc.fetchonedbmain(sqlh,[company_id])
        if (userlist==None):
            value=[company_id,userName,nickname,email,tel,mobile,qq,real_name,gmt_modified,gmt_created]
            sqlu="insert into bbs_user_profiler(company_id,account,nickname,email,tel,mobile,qq,real_name,gmt_modified,gmt_created) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            dbc.updatetodb(sqlu,value);
        #抽奖机会
        
        
        #绑定
        sqlc="select id from oauth_access where open_id=%s and target_account=%s and open_type='app.zz91.com'"
        list=dbc.fetchonedb(sqlc,[str(clientid),userName])
        if not list:
            sql="insert into oauth_access(open_id,open_type,target_account,gmt_created,gmt_modified) values(%s,%s,%s,%s,%s)"
            dbc.updatetodb(sql,[clientid,'app.zz91.com',userName,gmt_created,gmt_modified])
            
        #绑定QQ登录
        if qqopenid:
            sqlc="select id from oauth_access where open_id=%s and open_type='qq.com'"
            list=dbc.fetchonedb(sqlc,[str(qqopenid)])
            if not list:
                sql="insert into oauth_access(open_id,open_type,company_id,target_account,gmt_created,gmt_modified) values(%s,%s,%s,%s,%s,%s)"
                dbc.updatetodb(sql,[qqopenid,'qq.com',company_id,userName,gmt_created,gmt_modified])
        #首次安装APP送20 再生钱包#
        zzq.firstsendfee(company_id,clientid)
        #首次下载APP并登录
        choujiang(account=userName,appid=clientid)
        #自动登录
        token = hashlib.md5(str(passwd)+str(userName)+str(gmt_modified))
        token = token.hexdigest()[8:-8]
        #保存app登陆token
        sql="select id from app_token where token=%s"
        listd=dbc.fetchonedb(sql,[token])
        if not listd:
            oauth_id=0
            sqlp="select max(id) from oauth_access where open_id=%s and target_account=%s and open_type='app.zz91.com' and closeflag=0"
            lista=dbc.fetchonedb(sqlp,[clientid,userName])
            if lista:
                oauth_id=lista[0]
            sqlb="select id from app_token where company_id=%s"
            listb=dbc.fetchonedb(sqlb,[company_id])
            if not listb:
                sqlm="insert into app_token(oauth_id,company_id,token,gmt_created,gmt_modified) values(%s,%s,%s,%s,%s)"
                dbc.updatetodb(sqlm,[oauth_id,company_id,token,gmt_created,gmt_created])
            else:
                sqlm="update app_token set oauth_id=%s,token=%s,gmt_created=%s where company_id=%s"
                dbc.updatetodb(sqlm,[oauth_id,token,gmt_created,company_id])
        updatelogin(request,company_id)
        result=zzc.getcompanylogininfo(company_id=company_id)
        
        if datatype=="json":
            messagedata={'err':'false','errkey':'1','result':result,'token':token,'passwd':str(hashlib.md5(passwd).hexdigest()),'username':userName}
            return HttpResponse(simplejson.dumps(messagedata, ensure_ascii=False))  
        messagedata={'err':'false','errkey':'','type':'regsuc','company_id':company_id}
        return HttpResponse(simplejson.dumps(messagedata, ensure_ascii=False))
    if (errflag>=1):
        messagedata={'err':'true','errkey':errtext,'type':'regerr','errflag':errflag,'errname':errname}
        return HttpResponse(simplejson.dumps(messagedata, ensure_ascii=False))
 
# 会员登录    
def login(request):
    tourl=request.GET.get("tourl")
    if not tourl:
        tourl=""
    wintarget=request.GET.get("wintarget")
    tourlstr="请登录后进行操作！"
    if "myrc_index" in tourl:
        tourlstr="您需要登录后进入生意管家！"
    if "products_publish" in tourl:
        tourlstr="您需要登录后才能发布信息！"
    if "huzhupost" in tourl:
        tourlstr="您需要登录后才能发布/回复帖子！"
    if "huzhuview" in tourl:
        tourlstr="您需要登录后才能发布/回复帖子！"
    if "detail" in tourl:
        tourlstr="您需要登录后才能查看联系方式！"
    if "favorite" in tourl:
        tourlstr="您需要登录后收藏信息！"
    jsstr=request.GET.get("jsstr")
    if not wintarget:
        wintarget="blank"
    return render_to_response('main/login.html',locals())
def login1(request):
    tourl=request.GET.get("tourl")
    if not tourl:
        tourl=""
    wintarget=request.GET.get("tourl")
    if not wintarget:
        wintarget="blank"
    return render_to_response('main/login1.html',locals())
def loginout(request):
    request.session.delete()
    response=HttpResponseRedirect("/")
    return response

def loginok(request):
    company_id=request.session.get("company_id",None)
    if company_id:
        sql2='select id from app_company where company_id=%s'
        result=dbc.fetchonedb(sql2,company_id)
        if not result:
            gmt_date=datetime.date.today()
            gmt_created=datetime.datetime.now()
            sql='insert into app_company(company_id,gmt_date,gmt_created) values(%s,%s,%s)'
            dbc.updatetodb(sql,[company_id,gmt_date,gmt_created])
    response=HttpResponseRedirect("/")
    return response
def logininfo(request):
    appid=request.GET.get("appid")
    company_id=0
    if appid:
        sqlc="select id,target_account from oauth_access where open_id=%s and open_type=%s and closeflag=0"
        list=dbc.fetchonedb(sqlc,[str(appid),"app.zz91.com"])
        if list:
            account=list[1]
            sql="select company_id from company_account where account=%s"
            listc=dbc.fetchonedb(sql,[account])
            if listc:
                company_id=listc[0]
    return HttpResponse(str(company_id))
def logininfo1(request):
    appid=request.GET.get("appid")
    appsystem = request.GET.get('appsystem')
    userimei = request.GET.get('userimei')
    company_id=0
    contact=""
    gmt_modified=datetime.datetime.now()
    if appid and appid!="null":
        sqlp="select id from oauth_access where open_id=%s and open_type=%s"
        list=dbc.fetchonedb(sqlp,[str(appid),"app.zz91.com"])
        if not list:
            sql="insert into oauth_access(open_id,open_type,gmt_created,gmt_modified,appsystem,userimei) values(%s,%s,%s,%s,%s,%s)"
            dbc.updatetodb(sql,[appid,'app.zz91.com',gmt_modified,gmt_modified,appsystem,userimei])
            #首次安装APP送20 再生钱包#
            zzq.firstsendfee(company_id,appid)
        sqlc="select id,target_account from oauth_access where open_id=%s and open_type=%s  and closeflag=0"
        list=dbc.fetchonedb(sqlc,[str(appid),"app.zz91.com"])
        if list:
            account=list[1]
            if account:
                sql="select company_id,account,contact,sex from company_account where account=%s"
                listc=dbc.fetchonedb(sql,[account])
                if listc:
                    company_id=listc[0]
                    #sqlc="update oauth_access set company_id=%s where target_account=%s"
                    #dbc.updatetodb(sqlc,[company_id,account])
                    contact=listc[2]
                    sex=listc[3]
                    if str(sex)=="0":
                        if ("先生" not in contact) and ("女士" not in contact):
                            contact+="先生"
                    else:
                        if ("先生" not in contact) and ("女士" not in contact):
                            contact+="女士"
                    #更新登录记录
                    updatelogin(request,company_id)
                    
    messagedata={'company_id':company_id,'contact':contact}
    return HttpResponse(simplejson.dumps(messagedata, ensure_ascii=False))        

def getnowurl(request):
    host=request.path_info
    qstring=request.META.get('QUERY_STRING','/')
    qstring=qstring.replace("&","^and^")
    return host+"?"+qstring
#----登录保存
def loginsave(request):
    userName = request.POST.get('username')
    passwd = request.POST.get('passwd')
    appid = request.POST.get('appid')
    loginflag = request.POST.get('loginflag')
    appsystem = request.POST.get('appsystem')
    qqopenid = request.POST.get('qqopenid')
    open_type = request.POST.get('open_type')
    passwdjm = request.POST.get('passwdjm')
    if not userName:
        userName = request.GET.get('username')
        passwd = request.GET.get('passwd')
        appid = request.GET.get('appid')
        loginflag = request.GET.get('loginflag')
        appsystem = request.GET.get('appsystem')
        open_type = request.GET.get('open_type')
    md5pwd=""
    if passwd:
        md5pwd = hashlib.md5(passwd)
        md5pwd = md5pwd.hexdigest()[8:-8]
    else:
        md5pwd=passwdjm[8:-8]
    gmt_created=datetime.datetime.now()
    gmt_modified=datetime.datetime.now()
    token = hashlib.md5(str(passwd)+str(userName)+str(gmt_modified))
    token = token.hexdigest()[8:-8]
    firstinstall=0
    company_id=0
    
    sql="select id,username from auth_user where (username=%s or email=%s or mobile=%s or account=%s) and password=%s"
    plist=dbc.fetchonedb(sql,[userName,userName,userName,userName,md5pwd]);
    error="suc"
    
    if plist:
        account=plist[1]
        sqlc="select company_id from company_account where account=%s"
        list=dbc.fetchonedb(sqlc,[account]);
        if list:
            company_id=list[0]
            #判断是否拉黑
            sqlh="select id from company where id=%s and is_block=1"
            listh=dbc.fetchonedb(sqlh,[company_id]);
            if listh:
                error="该用户已经被禁止登录！"
                messagedata={'err':'true','errkey':error,'result':company_id,'token':''}
                return HttpResponse(simplejson.dumps(messagedata, ensure_ascii=False))
            if str(company_id)=="0":
                error="用户名或邮箱 还未在ZZ91注册！"
            else:
                sqlc="select id from oauth_access where target_account=%s and open_type='app.zz91.com'"
                list=dbc.fetchonedb(sqlc,[account])
                if list:
                    sql="update oauth_access set closeflag=1 where target_account=%s and open_type='app.zz91.com'"
                    dbc.updatetodb(sql,[str(account)])
                    sql="update oauth_access set closeflag=1 where open_id=%s and open_type='app.zz91.com'"
                    dbc.updatetodb(sql,[str(appid)])
                    sql="update oauth_access set closeflag=0,company_id=%s,open_id=%s where id=%s"
                    dbc.updatetodb(sql,[company_id,str(appid),list[0]])
                    error="suc"
                    #return HttpResponse(simplejson.dumps(appid, ensure_ascii=False))
                else:
                    sql="insert into oauth_access(open_id,open_type,target_account,gmt_created,gmt_modified,appsystem) values(%s,%s,%s,%s,%s,%s)"
                    dbc.updatetodb(sql,[appid,'app.zz91.com',account,gmt_created,gmt_modified,appsystem])
                    error="suc"
                    firstinstall=1
                    #首次安装APP送20 再生钱包#
                    zzq.firstsendfee(company_id,appid)
                    #首次下载APP并登录
                    choujiang(company_id=company_id,appid=appid)
        else:
            error="用户名或邮箱 还未在ZZ91注册！"
        
    else:
        sqlc="select account,company_id from company_account where mobile=%s order by id desc"
        list=dbc.fetchonedb(sqlc,[userName]);
        if list:
            account=list[0]
            company_id=list[1]
            #判断是否拉黑
            sqlh="select id from company where id=%s and is_block=1"
            listh=dbc.fetchonedb(sqlh,[company_id]);
            if listh:
                error="该用户已经被禁止登录！"
                messagedata={'err':'true','errkey':error,'result':company_id,'token':''}
                return HttpResponse(simplejson.dumps(messagedata, ensure_ascii=False))
            if str(company_id)!="0":
                sqlp="select id from auth_user where username=%s and password=%s"
                listp=dbc.fetchonedb(sqlp,[account,md5pwd]);
                if listp:
                    sqlc="select id from oauth_access where target_account=%s and open_type='app.zz91.com'"
                    list=dbc.fetchonedb(sqlc,[account])
                    if list:
                        sql="update oauth_access set closeflag=1 where target_account=%s and open_type='app.zz91.com'"
                        dbc.updatetodb(sql,[str(account)])
                        sql="update oauth_access set closeflag=1 where open_id=%s and open_type='app.zz91.com'"
                        dbc.updatetodb(sql,[str(appid)])
                        sql="update oauth_access set closeflag=0,company_id=%s,open_id=%s where id=%s"
                        dbc.updatetodb(sql,[company_id,str(appid),list[0]])
                        error="suc"
                    else:
                        sql="insert into oauth_access(open_id,open_type,target_account,gmt_created,gmt_modified,appsystem) values(%s,%s,%s,%s,%s,%s)"
                        dbc.updatetodb(sql,[appid,'app.zz91.com',account,gmt_created,gmt_modified,appsystem])
                        error="suc"
                        firstinstall=1
                        #首次安装APP送20 再生钱包#
                        zzq.firstsendfee(company_id,appid)
                        #首次下载APP并登录
                        choujiang(company_id=company_id,appid=appid)
                else:
                    error="用户名或密码错误！"
            else:
                error="用户名或密码错误！"
        else:
            error="密码错误或你填写的手机/用户名还未注册"
    if loginflag:
        if error=="suc":
            if firstinstall==1:
                content="您好，感谢您安装ZZ91客户端，客户端包含但不限以下功能：<br />"
                content+="一、    交易中心，您可以找到再生行业内供求信息；<br />"
                content+="二、    行情报价，您可以找到再生行业内报价信息；<br />"
                content+="三、    资讯中心，您可以看到再生行业内最新资讯；<br />"
                content+="四、    废料问答，您可以与业内人士共同讨论、交流；<br />"
                content+="…<br />"
                content+="如有问题，请您点击侧导航“意见反馈”，再生网团队将为您提供详尽的咨询服务。<br />"
                qvalue=['感谢您的安装','',gmt_created,content,company_id,0]
                sql="select id from app_message where company_id=%s"
                listd=dbc.fetchonedb(sql,[company_id])
                if not listd:
                    sqlm='insert into app_message(title,url,gmt_created,content,company_id,mtype) values(%s,%s,%s,%s,%s,%s)'
                    dbc.updatetodb(sqlm,qvalue)
            #保存app登陆token
            sql="select id from app_token where token=%s"
            listd=dbc.fetchonedb(sql,[token])
            if not listd:
                oauth_id=0
                sqlp="select max(id) from oauth_access where open_id=%s and target_account=%s and open_type='app.zz91.com' and closeflag=0"
                lista=dbc.fetchonedb(sqlp,[appid,account])
                if lista:
                    oauth_id=lista[0]
                sqlb="select id from app_token where company_id=%s"
                listb=dbc.fetchonedb(sqlb,[company_id])
                if not listb:
                    sqlm="insert into app_token(oauth_id,company_id,token,gmt_created,gmt_modified) values(%s,%s,%s,%s,%s)"
                    dbc.updatetodb(sqlm,[oauth_id,company_id,token,gmt_created,gmt_created])
                else:
                    sqlm="update app_token set oauth_id=%s,token=%s,gmt_created=%s where company_id=%s"
                    dbc.updatetodb(sqlm,[oauth_id,token,gmt_created,company_id])
            updatelogin(request,company_id)
            result=zzc.getcompanylogininfo(company_id=company_id)
            datatype=request.GET.get("datatype")
            if datatype=="json":
                messagedata={'err':'false','errkey':'1','result':result,'token':token}
            else:
                messagedata={'err':'false','errkey':'2','result':company_id,'token':token}
            #绑定QQ登录,微信登陆
            if qqopenid:
                if not open_type:
                    open_type="qq.com"
                sqlc="select id from oauth_access where open_id=%s and open_type=%s"
                list=dbc.fetchonedb(sqlc,[str(qqopenid),open_type])
                if not list:
                    sql="insert into oauth_access(open_id,open_type,company_id,target_account,gmt_created,gmt_modified) values(%s,%s,%s,%s,%s,%s)"
                    dbc.updatetodb(sql,[qqopenid,open_type,company_id,account,gmt_created,gmt_modified])
                else:
                    sql="update oauth_access set target_account set target_account=%s,company_id=%s where open_id=%s and open_type=%s"
                    dbc.updatetodb(sql,[account,company_id,qqopenid,open_type])
            return HttpResponse(simplejson.dumps(messagedata, ensure_ascii=False))
        else:
            messagedata={'err':'true','errkey':error,'result':company_id,'token':token}
            return HttpResponse(simplejson.dumps(messagedata, ensure_ascii=False))
    else:
        messagedata={'err':'true','errkey':error,'result':company_id,'token':token}
        return HttpResponse(simplejson.dumps(messagedata, ensure_ascii=False))
def tokeninfo(request):
    token=request.POST.get("usertoken")
    company_id=request.POST.get("company_id")
    sql="insert into err_log(content) values(%s)"
    #dbc.updatetodb(sql,[str(company_id)+request.META.get("HTTP_X_FORWARDED_FOR")+request.META.get("HTTP_USER_AGENT")])
    
    messagedata={'err':'true','errkey':'未获得TOKEN','result':''}
    if company_id:
        #过期时间为2小时  MINUTE,HOUR
        sql="select token from app_token where company_id=%s and token=%s and TIMESTAMPDIFF(HOUR,gmt_created,NOW())<=4"
        listd=dbc.fetchonedb(sql,[company_id,token])
        if not listd:
            messagedata={'err':'true','errkey':'未获得TOKEN','result':token+"-"+company_id}
        else:
            messagedata={'err':'false','errkey':'','result':token}
    return HttpResponse(simplejson.dumps(messagedata, ensure_ascii=False))
#获取新token
def get_token(request):
    token=request.POST.get("usertoken")
    company_id=request.POST.get("company_id")
    pwd_hash=request.POST.get("pwd_hash")
    username=request.POST.get("username")
    appid=request.POST.get("clientid")
    
    md5pwd=pwd_hash[8:-8]
    gmt_created=datetime.datetime.now()
    gmt_modified=datetime.datetime.now()
    token = hashlib.md5(str(md5pwd)+str(username)+str(gmt_modified))
    token = token.hexdigest()[8:-8]
    sucflag=0
    messagedata={'err':'true','errkey':'','result':''}
    sql="select id,username from auth_user where (username=%s or mobile=%s) and password=%s"
    plist=dbc.fetchonedb(sql,[username,username,md5pwd]);
    if plist:
        account=plist[1]
        sucflag=1
    else:
        sqlc="select account,company_id from company_account where mobile=%s order by id desc"
        list=dbc.fetchonedb(sqlc,[username]);
        if list:
            account=list[0]
            company_id=list[1]
            #判断是否拉黑
            sqlh="select id from company where id=%s and is_block=1"
            listh=dbc.fetchonedb(sqlh,[company_id]);
            if listh:
                error="该用户已经被禁止登录！"
                messagedata={'err':'true','errkey':error,'result':company_id,'token':''}
                return HttpResponse(simplejson.dumps(messagedata, ensure_ascii=False))
            if str(company_id)!="0":
                sqlp="select id from auth_user where username=%s and password=%s"
                listp=dbc.fetchonedb(sqlp,[account,md5pwd]);
                if listp:
                    sucflag=1
    if sucflag==1:
        oauth_id=0
        sqlp="select max(id) from oauth_access where open_id=%s and target_account=%s and open_type='app.zz91.com' and closeflag=0"
        lista=dbc.fetchonedb(sqlp,[appid,account])
        if lista:
            oauth_id=lista[0]
        if company_id:
            sqlb="select id from app_token where company_id=%s"
            listb=dbc.fetchonedb(sqlb,[company_id])
            if not listb:
                sqlm="insert into app_token(oauth_id,company_id,token,gmt_created,gmt_modified) values(%s,%s,%s,%s,%s)"
                dbc.updatetodb(sqlm,[oauth_id,company_id,token,gmt_created,gmt_created])
            else:
                sqlm="update app_token set oauth_id=%s,token=%s,gmt_created=%s where company_id=%s"
                dbc.updatetodb(sqlm,[oauth_id,token,gmt_created,company_id])
            messagedata={'err':'false','errkey':'','result':token}
    return HttpResponse(simplejson.dumps(messagedata, ensure_ascii=False))
    
def infosave(request):
    company_id=request.POST.get("company_id")
    companyname=request.POST.get("companyname")
    contact=request.POST.get("contact")
    mobile=request.POST.get("mobile")
    qq=request.POST.get("qq")
    business=request.POST.get("business")
    usertoken=request.POST.get("usertoken")
    if not getloginstatus(company_id,usertoken):
        errlist={'tokenerr':'true'}
        return HttpResponse(simplejson.dumps(errlist, ensure_ascii=False))
    if not company_id or str(company_id)=="0":
        return HttpResponse("err")
    if company_id:
        if mobile:
            sql="select id from company_account where mobile=%s and company_id>%s and company_id<%s"
            listd=dbc.fetchonedb(sql,[mobile,company_id,company_id])
            if listd:
                messagedata={'err':'true','errkey':"改手机已经注册，请改用其他手机注册！",'type':'infosave','result':''}
                return HttpResponse(simplejson.dumps(messagedata, ensure_ascii=False))
        sql="update company_account set contact=%s,mobile=%s,qq=%s where company_id=%s"
        dbc.updatetodb(sql,[contact,mobile,qq,company_id])
        sql="update company set business=%s where id=%s"
        dbc.updatetodb(sql,[business,company_id])
        cache.set("app_acompanydetail"+str(company_id),None,0)
        messagedata={'err':'false','errkey':'保存成功！','type':'infosave','result':''}
        return HttpResponse(simplejson.dumps(messagedata, ensure_ascii=False))
    else:
        messagedata={'err':'true','errkey':"系统错误",'type':'infosave','result':''}
        return HttpResponse(simplejson.dumps(messagedata, ensure_ascii=False))
def changeaccount(request):
    company_id=request.GET.get("company_id")
    usertoken=request.GET.get("usertoken")
    if not getloginstatus(company_id,usertoken):
        errlist={'tokenerr':'true'}
        return HttpResponse(simplejson.dumps(errlist, ensure_ascii=False))
    account=getaccount(company_id)
    clientid=request.GET.get("clientid")
    sql="update oauth_access set closeflag=1 where target_account=%s and open_id=%s and open_type='app.zz91.com'"
    dbc.updatetodb(sql,[account,clientid])
    messagedata={'changeflag':"true"}
    return HttpResponse(simplejson.dumps(messagedata, ensure_ascii=False))
def loginof(request):
    nowlanmu="<a href='/huzhu/'>再生互助</a>"
    done = request.POST['done']
    username = request.POST['username']
    pwd = request.POST['pwd']
    md5pwd = hashlib.md5(pwd)
    md5pwd = md5pwd.hexdigest()[8:-8]
    sql="select id,username from auth_user where (username=%s or email=%s or mobile=%s) and password=%s"
    plist=dbc.fetchonedb(sql,[username,username,username,md5pwd])
    if plist:
        request.session.set_expiry(6000*6000)
        username=plist[1]
        
        account=plist[1]
        sqlc="select company_id from company_account where account=%s"
        list=dbc.fetchonedb(sqlc,[account])
        if list:
            company_id=list[0]
            request.session['username']=username
            request.session['company_id']=company_id
        else:
            error="用户名或邮箱 还未注册！"
            return render_to_response('login.html',locals())
        if (done=="" or done=="None"):
            response=HttpResponseRedirect("/loginok/")
            return response
        else:
            response=HttpResponseRedirect(done)
            return response
    else:
        sqlc="select account,company_id from company_account where mobile=%s order by id desc"
        list=dbc.fetchonedb(sqlc,[username])
        if list:
            account=list[0]
            company_id=list[1]
            sqlp="select id from auth_user where username=%s and password=%s"
            listp=dbc.fetchonedb(sqlp,[account,md5pwd])
            if listp:
                request.session.set_expiry(6000*6000)
                request.session['username']=account
                request.session['company_id']=company_id
                updatelogin(request,company_id)
                response=HttpResponseRedirect("/loginok/")
                return response
            else:
                error="用户名或密码错误！"
                return render_to_response('main/login.html',locals())
        else:
            error="你填写的手机还未注册"
            return render_to_response('main/login.html',locals())
    return render_to_response('main/login.html',locals())
#-----忘记密码
def forgetpasswdpage(request):
    step= request.GET.get("step")
    clientid=request.GET.get("clientid")
    mobile=request.GET.get("mobile")
    account=request.GET.get("account")
    usertoken=request.GET.get("usertoken")
    if not getloginstatus(company_id,usertoken):
        errlist={'tokenerr':'true'}
        return HttpResponse(simplejson.dumps(errlist, ensure_ascii=False))
    if (step=="1"):
        step1=1
    if (step=="2"):
        step2=1
    if (step=="3"):
        step3=1
    if (step=="4"):
        company_id=0
        sqlc="select company_id from company_account where account=%s"
        list=dbc.fetchonedb(sqlc,[account]);
        if list:
            company_id=list[0]
        step4=1
    return render_to_response('main/forgetpasswd.html',locals())
def forgetpasswd(request):
    step= request.POST.get("step")
    clientid=request.POST.get("clientid")
    appsystem=request.POST.get("appsystem")
    username = request.POST.get('username')
    if not step:
        step= request.GET.get("step")
        clientid=request.GET.get("clientid")
        appsystem=request.GET.get("appsystem")
        username = request.GET.get('username')
    usertoken=request.POST.get("usertoken")
    if not usertoken:
        usertoken=request.GET.get("usertoken")
    if not getloginstatus(company_id,usertoken):
        errlist={'tokenerr':'true'}
        return HttpResponse(simplejson.dumps(errlist, ensure_ascii=False))
    gmt_modified=datetime.datetime.now()
    error=None
    if (step==None or step==""):
        step0=1
    if (step=="1"):
        step1=1
        if (username==""):
            step1=None
            step0=1
            error="请输入手机 或 用户名 或 邮箱"
        else:
            sql="select id,username from auth_user where (username=%s or email=%s or mobile=%s)"
            plist=dbc.fetchonedb(sql,[username,username,username]);
            if plist:
                account=plist[1]
                
                sqlc="select company_id,mobile from company_account where account=%s"
                list=dbc.fetchonedb(sqlc,[account]);
                if list:
                    company_id=list[0]
                    mobile=list[1]
                    
                    smsreresult=postsms(mobile,account,company_id)
                    
                    if (smsreresult!=True):
                        step1=None
                        step0=1
                        error=smsreresult    
                else:
                    step1=None
                    step0=1
                    error="未知的错误！"
                
            else:
                sqlc="select company_id,mobile,account from company_account where mobile=%s"
                list=dbc.fetchonedb(sqlc,[username]);
                if list:
                    company_id=list[0]
                    mobile=list[1]
                    account=list[2]
                    smsreresult=postsms(mobile,account,company_id)
                    if (smsreresult!=True):
                        step1=None
                        step0=1
                        error=smsreresult    
                else:
                    step1=None
                    step0=1
                    error="手机或用户名或邮箱不存在！"
        if error:
            messagedata={'err':'true','errkey':error,'type':'forgetpasswd'}
            return HttpResponse(simplejson.dumps(messagedata, ensure_ascii=False))
        else:
            list={'mobile':mobile,'account':account,'clientid':clientid}
            messagedata={'err':'false','errkey':'','type':'forgetpasswd','result':list,'step':1}
            return HttpResponse(simplejson.dumps(messagedata, ensure_ascii=False))
    if (step=="2"):
        step2=1
        mobile=request.POST.get("mobile")
        account = request.POST.get('account')
        yzcode = request.POST.get('yzcode')
        clientid = request.POST.get('clientid')
        if not mobile:
            mobile=request.GET.get("mobile")
            account = request.GET.get('account')
            yzcode = request.GET.get('yzcode')
            clientid = request.GET.get('clientid')
        sql="select id from auth_forgot_password where username=%s and auth_key=%s and DATEDIFF(CURDATE(),gmt_created)<1"
        plist=dbc.fetchonedb(sql,[account,yzcode]);
        if (plist==None):
            step1=1
            step2=None
            error="你输入的验证码错误！"
        if error:
            messagedata={'err':'true','errkey':error,'type':'forgetpasswd'}
            return HttpResponse(simplejson.dumps(messagedata, ensure_ascii=False))
        else:
            list={'mobile':mobile,'account':account,'clientid':clientid}
            messagedata={'err':'false','errkey':'','type':'forgetpasswd','result':list,'step':2}
            return HttpResponse(simplejson.dumps(messagedata, ensure_ascii=False))
        
    if (step=="3"):
        mobile=request.POST.get("mobile")
        account = request.POST.get('account')
        clientid = request.POST.get('clientid')
        passwd1=request.POST.get("passwd1")
        passwd2=request.POST.get("passwd2")
        if not mobile:
            mobile=request.GET.get("mobile")
            account = request.GET.get('account')
            clientid = request.GET.get('clientid')
            passwd1=request.GET.get("passwd1")
            passwd2=request.GET.get("passwd2")
        error=""
        if (passwd1==""):
            step2=1
            error="密码不能为空！"
        if (passwd1!=passwd2):
            step2=1
            error="两次输入的密码不一致！"
        if (error==""):
            md5pwd = hashlib.md5(passwd1)
            md5pwd = md5pwd.hexdigest()[8:-8]
            sql="update auth_user set password=%s,gmt_modified=%s where username=%s"
            dbc.updatetodb(sql,[md5pwd,gmt_modified,account]);
            sql="update company_account set password=%s,gmt_modified=%s where account=%s"
            dbc.updatetodb(sql,[passwd1,gmt_modified,account]);
            
            if clientid:
                sqlc="select id from oauth_access where open_id=%s and open_type='app.zz91.com'"
                list=dbc.fetchonedb(sqlc,[str(clientid)])
                if not list:
                    sql="insert into oauth_access(open_id,open_type,target_account,gmt_created,gmt_modified,appsystem) values(%s,%s,%s,%s,%s,%s)"
                    dbc.updatetodb(sql,[clientid,'app.zz91.com',account,gmt_modified,gmt_modified,appsystem])
                    
                    #首次安装APP送20 再生钱包#
                    zzq.firstsendfee(company_id,clientid)
                    #首次下载APP并登录
                    choujiang(company_id=company_id,appid=clientid)
                else:
                    id=list[0]
                    sql="update oauth_access set closeflag=1 where target_account=%s and open_type='app.zz91.com'"
                    dbc.updatetodb(sql,[account])
                    sql="update oauth_access set appsystem=%s,target_account=%s,closeflag=0 where id=%s"
                    dbc.updatetodb(sql,[appsystem,account,id])
        
        if error:
            messagedata={'err':'true','errkey':error,'type':'forgetpasswd'}
            return HttpResponse(simplejson.dumps(messagedata, ensure_ascii=False))
        else:
            list={'mobile':mobile,'account':account,'clientid':clientid}
            messagedata={'err':'false','errkey':'','type':'forgetpasswd','result':list,'step':4}
            return HttpResponse(simplejson.dumps(messagedata, ensure_ascii=False))    
            
            
    return render_to_response('main/forgetpasswd.html',locals())
def info(request):
    company_id=request.GET.get('company_id')
    usertoken=request.POST.get("usertoken")
    if not getloginstatus(company_id,usertoken):
        errlist={'tokenerr':'true'}
        return HttpResponse(simplejson.dumps(errlist, ensure_ascii=False))
    companyinfo=zzc.getcompanydetail(company_id)
    account=getaccount(company_id)
    return render_to_response('main/info.html',locals())
#解绑手机，验证码
def auth_yzmcode(request):
    usertoken=request.POST.get("usertoken")
    appsystem=request.POST.get("appsystem")
    company_id = request.POST.get('company_id')
    mobilemod = request.POST.get('mobile')
    """
    if not getloginstatus(company_id,usertoken):
        errlist={'tokenerr':'true'}
        return HttpResponse(simplejson.dumps(errlist, ensure_ascii=False))
    """
    forgettype = request.POST.get('forgettype')
    #忘记密码
    if forgettype=="forgetpasswd":
        sqlc="select company_id,mobile,account from company_account where mobile=%s"
        list=dbc.fetchonedb(sqlc,[mobilemod]);
        if list:
            company_id=list[0]
            mobile=list[1]
            account=list[2]
            smsreresult=postsms(mobile,account,company_id)
            if (smsreresult!=True):
                errkey=smsreresult
                err="true"
            else:
                errkey="发送成功1"
                err="false"
            messagedata={'err':err,'errkey':errkey,'company_id':company_id}
            return HttpResponse(simplejson.dumps(messagedata, ensure_ascii=False))
        #auth_usr
        sql="select id,username from auth_user where (username=%s or mobile=%s)"
        plist=dbc.fetchonedb(sql,[mobilemod,mobilemod]);
        if plist:
            account=plist[1]
            
            sqlc="select company_id,mobile from company_account where account=%s"
            list=dbc.fetchonedb(sqlc,[account]);
            if list:
                company_id=list[0]
                mobile=list[1]
                smsreresult=postsms(mobile,account,company_id)
                if (smsreresult!=True):
                    errkey=smsreresult
                    err="true"
                else:
                    errkey="发送成功2"
                    err="false"
            else:
                errkey="手机或用户名或邮箱不存在！"
                err="false"
            messagedata={'err':err,'errkey':errkey,'company_id':company_id}
            return HttpResponse(simplejson.dumps(messagedata, ensure_ascii=False))
        else:
            errkey="手机或用户名或邮箱不存在！"
            err="false"
            messagedata={'err':err,'errkey':errkey,'company_id':company_id}
            return HttpResponse(simplejson.dumps(messagedata, ensure_ascii=False))
    #修改密码
    sqlc="select mobile,account from company_account where company_id=%s"
    list=dbc.fetchonedb(sqlc,[company_id]);
    if list:
        mobile=list[0]
        account=list[1]
        if not mobile or mobile=="":
            mobile=mobilemod
        if mobile:
            smsreresult=postsms(mobile,account,company_id)
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
#解绑手机
def auth_unbundlingmobile(request):
    usertoken=request.POST.get("usertoken")
    appsystem=request.POST.get("appsystem")
    company_id = request.POST.get('company_id')
    yzcode = request.POST.get('yzcode')
    if not getloginstatus(company_id,usertoken):
        errlist={'tokenerr':'true'}
        return HttpResponse(simplejson.dumps(errlist, ensure_ascii=False))
    sql="select id from auth_forgot_password where userid=%s and auth_key=%s and TIMESTAMPDIFF(MINUTE,gmt_created,now())<600"
    plist=dbc.fetchonedb(sql,[company_id,yzcode]);
    if (plist):
        sqlc="select mobile,account from company_account where company_id=%s"
        list=dbc.fetchonedb(sqlc,[company_id]);
        if list:
            mobile=list[0]
            account=list[1]
            """
            #绑定手机时，如果账号和手机号相同，修改和绑定手机，需要把账号禁用，这样下次就不能用原手机登录了（因为账号不能修改）
            if account==mobile:
                sql="select id from auth_user_block where account=%s"
                list1=dbc.fetchonedb(sql1,[account])
                if list1:
                    sql="update auth_user_block set block=1 where account=%s"
                    dbc.updatetodb(sql,[account])
                else:
                    gmt_created=datetime.datetime.now()
                    sql="insert into auth_user_block(account,block,gmt_created) values(%s,%s,%s)"
                    dbc.updatetodb(sql,[account,1,gmt_created])
            """
            sql="update company_account set mobile='' where company_id=%s"
            dbc.updatetodb(sql,[company_id])
            sql="update auth_user set mobile='' where username=%s"
            dbc.updatetodb(sql,[account])
            errkey="解绑成功！"
            err="false"
        else:
            errkey="系统错误，账号不存在！"
            err="true"
    else:
        errkey="你输入的验证码错误！"
        err="true"
    messagedata={'err':err,'errkey':errkey}
    return HttpResponse(simplejson.dumps(messagedata, ensure_ascii=False))
#解绑手机
def auth_bindingmobile(request):
    usertoken=request.POST.get("usertoken")
    appsystem=request.POST.get("appsystem")
    company_id = request.POST.get('company_id')
    yzcode = request.POST.get('yzcode')
    mobile=request.POST.get("mobile")
    if not company_id:
        usertoken=request.GET.get("usertoken")
        appsystem=request.GET.get("appsystem")
        company_id = request.GET.get('company_id')
        yzcode = request.GET.get('yzcode')
        mobile=request.GET.get("mobile")
    if not getloginstatus(company_id,usertoken):
        errlist={'tokenerr':'true'}
        return HttpResponse(simplejson.dumps(errlist, ensure_ascii=False))
    sql="select id from auth_forgot_password where userid=%s and auth_key=%s and TIMESTAMPDIFF(MINUTE,gmt_created,now())<600"
    plist=dbc.fetchonedb(sql,[company_id,yzcode]);
    if (plist):
        sql="select id from auth_user where mobile=%s"
        list=dbc.fetchonedb(sql,[mobile]);
        if list:
            errkey="该手机号码已经绑定，你可以用此手机号码直接登录！"
            err="true"
            messagedata={'err':err,'errkey':errkey}
            return HttpResponse(simplejson.dumps(messagedata, ensure_ascii=False))
        
        sqlc="select id from company_account where mobile=%s"
        list=dbc.fetchonedb(sqlc,[mobile]);
        if list:
            errkey="该手机号码已经绑定，你可以用此手机号码直接登录！"
            err="true"
            messagedata={'err':err,'errkey':errkey}
            return HttpResponse(simplejson.dumps(messagedata, ensure_ascii=False))
        
        sqlc="select mobile,account from company_account where company_id=%s"
        list=dbc.fetchonedb(sqlc,[company_id]);
        if list:
            account=list[1]
            #绑定手机时，如果账号和手机号相同，修改和绑定手机，需要把账号禁用，这样下次就不能用原手机登录了（因为账号不能修改）
            if account==mobile:
                sql="select id from auth_user_block where account=%s"
                list1=dbc.fetchonedb(sql,[account])
                if list1:
                    sql="update auth_user_block set block=1 where account=%s"
                    dbc.updatetodb(sql,[account])
                else:
                    gmt_created=datetime.datetime.now()
                    sql="insert into auth_user_block(account,block,gmt_created) values(%s,%s,%s)"
                    dbc.updatetodb(sql,[account,1,gmt_created])
            sql="update company_account set mobile=%s where company_id=%s"
            dbc.updatetodb(sql,[mobile,company_id])
            sql="update auth_user set mobile=%s where username=%s"
            dbc.updatetodb(sql,[mobile,account])
            errkey="绑定成功！"
            err="false"
        else:
            errkey="系统错误，账号不存在！"
            err="true"
    else:
        errkey="你输入的验证码错误！"
        err="true"
    messagedata={'err':err,'errkey':errkey}
    return HttpResponse(simplejson.dumps(messagedata, ensure_ascii=False))
#修改公司资料
def myinfo(request):
    company_id=request.GET.get("company_id")
    usertoken=request.GET.get("usertoken")
    appsystem=request.GET.get("appsystem")
    if not getloginstatus(company_id,usertoken):
        errlist={'tokenerr':'true'}
        return HttpResponse(simplejson.dumps(errlist, ensure_ascii=False))
    if company_id:
        contactinfolist=zzc.get_contactinfo(company_id)
        companyinfolist=zzc.get_companyinfo(company_id)
        sql="select picture_path from bbs_user_profiler where company_id=%s"
        piclist=dbc.fetchonedb(sql,[company_id])
        faceurl=None
        if piclist:
            if piclist[0]:
                faceurl="http://img3.zz91.com/100x100/"+piclist[0]
        messagedata={'err':'false','errkey':'','type':'myinfo','contactinfolist':contactinfolist,'companyinfolist':companyinfolist,'faceurl':faceurl}
        return HttpResponse(simplejson.dumps(messagedata, ensure_ascii=False))
#修改公司资料保存
def myinfosave(request):
    company_id=request.POST.get("company_id")
    usertoken=request.POST.get("usertoken")
    if not getloginstatus(company_id,usertoken):
        errlist={'tokenerr':'true'}
        return HttpResponse(simplejson.dumps(errlist, ensure_ascii=False))
    piclist=otherimgupload(request)
    faceurl=None
    if piclist:
        for p in piclist:
            faceurl=p['databasepath']
            faceid=p['id']
    appsystem=request.POST.get("appsystem")
    contact = request.POST.get('contact')
    sex = request.POST.get('sex')
    qq = request.POST.get('qq')
    email = request.POST.get('email')
    industryCode = request.POST.get('industryCode')
    serviceCode = request.POST.get('serviceCode')
    areaCode = request.POST.get('areaCode')
    comname = request.POST.get('comname')
    weixin = request.POST.get('weixin')
    if not areaCode:
        areaCode="10011000"
    address = request.POST.get('address')
    addresszip = request.POST.get('addresszip')
    business = request.POST.get('business')
    
    if company_id:
        account=getaccount(company_id)
        #-互助用户表
        sqlh="select id from bbs_user_profiler where company_id=%s"
        userlist=dbc.fetchonedbmain(sqlh,[company_id])
        if (userlist==None):
            gmt_created=gmt_modified=datetime.datetime.now()
            value=[company_id,account,contact,email,qq,contact,gmt_modified,gmt_created]
            sqlu="insert into bbs_user_profiler(company_id,account,nickname,email,qq,real_name,gmt_modified,gmt_created) values(%s,%s,%s,%s,%s,%s,%s,%s)"
            dbc.updatetodb(sqlu,value);
        #保存头像
        if faceurl:
            sql="update bbs_user_profiler set picture_path=%s where company_id=%s"
            dbc.updatetodb(sql,[faceurl,company_id]);
        
        value=[industryCode,business,serviceCode,areaCode,address,addresszip,company_id]
        sql="update company set industry_code=%s,business=%s,service_code=%s,area_code=%s,address=%s,address_zip=%s where id=%s"
        dbc.updatetodb(sql,value);
        sql="select id  from company_account where email=%s and company_id>%s and company_id<%s"
        accountlist=dbc.fetchonedb(sql,[str(email),company_id,company_id])
        if (accountlist):
            errflag=1
            errtext="您填写邮箱已经注册！请更换其他邮箱，或点此<a href='/weixin/sendemail.html'>获得密码?</a>或请修改后重新提交！"
            messagedata={'err':'true','errkey':errtext,'type':'myinfosave'}
        else:
            value1=[email,qq,contact,sex,weixin,company_id]
            errtext=""
            sql1="update company_account set email=%s,qq=%s,contact=%s,sex=%s,weixin=%s where company_id=%s"
            dbc.updatetodb(sql1,value1);
            messagedata={'err':'false','errkey':errtext,'type':'myinfosave'}
        return HttpResponse(simplejson.dumps(messagedata, ensure_ascii=False))
#修改密码
def modpasswd(request):
    company_id=request.GET.get('company_id')
    usertoken=request.GET.get("usertoken")
    appsystem=request.GET.get("appsystem")
    if not getloginstatus(company_id,usertoken):
        errlist={'tokenerr':'true'}
        return HttpResponse(simplejson.dumps(errlist, ensure_ascii=False))
    if not company_id or str(company_id)=="0":
        return HttpResponse("err")
    return render_to_response('forgetpasswd/modpasswd.html',locals())
def resetpasswd(request):
    sedcold=request.POST.get('sedcold')
    newcold=request.POST.get('newcold')
    company_id=request.POST.get('company_id')
    yzcode = request.POST.get('yzcode')
    appsystem=request.POST.get("appsystem")
    if not yzcode:
        messagedata={'err':'true','errkey':'请输入验证码'}
        return HttpResponse(simplejson.dumps(messagedata, ensure_ascii=False))
    if sedcold!=newcold or not sedcold:
        messagedata={'err':'true','errkey':'两次输入的密码不一致，请重新输入'}
        return HttpResponse(simplejson.dumps(messagedata, ensure_ascii=False))
    if not company_id:
        messagedata={'err':'true','errkey':'未登录'}
        return HttpResponse(simplejson.dumps(messagedata, ensure_ascii=False))
    
    sql="select id from auth_forgot_password where userid=%s and auth_key=%s and TIMESTAMPDIFF(MINUTE,gmt_created,now())<600"
    plist=dbc.fetchonedb(sql,[company_id,yzcode]);
    gmt_modified=datetime.datetime.now()
    messagedata={"err":"true","errkey":"验证码错误！"}
    if plist:
        md5pwd_pass = hashlib.md5(sedcold)
        md5passwd = md5pwd_pass.hexdigest()[8:-8]
        account=getaccount(company_id)
        sql="update auth_user set password=%s,gmt_modified=%s where username=%s"
        dbc.updatetodb(sql,[md5passwd,gmt_modified,account]);
        sql="update company_account set password=%s,gmt_modified=%s where account=%s"
        dbc.updatetodb(sql,[newcold,gmt_modified,account]);
        messagedata={"err":"false","errkey":""}
    return HttpResponse(simplejson.dumps(messagedata, ensure_ascii=False))
        
def modpasswdsave(request):
    company_id=request.GET.get('company_id')
    oldcold=request.GET.get('oldcold')
    newcold=request.GET.get('newcold')
    newcold_true=request.GET.get('newcold')
    sedcold=request.GET.get('sedcold')
    usertoken=request.GET.get("usertoken")
    if not getloginstatus(company_id,usertoken):
        errlist={'tokenerr':'true'}
        return HttpResponse(simplejson.dumps(errlist, ensure_ascii=False))

    if oldcold:
        md5pwd_old = hashlib.md5(oldcold)
        oldcold = md5pwd_old.hexdigest()[8:-8]
    if newcold:
        md5pwd_new = hashlib.md5(newcold)
        newcold = md5pwd_new.hexdigest()[8:-8]
    gmt_modified=datetime.datetime.now()
    
    if company_id:
        sqlc="select account from company_account where company_id=%s"
        list=dbc.fetchonedb(sqlc,[company_id]);
        if list:
            account=list[0]
            
            sql="select id,username from auth_user where (username=%s and password=%s)"
            plist=dbc.fetchonedb(sql,[account,oldcold]);
            if plist:
                id=plist[0]
                sql="update auth_user set password=%s,gmt_modified=%s where id=%s"
                dbc.updatetodb(sql,[newcold,gmt_modified,id]);
                sql="update company_account set password=%s,gmt_modified=%s where account=%s"
                dbc.updatetodb(sql,[newcold_true,gmt_modified,account]);
                resultlist={"error_code":0,"reason":"","result":"成功！"}
                response = HttpResponse(simplejson.dumps(resultlist, ensure_ascii=False))
                return response
            else:
                resultlist={"error_code":10,"reason":"","result":"旧密码错误！"}
                response = HttpResponse(simplejson.dumps(resultlist, ensure_ascii=False))
                return response
        else:
            resultlist={"error_code":10,"reason":"","result":"用户不存在！"}
            response = HttpResponse(simplejson.dumps(resultlist, ensure_ascii=False))
            return response
    resultlist={"error_code":10,"reason":"","result":"错误"}
    response = HttpResponse(simplejson.dumps(resultlist, ensure_ascii=False))
    return response
#QQ登录绑定
def qqlogin(request):
    qqopenid=request.GET.get("qqopenid")
    #随机账号名
    username=request.GET.get("username")
    appid = request.GET.get('appid')
    datatype=request.GET.get("datatype")
    appsystem = request.GET.get('appsystem')
    open_type = request.GET.get('open_type')
    if not open_type:
        open_type="qq.com"
    gmt_modified=gmt_created=datetime.datetime.now()
    sqlc="select id,company_id,target_account from oauth_access where open_id=%s and open_type=%s"
    list=dbc.fetchonedb(sqlc,[str(qqopenid),open_type])
    if not list:
        messagedata={'err':'true','errkey':'','result':'noreg','token':''}
        return HttpResponse(simplejson.dumps(messagedata, ensure_ascii=False))
    else:
        #company_id=getcompanyid(list[2])
        username=list[2]
        sql="select password,company_id from company_account where account=%s"
        result=dbc.fetchonedb(sql,[username])
        if result:
            passwd=result[0]
            company_id=result[1]
            #判断是否拉黑
            sqlh="select id from company where id=%s and is_block=1"
            listh=dbc.fetchonedb(sqlh,[company_id]);
            if listh:
                error="该用户已经被禁止登录！"
                messagedata={'err':'true','errkey':error,'result':company_id,'token':''}
                return HttpResponse(simplejson.dumps(messagedata, ensure_ascii=False))
            token = hashlib.md5(str(passwd)+str(username)+str(gmt_modified))
            token = token.hexdigest()[8:-8]
            #保存app登陆token
            sql="select id from app_token where token=%s"
            listd=dbc.fetchonedb(sql,[token])
            if not listd:
                oauth_id=0
                sqlp="select max(id) from oauth_access where open_id=%s and target_account=%s and open_type='app.zz91.com' and closeflag=0"
                lista=dbc.fetchonedb(sqlp,[appid,username])
                if lista:
                    oauth_id=lista[0]
                sqlb="select id from app_token where company_id=%s"
                listb=dbc.fetchonedb(sqlb,[company_id])
                if not listb:
                    sqlm="insert into app_token(oauth_id,company_id,token,gmt_created,gmt_modified) values(%s,%s,%s,%s,%s)"
                    dbc.updatetodb(sqlm,[oauth_id,company_id,token,gmt_created,gmt_created])
                else:
                    sqlm="update app_token set oauth_id=%s,token=%s,gmt_created=%s where company_id=%s"
                    dbc.updatetodb(sqlm,[oauth_id,token,gmt_created,company_id])
            updatelogin(request,company_id)
            result=zzc.getcompanylogininfo(company_id=company_id)
            
            #首次安装APP送20 再生钱包#
            zzq.firstsendfee(company_id,appid)
            #首次app登录
            choujiang(company_id=company_id,appid=appid)
            if datatype=="json":
                messagedata={'err':'false','errkey':'1','result':result,'token':token,'passwd':str(hashlib.md5(passwd).hexdigest()),'username':username}
            else:
                messagedata={'err':'false','errkey':'2','result':company_id,'token':token}
            return HttpResponse(simplejson.dumps(messagedata, ensure_ascii=False))
        else:
            messagedata={'err':'true','errkey':'系统错误','result':'','token':''}
            return HttpResponse(simplejson.dumps(messagedata, ensure_ascii=False))
    
    
    
    