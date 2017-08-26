#-*- coding:utf-8 -*-
import MySQLdb   
import settings
import codecs,cgi,requests
from django.utils.http import urlquote
from django.shortcuts import render_to_response
from django.http import HttpResponse,HttpResponseRedirect,HttpResponsePermanentRedirect,HttpResponseForbidden,HttpResponseNotFound
from django.core.paginator import Paginator,InvalidPage,EmptyPage,PageNotAnInteger
import time,jieba
import random
import sys
import datetime
from datetime import timedelta, date 
import os
from django.core.cache import cache
from zz91settings import SPHINXCONFIG,limitpath
from operator import itemgetter, attrgetter
import shutil
try:
    import cPickle as pickle
except ImportError:
    import pickle

from math import ceil
import memcache
from sphinxapi import *
from zz91page import *
from zz91db_ast import companydb
from zz91db_ads import adsdb
from zz91db_2_news import newsdb
dbc=companydb()
dbads=adsdb()
dbn=newsdb()

reload(sys)
sys.setdefaultencoding('UTF-8')

nowpath=os.path.dirname(__file__)
execfile(nowpath+"/function.py")
imgurl="http://img0.zz91.com"
mc = cache
zzqianbao=qianbao()

def default(request):
    category1000=getindexcategorylist("1000",1)
    category1001=getindexcategorylist("1001",1,None)
    category1002=getindexcategorylist("1002",1,None)
    category1003=getindexcategorylist("1003",1,None)
    category1004=getindexcategorylist("1004",1,None)
    category1005=getindexcategorylist("1005",1,None)
    category1006=getindexcategorylist("1006",1,None)
    category1007=getindexcategorylist("1007",0,None)
    category1008=getindexcategorylist("1008",1,None)
    category1009=getindexcategorylist("1009",1,None)
    category1012=getindexcategorylist("1012",1,None)
    category_yl=getindexcategorylist_yl('20091000',1)
    return render_to_response('default.html',locals())

def procode(request,code=''):
    if code:
        sql="select label from category_products where code=%s"
        result=dbc.fetchonedb(sql,[code])
        if result:
            label=result[0]
            if label:
                lebel_hex=getjiami(label)
                nowurl="/trade/s-"+lebel_hex+".html"
                return HttpResponsePermanentRedirect(nowurl)

def searchfirst(request):
    keywords = request.GET.get("keywords")
    if keywords:
        keywords=keywords.replace("利乐","无菌")
        keywords=keywords.replace("利乐包","无菌包")
    ptype = request.GET.get("ptype")
    if (ptype==None):
        ptype=""
    province = request.GET.get("province")
    if (province==None):
        province=""
    posttime = request.GET.get("posttime")
    if (posttime==None):
        posttime=""
    if (ptype==None):
        ptype=""
    keywords_hex=getjiami(keywords)
    nowurl="/trade/s-"+keywords_hex+".html?ptype="+str(ptype)+"&province="+province+"&posttime="+str(posttime)
    return HttpResponsePermanentRedirect(nowurl)
def searchfirstcommon(request):
    keywords = request.GET.get("keywords")
    ptype = request.GET.get("ptype")
    if (ptype==None):
        ptype=""
    province = request.GET.get("province")
    if (province==None):
        province=""
    posttime = request.GET.get("posttime")
    if (posttime==None):
        posttime=""
    if (ptype==None):
        ptype=""
    keywords_hex=getjiami(keywords)
    nowurl="/trade/commonlist/c-"+keywords_hex+"-1.html?ptype="+str(ptype)+"&province="+province+"&posttime="+str(posttime)
    return HttpResponsePermanentRedirect(nowurl)
#---图片页面
def tradepic(request,products_id):
    list=getproductsinfo(products_id,'')
    piclist=gettradepiclist(products_id)
    otherprolist=getcompanyproductslist(0,8,list['com_id'],None)
    return render_to_response('pic.html',locals())
#竞价点击计费
def hiturl(request):
    rd=request.GET.get("rd")
    area=request.GET.get("area")
    clientid=request.GET.get("clientid")
    company_id=request.session.get("company_id",None)
    gmt_created=datetime.datetime.now()
    t=random.randrange(0,1000000)
    userid=request.session.get("userid",None)
    if not userid:
        userid=getjiami(str(t)+str(gmt_created)+clientid)
        request.session['userid']=userid
    else:
        request.session['userid']=userid
    if not rd:
        return HttpResponse("err")
    sql="select key_id,pdt_id,id,keywords from app_jingjia_search where hiturl=%s"
    result=dbc.fetchonedb(sql,[rd])
    if result:
        key_id=result[0]
        pdt_id=result[1]
        search_id=result[2]
        keywords=result[3]
        if pdt_id:
            sql="select company_id,price from app_jingjia_keywords where id=%s"
            result=dbc.fetchonedb(sql,[key_id])
            if result:
                forcompany_id=result[0]
                price=result[1]
                sourcetype=1
                user_company_id=company_id
                if str(company_id)!=str(forcompany_id):
                    gmt_created=datetime.datetime.now()
                    sqlc="select id from app_jingjia_click where key_id=%s and userid=%s"
                    res=dbc.fetchonedb(sqlc,[key_id,userid])
                    if not res:
                        clickcount=1
                        sqld="insert into app_jingjia_click(key_id,search_id,price,clickcount,sourcetype,userid,user_company_id,company_id,area,gmt_created) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
                        dbc.updatetodb(sqld,[key_id,search_id,price,clickcount,sourcetype,userid,user_company_id,forcompany_id,area,gmt_created])
                        #扣款
                        zzqianbao.getpayfee(company_id=forcompany_id,forcompany_id=company_id,product_id=search_id,ftype=55,fee=-int(price))
                    else:
                        sqld="update app_jingjia_click set clickcount=clickcount+1 where id=%s"
                        dbc.updatetodb(sqld,[res[0]])
        
        return HttpResponseRedirect("http://trade.zz91.com/productdetails"+str(pdt_id)+".htm")
    else:
        return HttpResponse("err")
def tradelist(request,keywords):
    pinyinlist=englishlist()
    
    keywords_hex=keywords
    
    keywords=keywords.decode("hex").decode('utf8','ignore')
    
    keywords=keywords.replace("astojh","#")
    keywords=keywords.replace("astoxg","/")
    
    keywords=keywords.replace("astoxf","%")
    keywords=keywords.replace("astoxl","\\")
    keywords=keywords.replace("astohg","-")
    keywords=keywords.replace("astokhl","(")
    keywords=keywords.replace("astokhr",")")
    keywords_re=keywords
    mingang=getmingganword(keywords)
    if mingang:
        return HttpResponseNotFound("<h1>404</h1>")
    company_id=request.session.get("company_id",None)
    #if keywords:
        #保存搜索记录
        #updatesearchKeywords(request,company_id,keywords,ktype="pc_trade")
    if not company_id:
        appid=request.session.get("appid",None)
    else:
        appid=company_id
    #mysearchkeylist=getkeywords(appid)
    #---特殊处理 pmma广告
    if keywords.upper()=="PMMA":
        showtopad=None
    else:
        showtopad=1
    
    keywordsurlcode=urlquote(keywords)
    page = request.GET.get("page")
    #微门户关键词
    cplist=getcplist(keywords,50)
    #产业带
    marketlist=getmarketlist(keywords)
    
    mobileurl="/trade/?keywords="+keywords
    imgurl="http://img0.zz91.com"
    
    #您是不是在找
    xgcategorylist=getcategorylist(kname=keywords,limitcount=20)
    #第一条供求对应类别
    firsttradetypelist=getfirsttradetype(kname=keywords)
    if (firsttradetypelist):
        firsttradelabel=firsttradetypelist['label']
        firsttradecode=firsttradetypelist['code']
        #行业类别
        tradecode=""
        if len(firsttradecode)>4:
            tradecode=firsttradecode[0:len(firsttradecode)-4]
        if tradecode:
            hycategorylist=getindexcategorylist(tradecode,0,keywords=keywords)
        if len(firsttradecode)==4:
            hycategorylist=getindexcategorylist("0",0,keywords=keywords)
        #右边价格行业关键词
        rightpricelistnav=getrightpricenav(firsttradecode[0:4])
        i=1
        pricenavelist=[]
        if rightpricelistnav:
            for na in rightpricelistnav:
                na['n']=i
                i+=1
                if i>=4:
                    i=1
                pricenavelist.append(na)
            rightpricelistnav=pricenavelist
        #右边相关行情
        rightpricelist=getindexpricelist(kname=firsttradelabel,limitcount=10)
    
    #黄金展位
    goldadlist=getgoldadlist(keywords,"48")
    
    #righttagslist=gettagslist(0,50,keywords)
    #相关企业报价
    #companypricelist=getcompanypricelist(kname=keywords,limitcount=8)
    
    #相关资讯
    newslist=getnewslist(keywords=keywords,frompageCount=0,limitNum=10)
    
    page = request.GET.get("page")
    if (page == None or page=='' or page=="None"):
        page = 1

    searchname = urlquote(request.GET.get("searchname"))
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
    havepic = request.GET.get("havepic")
    isldb = request.GET.get("isldb")
    sorttype=request.GET.get("sorttype")
    if not sorttype:
        sorttype=''
    pdtidlist=''
    #竞价排名
    if (page==1):
        pdtidlist=keywordsTop(keywords)
        #jingjialist=getjingjialist(keywords=keywords,limitcount=10,mycompany_id='')
        #推荐原料供求
        #yuanliaoList=getyuanliaolist(kname=keywords,limitcount=4)
    else:
        pdtidlist=""
        jingjialist=""
    

    if (pdtidlist!=None and pdtidlist!=''):
        #arrpdtidlist=pdtidlist.split(',')
        arrpdtidlist=pdtidlist
        listall=[]
        n=1
        for p in arrpdtidlist:
            if (p!=''):
                list1=getproductsinfo(p[0],keywords)
                m=1
                if (n<=1):
                    m=1
                elif(n>1 and n<=3):
                    m=2
                elif (n>3 and n<=18):
                    m=3
                if (list1!=None):
                    list1['vippaibian']=str(m)
                    n+=1
                    listall.append(list1)
        productListtop=listall
    
    #--------------------------------------------
    if province:
        province=cgi.escape(province)
    if (province=='' or province == None):
        province=''
    provinces=province
    if (province=='江浙沪'):
        provinces='浙江|江苏|上海'
    if (province=='华东区'):
        provinces='江苏|浙江|安徽|福建|山东|上海'
    if (province=='华南区'):
        provinces='云南|广东|广西|台湾|海南|福建'
    if (province=='华中区'):
        provinces='河南|湖北|湖南|四川'
    if (province=='华北区'):
        provinces='北京|天津|河北|山西|内蒙古'
    if (province=='国外'):
        provinces='美国|韩国|英国|日本|德国|爱尔兰|加拿大|西班牙|澳大利亚|新西兰|波兰|泰国|新加坡|荷兰|南非|马来西亚|津巴布韦|越南|阿联酋|意大利|法国|菲律宾|乌克兰'
    if (pdt_kind == '' or pdt_kind == None or pdt_kind=="0"):
        pdt_type=''
        pdt_kind='0'
        pdtkindtxt="供求"
        seo_title=provinces+keywords+"_"+provinces+keywords+pdtkindtxt+"_"+provinces+keywords+"价格"+"_"+keywords+"产品属性介绍-"+keywords+"交易中心"
    if (pdt_kind =='1'):
        pdt_type='0'
        pdtkindtxt="供应"
        seo_title=pdtkindtxt+provinces+keywords+"_"+provinces+keywords+"_"+provinces+keywords+"价格"+"_"+keywords+"产品属性介绍-"+keywords+"交易中心"
    if (pdt_kind=='2'):
        pdt_type='1'
        pdtkindtxt="求购"
        seo_title=pdtkindtxt+provinces+keywords+"_"+provinces+keywords+"_"+provinces+keywords+"价格"+"_"+keywords+"产品属性介绍-"+keywords+"交易中心"
    if (pdt_kind=="3"):
        pdt_type=''
    nowsearcher="offersearch_new"
    
    
    #热搜关键词
    #hotsearchkeylist=gettagslist(0,10,'')
    
    nowpage=int(page)
    page=20*(int(page)-1)
    
    keywords2=keywords.replace(' ','')
    
    
    keywords1=urlquote(keywords2)
    ttype = request.GET.get("ttype")
    
    keywords=keywords.replace('\\',' ')
    keywords=keywords.replace('%%',' ')
    keywords=keywords.replace('/',' ')
    keywords=keywords.replace('(',' ')
    keywords=keywords.replace(')',' ')
    keywords=keywords.replace('+',' ')
    keywords=keywords.replace('CD-R','')
    #产品推荐
    aboutproducts=getindexofferlist(keywords,pdt_type,6)
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
    
    
    searchname=str(keywords1)
    searchname=searchname.replace('%28','astokhl')
    searchname=searchname.replace('%29','astokhr')
    searchname=searchname.replace('%5C','asto5c')
    searchname=searchname.replace('/','astoxg')
    searchname=searchname.replace('-','astohg')
    after_range_num = 4
    before_range_num = 3
    
    #关闭属性
    clearlabel=request.GET.get("clear")
    if clearlabel=="province":
        province=''
    if clearlabel=="pdt_kind":
        pdt_kind="0"
    if clearlabel=="stime":
        posttime=""
    
    
    #省市
    provincelist=getareavalue('10011000',label=province)
    #url 拼接
    action="?s=1"
    if (pdt_kind):
        action=action + "&ptype="+ str(pdt_kind)
    if (province):
        action=action + "&province="+ urlquote(province)
    if (posttime):
        action=action + "&posttime="+ str(posttime)
    if (priceflag):
        action=action + "&priceflag="+ str(priceflag)
    if (nopiclist):
        action=action + "&nopiclist="+ str(nopiclist)
    if (havepic):
        action=action + "&havepic="+ str(havepic)
    if sorttype:
        action=action + "&sorttype="+ str(sorttype)
    #导航
    navlist=getnavlist(keywords=keywords,actionurl=action)
    #----
    if (not posttime):
        stime=None
    else:
        if (str(posttime)=='1'):
            stime="一天内"
        if (str(posttime)=='3'):
            stime="三天内"
        if (str(posttime)=='7'):
            stime="一周内"
        if (str(posttime)=='30'):
            stime="一个月内"
        if (str(posttime)=='60'):
            stime="二个月内"

    #----------------------------开始读取数据
    port = settings.SPHINXCONFIG['port']
    cl = SphinxClient()
    list = SphinxClient()
    
    cl.SetServer ( settings.SPHINXCONFIG['serverid'], port )
    list.SetServer ( settings.SPHINXCONFIG['serverid'], port )
    cl.SetMatchMode ( SPH_MATCH_BOOLEAN )
    list.SetMatchMode ( SPH_MATCH_BOOLEAN )
    
    #取得总数
    nowdate=date.today()-timedelta(days=2)
    nextday=date.today()+timedelta(days=2)
    formatnowdate=time.mktime(nowdate.timetuple())
    formatnextday=time.mktime(nextday.timetuple())
    searstr=''
    if (pdt_kind !='0' and pdt_kind!="3"):
        searstr+=";filter=pdt_kind,"+pdt_type
        cl.SetFilter('pdt_kind',[int(pdt_type)])
        list.SetFilter('pdt_kind',[int(pdt_type)])
    cl.SetFilter('check_status',[1])
    list.SetFilter('check_status',[1])
    cl.SetFilter('is_pause',[0])
    list.SetFilter('is_pause',[0])
    if(havepic=='1'):
        cl.SetFilterRange('havepic',1,100)
        list.SetFilterRange('havepic',1,100)

    if (ttype == '1'):    
        cl.SetFilterRange('pdt_date',int(formatnowdate),int(formatnextday))
        list.SetFilterRange('pdt_date',int(formatnowdate),int(formatnextday))
       
        
    if (posttime =='' or posttime==None or posttime=='None'):
        searstr +=''
    else:
        pfromdate=date.today()-timedelta(days=int(posttime)+1)
        ptodate=date.today()+timedelta(days=3)
        
        pfromdate_int=int(time.mktime(pfromdate.timetuple()))
        ptodate_int=int(time.mktime(ptodate.timetuple()))
        if (pfromdate!=None):
            cl.SetFilterRange('pdt_date',int(pfromdate_int),int(ptodate_int))
            list.SetFilterRange('pdt_date',int(pfromdate_int),int(ptodate_int))
            

    if (province ==None or province ==''):
        provincestr=''
    else:
        provincestr='&@(province,city) '+provinces

    if (priceflag == '1'):
        cl.SetFilter('length_price',[0],True)
        list.SetFilter('length_price',[0],True)
        list.SetSortMode( SPH_SORT_EXTENDED,"length_price desc,refresh_time desc" )
    elif (priceflag == '2'):
        list.SetFilter('length_price',[0],True)
        list.SetSortMode( SPH_SORT_EXTENDED,"length_price asc,refresh_time desc" )
    else:
        list.SetSortMode( SPH_SORT_EXTENDED,"refresh_time desc" )
    res = list.Query ( '@(title,label0,label1,label2,label3,label4,city,province,tags) '+keywords+provincestr+'',nowsearcher)
    if not res:
        listcount=0
    else:
        listcount=res['total_found']

    #----来电宝条件筛选
    if isldb:
        cl.SetFilter('viptype',[3])
    #else:
        #cl.SetFilterRange('viptype',1,5)

    #获得3天内再生通数据优先排序
    #listallvip=cache.get('list'+action)
    nowsearcherTop="offersearch_new_vip"
    cl.SetSortMode( SPH_SORT_EXTENDED,"company_id desc,refresh_time desc" )
    cl.SetLimits (0,100000,100000)
    rescount = cl.Query ( '@(title,label0,label1,label2,label3,label4,city,province,tags) '+keywords+provincestr+'',nowsearcherTop)
    pcount=0
    listall=[]
    if rescount:
        if rescount.has_key('matches'):
            tagslist=rescount['matches']
            testcom_id=0
            pcount=1000000
            ppcount=1000
            for match in tagslist:
                id=match['id']
                com_id=match['attrs']['company_id']
                viptype=match['attrs']['viptype']
                viptype_ldb=match['attrs']['viptype_ldb']
                refresh_time=float(match['attrs']['refresh_time'])
                pdt_date=float(match['attrs']['pdt_date'])
                phone_rate=int(match['attrs']['phone_rate'])
                phone_level=float(match['attrs']['phone_level'])
                all_score=float(match['attrs']['all_score'])
                score=float(match['attrs']['score'])
                if viptype>=1:
                    if (testcom_id==com_id):
                        pcount-=1
                    else:
                        pcount=1000000
                else:
                    if (testcom_id==com_id):
                        ppcount-=1
                    else:
                        ppcount=1000
                    pcount=ppcount
                #接听率
                phone_sort=100
                if str(viptype_ldb)=="6":
                    if int(phone_rate)>=85:
                        phone_sort=100
                    else:
                        phone_sort=2
                    if int(phone_rate)==0:
                        phone_sort=100
                list1=[id,pcount,viptype,refresh_time,pdt_date,score,phone_sort,all_score]
                listall.append(list1)
                testcom_id=com_id
    if sorttype=="member":
        listallvip=sorted(listall, key=itemgetter(1,4,2,5,3),reverse=True)
    elif sorttype=="pro":
        listallvip=sorted(listall, key=itemgetter(1,4,5,2,3),reverse=True)
    else:
        listallvip=sorted(listall, key=itemgetter(1,4,7,2,3),reverse=True)
      
    #优先排序数
    viplen=len(listallvip)
    
    #供求总数
    listcount+=int(viplen)
    #最后一页的供求数
    lastpNum=int(viplen-ceil(viplen / 20)*20)
    #开始供求数位置
    beginpage=page
    #优先排序页码
    #pageNum=0
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
        list1=getproductsinfo(int(match[0]),keywords2)
        if list1:
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
        notvip=1
    elif (nowpage==pageNum and lastpNum==0 and viplen==0):
        offsetNum=0
        limitNum=20
        notvip=1
    elif (pageNum==1 and nowpage==pageNum and lastpNum==0 and viplen>0):
        offsetNum=0
        limitNum=20
        notvip=0
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
    if (offsetNum<0):
        offsetNum=0
    if (limitNum<0):
        limitNum=20
    if (nowpage==pageNum and lastpNum!=0):
        listall=productList
    else:
        if (pageNum==1 and nowpage==pageNum and lastpNum==0):
            listall=productList
            notvip=0
        else:
            listall=[]
    if (notvip==1):
        list.SetLimits(offsetNum,limitNum,100000)
        res = list.Query ( '@(title,label0,label1,label2,label3,label4,city,province,tags) '+keywords+provincestr+'',nowsearcher)
        
        if res:
            if res.has_key('matches'):
                prodlist=res['matches']
                for list in prodlist:
                    id=list['id']
                    list1=getproductsinfo(id,keywords2)
                    if list1:
                        listall.append(list1)
                productList=listall
                
    if not productList:
        #关键词分词
        keywords_fenchi = jieba.cut(keywords)
        fenchilist=[]
        noproducts=1
        seo_title="暂无信息"
        for fenchi in keywords_fenchi:
            if fenchi and fenchi!=" ":
                l={'label':fenchi,'label_hex':getjiami(fenchi)}
                fenchilist.append(l)
        listn = SphinxClient()
        listn.SetServer ( settings.SPHINXCONFIG['serverid'], port )
        listn.SetMatchMode ( SPH_MATCH_ANY )
        listn.SetSortMode( SPH_SORT_EXTENDED,"@weight desc" )
        listn.SetLimits(offsetNum,limitNum,100000)
        res = listn.Query ( '@(title,label0,label1,label2,label3,label4,city,province,tags) '+keywords+provincestr+'',nowsearcher)
        listall=[]
        productList=''
        if res:
            if res.has_key('matches'):
                prodlist=res['matches']
                for list in prodlist:
                    id=list['id']
                    list1=getproductsinfo(id,keywords2)
                    if list1:
                        listall.append(list1)
                productList=listall
    #cache.set('productList', productList, 300)
    #底部页码
    #connt.close()
    try:
        page = int(request.GET.get('page',1))
        if page < 1:
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
    nextpage=page+1
    prvpage=page-1
    if page>4:
        firstone=1
    if (page<page_listcount-3):
        lastone=1
    #大于500页提示
    
    if(page_listcount>500 and page>=500):
        arrtishi="提示：为了提供最相关的搜索结果，ZZ91再生网只显示500页信息，建议您重新搜索！"
    else:
        arrtishi=None
    return render_to_response('list.html',locals())
    #return render_to_response('index.html',locals())
    
#----普通客户推荐
def commoncustomer(request):
    lb1=gettjhex1()
    lb2=gettjhex2()
    lb3=gettjhex3()
    
    companycount=getnomolcompanycount()
    companylist1=getcommoncompanylist(keywords="废金属".decode('utf8','ignore'),num=8,pic=1,companyflag=1,picwidth=200,picheight=169)
    companylist2=getcommoncompanylist(keywords="废塑料".decode('utf8','ignore'),num=8,pic=1,companyflag=1,picwidth=200,picheight=169)
    companylist3=getcommoncompanylist(keywords="纺织品|废纸|二手设备|电子电器|橡胶|轮胎|服务".decode('utf8','ignore'),num=8,pic=1,companyflag=1,picwidth=200,picheight=169)
    return render_to_response('common.html',locals())
def metal(request):
    return commoncustomermore(request,getjiami("废金属".decode('utf8','ignore')),1)
def plastic(request):
    return commoncustomermore(request,getjiami("废塑料".decode('utf8','ignore')),1)
def comprehensive(request):
    return commoncustomermore(request,getjiami("纺织品|废纸|二手设备|电子电器|橡胶|轮胎|服务".decode('utf8','ignore')),1) 
#----普通客户推荐（活跃）翻页
def commoncustomermore(request,keywords,page):
    lb1=gettjhex1()
    lb2=gettjhex2()
    lb3=gettjhex3()
    t=request.GET.get("t")
    companycount=getnomolcompanycount()
    keywords_hex=keywords
    
    if (keywords=="c"):
        keywords="废 !金属 & !塑料"
    else:
        keywords=getjiemi(keywords)
    if (page==None):
        page=1
    province = request.GET.get("province")
    pdt_kind = request.GET.get("ptype")
    havepic = request.GET.get("havepic")
    price = request.GET.get("price")
    keywords1=urlquote(keywords).decode('utf8','ignore')
    if (province ==None or province ==''):
        provincestr=''
        provincetext="所在地"
    else:
        provincestr='&@(province,city) '+province
        provincetext=province
    
    action="?n=1" 
    if (province!=None and province!=""):
        action=action + "&province="+ urlquote(province)
    if (pdt_kind == '' or pdt_kind == None or pdt_kind=="0"):
        pdt_type=None
        pdt_kind='0'
        pdtkindtxt="供求"
        pdt_kind=""
        kindclass={'lm1':'navon','lm2':'','lm3':''}
    if (pdt_kind =='1'):
        pdt_type='0'
        pdtkindtxt="供应"
        kindclass={'lm1':'','lm2':'navon','lm3':''}
    if (pdt_kind=='2'):
        pdt_type='1'
        pdtkindtxt="求购"
        kindclass={'lm1':'','lm2':'','lm3':'navon'}
    action=action + "&ptype="+str(pdt_kind)
    if (havepic=="1"):
        pic="1"
        actionpic=action.replace("&havepic="+ str(havepic),"")
        action=action + "&havepic="+str(havepic)
    else:
        actionpic=action
        pic=None
        
    if (price=="1"):
        price="1"
        action=action + "&price="+str(price)
        actionprice=action.replace("&price="+ str(price),"")
    else:
        actionprice=action
        price=None
    
    if (province!=None and province!=""): 
        actionprovince=action.replace("&province="+ urlquote(province),"")
    else:
        actionprovince=action
        
    
    xgcategorylist=getcategorylist(kname=keywords,limitcount=20)
    provincelist=getareavalue('10011000')
    navlist=getnavlist_tj(keywords=keywords)
    company6=getcommoncompanylist(keywords=keywords,num=None,frompageCount=0,limitNum=6,pic=None,companyflag=1)
    firsttradetypelist=getfirsttradetype(kname=keywords)
    if (firsttradetypelist):
        firsttradelabel=firsttradetypelist['label']
        firsttradecode=firsttradetypelist['code']
        rightpricelistnav=getrightpricenav(firsttradecode[0:4])
        rightpricelist=getindexpricelist(kname=firsttradelabel,limitcount=10)
    #companypricelist=getcompanypricelist(kname=keywords,limitcount=8)
    indexpricelist=getindexpricelist(kname=keywords,limitcount=5)
    indexbbslist=getindexbbslist(kname=keywords,limitcount=5)
    
    funpage = zz91page()
    limitNum=funpage.limitNum(16)
    nowpage=funpage.nowpage(int(page))
    frompageCount=funpage.frompageCount()
    after_range_num = funpage.after_range_num(4)
    before_range_num = funpage.before_range_num(4)
    companylist=getcommoncompanylist(keywords=keywords+provincestr,num=None,frompageCount=frompageCount,limitNum=16,ptype=pdt_type,pic=pic,price=price,companyflag="1")
    
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
    
    return render_to_response('commonlist.html',locals())
    
def companyinfo(request):
    company_id = request.GET.get("company_id")
    compinfo=getcompanydetail(None,company_id)
    return render_to_response('companyinfo.html',locals())
def companyinfos(request):
    company_id = request.GET.get("company_id")
    compinfo=getcompanydetail(None,company_id)
    return render_to_response('companyinfos.html',locals())
def categoryinfo(request):
    categorycode = request.GET.get("categorycode")
    if categorycode=="20091000":
        categorylist=getindexcategorylist_yl(categorycode,1)
    else:
        categorylist=getindexcategorylist(categorycode,1)
    return render_to_response('categorylist.html',locals())

#供求列表跳转
def offerlist(request):
    id1=request.GET.get('id1')
    id2=request.GET.get('id2')
    id3=request.GET.get('id3')
    id4=request.GET.get('id4')
    sqls=""
    if (id1!="0" and id1):
        sqls=" oldid1="+str(id1)
    if (id2!="0" and id2):
        sqls=" oldid2="+str(id2)
    if (id3!="0" and id3):
        sqls=" oldid3="+str(id3)
    if (id4!="0" and id4):
        sqls=" oldid4="+str(id4)
    sql="select label from category_products where "+sqls
    cursor.execute(sql)
    nlist = cursor.fetchone()
    if nlist:
        label=nlist[0]
        keywords_hex=getjiami(label)
        nowurl="http://trade.zz91.com/trade/s-"+keywords_hex+".html"
    else:
        nowurl="http://trade.zz91.com"
    return HttpResponseRedirect(nowurl)

#获得5条原料供求
def yuanliaolist(request):
    keywords=request.GET.get('keywords')
    yuanliaoList=getyuanliaolist(kname=keywords,limitcount=5)
    return  render_to_response('yuanliaolist.html',locals())