#-*- coding:utf-8 -*- 
import urllib,urllib2,re,os,random,sys
from simptools import time1,time2,time3,newspath,imgpath
import bs4,requests
from bs4 import BeautifulSoup
reload(sys)
sys.setdefaultencoding('utf8')

def get_url_content(url,arg='',re_encode=''):#突破网站防爬
    hea = {'User-Agent':'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.118 Safari/537.36'}  
    print url
    if "https" in url:
        os.system("wget "+url+" -O test.html")
        if re_encode=="gbk":
            html=open('test.html').read().decode('GB18030','ignore').encode('utf-8')
        else:
            html=open('test.html').read()
    else:
        html = requests.get(url,headers = hea,auth=('user', 'pass'))  
        html.encoding = re_encode #这一行是将编码转为utf-8否则中文会显示乱码。  
        html=html.text
    if html:
        html=html.replace("data-original=","src=")
    return html

def get_content(re_py,html):
    if html:
        urls_pat=re.compile(re_py,re.DOTALL)
        content=re.findall(urls_pat,html)
        for content in content:
            return content
def get_contentpagenum(url,page_html,re_contentpagenum="",re_contentpagestr="",main_url=""):
    if page_html and re_contentpagenum:
        soup = BeautifulSoup(page_html)
        page_url=soup.findAll('a')
        pagelist=[]
        num=None
        if len(page_url)>0:
            
            for p in page_url:
                page=p.text
                if page.isdigit()==True:
                    purl=p.get("href")
                    if purl:
                        if main_url in purl:
                            pagelist.append(purl)
                        else:
                            #http://www.ys137.com/ydys/1127152.html
                            if purl[0:1]=="/":
                                pagelist.append(main_url+purl)
                            else:
                                plist=url.split("/")
                                lasturl=plist[len(plist)-1]
                                nurl=url.replace(lasturl,"")
                                pagelist.append(nurl+purl)
        
        return pagelist
                    
            #num=page_url[len(page_url)-re_contentpagenum].text
        try:
            if num:
                page_list=range(2,int(num)+1)
                return page_list
        except:
            return [1]
    if re_contentpagestr:
        num=get_content(re_contentpagestr,page_html)
        return num
        if num:
            page_list=range(2,int(num)+1)
            a_url=url
            pagelist=[]
            for m in page_list:
                if "shtml" in a_url:
                    a2=re.sub('.shtml','_'+str(m)+'.shtml',a_url)
                if ".shtm" in a_url:
                    a2=re.sub('.shtm','_'+str(m)+'.shtm',a_url)
                else:
                    a2=re.sub('.html','_'+str(m)+'.html',a_url)
                pagelist.append(a2)
            return pagelist
#取关键字
def get_keywords(keywords,htmls):
    if keywords:
        keywordslist=get_content(keywords,htmls)
        keywordslist=get_innerlist_a(keywordslist)
        print keywordslist
        return keywordslist
def hand_content(re_py,content):
    urls_pat=re.compile(re_py,re.DOTALL)
    e_content=re.findall(urls_pat,content)
    for e_content in e_content:
        content=content.replace(e_content,'')
    return content
def hand_contentimg(content):
    content=content.lower()
    content=content.replace("IMG",'img').replace("SRC",'src')
    re_py1='<img.*?src="([^"]+)"'
    re_py='<img.*?>'
    #content=content.lower()
    urls_pat=re.compile(re_py,re.DOTALL)
    img_urls=re.findall(urls_pat,content)
    
    urls_pat1=re.compile(re_py1,re.DOTALL)
    img_urls1=re.findall(urls_pat1,content)
    if not img_urls1:
        re_py1='<img.*?src=([^"]+) .*?>'
        urls_pat1=re.compile(re_py1,re.DOTALL)
        img_urls1=re.findall(urls_pat1,content)
    if not img_urls1:
        re_py1="<img.*?src='(.*?)'"
        urls_pat1=re.compile(re_py1,re.DOTALL)
        img_urls1=re.findall(urls_pat1,content)
        
    i=0
    
    if not img_urls1:
        urls_pat1=re.compile('<img.*?data-original="([^"]+)"',re.DOTALL)
        img_urls1=re.findall(urls_pat1,content)
    for img_url in img_urls:
        #print img_url
        if i<len(img_urls1):
            print img_urls1[i]
            content=content.replace(img_url,'<img src="'+img_urls1[i]+'"><br />')
        i=i+1
    return content

def hand_content2(re_py,content):
    urls_pat=re.compile(re_py,re.DOTALL)
    e_content=re.findall(urls_pat,content)
    for e_content in e_content:
        content=content.replace(e_content,'&nbsp;&nbsp;&nbsp;&nbsp;')
    return content

def get_img_name(img):#获得图片名
    img_name=img[-20:]
    img_name=img_name.replace('/','')
    img_name=img_name.replace('-','')
    return img_name

def get_img_url(html):#获得图片url
    #html=html.lower()
    if html:
        html=html.replace("data-original=","src=").replace("IMG",'img').replace("SRC",'src').replace("data-src","src")
        
        #soup = BeautifulSoup(html)
        #imglist=[]
        #for img_url in soup.findAll('img'):
            #imglist.append(img_url['src'])
        #return imglist
        
        re_py3=r'<img.*?src="(.*?)".*?>'
        urls_pat3=re.compile(re_py3)
        img_url3=re.findall(urls_pat3,html)
        if img_url3:
            return img_url3
        re_py3=r"<img.*?src='(.*?)'.*?>"
        urls_pat3=re.compile(re_py3)
        img_url3=re.findall(urls_pat3,html)
        if img_url3:
            return img_url3
        re_py3=r'<img.*?src=(.*?) .*?>'
        urls_pat3=re.compile(re_py3)
        img_url3=re.findall(urls_pat3,html)
        if img_url3:
            return img_url3
#微信
def get_weixin_url(html):
    re_py=r'<a.*?href="([^"]+)"'
    urls_pat=re.compile(re_py)
    arg_url=re.findall(urls_pat,html)
    if arg_url:
        if main_url in arg_url[0]:
            return arg_url[0]
        else:
            return main_url+arg_url[0]
def get_a_url(html,main_url=""):
    html=html.lower()
    re_py=r'<a.*?href="([^"]+)"'
    urls_pat=re.compile(re_py)
    arg_url=re.findall(urls_pat,html)
    re_py1=r'<A.*?href="([^"]+)"'
    urls_pat1=re.compile(re_py1)
    arg_url1=re.findall(urls_pat1,html)
    re_py2=r"<a.*?href='([^\"]+)'"
    urls_pat2=re.compile(re_py2)
    arg_url2=re.findall(urls_pat2,html)
    
    re_py3=r"<a.*?href=([^\"]+) target.*?"
    urls_pat3=re.compile(re_py3)
    arg_url3=re.findall(urls_pat3,html)
    if arg_url:
        if main_url in arg_url[0]:
            return arg_url[0]
        else:
            return main_url+arg_url[0]
    if arg_url1:
        if main_url in arg_url1[0]:
            return arg_url1[0]
        else:
            return main_url+arg_url1[0]
    if arg_url2:
        if main_url in arg_url2[0]:
            return arg_url2[0]
        else:
            return main_url+arg_url2[0]
    if arg_url3:
        if main_url in arg_url3[0]:
            return arg_url3[0]
        else:
            return main_url+arg_url3[0]
    
def get_inner_a(html):
    if html:
        html=html.lower()
        re_py=r'<a.*?>([^"]+)</a>'
        urls_pat=re.compile(re_py)
        arg_url=re.findall(urls_pat,html)
        if arg_url:
            return arg_url[0]
        else:
            re_py2=r'<a.*?>([^"]+)'
            urls_pat2=re.compile(re_py2)
            arg_url2=re.findall(urls_pat2,html)
            if arg_url2:
                return arg_url2[0]
def get_innerlist_a(html):
    if html:
        html=html.lower()
        re_py=r'<a.*?>([^"]+)</a>'
        urls_pat=re.compile(re_py)
        arg_url=re.findall(urls_pat,html)
        k=""
        if arg_url:
            for l in arg_url:
                k+=l+","
            if k:
                return k[:-1]
def get_title_url(html):
    html=html.lower()
    re_py=r'<a.*?title="([^"]+)"'
    urls_pat=re.compile(re_py)
    img_url=re.findall(urls_pat,html)
    re_py2=r'<a.*?title="([^"]+)"'
    urls_pat2=re.compile(re_py2)
    img_url2=re.findall(urls_pat2,html)
    if img_url:
        return img_url[0]
    if img_url2:
        return img_url2[0]
    
def replace_img_sex(main_url,url,html,domain="",picpath="",localimgpath=""):#替换图片url
    img_urls=get_img_url(html)
    cms_path2=picpath
    cms_path=picpath+time2+'/'
    if not localimgpath:
        localimgpath=imgpath
    path2=localimgpath+cms_path2
    path=localimgpath+cms_path
    
    new_path = os.path.join(path2,time2)
    if not os.path.isdir(new_path):
        os.makedirs(new_path)
    
    #soup = BeautifulSoup(html)
    #for img_url in soup.findAll('img'):
    for img_url in img_urls:
        #img_url=img_url['src']
        
        if main_url in img_url:
            img_url=img_url
            realimgurl=img_url
        else:
            realimgurl=img_url
            if "http://" in img_url or "https://" in img_url:
                img_url=img_url
            else:
                if img_url[0:2]=="//":
                    img_url="http:"+img_url
                else:
                    img_url=main_url+img_url
        imgtype=img_url.split('.')
        imgtypes=''
        
        if imgtype:
            imgtypes=imgtype[-1]
        if imgtypes:
            if len(imgtypes)<=4:
                img_name=str(random.randint(000000000,999999999))+'.'+imgtypes
            else:
                img_name=str(random.randint(000000000,999999999))+'.jpg'
        else:
            img_name=str(random.randint(000000000,999999999))+'.jpg'
        if "wx_fmt=" in img_url:
            img_name=str(random.randint(000000000,999999999))+'.'+img_url.split("wx_fmt=")[1].split("&")[0]
        print "开始抓取"+img_url
        file_name=os.path.join(path,img_name)
        print file_name
        try:
            os.system("wget -b "+img_url+" -O "+file_name+" -T 60")
            os.system("rm -rf wget-log*")
            """
            i_headers = {"User-Agent": "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9.1) Gecko/20090624 Firefox/3.5",\
                     "Referer": main_url}
            req = urllib2.Request(img_url, headers=i_headers)
            data=urllib2.urlopen(req).read()
            open(file_name, "wb").write(data)
            #urllib.urlretrieve(img_url,file_name)#图片下载
            """
        except:
            print "no img err"
            return ''
        txt="img download ok" + time3
        print txt
        img_path=domain+cms_path+img_name#本地图片路径
        html=html.encode('utf-8')
        html=html.replace(realimgurl,img_path)
#        if img_url and len(img_url)<200:
        #html=re.sub(img_url,img_path,html)#替换html的图片src为本地路径
    return html

def get_html_script(html):#移除script
    if '<script' in html:
        re_py=r'<script.*?</script>'
        urls_pat=re.compile(re_py,re.DOTALL)
        html_script=re.findall(urls_pat,html)
        return html_script

def get_html_a(html):
    if '<a' in html:
        re_py=r'<a.*?>'
        urls_pat=re.compile(re_py,re.DOTALL)
        html_a=re.findall(urls_pat,html)
        return html_a
   
def strcmp(s, t):
    if len(s) > len(t):
        s, t = t, s
    #第一步
    n = len(s)
    m = len(t)
    if not m : return n
    if not n : return m
    #第二步
    v0 = [ i for i in range(0, m+1) ]
    v1 = [ 0 ] * (m+1)
    #第三步
    cost = 0
    for i in range(1, n+1):
        v1[0] = i
        for j in range(1, m+1):
            #第四步,五步
            if s[i-1] == t[j-1]:
                cost = 0
            else:
                cost = 1
            #第六步
            a = v0[j] + 1
            b = v1[j-1] + 1
            c = v0[j-1] + cost
            v1[j] = min(a, b, c)
        v0 = v1[:]
    #第七步
    return v1[m]
def getsimilarity(s,t):
    count=float(strcmp(s,t))
    if len(s)<len(t):
        return ((len(t)-count)/len(t))*100
    else:
        return ((len(s)-count)/len(s))*100