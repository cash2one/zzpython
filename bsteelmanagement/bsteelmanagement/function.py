#-*- coding:utf-8 -*-
def getreplacetable(content):
    headcontent=content.split('<table')[0]
    midcontent=getpricetable(content)
    footcontent=content.split('</table>')[-1]
    contents=headcontent+midcontent+footcontent
    return contents

def get_content(re_py,html):
    urls_pat=re.compile(re_py,re.DOTALL)
    content=re.findall(urls_pat,html)
    for content in content:
        return content

def getpricetable(content):
    soup = BeautifulSoup(content)
    tablestr=""
    for table in soup.findAll('table'):
        tablestr+="<table border=1>"
        i=1
        for row in table.findAll('tr'):
            tablestr+="<tr>"
            j=1
            for tr in row.findAll('td'):
                textname=tr.encode("utf-8")
                colspan=get_content(r'colspan="([^"]+)"',textname)
                if colspan:
                    tdspan='<td colspan='+colspan+'>'
                else:
                    tdspan='<td>'
                textname=re.sub('<td.*?>',tdspan,textname)
#                print textname
#                tablestr+=tdspan2+textname+"</td>"
                tablestr+=textname
                j+=1
            i+=1
            tablestr+="</tr>"
        tablestr+="</table>"
    return tablestr

def timestamp_datetime(value):
    format = '%Y-%m-%d %H:%M:%S'
    value = time.localtime(value)
    dt = time.strftime(format, value)
    return dt
def getYesterday():
    today=datetime.date.today()   
    oneday=datetime.timedelta(days=1)   
    yesterday=today-oneday    
    return yesterday
def getToday():   
    return datetime.date.today()  
#----更新到数据库
def updateintodb(sql,argument):
    cursor.execute(sql,argument)
    conn.commit()
#----查询所有数据
def fetchalldb(sql,argument=''):
    if argument:
        cursor.execute(sql,argument)
    else:
        cursor.execute(sql)
    resultlist=cursor.fetchall()
    if resultlist:
        return resultlist
    else:
        return []
#----查询一条数据
def fetchonedb(sql,argument=""):
    if argument:
        cursor.execute(sql,argument)
    else:
        cursor.execute(sql)
    result=cursor.fetchone()
    if result:
        return result
#----查询一条总数
def fetchnumberdb(sql,argument=""):
    if argument:
        cursor.execute(sql,argument)
    else:
        cursor.execute(sql)
    result=cursor.fetchone()
    if result:
        return result[0]
    else:
        return 0
#----获得栏目列表
def gettypelist():
    sql='select id,name,sortrank from bsteel_arttype order by sortrank,id'
    resultlist=fetchalldb(sql)
    listall=[]
    if resultlist:
        for result in resultlist:
            list={'id':result[0],'name':result[1],'sortrank':result[2]}
            listall.append(list)
    return listall
def gettypedetail(id):
    sql='select id,name,sortrank from bsteel_arttype where id=%s'
    result=fetchonedb(sql,[id])
    list=[]
    if result:
        list={'id':result[0],'name':result[1],'sortrank':result[2]}
    return list
#----获得文章列表
def getarticallist(frompageCount,limitNum,isdelete='',typeid='',stitle='',sort='',begintime='',endtime=''):
    seartext=''
    argument=[]
    if typeid:
        seartext=seartext+' and typeid=%s'
        argument.append(typeid)
    if stitle:
        seartext=seartext+' and title like %s'
        argument.append("%"+stitle+"%")
    if isdelete:
        seartext=seartext+' and isdelete=%s'
        argument.append(isdelete)
    if begintime:
        seartext=seartext+' and gmt_created>=%s'
        argument.append(begintime)
    if endtime:
        seartext=seartext+' and gmt_created<=%s'
        argument.append(endtime)
    
    sql1='select count(0) from bsteel_artical where id>0'
    sql1=sql1+seartext
    count=fetchnumberdb(sql1,argument)
    
    sql='select id,title,content,gmt_created,typeid,click,editor,sortrank from bsteel_artical where id>0'
    sql=sql+seartext
    if sort=='1':
        sql=sql+' order by sortrank desc'
    elif sort=='2':
        sql=sql+' order by click desc'
    else:
        sql=sql+' order by id desc'
    sql=sql+' limit %s,%s'
    argument.append(frompageCount)
    argument.append(limitNum)
    resultlist=fetchalldb(sql,argument)
    listall=[]
    if resultlist:
        for result in resultlist:
            typeid=result[4]
            typedetail=gettypedetail(typeid)
            if typedetail:
                typename=typedetail['name']
            else:
                typename=''
            editor=result[6]
            if not editor:
                editor=''
            list={'id':result[0],'title':result[1],'content':result[2],'gmt_created':result[3].strftime('%Y-%m-%d'),'sortrank':result[7].strftime('%Y-%m-%d'),'typeid':typeid,'typename':typename,'click':result[5],'editor':editor}
            listall.append(list)
    return {'list':listall,'count':count}

def getarticaldetail(id):
    sql='select id,title,content,gmt_created,typeid,click,editor from bsteel_artical where id=%s'
    result=fetchonedb(sql,[id])
    list=[]
    if result:
        typeid=result[4]
        typedetail=gettypedetail(typeid)
        if typedetail:
            typename=typedetail['name']
        else:
            typename=''
        content=replacepic(result[2])
        list={'id':result[0],'title':result[1],'content':content,'gmt_created':result[3].strftime('%Y-%m-%d'),'typeid':typeid,'typename':typename,'click':result[5],'editor':result[6],'gmt_created1':result[3].strftime('%Y-%m-%d %H:%M:%S')}
    return list

def addclick(id):
    sql='update bsteel_artical set click=click+1 where id=%s'
    updateintodb(sql,[id])

#----最终页上一篇下一篇
def getarticalup(id):
    sql="select id,title from bsteel_artical where id>%s and isdelete=0 order by id limit 0,1"
    resultu = fetchonedb(sql,id)
    if resultu:
        list={'id':resultu[0],'title':resultu[1]}
        return list
def getarticalnx(id):
    sql="select id,title from bsteel_artical where id<%s and isdelete=0 order by id desc limit 0,1"
    resultn = fetchonedb(sql,id)
    if resultn:
        list={'id':resultn[0],'title':resultn[1]}
        return list

#------最新企业报价信息
def getcompanypricelist(kname="",limitcount="",titlelen=""):
    if (titlelen=="" or titlelen==None):
        titlelen=100
    port = settings.SPHINXCONFIG['port']
    cl = SphinxClient()
    cl.SetServer ( settings.SPHINXCONFIG['serverid'], port )
    cl.SetMatchMode ( SPH_MATCH_BOOLEAN )
    cl.SetSortMode( SPH_SORT_EXTENDED,"post_time desc" )
    cl.SetLimits (0,limitcount,limitcount)
    if (kname):
        res = cl.Query ('@title '+kname,'company_price')
    else:
        res = cl.Query ('','company_price')
    if res:
        if res.has_key('matches'):
            tagslist=res['matches']
            listall_baojia=[]
            for match in tagslist:
                id=match['id']
                attrs=match['attrs']
                title=subString(attrs['ptitle'],titlelen)
                title=title.replace("\\","-")
                gmt_time=attrs['ppost_time']
                min_price=attrs['min_price']
                max_price=attrs['max_price']
                price_unit=attrs['price_unit']
                list1={'title':title,'id':id,'gmt_time':gmt_time,'min_price':min_price,'max_price':max_price,'price_unit':price_unit,'fulltitle':attrs['ptitle'],'url':'http://price.zz91.com/companyprice/priceDetails'+str(id)+'.htm'}
                listall_baojia.append(list1)
            listcount_baojia=res['total_found']
            return listall_baojia
        
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
                newpicurl="http://pyapp.zz91.com/app/changepic.html?url="+url+"&width=700&height=700"
                htmlstr=htmlstr.replace(url,newpicurl)

    return htmlstr

def getloginstatus(usertoken):
    myusertoken=gettoken()
    if not myusertoken:
        return None
    if myusertoken!=usertoken:
        return None
    else:
        return 1
#获得app token
def gettoken():
    sql="select token from token where TIMESTAMPDIFF(HOUR,gmt_created,NOW())<=1 order by id desc"
    listd=fetchonedb(sql)
    if listd:
        return listd[0]
