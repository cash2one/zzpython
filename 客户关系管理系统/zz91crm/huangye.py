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
execfile(nowpath+"/func/company_function.py")
execfile(nowpath+"/func/crmtools.py")
zzc=customer()

def hy_add(request):
    request_url=request.META.get('HTTP_REFERER','/')
    addaction="add"
    id=0
    pcheck=0
    username=request.session.get('username',default=None)
    user_id=request.session.get('user_id',default=None)
    if not username or not user_id:
        return HttpResponseRedirect("/icd/relogin.html")
    account=request.POST.get("account")
    if not account:
        account=''
    com_id=request.GET.get("com_id")
    huangye_qukan=request.session.get('huangye_qukan',default='')
    result=None
    if account:
        sql="select c.id,c.name,c.business,b.contact,b.mobile,c.address,b.weixin,b.sex,a.label,b.account,c.area_code from company as c left join company_account as b on c.id=b.company_id left join category as a on a.code=c.area_code where b.account=%s"
        result=db.fetchonedb(sql,[account])
    if com_id:
        sql="select c.id,c.name,c.business,b.contact,b.mobile,c.address,b.weixin,b.sex,a.label,b.account,c.area_code from company as c left join company_account as b on c.id=b.company_id left join category as a on a.code=c.area_code where c.id=%s"
        result=db.fetchonedb(sql,[com_id])
    if result:
        company_id=result['id']
        comname=result['name']
        business=result['business']
        contact=result['contact']
        sex=result['sex']
        if sex=="0":
            sex="女士"
        if sex=="1":
            sex="男士"
        mobile=result['mobile']
        address=result['address']
        province=result['label']
        area_code=result['area_code']
        guowai=None
        if area_code:
            if area_code[0:8]!="10011000":
                guowai=1
        province_code=area_code[0:12]
        city_code=area_code[0:16]
        province=zzc.get_area_txt(province_code)
        city=zzc.get_area_txt(city_code)
        
        account=result['account']
    
    sql="select code,label from huangye_category"
    huangyequkanlist=db.fetchalldb(sql)
    
    return render_to_response('huangye/add.html',locals())
def hy_edit(request):
    request_url=request.META.get('HTTP_REFERER','/')
    username=request.session.get('username',default=None)
    user_id=request.session.get('user_id',default=None)
    if not username or not user_id:
        return HttpResponseRedirect("/icd/relogin.html")
    authqx=zzc.geauthid(user_id=user_id)
    checkflag=None
    if "16" in authqx:
        checkflag=1
    addaction="edit"
    id=request.GET.get("id")
    sql="select * from huangye_list where id=%s"
    result=db.fetchonedb(sql,[id])
    if result:
        company_id=result['com_id']
        account=result['com_email']
        comname=result['cname']
        business=result['cproductslist']
        contact=result['ccontactp']
        mobile=result['cmobile']
        address=result['cadd']
        province=result['province']
        comkeywords=result['comkeywords']
        js1=result['js1']
        js2=result['js2']
        sl1=result['sl1']
        sl2=result['sl2']
        qt1=result['qt1']
        qt2=result['qt2']
        weixin=result['weixin']
        user_id=result['personid']
        pcheck=result['pcheck']
        if province:
            provincelist=province.split("|")
            province=provincelist[0]
            city=provincelist[1]
        huangye_qukan=result['huangye_qukan']
    
    sql="select code,label from huangye_category"
    huangyequkanlist=db.fetchalldb(sql)
    return render_to_response('huangye/add.html',locals())
def hy_save(request):
    username=request.session.get('username',default=None)
    user_id=request.session.get('user_id',default=None)
    if not username or not user_id:
        return HttpResponseRedirect("/icd/relogin.html")
    huangye_qukan=request.POST.get("huangye_qukan")
    id=request.POST.get("id")
    comkeywords=request.POST.get("ckeywords")
    cname=request.POST.get("cname")
    account=request.POST.get("account")
    fdate=datetime.datetime.now()
    js1=request.POST.get("js1")
    js2=request.POST.get("js2")
    sl1=request.POST.get("sl1")
    sl2=request.POST.get("sl2")
    qt1=request.POST.get("qt1")
    qt2=request.POST.get("qt2")
    province=request.POST.get("province")
    addaction=request.POST.get("addaction")
    if not province:
        province=''
    city=request.POST.get("city")
    if not city:
        city=''
    province=province+"|"+city
    cproductslist=request.POST.get("cproductslist")
    ccontactp=request.POST.get("ccontactp")
    cmobile=request.POST.get("cmobile")
    weixin=request.POST.get("weixin")
    cadd=request.POST.get("cadd")
    personid=request.POST.get("lpersonid")
    pcheck=request.POST.get("pcheck")
    if not pcheck:
        pcheck=0
    com_id=request.POST.get("com_id")
    if not com_id:
        com_id=0
    if addaction=="add":
        sql="select id from huangye_list where com_email=%s and huangye_qukan=%s"
        result=db.fetchonedb(sql,[account,huangye_qukan])
        if not result:
            sql="insert into huangye_list(com_email,com_id,cname,comkeywords,js1,js2,sl1,sl2,qt1,qt2,province,cproductslist,ccontactp,cmobile,weixin,cadd,personid,pcheck,fdate,huangye_qukan) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            db.updatetodb(sql,[account,com_id,cname,comkeywords,js1,js2,sl1,sl2,qt1,qt2,province,cproductslist,ccontactp,cmobile,weixin,cadd,personid,pcheck,fdate,huangye_qukan])
            if huangye_qukan:
                request.session['huangye_qukan']=huangye_qukan
        else:
            return HttpResponse("该账号已经录入，请不要重复录入！")
    if addaction=="edit":
        sql="update huangye_list set com_email=%s,com_id=%s,cname=%s,comkeywords=%s,js1=%s,js2=%s,sl1=%s,sl2=%s,qt1=%s,qt2=%s,province=%s,cproductslist=%s,ccontactp=%s,cmobile=%s,weixin=%s,cadd=%s,personid=%s,pcheck=%s,fdate=%s,huangye_qukan=%s where id=%s"
        db.updatetodb(sql,[account,com_id,cname,comkeywords,js1,js2,sl1,sl2,qt1,qt2,province,cproductslist,ccontactp,cmobile,weixin,cadd,personid,pcheck,fdate,huangye_qukan,id])
    return HttpResponseRedirect("list.html")
    #return render_to_response('huangye/add.html',locals())
def hy_list(request):
    username=request.session.get('username',default=None)
    user_id=request.session.get('user_id',default=None)
    if not username or not user_id:
        return HttpResponseRedirect("/icd/relogin.html")
    #是否为主管
    has_auth=zzc.is_hasauth(user_id=user_id)
    request_url=request.META.get('HTTP_REFERER','/')
    authqx=zzc.geauthid(user_id=user_id)
    checkflag=None
    if "16" in authqx:
        checkflag=1
    
    sql="select code,label from huangye_category"
    huangyeqklist=db.fetchalldb(sql)
    allsalesman=zzc.get_allsalesman(user_id=user_id)
    
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
    doperson=request.GET.get("doperson")
    pcheck=request.GET.get("pcheck")
    huangye_qukan=request.GET.get("huangye_qukan")
    ckeywords=request.GET.get('ckeywords')
    js1=request.GET.get('js1')
    js2=request.GET.get('js2')
    sl1=request.GET.get('sl1')
    sl2=request.GET.get('sl2')
    qt1=request.GET.get('qt1')
    qt2=request.GET.get('qt2')
    com_email=request.GET.get('com_email')
    if not com_email:
        com_email=''
    province=request.GET.get('province')
    if province=="请选择...":
        province=''
    city=request.GET.get('city')
    if city=="请选择...":
        city=''
    cname=request.GET.get('cname')
    cproductslist=request.GET.get('cproductslist')
    if not cproductslist:
        cproductslist=''
    searchlist={}
    if doperson:
        searchlist['doperson']=doperson
    if pcheck:
        searchlist['pcheck']=pcheck
    if huangye_qukan:
        searchlist['huangye_qukan']=huangye_qukan
    if ckeywords:
        searchlist['ckeywords']=ckeywords
    if js1:
        searchlist['js1']=js1
    if js2:
        searchlist['js2']=js2
    if sl1:
        searchlist['sl1']=sl1
    if sl2:
        searchlist['sl2']=sl2
    if qt1:
        searchlist['qt1']=qt1
    if qt2:
        searchlist['qt2']=qt2
    if com_email:
        searchlist['com_email']=com_email
    if province:
        searchlist['province']=province
    if city:
        searchlist['city']=city
    if cname:
        searchlist['cname']=cname
    if cproductslist:
        searchlist['cproductslist']=cproductslist
        
    searchurl=urllib.urlencode(searchlist)
    
    huangyelistall=zzc.gethuangyelist(frompageCount,limitNum,searchlist=searchlist)
    listall=huangyelistall['list']
    listcount=huangyelistall['count']
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
    
    return render_to_response('huangye/list.html',locals())
def hy_del(request):
    request_url=request.META.get('HTTP_REFERER','/')
    hid=request.GET.get("id")
    if hid:
        sql="delete from huangye_list where id=%s"
        db.updatetodb(sql,[hid])
        return HttpResponseRedirect(request_url)

#会刊导出
def hy_out(request):
    huangye_qukan=request.GET.get("huangye_qukan")
    if not huangye_qukan:
        huangye_qukan='201701'
    sql="select code,label from huangye_category"
    huangyeqklist=db.fetchalldb(sql)
    sqlh="select id,com_email,membertype,com_id,cname,comkeywords,province,cproductslist,ccontactp,ctel,cmobile,cadd,newemail,weixin from huangye_list where huangye_qukan=%s and pcheck=1 "
    results=db.fetchalldb(sqlh,[huangye_qukan])
    listall=results
    listcount=len(listall)
    return render_to_response('huangye/out.html',locals())