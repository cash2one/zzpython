class dacongfunc:
    def __init__(self):
        self.dcdb=dcdb
    def getnewslist(self,frompageCount,limitNum,ptype=None,arcrank=''):
        sqlarg=''
        argument=[]
        if ptype:
            if (ptype=="1"):
                sqlarg+=' and company_id>0'
            else:
                sqlarg+=' and company_id=0'
        if arcrank:
            sqlarg+=' and arcrank=%s'
            argument.append(arcrank)
        sql1='select count(0) from dede_archives where id>0'+sqlarg
        sql='select id,title,litpic,pubdate from dede_archives where id>0'+sqlarg
        sql=sql+' order by id desc limit '+str(frompageCount)+','+str(limitNum)
        count=self.dcdb.fetchnumberdb(sql1,argument)
        resultlist=self.dcdb.fetchalldb(sql,argument)
        listall=[]
        for result in resultlist:
            id=result[0]
            title=result[1]
            litpic=result[2]
            pubdate=int_to_strall(result[3])
            list={'id':id,'title':title,'litpic':litpic,'pubdate':pubdate}
            listall.append(list)
        return {'list':listall,'count':count}
    def gettypelist(self):
        sql='select id,typename,keywords from dede_arctype where reid>0'
        resultlist=self.dcdb.fetchalldb(sql)
        listall=[]
        for result in resultlist:
            id=result[0]
            typename=result[1]
            list={'id':id,'typename':typename}
            listall.append(list)
        return listall