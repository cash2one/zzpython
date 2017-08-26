#-*- coding:utf-8 -*-
def getYear(datestr):   
    return str(datestr)[0:4]
#获取当前月份 是一个字符串
def getMonth(datestr):
    return str(datestr)[5:7]
#获取当前天 是一个字符串  
def getDay(datestr):
    return str(datestr)[8:10]
def getTitleLen(title,titleLen):
    if title:
        return title[:titleLen]
    else:
        return ''
def get_img_url(html):#获得图片url
    if html and len(html)>20:
        re_py=r'<img.*?src="([^"]+)"'
        urls_pat=re.compile(re_py)
        img_url=re.findall(urls_pat,html)
        if img_url:
            return img_url
        re_py2=r'<IMG.*?src="([^"]+)"'
        urls_pat2=re.compile(re_py2)
        img_url2=re.findall(urls_pat2,html)
        if img_url2:
            return img_url2
        re_py3=r'<img.*?src=([^"]+)'
        urls_pat3=re.compile(re_py3)
        img_url3=re.findall(urls_pat3,html)
        if img_url3:
            return img_url3
        re_py3=r'<IMG.*?src=([^"]+)'
        urls_pat3=re.compile(re_py3)
        img_url3=re.findall(urls_pat3,html)
        if img_url3:
            return img_url3
def get_big_p(html):
    re_py2=r'<P.*?>'
    urls_pat2=re.compile(re_py2)
    big_p=re.findall(urls_pat2,html)
    if big_p:
        return big_p
def get_div_tag(html):
    div_tag1=re.findall(r'<div.*?>',html)
    if div_tag1 and len(div_tag1)>10:
        return div_tag1
    div_tag2=re.findall(r'<DIV.*?>',html)
    if div_tag2 and len(div_tag2)>10:
        return div_tag2
def get_p_tag(html):
    re_py1=r'<p.*?>'
    urls_pat1=re.compile(re_py1)
    p_tag=re.findall(urls_pat1,html)
    if p_tag and len(p_tag)>10:
        return p_tag
    re_py2=r'<P.*?>'
    urls_pat2=re.compile(re_py2)
    p_tag=re.findall(urls_pat2,html)
    if p_tag and len(p_tag)>10:
        return p_tag
def get_br_tag(html):
    re_py1=r'<br />'
    urls_pat1=re.compile(re_py1)
    br_tag=re.findall(urls_pat1,html)
    if br_tag and len(br_tag)>10:
        return br_tag
    re_py2=r'<BR />'
    urls_pat2=re.compile(re_py2)
    br_tag=re.findall(urls_pat2,html)
    if br_tag and len(br_tag)>10:
        return br_tag
def search_strong(search,title):
    search=search.replace(' ','')
    if re.findall('^[A-Z]+',search):
        title=re.sub(search,'<font color="red">'+search+'</font>',title)
        if '<font' not in title:
            losearch=search.lower()
            title=re.sub(losearch,'<font color="red">'+losearch+'</font>',title)
    elif re.findall('^[a-z]+',search):
        title=re.sub(search,'<font color="red">'+search+'</font>',title)
        if '<font' not in title:
            upsearch=search.upper()
            title=re.sub(upsearch,'<font color="red">'+upsearch+'</font>',title)
    else:
        searcht=split_str(search.decode('utf8'))
        title=title.decode('utf8')
        for s1 in searcht:
            title=title.replace(s1,u'<font color="red">'+s1+u'</font>')
    return title

def split_str(chinese):#传入的汉字分成一个一个的
    c=[]
    l=1
    len_c=range(0,len(chinese)/l)
    for lenn in len_c:
        ag=lenn*l
        ed=lenn*l+l
        c.append(chinese[ag:ed])
    return c 