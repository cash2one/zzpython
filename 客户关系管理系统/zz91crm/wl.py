#-*- coding:utf-8 -*-
from django.shortcuts import render_to_response,render
from django.http import HttpResponse,HttpResponseRedirect
import simplejson,sys,os,urllib,re,datetime,time,md5,hashlib,random,calendar
from conn import crmdb
from zz91page import *
db=crmdb()
reload(sys)
sys.setdefaultencoding('UTF-8')
nowpath=os.path.dirname(__file__)
execfile(nowpath+"/func/wl_function.py")
execfile(nowpath+"/func/crmtools.py")
execfile(nowpath+"/func/company_function.py")
zzc=customer()
zzs=zzwl()

#取出所有物流客户信息
def wl_list(request):
    username=request.session.get('username',default=None)
    user_id=request.session.get('user_id',default=None)
    if not username or not user_id:
        return HttpResponseRedirect("relogin.html")
    page=request.GET.get('page')
    #是否为主管
    has_auth=zzc.is_hasauth(user_id=user_id)
    if not page:
        page=1
    searchlist={}
    order_number=request.GET.get("order_number")
    if order_number:
         searchlist['order_number']=order_number
    else:
        order_number=''
    company_name=request.GET.get("company_name")
    if company_name:
        searchlist['company_name']=company_name
    else:
        company_name=''
    wechat=request.GET.get("wechat")
    if wechat:
        searchlist['wechat']=wechat
    else:
        wechat=''
    username=request.GET.get("username")
    if username:
        searchlist['username']=username
    else:
        username=''
    mobile=request.GET.get("mobile")
    if mobile:
        searchlist['mobile']=mobile
    else:
        mobile=''
    car_for=request.GET.get("car_for")
    if car_for:
        searchlist['car_for']=car_for
    else:
        car_for=''
    weight=request.GET.get("weight")
    if weight:
        searchlist['weight']=weight
    else:
        weight=''
    personid=request.GET.get("personid")
    if personid:
        searchlist['personid']=personid
    else:
        personid=''
    time1=request.GET.get('time1')
    time2=request.GET.get('time2')
    if time1 and time2:
        searchlist['time1']=time1
        searchlist['time2']=time2
    else:
        time1=''
        time2=''
    star=request.GET.get('star')
    if star:
        searchlist['star']=star
    else:
        star=''
    orderstr=request.GET.get('orderstr')
    if orderstr:
        searchlist['orderstr']=orderstr
    else:
        orderstr=''
    dotype=request.GET.get('dotype')
    if dotype:
        searchlist['dotype']=dotype
    else:
        dotype=''
    searchurl=urllib.urlencode(searchlist)
    searchlist['user_id']=user_id
    #获得销售人员列表(selection)
    allsalesman=zzc.get_allsalesman(user_id=user_id,wl=1)
    funpage=zz91page()
    limitNum=funpage.limitNum(15)
    nowpage=funpage.nowpage(int(page))
    frompageCount=funpage.frompageCount()
    after_range_num = funpage.after_range_num(3)
    before_range_num = funpage.before_range_num(6)
    userallr=zzs.getwllist(frompageCount=frompageCount,limitNum=limitNum,searchlist=searchlist)
    listcount=userallr['count']
    listall=userallr['list']
    listcount = funpage.listcount(listcount)
    page_listcount=funpage.page_listcount()
    firstpage = funpage.firstpage()
    lastpage = funpage.lastpage()
    page_range  = funpage.page_range()
    nextpage = funpage.nextpage()
    prvpage = funpage.prvpage()
    return render_to_response('wl/wl_list.html',locals())
#添加物流客户
def wl_add(request):
    username=request.session.get('username',default=None)
    user_id=request.session.get('user_id',default=None)
    if not username or not user_id:
        return HttpResponseRedirect("relogin.html")
    return render_to_response('wl/wl_add.html',locals())
def wl_save(request):
    company_name=request.POST.get('company_name')
    order_number=request.POST.get('order_number')
    wechat=request.POST.get('wechat')
    mobile=request.POST.get('mobile')
    username=request.POST.get('username')
    car_for=request.POST.get('car_for')
    weight=request.POST.get('weight')
    time=request.POST.get('time')
    main_business=request.POST.get('main_business')
    personid=request.session.get('user_id')
    register_time=datetime.datetime.now()
    sql='insert into wl_customer(company_name,order_number,wechat,mobile,username,car_for,weight,time,main_business,personid,register_time) values(%s, %s, %s,%s, %s, %s, %s, %s, %s, %s, %s)'
    result=db.updatetodb(sql,[company_name,order_number,wechat,mobile,username,car_for,weight,time,main_business,personid,register_time])
    sql='select id from wl_customer order by register_time desc '
    result1=db.fetchonedb(sql)
    last_insert_id=result1['id']
    sql='insert into wl_assign(uid,personid) values(%s, %s)'
    result2=db.updatetodb(sql,[last_insert_id,personid])
    return HttpResponseRedirect('list.html')
#修改人员信息
def wl_mod(request):
    if request.method=="POST":
        company_name=request.POST.get('company_name')
        order_number=request.POST.get('order_number')
        wechat=request.POST.get('wechat')
        username=request.POST.get('username')
        mobile=request.POST.get("mobile")
        car_for=request.POST.get('car_for')
        weight=request.POST.get('weight')
        time=request.POST.get('time')
        id=request.POST.get('id')
        if id:
            sql='update wl_customer set company_name=%s,order_number=%s,wechat=%s,username=%s,mobile=%s,car_for=%s,weight=%s,time=%s where id=%s'
            result=db.updatetodb(sql,[company_name,order_number,wechat,username,mobile,car_for,weight,time,id])
            return HttpResponseRedirect('list.html')
    else:
        id=request.GET.get('uid')
        if id:
            sql='select * from wl_customer where id=%s'
            result=db.fetchonedb(sql,[id])
            time=result['time']
            result['time']=formattime(time,flag=2)
            return render_to_response('wl/wl_mod.html',locals())

#批量处理
def wl_all(request):
    check_box_list = request.REQUEST.getlist("check_box_list")
    topersonid=request.POST.get('topersonid')
    value=request.POST.get('dostay',default=None)
    user_id=request.session.get('user_id',default=None)
    fdate=datetime.datetime.now()
    if not value:
        for id in check_box_list:
            sql='delete from wl_customer where id=%s'
            result=db.updatetodb(sql,[id])
    elif value=='assignto':
        for id in check_box_list:
            sql='insert into wl_assign(uid,personid,fdate) values(%s, %s, %s)'
            result=db.updatetodb(sql,[id,topersonid,fdate])
    elif value=='tomy':
        for id in check_box_list:
            sql='insert into wl_assign(uid,personid,fdate) values(%s, %s, %s)'
            result=db.updatetodb(sql,[id,user_id,fdate])
    elif value=='gonghai':
        for id in check_box_list:
            sql='delete from wl_assign where uid=%s and personid=%s'
            result=db.updatetodb(sql,[id,user_id])
    return HttpResponseRedirect('list.html')
    
#单独界面显示物流客户信息
def wl_customershow(request):
    if request.method=="POST":
        uid=request.GET.get('uid')
        contactstate=request.POST.get('contactstate')
        star=request.POST.get('star')
        nextcontact_time=request.POST.get('nextcontact_time')
        contact_bz=request.POST.get('contact_bz')
        personid=request.session.get('user_id',default=None)
        lastcontact_time=datetime.datetime.now()
        fdate=datetime.datetime.now()
        if uid:
            sql='insert into wl_history(uid,contactstate,star,nextcontact_time,contact_bz,personid,fdate) values(%s,%s,%s,%s,%s,%s,%s)'
            result=db.updatetodb(sql,[uid,contactstate,star,nextcontact_time,contact_bz,personid,fdate])
            sql='update wl_customer set star=%s,nextcontact_time=%s,lastcontact_time=%s where id=%s'
            result=db.updatetodb(sql,[star,nextcontact_time,lastcontact_time,uid])
            return HttpResponseRedirect('list.html')
    else:
        id=request.GET.get('uid')
        if id:
            sql='select * from wl_customer where id=%s'
            result=db.fetchonedb(sql,[id])
            time=result['time']
            result['time']=formattime(time,flag=2)
            time=result['register_time']
            result['register_time']=formattime(time,flag=2)
            return render_to_response('wl/wl_customershow.html',locals())
#操作记录
def wl_customer_history(request):
    page=request.GET.get('page')
    if not page:
        page=1
    searchlist={}
    uid=request.GET.get('uid')
    if uid:
        searchlist['uid']=uid
    funpage=zz91page()
    limitNum=funpage.limitNum(4)
    nowpage=funpage.nowpage(int(page))
    frompageCount=funpage.frompageCount()
    after_range_num = funpage.after_range_num(3)
    before_range_num = funpage.before_range_num(6)
    userallr=zzs.getcustomerhistory(searchlist=searchlist,frompageCount=frompageCount,limitNum=limitNum)
    listall=userallr['list']
    listcount=userallr['count']
    listcount = funpage.listcount(listcount)
    page_listcount=funpage.page_listcount()
    firstpage = funpage.firstpage()
    lastpage = funpage.lastpage()
    page_range  = funpage.page_range()
    nextpage = funpage  .nextpage()
    prvpage = funpage.prvpage()
    return render_to_response('wl/wl_customershow_history.html',locals())