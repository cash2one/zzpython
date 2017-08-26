#!/usr/bin/env python   
#coding=utf-8   
import sys
import codecs
import time,datetime
import struct
import os

reload(sys)
sys.setdefaultencoding('utf-8')
nowpath=os.path.dirname(__file__)
execfile(nowpath+"/conn.py")
#更新搜索引擎增量数据
def updatemodifydata():
    sql="SELECT UNIX_TIMESTAMP(max(gmt_modified)) as maxid FROM update_company "
    cursormy.execute(sql)
    resultlist=cursormy.fetchone()
    if resultlist:
        maxid=resultlist['maxid']
        if maxid:
            os.system("/usr/local/coreseek/bin/indexer --config /mnt/pythoncode/zz91crm/coreseek/etc/company.conf delta_company --rotate")
            #os.system("/usr/local/coreseek/bin/indexer --merge company delta_company --config /mnt/pythoncode/zz91crm/coreseek/etc/company.conf --rotate --merge-dst-range deleted 0 0")
            sqlc="update update_log set maxid=%s where utype='company'"
            cursormy.execute(sqlc,[maxid])
            connmy.commit()
updatemodifydata()