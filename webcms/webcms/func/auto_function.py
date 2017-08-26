#-*- coding:utf-8 -*-
import os,sys
reload(sys)
sys.setdefaultencoding('UTF-8')
sys.path.append('/var/pythoncode/zz91public/')
nowpath=os.path.dirname(__file__)
execfile(nowpath+"/function.py")
from zz91settings import pycmspath,ftpconn,pycmsurl
from zz91db_130 import pycmsdb
#pyftp = pyftp(ftpconn['ip'],ftpconn['uname'],ftpconn['pword'])
dbp=pycmsdb()

def cleararthtml():
    sql='select id,typeid from py_user_artical where is_del=1 and is_make=1'
    sql2='select reid,pinyin from py_user_arttype1 where id=%s'
    sql3='select pinyin from py_user_arttype1 where id=%s'
    sql4='update py_user_artical set is_make=0 where id=%s'
    resultlist=dbp.fetchalldb(sql)
    for result in resultlist:
        id=result[0]
        typeid=result[1]
        result2=dbp.fetchonedb(sql2,[typeid])
        if result2:
            reid=result2[0]
            pinyin=result2[1]
            if reid:
                result3=dbp.fetchonedb(sql3,[reid])
                if result3:
                    repinyin=result3[0]
                    pinyin=repinyin+'/'+pinyin
            filename=str(id)+'.html'
            ftpath=ftpconn['ftpath']['pycms']+'/'+pinyin
            try:
                #pyftp.delfile(ftpath,filename)
                dbp.updatetodb(sql4,[id])
            except:
                pass#没有这个文件'''
            print filename
            print ftpath
#            pyftp.delfile(ftpath,filename)

cleararthtml()