#-*- coding:utf-8 -*-
class zpycms:
    def __init__(self):
        self.dbp=dbp
    def getuserlist(self,frompageCount,limitNum,sortrank):
        sql='select id,username,password,admin_id from py_user where sortrank=%s'
        sql+=' order by id desc limit '+str(frompageCount)+','+str(limitNum)
        sql1='select count(0) from py_user where sortrank=%s'
        count=self.dbp.fetchnumberdb(sql1,sortrank)
        resultlist=self.dbp.fetchalldb(sql,sortrank)
        listall=[]
        for result in resultlist:
            id=result[0]
            username=result[1]
            password=result[2]
            admin_id=result[3]
            admin_name=self.getadminname(admin_id)
            list={'id':id,'username':username,'password':password,'admin_id':admin_id,'admin_name':admin_name}
            listall.append(list)
        return {'list':listall,'count':count}
    def getadminname(self,id):
        sql='select username from py_user where id=%s'
        result=self.dbp.fetchonedb(sql,id)
        if result:
            return result[0]
    def getusertempdetail(self,id):
        sql='select name,pic,pinyin from py_template where id=%s'
        result=self.dbp.fetchonedb(sql,id)
        list={'name':'','pic':'','pinyin':''}
        if result:
            name=result[0]
            pic=result[1]
            pinyin=result[2]
            list={'name':name,'pic':pic,'pinyin':pinyin}
        return list
    def getusertemplist(self,frompageCount,limitNum):
        sql='select id,user_id,temp_id from py_user_template where id>0'
        sql+=' order by id desc limit '+str(frompageCount)+','+str(limitNum)
        sql1='select count(0) from py_user_template where id>0'
        count=self.dbp.fetchnumberdb(sql1)
        resultlist=self.dbp.fetchalldb(sql)
        listall=[]
        for result in resultlist:
            id=result[0]
            user_id=result[1]
            temp_id=result[2]
            usertempdetail=self.getusertempdetail(temp_id)
            temp_name=usertempdetail['name']
            temp_pic=usertempdetail['pic']
            temp_pinyin=usertempdetail['pinyin']
            list={'id':id,'user_id':user_id,'temp_id':temp_id,'temp_name':temp_name,'temp_pic':temp_pic,'temp_pinyin':temp_pinyin}
            listall.append(list)
        return {'list':listall,'count':count}
    def getusertypelist(self,frompageCount,limitNum):
        sql='select id,user_id,typename,pinyin,tempname from py_user_arttype1 where id>0'
        sql+=' order by id desc limit '+str(frompageCount)+','+str(limitNum)
        sql1='select count(0) from py_user_arttype1 where id>0'
        count=self.dbp.fetchnumberdb(sql1)
        resultlist=self.dbp.fetchalldb(sql)
        listall=[]
        for result in resultlist:
            id=result[0]
            user_id=result[1]
            typename=result[2]
            pinyin=result[3]
            tempname=result[4]
            list={'id':id,'user_id':user_id,'typename':typename,'pinyin':pinyin,'tempname':tempname}
            listall.append(list)
        return {'list':listall,'count':count}