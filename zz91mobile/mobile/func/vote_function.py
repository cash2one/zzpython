#-*- coding:utf-8 -*-
class zvote:
    def __init__(self):
        self.dbc=dbc
    def votelist(self,frompageCount,limitNum,keywords=""):
        sqlarg=' from vote_list where id>0'
        argument=[]
        if keywords:
            sqlarg+=' and (orderid=%s'
            argument.append(keywords)
            sqlarg+=' or company_name like %s)'
            argument.append('%'+keywords+'%')
        sql1='select count(0)'+sqlarg
        sql='select id,orderid,company_id,company_name,business,votecount,gmt_created,checked '+sqlarg
        sql+=' order by orderid asc limit '+str(frompageCount)+','+str(limitNum)
        if argument:
            count=self.dbc.fetchnumberdb(sql1,argument)
            resultlist=self.dbc.fetchalldb(sql,argument)
        else:
            count=self.dbc.fetchnumberdb(sql1)
            resultlist=self.dbc.fetchalldb(sql)
        listall=[]
        for result in resultlist:
            id=result[0]
            orderid=result[1]
            company_id=result[2]
            company_name=result[3]
            business=result[4]
            votecount=self.votecount(company_id)
            gmt_created=formattime(result[6],0)
            checked=result[7]
            if checked==1:
                checkvalue='已审'
            else:
                checkvalue='<font color=red>未审</font>'
            list={'id':id,'company_id':company_id,'company_name':company_name,'gmt_created':gmt_created,'business':business,'votecount':votecount,'checkvalue':checkvalue,'orderid':orderid}
            listall.append(list)
        return {'list':listall,'count':count}
    def votecount(self,company_id):
        sql="select count(0) from vote_log where forcompany_id=%s and gmt_date<'2016-6-13'"
        result=self.dbc.fetchonedb(sql,[company_id])
        return result[0]
    def votelog(self,frompageCount,limitNum,company_id=""):
        sqlarg=' from vote_log where id>0'
        argument=[]
        if company_id:
            sqlarg+=' and forcompany_id=%s'
            argument.append(company_id)
        sql1='select count(0)'+sqlarg
        sql='select id,forcompany_id,random_num,gmt_created '+sqlarg
        sql+=' order by id desc limit '+str(frompageCount)+','+str(limitNum)
        if argument:
            count=self.dbc.fetchnumberdb(sql1,argument)
            resultlist=self.dbc.fetchalldb(sql,argument)
        else:
            count=self.dbc.fetchnumberdb(sql1)
            resultlist=self.dbc.fetchalldb(sql)
        listall=[]
        for result in resultlist:
            id=result[0]
            forcompany_id=result[1]
            random_num=result[2]
            gmt_created=formattime(result[3])
            sqlc="select name from company where id=%s"
            resultc=dbc.fetchonedb(sqlc,[forcompany_id])
            if resultc:
                company_name=resultc[0]
            list={'id':id,'forcompany_id':forcompany_id,'company_name':company_name,'gmt_created':gmt_created}
            listall.append(list)
        return {'list':listall,'count':count}
            
            
            
            