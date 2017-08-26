#-*- coding:utf-8 -*-
from django.shortcuts import render_to_response
from django.http import HttpResponse,HttpResponseRedirect
import simplejson,sys,os,urllib,re
from conn import bestjoydb
from zz91page import *
db = bestjoydb()
reload(sys)
sys.setdefaultencoding('UTF-8')
nowpath=os.path.dirname(__file__)
execfile(nowpath+"/func/admin_function.py")
execfile(nowpath+"/func/company_function.py")
zzu=useradmin()
zzc=customer()
#主框架
def main(request):
    username=request.session.get('username',default=None)
    if not username:
        return HttpResponseRedirect("login.html")
    return render_to_response('main.html',locals())

#--团队管理

#--员工列表
def userlist(request):
    username=request.session.get('username',default=None)
    user_id=request.session.get('user_id',default=None)
    if not username or not user_id:
        return HttpResponseRedirect("relogin.html")
    page=request.GET.get('page')
    if not page:
        page=1
    searchlist={}
    username=request.GET.get('username')
    user_category_code=request.GET.get('user_category_code')
    closeflag=request.GET.get('closeflag')
    if username:
        searchlist['username']=username
    if user_category_code:
        searchlist['user_category_code']=user_category_code
    if closeflag:
        searchlist['closeflag']=closeflag
    
    searchurl=urllib.urlencode(searchlist)
    funpage=zz91page()
    limitNum=funpage.limitNum(10)
    nowpage=funpage.nowpage(int(page))
    frompageCount=funpage.frompageCount()
    after_range_num = funpage.after_range_num(3)
    before_range_num = funpage.before_range_num(6)
    #获得团队
    userallr=zzu.get_user(frompageCount,limitNum,username,user_category_code=user_category_code,closeflag=closeflag)
    listcount=userallr['listcount']
    listall=userallr['listall']
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
    return render_to_response('userlist.html',locals())
def adduser(request):
    username=request.session.get('username',default=None)
    user_id=request.session.get('user_id',default=None)
    if not username or not user_id:
        return HttpResponseRedirect("relogin.html")
    label=request.POST.get('label')
    user_category_all=zzu.getusercategory()
    auth_category_all=zzu.getauthcategory()
    usercategory_code4=zzu.getusercategory_code4()
    return render_to_response('staff/adduser.html',locals())
def adduserok(request):
    username=request.session.get('username',default=None)
    user_id=request.session.get('user_id',default=None)
    if not username or not user_id:
        return HttpResponseRedirect("relogin.html")
    userid=request.POST.get('userid')
    username=request.POST.get('username')
    realname=request.POST.get('realname')
    password=request.POST.get('password')
    user_category_id=request.POST.getlist('user_category_id')
    user_category_id_txt=''
    for uc_id in user_category_id:
        user_category_id_txt=user_category_id_txt+str(uc_id)+','
    safepasswd=password
    user_category_code=request.POST.get('user_category')
    auth_category_id=request.POST.getlist('auth_category')
    auth_category_id_txt=''
    if auth_category_id:
        for ac_id in auth_category_id:
            auth_category_id_txt=auth_category_id_txt+str(ac_id)+','
    closeflag=request.POST.get('closeflag')
    if not closeflag:
        closeflag=0
    isadmin=request.POST.get('isadmin')
    isadmin=1
    if not userid:
        sql="select id from user where username=%s"
        result=db.fetchonedb(sql,[username])
        if not result:
            sql='insert into user (username,password,safepasswd,user_category_code,auth_category_id,user_category_id,realname,closeflag,isadmin) values (%s,%s,%s,%s,%s,%s,%s,%s,%s)'
            db.updatetodb(sql,[username,password,safepasswd,user_category_code,auth_category_id_txt,user_category_id_txt,realname,closeflag,isadmin])
        else:
            return HttpResponse("用户名重复，请使用其他用户名")
    else:
        sql='update user set username=%s,password=%s,safepasswd=%s,user_category_code=%s,auth_category_id=%s,user_category_id=%s,realname=%s,closeflag=%s,isadmin=%s where id=%s'
        db.updatetodb(sql,[username,password,safepasswd,user_category_code,auth_category_id_txt,user_category_id_txt,realname,closeflag,isadmin,userid])
    #request_url=request.META.get('HTTP_REFERER','/')
    request_url=request.POST.get('request_url')
    return HttpResponseRedirect(request_url)
    #return HttpResponseRedirect("userlist.html")
def edituser(request):
    username=request.session.get('username',default=None)
    user_id=request.session.get('user_id',default=None)
    if not username or not user_id:
        return HttpResponseRedirect("relogin.html")
    user_category_all=zzu.getusercategory()
    auth_category_all=zzu.getauthcategory()
    usercategory_code4=zzu.getusercategory_code4()#团队权限
    request_url=request.META.get('HTTP_REFERER','/')
    userid=request.GET.get('userid')
    #用户级别
    authlist=zzc.geauthid(user_id=user_id)
    #是否管理员
    isadmin=None
    if "1" in authlist:
        isadmin=1
    sql='select u.id,u.username,u.password,u.realname,u.user_category_code,u.auth_category_id,u.user_category_id,u.closeflag,u.isadmin,c.label as user_category,a.label as auth_category from user as u left join user_category as c on u.user_category_code=c.code  left join auth_category as a on u.auth_category_id=a.id where u.id=%s'
    result=db.fetchonedb(sql,[userid])
    user_category_id=result['user_category_id']
    if user_category_id:
        user_category_id=user_category_id[:-1]
    auth_category_id=result['auth_category_id']
    if auth_category_id:
        auth_category_id=auth_category_id[:-1]
    return render_to_response('moduser.html',locals())
#改变用户状态，开通还是冻结
def changestatus_user(request):
    username=request.session.get('username',default=None)
    user_id=request.session.get('user_id',default=None)
    if not username or not user_id:
        return HttpResponseRedirect("relogin.html")
    status=request.GET.get('status')
    id=request.GET.get('id')
    if int(status)==0:
        #动作为要关闭
        closeflag=1
        sql='update user set closeflag=%s where id=%s'
        db.updatetodb(sql,[closeflag,id])
    if int(status)==1:
        #动作为要打开
        closeflag=0
        sql='update user set closeflag=%s where id=%s'
        db.updatetodb(sql,[closeflag,id])
    request_url=request.META.get('HTTP_REFERER','/')
    return HttpResponseRedirect(request_url)
#员工一键删除
def del_alluser(request):
    username=request.session.get('username',default=None)
    user_id=request.session.get('user_id',default=None)
    if not username or not user_id:
        return HttpResponseRedirect("relogin.html")
    checkid=request.GET.getlist('checkid')
    zzu.del_alluser(checkid)
    request_url=request.META.get('HTTP_REFERER','/')
    return HttpResponseRedirect(request_url)
#员工一键删除
def deluser(request):
    username=request.session.get('username',default=None)
    user_id=request.session.get('user_id',default=None)
    if not username or not user_id:
        return HttpResponseRedirect("relogin.html")
    id=request.GET.get('id')
    zzu.del_alluser(id)
    request_url=request.META.get('HTTP_REFERER','/')
    return HttpResponseRedirect(request_url)
