#-*- coding:utf-8 -*-

from django.shortcuts import render_to_response
import simplejson
from django.http import HttpResponse,HttpResponseRedirect,HttpResponsePermanentRedirect
import MySQLdb,sys,os,memcache,settings,urllib,re,time,datetime,md5,hashlib,random,StringIO,Image,ImageDraw,ImageFont,ImageFilter
from django.core.cache import cache
#from commfunction import subString,filter_tags,replacepic,formattime
#from function import getnowurl
from zz91page import *
from zz91db_ast import companydb
from zz91db_2_news import newsdb
from zz91db_zzlog import zzlogdb
from zz91db_ads import adsdb
from zz91conn import database_mongodb
from sphinxapi import *
from settings import spconfig,appurl,pyuploadpath,pyimgurl
from zz91settings import SPHINXCONFIG
from zz91tools import formattime,subString,filter_tags,int_to_str,str_to_int,date_to_int

dbc=companydb()
dbn=newsdb()
dbads=adsdb()
dbzzlog=zzlogdb()
#连接loginfo集合（表）
dbmongo=database_mongodb()
 


reload(sys)
sys.setdefaultencoding('UTF-8')
nowpath=os.path.dirname(__file__)
execfile(nowpath+"/func/public_function.py")
execfile(nowpath+"/func/news_function.py")
execfile(nowpath+"/func/inquiry_function.py")
execfile(nowpath+"/func/huzhu_function.py")
execfile(nowpath+"/func/qianbao_function.py")
execfile(nowpath+"/func/message_function.py")
execfile(nowpath+"/func/order_function.py")
execfile(nowpath+"/func/price_function.py")
execfile(nowpath+"/func/myrc_function.py")
execfile(nowpath+"/func/company_function.py")

zzn=zznews()
zzi=zzinquiry()
zzh=zzhuzhu()
zzq=zzqianbao()
zzm=zzmessage()
zzo=zzorder()
zzmyrc=zmyrc()
zzprice=zprice()
zzc=zzcompany()

#----资讯列表
def newslist(request):
    newslist=zzn.getnewslist(frompageCount=0,limitNum=10,allnum=10)
    #return HttpResponse(simplejson.dumps(newslist, ensure_ascii=False))
    return render_to_response('news/list.html',locals())
def messagelistview(request):
    url=request.GET.get('tourl')
    id=request.GET.get('id')
    clientid=request.GET.get('clientid')
    
    company_id=request.GET.get("company_id")
    usertoken=request.GET.get("usertoken")
    appsystem=request.GET.get("appsystem")
    if not getloginstatus(company_id,usertoken):
        errlist={'tokenerr':'true'}
        return HttpResponse(simplejson.dumps(errlist, ensure_ascii=False))
    if not company_id or str(company_id)=="0":
        return HttpResponse("err")
    if url:
        url=url.replace("awena","?")
        url=url.replace("aanda","&")
    if not usertoken:
        usertoken=""
    zzm.updatemessages(id,company_id)
    
    list=zzm.getmessagedetail(id)
    #return render_to_response('main/messages_view.html',locals())
    if not url:
        return render_to_response('main/messages_view.html',locals())
    if "?" in url:
        return HttpResponseRedirect(url+"&company_id="+str(company_id)+"&clientid="+str(clientid)+"&usertoken="+usertoken)
    else:
        return HttpResponseRedirect(url+"?company_id="+str(company_id)+"&clientid="+str(clientid)+"&usertoken="+usertoken)
def messagescount(request):
    company_id=request.GET.get('company_id')
    if not company_id or str(company_id)=="0":
        return HttpResponse("err")
    count=zzm.getmessagecount(company_id=company_id)
    list={'count':count}
    return HttpResponse(simplejson.dumps(list, ensure_ascii=False))
def messagesreadall(request):
    company_id=request.GET.get('company_id')
    if not company_id or str(company_id)=="0":
        return HttpResponse("err")
    zzm.updatemessagesall(company_id)
    list={'suc':1}
    return HttpResponse(simplejson.dumps(list, ensure_ascii=False))
#未读系统消息
def messagesnoview(request):
    company_id=request.GET.get("company_id")
    usertoken=request.GET.get("usertoken")
    appsystem=request.GET.get("appsystem")
    #系统消息
    count0=zzm.getnoviewmessagecount(company_id,0)
    #留言提醒
    count1=zzm.getnoviewmessagecount(company_id,1)
    #社区回复提醒
    count2=zzm.getnoviewmessagecount(company_id,2)
    #钱包提醒
    count3=zzm.getnoviewmessagecount(company_id,3)
    #来电宝提醒
    count4=zzm.getnoviewmessagecount(company_id,4)
    list={'count0':count0,'count1':count1,'count2':count2,'count3':count3,'count4':count4}
    return HttpResponse(simplejson.dumps(list, ensure_ascii=False))
def messagesindex(request):
    company_id=request.GET.get("company_id")
    usertoken=request.GET.get("usertoken")
    appsystem=request.GET.get("appsystem")
    """
    if not getloginstatus(company_id,usertoken):
        errlist={'count0':0,'count1':0,'count2':0,'count3':0,'qlist':None}
        return HttpResponse(simplejson.dumps(errlist, ensure_ascii=False))
    """
    count0=0
    count1=0
    count2=0
    count3=0
    #系统消息
    #count0=zzm.getnoviewmessagecount(company_id,0)
    #留言提醒
    #count1=zzm.getnoviewmessagecount(company_id,1)
    #社区回复提醒
    #count2=zzm.getnoviewmessagecount(company_id,2)
    #钱包提醒
    #count3=zzm.getnoviewmessagecount(company_id,3)
    #聊天列表
    page=request.GET.get("page")
    if (page==None):
        page=1
    funpage = zz91page()
    limitNum=funpage.limitNum(10)
    nowpage=funpage.nowpage(int(page))
    frompageCount=funpage.frompageCount()
    after_range_num = funpage.after_range_num(2)
    before_range_num = funpage.before_range_num(9)
    qlistall=zzm.getchatlist(frompageCount=frompageCount,limitNum=limitNum,company_id=company_id)
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
    
    
    list={'count0':count0,'count1':count1,'count2':count2,'count3':count3,'qlist':qlist,'pagecount':page_listcount}
    datatype=request.GET.get("datatype")
    if datatype=="json":
        return HttpResponse(simplejson.dumps(list, ensure_ascii=False))
    return render_to_response('main/messages_main.html',locals())
#----消息推送列表
def messagelist(request):
    
    company_id=request.GET.get("company_id")
    usertoken=request.GET.get("usertoken")
    appsystem=request.GET.get("appsystem")
    if not getloginstatus(company_id,usertoken):
        errlist={'tokenerr':'true'}
        return HttpResponse(simplejson.dumps(errlist, ensure_ascii=False))
    if not company_id or str(company_id)=="0":
        return HttpResponse("err")
    appsystem=request.GET.get('appsystem')
    clientid=request.GET.get('clientid')
    isviews=request.GET.get('isviews')
    mtype=request.GET.get('mtype')
    viewupate=request.GET.get("viewupate")
    appsystemflag=None
    if appsystem=="Android":
        appsystemflag=1
    page=request.GET.get("page")
    if (page==None):
        page=1
    funpage = zz91page()
    limitNum=funpage.limitNum(20)
    nowpage=funpage.nowpage(int(page))
    frompageCount=funpage.frompageCount()
    after_range_num = funpage.after_range_num(2)
    before_range_num = funpage.before_range_num(9)
    
    qlistall=zzm.getmessagelist(company_id=company_id,frompageCount=frompageCount,limitNum=limitNum,isviews=isviews,mtype=mtype)
    listall=qlistall['list']
    listcount=qlistall['count']
    #更新系统消息为已读
    if str(viewupate)!="0":
        zzm.updatemessagesall(company_id,mtype=mtype)
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
        return HttpResponse(simplejson.dumps(listall, ensure_ascii=False))
    if int(page)>1:
        return render_to_response('main/messages_more.html',locals())
    else:
        return render_to_response('main/messages.html',locals())
#----消息列表
def messagelistmongo(request):
    
    company_id=request.GET.get('company_id')
    usertoken=request.GET.get("usertoken")
    if not getloginstatus(company_id,usertoken):
        errlist={'tokenerr':'true'}
        return HttpResponse(simplejson.dumps(errlist, ensure_ascii=False))
    if not company_id or str(company_id)=="0":
        return HttpResponse("err")
    appsystem=request.GET.get('appsystem')
    clientid=request.GET.get('clientid')
    isviews=request.GET.get('isviews')
    mtype=request.GET.get('mtype')
    appsystemflag=None
    if appsystem=="Android":
        appsystemflag=1
    page=request.GET.get("page")
    if (page==None):
        page=1
    funpage = zz91page()
    limitNum=funpage.limitNum(5)
    nowpage=funpage.nowpage(int(page))
    frompageCount=funpage.frompageCount()
    after_range_num = funpage.after_range_num(2)
    before_range_num = funpage.before_range_num(9)
    
    qlistall=zzm.getmessagelistmongo(company_id=company_id,frompageCount=frompageCount,limitNum=limitNum,isviews=isviews,mtype=mtype)
    listall=qlistall['list']
    listcount=qlistall['count']
    testlist=qlistall['testlist']

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
        return HttpResponse(simplejson.dumps(listall, ensure_ascii=False))
    if int(page)>1:
        return render_to_response('main/messages_more.html',locals())
    else:
        return render_to_response('main/messages.html',locals())

#----改变查看状态函数
def changeidview(request):
    type=request.GET.get('type')
    id=request.GET.get('id')
    dbname=''
    #----系统消息推送
    if type=='1':
        dbname='app_message_view'
    #----再生钱包
    if type=='2':
        dbname='pay_mobileWallet'
    #----商行定制
    if type=='3':
        dbname='app_custom'
    if dbname:
        sql='update '+dbname+' set is_views=1 where id=%s'
        dbc.updatetodb(sql,id)
        sql2='select is_views from '+dbname+' where id=%s'
        isviews=dbc.fetchnumberdb(sql2,id)
        list={'id':id,'isviews':isviews}
        return HttpResponse(simplejson.dumps(list, ensure_ascii=False))
    return HttpResponse()

#----钱包消息列表
def qianbaolist(request):
    company_id=request.session.get("company_id",None)
    page=request.GET.get('page')
    if not page:
        page=1
    payfeedata=zzq.getpayfeelist(company_id=company_id,frompageCount=(page-1)*20,limitNum=20)
    return HttpResponse(simplejson.dumps(payfeedata, ensure_ascii=False))

#---定制列表
def orderlist(request):
    type=request.GET.get('type')
    company_id=request.session.get("company_id",None)
    orderdata=zzo.getorderlist(company_id=company_id,type=type)
    return HttpResponse(simplejson.dumps(orderdata, ensure_ascii=False))

def getuser(request):
    username=request.session.get("username",None)
    company_id=request.session.get("company_id",None)
    if not company_id and username:
        company_id=getcompanyid(username)
        request.session['company_id']=company_id
    list={'username':username,'company_id':company_id}
    if not company_id and not username:
        list=''
    return HttpResponse(simplejson.dumps(list, ensure_ascii=False))
def index_ios(request):
    company_id=request.GET.get("company_id")
    clientid=request.GET.get('clientid')
    if clientid:
        sql="select appsystem from oauth_access where open_id=%s"
        systemreturn=dbc.fetchonedb(sql,[clientid])
        if systemreturn:
            if not systemreturn[0]:
                sql="update oauth_access set appsystem='iOS' where open_id=%s"
                dbc.updatetodb(sql,[clientid])
    
    mybusi=None
    if (company_id!="0"):
        mybusi=zzmyrc.get_mybusinesscollect(company_id)
    kname=""
    productlist=None
    if mybusi and company_id!="0":
        for b in mybusi:
            if b:
                kname+=b['keywords']+"|"
        #
        if kname!="":
            kname=kname[:-1]
            productlist=zzo.getindexofferlist(kname=kname,company_id=company_id,limitcount=5)
        else:
            productlist=zzo.getindexofferlist(company_id=company_id,limitcount=5)
            mybusi=None
    keywords_hex=kname
    productList=None
    if productlist:
        if productlist['list']:
            productList=productlist['list']
    adlist=getadlist(722)
    if not productList:
        productList=zzo.getindexofferlist(company_id=company_id,limitcount=10)['list']
    return render_to_response('main/index_ios.html',locals())

def index(request):
    company_id=request.GET.get("company_id")
    clientid=request.GET.get('clientid')
    if clientid:
        sql="select appsystem from oauth_access where open_id=%s"
        systemreturn=dbc.fetchonedb(sql,[clientid])
        if systemreturn:
            if not systemreturn[0]:
                sql="update oauth_access set appsystem='Android' where open_id=%s"
                dbc.updatetodb(sql,[clientid])
    #mypricecollect=zzmyrc.get_mypricecollectid(company_id)
    mybusi=zzmyrc.get_mybusinesscollect(company_id)
    """
    l=[99990]
    for a in mypricecollect:
        l.append(int(a))
    if not l or l==[99990]:
        pricelist=None
        pricelist=zzprice.getpricelist(frompageCount=0,limitNum=5,allnum=5)
    else:
        ll=getallpricecategroy(l)
        pricelist=zzprice.getpricelist(frompageCount=0,limitNum=5,allnum=5,category_id=ll)
    """
    pricelist=zzprice.getpricelist(frompageCount=0,limitNum=5,allnum=5)
    kname=""
    productlist=""
    if mybusi:
        for b in mybusi:
            if b:
                kname+=b['keywords']+"|"
        #
        if kname!="":
            kname=kname[:-1]
            productlist=zzo.getindexofferlist(kname=kname,company_id=company_id,limitcount=6)
        else:
            productlist=zzo.getindexofferlist(company_id=company_id,limitcount=6)
            mybusi=None
    else:
        productlist=zzo.getindexofferlist(company_id=company_id,limitcount=6)
        #return HttpResponse(kname)
    #return HttpResponse(productlist)
    #抢购栏目,取出最新的推荐产品
    ad1_1_=zzq.getadgoods(bclassid=0,adtype=1,adposition=1)
    ad1_2_=zzq.getadgoods(bclassid=0,adtype=1,adposition=2)
    ad1_3_=zzq.getadgoods(bclassid=0,adtype=1,adposition=3)
    ad1_4_=zzq.getadgoods(bclassid=0,adtype=1,adposition=4)
    ad1_5_=zzq.getadgoods(bclassid=0,adtype=1,adposition=5)
    ad1_6_=zzq.getadgoods(bclassid=0,adtype=1,adposition=6)
    
    if productlist:
        ad1list=productlist['list']
        i=0
        ad1_1={}
        ad1_2={}
        ad1_3={}
        ad1_4={}
        ad1_5={}
        ad1_6={}
        for ad in ad1list:
            if i==0:
                ad1_1['id']='p'+str(ad['pdt_id'])
                ad1_1['goodsName']=ad['pdt_kind']['kindtxt']+ad['pdt_name']
                ad1_1['goodsname_fu']=ad['pdt_price']+"   "+ad['com_province']
                ad1_1['pic']=ad['pdt_images']
                ad1_1['tourl']='/detail/?id='+str(ad['pdt_id'])
            if i==1:
                ad1_2['id']='p'+str(ad['pdt_id'])
                ad1_2['goodsName']=ad['pdt_kind']['kindtxt']+ad['pdt_name']
                ad1_2['goodsname_fu']=ad['pdt_price']+"   "+ad['com_province']
                ad1_2['pic']=ad['pdt_images']
                ad1_2['tourl']='/detail/?id='+str(ad['pdt_id'])
            if i==2:
                ad1_3['id']='p'+str(ad['pdt_id'])
                ad1_3['goodsName']=ad['pdt_kind']['kindtxt']+ad['pdt_name']
                ad1_3['goodsname_fu']=ad['pdt_price']+"   "+ad['com_province']
                ad1_3['pic']=ad['pdt_images']
                ad1_3['tourl']='/detail/?id='+str(ad['pdt_id'])
            if i==3:
                ad1_4['id']='p'+str(ad['pdt_id'])
                ad1_4['goodsName']=ad['pdt_kind']['kindtxt']+ad['pdt_name']
                ad1_4['goodsname_fu']=ad['pdt_price']+"   "+ad['com_province']
                ad1_4['pic']=ad['pdt_images']
                ad1_4['tourl']='/detail/?id='+str(ad['pdt_id'])
            if i==4:
                ad1_5['id']='p'+str(ad['pdt_id'])
                ad1_5['goodsName']=ad['pdt_kind']['kindtxt']+ad['pdt_name']
                ad1_5['goodsname_fu']=ad['pdt_price']+"   "+ad['com_province']
                ad1_5['pic']=ad['pdt_images']
                ad1_5['tourl']='/detail/?id='+str(ad['pdt_id'])
            if i==5:
                ad1_6['id']='p'+str(ad['pdt_id'])
                ad1_6['goodsName']=ad['pdt_kind']['kindtxt']+ad['pdt_name']
                ad1_6['goodsname_fu']=ad['pdt_price']+"   "+ad['com_province']
                ad1_6['pic']=ad['pdt_images']
                ad1_6['tourl']='/detail/?id='+str(ad['pdt_id'])
            i=i+1
    if not ad1_1:
        ad1_1=ad1_1_
    if not ad1_2:
        ad1_2=ad1_2_
    if not ad1_3:
        ad1_3=ad1_3_
    if not ad1_4:
        ad1_4=ad1_4_
    if not ad1_4:
        ad1_4=ad1_4_
    if not ad1_5:
        ad1_5=ad1_5_
    if not ad1_6:
        ad1_6=ad1_6_
    ad2_1=zzq.getadgoods(adtype=2)
    
    ad3_1=zzq.getadgoods(bclassid=0,adtype=3,adposition=1)
    ad3_2=zzq.getadgoods(bclassid=0,adtype=3,adposition=2)
    ad3_3=zzq.getadgoods(bclassid=0,adtype=3,adposition=3)
    ad3_4=zzq.getadgoods(bclassid=0,adtype=3,adposition=4)
    ad3_5=zzq.getadgoods(bclassid=0,adtype=3,adposition=5)
    #广告
    adlist=getadlist(780)
    if adlist:
        target_url=adlist['target_url']
        adlist['target_url']="javascript:gotourl('blank.html?openweb=openweb','blank')"
    adlistall=getadlistall(780)
    #adlist=None
    #adlist={'target_url':''}
    #adlist['target_url']="javascript:gotourl('blank.html?openweb=openweb','blank')"
    #ad4_1=zzq.getadgoods(bclassid=0,adtype=4,adposition=1)
    #ad4_2=zzq.getadgoods(bclassid=0,adtype=4,adposition=2)
    #ad4_3=zzq.getadgoods(bclassid=0,adtype=4,adposition=3)
    #ad4_4=zzq.getadgoods(bclassid=0,adtype=4,adposition=4)
    #ad4_5=zzq.getadgoods(bclassid=0,adtype=4,adposition=5)
    #ad4_6=zzq.getadgoods(bclassid=0,adtype=4,adposition=6)
    #ad4_7=zzq.getadgoods(bclassid=0,adtype=4,adposition=7)
    #ad4_8=zzq.getadgoods(bclassid=0,adtype=4,adposition=8)
    gmt_date=datetime.date.today()
    sql="select id from app_qiandao where company_id=%s and gmt_date=%s"
    result=dbc.fetchonedb(sql,[company_id,gmt_date])
    if result:
        qiandao=1
    else:
        qiandao=None
    #1条资讯
    onenewslist=zzn.getonenews()
    #1条互助
    onehuzhulist=zzh.getbbslistone()
    
    datatype=request.GET.get("datatype")
    if datatype=="json":
        resultlist={"pricelist":pricelist,'adlist':adlist,'qiandao':qiandao,'ad1_1':ad1_1,'ad1_2':ad1_2,'ad1_3':ad1_3,'ad1_4':ad1_4,'ad1_5':ad1_5,'ad1_6':ad1_6,'ad2_1':ad2_1,'ad3':{'ad3_1':ad3_1,'ad3_2':ad3_2,'ad3_3':ad3_3,'ad3_4':ad3_4,'ad3_5':ad3_5},'onenewslist':onenewslist,'onehuzhulist':onehuzhulist,'adlistall':adlistall}
        return HttpResponse(simplejson.dumps(resultlist, ensure_ascii=False))
    return render_to_response('main/index.html',locals())

def index_new(request):
    company_id=request.GET.get("company_id")
    clientid=request.GET.get('clientid')
    """
    if clientid:
        sql="select appsystem from oauth_access where open_id=%s"
        systemreturn=dbc.fetchonedb(sql,[clientid])
        if systemreturn:
            if not systemreturn[0]:
                sql="update oauth_access set appsystem='Android' where open_id=%s"
                dbc.updatetodb(sql,[clientid])
    
    mypricecollect=zzmyrc.get_mypricecollectid(company_id)
    l=[99990]
    for a in mypricecollect:
        l.append(int(a))
    if not l or l==[99990]:
        pricelist=None
        pricelist=zzprice.getpricelist(frompageCount=0,limitNum=5,allnum=5)
    else:
        ll=getallpricecategroy(l)
        pricelist=zzprice.getpricelist(frompageCount=0,limitNum=5,allnum=5,category_id=ll)
    """
    pricelist=None
    #pricelist=zzprice.getpricelist(frompageCount=0,limitNum=5,allnum=5)
    #广告
    adlistall=getadlistall(780)
    gmt_date=datetime.date.today()
    #是否签到
    qiandao=1
    """
    sql="select id from app_qiandao where company_id=%s and gmt_date=%s"
    result=dbc.fetchonedb(sql,[company_id,gmt_date])
    if result:
        qiandao=1
    else:
        qiandao=None
    """
    #1条资讯
    #onenewslist=zzn.getonenews()
    onenewslist=None
    #1条互助
    #onehuzhulist=zzh.getbbslistone()
    onehuzhulist=None
    #供求总数
    zz91app_pcount=cache.get("zz91app_pcount")
    if not zz91app_pcount:
        sql="select count(0) from products"
        result=dbc.fetchonedb(sql)
        pcount='{:,}'.format(int(result[0]*4.65))
        cache.set("zz91app_pcount",pcount,60*24)
    else:
        pcount=zz91app_pcount
    #诚信档案
    if company_id:
        zxinfo=zzc.getcxinfo(company_id)
        #更新登录记录
        updatelogin(request,company_id)
        zxclose=None
    else:
        zxclose=1
        zxinfo=""
    #头条资讯
    hotnewslist=zzn.getnewslist(frompageCount=0,limitNum=3,hot=1)
    hotnews=[]
    for list in hotnewslist['list']:
        ll={'id':list['id'],'title':list['title'],'content':list['subcontent'],'litpic':list['litpic']}
        hotnews.append(ll)
    resultlist={"pricelist":pricelist,'onenewslist':onenewslist,'onehuzhulist':onehuzhulist,'adlistall':adlistall,'qiandao':qiandao,'hotnews':hotnews,'pcount':pcount,'zxinfo':zxinfo,'zxclose':zxclose}
    return HttpResponse(simplejson.dumps(resultlist, ensure_ascii=False))


def trade(request):
    return render_to_response('main/trade.html',locals())
def appbody(request):
    return render_to_response('main/appbody.html',locals())
def question(request):
    return render_to_response('question/list.html',locals())
def bottom(request):
    type=request.GET.get("type")
    return render_to_response('bottom.html',locals())
def top(request):
    type=request.GET.get("type")
    return render_to_response('top.html',locals())

#--留言页面
def leavewordslist(request):
    company_id=request.GET.get('company_id')
    forcompany_id=request.GET.get('forcompany_id')
    page=request.GET.get("page")
    if (page==None):
        page=1
    funpage = zz91page()
    limitNum=funpage.limitNum(10)
    nowpage=funpage.nowpage(int(page))
    frompageCount=funpage.frompageCount()
    after_range_num = funpage.after_range_num(2)
    before_range_num = funpage.before_range_num(9)
    #----获得最新询盘
    leavewordsdata=zzi.getchatlist(rcomid=company_id,scomid=forcompany_id,frompageCount=frompageCount,limitNum=limitNum)
    qlist=leavewordsdata['list']
    qlistcount=leavewordsdata['count']
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
    return HttpResponse(simplejson.dumps(qlist, ensure_ascii=False))
#----首页
def default(request):
#    host=getnowurl(request)
    username=request.session.get("username",None)
    company_id=request.session.get("company_id",None)
    if username and company_id==None:
        company_id=getcompanyid(username)
        request.session['company_id']=company_id
    if (username==None or company_id==None):
        return HttpResponseRedirect("/login/")
    
#    company_id=583640
#    company_id=969597
#    account='liyunpq168@163.com'
    arg=request.GET.get('arg')
#    leavewordsnumb=zzi.getleavewordsnumb(account)
#    leavewordnew=zzi.getleavewordnew(account)
    if arg=='1':
        #----获得最新系统推送
        messagedata=zzm.getmessagecount(company_id=company_id)
        return HttpResponse(simplejson.dumps(messagedata, ensure_ascii=False))
    if arg=='2':
        #----获得最新询盘
        leavewordsdata=zzi.getleavewordslist(rcomid=company_id,comtype='1',is_viewed='0')
        return HttpResponse(simplejson.dumps(leavewordsdata, ensure_ascii=False))
    if arg=='3':
        #----获得最新互助消息
        bbsdata=zzh.getbbslist(company_id=company_id,check_status='0')
        return HttpResponse(simplejson.dumps(bbsdata, ensure_ascii=False))
    if arg=='4':
        #----获得最新钱包消息
        qianbaodata=zzq.getpayfeelist(company_id)
        return HttpResponse(simplejson.dumps(qianbaodata, ensure_ascii=False))
#    if arg=='5':
        #----获得最新供求
#        sampleofferdata=zzt.getindexofferlist(company_id=company_id)
#        return HttpResponse(simplejson.dumps(sampleofferdata, ensure_ascii=False))
    if arg=='6':
        #----获得订阅供求(条数)
        tradeorderdata=zzo.getordercount(company_id=company_id,type=1)
        return HttpResponse(simplejson.dumps(tradeorderdata, ensure_ascii=False))
    if arg=='7':
        #----获得订阅报价(条数)
        priceorderdata=zzo.getordercount(company_id=company_id,type=2)
        return HttpResponse(simplejson.dumps(priceorderdata, ensure_ascii=False))
    return HttpResponse()

def price301(request,typeid='',page='',page1='',id="",assist_id=""):
    jumpurl='http://app.zz91.com/'
    if typeid!="":
        jumpurl+="price/"+typeid+".html"
    else:
        if (id!=""):
            jumpurl+="/priceviews/?id="+str(id)
        if (assist_id):
            jumpurl+="price/p"+assist_id+".html"
    """
    if typeid:
        pinyin=zzprice.getpricecategorypinyin(typeid)has_industry_code
        pinyin=pinyin.replace('-','_')
        pinyin=pinyin.replace('/','_')
        jumpurl+=pinyin+'/'
    """
    return HttpResponseRedirect(jumpurl)

def fk(request):
    return render_to_response('main/fk.html',locals())
def feedbacksave(request):
    title = "手机问题反馈"
    content = request.POST.get('content')
    contact = request.POST.get('contact')
    company_id = request.POST.get('company_id')
    usertoken=request.POST.get("usertoken")
    if not getloginstatus(company_id,usertoken):
        errlist={'tokenerr':'true'}
        return HttpResponse(simplejson.dumps(errlist, ensure_ascii=False))
    if not contact:
        contact=""
    if not content:
        messagedata={'err':'true','errkey':'请填写问题描述','type':'leavewords'}
        return HttpResponse(simplejson.dumps(messagedata, ensure_ascii=False))
    gmt_created=datetime.datetime.now()
    paytype=47
    content=content+"<br/>电话："+contact
    sql='insert into shop_baoming(company_id,content,gmt_created,paytype) values(%s,%s,%s,%s)'
    dbc.updatetodb(sql,[company_id,content,gmt_created,paytype])
    #sql="insert into subject_baoming(title,contents,gmt_created) values(%s,%s,%s)"
    #dbc.updatetodb(sql,[title,content+"<br/>"+str(company_id)+"电话："+contact,gmt_created])
    messagedata={'err':'false','errkey':'提交成功,两个工作日内（节假日自动顺延）我们工作人员会联系您','type':'leavewords'}
    return HttpResponse(simplejson.dumps(messagedata, ensure_ascii=False))
def load(request):
    return render_to_response('main/load.html',locals())
def set(request):
    company_id=request.GET.get("company_id")
    if company_id=="0":
        company_id=None
    return render_to_response('main/set.html',locals())
def set_ios(request):
    company_id=request.GET.get("company_id")
    if company_id=="0":
        company_id=None
    return render_to_response('main/set_ios.html',locals())


def tongji(request):
    #连接loginfo集合（表）
    collection=dbmongo.loginfo
    company_id=request.GET.get("company_id")
    if not company_id:
        company_id=0
    appsystem=request.GET.get("appsystem")
    visitoncode=request.GET.get("visitoncode")
    clientid=request.GET.get("clientid")
    url=request.GET.get("url")
    gmt_created=gmt_modified=datetime.datetime.now()
    gmt_date=formattime(gmt_created,1)
    #gmt_date=str_to_datetime(gmt_date)
    gmt_date=str_to_int(gmt_date)
    sqld=""
    
    collection.insert({"clientid":clientid,"visitoncode":visitoncode,"company_id":company_id,"appsystem":appsystem,"url":url,"gmt_created":gmt_created,'check':0,'gmt_date':gmt_date})
    """
    if clientid:
        #sql="insert into app_log(company_id,appsystem,url,visitoncode,clientid,gmt_created) values(%s,%s,%s,%s,%s,%s)"
        #dbzzlog.updatetodb(sql,[company_id,appsystem,url,visitoncode,clientid,gmt_created])
        if clientid and clientid!="undefined":
            sql="select login_time from app_login where clientid=%s order by id desc limit 0,1"
            rec=dbzzlog.fetchonedb(sql,[clientid])
            if rec:
                oldlogindate=datetime_timestamp(formattime(rec[0],0))
                nowlogindate=int(time.time())
                logindatediff=int((nowlogindate-oldlogindate)/60)
                logindatediffmili=nowlogindate-oldlogindate
                #登录频率情况  30分钟内没有登录的再次登录算登录2次
                #并记录在线时长
                sql="select id from app_logincount where clientid=%s and login_date=%s"
                rec=dbzzlog.fetchonedb(sql,[clientid,gmt_date])
                if rec:
                    if logindatediff>30:
                        sqld="update app_logincount set login_count=login_count+1 where clientid=%s and login_date=%s"
                        dbzzlog.updatetodb(sqld,[clientid,gmt_date])
                    sqld="update app_logincount set login_long=login_long+"+str(logindatediffmili)+" where clientid=%s and login_date=%s"
                    dbzzlog.updatetodb(sqld,[clientid,gmt_date])
                else:
                    sqld="insert into app_logincount(company_id,clientid,login_date,login_count,login_long) values(%s,%s,%s,%s,%s)"
                    dbzzlog.updatetodb(sqld,[company_id,clientid,gmt_date,1,1])

            #登录情况
            sql="select id from app_login where clientid=%s"
            rec=dbzzlog.fetchonedb(sql,[clientid])
            if rec:
                sqld="update app_login set login_date=%s,login_time=%s,company_id=%s where clientid=%s"
                dbzzlog.updatetodb(sqld,[gmt_date,gmt_created,company_id,clientid])
            else:
                sqld="insert into app_login(company_id,appsystem,visitoncode,clientid,login_date,login_time) values(%s,%s,%s,%s,%s,%s)"
                dbzzlog.updatetodb(sqld,[company_id,appsystem,visitoncode,clientid,gmt_date,gmt_created])
                sqld="insert into app_logincount(company_id,clientid,login_date,login_count,login_long) values(%s,%s,%s,%s,%s)"
                dbzzlog.updatetodb(sqld,[company_id,clientid,gmt_date,1,1])
    """
    messagedata={'err':'false','result':''}
    return HttpResponse(simplejson.dumps(messagedata, ensure_ascii=False))

def robots(request):
    return render_to_response('robots.html',locals())

def gethtml(request):
    htmlurl=request.GET.get("htmlurl")
    return render_to_response(htmlurl,locals())
def getweburl(request):
    url=request.GET.get("weburl")
    url=getjiemi(url)
    #url=url.replace("TandT", "&").replace("wenhao", "?")
    return render_to_response("weburl.html",locals())

def getuserkeywords(request):
    company_id=request.GET.get("company_id")
    appsystem=request.GET.get("appsystem")
    clientid=request.GET.get('clientid')
    sql="select keywords from app_user_keywords where appid=%s and ktype='trade' order by id desc limit 0,5"
    rec=dbc.fetchalldb(sql,[clientid])
    kw=""
    if rec:
        for list in rec:
            kw=kw+list[0]+"|"
    if len(kw)>0:
        kw=kw[:-1]
    return HttpResponse(kw)

#邀请码
def invite(request):
    company_id=request.GET.get("company_id")
    appsystem=request.GET.get("appsystem")
    clientid=request.GET.get('clientid')
    suc=request.GET.get('suc')
    if not suc:
        suc=None
    return render_to_response("main/invite.html",locals())
def myinvite(request):
    company_id=request.GET.get("company_id")
    usertoken=request.GET.get("usertoken")
    if not getloginstatus(company_id,usertoken):
        errlist={'tokenerr':'true'}
        return HttpResponse(simplejson.dumps(errlist, ensure_ascii=False))
    appsystem=request.GET.get("appsystem")
    clientid=request.GET.get('clientid')
    code=str(random.randint(100000, 999999))
    isios=None
    if (appsystem=="iOS"):
        isios=1
    if company_id and str(company_id)!="0":
        username=getaccount(company_id)
        md5companyid = hashlib.md5(username+str(company_id))
        md5companyid = md5companyid.hexdigest()[8:-8]
        inviteurl="http://m.zz91.com/invite/s"+str(md5companyid)+".html"
        sql='select id,code from app_invite where company_id=%s'
        result=dbc.fetchonedb(sql,[company_id])
        if not result:
            gmt_created=datetime.datetime.now()
            
            sql2='insert into app_invite(company_id,code,gmt_created,jiamicompanyid) values(%s,%s,%s,%s)'
            dbc.updatetodb(sql2,[company_id,code,gmt_created,md5companyid])
        else:
            sql2="update app_invite set jiamicompanyid=%s where company_id=%s"
            dbc.updatetodb(sql2,[md5companyid,company_id])
            code=result[1]
            
        title="使用我的ZZ91再生网邀请码“"+str(code)+"”,即可获得获取20元再生钱包。可在 http://m.zz91.com/invite/help"+str(code)+".html 兑换"
    datatype=request.GET.get("datatype")
    if datatype=="json":
        messagedata={'err':'false','result':title,'code':code,'inviteurl':inviteurl}
        return HttpResponse(simplejson.dumps(messagedata, ensure_ascii=False))
    return render_to_response("main/myinvite.html",locals())
def invite_save(request):
    title = "邀请码"
    clientid = request.POST.get('clientid')
    company_id = request.POST.get('company_id')
    usertoken=request.POST.get("usertoken")
    if not getloginstatus(company_id,usertoken):
        errlist={'tokenerr':'true'}
        return HttpResponse(simplejson.dumps(errlist, ensure_ascii=False))
    code = request.POST.get('code')
    if not clientid:
        clientid = request.GET.get('clientid')
        company_id = request.GET.get('company_id')
        code = request.GET.get('code')
    if not code or not clientid or not company_id:
        messagedata={'err':'true','errkey':'请输入正确的验证码','type':'invite'}
        return HttpResponse(simplejson.dumps(messagedata, ensure_ascii=False))
    gmt_created=datetime.datetime.now()
    sql="select company_id,code from app_invite where code=%s"
    result=dbc.fetchonedb(sql,[code])
    if not result:
        messagedata={'err':'true','errkey':'请输入正确的验证码','type':'invite'}
        return HttpResponse(simplejson.dumps(messagedata, ensure_ascii=False))
    else:
        forcompany_id=result[0]
        if str(forcompany_id)!=str(company_id):
            sqla="select id from app_invite_company where company_id=%s"
            result=dbc.fetchonedb(sqla,[company_id])
            if not result:
                #邀请一个获得5元奖励 
                zzq.getsendfee(forcompany_id,5,19,more=1)
                #被邀请获得20元
                zzq.getsendfee(company_id,20,18)
                sql="insert into app_invite_company(forcompany_id,company_id,gmt_created) values(%s,%s,%s)"
                dbc.updatetodb(sql,[forcompany_id,company_id,gmt_created])
                messagedata={'err':'false','errkey':'','type':'invite'}
                return HttpResponse(simplejson.dumps(messagedata, ensure_ascii=False))
            else:
                messagedata={'err':'true','errkey':'您已经输入过该邀请码您已经成功被邀请过','type':'invite'}
                return HttpResponse(simplejson.dumps(messagedata, ensure_ascii=False))
        else:
            messagedata={'err':'true','errkey':'该邀请码是您自己的验证码','type':'invite'}
            return HttpResponse(simplejson.dumps(messagedata, ensure_ascii=False))
        
#推送列表页        
def app_pushlist(request):
    #company_id=request.GET.get('company_id')
    company_id=17519
    a=zzm.has_industry_code(company_id)
    if a:
        #获得industry_code
        industry_code=zzm.getindustrycode(company_id)
        messagelist=zzm.getapppushlist(industry_code)
        listall=messagelist['list']
        return render_to_response("main/app_pushlist.html",locals())
    else:
        #request_url=request.META.get('HTTP_REFERER','/')
        #进行行业类别选取
        return HttpResponseRedirect("app_choice_industry.html",locals())
#行业主营选择页       
def app_choice_industry(request):
    #request_url=request.POST['request_url']
    listall=zzm.get_ten_lei()    
    return render_to_response("main/app_choice_industry.html",locals())
def app_choice_industryok(request):
    #company_id=request.GET.get('company_id')
    company_id=17519
    industry_code=request.POST['category']
    #print 'aa',industry_code
    #将主营行业插入至company表
    #sql='insert into company (industry_code) values(%s) where id=%s'
    sql="update company set industry_code=%s where id=%s"
    dbc.updatetodb(sql,[industry_code,company_id])
    return HttpResponseRedirect("/app_pushlist.html")
def updateerrlog(request):
    content=request.POST.get("content")
    sql="insert into err_log(content) values(%s)"
    dbc.updatetodb(sql,[content])
    return HttpResponse(1)
#----图片上传
def chatimgupload(request):
    mid=request.POST.get("mid")
    timepath=time.strftime('%Y/%m/%d/',time.localtime(time.time()))
    gmt_created=datetime.datetime.now()
    nowtime=int(time.time())
    if request.FILES:
        file = request.FILES['file']
        tempim = StringIO.StringIO()
        mstream = StringIO.StringIO(file.read())
        im = Image.open(mstream)
        rheight=500
        rwidth=500
        
        pwidth=im.size[0]
        pheight=im.size[1]
        
        rate = int(pwidth/pheight)
        if rate==0:
            rate=1
        nwidth=200
        nheight=200
        if (pwidth>rwidth):
            nwidth=rwidth
            nheight=nwidth /rate
        else:
            nwidth=pwidth
            nheight=pheight
        
        if (pheight>rheight):
            nheight=rheight
            nwidth=rheight*rate
        else:
            nwidth=pwidth
            nheight=pheight
        im.thumbnail((nwidth,nheight),Image.ANTIALIAS)
        tmp = random.randint(100, 999)
        newpath=pyuploadpath+timepath
        imgpath=newpath+str(nowtime)+str(tmp)+"."+im.format
        if not os.path.isdir(newpath):
            os.makedirs(newpath)

        des_origin_f = open(imgpath,"w")
        for chunk in file.chunks():
            des_origin_f.write(chunk)  
        des_origin_f.close()

        mstream.closed
        tempim.closed
        picurl=imgpath.replace(pyuploadpath,'')
        pic_url=pyimgurl+picurl
        resultlist={"error_code":0,"reason":"","result":pic_url,"queryString":{"mid":mid}}
        return HttpResponse(simplejson.dumps(resultlist, ensure_ascii=False))
    return HttpResponse(simplejson.dumps({"error_code":10,"reason":""}, ensure_ascii=False))
        
        