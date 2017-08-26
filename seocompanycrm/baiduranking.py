#-*- coding:utf-8 -*-
from apscheduler.scheduler import Scheduler
import urllib,urllib2,re,datetime,time
import MySQLdb

newspath='/var/log/newsprint/'
time2=time.strftime('%Y-%m-%d',time.localtime(time.time()))
conn = MySQLdb.connect(host='192.168.2.10', user='seocompany', passwd='Gs8FXT6szWNqDhG8',db='seocompany',charset='utf8')
#conn = MySQLdb.connect(host='192.168.2.40', user='root', passwd='10534jun',db='seocompany',charset='utf8')
cursor = conn.cursor()

def getYesterday():   
    today=datetime.date.today()
    oneday=datetime.timedelta(days=1)
    yesterday=today-oneday
    return yesterday
def getToday():   
    return datetime.date.today()

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
                f=open(time2+'-out.txt','ab')
                print >>f,keywords
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

def updateranking():
    sql='select id,keywords,shopsaddress,standarddemand from seo_keywords where isdelete=0 and islost=0'
    cursor.execute(sql)
    resultlist=cursor.fetchall()
    if resultlist:
        gmt_created=datetime.datetime.now()
        for result in resultlist:
            keywords_id=result[0]
            keywords=result[1].encode('utf8')
            keywords=urllib.quote(keywords)
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
            sql3='select company_id from seo_keywords where id=%s'
            cursor.execute(sql3,[keywords_id])
            result3=cursor.fetchone()
            if result3:
                company_id=result3[0]
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
                                        expire_time = str(int(argtime[:4])+int(years))+argtime[4:]
                                        sql10='update seo_keywords set expire_time=%s where id=%s'
                                        cursor.execute(sql10,[expire_time,keywords_id])
                            if chargetype==2:
                                balance=result7[1]
                                unit_price=result7[2]
                                balance=balance-unit_price
                                sql8='update seo_keywords set balance=%s where id=%s'
                                cursor.execute(sql8,[balance,keywords_id])
#                print keywords_id
                conn.commit()

schedudler = Scheduler(daemonic = False)  
@schedudler.cron_schedule(second='1', minute='1', day_of_week='0-6', hour='0,4,8,12,17,20') 
def getbaidu():
    updateranking()
    f=open(newspath+time2+'-baidu.txt','ab')
#    f=open(time2+'-baidu.txt','ab')
    print >>f,'成功'
schedudler.start()

#sched = Scheduler()
#sched.daemonic = False
#sched.add_interval_job(getbaidu,minutes=120)
#sched.start()
