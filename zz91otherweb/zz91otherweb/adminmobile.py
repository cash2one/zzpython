#-*- coding:utf-8 -*-
from django.shortcuts import render_to_response
from django.http import HttpResponse,HttpResponseRedirect
from zz91page import *
from zz91db_mobile import payorder
from zz91db_ast import companydb
from zz91settings import SPHINXCONFIG,logpath
from zz91tools import formattime,getoptionlist,date_to_strall,date_to_str,filter_tags
import os,datetime,time,re,urllib,md5,json,sys,random,hashlib
from zz91db_work import workdb
from conn import dictzz91astdb
from django.core.cache import cache
dbw=workdb()
dbc=companydb()
dict_dbc=dictzz91astdb()
reload(sys)
sys.setdefaultencoding('UTF-8')
nowpath=os.path.dirname(__file__)
execfile(nowpath+"/func/mobile_function.py")
execfile(nowpath+"/func/weixin_function.py")
execfile(nowpath+"/func/huzhu_function.py")
execfile(nowpath+"/func/products_function.py")

zzm=mobile()
zzms=mshop()
zzweixin=zweixin()
zzhuzhu=zz91huzhu()
zzpro=zz91products()
def login(request):
    username=request.session.get('username')
    if username:
        return HttpResponseRedirect('index.html')
    return render_to_response('adminmobile/login.html',locals())
def loginsave(request):
    username1=request.POST['username1']
    password1=passwd=request.POST['password1']
    error1=''
    error2=''
    if not username1:
        error1='请输入用户名'
    if not password1:
        error2='请输入密码'
    if error1 or error2:
        return render_to_response('adminmobile/login.html',locals())
    if passwd:
        md5pwd = hashlib.md5(passwd)
        md5pwd = md5pwd.hexdigest()[8:-8]
    sql="select id,username from auth_user where username=%s and password=%s"
    plist=dbw.fetchonedb(sql,[username1,md5pwd]);
    if plist:
        userid=plist[0]
        username=plist[1]
        request.session.set_expiry(6000*6000)
        request.session['username']=username
        request.session['userid']=userid
        return HttpResponseRedirect('index.html')
    else:
        error1="用户或密码错误"
    
    return render_to_response('adminmobile/login.html',locals())

def logout(request):
    request_url = request.META.get('HTTP_REFERER', '/')
    request.session.delete()
    return HttpResponseRedirect('login.html')

def index(request):
    username=request.session.get('username')
    if not username:
        return HttpResponseRedirect('login.html')
    return render_to_response('adminmobile/index.html',locals())

def trade(request):
    username=request.session.get('username')
    if not username:
        return HttpResponseRedirect('login.html')
    page=request.GET.get('page')
    check_status=request.GET.get('check_status')
    if not check_status:
        check_status="0"
    searchlist={}
    if check_status:
        searchlist['check_status']=str(check_status)
    searchurl=urllib.urlencode(searchlist)
    if not page:
        page=1
    funpage=zz91page()
    limitNum=funpage.limitNum(10)
    nowpage=funpage.nowpage(int(page))
    frompageCount=funpage.frompageCount()
    after_range_num = funpage.after_range_num(3)
    before_range_num = funpage.before_range_num(6)
    messagelist=zzpro.getproductslist(frompageCount,limitNum,check_status=check_status)
    listcount=0
    listall=messagelist['list']
    listcount=messagelist['count']
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
    return render_to_response('adminmobile/trade.html',locals())

def huzhu(request):
    username=request.session.get('username')
    if not username:
        return HttpResponseRedirect('login.html')
    categorylist=zzhuzhu.getcategorylist()
    page=request.GET.get('page')
    account=request.GET.get('account')
    typeid=request.GET.get('typeid')
    if typeid:
        typename=zzhuzhu.getbbs_post_category(typeid)
    is_del=request.GET.get('is_del')
    check_status=request.GET.get('check_status')
    if check_status=='0':
        check_name='未审核'
    elif check_status=='1':
        check_name='已审核'
    elif check_status=='2':
        check_name='已读'
    elif check_status=='3':
        check_name='退回'
    ispush=request.GET.get('ispush')
    if ispush=='0':
        push_name='未推送'
    elif ispush=='1':
        push_name='已推送'

    guanzhu_id=request.GET.get('guanzhu_id')
    
    if guanzhu_id=='1':
        guanzhu_name='废金属'
    elif guanzhu_id=='2':
        guanzhu_name='废塑料'
    elif guanzhu_id=='3':
        guanzhu_name='综合废料'
    
    searchlist={}
    if account:
        searchlist['account']=account
    if typeid:
        searchlist['typeid']=typeid
    if is_del:
        searchlist['is_del']=is_del
    if check_status:
        searchlist['check_status']=check_status
    if ispush:
        searchlist['ispush']=ispush
    if guanzhu_id:
        searchlist['guanzhu_id']=guanzhu_id
    searchurl=urllib.urlencode(searchlist)

    if not page:
        page=1
    funpage=zz91page()
    limitNum=funpage.limitNum(20)
    nowpage=funpage.nowpage(int(page))
    frompageCount=funpage.frompageCount()
    after_range_num = funpage.after_range_num(3)
    before_range_num = funpage.before_range_num(6)
    if ispush=='1':
        bbspostlist=zzhuzhu.getpushlist(frompageCount,limitNum,guanzhu_id)
    else:
        bbspostlist=zzhuzhu.getbbspostlist(frompageCount,limitNum,typeid,check_status,ispush,is_del,account)
    listcount=0
    if (bbspostlist):
        listall=bbspostlist['list']
        listcount=bbspostlist['count']
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
    return render_to_response('adminmobile/huzhu.html',locals())
def del_bbs_post(request):
    username=request.session.get('username')
    if not username:
        return HttpResponseRedirect('login.html')
    request_url=request.META.get('HTTP_REFERER','/')
    postid=request.GET.get('postid')
    is_del=request.GET.get('is_del')
    zzhuzhu.updatedb(is_del,postid)
    return HttpResponseRedirect(request_url)
def shop_product(request):
    username=request.session.get('username')
    if not username:
        return HttpResponseRedirect('login.html')
    page=request.GET.get('page')
    paytype=request.GET.get('paytype')
    paytype="9"
    searchlist={}
    if paytype:
        searchlist['paytype']=paytype
        paytypename=zzm.getftypename(paytype)
    searchurl=urllib.urlencode(searchlist)
    if not page:
        page=1
    funpage=zz91page()
    limitNum=funpage.limitNum(15)
    nowpage=funpage.nowpage(int(page))
    frompageCount=funpage.frompageCount()
    after_range_num = funpage.after_range_num(3)
    before_range_num = funpage.before_range_num(6)
    if paytype=='9':
        shop_productlist=zzms.getshop_product_ranklist(frompageCount=frompageCount,limitNum=limitNum,paytype='10431004')
    else: 
        shop_productlist=zzms.getshop_productlist(frompageCount=frompageCount,limitNum=limitNum)
    if paytype=="42":
        shop_productlist=zzms.getshop_reflushlist(frompageCount=frompageCount,limitNum=limitNum)
    listcount=0
    listall=shop_productlist['list']
    listcount=shop_productlist['count']
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
    return render_to_response('adminmobile/shop_product_rank.html',locals())
def update_prorank(request):
    username=request.session.get('username')
    if not username:
        return HttpResponseRedirect('login.html')
    request_url=request.META.get('HTTP_REFERER','/')
    prorankid=request.GET.get('prorankid')
    sql='select product_id,name,start_time,end_time,is_checked,gmt_modified,company_id,apply_account,buy_time from products_keywords_rank where id=%s'
    result=dbc.fetchonedb(sql,prorankid)
    if result:
        pro_id=result[0]
        pro_title=zzm.getproduct_title(pro_id)
        name=result[1]
        start_time=formattime(result[2])
        timenow=time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
        if not start_time:
            start_time=timenow
        end_time=formattime(result[3])
        if not end_time:
            end_time=timenow
        is_checked=result[4]
        checklist2=getoptionlist(int(is_checked),['未审核','已审核','交易关闭'])
        gmt_modified=formattime(result[5])
        company_id=result[6]
        company_name=zzm.getcompany_name(company_id)
        company_account=result[7]
        buy_time=formattime(result[8])
    return render_to_response('adminmobile/update_prorank.html',locals())
def update_prorankok(request):
    username=request.session.get('username')
    if not username:
        return HttpResponseRedirect('login.html')
    request_url=request.GET.get('request_url')
    prorankid=request.GET.get('prorankid')
    if prorankid:
        is_checked=request.GET.get('is_checked')
        name=request.GET.get('name')
        start_time=request.GET.get('start_time')
        end_time=request.GET.get('end_time')
        sql='update products_keywords_rank set is_checked=%s,name=%s,start_time=%s,end_time=%s where id=%s'
        dbc.updatetodb(sql,[is_checked,name,start_time,end_time,prorankid])
        return HttpResponse("保存成功！")
def editpro(request):
    username=request.session.get('username')
    if not username:
        return HttpResponseRedirect('login.html')
    proid=request.GET.get('proid')
    #加工说明
    manufacturelist=zzpro.getcategorylist('1011')
    unpass_reasonlist=zzpro.getunpass_reason()
    if proid:
        sql="select * from products where id=%s"
        details=dict_dbc.fetchonedb(sql,[proid])
        if details:
            for (d,x) in details.items():
                if not x:
                    details[d]=""
            details['expire_time']=formattime(details['expire_time'])
            details['category_products_main']=zzpro.getcategory_name(details['category_products_main_code'])
        ispic=zzpro.getexitspic(proid)
    return render_to_response('adminmobile/editpro.html',locals())
def editpic(request):
    username=request.session.get('username')
    if not username:
        return HttpResponseRedirect('login.html')
    proid=request.GET.get('proid')
    piclist=zzpro.getcategorylist(proid)
    return render_to_response('adminmobile/editpic.html',locals())

def editcompany(request):
    username=request.session.get('username')
    if not username:
        return HttpResponseRedirect('login.html')
    proid=request.GET.get('proid')
    #industrylist=zzpro.getcategorylist('1011')
    comp=zzpro.getcompanydetail(proid)
    return render_to_response('adminmobile/editcompany.html',locals())

def procontent(request):
    username=request.session.get('username')
    if not username:
        return HttpResponseRedirect('login.html')
    proid=request.GET.get('proid')
    sql="select details from products where id=%s"
    details=dict_dbc.fetchonedb(sql,[proid])
    return render_to_response('adminmobile/content.html',locals())
def companycontent(request):
    username=request.session.get('username')
    if not username:
        return HttpResponseRedirect('login.html')
    company_id=request.GET.get('company_id')
    sql="select introduction from company where id=%s"
    details=dict_dbc.fetchonedb(sql,[company_id])
    return render_to_response('adminmobile/companycontent.html',locals())

def companybusiness(request):
    username=request.session.get('username')
    if not username:
        return HttpResponseRedirect('login.html')
    company_id=request.GET.get('company_id')
    sql="select business from company where id=%s"
    details=dict_dbc.fetchonedb(sql,[company_id])
    return render_to_response('adminmobile/companybusiness.html',locals())

def category(request):
    username=request.session.get('username')
    if not username:
        return HttpResponseRedirect('login.html')
    code = request.GET.get("code")
    proid=request.GET.get('proid')
    if (code==None):
        code='____'
        categorylist=zzpro.getindexcategorylist(code,2)
        return render_to_response('adminmobile/products_category.html',locals())
    else:
        categorylist=zzpro.getindexcategorylist(code,1)
        return render_to_response('adminmobile/products_category.html',locals())
    
def savecontent(request):
    username=request.session.get('username')
    if not username:
        return HttpResponseRedirect('login.html')
    username=request.session.get('username')
    gmt_created=datetime.datetime.now()
    fild = request.POST.get("fild")
    fildvalue = request.POST.get("fildvalue")
    tablevalue = request.POST.get("tablevalue")
    id=request.POST.get("id")
    sql="update "+str(tablevalue)+" set "+str(fild)+"=%s,gmt_modified=%s where id=%s"
    dbc.updatetodb(sql,[fildvalue,gmt_created,id])
    if tablevalue=="products":
        sql="update products set refresh_time=%s,check_time=%s,check_person=%s where id=%s"
        dbc.updatetodb(sql,[gmt_created,gmt_created,username,id])
    result={'err':'false','errkey':''}
    return HttpResponse(json.dumps(result, ensure_ascii=False))

#支付订单
def paylist(request):
    username=request.session.get('username')
    if not username:
        return HttpResponseRedirect('login.html')
    username=request.session.get('username')
    out_trade_no=request.GET.get("out_trade_no")
    mobile=request.GET.get("mobile")
    page=request.GET.get("page")
    if not username:
        return HttpResponseRedirect('login.html')
    searchlist={}
    if out_trade_no:
        searchlist['out_trade_no']=str(out_trade_no)
    if mobile:
        searchlist['mobile']=str(mobile)
    searchurl=urllib.urlencode(searchlist)
    if not page:
        page=1
    funpage=zz91page()
    limitNum=funpage.limitNum(10)
    nowpage=funpage.nowpage(int(page))
    frompageCount=funpage.frompageCount()
    after_range_num = funpage.after_range_num(3)
    before_range_num = funpage.before_range_num(6)
    messagelist=zzpro.getpayorderlist(frompageCount,limitNum,out_trade_no=out_trade_no,mobile=mobile)
    listcount=0
    listall=messagelist['list']
    listcount=messagelist['count']
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
    return render_to_response('adminmobile/paylist.html',locals())
def chongzhisearch(request):
    mobile=request.GET.get("mobile")
    company_id=None
    if mobile:
        company_id=zzm.getcompany_id(mobile,mobile)
        companyname=zzm.getcompany_name(company_id)
    return render_to_response('adminmobile/chongzhi_add.html',locals())
def chongzhi(request):
    username=request.session.get('username')
    if not username:
        return HttpResponseRedirect('login.html')
    company_id=request.GET.get("company_id")
    paytypelist=zzm.getpaytypelist()['list']
    paytypemlist=zzm.getpaytypemlist()
    return render_to_response('adminmobile/chongzhi.html',locals())
def savechongzhi(request):
    username=request.session.get('username')
    if not username:
        return HttpResponseRedirect('login.html')
    company_id=request.POST.get("company_id")
    fee=request.POST.get("fee")
    ftype=request.POST.get("ftype")
    payfrom=request.POST.get('payfrom')
    paytype=request.POST.get('paytype')
    bz=request.POST.get('bz')
    gmt_created=gmt_modified=datetime.datetime.now()
    gmt_date=datetime.date.today()
    
    sql="insert into pay_mobilewallet(company_id,fee,ftype,gmt_created,gmt_modified,gmt_date,paytype,payfrom,bz) values(%s,%s,%s,%s,%s,%s,%s,%s,%s)"
    dbc.updatetodb(sql,[company_id,fee,ftype,gmt_created,gmt_modified,gmt_date,paytype,payfrom,bz])
    result={'err':'false','errkey':''}
    return HttpResponse(json.dumps(result, ensure_ascii=False))

def outfee(request):
    username=request.session.get('username')
    if not username:
        return HttpResponseRedirect('login.html')
    paytype=request.GET.get('paytype')
    paytypem=request.GET.get('paytypem')
    gmt_begin=request.GET.get('gmt_begin')
    gmt_end=request.GET.get('gmt_end')
    page=request.GET.get('page')
    paytypeid=request.GET.get('paytypeid')
    company_id=request.GET.get('company_id')
    company_name=request.GET.get('company_name')
    account=request.GET.get('account')
    mobile=request.GET.get('mobile')
    searchlist={}
    paytype=str(paytype)
    if not paytypeid or paytype=="1":
        paytypeid=5
    if paytype=="2":
        paytypeid=None
    if paytype and paytype!="None":
        searchlist['paytype']=paytype
        paytype=int(paytype)
    if gmt_begin:
        searchlist['gmt_begin']=gmt_begin
    if gmt_end:
        searchlist['gmt_end']=gmt_end
    if account:
        searchlist['account']=account
    if mobile:
        searchlist['mobile']=mobile
    if company_id:
        searchlist['company_id']=company_id
    if company_name:
        searchlist['company_name']=company_name
        company_name=company_name.encode('utf-8')
    if paytypem:
        searchlist['paytypem']=paytypem
        paytypem=paytypem.encode('utf-8')
    if paytypeid:
        searchlist['paytypeid']=paytypeid
        paytypename=zzm.getftypename(paytypeid)
    searchurl=urllib.urlencode(searchlist)
    paytypelist=zzm.getpaytypelist(paytype=paytype)['list']
    paytypemlist=zzm.getpaytypemlist()
    if not page:
        page=1
    funpage=zz91page()
    limitNum=funpage.limitNum(20)
    nowpage=funpage.nowpage(int(page))
    frompageCount=funpage.frompageCount()
    after_range_num = funpage.after_range_num(3)
    before_range_num = funpage.before_range_num(6)
    outfeelist=zzm.getoutfeelist(frompageCount=frompageCount,limitNum=limitNum,type=paytype,gmt_begin=gmt_begin,gmt_end=gmt_end,paytypeid=paytypeid,company_id=company_id,company_name=company_name,account=account,mobile=mobile,paytypem=paytypem)
    listcount=0
    listall=outfeelist['list']
    listcount=outfeelist['count']
    sumfee=outfeelist['sumfee']
    pcount=outfeelist['pcount']
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
    return render_to_response('adminmobile/outfee.html',locals())

#服务开通单列表
def servicelist(request):
    username=request.session.get('username')
    if not username:
        return HttpResponseRedirect('login.html')
    gmt_start=request.GET.get('gmt_start')
    gmt_end=request.GET.get('gmt_end')
    page=request.GET.get('page')
    company_id=request.GET.get('company_id')
    company_name=request.GET.get('company_name')
    account=request.GET.get('account')
    mobile=request.GET.get('mobile')
    searchlist={}
    if gmt_start:
        searchlist['gmt_start']=gmt_start
    if gmt_end:
        searchlist['gmt_end']=gmt_end
    if account:
        searchlist['account']=account
    if mobile:
        searchlist['mobile']=mobile
    if company_id:
        searchlist['company_id']=company_id
    if company_name:
        searchlist['company_name']=company_name
        company_name=company_name.encode('utf-8')
    searchurl=urllib.urlencode(searchlist)
    if not page:
        page=1
    funpage=zz91page()
    limitNum=funpage.limitNum(20)
    nowpage=funpage.nowpage(int(page))
    frompageCount=funpage.frompageCount()
    after_range_num = funpage.after_range_num(3)
    before_range_num = funpage.before_range_num(6)
    outfeelist=zzm.getservicelist(frompageCount=frompageCount,limitNum=limitNum,gmt_start=gmt_start,gmt_end=gmt_end,mobile=mobile)
    listcount=0
    listall=outfeelist['list']
    listcount=outfeelist['count']
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
    return render_to_response('adminmobile/service.html',locals())
