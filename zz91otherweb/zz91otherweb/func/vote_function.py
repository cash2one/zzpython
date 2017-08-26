#-*- coding:utf-8 -*-
class zvote:
    def __init__(self):
        self.dbc=dbc
    def votelist(self,frompageCount,limitNum,searchlist=""):
        sqlarg=' from vote_list where id>0'
        argument=[]
        if searchlist.has_key("orderid"):
            orderid=searchlist['orderid']
            sqlarg+=' and orderid=%s'
            argument.append(orderid)
        if searchlist.has_key("company_name"):
            company_name=searchlist['company_name']
            sqlarg+=' and company_name like %s'
            argument.append('%'+company_name+'%')
        if searchlist.has_key("vtype"):
            vtype=searchlist['vtype']
            sqlarg+=' and vtype=%s'
            argument.append(vtype)
        sql1='select count(0)'+sqlarg
        sql='select id,orderid,company_id,company_name,business,votecount,gmt_created,checked '+sqlarg
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
            orderid=result[1]
            company_id=result[2]
            company_name=result[3]
            business=result[4]
            votecount=result[5]
            gmt_created=formattime(result[6])
            checked=result[7]
            if checked==1:
                checkvalue='已审'
            else:
                checkvalue='<font color=red>未审</font>'
            list={'id':id,'company_id':company_id,'company_name':company_name,'gmt_created':gmt_created,'business':business,'votecount':votecount,'checkvalue':checkvalue,'orderid':orderid}
            listall.append(list)
        return {'list':listall,'count':count}
    def votelog(self,frompageCount,limitNum,company_id="",searchlist=""):
        sqlarg=' from vote_log where id>0'
        argument=[]
        if company_id:
            sqlarg+=' and forcompany_id=%s'
            argument.append(company_id)
        if searchlist.has_key("vtype"):
            vtype=searchlist['vtype']
            sqlarg+=' and vtype=%s'
            argument.append(vtype)
        sql1='select count(0)'+sqlarg
        sql='select id,forcompany_id,random_num,gmt_created,clientid '+sqlarg
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
            clientid=result[4]
            sqlc="select name from company where id=%s"
            resultc=dbc.fetchonedb(sqlc,[forcompany_id])
            if resultc:
                company_name=resultc[0]
            list={'id':id,'forcompany_id':forcompany_id,'company_name':company_name,'gmt_created':gmt_created,'clientid':clientid}
            listall.append(list)
        return {'list':listall,'count':count}
    def ybp_vote_userlist(self,frompageCount,limitNum,pcontact="",pname="",vote_cid=""):
        sqlarg=' from vote_content_contact where id>0'
        argument=[]
        if pcontact:
            sqlarg+=' and pcontact like %s'
            argument.append(pcontact)
        if pname:
            sqlarg+=' and pname like %s'
            argument.append(pname)
        if vote_cid:
            sqlarg+=' and exists(select openid from vote_content_select where vote_cid=%s and openid=vote_content_contact.openid)'
            argument.append(vote_cid)
        sql1='select count(0)'+sqlarg
        sql='select openid,pname,pcontact,gmt_created '+sqlarg
        sql+=' order by id desc limit '+str(frompageCount)+','+str(limitNum)
        if argument:
            count=self.dbc.fetchnumberdb(sql1,argument)
            resultlist=self.dbc.fetchalldb(sql,argument)
        else:
            count=self.dbc.fetchnumberdb(sql1)
            resultlist=self.dbc.fetchalldb(sql)
        listall=[]
        for result in resultlist:
            openid=result[0]
            pname=result[1]
            pcontact=result[2]
            gmt_created=formattime(result[3])
            list={'openid':openid,'pname':pname,'pcontact':pcontact,'gmt_created':gmt_created}
            listall.append(list)
        return {'list':listall,'count':count}
    def ybp_vote_select(self,openid=""):
        sql="select a.vote_cid,b.parent_id,a.vote_ctext from vote_content_select as a left join vote_content as b on a.vote_cid=b.id where a.openid=%s"
        result=self.dbc.fetchalldb(sql,[openid])
        listall=[]
        if result:
            for list in result:
                l={'cid':list[0],'parent_id':list[1],'vote_ctext':list[2]}
                listall.append(l)
        return listall
    def ybp_vote_count(self,vote_cid):
        sql="select count(0) from vote_content_select where vote_cid=%s"
        result=self.dbc.fetchonedb(sql,[vote_cid])
        return result[0]
    def ybp_vote_detail(self,forno=""):
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
                        vcount=self.ybp_vote_count(id1)
                        label1=list[1]
                        nomust1=0
                        #是否必填
                        if (label1[0:1]=="*"):
                            nomust1=1
                        ctype1=list[2]
                        l={'id':id1,'label':label1,'ctype':ctype1,'nomust':nomust1,'child':None,'vcount':vcount}
                        lall.append(l)
                ll={'id':id,'label':label,'ctype':ctype,'nomust':nomust,'child':lall,'n':n}
                listall.append(ll)
                n=n+1
        return listall
            
            
            
            