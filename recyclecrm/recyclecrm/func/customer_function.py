#-*- coding=utf-8 -*-
class zzcustomer():
    def __init__(self):
        self.db=db
#所有客户
    def list(self,request=""):
        sqls=""
        argument=[]
        my_user_id=request.session.get('user_id',default=None)
        star=request.GET.get('star')
        today=request.GET.get('today')
        time_today=datetime.date.today()
        losecontact=request.GET.get('losecontact')
        if my_user_id:
            sqls+=" and a.my_user_id=%s"
            argument.append(my_user_id)
        if star:
            sqls+=" and c.star=%s"
            argument.append(star)
        if today:
            if today=='0':
                time_today='%'+str(time_today)+'%'
                sqls+=" and c.next_contact_time like %s"
                argument.append(time_today)
            else:
                time_today='%'+str(time_today)+'%'
                sqls+=" and c.next_contact_time like %s and c.recently_remark_type=%s"
                argument.append(time_today)
                argument.append(today)
        if losecontact:
            sqls+=" and c.next_contact_time<%s"
            argument.append(time_today)
        sql="select a.company_id,a.name,a.area,b.contact,c.recently_contact_time,c.next_contact_time,c.star,c.recently_remark_type from company_customer as a left join user as b on a.company_id=b.company_id left join user_remark as c on c.user_id=b.id where a.id>0 "+sqls+""
        listall=db.fetchalldb(sql,argument)
        for list in listall:
            if list['star']==6:
                list['star']='待回访客户'
            elif list['star']==1:
                list['star']='无意向客户'
            elif list['star']==2:
                list['star']='潜在客户'
            elif list['star']==3:
                list['star']='有意向客户'
            elif list['star']==4:
                list['star']='确认合作客户'
            elif list['star']==5:
                list['star']='重点客户'
            if list['recently_remark_type']==1:
                list['recently_remark_type']='打电话'
            if list['recently_remark_type']==2:
                list['recently_remark_type']='发短信'
            if list['recently_remark_type']==3:
                list['recently_remark_type']='约见面'
            if list['next_contact_time']==None:
                list['next_contact_time']=''
            else:
                next_contact_time=list['next_contact_time']
                list['next_contact_time']=formattime(next_contact_time,2)
            if list['recently_contact_time']==None:
                list['recently_contact_time']=''
            else:
                recently_contact_time=list['recently_contact_time']
                list['recently_contact_time']=formattime(recently_contact_time,2)
        return {'listall':listall}
#批量处理
    def all(self,request=""):
        check_box_list = request.REQUEST.getlist("check_box_list")
        dostay=request.POST.get('dostay')
        if dostay=="throw":
            for id in check_box_list:
                sql='update user_customer set isflag=1 where id=%s'
                result=db.updatetodb(sql,[id])
        elif dostay=="assignto":
            for id in check_box_list:
                sql='insert into user_customer() values()'
                result=db.updatetodb(sql,[id])
        elif dostay=="del":
            for id in check_box_list:
                sql='delete from user_customer where id=%s'
                result=db.updatetodb(sql,[id])
#操作记录
    def remark(self,request=""):
        value=request.GET.get('dotype')
        my_user_id=request.session.get('user_id')
        user_id=request.GET.get('user_id')
        iscontact=1
        recently_contact_time=datetime.datetime.now()
        gmt_created=datetime.datetime.now()
        gmt_modified=datetime.datetime.now()
        content=request.POST.get('content')
        next_contact=request.POST.get('next_contact')
        timestamp=time.time()
        timestamp_today=timestamp-timestamp%86400
        next_contact_timestamp=0
        if next_contact=='1':
            next_contact_timestamp+=time.time()+60*60
        elif next_contact=='2':
            next_contact_timestamp+=timestamp_today+24*60*60+60*60
        elif next_contact=='3':
            next_contact_timestamp+=timestamp_today+24*60*60+7*60*60
        elif next_contact=='4':
            next_contact_timestamp+=timestamp_today+2*24*60*60+60*60
        elif next_contact=='5':
            next_contact_timestamp+=timestamp_today+2*24*60*60+7*60*60
        next_contact_time=timestamp_to_date(float(next_contact_timestamp))
        sql='select id from user_remark where my_user_id=%s and user_id=%s'
        result=db.fetchonedb(sql,[my_user_id,user_id])
        if value=='call':
            recently_remark_type='2'
            remark_type='2'
            if not result:
                sql='insert into user_remark(my_user_id,user_id,recently_remark_type,iscontact,recently_contact_time,call_count,gmt_created) values(%s,%s,%s,%s,%s,%s,%s)'
                result=db.updatetodb(sql,[my_user_id,user_id,recently_remark_type,iscontact,recently_contact_time,1,gmt_created])
            else:
                sql='update user_remark set recently_remark_type=%s,iscontact=%s,recently_contact_time=%s,call_count=call_count+1,gmt_modified=%s where my_user_id=%s and user_id=%s'
                result=db.updatetodb(sql,[recently_remark_type,iscontact,recently_contact_time,gmt_modified,my_user_id,user_id])
            sqls='insert into user_remark_log(my_user_id,user_id,remark_type,iscontact,recently_contact_time,gmt_created) values(%s,%s,%s,%s,%s,%s)'
            result=db.updatetodb(sqls,[my_user_id,user_id,remark_type,iscontact,recently_contact_time,gmt_created])
        elif value=='text':
            recently_remark_type='1'
            remark_type='1'
            if not result:
                sql='insert into user_remark(my_user_id,user_id,recently_remark_type,iscontact,recently_contact_time,message_count,gmt_created) values(%s,%s,%s,%s,%s,%s,%s)'
                result=db.updatetodb(sql,[my_user_id,user_id,recently_remark_type,iscontact,recently_contact_time,1,gmt_created])
            else:
                sql='update user_remark set recently_remark_type=%s,iscontact=%s,recently_contact_time=%s,message_count=message_count+1,gmt_modified=%s where my_user_id=%s and user_id=%s'
                result=db.updatetodb(sql,[recently_remark_type,iscontact,recently_contact_time,gmt_modified,my_user_id,user_id])
            sqls='insert into user_remark_log(my_user_id,user_id,remark_type,content,iscontact,recently_contact_time,gmt_created) values(%s,%s,%s,%s,%s,%s,%s)'
            result=db.updatetodb(sqls,[my_user_id,user_id,remark_type,content,iscontact,recently_contact_time,gmt_created])
        elif value=='date':
            recently_remark_type='3'
            remark_type='3'
            if not result:
                sql='insert into user_remark(my_user_id,user_id,recently_remark_type,iscontact,recently_contact_time,next_contact_time,visit_count,gmt_created) values(%s,%s,%s,%s,%s,%s,%s,%s)'
                result=db.updatetodb(sql,[my_user_id,user_id,recently_remark_type,iscontact,recently_contact_time,next_contact_time,1,gmt_created])
            else:
                sql='update user_remark set recently_remark_type=%s,iscontact=%s,recently_contact_time=%s,next_contact_time=%s,visit_count=visit_count+1,gmt_modified=%s where my_user_id=%s and user_id=%s'
                result=db.updatetodb(sql,[recently_remark_type,iscontact,recently_contact_time,next_contact_time,gmt_modified,my_user_id,user_id])
            sqls='insert into user_remark_log(my_user_id,user_id,remark_type,iscontact,recently_contact_time,next_contact_time,gmt_created) values(%s,%s,%s,%s,%s,%s,%s)'
            result=db.updatetodb(sqls,[my_user_id,user_id,remark_type,iscontact,recently_contact_time,next_contact_time,gmt_created])
#丢公海
    def throw(self,request=""):
        user_id=request.GET.get('user_id')
        sql='delete from user_customer where user_id=%s'
        result=db.updatetodb(sql,[user_id])
        
#+行动
    def action(self,request=""):
        my_user_id=request.session.get('user_id')
        user_id=request.POST.get('user_id')
        recently_remark_type=request.POST.get('recently_remark_type')
        remark_type=request.POST.get('recently_remark_type')
        recently_contact_time=datetime.datetime.now()
        next_contact=request.POST.get('next_contact')
        timestamp=time.time()
        timestamp_today=timestamp-timestamp%86400
        next_contact_timestamp=0
        if next_contact=='1':
            next_contact_timestamp+=time.time()+60*60
        elif next_contact=='2':
            next_contact_timestamp+=timestamp_today+24*60*60+60*60
        elif next_contact=='3':
            next_contact_timestamp+=timestamp_today+24*60*60+7*60*60
        elif next_contact=='4':
            next_contact_timestamp+=timestamp_today+2*24*60*60+60*60
        elif next_contact=='5':
            next_contact_timestamp+=timestamp_today+2*24*60*60+7*60*60
        next_contact_time=timestamp_to_date(float(next_contact_timestamp))
        gmt_created=datetime.datetime.now()
        gmt_modified=datetime.datetime.now()
        sql='select id from user_remark where my_user_id=%s and user_id=%s'
        result=db.fetchonedb(sql,[my_user_id,user_id])
        if not result:
            sql='insert into user_remark(my_user_id,user_id,recently_remark_type,recently_contact_time,next_contact_time,gmt_created) values(%s,%s,%s,%s,%s,%s)'
            result=db.updatetodb(sql,[my_user_id,user_id,recently_remark_type,recently_contact_time,next_contact_time,gmt_created])
        else:
            sql='update user_remark set recently_remark_type=%s,recently_contact_time=%s,next_contact_time=%s,gmt_modified=%s where my_user_id=%s and user_id=%s'
            result=db.updatetodb(sql,[recently_remark_type,recently_contact_time,next_contact_time,gmt_created,my_user_id,user_id])
        sqls='insert into user_remark_log(my_user_id,user_id,remark_type,recently_contact_time,next_contact_time,gmt_created) values(%s,%s,%s,%s,%s,%s)'
        result=db.updatetodb(sqls,[my_user_id,user_id,remark_type,recently_contact_time,next_contact_time,gmt_created])