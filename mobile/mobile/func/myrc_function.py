#-*- coding:utf-8 -*-
class zmyrc:
    #----初始化ast数据库
    def __init__(self):
        self.dbc=dbc
    #----生意管家 供求管理
    def getmyproductslist(self,frompageCount="",limitNum="",company_id="",checkStatus="",is_pause=""):
        #if (checkStatus=="" or checkStatus==None):
            #checkStatus=1
        #if (is_pause=="" or is_pause==None):
            #is_pause=0
        sqls1=''
        sqls2=''
        argument=[company_id]
        if checkStatus:
            sqls1='and check_status=%s and is_pause=0'
            argument.append(checkStatus)
        if is_pause:
            sqls2='and is_pause=%s'
            argument.append(is_pause)
        sql="select count(0) from products where company_id=%s and is_del=0 "+sqls1+" "+sqls2+""
        alist=self.dbc.fetchonedb(sql,argument)
        if alist:
            listcount=alist[0]
        argument.append(frompageCount)
        argument.append(limitNum)
        sql="select id,title,real_time,refresh_time,unpass_reason,expire_time,check_status,products_type_code from products where company_id=%s and is_del=0 "+sqls1+" "+sqls2+" order by refresh_time desc limit %s,%s"
        alist=self.dbc.fetchalldb(sql,argument)
        listall=[]
        if alist:
            for list in alist:
                timenow=datetime.datetime.now()
                expire_time=list[5]
                is_expire=''
                if timenow>expire_time:
                    is_expire=1
                unpass_reason=list[4]
                check_status=list[6]
                products_type_code=list[7]
                if products_type_code=="10331000":
                    products_typetext="供应"
                else:
                    products_typetext="求购"
                if unpass_reason==None:
                    unpass_reason=""
                
                rlist={'proid':list[0],'protitle':products_typetext+list[1],'real_time':formattime(list[2],0),'refresh_time':formattime(list[3],0),'unpass_reason':unpass_reason,'is_expire':is_expire,'check_status':check_status}
                listall.append(rlist)
        return {'list':listall,'count':listcount}
    def getviptype(self,company_id):
        sql='select membership_code from company where id=%s'
        result=self.dbc.fetchonedb(sql,[company_id])
        if result:
            return result[0]
    #绑定的客户自动登录
    def weixinautologin(self,request,weixinid):
        if (weixinid and weixinid!=""):
            account=self.weixinbinding(weixinid)
            if account:
                company_id=self.getcompanyid(account)
                request.session.set_expiry(60*60*60)
                request.session['username']=account
                request.session['company_id']=company_id
                request.session['weixinid']=weixinid
                return 1
            else:
                return None
        else:
            return None
        #验证微信是否绑定
    def weixinbinding(self,weixinid):
        sql="select target_account from oauth_access where open_id=%s and target_account<>'0' and closeflag=0"
        list=self.dbc.fetchonedb(sql,[weixinid]);
        if list:
            return list[0]
        else:
            return None
    #--获得公司id
    def getcompanyid(self,account):
        sql="select company_id from  company_account where account=%s"
        result=self.dbc.fetchonedb(sql,[account])
        if result:
            return result[0]
    #新版app我的行情定制
    def getmyorderprice(self,company_id):
        
        sql='select id,label,company_id,category_id,assist_id,keywords from app_order_price where company_id=%s'
        alistall = self.dbc.fetchalldb(sql,[company_id])
        listall=[]
        if alistall:
            for alist in alistall:
                list={'id':alist[0],
                      'label':alist[1],
                      'company_id':alist[2],
                      'category_id':alist[3],
                      'assist_id':alist[4],
                      'keywords':alist[5]}
                listall.append(list)
        return listall
    #新版app定制行情
    def savemyorderprice(self,list):
        company_id=list['company_id']
        label=list['label']
        category_id=list['category_id']
        assist_id=list['assist_id']
        keywords=list['keywords']
        gmt_created=datetime.datetime.now()
        value=[label,company_id,category_id,assist_id,keywords,gmt_created]
        sql="select id from app_order_price where company_id=%s and category_id=%s and label=%s and assist_id=%s and keywords=%s"
        alist = self.dbc.fetchonedb(sql,[company_id,category_id,label,assist_id,keywords])
        if not alist:
            sql="insert into app_order_price(label,company_id,category_id,assist_id,keywords,gmt_created) values(%s,%s,%s,%s,%s,%s)"
            result=self.dbc.updatetodb(sql,value)
            if result:
                return result[0]
            return '0'
        else:
            return None
    #新版app供求定制保存
    def savemyordertrade(self,list):
        company_id=list['company_id']
        otype=list['otype']
        timelimit=list['timelimit']
        keywordslist=list['keywordslist']
        provincelist=list['provincelist']
        gmt_created=datetime.datetime.now()
        value=[otype,company_id,timelimit,keywordslist,provincelist,gmt_created]
        sql="select id from app_order_trade where company_id=%s"
        alist = self.dbc.fetchonedb(sql,[company_id])
        if not alist:
            sql="insert into app_order_trade(type,company_id,timelimit,keywordslist,provincelist,gmt_created) values(%s,%s,%s,%s,%s,%s)"
            result=self.dbc.updatetodb(sql,value)
            if result:
                return result[0]
            return '0'
        else:
            sql="update app_order_trade set type=%s,timelimit=%s,keywordslist=%s,provincelist=%s where company_id=%s"
            result=self.dbc.updatetodb(sql,[otype,timelimit,keywordslist,provincelist,company_id])
            if result:
                return result[0]
            return '0'
    #新版app我的供求定制
    def getmyordertrade(self,company_id):
        sql='select id,type,company_id,timelimit,keywordslist,provincelist from app_order_trade where company_id=%s'
        alist = self.dbc.fetchonedb(sql,[company_id])
        list=None
        if alist:
            list={'id':alist[0],
                  'otype':alist[1],
                  'company_id':alist[2],
                  'timelimit':alist[3],
                  'keywordslist':alist[4],
                  'provincelist':alist[5]}
        return list
    #我的通讯录
    def getmyaddressbooklist(self,frompageCount="",limitNum="",company_id=""):
        sqlarg=""
        sql="select count(0) from company_addressbook where company_id=%s "+sqlarg
        listcount=0
        alist=self.dbc.fetchonedb(sql,[company_id])
        if alist:
            listcount=alist[0]           
        sql2="select forcompany_id,bz from company_addressbook where company_id=%s "+sqlarg+" order by id desc limit "+str(frompageCount)+","+str(limitNum)+""
        aalist=self.dbc.fetchalldb(sql2,[company_id])
        listall=[]
        if alist:
            for list in aalist:
                forcompany_id=list[0]
                contact=""
                position=""
                sql="select contact,sex,position from company_account where company_id=%s"
                alist=self.dbc.fetchonedb(sql,[forcompany_id])
                if alist:
                    contact=alist[0]
                    sex=alist[1]
                    position=alist[2]
                    if str(sex)=="0":
                        if ("先生" not in contact) and ("女士" not in contact):
                            contact+="先生"
                    else:
                        if ("先生" not in contact) and ("女士" not in contact):
                            contact+="女士"
                    if (position==None):
                        position=""
                    position=position.strip()
                compname=""
                sqlc="select name from company where id=%s"
                clist=self.dbc.fetchonedb(sqlc,[forcompany_id])
                if clist:
                    compname=clist[0]
                bz=list[1]
                faceurl=None
                sql="select picture_path from bbs_user_profiler where company_id=%s"
                piclist=dbc.fetchonedb(sql,[forcompany_id])
                faceurl=None
                if piclist:
                    if piclist[0]:
                        if piclist[0]:
                            faceurl="http://img3.zz91.com/100x100/"+piclist[0]
                if not faceurl:
                    faceurl='http://static.m.zz91.com/aui/images/noavatar.gif'
                lista={'company_id':forcompany_id,'contact':contact,'position':position,'compname':compname,'faceurl':faceurl}
                listall.append(lista)
        return {'list':listall,'count':listcount}