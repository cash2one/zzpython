#-*- coding:utf-8 -*-
from django.shortcuts import render_to_response
from django.http import HttpResponse,HttpResponseRedirect,HttpResponsePermanentRedirect
import MySQLdb,sys,os,memcache,settings,urllib,re,time,datetime,simplejson
from django.core.cache import cache
from sphinxapi import *
from zz91page import *

from settings import spconfig,appurl
#from commfunction import subString,filter_tags,replacepic,
#from commfunction import filter_tags,formattime,subString
from zz91tools import subString,filter_tags
from zz91db_ast import companydb
dbc=companydb()

reload(sys)
sys.setdefaultencoding('UTF-8')
nowpath=os.path.dirname(__file__)
execfile(nowpath+"/func/public_function.py")
execfile(nowpath+"/func/qianbao_function.py")
execfile(nowpath+"/func/trade_function.py")
execfile(nowpath+"/func/weixin_function.py")
execfile(nowpath+"/func/company_function.py")
execfile(nowpath+"/func/ldb_weixin_function.py")

zzc=zzcompany()
zzq=zzqianbao()
zzt=zztrade()
ldb_weixin=ldbweixin()

#公司列表
def company(request):
    host=getnowurl(request)
    alijsload="1"
    webtitle="公司列表"
    ldb=request.GET.get("ldb")
    nowlanmu="<a href='/company/'>公司列表</a>"
    keywords=request.GET.get("keywords")
    page=request.GET.get("page")
    username=request.session.get("username",None)
    if (page==None):
        page=1
    funpage = zz91page()
    limitNum=funpage.limitNum(20)
    nowpage=funpage.nowpage(int(page))
    frompageCount=funpage.frompageCount()
    after_range_num = funpage.after_range_num(5)
    before_range_num = funpage.before_range_num(4)
    
    if (str(keywords)=='None'):    
        keywords=None
    companylistall=zzc.getcompanylist(keywords,frompageCount,limitNum,ldb=ldb)
    companylist=companylistall['list']
    companylistcount=companylistall['count']
    listcount=companylistcount
    if (int(listcount)>100000):
        listcount=100000
    listcount = funpage.listcount(listcount)
    page_listcount=funpage.page_listcount()
    firstpage = funpage.firstpage()
    lastpage = funpage.lastpage()
    page_range  = funpage.page_range()
    nextpage = funpage.nextpage()
    prvpage = funpage.prvpage()
    datatype=request.GET.get("datatype")
    if datatype=="json":
        response = HttpResponse(simplejson.dumps(companylistall, ensure_ascii=False))
        return response
    if (companylistcount==1):
        morebutton='style=display:none'
    else:
        morebutton=''
    if int(page)>1:
        #返回json数据
        datatype=request.GET.get("datatype")
        if datatype=="json":
            return HttpResponse(simplejson.dumps(companylistall, ensure_ascii=False))
        return render_to_response('company/listmore.html',locals())
    #返回json数据
    datatype=request.GET.get("datatype")
    if datatype=="json":
        return HttpResponse(simplejson.dumps(companylistall, ensure_ascii=False))
    return render_to_response('company/list.html',locals())
#公司供求
def companyproductslist(request):
    company_id=request.GET.get("company_id")
    forcompany_id=request.GET.get("forcompany_id")
    if forcompany_id:
        company_id=forcompany_id
    page=request.GET.get("page")
    keywords=None
    if (page==None):
        page=1
    funpage = zz91page()
    limitNum=funpage.limitNum(10)
    nowpage=funpage.nowpage(int(page))
    frompageCount=funpage.frompageCount()
    after_range_num = funpage.after_range_num(2)
    before_range_num = funpage.before_range_num(9)
    
    listall=zzt.getcompanyproductslist(kname=keywords,frompageCount=frompageCount,limitNum=limitNum,company_id=company_id,status=1,realdata=1)
    productslist=listall['list']
    productslistcount=listall['count']
    listcount=productslistcount
    if (int(listcount)>100000):
        listcount=100000
    listcount = funpage.listcount(listcount)
    page_listcount=funpage.page_listcount()
    firstpage = funpage.firstpage()
    lastpage = funpage.lastpage()
    page_range  = funpage.page_range()
    nextpage = funpage.nextpage()
    prvpage = funpage.prvpage()
    
    datatype=request.GET.get("datatype")
    plistall=[]
    for list in productslist:
        plist={'pdt_id':list['pdt_id']}
        plist['pdt_kind']=list['pdt_kind']
        plist['pdt_name']=list['pdt_name']
        plist['com_province']=list['com_province']
        plist['pdt_time_en']=list['pdt_time_en']
        plist['pdt_price']=list['pdt_price']
        plist['pdt_images']=list['pdt_images']
        plist['pagecount']=page_listcount
        plist['count']=productslistcount
        plistall.append(plist)
    return HttpResponse(simplejson.dumps(plistall, ensure_ascii=False))
#公司详细首页
def companyshop(request):
    company_id=request.GET.get("company_id")
    forcompany_id=request.GET.get("forcompany_id")
    page=request.GET.get("page")
    #记录pv
    getproductspv(0,forcompany_id)
    
    keywords=None
    if (page==None):
        page=1
    funpage = zz91page()
    limitNum=funpage.limitNum(20)
    nowpage=funpage.nowpage(int(page))
    frompageCount=funpage.frompageCount()
    after_range_num = funpage.after_range_num(2)
    before_range_num = funpage.before_range_num(9)
    
    listall=zzt.getcompanyproductslist(kname=keywords,frompageCount=frompageCount,limitNum=limitNum,company_id=forcompany_id)
    productslist=listall['list']
    productslistcount=listall['count']
    listcount=productslistcount
    if (int(listcount)>100000):
        listcount=100000
    listcount = funpage.listcount(listcount)
    page_listcount=funpage.page_listcount()
    firstpage = funpage.firstpage()
    lastpage = funpage.lastpage()
    page_range  = funpage.page_range()
    nextpage = funpage.nextpage()
    prvpage = funpage.prvpage()
    
    datatype=request.GET.get("datatype")
    if not forcompany_id or forcompany_id=="null":
        return HttpResponse("err")
    companyinfoall={}
    if str(page)=="1":
        if (forcompany_id) and forcompany_id!="null":
            isaddressbook=zzc.isaddressbook(company_id,forcompany_id)
            clist=zzc.getcompanydetail(forcompany_id)
            if clist:
                companyinfoall={'compname':clist['name'],'business':clist['business'],'address':clist['address'],'isaddressbook':isaddressbook}
            companyinfoall['productslistcount']=productslistcount
            favoriteflag=0
            if company_id:
                favoriteflag=isfavorite(forcompany_id,'10091003',company_id)
            companyinfoall['favoriteflag']=favoriteflag
            #诚信档案
            zxinfo=zzc.getcxinfocheck(forcompany_id)
            companyinfoall['zxinfo']=zxinfo
    plistall=[]
    for list in productslist:
        plist={'pdt_id':list['pdt_id']}
        plist['pdt_kind']=list['pdt_kind']
        plist['pdt_name']=list['pdt_name']
        plist['com_province']=list['com_province']
        plist['pdt_time_en']=list['pdt_time_en']
        plist['pdt_price']=list['pdt_price']
        plist['pdt_images']=list['pdt_images']
        plistall.append(plist)
    companyinfoall['plist']=plistall
    companyinfoall['pagecount']=page_listcount
    
    if str(page)=="1" and forcompany_id:
        list=zzc.getcompanydetail(forcompany_id)
        #被查看者是高会直接显示联系方式
        iszstflag=zzt.getiszstcompany(forcompany_id)
        if iszstflag:
            companyinfoall['list']=list
            companyinfoall['viewflag']=1
            return HttpResponse(simplejson.dumps(companyinfoall, ensure_ascii=False))
    
        #----判断是否为来电宝用户
        viptype=zzq.getviptype(forcompany_id)
        #来电宝客户联系方式公开
        if viptype=='10051003':
            if list['viptype']:
                if list['viptype']['ldb']:
                    list['mobile1']=None
                    if list['viptype']['ldb']['ldbphone']:
                        list['mobile1']=list['viptype']['ldb']['ldbphone']
            
            list['mobilelist']=[]
            companyinfoall['list']=list
            companyinfoall['viewflag']=1
            return HttpResponse(simplejson.dumps(companyinfoall, ensure_ascii=False))
    
        #是否已经查看过联系方式公开
        isseecompany=zzq.getisseecompany(company_id,forcompany_id)
        if isseecompany:
            companyinfoall['list']=list
            companyinfoall['viewflag']=1
            return HttpResponse(simplejson.dumps(companyinfoall, ensure_ascii=False))
            
            
    return HttpResponse(simplejson.dumps(companyinfoall, ensure_ascii=False))


    
#公司供求列表
def companyproducts(request):
    host=getnowurl(request)
    alijsload="1"
    nowlanmu="<a href='/company/'>公司列表</a>"
    username=request.session.get("username",None)
    keywords=request.GET.get("keywords")
    kname=""
    company_id=request.GET.get("company_id")
    if not company_id or company_id=="0":
        return HttpResponse("err")
    page=request.GET.get("page")
    pdt_kind = request.GET.get("ptype")
    if (page==None):
        page=1
    funpage = zz91page()
    limitNum=funpage.limitNum(20)
    nowpage=funpage.nowpage(int(page))
    frompageCount=funpage.frompageCount()
    after_range_num = funpage.after_range_num(2)
    before_range_num = funpage.before_range_num(9)
    
    if (pdt_kind == '' or pdt_kind == None or pdt_kind=="0"):
        pdt_type=''
        pdt_kind='0'
        stab1="offerselect"
        stab2=""
        stab3=""
    if (pdt_kind =='1'):
        pdt_type='0'
        stab1=""
        stab2="offerselect"
        stab3=""
    if (pdt_kind=='2'):
        pdt_type='1'
        stab1=""
        stab2=""
        stab3="offerselect"
    
    if (str(keywords)=='None'):    
        keywords=None
    listall=zzt.getcompanyproductslist(kname=keywords,frompageCount=frompageCount,limitNum=limitNum,company_id=company_id,pdt_type=pdt_type)
    productslist=listall['list']
    productslistcount=listall['count']
    listcount=productslistcount
    if (int(listcount)>100000):
        listcount=100000
    listcount = funpage.listcount(listcount)
    page_listcount=funpage.page_listcount()
    firstpage = funpage.firstpage()
    lastpage = funpage.lastpage()
    page_range  = funpage.page_range()
    nextpage = funpage.nextpage()
    prvpage = funpage.prvpage()
    datatype=request.GET.get("datatype")
    if datatype=="json":
        response = HttpResponse(simplejson.dumps(listall, ensure_ascii=False))
        return response
    if (productslistcount==1):
        morebutton='style=display:none'
    else:
        morebutton=''
    #返回json数据
    datatype=request.GET.get("datatype")
    if datatype=="json":
        return HttpResponse(simplejson.dumps(listall, ensure_ascii=False))
    return render_to_response('company/companyofferlist.html',locals())
def compinfo(request):
    forcompany_id=request.GET.get("forcid")
    company_id=request.GET.get("company_id")
    list=zzc.getcompanydetail(forcompany_id)
    listall={}
    listall['compname']=list['name']
    listall['viptype']=list['viptype']
    listall['business']=list['business']
    listall['introduction']=list['introduction']
    listall['contact']=list['contact']
    listall['address']=list['address']
    zxinfo=zzc.getcxinfocheck(forcompany_id)
    listall['zxinfo']=zxinfo
    #返回json数据
    datatype=request.GET.get("datatype")
    if datatype=="json":
        return HttpResponse(simplejson.dumps(listall, ensure_ascii=False))
    
def companyinfo(request):
    host=getnowurl(request)
    alijsload="1"
    nowlanmu="<a href='/company/'>公司列表</a>"
    forcompany_id=request.GET.get("forcid")
    company_id=request.GET.get("company_id")
    if not company_id or company_id=="0":
        company_id=0
    username=getaccount(company_id)
    iszstflag=zzt.getiszstcompany(forcompany_id)
    pdtid=request.GET.get("pdtid")
    appsystem=request.GET.get("appsystem")
    if appsystem=="iOS":
        ios=1
    list=zzc.getcompanydetail(forcompany_id)
    if list:
        compzstflag=list['viptype']['vipcheck']
        webtitle=list['name']
    else:
        compzstflag=None
    #是否被查看        
    if iszstflag==1 or compzstflag==1:
        viewflag=1
    else:
        viewflag=None
        
    backurl=request.META.get('HTTP_REFERER','/')
    #----判断举报状态
    reportcheck=zzt.getreportcheck(company_id,forcompany_id,0)
    if reportcheck==0:
        idcheck=1
        idchecktxt='举报处理中'
    if reportcheck==1:
        idcheck=1
        idchecktxt='举报已处理'
    if reportcheck==2:
        idcheck=1
        idchecktxt='举报退回'
    #该公司是否被举报成功过
    isjubao=zzt.getreportischeck(forcompany_id,0)
     #判断是否首次安装APP查看扣费
    #account=getaccount(company_id)
    paymoney=10
    #installDaynum=zzq.getfistinstallapp(account)
    #if installDaynum:
        #paymoney=4
    #else:
        #paymoney=5
    #----判断是否为来电宝用户,获取来电宝余额
    isldb=None
    list=[]
    #返回json数据
    datatype=request.GET.get("datatype")
    if datatype=="json":
        return HttpResponse(simplejson.dumps(list, ensure_ascii=False))
    return render_to_response('company/companyinfo.html',locals())
#二级域名获得companyid
def getcompanyidfromdomain(request):
    domain_zz91=request.GET.get("domain_zz91")
    sql='select id from company where domain_zz91=%s'
    result=dbc.fetchonedb(sql,[domain_zz91])
    list={'company_id':None}
    if result:
        list['company_id']=result[0]
    else:
        if domain_zz91:
            if "mcompany/shop" in domain_zz91:
                company_id=domain_zz91.replace("mcompany/shop","").replace(".html","")
                list['company_id']=company_id
        #返回json数据
    datatype=request.GET.get("datatype")
    if datatype=="json":
        return HttpResponse(simplejson.dumps(list, ensure_ascii=False))