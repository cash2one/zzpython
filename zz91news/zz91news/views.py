#-*- coding:utf-8 -*-
from django.http import HttpResponse,HttpResponseRedirect,HttpResponsePermanentRedirect
from django.shortcuts import render_to_response
from django.core.cache import cache
from zz91settings import SPHINXCONFIG
from sphinxapi import SphinxClient,SPH_MATCH_BOOLEAN,SPH_SORT_EXTENDED,SPH_GROUPBY_ATTR,SPH_SORT_ATTR_DESC
from zz91page import *
import os,datetime,time,re,requests
from zz91tools import int_to_str,int_to_str2,getjiami,int_to_strall,getjiemi,filter_tags,subString,mobileuseragent,date_to_str,int_to_strall
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
zzn=zz91news()
execfile(nowpath+"/func/news_dbfunction.py")

def getlmselected(nid):
    list={'n1':'','n2':'','n3':'','n4':'','n5':'','n6':'','n7':'','n8':'','n9':'','n10':'','n185':'','n186':'','n187':'','n188':'','n175':'','n176':'','n195':'','n196':''}
    list[nid]={'css1':'class=nav-arrow','css2':'style=color:#FF0'}
    return list

def search(request):
    keywords = request.GET.get("keywords")
    keywords_hex=getjiami(keywords)
    nowurl="/column_list/tags-"+keywords_hex+".html"
    return HttpResponseRedirect(nowurl)

def zhuanti(request):
    webtitle="废金属行业知识_废塑料再生技术_废料防骗技巧-zz91再生网资讯中心"
    webkeywords="废金属行业知识，废塑料再生技术，废料防骗技巧"
    webdescription="zz91再生网资讯中心，为您整理废金属、废塑料行业知识，让您了解更多的再生技术，同时为您带来的还有废料生意防骗技巧，安全、放心地做生意。"
    typename='专题'
    typeurl="zhuanti"
    columnid=zzn.getcolumnid()
    #热门资讯排行
    hotest=zzn.getnewslist(num=10,typeid=columnid)
    #专题列表
    special_list=get_special_list()
    count=len(special_list)
    #专题推荐
    special_tui=zzn.get_news_all(0,4,flag='p,d')['list']
    return render_to_response('special.html',locals())

def index(request):
    lmselected=getlmselected("n1")
        #----进入手机模版
    agent=request.META['HTTP_USER_AGENT']
    agentflag=mobileuseragent(agent)
    seohost=" "
    if agentflag:
        return HttpResponsePermanentRedirect('http://m.zz91.com/news/')
    newslinks=getnewslinks1(0,40)
    webtitle="实时发布再生资源行业废料最新新闻资讯-zz91再生网资讯中心"
    webkeywords="废料新闻，废料资讯，废料行业资讯，废料资讯网，废料资讯中心，zz91再生网资讯中心"
    webdescription="zz91再生网资讯中心，为国内外废料商家提供最新、最及时的废料资讯，助您快速获得废金属、废塑料、综合废料等各个废料行业的最新信息。"
    subjectadlist=getadlist(593)
    time2=time.strftime('%Y-%m-%d',time.localtime(time.time()))
    #最下面的图片
    column_imgs=zzn.get_news_all(0,6,flag='p')['list']
    #早晚报
    downloadinfolist=getdownloadinfo()
    #id列表
    columnid=zzn.getcolumnid()
    #热门资讯排行
    hotnewslist=zzn.getnewslist(num=10,typeid=columnid)
    #企业新闻
    companynews=getcompanynews(0,8)
    #头条
    focus1=zzn.get_news_all(0,1,flag='h',has_txt=220)
    focus2=zzn.get_news_all(1,2,flag='h',has_txt=190)['list']
    #6条推荐
    choose6=zzn.get_news_all(0,6,flag='c',kwd=1)['list']
    #幻灯图片
    topic_img=zzn.get_news_all(0,4,flag='f')['list']
    #政策法规
    hangye10=zzn.get_news_all(0,10,typeid=185)['list']
    pinlun10=zzn.get_news_all(0,10,typeid=186)['list']
    jishu10=zzn.get_news_all(0,10,typeid=187)['list']
    kinds4=getfuzhuindexlist()
#    cols3=zzn.gettypelist(0,3,reid=184,has_news=10)
    return render_to_response('index.html',locals())

def newsdetail(request,kltype='',mltype='',newsid='',page=''):
    #----进入手机模版
    agent=request.META['HTTP_USER_AGENT']
    agentflag=mobileuseragent(agent)
    seohost="newsdetail"+str(newsid)+".htm"
    if agentflag and newsid:
        return HttpResponsePermanentRedirect('http://m.zz91.com/news/newsdetail'+newsid+'.htm')
    if kltype:
        typenameall=zzn.gettypenameid(kltype)
        if typenameall:
            typeid=typenameall['id']
            typename=typenameall['typename']
            lmselected=getlmselected("n"+str(typeid))
    if mltype:
        typenameall2=zzn.gettypenameid(mltype)
        if typenameall2:
            typeid2=typenameall2['id']
            typename2=typenameall2['typename']
    if newsid:
        if kltype and mltype:
            altype=kltype+'/'+mltype
        else:
            altype=kltype
        if not page:#翻页不加点击数
            sql="update dede_archives set click=click+1 where id=%s"
            dbn.updatetodb(sql,[newsid])
#        sql="select typeid,typeid2 from dede_archives where id=%s"
        newsdetails=zzn.getnewsdetail(newsid)
        if newsdetails:
            artypeid=newsdetails['typeid']
            columnid=zzn.getcolumnid()
            if artypeid in columnid:
                lmselected=getlmselected("n"+str(artypeid))
                artyped=zzn.gettypenameurl(artypeid)
                if artyped:
                    #获取主栏目
                    col_url=artyped['keywords']
                    col_name=artyped['typename']
                #获取副类别
                artypeid2=newsdetails['typeid2']
                gnjp='1'
                kind_url=''
                if artypeid2=='0' or artypeid2=="" or artypeid2==None:
                    kind_name=''
                    detail_url=col_url
                    stypeid2=''
                else:
                    artyped2=zzn.gettypenameurl(artypeid2)
                    if artyped2:
                        kind_url=artyped2['keywords']
                        kind_name=artyped2['typename']
                    detail_url=kind_url+'/'+col_url
                    gnjp=''
                    stypeid2=[int(artypeid2)]
                if altype==detail_url:
#                    return HttpResponse(altype)
                    qrcode_arg="http://m.zz91.com/newsviews.html?id="+newsid
                    #延伸阅读:辅助类别
                    news_detail_about=zzn.getnewslist(num=10,typeid=[artypeid],typeid2=stypeid2)
                    #本周热门资讯推荐
                    hotnewslist=zzn.getnewslist(num=10,typeid=[artypeid])
                    #推荐图片
                    hot_img=zzn.get_news_all(0,6,flag='p')['list']
                    #最新供求
                    indexofferlist=getindexofferlist_pic(kname='废',limitcount=3,membertype=1)
                    
                    #上一篇,下一篇文章
                    up_detail=zzn.getarticalup(newsid,artypeid,artypeid2,detail_url)
                    nex_detail=zzn.getarticalnx(newsid,artypeid,artypeid2,detail_url)
                    
                    content=newsdetails['body']
                    if content:
                        arg_content=content.replace(' ','')[:400]
                        img_url=get_img_url(arg_content)
                        div_tag=get_div_tag(content)
                        p_tag=get_p_tag(content)
                        br_tag=get_br_tag(content)
                        
                        content=content.replace('</div>','</div><br />')
                        content=content.replace('</p>','</p><br />')
                    else:
                        content=""
                    f139='富宝资讯'.decode('utf-8')
                    if f139 in content:
                        content=content.replace(f139,'')
                    text=filter_tags(content)
                    text_len=len(text)
                    every=120000
                    if text_len>120000 and '<tr' not in content:
                        if p_tag or br_tag:
                    #        all_page=len(content)/every+1
                            text_len=float(text_len)
                            
                            all_page=text_len/every
                            all_page=str(all_page)
                            
                            if '.' in all_page:#结果进一位(改变四舍五入)
                                all_page=int(all_page[:1])+1
                    
                            if (page=="" or page==None):
                                page=1
                            else:
                                page=int(page)
                            if (page==all_page):
                                pagenext=all_page
                            else:
                                pagenext=page+1
                            if (page==1):
                                pageprv=1
                            else:
                                pageprv=page-1
                                
                            pagefr=page-3
                            if pagefr<1:
                                pagefr=1
                            pagefd=pagefr+8
                            if pagefd>all_page:
                                pagefd=all_page
                            page_list=range(pagefr,pagefd+1)
                            
                            p_new=content.split('</p>')
                            big_p=get_big_p(content)
                            if big_p:
                                p_new=content.split('</P>')
                            if br_tag:
                                p_new=content.split('<br />')
                    #        len_c=[]
                    #        for clen in p_new:
                    #            if len(clen)<100:
                    #               len_c.append(clen)
                            l=len(p_new)#共几段
                            l=float(l)
                            
                            next=l/all_page
                            next=str(next)
                            if '.' in next:#结果进一位(改变四舍五入)
                                next=float(next)
                                if next<10.0:
                                    next=str(next)
                                    next=int(next[:1])+1
                                else:
                                    next=str(next)
                                    next=int(next[:2])+1
                            
                            pagea=(page-1)*next#开始读的位置
                            pagee=pagea+next#每次读几段
                            p_next=p_new[pagea:pagee]
                    
                            #content=''
                            #for p in p_next:
                            #    content=content+p+'</p>'
                            #content=content.replace(" [需要查看更多数据，请免费试用钢联数据]","")
                            text_len=int(text_len)
                            l=int(l)
                    title=newsdetails['title']
                    pubdate=newsdetails['pubdate']
                    click=newsdetails['click']
                    kwdlist=newsdetails['kwdlist']
                    if not title:
                        title=''
                    if not kind_name:
                        kind_name=''
                    if not col_name:
                        col_name=''
                    webtitle=title+'_'+kind_name+col_name+"-zz91再生网资讯中心".decode("utf8")
                    webkeywords=''
                    webdescription=text[:80]
                    if col_url=='zhuanti':
                        zhuanti=1
                        if kind_url=='fangpian':
                            fangpian=1
                    return render_to_response('news_detail.html',locals())
                else:
                    return HttpResponsePermanentRedirect('http://news.zz91.com/'+detail_url+'/newsdetail1'+newsid+'.htm')
    return render_to_response('news_detail.html',locals())
    return render_to_response('404.html',locals())

def newsalllist(request,kltype='',mltype='',tags_hex='',page=''):
#    return HttpResponse(tags_hex)
    typeid=''
    typeid2=''
    typename=''
    typename2=''
    if not kltype:
        kltype=request.META['PATH_INFO'].split('/')[1]
    keywords=''
    seohost=kltype+"/"
    if tags_hex:
        keywords=getjiemi(tags_hex)
        if kltype=='column_list':
            kltype=''
    if kltype:
        typenameall=zzn.gettypenameid(kltype)
        if typenameall:
            typeid=typenameall['id']
            typename=typenameall['typename']
            lmselected=getlmselected("n"+str(typeid))
        else:
            return render_to_response('404.html',locals())
    if mltype:
        typenameall2=zzn.gettypenameid(mltype)
        if typenameall2:
            typeid2=typenameall2['id']
            typename2=typenameall2['typename']
    nowlanmu=typename
    if typename2:
        nowlanmu=typename2
    col4=[185,186,187,188]
    otherm=[175,176,195,196]
    kid4=[153,154,155,156]
    stypeid=[typeid]
    if keywords:
        stypeid=''
        stypeid2=''
        nowlanmu=keywords
    if typeid in col4+otherm:
        #----主栏目
        is_main=1
        stypeid2=''
        if typeid2:
            stypeid2=[typeid2]
    elif typeid in kid4:
        #----辅助栏目
        is_main=''
        stypeid2=stypeid
        stypeid=''
        if typeid2:
            stypeid=[typeid]
            lmselected=getlmselected("n1")
    else:
        if not keywords:
            return render_to_response('404.html',locals())
    hotnewslist=zzn.getnewslist(num=10,typeid=stypeid,typeid2=stypeid2)
    special_tui=zzn.get_news_all(0,4,flag='p,d')['list']
    if not page:
        page=1
    funpage=zz91page()
    limitNum=funpage.limitNum(20)
    nowpage=funpage.nowpage(int(page))
    frompageCount=funpage.frompageCount()
    after_range_num = funpage.after_range_num(5)
    before_range_num = funpage.before_range_num(6)
    flag=''
    if typeid==196:
        flag=1
        stypeid=''
        hotnewslist=zzn.getnewslist(num=10,flag=flag)
    if typeid==195:
        columnid=zzn.getcolumnid()
        newslist=getcompanynews(frompageCount,limitNum,allcount=1)
        hotnewslist=zzn.getnewslist(num=10,typeid=columnid)
    else:
        newslist=zzn.getnewslist(keywords=keywords,frompageCount=frompageCount,limitNum=limitNum,typeid=stypeid,typeid2=stypeid2,flag=flag)
    listcount=0
    listall=newslist['list']
    titles1=listall[:5]
    titles2=listall[5:10]
    titles3=listall[10:15]
    titles4=listall[15:20]
    listcount=newslist['count']
    if int(listcount)>1000000:
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

    #获取url
    request_col=request.META['PATH_INFO']
    #用于行业资讯-废钢铁-列表if len_list==3
    col_req_all=re.findall('.*?/',request_col)
    #获取url第一,第二参数
    col_req=col_req_all[1].replace('/','')
    len_list=len(col_req_all)
    if len_list==3:
        col_req2=col_req_all[2].replace('/','')
    else:
        col_req2=''
    clo_name=typename
    if keywords:
        clo_name=keywords
        lmselected=getlmselected("n1")
    webtitle=clo_name+"废料资讯,废料新闻,再生资源资讯,再生资源行业动态,废料知识 - ZZ91再生网".decode('utf8')
    webkeywords=clo_name+"废料资讯,废料新闻,再生资源资讯,再生资源新闻,再生资源行业动态,再生资源企业新闻".decode('utf8')
    webdescription=clo_name+"ZZ91再生网商业资讯，实时发布最新行业资讯，助你掌握废金属、废塑料、综合废料等行业资讯".decode('utf8')
    if col_req=='hangye' and col_req2:
        webtitle=clo_name+'行业新闻资讯-zz91再生网资讯中心'.decode('utf8')
        webkeywords=clo_name+'行业资讯，'.decode('utf8')+clo_name+'行业新闻，'.decode('utf8')+'行业资讯网'.decode('utf8')
        webdescription='zz91再生网资讯中心，每一天都会实时地为您提供'.decode('utf8')+clo_name+'行业资讯和行业新闻，'.decode('utf8')+clo_name+'行业资讯网助您更好地了解您所在的行业。'.decode('utf8')
    elif col_req=='pinlun' and col_req2:
        webtitle=clo_name+'评论_'.decode('utf8')+clo_name+'分析_'.decode('utf8')+clo_name+'预测_-zz91再生网资讯中心'.decode('utf8')
        webkeywords=clo_name+'评论预测，'.decode('utf8')+clo_name+'分析预测'.decode('utf8')
        webdescription='zz91再生网资讯中心，快速发布关于废金属、废塑料、综合废料的市场前景以及专家的分析、评论和预测，让您随时知悉市场动态。'
    elif col_req=='tech' and col_req2:
        webtitle=clo_name+'技术_'.decode('utf8')+clo_name+'知识-zz91再生网资讯中心'.decode('utf8')
        webkeywords=clo_name+'技术，'.decode('utf8')+clo_name+'知识，'.decode('utf8')+clo_name+'技术资讯网'.decode('utf8')
        webdescription='zz91再生网资讯中心技术文库频道，为您带来各种关于废金属、废塑料和综合废料的专业知识，私人定制您所在行业的知识宝库。'
    elif col_req2=='hangye':
        webtitle=clo_name+'行业资讯_'.decode('utf8')+clo_name+'行业新闻-zz91再生网资讯中心'.decode('utf8')
        webkeywords=clo_name+'行业资讯，'.decode('utf8')+clo_name+'行业新闻，'.decode('utf8')+clo_name+'行业资讯网'.decode('utf8')
        webdescription='zz91再生网资讯中心，每一天都会实时地为您提供***行业资讯和行业新闻，***行业资讯网助您更好地了解您所在的行业。'
    elif col_req2=='pinlun':
        webtitle=clo_name+'评论_'.decode('utf8')+clo_name+'分析_'.decode('utf8')+clo_name+'预测_-zz91再生网资讯中心'.decode('utf8')
        webkeywords=clo_name+'评论预测，'.decode('utf8')+clo_name+'分析预测'.decode('utf8')
        webdescription='zz91再生网资讯中心，每一天都会实时地为您提供'.decode('utf8')+clo_name+'评论和分析预测，'.decode('utf8')+clo_name+'资讯网助您更好地了解您所在的行业。'.decode('utf8')
    elif col_req2=='tech':
        webtitle=clo_name+'技术_'.decode('utf8')+clo_name+'知识-zz91再生网资讯中心'.decode('utf8')
        webkeywords=clo_name+'技术，'.decode('utf8')+clo_name+'知识，'.decode('utf8')+clo_name+'技术资讯7F51'.decode('utf8')
        webdescription='zz91再生网资讯中心，每一天都会实时地为您提供'.decode('utf8')+clo_name+'技术和基础知识，'.decode('utf8')+clo_name+'资讯网助您更好地了解您所在的行业。'.decode('utf8')
    elif col_req2=='law':
        webtitle=clo_name+'政策法规-zz91再生网资讯中心'.decode('utf8')
        webkeywords=clo_name+'政策法规，'.decode('utf8')+clo_name+'政策，'.decode('utf8')+clo_name+'法规'.decode('utf8')
        webdescription=clo_name+'zz91再生网资讯中心，每一天都会实时地为您提供'.decode('utf8')+clo_name+'政策法规，'.decode('utf8')+clo_name+'资讯网助您更好地了解您所在的行业。'.decode('utf8')
    elif col_req=='guonei':
        webtitle='废料国内财经新闻资讯-zz91再生网资讯中心'
        webkeywords='废料国内财经，废料国内财经资讯，废料国内财经新闻'
        webdescription='zz91再生网资讯中心国内财经频道，及时地发包括宏观经济、GDP、CPI、PPI最新的国内废料财经新闻资讯，让您在国内投资市场的方向上更有把握。'
    elif col_req=='guoji':
        webtitle='废料国际财经新闻资讯-zz91再生网资讯中心'
        webkeywords='废料国际财经，废料国际财经资讯，废料国际财经新闻'
        webdescription='zz91再生网资讯中心国际财经频道，为您提供国际财经新闻报道,国际财经研究,分析、管理、增长、政策等资讯，让您在国际投资市场的方向上更有把握。'
    elif col_req=='law':
        webtitle='废料政策法规_废料政策_再生资源法规-zz91再生网资讯中心'
        webkeywords='废料政策法规，废料政策，废料法规，再生资源政策，再生资源法规'
        webdescription='zz91再生网资讯中心政策法规频道，为您整理再生资源各行各业的政策法规，让您随时随地掌握各种废料行业政策动态，放心做生意。'
    elif col_req=='company':
        webtitle='废料企业新闻_企业资讯_再生资源企业动态-zz91再生网资讯中心'
        webkeywords='废料企业新闻，废料企业资讯，再生资源企业动态'
        webdescription='zz91再生网资讯中心企业新闻频道，为您整理再生网注册的企业发布的最新企业新闻、废料动态和再生资源企业动态，在这里您可以了解到其他企业最新动态。'
    
    elif request_col=='/steel/list/':
        webtitle='废钢铁资讯_废钢铁新闻_废钢铁行业动态-zz91再生网资讯中心'
        webkeywords='废钢铁资讯，废钢铁新闻，废钢铁行业动态，废钢铁资讯网'
        webdescription='zz91再生网资讯中心废钢铁频道每天为您发布最新、最全面、最及时的废旧钢铁新闻、资讯以及行业动态。'
    elif request_col=='/youse/list/':
        webtitle='废有色金属资讯_废有色金属新闻_废有色行业动态-zz91再生网资讯中心'
        webkeywords='废有色金属资讯，废有色金属新闻，废有色金属行业动态，废金属资讯网'
        webdescription='zz91再生网资讯中心废有色频道每天为您发布包括金、银、铜、铅、铝、镍、锌以及它们之间构成的合金等废有色金属行业最全面的的新闻、资讯以及行业动态。'
    elif request_col=='/plastic/list/':
        webtitle='废塑料资讯_再生料行情_再生颗粒新闻-zz91再生网资讯中心'
        webkeywords='废塑料资讯，再生料行情，再生颗粒新闻，废塑料资讯网'
        webdescription='zz91再生网资讯中心废塑料频道每天为您发布最新、最全面、最及时的废塑料资讯，再生料行情以及再生颗粒新闻，同时分析当下的废料市场，为废塑料行业提供参考。'
    elif request_col=='/otherwaste/list/':
        webtitle='综合废料资讯_综合废料新闻_综合废料行业动态-zz91再生网资讯中心'
        webkeywords='综合废料资讯，综合废料新闻，综合废料行业动态'
        webdescription='zz91再生网资讯中心综合废料频道每天为您发布最权威的综合废料新闻、资讯以及行业动态，结合当下的市场情况，为您全面讲诉综合废料。'
    elif typeid==196:
        webtitle='废料图片新闻_再生资源图片资讯-zz91再生网资讯中心'
        webkeywords='废料图片新闻，废料图片资讯，再生资源图片资讯'
        webdescription='zz91再生网资讯中心图片新闻频道，通过各种废料的行情价格走势图、相关图片，为您归纳总结关于再生资源行业的价格行情，掌握一手资料，让做生意更简单。'

    return render_to_response('list_page.html',locals())

def newstype(request,kltype='',mltype=''):
    if kltype:
        typenameall=zzn.gettypenameid(kltype)
        if typenameall:
            typeid=typenameall['id']
            typename=typenameall['typename']
            lmselected=getlmselected("n"+str(typeid))
        else:
            return render_to_response('404.html',locals())
    special_te=zzn.get_news_all(0,2,flag='p,d')['list']
    hot_img=zzn.get_news_all(0,6,flag='p')['list']
    col4=[185,186,187,188]
    kid4=[153,154,155,156]
    #----进入手机模版
    agent=request.META['HTTP_USER_AGENT']
    agentflag=mobileuseragent(agent)
    if agentflag:
        if typeid in [185,186,187,188,175,176,195,196]:
            return HttpResponsePermanentRedirect('http://m.zz91.com/news/list-'+str(id)+'.html')
    is_main=''
    stypeid=[typeid]
    seohost=kltype+"/"
    if typeid in col4:
        #----主栏目
        is_main=1
        stypeid2=''
        typeid2=''
        toutypeflag='l'
        trtypeflag='e'
        choseflag='d'
        imgflag='b'
        retypeid=183
    elif typeid in kid4:
        #----辅助栏目
        typeid2=typeid
        stypeid2=stypeid
        stypeid=''
        typeid=''
        toutypeflag='g'
        trtypeflag='k'
        choseflag='i'
        imgflag='a'
        retypeid=184
    else:
        return render_to_response('404.html',locals())
        
    #本周热门资讯(栏目首页 和 类别首页)
    hot_thisweek=zzn.getnewslist(num=10,typeid=stypeid,typeid2=stypeid2)
    deputy_focus=zzn.get_news_all(0,3,flag=toutypeflag,typeid=typeid,typeid2=typeid2)['list']
    special=zzn.get_news_all(0,6,flag=trtypeflag,typeid=typeid)['list']
    choose6=zzn.get_news_all(0,6,flag=choseflag,typeid=typeid,typeid2=typeid2,kwd=1)['list']
    deputy_topic_img=zzn.get_news_all(0,4,flag=imgflag,typeid=typeid)['list']
    kinds4h=zzn.gettypelist(0,4,reid=retypeid,has_news=1,has_txt=30,typeid=typeid,typeid2=typeid2)
    kinds4=zzn.gettypelist(0,4,reid=retypeid,has_news=6,fromnews=1,typeid=typeid,typeid2=typeid2)
    kinds4h_1=kinds4h[0]
    kinds4h_2=kinds4h[1]
    kinds4h_3=kinds4h[2]
    kinds4h_4=kinds4h[3]
    kinds4_1=kinds4[0]
    kinds4_2=kinds4[1]
    kinds4_3=kinds4[2]
    kinds4_4=kinds4[3]
    if deputy_focus:
        deputy_focus1=deputy_focus[0]
        if len(deputy_focus)>1:
            deputy_focus2=deputy_focus[1]
        if len(deputy_focus)>2:
            deputy_focus3=deputy_focus[2]
    if special:
        special1=special[0]
        if len(special)>1:
            special2=special[1]
        if len(special)>2:
            special3=special[2]
        if len(special)>3:
            special4=special[3]
        if len(special)>4:
            special5=special[4]
        if len(special)>5:
            special6=special[5]
    if kltype=='hangye':
        webtitle='废料行业资讯_废料行业新闻_再生资源行业资讯_再生资源行业动态-zz91再生网资讯中心'
        webkeywords='废料行业资讯，废料行业新闻，再生资源行业资讯，再生资源行业动态'
        webdescription='zz91再生网资讯中心行业资讯频道，倾情为废金属、废金属、废塑料、综合废料等各个废料行业提供实时的行业资讯动态。'
    if kltype=='pinlun':
        webtitle='废料评论预测-zz91再生网资讯中心'
        webkeywords='废料评论预测，废料评论，废料预测 '
        webdescription='zz91再生网资讯中心评论预测频道，快速发布关于废金属、废塑料、综合废料的市场前景以及专家评论预测，让您随时知悉市场动态。'
    if kltype=='tech':
        webtitle='废料技术文库_废料基础知识_再生资源知识-zz91再生网资讯中心'
        webkeywords='废料知识，废料技术文库，废料基础知识，再生资源知识'
        webdescription='zz91再生网资讯中心技术文库频道，为您带来各种关于废金属、废塑料和综合废料的专业基础知识，私人定制您所在行业的知识宝库。'
    if not is_main:
        webtitle=typename+'新闻资讯-zz91再生网资讯中心'
        webkeywords=typename+'新闻，'+typename+'资讯，'+typename+'资讯中心'
        webdescription='zz91再生网资讯中心，不间断地为您发布关于'+typename+'的新闻资讯，让您能够快速获取'+typename+'方面的最新新闻资讯。'
    return render_to_response('cloumn_pg.html',locals())

#----------最终页
def replace_once(wenben,content,replace_content):
    if wenben in content:
        content_p=content.split(wenben)
        js=0
        for cp in content_p:
            js=js+1
            if 'alt=' not in cp:
                print js
                break
        content=wenben.join(content_p[:js])+replace_content+wenben.join(content_p[js:])
    return content

def verifycode(request):
    import StringIO,qrcode
    arg=request.GET.get('arg')
    if arg:
        return HttpResponsePermanentRedirect('http://www.feiliao123.com/verifycode/?arg='+arg)
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(arg)
    qr.make(fit=True)
    img = qr.make_image()
    mstream = StringIO.StringIO()
    img.save(mstream, "GIF")
    mstream.closed
    return HttpResponse(mstream.getvalue(),'image/gif')