#-*- coding:utf-8 -*-
import time,re
#imgpath='/var/www/zz91news/'
imgpath='/mnt/phpcode/zz91news/'
newspath='/mnt/var/log/newsprint/'
savetime=time.strftime('%m-%d',time.localtime(time.time()))
time3=time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
time2=time.strftime('%Y-%m-%d',time.localtime(time.time()))
time1=time.time()
def date_to_strall(dttime):
    return dttime.strftime('%Y-%m-%d %H:%M:%S')
def date_to_int(dttime):
    return str_to_int(date_to_strall(dttime))
def str_to_int(stringDate):
    if stringDate:
        stringDate=stringDate.strip()
        if not ':' in stringDate:
            stringDate=stringDate+' 00:00:00'
        else:
            rtime=stringDate.split(":")
            if len(rtime)<=2:
                stringDate=stringDate+":00"
        return int(time.mktime(time.strptime(stringDate,"%Y-%m-%d %H:%M:%S")))

def remove_script(html):#移除script
    if '<script' in html:
        re_py=r'<script.*?</script>'
        urls_pat=re.compile(re_py,re.DOTALL)
        img_url=re.findall(urls_pat,html)
        for img_url in img_url:
            html=html.replace(img_url,'')
    return html

def remove_content_a(html):#移除a链接
    html=re.sub('<A.*?>','',html)
    html=re.sub('</A>','',html)
    html=re.sub('<a.*?>','',html)
    html=re.sub('</a>','',html)
    return html
def getsimplecontent(htmlstr,main_url):
    #先过滤CDATA
    re_cdata=re.compile('//<!\[CDATA\[[^>]*//\]\]>',re.I) #匹配CDATA
    re_script=re.compile('<\s*script[^>]*>[^<]*<\s*/\s*script\s*>',re.I)#Script
    re_style=re.compile('<\s*style[^>]*>[^<]*<\s*/\s*style\s*>',re.I)#style
    #re_br=re.compile('<br\s*?/?>')#处理换行
    #re_h=re.compile('</?\w+[^>]*>')#HTML标签
    #re_comment=re.compile('<!--[^>]*-->')#HTML注释
    s=re_cdata.sub('',htmlstr)#去掉CDATA
    s=re_script.sub('',s) #去掉SCRIPT
    s=re_style.sub('',s)#去掉style
    #s=re_br.sub('\n',s)#将br转换为换行
    #s=re_h.sub('',s) #去掉HTML 标签
    #s=re_comment.sub('',s)#去掉HTML注释
    #去掉多余的空行
    #blank_line=re.compile('\n+')
    #s=blank_line.sub('\n',s)
    s=remove_content_a(s)
    s=replaceCharEntity(s)#替换实体
    s=s.replace(main_url,"")
    return s
#@param htmlstr HTML字符串.
def filter_tags(htmlstr):
    #先过滤CDATA
    re_cdata=re.compile('//<!\[CDATA\[[^>]*//\]\]>',re.I) #匹配CDATA
    re_script=re.compile('<\s*script[^>]*>[^<]*<\s*/\s*script\s*>',re.I)#Script
    re_style=re.compile('<\s*style[^>]*>[^<]*<\s*/\s*style\s*>',re.I)#style
    re_br=re.compile('<br\s*?/?>')#处理换行
    re_h=re.compile('</?\w+[^>]*>')#HTML标签
    re_comment=re.compile('<!--[^>]*-->')#HTML注释
    s=re_cdata.sub('',htmlstr)#去掉CDATA
    s=re_script.sub('',s) #去掉SCRIPT
    s=re_style.sub('',s)#去掉style
    s=re_br.sub('\n',s)#将br转换为换行
    s=re_h.sub('',s) #去掉HTML 标签
    s=re_comment.sub('',s)#去掉HTML注释
    #去掉多余的空行
    blank_line=re.compile('\n+')
    s=blank_line.sub('\n',s)
    s=replaceCharEntity(s)#替换实体
    return s
##替换常用HTML字符实体.
#使用正常的字符替换HTML中特殊的字符实体.
#你可以添加新的实体字符到CHAR_ENTITIES中,处理更多HTML字符实体.
#@param htmlstr HTML字符串.
def replaceCharEntity(htmlstr):
    CHAR_ENTITIES={'nbsp':' ','160':' ',
                'lt':'<','60':'<',
                'gt':'>','62':'>',
                'amp':'&','38':'&',
                'quot':'"','34':'"',}
   
    re_charEntity=re.compile(r'&#?(?P<name>\w+);')
    sz=re_charEntity.search(htmlstr)
    while sz:
        entity=sz.group()#entity全称，如&gt;
        key=sz.group('name')#去除&;后entity,如&gt;为gt
        try:
            htmlstr=re_charEntity.sub(CHAR_ENTITIES[key],htmlstr,1)
            sz=re_charEntity.search(htmlstr)
        except KeyError:
            #以空串代替
            htmlstr=re_charEntity.sub('',htmlstr,1)
            sz=re_charEntity.search(htmlstr)
    return htmlstr