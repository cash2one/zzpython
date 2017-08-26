#-*- coding:utf-8 -*-
class zzweixin:
    #----初始化ast数据库
    def __init__(self):
        self.dbc=dbc
    #绑定的客户自动登录
    def weixinautologin(self,request,weixinid):
        if (weixinid and weixinid!=""):
            account=weixinbinding(weixinid)
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
    #--获得公司id
    def getcompanyid(self,account):
        sql="select company_id from  company_account where account=%s"
        result=self.dbc.fetchonedb(sql,[account])
        if result:
            return result[0]
    
#----微信积分
class weixinscore():
    def __init__(self):
        self.dbc=dbc
        self._account = None
        self._page=1
    def getscorelist(self,account,page=''):
        if account==None:
            return None
        if page==None or page=='':
            page=self._page
        listall=[]
        frompage=10*(int(page)-1)
        topage=10
        wdate=str(getToday())
        format="%Y-%m-%d";
        nowday=strtodatetime(wdate,format)
        sql="select score,gmt_created,validity from weixin_score where account=%s and rules_code=%s and validity>'"+str(nowday)+"' order by gmt_created desc limit "+str(frompage)+","+str(topage)+""
        returnlist=self.dbc.fetchalldb(sql,[account,'qiaodao'])
        for a in returnlist:
            bz=''
            if a[0]<0:
                bz='未签到'
                
            list={'score':a[0],'bz':bz,'gmt_created':str(formattime(a[1],1)),'validity':str(formattime(a[2],1))}
            listall.append(list)
        return listall
    def getprizelist(self,account,page=''):
        if account==None:
            return None
        if page==None or page=='':
            page=self._page
        listall=[]
        frompage=20*(int(page)-1)
        topage=20
        sql="select pic,title,score,num,gmt_created,content,id,closeflag,numall from weixin_prize where type=1 order by ord asc limit "+str(frompage)+","+str(topage)+""
        returnlist=self.dbc.fetchalldb(sql)
        for a in returnlist:
            list={'id':a[6],'pic':a[0],'title':a[1],'score':a[2],'num':a[3],'content':a[5],'gmt_created':str(formattime(a[4],1)),'closeflag':a[7],'numall':a[8]}
            listall.append(list)
        return listall
    def getprizelog(self,account,page=''):
        if account==None:
            return None
        if page==None or page=='':
            page=self._page
        listall=[]
        frompage=10*(int(page)-1)
        topage=10
        sql="select a.prizeid,a.score,a.gmt_created,b.title,a.ischeck from weixin_prizelog as a left join weixin_prize as b on a.prizeid=b.id where a.account=%s limit "+str(frompage)+","+str(topage)+""
        returnlist=self.dbc.fetchalldb(sql,[account])
        for a in returnlist:
            ischeck=a[4]
            if ischeck==1:
                ischeckvalue="已兑换"
            else:
                ischeckvalue=""
            list={'prizeid':a[0],'score':a[1],'gmt_created':str(formattime(a[2],1)),'title':a[3],'ischeckvalue':ischeckvalue}
            listall.append(list)
        return listall
    #----查看联系方式
    def getviewcontact(self,account):
        if account==None:
            return None
        sql="select id from weixin_prizelog where account=%s and prizeid=1 and ischeck=0"
        returnlist=self.dbc.fetchonedb(sql,[account])
        if returnlist:
            return 1
        else:
            return None
    #----更新兑换查看联系方式
    def saveviewcontact(self,account,company_id=''):
        if account==None:
            return None
        sql="select id from weixin_prizelog where account=%s and prizeid=1 and ischeck=0"
        returnlist=self.dbc.fetchonedb(sql,[account])
        if returnlist:
            sqlg="select id from weixin_lookcontactlog where company_id=%s and account=%s"
            returna=self.dbc.fetchonedb(sqlg,[company_id,account])
            if returna==None:
                sqlp="update weixin_prizelog set ischeck=1 where id=%s"
                self.dbc.updatetodb(sqlp,[returnlist[0]])
                gmt_created=datetime.datetime.now()
                sqlp="insert into weixin_lookcontactlog (account,company_id,gmt_created) values(%s,%s,%s)"
                self.dbc.updatetodb(sqlp,[account,company_id,gmt_created])
    #----失效积分
    def getlimitoutscore(self,account):
        if account==None:
            return 0
        wdate=str(getToday())
        format="%Y-%m-%d";
        nowday=strtodatetime(wdate,format)
        sql="select sum(score) from weixin_score where account=%s and validity<='"+str(nowday)+"'"
        returnlist=self.dbc.fetchonedb(sql,[account])
        if returnlist:
            if returnlist[0]==None:
                return 0
            else:
                return returnlist[0]
        else:
            return 0
    #---积分数
    def getscorecount(self,account):
        if account==None:
            return 0
        wdate=str(getToday())
        format="%Y-%m-%d";
        nowday=strtodatetime(wdate,format)
        sql="select sum(score) from weixin_score where account=%s and validity>'"+str(nowday)+"'"
        returnlist=self.dbc.fetchonedb(sql,[account])
        if returnlist:
            if returnlist[0]==None:
                inconescore=0
            else:
                inconescore=returnlist[0]
        else:
            inconescore=0
        
        sql="select sum(score) from weixin_prizelog where account=%s"
        returnlist=self.dbc.fetchonedb(sql,[account])
        if returnlist:
            xfscore=returnlist[0]
            if xfscore:
                leascore=int(xfscore)
            else:
                leascore=0
        else:
            leascore=0
            
        return inconescore-leascore
