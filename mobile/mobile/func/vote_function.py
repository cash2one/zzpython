#-*- coding:utf-8 -*-
class zvote:
    def __init__(self):
        self.dbc=dbc
    def votelist(self,frompageCount,limitNum,keywords="",vtype=""):
        sqlarg=' from vote_list where id>0 '
        argument=[]
        if keywords:
            sqlarg+=' and (orderid=%s'
            argument.append(keywords)
            sqlarg+=' or company_name like %s)'
            argument.append('%'+keywords+'%')
        if vtype:
            sqlarg+=' and vtype=%s'
            argument.append(vtype)
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
            votecount=self.getvotecount(company_id,vtype)
            gmt_created=formattime(result[6],0)
            checked=result[7]
            if checked==1:
                checkvalue='已审'
            else:
                checkvalue='<font color=red>未审</font>'
            list={'id':id,'company_id':company_id,'company_name':company_name,'gmt_created':gmt_created,'business':business,'votecount':votecount,'checkvalue':checkvalue,'orderid':orderid}
            listall.append(list)
        return {'list':listall,'count':count,'sql':sql}
    def getvotedetail(self,id=""):
        sql="select orderid,company_name,business,company_id from vote_list where id=%s"
        result=dbc.fetchonedb(sql,[id])
        list=[]
        if result:
            orderid=result[0]
            company_name=result[1]
            business=result[2]
            company_id=result[3]
            list={'id':id,'orderid':orderid,'company_name':company_name,'business':business,'company_id':company_id}
        return list
    def getvotecount(self,company_id,vtype):
        sql="select count(0) from vote_log where forcompany_id=%s and vtype=%s"
        result=self.dbc.fetchonedb(sql,[company_id,vtype])
        return result[0]
    #调查问卷
    def votecontent(self,forno=""):
        sql="select id,label,ctype from vote_content where parent_id=0 and forno=%s order by corder asc,id asc"
        result=self.dbc.fetchalldb(sql,[forno])
        listall=[]
        if result:
            n=1
            for list in result:
                id=list[0]
                label=list[1]
                nomust=0
                #是否必填
                if (label[0:1]=="*"):
                    nomust=1
                ctype=list[2]
                l=None
                sql1="select id,label,ctype from vote_content where parent_id=%s and forno=%s order by corder asc,id asc"
                result1=self.dbc.fetchalldb(sql1,[id,forno])
                lall=[]
                if result1:
                    for list in result1:
                        id1=list[0]
                        label1=list[1]
                        nomust1=0
                        #是否必填
                        if (label1[0:1]=="*"):
                            nomust1=1
                        ctype1=list[2]
                        l={'id':id1,'label':label1,'ctype':ctype1,'nomust':nomust1,'child':None}
                        lall.append(l)
                ll={'id':id,'label':label,'ctype':ctype,'nomust':nomust,'child':lall,'n':n}
                listall.append(ll)
                n=n+1
        return listall
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
    #投票活动
    def getvote(self,vtype='',id=''):
        if id:
            sql="select vname,vcount,vfromdate,vtodate from vote_pv where id=%s"
            result=dbc.fetchonedb(sql,[id])
        else:
            if vtype:
                sql="select vname,vcount,vfromdate,vtodate from vote_pv where vtype=%s"
                result=dbc.fetchonedb(sql,[vtype])
        list=[]
        if result:
            vname=result[0]
            vcount=result[1]
            vfromdate=result[2]
            vtodate=result[3]
            vtodate_int=date_to_int(vtodate)
            nowint=date_to_int(datetime.date.today())
            haveday=None
            if vtodate_int>=nowint:
                haveday=(vtodate_int-nowint)/(3600*24)+1
            list={'vname':vname,'vcount':vcount,'vfromdate':vcount,'vtodate':vtodate,'haveday':haveday}
        return list
            
            
            