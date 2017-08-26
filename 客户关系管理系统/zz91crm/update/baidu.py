#!/usr/bin/env python
# -*- coding: utf-8 -*-
import requests,httplib
import json
import re
import sys
import codecs
import time,datetime
import struct
import os

reload(sys)
sys.setdefaultencoding('utf-8')
nowpath=os.path.dirname(__file__)
execfile(nowpath+"conn.py")

def baiduts():
    sql="select pingyin,id from daohang where id>( SELECT maxid FROM update_log WHERE utype='baidu_daohang') and sid=3738 and checked=1 order by id asc limit 0,2000 "
    cursorserver.execute(sql)
    results = cursorserver.fetchall()
    data=""
    for list in results:
        pingyin=list['pingyin']
        maxid=id=list['id']
        data+='''http://www.zz91.com/cp/'''+str(pingyin)+'/''''
'''
    print data
    r=requests.post("http://data.zz.baidu.com/urls?site=www.zz91.com&token=b35gLljevCgUJrj5",data=data)
    print id
    print r.content
    sqlc="update update_log set maxid=%s where utype='baidu_daohang'"
    cursorserver.execute(sqlc,[maxid])
    connserver.commit()
    #time.sleep(2)
baiduts()
time.sleep(2)
baiduts()
time.sleep(2)
baiduts()
time.sleep(2)
baiduts()
time.sleep(2)
baiduts()
time.sleep(2)
baiduts()
time.sleep(2)
baiduts()
time.sleep(2)
baiduts()
