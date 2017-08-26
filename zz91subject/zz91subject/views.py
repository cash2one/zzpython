#-*- coding:utf-8 -*-
import MySQLdb,datetime,sys,time,os,settings,codecs,shutil,random,memcache
from django.utils.http import urlquote
from django.shortcuts import render_to_response
from django.http import HttpResponse,HttpResponseRedirect
from django.core.paginator import Paginator,InvalidPage,EmptyPage,PageNotAnInteger
from datetime import timedelta,date 
from django.views.decorators.cache import cache_control
from django.core.cache import cache
from zz91tools import *
from zz91db import zz91company
zzcomp=zz91company()

try:
    import cPickle as pickle
except ImportError:
    import pickle

from math import ceil

from sphinxapi import *
from zz91page import *


nowpath=os.path.dirname(__file__)
execfile(nowpath+"/conn.py")
execfile(nowpath+"/commfunction.py")
execfile(nowpath+"/function.py")

def addclick(request):
    weburl=request.GET.get('weburl')
    sql='select id from website where url=%s'
    cursor_other.execute(sql,[weburl])
    result = cursor_other.fetchone()
    if result:
        id=result[0]
        sql='update website set click=click+1 where id=%s'
        cursor_other.execute(sql,[id])
        conn_other.commit()
    return HttpResponse('')

#---2014专题
def default1(request):
    websitelist1=getwebsitelist(0,1,'','',2,'click')
    if websitelist1:
        recommendlist1=websitelist1['list']
        if recommendlist1:
            recommendlist1=recommendlist1[0]
    websitelist=getwebsitelist(1,9,'','',2,'click')
    if websitelist:
        recommendlist=websitelist['list']
    webtypelist=getwebtypelist(0,4,2,2)
    if webtypelist:
        listall=webtypelist['list']
    listall2=getnewslist('',0,10)
    if listall2:
        newslist=listall2['list']
    return render_to_response('new2014/index.html',locals())
#---专题更多
def zhuantimore(request,typeid='',page=''):
    offerSalesinfo=offerlist('',"0",7)
    offerBuyinfo=offerlist('',"1",7)
    typename=gettypedetail(typeid)['typename']
    if not page:
        page=1
    funpage=zz91page()
    limitNum=funpage.limitNum(9)
    nowpage=funpage.nowpage(int(page))
    frompageCount=funpage.frompageCount()
    after_range_num = funpage.after_range_num(3)
    before_range_num = funpage.before_range_num(6)
    websitelist=getwebsitelist(frompageCount,limitNum,typeid,'')
    listcount=0
    if (websitelist):
        listall=websitelist['list']
        listcount=websitelist['count']
        listall1=listall[:3]
        if len(listall)>3:
            listall2=listall[3:6]
        if len(listall)>6:
            listall3=listall[6:]
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
    return render_to_response('new2014/more.html',locals())




#报名保存GET方式
def baomingsave_get(request):
    title=request.GET.get("title")
    contents=request.GET.get("contents")
    gmt_creatdate=datetime.datetime.now()
    value=[title,contents,gmt_creatdate]
    sql="insert into subject_baoming(title,contents,gmt_created) values(%s,%s,%s)"
    cursor.execute(sql,value);
    conn.commit()
    return render_to_response('baoming.html',locals())
#报名保存POST方式
def baomingsave(request):
    title=request.POST.get("title")
    contents=request.POST.get("contents")
    backurl=request.POST.get("backurl")
    gmt_creatdate=datetime.datetime.now()
    value=[title,contents,gmt_creatdate]
    sql="insert into subject_baoming(title,contents,gmt_created) values(%s,%s,%s)"
    cursor.execute(sql,value);
    conn.commit()
    return render_to_response('baoming.html',locals())
    #closeconn()
#@cache_control(private=True)
def baoming_save(request):
    title=request.POST["title"]
    contents=request.POST["contents"]
    bh=request.POST["bh"]
    mobile=request.POST["mobile"]
    gmt_creatdate=datetime.datetime.now()
    value=[title,contents,gmt_creatdate,bh]
    sql="insert into subject_baoming(title,contents,gmt_created,code) values(%s,%s,%s,%s)"
    cursor.execute(sql,value);
    conn.commit()
    #发短信
    receiver=mobile
    gmt_modified=gmt_created=gmt_send=datetime.datetime.now()
    content='尊敬的zz91会员您好，你申请的再生通会员双11特价，已申请成功，编号为'+str(bh)+'，凭此编号双十一当天办理享受特价！'
    template_code='sms_11huiyuan'
    send_status=0
    priority=1
    if (content!="" and content!=None and len(mobile)==11):
        if (mobile!="" and mobile!=None):
            sqla="select id from sms_log where receiver=%s and template_code=%s"
            cursor_sms.execute(sqla,[mobile,template_code])
            resaultlist=cursor_sms.fetchone()
            value=[template_code,receiver,send_status,gmt_send,priority,gmt_created,gmt_modified,content]
            if (resaultlist==None):
                sqlp="insert into sms_log(template_code,receiver,send_status,gmt_send,priority,gmt_created,gmt_modified,content) values(%s,%s,%s,%s,%s,%s,%s,%s)"
                cursor_sms.execute(sqlp,value)
                conn_sms.commit()
    #####----------------
    return HttpResponseRedirect('/1111/baoming_suc/?bh='+str(bh))
    closeconn()
#@cache_control(private=no-cache)
def miaosha_save(request):
    title=request.POST["title"]
    contents=request.POST["contents"]
    gmt_creatdate=datetime.datetime.now()
    value=[title,contents,gmt_creatdate]
    sql="insert into subject_baoming(title,contents,gmt_created) values(%s,%s,%s)"
    cursor.execute(sql,value);
    conn.commit()
    return HttpResponseRedirect('/1111/miaosha_suc/')
    closeconn()
def huangye_save(request):
    title=request.POST["title"]
    contents=request.POST["contents"]
    gmt_creatdate=datetime.datetime.now()
    value=[title,contents,gmt_creatdate]
    sql="insert into subject_baoming(title,contents,gmt_created) values(%s,%s,%s)"
    cursor.execute(sql,value);
    conn.commit()
    return HttpResponseRedirect('/huangye2013/baoming_suc/')
    closeconn()
def default(request,subjectname):
    host = request.META['HTTP_HOST']
    return subject(request , subjectname,"default")
def getpicurl(pdtid):
    if str(pdtid)[0:1]!="0":
        sql1="select pic_address from products_pic where product_id=%s and check_status=1 order by is_default desc,id desc"
        cursor.execute(sql1,[pdtid])
        productspic = cursor.fetchone()
        if productspic:
            pdt_images=productspic[0]
        else:
            pdt_images=""
        if (pdt_images == '' or pdt_images == '0'):
            pdt_images='../cn/img/noimage.gif'
        else:
            pdt_images='http://img3.zz91.com/200x120/'+pdt_images+''
        return pdt_images
    else:
        return str(pdtid)[1:len(pdtid)]
def get2014zh():
    zw="A11|B11|B8|A8|A3|B3|B1|A16|A23|A22|A1|A13|B13|B16|A5|B5|A2|B2|A20|A21|A6|A19|A25|B9|A15|B6"
    comname="常州环亚再生资源利用有限公司|亿行塑料造粒厂|台州市路桥天来塑料造粒厂|晋江市柏伟塑料科技有限公司|鎏昇再生资源有限公司|北京市京元物环认证咨询有限公司|天津市华鑫达投资有限公司|文安县赵各庄镇尹村鑫维塑料厂|台州市创新工贸有限公司|上海途建贸易有限公司|大连国家生态工业示范园区|揭阳市美之达铜镍科技有限公司|成都海川塑胶有限公司|TOP YANG 锦扬国际|扬州群凯物资有限公司|Ginfery Group, Inc|余姚市杰杰工贸有限公司|广州市炜业塑胶有限公司|中国轻工业对外经济技术合作福建公司|江阴市宏华包装材料有限公司|余姚市创伟塑化商行|上海帝塑实业有限公司|苏州绿城物资科技有限公司|威宏國際貿易洋行（WEI HUNG INT’L TRADING CO.）|南京涵轶嘉商贸有限公司|美国桑格尔进出口股份有限公司(SunGar Trading, Inc.)"
    contact="吴先生|朱威杭|朱华生|苏子黑|顾理生|李双华|黄经理|薛梦超|王贤骁|聂先生| 杨福杰/梁悦|梁生|姜洪平|竺先生|张林|袁率|张红权|陈炜杭|许振声|华先生|褚小姐/褚先生|郭女士|衡女士|Ｍａｉｋｅ（麥克）年Ｒ|韩召峰|Kai Lin"
    tel="18761160813|13777688997/13989672229|13605768727/13606668090 |13599161184/13599998857|13776911918/13382359993|86-010-56706869|13805819974/18822331077|18531603888/15076677787|13505768019|13671876954/13817831911|18909867696/13942864756|13580171555|13032803373/13548024666|13501779672|13338844411|（中国）86- 18611107434（USA） 1-954-363-7320|13605848510|13902392174/13926298378|15306939758|13771278585|13736027539/18858475728|13122062888|13771824327|（台湾）886-932136895﻿ /15000335351 |18105168668/18905184025|001-520-255-2255"
    zyyw="供应PP、PE破碎料及再生颗粒。我司拥有国家环保总局颁发的环保批文，主要从事废塑料的回收、加工服务。|主营：聚丙（PP）、高压（HDPE）、低压（LDPE）、高低压混合|主营：聚丙（PP）、高压（HDPE）、低压（LDPE）、高低压混合|求购EPS冷压泡沫、EPS热熔块；销售PP再生颗粒、PE再生颗粒、EPS再生颗粒；可代理加工各种注塑产品|供应进口PE、PS、EPS颗粒以及EPS流动加工压块机（国际专利）、无尘过滤网烽烧炉（国家专利）等|AQSIQ进口废物原料国外供货商注册、国内收货人登记, CCIC、固体废物进口许可证办理咨询, 废料进出口贸易等|公司长期销售各种日本、韩国、美国、德国等各种回料PP、PE,PA、PET、ABS、PVC、PMMA、MS、EVA、PBT等。|购销各种玻纤增强PP、阻燃PP、增强尼龙、PA66、工程塑料、汽车专用料|塑料制品、模具、紧固件、泵、真空设备制造，塑料树脂批发、零售|供应PVC发泡板破碎料、磨粉料、白色、黑色、花色均有；求购PVC发泡板。|进口及国内再生资源产业、大连地区再生资源产业、再生资源深加工产业、低碳产业、再生资源交易市场|收购各类表面含金属的电镀塑料；长期出售褪度电镀ABS废塑料，高品质通用级、电镀级ABS、PC/ABS等再生改性颗粒|1.万吨销售pvc边角料、粉碎料、颗粒。  2.万吨销售再生pp编织袋颗粒。  3.专业尼龙改型注塑料。|专业经营清关及国外进口塑料再生料，如供应德国PET打包带及日本PET白毛片等.|锦纶6原料、己内酰胺、锦纶6切片、浇铸尼龙制品、锦纶6再生切片制品、锦纶6线、绳制品|供应：LDPE农膜（未洗）、LDPE农膜（洗净）、PEX Purge(机头料)、PEX Regrind（粉碎料）|生产各种颜色高质量PP，共聚PP，可按颜色质量要求提供样品；另供应黑色、彩色母粒, 钛白母粒, 阻燃母粒|供PVC破碎料、压薄料、电线皮团粒料，月产量达到1200吨以上，质量保证，价格合理|供应PP、PE等破碎料，各类LDPE膜料，滴管带软硬管、PC、PS、尼龙、水口料及吨袋粒子等。|供应白色一级PE/PA、LDPE再生颗粒，用于吹膜、注塑、拉丝、拉管等；求购PA/PE卷膜、LDPE复合膜等|供应各色增强尼龙及阻燃塑料POM 、PBT、ABS、PP原料、再生料|废塑料进口、塑料改性造粒、色母生产三大系列产品。|生产销售各种尼龙粒子，产品优质，价格合适|主营：废塑料，金属和合金废料，混合废金属，冶炼矿渣, 废纸|供应进口ABS破碎料,PP破碎料,PP周转箱粒子，PP吨袋粒子，牛奶瓶片、德国美国瓶盖、管道等|供废料类ABS, GPPS, PC/ABS, PC, HDPE, LDPE, PP, XLPE, PVC, PET, PA, 硬杂等"
    url="http://huanya.zz91.com/|||http://suzh.zz91.com/|http://liushengzs.zz91.com/|http://aqsiqcn.zz91.com/|http://hxdce.zz91.com/|http://xinweisl.zz91.com/|http://zjtzcx.zz91.com/|http://tujian.zz91.com/|http://dalgjst.zz91.com/|http://lianghait.zz91.com/||http://zm.zz91.com/|||http://zhanghq.zz91.com/|||http://huakangsl.zz91.com/||http://shdisu.zz91.com/|||http://hanzhaofeng.zz91.com/|"
    pic="860967|0http://i03.c.aliimg.com/img/ibank/2014/183/049/1706940381_1903475160.jpg|0http://i03.c.aliimg.com/img/ibank/2014/227/511/1623115722_1903475160.jpg|1085612|0http://jsdls.net/infoimg/20142139253350807.jpg|870065|1008066|1088148|904317|1407969|1209083|685969|1058779|1048138|0http://file.youboy.com/a/78/39/62/2/11121622.jpg|1094542|765890|694950|992098|1381294|965906|841035|766864|743325|1428939|1245347"
    
    zwlist=zw.split("|")
    comnamelist=comname.split("|")
    contactlist=contact.split("|")
    tellist=tel.split("|")
    zyywlist=zyyw.split("|")
    urllist=url.split("|")
    piclist=pic.split("|")
    i=0
    listall=[]
    for list in zwlist:
        zw=list
        comname=comnamelist[i]
        contact=contactlist[i]
        tel=tellist[i]
        zyyw=zyywlist[i]
        url=urllist[i]
        if url=="":
            url="javascript:;"
        pic2=piclist[i]
        pic=getpicurl(pic2)
        i=i+1
        lis=""
        if (i%8)==0:
            lis="</dl></li><li><dl>"
        
        listvalue={'zw':zw,'comname':comname,'contact':contact,'tel':tel,'zyyw':zyyw,'url':url,'pic':pic,'lis':lis}
        listall.append(listvalue)
    for i in range(0,6):
        zw=zwlist[i]
        comname=comnamelist[i]
        contact=contactlist[i]
        tel=tellist[i]
        zyyw=zyywlist[i]
        url=urllist[i]
        if url=="":
            url="javascript:;"
        pic2=piclist[i]
        pic=getpicurl(pic2)
        listvalue={'zw':zw,'comname':comname,'contact':contact,'tel':tel,'zyyw':zyyw,'url':url,'pic':pic,'lis':lis}
        listall.append(listvalue)
    return listall
def taozaisheng(request,subjectname,pagename):
    return render_to_response('html/taozaisheng/'+subjectname+'/'+pagename+'.html',locals())
@cache_control(no_cache=True)
def subject(request , subjectname,pagename):
    if (subjectname=="carveout"):
        compinfo1=getcomplist(10001001);
        compinfo2=getcomplist(10001000);
        compinfo3=getcomplist(10001003);
    host = request.META['HTTP_HOST']
    #return HttpResponse(request.META)
    if (host=="www.taozaisheng.com"):
        return render_to_response('html/taozaisheng/'+subjectname+'/'+pagename+'.html',locals())
    if (subjectname=='warmwinter'):
        if (getwarmwinter(189)):
            adlist_sales=getwarmwinter(189)[0]
        if (getwarmwinter(190)):
            adlist_buy=getwarmwinter(190)[0]
    #---
    if (subjectname=='scoreboard'):
        accountscore=zzcomp.getaccountscore(0,12)
        if accountscore:
            accountlist=accountscore['list']
            if len(accountlist)>10:
                accountlist=accountlist[:10]
        scoreexchange=zzcomp.getscoreexchange(frompageCount=0,limitNum=10,account='',prizeid='',ischeck=1,order='score')
    #----14届塑料交易会
    if (subjectname=="tz"):
        nday=datetostr(getToday())
        
        #datanum=datediff(nday,"2014-9-25")
        datanum=0
        datanum=str(datanum)
        if 1<len(datanum)<3:
            datanum="0"+str(datanum)
        if 0<len(datanum)<2:
            datanum="00"+str(datanum)
        da1=datanum[0:1]
        da2=datanum[1:2]
        da3=datanum[2:3]
    if (subjectname=="tzm"):
        listall=get2014zh()
        
    #--2014pet专场
    if (subjectname in ("mashang","ztpp","pe","pvc","july","aug","sep","oct","nov","dec","1501","1502","1503","1504","1505","1506")):
        page=request.GET.get("page")
        if subjectname=="mashang":
            keyw="pet"
        if subjectname=="ztpp":
            keyw="pp"
            adpostionnum=getadpostionNum(605)+1
            adlist=[]
            for i in range(1,adpostionnum):
                list=getOrderadlist(605,i)
                adlist.append(list)
        if subjectname=="pe":
            keyw="pe"
            adpostionnum=getadpostionNum(612)+1
            adlist=[]
            for i in range(1,adpostionnum):
                list=getOrderadlist(612,i)
                adlist.append(list)
        if subjectname=="pvc":
            keyw="pvc"
            adpostionnum=getadpostionNum(619)+1
            adlist=[]
            for i in range(1,adpostionnum):
                list=getOrderadlist(619,i)
                adlist.append(list)
        if subjectname=="july":
            keyw="金属"
            adpostionnum=getadpostionNum(623)+1
            adlist=[]
            for i in range(1,adpostionnum):
                list=getOrderadlist(623,i)
                adlist.append(list)
        if subjectname=="aug":
            keyw="abs"
            adpostionnum=getadpostionNum(631)+1
            adlist=[]
            for i in range(1,adpostionnum):
                list=getOrderadlist(631,i)
                adlist.append(list)
        if subjectname=="sep":
            keyw="贵金属"
            adpostionnum=getadpostionNum(654)+1
            adlist=[]
            for i in range(1,adpostionnum):
                list=getOrderadlist(654,i)
                adlist.append(list)
        if subjectname=="oct":
            keyw="衣服"
            adpostionnum=getadpostionNum(666)+1
            adlist=[]
            for i in range(1,adpostionnum):
                list=getOrderadlist(666,i)
                adlist.append(list)
        if subjectname=="nov":
            keyw="pp"
            adpostionnum=getadpostionNum(713)+1
            adlist=[]
            for i in range(1,adpostionnum):
                list=getOrderadlist(713,i)
                adlist.append(list)
        if subjectname=="dec":
            keyw="通用废塑料"
            adpostionnum=getadpostionNum(720)+1
            adlist=[]
            for i in range(1,adpostionnum):
                list=getOrderadlist(720,i)
                adlist.append(list)
        if subjectname=="1501":
            keyw="pet"
            adpostionnum=getadpostionNum(726)+1
            adlist=[]
            for i in range(1,adpostionnum):
                list=getOrderadlist(726,i)
                adlist.append(list)
        if subjectname=="1502":
            keyw="pp"
            adpostionnum=getadpostionNum(735)+1
            adlist=[]
            for i in range(1,adpostionnum):
                list=getOrderadlist(735,i)
                adlist.append(list)
        if subjectname=="1503":
            keyw="pe"
            adpostionnum=getadpostionNum(737)+1
            adlist=[]
            for i in range(1,adpostionnum):
                list=getOrderadlist(737,i)
                adlist.append(list)
        if subjectname=="1504":
            keyw="pe"
        if subjectname=="1505":
            keyw="pp"
        if subjectname=="1506":
            keyw="abs"
            
        if (page==None):
            page=1
        funpage = zz91page()
        limitNum=funpage.limitNum(16)
        nowpage=funpage.nowpage(int(page))
        frompageCount=funpage.frompageCount()
        after_range_num = funpage.after_range_num(5)
        before_range_num = funpage.before_range_num(9)
        companylist=getindexcompanylist_pic(keywords=keyw,num=None,frompageCount=frompageCount,limitNum=16)
        listcount=0
        if (companylist):
            listall=companylist['list']
            listcount=companylist['listcount']
            if (int(listcount)>1000000):
                listcount=1000000-1
        listcount = funpage.listcount(listcount)
        page_listcount=funpage.page_listcount()
        firstpage = funpage.firstpage()
        lastpage = funpage.lastpage()
        page_range  = funpage.page_range()
        nextpage = funpage.nextpage()
        prvpage = funpage.prvpage()
        comcompanylist=getcommoncompanylist(keywords=keyw,num=20,ptype=0,companyflag=1)
        comcompanylist1=getcommoncompanylist(keywords=keyw,num=20,ptype=1,companyflag=1)
    if (subjectname=="315chengxin"):
        companylist=getchenxincompany(num=50)
    if (subjectname=='newyear'):
        adlistmain=getwarmwinter(202)
        if adlistmain:
            adlist=adlistmain[0]
            adlistcount=adlistmain[1]
            arrcount=[]
            clist=''
            for i in range(0,18-adlistcount):
                arrcount.append(i)
    #2012最后的相亲会
    if (subjectname=='xiangqin'):
        arrcount=[]
        adlist=[]
        adpostionnum1=getadpostionNum(499)+1
        adpostionnum2=getadpostionNum(507)+1
        for i in range(1,adpostionnum1):
            list=getOrderadlist(499,i)
            adlist.append(list)
            arrcount=[]
        adlist1=[]
        for i in range(1,adpostionnum2):
            list1=getOrderadlist(507,i)
            adlist1.append(list1)
    #2013年底促销
    if (subjectname=='year'):
        adpostionnum1=getadpostionNum(581)+1
        adpostionnum2=getadpostionNum(582)+1
        adpostionnum3=getadpostionNum(583)+1
        
        adlist1=[]
        for i in range(1,adpostionnum1):
            list1=getOrderadlist(581,i)
            adlist1.append(list1)
        adlist2=[]
        for i in range(1,adpostionnum2):
            list2=getOrderadlist(582,i)
            adlist2.append(list2)
        adlist3=[]
        for i in range(1,adpostionnum3):
            list3=getOrderadlist(583,i)
            adlist3.append(list3)
    #2014年底促销
    if (subjectname=='2015newyear'):
        adpostionnum1=getadpostionNum(732)+1
        adpostionnum2=getadpostionNum(731)+1
        adpostionnum3=getadpostionNum(733)+1
        
        adlist1=[]
        for i in range(1,adpostionnum1):
            list1=getOrderadlist(732,i)
            adlist1.append(list1)
        adlist2=[]
        for i in range(1,adpostionnum2):
            list2=getOrderadlist(731,i)
            adlist2.append(list2)
        adlist3=[]
        for i in range(1,adpostionnum3):
            list3=getOrderadlist(733,i)
            adlist3.append(list3)
            
    #2013双11活动
    if (subjectname=='1111'):
        bh=request.GET.get("bh")
        nHour=getHour()
        if (int(nHour)<10 or (int(nHour)>11 and int(nHour)<15) or int(nHour)>16):
            ms=None
        else:
            ms=1
        t=random.randrange(0,1000000)
        t=getRange()
    #15届中国塑料交易会会后报道
    if (subjectname=="tzshow"):
        zhcomplist=zsshowcomp()
    #2012春季推荐
    if (host=="tuijian.zz91.com"):
        if (pagename=="03"):
            adlistmain=getwarmwinter(233)
            adcount=40
        if (pagename=="05"):
            adlistmain=getwarmwinter(355)
            adcount=20
        if (pagename=="06"):
            adlistmain=getwarmwinter(366)
            adcount=16
            #热门推荐
            adlistmain_hot=getwarmwinter(367)
            adcount_hot=12
        if (pagename=="09"):
            adlistmain=getwarmwinter(444)
            adcount=35
            #热门推荐
            adlistmain_hot=getwarmwinter(445)
            adcount_hot=15
        if (adlistmain or adlistmain_hot):
            if (adlistmain):
                adlist=adlistmain[0]
                adlistcount=adlistmain[1]
            else:
                adlistcount=0
            arrcount=[]
            clist=''
            for i in range(0,adcount-adlistcount):
                arrcount.append(i)
            if (pagename=="06" or pagename=="09"):
                #热门推荐
                if adlistmain_hot:
                    adlist_hot=adlistmain_hot[0]
                    adlistcount_hot=adlistmain_hot[1]
                    arrcount_hot=[]
                    clist=''
                    for i in range(0,adcount_hot-adlistcount_hot):
                        arrcount_hot.append(i)
                else:
                    arrcount_hot=[]
                    clist=''
                    for i in range(0,adcount_hot):
                        arrcount_hot.append(i)
        else:
            arrcount=[]
            clist=''
            for i in range(0,adcount):
                arrcount.append(i)
            arrcount_hot=[1,2,3,4,5,6,7,8,9,10]
        
        return render_to_response('html/cjtj/'+subjectname+'/'+pagename+'.html',locals())
    else:
        return render_to_response('html/'+subjectname+'/'+pagename+'.html',locals())
    return render_to_response('html/'+subjectname+'/'+pagename+'.html',locals())
    closeconn()