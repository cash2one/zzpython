#-*- coding:utf-8 -*-
from django.http import HttpResponse,HttpResponseRedirect,HttpResponsePermanentRedirect,HttpResponseNotFound
from django.shortcuts import render_to_response
from django.core.cache import cache
from django.template.loader import get_template
from django.template import Context
from zz91settings import SPHINXCONFIG
from sphinxapi import SphinxClient,SPH_MATCH_BOOLEAN,SPH_SORT_EXTENDED,SPH_GROUPBY_ATTR,SPH_SORT_ATTR_DESC
from zz91page import *
import simplejson,os,datetime,time,re,urllib,requests
from zz91tools import int_to_str,formattime,int_to_str2,date_to_int,getjiami,int_to_strall,getjiemi,filter_tags,subString,mobileuseragent,date_to_str,int_to_strall
from zz91db_ast import companydb
from zz91db_ads import adsdb
from zz91db_2_news import newsdb
from datetime import date,timedelta
from zz91db_130 import otherdb
dbo=otherdb()
dbc=companydb()
dba=adsdb()
dbn=newsdb()


nowpath=os.path.dirname(__file__)
execfile(nowpath+"/func/news_tools.py")
execfile(nowpath+"/func/news_function.py")
execfile(nowpath+"/func/news_dbfunction.py")

zzn=zz91news()
def index(request):
    topadlist=getadlist(851)
    hotnewslist=zzn.getnewslist(num=10,sortby='click desc',has_txt=300,flag=1,hot=1)
    hylist=zzn.getnewslist(num=6,typeid=[185],sortby='pubdate desc',has_txt=300,flag=1)
    cjlist=zzn.getnewslist(num=5,typeid=[175,176],sortby='pubdate desc',has_txt=300)
    zclist=zzn.getnewslist(num=5,typeid=[188],sortby='pubdate desc',has_txt=300)
    guanzhulist=zzn.getguanzhu()
    return render_to_response('new/index.html',locals())

#展会频道
def zhindex(request):
    topadlist=getadlist(852)
    rightadlist=getadlist(853)
    #专题报道
    searchlist={}
    searchlist['plate_category_code']="10371003"
    ztlist=zzn.getzhlist(0,4,searchlist=searchlist)
    
    #展会报道
    searchlist={}
    searchlist['plate_category_code']="10371009"
    bdlist=zzn.getzhlist(0,5,searchlist=searchlist)
    
    #即将召开
    searchlist={'noexpress':1}
    #searchlist['plate_category_code']="10371002"
    nowlist=zzn.getzhlist(0,1,searchlist=searchlist)
    
    #中部展会广告
    searchlist={}
    searchlist['plate_category_code']="10371005"
    midlist=zzn.getzhlist(0,1,searchlist=searchlist)
    
    
    return render_to_response('new/zhindex.html',locals())

def zhlist(request,type=''):
    if not type:
        t = get_template('404.html')
        html = t.render(Context())
        return HttpResponseNotFound(html)
    typename=zzn.getcategorylabel(type)
    topadlist=getadlist(852)
    page=request.GET.get("page")
    searchlist={}
    searchlist['plate_category_code']=type
    #if searchlist:
    #    searchurl="?"+urllib.urlencode(searchlist)
    if not page:
        page=1
    funpage=zz91page()
    limitNum=funpage.limitNum(20)
    nowpage=funpage.nowpage(int(page))
    frompageCount=funpage.frompageCount()
    after_range_num = funpage.after_range_num(5)
    before_range_num = funpage.before_range_num(6)
    newslist=zzn.getzhlist(frompageCount=frompageCount,limitNum=limitNum,searchlist=searchlist)
    listcount=0
    listall=newslist['list']
    listcount=newslist['count']
    if int(listcount)>1000000:
        listcount=1000000-1
    listcount = funpage.listcount(listcount)
    page_listcount=funpage.page_listcount()
    firstpage = funpage.firstpage()
    lastpage = funpage.lastpage()
    page_range  = funpage.page_range()
    nextpage = funpage.nextpage()
    prvpage = funpage.prvpage()
    if prvpage<=1:
        prvpage=1
    if nextpage>=page_listcount:
        nextpage=page_listcount
    if nextpage>500:
        nextpage=500
    page=str(page)
    webtitle=typename+"_再生资源会展-第"+page+"页-ZZ91再生网"
    webkeywords=typename+",废金属展会,国际塑胶展览会,二手设备展会,再生资源会展"
    webdescription="ZZ91再生网展会频道提供最新国内再生资源行业展会、国际展会、展会动态、展会报道、参展咨询及展会回顾等丰富信息内容，更多信息可登录ZZ91再生网查看更多。"
    return render_to_response('new/zhlist.html',locals())

def zhdetail(request,zhid=''):
    sql="select a.name,a.area,a.start_time,a.end_time,a.plate_category_code,a.exhibit_category_code,a.content,a.tags,a.photo_cover,a.allzhuban,a.hz_categorylist,a.gmt_created,a.gmt_modified,d.label as area_name,a.redircturl from exhibit as a left outer join category as d on a.area_code=d.code where a.id=%s"
    result=dbc.fetchonedb(sql,[zhid])
    if result:
        name=result[0]
        area=result[1]
        
        start_time=formattime(result[2],1)
        intstarttime=date_to_int(result[2])
        nowint=date_to_int(datetime.datetime.now())
        haveday=None
        if intstarttime>nowint:
            haveday=(intstarttime-nowint)/(3600*24)
        end_time=formattime(result[3],1)
        plate_category_code=result[4]
        exhibit_category_code=result[5]
        content=result[6]
        tags=result[7]
        if not tags:
            tags=''
        litpic=result[8]
        if not litpic:
            litpic=''
        allzhuban=result[9]
        if not allzhuban:
            allzhuban=''
        hz_categorylist=result[10]
        area_name=result[13]
        redircturl=result[14]
        if redircturl:
            return HttpResponseRedirect(redircturl)
        if not area:
            area=area_name
        if not area_name:
            area_name=area
        if not area:
            area=''
        if not area_name:
            area_name=''
        if not hz_categorylist:
            hz_categorylist=''
    else:
        t = get_template('404.html')
        html = t.render(Context())
        return HttpResponseNotFound(html)
        
    searchlist={}
    searchlist['plate_category_code']="10371009"
    zhnewslist=zzn.getzhlist(0,20,searchlist=searchlist)
    #专题报道
    searchlist={}
    searchlist['plate_category_code']="10371003"
    ztlist=zzn.getzhlist(0,4,searchlist=searchlist)
    webtitle=name+"_"+area_name+"- ZZ91再生网"
    webkeywords=""
    webdescription=subString(filter_tags(content),100)
    return render_to_response('new/zhdetail.html',locals())

def newslist(request,type='',type1='',page=''):
    keywords=request.GET.get("keywords")
    typeid=''
    typeid2=''
    typename=''
    typename2=''
    searchlist={}
    if keywords:
        searchlist['keywords']=keywords
    if type:
        if type=="hydt":
            typeid=[186,185]
            typename="行业动态"
        elif type=="cjxw":
            typeid=[175,176]
            typename="财经新闻"
        else:
            typelist=zzn.gettypenameid(type)
            if typelist:
                typeid=[typelist['id']]
                typename=typelist['typename']
    if type1:
        typelist1=zzn.gettypenameid(type1)
        if typelist1:
            typeid2=[typelist1['id']]
            typename2=typelist1['typename']
    else:
        typeid2=None
    searchurl=''
    if searchlist:
        searchurl="?"+urllib.urlencode(searchlist)
    if not page:
        page=1
    funpage=zz91page()
    limitNum=funpage.limitNum(20)
    nowpage=funpage.nowpage(int(page))
    frompageCount=funpage.frompageCount()
    after_range_num = funpage.after_range_num(5)
    before_range_num = funpage.before_range_num(6)
    newslist=zzn.getnewslist(keywords=keywords,frompageCount=frompageCount,limitNum=limitNum,allnum=100000,typeid=typeid,typeid2=typeid2,has_txt=300)
    listcount=0
    listall=newslist['list']
    listcount=newslist['count']
    if int(listcount)>1000000:
        listcount=1000000-1
    listcount = funpage.listcount(listcount)
    page_listcount=funpage.page_listcount()
    firstpage = funpage.firstpage()
    lastpage = funpage.lastpage()
    page_range  = funpage.page_range()
    nextpage = funpage.nextpage()
    prvpage = funpage.prvpage()
    if prvpage<=1:
        prvpage=1
    if nextpage>500:
        nextpage=500
    #热门产品导航
    cplist=zzn.getcplist(keywords,30)
    guanzhulist=zzn.getguanzhu()
    if not listall:
        hotnewslist=zzn.getnewslist(num=10,sortby='click desc',has_txt=300,flag=1,hot=1)
    col_req=type
    col_req2=type1
    clo_name=typename
    clo_name1=typename2
    if keywords:
        clo_name=keywords
    page=str(page)
    webtitle=clo_name+"废料资讯,废料新闻,再生资源资讯,再生资源行业动态,废料知识-第"+page+"页 - ZZ91再生网"
    webkeywords=clo_name+"废料资讯,废料新闻,再生资源资讯,再生资源新闻,再生资源行业动态,再生资源企业新闻"
    webdescription=clo_name+"ZZ91再生网商业资讯，实时发布最新行业资讯，助你掌握废金属、废塑料、综合废料等行业资讯"
    if (col_req=='hydt' or col_req=='hangye') and not col_req2:
        webtitle=clo_name+'行业新闻资讯-第'+page+'页-zz91再生网资讯中心'
        webkeywords=clo_name+'行业资讯，'+clo_name+'行业新闻，行业资讯网'
        webdescription='zz91再生网资讯中心，每一天都会实时地为您提供'+clo_name+'行业资讯和行业新闻，'+clo_name+'行业资讯网助您更好地了解您所在的行业。'
    if col_req=='hydt' and col_req2:
        webtitle=clo_name1+'行业新闻资讯-第'+page+'页-zz91再生网资讯中心'
        webkeywords=clo_name1+'行业资讯，'+clo_name1+'行业新闻，行业资讯网'
        webdescription='zz91再生网资讯中心，每一天都会实时地为您提供'+clo_name1+'行业资讯和行业新闻，'+clo_name1+'行业资讯网助您更好地了解您所在的行业。'
    
    
    elif col_req=='tech' and not col_req2:
        webtitle='废料技术文库_废料基础知识_再生资源知识-第'+page+'页-zz91再生网资讯中心'
        webkeywords='废料知识，废料技术文库，废料基础知识，再生资源知识'
        webdescription='zz91再生网资讯中心技术文库频道，为您带来各种关于废金属、废塑料和综合废料的专业基础知识，私人定制您所在行业的知识宝库。'
    elif col_req=='tech' and col_req2:
        webtitle=clo_name1+'技术_'+clo_name1+'知识-第'+page+'页-zz91再生网资讯中心'
        webkeywords=clo_name1+'技术，'+clo_name1+'知识，'+clo_name1+'技术资讯网'
        webdescription='zz91再生网资讯中心技术文库频道，为您带来各种关于废金属、废塑料和综合废料的专业知识，私人定制您所在行业的知识宝库。'
    
    
    elif col_req2=='hangye':
        webtitle=clo_name+'行业资讯_'+clo_name+'行业新闻-第'+page+'页-zz91再生网资讯中心'
        webkeywords=clo_name+'行业资讯，'+clo_name+'行业新闻，'+clo_name+'行业资讯网'
        webdescription='zz91再生网资讯中心，每一天都会实时地为您提供***行业资讯和行业新闻，***行业资讯网助您更好地了解您所在的行业。'
    elif col_req2=='pinlun':
        webtitle=clo_name+'评论_'+clo_name+'分析_'+clo_name+'预测-第'+page+'页-zz91再生网资讯中心'
        webkeywords=clo_name+'评论预测，'+clo_name+'分析预测'
        webdescription='zz91再生网资讯中心，每一天都会实时地为您提供'+clo_name+'评论和分析预测，'+clo_name+'资讯网助您更好地了解您所在的行业。'
    elif col_req2=='tech':
        webtitle=clo_name+'技术_'+clo_name+'知识-第'+page+'页-zz91再生网资讯中心'
        webkeywords=clo_name+'技术，'+clo_name+'知识，'+clo_name+'技术资讯7F51'
        webdescription='zz91再生网资讯中心，每一天都会实时地为您提供'+clo_name+'技术和基础知识，'+clo_name+'资讯网助您更好地了解您所在的行业。'
    elif col_req2=='law':
        webtitle=clo_name+'政策法规-第'+page+'页-zz91再生网资讯中心'
        webkeywords=clo_name+'政策法规，'+clo_name+'政策，'+clo_name+'法规'
        webdescription=clo_name+'zz91再生网资讯中心，每一天都会实时地为您提供'+clo_name+'政策法规，'+clo_name+'资讯网助您更好地了解您所在的行业。'
    elif col_req=="cjxw" and not col_req2:
        webtitle='废料财经新闻资讯-第'+page+'页-zz91再生网资讯中心'
        webkeywords='废料财经，废料财经资讯，废料财经新闻'
        webdescription='zz91再生网资讯中心财经频道，及时地发包括宏观经济、GDP、CPI、PPI最新的废料财经新闻资讯，让您在投资市场的方向上更有把握。'
    elif col_req2=='guonei':
        webtitle='废料国内财经新闻资讯-第'+page+'页-zz91再生网资讯中心'
        webkeywords='废料国内财经，废料国内财经资讯，废料国内财经新闻'
        webdescription='zz91再生网资讯中心国内财经频道，及时地发包括宏观经济、GDP、CPI、PPI最新的国内废料财经新闻资讯，让您在国内投资市场的方向上更有把握。'
    elif col_req2=='guoji':
        webtitle='废料国际财经新闻资讯-第'+page+'页-zz91再生网资讯中心'
        webkeywords='废料国际财经，废料国际财经资讯，废料国际财经新闻'
        webdescription='zz91再生网资讯中心国际财经频道，为您提供国际财经新闻报道,国际财经研究,分析、管理、增长、政策等资讯，让您在国际投资市场的方向上更有把握。'
    elif col_req=='law' and not col_req2:
        webtitle='废料政策法规_废料政策_再生资源法规-第'+page+'页-zz91再生网资讯中心'
        webkeywords='废料政策法规，废料政策，废料法规，再生资源政策，再生资源法规'
        webdescription='zz91再生网资讯中心政策法规频道，为您整理再生资源各行各业的政策法规，让您随时随地掌握各种废料行业政策动态，放心做生意。'
    
    elif col_req=='pinlun' and not col_req2:
        webtitle=clo_name+'评论_'+clo_name+'分析_'+clo_name+'预测-第'+page+'页-zz91再生网资讯中心'
        webkeywords=clo_name+'评论预测，'+clo_name+'分析预测'
        webdescription='zz91再生网资讯中心，快速发布关于废金属、废塑料、综合废料的市场前景以及专家的分析、评论和预测，让您随时知悉市场动态。'
    
    elif col_req=='company':
        webtitle='废料企业新闻_企业资讯_再生资源企业动态-第'+page+'页-zz91再生网资讯中心'
        webkeywords='废料企业新闻，废料企业资讯，再生资源企业动态'
        webdescription='zz91再生网资讯中心企业新闻频道，为您整理再生网注册的企业发布的最新企业新闻、废料动态和再生资源企业动态，在这里您可以了解到其他企业最新动态。'
    
    elif not col_req and col_req2=='steel':
        webtitle='废钢铁资讯_废钢铁新闻_废钢铁行业动态-第'+page+'页-zz91再生网资讯中心'
        webkeywords='废钢铁资讯，废钢铁新闻，废钢铁行业动态，废钢铁资讯网'
        webdescription='zz91再生网资讯中心废钢铁频道每天为您发布最新、最全面、最及时的废旧钢铁新闻、资讯以及行业动态。'
    elif not col_req and col_req2=='youse':
        webtitle='废有色金属资讯_废有色金属新闻_废有色行业动态-第'+page+'页-zz91再生网资讯中心'
        webkeywords='废有色金属资讯，废有色金属新闻，废有色金属行业动态，废金属资讯网'
        webdescription='zz91再生网资讯中心废有色频道每天为您发布包括金、银、铜、铅、铝、镍、锌以及它们之间构成的合金等废有色金属行业最全面的的新闻、资讯以及行业动态。'
    elif not col_req and col_req2=='plastic':
        webtitle='废塑料资讯_再生料行情_再生颗粒新闻-第'+page+'页-zz91再生网资讯中心'
        webkeywords='废塑料资讯，再生料行情，再生颗粒新闻，废塑料资讯网'
        webdescription='zz91再生网资讯中心废塑料频道每天为您发布最新、最全面、最及时的废塑料资讯，再生料行情以及再生颗粒新闻，同时分析当下的废料市场，为废塑料行业提供参考。'
    elif not col_req and col_req2=='otherwaste':
        webtitle='综合废料资讯_综合废料新闻_综合废料行业动态-第'+page+'页-zz91再生网资讯中心'
        webkeywords='综合废料资讯，综合废料新闻，综合废料行业动态'
        webdescription='zz91再生网资讯中心综合废料频道每天为您发布最权威的综合废料新闻、资讯以及行业动态，结合当下的市场情况，为您全面讲诉综合废料。'

    return render_to_response('new/newslist.html',locals())
def myorderlist(request):
    company_id=request.GET.get("company_id")
    page=request.GET.get("page")
    if not page:
        page=1
    hotnewslist=zzn.getnewslist(frompageCount=int(page)*10,limitNum=10,sortby='pubdate desc',has_txt=300,company_id=company_id)
    res={'err':'false','errkey':'','list':hotnewslist}
    res=simplejson.dumps(res,ensure_ascii=False)
    return HttpResponse(res)
def myguanzhu(request):
    company_id=request.GET.get("company_id")
    guanzhu=zzn.getmyguanzhu(company_id)
    if guanzhu:
        res={'err':'false','errkey':'','guanzhu':guanzhu}
    else:
        res={'err':'true','errkey':'无关注信息'}
    res=simplejson.dumps(res,ensure_ascii=False)
    return HttpResponse(res)
#点赞
def dianzhan(request):
    newsid=request.GET.get("newsid")
    company_id=request.GET.get("company_id")
    sql="select id from dianzhan where aid=%s and company_id=%s"
    result=dbn.fetchonedb(sql,[newsid,company_id])
    if not result:
        sql="update dede_archives set goodpost=goodpost+1 where id=%s"
        result=dbn.updatetodb(sql,[newsid])
        gmt_created=datetime.datetime.now()
        sql="insert into dianzhan (aid,company_id,gmt_created) values(%s,%s,%s)"
        result=dbn.updatetodb(sql,[newsid,company_id,gmt_created])
        if result:
            res={'err':'false','errkey':'点赞成功','type':'zhan'}
    else:
        sql="delete from dianzhan where aid=%s and company_id=%s"
        dbn.updatetodb(sql,[newsid,company_id]);
        res={'err':'false','errkey':'取消成功','type':'unzhan'}
        sql="update dede_archives set goodpost=goodpost-1 where id=%s"
        result=dbn.updatetodb(sql,[newsid])
    res=simplejson.dumps(res,ensure_ascii=False)
    return HttpResponse(res)
#是否点赞
def isdianzhan(request):
    newsid=request.GET.get("newsid")
    company_id=request.GET.get("company_id")
    newslist=newsid.split(",")
    nlist=[]
    for nid in newslist:
        if nid:
            sql="select id from dianzhan where aid=%s and company_id=%s"
            result=dbn.fetchonedb(sql,[nid,company_id])
            if result:
                nlist.append(1)
            else:
                nlist.append(0)
    res={'err':'false','errkey':'','zhanlist':nlist}
    res=simplejson.dumps(res,ensure_ascii=False)
    return HttpResponse(res)

def detail(request,type='',newsid=''):
    newsdetails=zzn.getnewsdetail(newsid)
    if not newsdetails:
        t = get_template('404.html')
        html = t.render(Context())
        return HttpResponseNotFound(html)
    if newsdetails.get("redirecturl"):
        return HttpResponseRedirect(newsdetails.get("redirecturl"))
    sql="update dede_archives set click=click+1 where id=%s"
    dbn.updatetodb(sql,[newsid])
    #热门产品导航
    cplist=zzn.getcplist('',30)
    guanzhulist=zzn.getguanzhu()
    typename=newsdetails['typename']
    typename2=newsdetails['typename2']
    webtitle=newsdetails['title']+'_'+typename+"-zz91再生网资讯中心"
    webkeywords=''
    webdescription=newsdetails['minbody']
    return render_to_response('new/detail.html',locals())
#我的订阅
def myorder(request):
    #热门产品导航
    cplist=zzn.getcplist('',30)
    return render_to_response('new/myorder.html',locals())
#关注
def insert_myguanzhu(request):
    company_id=request.GET.get("company_id")
    if not company_id:
        errlist={'err':'login'}
        return HttpResponse(simplejson.dumps(errlist, ensure_ascii=False))
    tags=request.GET.get("tags")
    typeid=request.GET.get("typeid")
    fclose=request.GET.get("close")
    addtime=time.time()
    if str(fclose)=="1":
        sql="delete from myguanzhu where company_id=%s and tags=%s"
        dbn.updatetodb(sql,[company_id,tags])
        gzflag=0
    else:
        sql="select id from myguanzhu where company_id=%s and tags=%s"
        result=dbn.fetchonedb(sql,[company_id,tags])
        if not result:
            sql="insert into myguanzhu (company_id,tags,typeid,addtime) values(%s,%s,%s,%s)"
            dbn.updatetodb(sql,[company_id,tags,typeid,addtime])
            gzflag=1
        else:
            gzflag=1
    return HttpResponse(simplejson.dumps({"err":"false","errkey":"",'gzflag':gzflag}, ensure_ascii=False))
#是否已经收藏
def isfavorite(request):
    company_id=request.GET.get("company_id")
    favorite_type_code='10091012'
    newsid=request.GET.get("newsid")
    newslist=newsid.split(",")
    nlist=[]
    for nid in newslist:
        if nid:
            result=zzn.isfavorite(nid,favorite_type_code,company_id)
            nlist.append(result)
    res={'err':'false','errkey':'','favortelist':nlist}
    res=simplejson.dumps(res,ensure_ascii=False)
    return HttpResponse(res)
#收藏
def favorite(request):
    company_id=request.GET.get("company_id")
    if not company_id or str(company_id)=="0":
        return HttpResponse(simplejson.dumps({'err':'login'}, ensure_ascii=False))
    account=getaccount(company_id)
    
    favorite_type_code=request.GET.get("favorite_type_code")
    content_id=request.GET.get("content_id")
    if not content_id:
        content_id=0
    content_title=request.GET.get("title")
    if not content_title:
        sql='select title from dede_archives where id=%s'
        result=dbn.fetchonedb(sql,[content_id])
        if result:
            content_title=result[0]
        else:
            messagedata={'err':'true','errkey':'错误','type':'favorite'}
            return HttpResponse(simplejson.dumps(messagedata, ensure_ascii=False))
        
    gmt_created=datetime.datetime.now()
    gmt_modified=datetime.datetime.now()

    value=[favorite_type_code,content_id,content_title,gmt_created,gmt_modified,company_id,account]
    sql="select id from myfavorite where favorite_type_code=%s and content_id=%s and company_id=%s"
    clist=dbc.fetchonedb(sql,[favorite_type_code,content_id,company_id])
    if (clist):
        sql="delete from myfavorite where favorite_type_code=%s and content_id=%s and company_id=%s"
        dbc.updatetodb(sql,[favorite_type_code,content_id,company_id]);
        messagedata={'err':'false','errkey':'取消成功','type':'unfavorite'}
        return HttpResponse(simplejson.dumps(messagedata, ensure_ascii=False))
    else:
        sql="insert into myfavorite(favorite_type_code,content_id,content_title,gmt_created,gmt_modified,company_id,account) values(%s,%s,%s,%s,%s,%s,%s)"
        dbc.updatetodb(sql,value);
        messagedata={'err':'false','errkey':'收藏成功','type':'favorite'}
    return HttpResponse(simplejson.dumps(messagedata, ensure_ascii=False))
def myfavoritelist(request):
    company_id=request.GET.get("company_id")
    page=request.GET.get("page")
    if not page:
        page=1
    if company_id:
        list=zzn.myfavorite(company_id,(int(page)-1)*10,10)
        messagedata={'err':'false','errkey':'','list':list}
    else:
        messagedata={'err':'true','errkey':'','list':''}
    return HttpResponse(simplejson.dumps(messagedata, ensure_ascii=False))

def verifycode(request):
    import StringIO,qrcode
    arg=request.GET.get('arg')
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=2,
    )
    qr.add_data(arg)
    qr.make(fit=True)
    img = qr.make_image()
    mstream = StringIO.StringIO()
    img.save(mstream, "GIF")
    mstream.closed
    return HttpResponse(mstream.getvalue(),'image/gif')
