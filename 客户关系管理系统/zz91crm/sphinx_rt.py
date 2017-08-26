#-*- coding:utf-8 -*-
import sys
from MySQLdb.cursors import DictCursor
from conn import opendb_rt
from conn import opendb
reload(sys)
sys.setdefaultencoding('UTF-8')
class spcursor:
    def __init__(self):
        self._conn=opendb_rt()
        self._cursor=self._conn.cursor(cursorclass = DictCursor)
        self._connmy=opendb()
        self._cursormy=self._connmy.cursor(cursorclass = DictCursor)
    #写入和保存
    def update(self,fromtable,rttable,sqlvalues,id):
        sql="select * from "+str(fromtable)+" where id=%s"
        self._cursormy.execute(sql,[id])
        results = self._cursormy.fetchall()
        vals=[]
        if results:
            for list in results:
                filds=""
                vlist=""
                id=list['id']
                l=[id]
                for ll in list.keys():
                    if ll!="id":
                        filds+=ll+","
                        vlist+="%s,"
                        content=list[ll]
                        if sqlvalues:
                            if sqlvalues.has_key(ll):
                                content=sqlvalues[ll]
                        if not content:
                            content=""
                        l.append(str(content))
                l=tuple(l)
                vals.append(l)
                filds=filds[0:len(filds)-1]
                vlist=vlist[0:len(vlist)-1]
            sql="replace into "+str(rttable)+"(id,"+str(filds)+") values(%s,"+vlist+")"
            self._cursor.executemany(sql,vals)
            self._conn.commit()
    #删除
    def delete(self,rttable,id):
        sql="delete from "+str(rttable)+" where id=%s"
        self._cursor.execute(sql,[id])
        self._conn.commit()
        
            
            