#-*- coding:utf-8 -*-
class zzwl:
    def __init__(self):
        self.db=db
#所有数据
    def getwllist(self,frompageCount="",limitNum="",searchlist=""):
        argument=[]
        sqls=""
        order_number=searchlist.get("order_number")
        company_name=searchlist.get("company_name")
        wechat=searchlist.get("wechat")
        username=searchlist.get("username")
        mobile=searchlist.get("mobile")
        car_for=searchlist.get("car_for")
        weight=searchlist.get("weight")
        personid=searchlist.get("personid")
        time1=searchlist.get("time1")
        time2=searchlist.get("time2")
        star=searchlist.get("star")
        orderstr=searchlist.get("orderstr")
        dotype=searchlist.get("dotype")
        user_id=searchlist.get("user_id")
        time_today=datetime.date.today()
        if order_number:
            sqls+=" and a.order_number like %s"
            argument.append('%'+order_number+'%')
        if company_name:
            sqls+=" and a.company_name like %s"
            argument.append('%'+company_name+'%')
        if wechat:
            sqls+=" and a.wechat like %s"
            argument.append('%'+wechat+'%')
        if username:
            sqls+="and a.username like %s"
            argument.append('%'+username+'%')
        if mobile:
            sqls+=" and a.mobile like %s"
            argument.append('%'+mobile+'%')
        if car_for:
            sqls+=" and a.car_for like %s"
            argument.append('%'+car_for+'%')
        if weight:
            sqls+=" and a.weight like %s"
            argument.append('%'+weight+'%')
        if personid:
            sqls+=" and a.personid=%s"
            argument.append(personid)
        if star:
            sqls+=" and a.star=%s"
            argument.append(star)
        if time1 and time2:
            sqls+=" and a.time between %s and %s"
            argument.append(time1)
            argument.append(time2)
        if orderstr == "1":
            sqls+=" order by nextcontact_time desc"
        elif orderstr == "2":
            sqls+=" order by register_time desc"
        elif orderstr == "3":
            sqls+=" order by lastcontact_time desc"
        if dotype == "nocontact":
            sqls+=" and ISNULL(a.nextcontact_time)"
        elif dotype == "today":
            sqls+=" and a.nextcontact_time=%s"
            argument.append(time_today)
        elif dotype == "contact":
            sqls+=" and a.nextcontact_time<%s"
            argument.append(time_today)
        elif dotype == "my":
            sqls+=" and a.personid=%s"
            argument.append(user_id)
        elif dotype == "gonghai_nocontact":
            sqls="and a.id not in (select uid from wl_assign) and ISNULL(a.nextcontact_time)"
        elif dotype == "gonghai_contact":
            sqls="and a.id not in (select uid from wl_assign) and a.nextcontact_time!=''"
        elif dotype == "gonghai":
            sqls="and a.id not in (select uid from wl_assign)"
        elif dotype == "all":
            pass
        sqlcount="select count(0) as count from wl_customer as a where a.id>0 "+sqls+""
        count=db.fetchonedb(sqlcount,argument)['count']
        sqllist="select a.id,a.star,a.order_number,a.company_name,a.wechat,a.username,a.main_business,a.mobile,a.car_for,a.weight,a.time,a.register_time,a.nextcontact_time,a.lastcontact_time,a.personid,b.realname from wl_customer as a left join user as b on a.personid=b.id where a.id>0 "+sqls+" limit "+str(frompageCount)+","+str(limitNum)+""
        listall=db.fetchalldb(sqllist,argument)
        for list in listall:
            time=list['time']
            list['time']=formattime(time,flag=2)
            register_time=list['register_time']
            list['register_time']=formattime(register_time,flag=2)
            nextcontact_time=list['nextcontact_time']
            list['nextcontact_time']=formattime(nextcontact_time,flag=2)
            lastcontact_time=list['lastcontact_time']
            list['lastcontact_time']=formattime(lastcontact_time,flag=2)
            list['last_realname']=self.getlastcontact(list['id'])
            if list['star'] is None:
                list['star']=""
            if list['last_realname'] is None:
                list['last_realname']=""
        return {'count':count,'list':listall}
    #最后跟进人员
    def getlastcontact(self,id):
        sql="select b.realname from wl_history as a left join user as b on a.personid=b.id where a.uid=%s order by a.fdate desc"
        result=db.fetchonedb(sql,[id])
        if result:
            return result['realname']
    #过程记录
    def getcustomerhistory(self,frompageCount="",limitNum="",searchlist=""):
        argument=[]
        uid=searchlist.get("uid")
        if uid:
            argument.append(uid)
        sqlcount="select count(0) as count from wl_history where uid=%s"
        count=db.fetchonedb(sqlcount,argument)['count']
        sqllist="SELECT a.contactstate,a.star,a.nextcontact_time,a.contact_bz,a.fdate,a.personid,b.realname from wl_history as a LEFT JOIN user as b on a.personid=b.id where uid=%s limit "+str(frompageCount)+","+str(limitNum)+""
        listall=db.fetchalldb(sqllist,argument)
        for list in listall:
            time=list['nextcontact_time']
            list['nextcontact_time']=formattime(time,flag=2)
            time=list['fdate']
            list['fdate']=formattime(time,flag=2)
            if list['contactstate']==1:
                list['contactstate']="有效联系"
            elif list['contactstate']==0:
                 list['contactstate']="无效联系"
        return {'count':count,'list':listall}