class zzsh:
    def __init__(self):
        self.dbc=dict_dbc
    def getzshlist(self,frompageCount='',limitNum='',searchlist=''):
        sqlarg=''
        argument=[]
        mobile=searchlist.get("mobile")
        companyname=searchlist.get("companyname")
        zheng_no=searchlist.get("zheng_no")
        contact=searchlist.get("contact")
        ispay=searchlist.get("ispay")
        isnowin=searchlist.get("isnowin")
        getzheng=searchlist.get("getzheng")
        if mobile:
            sqlarg+=' and mobile=%s'
            argument.append(mobile)
        if companyname:
            sqlarg+=' and companyname like %s'
            argument.append('%'+companyname+'%')
        if contact:
            sqlarg+=' and contact like %s'
            argument.append('%'+contact+'%')
        if zheng_no:
            sqlarg+=' and zheng_no=%s'
            argument.append(zheng_no)
        if ispay:
            sqlarg+=' and ispay=%s'
            argument.append(ispay)
        if isnowin:
            sqlarg+=' and isnowin=%s'
            argument.append(isnowin)
        if getzheng:
            sqlarg+=' and getzheng=%s'
            argument.append(getzheng)
        sql1='select count(0) from zsh_list where id>0 '+sqlarg
        sql='select id,zheng_no,area,isqiandao,companyname,mobile,contact,business,fee,ispay,company_id,weixinid,paytime,paytype,salesperson,membertype,qiandaotime,getzheng from zsh_list where id>0 '+sqlarg
        count=self.dbc.fetchnumberdb(sql1,argument)
        sql=sql+' order by qiandaotime desc limit %s,%s'
        argument.append(frompageCount)
        argument.append(limitNum)
        resultlist=self.dbc.fetchalldb(sql,argument)
        
        listall=[]
        for list in resultlist:
            if not list['zheng_no']:
                list['zheng_no']=''
            list['qiandaotime']=formattime(list['qiandaotime'],0)
            list['paytime']=formattime(list['paytime'],0)
            """
            id=list[0]
            zheng_no=list[1]
            area=list[2]
            isqiandao=list[3]
            companyname=list[4]
            mobile=list[5]
            contact=list[6]
            business=list[7]
            fee=list[8]
            ispay=list[9]
            company_id=list[10]
            weixinid=list[11]
            paytime=list[12]
            paytype=list[13]
            
            salesperson=list[14]
            membertype=list[15]
            """
            #ll={"id":id,"zheng_no":zheng_no,"area":area,"isqiandao":isqiandao,"companyname":companyname,"mobile":mobile,"contact":contact,"business":business,"fee":fee,"ispay":ispay,"company_id":company_id,"weixinid":weixinid,"paytime":paytime,"paytype":paytype,"salesperson":paytype,"membertype":membertype}
            #listall.append(ll)
        return {'list':resultlist,'count':count}