#!/usr/bin/env python   
#-*-coding:gb2312-*-
import pymssql
import sys
reload(sys)
sys.setdefaultencoding('gb2312')
conn=pymssql.connect(host=r'192.168.2.2',trusted=False,user=r'rcu_crm',password=r'fdf@$@#dfdf9780@#1.kdsfd',database=r'rcu_crm',charset='gb2312')
cursor=conn.cursor()

sql="select convert(text,detail) from test where id=2"
cursor.execute(sql)
results = cursor.fetchone()
if results:
    print results[0]
