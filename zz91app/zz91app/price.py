#-*- coding:utf-8 -*-
from django.shortcuts import render_to_response
from django.http import HttpResponse,HttpResponseRedirect,HttpResponsePermanentRedirect
import MySQLdb,sys,os,memcache,settings,urllib,re,time,datetime,simplejson
from datetime import timedelta,date
from django.core.cache import cache

from zz91tools import subString,filter_tags,formattime,int_to_str,str_to_int
from zz91page import *
from zz91db_ast import companydb
from sphinxapi import *
from settings import spconfig,appurl

spconfig=settings.SPHINXCONFIG
dbc=companydb()

reload(sys)
sys.setdefaultencoding('UTF-8')
nowpath=os.path.dirname(__file__)
execfile(nowpath+"/func/public_function.py")
execfile(nowpath+"/func/price_function.py")
execfile(nowpath+"/func/trade_function.py")
zzprice=zprice()
zzt=zztrade()

def index(request):
    host=getnowurl(request)
    webtitle="行情报价"
    nowlanmu="<a href='/priceindex/'>行情报价</a>"
    return render_to_response('price/index.html',locals())


#----报价列表
def pricelist(request,category_id='',assist_id=''):
    host=getnowurl(request)
    appsystem=request.GET.get("appsystem")
    company_id=request.GET.get('company_id')
    localhtmlflag=request.GET.get('localhtmlflag')
    orderflag=request.GET.get('orderflag')
    if '.html' in host:
        iscm=1
    alijsload="1"
    
    
    nowlanmu="<a href='/priceindex/'>行情报价</a>"
    if not category_id:
        category_id=request.GET.get("category_id")
#    searchlist={}
    webtitle="行情报价"
    assistvalue=None
    categoryvalue=None
    if category_id and category_id!="undefined":
        categoryvalue=[int(category_id)]
        categoryvalue=getallpricecategroy([int(category_id),99999])
        #return HttpResponse(str(categoryvalue))
        category_label=zzprice.getcategory_label(category_id)
        mulu1='> <a href="/priceindex/'+str(category_id)+'.html">'+category_label+'</a>'
        webtitle+=category_label
        #记录搜索记录
        clientid=request.GET.get("clientid")
        updatesearchKeywords(clientid,company_id,category_label,ktype="price")
    if assist_id=="":
        assist_id=request.GET.get("assist_id")
    if assist_id:
        assist_label=zzprice.getcategory_label(assist_id)
        mulu3='> <a href="?assist_id='+assist_id+'">'+assist_label+'</a>'
        assistvalue=[int(assist_id)]
        webtitle+="-"+assist_label
    username=request.session.get("username",None)
    keywords=request.GET.get("keywords")
    if (gethextype(keywords)==False):
        keywords_hex=getjiami(keywords)
    else:
        keywords=getjiemi(keywords)
        keywords_hex=getjiami(keywords)
    if (keywords!=None):
        mulu2='> <a href="?keywords='+keywords+'">'+keywords+'</a>'
        keywords=keywords.replace("报价","")
        keywords=keywords.replace("价格","")
        webtitle=keywords
        webtitle+="-"+keywords
    if (str(keywords)=='None'):    
        keywords=None
    if (str(category_id)=='None'):
        category_id=None
    if (category_id==None and keywords==None):
        categoryvalue=[]
    if (str(category_id)=='1'):
        labelstyle1="class=chk"
        labelstyle2=""
        labelstyle3=""
    if (str(category_id)=='2'):
        labelstyle1=""
        labelstyle2="class=chk"
        labelstyle3=""
    if (str(category_id)=='3'):
        labelstyle1=""
        labelstyle2=""
        labelstyle3="class=chk"
    arealist=[]
    if category_id in ["40","42","41","52","44","45","47","43"]:
        showarea=1
        if category_id=="40":
            arealist="江浙沪,广东,南海 ,临沂,汨罗,北京,长葛,清远,四川,天津,安徽,河北,成都,江西,山东,辽宁,贵州,重庆,台州,陕西,福建,云南"
        if category_id=="42":
            arealist="江浙沪,山东,河南,天津,四川,湖北,江西,山西,广东,福建"
        if category_id=="41":
            arealist="废铝,江浙沪,广东,南海,长葛,汨罗,临沂,天津,福建,四川,清远,宁波,河北,台州,山东,云南,重庆,陕西"
        if category_id=="52":
            arealist="全国,山东,陕西,长葛,江浙沪,广东,四川,重庆"
        if category_id=="44":
            arealist="江浙沪,广东,南海,临沂,台州,宁波,天津,清远"
        if category_id=="45":
            arealist="江浙沪,南海,临沂,天津,广东 "
        if category_id=="47":
            arealist="江浙沪,临沂,南海"
        if category_id=="43":
            arealist="江浙沪,南海,广东,天津,河北,临沂"
        arealist=arealist.split(",")
    if str(category_id)=="110":
        categoryvalue=[110,324]
    if str(category_id)=="42":
        categoryvalue=[42,328]
    #定制商机
    if orderflag:
        orderlist=zzprice.getmyorderprice(company_id)
        categoryvalue=[]
        assistvalue=[]
        keywordslist=""
        if not orderlist or not company_id:
            resultlist={"error_code":1,"reason":"您定制的内容暂无信息","result":''}
            response = HttpResponse(simplejson.dumps(resultlist, ensure_ascii=False))
            return response
        if orderlist:
            for list in orderlist:
                category_id=list['category_id']
                if category_id:
                    categoryvalue.append(category_id)
                assist_id=list['assist_id']
                if assist_id:
                    assistvalue.append(assist_id)
                keywords=list['keywords']
                if keywords:
                    if (gethextype(keywords)==False):
                        keywords=keywords
                    else:
                        keywords=getjiemi(keywords)
                    keywordslist+=str(keywords)+"|"
                
            if keywordslist:
                keywordslist=keywordslist[0:len(keywordslist)-1]
            keywords=keywordslist
        
    #return HttpResponse(str(categoryvalue))
    pricelistall=zzprice.getpricelist(keywords=keywords,frompageCount=0,limitNum=20,category_id=categoryvalue,allnum=20,assist_type_id=assistvalue)
    pricelist=pricelistall['list']
    
    pricelistcount=pricelistall['count']
    if (pricelistcount==1):
        morebutton='style=display:none'
    else:
        morebutton=''
    datatype=request.GET.get("datatype")
    resultlist={"error_code":0,"reason":"","result":pricelist,"queryString":{"category_id":category_id,"keywords":keywords_hex},"lastpage":"",'listcount':pricelistcount,'arealist':arealist}
    response = HttpResponse(simplejson.dumps(resultlist, ensure_ascii=False))
    return response

    return render_to_response('price/list.html',locals())
#----报价列表 更多
def pricemore(request,category_id='',assist_id=''):
    nowlanmu="<a href='/priceindex/'>行情报价</a>"
    username=request.session.get("username",None)
    if not category_id:
        category_id=request.GET.get("category_id")
    keywords=request.GET.get("keywords")
    company_id=request.GET.get("company_id")
    orderflag=request.GET.get("orderflag")
    #定制商机
    if orderflag:
        orderlist=zzprice.getmyorderprice(company_id)
        categoryvalue=[]
        assistvalue=[]
        keywordslist=""
        if not orderlist:
            resultlist={"error_code":1,"reason":"您定制的内容暂无信息","result":''}
            response = HttpResponse(simplejson.dumps(resultlist, ensure_ascii=False))
            return response
        if orderlist:
            for list in orderlist:
                category_id=list['category_id']
                if category_id:
                    categoryvalue.append(category_id)
                assist_id=list['assist_id']
                if assist_id:
                    assistvalue.append(assist_id)
                keywords=list['keywords']
                if keywords:
                    if (gethextype(keywords)==False):
                        keywords=keywords
                    else:
                        keywords=getjiemi(keywords)
                    keywordslist+=str(keywords)+"|"
                
            if keywordslist:
                keywordslist=keywordslist[0:len(keywordslist)-1]
            keywords=keywordslist
    if (gethextype(keywords)==False):
        keywords_hex=getjiami(keywords)
    else:
        keywords=getjiemi(keywords)
        keywords_hex=getjiami(keywords)
    if not assist_id:
        assist_id=request.GET.get("assist_id")
    assistvalue=None
    if assist_id:
        assistvalue=[int(assist_id)]
    if (keywords!=None):
        webtitle=keywords+"报价列表"
    else:
        webtitle="报价列表"
    if (str(keywords)=='None'):
        keywords=None
    page=request.GET.get("page")
    if page==None:
        page=0
    if (str(category_id)=='None'):
        category_id=None
    if category_id and category_id!="undefined":
        category_id=int(category_id)
    categoryvalue=[category_id]
    if category_id=="undefined":
        categoryvalue=None
    if not category_id:
        categoryvalue=None
    if str(category_id)=="110":
        categoryvalue=[110,324]
    if str(category_id)=="42":
        categoryvalue=[42,328]
    pricelistall=zzprice.getpricelist(keywords=keywords,frompageCount=int(page)*20,limitNum=20,category_id=categoryvalue,allnum=1000,assist_type_id=assistvalue)
    pricelist=pricelistall['list']
    ##返回json数据
    datatype=request.GET.get("datatype")
    return HttpResponse(simplejson.dumps(pricelist, ensure_ascii=False))
    return render_to_response('price/listmore.html',locals())
#企业报价
def companypricelist(request):
    host=getnowurl(request)
    keywords=request.GET.get("keywords")
    category_id=request.GET.get("category_id")
    company_id=request.GET.get("company_id")
    page=request.GET.get("page")
    if not page:
        page=1
    funpage=zz91page()
    limitNum=funpage.limitNum(20)
    nowpage=funpage.nowpage(int(page))
    frompageCount=funpage.frompageCount()
    after_range_num = funpage.after_range_num(8)
    before_range_num = funpage.before_range_num(9)
    pricelist=zzt.getpricelist_company(kname=keywords,frompageCount=frompageCount,limitNum=limitNum)
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
    #研究院 独家观点
    price_dj=zzprice.getpricedblist(frompageCount=0,limitNum=5,typeid='359,360')
    
    jsonlist={'list':listall,'pagecount':page_listcount,'price_dj':price_dj}
    return HttpResponse(simplejson.dumps(jsonlist, ensure_ascii=False))
#研究院列表
def studylist(request):
    host=getnowurl(request)
    typeid=request.GET.get("typeid")
    page=request.GET.get("page")
    if not page:
        page=1
    funpage=zz91page()
    limitNum=funpage.limitNum(10)
    nowpage=funpage.nowpage(int(page))
    frompageCount=funpage.frompageCount()
    after_range_num = funpage.after_range_num(8)
    before_range_num = funpage.before_range_num(9)
    pricelist=zzprice.getpricedblist(frompageCount=frompageCount,limitNum=limitNum,typeid=typeid)
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
    jsonlist={'list':listall,'pagecount':page_listcount}
    return HttpResponse(simplejson.dumps(jsonlist, ensure_ascii=False))
def study_detail(request):
    price_id=request.GET.get("price_id")
    detail='{}'
    if price_id:
        detail=zzprice.getpricedetail(price_id)
    return HttpResponse(simplejson.dumps(detail, ensure_ascii=False))
#----行情报价最终页
def details(request):
    host=getnowurl(request)
    alijsload="1"
    nowlanmu="<a href='/priceindex/'>行情报价</a>"
    id=request.GET.get("id")
    company_id=request.GET.get("company_id")
    category_id=request.GET.get("category_id")
    keywords=request.GET.get("keywords")
    if (gethextype(keywords)==False):
        keywords_hex=getjiami(keywords)
    else:
        keywords=getjiemi(keywords)
        keywords_hex=getjiami(keywords)
    assist_id=request.GET.get("assist_id")
    searchkeyword=''
    category_id2=[]
    assist_id2=[]
    priceabout=[]
    arg=''
    if category_id:
        category_label=zzprice.getcategory_label(category_id)
        parent_id=zzprice.parent_id(category_id)
        parent_id2=zzprice.parent_id(parent_id)
        parent_id3=zzprice.parent_id(parent_id2)
        category_id2=[int(category_id)]
        if parent_id==5 or parent_id2==5 or parent_id3==5:
            searchkeyword='废金属'
            arg=1
        elif parent_id==6 or parent_id2==6 or parent_id3==6:
            searchkeyword='废塑料'
            arg=2
        elif parent_id==7 or parent_id2==7 or parent_id3==7:
            searchkeyword='废纸'
        elif parent_id==8 or parent_id2==8 or parent_id3==8:
            searchkeyword='废橡胶'
        elif parent_id==213 or parent_id2==213 or parent_id3==213:
            searchkeyword='原油'
        mulu1='> <a href="/priceindex/'+str(category_id)+'.html">'+category_label+'</a>'
    if keywords:
        webtitle=keywords
#        if arg==1:
#            searchkeyword=keywords
        mulu2='> <a href="/price/?keywords='+keywords+'">'+keywords+'</a>'
    if assist_id:
        assist_id2=[int(assist_id)]
        assist_label=zzprice.getcategory_label(assist_id)
        if arg==1:
#            searchkeyword=assist_label
            priceabout=zzprice.getpricelist('',0,7,category_id2,7,assist_id2,1)['list']
            searchkeyword=category_label
        elif arg==2:
            searchkeyword=assist_label
            priceabout=zzprice.getpricelist('',0,7,category_id2,7,assist_id2,2)['list']
        if assist_id!=0 and assist_label:
            mulu3='> <a href="/price/?assist_id='+str(assist_id)+'">'+str(assist_label)+'</a>'
    username=request.session.get("username",None)
    type_id=''
    sql="select title,content,gmt_created,type_id,assist_type_id from price where id=%s and is_checked=1"
    alist = zzprice.dbc.fetchonedb(sql,[id])
    listall=[]
    if alist:
        title=alist[0]
        content=alist[1]
        type_id=alist[3]
        assist_type_id=alist[4]
        if not category_id:
            category_id=type_id
            category_label=zzprice.getcategory_label(category_id)
            assist_type_label=zzprice.getcategory_label(assist_type_id)
            searchkeyword=category_label
            parent_id=zzprice.parent_id(category_id)
            parent_id2=zzprice.parent_id(parent_id)
            parent_id3=zzprice.parent_id(parent_id2)
            category_id2=[int(category_id)]
            if parent_id==5 or parent_id2==5 or parent_id3==5:
#                searchkeyword='废金属'
                arg=1
            elif parent_id==6 or parent_id2==6 or parent_id3==6:
#                searchkeyword='废塑料'
                searchkeyword=assist_type_label
                arg=2
            elif parent_id==7 or parent_id2==7 or parent_id3==7:
                searchkeyword='废纸'
            elif parent_id==8 or parent_id2==8 or parent_id3==8:
                searchkeyword='废橡胶'
            elif parent_id==213 or parent_id2==213 or parent_id3==213:
                searchkeyword='原油'
        webtitle=title
        if category_id in [40,42,328,41,45,47,44,308,46,49]:
            #数据字段
            pricefield=zzprice.getpricefield2(categoryid=category_id,assist_type_id=assist_id,priceid=id)
            listname=pricefield['listname']
            listfield=pricefield['listfield']
            pricedetaillist=zzprice.getdetailpricelist(id,listfield)
            
            tabstr='<table cellpadding="0" cellspacing="0" class="infotable">'
            tabstr+='    <tr>'
            tabstr+='        <th nowrap>趋势图</th>'
            for pf in listname:
                tabstr+='    <th>'+str(pf)+'</th>'
            tabstr+='    </tr>'
            if pricedetaillist:
                for pl in pricedetaillist:
                    tabstr+='<tr pid='+str(pl['id'])+'>'
                    tabstr+='    <td class="qushi" nowrap pid='+str(pl['id'])+'><img src="http://img0.zz91.com/zz91/images/qushi.png" pid='+str(pl['id'])+' style="width:25px"/></td>'
                    for field in pl['listvalue']:
                        tabstr+='<td>'+str(field)+'</td>'
                    tabstr+='</tr>'
                tabstr+='</table>'
                pricedetaillist=tabstr
            else:
                pricedetaillist=None
        else:
            pricedetaillist=None
        gmt_created=alist[2].strftime( '%-Y-%-m-%-d %-H:%-M:%-S')
        if str(type_id) in ("25","51","137"):
            content=zzprice.getwebprice(id)
        content=replacepic(content)
        #content=content.replace("http://price.zz91.com/priceDetails_","http://app.zz91.com/priceviews/")
        content=content.replace("http://price.zz91.com/","http://app.zz91.com/")
        content=remove_script(content)
        content=remove_content_a(content)
        list={'title':title,'content':content,'gmt_created':gmt_created}
        favoriteflag=0
        if company_id:
            favoriteflag=isfavorite(id,'10091004',company_id)
        list['favoriteflag']=favoriteflag
        listall.append(list)
    feizhibbsd=zzprice.getbbslist(searchkeyword,10)
    feizhibbs=None
    if feizhibbsd:
        feizhibbs=feizhibbsd['list']
    zhibuy=None
    #zhibuy=zzprice.offerlist(searchkeyword,'1',5)
    #zhioffer=zzprice.offerlist(searchkeyword,'0',3)
    if searchkeyword==None:
        searchkeyword=""
    if not priceabout:
        if category_id:
            priceabout=zzprice.getpricelist(searchkeyword,0,7,[int(category_id)],7)['list']
    ##返回json数据
    datatype=request.GET.get("datatype")
    jsonlist={'listall':listall,'priceabout':priceabout,'feizhibbs':feizhibbs,'offerlist':zhibuy,'pricedetaillist':pricedetaillist}
    return HttpResponse(simplejson.dumps(jsonlist, ensure_ascii=False))
    return render_to_response('price/details.html',locals())
def pricechart(request):
    id=request.GET.get('id')
    sql="select label from price_list where id=%s"
    result=dbc.fetchonedb(sql,[id])
    label=''
    if result:
        label=result[0]
    jsonlist={'id':id,'label':label}
    return HttpResponse(simplejson.dumps(jsonlist, ensure_ascii=False))
    #return render_to_response('aui/jiage/chart.html',locals())
#新版获得报价趋势图数据
def pricechartdata(request):
    id=request.GET.get('id')
    gmt_begin=request.GET.get('gmt_begin')
    gmt_end=request.GET.get('gmt_end')
    ctype=request.GET.get('ctype')
    
    if not gmt_end:
        gmt_end=""
    else:
        gmt_end=str_to_int(gmt_end)
    if not gmt_begin:
        gmt_begin=""
    else:
        gmt_begin=str_to_int(gmt_begin)
    
    
    label=''
    area=''
    type_id=''
    sql2='select priceid,label,label1,area,type_id,spec from price_list where id=%s'
    result2=dbc.fetchonedb(sql2,[id])
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
        
    chartpricelist=zzprice.getchartpricelist(keywords=label,frompageCount=0,gmt_begin=gmt_begin,gmt_end=gmt_end,area=area,group='postdate',categoryid=type_id,ctype=ctype)
    if not chartpricelist:
        chartpricelist=zzprice.getchartpricelist(keywords=label,frompageCount=0,gmt_begin=gmt_begin,gmt_end=gmt_end,area=area,group='postdate',ctype=ctype)
    if chartpricelist:
        chartpricelist=chartpricelist[::-1]
    return HttpResponse(simplejson.dumps(chartpricelist, ensure_ascii=False))
#----企业报价
def compdetails(request):
    nowlanmu="<a href='/priceindex/'>行情报价</a>"
    id=request.GET.get("id")
    nowlanmu="<a href='/priceindex/'>行情报价</a>"
    webtitle="商家报价"
    sql='select title,details,category_company_price_code,refresh_time,company_id from company_price where id=%s'
    alist = zzprice.dbc.fetchonedb(sql,[id])
    if alist:
        title=alist[0]
        webtitle=title
        content=alist[1]
        category_cprice_code=alist[2]
        gmt_created=formattime(alist[3],3)
        sql2='select label from category_company_price where code=%s'
        alist2 = zzprice.dbc.fetchonedb(sql2,[category_cprice_code])
        if alist2:
            clabel=alist2[0]
            priceabout=zzprice.getpricelist(clabel,0,7,'',7)['list']
            zhioffer=zzprice.offerlist(clabel,'0',5)
            feizhibbsd=zzprice.getbbslist(clabel,10)
            if feizhibbsd:
                feizhibbs=feizhibbsd['list']
        
    #返回json数据
    datatype=request.GET.get("datatype")
    jsonlist={'alist':alist,}
    return HttpResponse(simplejson.dumps(jsonlist, ensure_ascii=False))
#企业报价类别
def companycategory(request):
    code=request.GET.get("code")
    categorylist=getcategory_company_price(code)
    return HttpResponse(simplejson.dumps(categorylist, ensure_ascii=False))

#企业报价详细
def companyprice_detail(request):
    id=request.GET.get("id")
    detail=zzprice.getcompanyprice_detail(id)
    company_id=0
    clabel=''
    if detail:
        clabel=detail['clabel']
    othercompany_price=zzt.getpricelist_company(frompageCount=0,limitNum=20,kname=clabel)
    jsonlist={'detail':detail,'othercompany_price':othercompany_price}
    return HttpResponse(simplejson.dumps(jsonlist, ensure_ascii=False))

#保存企业报价
def companyprice_save(request):
    company_id=request.POST.get("company_id")
    usertoken=request.POST.get("usertoken")
    if not getloginstatus(company_id,usertoken):
        errlist={'tokenerr':'true'}
        return HttpResponse(simplejson.dumps(errlist, ensure_ascii=False))
    
    account=getaccount(company_id)
    product_id=0
    appsystem=request.POST.get("appsystem")
    category_company_price_code=request.POST.get("category_company_price_code")
    title=request.POST.get("title")
    min_price=request.POST.get("min_price")
    max_price=request.POST.get("max_price")
    price_unit=request.POST.get("price_unit")
    area_code=request.POST.get("area_code")
    details=request.POST.get("details")
    is_checked=0
    post_time=gmt_created=gmt_modified=datetime.datetime.now()
    qpic="http://img0.zz91.com/zz91/images/indexLogo.png"
    
    sql="insert into company_price (company_id,account,product_id,category_company_price_code,title,min_price,max_price,price_unit,area_code,details,is_checked,post_time,gmt_created,gmt_modified) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
    result=dbc.updatetodb(sql,[company_id,account,product_id,category_company_price_code,title,min_price,max_price,price_unit,area_code,details,is_checked,post_time,gmt_created,gmt_modified])
    if result:
        qurl="http://m.zz91.com/jiage/cdetail"+str(result[0])+".html"
        sharelist={'title':title,'pic':qpic,'url':qurl}
        messagedata={'err':'false','errkey':'','type':'pricesave','sharelist':sharelist}
    else:
        messagedata={'err':'true','errkey':'系统错误，请重试3'}
    return HttpResponse(simplejson.dumps(messagedata, ensure_ascii=False))
    

def qihuo(request):
    host=getnowurl(request)
    nowlanmu="<a href='/priceindex/'>行情报价</a>"
    webtitle="期货"
    return render_to_response('price/qihuo.html',locals())
def youse(request):
    host=getnowurl(request)
    nowlanmu="<a href='/priceindex/'>行情报价</a>"
    webtitle="有色"
    return render_to_response('price/youse.html',locals())
def jinshuarea(request):
    host=getnowurl(request)
    nowlanmu="<a href='/priceindex/'>行情报价</a>"
    webtitle="废金属全国各地价格"
#    jinshulist=zzprice.getprice_clist(3)
    return render_to_response('price/jinshuarea.html',locals())
def suliaoarea(request):
    nowlanmu="<a href='/priceindex/'>行情报价</a>"
    webtitle="废塑料全国各地价格"
    host=getnowurl(request)
    return render_to_response('price/suliaoarea.html',locals())
def suliaoxinliao(request):
    webtitle="废塑料新料"
    nowlanmu="<a href='/priceindex/'>行情报价</a>"
    host=getnowurl(request)
    return render_to_response('price/suliaoxinliao.html',locals())
def areasuliao(request):
    nowlanmu="<a href='/priceindex/'>行情报价</a>"
    host=getnowurl(request)
    webtitle="各地废塑料行情"
    return render_to_response('price/areasuliao.html',locals())
def suliaoqihuo(request):
    nowlanmu="<a href='/priceindex/'>行情报价</a>"
    host=getnowurl(request)
    webtitle="塑料期货"
    return render_to_response('price/suliaoqihuo.html',locals())
def suliaozaishengliao(request):
    nowlanmu="<a href='/priceindex/'>行情报价</a>"
    host=getnowurl(request)
    webtitle="塑料再生料价格"
    return render_to_response('price/suliaozaishengliao.html',locals())
def meiguosuliao(request):
    nowlanmu="<a href='/priceindex/'>行情报价</a>"
    host=getnowurl(request)
    webtitle="美国废塑料价格"
    return render_to_response('price/meiguosuliao.html',locals())
def ouzhousuliao(request):
    nowlanmu="<a href='/priceindex/'>行情报价</a>"
    host=getnowurl(request)
    webtitle="欧洲废塑料价格"
    return render_to_response('price/ouzhousuliao.html',locals())
def feizhidongtai(request):
    nowlanmu="<a href='/priceindex/'>行情报价</a>"
    host=getnowurl(request)
    webtitle="废纸行情动态"
    return render_to_response('price/feizhidongtai.html',locals())
def feizhiarea(request):
    nowlanmu="<a href='/priceindex/'>行情报价</a>"
    webtitle="废纸各地价格"
    host=getnowurl(request)
    return render_to_response('price/feizhiarea.html',locals())
def feizhiriping(request):
    nowlanmu="<a href='/priceindex/'>行情报价</a>"
    webtitle="废纸日评"
    host=getnowurl(request)
    return render_to_response('price/feizhiriping.html',locals())