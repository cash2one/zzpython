#-*- coding:utf-8 -*-
import MySQLdb,sys,os,memcache,settings,urllib,re,time
from zz91db_sex import newsdb
from zz91db_ast import companydb
from settings import spconfig,appurl
spconfig=settings.SPHINXCONFIG
from sphinxapi import *
from zz91page import *

dbn=newsdb()
reload(sys)
sys.setdefaultencoding('UTF-8')
nowpath="/var/pythoncode/zz91app/zz91app/"
execfile(nowpath+"/func/public_function.py")
execfile(nowpath+"/func/sex_function.py")

zzn=zznews()

newslist=zzn.get_typenews(typeid=34,num=500)
for list in newslist:
    time1=time.time()
    pubdate=int(time1)
    id=list['id']
    print pubdate
    sql="update dede_archives set pubdate=%s where id=%s"
    dbn.updatetodb(sql,[pubdate,id])
    time.sleep(0.3)