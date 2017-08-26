#-*- coding:utf-8 -*-
def getnowurl(request):
    host=request.path_info
    qstring=request.META.get('QUERY_STRING','/')
    qstring=qstring.replace("&","^and^")
    return host+"?"+qstring
def formattime(value,flag):
    if value:
        if (flag==1):
            return value.strftime( '%-Y-%-m-%-d')
        if (flag==2):
            return value.strftime( '%-m-%-d %-H:%-M')
        if (flag==3):
            return value.strftime( '%Y-%-m-%d &nbsp;%-H:%M')
        else:
            return value.strftime( '%-Y-%-m-%-d %-H:%-M:%-S')
    else:
        return ''
def subString(string,length):   
    if length >= len(string):   
        return string   
    result = ''  
    i = 0  
    p = 0  
    while True:   
        ch = ord(string[i])   
        #1111110x   
        if ch >= 252:   
            p = p + 6  
        #111110xx   
        elif ch >= 248:   
            p = p + 5  
        #11110xxx   
        elif ch >= 240:   
            p = p + 4  
        #1110xxxx   
        elif ch >= 224:   
            p = p + 3  
        #110xxxxx   
        elif ch >= 192:
            p = p + 2  
        else:   
            p = p + 1       
        if p >= length:   
            break;
        else:   
            i = p   
    return string[0:i]
    pass
def remove_script(html):#移除script
    if '<script' in html:
        re_py=r'<script.*?</script>'
        urls_pat=re.compile(re_py,re.DOTALL)
        img_url=re.findall(urls_pat,html)
        for img_url in img_url:
            html=html.replace(img_url,'')
    return html
def remove_content_value(html):#移除a链接
    html=re.sub('<A.*?>','',html)
    html=re.sub('</A>','',html)
    html=re.sub('<a.*?>','',html)
    html=re.sub('</a>','',html)
    #html=re.sub('<table.*?>','',html)
    #html=re.sub('<tr.*?>','',html)
    #html=re.sub('<td.*?>','',html)
    #html=re.sub('</table>','',html)
    #html=re.sub('</tr>','',html)
    #html=re.sub('</td>','',html)
    html=re.sub('\r','',html)
    html=re.sub('\n','',html)
    html=re.sub('\t','',html)
    html=re.sub('<tbody.*?>','',html)
    html=re.sub('<tbody.*?>','',html)
    html=re.sub('<!--.*?-->','',html)
    #html=re.sub('<span.*?>','',html)
    #html=re.sub('</span>','',html)
    
    #html=re.sub('<wb.*?>','',html)
    #html=re.sub('</wb.*?>','',html)
    #html=re.sub('<iframe.*?>','',html)
    #html=re.sub('</iframe>','',html)
    
    #html=re.sub('<h.*?>','',html)
    #html=re.sub('</h.*?>','',html)
    #html=re.sub('<li.*?>','',html)
    #html=re.sub('</li>','<br />',html)
    #html=re.sub('<ul.*?>','',html)
    #html=re.sub('</ul>','',html)
    #html=re.sub('<ol.*?>','',html)
    #html=re.sub('</ol>','',html)
    
    #html=re.sub('<div.*?>','',html)
    #html=re.sub('<em*?>','',html)
    #html=re.sub('</em>','',html)
    #html=re.sub('</div>','<br />',html)
    
    #html=re.sub('align=".*?"','',html)
    html=re.sub('<pre.*?>','',html)
    html=re.sub('</pre>','',html)
    
    html=re.sub('<blockquote.*?>','<div style="background-color:#ebebeb;padding:10px">',html)
    html=re.sub('</blockquote>','',html)
    
    html=re.sub('STYLE=".*?"','',html)
    html=re.sub('style=".*?"','',html)
    html=re.sub('class=".*?"','',html)
    #html=re.sub('ALIGN=".*?"','',html)
    #html=re.sub('align=center','',html)
    html=re.sub('width=".*?"','',html)
    html=re.sub('height=".*?"','',html)
    html=re.sub('<input.*?>','',html)
    html=re.sub('<section.*?>','',html)
    html=re.sub('</section>','',html)
    
    
    
    return "<p>"+html+"</p>"
#图片替换
def replacepic(htmlstr):
    nowhtml=htmlstr
    for n in range(1,20):
        head = nowhtml.find('<img')
        tail=len(nowhtml)
        if head != -1:
            cut = nowhtml[head:tail]
            src = cut.find('http')
            cut2 = cut[src:tail]
            quo = cut2.find('"')
            url = cut2[0:quo]
            
            cc = nowhtml[head-4:tail]
            dd = cc.find('>')
            ee = cc[0:dd+1]
            
            if (url.find("13327300632836987")!=-1):
                htmlstr=htmlstr.replace(ee,"")
            nowhtml=cut2
            if (url!=''):
                
                #url=url.replace("http://img1.zz91.com/","")
                #url=url.replace("http://","")
                newpicurl="http://img3.zz91.com/300x15000/"+url+""
                newpicurl=newpicurl.replace("http://img1.zz91.com/","")
                #newpicurl=url
                #htmlstr=htmlstr
                htmlstr=htmlstr.replace(url,newpicurl)
                #htmlstr=htmlstr.replace(ee,"")
                #htmlstr=htmlstr.replace("http://img1.zz91.com/bbsPost/2012/3/26/13327300632836987.jpg","")
            #htmlstr=htmlstr.replace("style='margin: 0px; padding: 0px; width: 482px; height: 115px;'","")
    return htmlstr
#----发手机短信
def postsms(mobile,mid):
    sqlp="select TIMESTAMPDIFF(SECOND,gmt_created,now()) as ltime from mobile_code where mid=%s and DATEDIFF(CURDATE(),gmt_created)<1 order by gmt_created desc"
    plist=dbn.fetchalldb(sqlp,[mid]);
    pcount=len(plist)
    if (pcount<10):
        if plist:
            ltime=plist[0][0]
            if ltime<=60:
                return '验证码已经发送，一分钟内请不要重复提交！'
        tmp = random.randint(10000, 99999)
        #content="欢迎使用ZZ91再生网服务。验证码是："+str(tmp)+",输入验证码继续完成操作，该验证码10分钟内输入有效。"
        ##url="http://mt.10690404.com/send.do?Account=astokf&Password=C@4k@33lsbe2lw^6&Mobile="+str(mobile)+"&Content="+content+"&Exno=0"
        #f = urllib.urlopen(url)
        #html = f.read()
        #o = json.loads(html)
        sms_template_code="SMS_12520535"
        sms_free_sign_name="大葱来了"
        smscontent=r'验证是：(.*?)，请勿泄露'
        code=tmp
        sms_param={"code": str(code), "product": "解绑手机"}
        returnsms=postsms_dayu(mobile[0:11],sms_template_code,sms_free_sign_name,sms_param)
        
        gmt_created=datetime.datetime.now()
        sqlp="select id from mobile_code where  mid=%s order by id desc"
        plist=dbn.fetchonedb(sqlp,[mid]);
        if not plist:
            sql="insert into mobile_code(mid,code,gmt_created) values(%s,%s,%s)"
            dbn.updatetodb(sql,[mid,tmp,gmt_created]);
        else:
            sql="update mobile_code set code=%s,gmt_created=%s where id=%s"
            dbn.updatetodb(sql,[tmp,gmt_created,plist[0]]);
        return True
    else:
        return "您已经超过了每天发生5条短信的限制！"
#阿里大于短信系统
def postsms_dayu(mobile,sms_template_code,sms_free_sign_name,sms_param):
    req = top.api.AlibabaAliqinFcSmsNumSendRequest()
    req.set_app_info(top.appinfo("23410861", "72b4d7f51b757714b946d82ff9376a55"))
    req.sms_type = "normal"
    req.rec_num = mobile
    req.sms_template_code=sms_template_code
    req.sms_free_sign_name=sms_free_sign_name
    req.sms_param = json.dumps(sms_param,ensure_ascii=False,indent=2)
    try:
        resp= req.getResponse()
        if resp.get('alibaba_aliqin_fc_sms_num_send_response').get('result').get('success')==True:
            return True
        else:
            return False
    except Exception,e:
        return False
#阿里大于短信系统
def postsms_dayu(mobile,sms_template_code,sms_free_sign_name,sms_param):
    req = top.api.AlibabaAliqinFcSmsNumSendRequest()
    req.set_app_info(top.appinfo("23576151", "f50e7a6988c243508be85db501128ae5"))
    req.sms_type = "normal"
    req.rec_num = mobile
    req.sms_template_code=sms_template_code
    req.sms_free_sign_name=sms_free_sign_name
    req.sms_param = json.dumps(sms_param,ensure_ascii=False,indent=2)
    try:
        resp= req.getResponse()
        if resp.get('alibaba_aliqin_fc_sms_num_send_response').get('result').get('success')==True:
            return True
        else:
            return False
    except Exception,e:
        return False
#腾讯视频宽度替换
def qqvadio(html):
    
    reg = r'<iframe.*?></iframe>' 
    qqre = re.compile(reg)  
    qqlist1 = qqre.findall(html)
   
    reg = r'<iframe.*?src=.*?vid=(.+?)&.*?</iframe>' 
    qqre = re.compile(reg)  
    qqlist2 = qqre.findall(html)
    if not qqlist2:
        reg = r'<iframe.*?src=.*?vid=(.+?)".*?</iframe>' 
        qqre = re.compile(reg)  
        qqlist2 = qqre.findall(html)
    i=0
    for ql1 in qqlist1:
        if qqlist2:
            ql2=qqlist2[i]
            ql2=re.sub('width=.*?&','',ql2)
            ql2=re.sub('height=.*?&','',ql2)
            #ql2=ql2.replace("https://","http://")
            #http://static.video.qq.com/TencentPlayer.swf?vid=n0345cwyyj9
            #http://v.qq.com/iframe/player.html?vid=
            #http://cache.tv.qq.com/qqplayerout.swf?vid=
            vadiostr='<video controls="controls" autoplay="autoplay" preload="auto" poster="screen.jpg" onplay="true" width="100%" height="100%" id="vodioplay">'
            vadiostr+='  <source src="http://cache.tv.qq.com/qqplayerout.swf?vid='+ql2+'"></source>'
            vadiostr+='</video>'
            #vadiostr='<embed src="http://static.video.qq.com/TencentPlayer.swf?vid='+ql2+'&auto=1&outhost=http://cf.qq.com/" allowFullScreen="true" quality="high" align="middle" type="application/x-shockwave-flash" width="100%" height="100%" />'
            #html=html.replace(ql1,vadiostr)
            html=html.replace(ql1,"<iframe src='http://v.qq.com/iframe/player.html?vid="+ql2+"'  frameborder='0'  style='background-color:#000000;' scrolling=no allowtransparency='true'>视频加载中...</iframe>")
            
        i+=1
    return html
    
#图片替换
def replacepic1(htmlstr):
    nowhtml=htmlstr
    reg = r'src="(.+?)"' 
    imgre = re.compile(reg)  
    imglist = imgre.findall(htmlstr)  
    x = 0  
    for imgurl in imglist: 
        if "http://" in imgurl:
            imgurl=imgurl
        else:
            imgurl="http://app.zz91.com"+imgurl
        newpicurl="http://pyapp.zz91.com/app/changepic.html?url="+imgurl+"&width=300&height=300"
        htmlstr=htmlstr.replace(imgurl,newpicurl)
        x = x + 1
    re_cdata=re.compile('//<!\[CDATA\[[^>]*//\]\]>',re.I) #匹配CDATA
    re_script=re.compile('<\s*script[^>]*>[^<]*<\s*/\s*script\s*>',re.I)#Script
    re_style=re.compile('<\s*style[^>]*>[^<]*<\s*/\s*style\s*>',re.I)#style
    #re_a=re.compile('<\s*a[^>]*>[^<]*<\s*/\s*a\s*>',re.I)#a
    re_style1=re.compile(r'style="(.+?)"')
    #re_h=re.compile('</?\w+[^>]*>')#HTML标签
    s=re_cdata.sub('',htmlstr)#去掉CDATA
    s=re_script.sub('',s) #去掉SCRIPT
    s=re_style.sub('',s)#去掉style
    s=re_style1.sub('',s)#去掉style
    #s=re_h.sub('',s) #去掉HTML 标签
    #s=re_a.sub('',s) #去掉a 标签
    #s=replaceCharEntity(s)#替换实体
    htmlstr=s
    
    return htmlstr

def getIPFromDJangoRequest(request):
    if 'HTTP_X_FORWARDED_FOR' in request.META:
        return request.META.get('HTTP_X_FORWARDED_FOR')
    else:
        return request.META.get('REMOTE_ADDR')

#昨天
def getYesterday():   
    today=datetime.date.today()   
    oneday=datetime.timedelta(days=1)   
    yesterday=today-oneday    
    return yesterday  

#今天     
def getToday():   
    return datetime.date.today()     
 
#获取给定参数的前几天的日期，返回一个list   
def getDaysByNum(num):   
    today=datetime.date.today()   
    oneday=datetime.timedelta(days=1)       
    li=[]        
    for i in range(0,num):   
        #今天减一天，一天一天减   
        today=today-oneday   
        #把日期转换成字符串   
        #result=datetostr(today)   
        li.append(datetostr(today))   
    return li   

def timestamp_datetime(value):
    format = '%Y-%m-%d %H:%M:%S'
    # value为传入的值为时间戳(整形)，如：1332888820
    value = time.localtime(value)
    ## 经过localtime转换后变成
    ## time.struct_time(tm_year=2012, tm_mon=3, tm_mday=28, tm_hour=6, tm_min=53, tm_sec=40, tm_wday=2, tm_yday=88, tm_isdst=0)
    # 最后再经过strftime函数转换为正常日期格式。
    dt = time.strftime(format, value)
    return dt
def datetime_timestamp(dt):
     #dt为字符串
     #中间过程，一般都需要将字符串转化为时间数组
     #time.strptime(dt, '%Y-%m-%d %H:%M:%S')
     ## time.struct_time(tm_year=2012, tm_mon=3, tm_mday=28, tm_hour=6, tm_min=53, tm_sec=40, tm_wday=2, tm_yday=88, tm_isdst=-1)
     #将"2012-03-28 06:53:40"转化为时间戳
     s = time.mktime(time.strptime(dt, '%Y-%m-%d %H:%M:%S'))
     return int(s)
#将字符串转换成datetime类型  
def strtodatetime(datestr,format):       
    return datetime.datetime.strptime(datestr,format)   
 
#时间转换成字符串,格式为2008-08-02   
def datetostr(date):     
    return   str(date)[0:10]   
 
#两个日期相隔多少天，例：2008-10-03和2008-10-01是相隔两天  
def datediff(beginDate,endDate):   
    format="%Y-%m-%d";
    bd=strtodatetime(beginDate,format)   
    ed=strtodatetime(endDate,format)       
    oneday=datetime.timedelta(days=1)   
    count=0 
    while bd!=ed:   
        ed=ed-oneday   
        count+=1 
    return count   

 
 
#获取两个时间段的所有时间,返回list  
def getDays(beginDate,endDate):   
    format="%Y-%m-%d";   
    bd=strtodatetime(beginDate,format)   
    ed=strtodatetime(endDate,format)   
    oneday=datetime.timedelta(days=1)    
    num=datediff(beginDate,endDate)+1    
    li=[]   
    for i in range(0,num):    
        li.append(datetostr(ed))   
        ed=ed-oneday   
    return li   


#获取当前年份 是一个字符串  
def getYear(datestr=""):
    if not datestr: 
        return str(datetime.date.today())[0:4]
    else:
        return str(datestr)[0:4]
 
#获取当前月份 是一个字符串  
def getMonth(datestr=""):
    if not datestr:  
        return str(datetime.date.today())[5:7]
    else:
        return str(datestr)[5:7]  
 
#获取当前天 是一个字符串  
def getDay(datestr=""):
    if not datestr:
        return str(datetime.date.today())[8:10]
    else:
        return str(datestr)[8:10]    

def getNow():   
    return datetime.datetime.now()

def getdatelist():
    nyear=getYear()
    nmonth=getMonth()
    yearlist=[]
    monthlist=[]
    for i in range(1,int(nmonth)+1):
        monthlist.append(i)
    for i in range(int(nyear),2004,-1):
        if (i!=int(nyear)):
            monthl=[1,2,3,4,5,6,7,8,9,10,11,12]
        else:
            monthl=monthlist
        list={'year':i,'month':monthl}
        yearlist.append(list)
    return yearlist

#获得远程图片宽和高
def getpicturewh(url):
    #url = 'http://img1.zz91.com/ads/1377964800000/f53cb9e8-8fc5-4bf1-ae3b-468f5f814da0.gif'
    file = urllib.urlopen(url)
    tmpIm = StringIO.StringIO(file.read())
    im = Image.open(tmpIm)
    isize={'width':im.size[0],'height':im.size[1]}
    return isize
#加密
def getjiami(strword):
    if strword:
        return strword.encode('utf8','ignore').encode("hex")
    else:
        return ''
def getjiemi(strword):
    if strword:
        return strword.decode("hex").decode('utf8','ignore')
    else:
        return ''
#判断是否为HEX码
def gethextype(keywords):
    zwtype=0
    zwflag=0
    strvalue="abcdef0123456789"
    if keywords:
        for a in keywords:
            if (a >= u'\u4e00' and a<=u'\u9fa5'):
                zwflag=zwflag+1
        if zwflag>0:
            zwtype=1
        zwflag=0
        if zwtype==0:
            for a in keywords:
                if (strvalue.find(a)==-1):
                    zwflag=zwflag+1
            if zwflag>0:
                zwtype=1
        if zwtype==1:
            return False
        else:
            return True
    else:
        return False
#关键字加亮  搜索引擎
def getlightkeywords(cl,docs,words,index):
    opts = {'before_match':'<font color=red>', 'after_match':'</font>', 'chunk_separator':' ... ', 'limit':400, 'around':15}
    tagscrl = cl.BuildExcerpts(docs, index, words, opts)
    if tagscrl:
        return tagscrl[0]
    else:
        return docs
def validateEmail(email):
    if len(email) > 5:
        if re.match("^.+\\@(\\[?)[a-zA-Z0-9\\-\\.]+\\.([a-zA-Z]{2,3}|[0-9]{1,3})(\\]?)$", email) != None:
           return 1
    return 0


#
#获得app token
def gettoken(mid):
    sql="select token from member_appinfo where mid=%s and TIMESTAMPDIFF(HOUR,gmt_modified,NOW())<=2"
    listd=dbn.fetchonedb(sql,[mid])
    if listd:
        return listd[0]
#
def getloginstatus(mid,usertoken):
    if not mid or str(mid)=="0" or not usertoken:
        return None
    else:
        myusertoken=gettoken(mid)
        if not myusertoken:
            return None
        if myusertoken!=usertoken:
            return None
    return 1
##过滤HTML中的标签
#将HTML中标签等信息去掉
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
    s=s.replace(" ","")
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

def get_content(re_py,html):
    if html:
        urls_pat=re.compile(re_py,re.DOTALL)
        content=re.findall(urls_pat,html)
        for content in content:
            return content
