#-*- coding:utf-8 -*-
def formattime(value,flag):
    if value:
        if (flag==1):
            return value.strftime( '%Y-%m-%d')
        else:
            return value.strftime( '%Y-%m-%d %H:%M:%S')
    else:
        return ''
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
def inserintodb(sql,argument):
    cursor.execute(sql,argument)
    conn.commit()

#----查询所有数据
def fetchalldb(sql):
    cursor.execute(sql)
    resultlist=cursor.fetchall()
    if resultlist:
        return resultlist
    else:
        return []
        
#----查询一条数据
def fetchonedb(sql,argument=''):
    if argument:
        cursor.execute(sql,argument)
    else:
        cursor.execute(sql)
    result=cursor.fetchone()
    if result:
        return result
#----查询一条总数
def fetchnumberdb(sql):
    cursor.execute(sql)
    result=cursor.fetchone()
    if result:
        return result[0]
    else:
        return 0

#----关键字列表
def get_keywords(frompageCount,limitNum,chargetype='',keywords_type='',sortrank='',keywords='',seouser_id='',shopsaddress='',begintime='',begintime2='',company_name='',mail='',mobile='',sales_id=''):
    listall=[]
    count=0
    sql1='select count(a.id),count(distinct b.id) from seo_keywords as a,seo_company as b where a.company_id=b.id and a.isdelete=0 and b.isdelete=0'
    if company_name:
        sql1=sql1+' and b.name like"%'+company_name+'%"'
        seouser_id=''
    if mail:
        sql1=sql1+' and b.mail="'+mail+'"'
        seouser_id=''
    if mobile:
        sql1=sql1+' and b.mobile="'+mobile+'"'
        seouser_id=''
    if keywords:
        sql1=sql1+' and a.keywords like"%'+keywords+'%"'
        seouser_id=''
    if shopsaddress:
        sql1=sql1+' and a.shopsaddress="'+shopsaddress+'"'
        seouser_id=''
    if seouser_id:
        sql1=sql1+' and a.seouser_id='+seouser_id
    if sales_id:
        sql1=sql1+' and a.salesman_id='+sales_id
    if begintime:
        sql1=sql1+' and a.begintime>="'+begintime+'"'
    if begintime2:
        sql1=sql1+' and a.begintime<="'+begintime2+'"'
    if chargetype:
        sql1=sql1+' and a.chargetype='+chargetype
    if keywords_type=='2':
        sql1=sql1+' and a.isstandard=1 and a.islost=0'
    if keywords_type=='3':
        sql1=sql1+' and a.isstandard=0 and a.islost=0'
    if keywords_type=='4':
        sql1=sql1+' and a.chargetype=1 and a.expire_time<(select CURRENT_DATE) and a.expire_time>0'
    if keywords_type=='6':
        sql1=sql1+' and a.chargetype=2 and a.balance<0'
    if keywords_type=='5':
        sql1=sql1.replace('a.isdelete=0','a.isdelete=1')
    if keywords_type=='7':
        sql1=sql1+' and a.islost=1'
    if keywords_type=='8':
        sql1=sql1+' and a.islost=0'
    result1=fetchonedb(sql1)
    count=0
    count1=0
    if result1:
        count=result1[0]
        count1=result1[1]
    sql='select a.id,a.company_id,a.baidu_ranking,a.keywords,a.begintime,a.standardtime,a.shopsaddress,a.chargetype,a.price,a.years,a.unit_price,a.seouser_id,a.standarddemand,a.expire_time,a.balance,a.salesman_id,b.name,b.mail from seo_keywords as a,seo_company as b where a.company_id=b.id and a.isdelete=0 and b.isdelete=0'
    if company_name:
        sql=sql+' and b.name like"%'+company_name+'%"'
    if mail:
        sql=sql+' and b.mail="'+mail+'"'
    if mobile:
        sql=sql+' and b.mobile="'+mobile+'"'
    if keywords:
        sql=sql+' and a.keywords like"%'+keywords+'%"'
    if seouser_id:
        sql=sql+' and a.seouser_id='+seouser_id
    if sales_id:
        sql=sql+' and a.salesman_id='+sales_id
    if shopsaddress:
        sql=sql+' and a.shopsaddress="'+shopsaddress+'"'
    if begintime:
        sql=sql+' and a.begintime>="'+begintime+'"'
    if begintime2:
        sql=sql+' and a.begintime<="'+begintime2+'"'
    if chargetype:
        sql=sql+' and a.chargetype='+chargetype
    if keywords_type=='2':
#        sql=sql+' and a.isstandard=1 and (a.balance is null or a.balance>=0) and (a.expire_time>=(select CURRENT_DATE) or a.expire_time is null)'
        sql=sql+' and a.isstandard=1 and a.islost=0'
    if keywords_type=='3':
        sql=sql+' and a.isstandard=0 and a.islost=0'
    if keywords_type=='4':
        sql=sql+' and a.chargetype=1 and a.expire_time<(select CURRENT_DATE) and a.expire_time>0'
    if keywords_type=='6':
        sql=sql+' and a.chargetype=2 and a.balance<0'
    if keywords_type=='5':
        sql=sql.replace('a.isdelete=0','a.isdelete=1')
    if keywords_type=='7':
        sql=sql+' and a.islost=1'
    if keywords_type=='8':
        sql=sql+' and a.islost=0'
    if sortrank=='1':
        sql=sql+' order by a.begintime'
    elif sortrank=='7':
        sql=sql+' order by a.begintime desc'
    elif sortrank=='2':
        sql=sql+' order by a.expire_time'
    elif sortrank=='9':
        sql=sql+' order by a.expire_time desc'
    elif sortrank=='4':
        sql=sql+' order by a.standardtime'
    elif sortrank=='8':
        sql=sql+' order by a.standardtime desc'
    elif sortrank=='3':
        sql=sql+' order by a.balance'
    elif sortrank=='6':
        sql=sql+' order by a.balance desc'
    elif sortrank=='10':
        sql=sql+' order by a.price'
    elif sortrank=='11':
        sql=sql+' order by a.price desc'
    else:
        sql=sql+' order by b.name'
    sql=sql+' limit '+str(frompageCount)+','+str(limitNum)
    resultlist=fetchalldb(sql)
    if resultlist:
        for result in resultlist:
            begintime=result[4]
            if begintime:
                begintime=begintime.strftime('%Y-%m-%d')
            standardtime=result[5]
            if standardtime:
                standardtime=standardtime.strftime('%Y-%m-%d')
            else:
                standardtime=''
            expire_time=result[13]
            if expire_time:
                expire_time=expire_time.strftime('%Y-%m-%d')
            else:
                expire_time=''
            seouser_name=getseoname(result[11])
            balance=result[14]
            salesman_name=getseoname(result[15])
            if not salesman_name:
                salesman_name=''
            if balance:
                balance=str(balance)+'元'
            else:
                balance=''
            list={
                'id':result[0],
                'company_name':result[16],
                'company_mail':result[17],
                'mail':result[17],
                'baidu_ranking':result[2],
                'keywords':result[3],
                'begintime':begintime,
                'standardtime':standardtime,
                'shopsaddress':result[6],
                'chargetype':result[7],
                'price':result[8],
                'years':result[9],
                'unit_price':result[10],
                'seouser_name':seouser_name,
                'salesman_name':salesman_name,
                'standarddemand':result[12],
                'expire_time':expire_time,
                'balance':balance,
                }
            listall.append(list)
    return {'list':listall,'count':count,'count1':count1}

#----公司列表
def get_company(frompageCount,limitNum,chargetype='',company_type='',company_name='',mobile='',mail='',contact='',seouser_id='',salesman_id=''):
    listall=[]
    count=0
    sql1='select distinct count(distinct a.id) from seo_company as a,seo_keywords as b where a.id=b.company_id and a.isdelete=0 and b.isdelete=0'
    if company_name:
        sql1=sql1+' and a.name like "%'+company_name+'%"'
        seouser_id=''
    if mobile:
        sql1=sql1+' and mobile="'+mobile+'"'
        seouser_id=''
    if mail:
        sql1=sql1+' and mail="'+mail+'"'
        seouser_id=''
    if contact:
        sql1=sql1+' and contact="'+contact+'"'
        seouser_id=''
    if company_type=='2':
        sql1=sql1+' and a.islost=0'
    if company_type=='5':
        sql1=sql1+' and a.islost=1'
    if company_type=='7':
        sql1=sql1.replace('a.isdelete=0','a.isdelete=1')
    if company_type=='4':
        sql1=sql1+' and b.chargetype=1 and b.expire_time<(select CURRENT_DATE) and b.expire_time>0'
    if company_type=='6':
        sql1=sql1+' and b.chargetype=2 and b.balance<0'
    if chargetype:
        sql1=sql1+' and b.chargetype='+chargetype
    if seouser_id:
        sql1=sql1+' and b.seouser_id='+seouser_id
    if salesman_id:
        sql1=sql1+' and b.salesman_id='+salesman_id
    count=fetchnumberdb(sql1)
    sql='select distinct a.id,a.name,a.mobile,a.mail,a.contact from seo_company as a,seo_keywords as b where a.id=b.company_id and a.isdelete=0 and b.isdelete=0'
    if company_name:
        sql=sql+' and a.name like "%'+company_name+'%"'
        seouser_id=''
    if mobile:
        sql=sql+' and a.mobile="'+mobile+'"'
        seouser_id=''
    if mail:
        sql=sql+' and a.mail="'+mail+'"'
        seouser_id=''
    if contact:
        sql=sql+' and a.contact="'+contact+'"'
        seouser_id=''
    if company_type=='2':
        sql=sql+' and a.islost=0'
    if company_type=='5':
        sql=sql+' and a.islost=1'
    if company_type=='7':
        sql=sql.replace('a.isdelete=0','a.isdelete=1')
    if company_type=='4':
        sql=sql+' and b.chargetype=1 and b.expire_time<(select CURRENT_DATE) and b.expire_time>0'
    if company_type=='6':
        sql=sql+' and b.chargetype=2 and b.balance<0'
    if chargetype:
        sql=sql+' and b.chargetype='+chargetype
    if seouser_id:
        sql=sql+' and b.seouser_id='+seouser_id
    if salesman_id:
        sql=sql+' and b.salesman_id='+salesman_id
    sql=sql+' order by id desc limit '+str(frompageCount)+','+str(limitNum)
    resultlist=fetchalldb(sql)
    if resultlist:
        for result in resultlist:
            id=result[0]
            comp_keywords=getcomp_keywords(id)
            list={'id':id,'name':result[1],'mobile':result[2],'mail':result[3],'contact':result[4],'comp_keywords':comp_keywords}
            listall.append(list)
    return {'list':listall,'count':count}

#----获得销售人员列表
def get_salesuser():
    sql='select id,name,username,password from seo_user where type=2'
    cursor.execute(sql)
    resultlist=cursor.fetchall()
    listall=[]
    if resultlist:
        for result in resultlist:
            list={'id':result[0],'name':result[1],'username':result[2],'password':result[3]}
            listall.append(list)
    return listall
#----根据关键词id获得公司id
#----获得seo优化人员列表
def get_seouser():
    sql='select SQL_NO_CACHE id,name,username,password from seo_user where type=1 limit 0,10'
    cursor.execute(sql)
    resultlist=cursor.fetchall()
    listall=[]
    if resultlist:
        for result in resultlist:
            list={'id':result[0],'name':result[1],'username':result[2],'password':result[3]}
            listall.append(list)
    return listall
#----根据关键词id获得公司id
def getcompany_id(id):
    sql='select company_id from seo_keywords where id=%s'
    cursor.execute(sql,[id])
    result=cursor.fetchone()
    if result:
        return result[0]
#----获得公司名
def getcompany_name(id):
    sql='select name from seo_company where id=%s'
    cursor.execute(sql,[id])
    result=cursor.fetchone()
    if result:
        return result[0]
#----获得关键字名
def getkeywords_name(id):
    sql='select keywords from seo_keywords where id=%s'
    cursor.execute(sql,[id])
    result=cursor.fetchone()
    if result:
        return result[0]

#----根据公司id获得关键词
def getcomp_keywords(id):
    listall=[]
    sql='select id,keywords from seo_keywords where isdelete=0 and company_id='+str(id)
    resultlist=fetchalldb(sql)
    if resultlist:
        for result in resultlist:
            list={'id':result[0],'keywords':result[1]}
            listall.append(list)
    return listall
#----获得公司详细信息
def getcompany_detail(id):
    sql='select id,name,mobile,mail,contact from seo_company where id=%s'
    cursor.execute(sql,[id])
    result=cursor.fetchone()
    if result:
        id=result[0]
        comp_keywords=getcomp_keywords(id)
        list={'id':id,'name':result[1],'mobile':result[2],'mail':result[3],'contact':result[4],'comp_keywords':comp_keywords}
        return list
#----获得关键字详细信息
def getkeywords_detail(id):
    sql='select id,keywords,begintime,standardtime,standarddemand,shopsaddress,chargetype,price,years,unit_price,seouser_id,baidu_ranking,company_id,expire_time,isstandard from seo_keywords where id=%s'
    cursor.execute(sql,[id])
    result=cursor.fetchone()
    list=[]
    if result:
        standardtime=result[3]
        if standardtime:
            standardtime=standardtime.strftime('%Y-%m-%d')
        else:
            standardtime=''
        seouser_id=result[10]
        seouser_name=getseoname(seouser_id)
        company_id=result[12]
        company_name=getcompany_name(company_id)
        expire_time=result[13]
        if expire_time:
            expire_time=expire_time.strftime('%Y-%m-%d')
        else:
            expire_time=''
        balance=''
        list={
              'id':result[0],
              'keywords':result[1],
              'begintime':result[2].strftime('%Y-%m-%d'),
              'standardtime':standardtime,
              'standarddemand':result[4],
              'shopsaddress':result[5],
              'chargetype':result[6],
              'price':result[7],
              'years':result[8],
              'unit_price':result[9],
              'seouser_id':seouser_id,
              'seouser_name':seouser_name,
              'baidu_ranking':result[11],
              'company_name':company_name,
              'expire_time':expire_time,
              'isstandard':result[14],
              }
    return list

#----获得seo优化人员姓名
def getseoname(id):
    sql='select name from seo_user where id=%s'
    cursor.execute(sql,[id])
    result=cursor.fetchone()
    if result:
        return result[0]
#----获得seo优化人员姓名
def getseo_password(id):
    sql='select password from seo_user where id=%s'
    cursor.execute(sql,[id])
    result=cursor.fetchone()
    if result:
        return result[0]
#----获得一条seo人员详情
def getseodetail(id):
    sql='select name,username,password from seo_user where id=%s'
    result=fetchonedb(sql,[id])
    list=[]
    if result:
        list={'name':result[0],'username':result[1],'password':result[2]}
    return list
#----获得备注信息根据id
def getremarks(id):
    sql='select id,company_id,remarks,seouser_id,gmt_created,keywords_id from seo_remarks where id='+id
    cursor.execute(sql)
    result=cursor.fetchone()
    list=[]
    if result:
        id=result[0]
        company_id=result[1]
        keywords_id=result[5]
        keywords_name=getkeywords_name(keywords_id)
        company_name=getcompany_name(company_id)
        seouser_id=result[3]
        seouser_name=getseoname(seouser_id)
        list={'id':id,'keywords_id':keywords_id,'keywords_name':keywords_name,'company_name':company_name,'remarks':result[2],'seouser_name':seouser_name,'gmt_created':result[4].strftime('%Y-%m-%d')}
    return list
#----获得备注信息
def getremarkslist(keywords_id):
    sql='select id,company_id,remarks,seouser_id,gmt_created from seo_remarks where keywords_id='+keywords_id
    cursor.execute(sql)
    resultlist=cursor.fetchall()
    listall=[]
    if resultlist:
        for result in resultlist:
            id=result[0]
            company_id=result[1]
            keywords_name=getkeywords_name(keywords_id)
            company_name=getcompany_name(company_id)
            seouser_id=result[3]
            seouser_name=getseoname(seouser_id)
            list={'id':id,'keywords_name':keywords_name,'company_name':company_name,'remarks':result[2],'seouser_name':seouser_name,'gmt_created':result[4].strftime('%Y-%m-%d')}
            listall.append(list)
    return listall


def get_url_content2(url):#突破网站防爬
    i_headers = {"User-Agent": "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9.1) Gecko/20090624 Firefox/3.5",\
                 "Referer": 'http://www.baidu.com'}
    req = urllib2.Request(url, headers=i_headers)
    html=urllib2.urlopen(req).geturl()
    return html
def get_url_content(url):#突破网站防爬
    i_headers = {"User-Agent": "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9.1) Gecko/20090624 Firefox/3.5",\
                 "Referer": 'http://www.baidu.com'}
    req = urllib2.Request(url, headers=i_headers)
    html=urllib2.urlopen(req).read()
    return html

def get_content(re_py,html):
    urls_pat=re.compile(re_py,re.DOTALL)
    content=re.findall(urls_pat,html)
    return content

def getbaidu_ranking(keywords,shopaddress,standarddemand):
    re_py=r'http://www.baidu.com/link\?url=.*?"'
    baidu_url='http://www.baidu.com/s?rn='+str(standarddemand*11)+'&q1='+keywords
    html2=get_url_content(baidu_url)
    html2=html2.replace('<b>','')
    html2=html2.replace('</b>','')
    html4=html2.split('<h3 class="t">')
    numb=-1
    for h2 in html4:
        numb=numb+1
        kthml=get_content(re_py,h2)
        for k in kthml:
            try:
                kt=get_url_content2(k[:-1])
                if shopaddress in kt:
                    if numb<=standarddemand*10:
                        isstandard=1
                    else:
                        isstandard=0
                    return {'baidu_ranking':numb,'isstandard':isstandard}
            except:
                ''
    return {'baidu_ranking':100,'isstandard':0}

def getwebhtml(baidu_url):
    html=urllib.urlopen(baidu_url).read()
    return html
#----seo抓取数据
def getbaidu_ranking2(keywords,shopsaddress,standarddemand):
    if len(shopsaddress)>14:
        shopsaddress=shopsaddress[:14]
    baidu_url='http://www.baidu.com/s?rn=100&q1='+keywords
    html=getwebhtml(baidu_url)
    html=html.replace('<b>','')
    html=html.replace('</b>','')
    html=html.split('<h3 class="t">')
    i=0
    c=0
    for list in html:
        if (list.find('<span class="g">'+shopsaddress)>0):
            c=1
            break
        i+=1
    if (c==0):
        i=100
    if (i<=10*standarddemand):
        dbtype=1
    else:
        dbtype=0
    return {'baidu_ranking':i,'isstandard':dbtype}

def updaterankings(keywords_id):
    sql='select id,keywords,shopsaddress,standarddemand from seo_keywords where id='+keywords_id
    cursor.execute(sql)
    result=cursor.fetchone()
    if result:
        gmt_created=datetime.datetime.now()
        keywords=result[1].encode('utf8')
#        keywords=urllib.quote(keywords)
        shopsaddress=result[2].encode('utf8')
        standarddemand=result[3]
        if len(shopsaddress)>22:
            ranking=getbaidu_ranking(keywords,shopsaddress,standarddemand)
        else:
            ranking=getbaidu_ranking2(keywords,shopsaddress,standarddemand)
        baidu_ranking=ranking['baidu_ranking']
        isstandard=ranking['isstandard']
        if isstandard==1:
            sql11='select standardtime from seo_keywords where id=%s and standardtime>0'
            cursor.execute(sql11,[keywords_id])
            result11=cursor.fetchone()
            if result11:
                sql2='update seo_keywords set baidu_ranking=%s,isstandard=%s where id=%s'
                cursor.execute(sql2,[baidu_ranking,isstandard,keywords_id])
            else:
                sql2='update seo_keywords set baidu_ranking=%s,isstandard=%s,standardtime=%s where id=%s'
                cursor.execute(sql2,[baidu_ranking,isstandard,gmt_created,keywords_id])
        else: 
            sql2='update seo_keywords set baidu_ranking=%s,isstandard=%s where id=%s'
            cursor.execute(sql2,[baidu_ranking,isstandard,keywords_id])
        company_id=getcompany_id(keywords_id)
        if company_id:
            datetoday=getToday()
            yesterday=getYesterday()
            sql5='select id from seo_rankinghistory where keywords_id=%s and gmt_created=%s'
            cursor.execute(sql5,[keywords_id,datetoday])
            result5=cursor.fetchone()
            if result5:
                sql6='update seo_rankinghistory set update_time=%s,baidu_ranking=%s where keywords_id=%s order by id desc limit 1'
                cursor.execute(sql6,[gmt_created,baidu_ranking,keywords_id])
            else:
                sql4='insert into seo_rankinghistory(keywords_id,company_id,gmt_created,baidu_ranking,update_time) values(%s,%s,%s,%s,%s)'
                cursor.execute(sql4,[keywords_id,company_id,datetoday,baidu_ranking,gmt_created])
#----达标当天扣费
                if isstandard==1:
                    sql7='select chargetype,balance,unit_price from seo_keywords where id=%s'
                    cursor.execute(sql7,[keywords_id])
                    result7=cursor.fetchone()
                    if result7:
                        chargetype=result7[0]
                        if chargetype==1:
                            sql9='select expire_time,years from seo_keywords where id=%s'
                            cursor.execute(sql9,[keywords_id])
                            result9=cursor.fetchone()
                            if result9:
                                expire_time=result9[0]
                                if expire_time==None:
                                    years=result9[1]
                                    argtime=time.strftime('%Y-%m-%d',time.localtime(time.time()))
                                    expire_time2 = str(int(argtime[:4])+int(years))+argtime[4:]
                                    sql10='update seo_keywords set expire_time=%s where id=%s'
                                    cursor.execute(sql10,[expire_time2,keywords_id])
                            
                        if chargetype==2:
                            balance=result7[1]
                            unit_price=result7[2]
                            balance=balance-unit_price
                            sql8='update seo_keywords set balance=%s where id=%s'
                            cursor.execute(sql8,[balance,keywords_id])
        conn.commit()
        return baidu_ranking