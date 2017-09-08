#-*- coding:utf-8 -*-
from django.shortcuts import render_to_response
from django.http import HttpResponse,HttpResponseRedirect
from zz91page import *
from zz91conn import database_mongodb
from zz91db_ast import companydb
from zz91db_zzlog import zzlogdb
from zz91settings import SPHINXCONFIG,logpath
from zz91tools import formattime,get_str_timeall,str_to_int
import time,urllib,sys,os,datetime,json,simplejson
from time import strftime, localtime
dbc=companydb()
dblog=zzlogdb()
reload(sys)
sys.setdefaultencoding('UTF-8')
nowpath=os.path.dirname(__file__)
execfile(nowpath+"/func/app_function.py")
execfile(nowpath+"/func/mobile_function.py")
#连接loginfo集合（表）
dbmongo=database_mongodb()

zzapp=zapp()
zzm=mobile()

from zzwx.client import Client

#----微信
def messagelist(request):
    page=request.GET.get('page')
    account=request.GET.get('account')
    ptype=request.GET.get('ptype')
    searchlist={}
    if account:
        searchlist['account']=account
    if ptype:
        searchlist['ptype']=ptype
    searchurl=urllib.urlencode(searchlist)
    if not page:
        page=1
    funpage=zz91page()
    limitNum=funpage.limitNum(20)
    nowpage=funpage.nowpage(int(page))
    frompageCount=funpage.frompageCount()
    after_range_num = funpage.after_range_num(3)
    before_range_num = funpage.before_range_num(6)
    messagelist=zzapp.getmessagelist(frompageCount,limitNum,account,ptype=ptype)
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
    return render_to_response('app/messagelist.html',locals())
#app安装统计
def appinstalluser(request):
    #wxc = Client("wxb3a1f99915ac43ed", "6514984261ac291bfd6ef38ab150fcfb")
    #token=wxc.get_ticket()
    #token=wxc.get_user_info("o0HDLjof6VWJ7-4QSg_Cwhql9Kn0")
    #token=wxc.send_text_message("o0HDLjof6VWJ7-4QSg_Cwhql9Kn0","nihao")
    token=simplejson.dumps({'a':'从今儿起'})
    page=request.GET.get('page')
    account=request.GET.get('account')
    searchlist={}
    if account:
        searchlist['account']=account
    if request.GET.get("action")=="del" and request.GET.get("id"):
        sql="delete from oauth_access where id=%s"
        dbc.updatetodb(sql,[request.GET.get("id")])
        request_url=request.META.get('HTTP_REFERER','/')
        return HttpResponseRedirect(request_url)
        
    gmt_begin=request.GET.get('gmt_begin')
    gmt_end=request.GET.get('gmt_end')
    open_type=request.GET.get('open_type')
    if gmt_begin:
        searchlist['gmt_begin']=gmt_begin
    if gmt_end:
        searchlist['gmt_end']=gmt_end
    if open_type:
        searchlist['open_type']=open_type
    searchurl=urllib.urlencode(searchlist)
    if not page:
        page=1
    funpage=zz91page()
    limitNum=funpage.limitNum(20)
    nowpage=funpage.nowpage(int(page))
    frompageCount=funpage.frompageCount()
    after_range_num = funpage.after_range_num(3)
    before_range_num = funpage.before_range_num(6)
    messagelist=zzapp.installuserlist(frompageCount,limitNum,account,gmt_begin=gmt_begin,gmt_end=gmt_end,open_type=open_type)
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
    return render_to_response('app/appinstalluser.html',locals())

#weixinlist
def weixinlist(request):
    page=request.GET.get('page')
    account=request.GET.get('account')
    gmt_created=request.GET.get('gmt_created')
    livetime=request.GET.get('livetime')
    order=request.GET.get('order')
    service=request.GET.get('service')
    searchlist={}
    if account:
        searchlist['account']=account
    if gmt_created:
        searchlist['gmt_created']=gmt_created
    if livetime:
        searchlist['livetime']=livetime
    if order:
        searchlist['order']=order
    if service:
        searchlist['service']=service
    searchurl=urllib.urlencode(searchlist)
    if not page:
        page=1
    funpage=zz91page()
    limitNum=funpage.limitNum(20)
    nowpage=funpage.nowpage(int(page))
    frompageCount=funpage.frompageCount()
    after_range_num = funpage.after_range_num(3)
    before_range_num = funpage.before_range_num(6)
    messagelist=zzapp.weixinlist(frompageCount,limitNum,account=account,gmt_created=gmt_created,livetime=livetime)
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
    return render_to_response('app/weixinlist.html',locals())
#发送服务号推广消息
def send_service_message(request):
    if request.method=='GET':
        return render_to_response('app/send_service_message.html',locals())
    if request.method=="POST":
        content=request.POST.get('content')

#发送其他推广消息
def send_other_message(request):
    if request.method=='GET':
        return render_to_response('app/send_other_message.html',locals())
    if request.method=="POST":
        content=request.POST.get('content')
        
        
    
def addmessage(request):
    request_url=request.META.get('HTTP_REFERER','/')
    return render_to_response('app/addmessage.html',locals())


def addmessageok(request):
    request_url=request.GET.get('request_url')
    title=request.GET.get('title')
    content=request.GET.get('content')
    url=request.GET.get('url')
    messageid=request.GET.get('messageid')
    error1=''
    error2=''
    if not title:
        error1='请输入标题'
    if not url:
        error2='请输入网址'
    if error1 or error2:
        return render_to_response('app/addmessage.html',locals())
    argument=[title,url]
    if messageid:
        argument.append(content)
        argument.append(messageid)
        sql='update app_message set title=%s,url=%s,content=%s where id=%s'
    else:
        gmt_created=datetime.datetime.now()
        sql='insert into app_message(title,url,gmt_created,content) values(%s,%s,%s,%s)'
        argument.append(gmt_created)
        argument.append(content)
    dbc.updatetodb(sql,argument)
    return HttpResponseRedirect(request_url)

def updatemessage(request):
    request_url=request.META.get('HTTP_REFERER','/')
    messageid=request.GET.get('messageid')
    sql='select title,url,content from app_message where id=%s'
    result=dbc.fetchonedb(sql,messageid)
    if result:
        title=result[0]
        url=result[1]
        content=result[2]
    return render_to_response('app/addmessage.html',locals())
def delmessage(request):
    request_url=request.META.get('HTTP_REFERER','/')
    messageid=request.GET.get('messageid')
    sql='delete from app_message where id=%s'
    dbc.updatetodb(sql,messageid)
    return HttpResponseRedirect(request_url)
#电话拨打列表
def telchecklist(request):
    page=request.GET.get('page')
    tel=request.GET.get('tel')
    pagefrom=request.GET.get('pagefrom')
    searchlist={}
    if tel:
        searchlist['tel']=tel
    if pagefrom:
        searchlist['pagefrom']=pagefrom
    gmt_begin=request.GET.get('gmt_begin')
    gmt_end=request.GET.get('gmt_end')
    if gmt_begin:
        searchlist['gmt_begin']=gmt_begin
    if gmt_end:
        searchlist['gmt_end']=gmt_end
    searchurl=urllib.urlencode(searchlist)
    if not page:
        page=1
    funpage=zz91page()
    limitNum=funpage.limitNum(20)
    nowpage=funpage.nowpage(int(page))
    frompageCount=funpage.frompageCount()
    after_range_num = funpage.after_range_num(3)
    before_range_num = funpage.before_range_num(6)
    messagelist=zzapp.telcheck(frompageCount,limitNum,tel=tel,pagefrom=pagefrom,gmt_begin=gmt_begin,gmt_end=gmt_end)
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
    return render_to_response('app/telchecklist.html',locals())
#每日用户状态，记录了新增用户，活跃用户，沉默用户的个数，和启动次数
def installchart(request):
    ftype=request.GET.get('ftype')
    t=request.GET.get('t')
    if not t:
        t="1"
    return render_to_response('app/installchart.html',locals())
def installcharturl(request):
    gmt_begin=''
    gmt_end=''
    ftype=None
    datall=request.GET.get('datall')
    
    if datall:
        if ',' in datall:
            datallist=datall.split(',')
            ftype=datallist[0]
            gmt_begin=datallist[1]
            gmt_end=datallist[2]
            t=datallist[3]
        else:
            ftype=datall
            t="1"
        tlist=['新增客户','活跃客户','启动次数','沉默客户','PV']
        ftypename=tlist[int(t)-1]
        installapplist=zzapp.eveuserstate(ftype=ftype,gmt_begin=gmt_begin,gmt_end=gmt_end,type=t)
    return render_to_response('app/installcharturl.html',locals())
#每日用户状态，记录了新增用户，活跃用户，沉默用户的个数，和启动次数
def activechart(request):
    ftype=request.GET.get('ftype')
    if not ftype:
        ftype="1"
    return render_to_response('app/active_chart.html',locals())
def activecharturl(request):
    gmt_begin=''
    gmt_end=''
    datall=request.GET.get('datall')
    
    if datall:
        if ',' in datall:
            datallist=datall.split(',')
            ftype=datallist[0]
            gmt_begin=datallist[1]
            gmt_end=datallist[2]
        else:
            ftype=datall
        tlist=['活跃客户','PV']
        if not ftype:
            ftype=1
        if not gmt_begin:
            gmt_begin=str(date.today())
        ftypename=gmt_begin+tlist[int(ftype)-1]
        activeapplist=zzapp.everyhourstate(ftype=ftype,gmt_begin=gmt_begin,gmt_end=gmt_end)
    return render_to_response('app/active_charturl.html',locals())

#app用户搜索关键字
def userKeywords(request):
    page=request.GET.get('page')
    account=request.GET.get('account')
    company_id=request.GET.get('com_id')
    ktype=request.GET.get('ktp')
    
    searchlist={}
    if account:
        searchlist['account']=account
    #如果com_id框有输入
    if company_id:
        searchlist['company_id']=company_id   
    #如果ktp框有输入
    if ktype:
        searchlist['ktype']=ktype   
    searchurl=urllib.urlencode(searchlist)
    
    if not page:
        page=1
    funpage=zz91page()
    limitNum=funpage.limitNum(20)
    nowpage=funpage.nowpage(int(page))
    frompageCount=funpage.frompageCount()
    after_range_num = funpage.after_range_num(3)
    before_range_num = funpage.before_range_num(6)
    messagelist=zzapp.getuserKeywords(frompageCount,limitNum,account,company_id=company_id,ktype=ktype)
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
    return render_to_response('app/userKeywords.html',locals())





#抢购首页
def qianggou(request):
    return render_to_response('app/qianggou.html',locals())
#-----app抢购商品表
#增加商品,插入数据库(goods)
def add_goods(request):
    billing_Class_ID=zzm.getpaytypelist(0,100,subid=22)
    return render_to_response('app/add_goods.html',locals())

def edit_goods(request):
    gid=request.GET.get('gid')
    list=zzapp.getgoods(gid)
    request_url=request.META.get('HTTP_REFERER','/')
    billing_Class_ID=zzm.getpaytypelist(0,100,subid=22)
    
    return render_to_response('app/edit_goods.html',locals())

def add_goods_ok(request):
    goodsName=request.POST.get('goodsName')
    goodsname_fu=request.POST.get('goodsname_fu')
    billing_Class_ID=request.POST.get('billing_Class_ID')
    start_Time=request.POST.get('start_Time')
    end_Time=request.POST.get('end_Time')
    original_Price=request.POST.get('original_Price')
    present_Price=request.POST.get('present_Price')
    sales_Num=request.POST.get('sales_Num')
    left_Num=sales_Num#剩下的数量
    pic=request.POST.get('pic')
    
    ad_type=request.POST.get('ad_type')
    ad_position=request.POST.get('ad_position')
    
    status=request.POST.get('status')
    tourl=request.POST.get('tourl')
    havenum=request.POST.get('havenum')
    
    dt = datetime.datetime.now()  
    release_Time=dt.strftime( '%Y-%m-%d %H:%M:%S' )
    zzapp.addgoodsok(goodsName=goodsName,goodsname_fu=goodsname_fu,billing_Class_ID=billing_Class_ID,start_Time=start_Time,end_Time=end_Time,original_Price=original_Price,present_Price=present_Price,sales_Num=sales_Num,left_Num=left_Num,pic=pic,release_Time=release_Time,ad_type=ad_type,ad_position=ad_position,status=status,tourl=tourl,havenum=havenum)
    return render_to_response('app/add_goods_ok.html',locals())

def edit_goods_ok(request):
    goodsName=request.POST.get('goodsName')
    goodsname_fu=request.POST.get('goodsname_fu')
    billing_Class_ID=request.POST.get('billing_Class_ID')
    start_Time=request.POST.get('start_Time')
    end_Time=request.POST.get('end_Time')
    original_Price=request.POST.get('original_Price')
    present_Price=request.POST.get('present_Price')
    sales_Num=request.POST.get('sales_Num')
    left_Num=request.POST.get('left_Num')
    pic=request.POST.get('pic')
    ad_type=request.POST.get('ad_type')
    ad_position=request.POST.get('ad_position')
    
    status=request.POST.get('status')
    tourl=request.POST.get('tourl')
    havenum=request.POST.get('havenum')
    dt = datetime.datetime.now()  
    release_Time=dt.strftime( '%Y-%m-%d %H:%M:%S' )
    gid=request.POST.get('gid')
    zzapp.editgoodsok(goodsName=goodsName,goodsname_fu=goodsname_fu,billing_Class_ID=billing_Class_ID,start_Time=start_Time,end_Time=end_Time,original_Price=original_Price,present_Price=present_Price,sales_Num=sales_Num,left_Num=left_Num,pic=pic,ad_type=ad_type,ad_position=ad_position,status=status,tourl=tourl,gid=gid,havenum=havenum)
    return render_to_response('app/add_goods_ok.html',locals())

#查看商品
def list_goods(request):
    page=request.GET.get('page')
    ptype=request.GET.get('ptype')
    goodsNmae=request.GET.get('goodsNmae')
    ad_type=request.GET.get('ad_type')
    searchlist={}
    if ptype:
        searchlist['ptype']=ptype
    if goodsNmae:
        searchlist['goodsNmae']=goodsNmae
    if ad_type:
        searchlist['ad_type']=ad_type
    searchurl=urllib.urlencode(searchlist)
    if not page:
        page=1
    funpage=zz91page()
    limitNum=funpage.limitNum(20)
    nowpage=funpage.nowpage(int(page))
    frompageCount=funpage.frompageCount()
    after_range_num = funpage.after_range_num(3)
    before_range_num = funpage.before_range_num(6)
    messagelist=zzapp.listgoods(frompageCount,limitNum,ptype=ptype,goodsNmae=goodsNmae,ad_type=ad_type)
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
    return render_to_response('app/list_goods.html',locals())

#上架操作
def turn_on(request):
    goodsID=request.GET.get('id')
    zzapp.turnon(goodsID=goodsID)
    request_url=request.META.get('HTTP_REFERER','/')
    return HttpResponseRedirect(request_url)
    
#下架操作
def turn_off(request):
    goodsID=request.GET.get('id')
    zzapp.turnoff(goodsID=goodsID)
    request_url=request.META.get('HTTP_REFERER','/')
    return HttpResponseRedirect(request_url)

#推荐操作
def tuijian_on(request):
    goodsID=request.GET.get('id')
    zzapp.tuijianon(goodsID=goodsID)
    request_url=request.META.get('HTTP_REFERER','/')
    return HttpResponseRedirect(request_url)

#取消推荐操作
def tuijian_off(request):
    goodsID=request.GET.get('id')
    zzapp.tuijianoff(goodsID=goodsID)
    request_url=request.META.get('HTTP_REFERER','/')
    return HttpResponseRedirect(request_url)


def delgoods(request):
    goodsID=request.GET.get('id')
    sql='delete from app_goods where id=%s'
    dbc.updatetodb(sql,[goodsID])
    request_url=request.META.get('HTTP_REFERER','/')
    return HttpResponseRedirect(request_url)



#----app推送供求列表
def app_pushlist(request):
    page=request.GET.get('page')
    searchlist={}
    if not page:
        page=1
    gmt_begin=request.GET.get('gmt_begin')
    gmt_end=request.GET.get('gmt_end')
    if gmt_begin:
        searchlist['gmt_begin']=gmt_begin
    if gmt_end:
        searchlist['gmt_end']=gmt_end
    searchurl=urllib.urlencode(searchlist)
    funpage=zz91page()
    limitNum=funpage.limitNum(20)
    nowpage=funpage.nowpage(int(page))
    frompageCount=funpage.frompageCount()
    after_range_num = funpage.after_range_num(3)
    before_range_num = funpage.before_range_num(6)
    messagelist=zzapp.getapppushlist(frompageCount,limitNum,gmt_begin=gmt_begin,gmt_end=gmt_end)
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
    return render_to_response('app/app_pushlist.html',locals())

#增加推送
def add_push(request):
    request_url=request.META.get('HTTP_REFERER','/')
    #artid=request.POST['artid']
    writer='admin'
    pubdate=get_str_timeall()
    typelist=zzapp.gettypelist()
    return render_to_response('app/add_push.html',locals())
def add_pushok(request):
    if request.POST.has_key('artid'):
        pid=request.POST['artid']
    request_url=request.POST['request_url']
    title=request.POST['title']
    typeid=request.POST['typeid']
    pubdate=request.POST['pubdate']
    
    if pubdate:
        pubdate=str_to_int(pubdate)
        
    content=request.POST['myEditor']
    if title and content:
        if pid:  
            zzapp.updatepush(title,typeid,content,pid)
        else:
            zzapp.addpush(title,typeid,content,pubdate)
    return HttpResponseRedirect(request_url)

#----修改推送
def update_app_push(request):
    request_url=request.META.get('HTTP_REFERER','/')
    pid=int(request.GET.get('artid'))
    detaillist=zzapp.getapppushdetail(pid)
    typeid=detaillist['code']
    typelist=zzapp.gettypelist()
    title=detaillist['title']
    content=detaillist['content']
    pubdate=get_str_timeall()
    typename=zzapp.getcategorylabel(typeid)
    return render_to_response('app/add_push.html',locals())

#----删除推送
def delthispush(request):
    request_url=request.META.get('HTTP_REFERER','/')
    id=request.GET.get('artid')
    zzapp.delthisp(id)
    return HttpResponseRedirect(request_url)


#---钱包优惠管理列表
def list_qianbao_gg(request):
    page=request.GET.get('page')
    searchlist={}
    if not page:
        page=1
    ptype=request.GET.get('ptype')
    gmt_begin=request.GET.get('gmt_begin')
    gmt_end=request.GET.get('gmt_end')
    adtxt=request.GET.get('adtxt')
    if ptype:
        if ptype=="0":
            typename="已开启"
        if ptype=="1":
            typename="已关闭"
    if ptype:
        searchlist['ptype']=ptype
    if gmt_begin:
        searchlist['gmt_begin']=gmt_begin
    if gmt_end:
        searchlist['gmt_end']=gmt_end
    searchurl=urllib.urlencode(searchlist)
    funpage=zz91page()
    limitNum=funpage.limitNum(10)
    nowpage=funpage.nowpage(int(page))
    frompageCount=funpage.frompageCount()
    after_range_num = funpage.after_range_num(3)
    before_range_num = funpage.before_range_num(6)
    messagelist=zzapp.getqianbaogglist(frompageCount,limitNum,ptype=ptype,adtxt=adtxt,gmt_begin=gmt_begin,gmt_end=gmt_end)
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
    return render_to_response('app/list_qianbao_gg.html',locals())
#添加钱包广告
def add_qianbao_gg(request):
    request_url=request.META.get('HTTP_REFERER','/')
    #id=request.GET.get('id')
    #qianbao_one=zzapp.getqianbao_one(id)
    return render_to_response('app/add_qianbao_gg.html',locals())
def add_qianbao_ggok(request):
    request_url=request.GET.get('request_url')
    adwords=request.GET.get('adwords')
    infee=request.GET.get('infee')
    sendfee=request.GET.get('sendfee')
    begin_time=request.GET.get('begin_time')
    end_time=request.GET.get('end_time')
    sql="insert into qianbao_gg (txt,infee,sendfee,begin_time,end_time)values (%s,%s,%s,%s,%s)"
    dbc.updatetodb(sql,[adwords,infee,sendfee,begin_time,end_time])
    return HttpResponseRedirect(request_url)
#编辑钱包广告  
def edit_this_gg(request):
    adid=request.GET.get('adid')
    request_url=request.META.get('HTTP_REFERER','/')
    qianbao_one=zzapp.getqianbao_one(adid)
    return render_to_response('app/edit_this_gg.html',locals())
def edit_this_ggok(request):
    request_url="list_qianbao_gg.html"
    adid=request.POST.get('adid')
    adwords=request.POST.get('adwords')
    infee=request.POST.get('infee')
    sendfee=request.POST.get('sendfee')
    begin_time=request.POST.get('begin_time')
    end_time=request.POST.get('end_time')
    sql="update qianbao_gg set txt=%s,infee=%s,sendfee=%s,begin_time=%s,end_time=%s where id=%s"
    dbc.updatetodb(sql,[adwords,infee,sendfee,begin_time,end_time,adid])
    return HttpResponseRedirect(request_url)
#删除钱包广告
def del_this_gg(request):
    request_url=request.META.get('HTTP_REFERER','/')
    adid=request.GET.get('adid')
    sql="delete from qianbao_gg where id=%s"
    dbc.updatetodb(sql,[adid])
    return HttpResponseRedirect(request_url)
#--钱包广告开关操作
def flag_on(request):
    request_url=request.META.get('HTTP_REFERER','/')
    adid=request.GET.get('id')
    zzapp.flagon(id=adid)
    return HttpResponseRedirect(request_url)
    
def flag_off(request):
    request_url=request.META.get('HTTP_REFERER','/')
    adid=request.GET.get('id')
    zzapp.flagoff(id=adid)
    return HttpResponseRedirect(request_url)
    
    
    """
    #上架操作
def turn_on(request):
    goodsID=request.GET.get('id')
    zzapp.turnon(goodsID=goodsID)
    request_url=request.META.get('HTTP_REFERER','/')
    return HttpResponseRedirect(request_url)
    """

def choujiang(request):
    page=request.GET.get('page')
    searchlist={}
    if not page:
        page=1
    btype=request.GET.get('btype')
    BANGDING_t=[]
    for l in BANGDING:
        BANGDING_t.append({'btype':l[0],'bname':BANGDING[str(l[0])]})
    if btype:
        btypename=BANGDING[btype]
    jiangpin=request.GET.get('jiangpin')
    if not jiangpin:
        if str(btype)=="7":
            jiangpin=""
            
    
    if str(btype)=="4":
        if not jiangpin and jiangpin!=0:
            jiangpinname=JIANGPIN_zajindan[str(jiangpin)]
        JIANGPIN=[]
        for l in JIANGPIN_zajindan:
            JIANGPIN.append({'btype':l[0],'bname':JIANGPIN_zajindan[str(l[0])]})
    if str(btype)=="5":
        JIANGPIN=[]
        for l in JIANGPIN_guaguale:
            JIANGPIN.append({'btype':l[0],'bname':JIANGPIN_guaguale[str(l[0])]})
        if jiangpin:
            jiangpinname=JIANGPIN_guaguale[str(jiangpin)]
    if str(btype)=="6":
        JIANGPIN=[]
        for l in JIANGPIN_guoqin:
            JIANGPIN.append({'btype':str(l),'bname':JIANGPIN_guoqin[str(l[0])]})
        if jiangpin:
            jiangpinname=JIANGPIN_guoqin[str(jiangpin)]
    if str(btype)=="7":
        JIANGPIN=[]
        for l in JIANGPIN_taizhou:
            if (l!="-1"):
                JIANGPIN.append({'btype':str(l),'bname':JIANGPIN_taizhou[str(l[0])]})
        if jiangpin:
            jiangpinname=JIANGPIN_taizhou[str(jiangpin)]
    
    company_id=request.GET.get('company_id')
    gmt_begin=request.GET.get('gmt_begin')
    gmt_end=request.GET.get('gmt_end')
    if btype:
        searchlist['btype']=btype
    if company_id:
        searchlist['company_id']=company_id
    if gmt_begin:
        searchlist['gmt_begin']=gmt_begin
    if gmt_end:
        searchlist['gmt_end']=gmt_end
    if jiangpin and jiangpin!=0:
        searchlist['jiangpin']=jiangpin
    searchurl=urllib.urlencode(searchlist)
    funpage=zz91page()
    limitNum=funpage.limitNum(10)
    nowpage=funpage.nowpage(int(page))
    frompageCount=funpage.frompageCount()
    after_range_num = funpage.after_range_num(3)
    before_range_num = funpage.before_range_num(6)
    messagelist=zzapp.getchoujianglist(frompageCount,limitNum,btype=btype,jiangpin=jiangpin,company_id=company_id)
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
    return render_to_response("app/choujiang.html",locals())
#删除
def del_this_cj(request):
    request_url=request.META.get('HTTP_REFERER','/')
    cjid=request.GET.get('cjid')
    sql='delete from subject_choujiang where id=%s'
    dbc.updatetodb(sql,[cjid])
    return HttpResponseRedirect(request_url)
#手动添加
def add_choujiang(request):
    request_url=request.META.get('HTTP_REFERER','/')
    gmt_created=formattime(datetime.datetime.now(),0)
    btype="6"
    btype=request.GET.get('btype')
    if btype:
        choujianaction="add_choujiangok.html"
    else:
        choujianaction="add_choujiang.html"
    BANGDING_t=[]
    for l in BANGDING:
        BANGDING_t.append({'btype':l[0],'bname':BANGDING[str(l[0])]})
    if str(btype)=="4":
        JIANGPIN=[]
        for l in JIANGPIN_zajindan:
            JIANGPIN.append({'btype':l[0],'bname':JIANGPIN_zajindan[str(l[0])]})
    if str(btype)=="5":
        JIANGPIN=[]
        for l in JIANGPIN_guaguale:
            JIANGPIN.append({'btype':l[0],'bname':JIANGPIN_guaguale[str(l[0])]})
    if str(btype)=="6":
        JIANGPIN=[]
        for l in JIANGPIN_guoqin:
            JIANGPIN.append({'btype':str(l),'bname':JIANGPIN_guoqin[str(l[0])]})
    return render_to_response("app/add_choujiang.html",locals())
def add_choujiangok(request):
    cjid=request.GET.get('cjid')
    request_url=request.GET.get('request_url')
    company_account=request.GET.get('company_account')
    company_id=zzapp.getcompany_id(company_account)
    btype=request.GET.get('btype')
    bnum=request.GET.get('bnum')
    jiangpin=request.GET.get('jiangpin')
    gmt_created=request.GET.get('gmt_created')
    error1=''
    error2=''
    error3=''
    error4=''
    if not company_account:
        error1="请填写公司帐号"
    if company_id==-1:
        error1="无此公司帐号"
    if not btype:
        error2="请选择绑定类型"
    if not bnum:
        error3="请填写抽奖次数"
    if not jiangpin:
        error4="请选择奖品"
    if error1 or error2 or error3 or error4:
        return render_to_response("app/add_choujiang.html",locals())
    if not cjid:
        sql='insert into subject_choujiang (company_id,btype,bnum,jiangpin,gmt_created) values (%s,%s,%s,%s,%s)'
        dbc.updatetodb(sql,[company_id,btype,bnum,jiangpin,gmt_created])
    else:
        sql='update subject_choujiang set company_id=%s,btype=%s,bnum=%s,jiangpin=%s,gmt_created=%s where id=%s'
        dbc.updatetodb(sql,[company_id,btype,bnum,jiangpin,gmt_created,cjid])
    return HttpResponseRedirect(request_url)
#编辑抽奖
def edit_this_cj(request):
    request_url=request.META.get('HTTP_REFERER','/')
    cjid=request.GET.get('cjid')
    sql='select company_id,btype,bnum,jiangpin,gmt_created from subject_choujiang where id=%s'
    result=dbc.fetchonedb(sql,[cjid])
    company_id=result[0]
    company_account=zzapp.getcompany_account(company_id)
    btype=result[1]
    btypetxt=BANGDING[str(btype)]
    bnum=result[2]
    jiangpin=result[3]
    jiangpintxt=JIANGPIN[str(jiangpin)]
    if str(btype)=="4":
        jiangpintxt=JIANGPIN_zajindan[str(jiangpin)]
    if str(btype)=="5":
        jiangpintxt=JIANGPIN_guaguale[str(jiangpin)]
    gmt_created=formattime(result[4],0)
    return render_to_response("app/add_choujiang.html",locals())