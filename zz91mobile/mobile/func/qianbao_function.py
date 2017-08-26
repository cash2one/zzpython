#-*- coding:utf-8 -*-
class mshop:
    def __init__(self):
        self.dbc=dbc
    def getis_wxtg(self,company_id):
        sql='select id from shop_product where company_id=%s and is_check=0'
        result=self.dbc.fetchonedb(sql,[company_id])
        if result:
            return result[0]

class qianbao:
    #----初始化ast数据库
    def __init__(self):
        self.dbc=dbc
    def getviptype(self,company_id):
        sql='select membership_code from company where id=%s'
        result=self.dbc.fetchonedb(sql,[company_id])
        if result:
            return result[0]
    def getcompany_account(self,company_id):
        sql='select account from company_account where company_id=%s'
        result=self.dbc.fetchonedb(sql,[company_id])
        if result:
            return result[0]
    def getsendfee(self,company_id,fee,ftype):
        sql='select id from pay_mobileWallet where company_id=%s and fee=%s and ftype=%s'
        result=self.dbc.fetchonedb(sql,[company_id,fee,ftype])
        if not result:
            gmt_date=datetime.date.today()
            gmt_created=datetime.datetime.now()
            sql2='insert into pay_mobileWallet(company_id,fee,ftype,gmt_date,gmt_created,gmt_modified) values(%s,%s,%s,%s,%s,%s)'
            self.dbc.updatetodb(sql2,[company_id,20,6,gmt_date,gmt_created,gmt_created])
    def getcompanycontact(self,company_id):
        sql='select contact,mobile from company_account where company_id=%s'
        result=self.dbc.fetchonedb(sql,[company_id])
        list={'contact':'','mobile':''}
        if result:
            contact=result[0]
            mobile=result[1]
            list={'contact':contact,'mobile':mobile}
        return list
    def getpayfeelist(self,company_id,frompageCount='',limitNum='',timarg=''):
        argument=[company_id]
        sqlarg=''
        if timarg:
            if timarg=='1':
                sqlarg=' and gmt_date>=%s'
                argument.append(getpastoneday(30))
            elif timarg=='2':
                sqlarg=' and gmt_date>=%s'
                argument.append(getpastoneday(90))
            elif timarg=='3':
                sqlarg=' and gmt_date>=%s'
                argument.append(getpastoneday(365))
            elif timarg=='4':
                sqlarg=' and gmt_date<%s'
                argument.append(getpastoneday(365))
        sql1='select count(0) from pay_mobileWallet where company_id=%s'+sqlarg
        sql='select id,fee,ftype,gmt_date,product_id from pay_mobileWallet where company_id=%s'+sqlarg
        sql=sql+' order by gmt_created desc limit '+str(frompageCount)+','+str(limitNum)
        count=self.dbc.fetchnumberdb(sql1,argument)
        resultlist=self.dbc.fetchalldb(sql,argument)
        listall=[]
        for result in resultlist:
            id=result[0]
            fee=result[1]
            if fee>0:
                fee='+'+str(fee)
            ftype=result[2]
            gmt_date=formattime(result[3],1)
            product_id=result[4]
            ftypename=self.getftypename(ftype)
            list={'id':id,'fee':fee,'ftype':ftype,'gmt_date':gmt_date,'ftypename':ftypename,'product_id':product_id}
            listall.append(list)
        return {'list':listall,'count':count}
    def getftypename(self,id):
        sql='select name from pay_wallettype where id=%s'
        result=self.dbc.fetchonedb(sql,[id])
        if result:
            return result[0]
    def getqianbaoblance(self,company_id):
        sql='select sum(fee) from pay_mobileWallet where company_id=%s'
        result=self.dbc.fetchonedb(sql,[company_id])[0]
        if result:
            if result<=0:
                return '0.00'
            else:
                return '%.2f'%result
        return '0.00'
    def getqianbaoblance2(self,company_id):
        sql='select sum(fee) from pay_mobileWallet where company_id=%s'
        result=self.dbc.fetchonedb(sql,[company_id])[0]
        if result:
            return result
        return 0.0
    def getpayfee(self,company_id='',forcompany_id='',product_id='',ftype='',fee='',once='',data=''):
        
        #判断活动时间
        payinsert=1
        if ftype:
            sqlc="select begin_time,end_time,maxfee from pay_wallettype where id=%s"
            resultgg=self.dbc.fetchonedb(sqlc,[ftype])
            timeall=datetime.datetime.now()
            if resultgg:
                begin_time=resultgg[0]
                end_time=resultgg[1]
                maxfee=resultgg[2]
            else:
                return 0.00
            payinsert=1
            if begin_time and end_time:
                if timeall>=begin_time and timeall<end_time:
                    payinsert=1
                else:
                    payinsert=0
        if payinsert==1:
            if not fee:
                fee=self.getpay_wallettypefee(ftype)
            if fee:
                #购买次数是否唯一
                if once:
                    sql="select id from pay_mobileWallet where company_id=%s and ftype=%s"
                    result=self.dbc.fetchonedb(sql,[company_id,ftype])
                    if result:
                        return "havebuy"
                #置顶广告获取购买数量
                if ftype=="36":
                    if data:
                        fee=int(data)*fee
                #----账户余额大于当前消费金额才可以进行交易
                sql4='select sum(fee) from pay_mobileWallet where company_id=%s'
                blance=self.dbc.fetchonedb(sql4,[company_id])[0]
                if blance>=-fee:
                    gmt_date=datetime.date.today()
                    gmt_created=datetime.datetime.now()
                    argument=[company_id,forcompany_id,product_id,fee,ftype,gmt_date,gmt_created,gmt_created]
                    sql='insert into pay_mobileWallet(company_id,forcompany_id,product_id,fee,ftype,gmt_date,gmt_created,gmt_modified) values(%s,%s,%s,%s,%s,%s,%s,%s)'
                    self.dbc.updatetodb(sql,argument)
                    if ftype in ['1','7']:
                        argument2=[forcompany_id,company_id,product_id,0.5,2,gmt_date,gmt_created,gmt_created]
                        sql2='insert into pay_mobileWallet(company_id,forcompany_id,product_id,fee,ftype,gmt_date,gmt_created,gmt_modified) values(%s,%s,%s,%s,%s,%s,%s,%s)'
                        self.dbc.updatetodb(sql2,argument2)
                    return 1
                else:
                    return "nomoney"
            else:
                return "err"
        else:
            return "outdate"
    def getpay_wallettypefee(self,id):
        sql='select fee from pay_wallettype where id=%s'
        result=self.dbc.fetchonedb(sql,[id])
        if result:
            return result[0]
    def getisbuyshowphone(self,company_id):
        gmt_created=datetime.datetime.now()
        sql='select id from shop_showphone where company_id=%s and gmt_end>=%s order by id desc'
        result=dbc.fetchonedb(sql,[company_id,gmt_created])
        if result:
            return 3
    def getisseecompany(self,company_id,forcompany_id):
        if company_id==forcompany_id:
            return 2
        isbuyshowphone=self.getisbuyshowphone(forcompany_id)
        if isbuyshowphone:
            return 2
        iszst=self.getiszstcompany(company_id)
        if iszst:
            return 2
        sql2='select membership_code from company where id=%s'
        result2=self.dbc.fetchonedb(sql2,[company_id])
        if result2:
            membership_code=result2[0]
#            if membership_code in ['10051001','100510021000','100510021001','100510021002']:
#                return 2
            if membership_code=='10051003':
                sql3='select id from phone_click_log where company_id=%s and target_id=%s'
                result3=self.dbc.fetchonedb(sql3,[company_id,forcompany_id])
                if result3:
                    return 4
        sql='select id from pay_mobileWallet where company_id=%s and forcompany_id=%s'
        result=self.dbc.fetchonedb(sql,[company_id,forcompany_id])
        if result:
            return 1
    #----判断是否为再生通
    def getiszstcompany(self,company_id):
        if company_id:
            sqll="select id from crm_company_service where company_id=%s and crm_service_code in('1000','1006') and apply_status=1 and DATEDIFF(CURDATE(),`gmt_end`)<=0"
            zstresult=self.dbc.fetchonedb(sqll,[company_id])
            if zstresult:
                return 1
            else:
                return None
        else:
            return None
    def getinfeegmt(self,company_id,gmt_begin='',gmt_end='',ftype=''):
        sql='select sum(fee) from pay_mobileWallet where company_id=%s and fee>0 and ftype=2'
        argument=[company_id]
        if gmt_begin:
            argument.append(gmt_begin)
            sql+=' and gmt_date>=%s'
        if gmt_end:
            argument.append(gmt_end)
            sql+=' and gmt_date<%s'
        if ftype:
            sql=sql.replace('and ftype=2',' and ftype in '+ftype)
        result=self.dbc.fetchonedb(sql,argument)[0]
        if result:
            return '%.1f'%result
        return 0.0
    def getoutfeegmt(self,company_id,gmt_begin='',gmt_end=''):
        sql='select sum(fee) from pay_mobileWallet where company_id=%s and fee<0'
        argument=[company_id]
        if gmt_begin:
            argument.append(gmt_begin)
            sql+=' and gmt_date>=%s'
        if gmt_end:
            sql+=' and gmt_date<%s'
            argument.append(gmt_end)
        result=self.dbc.fetchonedb(sql,argument)[0]
        if result:
            return '%.1f'%float(str(result)[1:])
        return 0.0
    def getinfeeyd(self,company_id):
        sql='select sum(fee) from pay_mobileWallet where company_id=%s and gmt_date=%s and fee>0 and ftype=2'
        result=self.dbc.fetchonedb(sql,[company_id,getYesterday()])[0]
        if result:
            return '%.2f'%result
        return '0.00'
    def getinfeeall(self,company_id):
        sql='select sum(fee) from pay_mobileWallet where company_id=%s and fee>0 and ftype=2'
        result=self.dbc.fetchonedb(sql,[company_id])[0]
        if result:
            return '%.2f'%result
        return '0.00'
    def getoutfeeyd(self,company_id):
        sql='select sum(fee) from pay_mobileWallet where company_id=%s and gmt_date=%s and fee<0'
        result=self.dbc.fetchonedb(sql,[company_id,getYesterday()])[0]
        if result:
            return '%.2f'%float(str(result)[1:])
        return '0.00'
    def getoutfeeall(self,company_id):
        benyue=time.strftime('%Y-%m-1 00:00:00',time.localtime(time.time()))
        sql='select sum(fee) from pay_mobileWallet where company_id=%s and fee<0 and gmt_created>=%s'
        result=self.dbc.fetchonedb(sql,[company_id,benyue])[0]
        if result:
            return '%.2f'%float(str(result)[1:])
        return '0.00'
        