#-*- coding:utf-8 -*-
from django.shortcuts import render_to_response
from django.http import HttpResponse,HttpResponseRedirect
import simplejson,sys,os,urllib,re,datetime,time,md5,hashlib,random,calendar
import calendar as cal
from conn import crmdb
from zz91page import *
from sphinxapi import *
from settings import searchconfig
#from sphinx_rt import spcursor
#sp=spcursor()
db = crmdb()
reload(sys)
sys.setdefaultencoding('UTF-8')
nowpath=os.path.dirname(__file__)
#行业字典
INDUSTRY_LABEL={
    '10001000':'废塑料',
    '10001001':'废金属',
    '10001002':'废纸',
    '10001003':'废旧轮胎与废橡胶',
    '10001004':'废纺织品与废皮革',
    '10001005':'废电子电器',
    '10001006':'废玻璃',
    '10001007':'废旧二手设备',
    '10001008':'其他废料',
    '10001009':'服务',
    '10001010':'塑料原料',
}
INDUSTRY_LABEL_old={
    '1':'废金属',
    '2':'废塑料',
    '3':'废纸',
    '4':'废旧轮胎与废橡胶',
    '5':'废纺织品与废皮革',
    '6':'废电子电器',
    '10':'废玻璃',
    '12':'机械设备',
    '14':'其他废料',
    '15':'服务',
    '16':'汽车拆解'
}
execfile(nowpath+"/func/company_function.py")
execfile(nowpath+"/func/crmtools.py")
zzc=customer()

def index(request):
    return render_to_response("icdhtml/index.html",locals())
#我的所有客户
def icdlist(request):
    username=request.session.get('username',default=None)
    user_id=request.session.get('user_id',default=None)
    if not username or not user_id:
        return HttpResponseRedirect("relogin.html")
    #是否为主管
    has_auth=zzc.is_hasauth(user_id=user_id)
    #用户级别
    authlist=zzc.geauthid(user_id=user_id)
    #是否管理员
    isadmin=None
    if "1" in authlist:
        isadmin=1
    
    request_url=request.META.get('HTTP_REFERER','/')
    page=request.GET.get('page')
    isvapflag=None
    if not page:
        page=1
    dotype=request.GET.get('dotype')
    #所有客户，只有管理员才能分配
    isfengpei=1
    if dotype=="allall" or dotype=="zsh_allall" or dotype=='customin' or dotype=='laji' or dotype=='zsh_customin':
        if not isadmin:
            isfengpei=None
    
    nowdint=int(time.strftime('%H%M',time.localtime(time.time())))
    if (dotype=="gonghai" or dotype=="zsh_gonghai"):
        wk=getToday().weekday()
        if wk in [0,1,2,3,4]:
            moth=getToday().strftime('%m')
            if str(moth) in ['01','02','03','04','05','11','12']:
                if nowdint > 830 and nowdint<1200:
                    return HttpResponse("该时间公海不开放！")
                if nowdint > 1330 and nowdint<1730:
                    return HttpResponse("该时间公海不开放！")
            if str(moth) in ['06','07','08','09','10']:
                if nowdint > 830 and nowdint<1200:
                    return HttpResponse("该时间公海不开放！")
                if nowdint > 1330 and nowdint<1800:
                    return HttpResponse("该时间公海不开放！")
    iszshflag=None
    isvapflag=None
    if dotype:
        if (dotype[0:3]=="vap"):
            isvapflag=1
        if (dotype[0:3]=="zsh"):
            iszshflag=1
    if dotype=="customin" or dotype=='zsh_customin':
        lucheck=1
    if dotype=="requestassign" or dotype=="zsh_requestassign":
        sqcheck=1
    lmaction=request.GET.get('lmaction')
    #搜索
    searchlist={}
    companyname=request.GET.get('companyname')
    contact=request.GET.get('contact')
    mobile=request.GET.get('mobile')
    email=request.GET.get('email')
    business=request.GET.get('business')
    address=request.GET.get('address')
    com_rank=request.GET.get('com_rank')
    
    industry=request.GET.get('industry')
    account=request.GET.get('account')
    industry_txt=''
    if industry:
        industry_txt=INDUSTRY_LABEL[industry]
    last_login_time_begin=request.GET.get('last_login_time_begin')
    last_login_time_end=request.GET.get('last_login_time_end')
    regtime_begin=request.GET.get('regtime_begin')
    regtime_end=request.GET.get('regtime_end')
    company_id=request.GET.get('company_id')
    province=request.GET.get('p')
    city=request.GET.get('c')
    
    ccountry=request.GET.get('ccountry')
    country=request.GET.get('country')
    if not country:
        country="1"
    area=request.GET.get('area')
    if not area:
        area=''
    
    contactnexttime_begin=request.GET.get('contactnexttime_begin')
    contactnexttime_end=request.GET.get('contactnexttime_end')
    comporder=request.GET.get('comporder')
    ascdesc=request.GET.get('ascdesc')
    comporder2=request.GET.get('comporder2')
    ascdesc2=request.GET.get('ascdesc2')
    comporder3=request.GET.get('comporder3')
    ascdesc3=request.GET.get('ascdesc3')
    lastteltime_begin=request.GET.get('lastteltime_begin')
    lastteltime_end=request.GET.get('lastteltime_end')
    servicetag=request.GET.get("servicetag")
    isqianbao=request.GET.get("isqianbao")
    
    adminuser_id=request.GET.get("adminuser_id")
    
    is4star=request.GET.get("is4star")
    is5star=request.GET.get("is5star")
    logincount=request.GET.get("logincount")
    
    companytype=request.GET.get("companytype")
    
    telpersoncount=request.GET.get("telpersoncount")
    telcount=request.GET.get("telcount")
    telnocount=request.GET.get("telnocount")
    
    today=getToday()
    today=date_to_int(today)
    
    today=today-60*60*24*5
    
    today=int_to_str(today)
    
    if company_id:
        searchlist['company_id']=company_id
    if telpersoncount:
        searchlist['telpersoncount']=telpersoncount
    if telcount:
        searchlist['telcount']=telcount
    if telnocount:
        searchlist['telnocount']=telnocount
    if adminuser_id:
        searchlist['adminuser_id']=adminuser_id
    if companytype:
        searchlist['companytype']=companytype
    if is4star:
        searchlist['is4star']=is4star
    if is5star:
        searchlist['is5star']=is5star
    if logincount:
        searchlist['logincount']=logincount
    if comporder:
        searchlist['comporder']=comporder
    if ascdesc:
        searchlist['ascdesc']=ascdesc
    if comporder2:
        searchlist['comporder2']=comporder2
    if ascdesc2:
        searchlist['ascdesc2']=ascdesc2
    if comporder3:
        searchlist['comporder3']=comporder3
    if ascdesc3:
        searchlist['ascdesc3']=ascdesc3
    if servicetag:
        searchlist['servicetag']=servicetag
    if companyname:
        searchlist['companyname']=companyname
    if contact:
        searchlist['contact']=contact
    if mobile:
        searchlist['mobile']=mobile
    if email:
        searchlist['email']=email
    if account:
        searchlist['account']=account
    if address:
        searchlist['address']=address
    if business:
        searchlist['business']=business
    if industry_txt:
        searchlist['industry_txt']=industry_txt
    if industry:
        searchlist['industry']=industry
    if com_rank:
        searchlist['com_rank']=com_rank
    if area:
        searchlist['area']=area
    if province:
        searchlist['p']=province
    if city:
        searchlist['c']=city
    if ccountry:
        searchlist['ccountry']=ccountry
    if country:
        searchlist['country']=country
    if last_login_time_begin:
        searchlist['last_login_time_begin']=last_login_time_begin
    if last_login_time_end:
        searchlist['last_login_time_end']=last_login_time_end
    if regtime_begin:
        searchlist['regtime_begin']=regtime_begin
    if regtime_end:
        searchlist['regtime_end']=regtime_end
        
    if lastteltime_begin:
        searchlist['lastteltime_begin']=lastteltime_begin
    if lastteltime_end:
        searchlist['lastteltime_end']=lastteltime_end
        
    if contactnexttime_begin:
        searchlist['contactnexttime_begin']=contactnexttime_begin
    if contactnexttime_end:
        searchlist['contactnexttime_end']=contactnexttime_end
    if isqianbao:
        searchlist['isqianbao']=isqianbao
        
    if not dotype:
        dotype=""
    if dotype:
        searchlist['dotype']=dotype
    if not lmaction:
        lmaction=""
    if lmaction:
        searchlist['lmaction']=lmaction
        
    searchurl=urllib.urlencode(searchlist)
    #过滤@号
    if searchlist:
        for ss in searchlist:
            values=searchlist[ss]
            values=values.replace("@"," ")
            searchlist[ss]=values
    #放公海的栏目
    if (dotype in ('my','contact','nocontact','today','allbm','vap_allbm','zsh_allbm','zsh_my','zsh_contact','zsh_nocontact','zsh_today')):
        dropbutton=1
    
    funpage=zz91page()
    limitNum=funpage.limitNum(10)
    nowpage=funpage.nowpage(int(page))
    frompageCount=funpage.frompageCount()
    after_range_num = funpage.after_range_num(3)
    before_range_num = funpage.before_range_num(6)
    #获得客户
    allcustomer=zzc.get_allcustomer(frompageCount=frompageCount,limitNum=limitNum,searchlist=searchlist,user_id=user_id)
    #获得销售人员列表(selection)
    if isvapflag:
        allsalesman=zzc.get_allsalesman(user_id=user_id)
    elif iszshflag:
        allsalesman=zzc.get_allsalesman(user_id=user_id,zsh=1)
    else:
        allsalesman=zzc.get_allsalesman(user_id=user_id)
    if allcustomer:
        listcount=allcustomer['listcount']
        listall=allcustomer['listall']
        listcount = funpage.listcount(listcount)
        page_listcount=funpage.page_listcount()
        firstpage = funpage.firstpage()
        lastpage = funpage.lastpage()
        page_range  = funpage.page_range()
        if len(page_range)>7:
            page_range=page_range[:7]
        nextpage = funpage.nextpage()
        prvpage = funpage.prvpage()
    provincelist=zzc.getprovincelist()
    #服务列表
    servicelist=zzc.getservicelist()
    guowaiprovincelist=zzc.getguowailist()
    
    return render_to_response("icdhtml/icdlist.html",locals())
#添加其他联系人页面
def otherperson(request):
    #编辑时取值
    editid=request.GET.get('edit')
    company_id=request.GET.get('company_id')
    dotype=request.GET.get('dotype')
    if editid:
        sql="select company_id,name,sex,tel,mobile,station,fax,email,address,bz,user_id,gmt_modified,gmt_created from kh_othercontact where id=%s"
        result=db.fetchonedb(sql,[editid])
    return render_to_response("icdhtml/otherperson.html",locals())
#添加其他联系人
def add_otherperson(request):
    username=request.session.get('username',default=None)
    user_id=request.session.get('user_id',default=None)
    if not username or not user_id:
        return HttpResponseRedirect("relogin.html")
    company_id=request.POST.get('company_id')
    dotype=request.POST.get('dotype')
    if not dotype:
        dotype=""
    name=request.POST.get('other_name')
    sex=request.POST.get('other_sex')
    tel=request.POST.get('other_tel')
    mobile=request.POST.get('other_mobile')
    station=request.POST.get('other_station')
    fax=request.POST.get('other_fax')
    email=request.POST.get('other_email')
    address=request.POST.get('other_address')
    bz=request.POST.get('other_bz')
    gmt_modified=datetime.datetime.now()
    gmt_created=gmt_modified
    editflag=request.POST.get('editflag')
    if editflag:
        sql='update kh_othercontact set company_id=%s,name=%s,sex=%s,tel=%s,mobile=%s,station=%s,fax=%s,email=%s,address=%s,bz=%s,user_id=%s,gmt_modified=%s where id=%s'
        db.updatetodb(sql,[company_id,name,sex,tel,mobile,station,fax,email,address,bz,user_id,gmt_modified,editflag])
    else:
        sql='insert into kh_othercontact (company_id,name,sex,tel,mobile,station,fax,email,address,bz,user_id,gmt_modified,gmt_created) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
        db.updatetodb(sql,[company_id,name,sex,tel,mobile,station,fax,email,address,bz,user_id,gmt_modified,gmt_created])
    zzc.updatemodifydata(company_id)
    savekhlog(company_id,user_id,user_id,'增加其他联系人')
    return HttpResponseRedirect("crm_cominfoedit.html?company_id="+str(company_id)+"&dotype="+dotype)
    res={'res':'suc'}
    res=simplejson.dumps(res,ensure_ascii=False)
    return HttpResponse(res)
#删除其他联系人
def del_otherperson(request):
    username=request.session.get('username',default=None)
    user_id=request.session.get('user_id',default=None)
    if not username or not user_id:
        return HttpResponseRedirect("relogin.html")
    otherperson_id=request.GET.get('otherperson_id')
    dotype=request.GET.get('dotype')
    user_id=request.session.get('user_id',default=None)
    company_id=request.GET.get('company_id')
    sql='delete from kh_othercontact where id=%s and user_id=%s'
    db.updatetodb(sql,[otherperson_id,user_id])
    savekhlog(company_id,user_id,user_id,'删除其他联系人')
    return HttpResponseRedirect("crm_cominfoedit.html?company_id="+str(company_id)+"&dotype="+dotype)

#销售记录列表(iframe)
def tellist(request):
    """
    username=request.session.get('username',default=None)
    user_id=request.session.get('user_id',default=None)
    if not username or not user_id:
        return HttpResponseRedirect("relogin.html")
    """
    #翻页
    page=request.GET.get('page')
    if not page:
        page=1
    funpage=zz91page()
    limitNum=funpage.limitNum(10)
    nowpage=funpage.nowpage(int(page))
    frompageCount=funpage.frompageCount()
    after_range_num = funpage.after_range_num(5)
    before_range_num = funpage.before_range_num(9)
    #参数获得
    request_url=request.META.get('HTTP_REFERER','/')
    company_id=request.GET.get("company_id")
    telflag=request.GET.get("telflag")
    
    searchlist={}
    if company_id:
        searchlist['company_id']=company_id
    if telflag:
        searchlist['telflag']=telflag
        
    searchurl=urllib.urlencode(searchlist)
    
    telsalelistall=zzc.gettelsalelist(frompageCount,limitNum,company_id=company_id,telflag=telflag)
    telsalelist=telsalelistall['list']
    listcount=telsalelistall['count']
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
    
    user_id=request.session.get('user_id',default=None)#销售id
    is_admin=zzc.get_is_admin(user_id)#是否为管理员权限
    #是否主管
    iszhuguan=None
    if user_id:
        has_auth=zzc.is_hasauth(user_id=user_id)
        if str(has_auth)=="1":
            iszhuguan=1
    #删除销售记录(管理员权限拥有)
    """
    del_flag=request.GET.get("del")
    com_id=request.GET.get("com_id")
    id=request.GET.get("id")
    if del_flag:
        sql='delete from kh_tel where id=%s and company_id=%s'
        db.updatetodb(sql,[id,com_id])
        return HttpResponseRedirect(request_url)
    """
    return render_to_response("icdhtml/tellist.html",locals())
#日志列表
def khloglist(request):
    username=request.session.get('username',default=None)
    user_id=request.session.get('user_id',default=None)
    if not username or not user_id:
        return HttpResponseRedirect("relogin.html")
    #翻页
    page=request.GET.get('page')
    if not page:
        page=1
    funpage=zz91page()
    limitNum=funpage.limitNum(10)
    nowpage=funpage.nowpage(int(page))
    frompageCount=funpage.frompageCount()
    after_range_num = funpage.after_range_num(5)
    before_range_num = funpage.before_range_num(9)
    #参数获得
    request_url=request.META.get('HTTP_REFERER','/')
    company_id=request.GET.get("company_id")
    admin_user_id=request.GET.get("admin_user_id")
    old_user_id=request.GET.get("old_user_id")
    dotype=request.GET.get('dotype')
    mydo=request.GET.get('mydo')
    searchlist={}
    if company_id:
        searchlist['company_id']=company_id
    if admin_user_id:
        searchlist['admin_user_id']=admin_user_id
    if old_user_id:
        searchlist['old_user_id']=old_user_id
    if dotype:
        searchlist['dotype']=dotype
    
    if mydo:
        searchlist['admin_user_id']=user_id
        
    searchurl=urllib.urlencode(searchlist)
    
    loglistall=zzc.getloglist(frompageCount,limitNum,searchlist=searchlist,dotype=dotype)
    loglist=loglistall['list']
    listcount=loglistall['count']
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
    
    
    is_admin=zzc.get_is_admin(user_id)#是否为管理员权限
    return render_to_response("icdhtml/log.html",locals())
#添加销售记录成功
def addtellist(request):
    username=request.session.get('username',default=None)
    user_id=request.session.get('user_id',default=None)
    if not username or not user_id:
        return HttpResponse(simplejson.dumps({'err':'login'}, ensure_ascii=False))
    company_id=request.POST.get('company_id')
    dotype=request.POST.get('dotype')
    contacttype=request.POST.get('contacttype')
    teltime=datetime.datetime.now()#当前电话时间
    rank=request.POST.get('com_rank')
    telflag=request.POST.get('telflag')
    seoflag=request.POST.get('telflag')
    if not seoflag:
        teltags=0
    else:
        teltags=seoflag
    contactnexttime=request.POST.get('contactnexttime')
    nocontacttype=request.POST.get('c_Nocontact')
    detail=request.POST.get('detail')
    gmt_created=teltime
    sql='insert into kh_tel (company_id,contacttype,teltime,user_id,rank,telflag,contactnexttime,nocontacttype,detail,gmt_created,teltags) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
    db.updatetodb(sql,[company_id,contacttype,teltime,user_id,rank,telflag,contactnexttime,nocontacttype,detail,gmt_created,teltags])
        
    if dotype[0:3]=="vap":
        sql2='select id,rank,lastteltime,is4star,is5star from kh_sales_vap where company_id=%s order by id desc'
        result=db.fetchonedb(sql2,[company_id])
        if not rank:
            rank=0
        is4star=0
        is5star=0
        if result:
            is4star=result['is4star']
            is5star=result['is5star']
        if rank:
            if float(rank)>=4 and float(rank)<5:
                is4star=1
            if float(rank)>=5:
                is5star=1
            if not is4star:
                is4star=0
            if not is5star:
                is5star=0
        oldrank=0
        if result:
            oldrank=result['rank']
            lastteltime=result['lastteltime']
            if str(contacttype)=="13":
                lastteltime=gmt_created
            #有，则更新哦
            sql3='update kh_sales_vap set company_id=%s,rank=%s,contactnexttime=%s,lastteltime=%s,contacttype=%s,gmt_modified=%s,is4star=%s,is5star=%s where id=%s'
            db.updatetodb(sql3,[company_id,rank,contactnexttime,lastteltime,contacttype,gmt_created,is4star,is5star,result['id']])
        else:
            #没有,则插入
            lastteltime=None
            if str(contacttype)=="13":
                lastteltime=gmt_created
            sql3='insert into kh_sales_vap (company_id,rank,contactnexttime,lastteltime,contacttype,is4star,is5star,gmt_created,gmt_modified) values (%s,%s,%s,%s,%s,%s,%s,%s,%s)'
            db.updatetodb(sql3,[company_id,rank,contactnexttime,lastteltime,contacttype,is4star,is5star,gmt_created,gmt_created])
        if contactnexttime:
            #更新为已联系
            sql="update kh_assign_vap set isnew=1 where company_id=%s and user_id=%s"
            db.updatetodb(sql,[company_id,user_id])
            updatesearchseek(['vap_contactnexttime','vap_lastteltime','vap_isnew','vap_is4star','vap_is5star','vap_rank'], {int(company_id):[str_to_int(contactnexttime),date_to_int(gmt_created),1,is4star,is5star,int(float(rank)*10)]})
        #转4、5星客户
        if rank:
            if float(rank)>float(oldrank) and float(rank)>=4 and float(rank)<5:
                sql="insert into kh_changestar(user_id,company_id,telflag,rank,gmt_created) values(%s,%s,%s,%s,%s)"
                db.updatetodb(sql,[user_id,company_id,4,4,gmt_created])
            if float(rank)>float(oldrank) and int(rank)==5:
                sql="insert into kh_changestar(user_id,company_id,telflag,rank,gmt_created) values(%s,%s,%s,%s,%s)"
                db.updatetodb(sql,[user_id,company_id,4,5,gmt_created])
    elif dotype[0:3]=="zsh":
        sql2='select id,rank,lastteltime,is4star,is5star from kh_sales_zsh where company_id=%s order by id desc'
        result=db.fetchonedb(sql2,[company_id])
        if not rank:
            rank=0
        is4star=0
        is5star=0
        if result:
            is4star=result['is4star']
            is5star=result['is5star']
        if rank:
            if float(rank)>=4 and float(rank)<5:
                is4star=1
            if float(rank)>=5:
                is5star=1
            if not is4star:
                is4star=0
            if not is5star:
                is5star=0
        oldrank=0
        if result:
            oldrank=result['rank']
            lastteltime=result['lastteltime']
            if str(contacttype)=="13":
                lastteltime=gmt_created
            #有，则更新哦
            sql3='update kh_sales_zsh set company_id=%s,rank=%s,contactnexttime=%s,lastteltime=%s,contacttype=%s,gmt_modified=%s,is4star=%s,is5star=%s where id=%s'
            db.updatetodb(sql3,[company_id,rank,contactnexttime,lastteltime,contacttype,gmt_created,is4star,is5star,result['id']])
        else:
            #没有,则插入
            lastteltime=None
            if str(contacttype)=="13":
                lastteltime=gmt_created
            sql3='insert into kh_sales_zsh (company_id,rank,contactnexttime,lastteltime,contacttype,is4star,is5star,gmt_created,gmt_modified) values (%s,%s,%s,%s,%s,%s,%s,%s,%s)'
            db.updatetodb(sql3,[company_id,rank,contactnexttime,lastteltime,contacttype,is4star,is5star,gmt_created,gmt_created])
        if contactnexttime:
            #更新为已联系
            sql="update kh_assign_zsh set isnew=1 where company_id=%s and user_id=%s"
            db.updatetodb(sql,[company_id,user_id])
            updatesearchseek(['zsh_contactnexttime','zsh_lastteltime','zsh_isnew','zsh_is4star','zsh_is5star','zsh_rank'], {int(company_id):[str_to_int(contactnexttime),date_to_int(gmt_created),1,is4star,is5star,int(float(rank)*10)]})
        #转4、5星客户
        if rank:
            if float(rank)>float(oldrank) and float(rank)>=4 and float(rank)<5:
                sql="insert into kh_changestar(user_id,company_id,telflag,rank,gmt_created) values(%s,%s,%s,%s,%s)"
                db.updatetodb(sql,[user_id,company_id,5,4,gmt_created])
            if float(rank)>float(oldrank) and int(rank)==5:
                sql="insert into kh_changestar(user_id,company_id,telflag,rank,gmt_created) values(%s,%s,%s,%s,%s)"
                db.updatetodb(sql,[user_id,company_id,5,5,gmt_created])
    else:
        sql2='select id,rank,lastteltime,is4star,is5star from kh_sales where company_id=%s order by id desc'
        result=db.fetchonedb(sql2,[company_id])
        if not rank:
            rank=0
        is4star=0
        is5star=0
        if result:
            is4star=result['is4star']
            is5star=result['is5star']
            if not is4star:
                is4star=0
            if not is5star:
                is5star=0
        if rank:
            if float(rank)>=4 and float(rank)<5:
                is4star=1
            if float(rank)>=5:
                is5star=1
        oldrank=0
        if result:
            oldrank=result['rank']
            lastteltime=result['lastteltime']
            if str(contacttype)=="13":
                lastteltime=gmt_created
            #有，则更新哦
            sql3='update kh_sales set company_id=%s,rank=%s,contactnexttime=%s,lastteltime=%s,contacttype=%s,gmt_modified=%s,is4star=%s,is5star=%s where id=%s'
            db.updatetodb(sql3,[company_id,rank,contactnexttime,lastteltime,contacttype,gmt_created,is4star,is5star,result['id']])
        else:
            #没有,则插入
            lastteltime=None
            if str(contacttype)=="13":
                lastteltime=gmt_created
            sql3='insert into kh_sales (company_id,rank,contactnexttime,lastteltime,contacttype,is4star,is5star,gmt_created,gmt_modified) values (%s,%s,%s,%s,%s,%s,%s,%s,%s)'
            db.updatetodb(sql3,[company_id,rank,contactnexttime,lastteltime,contacttype,is4star,is5star,gmt_created,gmt_created])
        if contactnexttime:
            #更新为已联系
            sql="update kh_assign set isnew=1 where company_id=%s and user_id=%s"
            db.updatetodb(sql,[company_id,user_id])
            updatesearchseek(['contactnexttime','lastteltime','isnew','is4star','is5star','rank'], {int(company_id):[str_to_int(contactnexttime),date_to_int(gmt_created),1,is4star,is5star,int(float(rank)*10)]})
        #转4、5星客户
        if rank:
            if float(rank)>float(oldrank) and float(rank)>=4 and float(rank)<5:
                sql="insert into kh_changestar(user_id,company_id,telflag,rank,gmt_created) values(%s,%s,%s,%s,%s)"
                db.updatetodb(sql,[user_id,company_id,0,4,gmt_created])
            if float(rank)>float(oldrank) and int(rank)==5:
                sql="insert into kh_changestar(user_id,company_id,telflag,rank,gmt_created) values(%s,%s,%s,%s,%s)"
                db.updatetodb(sql,[user_id,company_id,0,5,gmt_created])
    zzc.updatemodifydata(company_id)
    
    res={'res':'suc'}
    res=simplejson.dumps(res, ensure_ascii=False)
    return HttpResponse(res)
#主管建议
def admin_telsave(request):
    username=request.session.get('username',default=None)
    user_id=request.session.get('user_id',default=None)
    if not username or not user_id:
        return HttpResponse(simplejson.dumps({'err':'login'}, ensure_ascii=False))
    company_id=request.POST.get("company_id")
    dotype=request.POST.get("dotype")
    tel_id=request.POST.get("tel_id")
    details=request.POST.get("details")
    gmt_created=datetime.datetime.now()
    sql="insert into kh_tel_admin(user_id,company_id,tel_id,gmt_created,details) values(%s,%s,%s,%s,%s)"
    db.updatetodb(sql,[user_id,company_id,tel_id,gmt_created,details])
    res={'res':'添加成功'}
    res=simplejson.dumps(res, ensure_ascii=False)
    return HttpResponse(res)
#放入我的客户库
def assign_putmy(request):
    username=request.session.get('username',default=None)
    user_id=request.session.get('user_id',default=None)
    if not username or not user_id:
        return HttpResponse(simplejson.dumps({'err':'login'}, ensure_ascii=False))
    company_id=request.GET.get("company_id")
    dotype=request.GET.get("dotype")
    gmt_created=datetime.datetime.now()
    if user_id:
        if dotype[0:3]=="vap":
            #放VAP客户库
            sql="select id,user_id from kh_assign_vap where company_id=%s"
            result=db.fetchonedb(sql,[company_id])
            if not result:
                sqlt="insert into kh_assign_vap (company_id,user_id,gmt_created) values(%s,%s,%s)"
                db.updatetodb(sqlt,[company_id,user_id,gmt_created])
                ret={'res':'成功，你已成功放入该客户到VAP库里','err':'false'}
                zzc.updatemodifydata(company_id)
                savekhlog(company_id,user_id,user_id,'放入我的VAP客户库')
                sqld="update kh_income set assigncheck=0 where company_id=%s"
                db.updatetodb(sqld,[company_id])
                assign_time=dateall_to_int(gmt_created)
                updatesearchseek(['vap_user_id','vap_assigncheck','vap_assign_time','vap_isnew'], {int(company_id):[int(user_id),0,assign_time,0]})
                
            else:
                vap_user_id=result['user_id']
                if vap_user_id==user_id:
                    ret={'res':'失败，该客户已经在你的VAP客户库里','err':'true'}
                else:
                    ret={'res':'失败，该客户在其他VAP客户库里','err':'true'}
        elif dotype[0:3]=="zsh":
            #是否开通再生汇产品
            zshcheck=zzc.getiszshmember(company_id)
            isassign=1
            if not zshcheck:
                #在新签库里就不能分配
                sql="select id from kh_assign where company_id=%s"
                result=db.fetchonedb(sql,[company_id])
                if result:
                    ret={'res':'失败，该客户在其他新签客户库里','err':'true'}
                    isassign=0
            if isassign==1:
                #放再生汇客户库
                sql="select id,user_id from kh_assign_zsh where company_id=%s"
                result=db.fetchonedb(sql,[company_id])
                if not result:
                    sqlt="insert into kh_assign_zsh (company_id,user_id,gmt_created) values(%s,%s,%s)"
                    db.updatetodb(sqlt,[company_id,user_id,gmt_created])
                    ret={'res':'成功，你已成功放入该客户到再生汇库里','err':'false'}
                    zzc.updatemodifydata(company_id)
                    savekhlog(company_id,user_id,user_id,'放入我的再生汇客户库')
                    assign_time=dateall_to_int(gmt_created)
                    updatesearchseek(['zsh_user_id','zsh_assign_time','zsh_isnew'], {int(company_id):[int(user_id),assign_time,0]})
                    
                else:
                    zsh_user_id=result['user_id']
                    if zsh_user_id==user_id:
                        ret={'res':'失败，该客户已经在你的再生汇客户库里','err':'true'}
                    else:
                        ret={'res':'失败，该客户在其他再生汇客户库里','err':'true'}
        else:
            #预录入未审核不能放到我的客户库
            sql="select checked from company where id=%s"
            result=db.fetchonedb(sql,[company_id])
            if result:
                achecked=result['checked']
                if str(achecked)=="1":
                    ret={'res':'失败，该客户被其他销售申请并未审核，不能放不我库里','err':'true'}
                    return HttpResponse(simplejson.dumps(ret, ensure_ascii=False))
            #是否开通再生汇产品
            zshcheck=zzc.getiszshmember(company_id)
            isassign=1
            if not zshcheck:
                #在新签库里就不能分配
                sql="select id from kh_assign_zsh where company_id=%s"
                result=db.fetchonedb(sql,[company_id])
                if result:
                    ret={'res':'失败，该客户在再生汇客户库里','err':'true'}
                    isassign=0
            if isassign==1:
                sql="select id,user_id from kh_assign where company_id=%s"
                result=db.fetchonedb(sql,[company_id])
                if not result:
                    sqlt="insert into kh_assign (company_id,user_id,gmt_created) values(%s,%s,%s)"
                    db.updatetodb(sqlt,[company_id,user_id,gmt_created])
                    ret={'res':'成功，你已成功放入该客户到库里','err':'false'}
                    zzc.updatemodifydata(company_id)
                    savekhlog(company_id,user_id,user_id,'放入我的客户库')
                    assign_time=dateall_to_int(gmt_created)
                    sql="update company set checked=0 where id=%s"
                    db.updatetodb(sql,[company_id])
                    updatesearchseek(['user_id','assign_time','checked','isnew'], {int(company_id):[int(user_id),assign_time,0,0]})
                    
                else:
                    icd_user_id=result['user_id']
                    if icd_user_id==user_id:
                        ret={'res':'失败，该客户已经在你的客户库里','err':'true'}
                    else:
                        ret={'res':'失败，该客户在其他客户库里','err':'true'}
        #记录挑入记录
        if dotype:
            sdotype=dotype[0:3]
            if sdotype!="zsh" and sdotype!="vap":
                sdotype="icd"
        else:
            sdotype='icd'
        gmt_date=getToday()
        sql="select id from kh_gonghai_select where user_id=%s and company_id=%s and dotype=%s and gmt_date=%s"
        result=db.fetchonedb(sql,[user_id,company_id,sdotype,gmt_date])
        if not result:
            sql="insert into kh_gonghai_select (user_id,company_id,dotype,gmt_date) values(%s,%s,%s,%s)"
            db.updatetodb(sql,[user_id,company_id,sdotype,gmt_date])
    else:
        ret={'res':'失败！你还未登录','err':'true'}
    return HttpResponse(simplejson.dumps(ret, ensure_ascii=False))
#主管或管理员分配
def addnew_assign(request):
    username=request.session.get('username',default=None)
    user_id=request.session.get('user_id',default=None)
    if not username or not user_id:
        return HttpResponse(simplejson.dumps({'err':'login'}, ensure_ascii=False))
    has_auth=zzc.is_hasauth(user_id=user_id)
    if str(has_auth)=="0":
        ret={'res':'失败，你没有权限分配客户','err':'false'}
        return simplejson.dumps(ret, ensure_ascii=False)
    companylist=request.GET.getlist('companylist')
    user_id=request.GET.get('user_id')
    dotype=request.GET.get('dotype')
    adminuser_id=request.session.get('user_id',default=None)#销售id
    gmt_created=datetime.datetime.now()
    
    if user_id:
        
        ret={'res':'成功，你已成功放入该客户到库里','err':'false'}
        for company_id in companylist:
            if dotype[0:3]=="vap":
                sql="select id,user_id from kh_assign_vap where company_id=%s"
                result=db.fetchonedb(sql,[company_id])
                if not result:
                    sqlt="insert into kh_assign_vap (company_id,user_id,gmt_created) values(%s,%s,%s)"
                    db.updatetodb(sqlt,[company_id,user_id,gmt_created])
                    ret={'res':'成功，你已成功放入该客户到VAP库里','err':'false'}
                    zzc.updatemodifydata(company_id)
                    savekhlog(company_id,user_id,adminuser_id,'管理员分配到我的VAP客户库')
                    sqld="update kh_income set assigncheck=0 where company_id=%s"
                    db.updatetodb(sqld,[company_id])
                    vap_assign_time=dateall_to_int(gmt_created)
                    updatesearchseek(['vap_user_id','vap_assigncheck','vap_assign_time','vap_isnew'], {int(company_id):[int(user_id),0,vap_assign_time,0]})
                else:
                    aid=result["id"]
                    sqlt="update kh_assign_vap set user_id=%s,isnew=0,gmt_created=%s where id=%s"
                    db.updatetodb(sqlt,[user_id,gmt_created,aid])
                    ret={'res':'成功，你已成功放入该客户到库里','err':'false'}
                    zzc.updatemodifydata(company_id)
                    savekhlog(company_id,user_id,adminuser_id,'管理员分配到我的VAP客户库')
                    sqld="update kh_income set assigncheck=0 where company_id=%s"
                    db.updatetodb(sqld,[company_id])
                    vap_assign_time=dateall_to_int(gmt_created)
                    updatesearchseek(['vap_user_id','vap_assigncheck','vap_assign_time','vap_isnew'], {int(company_id):[int(user_id),0,vap_assign_time,0]})
                    
                    ret={'res':'成功，你已成功放入该客户到库里','err':'false'}
            elif dotype[0:3]=="zsh":
                #是否开通再生汇产品
                zshcheck=zzc.getiszshmember(company_id)
                isassign=1
                if not zshcheck:
                    #在新签库里
                    #管理员分配，新签入公海
                    sql="select id from kh_assign where company_id=%s"
                    result=db.fetchonedb(sql,[company_id])
                    if result:
                        sql="delete from kh_assign where company_id=%s"
                        result=db.updatetodb(sql,[company_id])
                        telflag=0
                        if result:
                            sql="select max(id) as maxid from kh_tel where company_id=%s and telflag=%s"
                            resultm=db.fetchonedb(sql,[company_id,telflag])
                            if resultm:
                                maxtelid=resultm['maxid']
                                sql="insert into kh_droptogonghai(company_id,tel_id,telflag,user_id,gmt_created) values(%s,%s,%s,%s,%s)"
                                db.updatetodb(sql,[company_id,maxtelid,telflag,adminuser_id,gmt_created])
                            zzc.updatemodifydata(company_id)
                            updatesearchseek(['user_id'], {int(company_id):[0]})
                            savekhlog(company_id,user_id,adminuser_id,'管理员放入公海')
                if isassign==1:
                    sql="select id,user_id from kh_assign_zsh where company_id=%s"
                    result=db.fetchonedb(sql,[company_id])
                    if not result:
                        sqlt="insert into kh_assign_zsh (company_id,user_id,gmt_created) values(%s,%s,%s)"
                        db.updatetodb(sqlt,[company_id,user_id,gmt_created])
                        ret={'res':'成功，你已成功放入该客户到再生汇库里','err':'false'}
                        zzc.updatemodifydata(company_id)
                        savekhlog(company_id,user_id,adminuser_id,'管理员分配到我的再生汇客户库')
                        zsh_assign_time=dateall_to_int(gmt_created)
                        updatesearchseek(['zsh_user_id','zsh_assign_time','zsh_isnew'], {int(company_id):[int(user_id),zsh_assign_time,0]})
                    else:
                        aid=result["id"]
                        sqlt="update kh_assign_zsh set user_id=%s,isnew=0,gmt_created=%s where id=%s"
                        db.updatetodb(sqlt,[user_id,gmt_created,aid])
                        ret={'res':'成功，你已成功放入该客户到库里','err':'false'}
                        zzc.updatemodifydata(company_id)
                        savekhlog(company_id,user_id,adminuser_id,'管理员分配到我的再生汇客户库')
                        zsh_assign_time=dateall_to_int(gmt_created)
                        updatesearchseek(['zsh_user_id','zsh_assign_time','zsh_isnew'], {int(company_id):[int(user_id),zsh_assign_time,0]})
                        ret={'res':'成功，你已成功放入该客户到库里','err':'false'}
            else:
                #预录入未审核不能放到我的客户库
                sql="select checked from company where id=%s"
                result=db.fetchonedb(sql,[company_id])
                if result:
                    achecked=result['checked']
                    if str(achecked)=="1":
                        ret={'res':'失败，该客户被其他销售申请并未审核，不能放不我库里','err':'true'}
                        return HttpResponse(simplejson.dumps(ret, ensure_ascii=False))
                #是否开通再生汇产品
                zshcheck=zzc.getiszshmember(company_id)
                isassign=1
                if not zshcheck:
                    #在新签库里就不能分配
                    sql="select id from kh_assign_zsh where company_id=%s"
                    result=db.fetchonedb(sql,[company_id])
                    if result:
                        #在新签库里
                        #管理员分配，新签入公海
                        sql="select id from kh_assign_zsh where company_id=%s"
                        result=db.fetchonedb(sql,[company_id])
                        if result:
                            sql="delete from kh_assign_zsh where company_id=%s"
                            result=db.updatetodb(sql,[company_id])
                            telflag=5
                            if result:
                                sql="select max(id) as maxid from kh_tel where company_id=%s and telflag=%s"
                                resultm=db.fetchonedb(sql,[company_id,telflag])
                                if resultm:
                                    maxtelid=resultm['maxid']
                                    sql="insert into kh_droptogonghai(company_id,tel_id,telflag,user_id,gmt_created) values(%s,%s,%s,%s,%s)"
                                    db.updatetodb(sql,[company_id,maxtelid,telflag,adminuser_id,gmt_created])
                                zzc.updatemodifydata(company_id)
                                updatesearchseek(['zsh_user_id'], {int(company_id):[0]})
                                savekhlog(company_id,user_id,adminuser_id,'管理员放入公海')
                if isassign==1:
                    sql="select id,user_id from kh_assign where company_id=%s"
                    result=db.fetchonedb(sql,[company_id])
                    if not result:
                        sqlt="insert into kh_assign (company_id,user_id,gmt_created) values(%s,%s,%s)"
                        db.updatetodb(sqlt,[company_id,user_id,gmt_created])
                        ret={'res':'成功，你已成功放入该客户到库里','err':'false'}
                        #sp.update("v_compall","company_rt",{'user_id':str(user_id)},int(company_id))
                        zzc.updatemodifydata(company_id)
                        savekhlog(company_id,user_id,adminuser_id,'管理员分配到我的客户库')
                        assign_time=dateall_to_int(gmt_created)
                        #更新申请分配标识
                        sql="update company set checked=0 where id=%s"
                        db.updatetodb(sql,[company_id])
                        updatesearchseek(['user_id','assign_time','checked','isnew'], {int(company_id):[int(user_id),assign_time,0,0]})
                    else:
                        aid=result["id"]
                        sqlt="update kh_assign set user_id=%s,isnew=0,gmt_created=%s where id=%s"
                        db.updatetodb(sqlt,[user_id,gmt_created,aid])
                        
                        zzc.updatemodifydata(company_id)
                        savekhlog(company_id,user_id,adminuser_id,'管理员分配到我的客户库')
                        assign_time=dateall_to_int(gmt_created)
                        #更新申请分配标识
                        sql="update company set checked=0 where id=%s"
                        db.updatetodb(sql,[company_id])
                        updatesearchseek(['user_id','assign_time','checked','isnew'], {int(company_id):[int(user_id),assign_time,0,0]})
                        ret={'res':'成功，你已成功放入该客户到库里','err':'false'}
                        if dotype=="qianbao":
                            sqlt="update kh_company_more set isassgin=1 where company_id=%s"
                            db.updatetodb(sqlt,[company_id])
                            updatesearchseek(['isassgin'], {int(company_id):[1]})
            zzc.updatemodifydata(company_id)
            
            
    else:
        ret={'res':'失败！请选择你要分配的销售人员','err':'true'}
    return HttpResponse(simplejson.dumps(ret, ensure_ascii=False))
#放入公海
def droptogonghai(request):
    username=request.session.get('username',default=None)
    user_id=request.session.get('user_id',default=None)
    if not username or not user_id:
        return HttpResponse(simplejson.dumps({'err':'login'}, ensure_ascii=False))
    companylist=request.GET.getlist('companylist')
    dotype=request.GET.get('dotype')
    if not dotype:
        dotype=''
    has_auth=zzc.is_hasauth(user_id=user_id)
        
    adminuser_id=request.session.get('user_id',default=None)#销售id
    gmt_created=datetime.datetime.now()
    ret={'res':'失败，该客户不在你的库里，或其他错误','err':'true'}
    if companylist:
        for company_id in companylist:
            #管理员放入公海
            if str(has_auth)=="1" and (dotype=="allbm" or dotype=="vap_allbm" or dotype=="zsh_allbm"):
                if dotype[0:3]=="vap":
                    sql="delete from kh_assign_vap where company_id=%s"
                    result=db.updatetodb(sql,[company_id])
                    telflag=4
                elif dotype[0:3]=="zsh":
                    sql="delete from kh_assign_zsh where company_id=%s"
                    result=db.updatetodb(sql,[company_id])
                    telflag=5
                else:
                    sql="delete from kh_assign where company_id=%s"
                    result=db.updatetodb(sql,[company_id])
                    telflag=0
                if result:
                    ret={'res':'成功，你已成功放入该客户到公海','err':'false'}
                    sql="select max(id) as maxid from kh_tel where company_id=%s and telflag=%s"
                    resultm=db.fetchonedb(sql,[company_id,telflag])
                    if resultm:
                        maxtelid=resultm['maxid']
                        sql="insert into kh_droptogonghai(company_id,tel_id,telflag,user_id,gmt_created) values(%s,%s,%s,%s,%s)"
                        db.updatetodb(sql,[company_id,maxtelid,telflag,adminuser_id,gmt_created])
                    
                    zzc.updatemodifydata(company_id)
                    if dotype[0:3]=="vap":
                        updatesearchseek(['vap_user_id'], {int(company_id):[0]})
                    elif dotype[0:3]=="zsh":
                        updatesearchseek(['zsh_user_id'], {int(company_id):[0]})
                    else:
                        updatesearchseek(['user_id'], {int(company_id):[0]})
                    savekhlog(company_id,user_id,adminuser_id,'管理员放入公海')
            else:
                if dotype:
                    ismycompany=zzc.getismycompany(dotype=dotype,company_id=company_id,user_id=user_id)
                if ismycompany:
                    sql="select id from kh_tel where company_id=%s"
                    resultb=db.fetchonedb(sql,[company_id])
                    if not resultb:
                        ret={'res':'失败，新客户请填写小计才可以放公海','err':'true'}
                    else:
                        if dotype[0:3]=="vap":
                            sql="delete from kh_assign_vap where company_id=%s and user_id=%s"
                            result=db.updatetodb(sql,[company_id,adminuser_id])
                            telflag=4
                        elif dotype[0:3]=="zsh":
                            sql="delete from kh_assign_zsh where company_id=%s and user_id=%s"
                            result=db.updatetodb(sql,[company_id,adminuser_id])
                            telflag=5
                        else:
                            sql="delete from kh_assign where company_id=%s and user_id=%s"
                            result=db.updatetodb(sql,[company_id,adminuser_id])
                            telflag=0
                        if result:
                            ret={'res':'成功，你已成功放入该客户到公海','err':'false'}
                            sql="select max(id) as maxid from kh_tel where company_id=%s and telflag=%s"
                            resultm=db.fetchonedb(sql,[company_id,telflag])
                            if resultm:
                                maxtelid=resultm['maxid']
                                sql="insert into kh_droptogonghai(company_id,tel_id,telflag,user_id,gmt_created) values(%s,%s,%s,%s,%s)"
                                db.updatetodb(sql,[company_id,maxtelid,telflag,adminuser_id,gmt_created])
                                
                            
                            zzc.updatemodifydata(company_id)
                            if dotype[0:3]=="vap":
                                updatesearchseek(['vap_user_id'], {int(company_id):[0]})
                            elif dotype[0:3]=="zsh":
                                updatesearchseek(['zsh_user_id'], {int(company_id):[0]})
                            else:
                                updatesearchseek(['user_id'], {int(company_id):[0]})
                            savekhlog(company_id,user_id,adminuser_id,'放入公海')
                else:
                    ret={'res':'失败，该客户不在你的库里，或其他错误','err':'true'}
    return HttpResponse(simplejson.dumps(ret, ensure_ascii=False))
#录入客户审核
def companychecked(request):
    username=request.session.get('username',default=None)
    user_id=request.session.get('user_id',default=None)
    if not username or not user_id:
        return HttpResponse(simplejson.dumps({'err':'login'}, ensure_ascii=False))
    companylist=request.GET.getlist('companylist')
    dotype=request.GET.get('dotype')
    if not dotype:
        dotype=''
    adminuser_id=request.session.get('user_id',default=None)#销售id
    gmt_created=datetime.datetime.now()
    ret={'res':'失败，系统出错','err':'true'}
    if companylist:
        for company_id in companylist:
            user_id=None
            sql="select user_id from company where id=%s"
            result=db.fetchonedb(sql,[company_id])
            if result:
                user_id=result['user_id']
            if user_id:
                #更新申请分配/审核标识
                sql="update company set checked=0 where id=%s"
                result=db.updatetodb(sql,[company_id])
                telflag=0
                if result:
                    if dotype[0:3]=='zsh':
                        ret={'res':'成功，该客户已经分到录入者库里','err':'false'}
                        sql="select id from kh_assign_zsh where company_id=%s"
                        result=db.fetchonedb(sql,[company_id])
                        if not result:
                            sqlt="insert into kh_assign_zsh (company_id,user_id,gmt_created) values(%s,%s,%s)"
                            db.updatetodb(sqlt,[company_id,user_id,gmt_created])
                            ret={'res':'成功，该客户已经分到录入者库里','err':'false'}
                            savekhlog(company_id,user_id,adminuser_id,'分配到我的再生汇客户库')
                            updatesearchseek(['user_id','adminuser_id','checked','zsh_isnew'], {int(company_id):[int(user_id),int(user_id),0,0]})
                        else:
                            savekhlog(company_id,user_id,adminuser_id,'分配到我的客户库')
                            updatesearchseek(['checked'], {int(company_id):[0]})
                            ret={'res':'失败，该客户已经在其他客户库里','err':'true'}
                    else:
                        ret={'res':'成功，该客户已经分到录入者库里','err':'false'}
                        sql="select id from kh_assign where company_id=%s"
                        result=db.fetchonedb(sql,[company_id])
                        if not result:
                            sqlt="insert into kh_assign (company_id,user_id,gmt_created) values(%s,%s,%s)"
                            db.updatetodb(sqlt,[company_id,user_id,gmt_created])
                            ret={'res':'成功，该客户已经分到录入者库里','err':'false'}
                            savekhlog(company_id,user_id,adminuser_id,'分配到我的客户库')
                            updatesearchseek(['user_id','adminuser_id','checked','isnew'], {int(company_id):[int(user_id),int(user_id),0,0]})
                        else:
                            savekhlog(company_id,user_id,adminuser_id,'分配到我的客户库')
                            updatesearchseek(['checked'], {int(company_id):[0]})
                            ret={'res':'失败，该客户已经在其他客户库里','err':'true'}
                    zzc.updatemodifydata(company_id)
            else:
                ret={'res':'失败，该客户录入者不存在！','err':'true'}
    return HttpResponse(simplejson.dumps(ret, ensure_ascii=False))
#预申请分配客户审核
def companysqchecked(request):
    username=request.session.get('username',default=None)
    user_id=request.session.get('user_id',default=None)
    if not username or not user_id:
        return HttpResponse(simplejson.dumps({'err':'login'}, ensure_ascii=False))
    companylist=request.GET.getlist('companylist')
    dotype=request.GET.get('dotype')
    if not dotype:
        dotype=''
    adminuser_id=request.session.get('user_id',default=None)#销售id
    gmt_created=datetime.datetime.now()
    ret={'res':'失败，系统出错','err':'true'}
    if companylist:
        for company_id in companylist:
            user_id=None
            sql="select user_id from kh_assign_request where company_id=%s"
            result=db.fetchonedb(sql,[company_id])
            if result:
                user_id=result['user_id']
            if user_id:
                #更新申请分配/审核标识
                sql="update company set checked=0 where id=%s"
                result=db.updatetodb(sql,[company_id])
                telflag=0
                if result:
                    if dotype[0:3]=='zsh':
                        ret={'res':'成功，该客户已经分到申请者库里','err':'false'}
                        sql="select id from kh_assign_zsh where company_id=%s"
                        result=db.fetchonedb(sql,[company_id])
                        if not result:
                            sqlt="insert into kh_assign_zsh (company_id,user_id,gmt_created) values(%s,%s,%s)"
                            db.updatetodb(sqlt,[company_id,user_id,gmt_created])
                            ret={'res':'成功，该客户已经分到申请者库里','err':'false'}
                            savekhlog(company_id,user_id,adminuser_id,'分配到我的客户库')
                            updatesearchseek(['user_id','checked','zsh_isnew'], {int(company_id):[int(user_id),0,0]})
                        else:
                            savekhlog(company_id,user_id,adminuser_id,'分配到我的客户库')
                            updatesearchseek(['checked'], {int(company_id):[0]})
                            ret={'res':'失败，该客户已经在其他客户库里','err':'true'}
                    else:
                        ret={'res':'成功，该客户已经分到申请者库里','err':'false'}
                        sql="select id from kh_assign where company_id=%s"
                        result=db.fetchonedb(sql,[company_id])
                        if not result:
                            sqlt="insert into kh_assign (company_id,user_id,gmt_created) values(%s,%s,%s)"
                            db.updatetodb(sqlt,[company_id,user_id,gmt_created])
                            ret={'res':'成功，该客户已经分到申请者库里','err':'false'}
                            savekhlog(company_id,user_id,adminuser_id,'分配到我的客户库')
                            updatesearchseek(['user_id','checked','isnew'], {int(company_id):[int(user_id),0,0]})
                        else:
                            savekhlog(company_id,user_id,adminuser_id,'分配到我的客户库')
                            updatesearchseek(['checked'], {int(company_id):[0]})
                            ret={'res':'失败，该客户已经在其他客户库里','err':'true'}
                    zzc.updatemodifydata(company_id)
            else:
                #更新申请分配/审核标识
                sql="update company set checked=0 where id=%s"
                result=db.updatetodb(sql,[company_id])
                updatesearchseek(['checked'], {int(company_id):[0]})
                zzc.updatemodifydata(company_id)
                ret={'res':'失败，该客户申请者不存在！'+str(user_id),'err':'true'}
    return HttpResponse(simplejson.dumps(ret, ensure_ascii=False))
#该公司详情
def crm_cominfoedit(request):
    request_url=request.META.get('HTTP_REFERER','/')
    username=request.session.get('username',default=None)
    user_id=request.session.get('user_id',default=None)
    gmt_created=formattime(datetime.datetime.now())
    if not username or not user_id:
        return HttpResponseRedirect("relogin.html")
    company_id=request.GET.get('company_id')
    dotype=request.GET.get('dotype')
    isvap=None
    iszsh=None
    telflag=0
    if not dotype:
        return HttpResponse("参数错误！")
    if dotype[0:3]=="vap":
        isvap=1
        telflag=4
    if dotype[0:3]=="zsh":
        iszsh=1
        telflag=5
    #用户部门
    partcode=zzc.getuserpart(user_id=user_id)
    #用户级别
    authlist=zzc.geauthid(user_id=user_id)
    #是否管理员
    isadmin=None
    if "1" in authlist:
        isadmin=1
    #是否主管
    iszhuguan=None
    has_auth=zzc.is_hasauth(user_id=user_id)
    if str(has_auth)=="1":
        iszhuguan=1
    #非管理员非续签部门
    if str(partcode)=='24' or iszhuguan:
        a=0
    else:
        if not isadmin:
            #是否再生汇客户
            zshcheck=zzc.getiszshmember(company_id)
            vapcheck=zzc.getispaymember(company_id)
            if iszsh:
                if not zshcheck and not vapcheck:
                    sql="select a.id from kh_assign as a where a.company_id=%s"
                    result=db.fetchonedb(sql,[company_id])
                    if result:
                        return HttpResponse("该客户新签客户库，你不能操作查看！")
            elif isvap:
                if not zshcheck and not vapcheck:
                    return HttpResponse("该客户不是付费客户，你不能操作！")
            else:
                if vapcheck:
                    return HttpResponse("该客户已经转到VAP客户库，新签不能打开！"+str(partcode))
                if not zshcheck:
                    sql="select a.id from kh_assign_zsh as a where a.company_id=%s"
                    result=db.fetchonedb(sql,[company_id])
                    if result:
                        return HttpResponse("该客户再生汇客户库，你不能操作查看！")
    
    ismycompany=zzc.getismycompany(dotype=dotype,company_id=company_id,user_id=user_id)
    if not ismycompany:
        ismycompany=0
    if not isadmin:
        #是否我部门客户
        ismysee=zzc.getismysee(dotype=dotype,company_id=company_id,user_id=user_id)
        if not ismysee:
            if iszhuguan:
                ismysee=0
            else:
                return HttpResponse("你没有权限查看该信息！")
    
    companyinfo=zzc.getcompanyinfo(company_id=company_id,user_id=user_id)
    if not companyinfo:
        telflag=0
        sql="delete from kh_assign where company_id=%s"
        result=db.updatetodb(sql,[company_id])
        if result:
            adminuser_id=0
            zzc.updatemodifydata(company_id)
            updatesearchseek(['user_id'], {int(company_id):[0]})
            savekhlog(company_id,user_id,adminuser_id,'放入公海')
        return HttpResponse("该用户数据问题，系统已经自动放入公海！")
    if isvap:
        companyinfo['emphases']=companyinfo['vap_emphases']
    if iszsh:
        companyinfo['emphases']=companyinfo['zsh_emphases']
    com_rank=''
    if isvap:
        sql='select rank from kh_sales_vap where company_id=%s'
        result=db.fetchonedb(sql,[company_id])
        if result:
            com_rank=result['rank']
    elif iszsh:
        sql='select rank from kh_sales_zsh where company_id=%s'
        result=db.fetchonedb(sql,[company_id])
        if result:
            com_rank=result['rank']
    else:
        sql='select rank from kh_sales where company_id=%s'
        result=db.fetchonedb(sql,[company_id])
        if result:
            com_rank=result['rank']
    business_type=companyinfo.get('business_type')
    if not business_type:
        companyinfo['business_type']="0"
    #客户冲突
    searchlist={}
    ctmobile=""
    #撞单客户
    companyinfo['mobile']
    if (companyinfo.has_key("mobile")):
        ctmobile=ctmobile+companyinfo['mobile']
    if (companyinfo.has_key("tel")) and (companyinfo.has_key("mobile")):
        cttel=companyinfo['tel']
        if cttel:
            ctmobile=ctmobile+"|"+cttel
    if (companyinfo.has_key("tel")) and (not companyinfo.has_key("mobile")):
        cttel=companyinfo['tel']
        if cttel:
            ctmobile=ctmobile+cttel
    
    otherpersonlist=zzc.getotherperson(company_id=company_id,my_user_id=user_id)
    if otherpersonlist:
        for m in otherpersonlist:
            ccmobile=m['mobile']
            if ccmobile:
                ctmobile=ctmobile+"|"+ccmobile
    if ctmobile[0:1]=="|":
        ctmobile=ctmobile[1:len(ctmobile)]
    if ctmobile:
        ctmobile=ctmobile.replace("-", '')
    searchlist['mobile']=ctmobile
    searchlist['dotype']='allall'
    searchlist['company_id']=company_id
    ctcompanylist=zzc.get_allcustomer(frompageCount=0,limitNum=50,searchlist=searchlist)
    ctcompanylist['listcount']=ctcompanylist['listcount']-1

    provincelist=zzc.getprovincelist()
    guowaiprovincelist=zzc.getguowailist()
    #获得额外联系人
    
    viptype=companyinfo['membership_code']
    #会员判断
    arrviptype={'vipname':'','vipsubname':'','vipcheck':'','ldb':''}
    if (viptype == '10051000'):
        arrviptype['vipname']='普通会员'
    if (viptype == '10051001'):
        arrviptype['vipname']='再生通'
    if (viptype == '100510021000'):
        arrviptype['vipname']='银牌品牌通'
    if (viptype == '100510021001'):
        arrviptype['vipname']='金牌品牌通'
    if (viptype == '100510021002'):
        arrviptype['vipname']='钻石品牌通'
    if (viptype == '10051000'):
        arrviptype['vipcheck']=None
    else:
        arrviptype['vipcheck']=1
    #来电宝客户
    sqll="select id from crm_company_service where company_id=%s and crm_service_code in ('1007','1008','1009','1010','1011') and apply_status=1"
    ldbresult=db.fetchonedb(sqll,[company_id])
    if ldbresult:
        sqlg="select front_tel from phone where company_id=%s"
        phoneresult=db.fetchonedb(sqlg,[company_id])
        if phoneresult:
            arrviptype['ldb']={'ldbphone':phoneresult['front_tel']}
        else:
            arrviptype['ldb']=None
    else:
        arrviptype['ldb']=None
    arrviptype['vipsubname'] = companyinfo['domain_zz91']
    
    sql="select id from crm_company_service where company_id=%s and crm_service_code='10001002'"
    result=db.fetchonedb(sql,[company_id])
    if result:
        loginflag=1
        sql="select id from crm_company_service where company_id=%s and crm_service_code in ('1000','1008','1009','1010','10001003','10001004','10001005','1011') and apply_status=1"
        resultl=db.fetchonedb(sql,[company_id])
        if resultl:
            loginflag=None
    #钱包余额
    fee=zzc.getqianbaoblance(company_id)
    isweixin=zzc.gethaveinstallweixin(company_id)
    isapp=zzc.gethaveinstallapp(company_id)
    
    #是否充值成功
    sql="select iszhifu from kh_company_more where company_id=%s"
    resultl=db.fetchonedb(sql,[company_id])
    if resultl:
        iszhifu=resultl['iszhifu']
        if iszhifu==1:
            iszhifu=1
        else:
            iszhifu=None
    
    if not companyinfo:
        return HttpResponse("err")
    else:
        return render_to_response("icdhtml/crm_cominfoedit.html",locals())
#保存公司详情
def save_crm_cominfoedit(request):
    username=request.session.get('username',default=None)
    user_id=request.session.get('user_id',default=None)
    if not username or not user_id:
        return HttpResponse(simplejson.dumps({'err':'login'}, ensure_ascii=False))
    company_id=request.POST.get("company_id")
    dotype=request.POST.get("dotype")
    if not dotype:
        dotype=''
    #公司信息
    company_name=request.POST.get("company_name")
    address=request.POST.get("address")
    address_zip=request.POST.get("address_zip")
    website=request.POST.get("website")
    industry_code=request.POST.get("industry_code")
    service_code=request.POST.get("service_code")
    introduction=request.POST.get("introduction")
    business=request.POST.get("business")
    business_type=request.POST.get("business_type")#主营方向
    sale_details=request.POST.get("sale_details")
    buy_details=request.POST.get("buy_details")
    area_code=request.POST.get("area_code")
    #账户信息
    tel_country_code=request.POST.get("tel_country_code")
    tel_area_code=request.POST.get("tel_area_code")
    tel=request.POST.get("tel")
    mobile=request.POST.get("mobile")
    contact=request.POST.get("contact")
    position=request.POST.get("position")
    sex=request.POST.get("sex")
    email=request.POST.get("email")
    fax_country_code=request.POST.get("fax_country_code")
    fax_area_code=request.POST.get("fax_area_code")
    fax=request.POST.get("fax")
    rubbish=request.POST.get("rubbish")
    
    emphases=request.POST.get("emphases")
    islaji=request.POST.get("islaji")
    if not emphases:
        emphases=0
    if not islaji:
        islaji=0
    isdeath=request.POST.get("isdeath")
    if not isdeath:
        isdeath=0
    
    
    sql1="update company set name=%s,area_code=%s,address=%s,address_zip=%s,website=%s,industry_code=%s,service_code=%s,introduction=%s,business=%s,business_type=%s,sale_details=%s,buy_details=%s,rubbish=%s,islaji=%s,isdeath=%s where id=%s"
    db.updatetodb(sql1,[company_name,area_code,address,address_zip,website,industry_code,service_code,introduction,business,business_type,sale_details,buy_details,rubbish,islaji,isdeath,company_id])
    sql2="update company_account set tel_country_code=%s,tel_area_code=%s,tel=%s,mobile=%s,contact=%s,position=%s,sex=%s,email=%s,fax_country_code=%s,fax_area_code=%s,fax=%s where company_id=%s"
    db.updatetodb(sql2, [tel_country_code,tel_area_code,tel,mobile,contact,position,sex,email,fax_country_code,fax_area_code,fax,company_id])
    if user_id:
        if dotype[0:3]=="vap":
            sql="update kh_assign_vap set emphases=%s where company_id=%s and user_id=%s"
            db.updatetodb(sql,[emphases,company_id,user_id])
            updatesearchseek(['vap_emphases','islaji','isdeath'], {int(company_id):[int(emphases),int(islaji),int(isdeath)]})
        elif dotype[0:3]=="zsh":
            sql="update kh_assign_zsh set emphases=%s where company_id=%s and user_id=%s"
            db.updatetodb(sql,[emphases,company_id,user_id])
            updatesearchseek(['zsh_emphases','islaji','isdeath'], {int(company_id):[int(emphases),int(islaji),int(isdeath)]})
        else:
            sql="update kh_assign set emphases=%s where company_id=%s and user_id=%s"
            db.updatetodb(sql,[emphases,company_id,user_id])
            updatesearchseek(['emphases','islaji','isdeath'], {int(company_id):[int(emphases),int(islaji),int(isdeath)]})
    zzc.updatemodifydata(company_id)
    res={'err':'false'}
    #updatesearchseek([['compname','area_code','address','industry_code','service_code','business','sale_details','buy_details','rubbish','emphases']], {int(company_id):[company_name,area_code,address,industry_code,service_code,business,sale_details,buy_details,rubbish,emphases]})
    res=simplejson.dumps(res, ensure_ascii=False)
    return HttpResponse(res)
#设置为重点客户
def set_emphases(request):
    username=request.session.get('username',default=None)
    user_id=request.session.get('user_id',default=None)
    if not username or not user_id:
        return HttpResponse(simplejson.dumps({'err':'login'}, ensure_ascii=False))
    company_id=request.POST.get("company_id")
    #ispay=zzc.getispaymember(company_id)
    ispay=None
    iszsh=None
    emphases=request.POST.get("emphases")
    dotype=request.POST.get("dotype")
    if dotype:
        if dotype[0:3]=="vap":
            ispay=1
        elif dotype[0:3]=="zsh":
            iszsh=1
    if ispay:
        sql="update kh_assign_vap set emphases=%s where company_id=%s and user_id=%s"
        db.updatetodb(sql,[emphases,company_id,user_id])
        updatesearchseek(['vap_emphases'], {int(company_id):[int(emphases)]})
    elif iszsh:
        sql="update kh_assign_zsh set emphases=%s where company_id=%s and user_id=%s"
        db.updatetodb(sql,[emphases,company_id,user_id])
        updatesearchseek(['zsh_emphases'], {int(company_id):[int(emphases)]})
    else:
        sql="update kh_assign set emphases=%s where company_id=%s and user_id=%s"
        db.updatetodb(sql,[emphases,company_id,user_id])
        updatesearchseek(['emphases'], {int(company_id):[int(emphases)]})
    zzc.updatemodifydata(company_id)
    if (emphases==1):
        res={'err':'false','res':'成功！已设置为重点客户！'}
    else:
        res={'err':'false','res':'成功！已经取消设置为重点客户'}
    res=simplejson.dumps(res, ensure_ascii=False)
    return HttpResponse(res)
#转4、5星客户统计
def tj_changestar(request):
    username=request.session.get('username',default=None)
    user_id=request.session.get('user_id',default=None)
    today=formattime(getToday(),1)
    fromdate=request.GET.get('fromdate')
    todate=request.GET.get('todate')
    if not fromdate:
        fromdate=today
    if not todate:
        todate=today
        todate=formattime(getnextdate(todate),1)
    if not username or not user_id:
        return simplejson.dumps({'err':'login'}, ensure_ascii=False)
    allsalesman=zzc.get_allsalesman(user_id=user_id)
    return render_to_response("icdhtml/tj_changestar.html",locals())
#再生汇转4、5星客户统计
def tj_changestarzsh(request):
    username=request.session.get('username',default=None)
    user_id=request.session.get('user_id',default=None)
    today=formattime(getToday(),1)
    fromdate=request.GET.get('fromdate')
    todate=request.GET.get('todate')
    if not fromdate:
        fromdate=today
    if not todate:
        todate=today
        todate=formattime(getnextdate(todate),1)
    if not username or not user_id:
        return simplejson.dumps({'err':'login'}, ensure_ascii=False)
    allsalesman=zzc.get_allsalesman(user_id=user_id,zsh=1)
    return render_to_response("icdhtml/tj_changestarzsh.html",locals())
#转4、5星客户统计
def tj_changestarvap(request):
    username=request.session.get('username',default=None)
    user_id=request.session.get('user_id',default=None)
    today=formattime(getToday(),1)
    fromdate=request.GET.get('fromdate')
    todate=request.GET.get('todate')
    if not fromdate:
        fromdate=today
    if not todate:
        todate=today
        todate=formattime(getnextdate(todate),1)
    if not username or not user_id:
        return simplejson.dumps({'err':'login'}, ensure_ascii=False)
    allsalesman=zzc.get_allsalesman(user_id=user_id,vap=1)
    return render_to_response("icdhtml/tj_changestarvap.html",locals())

#联系量统计
def tj_contact(request):
    username=request.session.get('username',default=None)
    user_id=request.session.get('user_id',default=None)
    today=formattime(getToday(),1)
    fromdate=request.GET.get('fromdate')
    todate=request.GET.get('todate')
    if not fromdate:
        fromdate=today
    if not todate:
        todate=today
        todate=formattime(getnextdate(todate),1)
    if not username or not user_id:
        return simplejson.dumps({'err':'login'}, ensure_ascii=False)
    allsalesman=zzc.get_allsalesman(user_id=user_id)
    return render_to_response("icdhtml/tj_contact.html",locals())

#联系量统计VAP
def tj_contactvap(request):
    username=request.session.get('username',default=None)
    user_id=request.session.get('user_id',default=None)
    today=formattime(getToday(),1)
    fromdate=request.GET.get('fromdate')
    todate=request.GET.get('todate')
    if not fromdate:
        fromdate=today
    if not todate:
        todate=today
        todate=formattime(getnextdate(todate),1)
    if not username or not user_id:
        return simplejson.dumps({'err':'login'}, ensure_ascii=False)
    allsalesman=zzc.get_allsalesman(user_id=user_id,vap=1)
    return render_to_response("icdhtml/tj_contactvap.html",locals())
#再生汇联系量统计
def tj_contactzsh(request):
    username=request.session.get('username',default=None)
    user_id=request.session.get('user_id',default=None)
    today=formattime(getToday(),1)
    fromdate=request.GET.get('fromdate')
    todate=request.GET.get('todate')
    if not fromdate:
        fromdate=today
    if not todate:
        todate=today
        todate=formattime(getnextdate(todate),1)
    if not username or not user_id:
        return simplejson.dumps({'err':'login'}, ensure_ascii=False)
    allsalesman=zzc.get_allsalesman(user_id=user_id,zsh=1)
    return render_to_response("icdhtml/tj_contactzsh.html",locals())
def tj_company(request):
    username=request.session.get('username',default=None)
    user_id=request.session.get('user_id',default=None)
    today=formattime(getToday(),1)
    fromdate=request.GET.get('fromdate')
    todate=request.GET.get('todate')
    if not fromdate:
        fromdate=today
    if not todate:
        todate=today
        todate=formattime(getnextdate(todate),1)
    if not username or not user_id:
        return simplejson.dumps({'err':'login'}, ensure_ascii=False)
    allsalesman=zzc.get_allsalesman(user_id=user_id)
    return render_to_response("icdhtml/tj_company.html",locals())
def tj_companyzsh(request):
    username=request.session.get('username',default=None)
    user_id=request.session.get('user_id',default=None)
    today=formattime(getToday(),1)
    fromdate=request.GET.get('fromdate')
    todate=request.GET.get('todate')
    if not fromdate:
        fromdate=today
    if not todate:
        todate=today
        todate=formattime(getnextdate(todate),1)
    if not username or not user_id:
        return simplejson.dumps({'err':'login'}, ensure_ascii=False)
    allsalesman=zzc.get_allsalesman(user_id=user_id,zsh=1)
    return render_to_response("icdhtml/tj_companyzsh.html",locals())
def tj_companyvap(request):
    username=request.session.get('username',default=None)
    user_id=request.session.get('user_id',default=None)
    today=formattime(getToday(),1)
    fromdate=request.GET.get('fromdate')
    todate=request.GET.get('todate')
    if not fromdate:
        fromdate=today
    if not todate:
        todate=today
        todate=formattime(getnextdate(todate),1)
    if not username or not user_id:
        return simplejson.dumps({'err':'login'}, ensure_ascii=False)
    allsalesman=zzc.get_allsalesman(user_id=user_id,vap=1)
    return render_to_response("icdhtml/tj_companyvap.html",locals())
#客户数统计
def tj_companyvalue(request):
    user_id=request.GET.get('user_id')
    rank=request.GET.get('rank')
    nocontact=request.GET.get('nocontact')
    gendiu=request.GET.get('gendiu')
    user_category_code=request.GET.get('user_category_code')
    vapflag=request.GET.get('vapflag')
    iszsh=request.GET.get('iszsh')
    if user_category_code=="0":
        tcount=0
    else:
        tcount=zzc.get_tongjicompany(user_id=user_id,rank=rank,nocontact=nocontact,gendiu=gendiu,user_category_code=user_category_code,vapflag=vapflag,iszsh=iszsh)
    tj={'count':tcount}
    res=simplejson.dumps(tj, ensure_ascii=False)
    return HttpResponse(res)
#转4星客户统计
def tj_changestarvalue(request):
    user_id=request.GET.get('user_id')
    rank=request.GET.get('rank')
    telflag=request.GET.get('telflag')
    income=request.GET.get('income')
    fromdate=request.GET.get('fromdate')
    todate=request.GET.get('todate')
    tcount=zzc.get_tongjichangestar(user_id=user_id,rank=rank,telflag=telflag,income=income,fromdate=fromdate,todate=todate)
    tj={'count':tcount}
    res=simplejson.dumps(tj, ensure_ascii=False)
    return HttpResponse(res)
#公司数据
def tj_companylist(request):
    user_id=request.GET.get('user_id')
    rank=request.GET.get('rank')
    nocontact=request.GET.get('nocontact')
    gendiu=request.GET.get('gendiu')
    user_category_code=request.GET.get('user_category_code')
    vapflag=request.GET.get('vapflag')
    iszsh=request.GET.get('iszsh')
    gonghai=request.GET.get('gonghai')
    fromdate=request.GET.get('fromdate')
    todate=request.GET.get('todate')
    page=request.GET.get('page')
    dotype=request.GET.get('dotype')
    
    if not page:
        page=1
    searchlist={}
    if user_id:
        searchlist['user_id']=user_id
    if rank:
        searchlist['rank']=rank
    if nocontact:
        searchlist['nocontact']=nocontact
    if gendiu:
        searchlist['gendiu']=gendiu
    if user_category_code:
        searchlist['user_category_code']=user_category_code
    if vapflag:
        searchlist['vapflag']=vapflag
    if gonghai:
        searchlist['gonghai']=gonghai
    if iszsh:
        searchlist['iszsh']=iszsh
    if fromdate:
        searchlist['fromdate']=fromdate
    if todate:
        searchlist['todate']=todate
    if dotype:
        searchlist['dotype']=dotype
    
    searchurl=urllib.urlencode(searchlist)
    funpage=zz91page()
    limitNum=funpage.limitNum(10)
    nowpage=funpage.nowpage(int(page))
    frompageCount=funpage.frompageCount()
    after_range_num = funpage.after_range_num(3)
    before_range_num = funpage.before_range_num(6)
    if gonghai:
        listall=zzc.get_tongjigonghailist(frompageCount=frompageCount,limitNum=limitNum,user_id=user_id,dotype=dotype,fromdate=fromdate,todate=todate)
    else:
        listall=zzc.get_tongjicompanylist(frompageCount,limitNum,user_id=user_id,rank=rank,nocontact=nocontact,gendiu=gendiu,user_category_code=user_category_code,vapflag=vapflag,iszsh=iszsh)
    listcount=listall['listcount']
    listall=listall['listall']
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
    
    return render_to_response("icdhtml/tj_companylist.html",locals())
#转4、5星客户公司数据
def tj_changestarlist(request):
    user_id=request.GET.get('user_id')
    rank=request.GET.get('rank')
    page=request.GET.get('page')
    
    telflag=request.GET.get('telflag')
    income=request.GET.get('income')
    fromdate=request.GET.get('fromdate')
    todate=request.GET.get('todate')
    vapflag=request.GET.get('vapflag')
    
    if not page:
        page=1
    searchlist={}
    if user_id:
        searchlist['user_id']=user_id
    if rank:
        searchlist['rank']=rank
    if telflag:
        searchlist['telflag']=telflag
    if income:
        searchlist['income']=income
    if fromdate:
        searchlist['fromdate']=fromdate
    if todate:
        searchlist['todate']=todate
    
    searchurl=urllib.urlencode(searchlist)
    funpage=zz91page()
    limitNum=funpage.limitNum(10)
    nowpage=funpage.nowpage(int(page))
    frompageCount=funpage.frompageCount()
    after_range_num = funpage.after_range_num(3)
    before_range_num = funpage.before_range_num(6)
    
    listall=zzc.get_tongjichangestarlist(frompageCount,limitNum,user_id=user_id,rank=rank,telflag=telflag,income=income,fromdate=fromdate,todate=todate)
    listcount=listall['listcount']
    listall=listall['listall']
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
    
    return render_to_response("icdhtml/tj_companylist.html",locals())
#联系量数据
def tj_contactvalue(request):
    user_id=request.GET.get('user_id')
    rank=request.GET.get('rank')
    contacttype=request.GET.get('contacttype')
    telflag=request.GET.get('telflag')
    today=formattime(getToday(),1)
    fromdate=request.GET.get('fromdate')
    todate=request.GET.get('todate')
    teltags=request.GET.get('teltags')
    tomorow=request.GET.get('tomorow')
    gonghai=request.GET.get('gonghai')
    dotype=request.GET.get('dotype')
    if not fromdate:
        fromdate=today
    if not todate:
        todate=today
        todate=formattime(getnextdate(todate),1)
    
    tcount=zzc.get_tongjicontact(user_id=user_id,rank=rank,contacttype=contacttype,telflag=telflag,fromdate=fromdate,todate=todate,teltags=teltags,tomorow=tomorow,gonghai=gonghai,dotype=dotype)
    tj={'count':tcount}
    res=simplejson.dumps(tj, ensure_ascii=False)
    return HttpResponse(res)
#联系量列表
def tj_contactlist(request):
    user_id=request.GET.get('user_id')
    rank=request.GET.get('rank')
    contacttype=request.GET.get('contacttype')
    telflag=request.GET.get('telflag')
    today=formattime(getToday(),1)
    fromdate=request.GET.get('fromdate')
    todate=request.GET.get('todate')
    teltags=request.GET.get('teltags')
    tomorow=request.GET.get('tomorow')
    gonghai=request.GET.get('gonghai')
    if gonghai:
        return tj_companylist(request)
    if not fromdate:
        fromdate=today
    if not todate:
        todate=today
        todate=formattime(getnextdate(todate),1)
    page=request.GET.get('page')
    if not page:
        page=1
    searchlist={}
    if user_id:
        searchlist['user_id']=user_id
    if rank:
        searchlist['rank']=rank
    if contacttype:
        searchlist['contacttype']=contacttype
    if telflag:
        searchlist['telflag']=telflag
    if fromdate:
        searchlist['fromdate']=fromdate
    if todate:
        searchlist['todate']=todate
    if teltags:
        searchlist['teltags']=teltags
    if tomorow:
        searchlist['tomorow']=tomorow
    
    searchurl=urllib.urlencode(searchlist)
    funpage=zz91page()
    limitNum=funpage.limitNum(10)
    nowpage=funpage.nowpage(int(page))
    frompageCount=funpage.frompageCount()
    after_range_num = funpage.after_range_num(3)
    before_range_num = funpage.before_range_num(6)
    
    tjlistall=zzc.get_tongjicontactlist(frompageCount,limitNum,user_id=user_id,rank=rank,contacttype=contacttype,telflag=telflag,fromdate=fromdate,todate=todate,teltags=teltags,tomorow=tomorow)
    listcount=tjlistall['count']
    listall=tjlistall['list']
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
    
    return render_to_response("icdhtml/tj_contactlist.html",locals())
#开通单列表
def orderlist(request):
    username=request.session.get('username',default=None)
    user_id=request.session.get('user_id',default=None)
    if not username or not user_id:
        return HttpResponse(simplejson.dumps({'err':'login'}, ensure_ascii=False))
    #用户级别
    authlist=zzc.geauthid(user_id=user_id)
    #是否管理员
    isadmin=None
    if "1" in authlist:
        isadmin=1
    user_category_code=request.GET.get('user_category_code')
    douser_id=request.GET.get('douser_id')
    account=request.GET.get('account')
    mobile=request.GET.get('mobile')
    allsalesman=zzc.get_allsalesman(user_id=user_id)
    
    today=formattime(getToday(),1)
    fromdate=request.GET.get('fromdate')
    todate=request.GET.get('todate')
    service_type=request.GET.get('service_type1')
    customType=request.GET.get('customType')
    sales_priceflag=request.GET.get('sales_priceflag')
    """
    if not fromdate:
        fromdate=today
    if not todate:
        todate=today
        todate=formattime(getnextdate(todate),1)
    """
        
    page=request.GET.get('page')
    if not page:
        page=1
    searchlist={}
    if douser_id:
        searchlist['douser_id']=douser_id
    if user_category_code:
        searchlist['user_category_code']=user_category_code
    if account:
        searchlist['account']=account
    if mobile:
        searchlist['mobile']=mobile
    if fromdate:
        searchlist['fromdate']=fromdate
    if todate:
        searchlist['todate']=todate
    if service_type:
        searchlist['service_type']=service_type
    if customType:
        searchlist['customType']=customType
    if sales_priceflag:
        searchlist['sales_priceflag']=sales_priceflag
    
    searchurl=urllib.urlencode(searchlist)
    funpage=zz91page()
    limitNum=funpage.limitNum(10)
    nowpage=funpage.nowpage(int(page))
    frompageCount=funpage.frompageCount()
    after_range_num = funpage.after_range_num(3)
    before_range_num = funpage.before_range_num(6)
    
    listalll=zzc.getorderlist(frompageCount,limitNum,searchlist=searchlist)
    listcount=listalll['count']
    listall=listalll['list']
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
    return render_to_response("icdhtml/orderlist.html",locals())

def ordercompany(request):
    company_id= request.GET.get("company_id")
    if company_id:
        searchlist={}
        searchlist['company_id']=company_id
        searchurl=urllib.urlencode(searchlist)
        frompageCount=0
        limitNum=20
        listall=zzc.getorderlist(frompageCount,limitNum,searchlist=searchlist)
        listcount=listall['count']
        listall=listall['list']
        return render_to_response("icdhtml/ordercompany.html",locals())
#销售开通单
def order(request):
    username=request.session.get('username',default=None)
    user_id=request.session.get('user_id',default=None)
    if not username or not user_id:
        return HttpResponse(simplejson.dumps({'err':'login'}, ensure_ascii=False))
    company_id= request.GET.get("company_id")
    mbflag=request.GET.get("mbflag")
    dotype=request.GET.get("dotype")
    if not mbflag:
        if dotype:
            if dotype[0:3]=="vap":
                mbflag="1"
            else:
                mbflag="2"
    mbflag=str(mbflag)
    if company_id:
        account=""
        sql="select account,contact,mobile from company_account where company_id=%s"
        result=db.fetchonedb(sql,[company_id])
        if result:
            account=result['account']
            com_contactperson=result['contact']
            com_mobile=result['mobile']
        if not account:
            return HttpResponse("该公司账号不存在！")
    else:
        return HttpResponse("错误！")
    
    allsalesman=zzc.get_allsalesman(user_id=user_id)
    
    
    
    service_type1=['再生通','品牌通','展会产品','广告','线下纸媒','百度优化','移动生意管家','国际站','终身服务','商铺服务','诚信会员','定金','微站','来电宝五元','来电宝免月租','来电宝按通','首页直达广告','企业秀','其他']
    service_type2=['再生通','品牌通','展会产品','广告','黄页','展会广告','百度优化','移动生意管家','终身服务','商铺服务','诚信会员','定金','微站','来电宝五元','来电宝免月租','来电宝按通','首页直达广告','企业秀','其他']
    service_type3=['再生通续费','再生通','品牌通续费','展会产品','百度优化','移动生意管家','广告续费','终身服务','商铺服务','诚信会员','定金','微站','来电宝五元','来电宝免月租','来电宝按通','首页直达广告','企业秀','其他']
    
    servicetype=service_type1
    if mbflag=="1":
        servicetype=service_type1
    if mbflag=="2":
        servicetype=service_type2
    if mbflag=="3":
        servicetype=service_type3
    
    typelist=[]
    n=0
    for list in servicetype:
        l={'name':list,'n':n}
        n+=1
        typelist.append(l)
        
    
    """
    if mbflag=="1":
        return render_to_response("icdhtml/order1.html",locals())
    if mbflag=="2":
        return render_to_response("icdhtml/order2.html",locals())
    if mbflag=="3":
        return render_to_response("icdhtml/order3.html",locals())
    """
    return render_to_response("icdhtml/order.html",locals())
def ordersave(request):
    dbserver = crmdb(dbtype="server")
    company_id=request.POST.get("company_id")
    user_id = request.POST.get("user_id")
    mtemplates = request.POST.get("templates")
    service_type1 = str(request.POST.get("service_type1"))
    gmt_income=paytime = request.POST.get("paytime")
    user_category_code=request.POST.get("user_category_code")
    
    account=request.POST.get("account")
    amount= payMoney = str(request.POST.get("payMoney"))+'00'
    sale_staff=saler=zzc.get_username(user_id)
    
    adkeywords = request.POST.get("adkeywords")
    adfromdate = request.POST.get("adfromdate")
    adtodate = request.POST.get("adtodate")
    adcontent = request.POST.get("adcontent")
    remark = request.POST.get("remark")
    gmt_created=datetime.datetime.now()
    gmt_modified=datetime.datetime.now()
    gmt_date=gmt_created.strftime('%Y-%m-%d')
    mbradio = request.POST.get("mbradio")
    qiyexiu = request.POST.get("qiyexiu")
    remark="服务：广告关键字："+adkeywords+"|开始时间："+adfromdate+"|结束时间："+adtodate+"|广告内容："+adcontent+"|备注："+remark
    #servicestr=request.REQUEST.getlist("service_type2")
    servicestr=request.POST.get("service_type2")
    if servicestr:
        servicestr=servicestr.split(",")
    else:
        servicestr=[]
    order_nostr=""
    for t in servicestr:
        if t:
            apply_group=random.randrange(0,1000000000)
            apply_groupstr=str(apply_group)+"|"
            order_no=str(gmt_income)+str(mbradio)+str(t)+str(company_id)+str(account)
            order_no = hashlib.md5(str(order_no))
            order_no = order_no.hexdigest()
            order_nostr=order_nostr+order_no+"|"
            #判断订单是否已经申请
            errflag=0
            #续费会员，获取过期时间
            end_time=''
            arrservice=t.split("|")
            if arrservice:
                if len(arrservice)>0:
                    service_type=arrservice[0]
                    
                if len(arrservice)>1:
                    end_time=arrservice[1]
            #来电宝客户获取余额
            arrservice=t.split("*")
            ldbblance=""
            if arrservice:
                if len(arrservice)>1:
                    service_type=arrservice[0]
                    ldbblance=arrservice[1]
            crm_service_code='1005'
            if ('再生通' in service_type):
                crm_service_code='1000'
            if ('品牌通' in service_type):
                crm_service_code='1000'
                remark1='开通品牌通'
            if ('增值' in service_type):
                crm_service_code='1002'
            if ('再生汇' in service_type):
                crm_service_code='1004'
            if ('来电宝5元' in service_type):
                crm_service_code='1008'
            if ('来电宝按通计费' in service_type):
                crm_service_code='1011'
                
            if (service_type=='百度优化'):
                crm_service_code='10001002'
            if (service_type=='商铺服务'):
                crm_service_code='10001004'
            if (service_type=='移动生意管家'):
                crm_service_code='10001000'
            if (service_type=='终身会员'):
                crm_service_code='10001003'
            if (service_type=='定金'):
                crm_service_code='10001006'
            if (service_type=='其他'):
                crm_service_code='1005'
            if (service_type=='微站'):
                crm_service_code='10001007'
            
            if (service_type=='企业秀'):
                crm_service_code='10001009'
            if (service_type=='移动生意管家'):
                crm_service_code='10001000'
            if str(service_type)==str(service_type1):
                amount=str(request.POST.get("payMoney"))+'00'
            else:
                amount=0
            sql="select id from crm_service_apply where order_no=%s"
            result=dbserver.fetchonedb(sql,[order_no])
            if not result:
                value=[apply_group, order_no, gmt_income, account, amount,  sale_staff, service_type,  gmt_created, gmt_modified]
                sql="insert into crm_service_apply(apply_group, order_no, gmt_income, email, amount,  sale_staff, remark,  gmt_created, gmt_modified) values(%s,%s,%s,%s,%s,%s,%s,%s,%s)"
                dbserver.updatetodb(sql,value)
                remark1=service_type
                apply_status='0'
                value=[company_id,crm_service_code,apply_group,remark1,gmt_created, gmt_modified,apply_status,mtemplates]
                sql="insert into crm_company_service(company_id,crm_service_code,apply_group,remark,gmt_created, gmt_modified,apply_status,mobile_templates) values(%s,%s,%s,%s,%s,%s,%s,%s)"
                dbserver.updatetodb(sql,value);
                
            if crm_service_code=='10001009':
                sql="select id from crm_service_qiyexiu where company_id=%s"
                resultd=dbserver.fetchonedb(sql,[company_id])
                if not resultd:
                    sql="insert into crm_service_qiyexiu(company_id,css,html) values(%s,%s,%s)"
                    dbserver.updatetodb(sql,[company_id,qiyexiu,qiyexiu]);
            #保存到本地数据库
            sql="select id from kh_income where order_no=%s"
            result=db.fetchonedb(sql,[order_no])
            if not result:
                realname=saler
                sales_date=paytime
                sales_type=request.POST.get("customType")
                sales_price=request.POST.get("payMoney")
                mobile=request.POST.get("com_mobile")
                bz=request.POST.get("remark")
                contactperson=request.POST.get("com_contactperson")
                com_ly1=request.POST.get("com_ly1")
                
                com_ly1=request.POST.get("com_ly1")
                com_ly2=request.POST.get("com_ly2")
                com_zq=request.POST.get("com_zq")
                com_fwq=request.POST.get("com_fwq")
                com_khdq=request.POST.get("com_khdq")
                com_pro=request.POST.get("com_pro")
                com_cpjb=request.POST.get("com_cpjb")
                com_cxfs=request.POST.get("com_cxfs")
                com_hkfs=request.POST.get("com_hkfs")
                com_gjd=request.POST.get("com_gjd")
                com_servernum=request.POST.get("com_servernum")
                if str(service_type)==str(service_type1):
                    sales_price=str(request.POST.get("payMoney"))
                else:
                    sales_price=0
                if not user_id:
                    user_id=0
                if not com_servernum:
                    com_servernum=0
                if not com_gjd:
                    com_gjd=''
                if user_id and user_category_code and company_id:
                    value=[int(user_id),int(user_category_code),int(company_id),order_no,realname,sales_date,service_type,service_type1,sales_type,sales_price,mobile,bz,contactperson,com_ly1,com_ly2,com_zq,com_fwq,com_khdq,com_pro,com_cpjb,com_cxfs,com_hkfs,com_gjd,com_servernum,gmt_created,end_time,ldbblance]
                    sqlc="insert into kh_income (user_id,user_category_code,company_id,order_no,realname,sales_date,service_type,service_type1,sales_type,sales_price,mobile,bz,contactperson,com_ly1,com_ly2,com_zq,com_fwq,com_khdq,com_pro,com_cpjb,com_cxfs,com_hkfs,com_gjd,com_servernum,gmt_created,end_time,ldbblance) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
                    db.updatetodb(sqlc,value)
    return HttpResponse("<script>parent.closeorder()</script>")
#开通单单个字段更新数据
def order_value(request):
    fild=request.GET.get("fild")
    id=request.GET.get("id")
    sql="select "+str(fild)+" from kh_income where id=%s"
    result=db.fetchonedb(sql,[id])
    fildvalue=''
    if result:
        fildvalue=result[fild]
        if fild=="sales_date":
            fildvalue=formattime(fildvalue,1)
    return render_to_response('icdhtml/order_value.html',locals())
def order_value_save(request):
    fild=request.GET.get("fild")
    fildvalue=request.GET.get("fildvalue")
    id=request.GET.get("id")
    sql="update kh_income set "+str(fild)+"=%s where id=%s"
    db.updatetodb(sql,[str(fildvalue),id])
    return HttpResponse(simplejson.dumps({'err':'false','res':sql}, ensure_ascii=False))
    
#开通单删除
def order_del(request):
    id=request.GET.get("id")
    request_url=request.META.get('HTTP_REFERER','/')
    sql="delete from kh_income where id=%s"
    db.updatetodb(sql,[id])
    return HttpResponseRedirect(request_url)
#放到ICD库
def assigntoicd(request):
    company_id=request.GET.get("company_id")
    sql="update company_account set ispay=0 where company_id=%s"
    db.updatetodb(sql,[company_id])
    zzc.updatemodifydata(company_id)
    updatesearchseek(['ispay'], {int(company_id):[0]})
    return HttpResponse(simplejson.dumps({'err':'false','res':'放入成功'}, ensure_ascii=False))
#开通单到单统计
def ordertongji(request):
    nowdate=request.GET.get("nowdate")
    if not nowdate:
        today=getToday()
    else:
        today=str_to_date(nowdate)
    #fromday=str_to_date(today.strftime('%Y-%m')+"-1")
    yearv=request.GET.get("yearv")
    mouthv=request.GET.get("mouthv")
    nowday=None
    if mouthv:
        today=str_to_date(yearv+"-"+mouthv+"-1")
        d = cal.monthrange(int(yearv), int(mouthv))
        nowday=d[1]
    nowyear=today.strftime('%Y')
    nowmoth=today.strftime('%m')
    if not nowday:
        nowday=today.strftime('%d')
       
    
    datelist=range(1,int(nowday)+1)
    
    
    icd1all="%.2f"%zzc.getincomecount(user_category_code="1306",ndate=date_to_str(today),mflag=1)
    icd2all="%.2f"%zzc.getincomecount(user_category_code="1322",ndate=date_to_str(today),mflag=1)
    icd3all="%.2f"%zzc.getincomecount(user_category_code="1307",ndate=date_to_str(today),mflag=1)
    icd4all="%.2f"%zzc.getincomecount(user_category_code="1320",ndate=date_to_str(today),mflag=1)
    icdall="%.2f"%float(float(icd1all)+float(icd2all)+float(icd3all)+float(icd4all))
    vapall="%.2f"%zzc.getincomecount(user_category_code="1315",ndate=date_to_str(today),mflag=1)
    csall="%.2f"%zzc.getincomecount(user_category_code="24",ndate=date_to_str(today),mflag=1)
    zshall="%.2f"%zzc.getincomecount(user_category_code="1325",ndate=date_to_str(today),mflag=1)
    jiaoyiall="%.2f"%zzc.getincomecount(user_category_code="1324",ndate=date_to_str(today),mflag=1)
    allall="%.2f"%zzc.getincomecount(ndate=date_to_str(today),mflag=1)
    
    dlist=[]
    for list in datelist:
        ndate=today.strftime('%Y-%m')+"-"+str(list)
        icd1=zzc.getincomecount(user_category_code="1306",ndate=ndate)
        icd2=zzc.getincomecount(user_category_code="1322",ndate=ndate)
        icd3=zzc.getincomecount(user_category_code="1307",ndate=ndate)
        icd4=zzc.getincomecount(user_category_code="1320",ndate=ndate)
        vap="%.2f"%zzc.getincomecount(user_category_code="1315",ndate=ndate)
        cs="%.2f"%zzc.getincomecount(user_category_code="24",ndate=ndate)
        zsh="%.2f"%zzc.getincomecount(user_category_code="1325",ndate=ndate)
        jiaoyi="%.2f"%zzc.getincomecount(user_category_code="1324",ndate=ndate)
        allprice="%.2f"%zzc.getincomecount(ndate=ndate)
        l={'date':ndate,'icd1':"%.2f"%icd1,'icd2':"%.2f"%icd2,'icd':"%.2f"%(icd1+icd2+icd3+icd4),'icd3':"%.2f"%icd3,'vap':vap,'cs':cs,'zsh':zsh,'jiaoyi':jiaoyi,'allprice':allprice}
        dlist.append(l)
    
    return render_to_response("icdhtml/ordertongji.html",locals())
#客户添加
def companyadd(request):
    username=request.session.get('username',default=None)
    user_id=request.session.get('user_id',default=None)
    if not username or not user_id:
        return simplejson.dumps({'err':'login'}, ensure_ascii=False)
    dbserver = crmdb(dbtype="server")
    #客户参加活动列表
    def getactive():
        sql="select label,code from category where parent_code='2003'"
        aclist=dbserver.fetchalldb(sql)
        return aclist
    addtype= request.GET.get("addtype")
    sid = request.GET.get("sid")
    com_mobile = request.GET.get("com_mobile")
    com_contactperson = request.GET.get("com_contactperson")
    activelist=getactive()
    if (com_mobile==None):
        com_mobile=""
    if (com_contactperson==None):
        com_contactperson=""
    if (addtype=="zst"):
        zstflag=1
    provincelist=zzc.getprovincelist()
    guowaiprovincelist=zzc.getguowailist()
    host=request.get_host()
    return render_to_response('icdhtml/compadd.html',locals())
#客户保存
def companysave(request):
    username=request.session.get('username',default=None)
    user_id=request.session.get('user_id',default=None)
    if not username or not user_id:
        return simplejson.dumps({'err':'login'}, ensure_ascii=False)
    dbserver = crmdb(dbtype="server")
    addtype=request.POST.get("addtype")
    name=cname = request.POST.get("cname")
    contact=ccontactp = request.POST.get("ccontactp")
    cdesi = request.POST.get("cdesi")
    industry_code = request.POST.get("industry_code")
    service_code = request.POST.get("service_code")
    sid = request.POST.get("sid")
    active_flag = request.POST.get("active_flag")
    address=cadd = request.POST.get("cadd")
    address_zip=czip = request.POST.get("czip")[0:6]
    ctel = request.POST.get("ctel")
    mobile=cmobile = request.POST.get("cmobile")
    cfax = request.POST.get("cfax")
    account = request.POST.get("account")
    cemail = request.POST.get("cemail")
    website=domain=cweb = request.POST.get("cweb")
    introduction=cintroduce = request.POST.get("cintroduce")
    business = cproductslist_en = request.POST.get("cproductslist_en")
    personid = request.POST.get("personid")
    countryselect = request.POST.get("countryselect")
    area_code  = request.POST.get("area_code")
    account=account.replace(' ','')
    cemail=cemail.replace(' ','')
    
    regtime=gmt_created=datetime.datetime.now()
    gmt_modified=datetime.datetime.now()
    password=sjs=random.randrange(0,100000000)
    md5pwd = hashlib.md5(str(password))
    md5pwd = md5pwd.hexdigest()[8:-8]
    #''判断邮箱帐号是否存在
    sql="select id  from auth_user where username='"+str(account)+"' or email='"+str(cemail)+"'"
    accountlist=dbserver.fetchonedb(sql)
    if (accountlist):
        response = HttpResponse()
        response.write("<script>alert('该用户名或邮箱已经存在！');</script>")
        return response
    
    #''帐号添加
    value=[account,md5pwd,cemail,gmt_created,gmt_modified];
    sql="insert into auth_user (username,password,email,gmt_created,gmt_modified) values(%s,%s,%s,%s,%s)";
    resultauth=dbserver.updatetodb(sql,value)
    auth_user_id=resultauth['id']
    zzc.getserverdbtable(dbserver,"auth_user",auth_user_id)
    
    #添加公司信息
    foreign_city=''
    category_garden_id=""
    membership_code='10051000'
    classified_code='10101002'
    regfrom_code='10031023'
    
    value=[name, industry_code, business, service_code, area_code, foreign_city, category_garden_id, membership_code,    domain, classified_code, regfrom_code,  regtime, gmt_created, gmt_modified,  address, address_zip, website, introduction,active_flag]
    sql="insert into company (name, industry_code, business, service_code, area_code, foreign_city, category_garden_id, membership_code,    domain, classified_code, regfrom_code,  regtime, gmt_created, gmt_modified,  address, address_zip, website, introduction,active_flag)"
    sql=sql+" values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)";
    result=dbserver.updatetodb(sql,value)
    if result:
        company_id=result['id']
        zzc.getserverdbtable(dbserver,"company",company_id)
        is_admin='1'
        tel_country_code=''
        tel_area_code=''
        tel=ctel
        fax_country_code=''
        fax_area_code=''
        fax=cfax
        email=cemail
        sex=cdesi
        #'添加联系方式
        value=[account, company_id, contact, is_admin, tel_country_code, tel_area_code, tel, mobile, fax_country_code, fax_area_code, fax, email, sex, password, gmt_modified, gmt_created]
        sql="insert into company_account (account, company_id, contact, is_admin, tel_country_code, tel_area_code, tel, mobile, fax_country_code, fax_area_code, fax, email, sex, password, gmt_modified, gmt_created)"
        sql=sql+" values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)";
        resulta=dbserver.updatetodb(sql,value)
        company_account_id=resulta['id']
        zzc.getserverdbtable(dbserver,"company_account",company_account_id)
        savekhlog(company_id,user_id,user_id,'录入客户')
        sql="update company set user_id=%s where id=%s"
        db.updatetodb(sql,[user_id,company_id])
        zzc.updatemodifydata(company_id)
        updateseekoneday()
        #保存到本地
        
    return HttpResponse("录入保存成功！<script>alert('录入成功，主管审核后即可放到你的客户库！');parent.addsucss()</script>")

def company_offercount(request):
    dbserver = crmdb(dbtype="server")
    account=request.GET.get("account")
    company_id=request.GET.get("company_id")
    pcount=0
    qcount=0
    rcount=0
    if company_id:
        sql="select count(0) as count from products where company_id=%s"
        result=dbserver.fetchonedb(sql,[company_id])
        pcount=result['count']
        sql="select qcount from inquiry_count where company_id=%s"
        result=dbserver.fetchonedb(sql,[company_id])
        if result:
            qcount=result['qcount']
    if account:
        sql="select count(0) as count from inquiry where sender_account=%s"
        result=dbserver.fetchonedb(sql,[account])
        rcount=result['count']
    list={'pcount':pcount,'qcount':qcount,'rcount':rcount}
    listall=simplejson.dumps(list, ensure_ascii=False)
    return HttpResponse(listall)
#客户分配设置
def user_assign(request):
    username=request.session.get('username',default=None)
    user_id=request.session.get('user_id',default=None)
    if not username or not user_id:
        return simplejson.dumps({'err':'login'}, ensure_ascii=False)
    allsalesman=zzc.get_allsalesman(user_id=user_id)
    sql="select id from user where assignflag=1"
    result=db.fetchalldb(sql)
    userassignlist="0"
    for list in result:
        userassignlist+=","+str(list['id'])
    return render_to_response("icdhtml/user_assign.html",locals())
def user_assign_ok(request):
    username=request.session.get('username',default=None)
    user_id=request.session.get('user_id',default=None)
    if not username or not user_id:
        return simplejson.dumps({'err':'login'}, ensure_ascii=False)
    useridlist=request.POST.getlist('userid')
    sql="update user set assignflag=0 where id>%s"
    db.updatetodb(sql,[0])
    for list in useridlist:
        sql="update user set assignflag=1 where id=%s"
        db.updatetodb(sql,[list])
    return HttpResponse("保存成功")
#客户分配设置
def user_assign_vap(request):
    username=request.session.get('username',default=None)
    user_id=request.session.get('user_id',default=None)
    if not username or not user_id:
        return simplejson.dumps({'err':'login'}, ensure_ascii=False)
    allsalesman=zzc.get_allsalesman(user_id=user_id)
    sql="select id from user where assignvapflag=1"
    result=db.fetchalldb(sql)
    userassignlist="0"
    for list in result:
        userassignlist+=","+str(list['id'])
    return render_to_response("icdhtml/user_assign_vap.html",locals())
def user_assign_vap_ok(request):
    username=request.session.get('username',default=None)
    user_id=request.session.get('user_id',default=None)
    if not username or not user_id:
        return simplejson.dumps({'err':'login'}, ensure_ascii=False)
    useridlist=request.POST.getlist('userid')
    sql="update user set assignvapflag=0 where id>%s"
    db.updatetodb(sql,[0])
    for list in useridlist:
        sql="update user set assignvapflag=1 where id=%s"
        db.updatetodb(sql,[list])
    return HttpResponse("保存成功")
        
#掉公海设置
def user_drop(request):
    username=request.session.get('username',default=None)
    user_id=request.session.get('user_id',default=None)
    if not username or not user_id:
        return simplejson.dumps({'err':'login'}, ensure_ascii=False)
    allsalesman=zzc.get_allsalesman(user_id=user_id)
    sql="select id from user where dropflag=1"
    result=db.fetchalldb(sql)
    userassignlist="0"
    for list in result:
        userassignlist+=","+str(list['id'])
    return render_to_response("icdhtml/user_drop.html",locals())
def user_drop_ok(request):
    useridlist=request.POST.getlist('userid')
    sql="update user set dropflag=0 where id>%s"
    db.updatetodb(sql,[0])
    for list in useridlist:
        sql="update user set dropflag=1 where id=%s"
        db.updatetodb(sql,[list])
    return HttpResponse("保存成功")

#预申请客户
def sqcompany(request):
    username=request.session.get('username',default=None)
    user_id=request.session.get('user_id',default=None)
    if not username or not user_id:
        return simplejson.dumps({'err':'login'}, ensure_ascii=False)
    company_id=request.GET.get("company_id")
    gmt_created=datetime.datetime.now()
    if company_id:
        dbserver = crmdb(dbtype="server")
        sql="select id from company_account where company_id=%s"
        result=dbserver.fetchonedb(sql,[company_id])
        if result:
            company_account_id=result['id']
            ca=zzc.getserverdbtable(dbserver,"company",company_id)
            cc=zzc.getserverdbtable(dbserver,"company_account",company_account_id)
            if ca==1:
                # 预分配客户申请
                sqld="replace into kh_assign_request (company_id,user_id,gmt_created) values(%s,%s,%s)"
                db.updatetodb(sqld,[company_id,user_id,gmt_created])
                
                sqlc="update company set checked=1 where id=%s"
                db.updatetodb(sqlc,[company_id])
                
                zzc.updatemodifydata(company_id)
                savekhlog(company_id,user_id,user_id,'申请分配新客户')
                updateseekoneday()
                updatesearchseek(['checked'], {int(company_id):[1]})
                return HttpResponse("申请成功，等待主管审核！")
            else:
                return HttpResponse("该客户已经在本地库，请在本地库搜索！")
    else:
        return HttpResponse("错误！")
            
            
def getnewcompanycount(request):
    username=request.session.get('username',default=None)
    user_id=request.session.get('user_id',default=None)
    if not username or not user_id:
        return simplejson.dumps({'err':'login'}, ensure_ascii=False)
    ccount=0
    sql="select ccount from kh_assign_count where user_id=%s"
    result=db.fetchonedb(sql,[user_id])
    if result:
        ccount=result['ccount']
    return HttpResponse(simplejson.dumps({'ccount':ccount}, ensure_ascii=False))
#获得地点
def getsite(request):
    sitecode=request.GET.get('sitecode')
    sitelist=zzc.getsitelist(sitecode=sitecode)
    sitelist=simplejson.dumps(sitelist, ensure_ascii=False)
    return HttpResponse(sitelist)
#重新登录
def relogin(request):
    return render_to_response("icdhtml/relogin.html",locals())
#返回
def returnpage(request):
    request_url=request.GET.get('request_url')
    return HttpResponseRedirect(request_url)
def getcompanyid(request):
    account=request.GET.get("account")
    if account:
        dbserver = crmdb(dbtype="server")
        sql="select username from auth_user where username=%s or account=%s or email=%s"
        result=dbserver.fetchonedb(sql,[account,account,account])
        if result:
            account=result["username"]
            sql="select company_id from company_account where account=%s"
            result=dbserver.fetchonedb(sql,[account])
            if result:
                company_id=result["company_id"]
                tourl="/icd/tellist.html?company_id="+str(company_id)
                return HttpResponseRedirect(tourl)
            else:
                return HttpResponse("录入的账号有误")
        else:
            return HttpResponse("录入的账号有误")
    else:
        return HttpResponse("录入的账号有误")
    
#再生钱包账单
def qianbaobalancelist(request):
    username=request.session.get('username',default=None)
    user_id=request.session.get('user_id',default=None)
    if not username or not user_id:
        return simplejson.dumps({'err':'login'}, ensure_ascii=False)
    
    company_id=request.GET.get('company_id')
        
    page=request.GET.get('page')
    if not page:
        page=1
    searchlist={}
    searchlist['company_id']=company_id
    
    searchurl=urllib.urlencode(searchlist)
    funpage=zz91page()
    limitNum=funpage.limitNum(10)
    nowpage=funpage.nowpage(int(page))
    frompageCount=funpage.frompageCount()
    after_range_num = funpage.after_range_num(3)
    before_range_num = funpage.before_range_num(6)
    
    listall=zzc.getpayfeelist(company_id,frompageCount,limitNum)
    listcount=listall['count']
    listall=listall['list']
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
    return render_to_response("icdhtml/qianbaobalancelist.html",locals())
        
#客户来源
def orderly(request):
    user_category_code=request.GET.get("user_category_code")
    
    return render_to_response("icdhtml/orderly.html",locals())
#客户产品服务
def ordercp(request):
    company_id=request.GET.get("company_id")
    #高会到期时间
    gmt_end=''
    sql="select max(gmt_end) as gmt_end from crm_company_service where company_id=%s and apply_status='1'"
    result=db.fetchonedb(sql,[company_id])
    if result:
        gmt_end=result['gmt_end']
        gmt_end=formattime(gmt_end,1)
    return render_to_response("icdhtml/ordercp.html",locals())
#客户产品服务
def ordercp2(request):
    return render_to_response("icdhtml/ordercp2.html",locals())
        