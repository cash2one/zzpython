#-*- coding:utf-8 -*-
from django.shortcuts import render_to_response,render
from django.http import HttpResponse,HttpResponseRedirect
import simplejson,sys,os,urllib,re,datetime,time,md5,hashlib,random,calendar,json
import calendar as cal
from conn import crmdb
from zz91page import *
from sphinxapi import *
from settings import searchconfig
db=crmdb()
reload(sys)
sys.setdefaultencoding('UTF-8')
nowpath=os.path.dirname(__file__)
execfile(nowpath+"/func/hr_function.py")
execfile(nowpath+"/func/crmtools.py")
execfile(nowpath+"/func/company_function.py")
zzc=customer()
zzs=zzhr()

#取出所有人员信息
def hr_list(request):
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
    dotype=request.GET.get("dotype")
    if dotype:
        searchlist['dotype']=dotype
    star=request.GET.get("star")
    if star:
        searchlist['star']=star
    else:
        star=''
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
    email=request.GET.get("email")
    if email:
        searchlist['email']=email
    else:
        email=''
    sex=request.GET.get("sex")
    if sex:
        searchlist['sex']=sex
    contactstat=request.GET.get("contactstat")
    if contactstat:
        searchlist['contactstat']=contactstat
    jl1=request.GET.get("jl1")
    if jl1:
        searchlist['jl1']=jl1
    jl2=request.GET.get("jl2")
    if jl2:
        searchlist['jl2']=jl2
    jl3=request.GET.get("jl3")
    if jl3:
        searchlist['jl3']=jl3
    jl4=request.GET.get("jl4")
    if jl4:
        searchlist['jl4']=jl4
    jl5=request.GET.get("jl5")
    if jl5:
        searchlist['jl5']=jl5
    personid=request.GET.get("personid")
    if personid:
        searchlist['personid']=personid
    rpersonid=request.GET.get("rpersonid")
    if rpersonid:
        searchlist['rpersonid']=rpersonid
    orderstr=request.GET.get("orderstr")
    if orderstr:
        searchlist['orderstr']=orderstr
    searchlist['user_id']=user_id
    contactstat_list=zzs.getcategorylist(code="22")
    jl1_list=zzs.getcategorylist(code="17")
    jl2_list=zzs.getcategorylist(code="18")
    jl3_list=zzs.getcategorylist(code="19")
    jl4_list=zzs.getcategorylist(code="20")
    jl5_list=zzs.getcategorylist(code="21")
    #获得销售人员列表(selection)
    allsalesman=zzc.get_allsalesman(user_id=user_id,renshi=1)
    interviewTime1=request.GET.get("interviewTime1")
    interviewTime2=request.GET.get("interviewTime2")
    if interviewTime1 and interviewTime2:
        searchlist['interviewTime1']=interviewTime1
        searchlist['interviewTime2']=interviewTime2
    else:
        interviewTime1=''
        interviewTime2=''
    gmt_created1=request.GET.get("gmt_created1")
    gmt_created2=request.GET.get("gmt_created2")
    if gmt_created1 and gmt_created2:
        searchlist['gmt_created1']=gmt_created1
        searchlist['gmt_created2']=gmt_created2
    else:
        gmt_created1=''
        gmt_created2=''
    orderstr=request.GET.get('orderstr')
    if orderstr:
        searchlist['orderstr']=orderstr
    else:
        orderstr=''
    searchurl=urllib.urlencode(searchlist)
    funpage=zz91page()
    limitNum=funpage.limitNum(15)
    nowpage=funpage.nowpage(int(page))
    frompageCount=funpage.frompageCount()
    after_range_num = funpage.after_range_num(3)
    before_range_num = funpage.before_range_num(6)
    userallr=zzs.gethrlist(frompageCount=frompageCount,limitNum=limitNum,searchlist=searchlist)
    listcount=userallr['count']
    listall=userallr['list']
    listcount = funpage.listcount(listcount)
    page_listcount=funpage.page_listcount()
    firstpage = funpage.firstpage()
    lastpage = funpage.lastpage()
    page_range  = funpage.page_range()
    nextpage = funpage.nextpage()
    prvpage = funpage.prvpage()
    return render_to_response('hr/hr_list.html',locals())
#添加人员
def hr_add(request):
    username=request.session.get('username',default=None)
    user_id=request.session.get('user_id',default=None)
    if not username or not user_id:
        return HttpResponseRedirect("relogin.html")
    renshi_station=zzs.getcategorylist(code="15")
    education_list=zzs.getcategorylist(code="16")
    return render_to_response('hr/hr_add.html',locals())
def hr_save(request):
    username=request.session.get('username',default=None)
    user_id=request.session.get('user_id',default=None)
    if not username or not user_id:
        return HttpResponseRedirect("relogin.html")
    username=request.POST.get('username')
    mobile=request.POST.get('mobile')
    othercontact=request.POST.get('othercontact')
    sex=request.POST.get('sex')
    email=request.POST.get('email')
    education=request.POST.get('education')
    worklonger=request.POST.get('worklonger')
    laiyuan=request.POST.get('laiyuan')
    station=request.POST.get('station')
    station2=request.POST.get('station2')
    gmt_created=gmt_modified=datetime.datetime.now()
    
    obj=request.FILES.get('fileField')
    timepath=time.strftime('%Y/%m/%d/',time.localtime(time.time()))
    tmp = random.randint(100, 999)
    nowtime=int(time.time())
    time_now=datetime.datetime.now()
    resumeUrl=''
    if obj:
        filename=obj.name
        kzname=''
        if filename:
            arrfile=filename.split(".")
            kzname=arrfile[len(arrfile)-1]
        newpath=nowpath+"/file/"+timepath
        
        imgpath=newpath+str(nowtime)+str(tmp)+"."+kzname
        if not os.path.isdir(newpath):
            os.makedirs(newpath)
        f=open(imgpath, 'wb')
        for chunk in obj.chunks():
            f.write(chunk)
            f.close()
        resumeUrl=timepath+str(nowtime)+str(tmp)+"."+kzname
    sql='insert into renshi_user(username,mobile,othercontact,sex,email,education,worklonger,laiyuan,station,station2,gmt_created,gmt_modified,resumeUrl,personid) values(%s, %s, %s,%s, %s, %s, %s, %s, %s, %s,%s,%s,%s,%s)'
    result=db.updatetodb(sql,[username,mobile,othercontact,sex,email,education,worklonger,laiyuan,station,station2,gmt_created,gmt_modified,resumeUrl,user_id])
    
    sql='select id from renshi_user order by id desc '
    result1=db.fetchonedb(sql)
    last_insert_id=result1['id']
    sql='insert into renshi_assign(uid,personid,fdate) values(%s, %s, %s)'
    result2=db.updatetodb(sql,[last_insert_id,user_id,time_now])
    
    return HttpResponseRedirect('list.html')
#修改人员信息
def hr_mod(request):
    username=request.session.get('username',default=None)
    user_id=request.session.get('user_id',default=None)
    if not username or not user_id:
        return HttpResponseRedirect("relogin.html")
    if request.method=="POST":
        gmt_modified=datetime.datetime.now()
        mobile=request.POST.get('mobile')
        username=request.POST.get('username')
        othercontact=request.POST.get('othercontact')
        sex=request.POST.get('sex')
        email=request.POST.get("email")
        worklonger=request.POST.get('worklonger')
        laiyuan=request.POST.get('laiyuan')
        id=request.POST.get('id')
        resumeUrl=request.POST.get('resumeUrl')
        station2=request.POST.get('station2')
        station=request.POST.get('station')
        education=request.POST.get('education')
        obj=request.FILES.get('fileField')
        timepath=time.strftime('%Y/%m/%d/',time.localtime(time.time()))
        tmp = random.randint(100, 999)
        nowtime=int(time.time())
        if obj:
            filename=obj.name
            kzname=''
            if filename:
                arrfile=filename.split(".")
                kzname=arrfile[len(arrfile)-1]
            newpath=nowpath+"/file/"+timepath
            
            imgpath=newpath+str(nowtime)+str(tmp)+"."+kzname
            if not os.path.isdir(newpath):
                os.makedirs(newpath)
            f=open(imgpath, 'wb')
            for chunk in obj.chunks():
                f.write(chunk)
                f.close()
            resumeUrl=timepath+str(nowtime)+str(tmp)+"."+kzname
        if username:
            sql='update renshi_user set mobile=%s,username=%s,othercontact=%s,sex=%s,email=%s,worklonger=%s,laiyuan=%s,gmt_modified=%s,resumeUrl=%s,station=%s,station2=%s,education=%s where id=%s'
            result=db.updatetodb(sql,[mobile,username,othercontact,sex,email,worklonger,laiyuan,gmt_modified,resumeUrl,station,station2,education,id])
            return HttpResponseRedirect('list.html')
    else:
        id=request.GET.get('id')
        resumeUrl=request.GET.get('resumeUrl')
        renshi_station=zzs.getcategorylist(code="15")
        education_list=zzs.getcategorylist(code="16")
        if id:
            sql='select * from renshi_user where id=%s'
            result=db.fetchonedb(sql,[id])
            if result:
                if result['sex']=='男':
                    pass
                elif result['sex'] == '女':
                    del result['sex']
                if not result['resumeUrl']:
                    result['resumeUrl']=None
            return render_to_response('hr/hr_mod.html',locals())
        if resumeUrl:
            newpath=os.path+resumeUrl
            with open(newpath) as f:  
                c = f.read()
            return render_to_response('hr/hr_mod.html',locals())

#批量处理
def hr_all(request):
    username=request.session.get('username',default=None)
    user_id=request.session.get('user_id',default=None)
    if not username or not user_id:
        return HttpResponseRedirect("relogin.html")
    check_box_list = request.REQUEST.getlist("check_box_list")
    topersonid=request.POST.get('topersonid')
    value=request.POST.get('dostay',default=None)
    user_id=request.session.get('user_id',default=None)
    fdate=datetime.datetime.now()
    if not value:
        for id in check_box_list:
            sql='delete from renshi_user where id=%s'
            result=db.updatetodb(sql,[id])
    elif value=='assignto':
        for id in check_box_list:
            sql="select id from renshi_assign where uid=%s"
            result=db.fetchonedb(sql,[id])
            if not result:
                sql='insert into renshi_assign(personid,uid,fdate) values(%s, %s, %s)'
                db.updatetodb(sql,[topersonid,id,fdate])
            else:
                sql="update renshi_assign set personid=%s where id=%s"
                db.updatetodb(sql,[topersonid,result['id']])
            bz="客户分配"
            sql='insert into renshi_history(bz,uid,personid,fdate) values(%s,%s,%s,%s)'
            db.updatetodb(sql,[bz,id,user_id,fdate])
    elif value=='tomy':
        for id in check_box_list:
            sql="select id from renshi_assign where uid=%s"
            result=db.fetchonedb(sql,[id])
            if not result:
                sql='insert into renshi_assign(personid,uid,fdate) values(%s, %s, %s)'
                db.updatetodb(sql,[user_id,id,fdate])
            else:
                sql="update renshi_assign set personid=%s where id=%s"
                db.updatetodb(sql,[user_id,result['id']])
            bz="放到我的客户库"
            sql='insert into renshi_history(bz,uid,personid,fdate) values(%s,%s,%s,%s)'
            db.updatetodb(sql,[bz,id,user_id,fdate])
    elif value=='gonghai':
        for id in check_box_list:
            sql='delete from renshi_assign where personid=%s and uid=%s'
            result=db.updatetodb(sql,[user_id,id])
            bz="放入公海"
            sql='insert into renshi_history(bz,uid,personid,fdate) values(%s,%s,%s,%s)'
            db.updatetodb(sql,[bz,id,user_id,fdate])
    return HttpResponseRedirect('list.html')
    
#单独界面显示个人信息
def hr_usershow(request):
    username=request.session.get('username',default=None)
    user_id=request.session.get('user_id',default=None)
    if not username or not user_id:
        return HttpResponseRedirect("relogin.html")
    contactstat_list=zzs.getcategorylist(code="22")
    jl1_list=zzs.getcategorylist(code="17")
    jl2_list=zzs.getcategorylist(code="18")
    jl3_list=zzs.getcategorylist(code="19")
    jl4_list=zzs.getcategorylist(code="20")
    jl5_list=zzs.getcategorylist(code="21")
    if request.method=="POST":
        uid=request.GET.get('uid')
        contactstat=request.POST.get('contactstat')
        selectjl=request.POST.get('selectjl')
        if selectjl=="1":
            code=request.POST.get('jl1')
        if selectjl=="2":
            code=request.POST.get('jl2')
        if selectjl=="3":
            code=request.POST.get('jl3')
        if selectjl=="4":
            code=request.POST.get('jl4')
        if selectjl=="5":
            code=request.POST.get('jl5')
        star=request.POST.get('star')
        nextteltime=request.POST.get('nextteltime')
        bz=request.POST.get('bz')
        user_id=request.session.get('user_id',default=None)
        fdate=datetime.datetime.now()
        gmt_created=datetime.datetime.now()
        if uid:
            sql='insert into renshi_history(contactstat,code,star,nextteltime,bz,uid,personid,fdate) values(%s,%s,%s,%s,%s,%s,%s,%s)'
            result=db.updatetodb(sql,[contactstat,code,star,nextteltime,bz,uid,user_id,fdate])
            sql='update renshi_user set star=%s,gmt_created=%s where id=%s'
            result=db.updatetodb(sql,[star,gmt_created,uid])
        return HttpResponseRedirect('list.html')
    else:
        id=request.GET.get('uid')
        if id:
            sql='select id,username,mobile,station,station2,othercontact,sex,email,education,worklonger,laiyuan from renshi_user where id=%s'
            result=db.fetchonedb(sql,[id])
            if result:
                result['station_name']=zzs.getcategorylabel(result['station'])
                result['station2_name']=zzs.getcategorylabel(result['station2'])
                result['education_name']=zzs.getcategorylabel(result['education'])
            return render_to_response('hr/hr_usershow.html',locals())
#操作记录
def hr_usershow_history(request):
    username=request.session.get('username',default=None)
    user_id=request.session.get('user_id',default=None)
    if not username or not user_id:
        return HttpResponseRedirect("relogin.html")
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
    userallr=zzs.getrenshihistory(searchlist=searchlist,frompageCount=frompageCount,limitNum=limitNum)
    listall=userallr['list']
    listcount=userallr['count']
    listcount = funpage.listcount(listcount)
    page_listcount=funpage.page_listcount()
    firstpage = funpage.firstpage()
    lastpage = funpage.lastpage()
    page_range  = funpage.page_range()
    nextpage = funpage.nextpage()
    prvpage = funpage.prvpage()
    return render_to_response('hr/hr_usershow_history.html',locals())
    
#人事基础数据
def hr_basic(request):
    username=request.session.get('username',default=None)
    user_id=request.session.get('user_id',default=None)
    if not username or not user_id:
        return HttpResponseRedirect("relogin.html")
    searchlist={}
    label=request.GET.get('label')
    if label:
        searchlist['label']=label
    basiclist=zzs.gethrbasiclist(searchlist=searchlist)
    return render_to_response('hr/hr_basic.html',locals())

#添加人事基础数据
def hr_basic_add(request):
    username=request.session.get('username',default=None)
    user_id=request.session.get('user_id',default=None)
    if not username or not user_id:
        return HttpResponseRedirect("relogin.html")
    code=request.GET.get('code')
    if code:
        label=request.POST.get('label')
        ord=request.POST.get('ord')
        if label:
            sql="select count(0) as count from renshi_category where code like %s"
            code1=str(db.fetchonedb(sql,[""+code+"__"])['count']+1)
            code1=code1.zfill(2)
            code=code+code1
            sql="insert into renshi_category(code,label,ord) values(%s, %s, %s)"
            result=db.updatetodb(sql,[code,label,ord])
            return HttpResponseRedirect('basic.html')
        return render(request,'hr/hr_basic_add.html')
    else:
        label=request.POST.get('label')
        ord=request.POST.get('ord')
        if label:
            sql="select max(left(code,2))+1 from renshi_category"
            code=db.fetchonedb(sql)['max(left(code,2))+1']
            sql="insert into renshi_category (code,label,ord) values(%s, %s, %s)"
            result=db.updatetodb(sql,[code,label,ord])
            return HttpResponseRedirect('basic.html')
        return render(request,'hr/hr_basic_add.html')
#修改人事基础数据
def hr_basic_mod(request):
    username=request.session.get('username',default=None)
    user_id=request.session.get('user_id',default=None)
    if not username or not user_id:
        return HttpResponseRedirect("relogin.html")
    if request.method=="POST":
        label=request.POST.get('label')
        ord=request.POST.get('ord')
        id=request.GET.get('id')
        if label:
            sql='update renshi_category set label=%s,ord=%s where id=%s'
            result=db.updatetodb(sql,[label,ord,id])
        return HttpResponseRedirect('basic.html')
    else:
        id=request.GET.get('id')
        if id:
            sql='select * from renshi_category where id=%s'
            result=db.fetchonedb(sql,[id])
            return render_to_response('hr/hr_basic_mod.html',locals())
#删除人事基础数据
def hr_basic_del(request):
    username=request.session.get('username',default=None)
    user_id=request.session.get('user_id',default=None)
    if not username or not user_id:
        return HttpResponseRedirect("relogin.html")
    id=request.GET.get('id')
    if id:
        sql='delete from renshi_category where id=%s'
        result=db.updatetodb(sql,[id])
        return HttpResponseRedirect('basic.html')
#保存
def hr_list_save(request):
    username=request.session.get('username',default=None)
    user_id=request.session.get('user_id',default=None)
    if not username or not user_id:
        list={'err':'login'}
        return HttpResponse(simplejson.dumps(list, ensure_ascii=False))
    hid=request.GET.get("hid")
    hvalue=request.GET.get("hvalue")
    hfild=request.GET.get("hfild")
    sql="update renshi_user set "+hfild+"=%s where id=%s"
    db.updatetodb(sql,[hvalue,hid])
    fdate=datetime.datetime.now()
    sql="insert into renshi_history(uid,code,personid,fdate) values(%s,%s,%s,%s)"
    db.updatetodb(sql,[hid,hvalue,user_id,fdate])
    list={'err':'false'}
    return HttpResponse(simplejson.dumps(list, ensure_ascii=False))
    
#获取基础类别列表
def hr_categorylist(request):
    username=request.session.get('username',default=None)
    user_id=request.session.get('user_id',default=None)
    if not username or not user_id:
        return HttpResponseRedirect("relogin.html")
    code=request.GET.get("code")
    list=zzs.getcategorylist(code=code[0:2])
    return HttpResponse(simplejson.dumps(list, ensure_ascii=False))