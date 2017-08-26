#!/usr/bin/env python   
#coding=utf-8 
from sphinxapi import *
import sys, time,MySQLdb
reload(sys)
sys.setdefaultencoding('utf-8')
from sphinx_rt import spcursor
sp=spcursor()
sp.update("v_compall","company_rt",{'user_id':'14'},6748)

flag=1
if flag:
    try:
        db = MySQLdb.connect(host="192.168.2.4", user="root", passwd="zj88friend", port=9306)
        cursor = db.cursor()
        print "Connect to db successfully!"
       
    except:
        print "Fail to connect to db!"
    
    sql="select * from company_rt where match('@@compname pp')"
    cursor.execute(sql)
    results = cursor.fetchall()
    print results
    sql="replace into company_rt (id,companyname,business) values (10,'中国','废料')"
    #cursor.execute(sql)
    #db.commit()
    
    #sql = "insert into company_rt (id,company_id,service_code,companyname,business) values(%s,%s,%s,%s,%s)"
    #cursor.execute(sql,(3,33,'324','sfsd','fsd'))
    sql = "replace into company_rt(id,compname,business,service_code) values(%s,%s,%s,%s)"
    #cursor.execute(sql,[6725,'d中国','dfsdf废料','dfsd'])
    #db.commit()
    #db.close

#放弃实时索引，用近实时索引来操作

cl = SphinxClient()
cl.SetServer ( "192.168.2.4", 9315 )
cl.SetMatchMode(SPH_MATCH_BOOLEAN)
cl.SetSortMode(SPH_SORT_EXTENDED,'id desc')
#cl.SetFilter('company_id',[6748])
#cl.SetFilter('user_id',[14])
res = cl.Query ( "@compname 公司 ", "company company_rt" )

if not res:
    print 'query failed: %s' % cl.GetLastError()
    sys.exit(1)
if res:
    if res.has_key('matches'):
        itemlist=res['matches']
        for match in itemlist:
            id=match['id']
            attrs=match['attrs']
            #print attrs
            regtime=attrs['regtime']
            #print regtime
if res.has_key('matches'):
        n = 1
        print '\nMatches:'
        for match in res['matches']:
                
                attrsdump = ''
                for attr in res['attrs']:
                        attrname = attr[0]
                        attrtype = attr[1]
                        value = match['attrs'][attrname]
                        if attrtype==SPH_ATTR_TIMESTAMP:
                                value = time.strftime ( '%Y-%m-%d %H:%M:%S', time.localtime(value) )
                        attrsdump = '%s, %s=%s' % ( attrsdump, attrname, value )

                print '%d. doc_id=%s, weight=%d%s' % (n, match['id'], match['weight'], attrsdump)
                n += 1