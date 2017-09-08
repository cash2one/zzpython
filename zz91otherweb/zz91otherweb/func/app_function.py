#-*- coding:utf-8 -*-
from time import strftime, localtime
from datetime import timedelta, date
import datetime
from symbol import argument
#奖品map
JIANGPIN={
          '-1':'未抽',
          '7':'没中',
          '0':'10元再生钱包',
          '1':'iphone6s',
          '2':'话费30',
          '3':'来电宝会员',
          '4':'再生通会员',
          '5':'商务大全',
          '6':'粽子大礼包',
          }
#砸金蛋奖品
JIANGPIN_zajindan={
          '1':'没中',
          '2':'绿茶糕',
          '3':'蛋黄酥',
          '4':'零食包',
          '5':'坚果包',
          '6':'广告位',
          '7':'20元现金红包'
          }
#刮刮乐奖品
JIANGPIN_guaguale={
          '0':'没中',
          '1':'再生钱包10元',
          '2':'再生钱包20元',
          '3':'再生钱包30元',
          '4':'再生钱包50元',
          }
#国庆抽奖奖品
JIANGPIN_guoqin={
          '9':'未抽',
          '0':'百度微门户广告6个月',
          '1':'再生钱包600元',
          '2':'移动端自动刷新服务3个月',
          '3':'APP供求置顶广告2个月',
          '4':'首页广告3个月',
          }
#绑定类型
BANGDING={
          '0':'抽奖记录',
          '1':'微信关注',
          '2':'分享链接',
          '3':'安装APP',
          '4':'砸金蛋',
          '5':'刮刮乐',
          '6':'2016国庆抽奖',
          '7':'2016台州塑交会抽奖',
          '8':'双11充值抽奖活动'
          }
JIANGPIN_taizhou={"0":"环保袋",
                 "1":"吉祥物",
                 "2":"2016再生资源商务大全",
                 "3":"移动端供求置顶服务2个月",
                 "4":"ZZ91《再生影响力》栏目专访",
                 "5":"移动端企业秀服务一年",
                 "6":"移动端独家广告2个月",
                 "7":"300元再生钱包",
                 '-1':'关注公众号',
                 }
class zapp:
    def __init__(self):
        self.dbc=dbc
        self.dblog=dblog
    def getmessagelist(self,frompageCount,limitNum,account='',ptype=None):
        sqlarg=''
        argument=[]
        if account:
            sqlarg+=' and account=%s'
            argument.append(account)
        if ptype:
            if (ptype=="1"):
                sqlarg+=' and company_id>0'
            else:
                sqlarg+=' and company_id=0'
        sql1='select count(0) from app_message where id>0'+sqlarg
        sql='select id,title,url,content,gmt_created,company_id from app_message where id>0'+sqlarg
        sql=sql+' order by id desc limit '+str(frompageCount)+','+str(limitNum)
        count=self.dbc.fetchnumberdb(sql1,argument)
        resultlist=self.dbc.fetchalldb(sql,argument)
        listall=[]
        for result in resultlist:
            id=result[0]
            title=result[1]
            url=result[2]
            content=result[3]
            gmt_created=formattime(result[4],0)
            company_id=result[5]
            list={'id':id,'title':title,'url':url,'content':content,'gmt_created':gmt_created,'company_id':company_id}
            listall.append(list)
        return {'list':listall,'count':count}
    #计费类型
    def getftypename(self,id):
        sql='select name from pay_wallettype where id=%s'
        result=self.dbc.fetchonedb(sql,[id])
        if result:
            return result[0]
        else:
            return "无"
    #app安装用户管理
    def installuserlist(self,frompageCount,limitNum,account='',gmt_begin="",gmt_end="",open_type=""):
        sqlarg=''
        argument=[]
        if account:
            sqlarg+=' and target_account=%s'
            argument.append(account)
        if gmt_begin:
            sqlarg+=" and gmt_created>=%s"
            argument.append(gmt_begin)
        if gmt_end:
            sqlarg+=" and gmt_created<=%s"
            argument.append(gmt_end)
        if not open_type:
            open_type="app.zz91.com"
        sql1='select count(0) from oauth_access where open_type="'+open_type+'"'+sqlarg
        sql='select id,open_id,open_type,target_account,closeflag,appsystem,gmt_created from oauth_access where open_type="'+open_type+'"'+sqlarg
        sql=sql+' order by id desc limit '+str(frompageCount)+','+str(limitNum)
        count=self.dbc.fetchnumberdb(sql1,argument)
        resultlist=self.dbc.fetchalldb(sql,argument)
        listall=[]
        for result in resultlist:
            id=result[0]
            open_id=result[1]
            open_type=result[2]
            target_account=result[3]
            instrudycode=self.getcompanyinstrudy(target_account)
            closeflag=result[4]
            gmt_created=formattime(result[6])
            appsystem=result[5]
            company_id=self.getcompany_id(target_account)
            
            list={'id':id,'open_id':open_id,'open_type':open_type,'target_account':target_account,'closeflag':closeflag,'appsystem':appsystem,'gmt_created':gmt_created,'instrudycode':instrudycode,'company_id':company_id}
            listall.append(list)
        return {'list':listall,'count':count}
    #app安装 图表统计
    def getinstallapp(self,ftype='',gmt_begin='',gmt_end='',limit=''):
        argument=[]
        sqlarg=''
        if gmt_begin:
            sqlarg+=' and gmt_created>=%s'
            argument.append(gmt_begin)
        if gmt_end:
            sqlarg+=' and gmt_created<=%s'
            argument.append(gmt_end)
        if ftype:
            sqlarg+=' and appsystem=%s'
            argument.append(ftype)
        sql='select count(id) as appcount,gmt_date from app_installchart where id>0 '+sqlarg
        sql+=' group by gmt_date order by gmt_created desc '
        if not gmt_begin and not gmt_end:
            sql+='limit 0,31'
        #sql='SELECT appcount,gmt_date FROM app_installchart  limit 0,'+str(limit)
        if argument:
            resultlist=self.dbc.fetchalldb(sql,argument)
        else:
            resultlist=self.dbc.fetchalldb(sql)
        listall=[]
        for result in resultlist[::-1]:
            appcount=result[0]
            gmt_date=result[1]
            list={'count':appcount,'gmt_date':gmt_date}
            listall.append(list)
        return listall
    #移动端拨打电话列表
    def telcheck(self,frompageCount,limitNum,tel='',pagefrom='',gmt_begin="",gmt_end=""):
        sqlarg=''
        argument=[]
        if tel:
            sqlarg+=' and tel like "'+tel+'%"'
            #argument.append(tel)
        if pagefrom:
            sqlarg+=' and pagefrom=%s'
            argument.append(pagefrom)
        if gmt_begin:
            sqlarg+=" and gmt_created>=%s"
            argument.append(gmt_begin)
        if gmt_end:
            sqlarg+=" and gmt_created<=%s"
            argument.append(gmt_end)
        sql1='select count(0) from phone_telclick_log where id>0 '+sqlarg
        sql='select id,company_id,pagefrom,tel,num,gmt_created,url from phone_telclick_log where id>0 '+sqlarg
        sql=sql+' order by id desc limit '+str(frompageCount)+','+str(limitNum)
        count=self.dbc.fetchnumberdb(sql1,argument)
        resultlist=self.dbc.fetchalldb(sql,argument)
        listall=[]
        for result in resultlist:
            id=result[0]
            company_id=result[1]
            pagefrom=result[2]
            tel=result[3]
            num=result[4]
            gmt_created=formattime(result[5])
            url=result[6]
            list={'id':id,'company_id':company_id,'pagefrom':pagefrom,'tel':tel,'num':num,'gmt_created':gmt_created,'url':url}
            listall.append(list)
        return {'list':listall,'count':count}
    
    #获得app用户搜索关键字列表,查询company_id和ktype
    def getuserKeywords(self,frompageCount,limitNum,account='',company_id='',ktype=''):
        sqlarg=''
        argument=[]
        if account:
            sqlarg+=' and account=%s'
            argument.append(account)

        if company_id:
            sqlarg+=" and company_id=%s"
            argument.append(company_id)
        if ktype:
            sqlarg+=" and ktype=%s"
            argument.append(ktype)
        
        sql1='select count(0) from app_user_keywords where id>0'+sqlarg    
        sql='select id,appid,company_id,ktype,keywords,gmt_created from app_user_keywords where id>0'+sqlarg
        sql=sql+' order by id desc limit '+str(frompageCount)+','+str(limitNum)
        count=self.dbc.fetchnumberdb(sql1,argument)
        resultlist=self.dbc.fetchalldb(sql,argument)
        listall=[]
        for result in resultlist:
            id=result[0]
            appid=result[1]
            company_id=result[2]
            ktype=result[3]
            keywords=result[4]
            gmt_created=formattime(result[5])
            list={'id':id,'appid':appid,'company_id':company_id,'ktype':ktype,'keywords':keywords,'gmt_created':gmt_created}
            listall.append(list)
        return {'list':listall,'count':count}
    #app 客户使用统计
    def eveuserstate(self,ftype='',gmt_begin='',gmt_end='',type=''):
        """
        current_date= date.today()#当前日期
        start_time=str(current_date)+" 00:00:00" #当前日期的0点
        end_time=str(current_date)+" 23:59:59" #当前日期的最后一秒
        #新增用户数
        sql="select count(*) from oauth_access where gmt_created >= %s and gmt_created <= %s"
        newUser_num=self.dbc.fetchnumberdb(sql,[start_time,end_time])
        #总活跃用户数(当天登录总记录数)
        sql1="select count(*) from app_logincount where login_date >= %s and login_date <= %s"
        all_active_num=self.dbc.fetchalldb(sql1,[start_time,end_time])
        #当日活跃数    
        #沉默用户数
        sql2=
        silence_num=
        
        #启动次数
        start_times=0
        sql4="select login_count from app_logincount where login_date >= %s and login_date <= %s"
        start_times_result=self.dbc.fetchalldb(sql4,[start_time,end_time])
        for result in start_times_result:
            start_times=start_times+result
        return{'newUser_num':newUser_num,'active_num':active_num,'silence_num':silence_num}
        """
        argument=[]
        sqlarg=''
        if gmt_begin:
            sqlarg+=' and gmt_date>=%s'
            argument.append(gmt_begin)
        if gmt_end:
            sqlarg+=' and gmt_date<=%s'
            argument.append(gmt_end)
            
        sql='select t_new,t_active,t_login,t_noactive,t_pv,gmt_date from app_tongji where id>0 '+sqlarg
        sql+=' order by gmt_date desc '
        if not gmt_begin and not gmt_end:
            sql+='limit 0,31'
        if argument:
            resultlist=self.dblog.fetchalldb(sql,argument)
        else:
            resultlist=self.dblog.fetchalldb(sql)
        listall=[]
        for result in resultlist[::-1]:
            appcount=result[int(type)-1]
            gmt_date=formattime(result[5])
            list={'count':appcount,'gmt_date':gmt_date}
            listall.append(list)
        return listall
    #app 客户使用统计
    def everyhourstate(self,ftype='',gmt_begin='',gmt_end=''):
        sfiled="t_active"
        
        hlist=range(0,24)
        listall=[]
        for h in hlist:
            argument=[]
            sqlarg=''
            if gmt_begin:
                sqlarg+=' and gmt_date>=%s'
                argument.append(gmt_begin)
            if gmt_end:
                sqlarg+=' and gmt_date<=%s'
                argument.append(gmt_end)
            if ftype=="1":
                sfiled="t_active"
            if ftype=="2":
                sfiled="t_pv"
            argument.append(h)
            sql='select sum('+sfiled+') from app_tongji_day where id>0 '+sqlarg+' and gmt_hour=%s'
            resultlist=self.dblog.fetchonedb(sql,argument)
            appcount=resultlist[0]
            gmt_date=h
            list={'count':appcount,'gmt_date':gmt_date}
            listall.append(list)
        return listall
    
    #-----以下是抢购商品表(goods)
    #增加抢购商品
    #goodsID,goodsName,billing_Class_ID,start_Time,end_Time,original_Price,present_Price,pic,status,release_Time
    def addgoodsok(self,goodsName='',goodsname_fu='',billing_Class_ID='',start_Time='',end_Time='',original_Price='',present_Price='',sales_Num='',left_Num='',pic='',release_Time='',tourl='',ad_type='',ad_position='',status='',havenum=""):
        sql = "insert into app_goods(goodsName,goodsname_fu,billing_Class_ID,start_Time,end_Time,original_Price,present_Price,sales_Num,left_Num,pic,release_Time,tourl,ad_type,ad_position,status,havenum) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        self.dbc.updatetodb(sql,[goodsName,goodsname_fu,billing_Class_ID,start_Time,end_Time,original_Price,present_Price,sales_Num,left_Num,pic,release_Time,tourl,ad_type,ad_position,status,havenum])
        return
    def editgoodsok(self,goodsName='',goodsname_fu='',billing_Class_ID='',start_Time='',end_Time='',original_Price='',present_Price='',sales_Num='',left_Num='',pic='',tourl='',ad_type='',ad_position='',status='',havenum="",gid=""):
        sql = "update app_goods set goodsName=%s,goodsname_fu=%s,billing_Class_ID=%s,start_Time=%s,end_Time=%s,original_Price=%s,present_Price=%s,sales_Num=%s,left_Num=%s,pic=%s,tourl=%s,ad_type=%s,ad_position=%s,status=%s,havenum=%s where id=%s"
        self.dbc.updatetodb(sql,[goodsName,goodsname_fu,billing_Class_ID,start_Time,end_Time,original_Price,present_Price,sales_Num,left_Num,pic,tourl,ad_type,ad_position,status,havenum,gid])
        return
    def getgoods(self,gid):
        sql="select id,goodsName,billing_Class_ID,start_Time,end_Time,original_Price,present_Price,sales_Num,left_Num,pic,status,release_Time,tuijian,goodsname_fu,tourl,ad_type,ad_position,havenum from app_goods where id=%s"
        result=self.dbc.fetchonedb(sql,[gid])
        if result:
            id=result[0]
            goodsName=result[1]
            goodsname_fu=result[13]
            if not goodsname_fu:
                goodsname_fu=""
            billing_Class_ID=result[2]
            billingname=self.getftypename(billing_Class_ID)
            start_Time=formattime(result[3],0)
            end_Time=formattime(result[4],0)
            original_Price=result[5]
            present_Price=result[6]
            sales_Num=result[7]
            left_Num=result[8]
            pic=result[9]
            if not pic:
                pic=""
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
            if not tourl:
                tourl=""
            ad_type=result[15]
            ad_position=result[16]
            havenum=result[17]
            if not havenum:
                havenum=5
            list={'id':id,'goodsName':goodsName,'goodsname_fu':goodsname_fu,'billing_Class_ID':billing_Class_ID,'start_Time':start_Time,'end_Time':end_Time,'original_Price':original_Price,'present_Price':present_Price,'sales_Num':sales_Num,'left_Num':left_Num,'pic':pic,'statustxt':statustxt,'status':status,'release_Time':release_Time,'billingname':billingname,'tuijiantxt':tuijiantxt,'tourl':tourl,'ad_type':ad_type,'ad_position':ad_position,'havenum':havenum}
        return list
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
                 
        sql1='select count(0) from app_goods where id>0'+sqlarg
        sql='select id,goodsName,billing_Class_ID,start_Time,end_Time,original_Price,present_Price,sales_Num,left_Num,pic,status,release_Time,tuijian,goodsname_fu,tourl,ad_type,ad_position,havenum from app_goods where id>0 '+sqlarg
        sql=sql+' order by id desc limit '+str(frompageCount)+','+str(limitNum)
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
            if not havenum:
                havenum=5
            list={'id':id,'goodsName':goodsName,'goodsname_fu':goodsname_fu,'billing_Class_ID':billing_Class_ID,'start_Time':start_Time,'end_Time':end_Time,'original_Price':original_Price,'present_Price':present_Price,'sales_Num':sales_Num,'left_Num':left_Num,'pic':pic,'statustxt':statustxt,'release_Time':release_Time,'billingname':billingname,'tuijiantxt':tuijiantxt,'tourl':tourl,'ad_type':ad_type,'adtypetext':adtypetext,'ad_position':ad_position,'havenum':havenum}
            listall.append(list)
        return {'list':listall,'count':count}
    
    def turnon(self,goodsID=''):
        s=1
        sql="update app_goods set status=%s where id=%s"
        self.dbc.updatetodb(sql,[s,goodsID])
        return
    
    def turnoff(self,goodsID=''):
        s=0
        sql="update app_goods set status=%s where id=%s"
        self.dbc.updatetodb(sql,[s,goodsID])
        return
    
    #推荐
    def tuijianon(self,goodsID=''):
        s=1
        sql="update app_goods set tuijian=%s where id=%s"
        self.dbc.updatetodb(sql,[s,goodsID])
        return
    
    #取消推荐
    def tuijianoff(self,goodsID=''):
        s=0
        sql="update app_goods set tuijian=%s where id=%s"
        self.dbc.updatetodb(sql,[s,goodsID])
        return

#---以下是app推送供求    
    #获得10个大类
    def gettypelist(self):
        sql="select code,label from category where parent_code='1000'"
        resultlist=self.dbc.fetchalldb(sql)
        listall=[]
        if resultlist:
            for result in resultlist:
                code=result[0]
                label=result[1] 
                list={'code':code,'label':label}
                listall.append(list)
        return {'list':listall}
    
    def getcategorylist(self,code):
        sql="select code,label from category where parent_code=%s"
        resultlist=self.dbc.fetchalldb(sql,[code])
        listall=[]
        if resultlist:
            for result in resultlist:
                code=result[0]
                label=result[1] 
                list={'code':code,'label':label}
                listall.append(list)
        return listall
    
    #根据code获得10个大类中的一个类的label
    def getcategorylabel(self,code):
        sql="select label from category where code=%s"
        resultlist=self.dbc.fetchonedb(sql,[code])
        if resultlist:
            return resultlist[0]
    #根据id获得获得详细信息
    def getapppushdetail(self,pid):
        sql="select title,code,content from app_push_tuijian where id=%s"
        resultlist=self.dbc.fetchonedb(sql,[pid])
        if resultlist:
            title=resultlist[0]
            code=resultlist[1]
            content=resultlist[2]
            list={"title":title,"code":code,"content":content}
        return list
    
    #过得app推送列表
    def getapppushlist(self,frompageCount,limitNum,gmt_begin="",gmt_end=""):
        sqlarg=''
        argument=[]
        if gmt_begin:
            sqlarg+=" and gmt_created>=%s"
            argument.append(gmt_begin)
        if gmt_end:
            sqlarg+=" and gmt_created<=%s"
            argument.append(gmt_end)
        sql1="select count(0) from app_push_tuijian where id>0"+sqlarg
        sql="select id,code,title,weburl,gmt_created from app_push_tuijian where id>0"+sqlarg
        sql=sql+' order by id desc limit '+str(frompageCount)+','+str(limitNum)
        count=self.dbc.fetchnumberdb(sql1,argument)
        resultlist=self.dbc.fetchalldb(sql,argument)
        listall=[]
        if resultlist:
            for result in resultlist:
                id=result[0]
                code=result[1]
                category_txt=self.getcategorylabel(code)
                title=result[2]
                weburl=result[3]
                gmt_created=formattime(result[4])
                list={"id":id,"category_txt":category_txt,"title":title,"weburl":weburl,"gmt_created":gmt_created}
                listall.append(list)
        return {'list':listall,'count':count}
    #增加推送消息
    def addpush(self,title,typeid,content,pubdate):
        sql=" insert into app_push_tuijian(code,title,content,gmt_created) values(%s,%s,%s,%s)"
        self.dbc.updatetodb(sql,[typeid,title,content,pubdate])
    #更新推送消息
    def updatepush(self,title,typeid,content,pid):
        gmt_created=datetime.datetime.now()  
        sql="update app_push_tuijian set title=%s,content=%s,gmt_created=%s where id=%s"
        self.dbc.updatetodb(sql,[title,content,gmt_created,pid])
    #删除推送消息
    def delthisp(self,id):
        sql='delete from app_push_tuijian where id=%s'
        self.dbc.updatetodb(sql,[id])
        
    #钱包优惠管理列表
    def getqianbaogglist(self,frompageCount,limitNum,ptype="",adtxt="",gmt_begin="",gmt_end=""):
        sqlarg=''
        argument=[]
        if ptype:
            if (ptype=="1"):
                sqlarg+=" and closeflag=1"
            elif (ptype=="0"):
                sqlarg+=" and closeflag=0"
        if adtxt:
            sqlarg+=" and txt=%s"
            argument.append(adtxt)
        if gmt_begin:
            sqlarg+=" and begin_time>=%s"
            argument.append(gmt_begin)
        if gmt_end:
            sqlarg+=" and end_time<=%s"
            argument.append(gmt_end)
        sql1="select count(0) from qianbao_gg where id>0"+sqlarg
        sql="select id,begin_time,end_time,infee,sendfee,txt,closeflag from qianbao_gg where id>0"+sqlarg
        sql=sql+' order by id desc limit '+str(frompageCount)+','+str(limitNum)
        count=self.dbc.fetchnumberdb(sql1,argument)
        resultlist=self.dbc.fetchalldb(sql,argument)
        listall=[]
        #statustxt=''
        if resultlist:
            for result in resultlist:
                statustxt=''
                id=result[0]
                begin_time=formattime(result[1],0)
                end_time=formattime(result[2],0)
                infee=result[3]
                sendfee=result[4]
                txt=result[5]
                closeflag=result[6]
                if closeflag==0:
                    statustxt="已开启"
                if closeflag==1:
                    statustxt="已关闭"
                list={"id":id,"begin_time":begin_time,"end_time":end_time,"infee":infee,"sendfee":sendfee,"txt":txt,"statustxt":statustxt,"closeflag":closeflag}
                listall.append(list)
        return {'list':listall,'count':count}
    def getqianbao_one(self,id):
        sql="select id,begin_time,end_time,infee,sendfee,txt from qianbao_gg where id=%s"
        result=self.dbc.fetchonedb(sql,[id])
        if result:
            id=result[0]
            begin_time=formattime(result[1],0)
            end_time=formattime(result[2],0)
            infee=result[3]
            sendfee=result[4]
            adwords=result[5]
            list={'id':id,'begin_time':begin_time,'end_time':end_time,'infee':infee,'sendfee':sendfee,'adwords':adwords}
            return list
    #开
    def flagon(self,id):
        s=1
        sql="update qianbao_gg set closeflag=%s where id=%s"
        self.dbc.updatetodb(sql,[s,id])
        return
    #关
    def flagoff(self,id):
        s=0
        sql="update qianbao_gg set closeflag=%s where id=%s"
        self.dbc.updatetodb(sql,[s,id])
        return
    
    def getcompanyinstrudy(self,account):
        sql="select c.industry_code,b.label from company as c left join company_account as a on a.company_id=c.id left OUTER join category as b on b.code=c.industry_code where a.account=%s"
        result=self.dbc.fetchonedb(sql,[account])
        if result:
            return {'code':result[1],'name':result[1]}
    #微信分组
    def getwxgroup(self,code=""):
        list={'10001000':('废塑料','103'),'10001001':('废金属','102'),'10001002':('废纸','106'),'10001003':('废旧轮胎与废橡胶','107'),'10001004':('废纺织品与废皮革','104'),'10001005':('废电子电器','105'),'10001006':('废玻璃','114'),'10001007':('废旧二手设备','113'),'10001008':('其他废料','115'),'10001009':('服务','116'),'10001010':('塑料原料','117')}
        if code:
            return list[code]
        else:
            return list
    #----抽奖专题
    #获得公司名
    def getcompany_name(self,company_id):
        sql='select name from company where id=%s'
        result=self.dbc.fetchonedb(sql,[company_id])
        if result:
            return result[0]
    #根据所输入的account获得公司id
    def getcompany_id(self,company_account):
        sql='select company_id from company_account where account=%s'
        result=self.dbc.fetchonedb(sql,[company_account])
        if result:
            return result[0]
        else:
            return -1
    #根据company_id获得公司帐号
    def getcompany_account(self,company_id):
        sql='select account from company_account where company_id=%s'
        result=self.dbc.fetchonedb(sql,[company_id])
        if result:
            return result[0]
    #抽奖列表    
    def getchoujianglist(self,frompageCount,limitNum,btype="",jiangpin="",company_id="",gmt_begin="",gmt_end=""):
        sqlarg=''
        argument=[]
        if btype:
            sqlarg+=" and btype="+str(btype)+""
        if jiangpin:
            if (jiangpin=="-1"):
                sqlarg+=" and jiangpin=-1"
            elif (jiangpin=="0"):
                sqlarg+=" and jiangpin=0"
            elif (jiangpin=="1"):
                sqlarg+=" and jiangpin=1"
            elif (jiangpin=="2"):
                sqlarg+=" and jiangpin=2"
            elif (jiangpin=="3"):
                sqlarg+=" and jiangpin=3"
            elif (jiangpin=="4"):
                sqlarg+=" and jiangpin=4"
            elif (jiangpin=="5"):
                sqlarg+=" and jiangpin=5"
            elif (jiangpin=="6"):
                sqlarg+=" and jiangpin=6"
            elif (jiangpin=="7"):
                sqlarg+=" and jiangpin=7"
            elif (jiangpin=="9"):
                sqlarg+=" and jiangpin=9"
        if company_id:
            sqlarg+=" and company_id=%s"
            argument.append(company_id)
        if gmt_begin:
            sqlarg+=" and begin_time>=%s"
            argument.append(gmt_begin)
        if gmt_end:
            sqlarg+=" and end_time<=%s"
            argument.append(gmt_end)
        sql1="select count(0) from subject_choujiang where id>0"+sqlarg
        sql="select id,btype,gmt_created,bnum,company_id,jiangpin from subject_choujiang where id>0"+sqlarg
        sql=sql+' order by id desc limit '+str(frompageCount)+','+str(limitNum)
        count=self.dbc.fetchnumberdb(sql1,argument)
        resultlist=self.dbc.fetchalldb(sql,argument)
        listall=[]
        if resultlist:
            for result in resultlist:
                id=result[0]
                btype=result[1]
                #bangdingtxt=BANGDING[str(btype)]
                bangdingtxt=self.getcategorylabel(btype)
                gmt_created=formattime(result[2],0)
                bnum=result[3]
                company_id=result[4]
                company_name=self.getcompany_name(company_id)
                jiangpin=result[5]
                jiangpintxt=self.getcategorylabel(jiangpin)
                """
                if str(btype)=="4":
                    jiangpintxt=JIANGPIN_zajindan[str(jiangpin)]
                elif str(btype)=="5":
                    jiangpintxt=JIANGPIN_guaguale[str(jiangpin)]
                elif str(btype)=="6":
                    jiangpintxt=JIANGPIN_guoqin[str(jiangpin)]
                elif str(btype)=="7":
                    jiangpintxt=JIANGPIN_taizhou[str(jiangpin)]
                else:
                    jiangpintxt=JIANGPIN.get(str(jiangpin))
                """
                list={"id":id,"bangdingtxt":bangdingtxt,"gmt_created":gmt_created,"bnum":bnum,"company_id":company_id,"company_name":company_name,"jiangpintxt":jiangpintxt}
                listall.append(list)
        return {'list':listall,'count':count}

    #weixinlist
    def weixinlist(self,frompageCount,limitNum,account="",gmt_created="",livetime=""):
        sqls=''
        argument=[]
        if account:
            sqls+='and a.account=%s'
            argument.append(account)
        if gmt_created:
            sqls+='and d.gmt_created like %s'
            argument.append(gmt_created+'%')
        if livetime:
            sqls+='and e.livetime=%s'
            argument.append(livetime+'%')
        sql='select a.weixin,a.account,b.name,c.label,b.business,d.gmt_created,d.closeflag,e.livetime,f.label as price_label,g.keywordslist as trade_label from company_account as a left join company as b on a.company_id=b.old_id left join category as c on c.code=b.industry_code left join oauth_access as d on d.company_id=a.company_id left join weixin_live as e on e.weixinid=d.open_id left join app_order_price as f on f.company_id=a.company_id left join app_order_trade as g on g.company_id=a.company_id where a.id>0 '+sqls+' limit '+str(frompageCount)+','+str(limitNum)+''
        result=self.dbc.fetchalldb(sql,argument)
        #sqlc='select count(0) as count from company_account as a left join company as b on a.company_id=b.old_id left join category as c on c.code=b.industry_code left join oauth_access as d on d.company_id=a.company_id left join weixin_live as e on e.weixinid=d.open_id left join app_order_price as f on f.company_id=a.company_id left join app_order_trade as g on g.company_id=a.company_id where a.id>0 '+sqls+''
        sqlc='select count(0) as count from company_account as a left join oauth_access as d on d.company_id=a.company_id left join weixin_live as e on e.weixinid=d.open_id where a.id>0 '+sqls+''
        count=self.dbc.fetchonedb(sqlc,argument)
        if count is None:
            count=0
        else:
            count=count[0]
        listall=[]
        if result:
            for list in result:
                weixin=list[0]
                if weixin is None:
                    weixin=''
                account=list[1]
                if account is None:
                    account=''
                name=list[2]
                if name is None:
                    name=''
                industry=list[3]
                if industry is None:
                    industry=''
                business=list[4]
                if business is None:
                    business=''
                gmt_created=list[5]
                if gmt_created is None:
                    gmt_created=''
                closeflag=list[6]
                if closeflag is None:
                    closeflag=''
                livetime=list[7]
                if livetime is None:
                    livetime=''
                price_label=list[8]
                if price_label is None:
                    price_label=''
                trade_label=list[9]
                if trade_label is None:
                    trade_label=''
                list={'weixin':weixin,'account':account,'name':name,'industry':industry,'business':business,'gmt_created':gmt_created,'closeflag':closeflag,'livetime':livetime,'price_label':price_label,'trade_label':trade_label}
                listall.append(list)
        return {'list':listall,'count':count}
