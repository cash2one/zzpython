#-*- coding:utf-8 -*-
INDUSTRY_LABEL={
                '10001000':'废塑料',
                '10001001':'废金属',
                '10001002':'废纸',
                '10001003':'废旧轮胎与废橡胶',
                '10001004':'废纺织品与废皮革',
                '10001005':'废电子电器',
                '10001006':'废玻璃',
                '10001007':'废旧二手设备',
                '10001008':'其他废料',
                '10001009':'服务',
                '10001010':'塑料原料',
                }
SERVICE_LABEL={
               '10201001':'国外供货商',
               '10201002':'国外回收贸易商',
               '10201003':'码头，仓库储存商',
               '10201004':'国内供应商',
               '10201005':'国内回收贸易商',
               '10201006':'国内加工，拆解商',
               '10201007':'利废企业',
               '10201008':'设备，技术，服务提供商',
               '10201009':'冶炼厂',
               '10201010':'电子厂',
               '10201011':'造粒厂',
               }
SEX_LABEL={
           '0':'先生',
           '1':'女士',
           }
class customer:
    def __init__(self):
        self.db=db
    #是否主管
    def is_hasauth(self,user_id=''):
        sql='select isadmin from user where id=%s'
        result=self.db.fetchonedb(sql,[user_id])
        isadmin=result['isadmin']
        if isadmin:
            return isadmin
    #用户权限级别
    def geauthid(self,user_id=""):
        sql='select auth_category_id from user where id=%s'
        result=self.db.fetchonedb(sql,[user_id])
        authall=[]
        if result:
            auth_category_id=result['auth_category_id']
            if auth_category_id:
                auth_category_id=auth_category_id[:-1]
                authlist=auth_category_id.split(",")
                for l in authlist:
                    authall.append(l)
        return authall
    #获取用户部门
    def getuserpart(self,user_id=""):
        sql='select user_category_code from user where id=%s'
        result=self.db.fetchonedb(sql,[user_id])
        if result:
            return result['user_category_code']
    #获得用户团队权限
    def getuserqx(self,user_id):
        sql="select user_category_id from user where id=%s and closeflag=0"
        result=self.db.fetchonedb(sql,[user_id])
        user_category_id=result['user_category_id']
        userqx=[]
        if user_category_id:
            for l in user_category_id.split(","):
                if l:
                    userqx.append(int(l))
        return userqx
    
    #更新最新数据表
    def updatemodifydata(self,company_id):
        gmt_modified=datetime.datetime.now()
        try:
            sql="replace into update_company (company_id,gmt_modified) values(%s,%s)"
            self.db.updatetodb(sql,[company_id,gmt_modified])
            return 1
        except TypeError:
            return None
    #联系量统计
    def get_tongjicontact(self,user_id="",rank="",contacttype="",telflag="",fromdate="",todate="",teltags="",tomorow="",gonghai="",dotype=""):
        if gonghai:
            sql="select count(distinct company_id) as count from kh_gonghai_select where user_id="+str(user_id)+" and gmt_date>='"+str(fromdate)+"' and gmt_date<='"+str(todate)+"'"
            if dotype:
                sql+=" and dotype='"+str(dotype)+"'"
            result=self.db.fetchonedb(sql)
            #return sql
            return result['count']
        sql="select count(distinct company_id) as count from kh_tel as n where n.id>0 "
        if user_id:
            sql+=" and n.user_id="+str(user_id)
        if rank:
            sql+=" and concat(n.rank,'')="+str(rank)
        if contacttype:
            sql+=" and n.contacttype="+str(contacttype)
        if telflag:
            sql+=" and n.telflag="+str(telflag)
        
        
        if teltags:
            sql+=" and n.teltags="+str(teltags)
        if tomorow:
            fromdate=todate
            todate=formattime(getnextdate(todate),1)
            sql+=" and n.contactnexttime>='"+str(fromdate)+"' and n.contactnexttime<'"+str(todate)+"'"
        else:
            if fromdate and todate:
                todate=formattime(getnextdate(todate),1)
                sql+=" and n.teltime>='"+str(fromdate)+"' and n.teltime<'"+str(todate)+"'"
        #return sql
        result=self.db.fetchonedb(sql)
        return result['count']
    def get_tongjicontactlist(self,frompageCount="",limitNum="",user_id="",rank="",contacttype="",telflag="",fromdate="",todate="",teltags="",tomorow=""):
        sqlarg=''
        argument=[]
        if user_id:
            sqlarg+=" and n.user_id="+str(user_id)
            argument.append(user_id)
        if rank:
            sqlarg+=" and concat(n.rank,'')="+str(rank)
            argument.append(rank)
        if contacttype:
            sqlarg+=" and n.contacttype="+str(contacttype)
            argument.append(contacttype)
        if telflag:
            sqlarg+=" and n.telflag="+str(telflag)
            argument.append(telflag)
        
        if teltags:
            sqlarg+=" and n.teltags="+str(teltags)
            argument.append(teltags)
        if tomorow:
            fromdate=todate
            todate=formattime(getnextdate(todate),1)
            sqlarg+=" and n.contactnexttime>='"+str(fromdate)+"' and n.contactnexttime<'"+str(todate)+"'"
            argument.append(tomorow)
        else:
            if fromdate and todate:
                todate=formattime(getnextdate(todate),1)
                sqlarg+=" and n.teltime>='"+str(fromdate)+"' and n.teltime<'"+str(todate)+"'"
                argument.append(fromdate)
                argument.append(todate)
            
        sqlc="select count(0) as count from kh_tel as n where n.id>0 "+sqlarg
        result=db.fetchonedb(sqlc)
        listcount=result['count']
        
        sql="select n.id,n.teltime,n.contacttype,n.nocontacttype,n.contactnexttime,b.realname,n.rank,n.detail,n.company_id from kh_tel as n left outer join user as b on n.user_id=b.id where n.id>0 "+sqlarg
        sql+='limit '+str(frompageCount)+','+str(limitNum)
        listall=db.fetchalldb(sql)
        for dic in listall:
            tid=dic['id']
            contacttypetxt=''
            nocontacttypetxt=''
            contacttype=dic['contacttype']
            nocontacttype=dic['nocontacttype']
            company_id=dic['company_id']
            ispay=self.getispaymember(dic['company_id'])
            if ispay:
                dotype1="vap_allbm"
            else:
                dotype1="allbm"
            dic['dotype']=dotype1
            companyname=self.getcompanyname(company_id)
            dic['companyname']=companyname
            if contacttype==13:
                contacttypetxt='有效联系'
            if contacttype==12:
                contacttypetxt='无效联系'
            if nocontacttype==1:
                nocontacttypetxt='无人接听'
            if nocontacttype==2:
                nocontacttypetxt='号码错误'
            if nocontacttype==3:
                nocontacttypetxt='停机'
            if nocontacttype==4:
                nocontacttypetxt='关机'
            if nocontacttype==5:
                nocontacttypetxt='无进展'
            dic['contacttypetxt']=contacttypetxt
            dic['nocontacttypetxt']=nocontacttypetxt
            #时间格式转换
            dic['teltime']=formattime(dic['teltime'],0)
            dic['contactnexttime']=formattime(dic['contactnexttime'],0)
        return {'list':listall,'count':listcount,'ret':sql}
            
            
    def getismysee(self,dotype="",company_id="",user_id=""):
        if user_id:
            #cs直接可以打开开通单
            sql="select user_category_code from user where id=%s"
            result=db.fetchonedb(sql,[user_id])
            if result:
                user_category_code=result['user_category_code']
                if str(user_category_code)=="24" or str(user_category_code)=="1320":
                    return 1
        
        if dotype:
            qxlist=self.getuserqx(user_id)
            if dotype[0:3]=="vap":
                sql="select a.id,b.user_category_code,user_id from kh_assign_vap as a left join user as b on a.user_id=b.id where a.company_id=%s"
                result=db.fetchonedb(sql,[company_id])
                if result:
                    user_category_code=result['user_category_code']
                    if str(user_category_code)=="24":
                        return 1
                    myuser_id=result['user_id']
                    if str(user_id)==str(myuser_id):
                        return 1
                    if user_category_code in qxlist:
                        return 1
                else:
                    return 2
            elif dotype[0:3]=="zsh":
                sql="select a.id,b.user_category_code,user_id from kh_assign_zsh as a left join user as b on a.user_id=b.id where a.company_id=%s"
                result=db.fetchonedb(sql,[company_id])
                if result:
                    user_category_code=result['user_category_code']
                    if str(user_category_code)=="24":
                        return 1
                    myuser_id=result['user_id']
                    if str(user_id)==str(myuser_id):
                        return 1
                    if user_category_code in qxlist:
                        return 1
                else:
                    return 2
            else:
                sql="select a.id,b.user_category_code,user_id from kh_assign as a left join user as b on a.user_id=b.id where a.company_id=%s"
                result=db.fetchonedb(sql,[company_id])
                if result:
                    user_category_code=result['user_category_code']
                    #cs直接可以开通
                    if str(user_category_code)=="24":
                        return 1
                    myuser_id=result['user_id']
                    if str(user_id)==str(myuser_id):
                        return 1
                    if user_category_code in qxlist:
                        return 1
                else:
                    return 2
        return 0
    def getismycompany(self,dotype="",company_id="",user_id=""):
        if dotype:
            if dotype[0:3]=="vap":
                sql="select a.id from kh_assign_vap as a where a.company_id=%s and user_id=%s"
                result=db.fetchonedb(sql,[company_id,user_id])
                if result:
                    return 1
            elif dotype[0:3]=="zsh":
                sql="select a.id from kh_assign_zsh as a where a.company_id=%s and user_id=%s"
                result=db.fetchonedb(sql,[company_id,user_id])
                if result:
                    return 1
            else:
                sql="select a.id from kh_assign as a where a.company_id=%s and user_id=%s"
                result=db.fetchonedb(sql,[company_id,user_id])
                if result:
                    return 1
    #客户数统计
    def get_tongjicompany(self,user_id="",rank="",nocontact="",gendiu="",user_category_code="",vapflag="",iszsh=""):
        indexname="company delta_company"
        servername=searchconfig['servername']
        serverport=searchconfig['serverport']
        cl=SphinxClient()
        cl.SetServer(servername,serverport)
        cl.SetMatchMode(SPH_MATCH_BOOLEAN)
        if vapflag:
            cl.SetFilter('ispay',[1])
            if (rank):
                cl.SetFilter('vap_rank',[int(float(rank)*10)])
            if user_id:
                cl.SetFilter('vap_user_id',[int(user_id)])
            if user_category_code:
                cl.SetFilter('vap_user_category_code',[int(user_category_code)])
            if str(gendiu)=="1":
                todayint=date_to_int(getToday())
                cl.SetFilterRange('vap_contactnexttime',0,int(todayint))
                cl.SetFilter('vap_isnew',[1])
            if str(nocontact)=="1":
                cl.SetFilter('vap_isnew',[0])
        elif iszsh:
            if (rank):
                cl.SetFilter('zsh_rank',[int(float(rank)*10)])
            if user_id:
                cl.SetFilter('zsh_user_id',[int(user_id)])
            if user_category_code:
                cl.SetFilter('zsh_user_category_code',[int(user_category_code)])
            if str(gendiu)=="1":
                todayint=date_to_int(getToday())
                cl.SetFilterRange('zsh_contactnexttime',0,int(todayint))
                cl.SetFilter('zsh_isnew',[1])
            if str(nocontact)=="1":
                cl.SetFilter('zsh_isnew',[0])
        else:
            if (rank):
                cl.SetFilter('rank',[int(float(rank)*10)])
            if user_id:
                cl.SetFilter('user_id',[int(user_id)])
            if user_category_code:
                cl.SetFilter('user_category_code',[int(user_category_code)])
            if str(gendiu)=="1":
                todayint=date_to_int(getToday())
                cl.SetFilterRange('contactnexttime',0,int(todayint))
                cl.SetFilter('isnew',[1])
            if str(nocontact)=="1":
                cl.SetFilter('isnew',[0])
        res=cl.Query('',indexname)
        listcount=res['total_found']
        return listcount
    def get_tongjichangestar(self,user_id="",rank="",telflag="",income="",fromdate="",todate=""):
        sql="select count(distinct a.id) as count from company as a left outer join kh_changestar as n on n.company_id=a.id left outer join kh_income as m on m.company_id=a.id where n.id>0 "
        if user_id:
            sql+=" and n.user_id="+str(user_id)
        if rank:
            sql+=" and concat(n.rank,'')="+str(rank)
        if telflag:
            sql+=" and n.telflag="+str(telflag)
        if fromdate and todate:
            todate=formattime(getnextdate(todate),1)
            sql+=" and n.gmt_created>='"+str(fromdate)+"' and n.gmt_created<'"+str(todate)+"'"
        if income:
            sql+=" and n.rank>=4"
            sql+=" and n.telflag="+str(telflag)
            sql+=" and m.user_id="+str(user_id)
            
        result=self.db.fetchonedb(sql)
        if result:
            return result['count']
        else:
            return 0
    def get_tongjichangestarlist(self,frompageCount="",limitNum="",user_id="",rank="",telflag="",income="",fromdate="",todate=""):
        sqlc="select count(distinct a.id) as count from company as a left outer join kh_changestar as n on n.company_id=a.id left outer join kh_income as m on m.company_id=a.id where n.id>0 "
        sql=''
        if user_id:
            sql+=" and n.user_id="+str(user_id)+" "
        if rank:
            sql+=" and concat(n.rank,'')="+str(rank)+" "
        if telflag:
            sql+=" and n.telflag="+str(telflag)+" "
        if fromdate and todate:
            todate=formattime(getnextdate(todate),1)
            sql+=" and n.gmt_created>='"+str(fromdate)+"' and n.gmt_created<'"+str(todate)+"' "
        if income:
            sql+=" and n.rank>=4 "
            sql+=" and n.telflag="+str(telflag)+" "
            sql+=" and m.user_id="+str(user_id)+" "
        sqlc=sqlc+sql
        listcount=self.db.fetchonedb(sqlc)['count']
        
        sqld="select distinct a.id from company as a left outer join kh_changestar as n on n.company_id=a.id left outer join kh_income as m on m.company_id=a.id where n.id>0 "
        sqld=sqld+sql
        sqld+='limit '+str(frompageCount)+','+str(limitNum)
        resultd=self.db.fetchalldb(sqld)
        listall=[]
        for list in resultd:
            id=list['id']
            companyinfo=self.getcompanyinfo_byid(id)
            companyinfo['regtime']=formattime(companyinfo['regtime'])
            ispay=self.getispaymember(id)
            if ispay:
                dotype1="vap_allbm"
            else:
                dotype1="allbm"
            companyinfo['dotype']=dotype1
            accountinfo=self.getaccountinfo_byid(id)
            listall.append({'companyinfo':companyinfo,'accountinfo':accountinfo,'id':id})
        return {"listall":listall,"listcount":listcount}
    #公海挑入客户
    def get_tongjigonghailist(self,frompageCount="",limitNum="",user_id="",dotype="",fromdate="",todate=""):
        sql="select distinct company_id from kh_gonghai_select where user_id=%s and dotype=%s "
        sqlc="select count(distinct company_id) as count from kh_gonghai_select where user_id=%s and dotype=%s "
        if fromdate:
            sql+=" and gmt_date>='"+str(fromdate)+"'"
        if todate:
            sql+=" and gmt_date<='"+str(todate)+"'"
            
        listcount=self.db.fetchonedb(sqlc,[user_id,dotype])['count']
        sql+='limit '+str(frompageCount)+','+str(limitNum)
        result=self.db.fetchalldb(sql,[user_id,dotype])
        listall=[]
        for list in result:
            id=list["company_id"]
            companyinfo=self.getcompanyinfo_byid(id)
            ispay=self.getispaymember(id)
            if ispay:
                dotype1="vap_allbm"
            else:
                dotype1="allbm"
            companyinfo['dotype']=dotype1
            
            accountinfo=self.getaccountinfo_byid(id)
            regtime=formattime(companyinfo['regtime'],0)
            companyinfo['regtime']=regtime
            listall.append({'companyinfo':companyinfo,'accountinfo':accountinfo,'id':id})
        return {"listall":listall,"listcount":listcount}
            
    def get_tongjicompanylist(self,frompageCount="",limitNum="",user_id="",rank="",nocontact="",gendiu="",user_category_code="",vapflag="",iszsh=""):
        indexname="company delta_company"
        servername=searchconfig['servername']
        serverport=searchconfig['serverport']
        cl=SphinxClient()
        cl.SetServer(servername,serverport)
        cl.SetMatchMode(SPH_MATCH_BOOLEAN)
        cl.SetSortMode(SPH_SORT_EXTENDED,'id desc')
        cl.SetLimits(frompageCount,limitNum)
        if vapflag:
            cl.SetFilter('ispay',[1])
            if (rank):
                cl.SetFilter('vap_rank',[int(float(rank)*10)])
            if user_id:
                cl.SetFilter('vap_user_id',[int(user_id)])
            if user_category_code:
                cl.SetFilter('vap_user_category_code',[int(user_category_code)])
            if str(gendiu)=="1":
                todayint=date_to_int(getToday())
                cl.SetFilterRange('vap_contactnexttime',0,int(todayint))
                cl.SetFilter('vap_isnew',[1])
            if str(nocontact)=="1":
                cl.SetFilter('vap_isnew',[0])
        elif iszsh:
            if (rank):
                cl.SetFilter('zsh_rank',[int(float(rank)*10)])
            if user_id:
                cl.SetFilter('zsh_user_id',[int(user_id)])
            if user_category_code:
                cl.SetFilter('zsh_user_category_code',[int(user_category_code)])
            if str(gendiu)=="1":
                todayint=date_to_int(getToday())
                cl.SetFilterRange('zsh_contactnexttime',0,int(todayint))
                cl.SetFilter('zsh_isnew',[1])
            if str(nocontact)=="1":
                cl.SetFilter('zsh_isnew',[0])
        else:
            if (rank):
                cl.SetFilter('rank',[int(float(rank)*10)])
            if user_id:
                cl.SetFilter('user_id',[int(user_id)])
            if user_category_code:
                cl.SetFilter('user_category_code',[int(user_category_code)])
            if str(gendiu)=="1":
                todayint=date_to_int(getToday())
                cl.SetFilterRange('contactnexttime',0,int(todayint))
                cl.SetFilter('isnew',[1])
            if str(nocontact)=="1":
                cl.SetFilter('isnew',[0])
        res=cl.Query('',indexname)
        listall=[]
        listcount=0
        if res:
            if res.has_key('matches'):
                itemlist=res['matches']
                for match in itemlist:
                    id=match['id']
                    attrs=match['attrs']
                    regtime=attrs['regtime']
                    if regtime:
                        regtime=timestamp_to_date(int(attrs['regtime']))
                    companyinfo=self.getcompanyinfo_byid(id)
                    companyinfo['regtime']=regtime
                    ispay=self.getispaymember(id)
                    if ispay:
                        dotype1="vap_allbm"
                    else:
                        dotype1="allbm"
                    companyinfo['dotype']=dotype1
                    accountinfo=self.getaccountinfo_byid(id)
                    listall.append({'companyinfo':companyinfo,'accountinfo':accountinfo,'id':id})
        listcount=res['total_found']
        return {"listall":listall,"listcount":listcount}
        
    #获得所有客户
    def get_allcustomer(self,frompageCount="",limitNum="",searchlist="",user_id=""):
        indexname="company delta_company"
        servername=searchconfig['servername']
        serverport=searchconfig['serverport']
        cl=SphinxClient()
        cl.SetServer(servername,serverport)
        cl.SetMatchMode(SPH_MATCH_BOOLEAN)
        cl.SetSortMode(SPH_SORT_EXTENDED,'id desc')
        cl.SetLimits(frompageCount,limitNum,100000)
        
        if searchlist:
            dotype=""
            lmaction=""
            if (searchlist.has_key("dotype")):
                dotype=searchlist['dotype']
            if (searchlist.has_key("lmaction")):
                lmaction=searchlist['lmaction']
            isvap=None
            iszsh=None
            if dotype:
                if dotype[0:3]=="vap":
                    isvap=1
                if dotype[0:3]=="zsh":
                    iszsh=1
            
            if (searchlist.get("company_id")):
                cl.SetFilter('company_id',[long(searchlist.get("company_id"))])
            #是否钱包充值客户
            if (searchlist.get("isqianbao")):
                cl.SetFilter("isqianbao",[1])
            
            if (searchlist.has_key("com_rank")):
                com_rank=searchlist['com_rank']
                if (com_rank):
                    if isvap:
                        cl.SetFilter('vap_rank',[int(float(com_rank)*10)])
                    elif iszsh:
                        cl.SetFilter('zsh_rank',[int(float(com_rank)*10)])
                    else:
                        cl.SetFilter('rank',[int(float(com_rank)*10)])
            #最近登录
            if (searchlist.has_key("last_login_time_begin") and searchlist.has_key("last_login_time_end")):
                last_login_time_begin=searchlist['last_login_time_begin']
                last_login_time_end=searchlist['last_login_time_end']
                if last_login_time_begin and last_login_time_end:
                    last_login_time_begin=time.mktime(time.strptime(last_login_time_begin, "%Y-%m-%d"))
                    last_login_time_end=time.mktime(time.strptime(last_login_time_end, "%Y-%m-%d"))+60*60*24
                    cl.SetFilterRange('last_login_time',int(last_login_time_begin),int(last_login_time_end))
            #注册时间
            if (searchlist.has_key("regtime_begin") and searchlist.has_key("regtime_end")):
                regtime_begin=searchlist['regtime_begin']
                regtime_end=searchlist['regtime_end']
                if regtime_begin and regtime_end:
                    regtime_begin=time.mktime(time.strptime(regtime_begin, "%Y-%m-%d"))
                    regtime_end=time.mktime(time.strptime(regtime_end, "%Y-%m-%d"))+60*60*24
                    cl.SetFilterRange('regtime',int(regtime_begin),int(regtime_end))
            
            #下次联系时间
            if isvap:
                if (searchlist.has_key("contactnexttime_begin") and searchlist.has_key("contactnexttime_end")):
                    contactnexttime_begin=searchlist['contactnexttime_begin']
                    contactnexttime_end=searchlist['contactnexttime_end']
                    if contactnexttime_begin and contactnexttime_end:
                        contactnexttime_begin=time.mktime(time.strptime(contactnexttime_begin, "%Y-%m-%d"))
                        contactnexttime_end=time.mktime(time.strptime(contactnexttime_end, "%Y-%m-%d"))+60*60*24
                        cl.SetFilterRange('vap_contactnexttime',int(contactnexttime_begin),int(contactnexttime_end))
            elif iszsh:
                if (searchlist.has_key("contactnexttime_begin") and searchlist.has_key("contactnexttime_end")):
                    contactnexttime_begin=searchlist['contactnexttime_begin']
                    contactnexttime_end=searchlist['contactnexttime_end']
                    if contactnexttime_begin and contactnexttime_end:
                        contactnexttime_begin=time.mktime(time.strptime(contactnexttime_begin, "%Y-%m-%d"))
                        contactnexttime_end=time.mktime(time.strptime(contactnexttime_end, "%Y-%m-%d"))+60*60*24
                        cl.SetFilterRange('zsh_contactnexttime',int(contactnexttime_begin),int(contactnexttime_end))
            else:
                if (searchlist.has_key("contactnexttime_begin") and searchlist.has_key("contactnexttime_end")):
                    contactnexttime_begin=searchlist['contactnexttime_begin']
                    contactnexttime_end=searchlist['contactnexttime_end']
                    if contactnexttime_begin and contactnexttime_end:
                        contactnexttime_begin=time.mktime(time.strptime(contactnexttime_begin, "%Y-%m-%d"))
                        contactnexttime_end=time.mktime(time.strptime(contactnexttime_end, "%Y-%m-%d"))+60*60*24
                        cl.SetFilterRange('contactnexttime',int(contactnexttime_begin),int(contactnexttime_end))
                    
            #最后联系时间
            if isvap:
                if (searchlist.has_key("lastteltime_begin") and searchlist.has_key("lastteltime_end")):
                    lastteltime_begin=searchlist['lastteltime_begin']
                    lastteltime_end=searchlist['lastteltime_end']
                    if lastteltime_begin and lastteltime_end:
                        lastteltime_begin=time.mktime(time.strptime(lastteltime_begin, "%Y-%m-%d"))
                        lastteltime_end=time.mktime(time.strptime(lastteltime_end, "%Y-%m-%d"))+60*60*24
                        cl.SetFilterRange('vap_lastteltime',int(lastteltime_begin),int(lastteltime_end))
            #最后联系时间
            elif iszsh:
                if (searchlist.has_key("lastteltime_begin") and searchlist.has_key("lastteltime_end")):
                    lastteltime_begin=searchlist['lastteltime_begin']
                    lastteltime_end=searchlist['lastteltime_end']
                    if lastteltime_begin and lastteltime_end:
                        lastteltime_begin=time.mktime(time.strptime(lastteltime_begin, "%Y-%m-%d"))
                        lastteltime_end=time.mktime(time.strptime(lastteltime_end, "%Y-%m-%d"))+60*60*24
                        cl.SetFilterRange('zsh_lastteltime',int(lastteltime_begin),int(lastteltime_end))
            else:
                if (searchlist.has_key("lastteltime_begin") and searchlist.has_key("lastteltime_end")):
                    lastteltime_begin=searchlist['lastteltime_begin']
                    lastteltime_end=searchlist['lastteltime_end']
                    if lastteltime_begin and lastteltime_end:
                        lastteltime_begin=time.mktime(time.strptime(lastteltime_begin, "%Y-%m-%d"))
                        lastteltime_end=time.mktime(time.strptime(lastteltime_end, "%Y-%m-%d"))+60*60*24
                        cl.SetFilterRange('lastteltime',int(lastteltime_begin),int(lastteltime_end))
            #选择销售对于客户
            adminuser_id=searchlist.get("adminuser_id")
            if adminuser_id:
                if isvap:
                    cl.SetFilter('vap_user_id',[int(adminuser_id)])
                elif iszsh:
                    cl.SetFilter('zsh_user_id',[int(adminuser_id)])
                else:
                    cl.SetFilter('user_id',[int(adminuser_id)])
            #-----------------------
            #VAP客户
            if dotype:
                if dotype[0:3]=="vap":
                    cl.SetFilter('ispay',[1])
            today=getToday()
            today=date_to_int(today)
            
            #充值钱包的客户
            if dotype=="qianbao":
                cl.SetFilter("isqianbao",[1])
                cl.SetFilter('user_id',[0])
                cl.SetFilter('isassgin',[0])
            #过期90-120天
            if dotype=="vap_gq90120":
                gq90=today-60*60*24*90
                gq120=today-60*60*24*120
                cl.SetFilterRange('service_endtime',int(gq120),int(gq90))
            #过期120-180天
            if dotype=="vap_gq120180":
                gq120=today-60*60*24*120
                gq180=today-60*60*24*180
                cl.SetFilterRange('service_endtime',int(gq180),int(gq120))
            #VAP黄金客户
            if dotype=="vap_huangjin":
                #10月内到期的客户
                month10=today+60*60*24*30*10
                cl.SetFilterRange('service_endtime',int(today),int(month10))
            if searchlist.get("companytype"):
                companytype=searchlist.get("companytype")
                if companytype=="黄金期":
                    month10=today+60*60*24*30*10
                    cl.SetFilterRange('service_endtime',int(today),int(month10))
                if companytype=="必杀期":
                    bsbegin=today-60*60*24*90
                    bsend=today+60*60*24*60
                    cl.SetFilterRange('service_endtime',int(bsbegin),int(bsend))
                if companytype=="过期90-120":
                    gq90=today-60*60*24*90
                    gq120=today-60*60*24*120
                    cl.SetFilterRange('service_endtime',int(gq120),int(gq90))
                if companytype=="过期120天后":
                    gq120=today-60*60*24*120
                    cl.SetFilterRange('service_endtime',1000,int(gq120))
                if companytype=="保鲜期":
                    month1=today+60*60*24*30
                    cl.SetFilterRange('service_starttime',int(today),int(month1))
            #今天安排联系的客户
            if dotype=="vap_today":
                if user_id:
                    todayint=date_to_int(getToday())
                    tomodayint=date_to_int(getTomorrow())
                    if searchlist.get("adminuser_id"):
                        cl.SetFilter('vap_user_id',[int(searchlist.get("adminuser_id"))])
                    else:
                        cl.SetFilter('vap_user_id',[int(user_id)])
                    cl.SetFilterRange('vap_contactnexttime',int(todayint),int(tomodayint))
            if dotype=="zsh_today":
                if user_id:
                    todayint=date_to_int(getToday())
                    tomodayint=date_to_int(getTomorrow())
                    if searchlist.get("adminuser_id"):
                        cl.SetFilter('zsh_user_id',[int(searchlist.get("adminuser_id"))])
                    else:
                        cl.SetFilter('zsh_user_id',[int(user_id)])
                    cl.SetFilterRange('zsh_contactnexttime',int(todayint),int(tomodayint))
            #我的一个月未回访客户
            if dotype=="vap_my30nocontact":
                if user_id:
                    if searchlist.get("adminuser_id"):
                        cl.SetFilter('vap_user_id',[int(searchlist.get("adminuser_id"))])
                    else:
                        cl.SetFilter('vap_user_id',[int(user_id)])
                    nocbegin=today-60*60*24*30
                    cl.SetFilterRange('vap_lastteltime',0,int(nocbegin))
            #一个月未回访客户
            if dotype=="vap_30nocontact":
                if user_id:
                    user_category_code=self.getuserqx(user_id)
                    if user_category_code:
                        cl.SetFilter('vap_user_category_code',user_category_code)
                nocbegin=today-60*60*24*30
                cl.SetFilterRange('vap_lastteltime',0,int(nocbegin))
            #新客户（未联系）
            if dotype=="vap_nocontact":
                if user_id:
                    if searchlist.get("adminuser_id"):
                        cl.SetFilter('vap_user_id',[int(searchlist.get("adminuser_id"))])
                    else:
                        cl.SetFilter('vap_user_id',[int(user_id)])
                    cl.SetFilter('vap_isnew',[0])
            if dotype=="zsh_nocontact":
                if user_id:
                    if searchlist.get("adminuser_id"):
                        cl.SetFilter('zsh_user_id',[int(searchlist.get("adminuser_id"))])
                    else:
                        cl.SetFilter('zsh_user_id',[int(user_id)])
                    cl.SetFilter('zsh_isnew',[0])
            #跟丢客户
            if dotype=="vap_contact":
                todayint=date_to_int(getToday())
                cl.SetFilterRange('vap_contactnexttime',0,int(todayint))
                if user_id:
                    if searchlist.get("adminuser_id"):
                        cl.SetFilter('vap_user_id',[int(searchlist.get("adminuser_id"))])
                    else:
                        cl.SetFilter('vap_user_id',[int(user_id)])
                    cl.SetFilter('vap_isnew',[1])
            if dotype=="zsh_contact":
                todayint=date_to_int(getToday())
                cl.SetFilterRange('zsh_contactnexttime',0,int(todayint))
                if user_id:
                    if searchlist.get("adminuser_id"):
                        cl.SetFilter('zsh_user_id',[int(searchlist.get("adminuser_id"))])
                    else:
                        cl.SetFilter('zsh_user_id',[int(user_id)])
                    cl.SetFilter('zsh_isnew',[1])
            #--我的所有
            if dotype=="vap_my":
                if user_id:
                    cl.SetFilter('vap_user_id',[int(user_id)])
                    cl.SetFilter('isdeath',[0])
            if dotype=="zsh_my":
                if user_id:
                    cl.SetFilter('zsh_user_id',[int(user_id)])
                    cl.SetFilter('isdeath',[0])
            #我的SEO客户
            if dotype=="vap_myseo":
                if user_id:
                    cl.SetFilter('vap_user_id',[int(user_id)])
            #我的重点客户
            if dotype=="vap_zhongdian":
                if user_id:
                    cl.SetFilter('vap_user_id',[int(user_id)])
                    cl.SetFilter('vap_emphases',[1])
            #公海客户
            if dotype=="vap_gonghai":
                cl.SetFilter('vap_user_id',[0])
                cl.SetFilter('isdeath',[0])
                #排除120天后过期的客户   VAP公海
                #gq120=today-60*60*24*120
                #cl.SetFilterRange('service_endtime',0,int(gq120),exclude=1)
            #自动掉公海客户
            if dotype=="droptosea3":
                cl.SetFilter('day3',[1])
            #自动掉公海客户
            if dotype=="droptosea30":
                cl.SetFilter('day30',[1])
            #cs必杀期
            if dotype=="vap_bisha":
                bsbegin=today-60*60*24*90
                bsend=today+60*60*24*60
                cl.SetFilterRange('service_endtime',int(bsbegin),int(bsend))
            #部门所有客户
            if dotype=="vap_allbm":
                if user_id:
                    user_category_code=self.getuserqx(user_id)
                    if user_category_code:
                        cl.SetFilter('vap_user_category_code',user_category_code)
            if dotype=="zsh_allbm":
                if user_id:
                    user_category_code=self.getuserqx(user_id)
                    if user_category_code:
                        cl.SetFilter('zsh_user_category_code',user_category_code)
            #死海客户
            if dotype=="vap_isdeath":
                cl.SetFilter('isdeath',[1])
            #放待开通未分配
            if dotype=="vap_noassign":
                cl.SetFilter('vap_user_id',[0])
                cl.SetFilter('vap_assigncheck',[1])
            #大客户>8000
            if dotype=="vap_pay8000":
                cl.SetFilterRange('vap_income',8000,1000000000)
            #客户>2000
            if dotype=="vap_pay2000":
                cl.SetFilterRange('vap_income',2000,8000)
                
            #---------------------------------------------ICD,新签客户
            #--我的所有
            if dotype=="my":
                if user_id:
                    cl.SetFilter('user_id',[int(user_id)])
                    
            #跟丢客户
            if dotype=="contact":
                todayint=date_to_int(getToday())
                cl.SetFilterRange('contactnexttime',0,int(todayint))
                if user_id:
                    if searchlist.get("adminuser_id"):
                        cl.SetFilter('user_id',[int(searchlist.get("adminuser_id"))])
                    else:
                        cl.SetFilter('user_id',[int(user_id)])
                    cl.SetFilter('isnew',[1])
            #公海客户
            if dotype=="gonghai":
                cl.SetFilter('user_id',[0])
                cl.SetFilter('zsh_user_id',[0])
                cl.SetFilter('ispay',[0])
            if dotype=="zsh_gonghai":
                cl.SetFilter('user_id',[0])
                cl.SetFilter('zsh_user_id',[0])
            #付费客户，再生汇
            if dotype=="paycomp":
                cl.SetFilter('ispay',[1])
            if dotype=="zsh_paycomp":
                cl.SetFilter('ispay',[1])
            #录入客户
            if dotype=="customin" or dotype=='zsh_customin':
                cl.SetFilter('adminuser_id',[0],1)
            #未审核录入客户
            if dotype=="requestassign" or dotype=="zsh_requestassign":
                cl.SetFilter('checked',[1])
            else:
                cl.SetFilter('checked',[0])
            #新客户（未联系）
            if dotype=="nocontact":
                if user_id:
                    if searchlist.get("adminuser_id"):
                        cl.SetFilter('user_id',[int(searchlist.get("adminuser_id"))])
                    else:
                        cl.SetFilter('user_id',[int(user_id)])
                    cl.SetFilter('isnew',[0])
            #今天安排联系的客户
            if dotype=="today":
                if user_id:
                    todayint=date_to_int(getToday())
                    tomodayint=date_to_int(getTomorrow())
                    if searchlist.get("adminuser_id"):
                        cl.SetFilter('user_id',[int(searchlist.get("adminuser_id"))])
                    else:
                        cl.SetFilter('user_id',[int(user_id)])
                    cl.SetFilterRange('contactnexttime',int(todayint),int(tomodayint))
            #部门所有客户
            if dotype=="allbm":
                if user_id:
                    user_category_code=self.getuserqx(user_id)
                    if user_category_code:
                        cl.SetFilter('user_category_code',user_category_code)
            #部门曾4星客户
            if dotype=="changeto4star":
                if user_id:
                    user_category_code=self.getuserqx(user_id)
                    if user_category_code:
                        cl.SetFilter('user_category_code',user_category_code)
                    cl.SetFilter('is4star',[1])
            if dotype=="zsh_changeto4star":
                if user_id:
                    user_category_code=self.getuserqx(user_id)
                    if user_category_code:
                        cl.SetFilter('zsh_user_category_code',user_category_code)
                    cl.SetFilter('zsh_is4star',[1])
            #部门曾4星客户
            if dotype=="changeto5star":
                if user_id:
                    user_category_code=self.getuserqx(user_id)
                    if user_category_code:
                        cl.SetFilter('user_category_code',user_category_code)
                    cl.SetFilter('is5star',[1])
            if dotype=="zsh_changeto5star":
                if user_id:
                    user_category_code=self.getuserqx(user_id)
                    if user_category_code:
                        cl.SetFilter('zsh_user_category_code',user_category_code)
                    cl.SetFilter('zsh_is5star',[1])
            #曾4星 \5星客户
            if isvap:
                if str(searchlist.get("is4star"))=="1":
                    cl.SetFilter('vap_is4star',[1])
                if str(searchlist.get("is5star"))=="1":
                    cl.SetFilter('vap_is5star',[1])
            elif iszsh:
                if str(searchlist.get("is4star"))=="1":
                    cl.SetFilter('zsh_is4star',[1])
                if str(searchlist.get("is5star"))=="1":
                    cl.SetFilter('zsh_is5star',[1])
            else:
                if str(searchlist.get("is4star"))=="1":
                    cl.SetFilter('is4star',[1])
                if str(searchlist.get("is5star"))=="1":
                    cl.SetFilter('is5star',[1])
            #登录情况
            if str(searchlist.get("logincount"))!="" and searchlist.get("logincount"):
                arrlogincount=searchlist.get("logincount").split("-")
                cl.SetFilterRange('num_login',int(arrlogincount[0]),int(arrlogincount[1]))
            #联系人次情况
            if searchlist.get("telpersoncount"):
                arrtelpersoncount=searchlist.get("telpersoncount").split("-")
                cl.SetFilterRange('telpersoncount',int(arrtelpersoncount[0]),int(arrtelpersoncount[1]))
            #无效联系次数
            if searchlist.get("telnocount"):
                arrtelnocount=searchlist.get("telnocount").split("-")
                cl.SetFilterRange('telnocount',int(arrtelnocount[0]),int(arrtelnocount[1]))
            #联系次数情况
            if searchlist.get("telcount"):
                arrtelcount=searchlist.get("telcount").split("-")
                cl.SetFilterRange('telcount',int(arrtelcount[0]),int(arrtelcount[1]))
            #垃圾客户
            if dotype=="laji":
                cl.SetFilter('islaji',[1])
                
            
            #重点客户
            if lmaction=="emphases":
                if isvap:
                    cl.SetFilter('vap_emphases',[1])
                elif iszsh:
                    cl.SetFilter('zsh_emphases',[1])
                else:
                    cl.SetFilter('emphases',[1])
            #排除自己
            #if searchlist.get("company_id"):
            #    cl.SetFilter('id',[int(searchlist.get("company_id"))],1)
            #-------------------------
            searstr=""
            if (searchlist.has_key("companyname")):
                companyname=searchlist['companyname']
                if (companyname):
                    searstr="@(compname) "+companyname
            if (searchlist.has_key("contact")):
                contact=searchlist['contact']
                if (contact and searstr):
                    searstr+="&@(contact,othercontact) "+contact
                else:
                    searstr+="@(contact,othercontact) "+contact
            if (searchlist.has_key("email")):
                email=searchlist['email']
                if (email and searstr):
                    searstr+="&@(email,account,othercontact) "+email+""
                else:
                    searstr+="@(email,account,othercontact) "+email+""
            if (searchlist.has_key("account")):
                account=searchlist['account']
                if (account and searstr):
                    searstr+="&@(account) "+account+""
                else:
                    searstr+="@(account) "+account+""
            if (searchlist.has_key("mobile")):
                mobile=searchlist['mobile']
                if (mobile and searstr):
                    searstr+="&@(mobile,othercontact,tel) "+mobile
                else:
                    searstr+="@(mobile,othercontact,tel) "+mobile
                    
            #VAP服务类型
            if (searchlist.has_key("servicetag")):
                servicetag=searchlist['servicetag']
                if (servicetag and searstr):
                    searstr+="&@(servicetag) '"+servicetag+",'"
                else:
                    searstr+="@(servicetag) '"+servicetag+",'"
            
            #VAP非会员用户
            if dotype=="vap_nohuiyuan":
                if (searstr):
                    searstr+="&@(servicetag) 'service'-('a'|'f')"
                else:
                    searstr+="@(servicetag) 'service'-('a'|'f')"
            #VAP会员用户
            if dotype=="vap_huiyuan":
                if (searstr):
                    searstr+="&@(servicetag) ('a'|'f')"
                else:
                    searstr+="@(servicetag) ('a'|'f')"
            #过期120会员客户公海
            if dotype=="vap_gq120gonghai":
                cl.SetFilter('vap_user_id',[0])
                cl.SetFilter('isdeath',[0])
                gq120=today-60*60*24*120
                cl.SetFilterRange('service_endtime',1000,int(gq120))
                if (searstr):
                    searstr+="&@(servicetag) ('a'|'f')"
                else:
                    searstr+="@(servicetag) ('a'|'f')"
            #会员公海客户
            if dotype=="vap_gonghaihuiyuan":
                cl.SetFilter('vap_user_id',[0])
                cl.SetFilter('isdeath',[0])
                gq120=today-60*60*24*120
                cl.SetFilterRange('service_endtime',1000,int(gq120),1)
                if (searstr):
                    searstr+="&@(servicetag) ('a'|'f')"
                else:
                    searstr+="@(servicetag) ('a'|'f')"
            #公海非会员客户
            if dotype=="vap_gonghainohuiyuan":
                cl.SetFilter('isdeath',[0])
                cl.SetFilter('vap_user_id',[0])
                if (searstr):
                    searstr+="&@(servicetag) 'service'-('a'|'f')"
                else:
                    searstr+="@(servicetag) 'service'-('a'|'f')"
            
            #VAP会员用户
            if dotype=="vap_ppt":
                if (searstr):
                    searstr+="&@(servicetag) 'u'"
                else:
                    searstr+="@(servicetag) 'u'"
            #国外客户
            if dotype=="vap_guowai":
                guowailist=self.getguowai()
                if (searstr):
                    cl.SetFilter('area_code_length',[8])
                    searstr+="&@area_code '("+str(guowailist)+")'"
                else:
                    cl.SetFilter('area_code_length',[8])
                    searstr+="@area_code '("+str(guowailist)+")'"
            #过期再生通
            if dotype=="vap_guoqizst":
                cl.SetFilterRange('service_endtime',1000,int(today))
                searstr+="&@servicetag '('a'|'f')'"
            #过期SEO客户公海
            if dotype=="vap_gqseo":
                cl.SetFilterRange('service_endtime',1000,int(today))
                searstr+="&@servicetag 'i'"
                cl.SetFilter('vap_user_id',[0])
                    
            if (searchlist.has_key("business")):
                business=searchlist['business']
                if (business and searstr):
                    searstr+="&@(business,sale_details,buy_details,industry,tags) "+business
                else:
                    searstr+="@(business,sale_details,buy_details,industry,tags) "+business
            if (searchlist.has_key("industry_txt")):
                industry_txt=searchlist['industry_txt']
                if (industry_txt and searstr):
                    searstr+="&@(business,sale_details,buy_details,industry,tags) "+industry_txt
                else:
                    searstr+="@(business,sale_details,buy_details,industry,tags) "+industry_txt
            if (searchlist.has_key("address")):
                address=searchlist['address']
                if (address and searstr):
                    searstr+="&@(address,area_name,area_province,foreign_city) "+address
                else:
                    searstr+="@(address,area_name,area_province,foreign_city) "+address
            if (searchlist.has_key("area")):
                area=searchlist['area']
                if (area and searstr):
                    searstr+="&@(address,area_name,area_province,foreign_city) "+area
                else:
                    searstr+="@(address,area_name,area_province,foreign_city) "+area
            #排序
            orderstr=""
            if (searchlist.has_key("comporder") and searchlist.has_key("ascdesc")):
                comporder=str(searchlist['comporder'])
                ascdesc=searchlist['ascdesc']
                if comporder=="1":
                    if isvap:
                        orderstr="vap_rank "
                    elif iszsh:
                        orderstr="zsh_rank "
                    else:
                        orderstr="rank "
                if comporder=="2":
                    orderstr="num_login "
                if comporder=="3":
                    if isvap:
                        orderstr="vap_contactnexttime "
                    elif iszsh:
                        orderstr="zsh_contactnexttime "
                    else:
                        orderstr="contactnexttime "
                if comporder=="5":
                    if  isvap:
                        orderstr="vap_lastteltime "
                    elif iszsh:
                        orderstr="zsh_lastteltime "
                    else:
                        orderstr="lastteltime "
                if comporder=="6":
                    orderstr="regtime "
                if comporder=="7":
                    orderstr="last_login_time "
                if comporder=="8":
                    orderstr="service_endtime "
                if comporder=="9":
                    orderstr="visit_count "
                if comporder=="10":
                    if isvap:
                        orderstr="vap_assign_time "
                    elif iszsh:
                        orderstr="zsh_assign_time "
                    else:
                        orderstr="assign_time "
                    
                orderstr+=ascdesc
            if (searchlist.has_key("comporder2") and searchlist.has_key("ascdesc2")):
                if orderstr:
                    orderstr+=","
                comporder=searchlist['comporder2']
                ascdesc=searchlist['ascdesc2']
                if comporder=="1":
                    if isvap:
                        orderstr+="vap_rank "
                    elif iszsh:
                        orderstr+="zsh_rank "
                    else:
                        orderstr+="rank "
                if comporder=="2":
                    orderstr+="num_login "
                if comporder=="3":
                    if isvap:
                        orderstr+="vap_contactnexttime "
                    elif iszsh:
                        orderstr+="zsh_contactnexttime "
                    else:
                        orderstr+="contactnexttime "
                if comporder=="5":
                    if isvap:
                        orderstr+="vap_lastteltime "
                    elif iszsh:
                        orderstr+="zsh_lastteltime "
                    else:
                        orderstr+="lastteltime "
                if comporder=="6":
                    orderstr+="regtime "
                if comporder=="7":
                    orderstr+="last_login_time "
                if comporder=="8":
                    orderstr+="service_endtime "
                if comporder=="9":
                    orderstr+="visit_count "
                if comporder=="10":
                    if isvap:
                        orderstr+="vap_assign_time "
                    elif iszsh:
                        orderstr+="zsh_assign_time "
                    else:
                        orderstr+="assign_time "
                orderstr+=ascdesc
            if (searchlist.has_key("comporder3") and searchlist.has_key("ascdesc3")):
                if orderstr:
                    orderstr+=","
                comporder=searchlist['comporder3']
                ascdesc=searchlist['ascdesc3']
                if comporder=="1":
                    if isvap:
                        orderstr+="vap_rank "
                    elif iszsh:
                        orderstr+="zsh_rank "
                    else:
                        orderstr+="rank "
                if comporder=="2":
                    orderstr+="num_login "
                if comporder=="3":
                    if isvap:
                        orderstr+="vap_contactnexttime "
                    elif iszsh:
                        orderstr+="zsh_contactnexttime "
                    else:
                        orderstr+="contactnexttime "
                if comporder=="5":
                    if isvap:
                        orderstr+="vap_lastteltime "
                    elif iszsh:
                        orderstr+="zsh_lastteltime "
                    else:
                        orderstr+="lastteltime "
                if comporder=="6":
                    orderstr+="regtime "
                if comporder=="7":
                    orderstr+="last_login_time "
                if comporder=="8":
                    orderstr+="service_endtime "
                if comporder=="9":
                    orderstr+="visit_count "
                if comporder=="10":
                    if isvap:
                        orderstr+="vap_assign_time "
                    elif iszsh:
                        orderstr+="zsh_assign_time "
                    else:
                        orderstr+="assign_time "
                orderstr+=ascdesc
            if orderstr:
                cl.SetSortMode( SPH_SORT_EXTENDED, " "+str(orderstr)+" ")
            if searstr:
                res=cl.Query(searstr,indexname)
            else:
                res=cl.Query('',indexname)
        else:
            res=cl.Query('',indexname)
            
        listall=[]
        listcount=0
        attrs=''
        if res:
            if res.has_key('matches'):
                itemlist=res['matches']
                for match in itemlist:
                    id=match['id']
                    if searchlist.get("company_id"):
                        if str(id)==str(searchlist.get("company_id")):
                            continue
                    attrs=match['attrs']
                    regtime=attrs['regtime']
                    last_login_time=attrs['last_login_time']
                    if regtime:
                        regtime=timestamp_to_date(int(attrs['regtime']))
                    if last_login_time:
                        last_login_time=timestamp_to_date(int(last_login_time))
                    companyinfo=self.getcompanyinfo_byid(id)
                    accountinfo=self.getaccountinfo_byid(id)
                    
                    adminusername=''
                    visit_count=''
                    if companyinfo:
                        if companyinfo.has_key("visit_count"):
                            visit_count=companyinfo['visit_count']
                            if not visit_count:
                                visit_count=""
                        #录入者
                        if companyinfo.has_key("user_id"):
                            adminuser_id=companyinfo['user_id']
                            if adminuser_id and str(adminuser_id)!="0":
                                adminusername=self.get_username(adminuser_id)
                                
                    try:
                        name=companyinfo['name']
                    except TypeError:
                        name=""
                    try:
                        star=companyinfo['star']
                    except TypeError:
                        star=""
                    
                    try:
                        email=accountinfo['email']
                    except TypeError:
                        email=""
                    if not email:
                        email=""
                    try:
                        account=accountinfo['account']
                    except TypeError:
                        account=""
                    
                    try:
                        num_login=accountinfo['num_login']
                    except TypeError:
                        num_login=0
                    try:
                        contact=accountinfo['contact']
                    except TypeError:
                        contact=''
                    try:
                        tel_country_code=accountinfo['tel_country_code']
                    except TypeError:
                        tel_country_code=''
                    try:
                        tel_area_code=accountinfo['tel_area_code']
                    except TypeError:
                        tel_area_code=''
                    try:
                        tel=accountinfo['tel']
                    except TypeError:
                        tel=''
                    try:
                        mobile=accountinfo['mobile']
                    except TypeError:
                        mobile=''
                    #省份
                    area_code=''
                    checked=''
                    if companyinfo:
                        area_code=companyinfo.get('area_code')
                        checked=companyinfo.get('checked')
                    areatxt=''
                    if len(area_code)>=8:
                        areacontry=self.getarea(area_code=area_code[0:8])
                        areatxt+=areacontry
                    if len(area_code)>=12:
                        areaprovince=self.getarea(area_code=area_code[0:12])
                        areatxt+=areaprovince
                    if len(area_code)>=16:
                        areacity=self.getarea(area_code=area_code[0:16])
                        areatxt+=areacity
                    if len(area_code)>=20:
                        areaarea=self.getarea(area_code=area_code[0:20])
                        areatxt+=areaarea
                    if not areatxt:
                        areatxt=""
                    if area_code:
                        area_code=area_code[:-4]
                    #获得对应的销售人员
                    try:
                        assigninfo=self.getsalesman_bycompid(company_id=id)
                        salesman=assigninfo['salesman']
                        assigntime=assigninfo['gmt_created']
                        emphases=assigninfo['emphases']
                        user_category_code=assigninfo['user_category_code']
                        if assigntime:
                            assigntime=formattime(assigntime)
                        else:
                            assigntime=''
                    except:
                        salesman=''
                        assigntime=''
                        emphases=0
                        user_category_code=''
                    #vap对应销售信息
                    vapassigninfo=self.getvapsalesman_bycompid(id)
                    if vapassigninfo:
                        vap_salesman=vapassigninfo['salesman']
                        vap_assigntime=vapassigninfo['gmt_created']
                        vap_emphases=vapassigninfo['emphases']
                        if vap_assigntime:
                            vap_assigntime=formattime(vap_assigntime)
                        else:
                            vap_assigntime=''
                    else:
                        vap_salesman=''
                        vap_assigntime=''
                        vap_emphases=0
                    #再生汇对应用户信息
                    zshassigninfo=self.getzshsalesman_bycompid(id)
                    if zshassigninfo:
                        zsh_salesman=zshassigninfo['salesman']
                        zsh_assigntime=zshassigninfo['gmt_created']
                        zsh_emphases=zshassigninfo['emphases']
                        if zsh_assigntime:
                            zsh_assigntime=formattime(zsh_assigntime)
                        else:
                            zsh_assigntime=''
                    else:
                        zsh_salesman=''
                        zsh_assigntime=''
                        zsh_emphases=0
                    
                    #是否vap
                    if isvap:
                        salesinfo=self.getvapsalesinfo_bycomid(id)
                        assigntime=vap_assigntime
                    elif iszsh:
                        salesinfo=self.getzshsalesinfo_bycomid(id)
                        assigntime=zsh_assigntime
                    else:
                        salesinfo=self.getsalesinfo_bycomid(id)
                    
                    rank=''
                    if salesinfo:
                        if salesinfo.has_key('lastteltime'):
                            lastteltime=salesinfo['lastteltime']
                            if lastteltime:
                                salesinfo['lastteltime']=formattime(lastteltime)
                            else:
                                salesinfo['lastteltime']=''
                        if salesinfo.has_key('contactnexttime'):
                            contactnexttime=salesinfo['contactnexttime']
                            if contactnexttime:
                                if formattime(contactnexttime)=='1900-01-01 00:00:00':
                                    salesinfo['contactnexttime']=''
                                else:
                                    salesinfo['contactnexttime']=formattime(contactnexttime)
                            else:
                                salesinfo['contactnexttime']=''
                        rank=''
                        if salesinfo.has_key('rank'):
                            rank=salesinfo['rank']
                            if rank:
                                salesinfo['rank']=str(int(rank))+"星"
                                if isvap:
                                    if str(rank)=="4.1":
                                        salesinfo['rank']="短4星"
                                    if str(rank)=="4.8":
                                        salesinfo['rank']="长4星"
                                else:
                                    if str(rank)=="4.1":
                                        salesinfo['rank']="普4星"
                                    if str(rank)=="4.8":
                                        salesinfo['rank']="钻4星"
                                rank=str(rank)+"星"
                            else:
                                salesinfo['rank']=''
                                rank=''
                            rank=salesinfo['rank']
                    servicetime=self.getservicetime(id)
                    sqman=self.getsquser_bycompid(id)
                    lastgonghai=None
                    if dotype=="gonghai":
                        lastgonghai=self.lastgonghai_bycomid(id)
                    list={'id':id,'name':name,'checked':checked,'star':star,'last_login_time':last_login_time,'regtime':regtime,'email':email,'num_login':num_login,'contact':contact,'tel_country_code':tel_country_code,'tel_area_code':tel_area_code,'tel':tel,'mobile':mobile,'area_code':area_code,'areatxt':areatxt,'salesman':salesman,'assigntime':assigntime,'emphases':emphases,'sqman':sqman,'vap_salesman':vap_salesman,'vap_assigntime':vap_assigntime,'vap_emphases':vap_emphases,'zsh_salesman':zsh_salesman,'zsh_assigntime':zsh_assigntime,'zsh_emphases':zsh_emphases,'visit_count':visit_count,'salesinfo':salesinfo,'servicetime':servicetime,'adminusername':adminusername,'account':account,'rank':rank,'lastgonghai':lastgonghai,'user_category_code':user_category_code}
                    listall.append(list)
            listcount=res['total_found']
        return {"listall":listall,"listcount":listcount,"ret":searstr}
    #根据id获得公司信息
    def getcompanyinfo_byid(self,id):
        sql='select name,area_code,star,industry_code,service_code,address,address_zip,website,business,introduction,business_type,sale_details,buy_details,regtime,domain_zz91,rubbish,islaji,isdeath,user_id,membership_code,checked,b.real_visit_count as visit_count,c.label as regfrom from company left outer join analysis_esite_visit as b on company.id=b.company_id left outer join category as c on regfrom_code=c.code where company.id=%s'
        result=db.fetchonedb(sql,[id])
        return result
    #最后公海时间
    def lastgonghai_bycomid(self,company_id):
        sql="select gmt_created from kh_droptogonghai where company_id=%s order by gmt_created desc"
        res=db.fetchonedb(sql,[company_id])
        if res:
            return formattime(res['gmt_created'])
        else:
            return None
    #根据id获得账户信息
    def getaccountinfo_byid(self,id):
        sql='select email,num_login,gmt_last_login,contact,position,tel_country_code,tel_area_code,tel,mobile,fax_country_code,fax_area_code,fax,sex,account from company_account where company_id=%s'
        result=db.fetchonedb(sql,[id])
        return result
    #销售信息
    def getsalesinfo_bycomid(self,company_id):
        sql='select rank,contactnexttime,lastteltime,contacttype,is4star,is5star from kh_sales where company_id=%s'
        result=db.fetchonedb(sql,[company_id])
        return result
    #销售信息
    def getvapsalesinfo_bycomid(self,company_id):
        sql='select rank,contactnexttime,lastteltime,contacttype,is4star,is5star from kh_sales_vap where company_id=%s'
        result=db.fetchonedb(sql,[company_id])
        return result
    #销售信息
    def getzshsalesinfo_bycomid(self,company_id):
        sql='select rank,contactnexttime,lastteltime,contacttype,is4star,is5star from kh_sales_zsh where company_id=%s'
        result=db.fetchonedb(sql,[company_id])
        return result
    #获得省份
    def getarea(self,area_code=""):
        sql0='select label from category where code=%s'
        result0=db.fetchonedb(sql0,[area_code])
        if result0:
            return result0['label']
    #获得国外地区code
    def getguowai(self):
        sql="select code from category where parent_code='1001' and code!='10011000'"
        result=db.fetchalldb(sql)
        areacode=''
        for list in result:
            areacode+=list['code']+"|"
        return areacode[0:len(areacode)-1]
    #获得国外地区code
    def getguowailist(self):
        sql="select code,label from category where parent_code='1001' and code!='10011000'"
        result=db.fetchalldb(sql)
        return result
    #获得所有销售人员
    def get_allsalesman(self,user_id='',vap="",renshi='',wl='',zsh='',icd=''):
        qxlist=self.getuserqx(user_id)
        qx=""
        for l in qxlist:
            qx+=str(l)+","
        if qx:
            qx=qx[0:len(qx)-1]
        if not qx:
            qx='0'
        sql="select code,label from user_category where code in ("+qx+") and closeflag=0 "
        if vap:
            sql+=" and code=1315"
        if renshi:
            sql+=" and code=23"
        if wl:
            sql+=" and code=1323"
        if zsh:
            sql+=" and code=1325"
        if icd:
            sql+=" and code=1306"
        sql+=" order by ord desc"
        result=db.fetchalldb(sql)
        listall=[]
        for res in result:
            code=res['code']
            cate_label=res['label']
            thiscateman=self.getinthiscateman(code)
            list={"cate_label":cate_label,"thiscateman":thiscateman,'code':code}
            listall.append(list)
        if not listall:
            thiscateman=self.getinthiscateman('',user_id=user_id)
            listall=[{"cate_label":'',"thiscateman":thiscateman,'code':'0'}]
        return listall
    #获得团队下所有人员
    def getinthiscateman(self,code,user_id=""):
        if user_id:
            sql="select id,username,realname from user where id=%s and closeflag=0"
            result=db.fetchalldb(sql,[user_id])
            return result
        if code:
            sql="select id,username,realname from user where user_category_code=%s and closeflag=0"
        result=db.fetchalldb(sql,[code])
        return result
    #获得companyid对应的销售人员
    def getsalesman_bycompid(self,company_id):
        sql='select u.realname as salesman,k.gmt_created,k.emphases,u.user_category_code from user as u left join kh_assign as k on k.user_id=u.id where k.company_id=%s'
        result=db.fetchonedb(sql,[company_id])
        return result
    #获得companyid对应的预申请分配人员
    def getsquser_bycompid(self,company_id):
        sql='select u.realname from user as u left join kh_assign_request as k on k.user_id=u.id where k.company_id=%s'
        result=db.fetchonedb(sql,[company_id])
        if result:
            return result['realname']
        else:
            return ''
    #获得vapcompanyid对应的销售人员
    def getvapsalesman_bycompid(self,company_id):
        sql='select u.realname as salesman,k.gmt_created,k.emphases from user as u left join kh_assign_vap as k on k.user_id=u.id where k.company_id=%s'
        result=db.fetchonedb(sql,[company_id])
        return result
    #获得zshcompanyid对应的销售人员
    def getzshsalesman_bycompid(self,company_id):
        sql='select u.realname as salesman,k.gmt_created,k.emphases from user as u left join kh_assign_zsh as k on k.user_id=u.id where k.company_id=%s'
        result=db.fetchonedb(sql,[company_id])
        return result
    #获得所有行业
    def get_industry(self):
        sql='select code,label from category where parent_code=1000'
        result=db.fetchalldb(sql)
        return result
    #再生通服务时间
    def getservicetime(self,company_id):
        sql="select gmt_start,gmt_end from crm_company_service where company_id=%s and apply_status='1' and crm_service_code in (1000,1007,1008,1009,1010) order by gmt_end desc"
        result=db.fetchonedb(sql,[company_id])
        s=''
        if result:
            gmt_start=formattime(result['gmt_start'],1)
            gmt_end=formattime(result['gmt_end'],1)
            s={'gmt_start':gmt_start,'gmt_end':gmt_end}
        return s
    #判断是否为付费客户
    def getispaymember(self,company_id):
        #是否高会或付费会员
        sql="select id from company_account where company_id=%s and ispay=1"
        result=db.fetchonedb(sql,[company_id])
        if result:
            return 1
        else:
            return None
    #判断是否为开通再生汇
    def getiszshmember(self,company_id):
        sql="select id from company_account where company_id=%s and iszsh=1"
        result=db.fetchonedb(sql,[company_id])
        if result:
            return 1
        else:
            return None
    #获得客户的省份城市
    def get_area_txt(self,code):
        sql='select label from category where code=%s'
        result=db.fetchonedb(sql,[code])
        if result:
            return result['label']
        else:
            return ''
    
    #获得公司详情
    def getcompanyinfo(self,company_id="",user_id=""):
        companyinfo=self.getcompanyinfo_byid(company_id)
        accountinfo=self.getaccountinfo_byid(company_id)
        
        listall={}
        for ll in companyinfo:
            listall[ll]=companyinfo[ll]
            if not listall[ll]:
                listall[ll]=''
        if accountinfo:
            for ll in accountinfo:
                listall[ll]=accountinfo[ll]
                if not listall[ll]:
                    listall[ll]=''
        else:
            return None
        #是否垃圾客户
        islaji=companyinfo['islaji']
        if not islaji:
            islaji=0
        listall['islaji']=islaji
        
        #是死海客户
        isdeath=companyinfo['isdeath']
        if not isdeath:
            isdeath=0
        listall['isdeath']=isdeath
        
        
        area_code=listall['area_code']
        listall['guowai']=None
        if area_code:
            if area_code[0:8]!="10011000":
                listall['guowai']=1
        province_code=area_code[0:12]
        listall['province_code']=province_code
        city_code=area_code[0:16]
        listall['city_code']=city_code
        province_txt=self.get_area_txt(province_code)
        listall['province_txt']=province_txt
        city_txt=self.get_area_txt(city_code)
        listall['city_txt']=city_txt
        
        try:
            sex=listall['sex']
            sex_txt=SEX_LABEL[str(sex)]
        except KeyError:
            sex=''
            sex_txt='未填'
        listall['sex_txt']=sex_txt
        
        try:
            industry_code=listall['industry_code']
            industry_code_txt=INDUSTRY_LABEL[str(industry_code)]
        except KeyError:
            industry_code_txt=''
        listall['industry_code_txt']=industry_code_txt
        try:
            service_code=listall['service_code']
            service_code_txt=SERVICE_LABEL[str(service_code)]
        except KeyError:
            service_code_txt=''
        listall['service_code_txt']=service_code_txt
        #最近登录
        #last_login_time=timestamp_to_date(int(attrs['last_login_time']))
        gmt_last_login=listall['gmt_last_login']
        last_login_time=formattime(gmt_last_login)
        listall['last_login_time']=last_login_time
        #注册时间
        #regtime=timestamp_to_date(int(attrs['regtime']))
        regtime=formattime(listall['regtime'])
        listall['regtime']=regtime
        #登录次数
        num_login=listall['num_login']
        if not num_login:
            listall['num_login']=0
        company_name=listall['name']
        listall['company_name']=company_name
        if user_id:
            sql='select emphases from kh_assign where company_id=%s and user_id=%s'
            result=db.fetchonedb(sql,[company_id,user_id])
            listall['emphases']=0
            if result:
                emphases=result['emphases']
                listall['emphases']=result['emphases']
                if not emphases:
                    listall['emphases']=0
            sql='select emphases from kh_assign_vap where company_id=%s and user_id=%s'
            result=db.fetchonedb(sql,[company_id,user_id])
            if result:
                emphases=result['emphases']
                listall['vap_emphases']=result['emphases']
                if not emphases:
                    listall['vap_emphases']=0
            else:
                listall['vap_emphases']=0
            
            sql='select emphases from kh_assign_zsh where company_id=%s and user_id=%s'
            result=db.fetchonedb(sql,[company_id,user_id])
            if result:
                emphases=result['emphases']
                listall['zsh_emphases']=result['emphases']
                if not emphases:
                    listall['zsh_emphases']=0
            else:
                listall['zsh_emphases']=0
        #list={'company_name':company_name,'industry_code':industry_code,'industry_code_txt':industry_code_txt,'service_code':service_code,'service_code_txt':service_code_txt,'address':address,'address_zip':address_zip,'tel_country_code':tel_country_code,'tel_area_code':tel_area_code,'tel':tel,'mobile':mobile,'fax_country_code':fax_country_code,'fax_area_code':fax_area_code,'fax':fax,'email':email,'website':website,'domain_zz91':domain_zz91,'contact':contact,'position':position,'business':business,'introduction':introduction,'business_type':business_type,'sale_details':sale_details,'buy_details':buy_details,'last_login_time':last_login_time,'num_login':num_login,'regtime':regtime,'sex':sex,'sex_txt':sex_txt,'area_code':area_code,'province_code':province_code,'city_code':city_code,'province_txt':province_txt,'city_txt':city_txt,'rubbish':rubbish}
        return listall

    #获得省份
    def getprovincelist(self):
        sql='select code,label from category where parent_code=10011000'
        result=db.fetchalldb(sql)
        return result
    #获得省份，城市，区县
    def getsitelist(self,sitecode=''):
        sql='select code,label from category where parent_code=%s'
        result=db.fetchalldb(sql,[sitecode])
        return result
    #获得当前公司的所有销售记录
    def gettelsalelist(self,frompageCount,limitNum,company_id="",telflag=""):
        argument=[]
        sqlarg=''
        if company_id:
            sqlarg+=' and a.company_id=%s'
            argument.append(company_id)
        if telflag:
            sqlarg+=' and a.telflag=%s'
            argument.append(telflag)
        sql1="select count(0) from kh_tel as a where a.id>0"+sqlarg
        sql="select a.id,a.teltime,a.contacttype,a.nocontacttype,a.contactnexttime,b.realname,a.rank,a.detail,a.company_id,a.telflag from kh_tel as a left outer join user as b on a.user_id=b.id where a.id>0"+sqlarg
        sql=sql+' order by a.id desc limit '+str(frompageCount)+','+str(limitNum)
        count=db.fetchnumberdb(sql1,argument)
        resultlist=db.fetchalldb(sql,argument)
        for dic in resultlist:
            tid=dic['id']
            sql="select id,gmt_created,user_id from kh_droptogonghai where tel_id=%s"
            res=db.fetchonedb(sql,[tid])
            if res:
                dic['havegonghai']=formattime(res['gmt_created'])
                duser_id=res['user_id']
                if duser_id:
                    dic['dropgonghainame']=self.get_username(duser_id)
            contacttypetxt=''
            nocontacttypetxt=''
            contacttype=dic['contacttype']
            nocontacttype=dic['nocontacttype']
            if contacttype==13:
                contacttypetxt='有效联系'
            if contacttype==12:
                contacttypetxt='无效联系'
            if nocontacttype==1:
                nocontacttypetxt='无人接听'
            if nocontacttype==2:
                nocontacttypetxt='号码错误'
            if nocontacttype==3:
                nocontacttypetxt='停机'
            if nocontacttype==4:
                nocontacttypetxt='关机'
            if nocontacttype==5:
                nocontacttypetxt='无进展'
            dic['contacttypetxt']=contacttypetxt
            dic['nocontacttypetxt']=nocontacttypetxt
            #时间格式转换
            dic['teltime']=formattime(dic['teltime'],0)
            dic['contactnexttime']=formattime(dic['contactnexttime'],0)
            #主管建议
            sqla="select b.realname,a.details,a.gmt_created from kh_tel_admin as a left join user as b on a.user_id=b.id where tel_id=%s order by a.id desc"
            restellist=db.fetchalldb(sqla,[tid])
            for tlist in restellist:
                tlist['gmt_created']=formattime(tlist['gmt_created'],0)
            dic['admindetaillist']=restellist
            
            telflag=dic['telflag']
            rank=dic['rank']
            if telflag==4:
                dic['rank']=int(rank)
                if str(rank)=="4.1":
                    dic['rank']="短4"
                if str(rank)=="4.8":
                    dic['rank']="长4"
            else:
                dic['rank']=int(rank)
                if str(rank)=="4.1":
                    dic['rank']="普4"
                if str(rank)=="4.8":
                    dic['rank']="钻4"
        return {'list':resultlist,'count':count}
    #开通单列表
    def getorderlist(self,frompageCount,limitNum,searchlist=""):
        argument=[]
        sqlarg=''
        if searchlist.has_key('douser_id'):
            douser_id=searchlist['douser_id']
            if douser_id:
                sqlarg+=' and a.user_id=%s'
                argument.append(douser_id)
        if searchlist.has_key('user_category_code'):
            user_category_code=searchlist['user_category_code']
            if user_category_code:
                sqlarg+=' and a.user_category_code=%s'
                argument.append(user_category_code)
        if searchlist.has_key('service_type'):
            service_type=searchlist['service_type']
            if service_type:
                sqlarg+=' and a.service_type=%s'
                argument.append(service_type)
        if searchlist.has_key('sales_type'):
            sales_type=searchlist['sales_type']
            if sales_type:
                sqlarg+=' and a.sales_type=%s'
                argument.append(sales_type)
        if searchlist.has_key('customType'):
            customType=searchlist['customType']
            if customType:
                sqlarg+=' and a.sales_type=%s'
                argument.append(customType)
        if searchlist.has_key('sales_priceflag'):
            sales_priceflag=searchlist['sales_priceflag']
            if sales_priceflag:
                if str(sales_priceflag)=="0":
                    sqlarg+=' and a.sales_price=0'
                else:
                    sqlarg+=' and a.sales_price>0'
                #argument.append(sales_priceflag)
        
        
        if searchlist.has_key('account'):
            account=searchlist['account']
            if account:
                sqlarg+=' and b.account=%s'
                argument.append(account)
        if searchlist.has_key('company_id'):
            acompany_id=searchlist['company_id']
            if acompany_id:
                sqlarg+=' and a.company_id=%s'
                argument.append(acompany_id)
        if searchlist.has_key('mobile'):
            mobile=searchlist['mobile']
            if mobile:
                sqlarg+=' and b.mobile=%s'
                argument.append(mobile)
                
        if searchlist.has_key('fromdate'):
            fromdate=searchlist['fromdate']
            if fromdate:
                sqlarg+=' and a.sales_date>=%s'
                argument.append(fromdate)
                
        if searchlist.has_key('todate'):
            todate=searchlist['todate']
            if todate:
                sqlarg+=' and a.sales_date<=%s'
                argument.append(todate)
            
        sql1="select count(0) from kh_income as a left outer join company_account as b on a.company_id=b.company_id where a.id>0"+sqlarg
        sql="select a.* from kh_income as a left outer join company_account as b on a.company_id=b.company_id where a.id>0"+sqlarg
        sql=sql+' order by a.id desc limit '+str(frompageCount)+','+str(limitNum)
        count=db.fetchnumberdb(sql1,argument)
        resultlist=db.fetchalldb(sql,argument)
        for dic in resultlist:
            tid=dic['id']
            company_id=dic['company_id']
            accountinfo=self.getaccountinfo_byid(dic['company_id'])
            user_category_code=dic['user_category_code']
            user_category_name=self.get_user_category_name(user_category_code)
            dic['user_category_name']=user_category_name
            sales_date=dic['sales_date']
            dic['ispay']=self.getispaymember(dic['company_id'])
            if not dic['end_time']:
                dic['end_time']=''
            if not dic['ldbblance']:
                dic['ldbblance']=''
            if dic['ispay']:
                dotype1="vap_allbm"
            else:
                dotype1="allbm"
            dic['dotype']=dotype1
            if sales_date:
                dic['sales_date']=formattime(sales_date,1)
                wkdate=getweekday(sales_date)
                dic['wkdate']=wkdate
                dic['mkdate']=formattime(sales_date,3)
                dic['nkdate']=formattime(sales_date,4)
            dic['companyname']=self.getcompanyname(dic['company_id'])
            if accountinfo:
                dic['account']=accountinfo['account']
                dic['mobile']=accountinfo['mobile']
                dic['email']=accountinfo['email']
            if dic['com_pro']:
                com_pro=dic['com_pro']
                if INDUSTRY_LABEL_old.has_key(str(com_pro)):
                    dic['com_hy']=INDUSTRY_LABEL_old[str(dic['com_pro'])]
        return {'list':resultlist,'count':count,'sqlarg':sqlarg}
    #获得部门到单数据
    def getincomecount(self,user_category_code="",ndate="",mflag=""):
        argument=[]
        sql="select sum(sales_price) as price from kh_income where id>0 "
        if user_category_code:
            sql+=" and user_category_code=%s"
            argument.append(user_category_code)
        if mflag:
            if ndate:
                sql+=' and sales_date>=%s'
                today=str_to_date(ndate)
                #-----月第一天
                fromdate=str_to_date(today.strftime('%Y-%m')+"-1")
                argument.append(fromdate)
                #-----月最后一天
                ndate=calendar.monthrange(int(today.strftime('%Y')), int(today.strftime('%m')))
                ndate=today.strftime('%Y-%m')+"-"+str(ndate[1])
                todate=formattime(getnextdate(ndate),1)
                sql+=' and sales_date<%s'
                argument.append(todate)
        else:
            if ndate:
                sql+=' and sales_date>=%s'
                argument.append(ndate)
                todate=formattime(getnextdate(ndate),1)
                sql+=' and sales_date<%s'
                argument.append(todate)
            
        count=db.fetchonedb(sql,argument)
        if not count or not count['price']:
            return 0
        return count['price']
        
        
        
    #日志列表
    def getloglist(self,frompageCount,limitNum,searchlist="",dotype=""):
        argument=[]
        sqlarg=''
        if searchlist.has_key('company_id'):
            company_id=searchlist['company_id']
            if company_id:
                sqlarg+=' and company_id=%s'
                argument.append(company_id)
        if searchlist.has_key('old_user_id'):
            old_user_id=searchlist['old_user_id']
            if old_user_id:
                sqlarg+=' and user_id=%s'
                argument.append(old_user_id)
        if searchlist.has_key('admin_user_id'):
            admin_user_id=searchlist['admin_user_id']
            if admin_user_id:
                sqlarg+=' and admin_user_id=%s'
                argument.append(admin_user_id)
        
        sql1="select count(0) from kh_log as a where id>0"+sqlarg
        sql="select id,company_id,user_id,details,admin_user_id,gmt_created from kh_log where id>0"+sqlarg
        sql=sql+' order by id desc limit '+str(frompageCount)+','+str(limitNum)
        count=db.fetchnumberdb(sql1,argument)
        resultlist=db.fetchalldb(sql,argument)
        for dic in resultlist:
            #时间格式转换
            dic['gmt_created']=formattime(dic['gmt_created'])
            dic['admin_realname']=self.get_username(dic['admin_user_id'])
            dic['old_realname']=self.get_username(dic['user_id'])
            dic['companyname']=self.getcompanyname(dic['company_id'])
            dic['ispay']=self.getispaymember(dic['company_id'])
            if not dotype:
                if dic['ispay']:
                    dotype1="vap_allbm"
                else:
                    dotype1="allbm"
                dic['dotype']=dotype1
            else:
                dic['dotype']=dotype
            dic['icdsalesman']=self.getsalesman_bycompid(dic['company_id'])
            dic['vapsalesman']=self.getvapsalesman_bycompid(dic['company_id'])
            
        return {'list':resultlist,'count':count,'sql':sql}
    #获取公司名称
    def getcompanyname(self,company_id):
        sql="select name from company where id=%s"
        result=db.fetchonedb(sql,[company_id])
        if result:
            return result['name']
        else:
            return ''
    #获得额外联系人
    def getotherperson(self,company_id="",my_user_id=""):
        sql="select id,company_id,name,sex,station,tel,fax,mobile,email,address,gmt_created,bz,gmt_modified,user_id from kh_othercontact where company_id=%s"
        resultlist=db.fetchalldb(sql,[company_id])
        for dic in resultlist:
            sextxt=""
            if dic['sex']=='0':
                sextxt="男"
            if dic['sex']=='1':
                sextxt="女"
            dic['sextxt']=sextxt
            #时间格式转换
            dic['gmt_created']=formattime(dic['gmt_created'],0)
            dic['gmt_modified']=formattime(dic['gmt_modified'],0)
            if my_user_id:
                if str(dic['user_id'])==str(my_user_id):
                    dic['myflag']=1
        return resultlist
    
    #判断当前用户是否为管理员权限
    def get_is_admin(self,user_id):
        authlist=self.geauthid(user_id=user_id)
        if "1" in authlist:
            return 1
        else:
            return 0
    def getservicelist(self):
        sql="select code,tag,name from crm_service"
        resultlist=db.fetchalldb(sql)
        return resultlist
    #获得用户姓名
    def get_username(self,user_id):
        sql="select realname from user where id=%s"
        result=db.fetchonedb(sql,[user_id])
        if result:
            return result['realname']
        else:
            return ''
    def get_user_category_name(self,user_category_code):
        sql="select label from user_category where code=%s"
        result=db.fetchonedb(sql,[user_category_code])
        if result:
            return result['label']
        else:
            return ''
#     #获得客户的省份城市
#     def kh_province_and_city(self,company_id):
#         sql1='select area_code from company where id=%s'
#         result1=db.fetchonedb(sql1,[company_id])
#         province_code=result1['area_code'][0:11]
#         city_code=result1['area_code'][12:15]
#         sql2='select label from category where code=%s'
#         result2=db.fetchonedb(sql2,[province_code])
#         province_txt=result2['label']
#         result3=db.fetchonedb(sql2,[city_code])
#         city_txt=result3['label']
#         return {'province_code':province_code,'city_code':city_code,'province_txt':province_txt,'city_txt':city_txt}
    #保存到本地数据库
    def getserverdbtable(self,dbserver,tab,id):
        sql="select * from "+str(tab)+" where id=%s"
        results=dbserver.fetchonedb(sql,[id])
        filds=""
        vlist=""
        vals=[]
        id=results['id']
        for ll in results.keys():
            filds+=ll+","
            vlist+="%s,"
            content=results[ll]
            vals.append(content)
        filds=filds[0:len(filds)-1]
        vlist=vlist[0:len(vlist)-1]
        sql="select id from "+str(tab)+" where id=%s"
        result=db.fetchonedb(sql,[id])
        if not result:
            sql="insert into "+str(tab)+"("+str(filds)+") values("+vlist+")"
            db.updatetodb(sql,vals)
            return 1
        else:
            return 0
    #钱包余额
    def getqianbaoblance(self,company_id):
        if company_id:
            sql='select sum(fee) as fee from pay_mobilewallet where company_id=%s'
            result=db.fetchonedb(sql,[company_id])['fee']
            if result:
                if result<=0:
                    return '0.00'
                else:
                    return '%.2f'%result
        return '0.00'
    #账单列表
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
        sql1='select count(0) as count from pay_mobilewallet where company_id=%s'+sqlarg
        sql='select id,fee,ftype,gmt_date,product_id,forcompany_id,bz,gmt_created from pay_mobilewallet where company_id=%s'+sqlarg
        sql=sql+' order by gmt_created desc limit '+str(frompageCount)+','+str(limitNum)
        count=self.db.fetchonedb(sql1,argument)['count']
        resultlist=self.db.fetchalldb(sql,argument)
        listall=[]
        for result in resultlist:
            id=result["id"]
            fee=result["fee"]
            if fee>0:
                fee='+'+str(fee)
            ftype=result["ftype"]
            gmt_date=formattime(result["gmt_created"],0)
            product_id=result["product_id"]
            ftypename=self.getftypename(ftype)
            forcompany_id=result["forcompany_id"]
            bz=result['bz']
            forcompanyname=""
            if forcompany_id:
                if str(ftype)=="1":
                    forcompanyname=self.getcompanyname(forcompany_id)
            list={'id':id,'fee':fee,'ftype':ftype,'gmt_date':gmt_date,'ftypename':ftypename,'product_id':product_id,'forcompany_id':forcompany_id,'forcompanyname':forcompanyname,'bz':bz}
            listall.append(list)
        return {'list':listall,'count':count}
    #获取付费类型
    def getftypename(self,id):
        sql='select name from pay_wallettype where id=%s'
        result=self.db.fetchonedb(sql,[id])
        if result:
            return result["name"]
    def getcompanyname(self,company_id):
        sql="select name from company where id=%s"
        result=self.db.fetchonedb(sql,[company_id])
        if result:
            return result["name"]
    #是否安装app并绑定账号
    def gethaveinstallapp(self,company_id):
        sql="select account from company_account where company_id=%s"
        result=db.fetchonedb(sql,[company_id])
        if result:
            account=result['account']
            sql1="select id from oauth_access where target_account=%s and open_type='app.zz91.com'"
            result1=db.fetchonedb(sql1,[account])
            if result1:
                return 1
    def gethaveinstallweixin(self,company_id):
        sql="select account from company_account where company_id=%s"
        result=db.fetchonedb(sql,[company_id])
        if result:
            account=result['account']
            sql1="select id from oauth_access where target_account=%s and open_type='weixin.qq.com'"
            result1=db.fetchonedb(sql1,[account])
            if result1:
                return 1
    def getqikan(self,code):
        sql="select label from huangye_category where code=%s"
        result=db.fetchonedb(sql,[code])
        if result:
            return result['label']
        else:
            return ''
    #期刊列表
    def gethuangyelist(self,frompageCount,limitNum,searchlist=""):
        argument=[]
        sqlarg=''
        if searchlist.has_key('doperson'):
            doperson=searchlist['doperson']
            if doperson:
                sqlarg+=' and personid=%s'
                argument.append(doperson)
        if searchlist.has_key('pcheck'):
            pcheck=searchlist['pcheck']
            if pcheck:
                sqlarg+=' and pcheck=%s'
                argument.append(pcheck)
        if searchlist.has_key('huangye_qukan'):
            huangye_qukan=searchlist['huangye_qukan']
            if huangye_qukan:
                sqlarg+=' and huangye_qukan=%s'
                argument.append(huangye_qukan)
        if searchlist.has_key('ckeywords'):
            ckeywords=searchlist['ckeywords']
            if ckeywords:
                sqlarg+=' and comkeywords=%s'
                argument.append(ckeywords)
        js1=searchlist.get('js1')
        if js1:
            sqlarg+=' and js1=%s'
            argument.append(js1)
        js2=searchlist.get('js2')
        if js2:
            sqlarg+=' and js2=%s'
            argument.append(js2)
        sl1=searchlist.get('sl1')
        if sl1:
            sqlarg+=' and sl1=%s'
            argument.append(sl1)
        sl2=searchlist.get('sl2')
        if sl2:
            sqlarg+=' and sl2=%s'
            argument.append(sl2)
        qt1=searchlist.get('qt1')
        if qt1:
            sqlarg+=' and qt1=%s'
            argument.append(qt1)
        com_email=searchlist.get('com_email')
        if com_email:
            sqlarg+=' and com_email=%s'
            argument.append(com_email)
        province=searchlist.get('province')
        if province:
            sqlarg+=' and province like %s'
            argument.append('%'+province+'%')
        city=searchlist.get('city')
        if province:
            sqlarg+=' and province like %s'
            argument.append('%'+city+'%')
        cname=searchlist.get('cname')
        if cname:
            sqlarg+=' and cname like %s'
            argument.append('%'+cname+'%')
        cproductslist=searchlist.get('cproductslist')
        if cproductslist:
            sqlarg+=' and cproductslist like %s'
            argument.append('%'+cproductslist+'%')
        
        
        sql1="select count(0) from huangye_list where id>0"+sqlarg
        sql="select * from huangye_list where id>0"+sqlarg
        sql=sql+' order by id desc limit '+str(frompageCount)+','+str(limitNum)
        count=db.fetchnumberdb(sql1,argument)
        resultlist=db.fetchalldb(sql,argument)
        for dic in resultlist:
            #时间格式转换
            dic['fdate']=formattime(dic['fdate'])
            dic['realname']=self.get_username(dic['personid'])
            ckeywords=str(dic['comkeywords'])
            if ckeywords=="1":
                dic['hyname']="废金属"
            elif ckeywords=="2":
                dic['hyname']="废塑料"
            elif ckeywords=="3":
                dic['hyname']="综合"
            dic['qikanname']=self.getqikan(dic['huangye_qukan'])
            
        return {'list':resultlist,'count':count,'sql':sql}
#         