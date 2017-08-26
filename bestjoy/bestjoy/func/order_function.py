#-*- coding:utf-8 -*-
class orderfun:
    def __init__(self):
        self.db=db
    def orderlist(self,frompageCount="",limitNum="",searchlist="",status=''):
        sqlc="select count(a.id) as count from orderlist as a left outer join agentlist as b on a.agentlist_id=b.id where a.id>0 "
        sql=''
        argument=[]
        orderno=searchlist.get("orderno")
        if orderno:
            sql+=" and a.orderno=%s "
            argument.append(orderno)
            
        proname=searchlist.get("proname")
        if proname:
            sql+=" and a.proname like %s "
            argument.append('%'+proname+'%')
        protype=searchlist.get("protype")
        if protype:
            sql+=" and a.protype like %s "
            argument.append('%'+protype+'%')
        prosize1=searchlist.get("prosize1")
        if prosize1:
            sql+=" and a.prosize >= %s"
            argument.append(prosize1)
        prosize2=searchlist.get("prosize2")
        if prosize2:
            sql+=" and a.prosize <= %s"
            argument.append(prosize2)
            
        proprice1=searchlist.get("proprice1")
        if proprice1:
            sql+=" and a.proprice >= %s"
            argument.append(proprice1)
        proprice2=searchlist.get("proprice2")
        if proprice2:
            sql+=" and a.proprice <= %s"
            argument.append(proprice2)
            
        pronumber1=searchlist.get("pronumber1")
        if pronumber1:
            sql+=" and a.pronumber >= %s"
            argument.append(pronumber1)
        pronumber2=searchlist.get("pronumber2")
        if pronumber2:
            sql+=" and a.pronumber <= %s"
            argument.append(pronumber2)
            
        prodesc=searchlist.get("prodesc")
        if prodesc:
            sql+=" and a.prodesc like %s "
            argument.append('%'+prodesc+'%')
        area=searchlist.get("area")
        if area:
            sql+=" and a.area = %s "
            argument.append(area)
            
        address=searchlist.get("address")
        if address:
            sql+=" and a.address like %s "
            argument.append('%'+address+'%')
            
        postcode=searchlist.get("postcode")
        if postcode:
            sql+=" and a.postcode like %s "
            argument.append('%'+postcode+'%')
            
        contactname=searchlist.get("contactname")
        if postcode:
            sql+=" and a.contactname like %s "
            argument.append('%'+contactname+'%')
        mobile=searchlist.get("mobile")
        if mobile:
            sql+=" and a.mobile like %s "
            argument.append('%'+mobile+'%')
        phone=searchlist.get("phone")
        if phone:
            sql+=" and a.phone like %s "
            argument.append('%'+phone+'%')
        agentlist_id=searchlist.get("agentlist_id")
        if agentlist_id:
            sql+=" and a.agentlist_id=%s "
            argument.append(agentlist_id)
        if status:
            sql+=" and a.status=%s "
            argument.append(status)
        sqlc=sqlc+sql
        listcount=self.db.fetchonedb(sqlc,argument)['count']
        
        sqld="select a.id,a.orderno,a.proname,a.protype,a.prosize,a.proprice,a.pronumber,a.prodesc,a.area,a.address,a.postcode,a.contactname,a.phone,a.mobile,a.status,a.agentlist_id,a.gmt_created,a.gmt_modified,a.iscomplete,a.yuyue_time from orderlist as a left outer join agentlist as b on a.agentlist_id=b.id  where a.id>0 "
        sqld=sqld+sql
        sqld+='limit '+str(frompageCount)+','+str(limitNum)
        resultd=self.db.fetchalldb(sqld,argument)
        for dic in resultd:
            dic['gmt_created']=formattime(dic['gmt_created'])
            dic['yuyue_time']=formattime(dic['yuyue_time'],1)
            
            status=dic['status']
            if status==0:
                statustext="<font color=#ff0000>未分配</font>"
            if status==1:
                statustext="已分配"
            if status==2:
                statustext="<font color=#666>分配失败</font>"
            if status==3:
                statustext="<font color=#666>已取消</font>"
            dic['statustext']=statustext
            area=dic['area']
            proprice=dic['proprice']
            pronumber=dic['pronumber']
            allprice=0
            if proprice and pronumber:
                allprice=pronumber*proprice
            dic['allprice']=allprice
            if area:
                if len(area)>=12:
                    arealabel2=self.getarea(area_code=area[0:12])
                if len(area)>=16:
                    arealabel3=self.getarea(area_code=area[0:16])
                if len(area)>=20:
                    arealabel4=self.getarea(area_code=area[0:20])
                dic['arealabel']=arealabel2+"-"+arealabel3+"-"+arealabel4
        return {'list':resultd,'count':listcount}
    def agentlist(self,frompageCount="",limitNum="",searchlist=""):
        sqlc="select count(a.id) as count from agentlist as a where a.id>0 "
        sql=''
        argument=[]
        aname=searchlist.get("aname")
        if aname:
            sql+=" and a.aname like %s "
            argument.append('%'+aname+'%')
        dtype=searchlist.get("dtype")
        if dtype:
            sql+=" and a.dtype= %s "
            argument.append(dtype)
        area=searchlist.get("area")
        assignarea=searchlist.get("assignarea")
        if assignarea:
            sql+=" and a.area like %s "
            argument.append(assignarea+"%")
        else:
            if area:
                sql+=" and a.area= %s "
                argument.append(area)
        
        address=searchlist.get("address")
        if address:
            sql+=" and a.address like %s"
            argument.append("%"+address+"%")
            
        postcode=searchlist.get("postcode")
        if postcode:
            sql+=" and a.postcode = %s"
            argument.append(postcode)
            
        contactname=searchlist.get("contactname")
        if contactname:
            sql+=" and a.contactname like %s"
            argument.append("%"+contactname+"%")
            
        phone=searchlist.get("phone")
        if phone:
            sql+=" and a.phone like %s"
            argument.append("%"+phone+"%")
            
        sqlc=sqlc+sql
        listcount=self.db.fetchonedb(sqlc,argument)['count']
        
        sqld="select a.id,a.aname,a.dtype,a.area,a.address,a.postcode,a.contactname,a.phone,a.gmt_created,a.gmt_modified from agentlist as a  where a.isdel=0 "
        sqld=sqld+sql
        sqld+='limit '+str(frompageCount)+','+str(limitNum)
        resultd=self.db.fetchalldb(sqld,argument)
        for dic in resultd:
            dic['gmt_created']=formattime(dic['gmt_created'])
            area=dic['area']
            isbind=self.getbindweixincount(dic['id'])
            dic['weixinbind']=isbind
            if area:
                arealabel4=''
                arealabel3=''
                if len(area)>=12:
                    arealabel2=self.getarea(area_code=area[0:12])
                if len(area)>=16:
                    arealabel3=self.getarea(area_code=area[0:16])
                if len(area)>=20:
                    arealabel4=self.getarea(area_code=area[0:20])
                dic['arealabel']=arealabel2+"-"+arealabel3+"-"+arealabel4
        return {'list':resultd,'count':listcount}
    #订单详情
    def orderdetail(self,order_id):
        sql="select * from orderlist where id=%s"
        result=db.fetchonedb(sql,[order_id])
        area=result['area']
        arealabel2=''
        arealabel3=''
        arealabel4=''
        if len(area)>=12:
            arealabel2=orddb.getarea(area_code=area[0:12])
        if len(area)>=16:
            arealabel3=orddb.getarea(area_code=area[0:16])
        if len(area)>=20:
            arealabel4=orddb.getarea(area_code=area[0:20])
        result['arealabel']=arealabel2+"-"+arealabel3+"-"+arealabel4
        phone=result['phone']
        result['gmt_created']=formattime(result['gmt_created'])
        arrphone=phone.split("-")
        if len(arrphone)>=2:
            phone1=arrphone[0]
            phone2=arrphone[1]
            phone3=arrphone[2]
            result['phone1']=phone1
            result['phone2']=phone2
            result['phone3']=phone3
        return result
    #获取微信绑定
    def getbindweixincount(self,agent_id):
        sql="select count(id) as count from agent_contact where agent_id=%s and checked=1"
        result=db.fetchonedb(sql,[agent_id])
        if result:
            return result['count']
        else:
            return None
    #获得省份
    def getarea(self,area_code=""):
        sql0='select label from category where code=%s'
        result0=db.fetchonedb(sql0,[area_code])
        if result0:
            return result0['label']
    def getarealist(self,label=''):
        sql="select id,code,province,city,area,arealist from v_area where arealist like %s"
        result=db.fetchalldb(sql,['%'+str(label)+'%'])
        return result
            
            