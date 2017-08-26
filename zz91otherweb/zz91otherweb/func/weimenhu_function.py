#-*- coding:utf-8 -*-
from time import strftime, localtime
from datetime import timedelta, date
import datetime
class weimenhu:
    def __init__(self):
        self.dbc=dbc
        self.dblog=dblog
        self.dbwork=dbwork
        
#---微门户关键词库
#所有关键词
    def listallkeywords(self,frompageCount,limitNum,ptype=None,keywords='',pinyin=''):
        sqlarg=''
        argument=[]
        if ptype:
            if (ptype=="1"):
                sqlarg+=" and checked=1"
            elif (ptype=="0"):
                sqlarg+=" and checked=0"   
        if keywords:
            sqlarg+=' and label like %s'
            argument.append('%'+keywords+'%')   
        if pinyin:
            sqlarg+=' and pingyin=%s'
            argument.append(pinyin)       
        sql1='select count(0) from daohang where sid=3738'+sqlarg
        sql='select id,label,pingyin,gmt_created,checked from daohang where sid=3738'+sqlarg
        sql=sql+' order by id desc limit '+str(frompageCount)+','+str(limitNum)
        count=self.dbc.fetchnumberdb(sql1,argument)
        resultlist=self.dbc.fetchalldb(sql,argument)
        listall=[]
        checkedtxt=''
        for result in resultlist:
            kid=result[0]
            label=result[1]
            pingyin=result[2]
            gmt_created=formattime(result[3],0)
            checked=result[4]
            checkperson=self.getcheckperson(kid)
            if checked==0 or not checked:
                checkedtxt='未审核'
            if checked==1:
                checkedtxt='已审核'
            list={'id':kid,'label':label,'pingyin':pingyin,'gmt_created':gmt_created,'checkedtxt':checkedtxt,'checkperson':checkperson}
            listall.append(list)
        return {'list':listall,'count':count}
    def getcheckperson(self,kid):
        sql="select username,dodate from check_weimenhu where keyid=%s"
        result=self.dbwork.fetchonedb(sql,[kid])
        if result:
            return result[0]+' 审核时间：'+formattime(result[1],2)
        else:
            return ''
    def listallkeywords_del(self,frompageCount,limitNum,ptype=None,keywords='',pinyin=''):
        sqlarg=''
        argument=[]
        if ptype:
            if (ptype=="1"):
                sqlarg+=" and checked=1"
            elif (ptype=="0"):
                sqlarg+=" and checked=0"   
        if keywords:
            sqlarg+=' and label like %s'
            argument.append('%'+keywords+'%')   
        if pinyin:
            sqlarg+=' and pingyin=%s'
            argument.append(pinyin)       
        sql1='select count(0) from daohang_del where sid=3738'+sqlarg
        sql='select id,label,pingyin,gmt_created,checked from daohang_del where sid=3738'+sqlarg
        sql=sql+' order by gmt_created desc limit '+str(frompageCount)+','+str(limitNum)
        count=self.dbc.fetchnumberdb(sql1,argument)
        resultlist=self.dbc.fetchalldb(sql,argument)
        listall=[]
        checkedtxt=''
        for result in resultlist:
            kid=result[0]
            label=result[1]
            pingyin=result[2]
            gmt_created=formattime(result[3],0)
            checked=result[4]
            if checked==0 or not checked:
                checkedtxt='未审核'
            if checked==1:
                checkedtxt='已审核'
            list={'id':kid,'label':label,'pingyin':pingyin,'gmt_created':gmt_created,'checkedtxt':checkedtxt}
            listall.append(list)
        return {'list':listall,'count':count}
    #审核、删除 统计
    def checkweimenhu(self,request,keyid="",dotype=""):
        username=request.session.get("username",None)
        dodate=datetime.datetime.now()
        if username and keyid:
            if dotype==2:
                sql="select id from daohang where id=%s and checked=0"
                resultlist=self.dbc.fetchonedb(sql,[keyid])
                if resultlist:
                    sql="select id from check_weimenhu where keyid=%s"
                    resultlist=self.dbwork.fetchonedb(sql,[keyid])
                    if not resultlist:
                        sql1="insert into check_weimenhu (keyid,username,dotype,dodate) values(%s,%s,%s,%s)"
                        self.dbwork.updatetodb(sql1,[keyid,username,dotype,dodate])
            else:
                sql="select id from check_weimenhu where keyid=%s"
                resultlist=self.dbwork.fetchonedb(sql,[keyid])
                if not resultlist:
                    sql1="insert into check_weimenhu (keyid,username,dotype,dodate) values(%s,%s,%s,%s)"
                    self.dbwork.updatetodb(sql1,[keyid,username,dotype,dodate])
    def gettongjiweimenhu(self,frompageCount,limitNum,gmt_begin,gmt_end):
        sqlarg=''
        argument=[]
        if gmt_begin:
            sqlarg+=' and dodate >%s'
            argument.append(gmt_begin)
        if gmt_end:
            sqlarg+=' and dodate <%s'
            argument.append(gmt_end)
        usernamelist="'kangxy','leicf','fengh','majunjie','linmm','lihexu','chenxx','shenzl','mengyu','yangxj','wulf'"
        sql1='select count(0) from auth_user where username in ('+usernamelist+')'
        sql="select id,username from auth_user where username in ("+usernamelist+") "
        sql=sql+' order by id desc limit '+str(frompageCount)+','+str(limitNum)
        resultlist=self.dbwork.fetchalldb(sql)
        count=self.dbwork.fetchnumberdb(sql1)
        listall=[]
        for list in resultlist:
            username=list[1]
            name=''
            sqln="select name from staff where account=%s"
            result=self.dbwork.fetchonedb(sqln,[username])
            if result:
                name=result[0]
            userid=list[0]
            sqld="select count(*) from check_weimenhu where dotype=1 "+sqlarg+" and username='"+username+"' "
            sccount=self.dbwork.fetchonedb(sqld,argument)[0]
            sqld="select count(*) from check_weimenhu where dotype=2 "+sqlarg+" and username='"+username+"' "
            shcount=self.dbwork.fetchonedb(sqld,argument)[0]
            list={'name':name,'sccount':sccount,'shcount':shcount,'count':shcount+sccount}
            listall.append(list)
        return {'list':listall,'count':count}
        
    def shenheok(self,k_id='',request=""):
        s=1
        gmt_created=datetime.datetime.now()
        self.checkweimenhu(request,keyid=k_id,dotype=2)
        sql="update daohang set checked=%s,gmt_created=%s where id=%s"
        self.dbc.updatetodb(sql,[s,gmt_created,k_id])
        
        return
    #一键审核1
    def shenheokall(self,checkid,request=""):
        for id in checkid:
            s=1
            gmt_created=datetime.datetime.now()
            self.checkweimenhu(request,keyid=id,dotype=2)
            sql="update daohang set checked=%s,gmt_created=%s where id=%s"
            self.dbc.updatetodb(sql,[s,gmt_created,id])
        return
    
    def shenheno(self,k_id=''):
        s=0
        gmt_created=datetime.datetime.now()
        sql="update daohang set checked=%s,gmt_created=%s where id=%s"
        self.dbc.updatetodb(sql,[s,gmt_created,k_id])
        return
    
    #一键删除1
    def delall1(self,checkid,request=""):
        gmt_created=datetime.datetime.now()
        for id in checkid:
            self.checkweimenhu(request,keyid=id,dotype=1)
            sql="update daohang set gmt_created=%s where id=%s"
            self.dbc.updatetodb(sql,[gmt_created,id])
            sql="insert into daohang_del  select * from daohang where id=%s"
            self.dbc.updatetodb(sql,[id])
            sql="delete from daohang where id=%s"
            self.dbc.updatetodb(sql,[id])
        return

    
#-----未审核客户搜索关键字
    def getnocheckedkeywords(self,frompageCount,limitNum,ptype=None,keywords=''):
        #限制时间，只显示此时间以后的数据
        limited_time=" and gmt_target>='2015-07-01 00:00:00' " 
        sqlarg=''
        argument=[]
        if not ptype:
            sqlarg+=" and status=0"
        else:
            if (ptype=="1"):
                sqlarg+=" and status=1"
            elif (ptype=="0"):
                sqlarg+=" and status=0"
        if keywords:
            sqlarg+=' and kw like %s'
            argument.append('%'+keywords+'%')        
        sql1='select count(DISTINCT kw) from analysis_trade_keywords where id>0 and not exists(select label from daohang where label=analysis_trade_keywords.kw)'+limited_time+sqlarg
        sql='select DISTINCT kw,id,num,status,gmt_target from analysis_trade_keywords where id>0  and not exists(select label from daohang where label=analysis_trade_keywords.kw) '+limited_time+sqlarg
        sql=sql+' order by id desc limit '+str(frompageCount)+','+str(limitNum)
        count=self.dbc.fetchnumberdb(sql1,argument)
        resultlist=self.dbc.fetchalldb(sql,argument)
        listall=[]
        statustxt=''
        for result in resultlist:
            kid=result[0]
            kw=result[1]
            #pingyin=''
            num=result[2]
            status=result[3]
            if status==0 or not status:
                statustxt='未审核'
            if status==1:
                statustxt='已审核'
            gmt_target=formattime(result[4],0)
            list={'id':kid,'kw':kw,'num':num,'gmt_target':gmt_target,'statustxt':statustxt}
            listall.append(list)
        return {'list':listall,'count':count}
    
    
    def statusok(self,k_id=''):
        s=1
        gmt_modified=datetime.datetime.now()
        sql="update analysis_trade_keywords set status=%s,gmt_modified=%s where kw=%s"
        self.dbc.updatetodb(sql,[s,gmt_modified,k_id])
        return
    
    def statusno(self,k_id=''):
        s=0
        gmt_modified=datetime.datetime.now()
        sql="update analysis_trade_keywords set status=%s,gmt_modified=%s where kw=%s"
        self.dbc.updatetodb(sql,[s,gmt_modified,k_id])
        return
    
    def addbbs_post_invite(self,checkid):
        for id in checkid:
            #sql1="select id from daohang where id=%s"
            #sql1="select a.id from analysis_trade_keywords as a left join daohang as b on a.kw=b.label where a.id=%s"
            sql1="select id from daohang label=%s and sid=3738"
            result=self.dbc.fetchonedb(sql1,[id])
            if not result:
                kw=id
                label=kw.replace("+","")
                label=label.replace(" ","")
                
                """
                sql3="select kw from analysis_trade_keywords where id=%s"
                result1=self.dbc.fetchonedb(sql3,[id])
                if result1:
                    label=result1[0]
                    if label:
                        label=label.replace("+","")
                        label=label.replace(" ","")
                """    
                pingyin=chinese_abstract(label.decode('utf-8','ignore'))
                pingyin=pingyin.replace("#","jin")
                gmt_created=datetime.datetime.now()
                checked=1
                sql="insert into daohang(label,pingyin,gmt_created,checked,sid) values(%s,%s,%s,%s,3738)"
                self.dbc.updatetodb(sql,[label,pingyin,gmt_created,checked])
                #更改原表状态
                s=1
                sql2="update analysis_trade_keywords set status=%s where kw=%s"
                self.dbc.updatetodb(sql2,[s,id])
                #return 1
            else:
                sql2="update analysis_trade_keywords set status=%s where kw=%s"
                self.dbc.updatetodb(sql2,[1,id])
                #return None
        return
    #一键审核2
    def shenheokall2(self,checkid):
        gmt_modified=datetime.datetime.now()
        for id in checkid:
            s=1
            sql="update analysis_trade_keywords set status=%s,gmt_modified=%s where kw=%s"
            self.dbc.updatetodb(sql,[s,gmt_modified,id])
        return
    #一键删除2
    def delall2(self,checkid):
        for id in checkid:
            sql="delete from analysis_trade_keywords where kw=%s"
            self.dbc.updatetodb(sql,[id])
        return
    
    #根据时间导出数据
    def export_datalist(self,gmt_begin='',gmt_end=''):
        sqlarg=''
        argument=[]
        if gmt_begin:
            sqlarg+=" and gmt_created>=%s"
            argument.append(gmt_begin)
        if gmt_end:
            sqlarg+=" and gmt_created<=%s"
            argument.append(gmt_end)
        sql1='select id,label,pingyin,gmt_created,checked from daohang_del where id>0'+sqlarg+' order by gmt_created desc'
        resultlist=self.dbc.fetchalldb(sql1,argument)
        if resultlist:
            listall=[]
            checktxt=''
            for result in resultlist:
                id=result[0]
                label=result[1]
                pingyin=result[2]
                #首页
                url_index="www.zz91.com/cp/"+pingyin+"/"
                #价格
                url_price="www.zz91.com/cp/"+pingyin+"/price.html"
                url_pricemore="www.zz91.com/cp/"+pingyin+"/pricemore-1.html"
                #商家
                url_company="www.zz91.com/cp/"+pingyin+"/company.html"
                url_companymore="www.zz91.com/cp/"+pingyin+"/companymore-1.html"
                #采购
                url_caigou="http://www.zz91.com/cp/"+pingyin+"/trademore-1.html?ptype=1"
                #供求
                url_gongqiu="http://www.zz91.com/cp/"+pingyin+"/trademore-1.html?ptype=0"
                gmt_created=result[3]
                check=result[4]
                if check==1:
                    checktxt="已审"
                if check==0:
                    checktxt="未审"
                list={'id':id,'label':label,'pingyin':pingyin,'url_index':url_index,'url_price':url_price,'url_pricemore':url_pricemore,'url_company':url_company,'url_companymore':url_companymore,'url_caigou':url_caigou,'url_gongqiu':url_gongqiu,'gmt_created':gmt_created,'checktxt':checktxt,}
                listall.append(list)
            return listall
        else:
            return 0
    
    def getselectexport(self,checkid):
        listall=[]
        for id in checkid:
            sql="select id,label,pingyin,gmt_created,checked from daohang_del where id=%s"
            result=self.dbc.fetchonedb(sql,[id])
            if result:
                id=result[0]
                label=result[1]
                pingyin=result[2]
                #首页
                url_index="www.zz91.com/cp/"+pingyin+"/"
                #价格
                url_price="www.zz91.com/cp/"+pingyin+"/price.html"
                url_pricemore="www.zz91.com/cp/"+pingyin+"/pricemore-1.html"
                #商家
                url_company="www.zz91.com/cp/"+pingyin+"/company.html"
                url_companymore="www.zz91.com/cp/"+pingyin+"/companymore-1.html"
                #采购
                url_caigou="http://www.zz91.com/cp/"+pingyin+"/trademore-1.html?ptype=1"
                #供求
                url_gongqiu="http://www.zz91.com/cp/"+pingyin+"/trademore-1.html?ptype=0"
                gmt_created=result[3]
                check=result[4]
                if check==1:
                    checktxt="已审"
                if check==0:
                    checktxt="未审"
                list={'id':id,'label':label,'pingyin':pingyin,'url_index':url_index,'url_price':url_price,'url_pricemore':url_pricemore,'url_company':url_company,'url_companymore':url_companymore,'url_caigou':url_caigou,'url_gongqiu':url_gongqiu,'gmt_created':gmt_created,'checktxt':checktxt,}
                listall.append(list)
        return listall
    
    
    
    
    
    
        