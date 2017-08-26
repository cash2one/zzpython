#-*- coding:utf-8 -*-
class zzhr:
    def __init__(self):
        self.db=db
#所有数据
    def gethrlist(self,frompageCount="",limitNum="",searchlist=""):
        argument=[]
        sqls=""
        sqls1=""
        searchurl=""
        star=searchlist.get("star")
        username=searchlist.get("username")
        mobile=searchlist.get("mobile")
        email=searchlist.get("email")
        sex=searchlist.get("sex")
        contactstat=searchlist.get("contactstat")
        jl1=searchlist.get("jl1")
        jl2=searchlist.get("jl2")
        jl3=searchlist.get("jl3")
        jl4=searchlist.get("jl4")
        jl5=searchlist.get("jl5")
        personid=searchlist.get("personid")
        rpersonid=searchlist.get("rpersonid")
        interviewTime1=searchlist.get("interviewTime1")
        interviewTime2=searchlist.get("interviewTime2")
        gmt_created1=searchlist.get("gmt_created1")
        gmt_created2=searchlist.get("gmt_created2")
        orderstr=searchlist.get("orderstr")
        dotype=searchlist.get("dotype")
        user_id=searchlist.get("user_id")
        time_today=datetime.date.today()
        if star:
            sqls+=" and a.star=%s"
            argument.append(star)
        if username:
            sqls+=" and a.username like %s"
            argument.append('%'+username+'%')
        if mobile:
            sqls+=" and a.mobile like %s"
            argument.append('%'+mobile+'%')
        if email:
            sqls+="and a.email like %s"
            argument.append('%'+email+'%')
        if sex:
            sqls+=" and a.sex=%s"
            argument.append(sex)
        if contactstat:
            sqls+=" and a.contactstat=%s"
            argument.append(contactstat)
        if jl1:
            sqls+=" and a.jl1=%s"
            argument.append(jl1)
        if jl2:
            sqls+=" and a.jl2=%s"
            argument.append(jl2)
        if jl3:
            sqls+=" and a.jl3=%s"
            argument.append(jl3)
        if jl4:
            sqls+=" and a.jl4=%s"
            argument.append(jl4)
        if jl5:
            sqls+=" and a.jl5=%s"
            argument.append(jl5)
        if interviewTime1 and interviewTime2:
            sqls+=" and a.interviewTime between %s and %s"
            argument.append(interviewTime1)
            argument.append(interviewTime2)
        if gmt_created1 and gmt_created2:
            sqls+=" and a.gmt_created between %s and %s"
            argument.append(gmt_created1)
            argument.append(gmt_created2)
        if personid:
            sqls+=" and b.personid=%s"
            argument.append(personid)
        if rpersonid:
            sqls+=" and a.personid=%s"
            argument.append(rpersonid)
        
        if dotype == "today":
            sqls1+=" left outer join (select uid,max(nextteltime) as nextteltime from renshi_history group by uid) as d on a.id=d.uid"
            sqls+=" and d.nextteltime=%s"
            argument.append(time_today)
        elif dotype == "contact":
            sqls1+=" left outer join (select uid,max(nextteltime) as nextteltime from renshi_history group by uid) as d on a.id=d.uid"
            sqls+=" and d.nextteltime<%s"
            argument.append(time_today)
        elif dotype == "my":
            sqls+=" and a.personid=%s"
            argument.append(user_id)
        elif dotype == "luyong":
            sqls+=" and a.jl3=1902"
        elif dotype == "gonghai":
            sqls="and a.id not in (select uid from renshi_assign)"
        elif dotype == "all":
            pass
        
        sqlcount="select count(0) as count from renshi_user as a "+sqls1+" where a.id>0 "+sqls+""
        count=db.fetchonedb(sqlcount,argument)['count']
        if orderstr == "1":
            sqls+=" order by a.interviewTime desc"
        elif orderstr == "2":
            sqls+=" order by a.gmt_created desc"
        else:
            sqls+=" order by a.id desc"
        
        sqllist="select a.personid,a.id,a.star,a.mobile,a.username,a.sex,a.education,a.interviewTime,a.station,a.jl1,a.jl2,a.jl3,a.jl4,a.jl5,a.laiyuan,a.othercontact,a.email,a.gmt_created,a.station,a.station2,c.realname,a.contactstat from renshi_user as a left outer join renshi_assign as b on a.id=b.uid left outer join user as c on c.id=b.personid "+sqls1+" where a.id>0 "+sqls+" limit "+str(frompageCount)+","+str(limitNum)+""
        listall=db.fetchalldb(sqllist,argument)
        for list in listall:
            time=list['interviewTime']
            list['interviewTime']=formattime(time,flag=2)
            time=list['gmt_created']
            list['gmt_created']=formattime(time,flag=2)
            list['last_realname']=self.getlastcontact(list['id'])
            list['education_name']=self.getcategorylabel(list['education'])
            list['jl1_name']=self.getcategorylabel(list['jl1'])
            list['jl2_name']=self.getcategorylabel(list['jl2'])
            list['jl3_name']=self.getcategorylabel(list['jl3'])
            list['jl4_name']=self.getcategorylabel(list['jl4'])
            list['jl5_name']=self.getcategorylabel(list['jl5'])
            list['contactstat_name']=self.getcategorylabel(list['contactstat'])
            realname=list['realname']
            if not realname:
                list['realname']=''
        return {'count':count,'list':listall}
    #最后跟进人员
    def getlastcontact(self,uid):
        sql="select b.realname from renshi_history as a left join user as b on a.personid=b.id where a.uid=%s order by a.fdate desc"
        result=db.fetchonedb(sql,[uid])
        if result:
            return result['realname']
    #人事基础数据
    def gethrbasiclist(self,searchlist=""):
        argument=[]
        sqls=""
        label=searchlist.get("label")
        if label:
            sqls+="and label=%s"
            argument.append(label)
            sql='select id,code,label from renshi_category where label=%s'
            basiclist=db.fetchalldb(sql,argument)
        else:
            sqllist="select id,code,label from renshi_category where id>0 and code like '__' order by code"
            listall=db.fetchalldb(sqllist,argument)
            basiclist=[]
            for list in listall:
                sqla="select id,code,label from renshi_category where code like '"+list['code']+"__'"
                resulta=db.fetchalldb(sqla)
                childrenall=[]
                for list1 in resulta:
                    sqlb="select id,code,label from renshi_category where code like '"+list1['code']+"__'"
                    resultb=db.fetchalldb(sqlb)
                    childrenall1=[]
                    for list2 in resultb:
                        lll={'label':list2['label'],'id':list2['id'],'code':list2['code']}
                        childrenall1.append(lll)
                    ll={'label':list1['label'],'code':list1['code'],'id':list1['id'],'children':childrenall1}
                    childrenall.append(ll)
                l={'label':list['label'],'id':list['id'],'code':list['code'],'children':childrenall}
                basiclist.append(l)
        return basiclist
    def getcategorylist(self,code=''):
        sql="select id,code,label from renshi_category where code like %s order by ord asc"
        listall=db.fetchalldb(sql,[code+"__"])
        for list in listall:
            sql="select id,code,label from renshi_category where code like %s order by ord asc"
            childlist=db.fetchalldb(sql,[list['code']+"__"])
            list['childlist']=childlist
        return listall
    def getcategorylabel(self,code):
        if code:
            sql="select label from renshi_category where code=%s"
            result=db.fetchonedb(sql,[code])
            label=''
            if result:
                label=result['label']
                if not label:
                    label=''
        else:
            label=''
        return label
        
#面试记录
    def getrenshihistory(self,frompageCount="",limitNum="",searchlist=""):
        argument=[]
        uid=searchlist.get("uid")
        if uid:
            argument.append(uid)
        sqlcount="select count(0) as count from renshi_history where uid=%s"
        count=db.fetchonedb(sqlcount,argument)['count']
        sqllist="select a.bz,a.nextteltime,b.label,c.realname from renshi_history as a left join renshi_category as b on a.code=b.code left join user as c on c.id=a.personid where uid=%s limit "+str(frompageCount)+","+str(limitNum)+""
        listall=db.fetchalldb(sqllist,argument)
        for list in listall:
            time=list['nextteltime']
            list['nextteltime']=formattime(time,flag=2)
        return {'count':count,'list':listall}