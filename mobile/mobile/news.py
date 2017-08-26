#-*- coding:utf-8 -*-
from django.shortcuts import render_to_response
from django.http import HttpResponse,HttpResponseRedirect,HttpResponseNotFound,HttpResponsePermanentRedirect
import MySQLdb,sys,os,memcache,settings,urllib,re,time,datetime,requests,random,string,md5,hashlib
from django.core.cache import cache
from django.template.loader import get_template
from django.template import Context
from sphinxapi import *
from zz91page import *
from settings import spconfig
from zz91settings import SPHINXCONFIG
from commfunction import filter_tags,havepicflag,subString,getjiami,getIPFromDJangoRequest,validateEmail
from zz91tools import int_to_str,formattime,int_to_str2,date_to_int,getjiami,int_to_strall,getjiemi,filter_tags,subString,mobileuseragent,date_to_str
from datetime import timedelta, date 
from zz91db_ast import companydb
from zz91db_2_news import newsdb
dbc=companydb()
dbn=newsdb()

reload(sys)
sys.setdefaultencoding('UTF-8')
nowpath=os.path.dirname(__file__)
execfile(nowpath+"/commfunction.py")
execfile(nowpath+"/function.py")
execfile(nowpath+"/func/news_function.py")
zzn=zz91news()
#2017新版
def index(request,type='',type1='',page=''):
    host=getnowurl(request)
    seohost=host.replace("/news/","")
    keywords=request.GET.get("keywords")
    #最近搜索和相关搜索
    username=request.session.get("username",None)
    company_id=request.session.get("company_id",None)
    if not company_id:
        appid=request.session.get("appid",None)
    else:
        appid=company_id
    mysearchkeylist=getkeywords(appid)
    abountkeywords=searchtis(keywords)
    
    
    
    index=request.GET.get("index")
    typeid=''
    typeid2=''
    typename=''
    typename2=''
    searchlist={}
    if not index:
        index=0
    if not type and not type1 and not keywords:
        hot=1
        flag=1
    else:
        hot=None
        flag=None
    
    if keywords:
        searchlist['keywords']=keywords
    if index:
        searchlist['index']=index
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
    if (page=='' or page==0):
        page=1
    funpage=zz91page()
    limitNum=funpage.limitNum(20)
    nowpage=funpage.nowpage(int(page))
    frompageCount=funpage.frompageCount()
    after_range_num = funpage.after_range_num(5)
    before_range_num = funpage.before_range_num(4)
    newslist=zzn.getnewslist(keywords=keywords,frompageCount=frompageCount,limitNum=limitNum,allnum=100000,typeid=typeid,typeid2=typeid2,has_txt=300,flag=flag,hot=hot)
    listcount=0
    if (newslist):
        listall=newslist['list']
        listcount=newslist['count']
        if (int(listcount)>1000000):
            listcount=1000000-1
    listcount = funpage.listcount(listcount)
    page_listcount=funpage.page_listcount()
    firstpage = funpage.firstpage()
    lastpage = funpage.lastpage()
    page_range  = funpage.page_range()
    nextpage = funpage.nextpage()
    prvpage = funpage.prvpage()
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

    
    return render_to_response('aui/news/list.html',locals())
def zhlist(request,type='',page=''):
    host=getnowurl(request)
    seohost=host.replace("/news/","")
    if not type:
        t = get_template('404.html')
        html = t.render(Context())
        return HttpResponseNotFound(html)
    typename=zzn.getcategorylabel(type)
    index=request.GET.get("index")
    if not index:
        index=1
    searchlist={}
    #searchlist['plate_category_code']=type
    searchlist['index']=index
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
    if page=="1":
        topnewslist=zzn.getzhlist(frompageCount=0,limitNum=5,searchlist={'top':1})
    return render_to_response('aui/news/zhlist.html',locals())

def zhdetail(request,zhid=''):
    nottop=request.GET.get("nottop")
    host=getnowurl(request)
    seohost=host.replace("/news/","")
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
        
    webtitle=name+"_"+area_name+"- ZZ91再生网"
    webkeywords=""
    webdescription=subString(filter_tags(content),100)
    return render_to_response('aui/news/view_zh.html',locals())

def detail(request,type='',newsid=''):
    newsdetails=zzn.getnewsdetail(newsid)
    host=getnowurl(request)
    if not newsdetails:
        t = get_template('404.html')
        html = t.render(Context())
        return HttpResponseNotFound(html)
    if newsdetails.get("redirecturl"):
        return HttpResponseRedirect(newsdetails.get("redirecturl"))
    sql="update dede_archives set click=click+1 where id=%s"
    dbn.updatetodb(sql,[newsid])
    typeid=newsdetails['typeid']
    typename=newsdetails['typename']
    typename2=newsdetails['typename2']
    webtitle=newsdetails['title']+'_'+typename+"-zz91再生网资讯中心"
    webkeywords=''
    webdescription=newsdetails['minbody']
    keywords=newsdetails['keywords']
    if keywords:
        keywords=keywords.replace(",","|")
    #相关阅读
    xglist=zzn.getnewslist(keywords=keywords,num=5,sortby='pubdate desc',has_txt=300)
    newsurl=zzn.get_newstype(typeid=typeid)
    tourl="/"+newsurl["url"]+"/"+str(newsid)+".html"
    seohost=host.replace("/news/","")
    
    mycompany_id=request.session.get("company_id",None)
    favoriteflag=0
    if mycompany_id:
        favoriteflag=isfavorite(newsid,'10091012',mycompany_id)
    
    return render_to_response('aui/news/view.html',locals())
"""
#----资讯首页(一期)
def newsindex(request):
    keywords=request.GET.get("keywords")
    if keywords:
        return news_list(request,keywords=keywords)
    webtitle="资讯中心"
    nowlanmu="<a href='/news/'>资讯中心</a>"
    host=getnowurl(request)
    #cursor_news = conn_news.cursor()
    #newscolumn=getnewscolumn(cursor_news)
    newscolumn=getnewscolumn()
    #useragent=str(request.META)
    username=request.session.get("username",None)
    #cursor_news.close()
    return render_to_response('news/index.html',locals())
"""
#资讯列表页(一期)
def news_list301(request,typeid='',page=''):
    keywords=request.GET.get("keywords")
    tourl="/news/"
    if typeid:
        pinyin=getnewscolumnpinyin(typeid)
        tourl+=pinyin+"/"
    if page:
        tourl+="p"+str(page)+".html"
    if keywords:
        tourl+="?keywords="+keywords
    return HttpResponsePermanentRedirect(tourl)
def news_list(request,typeid='',type1='',page='',pinyin='',keywords=''):
    host=getnowurl(request)
    seohost=host.replace("/news/","")
    type=pinyin
    if type=="hydt":
        typeid=[186,185]
        typename="行业动态"
    elif type=="cjxw":
        typeid=[175,176]
        typename="财经新闻"
    else:
        if pinyin:
            typeid=getnewscolumnid(pinyin)
            if not typeid:
                return page404(request)
        if not typeid:
            typeid=0
        typename=get_typename(typeid)
        typeid=[typeid]
    if type1:
        typeid2=getnewscolumnid(type1)
        typename2=get_typename(typeid2)
    else:
        typeid2=None
    keywords=request.GET.get("keywords")
    if typeid==0:
       typename= keywords
    username=request.session.get("username",None)
    nowlanmu="<a href='/news/'>资讯中心</a>"
#    page=request.GET.get("page")
    if (keywords!=None):
        keywords=keywords.replace("资讯","")
        keywords=keywords.replace("价格","")
        webtitle=keywords
    if (str(keywords)=='None'):    
        keywords=None
        webtitle="资讯中心"
        
    if (page=='' or page==0):
        page=1
    funpage=zz91page()
    limitNum=funpage.limitNum(20)
    nowpage=funpage.nowpage(int(page))
    frompageCount=funpage.frompageCount()
    after_range_num = funpage.after_range_num(5)
    before_range_num = funpage.before_range_num(4)
    if str(typeid)=='196':
        newslist=getnewslist(keywords="p",frompageCount=frompageCount,limitNum=limitNum,typeid='',allnum='',typeid2=typeid2)
    elif str(typeid)=='195':
        newslist=getcompanynews(frompageCount,limitNum)
    else:
        newslist=getnewslist(keywords=keywords,frompageCount=frompageCount,limitNum=limitNum,typeid=typeid,allnum='',typeid2=typeid2)
    listcount=0
    if (newslist):
        listall=newslist['list']
        listcount=newslist['count']
        if (int(listcount)>1000000):
            listcount=1000000-1
    listcount = funpage.listcount(listcount)
    page_listcount=funpage.page_listcount()
    firstpage = funpage.firstpage()
    lastpage = funpage.lastpage()
    page_range  = funpage.page_range()
    nextpage = funpage.nextpage()
    prvpage = funpage.prvpage()
#    newsnav=getnewsnav()
#    listall=listalla['list']
#    newslistcount=listalla['count']
    
    if (listcount==1):
        morebutton='style=display:none'
    else:
        morebutton=''
    #cursor_news.close()
    return render_to_response('news/list.html',locals())

#----资讯最终页(一期)
def newsdetail(request,newsid=''):
    host=getnowurl(request)
    id=newsid
    seohost=host.replace("/news/","")
    #cursor_news = conn_news.cursor()
    typeid=request.GET.get("typeid")
    webtitle="资讯中心"
    nowlanmu="<a href='/news/'>资讯中心</a>"
    username=request.session.get("username",None)
    showpost=1
    if typeid=='195':
        content=getshowcompanynews(id)
        typename='企业新闻'
        articalup=getcompanyup(id)
        articalnx=getcompanynx(id)
    else:
        #newsclick_add(id)
        #content=getnewscontent(id)
        #webtitle=content['title']
        #if not webtitle:
        #    return HttpResponseNotFound("错误")
        #获得当前新闻栏目
        newstype=get_newstype(id)
        if newstype:
            typename=newstype['typename']
            typeid=newstype['typeid']
            newsurl=zzn.get_newstype(typeid=typeid)
            tourl="/news/"+newsurl["url"]+"/"+str(id)+".html"
            if newsurl:
                return HttpResponsePermanentRedirect(tourl)
            
            typeid2=newstype['typeid2']
            typeurl1=newstype['url']
            typeurl2=newstype['url2']
            if typeurl1==typeurl2:
                typeurl1=None
            seohost=""
            if typeurl2:
                seohost+=typeurl2+"/"
            if typeurl1:
                seohost+=typeurl1+"/"
            seohost+="newsdetail1"+str(id)+".htm"
            #相关阅读
            #typenews=get_typenews(typeid,typeid2,cursor_news)
            #上一篇文章
            articalup=getarticalup(id,typeid)
            #下一篇文章
            articalnx=getarticalnx(id,typeid)
    #cursor_news.close()
    return render_to_response('news/detail.html',locals())