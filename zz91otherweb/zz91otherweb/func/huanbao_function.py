#-*- coding:utf-8 -*-
class huanbaodb:
    def __init__(self):
        from zz91conn import database_huanbao
        self.conn_huanbao=database_huanbao()
        self.cursor_huanbao=self.conn_huanbao.cursor()
    #----更新到数据库
    def updatetodb(self,sql,argument):
        self.cursor_huanbao.execute(sql,argument)
        self.conn_huanbao.commit()
    #----查询所有数据
    def fetchalldb(self,sql,argument=''):
        if argument:
            self.cursor_huanbao.execute(sql,argument)
        else:
            self.cursor_huanbao.execute(sql)
        resultlist=self.cursor_huanbao.fetchall()
        if resultlist:
            return resultlist
        else:
            return []
    #----查询一条数据
    def fetchonedb(self,sql,argument=''):
        if argument:
            self.cursor_huanbao.execute(sql,argument)
        else:
            self.cursor_huanbao.execute(sql)
        result=self.cursor_huanbao.fetchone()
        if result:
            return result
    #----查询一条总数
    def fetchnumberdb(self,sql,argument=''):
        if argument:
            self.cursor_huanbao.execute(sql,argument)
        else:
            self.cursor_huanbao.execute(sql)
        result=self.cursor_huanbao.fetchone()
        if result:
            return result[0]
        else:
            return 0

class zz91huanbao:
    def __init__(self):
        self.db_huanbao=huanbaodb()
    def gethuanbaodetail(self,id):
        sql='select id,title,details from news where id=%s'
        result=self.db_huanbao.fetchonedb(sql,[id])
        if result:
            id=result[0]
            title=result[1]
            details=result[2]
            list={'id':id,'title':title,'details':details}
            return list
    def getcategory_name(self,code):
        sql='select name from news_category where code=%s'
        result=self.db_huanbao.fetchonedb(sql,[code])
        if result:
            return result[0]
    def gethuanbaolist(self,frompageCount,limitNum,category_code=''):
        sql1='select count(0) from news where id>0'
        sql='select id,title,gmt_created,category_code from news where id>0'
        argument=[]
        if category_code:
            sql1=sql1+' and category_code=%s'
            sql=sql+' and category_code=%s'
            argument.append(category_code)
        sql=sql+' order by id desc'
        sql=sql+' limit '+str(frompageCount)+','+str(limitNum)
        count=self.db_huanbao.fetchnumberdb(sql1,argument)
        resultlist=self.db_huanbao.fetchalldb(sql,argument)
        listall=[]
        if resultlist:
            for result in resultlist:
                id=result[0]
                title=result[1]
                gmt_created=result[2]
                category_code=result[3]
                category_name=self.getcategory_name(category_code)
                list={'id':id,'title':title,'gmt_created':date_to_str(gmt_created),'category_code':category_code,'category_name':category_name}
                listall.append(list)
        return {'list':listall,'count':count}
    
    #环保一键删除
    def delallhuanbaolist(self,checkid):
        for id in checkid:
            sql="delete from news where id=%s"
            self.db_huanbao.updatetodb(sql,[id])
        return