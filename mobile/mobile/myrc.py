#-*- coding:utf-8 -*-
from django.shortcuts import render_to_response
from django.http import HttpResponse,HttpResponseRedirect,HttpResponsePermanentRedirect
import MySQLdb,sys,os,memcache,settings,urllib,re,time,datetime,requests,md5,hashlib,random,simplejson,json
from django.core.cache import cache
from sphinxapi import *
from zz91page import *
from zz91tools import formattime,int_to_datetime,str_to_int,date_to_int,date_to_strall
from settings import spconfig,weixinconfig
#from commfunction import filter_tags,formattime,havepicflag,subString
from function import getnowurl
#from zz91tools import int_to_str
from zz91conn import database_mongodb
from zz91db_ast import companydb
from zz91db_sms import smsdb
from zz91db_2_news import newsdb
import top.api

dbc=companydb()
dbn=newsdb()

reload(sys)
sys.setdefaultencoding('UTF-8')
nowpath=os.path.dirname(__file__)
execfile(nowpath+"/commfunction.py")
execfile(nowpath+"/function.py")
execfile(nowpath+"/func/myrc_function.py")
execfile(nowpath+"/func/message_function.py")
execfile(nowpath+"/func/qianbao_function.py")
execfile(nowpath+"/func/company_function.py")
execfile(nowpath+"/func/ldb_weixin_function.py")
from zzwx.client import Client
zzm=zmyrc()
zzms=zzmessage()
dbmongo=database_mongodb()
zzq=qianbao()
dbsms=smsdb()
zzc=zcompany()
zzldb=ldbweixin()

#----生意管家首页
def myrc_index(request):
    host=getnowurl(request)
    webtitle="生意管家"
    nowlanmu="<a href='/myrc/'>生意管家</a>"
    zzm.weixinautologin(request,request.GET.get("weixinid"))
    username=request.session.get("username",None)
    company_id=request.session.get("company_id",None)
    if username and (company_id==None or str(company_id)=="0"):
        company_id=getcompanyid(username)
        request.session['company_id']=company_id
    if (username==None or (company_id==None or str(company_id)=="0")):
        return HttpResponseRedirect("/login/?done="+host)
    
    #判断是否拉黑
    sqlh="select id from company where id=%s and is_block=1"
    listh=dbc.fetchonedb(sqlh,[company_id]);
    if listh:
        error="该用户已经被禁止登录！"
        return HttpResponse(error)
    completeflag={'text':'','showflag':0}
    faceurl=None
    sql="select picture_path from bbs_user_profiler where company_id=%s"
    piclist=dbc.fetchonedb(sql,[company_id])
    faceurl=None
    if piclist:
        if piclist[0]:
            faceurl="http://img3.zz91.com/100x100/"+piclist[0]
    if not faceurl:
       completeflag['text']="请上传您的头像！"
       completeflag['showflag']=1
       faceurl="http://static.m.zz91.com/aui/images/noavatar.gif"
    #是否来电宝
    ldbjtl=None
    ldbvalue=getldbphone(company_id)
    if not ldbvalue:
        #----余额
        blance=zzq.getqianbaoblance(company_id)
        #留言量
        qcount=zzms.getnoviewmessagecount(company_id,1)
    else:
        blancelist=zzldb.getldbbalance(company_id)
        if blancelist:
            blance=blancelist['lave']
        qcount=0
        #接听率
        ldbjtl=zzldb.getnowmonthstate(company_id)
    #是否企业秀
    isqiyexiu=zzq.getisqiyexiu(company_id)
    #是否签到
    gmt_date=datetime.date.today()
    qiandao=None
    if not ldbvalue:
        sql="select id from app_qiandao where company_id=%s and gmt_date=%s"
        result=dbc.fetchonedb(sql,[company_id,gmt_date])
        if result:
            qiandao=1
        else:
            qiandao=None
    sqlc="select industry_code,business,area_code,address,name from company where id=%s"
    result=dbc.fetchonedb(sqlc,[company_id])
    if result:
        industry_code=result[0]
        business=result[1]
        area_code=result[2]
        address=result[3]
        companyname=result[4]
        if not industry_code or not business or not area_code or not address:
            completeflag['text']="填写完善获得更优质服务！"
            completeflag['showflag']=1
    if company_id:
        sql="select company_id,account,contact,sex,mobile,qq from company_account where company_id=%s"
        listc=dbc.fetchonedb(sql,[company_id])
        if listc:
            company_id=listc[0]
            contact=listc[2]
            sex=listc[3]
            mobile=listc[4]
            qq=listc[5]
            if not qq:
               completeflag['text']="请QQ号码！"
               completeflag['showflag']=1
            if str(sex)=="0":
                if ("先生" not in contact):
                    contact+="先生"
            if str(sex)=="1":
                if ("女士" not in contact):
                    contact+="女士"

        zxinfo=zzc.getcxinfo(company_id)
        zxclose=None
        #销售助理信息
        cslist=None
        sql="select cs_account from crm_cs where company_id=%s"
        result=dbc.fetchonedb(sql,[company_id])
        if result:
            cs_account=result[0]
            if cs_account:
                sql="select value from param where types='cs_info' and param.key=%s"
                result1=dbc.fetchonedb(sql,[cs_account])
                if result1:
                    value=result1[0]
                    if value:
                        valuelist=value.split(",")
                        csname=valuelist[0]
                        cstel=valuelist[1]
                        cslist={'name':csname,'tel':cstel}
        list={'err':'false','errkey':'','contact':contact,'blance':blance,'qcount':qcount,'ldbvalue':ldbvalue,'qiandao':qiandao,'faceurl':faceurl,'mobile':mobile,'ldbjtl':ldbjtl,'completeflag':completeflag,'zxinfo':zxinfo,'zxclose':zxclose,'isqiyexiu':isqiyexiu,'companyname':companyname,'cslist':cslist}
    else:
        list={'err':'true','errkey':'请重新登录！'}
    #互助未查看数
    notviewcount=getnoviewreplycount(company_id)
    if notviewcount>0:
        huzhucountshow=1
    #未读工单信息
    sql="select count(0) from gd_question as a left join gd_answer as b on a.id=b.question_id where b.isview=0 and a.company_id=%s"
    result=dbc.fetchonedb(sql,[company_id])
    noviewanwer=result[0]
    if noviewanwer>0:
        gdshow=1
    md5companyid = hashlib.md5(username+str(company_id))
    md5companyid = md5companyid.hexdigest()[8:-8]
    #----判断是否为来电宝用户
    viptype=zzm.getviptype(company_id)
    if viptype=='10051003':
        isldb=1
    return render_to_response('aui/myrc/index.html',locals())
    #return render_to_response('myrc/myrc.html',locals())
def oldmyrcindex(request):
    return HttpResponseRedirect("/myrc/index.html")
#获得打卡钱包
def getdakaqianbao(request):
    host=getnowurl(request)
    myrc=1
    showpost=1
    showgooglead=1
    webtitle="生意管家"
    nowlanmu="<a href='/myrc/'>生意管家</a>"
    gettype=request.GET.get("gettype")
    zzm.weixinautologin(request,request.GET.get("weixinid"))
    username=request.session.get("username",None)
    company_id=request.session.get("company_id",None)
    account=username
    if username and (company_id==None or str(company_id)=="0"):
        company_id=getcompanyid(username)
        request.session['company_id']=company_id
    if (username==None or (company_id==None or str(company_id)=="0")):
        return HttpResponseRedirect("/login/?done="+host)
    if gettype=="7day":
        sqld="select qiandao_count,qiandao_list,id from weixin_qiandao_count where account=%s and qiandao_count>=7 order by id asc"
        resultd=dbc.fetchonedb(sqld,[account])
        if resultd:
            id=resultd[2]
            qiandao_list=resultd[1]
            sql="update weixin_qiandao_count set qiandao_count=%s where id=%s"
            dbc.updatetodb(sql,[0,id])
            sql="update weixin_qiandao set checked=1 where account=%s and id in ("+str(qiandao_list)+")"
            dbc.updatetodb(sql,[account])
            #送10元再生钱包
            zzq.getsendfee(company_id,"10","46",more=1)
            return HttpResponse("恭喜您，你已经领取了10元再生钱包！")
    if gettype=="21day":
        sqld="select id,qiandao_list,count(0) from weixin_qiandao_count where account=%s and qiandao_count>=7 order by id asc"
        resultd=dbc.fetchalldb(sqld,[account])
        i=0
        lqflag=0
        if resultd:
            for list in resultd:
                id=list[0]
                qcount=list[2]
                qiandao_list=list[1]
                i=i+1
                if qcount>=3 and i<=3:
                    lqflag=1
                    sql="update weixin_qiandao_count set qiandao_count=%s where id=%s"
                    dbc.updatetodb(sql,[0,id])
                    sql="update weixin_qiandao set checked=1 where account=%s and id in ("+str(qiandao_list)+")"
                    dbc.updatetodb(sql,[account])
            if lqflag==1:
                #领取服务
                sql2='select id,UNIX_TIMESTAMP(gmt_end) from shop_reflush where company_id=%s and DATEDIFF(CURDATE(),gmt_end)<=0 order by id desc'
                result=dbc.fetchonedb(sql2,[company_id])
                if result:
                    errflag='true'
                    reupdate=1
                    gmt_begin=result[1]
                else:
                    reupdate=1
                    gmt_begin=int(time.time())
                if reupdate==1:
                    gmt_created=datetime.datetime.now()
                    gmt_date=datetime.date.today()
                    gmt_end=gmt_begin+(3600*24*30*1)
                    gmt_begin=int_to_datetime(gmt_begin)
                    gmt_end=int_to_datetime(gmt_end)
                    sql='insert into shop_reflush(company_id,gmt_begin,gmt_end,gmt_created,gmt_date) values(%s,%s,%s,%s,%s)'
                    dbc.updatetodb(sql,[company_id,gmt_begin,gmt_end,gmt_created,gmt_date])
                    errflag='false'
                    errtext='恭喜您，您已经成功开通供求自动刷新的服务！'
            return HttpResponse("恭喜您，你已经领取了“供求自动刷新”一个月服务！已经为你开通服务！")

#资料修改
def myrc_info(request):
    webtitle="资料修改"
    host=getnowurl(request)
    zzm.weixinautologin(request,request.GET.get("weixinid"))
    username=request.session.get("username",None)
    company_id=request.session.get("company_id",None)
    if username and (company_id==None or str(company_id)=="0"):
        company_id=getcompanyid(username)
        request.session['company_id']=company_id
    if (username==None or (company_id==None or str(company_id)=="0")):
        return HttpResponseRedirect("/login/?done="+host)
    if company_id:
        contactinfolist=get_contactinfo(company_id)
        companyinfolist=get_companyinfo(company_id)
        #industry_label=getindustrylabel(companyinfolist['industry_code'])
        #service_label=getservicelabel(companyinfolist['service_code'])
        
        qq = contactinfolist['qq']
        if not qq:
            qq=""
        mobile = contactinfolist['mobile']
        contact = contactinfolist['contact']
        if not contact:
            contact=""
        
        sex = contactinfolist['sex']
        email = contactinfolist['email']
        companyname=companyinfolist['name']
        if not companyname:
            companyname=""
        if not email:
            email=""
        industryCode = companyinfolist['industry_code']
        serviceCode = companyinfolist['service_code']
        areaCode = companyinfolist['area_code']
        if not areaCode:
            areaCode="10011000"
        address = companyinfolist['address']
        if not address:
            address=""
        addresszip = companyinfolist['address_zip']
        if not addresszip:
            addresszip=""
        business = companyinfolist['business']
        if not business:
            business=""
    
    return render_to_response('myrc/info_modify.html',locals())
#我的名片
def myrc_card(request):
    webtitle="资料密码"
    host=getnowurl(request)
    zzm.weixinautologin(request,request.GET.get("weixinid"))
    username=request.session.get("username",None)
    company_id=request.session.get("company_id",None)
    if username and (company_id==None or str(company_id)=="0"):
        company_id=getcompanyid(username)
        request.session['company_id']=company_id
    if (username==None or (company_id==None or str(company_id)=="0")):
        return HttpResponseRedirect("/login/?done="+host)
    
    appid=weixinconfig['zz91service']['appid']
    client = Client(weixinconfig['zz91service']['appid'], weixinconfig['zz91service']['secret'])
    host=getnowurl(request)
    host=host.replace("^and^","&")
    url="http://m.zz91.com"+host
    signlist=client.get_sign(url=url)
    timestamp=signlist['timestamp']
    nonceStr=signlist['nonceStr']
    signature=signlist['signature']
    jsapi_ticket=signlist['jsapi_ticket']
    
    return render_to_response('aui/myrc/card.html',locals())
#---我的通讯录
def myrc_addressbook(request):
    host=getnowurl(request)
    zzm.weixinautologin(request,request.GET.get("weixinid"))
    username=request.session.get("username",None)
    company_id=request.session.get("company_id",None)
    if username and (company_id==None or str(company_id)=="0"):
        company_id=getcompanyid(username)
        request.session['company_id']=company_id
    if (username==None or (company_id==None or str(company_id)=="0")):
        return HttpResponseRedirect("/login/?done="+host)
    searchlist={}
    searchurl=urllib.urlencode(searchlist)
    page=request.GET.get("page")
    if (page==None or str(page)=="0"):
        page=1
    funpage = zz91page()
    limitNum=funpage.limitNum(10)
    nowpage=funpage.nowpage(int(page))
    frompageCount=funpage.frompageCount()
    after_range_num = funpage.after_range_num(2)
    before_range_num = funpage.before_range_num(9)
    qlistall=zzm.getmyaddressbooklist(frompageCount=frompageCount,limitNum=limitNum,company_id=company_id)
    qlist=qlistall['list']
    qlistcount=qlistall['count']
    listcount=qlistcount
    if (int(listcount)>100000):
        listcount=100000
    listcount = funpage.listcount(listcount)
    page_listcount=funpage.page_listcount()
    firstpage = funpage.firstpage()
    lastpage = funpage.lastpage()
    page_range  = funpage.page_range()
    nextpage = funpage.nextpage()
    prvpage = funpage.prvpage()
    return render_to_response('aui/myrc/addressbook.html',locals())
#---删除通信录
def myrc_addressbook_del(request):
    host=getnowurl(request)
    zzm.weixinautologin(request,request.GET.get("weixinid"))
    username=request.session.get("username",None)
    company_id=request.session.get("company_id",None)
    if username and (company_id==None or str(company_id)=="0"):
        company_id=getcompanyid(username)
        request.session['company_id']=company_id
    if (username==None or (company_id==None or str(company_id)=="0")):
        errlist={'tokenerr':'true'}
        return HttpResponse(simplejson.dumps(errlist, ensure_ascii=False))
    forcompany_id=request.GET.get("forcompany_id")
    sql="delete from company_addressbook where company_id=%s and forcompany_id=%s"
    dbc.updatetodb(sql,[company_id,forcompany_id])
    messagedata={'err':'true','errkey':''}
    return HttpResponse(simplejson.dumps(messagedata, ensure_ascii=False))
def myrc_share(request):
    appid=weixinconfig['zz91service']['appid']
    client = Client(weixinconfig['zz91service']['appid'], weixinconfig['zz91service']['secret'])
    host=getnowurl(request)
    host=host.replace("^and^","&")
    url="http://m.zz91.com"+host
    signlist=client.get_sign(url=url)
    timestamp=signlist['timestamp']
    nonceStr=signlist['nonceStr']
    signature=signlist['signature']
    jsapi_ticket=signlist['jsapi_ticket']
    return render_to_response('aui/myrc/share.html',locals())
def myrc_password(request):
    webtitle="资料密码"
    host=getnowurl(request)
    zzm.weixinautologin(request,request.GET.get("weixinid"))
    username=request.session.get("username",None)
    company_id=request.session.get("company_id",None)
    if username and (company_id==None or str(company_id)=="0"):
        company_id=getcompanyid(username)
        request.session['company_id']=company_id
    if (username==None or (company_id==None or str(company_id)=="0")):
        return HttpResponseRedirect("/login/?done="+host)
    mobile=''
    sql="select mobile from company_account where company_id=%s"
    result=dbc.fetchonedb(sql,[company_id])
    if result:
        mobile=result[0]
    
    return render_to_response('aui/myrc/password.html',locals())
def forgetpassword(request):
    
    return render_to_response('aui/myrc/forgetpassword.html',locals())

def myrc_infosave(request):
    username=request.session.get("username",None)
    company_id=request.session.get("company_id",None)
    
    contact = request.POST.get('contact')
    sex = request.POST.get('sex')
    qq = request.POST.get('qq')
    email = request.POST.get('email')
    industryCode = request.POST.get('industryCode')
    serviceCode = request.POST.get('serviceCode')
    areaCode = request.POST.get('areaCode')
    if not areaCode:
        areaCode="10011000"
    address = request.POST.get('address')
    addresszip = request.POST.get('addresszip')
    business = request.POST.get('business')
    if company_id:
        value=[industryCode,business,serviceCode,areaCode,address,addresszip,company_id]
        sql="update company set industry_code=%s,business=%s,service_code=%s,area_code=%s,address=%s,address_zip=%s where id=%s"
        dbc.updatetodb(sql,value);
        sql="select id  from company_account where email=%s and company_id>%s and company_id<%s"
        accountlist=dbc.fetchonedb(sql,[str(email),company_id,company_id])
        if (accountlist):
            errflag=1
            errtext="您填写邮箱已经注册！请更换其他邮箱，或点此<a href='/weixin/sendemail.html'>获得密码?</a>或请修改后重新提交！"
            return render_to_response('myrc/info_modify.html',locals())
        else:
            value1=[email,qq,contact,sex,company_id]
            sql1="update company_account set email=%s,qq=%s,contact=%s,sex=%s where company_id=%s"
            dbc.updatetodb(sql1,value1);
            return HttpResponseRedirect("/myrc/")
    return render_to_response('myrc/info_modify.html',locals())
    
#----我的供求信息
def myrc_products(request):
    webtitle="生意管家"
    nowlanmu="<a href='/myrc/'>生意管家</a>"
    zzm.weixinautologin(request,request.GET.get("weixinid"))
    username=request.session.get("username",None)
    company_id=request.session.get("company_id",None)
    if (username==None or (company_id==None or str(company_id)=="0")):
        return HttpResponseRedirect("/login/?done=/myrc/products.html")
    page=request.GET.get("page")
    checkStatus=request.GET.get("checkStatus")
    if not checkStatus:
        checkStatus=''
    is_pause=request.GET.get("is_pause")
    
    if not page:
        page=1
    funpage = zz91page()
    limitNum=funpage.limitNum(5)
    nowpage=funpage.nowpage(int(page))
    frompageCount=funpage.frompageCount()
    after_range_num = funpage.after_range_num(2)
    before_range_num = funpage.before_range_num(9)
    qlistall=zzm.getmyproductslist(frompageCount=frompageCount,limitNum=limitNum,company_id=company_id,checkStatus=checkStatus,is_pause=is_pause)
    qlist=qlistall['list']
    qlistcount=qlistall['count']
    listcount=qlistcount
    if (int(listcount)>100000):
        listcount=100000
    listcount = funpage.listcount(listcount)
    page_listcount=funpage.page_listcount()
    firstpage = funpage.firstpage()
    lastpage = funpage.lastpage()
    page_range  = funpage.page_range()
    nextpage = funpage.nextpage()
    prvpage = funpage.prvpage()
    #审核通过
    sql1="select count(0) from products where company_id=%s and is_del=0 and is_pause=0"
    result1=dbc.fetchonedb(sql1,[company_id])
    if result1:
        alist=result1[0]
    #审核通过
    sql1="select count(0) from products where company_id=%s and check_status=1 and is_del=0 and is_pause=0"
    result1=dbc.fetchonedb(sql1,[company_id])
    if result1:
        alist1=result1[0]
    #审核中
    sql0="select count(0) from products where company_id=%s and check_status=0 and is_del=0 and is_pause=0"
    result0=dbc.fetchonedb(sql0,[company_id])
    if result0:
        alist0=result0[0]
    #审核未通过
    sql2="select count(0) from products where company_id=%s and check_status=2 and is_del=0 and is_pause=0"
    result2=dbc.fetchonedb(sql2,[company_id])
    if result2:
        alist2=result2[0]
    #暂停发布
    alist3=0
    sql3="select count(0) from products where company_id=%s and is_pause=1 and is_del=0"
    result3=dbc.fetchonedb(sql3,[company_id])
    if result3:
        alist3=result3[0]
    statustext="全部供求"
    #底部分页位置
    pagebottom=""
    #是否显示checkclick
    ischeckbox=None
    ismodify=1
    if not checkStatus and not is_pause:
        pagebottom="bottom:0px"
    if checkStatus=="1":
        statustext="审核通过("+str(alist1)+")"
        ischeckbox=1
    if checkStatus=="2":
        statustext="审核未通过("+str(alist2)+")"
        pagebottom="bottom:0px"
    if checkStatus=="0":
        statustext="审核中("+str(alist0)+")"
        pagebottom="bottom:0px"
        ismodify=None
    if is_pause:
        statustext="暂停发布("+str(alist3)+")"
        ischeckbox=1
    #return render_to_response('myrc/myrc_products.html',locals())
    return render_to_response('aui/myrc/products.html',locals())
#---刷新供求
def products_refurbish(request):
    gmt_created=datetime.datetime.now()
    proid=request.POST.get("proid")
        
    username=request.session.get("username",None)
    company_id=request.session.get("company_id",None)
    if (username==None or (company_id==None or str(company_id)=="0")):
        list={'err':'login'}
        return HttpResponse(simplejson.dumps(list, ensure_ascii=False))
    if proid=="0" or proid==None:
        messagedata={'err':'true','errkey':'请选择一条供求刷新'}
    else:
        messagedata={'err':'false','errkey':'','type':'proreflush'}
        sql="update products set refresh_time=%s,gmt_modified=%s where id in (%s) and company_id = %s"
        dbc.updatetodb(sql,[gmt_created,gmt_created,str(proid),company_id])
        
    return HttpResponse(simplejson.dumps(messagedata, ensure_ascii=False))
#---刷新供求
def products_refurbishall(request):
    gmt_created=datetime.datetime.now()
    username=request.session.get("username",None)
    company_id=request.session.get("company_id",None)
    if (username==None or (company_id==None or str(company_id)=="0")):
        list={'err':'login'}
        return HttpResponse(simplejson.dumps(list, ensure_ascii=False))
    if not company_id:
        company_id=request.POST.get("company_id")
    if company_id=="0" or company_id==None:
        messagedata={'err':'true','errkey':'系统错误'}
    else:
        messagedata={'err':'false','errkey':'','type':'proreflush'}
        sql="update products set refresh_time=%s,gmt_modified=%s where company_id = %s and check_status='1'"
        dbc.updatetodb(sql,[gmt_created,gmt_created,company_id])
    return HttpResponse(simplejson.dumps(messagedata, ensure_ascii=False))
#---暂不发布
def products_stop(request):
    gmt_created=datetime.datetime.now()
    proid=request.POST.get("proid")
    username=request.session.get("username",None)
    company_id=request.session.get("company_id",None)
    if (username==None or (company_id==None or str(company_id)=="0")):
        list={'err':'login'}
        return HttpResponse(simplejson.dumps(list, ensure_ascii=False))
    if proid=="0" or proid==None:
        messagedata={'err':'true','errkey':'请选择一条供求'}
    else:
        messagedata={'err':'false','errkey':'','type':'prostop'}
        sql="update products set is_pause=1,gmt_modified=%s where id in (%s) and company_id = %s"
        dbc.updatetodb(sql,[gmt_created,str(proid),company_id])
        
    return HttpResponse(simplejson.dumps(messagedata, ensure_ascii=False))
#---重新发布
def products_start(request):
    gmt_created=datetime.datetime.now()
    proid=request.POST.get("proid")
    username=request.session.get("username",None)
    company_id=request.session.get("company_id",None)
    if (username==None or (company_id==None or str(company_id)=="0")):
        list={'err':'login'}
        return HttpResponse(simplejson.dumps(list, ensure_ascii=False))
    if proid=="0" or proid==None:
        messagedata={'err':'true','errkey':'请选择一条供求信息后操作！'}
    else:
        messagedata={'err':'false','errkey':'','type':'prorestart'}
        sql="update products set is_pause=0,gmt_modified=%s where id in (%s) and company_id = %s"
        dbc.updatetodb(sql,[gmt_created,str(proid),company_id])
        
    return HttpResponse(simplejson.dumps(messagedata, ensure_ascii=False))
#----修改供求
def products_update(request):
    saveform="products_updatesave"
    proid=request.GET.get("proid")
    username=request.session.get("username",None)
    company_id=request.session.get("company_id",None)
    if (username==None or (company_id==None or str(company_id)=="0")):
        return HttpResponseRedirect("/login/?done=/myrc/proupdate.html")
    prodetail=getmyproductsbyid(proid)
    #供求类别
    procategory=getcategory_products(prodetail['categorycode'])
    #信息有效期
    proexpire=getproducts_expire(proid)
    
    #是否购买显示联系方式
    isshowphone=zzq.getisbuyshowphone(company_id)
    #是否高会
    isvip=zzq.getiszstcompany(company_id)
    #是否来电宝
    isldb=zzc.getisldb(company_id)
    showphone=1
    if isshowphone or isvip or isldb:
        showphone=None
    return render_to_response('aui/myrc/products_update.html',locals())
#----供求属性
def products_propertylist(request):
    proid=request.GET.get("proid")
    propertylist=[]
    if proid:
        propertylist=getproducts_property(proid)
    return HttpResponse(simplejson.dumps(propertylist, ensure_ascii=False))
#----供求图片
def products_picturelist(request):
    username=request.session.get("username",None)
    company_id=request.session.get("company_id",None)
    if (username==None or (company_id==None or str(company_id)=="0")):
        list={'err':'login'}
        return HttpResponse(simplejson.dumps(list, ensure_ascii=False))
    proid=request.GET.get("proid")
    sql="select id,pic_address from products_pic where product_id=%s"
    result=dbc.fetchalldb(sql,[proid])
    listall=[]
    for list in result:
        address=list[1]
        filetype=address.split(".")[-1]
        if (filetype.lower() in ["mp4","mov","avi","3gp","3gp2","wav","rm","mpg","asf","mid"]):
            mediatype="video"
            picurl="http://img.zz91.com/"+address
        else:
            mediatype="pic"
            picurl="http://img3.zz91.com/300x1500/"+address
        l={'id':list[0],'address':address,'picurl':picurl,'mediatype':mediatype}
        listall.append(l)
    return HttpResponse(simplejson.dumps(listall, ensure_ascii=False))
#----图片删除
def products_delpicture(request):
    pid=request.GET.get("pid")
    proid=request.GET.get("proid")
    username=request.session.get("username",None)
    company_id=request.session.get("company_id",None)
    if (username==None or (company_id==None or str(company_id)=="0")):
        list={'err':'login'}
        return HttpResponse(simplejson.dumps(list, ensure_ascii=False))
    list={'err':'true'}
    if pid and proid:
        sql="insert into products_pic_del select * from products_pic where id=%s and not exists(select id from products_pic_del where id=products_pic.id)"
        dbc.updatetodb(sql,[id])
        sql="delete from products_pic where id=%s and product_id=%s"
        dbc.updatetodb(sql,[pid,proid])
        list={'err':'false'}
    return HttpResponse(simplejson.dumps(list, ensure_ascii=False))
    
#绑定微信服务号
def myrc_bindweixin(request):
    webtitle="生意管家"
    nowlanmu="<a href='/myrc/'>生意管家</a>"
    username=request.session.get("username",None)
    company_id=request.session.get("company_id",None)
    if (username==None or (company_id==None or str(company_id)=="0")):
        return HttpResponseRedirect("/login/?done=/myrc/products.html")
    gmt_created=datetime.datetime.now()
    loginqrcode=request.session.get("loginqrcode",None)
    loginticket=request.session.get("loginticket",None)
    logintime=request.session.get("logintime",None)
    #gmtnow=getNow()
    #gmtnow = time.time()
    #weixintime=gmtnow-int(cache.get("weixintime"+weixinconfig['zz91service']['appid']))
    if not loginqrcode or not loginticket or not logintime:
        account=username
        loginqrcode = random.randint(1000000, 99999999)
        #request.session.set_expiry(60*10)
        request.session['loginqrcode']=loginqrcode
        qrcode=loginqrcode
        sqlb="select id from weixin_pclogin where account=%s and qrcode=%s and TIMESTAMPDIFF(MINUTE,gmt_created,now())<10"
        resultc=dbc.fetchonedb(sqlb,[account,qrcode])
        if not resultc:
            loginqrcode = qrcode = random.randint(1000000, 99999999)
            #request.session.set_expiry(60*10)
            request.session['loginqrcode']=loginqrcode
            sqlp="insert into weixin_pclogin (openid,account,loginflag,gmt_created,qrcode) values(%s,%s,%s,%s,%s)"
            dbc.updatetodb(sqlp,["",account,2,gmt_created,qrcode])
        else:
            sql="update weixin_pclogin set loginflag=2,gmt_created=%s where id=%s"
            dbc.updatetodb(sql,[gmt_created,resultc[0]])
        
        wxc = Client(weixinconfig['zz91service']['appid'], weixinconfig['zz91service']['secret'])
        data={"expire_seconds": 700, "action_name": "QR_SCENE", "action_info": {"scene": {"scene_id": loginqrcode}}}
        token=wxc.create_qrcode(data)
        difmin=0
        loginticket=token['ticket']
        request.session['loginticket']=loginticket
        request.session['logintime']=date_to_strall(gmt_created)
    else:
        gmtnow=getNow()
        '''判断是否是一个有效的日期字符串'''
        try:
            time.strptime(logintime, "%Y-%m-%d")
            logintime=date_to_int(logintime)
        except:
            logintime=str_to_int(logintime)

        difmin=date_to_int(gmtnow)-logintime
        if difmin>600:
            account=username
            loginqrcode = qrcode = random.randint(1000000, 99999999)
            #request.session.set_expiry(60*10)
            request.session['loginqrcode']=loginqrcode
            sqlp="insert into weixin_pclogin (openid,account,loginflag,gmt_created,qrcode) values(%s,%s,%s,%s,%s)"
            dbc.updatetodb(sqlp,["",account,2,gmt_created,qrcode])
            
            wxc = Client(weixinconfig['zz91service']['appid'], weixinconfig['zz91service']['secret'])
            data={"expire_seconds": 700, "action_name": "QR_SCENE", "action_info": {"scene": {"scene_id": loginqrcode}}}
            token=wxc.create_qrcode(data)
            loginticket=token['ticket']
            request.session['loginticket']=loginticket
            request.session['logintime']=date_to_strall(gmt_created)
            difmin=0
        else:
            loginticket=request.session.get("loginticket",None)
    img="https://mp.weixin.qq.com/cgi-bin/showqrcode?ticket="+loginticket
    return render_to_response('myrc/bindweixin.html',locals())
#我的收藏夹
def myrc_favorite(request):
    webtitle="生意管家"
    nowlanmu="<a href='/myrc_index/'>生意管家</a>"
    weixinautologin(request,request.GET.get("weixinid"))
    username=request.session.get("username",None)
    company_id=request.session.get("company_id",None)
    if (username==None or (company_id==None or str(company_id)=="0")):
        return HttpResponseRedirect("/login/?done=/myrc/favorite.html")
    #选择状态标签页
    statuslist={'0':'全部','1':'供求','2':'公司','3':'报价','4':'社区','5':'资讯'}
    checkStatus=request.GET.get("checkStatus")
    
    if (checkStatus=="" or checkStatus==None):
        checkStatus=0
    statustext=statuslist[str(checkStatus)]
    page=request.GET.get("page")
    if (page==None):
        page=1
    funpage = zz91page()
    limitNum=funpage.limitNum(20)
    nowpage=funpage.nowpage(int(page))
    frompageCount=funpage.frompageCount()
    after_range_num = funpage.after_range_num(2)
    before_range_num = funpage.before_range_num(9)
    qlistall=getfavoritelist(frompageCount,limitNum,company_id,checkStatus)
    qlist=qlistall['list']
    qlistcount=qlistall['count']
    listcount=qlistcount
    if (int(listcount)>100000):
        listcount=100000
    listcount = funpage.listcount(listcount)
    page_listcount=funpage.page_listcount()
    firstpage = funpage.firstpage()
    lastpage = funpage.lastpage()
    page_range  = funpage.page_range()
    nextpage = funpage.nextpage()
    prvpage = funpage.prvpage()
    
    #供求信息数量
    sql1="select count(0) from myfavorite where company_id=%s "
    result1=dbc.fetchonedb(sql1,[company_id])
    if result1:
        alist=result1[0]
    #供求信息数量
    sql1="select count(0) from myfavorite where company_id=%s and favorite_type_code in (10091006,10091000,10091001,10091007)"
    result1=dbc.fetchonedb(sql1,[company_id])
    if result1:
        alist1=result1[0]
    #公司信息数量    
    sql2="select count(0) from myfavorite where company_id=%s and favorite_type_code in (10091002,10091003) "
    result2=dbc.fetchonedb(sql2,[company_id])
    if result2:
        alist2=result2[0]
    #报价信息数量    
    sql3="select count(0) from myfavorite where company_id=%s and favorite_type_code=10091004 "
    result3=dbc.fetchonedb(sql3,[company_id])
    if result3:
        alist3=result3[0]
    #互助社区数量
    sql4="select count(0) from myfavorite where company_id=%s and favorite_type_code=10091005 "
    result4=dbc.fetchonedb(sql4,[company_id])
    if result4:
        alist4=result4[0]
    #资讯中心数量
    sql5="select count(0) from myfavorite where company_id=%s and favorite_type_code=10091012 "
    result5=dbc.fetchonedb(sql5,[company_id])
    if result5:
        alist5=result5[0]    
    
    #return render_to_response('myrc_favorite.html',locals())
    return render_to_response('aui/myrc/favorite.html',locals())
#----删除我的收藏
def myrc_favorite_del(request):
    webtitle="生意管家"
    nowlanmu="<a href='/myrc_index/'>生意管家</a>"
    weixinautologin(request,request.GET.get("weixinid"))
    username=request.session.get("username",None)
    company_id=request.session.get("company_id",None)
    if (username==None or (company_id==None or str(company_id)=="0")):
        return HttpResponseRedirect("/login/?done=/myrc/favorite.html")
    request_url=request.META.get('HTTP_REFERER','/')
    favid=request.GET.get('favid')
    sql='delete from myfavorite where id=%s and company_id=%s'
    dbc.updatetodb(sql,[favid,company_id])
    return HttpResponseRedirect(request_url)
def mobile_bunding(request):
    return render_to_response('aui/myrc/mobile_bunding.html',locals())
def mobile_unbunding(request):
    host=getnowurl(request)
    username=request.session.get("username",None)
    company_id=request.session.get("company_id",None)
    if username and (company_id==None or str(company_id)=="0"):
        company_id=getcompanyid(username)
        request.session['company_id']=company_id
    if (username==None or (company_id==None or str(company_id)=="0")):
        return HttpResponseRedirect("/login/?done="+host)
    mobile=''
    sql="select mobile from company_account where company_id=%s"
    result=dbc.fetchonedb(sql,[company_id])
    if result:
        mobile=result[0]
    return render_to_response('aui/myrc/mobile_unbunding.html',locals())
def mobile_login(request):
    return render_to_response('aui/myrc/mobile_login.html',locals())
#手机验证码快速登录
def mobile_loginof(request):
    company_id=request.POST.get("company_id")
    if not company_id:
        messagedata={'err':'true','errkey':'手机号码未注册或错误！'}
        return HttpResponse(simplejson.dumps(messagedata, ensure_ascii=False))
    yzcode = request.POST.get('yzcode')
    mobile=request.POST.get("mobile")
    sql="select id from auth_forgot_password where userid=%s and auth_key=%s and TIMESTAMPDIFF(MINUTE,gmt_created,now())<600"
    plist=dbc.fetchonedb(sql,[company_id,yzcode]);
    if (plist):
        sql="select id from company where id=%s and is_block=1"
        list=dbc.fetchonedb(sql,[company_id]);
        if list:
            messagedata={'err':'true','errkey':'改账号已被禁用！'}
            return HttpResponse(simplejson.dumps(messagedata, ensure_ascii=False))
        
        sqlc="select id,account from company_account where mobile=%s"
        list=dbc.fetchonedb(sqlc,[mobile]);
        if list:
            errkey=""
            err="false"
            username=list[1]
            request.session.set_expiry(6000*6000)
            request.session['username']=username
            request.session['company_id']=company_id
            messagedata={'err':err,'errkey':errkey}
            return HttpResponse(simplejson.dumps(messagedata, ensure_ascii=False))
        
        sql="select id,username from auth_user where (mobile=%s or username=%s or account=%s)"
        list=dbc.fetchonedb(sql,[mobile,mobile,mobile]);
        if list:
            username=list[1]
            errkey=""
            err="false"
            request.session.set_expiry(6000*6000)
            request.session['username']=username
            request.session['company_id']=company_id
            messagedata={'err':err,'errkey':errkey}
            
            return HttpResponse(simplejson.dumps(messagedata, ensure_ascii=False))
        
        errkey="手机号码未注册或错误"
        err="true"
    else:
        errkey="你输入的验证码错误！"
        err="true"
    messagedata={'err':err,'errkey':errkey}
    return HttpResponse(simplejson.dumps(messagedata, ensure_ascii=False))
#解绑手机，验证码
def auth_yzmcode(request):
    webtitle="生意管家"
    nowlanmu="<a href='/myrc/'>生意管家</a>"
    username=request.session.get("username",None)
    company_id=request.session.get("company_id",None)
    messagedata={'err':'true','errkey':'未登录'}
    mobilemod = request.POST.get('mobile')
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
                errkey="发送成功"
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
                    errkey="发送成功"
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
    if company_id:
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
                errkey="系统错误！"
                err="true"
        else:
            errkey="系统错误，账号不存在！"
            err="true"
        messagedata={'err':err,'errkey':errkey}
    return HttpResponse(simplejson.dumps(messagedata, ensure_ascii=False))
#解绑手机
def auth_unbundlingmobile(request):
    username=request.session.get("username",None)
    company_id=request.session.get("company_id",None)
    if (username==None or (company_id==None or str(company_id)=="0")):
        errlist={'login':'false'}
        return HttpResponse(simplejson.dumps(errlist, ensure_ascii=False))
    yzcode = request.POST.get('yzcode')
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
    username=request.session.get("username",None)
    company_id=request.session.get("company_id",None)
    if (username==None or (company_id==None or str(company_id)=="0")):
        errlist={'login':'false'}
        return HttpResponse(simplejson.dumps(errlist, ensure_ascii=False))
    yzcode = request.POST.get('yzcode')
    mobile=request.POST.get("mobile")
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
#修改密码
def resetpasswd(request):
    username=request.session.get("username",None)
    company_id=request.session.get("company_id",None)
    if (username==None or (company_id==None or str(company_id)=="0")):
        errlist={'login':'false'}
        company_id=request.POST.get("company_id")
        if not company_id:
            return HttpResponse(simplejson.dumps(errlist, ensure_ascii=False))
    sedcold=request.POST.get('sedcold')
    newcold=request.POST.get('newcold')
    yzcode = request.POST.get('yzcode')
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
    messagedata={"err":"true","errkey":"验证码错误或过期！"}
    if plist:
        md5pwd_pass = hashlib.md5(sedcold)
        md5passwd = md5pwd_pass.hexdigest()[8:-8]
        account=getcompanyaccount(company_id)
        sql="update auth_user set password=%s,gmt_modified=%s where username=%s"
        dbc.updatetodb(sql,[md5passwd,gmt_modified,account]);
        sql="update company_account set password=%s,gmt_modified=%s where account=%s"
        dbc.updatetodb(sql,[newcold,gmt_modified,account]);
        messagedata={"err":"false","errkey":"修改成功！"}
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
#加入通信录
def myrc_addressbook_join(request):
    host=getnowurl(request)
    zzm.weixinautologin(request,request.GET.get("weixinid"))
    username=request.session.get("username",None)
    company_id=request.session.get("company_id",None)
    if username and (company_id==None or str(company_id)=="0"):
        company_id=getcompanyid(username)
        request.session['company_id']=company_id
    if (username==None or (company_id==None or str(company_id)=="0")):
        errlist={'err':'login'}
        return HttpResponse(simplejson.dumps(errlist, ensure_ascii=False))
    forcompany_id=request.GET.get("forcompany_id")
    sql="select id from company_addressbook where company_id=%s and forcompany_id=%s"
    result=dbc.fetchonedb(sql,[company_id,forcompany_id])
    gmt_created=datetime.datetime.now()
    if not result:
        sqlc="insert into company_addressbook(company_id,forcompany_id,gmt_created) values(%s,%s,%s)"
        dbc.updatetodb(sqlc,[company_id,forcompany_id,gmt_created])
        messagedata={'err':'false','errkey':'加入成功！'}
    else:
        messagedata={'err':'true','errkey':'已经加入！'}
    return HttpResponse(simplejson.dumps(messagedata, ensure_ascii=False))
#收藏
def favorite_save(request):
    username=request.session.get("username",None)
    company_id=request.session.get("company_id",None)
    if (username==None or (company_id==None or str(company_id)=="0")):
        errlist={'err':'login'}
        return HttpResponse(simplejson.dumps(errlist, ensure_ascii=False))
    account=getcompanyaccount(company_id)
    
    cid=request.GET.get("forcompany_id")
    pdtid=request.GET.get("pdtid")
    products_type_code=request.GET.get("products_type_code")
    favorite_type_code=request.GET.get("favorite_type_code")
    favoriteflag=request.GET.get("favoriteflag")
    
    if favorite_type_code==None or favorite_type_code=="":
        if (pdtid==None or pdtid=='None'):
            favorite_type_code="10091002"
            content_id=cid
            
        else:
            if (products_type_code=="10331000"):
                favorite_type_code="10091006"
            if (products_type_code=="10331001"):
                favorite_type_code="10091006"
            content_id=pdtid
        #加入通信录
        if cid:
            zzc.joinaddressbook(company_id,cid)
    else: 
        content_id=request.GET.get("content_id")
    if not content_id:
        content_id=0
        
    content_title=request.GET.get("title")
    if not content_title:
        content_title="err"
    if str(favoriteflag)=="1":
        sql="delete from myfavorite where favorite_type_code=%s and content_id=%s and company_id=%s"
        dbc.updatetodb(sql,[favorite_type_code,content_id,company_id]);
        messagedata={'err':'false','errkey':'取消成功','type':'favorite'}
        return HttpResponse(simplejson.dumps(messagedata, ensure_ascii=False))
    gmt_created=datetime.datetime.now()
    gmt_modified=datetime.datetime.now()

    value=[favorite_type_code,content_id,content_title,gmt_created,gmt_modified,company_id,account]
    sql="select id from myfavorite where favorite_type_code=%s and content_id=%s and company_id=%s"
    clist=dbc.fetchonedb(sql,[favorite_type_code,content_id,company_id])
    if (clist):
        sucflag=None
    else:
        sql="insert into myfavorite(favorite_type_code,content_id,content_title,gmt_created,gmt_modified,company_id,account) values(%s,%s,%s,%s,%s,%s,%s)"
        dbc.updatetodb(sql,value);
        sucflag=1
    messagedata={'err':'false','errkey':'收藏成功','type':'favorite'}
    return HttpResponse(simplejson.dumps(messagedata, ensure_ascii=False))
#----我的留言
def myrc_xunpan(request):
    webtitle="生意管家"
    nowlanmu="<a href='/myrc/'>生意管家</a>"
    weixinautologin(request,request.GET.get("weixinid"))
    sendtype=request.GET.get("sendtype")
    if sendtype==None:
        sendtype="0"
    username=request.session.get("username",None)
    company_id=request.session.get("company_id",None)
    if str(company_id)=="0":
        company_id=getcompanyid(username)
        request.session['company_id']=company_id
    if not username:
        return HttpResponseRedirect("/login/?done=/myrc/xunpan.html")
    #----更新弹窗
    #updateopenfloat(company_id,1)
    zzms.updatemessagesall(company_id)
    page=request.GET.get("page")
    if (page==None):
        page=1
    funpage = zz91page()
    limitNum=funpage.limitNum(20)
    nowpage=funpage.nowpage(int(page))
    frompageCount=funpage.frompageCount()
    after_range_num = funpage.after_range_num(2)
    before_range_num = funpage.before_range_num(9)
    qlistall=zzms.getxunpanlist(frompageCount=frompageCount,limitNum=limitNum,company_id=company_id,sendtype=sendtype)
    qlist=qlistall['list']
    qlistcount=qlistall['count']
    listcount=qlistcount
    if (int(listcount)>100000):
        listcount=100000
    listcount = funpage.listcount(listcount)
    page_listcount=funpage.page_listcount()
    firstpage = funpage.firstpage()
    lastpage = funpage.lastpage()
    page_range  = funpage.page_range()
    nextpage = funpage.nextpage()
    prvpage = funpage.prvpage()
    #return render_to_response('myrc_leavewords.html',locals())
    return render_to_response('aui/myrc/xunpan.html',locals())
#----我的留言回复
def myrc_xunpan_reply(request):
    webtitle="留言回复"
    nowlanmu="<a href='/myrc/'>生意管家</a>"
    username=request.session.get("username",None)
    company_id=request.GET.get("company_id")
    inquired_id=request.GET.get("inquired_id")
    send_company_id=request.session.get("company_id",None)
    if (username==None or (company_id==None or str(company_id)=="0")):
        return HttpResponseRedirect("/login/?done=/myrc/xunpan_reply.html?company_id="+str(company_id)+"&inquired_id="+str(inquired_id))
    if (company_id=="" or (company_id==None or str(company_id)=="0")):
        syserr=1
    
    if str(send_company_id)!=str(company_id):
        sendflag=1
    getupdatelookquestion(inquired_id)
    qlist=getleavewords(inquired_id)
    return render_to_response('aui/myrc/xunpan_reply.html',locals())
#----留言回复保存
def myrc_xunpan_save(request):
    send_username=request.session.get("username",None)
    send_company_id=request.session.get("company_id",None)
    username=request.session.get("username",None)
    company_id=request.session.get("company_id",None)
    if (username==None or (company_id==None or str(company_id)=="0")):
        errlist={'err':'login'}
        return HttpResponse(simplejson.dumps(errlist, ensure_ascii=False))
    if send_username and send_company_id==None:
        send_company_id=getcompanyid(send_username)
        request.session['company_id']=send_company_id
    re_company_id = request.POST.get('forcompany_id')
    backurl=request.POST.get('backurl')
    title='回复留言！'
    content = request.POST.get('content')
    errflag=None
    if (content=="" or content==None):
        errflag=1
    if (errflag==None):
        be_inquired_type=request.POST.get('be_inquired_type')
        be_inquired_id=request.POST.get('be_inquired_id')
        inquired_type=0
        sender_account=send_username
        receiver_account=getcompanyaccount(re_company_id)
        send_time=datetime.datetime.now()
        gmt_created=datetime.datetime.now()
        gmt_modified=datetime.datetime.now()
        value=[title,content,be_inquired_type,be_inquired_id,inquired_type,sender_account,receiver_account,send_time,gmt_created,gmt_modified]
        sql="insert into inquiry(title,content,be_inquired_type,be_inquired_id,inquired_type,sender_account,receiver_account,send_time,gmt_created,gmt_modified) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        dbc.updatetodb(sql,value);
        #----更新弹窗
        #updateopenfloat(re_company_id,0)
        messagedata={'err':'false','errkey':'','type':'tradesave'}
        return HttpResponse(simplejson.dumps(messagedata, ensure_ascii=False))
    messagedata={'err':'true','errkey':'请填写留言内容！'}
    return HttpResponse(simplejson.dumps(messagedata, ensure_ascii=False))

#----我的社区
def myrc_community(request):
    webtitle="消息中心"
    nowlanmu="<a href='/myrc/'>生意管家</a>"
    company_id=request.session.get("company_id",None)
    username=request.session.get("username",None)
    if username and (company_id==None or str(company_id)=="0"):
        company_id=getcompanyid(username)
        request.session['company_id']=company_id
    if (username==None or (company_id==None or str(company_id)=="0")):
        return HttpResponseRedirect("/login/?done=/myrc/community.html")
    #----更新弹窗
    #updateopenfloat(company_id,1)
    #判断是否已经填写了昵称
    mynickname=getcompanynickname(company_id)
    if not mynickname or mynickname=="":
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
    """
    #邀请回答
    invitelist=getbbs_invite(company_id)
    if invitelist:
        invitecount=len(invitelist)
    else:
        invitecount=0
    """
    page=request.GET.get("page")
    if (page==None):
        page=1
    funpage = zz91page()
    limitNum=funpage.limitNum(5)
    nowpage=funpage.nowpage(int(page))
    frompageCount=funpage.frompageCount()
    after_range_num = funpage.after_range_num(2)
    before_range_num = funpage.before_range_num(9)
    huzhureply=getmessgelist(company_id,frompageCount,limitNum)
    if huzhureply:
        listall=huzhureply['list']
        count=huzhureply['count']
    listcount=huzhureply['count']
    if (int(listcount)>100000):
        listcount=100000
    listcount = funpage.listcount(listcount)
    page_listcount=funpage.page_listcount()
    firstpage = funpage.firstpage()
    lastpage = funpage.lastpage()
    page_range  = funpage.page_range()
    nextpage = funpage.nextpage()
    prvpage = funpage.prvpage()
    myrc_type="myrccommunity"
    #return render_to_response('myrc/myrc_mycommunity.html',locals())
    return render_to_response('aui/myrc/community.html',locals())
#---查看我的回复
def myrc_viewreply(request):
    reply_id=request.GET.get("reply_id")
    tourl=request.GET.get("tourl")
    company_id=request.session.get("company_id",None)
    username=request.session.get("username",None)
    if username and (company_id==None or str(company_id)=="0"):
        company_id=getcompanyid(username)
        request.session['company_id']=company_id
    if (username==None or (company_id==None or str(company_id)=="0")):
        return HttpResponseRedirect("/login/?done=/myrc/viewreply.html^wenhao^reply_id="+str(reply_id)+"&tourl="+str(tourl))
    
    sql="select viewlist from bbs_post_reply_view where company_id=%s"
    result=dbc.fetchonedb(sql,[company_id])
    if result:
        viewlist=result[0]
        viewlist=eval(viewlist)
        if str(reply_id) in viewlist.keys():
            viewlist.pop(reply_id)
        
        sql="update bbs_post_reply_view set viewlist=%s where company_id=%s"
        dbc.updatetodb(sql,[str(viewlist),company_id])
    tourl=tourl.replace("^and^","&")
    tourl=tourl.replace("^wenhao^","?")
    tourl=tourl.replace("%5Eand%5E","&")
    tourl=tourl.replace("^jing^","#")
    return HttpResponseRedirect(tourl)
    
    
#----我发布的互助信息
def myrc_mypost(request):
    webtitle="我的提问"
    nowlanmu="<a href='/myrc/'>生意管家</a>"
    company_id=request.session.get("company_id",None)
    username=request.session.get("username",None)
    if username and (company_id==None or str(company_id)=="0"):
        company_id=getcompanyid(username)
        request.session['company_id']=company_id
    if (username==None or (company_id==None or str(company_id)=="0")):
        return HttpResponseRedirect("/login/?done=/myrc/mypost.html")
    #未查看数
    notviewcount=getnoviewreplycount(company_id)
    
    page=request.GET.get("page")
    if (page==None):
        page=1
    funpage = zz91page()
    limitNum=funpage.limitNum(20)
    nowpage=funpage.nowpage(int(page))
    frompageCount=funpage.frompageCount()
    after_range_num = funpage.after_range_num(2)
    before_range_num = funpage.before_range_num(9)
    myquestion=getmyquestion(company_id,frompageCount,limitNum)
    if myquestion:
        listall=myquestion['list']
        count=myquestion['count']
    listcount=myquestion['count']
    if listcount:
        if (int(listcount)>100000):
            listcount=100000
    listcount = funpage.listcount(listcount)
    page_listcount=funpage.page_listcount()
    firstpage = funpage.firstpage()
    lastpage = funpage.lastpage()
    page_range  = funpage.page_range()
    nextpage = funpage.nextpage()
    prvpage = funpage.prvpage()
    #return render_to_response('myrc/myrc_mypost.html',locals())
    return render_to_response('aui/myrc/mypost.html',locals())

#----我的回复
def myrc_myreply(request):
    webtitle="我的回复"
    nowlanmu="<a href='/myrc/'>生意管家</a>"
    company_id=request.session.get("company_id",None)
    username=request.session.get("username",None)
    if username and (company_id==None or str(company_id)=="0"):
        company_id=getcompanyid(username)
        request.session['company_id']=company_id
    if (username==None or (company_id==None or str(company_id)=="0")):
        return HttpResponseRedirect("/login/?done=/myrc/myreply.html")
    #未查看数
    notviewcount=getnoviewreplycount(company_id)
    page=request.GET.get("page")
    if (page==None):
        page=1
    funpage = zz91page()
    limitNum=funpage.limitNum(5)
    nowpage=funpage.nowpage(int(page))
    frompageCount=funpage.frompageCount()
    after_range_num = funpage.after_range_num(2)
    before_range_num = funpage.before_range_num(9)
    myreply=getmyreply(company_id,frompageCount,limitNum)
    if myreply:
        listall=myreply['list']
        count=myreply['count']
    listcount=myreply['count']
    if (int(listcount)>100000):
        listcount=100000
    listcount = funpage.listcount(listcount)
    page_listcount=funpage.page_listcount()
    firstpage = funpage.firstpage()
    lastpage = funpage.lastpage()
    page_range  = funpage.page_range()
    nextpage = funpage.nextpage()
    prvpage = funpage.prvpage()
    myrc_type="myrc_myreply"
    #return render_to_response('myrc/myrc_myreply.html',locals())
    return render_to_response('aui/myrc/myreply.html',locals())

#----我的关注
def myrc_myguanzhu(request):
    webtitle="我的关注"
    nowlanmu="<a href='/myrc/'>生意管家</a>"
    company_id=request.session.get("company_id",None)
    username=request.session.get("username",None)
    if username and (company_id==None or str(company_id)=="0"):
        company_id=getcompanyid(username)
        request.session['company_id']=company_id
    if (username==None or (company_id==None or str(company_id)=="0")):
        return HttpResponseRedirect("/login/?done=/myrc/myguanzhu.html")
    
    #未查看数
    notviewcount=getnoviewreplycount(company_id)
    page=request.GET.get("page")
    if (page==None):
        page=1
    funpage = zz91page()
    limitNum=funpage.limitNum(5)
    nowpage=funpage.nowpage(int(page))
    frompageCount=funpage.frompageCount()
    after_range_num = funpage.after_range_num(2)
    before_range_num = funpage.before_range_num(9)
    qlistall=getmygaunzhu(company_id,frompageCount,limitNum)
    listall=qlistall['list']
    listcount=qlistall['count']

    if (int(listcount)>100000):
        listcount=100000
    listcount = funpage.listcount(listcount)
    page_listcount=funpage.page_listcount()
    firstpage = funpage.firstpage()
    lastpage = funpage.lastpage()
    page_range  = funpage.page_range()
    nextpage = funpage.nextpage()
    prvpage = funpage.prvpage()
    return render_to_response('aui/myrc/myguanzhu.html',locals())
