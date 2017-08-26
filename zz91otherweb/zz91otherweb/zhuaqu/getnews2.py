#-*- coding:utf-8 -*-
import re,time,os,sys
from getnews import get_content,get_keywords,hand_content,hand_contentimg,get_url_content,replace_img_sex,get_img_url,get_title_url,get_a_url,get_inner_a,get_contentpagenum
from simptools import time1,time2,time3,newspath,remove_script,remove_content_a,savetime,filter_tags
from savetodb import savedbdacong,get_new,iszhuaqu
import bs4
from bs4 import BeautifulSoup
reload(sys)
sys.setdefaultencoding('utf8')
#dachonglaile 数据抓取
def get_daconglist(typeid,typeid2,url,pagelist,listconf):
    main_url=listconf['main_url']
    re_html=listconf['re_html']
    re_list=listconf['re_list']
    re_time=''
    re_content=listconf['re_content']
    re_hand=[]
    re_encode=listconf['re_encode']
    re_contentpage=listconf['re_contentpage']
    re_contentpagenum=listconf['re_contentpagenum']
    re_contentpagestr=listconf['re_contentpagestr']
    re_keywords=''
    if listconf.has_key("re_keywords"):
        re_keywords=listconf['re_keywords']
    keywords=''
    if listconf.has_key("keywords"):
        keywords=listconf['keywords']
    if  not listconf.has_key("domain"): 
        domain="http://img.daconglaile.com/"
        listconf['domain']=domain
        picpath="uploads/dacong/"
        listconf['picpath']=picpath
    else:
        domain=listconf['domain']
        picpath=listconf['picpath']
    if not listconf.has_key("database"):
        database="dacong"
        listconf['database']=database
    else:
        database=listconf['database']
    if pagelist:
        pagelist=sorted(pagelist,reverse=True)
        for p in pagelist:
            purl=url.replace("(*)",str(p))
            if p==0:
                purl=url.replace("_(*)","")
            simpget_news(main_url,purl,typeid,typeid2,re_html,re_list,re_time,re_content,re_hand,re_contentpage=re_contentpage,re_encode=re_encode,re_contentpagenum=re_contentpagenum,re_contentpagestr=re_contentpagestr,keywords=keywords,re_keywords=re_keywords,domain=domain,picpath=picpath,database=database,listconf=listconf)
    else:
        purl=url
        simpget_news(main_url,purl,typeid,typeid2,re_html,re_list,re_time,re_content,re_hand,re_contentpage=re_contentpage,re_encode=re_encode,re_contentpagenum=re_contentpagenum,re_contentpagestr=re_contentpagestr,keywords=keywords,re_keywords=re_keywords,domain=domain,picpath=picpath,database=database,listconf=listconf)

def simpget_news(main_url,url,typeid,typeid2,re_html,re_list,re_time,re_content,re_hand,re_contentpage="",re_encode="",re_contentpagenum="",re_contentpagestr="",keywords="",re_keywords="",domain="",picpath="",database="",listconf=""):
    title=''
    contents='1'
    htmla=get_url_content(url,re_encode=re_encode)
    urls_pat=re.compile(re_html,re.DOTALL)
    htmla1=re.findall(urls_pat,htmla)
    html_a=''
    if htmla1:
        html_a=htmla1[0]
    else:
        if 're_html1' in listconf:
            if listconf['re_html1']:
                urls_pat=re.compile(listconf['re_html1'],re.DOTALL)
                htmla1=re.findall(urls_pat,htmla)
                if htmla1:
                    html_a=htmla1[0]
    #抓取下一页url
    if 'list_nextpage' in listconf:
        nexturlhtml=get_content(listconf['list_nextpage'],htmla)
        nexturl=get_a_url(nexturlhtml,main_url=main_url)
        print nexturl
        if not nexturl:
            return
    
    urls_pat=re.compile(re_list,re.DOTALL)
    alist=re.findall(urls_pat,html_a)
    newtime=''
    for als in alist:
        isweixin=listconf.has_key("weixin")
        if isweixin:
            title=als[1]
            als=als[0]
        else:
            newtimes=savetime
            title=get_inner_a(als)
            if title:
                title=filter_tags(title.replace(' ',''))
        if not title:
            continue
        if main_url not in als:
            if als[0:2]=="./":
                als=als.replace("./","")
            als=main_url+als
        if isweixin:
            a_url=als
        else:
            a_url=get_a_url(als,main_url=main_url)
        if not a_url:
            continue
        result=get_new(title)
        if result:
            print '已抓取'
            continue
        #url是否已经抓取
        zhuaquflag=iszhuaqu(a_url)
        if zhuaquflag:
            print '已抓取'
            continue
        
        htmls=get_url_content(a_url,re_encode=re_encode)
        contents=get_content(re_content,htmls)
        if listconf.has_key("re_title"):
            title=get_content(listconf['re_title'],htmls)
            if title:
                title=filter_tags(title)
            
        if title[0].encode("hex")=="f09f94b4":
            title=title[1:]
        
        if not contents:
            print '没有内容'
            if 're_content1' in listconf:
                contents=get_content(listconf['re_content1'],htmls)
                if not contents:
                    if 're_content2' in listconf:
                        contents=get_content(listconf['re_content2'],htmls)
                        if not contents:
                            print '没有内容'
                            continue
        if re_keywords:
            re_keywords=get_keywords(re_keywords,htmls)
        re_timelist=re_time
        re_time=''
        if listconf.has_key("re_time"):
            re_timelist=listconf['re_time']
            if re_timelist:
                re_time=get_content(re_timelist,htmls)
                if re_time:
                    re_time=re_time.replace("发布时间：", "")
                print re_time
            
        
        if re_contentpage:
            page_html=get_content(re_contentpage,htmls)
            if page_html:
                page_url=get_contentpagenum(a_url,page_html,re_contentpagenum=re_contentpagenum,re_contentpagestr=re_contentpagestr,main_url=main_url)
                if page_url:
                    m=2
                    for p in page_url:
                        a2=p
                        print a2
                        htmls2=get_url_content(a2,re_encode=re_encode)
                        content2=get_content(re_content,htmls2)
                        m=m+1
                        if content2:
                            contents=contents+content2
        if 're_remove' in listconf:
            if listconf['re_remove']:
                for rhtml in listconf['re_remove']:
                    contents=hand_content(rhtml,contents)
        if contents:
            contents=remove_script(contents)
            img_url=get_img_url(contents)
            if img_url:
                if listconf.has_key("localimgpath"):
                    localimgpath=listconf['localimgpath']
                else:
                    localimgpath=None
                contents=replace_img_sex(main_url,a_url,contents,domain=domain,picpath=picpath,localimgpath=localimgpath)
            contents=hand_contentimg(contents)
            
            if (database=="dacong"):
                savedbdacong(typeid,typeid2,main_url,a_url,title,contents,keywords=keywords,re_keywords=re_keywords,listconf=listconf,domain=domain,re_time=re_time)
    if nexturl:
        purl=nexturl
        simpget_news(main_url,purl,typeid,typeid2,re_html,re_list,re_time,re_content,re_hand,re_contentpage=re_contentpage,re_encode=re_encode,re_contentpagenum=re_contentpagenum,re_contentpagestr=re_contentpagestr,keywords=keywords,re_keywords=re_keywords,domain=domain,picpath=picpath,database=database,listconf=listconf)
def getonenews(typeid,typeid2,a_url,listconf):
    #url是否已经抓取
    zhuaquflag=iszhuaqu(a_url)
    #if zhuaquflag:
    #    return "已经抓取"
    if listconf.has_key("re_contentpage"):
        re_contentpage=listconf['re_contentpage']
    re_contentpagenum=listconf['re_contentpagenum']
    re_contentpagestr=listconf['re_contentpagestr']
    main_url=listconf['main_url']
    re_encode=listconf['re_encode']
    re_content=listconf['re_content']
    re_keywords=''
    if listconf.has_key("re_keywords"):
        re_keywords=listconf['re_keywords']
    keywords=''
    if listconf.has_key("keywords"):
        keywords=listconf['keywords']
    if  not listconf.has_key("domain"): 
        domain="http://img.daconglaile.com/"
        listconf['domain']=domain
        picpath="uploads/dacong/"
        listconf['picpath']=picpath
    else:
        domain=listconf['domain']
        picpath=listconf['picpath']
    
    htmls=get_url_content(a_url,re_encode=re_encode)
    contents=get_content(re_content,htmls)
    if listconf.has_key("re_title"):
        title=get_content(listconf['re_title'],htmls)
        if title:
            title=filter_tags(title)
        
        if title[0].encode("hex")=="f09f94b4":
            title=title[1:]
    
    if not contents:
        return '没有内容'
    re_keywords=get_keywords(re_keywords,htmls)
    re_time=''
    if listconf.has_key("re_time"):
        re_timelist=listconf['re_time']
        if re_timelist:
            re_time=get_content(re_timelist,htmls)
            if re_time:
                re_time=re_time.replace("发布时间：", "")
    
    if re_contentpage:
        page_html=get_content(re_contentpage,htmls)
        if page_html:
            page_url=get_contentpagenum(a_url,page_html,re_contentpagenum=re_contentpagenum,re_contentpagestr=re_contentpagestr,main_url=main_url)
            if page_url:
                m=2
                for p in page_url:
                    a2=p
                    htmls2=get_url_content(a2,re_encode=re_encode)
                    content2=get_content(re_content,htmls2)
                    m=m+1
                    if content2:
                        contents=contents+content2
                        
    if listconf.has_key("re_remove"):
        if listconf['re_remove']:
            for rhtml in listconf['re_remove']:
                contents=hand_content(rhtml,contents)
    if contents:
        contents=remove_script(contents)
        img_url=get_img_url(contents)
        if img_url:
            if listconf.has_key("localimgpath"):
                localimgpath=listconf['localimgpath']
            else:
                localimgpath=None
            contents=replace_img_sex(main_url,a_url,contents,domain=domain,picpath=picpath,localimgpath=localimgpath)
        contents=hand_contentimg(contents)
        #return contents
        return savedbdacong(typeid,typeid2,main_url,a_url,title,contents,keywords=keywords,re_keywords=re_keywords,listconf=listconf,domain=domain,re_time=re_time)
        
