#-*- coding:utf-8 -*-
#----负数变正数
def fu_to_zheng(shuzi):
    if '-' in str(shuzi):
        shuzi=str(shuzi)[1:]
    return shuzi
class mshop:
    def __init__(self):
        self.dbc=dbc
    def getshop_product_ranklist(self,frompageCount,limitNum,paytype='',is_checked='',account='',bz='',mobile='',keywords=''):
        sqlarg=' from products_keywords_rank where id>0'
        argument=[]
        if paytype:
            sqlarg+=' and type=%s'
            argument.append(paytype)
        if is_checked:
            sqlarg+=' and is_checked=%s'
            argument.append(is_checked)
        if account:
            sqlarg+=' and apply_account=%s'
            argument.append(account)
        if bz:
            sqlarg+=' and bz=%s'
            argument.append(bz)
        if keywords:
            sqlarg+=' and name like %s'
            argument.append('%'+keywords+'%')
        if mobile:
            sqlarg+=' and exists(select company_id from company_account where company_id=products_keywords_rank.company_id and mobile=%s)'
            argument.append(mobile)
        sql1='select count(0)'+sqlarg
        sql='select id,product_id,name,start_time,end_time,is_checked,gmt_modified,company_id,apply_account,buy_time,bz'+sqlarg
        sql+=' order by id desc limit '+str(frompageCount)+','+str(limitNum)
        count=self.dbc.fetchnumberdb(sql1,argument)
        resultlist=self.dbc.fetchalldb(sql,argument)
        listall=[]
        for result in resultlist:
            id=result[0]
            pro_id=result[1]
            pro_title=self.getproduct_title(pro_id)
            name=result[2]
            start_time=formattime(result[3])
            end_time=formattime(result[4])
            is_checked=result[5]
            check_name=''
            if is_checked=='0':
                check_name="未审核"
            if is_checked=='1':
                check_name="已审核"
            if is_checked=='2':
                check_name="交易关闭"
            gmt_modified=formattime(result[6])
            company_id=result[7]
            company_name=self.getcompany_name(company_id)
            company_account=result[8]
            buy_time=formattime(result[9])
            bz=result[10]
            if not bz:
                bz=''
            list={'id':id,'pro_id':pro_id,'pro_title':pro_title,'paytype':paytype,'name':name,'start_time':start_time,'end_time':end_time,'is_checked':is_checked,'check_name':check_name,'gmt_created':gmt_modified,'company_id':company_id,'company_name':company_name,'company_account':company_account,'bz':bz}
            listall.append(list)
        return {'list':listall,'count':count}
    def getshop_productlist(self,frompageCount,limitNum,paytype='',account='',mobile=''):
        sqlarg=' from v_shop_showphone where id>0'
        argument=[]
        if paytype:
            sqlarg+=' and paytype=%s'
            argument.append(paytype)
        if account:
            sqlarg+=' and account=%s'
            argument.append(account)
        if mobile:
            sqlarg+=' and mobile=%s'
            argument.append(mobile)
        sql1='select count(0)'+sqlarg
        sql='select id,company_id,gmt_begin,gmt_end,gmt_created'+sqlarg
        sql+=' order by id desc limit '+str(frompageCount)+','+str(limitNum)
        count=self.dbc.fetchnumberdb(sql1,argument)
        resultlist=self.dbc.fetchalldb(sql,argument)
        listall=[]
        for result in resultlist:
            id=result[0]
            company_id=result[1]
            company_name=self.getcompany_name(company_id)
            gmt_begin=formattime(result[2])
            gmt_end=formattime(result[3])
            gmt_created=formattime(result[4])
            list={'id':id,'company_id':company_id,'company_name':company_name,'gmt_begin':gmt_begin,'gmt_end':gmt_end,'gmt_created':gmt_created}
            listall.append(list)
        return {'list':listall,'count':count}
    def getllb_keywords(self,frompageCount,limitNum,searchlist=''):
        sqlarg=' from v_shop_app_jingjia_keywords where id>0'
        argument=[]
        account=searchlist.get('account')
        mobile=searchlist.get('mobile')
        checked=searchlist.get('checked')
        if account:
            sqlarg+=' and account=%s'
            argument.append(account)
        if mobile:
            sqlarg+=' and mobile=%s'
            argument.append(mobile)
        if checked:
            sqlarg+=' and checked=%s'
            argument.append(checked)
        sql1='select count(0)'+sqlarg
        sql='select id,company_id,keywords,price,product_id,checked,gmt_created'+sqlarg
        sql+=' order by id desc limit '+str(frompageCount)+','+str(limitNum)
        count=self.dbc.fetchnumberdb(sql1,argument)
        resultlist=self.dbc.fetchalldb(sql,argument)
        listall=[]
        for result in resultlist:
            id=result[0]
            key_id=id
            company_id=result[1]
            company_name=self.getcompany_name(company_id)
            keywords=result[2]
            price=result[3]
            product_id=result[4]
            product_title=self.getproduct_title(product_id)
            checked=result[5]
            if checked==1:
                checkedtext="上线"
            else:
                checkedtext="<font color=red>下线</font>"
            gmt_created=formattime(result[6])
            key_showcount=0
            key_clickcount=0
            sqlk="select sum(showcount) from app_jingjia_search where company_id=%s and key_id=%s"
            resultc=dbc.fetchonedb(sqlk,[company_id,key_id])
            if resultc:
                key_showcount=resultc[0]
                if not key_showcount:
                    key_showcount=0
                
            sqlk="select sum(clickcount) from app_jingjia_click where company_id=%s and key_id=%s"
            resultc=dbc.fetchonedb(sqlk,[company_id,key_id])
            if resultc:
                key_clickcount=resultc[0]
                if not key_clickcount:
                    key_clickcount=0
                    
            sqlk="select sum(fee) from pay_mobilewallet where company_id=%s and ftype=%s"
            result=dbc.fetchonedb(sqlk,[company_id,55])
            key_pricecount=0
            if result:
                key_pricecount=result[0]
            if not key_pricecount:
                key_pricecount=0
            phonecount=0
            sql="select count(0) from phone_telclick_log where forcompany_id=%s"
            result=dbc.fetchonedb(sql,[company_id])
            if result:
                phonecount=result[0]
                if not phonecount:
                    phonecount=0
            list={'id':id,'company_id':company_id,'company_name':company_name,'keywords':keywords,'key_showcount':key_showcount,'key_clickcount':key_clickcount,'key_pricecount':key_pricecount,'phonecount':phonecount,'product_id':product_id,'price':price,'product_title':product_title,'checked':checked,'checkedtext':checkedtext,'gmt_created':gmt_created}
            listall.append(list)
        return {'list':listall,'count':count}
    
    def getshop_reflushlist(self,frompageCount,limitNum,paytype='',account='',mobile=''):
        sqlarg=' from v_shop_reflush where id>0'
        argument=[]
        if paytype:
            sqlarg+=' and paytype=%s'
            argument.append(paytype)
        if account:
            sqlarg+=' and account=%s'
            argument.append(account)
        if mobile:
            sqlarg+=' and mobile=%s'
            argument.append(mobile)
        sql1='select count(0)'+sqlarg
        sql='select id,company_id,gmt_begin,gmt_end,gmt_created'+sqlarg
        sql+=' order by id desc limit '+str(frompageCount)+','+str(limitNum)
        count=self.dbc.fetchnumberdb(sql1,argument)
        resultlist=self.dbc.fetchalldb(sql,argument)
        listall=[]
        for result in resultlist:
            id=result[0]
            company_id=result[1]
            company_name=self.getcompany_name(company_id)
            gmt_begin=formattime(result[2])
            gmt_end=formattime(result[3])
            gmt_created=formattime(result[4])
            list={'id':id,'company_id':company_id,'company_name':company_name,'gmt_begin':gmt_begin,'gmt_end':gmt_end,'gmt_created':gmt_created}
            listall.append(list)
        return {'list':listall,'count':count}
    def getshop_baoming(self,frompageCount,limitNum,paytype=''):
        sqlarg=' from shop_baoming where id>0'
        argument=[]
        if paytype:
            sqlarg+=' and paytype=%s'
            argument.append(paytype)
        sql1='select count(0)'+sqlarg
        sql='select id,company_id,gmt_created,content'+sqlarg
        sql+=' order by id desc limit '+str(frompageCount)+','+str(limitNum)
        count=self.dbc.fetchnumberdb(sql1,argument)
        resultlist=self.dbc.fetchalldb(sql,argument)
        listall=[]
        for result in resultlist:
            id=result[0]
            company_id=result[1]
            company_name=self.getcompany_name(company_id)
            gmt_created=formattime(result[2])
            content=result[3]
            list={'id':id,'company_id':company_id,'company_name':company_name,'gmt_created':gmt_created,'content':content}
            listall.append(list)
        return {'list':listall,'count':count}
    def getcompany_name(self,company_id):
        sql='select name from company where id=%s'
        result=self.dbc.fetchonedb(sql,[company_id])
        if result:
            return result[0]
    def getproduct_title(self,proid):
        sql='select title from products where id=%s'
        result=self.dbc.fetchonedb(sql,[proid])
        if result:
            return result[0]
class mobile:
    def __init__(self):
        self.dbc=dbc
    def getpay_orderlist(self,frompageCount,limitNum,searchlist=''):
        sqlarg=' from pay_order where id>0'
        argument=[]
        if searchlist.get("out_trade_no"):
            sqlarg+=' and out_trade_no=%s'
            argument.append(searchlist.get("out_trade_no"))
        if searchlist.get("mobile"):
            sqlarg+=' and mobile=%s'
            argument.append(searchlist.get("mobile"))
        is_success=searchlist.get("is_success")
        if is_success:
            if str(is_success)=="1":
                sqlarg+=' and is_success="SUCCESS"'
            else:
                sqlarg+=' and is_success in (F,"")'
        sql1='select count(0)'+sqlarg
        sql='select id,buyer_email,buyer_id,is_success,notify_id,notify_time,out_trade_no,subject,total_fee,trade_no,trade_status,contact,mobile,gmt_created,company_id'+sqlarg
        sql+=' order by id desc limit '+str(frompageCount)+','+str(limitNum)
        count=self.dbc.fetchnumberdb(sql1,argument)
        resultlist=self.dbc.fetchalldb(sql,argument)
        listall=[]
        for result in resultlist:
            id=result[0]
            buyer_email=result[1]
            buyer_id=result[2]
            is_success=result[3]
            notify_id=result[4]
            notify_time=result[5]
            out_trade_no=result[6]
            subject=result[7]
            total_fee=result[8]
            trade_no=result[9]
            trade_status=result[10]
            contact=result[11]
            mobile=result[12]
            gmt_created=formattime(result[13])
            company_id=result[14]
            companyname=self.getcompany_name(company_id)
            list={'id':id,'buyer_email':buyer_email,'buyer_id':buyer_id,'is_success':is_success,'notify_id':notify_id,'notify_time':notify_time,'out_trade_no':out_trade_no,'subject':subject,'total_fee':total_fee,'trade_no':trade_no,'trade_status':trade_status,'contact':contact,'mobile':mobile,'gmt_created':gmt_created,'company_id':company_id,'companyname':companyname}
            listall.append(list)
        return {'list':listall,'count':count}
    def getcompany_name(self,company_id):
        sql='select name from company where id=%s'
        result=self.dbc.fetchonedb(sql,[company_id])
        if result:
            return result[0]
    def getoutfeelist(self,frompageCount,limitNum,type='',gmtdate='',gmt_begin='',gmt_end='',paytypeid='',company_id='',company_name='',account='',mobile='',paytypem=''):
        argument=[]
        sqlarg=' from pay_mobileWallet as a left join company as b on a.company_id=b.id left join company_account as c on a.company_id=c.company_id where a.id>0'
        if type==1:
            sqlarg+=' and a.fee>0'
        elif type==2:
            sqlarg+=' and a.fee<0'
        if gmtdate:
            sqlarg+=' and a.gmt_date=%s'
            argument.append(gmtdate)
        if gmt_begin:
            sqlarg+=' and a.gmt_date>=%s'
            argument.append(gmt_begin)
        if gmt_end:
            sqlarg+=' and a.gmt_date<=%s'
            argument.append(gmt_end)
        if paytypeid:
            sqlarg+=' and a.ftype=%s'
            argument.append(paytypeid)
        if company_name:
            sqlarg+=' and b.name=%s'
            argument.append(company_name)
        if company_id:
            sqlarg+=' and b.id=%s'
            argument.append(company_id)
        if account:
            sqlarg+=' and c.account=%s'
            argument.append(account)
        if mobile:
            sqlarg+=' and c.mobile=%s'
            argument.append(mobile)
        if paytypem:
            sqlarg+=' and a.paytype=%s'
            argument.append(paytypem)
        sql3='select count(distinct a.company_id)'+sqlarg
        sql2='select sum(a.fee)'+sqlarg
        sql1='select count(a.id)'+sqlarg
        sql='select a.id,a.company_id,a.fee,a.ftype,a.gmt_created,b.name,c.account,c.mobile,a.payfrom,a.paytype,a.forcompany_id,a.product_id,a.bz'+sqlarg
        pcount=self.dbc.fetchnumberdb(sql3,argument)
        sumfee=self.dbc.fetchnumberdb(sql2,argument)
        if sumfee:
            sumfee='%.2f'%sumfee
        count=self.dbc.fetchnumberdb(sql1,argument)
        sql=sql+' order by a.gmt_created desc limit '+str(frompageCount)+','+str(limitNum)
        resultlist=self.dbc.fetchalldb(sql,argument)
        none1=1
        none2=1
        listall=[]
        for result in resultlist:
            id=result[0]
            company_id=result[1]
            fee=result[2]
            ftype=result[3]
            ftypename=self.getftypename(ftype)
            gmt_created=formattime(result[4])
            company_name=result[5]
            account=result[6]
            mobile=result[7]
            paytype=result[9]
            payfrom=result[8]
            forcompany_id=result[10]
            product_id=result[11]
            bz=result[12]
            list={'id':id,'company_id':company_id,'company_name':company_name,'account':account,'mobile':mobile,'fee':fee,'ftype':ftype,'ftypename':ftypename,'gmt_created':gmt_created,'paytype':paytype,'payfrom':payfrom,'forcompany_id':forcompany_id,'product_id':product_id,'bz':bz}
            listall.append(list)
        return {'list':listall,'count':count,'sumfee':sumfee,'pcount':pcount}
    #开通单
    def getservicelist(self,frompageCount,limitNum,gmt_start='',gmt_end='',company_name='',company_id='',account='',mobile=''):
        argument=[]
        sqlarg=' from crm_company_service as a left join company as b on a.company_id=b.id left join company_account as c on a.company_id=c.company_id where a.id>0'
        if gmt_start:
            sqlarg+=' and a.gmt_start>%s'
            argument.append(gmt_start)
        if gmt_end:
            sqlarg+=' and a.gmt_end<=%s'
            argument.append(gmt_end)
        
        if company_name:
            sqlarg+=' and b.name=%s'
            argument.append(company_name)
        if company_id:
            sqlarg+=' and b.id=%s'
            argument.append(company_id)
        if account:
            sqlarg+=' and c.account=%s'
            argument.append(account)
        if mobile:
            sqlarg+=' and c.mobile=%s'
            argument.append(mobile)
        sql1='select count(a.id)'+sqlarg
        sql='select a.id,a.company_id,a.crm_service_code,a.gmt_start,a.gmt_end,a.apply_status,a.remark,a.gmt_created,a.membership_code,a.zst_year,b.name,c.account,c.mobile'+sqlarg
        count=self.dbc.fetchnumberdb(sql1,argument)
        sql=sql+' order by a.gmt_created desc limit '+str(frompageCount)+','+str(limitNum)
        resultlist=self.dbc.fetchalldb(sql,argument)
        none1=1
        none2=1
        listall=[]
        for result in resultlist:
            id=result[0]
            company_id=result[1]
            crm_service_code=result[2]
            crm_service=self.getcrmservicetype(crm_service_code)
            gmt_start=formattime(result[3])
            gmt_end=formattime(result[4])
            apply_status=result[5]
            if str(apply_status)=="1":
                apply_statustext='已经开通'
            else:
                apply_statustext='未开通'
            remark=result[6]
            membership_code=result[8]
            zst_year=result[9]
            if not zst_year:
                zst_year=0
            companyname=result[10]
            account=result[11]
            mobile=result[12]
            list={'id':id,'company_id':company_id,'crm_service':crm_service,'gmt_start':gmt_start,'gmt_end':gmt_end,'apply_statustext':apply_statustext,'remark':remark,'membership_code':membership_code,'zst_year':zst_year,'company_name':companyname,'account':account,'mobile':mobile,'apply_status':apply_status}
            listall.append(list)
        return {'list':listall,'count':count}
            
            
    #申请服务类型
    def getcrmservicetype(self,code):
        sql="select name from crm_service where code=%s"
        result=self.dbc.fetchonedb(sql,[code])
        if result:
            return result[0]
    def getcompany_name(self,company_id):
        sql='select name from company where id=%s'
        if company_id:
            result=self.dbc.fetchonedb(sql,company_id)
            if result:
                return result[0]
        else:
            return None
    def getproduct_title(self,proid):
        sql='select title from products where id=%s'
        result=self.dbc.fetchonedb(sql,[proid])
        if result:
            return result[0]
    def getcompany_id(self,account='',mobile=''):
        argument=[]
        if account:
            argument=[account]
        if mobile:
            argument=[mobile]
        sql='select company_id from company_account where account=%s'
        if argument:
            result=self.dbc.fetchonedb(sql,argument)
            if result:
                return result[0]
    def getcompanyaccount(self,company_id):
        sql="select account from company_account where company_id=%s"
        result=self.dbc.fetchonedb(sql,[company_id])
        if result:
            return result[0]
    def getftypename(self,id):
        sql='select name from pay_wallettype where id=%s'
        result=self.dbc.fetchonedb(sql,[id])
        if result:
            return result[0]
        else:
            return "无"
    def getftypefee(self,id):
        sql='select fee from pay_wallettype where id=%s'
        result=self.dbc.fetchonedb(sql,[id])
        if result:
            return result[0]
    def getpaytypelist(self,frompageCount=0,limitNum=200,paytype='',subid=''):
        sqlarg=''
        if paytype==1:
            sqlarg+=' and fee>=0'
        elif paytype==2:
            sqlarg+=' and fee<0'
        if subid:
            sqlarg+=' and subid='+str(subid)+''
        sql1='select count(0) from pay_wallettype where id>0 '+sqlarg
        sql='select id,name,fee,sortrank,subid from pay_wallettype where id>0 '+sqlarg
        count=self.dbc.fetchnumberdb(sql1)
        sql=sql+' order by sortrank,id limit '+str(frompageCount)+','+str(limitNum)
        resultlist=self.dbc.fetchalldb(sql)
        listall=[]
        for result in resultlist:
            id=result[0]
            name=result[1]
            fee=result[2]
            sortrank=result[3]
            subid=result[4]
            subname=self.getftypename(subid)
            list={'id':id,'name':name,'fee':fee,'sortrank':sortrank,'subid':subid,'subname':subname}
            listall.append(list)
        return {'list':listall,'count':count}
    def getreportlist(self,frompageCount,limitNum,ischeck='',gmtdate='',account='',foraccount=''):
        company_id=None
        forcompany_id=None
        if account:
            sqlc="select company_id from company_account where account=%s"
            result=self.dbc.fetchonedb(sqlc,[account])
            if result:
                company_id=result[0]
        if foraccount:
            sqlc="select company_id from company_account where account=%s"
            result=self.dbc.fetchonedb(sqlc,[foraccount])
            if result:
                forcompany_id=result[0]
        sql1='select count(0) from pay_report where id>0'
        sql='select id,content,company_id,forcompany_id,product_id,gmt_created,check_status from pay_report where id>0'
        argument=[]
        if ischeck:
            sql1=sql1+' and check_status=%s'
            sql=sql+' and check_status=%s'
            argument.append(ischeck)
        if gmtdate:
            sql1=sql1+' and gmt_date=%s'
            sql=sql+' and gmt_date=%s'
            argument.append(gmtdate)
        if forcompany_id:
            sql1=sql1+' and forcompany_id=%s'
            sql=sql+' and forcompany_id=%s'
            argument.append(forcompany_id)
        if company_id:
            sql1=sql1+' and company_id=%s'
            sql=sql+' and company_id=%s'
            argument.append(company_id)
            
        count=self.dbc.fetchnumberdb(sql1,argument)
        sql=sql+' order by gmt_created desc limit '+str(frompageCount)+','+str(limitNum)
        resultlist=self.dbc.fetchalldb(sql,argument)
        listall=[]
        for result in resultlist:
            id=result[0]
            contents=result[1]
            content=self.getjubaocontent(contents)
            company_id=result[2]
            company_name=self.getcompany_name(company_id)
            forcompany_id=result[3]
            forcompany_name=self.getcompany_name(forcompany_id)
            product_id=result[4]
            pro_title=self.getproduct_title(product_id)
            gmt_created=formattime(result[5])
            check_status=result[6]
            if check_status==0:
                check_name='未处理'
            if check_status==1:
                check_name='已处理'
            if check_status==2:
                check_name='退回'
            list={'id':id,'content':content,'company_id':company_id,'company_name':company_name,'forcompany_id':forcompany_id,'forcompany_name':forcompany_name,'product_id':product_id,'pro_title':pro_title,'gmt_created':gmt_created,'check_status':check_status,'check_name':check_name}
            listall.append(list)
        return {'list':listall,'count':count}
    def getjubaocontent(self,contents):
        jubaotypelist=['违法违规','虚假信息','过期信息','虚假号码']
        jubaocontent=''
        if contents:
            if ',' in contents:
                contentlist=contents.split(',')
                for content in contentlist:
                    if content:
                        try:
                            jubaocontent+=jubaotypelist[int(content)-1]+','
                        except:
                            pass
            else:
                if contents.isdigit()==True:
                    jubaocontent=jubaotypelist[int(contents)-1]
                else:
                    jubaocontent=contents
        return jubaocontent
    #是否为来电宝
    def isldb(self,company_id):
        sqll="select id from crm_company_service where company_id=%s and crm_service_code in ('1007','1008','1009','1010')  and apply_status=1 and DATEDIFF(CURDATE(),`gmt_end`)<=0"
        ldbresult=self.dbc.fetchonedb(sqll,[company_id])
        if ldbresult:
            sqlg="select id from phone where company_id=%s and expire_flag=0"
            phoneresult=self.dbc.fetchonedb(sqlg,[company_id])
            if phoneresult:
                return 1
            else:
                return None
        else:
            return None
                
    def getbackfee(self,report_id,backfee=None):
        sql='select company_id,forcompany_id,product_id from pay_report where id=%s'
        result=self.dbc.fetchonedb(sql,[report_id])
        if result:
            company_id=result[0]
            forcompany_id=result[1]
            product_id=result[2]
            gmt_date=datetime.date.today()
            gmt_created=datetime.datetime.now()
            fee3=self.getftypefee(3)
            fee4=self.getftypefee(4)
            fee5=self.getftypefee(15)
            isldbflag=self.isldb(company_id)
            if isldbflag:
                sql='select id,amount from phone where company_id=%s and expire_flag=0'
                result=self.dbc.fetchonedb(sql,[company_id])
                lave=0
                if result:
                    #退回查看金额 到来电宝
                    lave=int(result[1])+5
                    lid=result[0]
                    sql1="update phone set amount=%s where id=%s"
                    result1=self.dbc.updatetodb(sql1,[lave,lid])
                    #分成退回
                    argument=[forcompany_id,company_id,product_id,fee5,15,gmt_date,gmt_created,gmt_created]
                    sql='insert into pay_mobileWallet(company_id,forcompany_id,product_id,fee,ftype,gmt_date,gmt_created,gmt_modified) values(%s,%s,%s,%s,%s,%s,%s,%s)'
                    self.dbc.updatetodb(sql,argument)
            else:
                #退回查看金额
                argument=[company_id,forcompany_id,product_id,fee3,3,gmt_date,gmt_created,gmt_created]
                sql='insert into pay_mobileWallet(company_id,forcompany_id,product_id,fee,ftype,gmt_date,gmt_created,gmt_modified) values(%s,%s,%s,%s,%s,%s,%s,%s)'
                self.dbc.updatetodb(sql,argument)
                if self.getiszstcompany(forcompany_id)==None and str(backfee)=="1":
                    #罚款
                    argument=[forcompany_id,company_id,product_id,fee4,4,gmt_date,gmt_created,gmt_created]
                    sql='insert into pay_mobileWallet(company_id,forcompany_id,product_id,fee,ftype,gmt_date,gmt_created,gmt_modified) values(%s,%s,%s,%s,%s,%s,%s,%s)'
                    self.dbc.updatetodb(sql,argument)
                #分成退回
                argument=[forcompany_id,company_id,product_id,fee5,15,gmt_date,gmt_created,gmt_created]
                sql='insert into pay_mobileWallet(company_id,forcompany_id,product_id,fee,ftype,gmt_date,gmt_created,gmt_modified) values(%s,%s,%s,%s,%s,%s,%s,%s)'
                self.dbc.updatetodb(sql,argument)
                
            sql='update pay_report set check_status=%s where id=%s'
            self.dbc.updatetodb(sql,[1,report_id])
    def getchartinfee(self,ftype='',gmt_begin='',gmt_end='',limit=31):
        argument=[ftype]
        sqlarg=''
        if gmt_begin:
            sqlarg+=' and gmt_date>=%s'
            argument.append(gmt_begin)
        if gmt_end:
            sqlarg+=' and gmt_date<=%s'
            argument.append(gmt_end)
        sql='select sum(fee),gmt_date from pay_mobileWallet where ftype=%s'+sqlarg
        sql+=' group by gmt_date order by gmt_date desc limit 0,'+str(limit)
        resultlist=self.dbc.fetchalldb(sql,argument)
        listall=[]
        for result in resultlist[::-1]:
            fee=result[0]
            gmt_date=formattime(result[1],1)
            list={'fee':fu_to_zheng(fee),'gmt_date':gmt_date}
            listall.append(list)
        return listall
    def getqianbao_gglist(self,frompageCount,limitNum):
        sql='select id,begin_time,end_time,infee,sendfee,txt from qianbao_gg'
        sql+=' order by id limit '+str(frompageCount)+','+str(limitNum)
        sql1='select count(0) from qianbao_gg'
        count=self.dbc.fetchnumberdb(sql1)
        resultlist=self.dbc.fetchalldb(sql)
        listall=[]
        for result in resultlist:
            id=result[0]
            begin_time=formattime(result[1],1)
            end_time=formattime(result[2],1)
            infee=result[3]
            sendfee=result[4]
            txt=result[5]
            list={'id':id,'begin_time':begin_time,'end_time':end_time,'infee':infee,'sendfee':sendfee,'txt':txt}
            listall.append(list)
        return {'list':listall,'count':count}
    def qianbaoblancelist(self,frompageCount,limitNum,gmtdate='',gmt_begin='',gmt_end='',paytypeid='',company_name='',account='',mobile='',order=''):
        argument=[]
        if order=="fee" or order=="fee desc":
            sqlarg=' from pay_mobileWallet as a left join company as b on a.company_id=b.id left join company_account as c on a.company_id=c.company_id where a.id>0'
        else:
            sqlarg=' from pay_mobileWallet as a left join company as b on a.company_id=b.id left join company_account as c on a.company_id=c.company_id where a.ftype=5'
        sqlarg2=' from pay_mobileWallet as a left join company as b on a.company_id=b.id left join company_account as c on a.company_id=c.company_id where a.id>0'
        
        if gmtdate:
            sqlarg+=' and a.gmt_date=%s'
            sqlarg2+=' and a.gmt_date=%s'
            argument.append(gmtdate)
        if gmt_begin:
            sqlarg+=' and a.gmt_date>=%s'
            sqlarg2+=' and a.gmt_date>=%s'
            argument.append(gmt_begin)
        if gmt_end:
            sqlarg+=' and a.gmt_date<=%s'
            sqlarg2+=' and a.gmt_date<=%s'
            argument.append(gmt_end)
        if paytypeid:
            sqlarg+=' and a.ftype=%s'
            sqlarg2+=' and a.ftype=%s'
            argument.append(paytypeid)
        if company_name:
            sqlarg+=' and b.name=%s'
            sqlarg2+=' and b.name=%s'
            argument.append(company_name)
        if account:
            sqlarg+=' and c.account=%s'
            sqlarg2+=' and c.account=%s'
            argument.append(account)
        if mobile:
            sqlarg+=' and c.mobile=%s'
            sqlarg2+=' and c.mobile=%s'
            argument.append(mobile)
        sql='select a.id,a.company_id,sum(a.fee) as infee,a.ftype,a.gmt_created,b.name,c.account,c.mobile'+sqlarg
        sql1='select count(distinct a.company_id)'+sqlarg
        sql2='select sum(a.fee)'+sqlarg2
        sql3=sql2+' and a.ftype=5'
        sql4=sql2+' and a.ftype in (6,7)'
        count=self.dbc.fetchnumberdb(sql1,argument)
        countall=self.dbc.fetchnumberdb(sql2,argument)
        countin=self.dbc.fetchnumberdb(sql3,argument)
        countiyan=self.dbc.fetchnumberdb(sql4,argument)
        if not countiyan:
            countiyan=0
        countall-=countiyan
        sql+=' group by a.company_id'
        if order:
            if order=="fee":
                sql+=' order by sum(a.fee) asc'
            elif order=="fee desc":
                sql+=' order by sum(a.fee) desc'
            else:
                sql+=' order by '+order
        else:
            sql+=' order by a.gmt_created'
        sql+=' limit '+str(frompageCount)+','+str(limitNum)
        resultlist=self.dbc.fetchalldb(sql,argument)
        listall=[]
        for result in resultlist:
            id=result[0]
            company_id=result[1]
            infee=result[2]
            if order=="fee" or order=="fee desc":
                infee=self.getqianbaoblance(company_id,ftype=5)
            fee=self.getqianbaoblance(company_id)
            ftype=result[3]
            ftypename=self.getftypename(ftype)
            gmt_created=formattime(result[4])
            company_name=result[5]
            account=result[6]
            mobile=result[7]
            list={'id':id,'company_id':company_id,'company_name':company_name,'account':account,'mobile':mobile,'infee':infee,'fee':fee,'ftype':ftype,'ftypename':ftypename,'gmt_created':gmt_created}
            listall.append(list)
        return {'list':listall,'count':count,'countin':countin,'countall':countall}
    
    def getqianbaoblance(self,company_id,ftype=""):
        sql='select sum(fee) from pay_mobileWallet where company_id=%s'
        if ftype:
            sql+=" and ftype="+str(ftype)+""
        result=self.dbc.fetchonedb(sql,[company_id])[0]
        if result:
            if result<=0:
                return '0.00'
            else:
                return '%.2f'%result
        return '0.00'
    def getpaytypemlist(self):
        sql="select code,label from category where code like '2006____'"
        result=self.dbc.fetchalldb(sql)
        listall=[]
        if result:
            for list in result:
                lis={'code':list[0],'label':list[1]}
                listall.append(lis)
        return listall
    #----判断是否为再生通
    def getiszstcompany(self,company_id):
        if company_id:
            sqll="select id from crm_company_service where company_id=%s and crm_service_code='1000' and apply_status=1 and DATEDIFF(CURDATE(),`gmt_end`)<=0"
            zstresult=self.dbc.fetchonedb(sqll,[company_id])
            if zstresult:
                return 1
            else:
                return None
        else:
            return None
        
    #--砍价报名列表
    def getkanjiabaoming(self,frompageCount="",limitNum="",pro_id=""):
        argument=[]
        sqlarg=''
        if pro_id:
            sqlarg+=' and pro_id=%s'
            argument.append(pro_id)
        sql='select id,company_id,pro_id,price_now,payflag,gmt_created from subject_kanjia_baoming where id>0'+sqlarg
        sql+=' order by id limit '+str(frompageCount)+','+str(limitNum)
        sql1='select count(0) from subject_kanjia_baoming where id>0'+sqlarg
        count=self.dbc.fetchnumberdb(sql1,argument)
        resultlist=self.dbc.fetchalldb(sql,argument)
        listall=[]
        for result in resultlist:
            id=result[0]
            gmt_created=formattime(result[5],1)
            company_id=result[1]
            price_now=result[3]
            payflag=result[4]
            company_name=self.getcompany_name(company_id)
            sqlc="select count(0) from subject_kanjia_havecut where baoming_id=%s"
            resultc=self.dbc.fetchonedb(sqlc,[id])
            cutcount=resultc[0]
            list={'id':id,'company_name':company_name,'gmt_created':gmt_created,'company_id':company_id,'price_now':price_now,'payflag':payflag,'cutcount':cutcount}
            listall.append(list)
        return {'list':listall,'count':count}
    #--砍价报名列表
    def getkanjiacutlist(self,frompageCount="",limitNum="",baoming_id=""):
        argument=[]
        sqlarg=''
        if baoming_id:
            sqlarg+=' and baoming_id=%s'
            argument.append(baoming_id)
        sql='select id,weixinid,pro_id,baoming_id,price_cut,gmt_created from subject_kanjia_havecut where id>0'+sqlarg
        sql+=' order by id limit '+str(frompageCount)+','+str(limitNum)
        sql1='select count(0) from subject_kanjia_havecut where id>0'+sqlarg
        count=self.dbc.fetchnumberdb(sql1,argument)
        resultlist=self.dbc.fetchalldb(sql,argument)
        listall=[]
        for result in resultlist:
            id=result[0]
            gmt_created=formattime(result[5],1)
            weixinid=result[1]
            pro_id=result[2]
            price_cut=result[4]
            list={'id':id,'pro_id':pro_id,'gmt_created':gmt_created,'price_cut':price_cut,'weixinid':weixinid}
            listall.append(list)
        return {'list':listall,'count':count}