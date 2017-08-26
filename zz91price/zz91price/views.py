#-*- coding:utf-8 -*-
from django.shortcuts import render_to_response
from django.http import HttpResponse,HttpResponseRedirect,HttpResponseNotFound,HttpResponsePermanentRedirect,HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt
from django.core.cache import cache
from zz91db import zz91news,getlightkeywords
from zz91settings import SPHINXCONFIG
from zz91tools import filter_tags,getjiami,getjiemi,subString,formattime,getpastday,int_to_str,int_to_str2,str_to_int,str_to_date,date_to_int,date_to_str,getpastoneday,getnextdate,getTomorrow,mobileuseragent
from zz91db_ast import companydb
from zz91page import *
from sphinxapi import *
from bs4 import BeautifulSoup
from func import PriceOffer
from study import index as studyindex
import MySQLdb,os,datetime,time,sys,calendar,urllib,simplejson,requests
try:
    import cStringIO as StringIO
except ImportError:
    import StringIO
dbc=companydb()

reload(sys)
sys.setdefaultencoding('UTF-8')
nowpath=os.path.dirname(__file__)
execfile(nowpath+"/func/function.py")
zzcomp=zz91company()
zznews=zz91news()
#zzcomp=zz91tags()
def pindex(request,pinyin=""):
    if (pinyin=="suliao"):
        labelname="废塑料"
        labelname1="废塑料日评"
        #----废塑料评论
        pinglun=zzcomp.getpricedblist(0,7,34)['list']
        #----塑料周报
        zhoubao=zzcomp.getpricedblist(0,7,35)['list']
        zongshu=zzcomp.getpricedblist(0,16,217)['list']
        shichang=zzcomp.getprlist(0,16,16,'',[60,61])['list']
        companyprice=zzcomp.getpricelist_company('塑料',0,5,9)['list']
        hangqing=zzcomp.getprlist(0,12,12,'',[20])['list']
        qihuo=zzcomp.getprlist(0,12,12,'',[233])['list']
        wangshang=zzcomp.getprlist(0,12,12,'',[137])['list']
        seotitle="废塑料网_废塑料价格|废塑料资讯|废塑料行情_报价资讯中心_ZZ91再生网"
        seokeywords="废塑料网,废塑料价格,废塑料资讯,废塑料行情,废塑料市场,abs ,eva,pa,pp,ps,pe,pvc,pc,pet,塑料颗粒"
        seodescription="ZZ91再生网旗下废塑料,为您提供各地区ABS价格,EVA价格,PA价格,PP价格,PS价格,PE价格,PVC价格,PC价格,PET价格,塑料颗粒价格等废塑料价格、市场动态、行情资讯、供应、求购信息,是废塑料商人销售产品、拓展市场及网络推广的可靠网站。"
    if (pinyin=="jinshu"):
        labelname="废金属"
        labelname1="废金属日评"
        pinglun=zzcomp.getpricedblist(0,7,32)['list']
        zhoubao=zzcomp.getpricedblist(0,7,33)['list']
        zongshu=zzcomp.getpricedblist(0,16,216)['list']
        shichang=zzcomp.getprlist(0,16,16,'',[69,70,71,72,206,66])['list']
        companyprice=zzcomp.getpricelist_company('金属',0,5,9)['list']
        hangqing=zzcomp.getprlist(0,12,12,'',[40,41,328,43,44,45,46,47,48,49,50,308,297])['list']
        qihuo=zzcomp.getprlist(0,12,12,'',[69,70,71,72,206,66])['list']
        wangshang=zzcomp.getprlist(0,12,12,'',[51])['list']
        seotitle="废金属网_废金属价格|废金属资讯|废金属行情_报价资讯中心_ZZ91再生网"
        seokeywords="废金属网,废金属价格,废金属资讯,废金属行情,废金属市场,废钢,废铁,废铜,废铝,废金属"
        seodescription="ZZ91再生网旗下废金属,为您提供各地区废钢价格、废铁价格、废铜价格、废铝价格等废金属价格、市场动态、行情资讯、供应、求购信息,是废金属商人销售产品、拓展市场及网络推广的可靠网站。"
    if (pinyin=="other"):
        labelname="综合废料"
        labelname1="油价"
        pinglun=zzcomp.getpricedblist(0,16,190)['list']
        zhoubao=None
        zongshu=zzcomp.getprlist(0,16,16,'',[218,219,220])['list']
        shichang=zzcomp.getprlist(0,16,16,'',[30])['list']
        companyprice=zzcomp.getpricelist_company('废纸',0,5,9)['list']
        companyprice=companyprice+zzcomp.getpricelist_company('综合',0,5,9)['list']
        hangqing=zzcomp.getprlist(0,12,12,'',[30,231,26,27,28,29])['list']
        qihuo=zzcomp.getprlist(0,12,12,'',[23])['list']
        wangshang=zzcomp.getprlist(0,12,12,'',[25])['list']
        seotitle="废纸废橡胶网_废纸价格|废橡胶价格|废纸价格行情|废橡胶价格行情_报价资讯中心_ZZ91再生网"
        seokeywords="废纸废橡胶网,废纸价格,废橡胶价格,废纸资讯,废橡胶资讯,废纸行情,废橡胶行情"
        seodescription="ZZ91再生网旗下废纸废橡胶网,为您提供废纸废橡胶报价、废纸废橡胶行情、废纸废橡胶再生技术、等废纸废橡胶资讯信息,是以废纸废橡胶为核心的一个专业频道版块。"
    suliao_daohang=zzcomp.getdaohanglist(100810011002)
    
    cplist=zzcomp.getcplist(SPHINXCONFIG,'',20)
    
    price_link=zzcomp.getdaohanglist(100810011003)
    
    return render_to_response('main/pindex.html',locals())

def pricedetail301(request,id):
    jumpurl='http://jiage.zz91.com/detail/'+id+".html"
    return HttpResponsePermanentRedirect(jumpurl)
def price301(request,typeid='',page='',page1=''):
    jumpurl='http://jiage.zz91.com/'
    id=request.GET.get('id')
    if id:
        jumpurl+='hotchart-'+id+'.html'
    elif typeid:
        pinyin=zzcomp.getpricecategorypinyin(typeid)
        pinyin=pinyin.replace('-','_')
        pinyin=pinyin.replace('/','_')
        jumpurl+=pinyin+'/'
    return HttpResponsePermanentRedirect(jumpurl)
def cprice301(request,page='',cid='',kwd='',code='',numb='',pr1='',pr2=''):
    jumpurl='http://jiage.zz91.com/'
    categoryCompanyPriceCode=request.GET.get('categoryCompanyPriceCode')
    areaCode=request.GET.get('areaCode')
    id=request.GET.get('id')
    if areaCode:
        area=zzcomp.getclabel(areaCode)
        jumpurl+='cprice/'
        hexkwd=getjiami(area)
        jumpurl+='_k'+hexkwd+'_/'
        return HttpResponsePermanentRedirect(jumpurl)
    if categoryCompanyPriceCode:
        jumpurl+='cprice-'+categoryCompanyPriceCode+'/'
        return HttpResponsePermanentRedirect(jumpurl)
    elif id:
        jumpurl+='cdetail/'+id+'.html'
        return HttpResponsePermanentRedirect(jumpurl)
    elif cid:
        jumpurl+='cdetail/'+str(cid)+'.html'
        return HttpResponsePermanentRedirect(jumpurl)
    else:
        nsk=0
        if code:
            jumpurl+='cprice-'+code+'/'
        else:
            jumpurl+='cprice/'
        if kwd:
            hexkwd=getjiami(kwd)
            jumpurl+='_k'+hexkwd+'_'
            nsk=1
        if numb:
            jumpurl+='_d'+numb+'_'
            nsk=1
        if pr1 and pr2:
            if pr1=='0' and pr2=='1000':
                jumpurl+='_q1a1000_'
            elif pr1=='1000' and pr2=='3000':
                jumpurl+='_q1000a3000_'
            elif pr1=='3000' and pr2=='5000':
                jumpurl+='_q3000a5000_'
            elif pr1=='5000' and pr2=='10000':
                jumpurl+='_q5000a10000_'
            elif pr1=='10000' and pr2=='1000000':
                jumpurl+='_10000a1000000_'
            nsk=1
        if nsk==1:
            jumpurl+='/'
        if page:
            tpage=int(page)
            tpage=(tpage/20)+1
            jumpurl+='p'+str(tpage)+'.html'
    return HttpResponsePermanentRedirect(jumpurl)
def hotchart(request,chartnum='',chartcid='',page=''):
    gmt_begin=request.GET.get('gmt_begin')
    gmt_end=request.GET.get('gmt_end')
    longtime=1
    chartarg=''
    if chartcid:
        chartarg=chartcid
    if gmt_begin and gmt_end:
        chartarg+=','+gmt_begin+','+gmt_end
        timedifferent=getimedifferent(gmt_begin,gmt_end)
        if timedifferent>92:
            longtime=''
#    if chartnum=='1':
    kindname=''
    typename=''
    stitle=''
    if chartcid:
        kindname=zzcomp.getchart_category(chartcid)
    if chartcid in ['7','8','9','10','11','12']:
#        chartemp='lmechart'
        typename='伦敦LME期货'
        label='伦敦LME'+kindname+'期货价格'
        chartclist=[
              {'name':'废铜','id':'7'},
              {'name':'废铝','id':'8'},
              {'name':'废铅','id':'9'},
              {'name':'废锌','id':'10'},
              {'name':'废锡','id':'11'},
              {'name':'废镍','id':'12'},
              ]
        stitle='LME'
        skindname=kindname.replace('废','')
        title='LME'+skindname+'价走势图_伦敦'+skindname+'价走势图_行情报价中心-zz91再生网'
        keywords='LME'+skindname+'价走势图，伦敦'+skindname+'价走势图'
        description='zz91再生网价格走势图频道，为您精心整理LME'+skindname+'价走势图，更多伦敦'+skindname+'价走势图，都在zz91再生网，专业的数据，助您快速知悉市场动态。'
    elif chartcid in ['13','14','15','16']:
#        chartemp='feitongchart'
        typename='废铜'
        chartclist=[
              {'name':'江浙沪光亮铜','id':'13'},
              {'name':'江浙沪黄杂铜','id':'14'},
              {'name':'广东南海光亮铜','id':'15'},
              {'name':'广东南海黄杂铜','id':'16'},
              ]
        stitle=typename
        title=kindname+'价格走势图_行情报价中心-zz91再生网'
        keywords=kindname+'价格走势图'
        description='zz91再生网价格走势图频道，为您精心整理'+kindname+'价格走势图，更多地区铜价走势图，都在zz91再生网，专业的数据，助您快速知悉市场动态。'
    elif chartcid in ['17','18','23','24']:
        typename='废不锈钢'
        chartclist=[
              {'name':'广东南海国产304','id':'17'},
              {'name':'广东南海进口304','id':'18'},
              {'name':'江浙沪国产304','id':'23'},
              {'name':'江浙沪进口304','id':'24'},
              ]
        stitle=typename
        title=''
        keywords=''
        description=''
        title=kindname+'价格走势图_行情报价中心-zz91再生网'
        keywords=kindname+'价格走势图'
        description='zz91再生网价格走势图频道，为您精心整理'+kindname+'价格走势图，更多地区铜价走势图，都在zz91再生网，专业的数据，助您快速知悉市场动态。'
    elif chartcid in ['19','20','21','22']:
        typename='废铅锌'
        chartclist=[
              {'name':'锌合金(无铅)','id':'19'},
              {'name':'锌合金(含铅)','id':'20'},
              {'name':'软铅皮','id':'21'},
              {'name':'破碎铅','id':'22'},
              ]
        stitle=typename
        title=kindname+'价格走势图_行情报价中心-zz91再生网'
        keywords=kindname+'价格走势图'
        description='zz91再生网价格走势图频道，为您精心整理'+kindname+'价格走势图，更多地区铅锌价走势图，都在zz91再生网，专业的数据，助您快速知悉市场动态。'
    elif chartcid in ['31','32','33','34']:
        typename='上海废金属'
        chartclist=[
              {'name':'沪铜','id':'31'},
              {'name':'沪铝','id':'32'},
              {'name':'沪锌','id':'33'},
              {'name':'沪钢','id':'34'},
              ]
        stitle=typename
        title=kindname+'价格走势图_行情报价中心-zz91再生网'
        keywords=kindname+'价格走势图'
        description='zz91再生网价格走势图频道，为您精心整理'+kindname+'价格走势图，更多地区铅锌价走势图，都在zz91再生网，专业的数据，助您快速知悉市场动态。'
    else:
        return render_to_response('404.html',locals())
    hexlabel=getjiami(stitle)
    hangqinglist=zzcomp.getprlist(0,6,6,typename)['list']
    aboucomplist=zzcomp.getpricelist_company(kname=stitle,frompageCount=0,limitNum=9,maxcount=9)['list']
    if not page:
        page=1
    funpage=zz91page()
    limitNum=funpage.limitNum(15)
    nowpage=funpage.nowpage(int(page))
    frompageCount=funpage.frompageCount()
    after_range_num = funpage.after_range_num(3)
    before_range_num = funpage.before_range_num(6)
    chartdatalistall=zzcomp.getchartdatalistall(frompageCount,limitNum,chartcid)
    listcount=0
    plist=chartdatalistall['list']
    listcount=chartdatalistall['count']
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
    return render_to_response('main/hotchart.html',locals())
#----走势图4张
def chartdetail(request):
#    lmechartlist=zzcomp.getchartlist('期货价格')
    chartarg=request.GET.get('chartarg')
    gmt_begin=''
    gmt_end=''
    if ',' in chartarg:
        chartarglist=chartarg.split(',')
        chartcid=chartarglist[0]
        gmt_begin=chartarglist[1]
        gmt_end=getnextdate(chartarglist[2])
    else:
        gmt_end=getTomorrow()
        gmt_begin=getpastoneday(30)
        chartcid=chartarg
    gmtlist=zzcomp.getchartgmtlist('期货价格',gmt_begin,gmt_end)
    if chartcid in ['7','8','9','10','11','12']:
        chart10list=zzcomp.getchartdetailist('金属价格（10：00）',chartcid,gmt_begin,gmt_end)
        chart11list=zzcomp.getchartdetailist('金属价格（11：40）',chartcid,gmt_begin,gmt_end)
        chart14list=zzcomp.getchartdetailist('金属价格（14：55）',chartcid,gmt_begin,gmt_end)
    else:
        kindname=zzcomp.getchart_category(chartcid)
        feitonglist=zzcomp.getchartdetailist('',chartcid,gmt_begin,gmt_end)
    return render_to_response('main/chartdetail.html',locals())
#----走势图4张
def lmechart(request):
    gmtlist=zzcomp.getchartgmtlist('期货价格')
    lmechartlist=zzcomp.getchartlist('期货价格')
    return render_to_response('main/charturl.html',locals())
def feitongchart(request):
    gmtlist=zzcomp.getchartgmtlist('废铜价格')
    lmechartlist=zzcomp.getchartlist('废铜价格')
    return render_to_response('main/charturl.html',locals())
def feibxgchart(request):
    gmtlist=zzcomp.getchartgmtlist('废不锈钢价格')
    lmechartlist=zzcomp.getchartlist('废不锈钢价格')
    return render_to_response('main/charturl.html',locals())
def feiqianxinchart(request):
    gmtlist=zzcomp.getchartgmtlist('江浙沪废锌/铅价格')
    lmechartlist=zzcomp.getchartlist('江浙沪废锌/铅价格')
    return render_to_response('main/charturl.html',locals())

@csrf_exempt
def pricehuilv(request):
#    numb=request.GET.get('numb')
#    miancountry=request.GET.get('miancountry')
#    country=request.GET.get('country')
    numb=request.POST['numb']
    miancountry=request.POST['miancountry']
    country=request.POST['country']
    huilvlist=zzcomp.gethuilvlist(numb,miancountry,country)
    if huilvlist:
        huilvlist1=huilvlist[0]
        huilvlist2=huilvlist[1]
        content=numb+miancountry+'='+str(huilvlist2)+country+'&nbsp;&nbsp;('+numb+country+'='+str(huilvlist1)+miancountry+')'
    else:
        content=""
    return HttpResponse(content)
#选择地区
def selectarealabel(request):
    type_id=request.GET.get("type_id")
    assist_id=request.GET.get("assist_id")
    gmt_begin=request.GET.get("gmt_begin")
    gmt_begin=str_to_int(gmt_begin)
    area=request.GET.get("area")
    id=zzcomp.getpricesearchlabel(kname=area,category_id=type_id,assist_id=assist_id,gmt_begin='')
    return HttpResponsePermanentRedirect('/detailn/'+str(id)+'.html')
#新版 2016
def pricedetailn(request,id=""):
    mobileflag=request.GET.get("mobileflag")
    #id=request.GET.get("id")
    if mobileflag and id:
        return HttpResponsePermanentRedirect('http://m.zz91.com/priceviews/?id='+id)
    numb=1
    
    
    sql='select title,type_id,assist_type_id,content,gmt_created,tags from price where id=%s'
    result=zzcomp.dbc.fetchonedb(sql,[id])
    if result:
        content=result[3]
        content=zzcomp.replacedetaila(content)
        title1=result[0]
        type_id=result[1]
        assist_id=assist_type_id=result[2]
        gmt_modified=formattime(result[4],1)
        categoryname=zzcomp.getpricecategory(type_id)
        #二级类别名
        assistname=zzcomp.getpricecategory(assist_id)
        #---企业报价
        if not content:
            pricedatalist=zzcomp.getpricedatalist(id)
        else:
            #---国际期货233 用原数据
            if type_id==233:
                pricelist=None
            else:
                #选择类别
                maindetail=zzcomp.getmaindetail(type_id)
                maintypename=maindetail['maintypename']
                maincategory=maindetail['maincategory']
                if '金属' in maincategory:
                    arealist=zzcomp.getpricearealist(type_id,1,title=title1)
                else:
                    arealist=zzcomp.getpricearealist(assist_type_id,1,title=title1)
                #历史其他时间供求
                searchtitle=re.sub(r'(.*?)日','',title1)
                
                gmt_begin=gettimecha(gmt_modified,-12)
                gmt_end=gettimecha(gmt_modified,2)
                if '废塑料网上报价' in searchtitle:
                    #为了完全匹配,以免出现塑料颗粒网上报价
                    searchtitle='"'+searchtitle+'"'
                histplist=zzcomp.getpricetimelist(limitNum=3,kname=searchtitle,category_id=[type_id],assist_id=[assist_id],gmt_begin=gmt_begin,gmt_end=gmt_end,id=id)
                #数据字段
                pricefield=zzcomp.getpricefield2(categoryid=type_id,assist_type_id=assist_type_id,priceid=id)
                
                listname=pricefield['listname']
                listfield=pricefield['listfield']
#                pricelist=zzcomp.getprice_list(frompageCount=0,limitNum=30,maxcount=30,listfiled=listfield,priceid=int(id))
                firstid=0
                pricelist=zzcomp.getdetailpricelist(id,listfield)
                if pricelist:
                    if pricelist[0]:
                        firstid=pricelist[0]['id']
                #相关企业报价
                comppricelist=zzcomp.getpricelist_company(categoryname,0,8,8)['list']
                if not comppricelist:
                    comppricelist=zzcomp.getpricelist_company(maintypename,0,8,8)['list']
                #相关互助
                bbslist=zzcomp.getbbslist(categoryname,8)
                if not bbslist:
                    bbslist=zzcomp.getbbslist(maintypename,8)
                #相关资讯
                newslist=zznews.getnewslist(SPHINXCONFIG,keywords=categoryname,frompageCount=0,limitNum=8,typeid="",typeid2="",allnum=8,arg='',flag='')
                if not newslist:
                    newslist=zznews.getnewslist(SPHINXCONFIG,keywords='',frompageCount=0,limitNum=8,typeid="",typeid2=typeid2,allnum=8,arg='',flag='',MATCH="1")
                #微门户关键词
                cplist=zzcomp.getcplist(SPHINXCONFIG,categoryname,30)
                #pricelist=None  DISTINCT
        id=int(id)
        timenow=int(time.time()*1000)
        title=title1+'_行情报价中心-zz91再生网'
        keywords=''
        description='zz91再生网'+categoryname+'行情报价中心，为您提供'+title+'，信息准确可靠，让您及时掌握一手'+assistname+categoryname+'价格信息，熟悉及时'+assistname+categoryname+'市场动态。'
    return render_to_response('main/pricedetailn.html',locals())

def pricedetail(request,id=''):
    #agent=request.META['HTTP_USER_AGENT']
    #agentflag=mobileuseragent(agent)
    mobileflag=request.GET.get("mobileflag")
    if mobileflag and id:
        return HttpResponsePermanentRedirect('http://m.zz91.com/priceviews/?id='+id)
    numb=1
    miancountry='人民币'
    country='美元'
    listcountry1=['人民币','美元','欧元','英镑','港元','台币','澳元','韩元','日元']
    listcountry2=['美元','欧元','英镑','港元','人民币','台币','澳元','韩元','日元']
    huilvlist=zzcomp.gethuilvlist(numb,miancountry,country)
    if huilvlist:
        huilvlist1=huilvlist[0]
        huilvlist2=huilvlist[1]
    sql='select title,type_id,assist_type_id,content,gmt_created,tags from price where id=%s'
    result=zzcomp.dbc.fetchonedb(sql,[id])
    if result:
        content=result[3]
        content=zzcomp.replacedetaila(content)
        title1=result[0]
        type_id=result[1]
        
        assist_type_id=result[2]
        #---企业报价
        if not content:
            pricedatalist=zzcomp.getpricedatalist(id)
        else:
            #---国际期货233 用原数据
            if type_id==233:
                pricelist=None
            else:
                #----替换内容锚文本,有些最终页不是表格,是直接显示出来的
#                content=zzcomp.replacedetaila(content)#内容里面已经被加好了锚文本,进行替换会产生其他冲突
                #pricefield=zzcomp.getpricefield(id)
                pricefield=zzcomp.getpricefield2(categoryid=type_id,assist_type_id=assist_type_id,priceid=id)
                
                listname=pricefield['listname']
                listfield=pricefield['listfield']
#                pricelist=zzcomp.getprice_list(frompageCount=0,limitNum=30,maxcount=30,listfiled=listfield,priceid=int(id))
                pricelist=zzcomp.getdetailpricelist(id,listfield)
                if pricelist:
                    if type_id in [40,42,328,41,45,47,44,308,46,49]:
                        return pricedetailn(request,id=id)
                #pricelist=None  DISTINCT
        #类别名
        categoryname=zzcomp.getpricecategory(type_id)
        assist_id=result[2]
        #二级类别名
        assistname=zzcomp.getpricecategory(assist_id)
        gmt_modified=formattime(result[4],1)
        tags=result[5]
        #标签
        taglist=tags.split(',')
        tgslist=[]
        for tag1 in taglist:
            tag_hex=getjiami(tag1)
            tgslist.append({'tag':tag1,'tag_hex':tag_hex})
        tgslist=getdaohanglist(tags,num=5)
        keywords=""
        if taglist:
            for l in taglist:
                keywords+="|"+l
        #微门户关键词
        cplist=zzcomp.getcplist(SPHINXCONFIG,keywords,20)
        
        searchtitle=re.sub(u'.*?日','',title1)
        gmt_begin=gettimecha(gmt_modified,-9)
        gmt_end=gettimecha(gmt_modified,7)
        if '废塑料网上报价' in searchtitle:
            #为了完全匹配,以免出现塑料颗粒网上报价
            searchtitle='"'+searchtitle+'"'
        #histplist=zzcomp.getpricetimelist(limitNum='3',kname=searchtitle,category_id=[type_id],assist_id=[assist_id],gmt_begin=gmt_begin,gmt_end=gmt_end)
        histplist=zzcomp.getprlist(0,7,1000,searchtitle,[type_id],[assist_id],arg='3',gmt_begin=gmt_begin,gmt_end=gmt_end)['list']
        if len(histplist)<=1:
            histplist=''
        aboutlist=zzcomp.getprlist(0,10,10,'',[type_id],[assist_id],1)['list']
        if not aboutlist:
            aboutlist=zzcomp.getprlist(0,8,8,'',[type_id])['list']
        if not aboutlist:
            aboutlist=zzcomp.getprlist(0,8,8,'','',[assist_id])['list']
        
        maindetail=zzcomp.getmaindetail(type_id)
        maintypename=maindetail['maintypename']
        maincategory=maindetail['maincategory']
        if maintypename=='废金属':
            typeid2=[153,154]
            maintype='废金属'
            typecode=100810031000
            areacode=100810031001
        elif maintypename=='废塑料':
            typeid2=[155]
            maintype='废塑料'
            typecode=100810031002
            areacode=100810031003
        else:
            typeid2=[156]
            maintype='综合废料'
            typecode=100810031004
            areacode=100810031005
        
        typecodelist=zzcomp.gettypecodelist(typecode)
        areacodelist=zzcomp.gettypecodelist(areacode)
        offerlist=zzcomp.getofferlist(categoryname,"",4,1)
        if not offerlist:
            offerlist=zzcomp.getofferlist(maintypename,"",4,1)
        bbslist=zzcomp.getbbslist(categoryname,6)
        if not bbslist:
            bbslist=zzcomp.getbbslist(maintypename,6)
        newslist=zznews.getnewslist(SPHINXCONFIG,keywords=categoryname,frompageCount=0,limitNum=10,typeid="",typeid2="",allnum=10,arg='',flag='',MATCH=1)
        if not newslist:
            newslist=zznews.getnewslist(SPHINXCONFIG,keywords='',frompageCount=0,limitNum=10,typeid="",typeid2=typeid2,allnum=10,arg='',flag='',MATCH=1)
        id=int(id)
        timenow=int(time.time()*1000)
        title=title1+'_行情报价中心-zz91再生网'
        keywords=''
        description='zz91再生网'+categoryname+'行情报价中心，为您提供'+title+'，信息准确可靠，让您及时掌握一手'+assistname+categoryname+'价格信息，熟悉及时'+assistname+categoryname+'市场动态。'
 
    return render_to_response('main/pricedetail.html',locals())

def pricelist(request,pinyin,type='',areapinyin='',areapinyin2='',attrpinyin='',timedate='',page=''):
    attrbute=""
    page_type=""
    pinyin=pinyin.replace("PVC1","PVC")
    pinyin=pinyin.replace("ABS1","ABS")
    time_today=time.strftime('%Y%m%d',time.localtime(time.time()))
    area=''
#    areapinyin=request.GET.get('areapinyin')
    if areapinyin:
        area=zzcomp.getpriceattrlabel(areapinyin)
        #----这部分是市场价的地区,是根据price_category来的
        if not area:
            area=zzcomp.getpricecategoryname(areapinyin)
    
    area2=''
    if areapinyin2:
        area2=zzcomp.getpriceattrlabel(areapinyin2)
        
    attrbute=''
    if attrpinyin:
        attrbute=zzcomp.getpriceattrlabel(attrpinyin)
    gmt_begin=request.GET.get('gmt_begin')
    gmt_end=request.GET.get('gmt_end')
    timedate2=''
    gmt_begin2=''
    gmt_end2=''
    if timedate:
        timedate=str(timedate)
        timedate2=gettimeall(timedate)
        timedate2=str_to_int(timedate2)
    categoryvalue=None
    assistvalue=None
    chichangjia=None
    if '_' in pinyin:
        pinyin=pinyin.replace('_','/')
    categorydetail=zzcomp.getcategorydetail(pinyin)
    categoryid=categorydetail['id']
    categoryid2=categoryid
    if categoryid:
        #----塑料市场价
        if categoryid2 in (60,64):
            if areapinyin:
                categorydetail2=zzcomp.getcategorydetail(areapinyin)
                categoryid=categorydetail2['id']
                chichangjia=1
        categoryvalue=[int(categoryid)]

#    return HttpResponse(str(areapinyin))
    categoryname=categorydetail['name']
    categoryname=categoryname.replace('价格','')
    categoryname=categoryname.replace('行情','')
    categoryname=categoryname.replace('废塑料','')
    categoryname=categoryname.strip()
    
    hex_categoryname=getjiami(categoryname)
    maindetail=zzcomp.getmaindetail(categoryid)
    maintypename=maindetail['maintypename']
    maincategory=maindetail['maincategory']
    
    searchcategory=categoryname
    if maincategory=='塑料地区':
        searchcategory='塑料'
    if maincategory=='金属地区':
        searchcategory='金属'
    
    
    mobileflag=request.GET.get("mobileflag")
    if mobileflag and categoryid:
        if maincategory in ['塑料地区','金属产品']:
            return HttpResponsePermanentRedirect('http://m.zz91.com/price/?category_id='+str(categoryid))
        else:
            return HttpResponsePermanentRedirect('http://m.zz91.com/price/?assist_id='+str(categoryid))
    if mobileflag and not categoryid:
        return HttpResponseNotFound("404")

    listfiled=[]
    listname=[]
    
    pricefield=zzcomp.getpricefield2(categoryid)
    if pricefield:
        listname=pricefield['listname']
        listfiled=pricefield['listfield']
    else:
        pricelist1=zzcomp.getprice_list(keywords=searchcategory,frompageCount=0,limitNum=1,area=area,categoryid=categoryid)
        if pricelist1:
            pricelist1=pricelist1['list']
        if pricelist1:
            priceid=pricelist1[0]['priceid']
            pricefield=zzcomp.getpricefield(priceid)
            listname=pricefield['listname']
            listfiled=pricefield['listfield']

    aboucomplist=zzcomp.getpricelist_company(searchcategory,0,9,9)['list']
    if not aboucomplist:
        aboucomplist=zzcomp.getpricelist_company(maintypename,0,9,9)['list']
    offerlist=zzcomp.getofferlist(searchcategory,"",4,1)
    if not offerlist:
        offerlist=zzcomp.getofferlist(maintypename,"",4,1)
    hangqinglist=zzcomp.getprlist(0,6,6,searchcategory)['list']
    if not hangqinglist:
        hangqinglist=zzcomp.getprlist(0,6,6,maintypename)['list']
#    arealist=zzcomp.getarealist(categoryname,0,56)
    arealist=zzcomp.getpricearealist(categoryid,103)
    if arealist:
        areactg=1
    else:
        arealist=zzcomp.getpricearealist(categoryid=categoryid,parent_id=1,page_type='0',morelist=1)
    shuxinglist=zzcomp.getpricearealist(categoryid,2)
#    if not arealist:
#        arealist=zzcomp.getarealist(searchcategory,0,56,area)
    nowmonthdayslist=getnowmonthdayslist()
    if gmt_begin:
        gmt_begin2=str_to_int(gmt_begin)
    if gmt_end:
        gmt_end2=str_to_int(gmt_end)
    if not page:
        page=1
    funpage=zz91page()
    limitNum=funpage.limitNum(15)
    nowpage=funpage.nowpage(int(page))
    frompageCount=funpage.frompageCount()
    after_range_num = funpage.after_range_num(3)
    before_range_num = funpage.before_range_num(6)
    if categoryid in [25,51,137]:
        if categoryid==25:
            scategory='纸'
        if categoryid==51:
            scategory='金属'
        if categoryid==137:
            scategory='塑料'
        netpricelist=1
        if timedate:
            gmt_begin2=timedate2
            gmt_end2=timedate2+3600*24
        pricelist=zzcomp.getnetpricelist(scategory,categoryid,frompageCount,limitNum,gmt_begin2,gmt_end2)
    else:
#        pricelist={'list':[],'count':0}
        pricelist=zzcomp.getprice_list(keywords=searchcategory,frompageCount=frompageCount,limitNum=limitNum,timedate=timedate2,gmt_begin=gmt_begin2,gmt_end=gmt_end2,area=area+' '+area2,listfiled=listfiled,attrbute=attrbute,categoryid=categoryid)
    listcount=0
    if pricelist:
        plist=pricelist['list']
        listcount=pricelist['count']
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
    
    seolist=seolistcontent(1,page_type,maintypename,categoryid,categoryname,page,area=area,attrbute=attrbute,pinyin=pinyin,maincategory=maincategory,areapinyin=areapinyin)
    title=seolist['title']
    keywords=seolist['keywords']
    description=seolist['description']
    
    if maintypename=='废金属':
        jinshu_hqzs=zzcomp.getprlist(0,10,10,'',[216])['list']
        return render_to_response('main/jinshupricelist.html',locals())
    if maintypename=='废塑料':
        suliao_hqzs=zzcomp.getprlist(0,10,10,'',[217])['list']
        suliao_zaowan=zzcomp.getprlist(0,10,10,'行情早参|行情晚报',[217])['list']
        suliao_pinglun=zzcomp.getprlist(0,7,7,'',[34])['list']
            
        return render_to_response('main/suliaopricelist.html',locals())
    else:
        zonghe_zongshu=zzcomp.getprlist(0,8,8,'',[218,219])['list']
        zonghe_pinglun=zzcomp.getprlist(0,7,7,'',[36,37,38,39,214,215])['list']
        marketlist=zzcomp.getmarketlist(categoryname)
        return render_to_response('main/pricelist.html',locals())

def priceindex(request,pinyin='',areapinyin='',attrpinyin='',timedate='',page=''):
    attrbute=''
    if pinyin=='companyprice':
        return HttpResponsePermanentRedirect('/cpriceindex/')
    if pinyin in ("suliao","jinshu","other"):
        return pindex(request,pinyin=pinyin)
    if pinyin=="study":
        return studyindex(request)
    #if pinyin:
        #pinyin=pinyin.upper()
    pinyin=pinyin.replace("PVC1","pvc")
    pinyin=pinyin.replace("ABS1","abs")
    categoryvalue=None
    assistvalue=None
    gmt_begin=request.GET.get('gmt_begin')
    gmt_end=request.GET.get('gmt_end')
    area=''
    if areapinyin:
        area=zzcomp.getpriceattrlabel(areapinyin)
    timedate2=''
    gmt_begin2=''
    gmt_end2=''
    if attrpinyin:
        attrbute=zzcomp.getpriceattrlabel(attrpinyin)
        attrbute=attrbute.replace(categoryname,'')
        searcharg=attrbute
    if timedate:
        timedate=str(timedate)
        timedate2=gettimeall(timedate)
        timedate2=str_to_int(timedate2)
    if '_' in pinyin:
        if 'feisuliaoqihuo' in pinyin and 'guoji' in pinyin:
            pinyin=pinyin.replace('_','-')
        elif 'feisuliaoqihuo' in pinyin and 'xianggang' in pinyin:
            pinyin=pinyin.replace('_','-')
    categorydetail=zzcomp.getcategorydetail(pinyin)
    
    categoryid=categorydetail['id']
#    return HttpResponse('categoryid')
    categoryparentid=zzcomp.getparent_id(categoryid)
    if categoryid:
        categoryvalue=[int(categoryid)]
    categoryname=categorydetail['name']
    categoryname=categoryname.replace('油价','原油期货价格')
    cplist=zzcomp.getcplist(SPHINXCONFIG,categoryname,20)
    page_type=categorydetail['page_type']
    hex_categoryname=getjiami(categoryname)
    maindetail=zzcomp.getmaindetail(categoryid)
    maintypename=maindetail['maintypename']
    maincategory=maindetail['maincategory']
    
    searchcategory=categoryname
    #----转入手机站
    #agent=request.META['HTTP_USER_AGENT']
    #agentflag=mobileuseragent(agent)
    mobileflag=request.GET.get("mobileflag")
    if mobileflag and categoryid:
        if maincategory in ['塑料地区','金属产品']:
            return HttpResponsePermanentRedirect('http://m.zz91.com/price/?category_id='+str(categoryid))
        else:
            return HttpResponsePermanentRedirect('http://m.zz91.com/price/?assist_id='+str(categoryid))
    if maincategory=='塑料地区':
        searchcategory='塑料'
    if maincategory=='金属地区':
        searchcategory='金属'
    if maintypename=='废金属':
        maintype='废金属'
        typecode=100810031000
        areacode=100810031001
    elif maintypename=='废塑料':
        maintype='废塑料'
        typecode=100810031002
        areacode=100810031003
    else:
        maintype='综合废料'
        typecode=100810031004
        areacode=100810031005
    typecodelist=zzcomp.gettypecodelist(typecode)
    areacodelist=zzcomp.gettypecodelist(areacode)
    offerlist=zzcomp.getofferlist(searchcategory,"",4,1)
    if not offerlist:
        offerlist=zzcomp.getofferlist(maintypename,"",4,1)
    bbslist=zzcomp.getbbslist(searchcategory,6)
    if not bbslist:
        bbslist=zzcomp.getbbslist(maintypename,6)
    newslist=zznews.getnewslist(SPHINXCONFIG,keywords=searchcategory,frompageCount=0,limitNum=10,typeid="",typeid2="",allnum=10,arg='',flag='',MATCH=1)
#    aboucomplist=zzcomp.getpricelist_company(categoryname,0,9)['list']
#    if not aboucomplist:
#        aboucomplist=zzcomp.getpricelist_company(maintypename,0,9)['list']
#    offerlist=zzcomp.getofferlist(categoryname,"",5,1)
#    hangqinglist=zzcomp.getprlist(0,6,6,categoryname)['list']
#    arealist=zzcomp.getarealist(categoryname,0,56)
#    arealist=zzcomp.getpricearealist(categoryid)
    
    area_list=[]
    arealist=zzcomp.getpricearealist(categoryid,103)
    if arealist:
        areactg=1
    else:
        arealist=zzcomp.getpricearealist(categoryid,1)
    if categoryid in (60,64) :
        arealist=zzcomp.getpricecategorychildlist(categoryid)
    shuxinglist=zzcomp.getpricearealist(categoryid,2)
    if page_type:
        page_type=int(page_type)
    else:
        page_type=0
    if page_type==0:
        #if not arealist:
        #    return render_to_response('404.html',locals())
        for areas in arealist:
            label1=areas['label']
            pinyin1=areas['pinyin']
            page_type11=areas['page_type']
            if categoryid in (60,64):
                categoryvalue=[areas['id']]
                #label1=None
            if label1=='其它':
                label1='国内'
            prlist1=zzcomp.getprlist(frompageCount=0,limitNum=6,maxcount=6,kname=label1,category_id=categoryvalue)['list']
            if not prlist1:
                prlist1=zzcomp.getprlist(frompageCount=0,limitNum=6,maxcount=6,kname=label1+" "+categoryname)['list']
            listal={'label':label1,'pinyin':pinyin1,'list':prlist1,'page_type':page_type11}
            area_list.append(listal)
        seolist=seolistcontent(1,page_type,maintypename,categoryid,categoryname,page,area=area,attrbute=attrbute,pinyin=pinyin,maincategory=maincategory,areapinyin=areapinyin)
        title=seolist['title']
        keywords=seolist['keywords']
        description=seolist['description']
        marketlist=zzcomp.getmarketlist(categoryname)
        return render_to_response('main/priceindex.html',locals())
    elif page_type==2:
        listfiled=[]
        listname=[]
        aboucomplist=zzcomp.getpricelist_company(searchcategory,0,9,9)['list']
        if not aboucomplist:
            aboucomplist=zzcomp.getpricelist_company(maintypename,0,9,9)['list']
        nowmonthdayslist=getnowmonthdayslist()
        time_today=time.strftime('%Y%m%d',time.localtime(time.time()))
        arealist=zzcomp.getpricearealist(categoryid,1)
        pricefield=zzcomp.getpricefield2(categoryid)
        if pricefield:
            listname=pricefield['listname']
            listfiled=pricefield['listfield']
        else:
            pricelist1=zzcomp.getprice_list(keywords=searchcategory,frompageCount=0,limitNum=1,area=area,categoryid=categoryid,maxcount=1)['list']
            if pricelist1:
                priceid=pricelist1[0]['priceid']
                pricefield=zzcomp.getpricefield(priceid)
                listname=pricefield['listname']
                listfiled=pricefield['listfield']
        if not page:
            page=1
        if page<1:
            page=1
        funpage=zz91page()
        limitNum=funpage.limitNum(15)
        nowpage=funpage.nowpage(int(page))
        frompageCount=funpage.frompageCount()
        after_range_num = funpage.after_range_num(3)
        before_range_num = funpage.before_range_num(6)
        if categoryid in [25,51,137]:
            if categoryid==25:
                scategory='纸'
            if categoryid==51:
                scategory='金属'
            if categoryid==137:
                scategory='塑料'
            netpricelist=1
#            return HttpResponse(str(categoryid))
            pricelist=zzcomp.getnetpricelist(scategory,categoryid,frompageCount,limitNum)
#            sql='SELECT a.id,a.price_id,a.price_id as pprice_id,a.product_name,a.product_name as pproduct_name,a.quote,a.quote as pquote,a.area,a.area as parea,a.company_name,a.company_name as pcompany_name,a.company_id,a.company_id as pcompany_id,UNIX_TIMESTAMP(a.gmt_created) as pgmt_created,b.category_company_price_code,c.label,c.label as plabel FROM company_price as b left join price_data as a on a.company_price_id=b.id left join category_company_price as c on b.category_company_price_code=c.code limit 0,10'
#            result0=zzcomp.dbc.fetchalldb(sql)
#            return render_to_response('main/pricelist2.html',locals())
        else:
            pricelist=zzcomp.getprice_list(keywords=searchcategory,frompageCount=frompageCount,limitNum=limitNum,timedate=timedate2,gmt_begin=gmt_begin2,gmt_end=gmt_end2,area=area,listfiled=listfiled,categoryid=categoryid)
        listcount=0
        plist=pricelist['list']
        #if not plist:
        #    return render_to_response('404.html',locals())
        listcount=pricelist['count']
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
        hangqinglist=zzcomp.getprlist(0,6,6,searchcategory)['list']
        if not hangqinglist:
            hangqinglist=zzcomp.getprlist(0,6,6,maintypename)['list']
        
        seolist=seolistcontent(1,page_type,maintypename,categoryid,categoryname,page,area=area,attrbute=attrbute,pinyin=pinyin,maincategory=maincategory,areapinyin=areapinyin)
        title=seolist['title']
        keywords=seolist['keywords']
        description=seolist['description']
        
        if maintypename=='废金属':
            jinshu_hqzs=zzcomp.getprlist(0,10,10,'',[216])['list']
            return render_to_response('main/jinshupricelist.html',locals())
        if maintypename=='废塑料':
            suliao_hqzs=zzcomp.getprlist(0,10,10,'',[217])['list']
            suliao_zaowan=zzcomp.getprlist(0,10,10,'行情早参|行情晚报',[217])['list']
            suliao_pinglun=zzcomp.getprlist(0,7,7,'',[34])['list']
            marketlist=zzcomp.getmarketlist(categoryname)
            return render_to_response('main/suliaopricelist.html',locals())
        else:
            zonghe_zongshu=zzcomp.getprlist(0,8,8,'',[218,219])['list']
            zonghe_pinglun=zzcomp.getprlist(0,7,7,'',[36,37,38,39,214,215])['list']
            marketlist=zzcomp.getmarketlist(categoryname)
            return render_to_response('main/pricelist.html',locals())
    elif str(page_type)=="1":
        if not page:
            page=1
        funpage=zz91page()
        limitNum=funpage.limitNum(10)
        nowpage=funpage.nowpage(int(page))
        frompageCount=funpage.frompageCount()
        after_range_num = funpage.after_range_num(3)
        before_range_num = funpage.before_range_num(4)
        if maintypename=='废塑料':
            if categoryid==22:
                categoryvalue=[127,128,129,130,132,138,142,315,316,317,318,319,320,321,322]
                pricelist=zzcomp.getprlist(frompageCount=frompageCount,limitNum=limitNum,maxcount=100000,category_id=categoryvalue)
            elif categoryid==60:
                categoryvalue=[110,111,112,113,114,115,118,119,120,126,324]
                pricelist=zzcomp.getprlist(frompageCount=frompageCount,limitNum=limitNum,maxcount=100000,category_id=categoryvalue)
            elif categoryid==110:
                categoryvalue=[324,110]
                pricelist=zzcomp.getprlist(frompageCount=frompageCount,limitNum=limitNum,maxcount=100000,category_id=categoryvalue)
            elif categoryid==42:
                categoryvalue=[328,42]
                pricelist=zzcomp.getprlist(frompageCount=frompageCount,limitNum=limitNum,maxcount=100000,category_id=categoryvalue)
            elif categoryparentid==22 or categoryid in (20,34,35,61,62,233,63):
                pricelist=zzcomp.getprlist(frompageCount=frompageCount,limitNum=limitNum,maxcount=100000,category_id=categoryvalue)
            #
            elif categoryparentid==60:
                pricelist=zzcomp.getprlist(frompageCount=frompageCount,limitNum=limitNum,maxcount=100000,category_id=categoryvalue)
            else:
                pricelist=zzcomp.getprlist(frompageCount=frompageCount,limitNum=limitNum,maxcount=100000,assist_id=categoryvalue)
            if not pricelist['list']:
                pricelist=zzcomp.getprlist(frompageCount=frompageCount,limitNum=limitNum,maxcount=100000,category_id=categoryvalue)
        else:
            if categoryid==13:
                categoryvalue=[231,23,25,26,27,28,29]
            if categoryid==14:
                categoryvalue=[36,37]
            if categoryid==220:
                categoryvalue=[218,219]
            if categoryid==64:
                categoryvalue=[69,70,71,72,206]
            if categoryparentid==3:
                pricelist=zzcomp.getprlist(frompageCount=frompageCount,limitNum=limitNum,maxcount=100000,assist_id=categoryvalue)
            else:
                pricelist=zzcomp.getprlist(frompageCount=frompageCount,limitNum=limitNum,maxcount=100000,category_id=categoryvalue)
        listcount=0
        if (pricelist):
            listall=pricelist['list']
            listcount=pricelist['count']
            if (int(listcount)>1000000):
                listcount=1000000-1
        if listcount==0:
            listall=None
        #if not listall:
        #    return render_to_response('404.html',locals())
        listcount = funpage.listcount(listcount)
        page_listcount=funpage.page_listcount()
        firstpage = funpage.firstpage()
        lastpage = funpage.lastpage()
        page_range  = funpage.page_range()
        if len(page_range)>5:
            page_range=page_range[:5]
        nextpage = funpage.nextpage()
        prvpage = funpage.prvpage()
        
        seolist=seolistcontent(1,page_type,maintypename,categoryid,categoryname,page,area=area,attrbute=attrbute,pinyin=pinyin,maincategory=maincategory,areapinyin=areapinyin)
        title=seolist['title']
        keywords=seolist['keywords']
        description=seolist['description']
        
        pinyin=pinyin.replace('/','_')
        pinyin=pinyin.replace('-','_')
        marketlist=zzcomp.getmarketlist(categoryname)
        #return HttpResponse(marketlist)
        return render_to_response('main/pricetxtlist.html',locals())
    
    #return render_to_response('404.html',locals())

def pricelist_txt(request,pinyin='',areapinyin='',attrpinyin='',page=''):
    categoryvalue=None
    assistvalue=None
    area=''
    searcharg=''
    if areapinyin:
        area=zzcomp.getpriceattrlabel(areapinyin)
        searcharg+=area
    if '_' in pinyin:
        pinyin=pinyin.replace('_','/')
    categorydetail=zzcomp.getcategorydetail(pinyin)
    categoryid=categorydetail['id']
    if categoryid==64:
        categorydetail=zzcomp.getcategorydetail(areapinyin)
        categoryid=categorydetail['id']
#        if attrpinyin:
#            area=attrpinyin
    if categoryid:
        categoryvalue=[int(categoryid)]
    
#    arealist=zzcomp.getpricearealist(categoryid,103)
#    if arealist:
#        areactg=1
#    else:
#        arealist=zzcomp.getpricearealist(categoryid=categoryid,parent_id=1,page_type='1',morelist=1)
#    shuxinglist=zzcomp.getpricearealist(categoryid,2)
    
    area_list=[]
    arealist=zzcomp.getpricearealist(categoryid,103)
    if arealist:
        areactg=1
    else:
        arealist=zzcomp.getpricearealist(categoryid,1)
    if categoryid in (60,64) :
        if areapinyin:
            categorydetail=zzcomp.getcategorydetail(areapinyin)
            categoryid=categorydetail['id']
            categoryvalue=[int(categoryid)]
    categoryparentid=zzcomp.getparent_id(categoryid)
    shuxinglist=zzcomp.getpricearealist(categoryid,2)  

    categoryname=categorydetail['name']
    page_type=categorydetail['page_type']
    hex_categoryname=getjiami(categoryname)
    maindetail=zzcomp.getmaindetail(categoryid)
    maintypename=maindetail['maintypename']
    maincategory=maindetail['maincategory']
    
    attrbute=''
    if attrpinyin:
        attrbute=zzcomp.getpriceattrlabel(attrpinyin)
        attrbute=attrbute.replace(categoryname,'')
        searcharg=attrbute
            
#    return HttpResponse(maincategory)
    searchcategory=categoryname
    if maincategory=='塑料地区':
        searchcategory='塑料'
    if maincategory=='金属地区':
        searchcategory='金属'

    if maintypename=='废金属':
        maintype='废金属'
        typecode=100810031000
        areacode=100810031001
    elif maintypename=='废塑料':
        maintype='废塑料'
        typecode=100810031002
        areacode=100810031003
    else:
        maintype='综合废料'
        typecode=100810031004
        areacode=100810031005
        
    mobileflag=request.GET.get("mobileflag")
    if mobileflag and categoryid:
        if maincategory in ['塑料地区','金属产品']:
            return HttpResponsePermanentRedirect('http://m.zz91.com/price/?category_id='+str(categoryid))
        else:
            return HttpResponsePermanentRedirect('http://m.zz91.com/price/?assist_id='+str(categoryid))
    
    typecodelist=zzcomp.gettypecodelist(typecode)
    areacodelist=zzcomp.gettypecodelist(areacode)
    offerlist=zzcomp.getofferlist(searchcategory,"",4,1)
    if not offerlist:
        offerlist=zzcomp.getofferlist(maintypename,"",4,1)
    bbslist=zzcomp.getbbslist(searchcategory,6)
    newslist=zznews.getnewslist(SPHINXCONFIG,keywords=searchcategory,frompageCount=0,limitNum=10,typeid="",typeid2="",allnum=10,arg='',flag='',MATCH=1)
    if not page:
        page=1
    funpage=zz91page()
    limitNum=funpage.limitNum(10)
    nowpage=funpage.nowpage(int(page))
    frompageCount=funpage.frompageCount()
    after_range_num = funpage.after_range_num(3)
    before_range_num = funpage.before_range_num(4)
    
    if maintypename=='废塑料':
        if categoryid==22:
            categoryvalue=[127,128,129,130,132,138,142,315,316,317,318,319,320,321,322]
            pricelist=zzcomp.getprlist(frompageCount=frompageCount,limitNum=limitNum,kname=searcharg,category_id=categoryvalue)
        elif categoryid==60:
            categoryvalue=[110,111,112,113,114,115,118,119,120,126,324]
            pricelist=zzcomp.getprlist(frompageCount=frompageCount,limitNum=limitNum,kname=searcharg,category_id=categoryvalue)
        elif categoryid==110:
            categoryvalue=[324,110]
            pricelist=zzcomp.getprlist(frompageCount=frompageCount,limitNum=limitNum,kname=searcharg,category_id=categoryvalue)
        elif categoryid==42:
            categoryvalue=[328,42]
            pricelist=zzcomp.getprlist(frompageCount=frompageCount,limitNum=limitNum,kname=searcharg,category_id=categoryvalue)
        elif categoryparentid==22 or categoryid in (20,34,35,61,62,233,63):
            pricelist=zzcomp.getprlist(frompageCount=frompageCount,limitNum=limitNum,kname=searcharg,category_id=categoryvalue)
        elif categoryparentid==60:
            pricelist=zzcomp.getprlist(frompageCount=frompageCount,limitNum=limitNum,kname=searcharg,category_id=categoryvalue)
        else:
            pricelist=zzcomp.getprlist(frompageCount=frompageCount,limitNum=limitNum,kname=searcharg,assist_id=categoryvalue)
        if not pricelist['list']:
            pricelist=zzcomp.getprlist(frompageCount=frompageCount,limitNum=limitNum,kname=searcharg,category_id=categoryvalue)
    else:
        if categoryid==13:
            categoryvalue=[231,23,25,26,27,28,29]
        if categoryid==14:
            categoryvalue=[36,37]
        if categoryid==220:
            categoryvalue=[218,219]
        if categoryparentid==3:
            pricelist=zzcomp.getprlist(frompageCount=frompageCount,limitNum=limitNum,kname=searcharg,assist_id=categoryvalue)
        else:
            pricelist=zzcomp.getprlist(frompageCount=frompageCount,limitNum=limitNum,kname=searcharg,category_id=categoryvalue)
        if not pricelist['list']:
            pricelist=zzcomp.getprlist(frompageCount=frompageCount,limitNum=limitNum,kname=searcharg,assist_id=categoryvalue)

    listcount=0
    if (pricelist):
        listall=pricelist['list']
        listcount=pricelist['count']
        if (int(listcount)>1000000):
            listcount=1000000-1
    if listcount==0:
        listall=None
    listcount = funpage.listcount(listcount)
    page_listcount=funpage.page_listcount()
    firstpage = funpage.firstpage()
    lastpage = funpage.lastpage()
    page_range  = funpage.page_range()
    if len(page_range)>5:
        page_range=page_range[:5]
    nextpage = funpage.nextpage()
    prvpage = funpage.prvpage()
    
    seolist=seolistcontent(2,page_type,maintypename,categoryid,categoryname,page,area=area,attrbute=attrbute,pinyin=pinyin,maincategory=maincategory,areapinyin=areapinyin,searcharg=searcharg)
    title=seolist['title']
    keywords=seolist['keywords']
    description=seolist['description']
    
    pinyin=pinyin.replace('/','_')
    marketlist=zzcomp.getmarketlist(categoryname)
    return render_to_response('main/pricetxtlist.html',locals())
#----price首页
def default(request):
    #agent=request.META['HTTP_USER_AGENT']
    #agentflag=mobileuseragent(agent)
    mobileflag=request.GET.get("mobileflag")
    if mobileflag:
        return HttpResponsePermanentRedirect('http://m.zz91.com/jiage/')
#    return render_to_response('main/index1.html',locals())
    title='废金属价格_废塑料价格行情 _废纸价格_废橡胶价格_行情报价中心-zz91再生网（原中国再生资源交易网）'
    keywords='废金属价格，废塑料价格，废橡胶价格，废纸价格，zz91再生网'
    description='ZZ91再生网报价资讯中心每天为您提供及时的废金属价格、废塑料价格行情、废纸价格、废橡胶价格等主流废料价格，实时更新，快速获取，安心做生意，放心有保障。'
    #行情研究院最新
    price_yjy1=zzcomp.getpricedblist(frompageCount=0,limitNum=3,typeid="359,360")
    price_yjy2=zzcomp.getpricedblist(frompageCount=3,limitNum=3,typeid="359,360")
    #----4个期货数据
    qihuo4=zzcomp.getqihuolist()
    time_today=time.strftime('%Y-%m-%d',time.localtime(time.time()))
    time_str=time.strftime('%m月%d日',time.localtime(time.time()))
    #----现货有色
    xianhuo_youse=zzcomp.getprlist(0,15,15,'',[79,80,81,210,83,84],'','','1')['list']
    #----现货lme
    xianhuo_lme=zzcomp.getprlist(0,15,15,'',[69,70,71,72,206],'','','1')['list']
    #----全国废铜
    #feitong_area=zzcomp.getprlist(0,1,1,'',[40],'','','1')['list'][0]
    #----各地废钢采购价价
    #feigangcaihou_area=zzcomp.getprlist(0,1,1,'',[279],'','','1')['list'][0]
    #----全国各地废金属报价
    jinshu_area=zzcomp.getprlist(0,15,15,'',[40,279,308,41,328,45,43,44,46,47,49,50],'','','1')['list']
    #----贵金属
    jinshu_guijinshu=zzcomp.getprlist(0,2,2,'',[86,208])['list']
    #----废金属日评
#    jinshu_pinglun=zzcomp.getprlist(0,7,7,'',[32])['list']
    jinshu_pinglun=zzcomp.getpricedblist(0,5,32)['list']
    #----废金属周报
#    jinshu_zhoubao=zzcomp.getprlist(0,7,7,'',[33])['list']
    jinshu_zhoubao=zzcomp.getpricedblist(0,6,33)['list']
    #----废金属行情综述
#    jinshu_hqzs=zzcomp.getprlist(0,8,8,'',[216])['list']
    jinshu_hqzs=zzcomp.getpricedblist(0,5,216)['list']
    #----国内废塑料
#    suliao_guonei=zzcomp.getprlist(0,9,9,'',[20])['list']
    suliao_guonei=zzcomp.getpricedblist(0,9,20)['list']
    #----塑料期货
#    suliao_qihuo=zzcomp.getprlist(0,6,6,'',[233])['list']
    suliao_qihuo=zzcomp.getpricedblist(0,6,233)['list']
    #----欧洲废塑料
#    ouzhou_suliao=zzcomp.getprlist(0,7,7,'',[63])['list']
    #塑料网上报价
    wangshang_suliao=zzcomp.getpricedblist(0,7,137)['list']
    #----美国废塑料
#    meiguo_suliao=zzcomp.getprlist(0,7,7,'',[62])['list']
    #废塑料采购价
    caigou_suliao=zzcomp.getpricedblist(0,7,337)['list']
    #----塑料再生料
#    suliao_zsl=zzcomp.getprlist(0,8,8,'',[98])['list']
    suliao_zsl=zzcomp.getpricedblist(0,8,98)['list']
    #----塑料新料
#    suliao_xinliao=zzcomp.getprlist(0,7,7,'',[21,60,61,110,111,112,113,114,115,118,119,120,121,126])['list']
    #----油价快报
#    youjia_kuaibao=zzcomp.getprlist(0,8,8,'',[190])['list']
    youjia_kuaibao=zzcomp.getpricedblist(0,8,190)['list']
    #----塑料评论
#    suliao_pinglun=zzcomp.getprlist(0,7,7,'',[34])['list']
    suliao_pinglun=zzcomp.getpricedblist(0,7,34)['list']
    #----塑料周报
#    suliao_zhoubao=zzcomp.getprlist(0,7,7,'',[35])['list']
    suliao_zhoubao=zzcomp.getpricedblist(0,7,35)['list']
    #----综合废料综述
    zonghe_zongshu=zzcomp.getprlist(0,8,8,'',[218,219])['list']
    #----废橡胶价格
#    xiangjiao_jiage=zzcomp.getprlist(0,8,8,'',[30])['list']
    xiangjiao_jiage=zzcomp.getpricedblist(0,8,30)['list']
    #----废纸价格
#    feizhi_jiage=zzcomp.getprlist(0,8,8,'',[231])['list']
    feizhi_jiage=zzcomp.getpricedblist(0,8,231)['list']
    #----废纸网上报价
#    zonghe_pinglun=zzcomp.getprlist(0,8,8,'',[25])['list']
    zonghe_pinglun=zzcomp.getpricedblist(0,8,25)['list']
    #----底部导航
    suliao_daohang=zzcomp.getdaohanglist(100810011002)
    
    cplist=zzcomp.getcplist(SPHINXCONFIG,'',20)
    
    #----最新塑料报价
    suliaobaojia=zzcomp.getpricelist_company('塑料',0,5,9)['list']
#    suliaobaojia=zzcomp.getprlist(0,5,5,'',[22,127,128,129,130,132,137,138,142,315,316,317,318,319,320,321,322])['list']
    #----最新金属报价
    jinshubaojia=zzcomp.getpricelist_company('金属',0,5,9)['list']
#    jinshubaojia=zzcomp.getprlist(0,5,5,'',[40,41,42,43,44,45,46,47,48,49,50,51,52,308])['list']
#    suliaopricelist=zzcomp.getprice_list('塑料',0,5)
    price_link=zzcomp.getdaohanglist(100810011003)
    return render_to_response('main/default.html',locals())

#----price搜索
def searchfirst(request):
    keywords = request.GET.get("keywords")
    if keywords==None:
        search=request.GET.get("search")
        keywords=search
        if search==None:
            title = request.GET.get("title")
            keywords=title
    keywords_hex=getjiami(keywords)
    nowurl="/s/"+keywords_hex+"-0/"
    return HttpResponseRedirect(nowurl)
def price_search(request,keywords_hex='',type='',page=''):
    if keywords_hex:
        keywords=getjiemi(keywords_hex)
        if keywords:
            keywords=keywords.upper()
            keywords=keywords.replace("报价","").replace("价格","").replace("今日","")
    else:
        keywords=request.GET.get('keywords')
        
        if keywords:
            keywords=keywords.upper()
            keywords=keywords.replace("报价","").replace("价格","").replace("今日","")
            keywords_hex=getjiami(keywords)
    #mingang=getmingganword(keywords)
    #if mingang:
    #    return HttpResponseForbidden("<h1>FORBIDDEN</h1>")
    k=request.GET.get('k')
    if keywords:
        xgcategorylist=zzcomp.getcategorylist(SPHINXCONFIG,keywords,24)
        cplist=zzcomp.getcplist(SPHINXCONFIG,keywords,50)
        ######统计搜索词
#        gmt_created=getToday()
#        detailtime=datetime.datetime.now()
#        if request.META.has_key('HTTP_X_FORWARDED_FOR'):
#            ip =  request.META['HTTP_X_FORWARDED_FOR']
#        else:
#            ip = request.META['REMOTE_ADDR']
        #zzother.addsearch_keywords(5,keywords,ip,gmt_created,detailtime,1)
        ######
        maintype=zzcomp.getoffertype(keywords,"",1,0)
        pricetype=zzcomp.getpricelist(frompageCount=0,limitNum=1,maxcount=1,kname=keywords)
        newslist=''
        gmt_end=int(time.time())
        gmt_begin=gmt_end-(3600*24*7)
        if pricetype:
            if pricetype['list']:
                if pricetype['list'][0].has_key('pricecategory'):
                    pricetypename=pricetype['list'][0]['pricecategory']
                if maintype=='1000':
                    maintypename='废金属'
                    typecode=100810021000
                    areacode=100810021001
                elif maintype=='1001':
                    maintypename='废塑料'
                    typecode=100810021002
                    areacode=100810021003
                else:
                    maintypename='综合废料'
                    typecode=100810031004
                    areacode=100810031005
                typecodelist=zzcomp.gettypecodelist(typecode)
                areacodelist=zzcomp.gettypecodelist(areacode)
                newslist=zznews.getnewslist(SPHINXCONFIG,keywords=keywords,frompageCount=0,limitNum=9,typeid="",typeid2="",allnum=9,arg='',flag='p',MATCH=1)['list']
                bbslist=zzcomp.getbbslist(keywords,14,gmt_begin,gmt_end,1)
                indexofferlist=zzcomp.getindexofferlist_pic(SPHINXCONFIG,kname=keywords,limitcount=5,membertype=1)
        if not newslist:
            compricelist1=zzcomp.getpricelist_company(kname=keywords,frompageCount=0,limitNum=1,maxcount=1)['list']
            if compricelist1:
                compricecategory=compricelist1[0]['pricecategory']
                categorycode=compricelist1[0]['categorycode']
                maincategorycode=categorycode[:4]
                if maincategorycode=='1000':
                    maintypename='废金属'
                    typecode=100810021000
                    areacode=100810021001
                elif maincategorycode=='1001':
                    maintypename='废塑料'
                    typecode=100810021002
                    areacode=100810021003
                else:
                    maintypename='综合废料'
                    typecode=100810031004
                    areacode=100810031005
                typecodelist=zzcomp.gettypecodelist(typecode)
                areacodelist=zzcomp.gettypecodelist(areacode)
#                return HttpResponse(compricecategory)
                newslist=zznews.getnewslist(SPHINXCONFIG,keywords=compricecategory,frompageCount=0,limitNum=9,typeid="",typeid2="",allnum=9,arg='',flag='',MATCH=1)['list']
                bbslist=zzcomp.getbbslist(compricecategory,14,gmt_begin,gmt_end,1)
                
        if not page:
            page=1
        funpage=zz91page()
        limitNum=funpage.limitNum(10)
        nowpage=funpage.nowpage(int(page))
        frompageCount=funpage.frompageCount()
        after_range_num = funpage.after_range_num(3)
        before_range_num = funpage.before_range_num(4)
        if type=='1':
            pcompany=1
            seotitle=keywords+"供应商报价_"+keywords+"厂家报价"
            pricelist=zzcomp.getpricelist_company(keywords,frompageCount,limitNum,maxcount=100000)
        else:
            type='0'
            seotitle=keywords+"市场行情"
            pricelist=zzcomp.getpricelist(frompageCount,limitNum,kname=keywords,maxcount=100000)
        listcount=0
        if (pricelist):
            listall=pricelist['list']
            listcount=pricelist['count']
            if (int(listcount)>1000000):
                listcount=1000000-1
        if listcount==0:
            listall=None
        listcount = funpage.listcount(listcount)
        if type=='0':
            if (listcount==0):
                return HttpResponseRedirect("/s/"+keywords_hex+"-1/")
        if not listall:
            seotitle='暂无'
            keywords='暂无'
        page_listcount=funpage.page_listcount()
        firstpage = funpage.firstpage()
        lastpage = funpage.lastpage()
        page_range  = funpage.page_range()
        if len(page_range)>5:
            page_range=page_range[:5]
        nextpage = funpage.nextpage()
        prvpage = funpage.prvpage()
    return render_to_response('price_search.html',locals())

def pricechart(request,id='',page=''):
    area=request.GET.get('area')
    gmt_begin=request.GET.get('gmt_begin')
    gmt_end=request.GET.get('gmt_end')
    sql2='select priceid,label,label1,area,type_id,assist_type_id,spec from price_list where id=%s'
    result2=zzcomp.dbc.fetchonedb(sql2,[id])
    categoryname=""
    if result2:
        priceid=result2[0]
        label=str(result2[1])
        label1=result2[2]
        if not label:
            label=label1
        if not area:
            area=result2[3]
        type_id=result2[4]
        assist_type_id=result2[5]
        spec=result2[6]
        if label=="" or str(label).upper()=="NONE" or label==None:
            label=spec

        hexlabel=getjiami(label)
        cplist=zzcomp.getcplist(SPHINXCONFIG,label,20)
      
        if type_id:
            #categoryid=pricelist2[0]['categoryid']
            categoryid=type_id
            categoryname=zzcomp.getpricecategory(categoryid)
            assistid=assist_type_id
            assistname=zzcomp.getpricecategory(assistid)
            #assistid=pricelist2[0]['assist_type_id']
            
            maindetail=zzcomp.getmaindetail(categoryid)
            maintypename=maindetail['maintypename']
            maincategory=maindetail['maincategory']
            if '金属' in maincategory:
                arealist=zzcomp.getpricearealist(categoryid,1)
            else:
                arealist=zzcomp.getpricearealist(assistid,1)
            aboucomplist=zzcomp.getpricelist_company(label,0,9,9)['list']
            if not aboucomplist:
                aboucomplist=zzcomp.getpricelist_company(maintypename,0,9,9)['list']
            hangqinglist=zzcomp.getprlist(0,6,6,label)['list']
            if not hangqinglist:
                hangqinglist=zzcomp.getprlist(0,6,6,maintypename)['list']
                

        listname=[]
        listfield=[]
        
        pricelista=zzcomp.getprice_list(keywords=label,frompageCount=0,limitNum=1,area=area,categoryid=type_id,maxcount=1)
        if pricelista:
            pricelist1=pricelista['list']
        if pricelist1:
            priceid=pricelist1[0]['priceid']
            #pricefield=zzcomp.getpricefield(priceid)
            pricefield=zzcomp.getpricefield2(categoryid=type_id,assist_type_id=assist_type_id,priceid=priceid)
            listname=pricefield['listname']
            listfield=pricefield['listfield']

        if not page:
            page=1
        funpage=zz91page()
        limitNum=funpage.limitNum(15)
        nowpage=funpage.nowpage(int(page))
        frompageCount=funpage.frompageCount()
        after_range_num = funpage.after_range_num(3)
        before_range_num = funpage.before_range_num(6)
        
        pricelist=zzcomp.getprice_list(group="priceid",keywords=label,frompageCount=frompageCount,limitNum=limitNum,area=area,listfiled=listfield,categoryid=type_id)
        listcount=0
        if pricelist:
            plist=pricelist['list']
            listcount=pricelist['count']
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
            
            chartarg=str(id)
            if area:
                hexarea=getjiami(area)
                chartarg+=','+hexarea
            if gmt_begin:
                chartarg+=','+gmt_begin
            if gmt_end:
                chartarg+=','+gmt_end
            if not area:
                area=""
            if not label:
                label=""
            if maintypename=='废塑料':
                suliao_hqzs=zzcomp.getprlist(0,10,10,'',[217])['list']
                suliao_zaowan=zzcomp.getprlist(0,10,10,'行情早参|行情晚报',[217])['list']
                suliao_pinglun=zzcomp.getprlist(0,7,7,'',[34])['list']
                label=label.upper()
                title=area+label+'价格走势_'+label+'价格走势图_行情报价中心-zz91再生网'
                keywords=area+label+'价格走势，'+label+'价格走势图'
                description='zz91再生网'+area+label+'行情报价中心，为您提供及时的'+area+label+'价格走势，让您能够快速知悉'+label+'及时市场动态，了解'+area+label+'及时价格走势就上zz91再生网。'
            elif maintypename=='废金属':
                parenttype=categoryname.replace('废','')
                parenttype=parenttype.replace('沪','')
                
                title=area+label+'价格走势图_'+parenttype+'价走势图_今日'+parenttype+'价走势图_行情报价中心-zz91再生网'
                keywords=area+label+'价格走势图，'+parenttype+'价走势图，今日'+parenttype+'价走势图'
                description='zz91再生网价格走势图频道，为您精心整理'+area+label+'价格走势图，更多今日'+parenttype+'价走势图，都在zz91再生网，专业的数据，助您快速知悉市场动态。'
            else:
                parenttype=categoryname.replace('废','')
                title=area+label+'价格走势图_'+parenttype+'价走势图_今日'+parenttype+'价走势图_行情报价中心-zz91再生网'
                keywords=area+label+'价格走势图，'+parenttype+'价走势图，今日'+parenttype+'价走势图'
                description='zz91再生网价格走势图频道，为您精心整理'+area+label+'价格走势图，更多今日'+parenttype+'价走势图，都在zz91再生网，专业的数据，助您快速知悉市场动态。'
    marketlist=zzcomp.getmarketlist(categoryname)
    return render_to_response('main/pricechart.html',locals())
#新版获得报价趋势图数据
def pricechartdata(request):
    id=request.GET.get('id')
    gmt_begin=request.GET.get('gmt_begin')
    gmt_end=request.GET.get('gmt_end')
    
    if not gmt_end:
        gmt_end=""
    else:
        gmt_end=str_to_int(gmt_end)
    if not gmt_begin:
        gmt_begin=""
    else:
        gmt_begin=str_to_int(gmt_begin)
    
    
    
    sql2='select priceid,label,label1,area,type_id,spec from price_list where id=%s'
    result2=zzcomp.dbc.fetchonedb(sql2,[id])
    if result2:
        priceid=result2[0]
        label=result2[1]
        label1=result2[2]
        area=result2[3]
        if not label:
            label=label1
        if not area:
            area=result2[3]
        spec=result2[5]
        if not label:
            label=spec
        if not label:
            label=""
        type_id=result2[4]
        
    chartpricelist=zzcomp.getchartpricelist(keywords=label,frompageCount=0,gmt_begin=gmt_begin,gmt_end=gmt_end,area=area,group='postdate',categoryid=type_id)
    if not chartpricelist:
        chartpricelist=zzcomp.getchartpricelist(keywords=label,frompageCount=0,gmt_begin=gmt_begin,gmt_end=gmt_end,area=area,group='postdate')
    if chartpricelist:
        chartpricelist=chartpricelist[::-1]
    return HttpResponse(simplejson.dumps(chartpricelist, ensure_ascii=False))
    '''
        chushiprice1=chartpricelist[0]['aveprice']
        if chushiprice1:
            chushiprice=chushiprice1-3000
    '''
    #return render_to_response('main/pricecharturl.html',locals())
def pricecharturl(request):
    chartarg=request.GET.get('chartarg')
    area=''
    gmt_begin=''
    gmt_end=''
    if ',' in chartarg:
        chartlist=chartarg.split(',')
        lenchart=len(chartlist)
        id=chartlist[0]
        if lenchart>1:
            area=chartlist[1]
            area=getjiemi(area)
        if lenchart>2:
            gmt_begin=str_to_int(chartlist[2])
        if lenchart>3:
            gmt_end=str_to_int(chartlist[3])
    else:
        id=chartarg
    
    sql2='select priceid,label,label1,area,type_id,spec from price_list where id=%s'
    result2=zzcomp.dbc.fetchonedb(sql2,[id])
    if result2:
        priceid=result2[0]
        label=result2[1]
        label1=result2[2]
        if not label:
            label=label1
        if not area:
            area=result2[3]
        spec=result2[5]
        if label=="" or str(label).upper()=="NONE" or label==None:
            label=spec
        type_id=result2[4]
    chartpricelist=zzcomp.getchartpricelist(keywords=label,frompageCount=0,limitNum=30,maxcount=30,gmt_begin=gmt_begin,gmt_end=gmt_end,area=area,group='postdate',categoryid=type_id)
    if not chartpricelist:
        chartpricelist=zzcomp.getchartpricelist(keywords=label,frompageCount=0,limitNum=30,maxcount=30,gmt_begin=gmt_begin,gmt_end=gmt_end,area=area,group='postdate')
    if chartpricelist:
        chartpricelist=chartpricelist[::-1]
    '''
        chushiprice1=chartpricelist[0]['aveprice']
        if chushiprice1:
            chushiprice=chushiprice1-3000
    '''
    return render_to_response('main/pricecharturl.html',locals())

def gethexkwd(request):
    keywords=request.GET.get('keywords')
    hexkwd=getjiami(keywords)
    return HttpResponse(hexkwd)

def getcitylist(request):
    provincecode=request.GET.get('provincecode')
    listall=zzcomp.getclist(provincecode)
    return HttpResponse(listall)
#----企业报价列表页
def compricelist(request,code='',searcharg='',page=''):
#    return HttpResponse('1')
#    keywords=request.GET.get('keywords')
    
    price1=''
    gmt_begin=''
    gmt_end=''
    daytxt=''
    hexkwd=''
    keyword=''
    citycode=''
    postInDays=''
    provincecode=''
    city=''
    province=''
    if searcharg:
#        codelist=re.findall('[\d]+',area)
        if '_k' in searcharg:
            hexkwd=re.findall('_k(.*?)_',searcharg)[0]
        if '_c' in searcharg:
            provincecode=re.findall('_c(.*?)_',searcharg)[0]
        if '_t' in searcharg:
            citycode=re.findall('_t(.*?)_',searcharg)[0]
        if '_d' in searcharg:
            postInDays=re.findall('_d(.*?)_',searcharg)[0]
        if '_q' in searcharg:
            price1=re.findall('_q(.*?)_',searcharg)[0]
    if hexkwd:
        keyword=getjiemi(hexkwd)
    label=''
    if code:
        label=zzcomp.getcompany_price_label(code)
        nextlabelist=zzcomp.getnext_category_comprice(code)
        maincode=code[:4]
    if keyword:
        skwd=keyword
    else:
        skwd=label
#    provincecode=request.GET.get('province')
#    citycode=request.GET.get('city')
    if provincecode:
        province=zzcomp.getclabel(provincecode)
        skwd+=' '+province
        ctlist=zzcomp.getclist(provincecode)
    if citycode:
        city=zzcomp.getclabel(citycode)
        skwd+=' '+city
    mobileflag=request.GET.get("mobileflag")
    if mobileflag:
        return HttpResponsePermanentRedirect('http://m.zz91.com/trade/pricelist.html?keywords='+skwd)
#    postInDays=request.GET.get('postInDays')
    if postInDays:
        if postInDays=='1':
            daytxt='最近一天'
        elif postInDays=='7':
            daytxt='最近一周'
        elif postInDays=='20':
            daytxt='最近20天'
        elif postInDays=='30':
            daytxt='最近一月'
        gmt_end=int(time.time())
        gmt_begin=gmt_end-(int(postInDays)*3600*24)
#    price1=request.GET.get('price1')
    min_price=''
    max_price=''
    if price1:
        if price1=='1a1000':
            pricetxt='1000以下'
        if price1=='1000a3000':
            pricetxt='1000到3000'
        if price1=='3000a5000':
            pricetxt='3000到5000'
        if price1=='5000a10000':
            pricetxt='5000到10000'
        if price1=='10000a1000000':
            pricetxt='10000以上'
        if price1=='0':
            pricetxt='其他价格'
        pricelist=price1.split('a')
        min_price=int(pricelist[0])
        max_price=int(pricelist[0])
        
    provincelist=zzcomp.getparentcategorylist()
    if not page:
        page=1
    funpage=zz91page()
    limitNum=funpage.limitNum(20)
    nowpage=funpage.nowpage(int(page))
    frompageCount=funpage.frompageCount()
    after_range_num = funpage.after_range_num(3)
    before_range_num = funpage.before_range_num(6)
    pricelist_company=zzcomp.getpricelist_company(kname=skwd,frompageCount=frompageCount,limitNum=limitNum,gmt_begin=gmt_begin,gmt_end=gmt_end,min_price=min_price,max_price=max_price)
    listcount=0
    complist=pricelist_company['list']
    listcount=pricelist_company['count']
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
    if label=='综合废料':
        hangqinglist=zzcomp.getprlist(0,6,6,'',[219,220])['list']
    else:
        hangqinglist=zzcomp.getprlist(0,6,6,label)['list']
    if keyword:
        sslabel=province+city+keyword
    else:
        sslabel=province+city+label
    if code=='10001000':
        title=province+city+'废塑料出厂价_行情报价中心_第'+str(page)+'页-zz91再生网'
        keywords=province+city+'废塑料出厂价'
        description='zz91再生网'+province+city+'废塑料企业报价频道，每天准时为您精选各地厂家提供的关于各种'+province+city+'废塑料的价格，了解及时'+province+city+'废塑料出厂价，就上zz91再生网。'
    elif code[:8]=='10001000':
        title=sslabel+' 废塑料企业报价_'+sslabel+'再生颗粒价格_行情报价中心_第'+str(page)+'页-zz91再生网'
        keywords=sslabel+' 废塑料企业报价，'+sslabel+'再生颗粒价格'
        description='zz91再生网'+sslabel+' 废塑料企业报价频道，每天准时为您精选各地厂家提供的关于各种'+sslabel+'废塑料的价格，了解及时'+sslabel+'再生颗粒价格，就上zz91再生网。'
    elif code=='10001001':
        title=province+city+'塑料颗粒企业报价_'+province+city+'塑料颗粒价格行情_行情报价中心_第'+str(page)+'页-zz91再生网'
        keywords=province+city+'塑料颗粒企业报价，塑料颗粒价格'
        description='zz91再生网'+province+city+'废塑料企业报价频道，每天准时为您精选各地厂家提供的关于各种'+province+city+'塑料颗粒的价格，了解及时'+province+city+'塑料颗粒企业报价，就上zz91再生网。'
    elif code[:8]=='10001001':
        title=sslabel+'企业报价_'+sslabel+'价格行情_行情报价中心_第'+str(page)+'页-zz91再生网'
        keywords=sslabel+'企业报价，'+sslabel+'价格'
        description='zz91再生网'+sslabel+'企业报价频道，每天准时为您精选各地厂家提供的关于各种'+sslabel+'的价格，了解及时'+sslabel+'企业报价，就上zz91再生网。'
    elif len(code)==8 and code[:4]=='1001':
        if code=='10011008':
            sslabel=province+city+'其他废金属'
        else:
            sslabel=province+city+'废'+label
        title=sslabel+'企业报价_今日'+sslabel+'报价_行情报价中心_第'+str(page)+'页-zz91再生网'
        keywords=sslabel+'企业报价，今日废铁报价'
        description='zz91再生网'+sslabel+'企业报价频道，每天准时为您精选各地厂家提供的关于各种'+sslabel+'产品的价格，了解今日'+sslabel+'报价，就上zz91再生网。'
    elif len(code)==8 and code[:4] in ['1002','1003']:
        title=sslabel+'企业报价_'+sslabel+'价格_'+sslabel+'厂家_行情报价中心_第'+str(page)+'页-zz91再生网'
        keywords=''+sslabel+'企业报价，'+sslabel+'价格，'+sslabel+'厂家'
        description='zz91再生网'+sslabel+'企业报价频道，每天准时为您精选各地厂家提供的关于各种'+sslabel+'价格，了解更多'+sslabel+'厂家，就上zz91再生网。'
    else:
        title=sslabel+'企业报价_'+sslabel+'出厂价_行情报价中心_第'+str(page)+'页-zz91再生网'
        keywords=sslabel+'企业报价,'+sslabel+'出厂价'
        description='zz91再生网'+sslabel+'企业报价频道，每天准时为您精选各地厂家提供的关于各种'+sslabel+'的价格，了解及时'+sslabel+'工厂价格，就上zz91再生网。'
    return render_to_response('main/compricelist.html',locals())

def cpriceindex(request):
    mobileflag=request.GET.get("mobileflag")
    if mobileflag and cid:
        return HttpResponsePermanentRedirect('http://m.zz91.com/jiage/')
    provincelist=zzcomp.getparentcategorylist()
    compricelist=zzcomp.getpricelist_company(frompageCount=0,limitNum=20,maxcount=20)['list']
    suliaocpricelist=zzcomp.getpricelist_company(kname='废塑料',frompageCount=0,limitNum=7,maxcount=7)['list']
    jinshucpricelist=zzcomp.getpricelist_company(kname='废金属',frompageCount=0,limitNum=7,maxcount=7)['list']
    zonghecpricelist=zzcomp.getpricelist_company(kname='综合废料',frompageCount=0,limitNum=7,maxcount=7)['list']
    feizhicpricelist=zzcomp.getpricelist_company(kname='废纸',frompageCount=0,limitNum=7,maxcount=7)['list']
    pricelist=zzcomp.getprlist(0,8,8)['list']
    qihuoprlist=zzcomp.getprlist(0,8,8,'',[64])['list']
    chartdatalist=zzcomp.getchartdatalistall(frompageCount=0,limitNum=7,zhangdie=1)['list']
    offerlist=zzcomp.getofferlist(pdt_type='0',limitcount=8)
    offbuylist=zzcomp.getofferlist(pdt_type='1',limitcount=8)
    return render_to_response('main/cpriceindex.html',locals())

#----企业报价最终页
def compricedetail(request,cid=''):
    mobileflag=request.GET.get("mobileflag")
    if mobileflag and cid:
        return HttpResponsePermanentRedirect('http://m.zz91.com/jiage/cdetail'+str(cid)+'.html')
    if not cid:
        return HttpResponse("404")
    sql='select company_id,account,product_id,title,category_company_price_code,price,price_unit,min_price,max_price,area_code,details,refresh_time from company_price where id=%s and is_checked=1'
    result=dbc.fetchonedb(sql,cid)
    if result:
        company_id=result[0]
        company_url=zzcomp.getcompany_url(company_id)
        compd=zzcomp.getcompaccountdetail(company_id)
        
        compricelist=zzcomp.getpricelist_company(frompageCount=0,limitNum=10,maxcount=10,company_id=company_id)['list']
        
        account=result[1]
        product_id=result[2]
        tagslist=zzcomp.getproductstags(product_id)
        keywords=""
        if tagslist:
            for l in tagslist:
                keywords+="|"+l['label']
        cplist=zzcomp.getcplist(SPHINXCONFIG,keywords,20)
        
        title=result[3]
        ctitle=title
        code=result[4]
        maincode=code[:4]
        mainlabel=zzcomp.getcompany_price_label(maincode)
        if mainlabel=='废金属':
            wsbjtxt='废金属'
            wsbjlist=zzcomp.getprlist(0,7,7,'',[51])['list']
        elif mainlabel=='废塑料':
            wsbjtxt='废塑料'
            wsbjlist=zzcomp.getprlist(0,7,7,'',[137])['list']
        else:
            wsbjtxt='废纸'
            wsbjlist=zzcomp.getprlist(0,7,7,'',[25])['list']
            iszonghe=1
        label=zzcomp.getcompany_price_label(code)
        price=result[5]
        price_unit=result[6]
        min_price=result[7]
        max_price=result[8]
        if price:
            price2=price
        else:
            if max_price !=None and max_price!='' and max_price !='0.0' :
                price2=min_price+'-'+max_price+price_unit
            else :
                price2=min_price+price_unit
        area_code=result[9]
        pprovince=''
        pcity=''
        if area_code:
            provincecode=area_code[:12]
            pprovince=zzcomp.getclabel(provincecode)
            citycode=area_code[:16]
            pcity=zzcomp.getclabel(citycode)
        details=result[10]
        refresh_time=formattime(result[11])
        provincelist=zzcomp.getparentcategorylist()
        offerlist=zzcomp.getofferlist(kname=mainlabel,pdt_type='0',limitcount=6)
        buylist=zzcomp.getofferlist(kname=mainlabel,pdt_type='1',limitcount=6)
        timenow=int(time.time()*1000)
        title=title+" 报价-企业报价"
    return render_to_response('main/compricedetail.html',locals())

#----走势图(没使用)
def chartlist(request,page=''):
    datebegin=request.GET.get('datebegin')
    dateend=request.GET.get('dateend')
    area_list=request.GET.getlist('arealist')
    if area_list:
        area_list=','.join(area_list)+datebegin+dateend
    arealist=zzcomp.getarealist(0,20,maxcount=20)
    keywords=request.GET.get('keywords')
    page_listcount=request.GET.get('page_listcount')
    if (page==None or page=='' or page=='0'):
        page=1
    elif page.isdigit()==False:
        page=1
    if page_listcount and int(page)>int(page_listcount):
        page=page_listcount
    funpage=zz91page()
    limitNum=funpage.limitNum(10)
    nowpage=funpage.nowpage(int(page))
    frompageCount=funpage.frompageCount()
    after_range_num = funpage.after_range_num(2)
    before_range_num = funpage.before_range_num(3)
    pricelist=zzcomp.getprice_list(keywords=keywords,frompageCount=frompageCount,limitNum=limitNum)
    listcount=0
    if (pricelist):
        listall=pricelist['list']
        listcount=pricelist['count']
        if (int(listcount)>1000000):
            listcount=1000000-1
    listcount = funpage.listcount(listcount)
    page_listcount=funpage.page_listcount()
    firstpage = funpage.firstpage()
    lastpage = funpage.lastpage()
    page_range  = funpage.page_range()
    if len(page_range)>5:
        page_range=page_range[:5]
    nextpage = funpage.nextpage()
    prvpage = funpage.prvpage()
    return render_to_response('chartlist.html',locals())
#没使用
def tongji_chart(request):
#    datebegin=request.GET.get('datebegin')
#    if datebegin:
#        datebegin=str_to_int(datebegin)
#    dateend=request.GET.get('dateend')
#    if dateend:
#        dateend=str_to_int(dateend)
    dateend=int(time.time())
    datebegin=dateend-3600*24*15
#    timelist2=gettimedifference(datebegin,dateend)
#    if datebegin and dateend:
        #----获得两段时间差的%Y-%m-%d时间格式列表
    arealist=[]
    area_list=request.GET.get('area_list')
    if area_list:
        arealist1=zzcomp.getarealist(SPHINXCONFIG,0,20,maxcount=20)
        numblist=area_list.split(',')
        if '-' in numblist[0]:
            datebegin=str_to_int(numblist[0])
            dateend=str_to_int(numblist[1])
            numblist=numblist[2:]
#        return HttpResponse(timelist2)
        for numb in numblist:
            for alt in arealist1:
                if int(numb)==alt['numb']:
                    arealist.append(alt['area'])
    timelist2=gettimedifference(datebegin,dateend)
    if not arealist:
        arealist=['东莞','浙江','山东']
    pricelist=zzcomp.getareapricelist('',0,12,arealist,datebegin,dateend)
    return render_to_response('tongji_chart.html',locals())
def sitemap(request):
    parent_id=17
    sx=1
    listall=[]
    navlist1=zzcomp.getcategoryxml(17,1)
    listall.append(navlist1)
    navlist1=zzcomp.getcategoryxml(64,1)
    listall.append(navlist1)
    navlist1=zzcomp.getcategoryxml(67,1)
    listall.append(navlist1)
    navlist1=zzcomp.getcategoryxml(68,1)
    listall.append(navlist1)
    navlist1=zzcomp.getcategoryxml("66",1,p=1)
    listall.append(navlist1)
    navlist1=zzcomp.getcategoryxml("32,33,216",1,p=1)
    listall.append(navlist1)
    navlist1=zzcomp.getcategoryxml("20",1,p=1)
    navlist1=zzcomp.getcategoryxml(60,1)
    listall.append(navlist1)
    navlist1=zzcomp.getcategoryxml("61",1,p=1)
    listall.append(navlist1)
    navlist1=zzcomp.getcategoryxml("127,138,137,132,130,128,62,63,98,233,34,35,217,231,23,25,26,27,28,29,218,30,219,190,220",1,p=1)
    listall.append(navlist1)
    navlist1=zzcomp.getcategoryxml("300,304,309,313,299,298,297,290,291,292,293,294,295,296",1,p=1,a=1)
    listall.append(navlist1)
    
    return render_to_response('sitemap.html',locals(),mimetype="application/xml")

#自主报价列表 
def selfpricelist(request,page='',searchKey='',category=''):
    if not page:
        page=1
    funpage=zz91page()
    limitNum=funpage.limitNum(15)
    owpage=funpage.nowpage(int(page))
    frompageCount=funpage.frompageCount()
    after_range_num = funpage.after_range_num(3)
    before_range_num = funpage.before_range_num(3)
    if searchKey == '' and category == '':
        sql = 'select id,title,category,company_id,instruction,download_num,gmt_created from price_offer where is_del=0 order by id desc ' + 'limit '+ str(frompageCount) + ',' + str(limitNum)
        names = dbc.fetchalldb(sql)
    elif category and searchKey == '':
        sql = "select id,title,category,company_id,instruction,download_num,gmt_created from price_offer where is_del=0 and category=%s order by id desc " + 'limit '+ str(frompageCount) + ',' + str(limitNum)
        names = dbc.fetchalldb(sql,[category])
    elif searchKey and category == '' :
        sql = "select id,title,category,company_id,instruction,download_num,gmt_created from price_offer where is_del=0 and title like concat('%%',%s,'%%') order by id desc " + 'limit '+ str(frompageCount) + ',' + str(limitNum)
        names = dbc.fetchalldb(sql,[searchKey])
    else :
        sql = "select id,title,category,company_id,instruction,download_num,gmt_created from price_offer where is_del=0 and title like concat('%%',%s,'%%') and category=%s order by id desc " + 'limit '+ str(frompageCount) + ',' + str(limitNum)
        names = dbc.fetchalldb(sql,[searchKey,category])
    clist = []
    for obj in names :
        c = PriceOffer.PriceOffer(obj[0],obj[1],categoryName(obj[2]),companyname(str(obj[3])),obj[4],obj[5],changedate(obj[6]))
        clist.append(c)
    if searchKey == '' and category == '':
        sql = 'select count(0) from price_offer where is_del=0'
        listcount = dbc.fetchnumberdb(sql)
    elif category and searchKey == '' :
        sql = "select count(0) from price_offer where is_del=0 and category=%s"
        listcount = dbc.fetchnumberdb(sql,[category])
    elif searchKey and category == '' :
        sql = "select count(0) from price_offer where is_del=0 and title like concat('%%',%s,'%%')"
        listcount = dbc.fetchnumberdb(sql,[searchKey])
    else :
        sql = "select count(0) from price_offer where is_del=0 and title like concat('%%',%s,'%%') and category=%s"
        listcount = dbc.fetchnumberdb(sql,[searchKey,category])
    listcount = funpage.listcount(listcount)
    page_listcount=funpage.page_listcount()
    firstpage = funpage.firstpage()
    lastpage = funpage.lastpage()
    nextpage = funpage.nextpage()
    prvpage = funpage.prvpage()
    page_range = funpage.page_range()
    if owpage == page_listcount :
        nextpage = owpage
    if owpage == 1:
        prvpage = 1
    return render_to_response('selfprice/list.html',locals())

#时间格式化
def changedate(datestring):
    if (datestring=="" or datestring==None):
        return ""
    else:
        nowsdatestr=datestring.strftime( '%Y-%m-%d %X')
        if (nowsdatestr=='1900-01-01 00:00:00'):
            nowsdatestr=""
        return nowsdatestr
    
#获取公司名称
def companyname(companyId):
    sql = 'select name from company where id=%s'
    result = dbc.fetchonedb(sql,[companyId])
    if result:
        content = result[0]
    else :
        content = ''
    return   content

#企业自主报价类别
def categoryName(category):
    sql = 'select label from category where code=%s'
    result = dbc.fetchonedb(sql,[category])
    if result :
        content = result[0]
    else :
        content = ''
    return content

#标注关注的状态（取消关注/关注）
def notice(request):
    company_id=request.GET.get('company_id')
    content_id=request.GET.get('id')
    sql = 'select count(0) from myfavorite where favorite_type_code=%s and content_id=%s and company_id=%s'
    result = dbc.fetchonedb(sql,['10091013',content_id,company_id])
    if result:
        content = result[0]
    sql1 = 'select download_num from price_offer where id=%s'
    result1 = dbc.fetchonedb(sql1,[content_id])
    if result1:
        content1 = result1[0]
    html="var content="+str(content)+";var xid="+str(content_id)+";var downnum=" + str(content1)
    return HttpResponse(html)

#自主报价预览 
def preview(request,id=''):
     sql = 'select company_id,excel_content from price_offer where id=%s '
     result = dbc.fetchonedb(sql,[id])
     if result:
         content = result[1]
         cname = companyname(result[0])
     return render_to_response('selfprice/preview.html',locals())

#下载文档
def download(request,id=''):
    sql = 'select excel_address,excel_name,download_num from price_offer where id=%s'
    result = dbc.fetchonedb(sql,[id])
    if result :
        address = result[0]
        name = result[1]
        num = result[2]+1
    url="http://img1.zz91.com"+address
    try:
        file = urllib.urlopen(url)
        data = StringIO.StringIO(file.read())
        #req = urllib2.Request(url)
        #data=urllib2.urlopen(req).read()
    except:
        data=None
    #f = open('/usr/data/resources'+address)
    #data = f.read()
    #f.close()
    #if mstream:
    response = HttpResponse(data,mimetype='application/octet-stream') 
    response['Content-Disposition'] = 'attachment; filename='+str(name)
    sql1 = 'update price_offer set download_num=%s,gmt_modified=now() where id=%s'
    dbc.updatetodb(sql1,[num,id])
    data.closed
    return response
    #else:
        #return HttpResponse(url)

#关注的具体动作及相应的弹框
def follow(request):
    companyId = request.GET.get('companyId')
    id = request.GET.get('id')
    mark = request.GET.get('mark')
    sql = 'select id from myfavorite where favorite_type_code=%s and content_id=%s and company_id=%s'
    i = dbc.fetchnumberdb(sql,['10091013',id,companyId])
    if i == 0:
        sql1 = 'select title from price_offer where id='+id
        result = dbc.fetchonedb(sql1)
        if result:
            title = result[0]
        sql2 = 'insert myfavorite(favorite_type_code,content_id,content_title,company_id,gmt_created,gmt_modified) values(%s,%s,%s,%s,now(),now())'
        dbc.updatetodb(sql2,['10091013',id,title,companyId])
        return render_to_response('selfprice/follow_suc.html',locals())
    if mark :
        sql3 = 'delete from myfavorite where favorite_type_code=%s and content_id=%s and company_id=%s'
        dbc.updatetodb(sql3,['10091013',id,companyId])
    return render_to_response('selfprice/follow_cancel.html',locals()) 
#回调函数
def submitCallback(request):
    id = request.GET.get('id')
    return render_to_response('selfprice/submitCallback.html',locals())