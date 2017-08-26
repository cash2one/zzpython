#-*- coding:utf-8 -*-

class ldbweixin:
    #----初始化ast数据库
    def __init__(self):
        self.dbc=dbc
        self.nowdate=datetime.datetime.now()
    #----获得来电宝余额
    def getldbbalance(self,company_id):
        mousefirst=date.today().strftime( '%-Y-%-m-1')
        phone400=self.getcompany400(company_id)
        mousefee=self.getldblaveall(company_id,datefrom=mousefirst)
        alllave=self.getldblaveall(company_id)
        list={'lave':'%.2f'%alllave,'mousefee':'%.2f'%mousefee}
        return list
    def getpayfee(self,company_id,target_id,click_fee):
        ldblaveall=self.getldblaveall(company_id)
        if ldblaveall>=5:
            gmt_created=datetime.datetime.now()
            sql='insert into phone_click_log(company_id,target_id,click_fee,gmt_created,gmt_modified) values(%s,%s,%s,%s,%s)'
            self.dbc.updatetodb(sql,[company_id,target_id,click_fee,gmt_created,gmt_created])
    #----获得来电宝帐号总余额
    def getldblaveall(self,company_id,datefrom=''):
        #----查看未接来电费用
        sqls='select sum(click_fee) from phone_call_click_fee where company_id=%s'
        if datefrom!='':
            sqls=sqls+" and gmt_created>'"+str(datefrom)+"'"
        results=self.dbc.fetchonedb(sqls,[company_id])
        phone_call_click_fee=0
        if results:
            phone_call_click_fee=results[0]
            if phone_call_click_fee==None:
                phone_call_click_fee=0
        #----电话费用
        sqls='select sum(call_fee) from phone_log where company_id=%s'
        if datefrom!='':
            sqls=sqls+" and start_time>'"+str(datefrom)+"'"
        results=self.dbc.fetchonedb(sqls,[company_id])
        call_fee=0
        if results:
            call_fee=results[0]
            if call_fee==None:
                call_fee=0
        #----点击查看联系方式费用
        sqls='select sum(click_fee) from phone_click_log where company_id=%s'
        if datefrom!='':
            sqls=sqls+" and gmt_created>'"+str(datefrom)+"'"
        results=self.dbc.fetchonedb(sqls,[company_id])
        phone_click_fee_fee=0
        if results:
            phone_click_fee_fee=results[0]
            if phone_click_fee_fee==None:
                phone_click_fee_fee=0
                            
        sql='select amount from phone where company_id=%s and expire_flag=0'
        result=self.dbc.fetchonedb(sql,[company_id])
        lave=0
        if result:
            lave=int(result[0])
            if lave:
                lave=lave-phone_call_click_fee-phone_click_fee_fee-call_fee
            else:
                lave=0
        if datefrom!='':
            return phone_call_click_fee+phone_click_fee_fee+call_fee
        return lave
    #----获得400号码电话记录
    def getphonerecords(self,frompageCount,limitNum,company_id,datearg=''):
        sqlarg=''
        argument=[company_id]
        if datearg:
            if datearg=='1':
                sqlarg=' and start_time>=%s'
                argument.append(getpastoneday(30))
            elif datearg=='2':
                sqlarg=' and start_time>=%s'
                argument.append(getpastoneday(90))
            elif datearg=='3':
                sqlarg=' and start_time>=%s'
                argument.append(getpastoneday(365))
            elif datearg=='4':
                sqlarg=' and start_time<%s'
                argument.append(getpastoneday(365))
        sql1='select count(0),sum(call_fee) from phone_log where company_id=%s'+sqlarg
        result1=self.dbc.fetchonedb(sql1,argument)
        if result1:
            count=result1[0]
            sum_call_fee=result1[1]
            if sum_call_fee==None:
                sum_call_fee=0
        sqlargall=sqlarg
        argumentall=argument
        #---未接来电扣费
        
        #argument1[0]=company_id
        sqlarg=sqlarg.replace("start_time","gmt_created")
        sql1='select sum(click_fee) from phone_call_click_fee where company_id=%s '+sqlarg
        result1=self.dbc.fetchonedb(sql1,argument)
        if result1:
            sum_click_fee=result1[0]
            if sum_click_fee==None:
                sum_click_fee=0
                
            sum_call_fee=sum_call_fee+sum_click_fee
           
        if sum_call_fee>0:
            #是否按通付费
            isonephone=self.getldbonephone(company_id)
            sql='select caller_id,call_fee,start_time,end_time,state,id,province,company_id,call_sn from phone_log where company_id=%s '+sqlargall+' order by gmt_created desc limit '+str(frompageCount)+','+str(limitNum)
            resultlist=self.dbc.fetchalldb(sql,argumentall)
            listall=[]
            for result in resultlist:
                caller_id=result[0]
                state=result[4]
                province=result[6]
                call_sn=result[8]
                if not province:
                    province=""
                forcompany_id=result[7]
                call_fee='-%.2f'%result[1]
                if state=="0":
                    statetxt="[<font color=red>未接</font>]"
                else:
                    statetxt='已接'
                    
                if isonephone:
                    state="1"
                    call_fee=statetxt
                #---是否已经查看未接来电
                sqld="select id,click_fee from phone_call_click_fee where caller_tel=%s and company_id=%s"
                resultd=self.dbc.fetchonedb(sqld,[caller_id,company_id])
                if resultd:
                    state="1"
                    call_fee="<font style='color:#ccc'>未接已查看</font>"
                    #call_fee='-%.2f'%resultd[1]
                
                if state!="1":
                    #已接来电直接显示
                    sql="select id from phone_log where caller_id=%s and state='1' and company_id=%s"
                    resultd=self.dbc.fetchonedb(sqld,[caller_id,company_id])
                    if resultd:
                        state="1"
                        caller_id=""
                    else:
                        if str(call_sn)!="0":
                            caller_id=result[0][:8]+'***未接'
                            call_fee=""
                list={'id':result[5],'caller_id':caller_id,'caller_id_':caller_id,'call_fee':call_fee,'start_time':formattime(result[2],0),'end_time':formattime(result[3],0),'state':state,'province':province,'forcompany_id':forcompany_id,'call_sn':call_sn}
                listall.append(list)
            return {'list':listall,'count':count,'sum_call_fee':'%.2f'%sum_call_fee}
    #----获得ldb点击记录
    def getphoneclick(self,frompageCount,limitNum,company_id):
        sql1='select count(0),sum(click_fee) from phone_click_log where company_id=%s'
        result1=self.dbc.fetchonedb(sql1,[company_id])
        count=result1[0]
        sum_click_fee=result1[1]
        if not sum_click_fee:
            sum_click_fee=0
        sql='select target_id,click_fee,gmt_created from phone_click_log where company_id=%s order by gmt_created desc limit '+str(frompageCount)+','+str(limitNum)
        resultlist=self.dbc.fetchalldb(sql,[company_id])
        listall=[]
        for result in resultlist:
            target_name=self.getcompanyname(result[0])
            target_id=result[0]
            list={'target_name':target_name,'click_fee':'%.2f'%result[1],'gmt_created':formattime(result[2],0),'company_id':target_id}
            listall.append(list)
        return {'list':listall,'count':count,'sum_click_fee':'%.2f'%sum_click_fee}
    #----获得公司的400号码
    def getcompany400(self,company_id):
        sql='select tel from phone where company_id=%s'
        result=self.dbc.fetchonedb(sql,[company_id])
        if result:
            return result[0]
    def getcompanymobile(self,company_id):
        sql='select mobile,contact from company_account where company_id=%s'
        result=self.dbc.fetchonedb(sql,[company_id])
        if result:
            return {'mobile':result[0],'contact':result[1]}
    def getcompanyname(self,id):
        sql='select name from company where id=%s'
        result=self.dbc.fetchonedb(sql,[id])
        if result:
            return result[0]
    #----哪个地方的客户对您的产品最感兴趣
    def getarea_custom(self,company_id):
        sql='select province from phone_log where company_id=%s group by province order by count(province) desc'
        resultlist=self.dbc.fetchalldb(sql,[company_id])
        listall=''
        numb=0
        if resultlist:
            for result in resultlist:
                province=result[0]
                if province:
                    if numb<3:
                        listall+=province+','
                    numb+=1
        return listall[:-1]
    #----哪个地方的客户对您的产品最感兴趣
    def getarea_custom2(self,company_id,frompageCount='',limitNum='',allnum=''):
        #phone400=self.getcompany400(company_id)
        cl = SphinxClient()
        cl.SetServer ( SPHINXCONFIG['serverid'], SPHINXCONFIG['port'] )
        cl.SetMatchMode ( SPH_MATCH_BOOLEAN )
#        cl.SetFilter('tel',[phone400])
        cl.SetGroupBy( 'pprovince',SPH_GROUPBY_ATTR,"@count desc")
#        cl.SetSortMode ( SPH_SORT_EXTENDED, "SUM(pprovince) desc" );
#        cl.SetSortMode( SPH_SORT_ATTR_DESC ,'@count' )
#        if allnum:
#            cl.SetLimits (frompageCount,limitNum,allnum)
#        else:
#            cl.SetLimits (frompageCount,limitNum)
        cl.SetFilter('company_id',[int(company_id)])
        res = cl.Query ('','phone_log')
        numb=0
        listall=''
        if res and res.has_key('matches'):
            matchlist=res['matches']
            for met in matchlist:
                attrs=met['attrs']
                pprovince=attrs['pprovince']
                if pprovince and numb<3:
                    listall+=pprovince+','
                    numb+=1
        if listall!='':
            return listall[:-1]
        else:
            return ""
    #----哪些时间是来电高峰
    def gettime_custom2(self,company_id):
        #phone400=self.getcompany400(company_id)
        cl = SphinxClient()
        cl.SetServer ( SPHINXCONFIG['serverid'], SPHINXCONFIG['port'] )
        cl.SetMatchMode ( SPH_MATCH_BOOLEAN )
        cl.SetGroupBy( 'hour_time',SPH_GROUPBY_ATTR,"@count desc")
        cl.SetFilter('company_id',[int(company_id)])
        res = cl.Query ('','phone_log')
        numb=0
        listall=''
        if res and res.has_key('matches'):
            matchlist=res['matches']
            for met in matchlist:
                attrs=met['attrs']
                hour_time=attrs['hour_time']
                if hour_time and numb<3:
                    listall+=str(hour_time)+','
                    numb+=1
        if listall!='':
            return listall[:-1]
        else:
            return ""
    #----哪些时间是来电高峰
    def gettime_custom(self,company_id):
        sql='select HOUR(`start_time`) from phone_log where company_id=%s group by HOUR(`start_time`) order by count(HOUR(`start_time`)) desc'
        resultlist=self.dbc.fetchalldb(sql,[company_id])
        listall=''
        numb=0
        if resultlist:
            for result in resultlist:
                start_time=result[0]
                if start_time:
                    if numb<3:
                        listall+=str(start_time)+','
                    numb+=1
        return listall[:-1]
    #----您的接听率
    def getnowmonthstate(self,company_id):
        sql="select phone_rate from ldb_level where company_id=%s and is_date=0"
        result=self.dbc.fetchonedb(sql,[company_id])
        if result:
            return result[0]
        else:
            return ''
        """
        phone400=self.getcompany400(company_id)
        if phone400:
            nowmonth=time.strftime('%Y-%m-01 00:00:00',time.localtime(time.time()))
            sql1='select count(0) from phone_log where tel=%s and gmt_created>=%s'
            count1=self.dbc.fetchnumberdb(sql1,[phone400,nowmonth])
            sql='select count(0) from phone_log where tel=%s and state=1 and gmt_created>=%s'
            count=self.dbc.fetchnumberdb(sql,[phone400,nowmonth])
            state_lv=str(float(count)*100/count1)[:5]+'%'
            return state_lv
        else:
            return ""
        """

    #----商机搜索
    def getppccomplist(self,companyname='',fromNom='',limitNum='',havepic='',picsize='200x200'):
        cl = SphinxClient()
        cl.SetServer ( settings.spconfig['serverid'], settings.spconfig['port'] )
        cl.SetLimits (fromNom,limitNum)
        if havepic:
            cl.SetFilterRange('havepic',1,100)
        cl.SetSortMode( SPH_SORT_ATTR_DESC ,'refresh_time' )
        cl.SetMatchMode ( SPH_MATCH_BOOLEAN )
        cl.SetGroupBy("company_id",SPH_GROUPBY_ATTR)
        if companyname and companyname!='':
#            company_id=self.getcompany_id(keyword)
#            cl.SetFilter('company_id',[company_id])
#            cl.SetMatchMode ( SPH_MATCH_ANY )
#            cl.SetSortMode( SPH_SORT_EXTENDED," refresh_time desc" )
            res = cl.Query ('@companyname '+companyname,'offersearch_ppc')
        else:
            res = cl.Query ('','offersearch_ppc')
        listall=[]
        listcount=0
        if res:
#            return res
            listcount=res['total_found']
            if res.has_key('matches'):
                tagslist=res['matches']
                for match in tagslist:
                    id=match['id']
                    attrs=match['attrs']
                    company_id=attrs['company_id']
                    area=self.getcompanyarea(company_id)
                    ptitle=attrs['ptitle']
                    ppckeywords1=attrs['ppckeywords']
                    ppckeywords=subString(ppckeywords1,50)
                    companyname=attrs['companyname']
                    front_tel=attrs['front_tel']
                    pdt_kind=attrs['pdt_kind']
                    pdttxt=""
                    if (str(pdt_kind)=="0"):
                        pdttxt="供应"
                    if (str(pdt_kind)=="1"):
                        pdttxt="求购"
                        
                    sql1="select tel from phone where company_id=%s"
                    phoneresult = self.dbc.fetchonedb(sql1,[company_id])
                    if phoneresult:
                        ftel=phoneresult[0]
                    else:
                        ftel=""
                    ftel=ftel.replace("-",";")
                    lis={'id':id,'ptitle':ptitle,'pdttxt':pdttxt,'area':area,'ftel':ftel,'company_id':company_id,'ppckeywords':ppckeywords,'ppctel':front_tel,'companyname':companyname}
                    listall.append(lis)
                    if limitNum==1:
                        return lis
        return {'list':listall,'count':listcount}

    def getcompany_id(self,companyname):
        sql='select id from company where name=%s'
        result=self.dbc.fetchonedb(sql,[companyname])
        if result:
            return result[0]
    def getcompanyid(self,username):
        sql='select company_id from  company_account where account=%s'
        result=self.dbc.fetchonedb(sql,[username])
        if result:
            return result[0]
    #----获得公司地区
    def getlabelc(self,code):
        sql='select label from category where code=%s'
        result=self.dbc.fetchonedb(sql,[code])
        if result:
            return result[0]
    def getcontact(self,id,company_id=''):
        lave=self.getldblaveall(company_id)
        if lave>=10:
            sql='select caller_id from phone_log where id=%s'
            result=self.dbc.fetchonedb(sql,[id])
            if result:
                caller_tel=result[0]
                sqld="select id from phone_call_click_fee where company_id=%s and caller_tel=%s"
                resultd=self.dbc.fetchonedb(sqld,[company_id,caller_tel])
                if resultd==None:
                    
                    #---扣费
                    sqlb="select lave,id from phone_cost_service where company_id=%s and lave>=10 order by id asc"
                    resultb=self.dbc.fetchonedb(sqlb,[company_id])
                    if resultb:
                        lave1=resultb[0]
                        id=resultb[1]
                        if lave1:
                            lave2=lave1-10
                            sqlg="update phone_cost_service set lave=%s where id=%s"
                            self.dbc.updatetodb(sqlg,[lave2,id])
                    else:
                        return "err"
                    
                    gmt_created=gmt_modified=self.nowdate
                    click_fee="10.00"
                    value=[caller_tel,company_id,click_fee,gmt_created,gmt_modified]
                    sqla="insert into phone_call_click_fee(caller_tel,company_id,click_fee,gmt_created,gmt_modified) values(%s,%s,%s,%s,%s)"
                    self.dbc.updatetodb(sqla,value)
                    
                return caller_tel
        else:
            return "err"
        return "err"
                
            
    
    def getcompanyarea(self,company_id):
        sql='select area_code from company where id=%s'
        result=self.dbc.fetchonedb(sql,[company_id])
        if result:
            area_code=result[0][:12]
            area=self.getlabelc(area_code)
            return area
    #来电宝查看联系方式费用
    def getldbonephonemoney(self,company_id):
        sql="select click_fee from phone_cost_service where company_id=%s and is_lack=0 order by id asc"
        #sql="select id from crm_company_service where company_id=%s and crm_service_code='1011' and apply_status=1 and DATEDIFF(CURDATE(),`gmt_end`)<=0"
        ldbresult=self.dbc.fetchonedb(sql,[company_id])
        if ldbresult:
            return ldbresult[0]
        else:
            return 10
        
    #来电宝是否按通付费客户
    def getldbonephone(self,company_id):
        sql="select id from crm_company_service where company_id=%s and crm_service_code='1011' and apply_status=1 and DATEDIFF(CURDATE(),`gmt_end`)<=0"
        ldbresult=self.dbc.fetchonedb(sql,[company_id])
        if ldbresult:
            return 1
        else:
            return None