#-*- coding:utf-8 -*-
from zz91db_130 import otherdb
from zz91tools import formattime

class hzjadmin:
    def __init__(self):
        self.db=otherdb()
    def gettypelist(self):
        sql='select id,name,sortrank from hunsha_arttype'
        resultlist=self.db.fetchalldb(sql)
        listall=[]
        if resultlist:
            for result in resultlist:
                list={'id':result[0],'name':result[1],'sortrank':result[2]}
                listall.append(list)
        return listall
    def gettypename(self,id):
        sql='select name from hunsha_arttype where id=%s'
        result=self.db.fetchonedb(sql,[id])
        if result:
            return result[0]
    def gethunshayuyue(self,frompageCount,limitNum,is_hand=''):
        listall=[]
        argument=[]
        sqlarg=''
        if is_hand:
            sqlarg+=' and is_handle=%s'
            argument.append(is_hand)
        sql1='select count(0) from hunsha_yuyue where id>=0'+sqlarg
        sql='select id,name,phone,mail,friend,remark,ip,sendtime,province,city,is_handle from hunsha_yuyue where id>=0'+sqlarg
        sql=sql+' order by sendtime desc limit '+str(frompageCount)+','+str(limitNum)
        count=self.db.fetchnumberdb(sql1,argument)
        resultlist=self.db.fetchalldb(sql,argument)
        for result in resultlist:
            is_handle=result[10]
            list={'id':result[0],'name':result[1],'phone':result[2],'mail':result[3],'friend':result[4],'remark':result[5],'ip':result[6],'sendtime':formattime(result[7]),'province':result[8],'city':result[9],'is_handle':is_handle}
            listall.append(list)
        return {'list':listall,'count':count}

    def getarticallist(self,frompageCount,limitNum,is_del=''):
        listall=[]
        sql1='select count(0) from hunsha_artical where is_del=0'
        sql='select id,typeid,title,gmt_created from hunsha_artical where is_del=0'
        sql=sql+' order by id desc limit '+str(frompageCount)+','+str(limitNum)
        if is_del:
            sql1=sql1.replace('is_del=0','is_del=1')
            sql=sql.replace('is_del=0','is_del=1')
        count=self.db.fetchnumberdb(sql1)
        resultlist=self.db.fetchalldb(sql)
        if resultlist:
            for result in resultlist:
                typeid=result[1]
                typename=self.gettypename(typeid)
                list={'id':result[0],'typeid':typeid,'typename':typename,'title':result[2],'gmt_created':formattime(result[3],1)}
                listall.append(list)
        return {'list':listall,'count':count}
    def getartdetail(self,id):
        sql='select typeid,title,content,gmt_created,litpic,sortrank from hunsha_artical where id=%s'
        result=self.db.fetchonedb(sql,id)
        if result:
            typeid=result[0]
            typename=self.gettypename(typeid)
            list={'typeid':typeid,'typename':typename,'title':result[1],'content':result[2],'gmt_created':formattime(result[3],1),'litpic':result[4],'sortrank':result[5]}
            return list