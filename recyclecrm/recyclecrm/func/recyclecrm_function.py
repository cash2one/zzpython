# -*- coding: utf-8 -*-  
class zzrecyclecrm:
    def __init__(self):
        self.db=db
#主页面
    def list(self,frompageCount="",limitNum=""):
        sqlcount="select count(0) as count from company where id>0"
        count=db.fetchonedb(sqlcount)['count']
        sqllist="select id,name,area,tel,fax,address,zip,industry_code,business,isdeleted,register_time from company limit "+str(frompageCount)+","+str(limitNum)+""
        listall=db.fetchalldb(sqllist)
        for list in listall:
            time=list.get('register_time')
            list['register_time']=formattime(time,flag=2)
        return {'count':count,'list':listall}
#保存客户信息
    def save(self,request=""):
        id=request.GET.get('id')
        company_id=request.POST.get('company_id')
        name=request.POST.get('name')
        area=request.POST.get('area')
        tel=request.POST.get('tel')
        fax=request.POST.get('fax')
        address=request.POST.get('address')
        zip=request.POST.get('zip')
        industry_code=request.POST.get('industry_code')
        business=request.POST.get('business')
        isdeleted=request.POST.get('isdeleted')
        time=datetime.datetime.now()
        if not id:
            sqls='insert into company(id,name,area,tel,fax,address,zip,industry_code,business,isdeleted,register_time,gmt_created) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
            result1=db.updatetodb(sqls,[company_id,name,area,tel,fax,address,zip,industry_code,business,isdeleted,time,time])
        elif id:
            sqls='update company set name=%s,area=%s,tel=%s,fax=%s,address=%s,zip=%s,industry_code=%s,business=%s,isdeleted=%s,gmt_modified=%s where id=%s'
            result1=db.updatetodb(sqls,[name,area,tel,fax,address,zip,industry_code,business,isdeleted,time,id])
#批处理
    def all(self,request="",check_box_list=""):
        dostay=request.POST.get('dostay')
        id=request.GET.get('id')
        dotype=request.GET.get('dotype')
        if not dostay:
            if id:
                sql='delete from company where id=%s'
                result=db.updatetodb(sql,[id])
            if check_box_list:
                for id in check_box_list:
                    sql='delete from company where id=%s'
                    result=db.updatetodb(sql,[id])
        if dotype=="leavemessage":
            sql='delete from user_leave_message where id=%s'
            result=db.updatetodb(sql,[id])
#用户信息
    def user(self,request="",frompageCount="",limitNum=""):
        company_id=request.GET.get('company_id')
        sqlcount='select count(0) as count from user where company_id=%s'
        count=db.fetchonedb(sqlcount,[company_id])['count']
        sqllist="select id,name,password,company_id,contact,sex,position,tel,mobile,wechat,qq,email,area,address,register_time,wechat_id,appid,header_path from user where company_id=%s limit "+str(frompageCount)+","+str(limitNum)+""
        listall=db.fetchalldb(sqllist,[company_id])
        for list in listall:
            time=list.get('register_time')
            if time:
                list['register_time']=formattime(time,flag=2)
        return {'count':count,'list':listall,'company_id':company_id}
#活动记录
    def activity(self,request="",frompageCount="",limitNum=""):
        company_id=request.GET.get('company_id')
        sqlcount='select count(0) as count from activity_remark where customer_id=%s'
        count=db.fetchonedb(sqlcount,[company_id])['count']
        sqllist='select my_id,customer_id,activity_type,activity_time,if_useful_contact,next_contact_time,customer_level,activity_comment from activity_remark where customer_id=%s'
        listall=db.fetchalldb(sqllist,[company_id])
        for list in listall:
            time1=list.get('activity_time')
            if time1:
                list['activity_time']=formattime(time1,flag=2)
            time2=list.get('next_contact_time')
            if time2:
                list['next_contact_time']=formattime(time2,flag=2)
        return {'count':count,'list':listall,'company_id':company_id}
#用户活动情况
    def user_activity(self,request="",frompageCount="",limitNum=""):
        company_id=request.GET.get('company_id')
        sqlcount='select count(0) as count from user_activity_remark where customer_id=%s'
        count=db.fetchonedb(sqlcount,[company_id])['count']
        sqllist='select id,my_id,customer_id,if_useful_contact,recently_contact_time,star,next_contact_time,call_frequency,visit_frequency,leave_message_frequency from user_activity_remark where customer_id=%s'
        listall=db.fetchalldb(sqllist,[company_id])
        for list in listall:
            time1=list.get('recently_contact_time')
            if time1:
                list['recently_contact_time']=formattime(time1,flag=2)
            time2=list.get('next_contact_time')
            if time2:
                list['next_contact_time']=formattime(time2,flag=2)
        return {'count':count,'list':listall,'company_id':company_id}
#用户留言
    def user_message(self,request="",frompageCount="",limitNum=""):
        company_id=request.GET.get('company_id')
        sqlcount='select count(0) as count from user_leave_message where customer_id=%s'
        count=db.fetchonedb(sqlcount,[company_id])['count']
        sqllist='select id,my_id,customer_id,message_type,message,time from user_leave_message where customer_id=%s'
        listall=db.fetchalldb(sqllist,[company_id])
        for list in listall:
            time=list.get('time')
            if time:
                list['time']=formattime(time,flag=2)
        return {'count':count,'list':listall,'company_id':company_id}
#删除留言
    def del_message(self,request=""):
        id=request.GET.get('id')
        sql='delete from user_leave_message where id=%s'
        result=db.updatetodb(sql,[id])
#公司信息
    def company(self,request=""):
        company_id=request.GET.get('company_id')
        sql='select id,name,area,tel,fax,address,zip,industry_code,business,isdeleted,register_time from company where id=%s'
        result=db.fetchonedb(sql,[company_id])
        return {'result':result,'company_id':company_id}
#公司图片
    def picture(self,request=""):
        company_id=request.GET.get('company_id')
        sql='select id,picture_name,intro,picture_path,picture_category from company_picture where id=%s'
        result=db.fetchonedb(sql,[company_id])
        return {'result':result,'company_id':company_id}
#详情
    def details(self,request=""):
        company_id=request.GET.get('company_id')
        sql='select id,name,area,tel,fax,address,zip,industry_code,business,isdeleted,register_time from company where id=%s'
        result=db.fetchonedb(sql,[company_id])
        return {'result':result}
#添加用户
    def save_user(self,request):
        id=request.session.get('user_id')
        name=request.POST.get('name')
        password=request.POST.get('password')
        company_id=request.POST.get('company_id')
        contact=request.POST.get('contact')
        sex=request.POST.get('sex')
        position=request.POST.get('position')
        tel=request.POST.get('tel')
        mobile=request.POST.get('mobile')
        wechat=request.POST.get('wechat')
        qq=request.POST.get('qq')
        email=request.POST.get('email')
        area=request.POST.get('area')
        address=request.POST.get('address')
        register_time=request.POST.get('register_time')
        wechat_id=request.POST.get('wechat_id')
        appid=request.POST.get('appid')
        header_path=request.POST.get('header_path')
        sql='insert into user(id,name,password,company_id,contact,sex,position,tel,mobile,wechat,qq,email,area,address,register_time,wechat_id,appid,header_path) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
        result=db.updatetodb(sql,[id,name,password,company_id,contact,sex,position,tel,mobile,wechat,qq,email,area,address,register_time,wechat_id,appid,header_path])
        
        
    #搜索引擎数据
    #公司信息列表 翻页
    def getcompanylist(self,keywords,frompageCount,limitNum,allnum):
        port = SPHINXCONFIG['port']
        cl = SphinxClient()
        cl.SetServer ( SPHINXCONFIG['serverid'], port )
        cl.SetMatchMode ( SPH_MATCH_BOOLEAN )
        cl.SetSortMode( SPH_SORT_EXTENDED,"membership_code desc,gmt_start desc" )
        cl.SetLimits (frompageCount,limitNum,allnum)
        keywords=request.POST.get('keywords')
        area=request.GET.get('area')
        industry_code=request.GET.get('industry_code')
        area_province=request.GET.get('area1')
        if (keywords):
            res = cl.Query ('@(compname,industry_code) '+keywords,'company')
        else:
            res = cl.Query ('','company')
        if res:
            if res.has_key('matches'):
                clist=res['matches']
                listall_comp=[]
                for match in clist:
                    id=match['id']
                    attrs=match['attrs']
                    compname=attrs['compname']
                    viptype=str(attrs['membership_code'])
                    domain_zz91=attrs['domain_zz91']
                    address=attrs['paddress']
                    membership="普通会员"
                    vipflag=None
                    if (viptype == '10051000'):
                        membership='普通会员'
                        vipflag=None
                    if (viptype == '10051001'):
                        membership='再生通'
                        vipflag=1
                    if (viptype == '1725773192'):
                        membership='银牌品牌通'
                        vipflag=1
                    if (viptype == '1725773193'):
                        membership='金牌品牌通'
                        vipflag=1
                    if (viptype == '1725773194'):
                        membership='钻石品牌通'
                        vipflag=1
                    pbusiness=attrs['pbusiness']
                    if pbusiness:
                        pbusiness=subString(filter_tags(pbusiness),500)
                    parea_province=attrs['parea_province']
                    list1={'id':id,'compname':compname,'business':pbusiness,'area_province':parea_province,'address':address,'membership':membership,'viptype':viptype,'vipflag':vipflag,'domain_zz91':domain_zz91,'productlist':productlist}
                    listall_comp.append(list1)
                listcount_comp=res['total_found']
    
                return {'list':listall_comp,'count':listcount_comp}