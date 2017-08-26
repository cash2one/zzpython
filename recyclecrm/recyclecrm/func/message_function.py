# -*- coding:utf-8 -*-
import codecs
codecs.register(lambda name: codecs.lookup('utf8') if name == 'utf8mb4' else None)
class zzmessage():
    def __init__(self):
        self.db=db
        self.dbc=dbc
#获取消息主页消息数量
    def getnumber(self,request=""):
        my_user_id=request.session.get('user_id')
        time_today=datetime.date.today()
        time_today='%'+str(time_today)+'%'
        sql1="select count(0) as count from user_remark where my_user_id=%s and next_contact_time like %s"
        num1=db.fetchonedb(sql1,[my_user_id,time_today])
        time_today=datetime.date.today()
        sql2='select count(0) as count from company_customer as a left join user as b on a.company_id=b.company_id left join user_remark as c on c.user_id=b.id where a.id>0 and a.my_user_id=%s and c.next_contact_time<%s'
        num2=db.fetchonedb(sql2,[my_user_id,time_today])
        sql3='select count(0) as count from user_remark_log where my_user_id=%s group by user_id'
        num3=db.fetchonedb(sql3,[my_user_id])
        return {'num1':num1,'num2':num2,'num3':num3}
#客户留言
    def leavemessage(self,request=""):
        my_user_id=request.session.get('user_id')
        sql='select a.user_id,a.content,a.recently_contact_time,b.contact,b.sex from user_remark_log as a left join user as b on a.user_id=b.id where my_user_id=%s group by user_id'
        result=db.fetchalldb(sql,[my_user_id])
        for list in result:
            time=list.get('recently_contact_time')
            if time:
                list['recently_contact_time']=formattime(time,flag=2)
            elif not time:
                list['recently_contact_time']=''
            name=list.get('contact')
            if not name:
                list['contact']=''
            content=list.get('content')
            if not content:
                list['content']=''
        return result
#留言列表
    def leave_list(self,request=""):
        my_user_id=request.session.get('user_id')
        user_id=request.GET.get('user_id')
        sql='select a.user_id,a.content,a.recently_contact_time,b.contact,b.sex from user_remark_log as a left join user as b on a.user_id=b.id where my_user_id=%s and user_id=%s'
        result=db.fetchalldb(sql,[my_user_id, user_id])
        for list in result:
            time=list.get('recently_contact_time')
            if not time:
                list['recently_contact_time']=''
            else:
                list['recently_contact_time']=formattime(time,flag=2)
        return {'result':result,'user_id':user_id}
#回复客户信息
    def reply(self,request=""):
        my_user_id=request.session.get('user_id')
        user_id=request.GET.get('user_id')
        content=request.GET.get('content')
        recently_contact_time=datetime.datetime.now()
        gmt_created=datetime.datetime.now()
        sql='insert into user_remark_log(my_user_id,user_id,content,recently_contact_time,gmt_created) values(%s,%s,%s,%s,%s)'
        result=db.updatetodb(sql,[my_user_id,user_id,content,recently_contact_time,gmt_created])