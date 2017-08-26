#!/usr/bin/env python   
#coding=utf-8   
import sys
import codecs
import time,datetime
import struct
import os
from crmtools import int_to_strall,str_to_int,getToday

reload(sys)
sys.setdefaultencoding('utf-8')
nowpath=os.path.dirname(__file__)
execfile(nowpath+"/conn.py")

def formattime(value,flag=''):
    if value:
        if (flag==1):
            return value.strftime('%Y-%m-%d')
        else:
            return value.strftime('%Y-%m-%d %H:%M:%S')
    else:
        return ''
def changezhongwen(strvalue):
    if(strvalue == None):
        tempstr=""
    else:
        tempstr=strvalue.decode('GB18030','ignore').encode('utf-8')
    return tempstr
#更新最新数据表
def updatemodifydata(company_id):
    gmt_modified=datetime.datetime.now()
    try:
        sql="replace into update_company (company_id,gmt_modified) values(%s,%s)"
        cursormy.execute(sql,[company_id,gmt_modified])
        connmy.commit()
        return 1
    except TypeError:
        return None
#更新数据表
def getcompany(tab,modate=""):
    print tab
    if tab=="pay_order":
        sql="select * from "+str(tab)+" where UNIX_TIMESTAMP(gmt_created)>( SELECT maxid FROM update_log WHERE utype='re_"+str(tab)+"') order by gmt_created asc limit 0,100000 "
    else:
        if modate:
            sql="select * from "+str(tab)+" where gmt_modified>'"+str(modate)+"' order by gmt_modified asc limit 0,100000"
        else:
            sql="select * from "+str(tab)+" where UNIX_TIMESTAMP(gmt_modified)>( SELECT maxid FROM update_log WHERE utype='re_"+str(tab)+"') order by gmt_modified asc limit 0,100000 "
    cursorserver.execute(sql)
    results = cursorserver.fetchall()
    for list in results:
        filds=""
        vlist=""
        ulist=""
        vals=[]
        id=list['id']
        if tab=="pay_order":
            gmt_modified=list['gmt_created']
        else:
            gmt_modified=list['gmt_modified']
        gmt_modified=gmt_modified.strftime('%Y-%m-%d %H:%M:%S')
        maxid=int(time.mktime(time.strptime(gmt_modified,"%Y-%m-%d %H:%M:%S")))
        for ll in list.keys():
            filds+=ll+","
            vlist+="%s,"
            ulist+=ll+"=%s,"
            content=list[ll]
            vals.append(content)
        filds=filds[0:len(filds)-1]
        vlist=vlist[0:len(vlist)-1]
        ulist=ulist[0:len(ulist)-1]
        
        if tab in ("crm_company_service","phone"):
            sql="replace into "+str(tab)+"("+str(filds)+") values("+vlist+")"
            cursormy.execute(sql,vals)
            connmy.commit()
            company_id=list['company_id']
            if tab=="crm_company_service":
                sqla="insert into kh_newcompany_vap (company_id,gmt_created) values(%s,%s)"
                cursormy.execute(sqla,[company_id,gmt_modified])
                connmy.commit()
            if company_id:
                updatemodifydata(company_id)
            print id
        else:
            sqla="select id from "+str(tab)+" where id=%s"
            result=cursormy.execute(sqla,[id])
            print id
            if not result:
                try:
                    sql="insert into "+str(tab)+"("+str(filds)+") values("+vlist+")"
                    cursormy.execute(sql,vals)
                    connmy.commit()
                except:
                    a=''
                if tab=="company":
                    sqla="insert into kh_newcompany (company_id,gmt_created) values(%s,%s)"
                    cursormy.execute(sqla,[id,gmt_modified])
                    connmy.commit()
                    updatemodifydata(id)
            else:
                sqla="update "+str(tab)+" set "+ulist+" where id="+str(id)
                cursormy.execute(sqla,vals)
                connmy.commit()
                if tab=="company":
                    updatemodifydata(id)
        if not modate:
            sqlc="update update_log set maxid=%s where utype='re_"+tab+"'"
            cursorserver.execute(sqlc,[maxid])
            connserver.commit()
#更新联系次数 人次
def contacthistory():
    sql="select id,company_id,gmt_modified from kh_sales where UNIX_TIMESTAMP(gmt_modified)>(SELECT maxid FROM update_log WHERE utype='contacthistory') order by gmt_modified asc"
    cursormy.execute(sql)
    results = cursormy.fetchall()
    for list in results:
        company_id=list['company_id']
        sid=list['id']
        gmt_modified=list['gmt_modified']
        gmt_modified=gmt_modified.strftime('%Y-%m-%d %H:%M:%S')
        maxid=int(time.mktime(time.strptime(gmt_modified,"%Y-%m-%d %H:%M:%S")))
        #联系人次
        sql="select count(distinct user_id) as telpersoncount from kh_tel where company_id=%s and telflag=0"
        cursormy.execute(sql,[company_id])
        result = cursormy.fetchone()
        telpersoncount=result['telpersoncount']
        
        sql="select count(id) as telcount from kh_tel where company_id=%s and telflag=0 and contacttype=13"
        cursormy.execute(sql,[company_id])
        result = cursormy.fetchone()
        telcount=result['telcount']
        
        sql="select count(id) as telnocount from kh_tel where company_id=%s and telflag=0 and contacttype=12"
        cursormy.execute(sql,[company_id])
        result = cursormy.fetchone()
        telnocount=result['telnocount']
        
        sqlc="update kh_sales set telpersoncount=%s,telcount=%s,telnocount=%s where id=%s"
        cursormy.execute(sqlc,[telpersoncount,telcount,telnocount,sid])
        connmy.commit()
        #updatemodifydata(company_id)
        
        sqlc="update update_log set maxid=%s where utype='contacthistory'"
        cursormy.execute(sqlc,[maxid])
        connmy.commit()
        print company_id
        

#客户分配
def assigncompany():
    sql="select count(0) as ucount from user where assignflag=1 and closeflag=0"
    cursormy.execute(sql)
    result = cursormy.fetchone()
    usercount=result['ucount']
    print usercount
    sql="select company_id from kh_newcompany"
    cursormy.execute(sql)
    results = cursormy.fetchall()
    minuserid=0
    n=0
    gmt_created=gmt_modified=datetime.datetime.now()
    for list in results:
        company_id=list['company_id']
        sqlc="select id from kh_assign where company_id=%s"
        cursormy.execute(sqlc,[company_id])
        resultone = cursormy.fetchone()
        if not resultone:
            sqlc="select user_id from company where id=%s"
            cursormy.execute(sqlc,[company_id])
            resultc = cursormy.fetchone()
            if resultc:
                #录入客户部参与分配
                lruser_id=resultc["user_id"]
                if str(lruser_id)=="0" or not lruser_id:
                    sqlu="select min(id) as minuser_id from user where assignflag=1 and closeflag=0 and id>"+str(minuserid)+" order by id asc"
                    cursormy.execute(sqlu)
                    resultu = cursormy.fetchone()
                    if resultu:
                        minuserid=resultu['minuser_id']
                        
                        sqlt="insert into kh_assign(company_id,user_id,gmt_created) values(%s,%s,%s)"
                        cursormy.execute(sqlt,[company_id,minuserid,gmt_created])
                        connmy.commit()
                        details="系统自动分配"
                        admin_user_id=0
                        sqlb="insert into kh_log (company_id,user_id,details,admin_user_id,gmt_created) values(%s,%s,%s,%s,%s)"
                        cursormy.execute(sqlb,[company_id,minuserid,details,admin_user_id,gmt_created])
                        connmy.commit()
                        sqlc="delete from kh_newcompany where company_id=%s"
                        cursormy.execute(sqlc,[company_id])
                        connmy.commit()
                        updatemodifydata(company_id)
                        n=n+1
                        if n>=usercount:
                            n=0
                            minuserid=0
                    print minuserid
                    print n
                else:
                    print '已经分配'
        else:
            print "已分配！"
#客户实时分配
def assigncompanynow(user_category_code=''):
    #删除不在安排分配客户的用户数据
    print '设置分配客户人员数据'
    sql="delete from kh_assign_count where user_id not in (select id from user where assignflag=1 and closeflag=0) and ctype=0"
    cursormy.execute(sql)
    connmy.commit()
    #未在安排分配人员里，写入，并按最少分配客户的人员来计算
    sql="select id from user where assignflag=1 and closeflag=0 "
    if user_category_code:
        sql+=" and user_category_code='"+str(user_category_code)+"'"
    sql+="order by id desc"
    cursormy.execute(sql)
    results = cursormy.fetchall()
    for list in results:
        user_id=list['id']
        ccount=0
        #获取最小的分配数
        sqlc="select min(ccount) as ccount from kh_assign_count where ctype=0"
        cursormy.execute(sqlc)
        resultc = cursormy.fetchone()
        if resultc:
            ccount=resultc['ccount']
            if not ccount:
                ccount=0
        sqlu="select id from kh_assign_count where ctype=0 and user_id=%s"
        cursormy.execute(sqlu,[user_id])
        resultu = cursormy.fetchone()
        if not resultu:
            sqld="insert into kh_assign_count(ctype,user_id,ccount) values(%s,%s,%s)"
            cursormy.execute(sqld,[0,user_id,ccount])
            connmy.commit()
        print user_id
    #开始分配客户
    print '开始分配'
    gmt_created=gmt_modified=datetime.datetime.now()
    sql="select company_id from kh_newcompany"
    cursormy.execute(sql)
    results = cursormy.fetchall()
    for list in results:
        company_id=list['company_id']
        sqlc="select id from kh_assign where company_id=%s"
        cursormy.execute(sqlc,[company_id])
        resultone = cursormy.fetchone()
        if not resultone:
            sqlc="select user_id from company where id=%s"
            cursormy.execute(sqlc,[company_id])
            resultc = cursormy.fetchone()
            if resultc:
                lruser_id=resultc["user_id"]
                if str(lruser_id)=="0" or not lruser_id:
                    #最少分配客户数的用户
                    sqlu="select a.id,a.user_id,a.ccount from kh_assign_count as a left join user as b on a.user_id=b.id where a.ctype=0 "
                    if user_category_code:
                        sql+=" and b.user_category_code='"+str(user_category_code)+"'"
                    sqlu+=" order by a.ccount asc,a.user_id asc"
                    cursormy.execute(sqlu)
                    resultu = cursormy.fetchone()
                    if resultu:
                        maxassigncount=1000
                        minuserid=resultu['user_id']
                        sqlg="select user_category_code from user where id=%s"
                        cursormy.execute(sqlg,[minuserid])
                        resultg = cursormy.fetchone()
                        if resultg:
                            #VAP销售最多分15个，ICD不限制
                            if resultg['user_category_code']=="1315":
                                maxassigncount=15
                        #分配客户是否超过15个
                        fdate=getToday()
                        sqld="select companycount from kh_assign_countdate where  user_id=%s and fdate=%s"
                        cursormy.execute(sqld,[minuserid,fdate])
                        resultd = cursormy.fetchone()
                        if resultd:
                            companycount=resultd['companycount']
                        else:
                            companycount=0
                            sqld="insert into kh_assign_countdate(user_id,companycount,fdate) values(%s,%s,%s)"
                            cursormy.execute(sqld,[minuserid,0,fdate])
                            connmy.commit()
                        if companycount<maxassigncount:
                            sqlt="insert into kh_assign(company_id,user_id,gmt_created) values(%s,%s,%s)"
                            cursormy.execute(sqlt,[company_id,minuserid,gmt_created])
                            connmy.commit()
                            details="系统自动分配"
                            admin_user_id=0
                            sqlb="insert into kh_log (company_id,user_id,details,admin_user_id,gmt_created) values(%s,%s,%s,%s,%s)"
                            cursormy.execute(sqlb,[company_id,minuserid,details,admin_user_id,gmt_created])
                            connmy.commit()
                            sqlc="delete from kh_newcompany where company_id=%s"
                            cursormy.execute(sqlc,[company_id])
                            connmy.commit()
                            sqld="update kh_assign_count set ccount=ccount+1 where id=%s"
                            cursormy.execute(sqld,[resultu['id']])
                            connmy.commit()
                            
                            #每日分配客户数据
                            sqld="update kh_assign_countdate set companycount=companycount+1 where user_id=%s and fdate=%s"
                            cursormy.execute(sqld,[minuserid,fdate])
                            connmy.commit()
                        """
                        else:
                            #分到黄芩客户库里
                            sqlt="insert into kh_assign(company_id,user_id,gmt_created) values(%s,%s,%s)"
                            cursormy.execute(sqlt,[company_id,800,gmt_created])
                            connmy.commit()
                            details="系统自动分配"
                            admin_user_id=0
                            sqlb="insert into kh_log (company_id,user_id,details,admin_user_id,gmt_created) values(%s,%s,%s,%s,%s)"
                            cursormy.execute(sqlb,[company_id,800,details,admin_user_id,gmt_created])
                            connmy.commit()
                            sqlc="delete from kh_newcompany where company_id=%s"
                            cursormy.execute(sqlc,[company_id])
                            connmy.commit()
                        """
                        
                        updatemodifydata(company_id)
                    print minuserid
                else:
                    print '已经分配'
        else:
            print "已分配！"

#客户实时分配
def assigncompany_vap_now():
    #删除不在安排分配客户的用户数据
    print '设置分配客户人员数据'
    sql="delete from kh_assign_count where user_id not in (select id from user where assignvapflag=1 and closeflag=0) and ctype=1"
    cursormy.execute(sql)
    connmy.commit()
    #未在安排分配人员里，写入，并按最少分配客户的人员来计算
    sql="select id from user where assignvapflag=1 and closeflag=0 order by id desc"
    cursormy.execute(sql)
    results = cursormy.fetchall()
    vapuserlist=[]
    for list in results:
        user_id=list['id']
        vapuserlist.append(user_id)
        ccount=0
        #获取最小的分配数
        sqlc="select min(ccount) as ccount from kh_assign_count where ctype=1"
        cursormy.execute(sqlc)
        resultc = cursormy.fetchone()
        if resultc:
            ccount=resultc['ccount']
            if not ccount:
                ccount=0
        sqlu="select id from kh_assign_count where ctype=1 and user_id=%s"
        cursormy.execute(sqlu,[user_id])
        resultu = cursormy.fetchone()
        if not resultu:
            sqld="insert into kh_assign_count(ctype,user_id,ccount) values(%s,%s,%s)"
            cursormy.execute(sqld,[1,user_id,ccount])
            connmy.commit()
        print user_id
    #开始分配客户
    print '开始分配'
    gmt_created=gmt_modified=datetime.datetime.now()
    sql="select company_id from kh_newcompany_vap"
    cursormy.execute(sql)
    results = cursormy.fetchall()
    for list in results:
        company_id=list['company_id']
        #是否是开通的付费客户
        sqlc="select id from crm_company_service where company_id=%s and apply_status='1'"
        cursormy.execute(sqlc,[company_id])
        resultone = cursormy.fetchone()
        if resultone:
            
            sqlc="select id from kh_assign_vap where company_id=%s"
            cursormy.execute(sqlc,[company_id])
            resultone = cursormy.fetchone()
            if not resultone:
                #ICD库的所属者是否为VAP销售，如果是直接分配给改VAP销售
                minuserid=None
                assignvv=None
                sqlu="select user_id from kh_assign where company_id=%s"
                cursormy.execute(sqlu,[company_id])
                resultu = cursormy.fetchone()
                if resultu:
                    nowicduserid=resultu['user_id']
                    print nowicduserid
                    if nowicduserid in vapuserlist:
                        minuserid=nowicduserid
                if not minuserid:
                    #最少分配客户数的用户
                    sqlu="select id,user_id,ccount from kh_assign_count where ctype=1 order by ccount asc,user_id asc"
                    cursormy.execute(sqlu)
                    resultu = cursormy.fetchone()
                    if resultu:
                        minuserid=resultu['user_id']
                        assignvv=1
                if minuserid:
                    sqlt="insert into kh_assign_vap(company_id,user_id,gmt_created) values(%s,%s,%s)"
                    cursormy.execute(sqlt,[company_id,minuserid,gmt_created])
                    connmy.commit()
                    details="vap系统自动分配"
                    admin_user_id=0
                    sqlb="insert into kh_log (company_id,user_id,details,admin_user_id,gmt_created) values(%s,%s,%s,%s,%s)"
                    cursormy.execute(sqlb,[company_id,minuserid,details,admin_user_id,gmt_created])
                    connmy.commit()
                    sqlc="delete from kh_newcompany_vap where company_id=%s"
                    cursormy.execute(sqlc,[company_id])
                    connmy.commit()
                    if assignvv:
                        sqld="update kh_assign_count set ccount=ccount+1 where id=%s"
                        cursormy.execute(sqld,[resultu['id']])
                        connmy.commit()
                    updatemodifydata(company_id)
                print minuserid
            else:
                sqlc="delete from kh_newcompany_vap where company_id=%s"
                cursormy.execute(sqlc,[company_id])
                connmy.commit()
                print "已分配！"
        else:
            sqlc="delete from kh_newcompany_vap where company_id=%s"
            cursormy.execute(sqlc,[company_id])
            connmy.commit()
#新签客户库里客户分配到再生汇客户库
def updateicdtozsh():
    sql="select a.id,a.company_id,a.user_id from kh_assign as a left join user as b on a.user_id=b.id where b.user_category_code='1325' and b.id!=176"
    cursormy.execute(sql)
    results = cursormy.fetchall()
    for list in results:
        company_id=list['company_id']
        user_id=list['user_id']
        sqlc="select id from kh_assign_zsh where company_id=%s"
        cursormy.execute(sqlc,[company_id])
        resultone = cursormy.fetchone()
        if not resultone:
            gmt_created=gmt_modified=datetime.datetime.now()
            sqlt="insert into kh_assign_zsh(company_id,user_id,gmt_created) values(%s,%s,%s)"
            cursormy.execute(sqlt,[company_id,user_id,gmt_created])
            connmy.commit()
            details="再生汇系统从新签自动分配"
            admin_user_id=0
            sqlb="insert into kh_log (company_id,user_id,details,admin_user_id,gmt_created) values(%s,%s,%s,%s,%s)"
            cursormy.execute(sqlb,[company_id,user_id,details,admin_user_id,gmt_created])
            connmy.commit()
            sqlc="delete from kh_assign where company_id=%s"
            cursormy.execute(sqlc,[company_id])
            connmy.commit()
            updatemodifydata(company_id)
        print company_id
            
#更新最后服务时间
def updateservice_endtime(day=''):
    sql="select gmt_end,company_id,gmt_start from v_company_service"
    if day:
        sql="select gmt_end,company_id,gmt_start from v_company_service where DATEDIFF(CURDATE(),gmt_modified)<=2"
    cursormy.execute(sql)
    results = cursormy.fetchall()
    for list in results:
        gmt_end=list['gmt_end']
        company_id=list['company_id']
        gmt_start=list['gmt_start']
        sqlc="select b.tag,a.membership_code,a.crm_service_code,a.apply_status from crm_company_service as a left join crm_service as b on a.crm_service_code=b.code where a.company_id=%s"
        cursormy.execute(sqlc,[company_id])
        tagslist = cursormy.fetchall()
        servicetag='service,'
        iszsh=0
        ispay=0
        for t in tagslist:
            tag=t['tag']
            crm_service_code=t['crm_service_code']
            membership_code=t['membership_code']
            apply_status=str(t['apply_status'])
            if tag:
                servicetag+=tag+","
            #品牌通
            if (str(membership_code) in ('100510021000','100510021001','100510021002')):
                servicetag+="u,"
            #是否开通再生汇产品
            if (apply_status=='1' and crm_service_code=='1004'):
                iszsh=1
                #是否再生汇部门提交的产品，如果是再生汇部门提交的，直接进入VAP库
                sql="select company_id from v_zshpro where company_id=%s"
                cursormy.execute(sql,[company_id])
                zlist = cursormy.fetchone()
                if zlist:
                    ispay=1
            #是否开通VAP
            elif (apply_status=='1' and crm_service_code!='1004'):
                ispay=1
                
        
        sql="update company_account set service_endtime=%s,service_starttime=%s,servicetag=%s,ispay=%s,iszsh=%s where company_id=%s"
        cursormy.execute(sql,[gmt_end,gmt_start,servicetag,ispay,iszsh,company_id])
        connmy.commit()
        if day:
            updatemodifydata(company_id)
        print company_id

#更新其他联系人信息
def update_othercontact():
    
    sql="select company_id,gmt_modified from kh_othercontact where UNIX_TIMESTAMP(gmt_modified)>( SELECT maxid FROM update_log WHERE utype='othercontact') order by gmt_modified asc"
    cursormy.execute(sql)
    results1 = cursormy.fetchall()
    for list1 in results1:
        company_id=list1['company_id']
        gmt_modified=list1['gmt_modified']
        gmt_modified=gmt_modified.strftime('%Y-%m-%d %H:%M:%S')
        maxid=int(time.mktime(time.strptime(gmt_modified,"%Y-%m-%d %H:%M:%S")))
        
        sql="select tel,mobile,name,email from kh_othercontact where company_id=%s"
        cursormy.execute(sql,[company_id])
        results = cursormy.fetchall()
        othercontact=''
        for list in results:
            tel=list['tel']
            mobile=list['mobile']
            name=list['name']
            email=list['email']
            if name:
                othercontact+=name+","
            if tel:
                othercontact+=tel+","
            if mobile:
                othercontact+=mobile+","
            if email:
                othercontact+=email+","
            
        sql="update company_account set othercontact=%s where company_id=%s"
        cursormy.execute(sql,[othercontact,company_id])
        connmy.commit()
        updatemodifydata(company_id)
        sqlc="update update_log set maxid=%s where utype='othercontact'"
        cursormy.execute(sqlc,[maxid])
        connmy.commit()

#2.2 数据更新
def old_zstinfo():
    sql="select com_id from comp_vapinfo"
    cursor.execute(sql)
    results = cursor.fetchall()
    for list in results:
        company_id=list[0]
        sql="update company_account set ispay=1 where company_id=%s"
        cursormy.execute(sql,[company_id])
        connmy.commit()
        print company_id
def old_cate_adminuser():
    sql="select id,code,meno,ord,closeflag from cate_adminuser "
    cursor.execute(sql)
    results = cursor.fetchall()
    for list in results:
        id=list[0]
        code=list[1]
        label=changezhongwen(list[2])
        ord=list[3]
        closeflag=list[4]
        if str(closeflag)=="1":
            closeflag=0
        else:
            closeflag=1
        sqlc="replace into user_category (id,code,label,ord,closeflag) values(%s,%s,%s,%s,%s)"
        cursormy.execute(sqlc,[id,code,label,ord,closeflag])
        connmy.commit()
def old_renshi_category():
    sql="select id,code,meno,ord from category "
    cursor.execute(sql)
    results = cursor.fetchall()
    for list in results:
        id=list[0]
        code=list[1]
        label=changezhongwen(list[2])
        ord=list[3]
        sqlc="replace into renshi_category (id,code,label,ord) values(%s,%s,%s,%s)"
        cursormy.execute(sqlc,[id,code,label,ord])
        connmy.commit()
def old_users():
    sql="select id,userid,name,password,safepass,realname,closeflag from users "
    cursor.execute(sql)
    results = cursor.fetchall()
    for list in results:
        id=list[0]
        user_category_code=list[1]
        username=changezhongwen(list[2])
        password=changezhongwen(list[3])
        safepasswd=changezhongwen(list[4])
        realname=changezhongwen(list[5])
        closeflag=list[6]
        if str(closeflag)=="1":
            closeflag=0
        else:
            closeflag=1
        sqla="select id from user where id=%s"
        cursormy.execute(sqla,[id])
        result = cursormy.fetchone()
        if not result:
            sqlc="replace into user (id,user_category_code,username,password,safepasswd,realname,closeflag) values(%s,%s,%s,%s,%s,%s,%s)"
            cursormy.execute(sqlc,[id,user_category_code,username,password,safepasswd,realname,closeflag])
            connmy.commit()
#公司其他联系人
def old_Crm_PersonInfo():
    sql="select id,com_id,personComname,PersonName,PersonSex,PersonKey,PersonStation,PersonEmail,PersonTel,PersonFax,PersonMoblie,PersonOther,PersonBz,PersonAddr,Fdate,personid,editDate from Crm_PersonInfo "
    cursor.execute(sql)
    results = cursor.fetchall()
    for list in results:
        id=list[0]
        company_id=list[1]
        name=changezhongwen(list[3])
        sex=list[4]
        if sex==1:
            sex=0
        else:
            sex=1
        station=changezhongwen(list[6])
        email=changezhongwen(list[7])
        tel=changezhongwen(list[8])
        fax=changezhongwen(list[9])
        mobile=changezhongwen(list[10])
        bz=changezhongwen(list[12])
        address=changezhongwen(list[13])
        gmt_created=gmt_modified=formattime(list[14])
        user_id=list[15]
        sqlc="replace into kh_othercontact (id,company_id,name,sex,station,email,tel,fax,mobile,bz,address,gmt_created,gmt_modified,user_id) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        cursormy.execute(sqlc,[id,company_id,name,sex,station,email,tel,fax,mobile,bz,address,gmt_created,gmt_modified,user_id])
        connmy.commit()
        print id
        
def old_assignicd():
    sql="select id,personid,cushion,com_id,fdate,emphases from crm_assign "
    cursor.execute(sql)
    results = cursor.fetchall()
    for list in results:
        id=list[0]
        user_id=list[1]
        isnew=list[2]
        company_id=list[3]
        gmt_created=formattime(list[4])
        emphases=list[5]
        sqlc="replace into kh_assign (id,user_id,isnew,company_id,gmt_created,emphases) values(%s,%s,%s,%s,%s,%s)"
        cursormy.execute(sqlc,[id,user_id,isnew,company_id,gmt_created,emphases])
        connmy.commit()
def old_assignvap():
    sql="select id,personid,cushion,com_id,fdate,emphases from crm_assignvap "
    cursor.execute(sql)
    results = cursor.fetchall()
    for list in results:
        id=list[0]
        user_id=list[1]
        isnew=list[2]
        company_id=list[3]
        gmt_created=formattime(list[4])
        emphases=list[5]
        sqlc="replace into kh_assign_vap (id,user_id,isnew,company_id,gmt_created,emphases) values(%s,%s,%s,%s,%s,%s)"
        cursormy.execute(sqlc,[id,user_id,isnew,company_id,gmt_created,emphases])
        connmy.commit()
        
def old_comsales():
    sql="select id,com_id,com_rank,contactnext_time,contacttype,lastteldate from comp_sales where id>=809259 order by id asc"
    cursor.execute(sql)
    results = cursor.fetchall()
    for list in results:
        try:
            id=list[0]
            company_id=list[1]
            rank=list[2]
            contactnexttime=formattime(list[3])
            contacttype=list[4]
            lastteltime=formattime(list[5])
            gmt_created=gmt_modified=lastteltime
            print id
            sqlc="replace into kh_sales (id,company_id,rank,contactnexttime,contacttype,lastteltime,gmt_created,gmt_modified) values(%s,%s,%s,%s,%s,%s,%s,%s)"
            cursormy.execute(sqlc,[id,company_id,rank,contactnexttime,contacttype,lastteltime,gmt_created,gmt_modified])
            connmy.commit()
        except:
            print 'err'
def old_salestime():
    sql="select lastteltime,contactnexttime,company_id from v_teltime"
    cursormy.execute(sql)
    results = cursormy.fetchall()
    for list in results:
        lastteltime=list['lastteltime']
        contactnexttime=list['contactnexttime']
        company_id=list['company_id']
        sqlc="update kh_sales set lastteltime=%s,contactnexttime=%s where company_id=%s"
        cursormy.execute(sqlc,[lastteltime,contactnexttime,company_id])
        connmy.commit()
        updatemodifydata(company_id)
        print company_id
#黄页
def old_huangye():
    maxid=0
    sql="select maxid from update_log where utype='old_huangye'"
    cursormy.execute(sql)
    results = cursormy.fetchone()
    if results:
        maxid=results['maxid']
    if maxid==0:
        fdate='2000-1-1'
    else:
        fdate=int_to_strall(maxid)
    print fdate
    sql="select 0,id,com_email,newemail,membertype,com_id,cname,comkeywords,js1,js2,sl1,sl2,qt1,qt2,province,city,convert(text,cproductslist),ccontactp,ctel,cmobile,weixin,cadd,personid,personname,fdate,pcheck,huangye_qukan from huangye_list where fdate>='"+str(fdate)+"' and huangye_qukan='2017' order by fdate asc"
    cursor.execute(sql)
    results = cursor.fetchall()
    for list in results:
        id=list[1]
        com_email=changezhongwen(list[2])
        newemail=list[3]
        membertype=list[4]
        com_id=list[5]
        cname=changezhongwen(list[6])
        comkeywords=list[7]
        js1=changezhongwen(list[8])
        js2=changezhongwen(list[9])
        sl1=changezhongwen(list[10])
        sl2=changezhongwen(list[11])
        qt1=changezhongwen(list[12])
        qt2=changezhongwen(list[13])
        province=changezhongwen(list[14])
        city=changezhongwen(list[15])
        cproductslist=changezhongwen(list[16])
        ccontactp=changezhongwen(list[17])
        ctel=changezhongwen(list[18])
        cmobile=changezhongwen(list[19])
        weixin=changezhongwen(list[20])
        cadd=changezhongwen(list[21])
        personid=list[22]
        personname=changezhongwen(list[23])
        fdate=formattime(list[24])
        pcheck=list[25]
        huangye_qukan=list[26]
        print fdate
        maxid=str_to_int(fdate)
        
        print id
        sqlc="replace into huangye_list (id,com_email,newemail,membertype,com_id,cname,comkeywords,js1,js2,sl1,sl2,qt1,qt2,province,city,cproductslist,ccontactp,ctel,cmobile,weixin,cadd,personid,personname,fdate,pcheck,huangye_qukan) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        cursormy.execute(sqlc,[id,com_email,newemail,membertype,com_id,cname,comkeywords,js1,js2,sl1,sl2,qt1,qt2,province,city,cproductslist,ccontactp,ctel,cmobile,weixin,cadd,personid,personname,fdate,pcheck,huangye_qukan])
        connmy.commit()
    sqlc="update update_log set maxid=%s where utype='old_huangye'"
    cursormy.execute(sqlc,[maxid])
    connmy.commit()
#人事信息
def old_renshiuser():
    maxid=0
    sql="select maxid from update_log where utype='old_renshiuser'"
    cursormy.execute(sql)
    results = cursormy.fetchone()
    if results:
        maxid=results['maxid']
    if maxid==0:
        fdate='1970-1-1'
    else:
        fdate=int_to_strall(maxid)
    print fdate
    sql="select id,username,mobile,station,othercontact,email,sex,education,requestSucc,interviewTime,resumeUrl,jl1,jl2,jl3,jl4,jl5,gmt_created,gmt_modified,personid,laiyuan,star,worklonger,contactstat,station2 from renshi_user where gmt_created>='"+str(fdate)+"' and id>32447 order by gmt_modified asc"
    cursor.execute(sql)
    results = cursor.fetchall()
    for list in results:
        id=list[0]
        username=changezhongwen(list[1])
        mobile=changezhongwen(list[2])
        station=changezhongwen(list[3])
        othercontact=changezhongwen(list[4])
        email=changezhongwen(list[5])
        sex=changezhongwen(list[6])
        education=changezhongwen(list[7])
        requestSucc=changezhongwen(list[8])
        interviewTime=formattime(list[9])
        resumeUrl=changezhongwen(list[10])
        jl1=list[11]
        jl2=list[12]
        jl3=list[13]
        jl4=list[14]
        jl5=list[15]
        gmt_created=formattime(list[16])
        gmt_modified=list[17]
        personid=list[18]
        laiyuan=changezhongwen(list[19])
        star=list[20]
        worklonger=list[21]
        contactstat=list[22]
        station2=list[23]
        maxid=str_to_int(gmt_created)
        
        print id
        sqlc="replace into renshi_user (id,username,mobile,station,othercontact,email,sex,education,requestSucc,interviewTime,resumeUrl,jl1,jl2,jl3,jl4,jl5,gmt_created,gmt_modified,personid,laiyuan,star,worklonger,contactstat,station2) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        cursormy.execute(sqlc,[id,username,mobile,station,othercontact,email,sex,education,requestSucc,interviewTime,resumeUrl,jl1,jl2,jl3,jl4,jl5,gmt_created,gmt_modified,personid,laiyuan,star,worklonger,contactstat,station2])
        connmy.commit()
    sqlc="update update_log set maxid=%s where utype='old_renshiuser'"
    cursormy.execute(sqlc,[maxid])
    connmy.commit()
def old_renshi_assign():
    maxid=0
    sql="select maxid from update_log where utype='old_renshi_assign'"
    cursormy.execute(sql)
    results = cursormy.fetchone()
    if results:
        maxid=results['maxid']
    if maxid==0:
        fdate='2017-1-16'
    else:
        fdate=int_to_strall(maxid)
    print fdate
    sql="select id,personid,uid,fdate from renshi_assign where fdate>='"+str(fdate)+"' order by fdate asc"
    cursor.execute(sql)
    results = cursor.fetchall()
    for list in results:
        id=list[0]
        personid=list[1]
        uid=list[2]
        
        fdate=formattime(list[3])
        maxid=str_to_int(fdate)
        print id
        sqlc="replace into renshi_assign (id,personid,uid,fdate) values(%s,%s,%s,%s)"
        cursormy.execute(sqlc,[id,personid,uid,fdate])
        connmy.commit()
    sqlc="update update_log set maxid=%s where utype='old_renshi_assign'"
    cursormy.execute(sqlc,[maxid])
    connmy.commit()
def old_renshi_history():
    maxid=0
    sql="select maxid from update_log where utype='old_renshi_history'"
    cursormy.execute(sql)
    results = cursormy.fetchone()
    if results:
        maxid=results['maxid']
    if maxid==0:
        fdate='1970-1-1'
    else:
        fdate=int_to_strall(maxid)
    print fdate
    sql="select id,uid,star,code,contactstat,convert(text,bz),nextteltime,fdate,personid from renshi_history where fdate>='"+str(fdate)+"' order by fdate asc"
    cursor.execute(sql)
    results = cursor.fetchall()
    for list in results:
        id=list[0]
        uid=list[1]
        star=list[2]
        code=changezhongwen(list[3])
        contactstat=list[4]
        bz=changezhongwen(list[5])
        nextteltime=formattime(list[6])
        fdate=formattime(list[7])
        maxid=str_to_int(fdate)
        personid=list[8]
        print id
        if not star:
            star=0
        if not contactstat:
            contactstat=0
        sqlc="replace into renshi_history (id,uid,star,code,contactstat,bz,nextteltime,fdate,personid) values(%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        cursormy.execute(sqlc,[id,uid,star,code,contactstat,bz,nextteltime,fdate,personid])
        connmy.commit()
    sqlc="update update_log set maxid=%s where utype='old_renshi_history'"
    cursormy.execute(sqlc,[maxid])
    connmy.commit()
    
def old_renshi_historyBz():
    maxid=0
    sql="select maxid from update_log where utype='old_renshi_historyBz'"
    cursormy.execute(sql)
    results = cursormy.fetchone()
    if results:
        maxid=results['maxid']
    if maxid==0:
        fdate='1970-1-1'
    else:
        fdate=int_to_strall(maxid)
    print fdate
    sql="select id,uid,personid,fdate,convert(text,bz) from renshi_historyBz where fdate>='"+str(fdate)+"' order by fdate asc"
    cursor.execute(sql)
    results = cursor.fetchall()
    for list in results:
        id=list[0]
        uid=list[1]
        personid=list[2]
        fdate=formattime(list[3])
        maxid=str_to_int(fdate)
        bz=changezhongwen(list[4])
        print id
        sqlc="replace into renshi_historyBz (id,uid,personid,fdate,bz) values(%s,%s,%s,%s,%s)"
        cursormy.execute(sqlc,[id,uid,personid,fdate,bz])
        connmy.commit()
    sqlc="update update_log set maxid=%s where utype='old_renshi_historyBz'"
    cursormy.execute(sqlc,[maxid])
    connmy.commit()
    
def old_seo_dolist():
    maxid=0
    sql="select maxid from update_log where utype='old_seo_dolist'"
    cursormy.execute(sql)
    results = cursormy.fetchone()
    if results:
        maxid=results['maxid']
    if maxid==0:
        fdate='1970-1-1'
    else:
        fdate=int_to_strall(maxid)
    print fdate
    sql="select id,sid,com_id,convert(text,detail),gmt_time,personid from seo_dolist where gmt_time>='"+str(fdate)+"' order by gmt_time asc"
    cursor.execute(sql)
    results = cursor.fetchall()
    for list in results:
        id=list[0]
        sid=list[1]
        com_id=list[2]
        detail=changezhongwen(list[3])
        gmt_time=formattime(list[4])
        maxid=str_to_int(gmt_time)
        personid=list[5]
        print id
        sqlc="replace into seo_dolist (id,sid,com_id,detail,gmt_time,personid) values(%s,%s,%s,%s,%s,%s)"
        cursormy.execute(sqlc,[id,sid,com_id,detail,gmt_time,personid])
        connmy.commit()
    sqlc="update update_log set maxid=%s where utype='old_seo_dolist'"
    cursormy.execute(sqlc,[maxid])
    connmy.commit()
def old_seo_keywords_history():
    maxid=0
    sql="select maxid from update_log where utype='old_seo_keywords_history'"
    cursormy.execute(sql)
    results = cursormy.fetchone()
    if results:
        maxid=results['maxid']
    if maxid==0:
        fdate='1970-1-1'
    else:
        fdate=int_to_strall(maxid)
    print fdate
    sql="select id,kid,sid,ktype,baidu_ranking,kdate,baidu_sl,baidu_kuaizhao,baidu_fanlian,gmt_created from seo_keywords_history where gmt_created>='"+str(fdate)+"' order by gmt_created asc"
    cursor.execute(sql)
    results = cursor.fetchall()
    valu=[]
    n=0
    for list in results:
        id=list[0]
        kid=list[1]
        sid=list[2]
        ktype=changezhongwen(list[3])
        baidu_ranking=list[4]
        kdate=formattime(list[5])
        baidu_sl=list[6]
        baidu_kuaizhao=formattime(list[7])
        baidu_fanlian=list[8]
        gmt_created=formattime(list[9])
        maxid=str_to_int(gmt_created)
        l=(id,kid,sid,ktype,baidu_ranking,kdate,baidu_sl,baidu_kuaizhao,baidu_fanlian,gmt_created)
        valu.append(l)
        n+=1
        if n>=10000:
            sqlc="replace into seo_keywords_history (id,kid,sid,ktype,baidu_ranking,kdate,baidu_sl,baidu_kuaizhao,baidu_fanlian,gmt_created) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            cursormy.executemany(sqlc,valu)
            connmy.commit()
            n=0
            valu=[]
            print n
            sqlc="update update_log set maxid=%s where utype='old_seo_keywords_history'"
            cursormy.execute(sqlc,[maxid])
            connmy.commit()
    if n<10000 and n>0:
        sqlc="replace into seo_keywords_history (id,kid,sid,ktype,baidu_ranking,kdate,baidu_sl,baidu_kuaizhao,baidu_fanlian,gmt_created) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        cursormy.executemany(sqlc,valu)
        connmy.commit()
        sqlc="update update_log set maxid=%s where utype='old_seo_keywords_history'"
        cursormy.execute(sqlc,[maxid])
        connmy.commit()
        n=0
        valu=[]

def old_seo_keywordslist():
    maxid=0
    sql="select maxid from update_log where utype='old_seo_keywordslist'"
    cursormy.execute(sql)
    results = cursormy.fetchone()
    if results:
        maxid=results['maxid']
    if maxid==0:
        fdate='1970-1-1'
    else:
        fdate=int_to_strall(maxid)
    print fdate
    sql="select id,sid,keywords,com_msb,seo_start,target_time,expire_time,target_require,target_assure,price,baidu_ranking,personid,dbtype,gmt_created from seo_keywordslist where gmt_created>='"+str(fdate)+"' order by gmt_created asc"
    cursor.execute(sql)
    results = cursor.fetchall()
    for list in results:
        id=list[0]
        sid=list[1]
        keywords=changezhongwen(list[2])
        com_msb=changezhongwen(list[3])
        seo_start=formattime(list[4])
        target_time=formattime(list[5])
        expire_time=formattime(list[6])
        target_require=list[7]
        target_assure=formattime(list[8])
        price=list[9]
        baidu_ranking=list[10]
        personid=list[11]
        dbtype=list[12]
        gmt_created=formattime(list[13])
        maxid=str_to_int(gmt_created)
        
        print id
        sqlc="replace into seo_keywordslist (id,sid,keywords,com_msb,seo_start,target_time,expire_time,target_require,target_assure,price,baidu_ranking,personid,dbtype,gmt_created) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        cursormy.execute(sqlc,[id,sid,keywords,com_msb,seo_start,target_time,expire_time,target_require,target_assure,price,baidu_ranking,personid,dbtype,gmt_created])
        connmy.commit()
    sqlc="update update_log set maxid=%s where utype='old_seo_keywordslist'"
    cursormy.execute(sqlc,[maxid])
    connmy.commit()
def old_seo_list():
    maxid=0
    sql="select maxid from update_log where utype='old_seo_list'"
    cursormy.execute(sql)
    results = cursormy.fetchone()
    if results:
        maxid=results['maxid']
    if maxid==0:
        fdate='1970-1-1'
    else:
        fdate=int_to_strall(maxid)
    print fdate
    sql="select id,com_id,com_email,target_assure,seo_start,target_time,target_require,expire_time,com_msb,price,baidu_ranking,baidu_sl,baidu_kuaizhao,baidu_fanlian,personid,salespersonid,gmt_created,dbflag,waste from seo_list where gmt_created>='"+str(fdate)+"' order by gmt_created asc"
    cursor.execute(sql)
    results = cursor.fetchall()
    for list in results:
        id=list[0]
        com_id=list[1]
        com_email=changezhongwen(list[2])
        target_assure=formattime(list[3])
        seo_start=formattime(list[4])
        target_time=formattime(list[5])
        target_require=formattime(list[6])
        expire_time=formattime(list[7])
        com_msb=changezhongwen(list[8])
        price=list[9]
        baidu_ranking=list[10]
        baidu_sl=list[11]
        baidu_kuaizhao=list[12]
        baidu_fanlian=list[13]
        personid=list[14]
        salespersonid=list[15]
        gmt_created=formattime(list[16])
        dbflag=list[17]
        waste=list[18]
        maxid=str_to_int(gmt_created)
        
        print id
        sqlc="replace into seo_list (id,com_id,com_email,target_assure,seo_start,target_time,target_require,expire_time,com_msb,price,baidu_ranking,baidu_sl,baidu_kuaizhao,baidu_fanlian,personid,salespersonid,gmt_created,dbflag,waste) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        cursormy.execute(sqlc,[id,com_id,com_email,target_assure,seo_start,target_time,target_require,expire_time,com_msb,price,baidu_ranking,baidu_sl,baidu_kuaizhao,baidu_fanlian,personid,salespersonid,gmt_created,dbflag,waste])
        connmy.commit()
    sqlc="update update_log set maxid=%s where utype='old_seo_list'"
    cursormy.execute(sqlc,[maxid])
    connmy.commit()
def old_comsalesvap():
    sql="select id,com_id,com_rank,contactnext_time,contacttype,lastteldate from comp_salesvap order by id asc"
    cursor.execute(sql)
    results = cursor.fetchall()
    for list in results:
        try:
            id=list[0]
            company_id=list[1]
            rank=list[2]
            contactnexttime=formattime(list[3])
            contacttype=list[4]
            lastteltime=formattime(list[5])
            gmt_created=gmt_modified=lastteltime
            print id
            sqlc="replace into kh_sales_vap (id,company_id,rank,contactnexttime,contacttype,lastteltime,gmt_created,gmt_modified) values(%s,%s,%s,%s,%s,%s,%s,%s)"
            cursormy.execute(sqlc,[id,company_id,rank,contactnexttime,contacttype,lastteltime,gmt_created,gmt_modified])
            connmy.commit()
        except:
            print 'err'
def old_comtel():
    maxid=0
    sql="select maxid from update_log where utype='old_comtel'"
    cursormy.execute(sql)
    results = cursormy.fetchone()
    if results:
        maxid=results['maxid']
    sql="select top 1000000 id,com_id,teldate,personid,com_rank,contactnext_time,telflag,convert(text,detail),contacttype from comp_tel where id>"+str(maxid)+" order by id asc"
    cursor.execute(sql)
    results = cursor.fetchall()
    valu=[]
    n=0
    for list in results:
        try:
            id=list[0]
            company_id=list[1]
            contacttype=list[8]
            teltime=formattime(list[2])
            user_id=list[3]
            rank=list[4]
            telflag=list[6]
            contactnexttime=formattime(list[5])
            detail=changezhongwen(list[7])
            gmt_created=gmt_modified=teltime
            
            maxid=id
            l=(id,company_id,contacttype,teltime,user_id,rank,telflag,contactnexttime,detail,gmt_created)
            valu.append(l)
        except:
            print 'err'
        n+=1
        print n
        if n>=1000:
            sqlc="replace into kh_tel (id,company_id,contacttype,teltime,user_id,rank,telflag,contactnexttime,detail,gmt_created) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            cursormy.executemany(sqlc,valu)
            connmy.commit()
            sqlc="update update_log set maxid=%s where utype='old_comtel'"
            cursormy.execute(sqlc,[maxid])
            connmy.commit()
            n=0
            valu=[]
        
    if n<1000 and n>0:
        sqlc="replace into kh_tel (id,company_id,contacttype,teltime,user_id,rank,telflag,contactnexttime,detail,gmt_created) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        cursormy.executemany(sqlc,valu)
        connmy.commit()
        n=0
        valu=[]
        sqlc="update update_log set maxid=%s where utype='old_comtel'"
        cursormy.execute(sqlc,[maxid])
        connmy.commit()
def old_assignHistory():
    maxid=0
    sql="select maxid from update_log where utype='old_historylog'"
    cursormy.execute(sql)
    results = cursormy.fetchone()
    if results:
        maxid=results['maxid']
    sql="select top 1000000 id,com_id,personid,fdate,sdetail,mypersonid from crm_assignHistory where id>"+str(maxid)+" order by id asc"
    cursor.execute(sql)
    results = cursor.fetchall()
    valu=[]
    n=0
    for list in results:
        try:
            id=list[0]
            company_id=list[1]
            user_id=list[5]
            gmt_created=formattime(list[3])
            details=changezhongwen(list[4])
            admin_user_id=list[2]
            if not user_id:
                user_id=0
            #print id
            l=(id,company_id,user_id,gmt_created,details,admin_user_id)
            valu.append(l)
            maxid=id
        except:
            print 'err'
        n+=1
        if n>=10000:
            sqlc="replace into kh_log (id,company_id,user_id,gmt_created,details,admin_user_id) values(%s,%s,%s,%s,%s,%s)"
            cursormy.executemany(sqlc,valu)
            connmy.commit()
            sqlc="update update_log set maxid=%s where utype='old_historylog'"
            cursormy.execute(sqlc,[maxid])
            connmy.commit()
            n=0
            valu=[]
            print n
    if n<10000 and n>0:
        sqlc="replace into kh_log (id,company_id,user_id,gmt_created,details,admin_user_id) values(%s,%s,%s,%s,%s,%s)"
        cursormy.executemany(sqlc,valu)
        connmy.commit()
        sqlc="update update_log set maxid=%s where utype='old_historylog'"
        cursormy.execute(sqlc,[maxid])
        connmy.commit()
        n=0
        valu=[]
    
def old_is4star():
    sql="select com_id from crm_have4star"
    cursor.execute(sql)
    results = cursor.fetchall()
    for list in results:
        try:
            sqlc="update kh_sales set is4star=1 where company_id=%s"
            cursormy.execute(sqlc,[list[0]])
            connmy.commit()
            print list[0]
        except:
            print 'err'
def old_is5star():
    sql="select com_id from crm_have5star"
    cursor.execute(sql)
    results = cursor.fetchall()
    for list in results:
        try:
            sqlc="update kh_sales set is5star=1 where company_id=%s"
            cursormy.execute(sqlc,[list[0]])
            connmy.commit()
            print list[0]
        except:
            print 'err'
            
def old_to4star():
    maxid=0
    sql="select maxid from update_log where utype='old_to4star'"
    cursormy.execute(sql)
    results = cursormy.fetchone()
    if results:
        maxid=results['maxid']
    sql="select id,personid,com_id,fdate from crm_to4star where id>"+str(maxid)+" and fdate>'2015-11-1'"
    cursor.execute(sql)
    results = cursor.fetchall()
    for list in results:
        id=list[0]
        user_id=list[1]
        company_id=list[2]
        gmt_created=formattime(list[3])
        rank=4
        sqlc="insert into kh_changestar (user_id,rank,company_id,gmt_created,telflag) values(%s,%s,%s,%s,%s)"
        cursormy.execute(sqlc,[user_id,rank,company_id,gmt_created,0])
        connmy.commit()
        print id
        maxid=id
    sqlc="update update_log set maxid=%s where utype='old_to4star'"
    cursormy.execute(sqlc,[maxid])
    connmy.commit()
def old_to5star():
    maxid=0
    sql="select maxid from update_log where utype='old_to5star'"
    cursormy.execute(sql)
    results = cursormy.fetchone()
    if results:
        maxid=results['maxid']
    sql="select id,personid,com_id,fdate from crm_to5star where id>"+str(maxid)+" and fdate>'2015-11-1'"
    cursor.execute(sql)
    results = cursor.fetchall()
    for list in results:
        id=list[0]
        user_id=list[1]
        company_id=list[2]
        gmt_created=formattime(list[3])
        rank=5
        sqlc="insert into kh_changestar (user_id,rank,company_id,gmt_created,telflag) values(%s,%s,%s,%s,%s)"
        cursormy.execute(sqlc,[user_id,rank,company_id,gmt_created,0])
        connmy.commit()
        maxid=id
        print id
    sqlc="update update_log set maxid=%s where utype='old_to5star'"
    cursormy.execute(sqlc,[maxid])
    connmy.commit()

def old_vaptostar():
    maxid=0
    sql="select maxid from update_log where utype='old_vaptostar'"
    cursormy.execute(sql)
    results = cursormy.fetchone()
    if results:
        maxid=results['maxid']
    sql="select id,personid,com_id,fdate,star from crm_Tostar_vap where id>"+str(maxid)+" and fdate>'2015-11-1'"
    cursor.execute(sql)
    results = cursor.fetchall()
    for list in results:
        id=list[0]
        user_id=list[1]
        company_id=list[2]
        gmt_created=formattime(list[3])
        rank=list[4]
        sqlc="insert into kh_changestar (user_id,rank,company_id,gmt_created,telflag) values(%s,%s,%s,%s,%s)"
        cursormy.execute(sqlc,[user_id,rank,company_id,gmt_created,4])
        connmy.commit()
        print id
        maxid=id
    sqlc="update update_log set maxid=%s where utype='old_vaptostar'"
    cursormy.execute(sqlc,[maxid])
    connmy.commit()
            
def old_assignout():
    sql="select id,com_id,telid,fdate from crm_assign_out where id >1701915"
    cursor.execute(sql)
    results = cursor.fetchall()
    valu=[]
    n=0
    for list in results:
        id=list[0]
        company_id=list[1]
        tel_id=list[2]
        sqlc="select personid,telflag from comp_tel where id="+str(tel_id)
        cursor.execute(sqlc)
        retp = cursor.fetchone()
        user_id=0
        telflag=0
        if retp:
            user_id=retp[0]
            telflag=retp[1]
        gmt_created=formattime(list[3])
        l=(id,company_id,user_id,tel_id,gmt_created,telflag)
        valu.append(l)
        n+=1
        if n>=10000:
            sqlc="replace into kh_droptogonghai (id,company_id,user_id,tel_id,gmt_created,telflag) values(%s,%s,%s,%s,%s,%s)"
            cursormy.executemany(sqlc,valu)
            connmy.commit()
            n=0
            valu=[]
            print n
            
    if n<10000 and n>0:
        sqlc="replace into kh_droptogonghai (id,company_id,user_id,tel_id,gmt_created,telflag) values(%s,%s,%s,%s,%s,%s)"
        cursormy.executemany(sqlc,valu)
        connmy.commit()
        n=0
        valu=[]

def old_crm_seotel():
    sql="select id,telid from crm_seotel where id >0 order by id asc"
    cursor.execute(sql)
    results = cursor.fetchall()
    for list in results:
        id=list[0]
        telid=list[1]
        sqlc="update kh_tel set teltags=1 where id=%s"
        cursormy.execute(sqlc,[telid])
        connmy.commit()
        print id
#录入客户
def old_crm_InsertCompWeb():
    sql="select id,com_id,personid,ccheck from crm_InsertCompWeb where id >0 order by id asc"
    cursor.execute(sql)
    results = cursor.fetchall()
    for list in results:
        id=list[0]
        company_id=list[1]
        user_id=list[2]
        checked=list[3]
        #1为未审核  0 已审核  默认已经审核
        if (str(checked)=="0"):
            checked=1
        else:
            checked=0
        sqlc="update company set user_id=%s,checked=%s where id=%s"
        cursormy.execute(sqlc,[user_id,checked,company_id])
        connmy.commit()
        print id
#垃圾客户
def old_lajicomp():
    sql="select com_id,com_type from v_salescomp where com_type=13 order by com_id asc"
    cursor.execute(sql)
    results = cursor.fetchall()
    for list in results:
        company_id=list[0]
        com_type=list[1]
        if (str(com_type)=="13"):
            islaji=1
        else:
            islaji=0
        sqlc="update company set islaji=%s where id=%s"
        cursormy.execute(sqlc,[islaji,company_id])
        connmy.commit()
        print company_id
        
#死海客户
def old_isdeathcomp():
    sql="select com_id from crm_notbussiness order by com_id asc"
    cursor.execute(sql)
    results = cursor.fetchall()
    for list in results:
        company_id=list[0]
        sqlc="update company set isdeath=%s where id=%s"
        cursormy.execute(sqlc,[1,company_id])
        connmy.commit()
        print company_id
        
def old_salesincome():
    sql="select id,personid,userid,com_id,order_no,realname,sales_date,service_type,service_type1,sales_type,sales_price,sales_email,sales_mobile,sales_bz,com_contactperson,com_mobile,com_ly1,com_ly2,com_zq,com_fwq,com_khdq,com_pro,com_cpjb,com_cxfs,com_regtime,com_hkfs,com_logincount,com_gjd,com_servernum from renshi_salesIncome where id >0"
    cursor.execute(sql)
    results = cursor.fetchall()
    valu=[]
    n=0
    for list in results:
        id=list[0]
        user_id=list[1]
        user_category_code=list[2]
        company_id=list[3]
        order_no=list[4]
        realname=changezhongwen(list[5])
        sales_date=formattime(list[6])
        service_type=changezhongwen(list[7])
        service_type1=changezhongwen(list[8])
        sales_type=changezhongwen(list[9])
        sales_price=list[10]
        email=changezhongwen(list[11])
        mobile=changezhongwen(list[15])
        bz=changezhongwen(list[13])
        contactperson=changezhongwen(list[14])
        com_ly1=changezhongwen(list[16])
        com_ly2=changezhongwen(list[17])
        com_zq=changezhongwen(list[18])
        com_fwq=changezhongwen(list[19])
        com_khdq=changezhongwen(list[20])
        com_pro=changezhongwen(list[21])
        com_cpjb=changezhongwen(list[22])
        com_cxfs=changezhongwen(list[23])
        regtime=formattime(list[24])
        com_hkfs=changezhongwen(list[25])
        logincount=list[26]
        com_gjd=changezhongwen(list[27])
        com_servernum=list[28]
        gmt_created=sales_date
        sqlc="select assignflag from crm_openConfirm where confirmID='"+str(order_no)+"' and com_id="+str(company_id)+""
        cursor.execute(sqlc)
        resultsc = cursor.fetchone()
        assignflag=0
        if resultsc:
            #放待开通未分配
            assignflag=resultsc[0]
            if str(assignflag)=="0":
                assignflag=1  #未分配
            else:
                assignflag=0  #已分配

        l=(id,user_id,user_category_code,company_id,order_no,realname,sales_date,service_type,service_type1,sales_type,sales_price,email,mobile,bz,contactperson,com_ly1,com_ly2,com_zq,com_fwq,com_khdq,com_pro,com_cpjb,com_cxfs,regtime,com_hkfs,logincount,com_gjd,com_servernum,gmt_created,assignflag)
        valu.append(l)
        n+=1
        if n>=1000:
            sqlc="replace into kh_income (id,user_id,user_category_code,company_id,order_no,realname,sales_date,service_type,service_type1,sales_type,sales_price,email,mobile,bz,contactperson,com_ly1,com_ly2,com_zq,com_fwq,com_khdq,com_pro,com_cpjb,com_cxfs,regtime,com_hkfs,logincount,com_gjd,com_servernum,gmt_created,assigncheck) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            cursormy.executemany(sqlc,valu)
            connmy.commit()
            n=0
            valu=[]
            print n
            
    if n<1000 and n>0:
        sqlc="replace into kh_income (id,user_id,user_category_code,company_id,order_no,realname,sales_date,service_type,service_type1,sales_type,sales_price,email,mobile,bz,contactperson,com_ly1,com_ly2,com_zq,com_fwq,com_khdq,com_pro,com_cpjb,com_cxfs,regtime,com_hkfs,logincount,com_gjd,com_servernum,gmt_created,assigncheck) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        cursormy.executemany(sqlc,valu)
        connmy.commit()
        n=0
        valu=[]
#更新客户消费金额
def update_salesincome():
    sql="select sum(sales_price) as sales_price,company_id from kh_income group by company_id"
    cursormy.execute(sql)
    results = cursormy.fetchall()
    for list in results:
        price=list['sales_price']
        if price:
            price=int(price)
        if not price:
            price=0
        company_id=list['company_id']
        valu=[price,company_id]
        sqlc="update kh_sales_vap set income=%s where company_id=%s"
        cursormy.execute(sqlc,valu)
        connmy.commit()
        print company_id
            
    
def insertrtdata():
    """
    sql="select id,compname,business,service_code,regtime from v_compall order by id asc limit 0,10"
    cursormy.execute(sql)
    results = cursormy.fetchall()
    valu=[]
    if results:
        for list in results:
            l=(list['id'],list['compname'],list['business'],list['service_code'],str(list['regtime']))
            valu.append(l)
    print valu
    sql = "replace into company_rt(id,compname,business,service_code,regtime) values(%s,%s,%s,%s,%s)"
    cursor_rt.executemany(sql,valu)
    conn_rt.commit()
    #return
    """
    sql="select * from v_compall limit 0,1000"
    cursormy.execute(sql)
    results = cursormy.fetchall()
    vals=[]
    for list in results:
        filds=""
        vlist=""
        id=list['id']
        l=[id]
        for ll in list:
            if ll!="id":
                filds+=ll+","
                vlist+="%s,"
                content=list[ll]
                if not content:
                    content=""
                l.append(str(content))
        l=tuple(l)
        vals.append(l)
        filds=filds[0:len(filds)-1]
        vlist=vlist[0:len(vlist)-1]
    
    sql="replace into company_rt(id,"+str(filds)+") values(%s,"+vlist+")"
    print sql
    print vals
    cursor_rt.executemany(sql,vals)
    conn_rt.commit()
    
#新注册或公海挑入3天内未联系
def drop_newcomp():
    sql="select a.user_id,a.company_id from kh_assign as a left join user as b on a.user_id=b.id where a.isnew=0 and DATEDIFF(CURDATE(),a.gmt_created)>=4 and b.closeflag=0 and b.dropflag=1"
    cursormy.execute(sql)
    resultall = cursormy.fetchall()
    for list in resultall:
        gmt_created=gmt_modified=datetime.datetime.now()
        company_id=list['company_id']
        user_id=list['user_id']
        sqla="select id from kh_assign where company_id=%s"
        cursormy.execute(sqla,[company_id])
        resulta = cursormy.fetchone()
        if resulta:
            #记录客户记录
            details="新客户3天未联系掉公海"
            admin_user_id=0
            sqlb="insert into kh_log (company_id,user_id,details,admin_user_id,gmt_created) values(%s,%s,%s,%s,%s)"
            cursormy.execute(sqlb,[company_id,user_id,details,admin_user_id,gmt_created])
            connmy.commit()
            print company_id
            #记录掉公海记录
            sqlc="select id from kh_autogonghai where company_id=%s"
            cursormy.execute(sqlc,[company_id])
            result = cursormy.fetchone()
            if not result:
                sqlb="insert into kh_autogonghai (company_id,user_id,day3,gmt_created) values(%s,%s,%s,%s)"
                cursormy.execute(sqlb,[company_id,user_id,1,gmt_created])
                connmy.commit()
            else:
                aid=result['id']
                sqlb="update kh_autogonghai set user_id=%s,day3=1,gmt_created=%s where id=%s"
                cursormy.execute(sqlb,[user_id,gmt_created,aid])
                connmy.commit()
            #删除个人库
            sqld="delete from kh_assign where company_id=%s and user_id=%s"
            cursormy.execute(sqld,[company_id,user_id])
            connmy.commit()
            updatemodifydata(company_id)

#30天未联系入公海
def drop_30daynocontact():
    sql="select b.user_id,a.company_id from kh_sales as a left join kh_assign as b on a.company_id=b.company_id left join user as c on b.user_id=c.id where DATEDIFF(CURDATE(),a.lastteltime)>30 and DATEDIFF(CURDATE(),b.gmt_created)>=4 and c.closeflag=0 and c.dropflag=1 and b.isnew=1"
    cursormy.execute(sql)
    resultall = cursormy.fetchall()
    for list in resultall:
        gmt_created=gmt_modified=datetime.datetime.now()
        company_id=list['company_id']
        user_id=list['user_id']
        sqla="select id from kh_assign where company_id=%s"
        cursormy.execute(sqla,[company_id])
        resulta = cursormy.fetchone()
        if resulta:
            #记录客户记录
            details="30天未联系掉公海"
            admin_user_id=0
            sqlb="insert into kh_log (company_id,user_id,details,admin_user_id,gmt_created) values(%s,%s,%s,%s,%s)"
            cursormy.execute(sqlb,[company_id,user_id,details,admin_user_id,gmt_created])
            connmy.commit()
            #记录掉公海记录
            print company_id
            sqlc="select id from kh_autogonghai where company_id=%s"
            cursormy.execute(sqlc,[company_id])
            result = cursormy.fetchone()
            if not result:
                sqlb="insert into kh_autogonghai (company_id,user_id,day30,gmt_created) values(%s,%s,%s,%s)"
                cursormy.execute(sqlb,[company_id,user_id,1,gmt_created])
                connmy.commit()
            else:
                aid=result['id']
                sqlb="update kh_autogonghai set user_id=%s,day30=1,gmt_created=%s where id=%s"
                cursormy.execute(sqlb,[user_id,gmt_created,aid])
                connmy.commit()
            #删除个人库
            sqld="delete from kh_assign where company_id=%s and user_id=%s"
            cursormy.execute(sqld,[company_id,user_id])
            connmy.commit()
            updatemodifydata(company_id)
#新签超过500客户掉公海
def limit500kh():
    sql="select id from user where closeflag=0 and dropflag=1"
    cursormy.execute(sql)
    resultall = cursormy.fetchall()
    for list in resultall:
        user_id=list['id']
        sqlc="select count(0) as count from kh_assign where user_id=%s"
        cursormy.execute(sqlc,[user_id])
        resultc = cursormy.fetchone()
        compcount=resultc['count']
        print compcount
        if compcount>500:
            print str(compcount-500)
            #多余客户掉公海
            sqlg="select b.user_id,b.company_id,d.lastteltime from kh_assign as b left join user as c on b.user_id=c.id left join kh_sales as d on d.company_id=b.company_id where c.id=%s and b.isnew=1 order by d.lastteltime asc limit 0,"+str(compcount-500)
            cursormy.execute(sqlg,[user_id])
            resultg = cursormy.fetchall()
            for list in resultg:
                print list['lastteltime']
                gmt_created=gmt_modified=datetime.datetime.now()
                company_id=list['company_id']
                user_id=list['user_id']
                sqla="select id from kh_assign where company_id=%s"
                cursormy.execute(sqla,[company_id])
                resulta = cursormy.fetchone()
                if resulta:
                    #记录客户记录
                    details="库容超500掉公海"
                    admin_user_id=0
                    sqlb="insert into kh_log (company_id,user_id,details,admin_user_id,gmt_created) values(%s,%s,%s,%s,%s)"
                    cursormy.execute(sqlb,[company_id,user_id,details,admin_user_id,gmt_created])
                    connmy.commit()
                    #记录掉公海记录
                    print company_id
                    sqlc="select id from kh_autogonghai where company_id=%s"
                    cursormy.execute(sqlc,[company_id])
                    result = cursormy.fetchone()
                    if not result:
                        sqlb="insert into kh_autogonghai (company_id,user_id,more500,gmt_created) values(%s,%s,%s,%s)"
                        cursormy.execute(sqlb,[company_id,user_id,1,gmt_created])
                        connmy.commit()
                    else:
                        aid=result['id']
                        sqlb="update kh_autogonghai set user_id=%s,more500=1,gmt_created=%s where id=%s"
                        cursormy.execute(sqlb,[user_id,gmt_created,aid])
                        connmy.commit()
                    #删除个人库
                    sqld="delete from kh_assign where company_id=%s and user_id=%s"
                    cursormy.execute(sqld,[company_id,user_id])
                    connmy.commit()
                    updatemodifydata(company_id)
        
def back170227():
    gmt_created=gmt_modified=datetime.datetime.now()
    clist=[{'vap_user_id': 0, 'user_id': 1527, 'company_id': 123559649}, {'vap_user_id': 0, 'user_id': 1480, 'company_id': 123559648}, {'vap_user_id': 0, 'user_id': 1413, 'company_id': 123559647}, {'vap_user_id': 0, 'user_id': 1328, 'company_id': 123559646}, {'vap_user_id': 0, 'user_id': 1308, 'company_id': 123559645}, {'vap_user_id': 0, 'user_id': 1041, 'company_id': 123559644}, {'vap_user_id': 0, 'user_id': 1035, 'company_id': 123559643}, {'vap_user_id': 0, 'user_id': 978, 'company_id': 123559642}, {'vap_user_id': 0, 'user_id': 709, 'company_id': 123559641}, {'vap_user_id': 0, 'user_id': 338, 'company_id': 123559640}, {'vap_user_id': 0, 'user_id': 47, 'company_id': 123559639}, {'vap_user_id': 0, 'user_id': 1630, 'company_id': 123559638}, {'vap_user_id': 0, 'user_id': 1624, 'company_id': 123559637}, {'vap_user_id': 0, 'user_id': 1622, 'company_id': 123559636}, {'vap_user_id': 0, 'user_id': 1620, 'company_id': 123559635}, {'vap_user_id': 0, 'user_id': 1618, 'company_id': 123559634}, {'vap_user_id': 0, 'user_id': 1599, 'company_id': 123559633}, {'vap_user_id': 0, 'user_id': 1595, 'company_id': 123559632}, {'vap_user_id': 0, 'user_id': 1594, 'company_id': 123559631}, {'vap_user_id': 0, 'user_id': 1579, 'company_id': 123559630}, {'vap_user_id': 0, 'user_id': 1577, 'company_id': 123559629}, {'vap_user_id': 0, 'user_id': 1559, 'company_id': 123559628}, {'vap_user_id': 0, 'user_id': 1535, 'company_id': 123559627}, {'vap_user_id': 0, 'user_id': 1527, 'company_id': 123559626}, {'vap_user_id': 0, 'user_id': 1480, 'company_id': 123559625}, {'vap_user_id': 0, 'user_id': 1413, 'company_id': 123559624}, {'vap_user_id': 0, 'user_id': 1328, 'company_id': 123559623}, {'vap_user_id': 0, 'user_id': 1308, 'company_id': 123559622}, {'vap_user_id': 0, 'user_id': 1041, 'company_id': 123559621}, {'vap_user_id': 0, 'user_id': 1035, 'company_id': 123559620}, {'vap_user_id': 0, 'user_id': 978, 'company_id': 123559619}, {'vap_user_id': 0, 'user_id': 709, 'company_id': 123559618}, {'vap_user_id': 0, 'user_id': 338, 'company_id': 123559617}, {'vap_user_id': 0, 'user_id': 47, 'company_id': 123559616}, {'vap_user_id': 0, 'user_id': 1630, 'company_id': 123559615}, {'vap_user_id': 0, 'user_id': 1624, 'company_id': 123559614}, {'vap_user_id': 0, 'user_id': 1622, 'company_id': 123559613}, {'vap_user_id': 0, 'user_id': 1620, 'company_id': 123559612}, {'vap_user_id': 0, 'user_id': 1618, 'company_id': 123559611}, {'vap_user_id': 0, 'user_id': 1599, 'company_id': 123559610}, {'vap_user_id': 0, 'user_id': 1595, 'company_id': 123559609}, {'vap_user_id': 0, 'user_id': 1594, 'company_id': 123559608}, {'vap_user_id': 0, 'user_id': 1579, 'company_id': 123559607}, {'vap_user_id': 0, 'user_id': 1577, 'company_id': 123559606}, {'vap_user_id': 0, 'user_id': 1559, 'company_id': 123559605}, {'vap_user_id': 0, 'user_id': 1535, 'company_id': 123559604}, {'vap_user_id': 0, 'user_id': 1527, 'company_id': 123559603}, {'vap_user_id': 0, 'user_id': 1480, 'company_id': 123559602}, {'vap_user_id': 0, 'user_id': 1413, 'company_id': 123559601}, {'vap_user_id': 0, 'user_id': 1328, 'company_id': 123559600}, {'vap_user_id': 0, 'user_id': 1308, 'company_id': 123559599}, {'vap_user_id': 0, 'user_id': 1041, 'company_id': 123559598}, {'vap_user_id': 0, 'user_id': 1035, 'company_id': 123559597}, {'vap_user_id': 0, 'user_id': 978, 'company_id': 123559596}, {'vap_user_id': 0, 'user_id': 709, 'company_id': 123559595}, {'vap_user_id': 0, 'user_id': 338, 'company_id': 123559594}, {'vap_user_id': 0, 'user_id': 47, 'company_id': 123559593}, {'vap_user_id': 0, 'user_id': 1630, 'company_id': 123559592}, {'vap_user_id': 0, 'user_id': 1624, 'company_id': 123559591}, {'vap_user_id': 0, 'user_id': 1622, 'company_id': 123559590}, {'vap_user_id': 0, 'user_id': 1620, 'company_id': 123559589}, {'vap_user_id': 0, 'user_id': 1618, 'company_id': 123559588}, {'vap_user_id': 0, 'user_id': 1599, 'company_id': 123559587}, {'vap_user_id': 0, 'user_id': 1595, 'company_id': 123559586}, {'vap_user_id': 0, 'user_id': 1594, 'company_id': 123559585}, {'vap_user_id': 0, 'user_id': 1579, 'company_id': 123559584}, {'vap_user_id': 0, 'user_id': 1577, 'company_id': 123559583}, {'vap_user_id': 0, 'user_id': 1559, 'company_id': 123559582}, {'vap_user_id': 0, 'user_id': 1535, 'company_id': 123559581}, {'vap_user_id': 0, 'user_id': 1527, 'company_id': 123559580}, {'vap_user_id': 0, 'user_id': 1480, 'company_id': 123559579}, {'vap_user_id': 0, 'user_id': 1413, 'company_id': 123559578}, {'vap_user_id': 0, 'user_id': 1328, 'company_id': 123559577}, {'vap_user_id': 0, 'user_id': 1308, 'company_id': 123559576}, {'vap_user_id': 0, 'user_id': 1041, 'company_id': 123559575}, {'vap_user_id': 0, 'user_id': 1035, 'company_id': 123559574}, {'vap_user_id': 0, 'user_id': 978, 'company_id': 123559573}, {'vap_user_id': 0, 'user_id': 709, 'company_id': 123559572}, {'vap_user_id': 0, 'user_id': 338, 'company_id': 123559571}, {'vap_user_id': 0, 'user_id': 47, 'company_id': 123559570}, {'vap_user_id': 0, 'user_id': 1630, 'company_id': 123559569}, {'vap_user_id': 0, 'user_id': 1624, 'company_id': 123559568}, {'vap_user_id': 0, 'user_id': 1622, 'company_id': 123559567}, {'vap_user_id': 0, 'user_id': 1620, 'company_id': 123559566}, {'vap_user_id': 0, 'user_id': 1618, 'company_id': 123559565}, {'vap_user_id': 0, 'user_id': 1599, 'company_id': 123559564}, {'vap_user_id': 0, 'user_id': 1595, 'company_id': 123559563}, {'vap_user_id': 0, 'user_id': 1594, 'company_id': 123559562}, {'vap_user_id': 0, 'user_id': 1579, 'company_id': 123559561}, {'vap_user_id': 0, 'user_id': 1577, 'company_id': 123559560}, {'vap_user_id': 0, 'user_id': 1559, 'company_id': 123559559}, {'vap_user_id': 0, 'user_id': 1535, 'company_id': 123559558}, {'vap_user_id': 0, 'user_id': 1527, 'company_id': 123559557}, {'vap_user_id': 0, 'user_id': 1480, 'company_id': 123559556}, {'vap_user_id': 0, 'user_id': 0, 'company_id': 123559555}, {'vap_user_id': 0, 'user_id': 1328, 'company_id': 123559554}, {'vap_user_id': 0, 'user_id': 1308, 'company_id': 123559553}, {'vap_user_id': 0, 'user_id': 1041, 'company_id': 123559552}, {'vap_user_id': 0, 'user_id': 1035, 'company_id': 123559551}, {'vap_user_id': 0, 'user_id': 978, 'company_id': 123559550}, {'vap_user_id': 0, 'user_id': 709, 'company_id': 123559549}, {'vap_user_id': 0, 'user_id': 338, 'company_id': 123559548}, {'vap_user_id': 0, 'user_id': 47, 'company_id': 123559547}, {'vap_user_id': 0, 'user_id': 1630, 'company_id': 123559546}, {'vap_user_id': 0, 'user_id': 1624, 'company_id': 123559545}, {'vap_user_id': 0, 'user_id': 1622, 'company_id': 123559544}, {'vap_user_id': 0, 'user_id': 1620, 'company_id': 123559543}, {'vap_user_id': 0, 'user_id': 1618, 'company_id': 123559542}, {'vap_user_id': 0, 'user_id': 1599, 'company_id': 123559540}, {'vap_user_id': 0, 'user_id': 1595, 'company_id': 123559539}, {'vap_user_id': 0, 'user_id': 0, 'company_id': 123559537}, {'vap_user_id': 0, 'user_id': 1579, 'company_id': 123559536}, {'vap_user_id': 0, 'user_id': 1577, 'company_id': 123559535}, {'vap_user_id': 0, 'user_id': 1559, 'company_id': 123559534}, {'vap_user_id': 0, 'user_id': 1535, 'company_id': 123559533}, {'vap_user_id': 0, 'user_id': 1527, 'company_id': 123559532}, {'vap_user_id': 0, 'user_id': 1480, 'company_id': 123559531}, {'vap_user_id': 0, 'user_id': 1413, 'company_id': 123559530}, {'vap_user_id': 0, 'user_id': 1328, 'company_id': 123559529}, {'vap_user_id': 0, 'user_id': 1308, 'company_id': 123559528}, {'vap_user_id': 0, 'user_id': 1041, 'company_id': 123559527}, {'vap_user_id': 0, 'user_id': 1035, 'company_id': 123559526}, {'vap_user_id': 0, 'user_id': 978, 'company_id': 123559525}, {'vap_user_id': 0, 'user_id': 709, 'company_id': 123559524}, {'vap_user_id': 0, 'user_id': 709, 'company_id': 123559523}, {'vap_user_id': 0, 'user_id': 338, 'company_id': 123559522}, {'vap_user_id': 0, 'user_id': 47, 'company_id': 123559521}, {'vap_user_id': 0, 'user_id': 1630, 'company_id': 123559520}, {'vap_user_id': 0, 'user_id': 1624, 'company_id': 123559519}, {'vap_user_id': 0, 'user_id': 1622, 'company_id': 123559518}, {'vap_user_id': 0, 'user_id': 1620, 'company_id': 123559517}, {'vap_user_id': 0, 'user_id': 1618, 'company_id': 123559516}, {'vap_user_id': 0, 'user_id': 1599, 'company_id': 123559515}, {'vap_user_id': 0, 'user_id': 1595, 'company_id': 123559514}, {'vap_user_id': 0, 'user_id': 1620, 'company_id': 123559513}, {'vap_user_id': 0, 'user_id': 1579, 'company_id': 123559512}, {'vap_user_id': 0, 'user_id': 1577, 'company_id': 123559511}, {'vap_user_id': 0, 'user_id': 1559, 'company_id': 123559510}, {'vap_user_id': 0, 'user_id': 1535, 'company_id': 123559509}, {'vap_user_id': 0, 'user_id': 1527, 'company_id': 123559508}, {'vap_user_id': 0, 'user_id': 1480, 'company_id': 123559507}, {'vap_user_id': 0, 'user_id': 0, 'company_id': 123559506}, {'vap_user_id': 0, 'user_id': 1328, 'company_id': 123559505}, {'vap_user_id': 0, 'user_id': 1308, 'company_id': 123559504}, {'vap_user_id': 0, 'user_id': 0, 'company_id': 123559503}, {'vap_user_id': 0, 'user_id': 1035, 'company_id': 123559502}, {'vap_user_id': 0, 'user_id': 978, 'company_id': 123559501}, {'vap_user_id': 0, 'user_id': 709, 'company_id': 123559500}, {'vap_user_id': 0, 'user_id': 1622, 'company_id': 123559499}, {'vap_user_id': 0, 'user_id': 47, 'company_id': 123559498}, {'vap_user_id': 0, 'user_id': 0, 'company_id': 123559497}, {'vap_user_id': 0, 'user_id': 1624, 'company_id': 123559496}, {'vap_user_id': 0, 'user_id': 1622, 'company_id': 123559495}, {'vap_user_id': 0, 'user_id': 1620, 'company_id': 123559494}, {'vap_user_id': 0, 'user_id': 0, 'company_id': 123559493}, {'vap_user_id': 0, 'user_id': 1599, 'company_id': 123559492}, {'vap_user_id': 0, 'user_id': 1595, 'company_id': 123559491}, {'vap_user_id': 0, 'user_id': 1594, 'company_id': 123559490}, {'vap_user_id': 0, 'user_id': 1579, 'company_id': 123559489}, {'vap_user_id': 0, 'user_id': 1577, 'company_id': 123559488}, {'vap_user_id': 0, 'user_id': 0, 'company_id': 123559487}, {'vap_user_id': 0, 'user_id': 1535, 'company_id': 123559486}, {'vap_user_id': 0, 'user_id': 1527, 'company_id': 123559485}, {'vap_user_id': 0, 'user_id': 0, 'company_id': 123559484}, {'vap_user_id': 0, 'user_id': 1413, 'company_id': 123559483}, {'vap_user_id': 0, 'user_id': 1328, 'company_id': 123559482}, {'vap_user_id': 0, 'user_id': 0, 'company_id': 123559481}, {'vap_user_id': 0, 'user_id': 1041, 'company_id': 123559480}, {'vap_user_id': 0, 'user_id': 1035, 'company_id': 123559479}, {'vap_user_id': 0, 'user_id': 978, 'company_id': 123559478}, {'vap_user_id': 0, 'user_id': 1620, 'company_id': 123559477}, {'vap_user_id': 0, 'user_id': 0, 'company_id': 123559476}, {'vap_user_id': 0, 'user_id': 47, 'company_id': 123559475}, {'vap_user_id': 0, 'user_id': 1630, 'company_id': 123559474}, {'vap_user_id': 0, 'user_id': 1624, 'company_id': 123559473}, {'vap_user_id': 0, 'user_id': 1622, 'company_id': 123559472}, {'vap_user_id': 0, 'user_id': 1620, 'company_id': 123559471}, {'vap_user_id': 0, 'user_id': 1618, 'company_id': 123559470}, {'vap_user_id': 0, 'user_id': 1599, 'company_id': 123559469}, {'vap_user_id': 0, 'user_id': 1595, 'company_id': 123559468}, {'vap_user_id': 0, 'user_id': 1594, 'company_id': 123559467}, {'vap_user_id': 0, 'user_id': 1579, 'company_id': 123559466}, {'vap_user_id': 0, 'user_id': 1577, 'company_id': 123559465}, {'vap_user_id': 0, 'user_id': 1559, 'company_id': 123559464}, {'vap_user_id': 0, 'user_id': 1535, 'company_id': 123559463}, {'vap_user_id': 0, 'user_id': 1527, 'company_id': 123559462}, {'vap_user_id': 0, 'user_id': 0, 'company_id': 123559461}, {'vap_user_id': 0, 'user_id': 1413, 'company_id': 123559460}, {'vap_user_id': 0, 'user_id': 1328, 'company_id': 123559459}, {'vap_user_id': 0, 'user_id': 0, 'company_id': 123559458}, {'vap_user_id': 0, 'user_id': 0, 'company_id': 123559457}, {'vap_user_id': 0, 'user_id': 1035, 'company_id': 123559456}, {'vap_user_id': 0, 'user_id': 978, 'company_id': 123559455}, {'vap_user_id': 0, 'user_id': 709, 'company_id': 123559454}, {'vap_user_id': 0, 'user_id': 1622, 'company_id': 123559453}, {'vap_user_id': 0, 'user_id': 47, 'company_id': 123559452}, {'vap_user_id': 0, 'user_id': 0, 'company_id': 123559451}, {'vap_user_id': 0, 'user_id': 1624, 'company_id': 123559450}, {'vap_user_id': 0, 'user_id': 1622, 'company_id': 123559449}, {'vap_user_id': 0, 'user_id': 1620, 'company_id': 123559448}, {'vap_user_id': 0, 'user_id': 0, 'company_id': 123559447}, {'vap_user_id': 0, 'user_id': 1599, 'company_id': 123559446}, {'vap_user_id': 0, 'user_id': 0, 'company_id': 123559445}, {'vap_user_id': 0, 'user_id': 1594, 'company_id': 123559444}, {'vap_user_id': 0, 'user_id': 0, 'company_id': 123559443}, {'vap_user_id': 0, 'user_id': 1577, 'company_id': 123559442}, {'vap_user_id': 0, 'user_id': 0, 'company_id': 123559441}, {'vap_user_id': 0, 'user_id': 1535, 'company_id': 123559440}, {'vap_user_id': 0, 'user_id': 1527, 'company_id': 123559439}, {'vap_user_id': 0, 'user_id': 1480, 'company_id': 123559438}, {'vap_user_id': 0, 'user_id': 1413, 'company_id': 123559437}, {'vap_user_id': 0, 'user_id': 1328, 'company_id': 123559436}, {'vap_user_id': 0, 'user_id': 0, 'company_id': 123559435}, {'vap_user_id': 0, 'user_id': 0, 'company_id': 123559434}, {'vap_user_id': 0, 'user_id': 1035, 'company_id': 123559433}, {'vap_user_id': 0, 'user_id': 978, 'company_id': 123559432}, {'vap_user_id': 0, 'user_id': 709, 'company_id': 123559431}, {'vap_user_id': 0, 'user_id': 1622, 'company_id': 123559430}, {'vap_user_id': 0, 'user_id': 47, 'company_id': 123559429}, {'vap_user_id': 0, 'user_id': 1630, 'company_id': 123559428}, {'vap_user_id': 0, 'user_id': 1620, 'company_id': 123559427}, {'vap_user_id': 0, 'user_id': 0, 'company_id': 123559426}, {'vap_user_id': 0, 'user_id': 0, 'company_id': 123559425}, {'vap_user_id': 0, 'user_id': 1618, 'company_id': 123559424}, {'vap_user_id': 0, 'user_id': 1609, 'company_id': 123559423}, {'vap_user_id': 0, 'user_id': 1595, 'company_id': 123559422}, {'vap_user_id': 0, 'user_id': 1594, 'company_id': 123559421}, {'vap_user_id': 0, 'user_id': 0, 'company_id': 123559420}, {'vap_user_id': 0, 'user_id': 1577, 'company_id': 123559419}, {'vap_user_id': 0, 'user_id': 1559, 'company_id': 123559418}, {'vap_user_id': 0, 'user_id': 1579, 'company_id': 123559417}, {'vap_user_id': 0, 'user_id': 0, 'company_id': 123559416}, {'vap_user_id': 0, 'user_id': 1527, 'company_id': 123559415}, {'vap_user_id': 0, 'user_id': 0, 'company_id': 123559414}, {'vap_user_id': 0, 'user_id': 0, 'company_id': 123559413}, {'vap_user_id': 0, 'user_id': 1328, 'company_id': 123559412}, {'vap_user_id': 0, 'user_id': 1308, 'company_id': 123559411}, {'vap_user_id': 0, 'user_id': 1041, 'company_id': 123559410}, {'vap_user_id': 0, 'user_id': 1035, 'company_id': 123559409}, {'vap_user_id': 0, 'user_id': 978, 'company_id': 123559408}, {'vap_user_id': 0, 'user_id': 0, 'company_id': 123559407}, {'vap_user_id': 0, 'user_id': 1622, 'company_id': 123559406}, {'vap_user_id': 0, 'user_id': 47, 'company_id': 123559405}, {'vap_user_id': 0, 'user_id': 0, 'company_id': 123559404}, {'vap_user_id': 0, 'user_id': 1624, 'company_id': 123559403}, {'vap_user_id': 0, 'user_id': 1622, 'company_id': 123559402}, {'vap_user_id': 0, 'user_id': 1620, 'company_id': 123559401}, {'vap_user_id': 0, 'user_id': 1618, 'company_id': 123559400}, {'vap_user_id': 0, 'user_id': 1599, 'company_id': 123559399}, {'vap_user_id': 0, 'user_id': 0, 'company_id': 123559398}, {'vap_user_id': 0, 'user_id': 1594, 'company_id': 123559397}, {'vap_user_id': 0, 'user_id': 0, 'company_id': 123559396}, {'vap_user_id': 0, 'user_id': 1577, 'company_id': 123559395}, {'vap_user_id': 0, 'user_id': 1559, 'company_id': 123559394}, {'vap_user_id': 0, 'user_id': 0, 'company_id': 123559393}, {'vap_user_id': 0, 'user_id': 1527, 'company_id': 123559392}, {'vap_user_id': 0, 'user_id': 1480, 'company_id': 123559391}, {'vap_user_id': 0, 'user_id': 0, 'company_id': 123559390}, {'vap_user_id': 0, 'user_id': 1328, 'company_id': 123559389}, {'vap_user_id': 0, 'user_id': 1308, 'company_id': 123559388}, {'vap_user_id': 0, 'user_id': 0, 'company_id': 123559387}, {'vap_user_id': 0, 'user_id': 1035, 'company_id': 123559386}, {'vap_user_id': 0, 'user_id': 978, 'company_id': 123559385}, {'vap_user_id': 0, 'user_id': 0, 'company_id': 123559384}, {'vap_user_id': 0, 'user_id': 1622, 'company_id': 123559383}, {'vap_user_id': 0, 'user_id': 47, 'company_id': 123559382}, {'vap_user_id': 0, 'user_id': 1630, 'company_id': 123559381}, {'vap_user_id': 0, 'user_id': 0, 'company_id': 123559380}, {'vap_user_id': 0, 'user_id': 0, 'company_id': 123559379}, {'vap_user_id': 0, 'user_id': 1620, 'company_id': 123559378}, {'vap_user_id': 0, 'user_id': 1618, 'company_id': 123559377}, {'vap_user_id': 0, 'user_id': 1599, 'company_id': 123559376}, {'vap_user_id': 0, 'user_id': 0, 'company_id': 123559375}, {'vap_user_id': 0, 'user_id': 1594, 'company_id': 123559374}, {'vap_user_id': 0, 'user_id': 0, 'company_id': 123559373}, {'vap_user_id': 0, 'user_id': 0, 'company_id': 123559372}, {'vap_user_id': 0, 'user_id': 709, 'company_id': 123559371}, {'vap_user_id': 0, 'user_id': 1620, 'company_id': 123559370}, {'vap_user_id': 0, 'user_id': 0, 'company_id': 123559369}, {'vap_user_id': 0, 'user_id': 1527, 'company_id': 123559368}, {'vap_user_id': 0, 'user_id': 0, 'company_id': 123559367}, {'vap_user_id': 0, 'user_id': 0, 'company_id': 123559366}, {'vap_user_id': 0, 'user_id': 1328, 'company_id': 123559365}, {'vap_user_id': 0, 'user_id': 1308, 'company_id': 123559364}, {'vap_user_id': 0, 'user_id': 0, 'company_id': 123559363}, {'vap_user_id': 0, 'user_id': 1035, 'company_id': 123559362}, {'vap_user_id': 0, 'user_id': 978, 'company_id': 123559361}, {'vap_user_id': 0, 'user_id': 0, 'company_id': 123559360}, {'vap_user_id': 0, 'user_id': 0, 'company_id': 123559359}, {'vap_user_id': 0, 'user_id': 47, 'company_id': 123559358}, {'vap_user_id': 0, 'user_id': 0, 'company_id': 123559357}, {'vap_user_id': 0, 'user_id': 0, 'company_id': 123559356}, {'vap_user_id': 0, 'user_id': 1622, 'company_id': 123559355}, {'vap_user_id': 0, 'user_id': 1620, 'company_id': 123559354}, {'vap_user_id': 0, 'user_id': 0, 'company_id': 123559353}, {'vap_user_id': 0, 'user_id': 0, 'company_id': 123559352}, {'vap_user_id': 0, 'user_id': 0, 'company_id': 123559351}, {'vap_user_id': 0, 'user_id': 1594, 'company_id': 123559350}, {'vap_user_id': 0, 'user_id': 1579, 'company_id': 123559349}, {'vap_user_id': 0, 'user_id': 0, 'company_id': 123559348}, {'vap_user_id': 0, 'user_id': 0, 'company_id': 123559347}, {'vap_user_id': 0, 'user_id': 1535, 'company_id': 123559346}, {'vap_user_id': 0, 'user_id': 1527, 'company_id': 123559345}, {'vap_user_id': 0, 'user_id': 1480, 'company_id': 123559344}, {'vap_user_id': 0, 'user_id': 0, 'company_id': 123559343}, {'vap_user_id': 0, 'user_id': 0, 'company_id': 123559342}, {'vap_user_id': 0, 'user_id': 1308, 'company_id': 123559341}, {'vap_user_id': 0, 'user_id': 1041, 'company_id': 123559340}, {'vap_user_id': 0, 'user_id': 1035, 'company_id': 123559339}, {'vap_user_id': 0, 'user_id': 978, 'company_id': 123559338}, {'vap_user_id': 0, 'user_id': 709, 'company_id': 123559337}, {'vap_user_id': 0, 'user_id': 1622, 'company_id': 123559336}, {'vap_user_id': 0, 'user_id': 47, 'company_id': 123559335}, {'vap_user_id': 0, 'user_id': 0, 'company_id': 123559334}, {'vap_user_id': 0, 'user_id': 0, 'company_id': 123559333}, {'vap_user_id': 0, 'user_id': 1620, 'company_id': 123559332}, {'vap_user_id': 0, 'user_id': 1618, 'company_id': 123559331}, {'vap_user_id': 0, 'user_id': 1599, 'company_id': 123559330}, {'vap_user_id': 0, 'user_id': 0, 'company_id': 123559329}, {'vap_user_id': 0, 'user_id': 1594, 'company_id': 123559328}, {'vap_user_id': 0, 'user_id': 1579, 'company_id': 123559327}, {'vap_user_id': 0, 'user_id': 1620, 'company_id': 123559326}, {'vap_user_id': 0, 'user_id': 0, 'company_id': 123559325}, {'vap_user_id': 0, 'user_id': 0, 'company_id': 123559324}, {'vap_user_id': 0, 'user_id': 1527, 'company_id': 123559323}, {'vap_user_id': 0, 'user_id': 1480, 'company_id': 123559322}, {'vap_user_id': 0, 'user_id': 0, 'company_id': 123559321}, {'vap_user_id': 0, 'user_id': 1328, 'company_id': 123559320}, {'vap_user_id': 0, 'user_id': 1308, 'company_id': 123559319}, {'vap_user_id': 0, 'user_id': 0, 'company_id': 123559318}, {'vap_user_id': 0, 'user_id': 1035, 'company_id': 123559317}, {'vap_user_id': 0, 'user_id': 978, 'company_id': 123559316}, {'vap_user_id': 0, 'user_id': 0, 'company_id': 123559315}, {'vap_user_id': 0, 'user_id': 338, 'company_id': 123559314}, {'vap_user_id': 0, 'user_id': 47, 'company_id': 123559313}, {'vap_user_id': 0, 'user_id': 1620, 'company_id': 123559311}, {'vap_user_id': 0, 'user_id': 1599, 'company_id': 123559309}, {'vap_user_id': 0, 'user_id': 0, 'company_id': 123559308}, {'vap_user_id': 0, 'user_id': 0, 'company_id': 123559307}, {'vap_user_id': 0, 'user_id': 1579, 'company_id': 123559306}, {'vap_user_id': 0, 'user_id': 1577, 'company_id': 123559305}, {'vap_user_id': 0, 'user_id': 0, 'company_id': 123559303}, {'vap_user_id': 0, 'user_id': 1527, 'company_id': 123559302}, {'vap_user_id': 0, 'user_id': 1413, 'company_id': 123559300}, {'vap_user_id': 0, 'user_id': 0, 'company_id': 123559299}, {'vap_user_id': 0, 'user_id': 1308, 'company_id': 123559298}, {'vap_user_id': 0, 'user_id': 0, 'company_id': 123559296}, {'vap_user_id': 0, 'user_id': 709, 'company_id': 123559294}, {'vap_user_id': 0, 'user_id': 1622, 'company_id': 123559293}, {'vap_user_id': 0, 'user_id': 0, 'company_id': 123559290}, {'vap_user_id': 0, 'user_id': 0, 'company_id': 123559289}, {'vap_user_id': 0, 'user_id': 1618, 'company_id': 123559287}, {'vap_user_id': 0, 'user_id': 1599, 'company_id': 123559286}, {'vap_user_id': 0, 'user_id': 1595, 'company_id': 123559285}, {'vap_user_id': 0, 'user_id': 0, 'company_id': 123559284}, {'vap_user_id': 0, 'user_id': 1579, 'company_id': 123559283}, {'vap_user_id': 0, 'user_id': 1559, 'company_id': 123559281}, {'vap_user_id': 0, 'user_id': 0, 'company_id': 123559280}, {'vap_user_id': 0, 'user_id': 0, 'company_id': 123559277}, {'vap_user_id': 0, 'user_id': 0, 'company_id': 123559276}, {'vap_user_id': 0, 'user_id': 0, 'company_id': 123559274}, {'vap_user_id': 0, 'user_id': 1035, 'company_id': 123559273}, {'vap_user_id': 0, 'user_id': 978, 'company_id': 123559272}, {'vap_user_id': 0, 'user_id': 0, 'company_id': 123559271}, {'vap_user_id': 0, 'user_id': 1622, 'company_id': 123559270}, {'vap_user_id': 0, 'user_id': 1630, 'company_id': 123559268}, {'vap_user_id': 0, 'user_id': 1624, 'company_id': 123559267}, {'vap_user_id': 0, 'user_id': 1618, 'company_id': 123559264}, {'vap_user_id': 0, 'user_id': 1599, 'company_id': 123559263}, {'vap_user_id': 0, 'user_id': 0, 'company_id': 123559262}, {'vap_user_id': 0, 'user_id': 0, 'company_id': 123559260}, {'vap_user_id': 0, 'user_id': 0, 'company_id': 123559258}, {'vap_user_id': 0, 'user_id': 0, 'company_id': 123559257}, {'vap_user_id': 0, 'user_id': 0, 'company_id': 123559256}, {'vap_user_id': 0, 'user_id': 0, 'company_id': 123559255}, {'vap_user_id': 0, 'user_id': 0, 'company_id': 123559253}, {'vap_user_id': 0, 'user_id': 1041, 'company_id': 123559251}, {'vap_user_id': 0, 'user_id': 1035, 'company_id': 123559250}, {'vap_user_id': 0, 'user_id': 978, 'company_id': 123559249}, {'vap_user_id': 0, 'user_id': 0, 'company_id': 123559248}, {'vap_user_id': 0, 'user_id': 0, 'company_id': 123559247}, {'vap_user_id': 0, 'user_id': 0, 'company_id': 123559245}, {'vap_user_id': 0, 'user_id': 0, 'company_id': 123559244}, {'vap_user_id': 0, 'user_id': 0, 'company_id': 123559243}, {'vap_user_id': 0, 'user_id': 1618, 'company_id': 123559241}, {'vap_user_id': 0, 'user_id': 0, 'company_id': 123559240}, {'vap_user_id': 0, 'user_id': 1595, 'company_id': 123559239}, {'vap_user_id': 0, 'user_id': 0, 'company_id': 123559238}, {'vap_user_id': 0, 'user_id': 0, 'company_id': 123559237}, {'vap_user_id': 0, 'user_id': 0, 'company_id': 123559236}, {'vap_user_id': 0, 'user_id': 1559, 'company_id': 123559235}, {'vap_user_id': 0, 'user_id': 1535, 'company_id': 123559234}, {'vap_user_id': 0, 'user_id': 0, 'company_id': 123559232}, {'vap_user_id': 0, 'user_id': 1308, 'company_id': 123559229}, {'vap_user_id': 0, 'user_id': 0, 'company_id': 123559228}, {'vap_user_id': 0, 'user_id': 0, 'company_id': 123559227}, {'vap_user_id': 0, 'user_id': 978, 'company_id': 123559226}, {'vap_user_id': 0, 'user_id': 1622, 'company_id': 123559224}, {'vap_user_id': 0, 'user_id': 47, 'company_id': 123559223}, {'vap_user_id': 0, 'user_id': 0, 'company_id': 123559222}, {'vap_user_id': 0, 'user_id': 0, 'company_id': 123559221}, {'vap_user_id': 0, 'user_id': 1620, 'company_id': 123559219}, {'vap_user_id': 0, 'user_id': 1618, 'company_id': 123559218}, {'vap_user_id': 0, 'user_id': 1599, 'company_id': 123559217}, {'vap_user_id': 0, 'user_id': 1595, 'company_id': 123559216}, {'vap_user_id': 0, 'user_id': 1594, 'company_id': 123559215}, {'vap_user_id': 0, 'user_id': 0, 'company_id': 123559214}, {'vap_user_id': 0, 'user_id': 0, 'company_id': 123559213}, {'vap_user_id': 0, 'user_id': 0, 'company_id': 123559212}, {'vap_user_id': 0, 'user_id': 0, 'company_id': 123559211}, {'vap_user_id': 0, 'user_id': 0, 'company_id': 123559209}, {'vap_user_id': 0, 'user_id': 1413, 'company_id': 123559208}, {'vap_user_id': 0, 'user_id': 0, 'company_id': 123559207}, {'vap_user_id': 0, 'user_id': 1308, 'company_id': 123559206}, {'vap_user_id': 0, 'user_id': 1041, 'company_id': 123559205}, {'vap_user_id': 0, 'user_id': 0, 'company_id': 123559204}, {'vap_user_id': 0, 'user_id': 978, 'company_id': 123559203}, {'vap_user_id': 0, 'user_id': 0, 'company_id': 123559202}, {'vap_user_id': 0, 'user_id': 1622, 'company_id': 123559201}, {'vap_user_id': 0, 'user_id': 47, 'company_id': 123559200}, {'vap_user_id': 0, 'user_id': 0, 'company_id': 123559199}, {'vap_user_id': 0, 'user_id': 1622, 'company_id': 123559197}, {'vap_user_id': 0, 'user_id': 0, 'company_id': 123559196}, {'vap_user_id': 0, 'user_id': 1618, 'company_id': 123559195}, {'vap_user_id': 0, 'user_id': 1599, 'company_id': 123559194}, {'vap_user_id': 0, 'user_id': 1595, 'company_id': 123559193}, {'vap_user_id': 0, 'user_id': 0, 'company_id': 123559192}, {'vap_user_id': 0, 'user_id': 1579, 'company_id': 123559191}, {'vap_user_id': 0, 'user_id': 0, 'company_id': 123559190}, {'vap_user_id': 0, 'user_id': 0, 'company_id': 123559189}, {'vap_user_id': 0, 'user_id': 1535, 'company_id': 123559188}, {'vap_user_id': 0, 'user_id': 1480, 'company_id': 123559186}, {'vap_user_id': 0, 'user_id': 0, 'company_id': 123559185}, {'vap_user_id': 0, 'user_id': 0, 'company_id': 123559183}, {'vap_user_id': 0, 'user_id': 1035, 'company_id': 123559181}, {'vap_user_id': 0, 'user_id': 978, 'company_id': 123559180}, {'vap_user_id': 0, 'user_id': 0, 'company_id': 123559179}, {'vap_user_id': 0, 'user_id': 0, 'company_id': 123559178}, {'vap_user_id': 0, 'user_id': 1630, 'company_id': 123559176}, {'vap_user_id': 0, 'user_id': 1624, 'company_id': 123559175}, {'vap_user_id': 0, 'user_id': 1622, 'company_id': 123559174}, {'vap_user_id': 0, 'user_id': 1618, 'company_id': 123559172}, {'vap_user_id': 0, 'user_id': 0, 'company_id': 123559171}, {'vap_user_id': 0, 'user_id': 0, 'company_id': 123559170}, {'vap_user_id': 0, 'user_id': 0, 'company_id': 123559169}, {'vap_user_id': 0, 'user_id': 1579, 'company_id': 123559168}, {'vap_user_id': 0, 'user_id': 0, 'company_id': 123559166}, {'vap_user_id': 0, 'user_id': 1535, 'company_id': 123559165}, {'vap_user_id': 0, 'user_id': 1308, 'company_id': 123559160}, {'vap_user_id': 0, 'user_id': 0, 'company_id': 123559158}, {'vap_user_id': 0, 'user_id': 0, 'company_id': 123559156}, {'vap_user_id': 0, 'user_id': 0, 'company_id': 123559155}, {'vap_user_id': 0, 'user_id': 47, 'company_id': 123559154}, {'vap_user_id': 0, 'user_id': 0, 'company_id': 123559153}, {'vap_user_id': 0, 'user_id': 1624, 'company_id': 123559152}, {'vap_user_id': 0, 'user_id': 0, 'company_id': 123559151}, {'vap_user_id': 0, 'user_id': 0, 'company_id': 123559150}, {'vap_user_id': 0, 'user_id': 1599, 'company_id': 123559148}, {'vap_user_id': 0, 'user_id': 0, 'company_id': 123559147}, {'vap_user_id': 0, 'user_id': 0, 'company_id': 123559145}, {'vap_user_id': 0, 'user_id': 1577, 'company_id': 123559144}, {'vap_user_id': 0, 'user_id': 0, 'company_id': 123559143}, {'vap_user_id': 0, 'user_id': 0, 'company_id': 123559142}, {'vap_user_id': 0, 'user_id': 0, 'company_id': 123559140}, {'vap_user_id': 0, 'user_id': 0, 'company_id': 123559138}, {'vap_user_id': 0, 'user_id': 0, 'company_id': 123559136}, {'vap_user_id': 0, 'user_id': 0, 'company_id': 123559134}, {'vap_user_id': 0, 'user_id': 0, 'company_id': 123559133}, {'vap_user_id': 0, 'user_id': 1622, 'company_id': 123559132}, {'vap_user_id': 0, 'user_id': 0, 'company_id': 123559130}, {'vap_user_id': 0, 'user_id': 1624, 'company_id': 123559129}, {'vap_user_id': 0, 'user_id': 1622, 'company_id': 123559128}, {'vap_user_id': 0, 'user_id': 1620, 'company_id': 123559127}, {'vap_user_id': 0, 'user_id': 1618, 'company_id': 123559126}, {'vap_user_id': 0, 'user_id': 1599, 'company_id': 123559125}, {'vap_user_id': 0, 'user_id': 1595, 'company_id': 123559124}, {'vap_user_id': 0, 'user_id': 0, 'company_id': 123559123}, {'vap_user_id': 0, 'user_id': 1579, 'company_id': 123559122}, {'vap_user_id': 0, 'user_id': 1559, 'company_id': 123559120}, {'vap_user_id': 0, 'user_id': 0, 'company_id': 123559119}, {'vap_user_id': 0, 'user_id': 1527, 'company_id': 123559118}, {'vap_user_id': 0, 'user_id': 1413, 'company_id': 123559116}, {'vap_user_id': 0, 'user_id': 0, 'company_id': 123559115}, {'vap_user_id': 0, 'user_id': 0, 'company_id': 123559114}, {'vap_user_id': 0, 'user_id': 0, 'company_id': 123559112}, {'vap_user_id': 0, 'user_id': 0, 'company_id': 123559111}, {'vap_user_id': 0, 'user_id': 0, 'company_id': 123559110}, {'vap_user_id': 0, 'user_id': 1622, 'company_id': 123559109}, {'vap_user_id': 0, 'user_id': 0, 'company_id': 123559107}, {'vap_user_id': 0, 'user_id': 1624, 'company_id': 123559106}, {'vap_user_id': 0, 'user_id': 0, 'company_id': 123559105}, {'vap_user_id': 0, 'user_id': 1620, 'company_id': 123559104}, {'vap_user_id': 0, 'user_id': 1618, 'company_id': 123559103}, {'vap_user_id': 0, 'user_id': 0, 'company_id': 123559102}, {'vap_user_id': 0, 'user_id': 0, 'company_id': 123559101}, {'vap_user_id': 0, 'user_id': 1594, 'company_id': 123559100}, {'vap_user_id': 0, 'user_id': 1579, 'company_id': 123559099}, {'vap_user_id': 0, 'user_id': 1577, 'company_id': 123559098}, {'vap_user_id': 0, 'user_id': 0, 'company_id': 123559097}, {'vap_user_id': 0, 'user_id': 1480, 'company_id': 123559094}, {'vap_user_id': 0, 'user_id': 0, 'company_id': 123559093}, {'vap_user_id': 0, 'user_id': 0, 'company_id': 123559092}, {'vap_user_id': 0, 'user_id': 0, 'company_id': 123559091}, {'vap_user_id': 0, 'user_id': 0, 'company_id': 123559090}, {'vap_user_id': 0, 'user_id': 0, 'company_id': 123559089}, {'vap_user_id': 0, 'user_id': 0, 'company_id': 123559088}, {'vap_user_id': 0, 'user_id': 0, 'company_id': 123559087}, {'vap_user_id': 0, 'user_id': 1622, 'company_id': 123559086}, {'vap_user_id': 0, 'user_id': 47, 'company_id': 123559085}, {'vap_user_id': 0, 'user_id': 0, 'company_id': 123559084}, {'vap_user_id': 0, 'user_id': 0, 'company_id': 123559083}, {'vap_user_id': 0, 'user_id': 1620, 'company_id': 123559081}, {'vap_user_id': 0, 'user_id': 1618, 'company_id': 123559080}, {'vap_user_id': 0, 'user_id': 0, 'company_id': 123559079}, {'vap_user_id': 0, 'user_id': 1595, 'company_id': 123559078}, {'vap_user_id': 0, 'user_id': 1594, 'company_id': 123559077}, {'vap_user_id': 0, 'user_id': 1579, 'company_id': 123559076}, {'vap_user_id': 0, 'user_id': 1577, 'company_id': 123559075}, {'vap_user_id': 0, 'user_id': 0, 'company_id': 123559071}, {'vap_user_id': 0, 'user_id': 1413, 'company_id': 123559070}, {'vap_user_id': 0, 'user_id': 0, 'company_id': 123559069}, {'vap_user_id': 0, 'user_id': 0, 'company_id': 123559068}, {'vap_user_id': 0, 'user_id': 0, 'company_id': 123559067}, {'vap_user_id': 0, 'user_id': 0, 'company_id': 123559066}, {'vap_user_id': 0, 'user_id': 978, 'company_id': 123559065}, {'vap_user_id': 0, 'user_id': 709, 'company_id': 123559064}, {'vap_user_id': 0, 'user_id': 1622, 'company_id': 123559063}, {'vap_user_id': 0, 'user_id': 0, 'company_id': 123559061}, {'vap_user_id': 0, 'user_id': 1622, 'company_id': 123559059}, {'vap_user_id': 0, 'user_id': 1618, 'company_id': 123559057}, {'vap_user_id': 0, 'user_id': 0, 'company_id': 123559056}, {'vap_user_id': 0, 'user_id': 1595, 'company_id': 123559055}, {'vap_user_id': 0, 'user_id': 0, 'company_id': 123559053}, {'vap_user_id': 0, 'user_id': 1559, 'company_id': 123559051}, {'vap_user_id': 0, 'user_id': 0, 'company_id': 123559050}, {'vap_user_id': 0, 'user_id': 0, 'company_id': 123559048}, {'vap_user_id': 0, 'user_id': 0, 'company_id': 123559047}, {'vap_user_id': 0, 'user_id': 1041, 'company_id': 123559044}, {'vap_user_id': 0, 'user_id': 0, 'company_id': 123559043}, {'vap_user_id': 0, 'user_id': 0, 'company_id': 123559042}, {'vap_user_id': 0, 'user_id': 709, 'company_id': 123559041}, {'vap_user_id': 0, 'user_id': 1622, 'company_id': 123559040}, {'vap_user_id': 0, 'user_id': 0, 'company_id': 123559038}, {'vap_user_id': 0, 'user_id': 0, 'company_id': 123559037}, {'vap_user_id': 0, 'user_id': 1624, 'company_id': 123559036}, {'vap_user_id': 0, 'user_id': 0, 'company_id': 123559035}, {'vap_user_id': 0, 'user_id': 0, 'company_id': 123559033}, {'vap_user_id': 0, 'user_id': 0, 'company_id': 123559032}, {'vap_user_id': 0, 'user_id': 0, 'company_id': 123559031}, {'vap_user_id': 0, 'user_id': 1579, 'company_id': 123559029}, {'vap_user_id': 0, 'user_id': 0, 'company_id': 123559027}, {'vap_user_id': 0, 'user_id': 0, 'company_id': 123559026}, {'vap_user_id': 0, 'user_id': 1480, 'company_id': 123559024}, {'vap_user_id': 0, 'user_id': 1413, 'company_id': 123559023}, {'vap_user_id': 0, 'user_id': 1328, 'company_id': 123559022}, {'vap_user_id': 0, 'user_id': 1308, 'company_id': 123559021}, {'vap_user_id': 0, 'user_id': 0, 'company_id': 123559020}, {'vap_user_id': 0, 'user_id': 709, 'company_id': 123559017}, {'vap_user_id': 0, 'user_id': 0, 'company_id': 123559016}, {'vap_user_id': 0, 'user_id': 47, 'company_id': 123559015}, {'vap_user_id': 0, 'user_id': 1624, 'company_id': 123559014}, {'vap_user_id': 0, 'user_id': 1620, 'company_id': 123559012}, {'vap_user_id': 0, 'user_id': 0, 'company_id': 123559010}, {'vap_user_id': 0, 'user_id': 0, 'company_id': 123559009}, {'vap_user_id': 0, 'user_id': 1594, 'company_id': 123559008}, {'vap_user_id': 0, 'user_id': 0, 'company_id': 123559007}, {'vap_user_id': 0, 'user_id': 1577, 'company_id': 123559006}, {'vap_user_id': 0, 'user_id': 1559, 'company_id': 123559005}, {'vap_user_id': 0, 'user_id': 0, 'company_id': 123559004}, {'vap_user_id': 0, 'user_id': 1527, 'company_id': 123559003}, {'vap_user_id': 0, 'user_id': 1480, 'company_id': 123559002}, {'vap_user_id': 0, 'user_id': 0, 'company_id': 123559000}, {'vap_user_id': 0, 'user_id': 1308, 'company_id': 123558999}, {'vap_user_id': 0, 'user_id': 0, 'company_id': 123558998}, {'vap_user_id': 0, 'user_id': 0, 'company_id': 123558997}, {'vap_user_id': 0, 'user_id': 0, 'company_id': 123558996}, {'vap_user_id': 0, 'user_id': 1622, 'company_id': 123558994}, {'vap_user_id': 0, 'user_id': 0, 'company_id': 123558992}, {'vap_user_id': 0, 'user_id': 1624, 'company_id': 123558991}, {'vap_user_id': 0, 'user_id': 0, 'company_id': 123558990}, {'vap_user_id': 0, 'user_id': 0, 'company_id': 123558988}, {'vap_user_id': 0, 'user_id': 0, 'company_id': 123558987}, {'vap_user_id': 0, 'user_id': 1595, 'company_id': 123558986}, {'vap_user_id': 0, 'user_id': 0, 'company_id': 123558985}, {'vap_user_id': 0, 'user_id': 1579, 'company_id': 123558984}, {'vap_user_id': 0, 'user_id': 1577, 'company_id': 123558983}, {'vap_user_id': 0, 'user_id': 0, 'company_id': 123558982}, {'vap_user_id': 0, 'user_id': 0, 'company_id': 123558981}, {'vap_user_id': 0, 'user_id': 0, 'company_id': 123558980}, {'vap_user_id': 0, 'user_id': 0, 'company_id': 123558979}, {'vap_user_id': 0, 'user_id': 0, 'company_id': 123558978}, {'vap_user_id': 0, 'user_id': 1328, 'company_id': 123558977}, {'vap_user_id': 0, 'user_id': 1041, 'company_id': 123558975}, {'vap_user_id': 0, 'user_id': 1035, 'company_id': 123558974}, {'vap_user_id': 0, 'user_id': 978, 'company_id': 123558973}, {'vap_user_id': 0, 'user_id': 0, 'company_id': 123558972}, {'vap_user_id': 0, 'user_id': 1622, 'company_id': 123558971}, {'vap_user_id': 0, 'user_id': 0, 'company_id': 123558969}, {'vap_user_id': 0, 'user_id': 0, 'company_id': 123558968}, {'vap_user_id': 0, 'user_id': 1620, 'company_id': 123558966}, {'vap_user_id': 0, 'user_id': 1618, 'company_id': 123558965}, {'vap_user_id': 0, 'user_id': 1599, 'company_id': 123558964}, {'vap_user_id': 0, 'user_id': 1595, 'company_id': 123558963}, {'vap_user_id': 0, 'user_id': 1594, 'company_id': 123558962}, {'vap_user_id': 0, 'user_id': 0, 'company_id': 123558961}, {'vap_user_id': 0, 'user_id': 1577, 'company_id': 123558960}, {'vap_user_id': 0, 'user_id': 1559, 'company_id': 123558959}, {'vap_user_id': 0, 'user_id': 0, 'company_id': 123558958}, {'vap_user_id': 0, 'user_id': 1527, 'company_id': 123558957}, {'vap_user_id': 0, 'user_id': 1480, 'company_id': 123558956}, {'vap_user_id': 0, 'user_id': 0, 'company_id': 123558955}, {'vap_user_id': 0, 'user_id': 0, 'company_id': 123558953}, {'vap_user_id': 0, 'user_id': 0, 'company_id': 123558952}, {'vap_user_id': 0, 'user_id': 0, 'company_id': 123558951}, {'vap_user_id': 0, 'user_id': 0, 'company_id': 123558950}, {'vap_user_id': 0, 'user_id': 0, 'company_id': 123558949}, {'vap_user_id': 0, 'user_id': 1622, 'company_id': 123558948}, {'vap_user_id': 0, 'user_id': 47, 'company_id': 123558947}, {'vap_user_id': 0, 'user_id': 1624, 'company_id': 123558945}, {'vap_user_id': 0, 'user_id': 0, 'company_id': 123558944}, {'vap_user_id': 0, 'user_id': 0, 'company_id': 123558941}, {'vap_user_id': 0, 'user_id': 1595, 'company_id': 123558940}, {'vap_user_id': 0, 'user_id': 1594, 'company_id': 123558939}, {'vap_user_id': 0, 'user_id': 0, 'company_id': 123558938}, {'vap_user_id': 0, 'user_id': 1577, 'company_id': 123558937}, {'vap_user_id': 0, 'user_id': 0, 'company_id': 123558936}, {'vap_user_id': 0, 'user_id': 0, 'company_id': 123558935}, {'vap_user_id': 0, 'user_id': 1527, 'company_id': 123558934}, {'vap_user_id': 0, 'user_id': 0, 'company_id': 123558933}, {'vap_user_id': 0, 'user_id': 1413, 'company_id': 123558932}, {'vap_user_id': 0, 'user_id': 0, 'company_id': 123558930}, {'vap_user_id': 0, 'user_id': 0, 'company_id': 123558929}, {'vap_user_id': 0, 'user_id': 0, 'company_id': 123558928}, {'vap_user_id': 0, 'user_id': 0, 'company_id': 123558927}, {'vap_user_id': 0, 'user_id': 709, 'company_id': 123558926}, {'vap_user_id': 0, 'user_id': 0, 'company_id': 123558925}, {'vap_user_id': 0, 'user_id': 47, 'company_id': 123558924}, {'vap_user_id': 0, 'user_id': 0, 'company_id': 123558922}, {'vap_user_id': 0, 'user_id': 1620, 'company_id': 123558919}, {'vap_user_id': 0, 'user_id': 0, 'company_id': 123558918}, {'vap_user_id': 0, 'user_id': 0, 'company_id': 123558917}, {'vap_user_id': 0, 'user_id': 0, 'company_id': 123558916}, {'vap_user_id': 0, 'user_id': 0, 'company_id': 123558914}, {'vap_user_id': 0, 'user_id': 1559, 'company_id': 123558912}, {'vap_user_id': 0, 'user_id': 0, 'company_id': 123558911}, {'vap_user_id': 0, 'user_id': 0, 'company_id': 123558909}, {'vap_user_id': 0, 'user_id': 1328, 'company_id': 123558907}, {'vap_user_id': 0, 'user_id': 0, 'company_id': 123558905}, {'vap_user_id': 0, 'user_id': 0, 'company_id': 123558904}, {'vap_user_id': 0, 'user_id': 0, 'company_id': 123558903}, {'vap_user_id': 0, 'user_id': 1622, 'company_id': 123558901}, {'vap_user_id': 0, 'user_id': 0, 'company_id': 123558899}, {'vap_user_id': 0, 'user_id': 1624, 'company_id': 123558898}, {'vap_user_id': 0, 'user_id': 0, 'company_id': 123558893}, {'vap_user_id': 0, 'user_id': 0, 'company_id': 123558891}, {'vap_user_id': 0, 'user_id': 0, 'company_id': 123558883}, {'vap_user_id': 0, 'user_id': 1041, 'company_id': 123558882}, {'vap_user_id': 0, 'user_id': 0, 'company_id': 123558881}, {'vap_user_id': 0, 'user_id': 0, 'company_id': 123558880}, {'vap_user_id': 0, 'user_id': 1622, 'company_id': 123558878}, {'vap_user_id': 0, 'user_id': 0, 'company_id': 123558875}, {'vap_user_id': 0, 'user_id': 0, 'company_id': 123558873}, {'vap_user_id': 0, 'user_id': 1618, 'company_id': 123558872}, {'vap_user_id': 0, 'user_id': 0, 'company_id': 123558870}, {'vap_user_id': 0, 'user_id': 0, 'company_id': 123558869}, {'vap_user_id': 0, 'user_id': 0, 'company_id': 123558868}, {'vap_user_id': 0, 'user_id': 1579, 'company_id': 123558867}, {'vap_user_id': 0, 'user_id': 1577, 'company_id': 123558866}, {'vap_user_id': 0, 'user_id': 1559, 'company_id': 123558865}, {'vap_user_id': 0, 'user_id': 1535, 'company_id': 123558864}, {'vap_user_id': 0, 'user_id': 0, 'company_id': 123558859}, {'vap_user_id': 0, 'user_id': 0, 'company_id': 123558858}, {'vap_user_id': 0, 'user_id': 0, 'company_id': 123558856}, {'vap_user_id': 0, 'user_id': 1622, 'company_id': 123558854}, {'vap_user_id': 0, 'user_id': 1624, 'company_id': 123558851}, {'vap_user_id': 0, 'user_id': 1620, 'company_id': 123558849}, {'vap_user_id': 0, 'user_id': 0, 'company_id': 123558846}, {'vap_user_id': 0, 'user_id': 1594, 'company_id': 123558845}, {'vap_user_id': 0, 'user_id': 0, 'company_id': 123558844}, {'vap_user_id': 0, 'user_id': 1527, 'company_id': 123558840}, {'vap_user_id': 0, 'user_id': 0, 'company_id': 123558836}, {'vap_user_id': 0, 'user_id': 0, 'company_id': 123558834}, {'vap_user_id': 0, 'user_id': 0, 'company_id': 123558833}, {'vap_user_id': 0, 'user_id': 1622, 'company_id': 123558831}, {'vap_user_id': 0, 'user_id': 0, 'company_id': 123558824}, {'vap_user_id': 0, 'user_id': 0, 'company_id': 123558823}, {'vap_user_id': 0, 'user_id': 0, 'company_id': 123558813}, {'vap_user_id': 0, 'user_id': 0, 'company_id': 123558812}, {'vap_user_id': 0, 'user_id': 0, 'company_id': 123558811}, {'vap_user_id': 0, 'user_id': 1622, 'company_id': 123558808}, {'vap_user_id': 0, 'user_id': 1624, 'company_id': 123558805}, {'vap_user_id': 0, 'user_id': 0, 'company_id': 123558800}, {'vap_user_id': 0, 'user_id': 1620, 'company_id': 123558794}, {'vap_user_id': 0, 'user_id': 1579, 'company_id': 123558792}, {'vap_user_id': 0, 'user_id': 0, 'company_id': 123558790}, {'vap_user_id': 0, 'user_id': 0, 'company_id': 123558787}, {'vap_user_id': 0, 'user_id': 1620, 'company_id': 123558786}, {'vap_user_id': 0, 'user_id': 1622, 'company_id': 123558785}, {'vap_user_id': 0, 'user_id': 1620, 'company_id': 123558780}, {'vap_user_id': 0, 'user_id': 1579, 'company_id': 123558775}, {'vap_user_id': 0, 'user_id': 1295, 'company_id': 123558772}, {'vap_user_id': 0, 'user_id': 0, 'company_id': 123558766}, {'vap_user_id': 0, 'user_id': 1041, 'company_id': 123558765}, {'vap_user_id': 0, 'user_id': 0, 'company_id': 123558763}, {'vap_user_id': 0, 'user_id': 1618, 'company_id': 123558757}, {'vap_user_id': 0, 'user_id': 1620, 'company_id': 123558754}, {'vap_user_id': 0, 'user_id': 0, 'company_id': 123558745}, {'vap_user_id': 0, 'user_id': 0, 'company_id': 123558744}, {'vap_user_id': 0, 'user_id': 0, 'company_id': 123558743}, {'vap_user_id': 0, 'user_id': 1622, 'company_id': 123558740}, {'vap_user_id': 0, 'user_id': 1620, 'company_id': 123558737}, {'vap_user_id': 0, 'user_id': 1595, 'company_id': 123558734}, {'vap_user_id': 0, 'user_id': 1413, 'company_id': 123558726}, {'vap_user_id': 0, 'user_id': 0, 'company_id': 123558724}, {'vap_user_id': 0, 'user_id': 1579, 'company_id': 123558723}, {'vap_user_id': 0, 'user_id': 1035, 'company_id': 123558722}, {'vap_user_id': 0, 'user_id': 1630, 'company_id': 123558717}, {'vap_user_id': 0, 'user_id': 1618, 'company_id': 123558715}, {'vap_user_id': 0, 'user_id': 1620, 'company_id': 123558706}, {'vap_user_id': 0, 'user_id': 1620, 'company_id': 123558705}, {'vap_user_id': 0, 'user_id': 0, 'company_id': 123558690}, {'vap_user_id': 0, 'user_id': 1622, 'company_id': 123558685}, {'vap_user_id': 0, 'user_id': 1620, 'company_id': 123558682}, {'vap_user_id': 0, 'user_id': 0, 'company_id': 123558681}, {'vap_user_id': 0, 'user_id': 0, 'company_id': 123558680}, {'vap_user_id': 0, 'user_id': 1559, 'company_id': 123558675}, {'vap_user_id': 0, 'user_id': 0, 'company_id': 123558671}, {'vap_user_id': 0, 'user_id': 0, 'company_id': 123558669}, {'vap_user_id': 0, 'user_id': 0, 'company_id': 123558668}, {'vap_user_id': 0, 'user_id': 1620, 'company_id': 123558661}, {'vap_user_id': 0, 'user_id': 1618, 'company_id': 123558660}, {'vap_user_id': 0, 'user_id': 1413, 'company_id': 123558656}, {'vap_user_id': 0, 'user_id': 1579, 'company_id': 123558655}, {'vap_user_id': 0, 'user_id': 1535, 'company_id': 123558652}, {'vap_user_id': 0, 'user_id': 0, 'company_id': 123558647}, {'vap_user_id': 0, 'user_id': 1041, 'company_id': 123558646}, {'vap_user_id': 0, 'user_id': 0, 'company_id': 123558638}, {'vap_user_id': 0, 'user_id': 1599, 'company_id': 123558637}, {'vap_user_id': 0, 'user_id': 1595, 'company_id': 123558636}, {'vap_user_id': 0, 'user_id': 1579, 'company_id': 123558634}, {'vap_user_id': 0, 'user_id': 0, 'company_id': 123558632}, {'vap_user_id': 0, 'user_id': 0, 'company_id': 123558626}, {'vap_user_id': 0, 'user_id': 1622, 'company_id': 123558621}, {'vap_user_id': 0, 'user_id': 1620, 'company_id': 123558618}, {'vap_user_id': 0, 'user_id': 1577, 'company_id': 123558612}, {'vap_user_id': 0, 'user_id': 1620, 'company_id': 123558611}, {'vap_user_id': 0, 'user_id': 1308, 'company_id': 123558608}, {'vap_user_id': 0, 'user_id': 1480, 'company_id': 123558607}, {'vap_user_id': 0, 'user_id': 1308, 'company_id': 123558606}, {'vap_user_id': 0, 'user_id': 1308, 'company_id': 123558603}, {'vap_user_id': 0, 'user_id': 1624, 'company_id': 123558602}, {'vap_user_id': 0, 'user_id': 0, 'company_id': 123558601}, {'vap_user_id': 0, 'user_id': 0, 'company_id': 123558594}, {'vap_user_id': 0, 'user_id': 1620, 'company_id': 123558593}, {'vap_user_id': 0, 'user_id': 1618, 'company_id': 123558592}, {'vap_user_id': 0, 'user_id': 0, 'company_id': 123558591}, {'vap_user_id': 0, 'user_id': 0, 'company_id': 123558579}, {'vap_user_id': 0, 'user_id': 338, 'company_id': 123558574}, {'vap_user_id': 0, 'user_id': 1595, 'company_id': 123558572}, {'vap_user_id': 0, 'user_id': 1620, 'company_id': 123558571}, {'vap_user_id': 0, 'user_id': 1599, 'company_id': 123558569}, {'vap_user_id': 0, 'user_id': 1328, 'company_id': 123558559}, {'vap_user_id': 0, 'user_id': 1620, 'company_id': 123558558}, {'vap_user_id': 0, 'user_id': 1620, 'company_id': 123558557}, {'vap_user_id': 0, 'user_id': 1620, 'company_id': 123558550}, {'vap_user_id': 0, 'user_id': 1599, 'company_id': 123558548}, {'vap_user_id': 0, 'user_id': 1620, 'company_id': 123558546}, {'vap_user_id': 0, 'user_id': 1620, 'company_id': 123558533}, {'vap_user_id': 0, 'user_id': 1620, 'company_id': 123558529}, {'vap_user_id': 0, 'user_id': 0, 'company_id': 123558528}, {'vap_user_id': 0, 'user_id': 0, 'company_id': 123558526}, {'vap_user_id': 0, 'user_id': 1620, 'company_id': 123558495}, {'vap_user_id': 0, 'user_id': 0, 'company_id': 123558494}, {'vap_user_id': 0, 'user_id': 1620, 'company_id': 123558487}, {'vap_user_id': 0, 'user_id': 1620, 'company_id': 123558472}, {'vap_user_id': 0, 'user_id': 1620, 'company_id': 123558470}, {'vap_user_id': 0, 'user_id': 1308, 'company_id': 123558462}, {'vap_user_id': 0, 'user_id': 1594, 'company_id': 123558461}, {'vap_user_id': 0, 'user_id': 0, 'company_id': 123558455}, {'vap_user_id': 0, 'user_id': 0, 'company_id': 123558452}, {'vap_user_id': 0, 'user_id': 1620, 'company_id': 123558451}, {'vap_user_id': 0, 'user_id': 1620, 'company_id': 123558447}, {'vap_user_id': 0, 'user_id': 1620, 'company_id': 123558436}, {'vap_user_id': 0, 'user_id': 0, 'company_id': 123558432}, {'vap_user_id': 0, 'user_id': 0, 'company_id': 123558430}, {'vap_user_id': 0, 'user_id': 0, 'company_id': 123558423}, {'vap_user_id': 0, 'user_id': 0, 'company_id': 123558412}, {'vap_user_id': 0, 'user_id': 1559, 'company_id': 123558405}, {'vap_user_id': 0, 'user_id': 1620, 'company_id': 123558369}, {'vap_user_id': 0, 'user_id': 0, 'company_id': 123558368}, {'vap_user_id': 0, 'user_id': 1595, 'company_id': 123558366}, {'vap_user_id': 0, 'user_id': 1527, 'company_id': 123558360}, {'vap_user_id': 0, 'user_id': 1595, 'company_id': 123558346}, {'vap_user_id': 0, 'user_id': 0, 'company_id': 123558335}, {'vap_user_id': 0, 'user_id': 1595, 'company_id': 123558326}, {'vap_user_id': 0, 'user_id': 1622, 'company_id': 123558311}, {'vap_user_id': 0, 'user_id': 1618, 'company_id': 123558308}, {'vap_user_id': 0, 'user_id': 0, 'company_id': 123558302}, {'vap_user_id': 0, 'user_id': 0, 'company_id': 123558296}, {'vap_user_id': 0, 'user_id': 1594, 'company_id': 123558265}, {'vap_user_id': 0, 'user_id': 1620, 'company_id': 123558261}, {'vap_user_id': 0, 'user_id': 1328, 'company_id': 123558257}, {'vap_user_id': 0, 'user_id': 0, 'company_id': 123558247}, {'vap_user_id': 0, 'user_id': 1328, 'company_id': 123558237}, {'vap_user_id': 0, 'user_id': 338, 'company_id': 123558231}, {'vap_user_id': 0, 'user_id': 1618, 'company_id': 123558228}, {'vap_user_id': 0, 'user_id': 1595, 'company_id': 123558226}, {'vap_user_id': 0, 'user_id': 1599, 'company_id': 123558187}, {'vap_user_id': 0, 'user_id': 0, 'company_id': 123558150}, {'vap_user_id': 0, 'user_id': 1618, 'company_id': 123558120}, {'vap_user_id': 0, 'user_id': 1041, 'company_id': 123558099}, {'vap_user_id': 0, 'user_id': 1618, 'company_id': 123558093}, {'vap_user_id': 0, 'user_id': 1413, 'company_id': 123558083}, {'vap_user_id': 0, 'user_id': 1618, 'company_id': 123558081}, {'vap_user_id': 0, 'user_id': 1618, 'company_id': 123558073}, {'vap_user_id': 0, 'user_id': 1480, 'company_id': 123558064}, {'vap_user_id': 0, 'user_id': 0, 'company_id': 123558044}, {'vap_user_id': 0, 'user_id': 0, 'company_id': 123558036}, {'vap_user_id': 0, 'user_id': 1559, 'company_id': 123558006}, {'vap_user_id': 0, 'user_id': 1577, 'company_id': 123557950}, {'vap_user_id': 0, 'user_id': 0, 'company_id': 123557943}, {'vap_user_id': 0, 'user_id': 47, 'company_id': 123557937}, {'vap_user_id': 0, 'user_id': 0, 'company_id': 123557933}, {'vap_user_id': 0, 'user_id': 1535, 'company_id': 123557929}, {'vap_user_id': 0, 'user_id': 1308, 'company_id': 123557865}, {'vap_user_id': 0, 'user_id': 978, 'company_id': 123557863}, {'vap_user_id': 0, 'user_id': 1559, 'company_id': 123557853}, {'vap_user_id': 0, 'user_id': 0, 'company_id': 123557848}, {'vap_user_id': 0, 'user_id': 0, 'company_id': 123557840}, {'vap_user_id': 0, 'user_id': 1579, 'company_id': 123557778}, {'vap_user_id': 0, 'user_id': 1527, 'company_id': 123557755}, {'vap_user_id': 0, 'user_id': 1527, 'company_id': 123557736}, {'vap_user_id': 0, 'user_id': 1480, 'company_id': 123557735}, {'vap_user_id': 0, 'user_id': 1413, 'company_id': 123557734}, {'vap_user_id': 0, 'user_id': 1618, 'company_id': 123557725}, {'vap_user_id': 0, 'user_id': 0, 'company_id': 123557714}, {'vap_user_id': 0, 'user_id': 0, 'company_id': 123557700}, {'vap_user_id': 0, 'user_id': 1413, 'company_id': 123557669}, {'vap_user_id': 0, 'user_id': 0, 'company_id': 123557647}, {'vap_user_id': 0, 'user_id': 1535, 'company_id': 123557627}, {'vap_user_id': 0, 'user_id': 1595, 'company_id': 123557619}, {'vap_user_id': 0, 'user_id': 1579, 'company_id': 123557598}, {'vap_user_id': 0, 'user_id': 1595, 'company_id': 123557581}, {'vap_user_id': 0, 'user_id': 1413, 'company_id': 123557534}, {'vap_user_id': 0, 'user_id': 0, 'company_id': 123557533}, {'vap_user_id': 0, 'user_id': 709, 'company_id': 123557528}, {'vap_user_id': 0, 'user_id': 1577, 'company_id': 123557525}, {'vap_user_id': 0, 'user_id': 1034, 'company_id': 123557517}, {'vap_user_id': 0, 'user_id': 1618, 'company_id': 123557505}, {'vap_user_id': 0, 'user_id': 340, 'company_id': 123557492}, {'vap_user_id': 0, 'user_id': 1527, 'company_id': 123557477}, {'vap_user_id': 0, 'user_id': 1480, 'company_id': 123557476}, {'vap_user_id': 0, 'user_id': 1413, 'company_id': 123557475}, {'vap_user_id': 0, 'user_id': 1577, 'company_id': 123557436}, {'vap_user_id': 0, 'user_id': 1480, 'company_id': 123557419}, {'vap_user_id': 0, 'user_id': 0, 'company_id': 123557416}, {'vap_user_id': 0, 'user_id': 0, 'company_id': 123557413}, {'vap_user_id': 0, 'user_id': 0, 'company_id': 123557394}, {'vap_user_id': 0, 'user_id': 0, 'company_id': 123557390}, {'vap_user_id': 0, 'user_id': 1599, 'company_id': 123557389}, {'vap_user_id': 0, 'user_id': 1618, 'company_id': 123557379}, {'vap_user_id': 0, 'user_id': 1579, 'company_id': 123557377}, {'vap_user_id': 0, 'user_id': 0, 'company_id': 123557349}, {'vap_user_id': 0, 'user_id': 1577, 'company_id': 123557332}, {'vap_user_id': 0, 'user_id': 1595, 'company_id': 123557330}, {'vap_user_id': 0, 'user_id': 0, 'company_id': 123557319}, {'vap_user_id': 0, 'user_id': 0, 'company_id': 123557309}, {'vap_user_id': 0, 'user_id': 1618, 'company_id': 123557303}, {'vap_user_id': 0, 'user_id': 1599, 'company_id': 123557295}, {'vap_user_id': 0, 'user_id': 1618, 'company_id': 123557292}, {'vap_user_id': 0, 'user_id': 0, 'company_id': 123557273}, {'vap_user_id': 0, 'user_id': 0, 'company_id': 123557265}, {'vap_user_id': 0, 'user_id': 0, 'company_id': 123557264}, {'vap_user_id': 0, 'user_id': 1594, 'company_id': 123557262}, {'vap_user_id': 0, 'user_id': 1527, 'company_id': 123557257}, {'vap_user_id': 0, 'user_id': 1559, 'company_id': 123557220}, {'vap_user_id': 0, 'user_id': 0, 'company_id': 123557198}, {'vap_user_id': 0, 'user_id': 0, 'company_id': 123557185}, {'vap_user_id': 0, 'user_id': 0, 'company_id': 123557166}, {'vap_user_id': 0, 'user_id': 1480, 'company_id': 123557160}, {'vap_user_id': 0, 'user_id': 0, 'company_id': 123557141}, {'vap_user_id': 0, 'user_id': 1618, 'company_id': 123557139}, {'vap_user_id': 0, 'user_id': 0, 'company_id': 123557127}, {'vap_user_id': 0, 'user_id': 0, 'company_id': 123557117}, {'vap_user_id': 0, 'user_id': 1595, 'company_id': 123557109}, {'vap_user_id': 0, 'user_id': 1579, 'company_id': 123557107}, {'vap_user_id': 0, 'user_id': 1577, 'company_id': 123557087}, {'vap_user_id': 0, 'user_id': 1577, 'company_id': 123557055}, {'vap_user_id': 0, 'user_id': 1599, 'company_id': 123557053}, {'vap_user_id': 0, 'user_id': 0, 'company_id': 123557047}, {'vap_user_id': 0, 'user_id': 0, 'company_id': 123557023}, {'vap_user_id': 0, 'user_id': 0, 'company_id': 123557005}, {'vap_user_id': 0, 'user_id': 1579, 'company_id': 123557003}, {'vap_user_id': 0, 'user_id': 1618, 'company_id': 123556978}, {'vap_user_id': 0, 'user_id': 1599, 'company_id': 123556977}, {'vap_user_id': 0, 'user_id': 1595, 'company_id': 123556976}, {'vap_user_id': 0, 'user_id': 1620, 'company_id': 123556948}, {'vap_user_id': 0, 'user_id': 1599, 'company_id': 123556887}, {'vap_user_id': 0, 'user_id': 1595, 'company_id': 123556886}, {'vap_user_id': 0, 'user_id': 338, 'company_id': 123556871}, {'vap_user_id': 0, 'user_id': 1618, 'company_id': 123556869}, {'vap_user_id': 0, 'user_id': 1535, 'company_id': 123556843}, {'vap_user_id': 0, 'user_id': 1620, 'company_id': 123556824}, {'vap_user_id': 0, 'user_id': 0, 'company_id': 123556816}, {'vap_user_id': 0, 'user_id': 0, 'company_id': 123556784}, {'vap_user_id': 0, 'user_id': 1535, 'company_id': 123556766}, {'vap_user_id': 0, 'user_id': 1618, 'company_id': 123556762}, {'vap_user_id': 0, 'user_id': 1594, 'company_id': 123556751}, {'vap_user_id': 0, 'user_id': 1527, 'company_id': 123556746}, {'vap_user_id': 0, 'user_id': 0, 'company_id': 123556734}, {'vap_user_id': 0, 'user_id': 1594, 'company_id': 123556732}, {'vap_user_id': 0, 'user_id': 1577, 'company_id': 123556730}, {'vap_user_id': 0, 'user_id': 1480, 'company_id': 123556726}, {'vap_user_id': 0, 'user_id': 1618, 'company_id': 123556724}, {'vap_user_id': 0, 'user_id': 1413, 'company_id': 123556706}, {'vap_user_id': 0, 'user_id': 0, 'company_id': 123556704}, {'vap_user_id': 0, 'user_id': 1480, 'company_id': 123556688}, {'vap_user_id': 0, 'user_id': 338, 'company_id': 123556667}, {'vap_user_id': 0, 'user_id': 0, 'company_id': 123556658}, {'vap_user_id': 0, 'user_id': 0, 'company_id': 123556645}, {'vap_user_id': 0, 'user_id': 1599, 'company_id': 123556644}, {'vap_user_id': 0, 'user_id': 1480, 'company_id': 123556617}, {'vap_user_id': 0, 'user_id': 1579, 'company_id': 123556614}, {'vap_user_id': 0, 'user_id': 1594, 'company_id': 123556604}, {'vap_user_id': 0, 'user_id': 1579, 'company_id': 123556603}, {'vap_user_id': 0, 'user_id': 0, 'company_id': 123556602}, {'vap_user_id': 0, 'user_id': 709, 'company_id': 123556591}, {'vap_user_id': 0, 'user_id': 1535, 'company_id': 123556581}, {'vap_user_id': 0, 'user_id': 0, 'company_id': 123556554}, {'vap_user_id': 0, 'user_id': 1618, 'company_id': 123556550}, {'vap_user_id': 0, 'user_id': 1618, 'company_id': 123556531}, {'vap_user_id': 0, 'user_id': 1599, 'company_id': 123556530}, {'vap_user_id': 0, 'user_id': 0, 'company_id': 123556525}, {'vap_user_id': 0, 'user_id': 0, 'company_id': 123556517}, {'vap_user_id': 0, 'user_id': 1595, 'company_id': 123556510}, {'vap_user_id': 0, 'user_id': 1618, 'company_id': 123556474}, {'vap_user_id': 0, 'user_id': 1035, 'company_id': 123556470}, {'vap_user_id': 0, 'user_id': 1618, 'company_id': 123556434}, {'vap_user_id': 0, 'user_id': 1599, 'company_id': 123556403}, {'vap_user_id': 0, 'user_id': 1618, 'company_id': 123556366}, {'vap_user_id': 0, 'user_id': 1618, 'company_id': 123556358}, {'vap_user_id': 0, 'user_id': 1599, 'company_id': 123556357}, {'vap_user_id': 0, 'user_id': 1594, 'company_id': 123556355}, {'vap_user_id': 0, 'user_id': 1594, 'company_id': 123556347}, {'vap_user_id': 0, 'user_id': 1480, 'company_id': 123556341}, {'vap_user_id': 0, 'user_id': 0, 'company_id': 123556335}, {'vap_user_id': 0, 'user_id': 709, 'company_id': 123556307}, {'vap_user_id': 0, 'user_id': 1035, 'company_id': 123556290}, {'vap_user_id': 0, 'user_id': 1599, 'company_id': 123556284}, {'vap_user_id': 0, 'user_id': 1618, 'company_id': 123556266}, {'vap_user_id': 0, 'user_id': 1480, 'company_id': 123556181}, {'vap_user_id': 0, 'user_id': 1535, 'company_id': 123556159}, {'vap_user_id': 0, 'user_id': 0, 'company_id': 123556139}, {'vap_user_id': 0, 'user_id': 0, 'company_id': 123556136}, {'vap_user_id': 0, 'user_id': 1618, 'company_id': 123556132}, {'vap_user_id': 0, 'user_id': 0, 'company_id': 123556130}, {'vap_user_id': 0, 'user_id': 1618, 'company_id': 123556120}, {'vap_user_id': 0, 'user_id': 1535, 'company_id': 123556105}, {'vap_user_id': 0, 'user_id': 1618, 'company_id': 123556101}, {'vap_user_id': 0, 'user_id': 1035, 'company_id': 123556098}, {'vap_user_id': 0, 'user_id': 1579, 'company_id': 123556089}, {'vap_user_id': 0, 'user_id': 1577, 'company_id': 123556088}, {'vap_user_id': 0, 'user_id': 1413, 'company_id': 123556083}, {'vap_user_id': 0, 'user_id': 0, 'company_id': 123556062}, {'vap_user_id': 0, 'user_id': 1599, 'company_id': 123556054}, {'vap_user_id': 0, 'user_id': 1577, 'company_id': 123556050}, {'vap_user_id': 0, 'user_id': 1480, 'company_id': 123556027}, {'vap_user_id': 0, 'user_id': 1559, 'company_id': 123556011}, {'vap_user_id': 0, 'user_id': 0, 'company_id': 123555992}, {'vap_user_id': 0, 'user_id': 1328, 'company_id': 123555969}, {'vap_user_id': 0, 'user_id': 1594, 'company_id': 123555958}, {'vap_user_id': 0, 'user_id': 978, 'company_id': 123555946}, {'vap_user_id': 0, 'user_id': 1577, 'company_id': 123555937}, {'vap_user_id': 0, 'user_id': 1599, 'company_id': 123555862}, {'vap_user_id': 0, 'user_id': 1624, 'company_id': 123555775}, {'vap_user_id': 0, 'user_id': 1594, 'company_id': 123555764}, {'vap_user_id': 0, 'user_id': 1413, 'company_id': 123555757}, {'vap_user_id': 0, 'user_id': 0, 'company_id': 123555751}, {'vap_user_id': 0, 'user_id': 1624, 'company_id': 123555683}, {'vap_user_id': 0, 'user_id': 1308, 'company_id': 123555682}, {'vap_user_id': 0, 'user_id': 709, 'company_id': 123555678}, {'vap_user_id': 0, 'user_id': 1594, 'company_id': 123555614}, {'vap_user_id': 0, 'user_id': 1599, 'company_id': 123555599}, {'vap_user_id': 0, 'user_id': 1618, 'company_id': 123555566}, {'vap_user_id': 0, 'user_id': 1618, 'company_id': 123555557}, {'vap_user_id': 0, 'user_id': 1041, 'company_id': 123555555}, {'vap_user_id': 0, 'user_id': 1622, 'company_id': 123555550}, {'vap_user_id': 0, 'user_id': 338, 'company_id': 123555517}, {'vap_user_id': 0, 'user_id': 1599, 'company_id': 123555497}, {'vap_user_id': 0, 'user_id': 1618, 'company_id': 123555464}, {'vap_user_id': 0, 'user_id': 0, 'company_id': 123555447}, {'vap_user_id': 0, 'user_id': 1413, 'company_id': 123555422}, {'vap_user_id': 0, 'user_id': 1595, 'company_id': 123555377}, {'vap_user_id': 0, 'user_id': 1599, 'company_id': 123555360}, {'vap_user_id': 0, 'user_id': 338, 'company_id': 123555329}, {'vap_user_id': 0, 'user_id': 1413, 'company_id': 123555306}, {'vap_user_id': 0, 'user_id': 0, 'company_id': 123555243}, {'vap_user_id': 0, 'user_id': 1308, 'company_id': 123555236}, {'vap_user_id': 0, 'user_id': 1308, 'company_id': 123555199}, {'vap_user_id': 0, 'user_id': 1480, 'company_id': 123555151}]
    for d in clist:
        user_id=d['user_id']
        company_id=d['company_id']
        if user_id!=0:
            sqlc="select id from kh_assign where company_id=%s"
            cursormy.execute(sqlc,[company_id])
            result = cursormy.fetchone()
            if not result:
                sqlt="insert into kh_assign(company_id,user_id,gmt_created) values(%s,%s,%s)"
                cursormy.execute(sqlt,[company_id,user_id,gmt_created])
                connmy.commit()
                print "in"+str(company_id)
            else:
                sqlt="update kh_assign set user_id=%s where company_id=%s"
                cursormy.execute(sqlt,[user_id,company_id])
                connmy.commit()
                print "update"+str(company_id)
            updatemodifydata(company_id)
#更新钱包充值客户
def qianbaocompany():
    maxid=0
    sql="select maxid from update_log where utype='pay_mobilewallet'"
    cursormy.execute(sql)
    results = cursormy.fetchone()
    if results:
        maxid=results['maxid']
    sql="select id,company_id from pay_mobilewallet where ftype=5 and id>"+str(maxid)+" order by id asc"
    cursormy.execute(sql)
    resultall = cursormy.fetchall()
    if resultall:
        for list in resultall:
            gmt_created=gmt_modified=datetime.datetime.now()
            company_id=list['company_id']
            sqla="select id from kh_company_more where company_id=%s"
            cursormy.execute(sqla,[company_id])
            results = cursormy.fetchone()
            if not results:
                sqlb="insert into kh_company_more(company_id,isqianbao,iszhifu,gmt_created) values(%s,%s,%s,%s)"
                cursormy.execute(sqlb,[company_id,1,1,gmt_created])
                connmy.commit()
            print company_id
            maxid=list['id']
        sqlc="update update_log set maxid=%s where utype='pay_mobilewallet'"
        cursormy.execute(sqlc,[maxid])
        connmy.commit()
#更新支付记录
def payorderlist():
    maxid=0
    sql="select maxid from update_log where utype='pay_order'"
    cursormy.execute(sql)
    results = cursormy.fetchone()
    if results:
        maxid=results['maxid']
    sql="select id,company_id,is_success from pay_order where id>"+str(maxid)+" order by id asc"
    cursormy.execute(sql)
    resultall = cursormy.fetchall()
    if resultall:
        for list in resultall:
            gmt_created=gmt_modified=datetime.datetime.now()
            company_id=list['company_id']
            is_success=list['is_success']
            if company_id:
                iszhifu=0
                if is_success=="SUCCESS":
                    iszhifu=1
                sqla="select id from kh_company_more where company_id=%s"
                cursormy.execute(sqla,[company_id])
                results = cursormy.fetchone()
                if not results:
                    sqlb="insert into kh_company_more(company_id,isqianbao,iszhifu,gmt_created) values(%s,%s,%s,%s)"
                    cursormy.execute(sqlb,[company_id,1,iszhifu,gmt_created])
                    connmy.commit()
                else:
                    if (iszhifu==1):
                        sqlb="update kh_company_more set iszhifu=1 where id=%s"
                        cursormy.execute(sqlb,[results['id']])
                        connmy.commit()
                print company_id
                maxid=list['id']
        sqlc="update update_log set maxid=%s where utype='pay_order'"
        cursormy.execute(sqlc,[maxid])
        connmy.commit()
    
"""

old_to4star()
old_to5star()
old_vaptostar()
old_zstinfo()
old_assignicd()
old_assignvap()
old_comsales()
old_comsalesvap()
old_comtel()
old_assignHistory()
old_assignout()
old_crm_seotel()
old_salesincome()
old_isdeathcomp()
old_is4star()
old_is5star()
old_crm_InsertCompWeb()
old_lajicomp()
old_Crm_PersonInfo()
#old_huangye()
"""
