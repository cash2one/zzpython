#-*- coding:utf-8 -*-
from zz91db_130 import otherdb
from zz91tools import formattime

class hunzhiji:
    def __init__(self):
        self.db=otherdb()
    def getartlist(self,numb,typeid='',order=''):
        listall=[]
        argument=[]
        sqlarg=''
        if typeid:
            sqlarg+=' and typeid=%s'
            argument.append(typeid)
        sql='select id,title,litpic from hunsha_artical where is_del=0'+sqlarg+' limit 0,'+str(numb)
        resultlist=self.db.fetchalldb(sql,argument)
        for result in resultlist:
            list={'id':result[0],'title':result[1],'litpic':result[2]}
            listall.append(list)
        return listall
    def gettypename(self,id):
        sql='select name from hunsha_arttype where id=%s'
        result=self.db.fetchonedb(sql,[id])
        if result:
            return result[0]
    def getartdetail(self,id):
        sql='select typeid,title,content,gmt_created,litpic,sortrank from hunsha_artical where id=%s'
        result=self.db.fetchonedb(sql,id)
        if result:
            typeid=result[0]
            typename=self.gettypename(typeid)
            list={'typeid':typeid,'typename':typename,'title':result[1],'content':result[2],'gmt_created':formattime(result[3],1),'litpic':result[4],'sortrank':result[5]}
            return list