#-*- coding:utf-8 -*-
#----负数变正数
def fu_to_zheng(shuzi):
    if '-' in str(shuzi):
        shuzi=str(shuzi)[1:]
    return shuzi

class zweixin:
    def __init__(self):
        self.dbc=dbc
    def getexchangetypelist(self,frompageCount='',limitNum='',type='',closeflag=''):
        sqlarg=''
        argument=[]
        if closeflag:
            sqlarg+=' and closeflag=%s'
            argument.append(closeflag)
        if type:
            sqlarg+=' and type=%s'
            argument.append(type)
        sql1='select count(0) from weixin_prize where id>0'+sqlarg
        sql='select id,title,pic,webpic,score,num,numall,ord,closeflag,gmt_created,type from weixin_prize where id>0'+sqlarg
        count=self.dbc.fetchnumberdb(sql1,argument)
        sql=sql+' order by ord,id limit '+str(frompageCount)+','+str(limitNum)
        resultlist=self.dbc.fetchalldb(sql,argument)
        listall=[]
        for result in resultlist:
            id=result[0]
            title=result[1]
            pic=result[2]
            webpic=result[3]
            score=result[4]
            num=result[5]
            numall=result[6]
            ord=result[7]
            closeflag=result[8]
            if closeflag==0:
                closeflagtxt='打开'
            else:
                closeflagtxt='关闭'
            gmt_created=result[9]
            type=result[10]
            if type==1:
                typename='手机站'
            else:
                typename='PC站'
            list={'id':id,'title':title,'pic':pic,'webpic':webpic,'score':score,'num':num,'numall':numall,'ord':ord,'closeflag':closeflag,'closeflagtxt':closeflagtxt,'gmt_created':formattime(gmt_created),'type':type,'typename':typename}
            listall.append(list)
        return {'list':listall,'count':count}
    def getprize(self,id):
        sql='select title from weixin_prize where id=%s'
        result=self.dbc.fetchonedb(sql,[id])
        if result:
            return result[0]
    def getprizetype(self):
        sql='select id,title from weixin_prize'
        resultlist=self.dbc.fetchalldb(sql)
        listall=[]
        if resultlist:
            for result in resultlist:
                list={'id':result[0],'title':result[1]}
                listall.append(list)
        return listall
    def getweixinmobile(self,account):
        sql='select mobile from weixin_account where account=%s'
        result=self.dbc.fetchonedb(sql,[account])
        if result:
            return result[0]
        sql='select mobile from company_account where account=%s'
        result=self.dbc.fetchonedb(sql,[account])
        if result:
            return result[0]
    def getaccountbycontact(self,contact):
        sql='select account from company_account where contact=%s'
        resultlist=self.dbc.fetchall(sql,[contact])
        if resultlist:
            listall=[]
            for result in resultlist:
                listall.append(result[0])
            return listall
    def getaccountbynickname(self,nickname):
        sql='select account from bbs_user_profiler where nickname=%s'
        resultlist=self.dbc.fetchall(sql,[nickname])
        if resultlist:
            listall=[]
            for result in resultlist:
                listall.append(result[0])
            return listall
    def getaccountbymobile(self,mobile):
        sql='select account from weixin_account where mobile=%s'
        resultlist=self.dbc.fetchalldb(sql,[mobile])
        if resultlist:
            listall=[]
            for result in resultlist:
                listall.append(result[0])
            return listall
        sql='select account from company_account where mobile=%s'
        resultlist=self.dbc.fetchalldb(sql,[mobile])
        if resultlist:
            listall=[]
            for result in resultlist:
                listall.append(result[0])
            return listall
    def getnickname(self,account):
        sql='select nickname from bbs_user_profiler where account=%s'
        result=self.dbc.fetchonedb(sql,[account])
        if result:
            return result[0]
        return ''
    def hasaccount(self,account):
        sql='select id from weixin_scoresall where account=%s'
        result=self.dbc.fetchonedb(sql,[account])
        if result:
            return result[0]
    def addwexinscore(self,account,score):
        sql='insert into weixin_score(account,gmt_created,score,validity,rules_code) values(%s,%s,%s,%s,%s)'
        gmt_created=getToday()
        validity='9999-01-01'
        self.dbc.updatetodb(sql,[account,gmt_created,score,validity,'huzhu_answer'])
    def updateprizelog(self,id):
        sql='update weixin_prizelog set ischeck=1 where id=%s'
        self.dbc.updatetodb(sql,[id])
    def getscoreexchange(self,frompageCount,limitNum,account='',prizeid='',ischeck='',type='',order=''):
        sqlarg=''
        argument=[]
        if ischeck and not ischeck=='2':
            sqlarg+=' and ischeck=%s'
            argument.append(ischeck)
        if account:
            sqlarg+=' and account=%s'
            argument.append(account)
        if prizeid:
            sqlarg+=' and prizeid=%s'
            argument.append(prizeid)
        if type:
            sqlarg+=' and type=%s'
            argument.append(type)
        sql1='select count(0) from weixin_prizelog where id>0'+sqlarg
        sql='select id,account,gmt_created,score,ischeck,prizeid,type from weixin_prizelog where id>0'+sqlarg
        if order:
            sql=sql+' order by '+order+' desc'
        else:
            sql=sql+' order by gmt_created desc'
        sql=sql+' limit '+str(frompageCount)+','+str(limitNum)
        listall=[]
        count=self.dbc.fetchnumberdb(sql1,argument)
        resultlist=self.dbc.fetchalldb(sql,argument)
        if resultlist:
            numb=0
            for result in resultlist:
                numb=numb+1
                ischeck=result[4]
                prizeid=result[5]
                account=result[1]
                prizename=self.getprize(prizeid)
                mobile=self.getweixinmobile(account)
                companyname=self.getcompanyname(account)
                companyurl=self.getcompanyurl(account)
                if ischeck==1:
                    ischeck='是'
                else:
                    ischeck='否'
                type=result[6]
                if type==1:
                    typename='手机站'
                else:
                    typename='PC站'
                list={'id':result[0],'prizename':prizename,'account':account,'gmt_created':formattime(result[2]),'score':result[3],'ischeck':ischeck,'mobile':mobile,'numb':numb,'companyname':companyname,'companyurl':companyurl,'type':type,'typename':typename}
                listall.append(list)
        return {'list':listall,'count':count}
    def getcompanyname(self,account):
        sql='select company_id from company_account where account=%s'
        result=self.dbc.fetchonedb(sql,[account])
        if result:
            company_id=result[0]
            sql1='select name from company where id=%s'
            result1=self.dbc.fetchonedb(sql1,[company_id])
            if result1:
                return result1[0]
    def getcompanyurl(self,account):
        sql='select company_id from company_account where account=%s'
        result=self.dbc.fetchonedb(sql,[account])
        if result:
            company_id=result[0]
            sql1='select domain_zz91 from company where id=%s'
            result1=self.dbc.fetchonedb(sql1,[company_id])
            if result1:
                url2=result1[0]
                if url2:
                    url='http://'+url2+'.zz91.com'
                    return url
            return 'http://company.zz91.com/compinfo'+str(company_id)+'.htm'
    def getaccountscore(self,frompageCount,limitNum,account='',nickname='',contact='',mobile=''):
        listall=[]
        count=0
        if nickname or contact or mobile:
            if nickname:
                accountlist=self.getaccountbynickname(nickname)
            if contact:
                accountlist=self.getaccountbycontact(contact)
            if mobile:
                accountlist=self.getaccountbymobile(mobile)
            if accountlist:
                for ac in accountlist:
                    sql3='select score,account from weixin_scoresall where account=%s'
                    result=self.dbc.fetchonedb(sql3,[ac])
                    if result:
                        account=result[1]
                        score=result[0]
                        mobile=self.getweixinmobile(account)
                        list={'score':score,'account':account,'mobile':mobile,'nickname':nickname}
                        listall.append(list)
            if listall:
                count=len(listall)
            return {'list':listall,'count':count}
        argument=[]
        sql1='select count(0) from weixin_scoresall'
        sql='select score,account from weixin_scoresall'
        if account:
            argument.append(account)
            sql1=sql1+' where account=%s'
            sql=sql+' where account=%s'
#        sql=sql+' order by gmt_created desc'
        sql=sql+' order by score desc'
        sql=sql+' limit '+str(frompageCount)+','+str(limitNum)
        result1=self.dbc.fetchonedb(sql1,argument)
        if result1:
            count=result1[0]
        else:
            count=0
        resultlist=self.dbc.fetchalldb(sql,argument)
        if resultlist:
            numb=0
            for result in resultlist:
                account=result[1]
                score=result[0]
                mobile=self.getweixinmobile(account)
                nickname=self.getnickname(account)
                companyname=self.getcompanyname(account)
                companyurl=self.getcompanyurl(account)
                list={'score':score,'account':account,'mobile':mobile,'nickname':nickname,'numb':'','companyname':companyname,'companyurl':companyurl}
                if account not in ['fenghui12039','PoOO']:
                    numb=numb+1
                    list['numb']=numb
                    listall.append(list)
        return {'list':listall,'count':count}
    def getweixinscore(self,frompageCount,limitNum,account=''):
        argument=[]
        sql1='select count(0) from weixin_score'
        sql='select id,account,gmt_created,score,validity  from weixin_score'
        if account:
            argument.append(account)
            sql1=sql1+' where account=%s'
            sql=sql+' where account=%s'
        sql=sql+' order by gmt_created desc'
        sql=sql+' limit '+str(frompageCount)+','+str(limitNum)
        result1=self.dbc.fetchonedb(sql1,argument)
        if result1:
            count=result1[0]
        else:
            count=0
        resultlist=self.dbc.fetchalldb(sql,argument)
        listall=[]
        if resultlist:
            for result in resultlist:
                account=result[1]
                mobile=self.getweixinmobile(account)
                list={'id':result[0],'account':account,'gmt_created':formattime(result[2]),'score':result[3],'validity':formattime(result[4],1),'mobile':mobile}
                listall.append(list)
        return {'list':listall,'count':count}