#-*- coding:utf-8 -*-
import time,datetime
class zhelp:
    def __init__(self):
        self.dbh=dbh
        
    #所有栏目
    def getcolumn(self,pid=''):
        sqlarg=''
        ctype=0#父栏目为0.子栏目为1
        argument=[]
        if pid :
            sqlarg+=" where pid=%s"
            if int(pid)!=0:
                ctype=1
            argument.append(pid) 
        sql1='select count(0) from bz_category '+sqlarg
        sql='select cid,cat_name,pid from bz_category '+sqlarg
        
        count=self.dbh.fetchnumberdb(sql1,argument)
        resultlist=self.dbh.fetchalldb(sql,argument)
        listall=[]
        sonlist=[]
        has_son=0
        for result in resultlist:
            cid=result[0]
            cat_name=result[1]
            pid=result[2]
            sql_son_count='select count(0) from bz_category where pid=%s'
            son_count=self.dbh.fetchnumberdb(sql_son_count,[cid])
            if son_count>0:
                has_son=1
            else:
                has_son=0
            sql_son_list='select cid,cat_name,pid from bz_category where pid=%s'
            son_resultlist=self.dbh.fetchalldb(sql_son_list,[cid])
            if son_resultlist:
                for son_result in son_resultlist:
                    cid_son=son_result[0]
                    cat_name_son=son_result[1]
                    pid_son=son_result[2]
                    slist={'cid_son':cid_son,'cat_name_son':cat_name_son,'pid_son':pid_son}
                    sonlist.append(slist)
            list={'ctype':ctype,'cid':cid,'cat_name':cat_name,'pid':pid,'has_son':has_son,'son_count':son_count,'sonlist':sonlist}
            listall.append(list)
        return {'list':listall,'count':count}
    
    #所有列表内容
    def getarticallist(self,frompageCount,limitNum,subject='',typeid=''):
        sqlarg=''
        argument=[]
        if typeid:
            argument.append(typeid)
            sqlarg+='  and cat_id=%s'
        if subject:
            sqlarg+=' and subject like %s'
            argument.append('%'+subject+'%')
        sql1='select count(0) from bz_article where aid>0'+sqlarg
        sql='select aid,cat_id,subject,content,posttime from bz_article where aid>0'+sqlarg
        sql=sql+' order by aid desc limit '+str(frompageCount)+','+str(limitNum)
        count=self.dbh.fetchnumberdb(sql1,argument)
        resultlist=self.dbh.fetchalldb(sql,argument)
        listall=[]
        if resultlist:
            for result in resultlist:
                aid=result[0]
                cat_id=result[1]
                subject=result[2]
                content=result[3]
                posttime=result[4]
                ltime=time.localtime(posttime)
                gmt_modified=time.strftime("%Y-%m-%d %H:%M:%S", ltime)
                sql2='select cid,cat_name,pid from bz_category where cid=%s'
                s_result=self.dbh.fetchonedb(sql2,[cat_id])
                if s_result:
                    #cid=s_result[0]
                    s_cat_name=s_result[1]
                    pid=s_result[2]
                    sql3='select cat_name from bz_category where cid=%s'
                    f_result=self.dbh.fetchonedb(sql3,[pid])
                    f_cat_name=f_result[0]
                    list={'aid':aid,'cat_id':cat_id,'subject':subject,'content':content,'gmt_modified':gmt_modified,'s_cat_name':s_cat_name,'f_cat_name':f_cat_name}
                    listall.append(list)
        return {'list':listall,'count':count}
    
    #获得所有栏目
    def getcolumnlist(self):
        sql='select cid,cat_name,pid from bz_category where pid=0'
        resultlist=self.dbh.fetchalldb(sql)
        listall=[]
        if resultlist:
            for result in resultlist:
                cid=result[0]
                cat_name=result[1]
                pid=result[2]
                nextcolumn=self.getnextcolumn(cid)
                list={'cid':cid,'cat_name':cat_name,'pid':pid,'nextcolumn':nextcolumn}
                listall.append(list)
        return listall
    def getnextcolumn(self,reid):
        listall=[]
        sql='select cid,cat_name,pid from bz_category where pid=%s'
        resultlist=self.dbh.fetchalldb(sql,[reid])
        if resultlist:
            for result in resultlist:
                cid=result[0]
                cat_name=result[1]
                pid=result[2]
                list={'cid':cid,'cat_name':cat_name,'pid':pid}
                listall.append(list)
        return listall
    
    #根据id获得类别名称
    def getcatname(self,id):
        sql='select cat_name from bz_category where cid=%s'
        result=self.dbh.fetchonedb(sql,[id])
        return result[0]
    
    #获得帮助详细
    def gethelpdetail(self,aid):
        sql='select aid,cat_id,subject,content,posttime from bz_article where aid=%s'
        result=self.dbh.fetchonedb(sql,[aid])
        if result:
            aid=result[0]
            cat_id=result[1]
            subject=result[2]
            content=result[3]
            list={'aid':aid,'cat_id':cat_id,'subject':subject,'content':content}
            return list
    #更新    
    def updatehelpartical(self,cat_id,subject,content,aid):
        posttime=time.time()
        sql='update bz_article set cat_id=%s,subject=%s,content=%s,posttime=%s where aid=%s'
        self.dbh.updatetodb(sql,[cat_id,subject,content,posttime,aid])
    #增加   
    def addhelpartical(self,cat_id,subject,content):
        posttime=time.time()
        sql='insert into bz_article (cat_id,subject,content,posttime) values (%s,%s,%s,%s)'
        self.dbh.updatetodb(sql,[cat_id,subject,content,posttime])
    
        