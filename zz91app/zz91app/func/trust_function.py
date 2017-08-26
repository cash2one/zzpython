#-*- coding:utf-8 -*-
import datetime,time
detail=''
buy_no=0
class zztrust:
    #----初始化ast数据库
    def __init__(self):
        self.dbc=dbc
    def Caltime(self,date1,date2):
        date1=time.strptime(date1,"%Y-%m-%d %H:%M:%S")
        date2=time.strptime(date2,"%Y-%m-%d %H:%M:%S")
        date1=datetime.datetime(date1[0],date1[1],date1[2],date1[3],date1[4],date1[5])
        date2=datetime.datetime(date2[0],date2[1],date2[2],date2[3],date2[4],date2[5])
        cha=date2-date1
        d=cha.days
        s=cha.seconds
        if d==0:
            differ_time=s/60
            if differ_time>=60:
                differ_time=differ_time/60
                return str(differ_time)+'小时'
            else:
                return str(differ_time)+'分钟'
        else:
            differ_time=d
            return  str(differ_time)+'天'
    def getcaigou(self,frompageCount,limitNum):
        sql1='select count(0) from trust_buy where id>0 and status!="00" and status!="99"'
        sql='select id,company_id,status,title,useful,quantity,price,area_code,buy_no,color,level,gmt_refresh from trust_buy where id>0 and status!="00" and status!="99"'
        sql=sql+' order by gmt_refresh desc limit '+str(frompageCount)+','+str(limitNum)
        count=self.dbc.fetchnumberdb(sql1)
        resultlist=self.dbc.fetchalldb(sql)
        listall=[]
        now_time=formattime(datetime.datetime.now(),0)
        statustxt=''
        for result in resultlist:
            sid=result[0]
            company_id=result[1]
            status=result[2]
            bjdisable=1
            if status=='00':
                statustxt='未审核'
            if status=='01':
                statustxt='正在报价'
            if status=='02':
                statustxt='已有报价'
            if status=='03':
                statustxt='正在洽谈'
            if status=='04':
                statustxt='等待打款'
            if status=='05':
                statustxt='交易完成'
                bjdisable=0
            if status=='06':
                statustxt='交易终止'
            if status=='99':
                statustxt='审核通过'
            title=result[3]
            useful=result[4]
            quantity=result[5]
            price=result[6]
            area_code=result[7]
            area=getnavareavalue(area_code)
            if area:
                area=area[0]
            buy_no=result[8]
            color=result[9]
            level=result[10]
            gmt_refresh=formattime(result[11],0)
            differ_time=self.Caltime(gmt_refresh,now_time)
            dealerid=self.getdealerid(buy_no)
            dealertel=self.getdealertel(dealerid)
            dealername=self.getdealername(dealerid)
            """
            gmt_refresh=result[11]
            s=(now_time-gmt_refresh).seconds
            differ_time=s/60
            """
            list={'id':sid,'company_id':sid,'forcompany_id':company_id,'status':statustxt,'title':title,'useful':useful,'quantity':quantity,'price':price,'area_code':area_code,'area':area,'buy_no':buy_no,'color':color,'level':level,'differ_time':differ_time,'dealertel':dealertel,'dealername':dealername,'bjdisable':bjdisable}
            listall.append(list)
        return {'list':listall,'count':count}
    #采购列表
    def getcaigoulist(self,keywords="",frompageCount=0,limitNum=10):
        port = spconfig['port']
        cl = SphinxClient()
        cl.SetServer ( spconfig['serverid'], port )
        cl.SetMatchMode ( SPH_MATCH_BOOLEAN )
        #cl.SetFilter('is_del',[0])
        #cl.SetFilter('is_pause',[0])
        cl.SetSortMode( SPH_SORT_EXTENDED,"id desc" )
        cl.SetLimits (frompageCount,limitNum,20000)
        
        if (keywords):
            res = cl.Query ('@(title,color,price,level,useful) '+keywords+'@status (01|02|03|04|05|06|07|08) -(00|99)','trust_buy')
        else:
            res = cl.Query (''+ '@status (01|02|03|04|05|06|07|08) -(00|99)','trust_buy')
        listall=[]
        listcount=0
        if res:
            if res.has_key('matches'):
                listcount=res['total_found']
                tagslist=res['matches']
                for match in tagslist:
                    id=match['id']
                    list=self.gettrust_buy_detail(id)
                    listall.append(list)
        return {'list':listall,'count':listcount}
    #//采购详情
    def gettrust_buy_detail(self,id):
        sql="select id,company_id,status,title,useful,quantity,price,area_code,buy_no,color,level,gmt_refresh from trust_buy where id=%s"
        result=self.dbc.fetchonedb(sql,[id])
        list=None
        now_time=formattime(datetime.datetime.now(),0)
        if result:
            sid=result[0]
            company_id=result[1]
            status=result[2]
            bjdisable=1
            if status=='00':
                statustxt='未审核'
            if status=='01':
                statustxt='正在报价'
            if status=='02':
                statustxt='已有报价'
            if status=='03':
                statustxt='正在洽谈'
            if status=='04':
                statustxt='等待打款'
            if status=='05':
                statustxt='交易完成'
                bjdisable=0
            if status=='06':
                statustxt='交易终止'
            if status=='99':
                statustxt='审核通过'
            title=result[3]
            useful=result[4]
            quantity=result[5]
            price=result[6]
            area_code=result[7]
            area=getnavareavalue(area_code)
            if area:
                area=area[0]
            buy_no=result[8]
            color=result[9]
            level=result[10]
            gmt_refresh=formattime(result[11],0)
            differ_time=self.Caltime(gmt_refresh,now_time)
            dealerid=self.getdealerid(buy_no)
            dealertel=self.getdealertel(dealerid)
            dealername=self.getdealername(dealerid)
            """
            gmt_refresh=result[11]
            s=(now_time-gmt_refresh).seconds
            differ_time=s/60
            """
            list={'id':sid,'company_id':sid,'forcompany_id':company_id,'status':statustxt,'title':title,'useful':useful,'quantity':quantity,'price':price,'area_code':area_code,'area':area,'buy_no':buy_no,'color':color,'level':level,'differ_time':differ_time,'dealertel':dealertel,'dealername':dealername,'bjdisable':bjdisable}
        return list
    #获取最大的id号
    def getmaxid(self,table='',company_id=""):
        sqlidmax='select max(id) from '+table+''
        result=self.dbc.fetchonedb(sqlidmax)
        if result:
            maxid= result[0]
        return result[0]
    #根据buy_no获得交易员id
    def getdealerid(self,buy_no):
        sql='select dealer_id from trust_relate_dealer where buy_no=%s'
        result=self.dbc.fetchonedb(sql,[buy_no])
        if result:
            return result[0]
    #根据交易员id获得交易员电话
    def getdealertel(self,dealer_id):
        sql='select tel from trust_dealer where id=%s'
        result=self.dbc.fetchonedb(sql,[dealer_id])
        if result:
            return result[0]
    #根据交易员id获得交易员姓名
    def getdealername(self,dealer_id):
        sql='select name from trust_dealer where id=%s'
        result=self.dbc.fetchonedb(sql,[dealer_id])
        if result:
            return result[0]
        
    #根据sell_id获得buy_id
    def getbuyid(self,sell_id):
        sql='select buy_id from trust_relate_sell where sell_id=%s'
        result=self.dbc.fetchonedb(sql,[sell_id])
        if result:
            return result[0]
    #根据buy_id获得detail，与流水号buy_no
    def getdetail(self,buy_id):
        sql='select detail,buy_no from trust_buy where id=%s'
        result=self.dbc.fetchonedb(sql,[buy_id])
        if result:
            global detail,buy_no
            detail=result[0]
            buy_no=result[1]
        return {'detail':detail,'buy_no':buy_no}

    #获取我的采购
    def getmycaigou(self,frompageCount,limitNum,ptype=None,company_id=''):
        sqlarg=''
        if ptype:
            if (ptype=="00"):
                sqlarg+=" and status=00"
            elif (ptype=="01"):
                sqlarg+=" and status=01"
            elif (ptype=="02"):
                sqlarg+=" and status=02"
            elif (ptype=="03"):
                sqlarg+=" and status=03" 
            elif (ptype=="04"):
                sqlarg+=" and status=04" 
            elif (ptype=="05"):
                sqlarg+=" and status=05" 
            elif (ptype=="06"):
                sqlarg+=" and status=06" 
            elif (ptype=="99"):
                sqlarg+=" and status=99" 
        sql1='select count(0) from trust_buy where company_id=%s '+sqlarg
        sql='select  buy_no,status,detail,gmt_refresh from trust_buy where company_id=%s '+sqlarg
        sql=sql+' order by gmt_refresh desc limit '+str(frompageCount)+','+str(limitNum)
        count=self.dbc.fetchnumberdb(sql1,[company_id])
        resultlist=self.dbc.fetchalldb(sql,[company_id])
        listall=[]
        statustxt=''
        for result in resultlist:
            buy_no=result[0]
            status=result[1]
            detail=result[2]
            gmt_refresh=formattime(result[3],1)
            if status=='00':
                statustxt='未审核'
            if status=='01':
                statustxt='正在报价'
            if status=='02':
                statustxt='已有报价'
            if status=='03':
                statustxt='正在洽谈'
            if status=='04':
                statustxt='等待打款'
            if status=='05':
                statustxt='交易完成'
            if status=='06':
                statustxt='交易终止'
            if status=='99':
                statustxt='审核通过'
            dealerid=self.getdealerid(buy_no)
            dealername=self.getdealername(dealerid)
            list={'buy_no':buy_no,'status':statustxt,'detail':detail,'gmt_refresh':gmt_refresh,'dealername':dealername}
            listall.append(list)
        return {'list':listall,'count':count}
    #获取我的供货
    def getmysupply(self,frompageCount,limitNum,ptype=None,company_id=''):
        sqlarg=''
        if ptype:
            if (ptype=="00"):
                sqlarg+=" and status=00"
            elif (ptype=="01"):
                sqlarg+=" and status=01"
            elif (ptype=="99"):
                sqlarg+=" and status=99" 
        sql1='select count(0) from trust_sell where company_id=%s'+sqlarg
        sql='select id,status,content,gmt_modified from trust_sell where company_id=%s'+sqlarg
        sql=sql+' order by gmt_modified desc limit '+str(frompageCount)+','+str(limitNum)
        count=self.dbc.fetchnumberdb(sql1,[company_id])
        resultlist=self.dbc.fetchalldb(sql,[company_id])
        listall=[]
        statustxt=''
        for result in resultlist:
            sell_id=result[0]
            status=result[1]
            #供货内容
            content=result[2]
            gmt_modified=formattime(result[3],1)
            if status=='00':
                statustxt='已报价'
            if status=='01':
                statustxt='报价被采纳'
            if status=='99':
                statustxt='报价被否决'
            #获得采购内容 
            buy_id=self.getbuyid(sell_id) 
            out=self.getdetail(buy_id)
            detail=out['detail']  
            #获得流水号
            buy_no=out['buy_no']  
            #获得交易员名字
            dealerid=self.getdealerid(buy_no)
            dealername=self.getdealername(dealerid)
            list={'content':content,'detail':detail,'buy_no':buy_no,'status':statustxt,'dealername':dealername,'gmt_modified':gmt_modified}
            listall.append(list)
        return {'list':listall,'count':count}