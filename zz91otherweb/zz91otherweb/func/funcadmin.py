#-*- coding:utf-8 -*-
from time import strftime, localtime
from datetime import timedelta, date
import datetime
from symbol import argument
import xml.dom.minidom

def getadmintypelist():
    sql='select id,typename from webtype where wtype=9 order by sortrank,id'
    cursor.execute(sql)
    resultlist=cursor.fetchall()
    listall3=[]
    if resultlist:
        for result in resultlist:
            typeid=result[0]
            typename=result[1]
            sql2='select id,typename from webtype where reid=%s order by sortrank,id'
            cursor.execute(sql2,[typeid])
            resultlist2=cursor.fetchall()
            if resultlist2:
                listall2=[]
                for result2 in resultlist2:
                    typeid2=result2[0]
                    typename2=result2[1]
                    sql3='select id,name,url from website where typeid=%s and isdelete=0 order by sortrank,id'
                    cursor.execute(sql3,[typeid2])
                    resultlist3=cursor.fetchall()
                    if resultlist3:
                        listall=[]
                        for result3 in resultlist3:
                            list={'id':result3[0],'name':result3[1],'url':result3[2]}
                            listall.append(list)
                    list2={'typeid':typeid2,'typename':typename2,'website':listall}
                    listall2.append(list2)
            list3={'typeid':typeid,'typename':typename,'nextype':listall2}
            listall3.append(list3)
        return listall3


class zadmin():
    def __init__(self):
        self.dbc=dbc
    #文件上传
    def getseofilelist(self):
        sql="select id,filename,path,url,gmt_created,gmt_modify from seo_xmlfile where id>0 order by id desc"
        resultlist=self.dbc.fetchalldb(sql)
        listall=[]
        if resultlist:
            for result in resultlist:
                id=result[0]
                filename=result[1]
                path=result[2]
                url=result[3]
                gmt_created=formattime(result[4],0)
                gmt_modify=formattime(result[5],0)
                list={'id':id,'filename':filename,'path':path,'url':url,'gmt_created':gmt_created,'gmt_modify':gmt_modify}
                listall.append(list)
        return listall
    def getthisfilename(self,id):
        sql="select id,filename,path from seo_xmlfile where id=%s"
        result=self.dbc.fetchonedb(sql,[id])
        if result:
            id=result[0]
            filename=result[1]
            path=result[2]
            return{"id":id,"filename":filename,"path":path}
    def getcompanyname(self,company_id):
        sql="select name,is_block from company where id=%s"
        result=self.dbc.fetchonedb(sql,[company_id])
        if result:
            company_name=result[0]
            return {'name':company_name,'is_block':result[1]}
        else:
            return {'name':'','is_block':''}
    #敏感词
    def getminganglist(self,frompageCount='',limitNum=''):
        sqlc="select count(*) from company_block"
        resultc=self.dbc.fetchonedb(sqlc)
        listcount=resultc[0]
        sql='select id,company_id,keyv,burl,checked,gmt_created from company_block where company_id>0 order by id desc limit '+str(frompageCount)+','+str(limitNum)
        result=self.dbc.fetchalldb(sql)
        listall=[]
        if result:
            for list in result:
                compinfo=self.getcompanyname(list[1])
                companyname=compinfo['name']
                is_block=compinfo['is_block']
                gmt_created=formattime(list[5],0)
                if is_block=="1":
                    blockstats="黑名单"
                else:
                    blockstats=""
                l={'id':list[0],'company_id':list[1],'keyv':list[2],'burl':list[3],'checked':list[4],'companyname':companyname,'blockstats':blockstats,'gmt_created':gmt_created}
                listall.append(l)
        return {'list':listall,'count':listcount}
                    