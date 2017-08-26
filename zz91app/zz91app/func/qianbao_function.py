#-*- coding:utf-8 -*-
class mshop:
    def __init__(self):
        self.dbc=dbc
    def getis_wxtg(self,company_id):
        sql='select id from shop_product where company_id=%s and is_check=0'
        result=self.dbc.fetchonedb(sql,[company_id])
        if result:
            return result[0]
class zzqianbao:
    #----初始化ast数据库
    def __init__(self):
        self.dbc=dbc
    def getviptype(self,company_id):
        sql='select membership_code from company where id=%s'
        result=self.dbc.fetchonedb(sql,[company_id])
        if result:
            return result[0]
    #首次安装或钱包
    def firstsendfee(self,company_id,appid):
        if appid:
            sqlc="select id from oauth_access where open_id=%s and open_type='app.zz91.com'"
            list=self.dbc.fetchonedb(sqlc,[str(appid)])
            if not list:
                self.getsendfee(company_id,20,12)
    def getsendfee(self,company_id,fee,ftype,more=""):
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
        if (payinsert==1):
            sql='select id from pay_mobileWallet where company_id=%s and ftype=%s'
            result=self.dbc.fetchonedb(sql,[company_id,ftype])
            if not result:
                if not ftype:
                    ftype=6
                if not fee:
                    fee=20
                gmt_date=datetime.date.today()
                gmt_created=datetime.datetime.now()
                
                sql2='insert into pay_mobileWallet(company_id,fee,ftype,gmt_date,gmt_created,gmt_modified) values(%s,%s,%s,%s,%s,%s)'
                self.dbc.updatetodb(sql2,[company_id,fee,ftype,gmt_date,gmt_created,gmt_created])
            else:
                
                #多次获得钱包
                if more and more!="None":
                    gmt_date=datetime.date.today()
                    gmt_created=datetime.datetime.now()
                    #判断当天最大进账数
                    insertfee=0
                    nowfeeall=self.getinfeedate(company_id,gmt_begin=gmt_date,ftype="("+str(ftype)+")")
                    if not nowfeeall:
                        nowfeeall=0
                    if float(maxfee)>0:
                        if float(nowfeeall)<float(maxfee):
                            insertfee=1
                    else:
                        insertfee=1
                    if insertfee==1:
                        sql2='insert into pay_mobileWallet(company_id,fee,ftype,gmt_date,gmt_created,gmt_modified) values(%s,%s,%s,%s,%s,%s)'
                        self.dbc.updatetodb(sql2,[company_id,fee,ftype,gmt_date,gmt_created,gmt_created])
        
    def getcompanycontact(self,company_id):
        sql='select contact,mobile from company_account where company_id=%s'
        result=self.dbc.fetchonedb(sql,[company_id])
        list={'contact':'','mobile':''}
        if result:
            contact=result[0]
            mobile=result[1]
            if mobile:
                mobile=mobile[0:11]
            list={'contact':contact,'mobile':mobile}
        return list
    #收支明细
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
        sql='select id,fee,ftype,gmt_date,product_id,forcompany_id from pay_mobileWallet where company_id=%s'+sqlarg
        sql=sql+' order by gmt_created desc limit '+str(frompageCount)+','+str(limitNum)
        count=self.dbc.fetchnumberdb(sql1,argument)
        resultlist=self.dbc.fetchalldb(sql,argument)
        listall=[]
        for result in resultlist:
            id=result[0]
            fee=result[1]
            if fee>0:
                fee='+'+str('%.2f'%fee)
            else:
                fee=('%.2f'%fee)
            ftype=result[2]
            gmt_date=formattime(result[3],1)
            product_id=result[4]
            forcompany_id=result[5]
            forcompanyname=""
            if forcompany_id:
                if str(ftype)=="1":
                    forcompanyname=self.getcompanyname(forcompany_id)
            ftypename=self.getftypename(ftype)
            list={'id':id,'fee':fee,'ftype':ftype,'gmt_date':gmt_date,'ftypename':ftypename,'product_id':product_id,'forcompany_id':forcompany_id,'forcompanyname':forcompanyname}
            listall.append(list)
        return {'list':listall,'count':count}
    def getcompanyname(self,company_id):
        sql="select name from company where id=%s"
        result=self.dbc.fetchonedb(sql,[company_id])
        if result:
            return result[0]
    def getftypename(self,id):
        sql='select name from pay_wallettype where id=%s'
        result=self.dbc.fetchonedb(sql,[id])
        if result:
            return result[0]
    #钱包类型
    def getftypelist(self,subid):
        sql='select id,name,fee from pay_wallettype where subid=%s'
        result=self.dbc.fetchalldb(sql,[subid])
        if result:
            listall=[]
            for l in result:
                list={'id':l[0],'name':l[1],'fee':l[2]}
                listall.append(list)
            return listall
    def getqianbaoblance(self,company_id,jingjia=''):
        if jingjia:
            sql='select sum(fee) from pay_mobileWallet where company_id=%s'
        else:
            sql='select sum(fee) from pay_mobileWallet where company_id=%s '
        result=self.dbc.fetchonedb(sql,[company_id])[0]
        if result:
            if result<=0:
                return '0.00'
            else:
                return '%.2f'%result
        return '0.00'
    def getqianbaoblance2(self,company_id):
        sql='select sum(fee) from pay_mobileWallet where company_id=%s '
        result=self.dbc.fetchonedb(sql,[company_id])[0]
        if result:
            return result
        return 0.0
    def getpayfee(self,company_id="",forcompany_id="",product_id="",ftype="",more=None,fee=None):
        #----判断该客户是被送了20元
        sql4='select id from pay_mobileWallet where company_id=%s and ftype=6'
        idsend20=self.dbc.fetchonedb(sql4,[company_id])
        if idsend20:
            #----手机钱包开张送20活动,优先扣这20元
            sql3='select sum(fee) from pay_mobileWallet where company_id=%s and fee<0'
            outfeeall=self.dbc.fetchonedb(sql3,[company_id])[0]
            if not outfeeall:
                outfeeall=0.0
            if ftype=='1' and outfeeall>-20:
                ftype='7'
        if not fee:
            fee=self.getpay_wallettypefee(ftype)
        if not fee:
            return "nomoney"
        if more:
            sql='select id from pay_mobileWallet where company_id=%s and ftype=%s'
            result=self.dbc.fetchonedb(sql,[company_id,ftype])
            if result:
                return "havepay"
        #----账户余额大于当前消费金额才可以进行交易
        sql4='select sum(fee) from pay_mobileWallet where company_id=%s'
        blance=self.dbc.fetchonedb(sql4,[company_id])[0]
        if not product_id:
            product_id=0
        if blance>=-fee:
            gmt_date=datetime.date.today()
            gmt_created=datetime.datetime.now()
            if str(ftype) in ['1','7']:
                sql="select id from pay_mobileWallet where company_id=%s and forcompany_id=%s and ftype=1"
                resultpay=self.dbc.fetchonedb(sql,[company_id,forcompany_id])
                if not resultpay:
                    argument=[company_id,forcompany_id,product_id,fee,ftype,gmt_date,gmt_created,gmt_created]
                    sql='insert into pay_mobileWallet(company_id,forcompany_id,product_id,fee,ftype,gmt_date,gmt_created,gmt_modified) values(%s,%s,%s,%s,%s,%s,%s,%s)'
                    self.dbc.updatetodb(sql,argument)
                    if ftype in ['1','7']:
                        argument2=[forcompany_id,company_id,product_id,0.5,2,gmt_date,gmt_created,gmt_created]
                        sql2='insert into pay_mobileWallet(company_id,forcompany_id,product_id,fee,ftype,gmt_date,gmt_created,gmt_modified) values(%s,%s,%s,%s,%s,%s,%s,%s)'
                        self.dbc.updatetodb(sql2,argument2)
            else:
                argument=[company_id,forcompany_id,product_id,fee,ftype,gmt_date,gmt_created,gmt_created]
                sql='insert into pay_mobileWallet(company_id,forcompany_id,product_id,fee,ftype,gmt_date,gmt_created,gmt_modified) values(%s,%s,%s,%s,%s,%s,%s,%s)'
                self.dbc.updatetodb(sql,argument)
            return 1
        else:
            return "nomoney"
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
        iszst=self.getiszstcompany(company_id)
        if iszst:
            return 2
        isbuyshowphone=self.getisbuyshowphone(forcompany_id)
        if isbuyshowphone:
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
        sql='select id from pay_mobileWallet where company_id=%s and forcompany_id=%s and ftype=1'
        result=self.dbc.fetchonedb(sql,[company_id,forcompany_id])
        if result:
            return 1
    #购买供求刷新服务
    def buyreflushtrade(self,company_id,money):
        gmt_end=''
        gmt_created=datetime.datetime.now()
        gmt_date=datetime.date.today()
        sql2='select id,UNIX_TIMESTAMP(gmt_end) from shop_reflush where company_id=%s and DATEDIFF(CURDATE(),gmt_end)<=0 order by id desc'
        result=self.dbc.fetchonedb(sql2,[company_id])
        if result:
            gmt_begin=result[1]
        else:
            gmt_begin=int(time.time())
        if money:
            gmt_end=gmt_begin-(3600*24*30*int(money))
        gmt_begin=int_to_datetime(gmt_begin)
        gmt_end=int_to_datetime(gmt_end)
        sql='insert into shop_reflush(company_id,gmt_begin,gmt_end,gmt_created,gmt_date) values(%s,%s,%s,%s,%s)'
        result=self.dbc.updatetodb(sql,[company_id,gmt_begin,gmt_end,gmt_created,gmt_date])
        return result[0]
    #购买显示联系方式
    def buyshowcontact(self,company_id,money,datevalue=""):
        gmt_end=''
        gmt_created=datetime.datetime.now()
        gmt_date=datetime.date.today()
        sql2='select id,UNIX_TIMESTAMP(gmt_end) from shop_showphone where company_id=%s and DATEDIFF(CURDATE(),gmt_end)<=0 order by id desc'
        result=self.dbc.fetchonedb(sql2,[company_id])
        if result:
            gmt_begin=result[1]
        else:
            gmt_begin=int(time.time())
        if datevalue:
            money=int("-"+str(datevalue))
        if money==-300:
            gmt_end=gmt_begin+(3600*24*30)
        if money==-500:
            gmt_end=gmt_begin+(3600*24*30*2)
        if money==-1500:
            gmt_end=gmt_begin+(3600*24*30*6)
        if money==-3000:
            gmt_end=gmt_begin+(3600*24*365)
        gmt_begin=int_to_datetime(gmt_begin)
        gmt_end=int_to_datetime(gmt_end)
        sql='insert into shop_showphone(company_id,gmt_begin,gmt_end,gmt_created,gmt_date) values(%s,%s,%s,%s,%s)'
        result=self.dbc.updatetodb(sql,[company_id,gmt_begin,gmt_end,gmt_created,gmt_date])
        return result[0]
    #购买企业秀
    def buyqiyexiu(self,company_id,datediff,xiumovalue="h1"):
        gmt_end=''
        gmt_created=gmt_modified=datetime.datetime.now()
        gmt_date=datetime.date.today()
        sql="select id,UNIX_TIMESTAMP(gmt_end) from crm_company_service where company_id=%s and crm_service_code='10001009' and apply_status=1 and DATEDIFF(CURDATE(),`gmt_end`)<=0 order by id desc"
        result=self.dbc.fetchonedb(sql,[company_id])
        if result:
            gmt_start=result[1]
        else:
            gmt_start=int(time.time())
            
        if datediff:
            gmt_end=gmt_start+(3600*24*30*int(datediff))
        if gmt_end:
            gmt_start=int_to_datetime(gmt_start)
            gmt_end=int_to_datetime(gmt_end)
            crm_service_code="10001009"
            gmt_signed=gmt_created
            apply_status=1
            remark="app自动开通服务"
            mobile_templates="03"
            sql='insert into crm_company_service(company_id,crm_service_code,gmt_signed,gmt_start,gmt_end,apply_status,remark,gmt_created,gmt_modified,mobile_templates) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
            result=self.dbc.updatetodb(sql,[company_id,crm_service_code,gmt_signed,gmt_start,gmt_end,apply_status,remark,gmt_created,gmt_modified,mobile_templates])
            
            if xiumovalue:
                sql="select id from crm_service_qiyexiu where company_id=%s"
                result1=self.dbc.fetchonedb(sql,[company_id])
                if not result1:
                    sql="insert into crm_service_qiyexiu(company_id,css,html) values(%s,%s,%s)"
                    result=self.dbc.updatetodb(sql,[company_id,xiumovalue,xiumovalue])
            return result[0]
    #供求置顶服务
    def getprotop(self,company_id,datediff,keywords,product_id):
        gmt_end=''
        gmt_created=gmt_modified=datetime.datetime.now()
        gmt_date=datetime.date.today()
        sql="select id,UNIX_TIMESTAMP(end_time) from products_keywords_rank where company_id=%s and type='10431004' and is_checked=1 and DATEDIFF(CURDATE(),`end_time`)<=0 order by id desc"
        result=self.dbc.fetchonedb(sql,[company_id])
        if result:
            gmt_start=result[1]
        else:
            gmt_start=int(time.time())
            
        if datediff:
            gmt_end=gmt_start+(3600*24*30*int(datediff))
        if gmt_end:
            start_time=int_to_datetime(gmt_start)
            end_time=int_to_datetime(gmt_end)
            type="10431004"
            buy_time=gmt_created
            is_checked=1
            name=keywords
            apply_account=self.getcompanyaccount(company_id)
            bz="app自动开通服务"
            sql='insert into products_keywords_rank(product_id,company_id,type,buy_time,start_time,end_time,is_checked,bz,gmt_created,gmt_modified,name,apply_account) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
            result=self.dbc.updatetodb(sql,[product_id,company_id,type,buy_time,start_time,end_time,is_checked,bz,gmt_created,gmt_modified,name,apply_account])
            return result[0]
    def getcompanyaccount(self,company_id):
        sql="select account from company_account where company_id=%s"
        result=self.dbc.fetchonedb(sql,[company_id])
        if result:
            return result[0]
    #--是否企业秀
    def getisqiyexiu(self,company_id):
        if company_id:
            sql="select id,UNIX_TIMESTAMP(gmt_end) from crm_company_service where company_id=%s and crm_service_code='10001009' and apply_status=1 and DATEDIFF(CURDATE(),`gmt_end`)<=0 order by id desc"
            result=self.dbc.fetchonedb(sql,[company_id])
            if result:
                return 1
            else:
                return None
        else:
            return None
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
    def getinfeegmt(self,company_id,gmt_begin='',gmt_end='',ftype='',notftype=''):
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
        if notftype:
            sql=sql.replace('and ftype=2','')
            sql+=' and ftype not in '+notftype+''
        result=self.dbc.fetchonedb(sql,argument)[0]
        if result:
            return '%.2f'%result
        return 0.0
    def getinfeedate(self,company_id,gmt_begin='',ftype='',notftype=''):
        sql='select sum(fee) from pay_mobileWallet where company_id=%s and fee>0 and ftype=2'
        argument=[company_id]
        if gmt_begin:
            argument.append(gmt_begin)
            sql+=' and gmt_date=%s'
        if ftype:
            sql=sql.replace('and ftype=2',' and ftype in '+ftype)
        if notftype:
            sql=sql.replace('and ftype=2','')
            sql+=' and ftype not in '+notftype+''
        result=self.dbc.fetchonedb(sql,argument)[0]
        if not result:
            result=0
        return result
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
            return '%.2f'%float(str(result)[1:])
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
        sql='select sum(fee) from pay_mobileWallet where company_id=%s and fee<0'
        result=self.dbc.fetchonedb(sql,[company_id])[0]
        if result:
            return '%.2f'%float(str(result)[1:])
        return '0.00'
    #判断首次安装app时间
    def getfistinstallapp(self,account):
        sql="select id from oauth_access where open_type='app.zz91.com' and DATEDIFF(CURDATE(),gmt_created)<=7 and target_account=%s and closeflag=0"
        result=self.dbc.fetchonedb(sql,[account])
        if result:
            return 1
        else:
            return None
    #查看商品表
    def listgoods(self,frompageCount,limitNum,ptype=None,goodsNmae=None,ad_type=None):
        #a=["已上架"]
        #b=["已上架"]
        argument=[]
        sqlarg=''
        if ptype:
            if (ptype=="1"):
                sqlarg+=" and status=1"
            elif (ptype=="0"):
                sqlarg+=" and status=0"
            elif (ptype=="2"):
                sqlarg+=" and tuijian=1"
            elif (ptype=="3"):
                sqlarg+=" and tuijian=0"
        if goodsNmae:
            sqlarg+=' and goodsName=%s'
            argument.append(goodsNmae)
        if ad_type:
            if (ad_type=="1"):
                sqlarg+=" and ad_type=1"
            elif (ad_type=="2"):
                sqlarg+=" and ad_type=2"
            elif (ad_type=="3"):
                sqlarg+=" and ad_type=3"
            elif (ad_type=="4"):
                sqlarg+=" and ad_type=4"
                 
        sql1='select count(0) from app_goods where status=1'+sqlarg
        sql='select id,goodsName,billing_Class_ID,start_Time,end_Time,original_Price,present_Price,sales_Num,left_Num,pic,status,release_Time,tuijian,goodsname_fu,tourl,ad_type,ad_position,havenum,DATEDIFF(end_Time,CURDATE()) from app_goods where status=1 '+sqlarg
        sql=sql+' order by start_Time desc limit '+str(frompageCount)+','+str(limitNum)
        count=self.dbc.fetchnumberdb(sql1,argument)
        resultlist=self.dbc.fetchalldb(sql,argument)
        listall=[]
        statustxt=''
        tuijiantxt=''
        for result in resultlist:
            id=result[0]
            goodsName=result[1]
            goodsname_fu=result[13]
            billing_Class_ID=result[2]
            billingname=self.getftypename(billing_Class_ID)
            start_Time=formattime(result[3],1)
            end_Time=formattime(result[4],1)
            original_Price=result[5]
            present_Price=result[6]
            sales_Num=result[7]
            left_Num=result[8]
            pic=result[9]
            status=str(result[10])
            statustxt=""
            if status=="0":
                statustxt='已下架'
            if status=="1":
                statustxt='已上架'
            release_Time=formattime(result[11],0)
            tuijian=str(result[12])
            tuijiantxt=""
            if tuijian=="1":
                tuijiantxt='已推荐'
            if tuijian=="0":
                tuijiantxt='未推荐'
            tourl=result[14]
            ad_type=str(result[15])
            adtypetext=""
            if ad_type=="1":
                adtypetext="优质推荐"
            if ad_type=="2":
                adtypetext="每日抢购"
            if ad_type=="3":
                adtypetext="热门产品"
            if ad_type=="4":
                adtypetext="热门品牌"
            ad_position=result[16]
            havenum=result[17]
            difftime=result[18]
            if difftime>0:
                difftext="<p style='color: #F1C40F'>活动截止："+str(difftime)+"天后结束</p>"
                if end_Time[0:4]=="9999":
                    difftext=""
            else:
                difftext="<p style='color: #ff0000'>活动已结束</p>"
            if not havenum:
                havenum=5
            list={'id':id,'goodsName':goodsName,'goodsname_fu':goodsname_fu,'billing_Class_ID':billing_Class_ID,'start_Time':start_Time,'end_Time':end_Time,'original_Price':original_Price,'present_Price':present_Price,'sales_Num':sales_Num,'left_Num':left_Num,'pic':pic,'statustxt':statustxt,'release_Time':release_Time,'billingname':billingname,'tuijiantxt':tuijiantxt,'tourl':tourl,'ad_type':ad_type,'adtypetext':adtypetext,'ad_position':ad_position,'havenum':havenum,'difftime':difftext}
            listall.append(list)
        return {'list':listall,'count':count}
    #---首页广告模块-
    def getadgoods(self,bclassid="",adtype="",adposition="",gid=""):
        sevalue=[]
        list=None
        sql="select id,goodsName,billing_Class_ID,start_Time,end_Time,original_Price,present_Price,sales_Num,left_Num,pic,status,release_Time,tuijian,goodsname_fu,tourl,ad_type,ad_position,havenum from app_goods where id>0 and status=1"
        if bclassid:
            sql+=" and billing_Class_ID=%s "
            sevalue.append(int(bclassid))
        if adtype:
            sql+=" and ad_type=%s "
            sevalue.append(int(adtype))
        if adposition:
            sql+=" and ad_position=%s "
            sevalue.append(int(adposition))
        if gid:
            sql+=" and id=%s "
            sevalue.append(int(gid))
        sql+=" order by start_Time asc"
        result=self.dbc.fetchonedb(sql,sevalue)
        if result:
            id=result[0]
            goodsName=result[1]
            goodsname_fu=result[13]
            if not goodsname_fu:
                goodsname_fu=""
            billing_Class_ID=result[2]
            start_Time=formattime(result[3],0)
            end_Time=formattime(result[4],0)
            original_Price=result[5]
            present_Price=result[6]
            sales_Num=result[7]
            left_Num=result[8]
            pic=result[9]
            if not pic:
                pic=""
            else:
                pic="http://img3.zz91.com/300x200/"+pic.replace("http://img1.zz91.com/","")
            status=str(result[10])
            statustxt=""
            if status=="0":
                statustxt='已下架'
            if status=="1":
                statustxt='已上架'
            release_Time=formattime(result[11],0)
            tuijian=str(result[12])
            tuijiantxt=""
            if tuijian=="1":
                tuijiantxt='已推荐'
            if tuijian=="0":
                tuijiantxt='未推荐'
            tourl=result[14]
            if tourl:
                tourl=tourl.strip()
                if "keywords=" in tourl:
                    adkeywords=tourl.replace("/offerlist/?keywords=", "")
                    tourl="/offerlist/?keywords="+getjiami(adkeywords)
            if not tourl:
                tourl=""
            ad_type=result[15]
            ad_position=result[16]
            havenum=result[17]
            if not havenum:
                havenum=0
            list={'id':id,'goodsName':goodsName,'goodsname_fu':goodsname_fu,'billing_Class_ID':billing_Class_ID,'start_Time':start_Time,'end_Time':end_Time,'original_Price':original_Price,'present_Price':present_Price,'sales_Num':sales_Num,'left_Num':left_Num,'pic':pic,'statustxt':statustxt,'status':status,'release_Time':release_Time,'tuijiantxt':tuijiantxt,'tourl':tourl,'ad_type':ad_type,'ad_position':ad_position,'havenum':havenum}
        return list
    #添加代金券
    def insert_voucher(self,company_id="0",qtype_id="0",fee="0",title=""):
        begin_time=int(time.time())
        end_time=begin_time+(3600*24*30*2)
        begin_time=int_to_datetime(begin_time)
        end_time=int_to_datetime(end_time)
        todate=datetime.datetime.now()
        today=todate.strftime('%Y%m%d')
        t=random.randrange(100000,999999)
        qcode=str(today)+str(t)
        
        sql="insert into shop_voucher(title,company_id,qcode,qtype_id,begin_time,end_time,fee) values(%s,%s,%s,%s,%s,%s,%s)"
        result=self.dbc.updatetodb(sql,[title,company_id,qcode,qtype_id,begin_time,end_time,fee])
        return result
    def jingjia_keywords(self,company_id=''):
        sql="select id,keywords from app_jingjia_keywords where company_id=%s"
        result=dbc.fetchalldb(sql,[company_id])
        listall=[]
        for list in result:
            id=list[0]
            keywords=list[1]
            ll={'id':id,'keywords':keywords}
            listall.append(ll)
        return listall
    def jingjia_keywords_online(self,company_id=''):
        sql="select id from app_jingjia_keywords where company_id=%s and checked=1"
        result=self.dbc.fetchonedb(sql,[company_id])
        return result
    #竞价排名关键词消费明细
    def jingjia_keypaylist(self,frompageCount,limitNum,company_id="",key_id="",datekey=''):
        argument=[]
        sqlarg=''
        if company_id:
            sqlarg+=" and a.company_id=%s"
            argument.append(company_id)
        if key_id:
            sqlarg+=" and a.key_id=%s"
            argument.append(key_id)
        if datekey:
            if str(datekey)=="1":
                sqlarg+=" and a.gmt_modified>%s and a.gmt_modified<%s"
                argument.append(date_to_str(getpastoneday(int(datekey))))
                argument.append(date_to_str(getpastoneday(0)))
            else:
                sqlarg+=" and a.gmt_modified>%s"
                argument.append(date_to_str(getpastoneday(int(datekey))))
        sql1='select count(0) from app_jingjia_search as a where a.id>0 '+sqlarg
        sql='select a.id,a.keywords as searchkeywords,b.keywords,a.key_id,a.showcount,c.clickcount,c.price,a.gmt_modified,a.gmt_created from app_jingjia_search as a left outer join app_jingjia_keywords as b on a.key_id=b.id left outer join app_jingjia_click as c on a.id=c.search_id where a.id>0 '+sqlarg
        sql=sql+' order by a.id desc limit '+str(frompageCount)+','+str(limitNum)
        count=self.dbc.fetchnumberdb(sql1,argument)
        resultlist=self.dbc.fetchalldb(sql,argument)
        listall=[]
        for list in resultlist:
            sid=list[0]
            searchkeywords=list[1]
            keywords=list[2]
            key_id=list[3]
            showcount=list[4]
            clickcount=list[5]
            if not clickcount:
                clickcount=0
            price=list[6]
            gmt_modified=formattime(list[7],0)
            feenumber=0
            if clickcount and price:
                feenumber=price
            ll={'sid':sid,'searchkeywords':searchkeywords,'keywords':keywords,'key_id':key_id,'showcount':showcount,'clickcount':clickcount,'gmt_modified':gmt_modified,'feenumber':feenumber}
            listall.append(ll)
        return {'list':listall,'count':count,'sql':argument}
    #用户点击明细
    def jingjia_keyclicklist(self,frompageCount,limitNum,company_id="",key_id=""):
        argument=[]
        sqlarg=''
        if company_id:
            sqlarg+=" and a.company_id=%s"
            argument.append(company_id)
        if key_id:
            sqlarg+=" and a.key_id=%s"
            argument.append(key_id)
        sql1='select count(0) from app_jingjia_click as a where a.id>0 '+sqlarg
        sql='select a.id,a.key_id,a.search_id,b.keywords,a.price,a.clickcount,a.sourcetype,a.user_company_id,a.area,a.gmt_created from app_jingjia_click as a left join app_jingjia_keywords as b on a.key_id=b.id where a.id>0 '+sqlarg
        sql=sql+' order by a.id desc limit '+str(frompageCount)+','+str(limitNum)
        count=self.dbc.fetchnumberdb(sql1,argument)
        resultlist=self.dbc.fetchalldb(sql,argument)
        listall=[]
        for list in resultlist:
            cid=list[0]
            keywords=list[3]
            key_id=list[1]
            search_id=list[2]
            
            
            price=list[4]
            clickcount=list[5]
            sourcetype=list[6]
            user_company_id=list[7]
            user_person=""
            if user_company_id and user_company_id!=0:
                user_person=self.getcompanycontact(user_company_id)
                if user_person:
                    user_person=user_person['contact']
            if not user_person:
                user_person="浏览未知用户"
            area=list[8]
            gmt_created=formattime(list[9],0)
            feenumber=0
            if clickcount and price:
                feenumber=price
            ll={'cid':cid,'keywords':keywords,'area':area,'key_id':key_id,'search_id':search_id,'price':price,'clickcount':clickcount,'sourcetype':sourcetype,'user_company_id':user_company_id,'gmt_created':gmt_created,'feenumber':feenumber,'user_person':user_person}
            listall.append(ll)
        return {'list':listall,'count':count}
            
            
            