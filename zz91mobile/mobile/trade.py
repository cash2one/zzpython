#-*- coding:utf-8 -*-
from django.shortcuts import render_to_response
from django.http import HttpResponse,HttpResponseRedirect,HttpResponsePermanentRedirect
import MySQLdb,sys,os,memcache,settings,urllib,re,time,datetime,requests,chardet
from django.core.cache import cache
from datetime import timedelta,date
from django.utils.http import urlquote
from operator import itemgetter, attrgetter
from sphinxapi import *
from zz91page import *

from settings import spconfig
#from commfunction import subString,filter_tags,replacepic,
from commfunction import filter_tags,formattime,subString
from function import getnowurl
from zz91db_ast import companydb
from zz91db_sms import smsdb
from zz91db_2_news import newsdb
from zz91db_ads import adsdb
dbc=companydb()
dbsms=smsdb()
dbn=newsdb()
dbads=adsdb()

reload(sys)
sys.setdefaultencoding('UTF-8')
nowpath=os.path.dirname(__file__)
execfile(nowpath+"/commfunction.py")
execfile(nowpath+"/function.py")
execfile(nowpath+"/func/trade_function.py")
execfile(nowpath+"/func/qianbao_function.py")
execfile(nowpath+"/func/ldb_weixin_function.py")

zzqianbao=qianbao()
zztrade=ztrade()
ldb_weixin=ldbweixin()

def tradeindex(request):
    keywords = request.GET.get("keywords")#搜索
    if keywords:
        return offerlist(request)
    host=getnowurl(request)
    webtitle="供求类别"
    showpost=1
    nowlanmu="<a href='/trade/'>供求分类</a>"
    code = request.GET.get("code")
    username=request.session.get("username",None)
    return render_to_response('2016new/trade/index.html',locals())

    if (code==None):
        code='____'
        categorylist=getindexcategorylist(code,2)
        return render_to_response('trade/index.html',locals())
    else:
        categorylist=getindexcategorylist(code,1)
        return render_to_response('trade/categorymore.html',locals())
def category(request,code):
    if code:
        nowcategory=getcategory_products(code)
        categorylist=getindexcategorylist(code,1)
        categorylistmain=getindexcategorylist('____',2)
        webtitle=nowcategory['label']
        nowlanmu="<a href='/trade/'>"+nowcategory['label']+"</a>"
    return render_to_response('2016new/trade/index.html',locals())
    return render_to_response('trade/category.html',locals())
#--供求供应
def offergongyin(request,pinyin="",page=""):
    
    return offerlist(request,pinyin=pinyin,ptype="1",page=page)
#--供求求购
def offerqiugou(request,pinyin="",page=""):
    return offerlist(request,pinyin=pinyin,ptype="2",page=page)
#----供求列表(排序最复杂)
def offerlist(request,pinyin="",ptype="",page=""):
    if pinyin:
        keywords=zztrade.getcategorylabel(pinyin)
        if not keywords:
            return page404(request)
        nopinyin=None
    else:
        keywords = request.GET.get("keywords")#搜索
        nopinyin=1
    #shoprolist=getshoprolist()
    showpost=1
    arealist=['浙江','广东','江苏','福建','安徽','河南','河北','湖北','湖南','四川','江西','山东','海南','黑龙江','北京','上海','天津','青海','陕西','山西','贵州','辽宁','宁夏','吉林','内蒙古','广西','云南','西藏','重庆','甘肃','新疆','台湾','香港','澳门']
    host=getnowurl(request)
    #alijsload="1"
    nowlanmu="<a href='/trade/'>供求类别</a>"
    if not page or page=="":
        page = request.GET.get("page")
    if (page == None or page=='' or page=="None"):
        page = "1"
    pagenum=page
    nowsearcher="offersearch_new"
    
    if (keywords):
        keywords=keywords.replace("+","")
        keywords=keywords.replace("\\","")
        keywords=keywords.replace("#","")
        keywords=keywords.replace(")","")
        keywords=keywords.replace("(","")
    
    keywords_real = keywords#搜索
    keywords111=str(host)
    arrkey=keywords111.split("keywords=")
    if len(arrkey)>1:
        keywords111=arrkey[1]
        arrkey=keywords111.split("^and^")
        keywords111=arrkey[0]
    
        #keywords111="ppr%D4%D9%C9%FA%BF%C5%C1%A3"
        charttype=chardet.detect(urllib.unquote(str(keywords111)))['encoding']
        #keywords111=charttype
        #if charttype:
            #if ("utf" not in charttype):
                #keywords=urllib.unquote(str(keywords111)).decode('gb2312','ignore').encode('utf-8')
    if not keywords:
        keywords=keywords_real
    if keywords:
        adlist=getadlistkeywords("736",keywords)
    if keywords:
        webtitle=keywords+"_供求列表"
    if keywords=='None' or keywords=='':
        webtitle="供求列表"
        keywords=''
    
    company_id=request.session.get("company_id",None)
    if company_id:
        #----判断是否为来电宝用户,获取来电宝余额
        isldb=None
        viptype=getviptype(company_id)
        if viptype=='10051003':
            isldb=1
            ldbblance=getldblaveall(company_id,"")
            qianbaoblance=ldbblance
        else:
            qianbaoblance=getqianbaoblance2(company_id,"")
    username=request.session.get("username",None)
    searchname = urlquote(request.GET.get("searchname"))
    if ptype:
        pdt_kind=ptype
    else:
        pdt_kind = request.GET.get("ptype")
    province = request.GET.get("province")
    provincecode = request.GET.get("provincecode")
    posttime = request.GET.get("posttime")
    pdtidlist = request.GET.get("pdtidlist")
    priceflag = str(request.GET.get("priceflag"))
    nopiclist = request.GET.get("nopiclist")
    tfromdate = request.GET.get("fromdate")
    ttodate = request.GET.get("todate")
    jmsearchname = request.GET.get("jmsearchname")
    fromsort = request.GET.get("fromsort")
    
    for ltt0 in ['供应','出售','卖']:
        if ltt0 in keywords:
            keywords=keywords.replace(ltt0,'')
            pdt_kind='1'
    for ltt1 in ['求购','回收','买','收购']:
        if ltt1 in keywords:
            keywords=keywords.replace(ltt1,'')
            pdt_kind='2'
    
    forcompany_id = request.GET.get("company_id")
    havepic = request.GET.get("havepic")
    haveprice = request.GET.get("haveprice")
    isding=1
    if havepic or haveprice:
        isding=''
    pdt_kindname=''
    if pdt_kind=='1':
        pdt_kindname='供应'
    if pdt_kind=='2':
        pdt_kindname='求购'
    nowlanmu2=pdt_kindname
    if haveprice:
        nowlanmu2+='－ 价格'
    if havepic:
        nowlanmu2+='－ 图片'
    #----时间筛选
    timearg = request.GET.get("timearg")
    if timearg:
        gmt_end=int(time.time())
        if timearg=='1':
            gmt_begin=gmt_end-24*3600
        elif timearg=='2':
            gmt_begin=gmt_end-24*3600*3
        elif timearg=='3':
            gmt_begin=gmt_end-24*3600*7
        elif timearg=='4':
            gmt_begin=gmt_end-24*3600*30
        elif timearg=='5':
            gmt_begin=gmt_end-24*3600*60
    else:
        timearg=''

    if (str(page)=='1' or page=='' or str(page)=='None'):
        pdtidlist=keywordsTop(keywords)
    else:
        pdtidlist=""

    #‘’‘’‘’‘’‘’‘’‘’‘
    if (nopiclist=='' or nopiclist==None or nopiclist=='None'):
        nopiclist=None
        offerFilterListPicInfo_class="offerFilterListPicInfo"
    else:
        offerFilterListPicInfo_class="offerFilterListPicInfo_long"
    #获得相关类别
    categorylist=getcategorylist(kname=keywords,limitcount=20)
    if (pdtidlist!=None and pdtidlist!=''):
        #arrpdtidlist=pdtidlist.split(',')
        arrpdtidlist=pdtidlist
        listall=[]
        n=1
        for p in arrpdtidlist:
            if (p!=''):
                list1=getcompinfo(p[0],"",keywords,company_id)
                m=1
                if (n<=1):
                    m=1
                elif(n>1 and n<=3):
                    m=2
                elif (n>3 and n<=7):
                    m=3
                if (list1!=None):
                    list1['vippaibian']=str(m)
                    n+=1
                    listall.append(list1)
        productListtop=listall
    
    #--------------------------------------------
    if (province=='' or province == None):
        province=''
        
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
    
    if not page:
        page=1
    nowpage=int(page)
    page=20*(int(page)-1)
    keywords2=keywords.replace('|','')
    keywords2=keywords2.replace(' ','')
    
    keywords1=urlquote(keywords2)
    ttype = request.GET.get("ttype")
    keywords=keywords.replace('|',' ')
    keywords=keywords.replace('\\',' ')
    keywords=keywords.replace('/',' ')
    keywords=keywords.replace('/',' ')
    keywords=keywords.replace('(',' ')
    keywords=keywords.replace(')',' ')
    seo_keywords=keywords
    
    if (ttype==None):
        ttype=''
    if (posttime==None):
        posttime=''
    if (priceflag==None or str(priceflag)=='None'):
        priceflag=''
    if (nopiclist==None or str(nopiclist)=='None'):
        nopiclist=''
    if (havepic==None or str(havepic)=='None'):
        havepic=''
    #action = '&keywords='+searchname+'&ptype='+pdt_kind+'&province='+urlquote(province)+'&posttime='+str(posttime)+'&ttype='+str(ttype)+'&priceflag='+str(priceflag)+'&nopiclist='+str(nopiclist)+'&jmsearchname='+str(jmsearchname)+'&havepic='+str(havepic)+'&fromsort='+str(fromsort)
    #a(\d*)--b(\d*)--c(\d*)--d(\d*)--e(\d*)--f(\d*)
    action='a'+str(pdt_kind)+'--b'+str(provincecode)+'--c'+str(posttime)+'--d'+str(priceflag)+'--e'+str(nopiclist)+'--f'+str(havepic)+''
    searchname=str(keywords1)
    searchname=searchname.replace('%28','astokhl')
    searchname=searchname.replace('%29','astokhr')
    searchname=searchname.replace('%5C','asto5c')
    searchname=searchname.replace('/','astoxg')
    searchname=searchname.replace('-','astohg')
    after_range_num = 8
    before_range_num = 9
    port = spconfig['port']
    if pdt_kind=="1":
        gyurl="gy"
    if pdt_kind=="2":
        gyurl="qg"
    #----------------------------
    cl = SphinxClient()
    cl = SphinxClient()
    list = SphinxClient()
    
    cl.SetServer ( spconfig['serverid'], port )
    list.SetServer ( spconfig['serverid'], port )
    cl.SetMatchMode ( SPH_MATCH_BOOLEAN )
    list.SetMatchMode ( SPH_MATCH_BOOLEAN )
    
    #取得总数
    nowdate=date.today()-timedelta(days=2)
    nextday=date.today()+timedelta(days=2)
    formatnowdate=time.mktime(nowdate.timetuple())
    formatnextday=time.mktime(nextday.timetuple())
    searstr=''
    
    if (pdt_kind !='0'):
        searstr+=";filter=pdt_kind,"+pdt_type
        cl.SetFilter('pdt_kind',[int(pdt_type)])
        list.SetFilter('pdt_kind',[int(pdt_type)])
        
    if(havepic=='1'):
        cl.SetFilterRange('havepic',1,100)
        list.SetFilterRange('havepic',1,100)
    #list.SetFilter('viptype',[0],True)
    #cl.SetFilter('offerstaus',[0])
    #list.SetFilter('offerstaus',[0])
    if (ttype == '1'):    
        cl.SetFilterRange('pdt_date',int(formatnowdate),int(formatnextday))
        list.SetFilterRange('pdt_date',int(formatnowdate),int(formatnextday))
        #searstr+=' ;range=refresh_time,'+str(formatnowdate)+','+str(formatnextday)+''
        
    if (posttime =='' or posttime==None or posttime=='None'):
        searstr +=''
    else:
        pfromdate=date.today()-timedelta(days=int(posttime)+1)
        #test=str(time.mktime(pfromdate.timetuple()))
        ptodate=date.today()+timedelta(days=3)
        
        pfromdate_int=int(time.mktime(pfromdate.timetuple()))
        ptodate_int=int(time.mktime(ptodate.timetuple()))
        if (pfromdate!=None):
            cl.SetFilterRange('pdt_date',int(pfromdate_int),int(ptodate_int))
            list.SetFilterRange('pdt_date',int(pfromdate_int),int(ptodate_int))
        #searstr += ';refresh_time,'+str(pfromdate_int)+','+str(ptodate_int)+''
    if timearg:
        cl.SetFilterRange('pdt_date',gmt_begin,gmt_end)
        list.SetFilterRange('pdt_date',gmt_begin,gmt_end)
    if haveprice:
        cl.SetFilterRange('length_price',4,10000)
        list.SetFilterRange('length_price',4,10000)
        cl.SetFilter('haveprice',[1],True)
        list.SetFilter('haveprice',[1],True)
    if forcompany_id:
        forcompany_id=int(forcompany_id)
        cl.SetFilter('company_id',[forcompany_id])
        list.SetFilter('company_id',[forcompany_id])
        forcompany_name=getppccompanyinfo(forcompany_id)
        if forcompany_name:
            forcompany_name=forcompany_name['companyname']
        seo_keywords=forcompany_name
    
    if (province ==None or province ==''):
        provincestr=''
    else:
        provincestr='&@(province,city) '+province

    if (priceflag == '1'):
        cl.SetFilter('length_price',[0],True)
        list.SetFilter('length_price',[0],True)
        list.SetSortMode( SPH_SORT_EXTENDED,"length_price desc,refresh_time desc" )
    elif (priceflag == '2'):
        list.SetFilter('length_price',[0],True)
        list.SetSortMode( SPH_SORT_EXTENDED,"length_price asc,refresh_time desc" )
    else:
        list.SetSortMode( SPH_SORT_EXTENDED,"refresh_time desc" )
    if keywords=='':
        res = list.Query ('',nowsearcher)
    else:
        res = list.Query ( '@(title,label0,label1,label2,label3,label4,city,province,tags) '+keywords+provincestr+'',nowsearcher)
    if not res:
        listcount=0
    else:
        listcount=res['total_found']
    
    cl.SetFilterRange('viptype',1,5)
    #cl.SetFilterRange('Prodatediff',0,3)
    
    #获得3天内再生通数据优先排序
    #listallvip=cache.get('list'+action)
    
    cl.SetSortMode( SPH_SORT_EXTENDED,"company_id desc,refresh_time desc" )
    cl.SetLimits (0,100000,100000)
    if keywords=='':
        rescount = cl.Query ('','offersearch_new_vip')
    else:
        rescount = cl.Query ( '@(title,label0,label1,label2,label3,label4,city,province,tags) '+keywords+provincestr+'','offersearch_new_vip')
    pcount=0
    listall=[]
    if rescount:
        if rescount.has_key('matches'):
            tagslist=rescount['matches']
            testcom_id=0
            pcount=100000
            for match in tagslist:
                id=match['id']
                com_id=match['attrs']['company_id']
                viptype=match['attrs']['viptype_ldb']
                phone_rate=int(match['attrs']['phone_rate'])
                phone_num=int(match['attrs']['phone_num'])
                phone_fee=float(match['attrs']['phone_cost'])
                refresh_time=float(match['attrs']['refresh_time'])
                pdt_date=float(match['attrs']['pdt_date'])
                phone_level=float(match['attrs']['phone_level'])
                if (testcom_id==com_id):
                    pcount-=1
                else:
                    pcount=100000
                if phone_num==10000:
                    phone_sort=10000;
                else:
                    phone_sort=phone_rate*0.05+phone_num*0.85+phone_fee*0.1
                list1=(id,pcount,viptype,refresh_time,pdt_date,phone_sort,phone_level)
                listall.append(list1)
                testcom_id=com_id
    listallvip=sorted(listall, key=itemgetter(1,4,2,5,6,3),reverse=True)
    #listallvip=tradeorderby(listall)
    
    #cache.set('list'+action, listallvip, 15*60)
    #优先排序数
    viplen=len(listallvip)
    
    #供求总数
    listcount+=int(viplen)
    #最后一页的供求数
    lastpNum=int(viplen-ceil(viplen / 20)*20)
    #开始供求数位置
    beginpage=page
    #优先排序页码
    pageNum=0
    if (lastpNum==0):
        pageNum=int(ceil(viplen / 20))
    else:
        pageNum=int(ceil(viplen / 20)+1)
    
    #结束供求数位置
    if (int(nowpage)==int(pageNum) and lastpNum!=0):
        endpage=int(page+lastpNum)
    elif(int(nowpage)==int(pageNum) and lastpNum==0 and int(nowpage)==1):
        endpage=20
    elif(int(nowpage)==int(pageNum) and lastpNum==0):
        endpage=int(page)
    else:
        endpage=page+20
    #列出供求信息列表
    listall=[]
    for match in listallvip[beginpage:endpage]:
        list1=getcompinfo(match[0],"",keywords2,company_id)
        listall.append(list1)
    productList=listall
    
    #普通供求开始数
    offsetNum=0
    limitNum=20
    if (nowpage==pageNum and lastpNum!=0):
        offsetNum=0
        limitNum=20-lastpNum
        notvip=1
    elif (nowpage==pageNum and lastpNum==0 and viplen>0):
        offsetNum=0
        limitNum=20-lastpNum
        notvip=0
    elif (nowpage==pageNum and lastpNum==0 and viplen==0):
        offsetNum=0
        limitNum=20
        notvip=1
    elif (nowpage>pageNum and lastpNum==0):
        offsetNum=(nowpage-pageNum-1)*20
        limitNum=20-lastpNum
        notvip=1
    elif(nowpage>pageNum and lastpNum>0):
        offsetNum=((int(nowpage)-int(pageNum)-1)*20)+(20-int(lastpNum))
        limitNum=20
        notvip=1
    elif (viplen<1):
        offsetNum=(nowpage-1)*20
        limitNum=20
        notvip=1
    else:
        notvip=0
    #优先排序供求结束页的
    #test=str(lastpNum)+'|'+str(pageNum)+'|'+str(offsetNum)+'|'+str(limitNum)
    
    if (nowpage==pageNum and lastpNum!=0):
        listall=productList
    else:
        listall=[]
    if (notvip==1):
        list.SetLimits (offsetNum,limitNum,100000)
        if keywords=='':
            res = list.Query ('',nowsearcher)
        else:
            res = list.Query ('@(title,label0,label1,label2,label3,label4,city,province,tags) '+keywords+provincestr+'',nowsearcher)

        if res:
            if res.has_key('matches'):
                prodlist=res['matches']
                for list in prodlist:
                    id=list['id']
                    list1=getcompinfo(id,"",keywords2,company_id)
                    listall.append(list1)
                productList=listall
    
    #cache.set('productList', productList, 300)
    #底部页码
    #connt.close()
    try:
        page = int(pagenum)
        if int(page) < 1:
            page = 1
    except ValueError:
            page = 1
    page_listcount=int(ceil(listcount / 20))+1
    page_rangep=[]
    i=1
    while (i<=page_listcount):
        pages={'number':'','nowpage':''}
        pages['number']=i
        if (i==page):
            pages['nowpage']='1'
        else:
            pages['nowpage']=None
            
        page_rangep.append(pages)
        i+=1
    if (page_listcount>1 and page>1):
        firstpage=1
    else:
        firstpage=None
    if (page<page_listcount and page_listcount>1):
        lastpage=1
    else:
        lastpage=None
    if page >= after_range_num:
        page_range = page_rangep[page-after_range_num:page + before_range_num]
    else:
        page_range = page_rangep[0:int(page) + before_range_num]
    nextpage=int(page)+1
    prvpage=int(page)-1
    #大于500页提示

    if(page_listcount>500 and page>=500):
        arrtishi="提示：为了提供最相关的搜索结果，ZZ91再生网只显示500页信息，建议您重新搜索！"
    else:
        arrtishi=None
    return render_to_response('trade/list_new.html',locals())
def detail301(request):
    id=request.GET.get("id")
    return HttpResponsePermanentRedirect("/trade/detail"+str(id)+".html")
#----供求最终页
def detail(request,pid=""):
    host=getnowurl(request)
    showpost=1
    backurl=request.META.get('HTTP_REFERER','/')
    username=request.session.get("username",None)
    company_id=request.session.get("company_id",None)
    if username and (company_id==None or str(company_id)=="0"):
        company_id=zztrade.getcompanyid(username)
        request.session['company_id']=company_id
    nowlanmu='<a href="/category/">交易中心 </a>'
    nowlanmu2='<a href="/category/">交易中心 </a> > '
    keywords1=''
    keywords=request.GET.get("keywords")
    gmt_created=datetime.datetime.now()
    if not keywords:
        if '&' in backurl:
            keywords1=re.findall('keywords=(.*?)&',backurl)
        else:
            keywords1=re.findall('keywords=(.*)',backurl)
        #if keywords1:
          # keywords=urllib.unquote(keywords1[0])
    if keywords and keywords!="None":
        nowlanmu2+='<a href="/trade/?keywords='+str(keywords)+'">'+str(keywords)+'</a>&nbsp;>'
    if not pid:
        id=request.GET.get("id")
    else:
        id=pid
    done = request.path
    iszstflag=zztrade.getiszstcompany(company_id)
    list=zztrade.getproductdetail(id)
    #return HttpResponse(list)
    forcompany_id=0
    if list:
        forcompany_id=list['company_id']
    if forcompany_id==0:
        return render_to_response('404.html',locals())
    
    foriszstflag=zztrade.getiszstcompany(forcompany_id)
    #----判断举报状态
    reportcheck=zztrade.getreportcheck(company_id,forcompany_id,pid)
    if reportcheck==0:
        idcheck=1
        idchecktxt='举报处理中'
    if reportcheck==1:
        idcheck=1
        idchecktxt='举报已处理'
    if reportcheck==2:
        idcheck=1
        idchecktxt='举报退回'
    now = int(time.time())
    if now>1459440000:
        paymoney=10
    else:
        paymoney=5
    #该公司是否被举报成功过
    isjubao=zztrade.getreportischeck(forcompany_id,pid)
    #----判断是否为来电宝用户,获取来电宝余额
    isldb=None
    viptype=zzqianbao.getviptype(company_id)
#    if company_id==969597:#----测试信息
#        viptype='10051003'#----测试信息
    if viptype=='10051003':
        isldb=1
        paymoney=5
        ldbblance=ldb_weixin.getldblaveall(company_id)
        qianbaoblance=ldbblance
    else:
        qianbaoblance=zzqianbao.getqianbaoblance2(company_id)
    
#    if company_id==969597:#----测试信息
#        qianbaoblance=999999#----测试信息
    isseecompany=zzqianbao.getisseecompany(company_id,forcompany_id)
    if not isseecompany:
        paytype=request.GET.get("paytype")
        if paytype:
            if qianbaoblance>=paymoney:
                if isldb:
                    seepay=ldb_weixin.getpayfee(company_id,forcompany_id,paymoney)
                else:
                    seepay=zzqianbao.getpayfee(company_id,forcompany_id,id,paytype)
                if seepay==1:
                    isseecompany=1
            else:
                isseecompany==None
    #isseecompany=zzqianbao.getisseecompany(company_id,forcompany_id)
    #高会联系方式公开
    forviptype=zzqianbao.getviptype(forcompany_id)
    forvipflag=1
    if forviptype:
        if forviptype=="100510021001" or forviptype=="100510021002" or forviptype=="100510021000" or forviptype=="10051001":
            isseecompany=1
            forvipflag=None
    #z置顶客户显示联系方式
    keywordstopcompanyflag=zztrade.keywordstopcompany(id)
    if keywordstopcompanyflag:
        isseecompany=1
        forvipflag=None
    if list:
        #高会查看联系方式
        compzstflag=list['viptype']['vipcheck']
        if iszstflag==1 or compzstflag==1:
            viewflag=1
        else:
            viewflag=None
        webtitle=list['title']
        nowlanmu2+='&nbsp;'+str(webtitle)
        products_type_code=list['products_type_code']
    #钱包充值广告词
    #ggc=dbc.fetchnumberdb('select txt from qianbao_gg where id=1')
    return render_to_response('trade/detail.html',locals())

def seecompanycontact(request):
    username=request.session.get("username",None)
    company_id=request.session.get("company_id",None)
    if username and (company_id==None or str(company_id)=="0"):
        company_id=zztrade.getcompanyid(username)
        request.session['company_id']=company_id
    id=request.GET.get("id")
    iszstflag=zztrade.getiszstcompany(company_id)
    list=zztrade.getproductdetail(id)
    if not id:
        id=0
    forcompany_id=0
    if list:
        forcompany_id=list['company_id']
    if forcompany_id==0:
        return render_to_response('404.html',locals())
    
    foriszstflag=zztrade.getiszstcompany(forcompany_id)
    #----判断举报状态
    reportcheck=zztrade.getreportcheck(company_id,forcompany_id,id)
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
    isjubao=zztrade.getreportischeck(forcompany_id,id)
    #----判断是否为来电宝用户,获取来电宝余额
    isldb=None
    viptype=zzqianbao.getviptype(company_id)
    paymoney=10
    if viptype=='10051003':
        isldb=1
        paymoney=5
        ldbblance=ldb_weixin.getldblaveall(company_id)
        qianbaoblance=ldbblance
    else:
        qianbaoblance=zzqianbao.getqianbaoblance2(company_id)
    
#    if company_id==969597:#----测试信息
#        qianbaoblance=999999#----测试信息
    isseecompany=zzqianbao.getisseecompany(company_id,forcompany_id)
    if not isseecompany:
        paytype=request.GET.get("paytype")
        if paytype:
            if qianbaoblance>=paymoney:
                if isldb:
                    ldb_weixin.getpayfee(company_id,forcompany_id,paymoney)
                else:
                    zzqianbao.getpayfee(company_id,forcompany_id,id,paytype)
            else:
                isseecompany==None

def pro_report(request):
    company_id=request.GET.get("company_id")
    forcompany_id=request.GET.get("forcompany_id")
    product_id=request.GET.get("product_id")
    content=request.GET.get("chk_value")
    if content:
        #----一家公司只能被一个客户投诉一次
        sql='select id from pay_report where company_id=%s and forcompany_id=%s and product_id=%s'
        result=dbc.fetchonedb(sql,[company_id,forcompany_id,product_id])
        if not result:
            zztrade.getpro_report(company_id,forcompany_id,product_id,content)
    return HttpResponse('1')

#拨打电话记录
def telclicklog(request):
    username=request.session.get("username",None)
    company_id=request.session.get("company_id",None)
    backurl = request.META.get('HTTP_REFERER','/')
    if not company_id:
        company_id=request.GET.get("company_id",None)
    gmt_created=datetime.datetime.now()
    tel=request.GET.get("tel")
    pagefrom=request.GET.get("pagefrom")
    if username and (company_id==None or str(company_id)=="0"):
        company_id=zztrade.getcompanyid(username)
        request.session['company_id']=company_id
    if (company_id==None or str(company_id)=="0"):
        company_id=0
    sql="select id from phone_telclick_log where tel=%s and company_id=%s"
    result=dbc.fetchonedb(sql,[tel,company_id])
    if not result:
        sqlp="insert into phone_telclick_log(company_id,tel,pagefrom,gmt_created,url) values(%s,%s,%s,%s,%s)"
        dbc.updatetodb(sqlp,[company_id,tel,pagefrom,gmt_created,backurl])
    else:
        sqlp="update phone_telclick_log set num=num+1 where id=%s"
        dbc.updatetodb(sqlp,[result[0]])
    return HttpResponse('1')

def pricelist(request):
    keywords=request.GET.get("keywords")
    type=request.GET.get("type")
    page=request.GET.get("page")
    nowlanmu='<a href="/trade/">交易中心 </a>'
    if keywords:
        if type=="0":
            webtitle=keywords+"行情报价"
        else:
            webtitle=keywords+"商家报价"
    else:
        webtitle="行情报价"
    if not page:
        page=1
    funpage=zz91page()
    limitNum=funpage.limitNum(20)
    nowpage=funpage.nowpage(int(page))
    frompageCount=funpage.frompageCount()
    after_range_num = funpage.after_range_num(8)
    before_range_num = funpage.before_range_num(9)
    if type=='0':
        pricelist=zztrade.getprlist(frompageCount=frompageCount,limitNum=limitNum,kname=keywords)
    else:
        pricelist=zztrade.getpricelist_company(kname=keywords,frompageCount=frompageCount,limitNum=limitNum)
    listall=pricelist['list']
    listcount=pricelist['count']
    if (int(listcount)>1000000):
        listcount=1000000-1
    listcount = funpage.listcount(listcount)
    page_listcount=funpage.page_listcount()
    firstpage = funpage.firstpage()
    lastpage = funpage.lastpage()
    page_range  = funpage.page_range()
    nextpage = funpage.nextpage()
    prvpage = funpage.prvpage()
    return render_to_response('trade/pricelist.html',locals())

