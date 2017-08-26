#-*- coding:utf-8 -*-
class zmyrc:
    #----初始化ast数据库
    def __init__(self):
        self.dbc=dbc
    #----生意管家 供求管理
    def getmyproductslist(self,frompageCount="",limitNum="",company_id="",checkStatus=""):
        if (checkStatus=="" or checkStatus==None):
            checkStatus=1
        sql="select count(0) from products where company_id=%s and check_status=%s and is_del=0"
        alist=self.dbc.fetchonedb(sql,[company_id,checkStatus])
        if alist:
            listcount=alist[0]
        sql="select id,title,real_time,refresh_time,unpass_reason,expire_time from products where company_id=%s and check_status=%s and is_del=0 order by refresh_time desc limit "+str(frompageCount)+","+str(frompageCount+limitNum)+""
        alist=self.dbc.fetchalldb(sql,[company_id,checkStatus])
        listall=[]
        if alist:
            for list in alist:
                timenow=datetime.datetime.now()
                expire_time=list[5]
                is_expire=''
                if timenow>expire_time:
                    is_expire=1
                rlist={'proid':list[0],'protitle':list[1],'real_time':formattime(list[2],0),'refresh_time':formattime(list[3],0),'unpass_reason':list[4],'is_expire':is_expire}
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
                return 1
            else:
                return None
        else:
            return None
        #验证微信是否绑定
    def weixinbinding(self,weixinid):
        sql="select target_account from oauth_access where open_id=%s and target_account<>'0'"
        cursor.execute(sql,[weixinid]);
        list=cursor.fetchone()
        if list:
            return list[0]
        else:
            return None
    #--获得公司id
    def getcompanyid(self,account):
        sql="select company_id from  company_account where account=%s"
        cursor.execute(sql,[account])
        result=cursor.fetchone()
        if result:
            return result[0]